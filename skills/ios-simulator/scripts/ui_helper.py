#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SNAPSHOT_JSON_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)
INTERACTIVE_TYPES = {
    "Button",
    "CheckBox",
    "PopUpButton",
    "TextField",
    "SecureTextField",
}
INTERACTIVE_ROLES = {
    "AXButton",
    "AXCheckBox",
    "AXPopUpButton",
    "AXTextField",
}


@dataclass(frozen=True)
class Node:
    path: str
    node_type: str | None
    role: str | None
    subrole: str | None
    label: str | None
    unique_id: str | None
    value: str | None
    title: str | None
    enabled: bool
    frame_x: float
    frame_y: float
    frame_width: float
    frame_height: float

    @property
    def center_x(self) -> int:
        return round(self.frame_x + (self.frame_width / 2))

    @property
    def center_y(self) -> int:
        return round(self.frame_y + (self.frame_height / 2))

    @property
    def is_visible(self) -> bool:
        return self.frame_width > 0 and self.frame_height > 0

    @property
    def is_interactive(self) -> bool:
        return (self.node_type in INTERACTIVE_TYPES) or (self.role in INTERACTIVE_ROLES)

    @property
    def is_switch(self) -> bool:
        return self.subrole == "AXSwitch" or self.role == "AXCheckBox"

    def right_edge_point(self) -> tuple[int, int]:
        x = round(self.frame_x + max(self.frame_width - 20, self.frame_width * 0.82))
        y = self.center_y
        return (x, y)

    def description(self) -> str:
        parts = [
            f"path={self.path}",
            f"type={self.node_type or '-'}",
            f"role={self.role or '-'}",
            f"subrole={self.subrole or '-'}",
            f"label={self.label or '-'}",
            f"id={self.unique_id or '-'}",
            f"value={self.value or '-'}",
            f"center=({self.center_x}, {self.center_y})",
            (
                "frame=("
                f"{round(self.frame_x, 1)}, {round(self.frame_y, 1)}, "
                f"{round(self.frame_width, 1)}, {round(self.frame_height, 1)})"
            ),
        ]
        return ", ".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Find visible simulator UI elements from xcodebuildmcp snapshot-ui output "
            "and optionally tap them with retry fallback."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    find_parser = subparsers.add_parser("find", help="Find matching elements in the current UI snapshot.")
    add_shared_args(find_parser, needs_simulator=False)
    find_parser.add_argument("--limit", type=int, default=5, help="Maximum matches to print.")

    tap_parser = subparsers.add_parser("tap", help="Tap the best matching element.")
    add_shared_args(tap_parser, needs_simulator=True)
    tap_parser.add_argument(
        "--expect-change",
        action="store_true",
        help="Re-snapshot after tapping and retry if the UI did not change.",
    )
    tap_parser.add_argument(
        "--post-delay",
        type=float,
        default=0.6,
        help="Seconds to wait before checking for a changed snapshot after each attempt.",
    )
    tap_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve and print the chosen element without tapping.",
    )

    return parser.parse_args()


def add_shared_args(parser: argparse.ArgumentParser, *, needs_simulator: bool) -> None:
    parser.add_argument("--simulator-id", required=needs_simulator, help="Booted simulator UDID.")
    parser.add_argument(
        "--snapshot-file",
        help="Optional path to saved snapshot-ui JSON/text output for offline inspection.",
    )
    selector_group = parser.add_mutually_exclusive_group(required=True)
    selector_group.add_argument("--id", help="Exact accessibility id to match.")
    selector_group.add_argument("--label", help="Exact accessibility label to match.")
    selector_group.add_argument("--contains", help="Substring to match across label, id, value, or title.")
    parser.add_argument(
        "--index",
        type=int,
        default=0,
        help="Pick the Nth match after scoring and sorting. Defaults to the best match.",
    )


def run_command(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        message = stderr or stdout or "Unknown command failure"
        raise SystemExit(message)
    return result.stdout.strip()


def load_snapshot_text(simulator_id: str | None, snapshot_file: str | None) -> str:
    if snapshot_file:
        return Path(snapshot_file).read_text()
    if not simulator_id:
        raise SystemExit("--simulator-id is required when --snapshot-file is not provided")
    return run_command(
        [
            "xcodebuildmcp",
            "simulator",
            "snapshot-ui",
            "--simulator-id",
            simulator_id,
            "--output",
            "json",
        ]
    )


def extract_snapshot_tree(snapshot_text: str) -> list[dict[str, Any]]:
    stripped = snapshot_text.strip()
    if not stripped:
        raise SystemExit("snapshot-ui output was empty")

    if stripped.startswith("{"):
        outer = json.loads(stripped)
        for item in outer.get("content", []):
            if item.get("type") != "text":
                continue
            text = item.get("text", "")
            match = SNAPSHOT_JSON_RE.search(text)
            if match:
                return json.loads(match.group(1))
            text_stripped = text.strip()
            if text_stripped.startswith("["):
                return json.loads(text_stripped)
        raise SystemExit("Could not find snapshot JSON inside xcodebuildmcp output")

    match = SNAPSHOT_JSON_RE.search(stripped)
    if match:
        return json.loads(match.group(1))
    if stripped.startswith("["):
        return json.loads(stripped)
    raise SystemExit("Unsupported snapshot file format")


def flatten_nodes(tree: list[dict[str, Any]]) -> list[Node]:
    nodes: list[Node] = []

    def visit(node: dict[str, Any], path: str) -> None:
        frame = node.get("frame") or {}
        frame_x = float(frame.get("x", 0))
        frame_y = float(frame.get("y", 0))
        frame_width = float(frame.get("width", 0))
        frame_height = float(frame.get("height", 0))
        nodes.append(
            Node(
                path=path,
                node_type=node.get("type"),
                role=node.get("role"),
                subrole=node.get("subrole"),
                label=node.get("AXLabel"),
                unique_id=node.get("AXUniqueId"),
                value=_coerce_text(node.get("AXValue")),
                title=_coerce_text(node.get("title")),
                enabled=bool(node.get("enabled", True)),
                frame_x=frame_x,
                frame_y=frame_y,
                frame_width=frame_width,
                frame_height=frame_height,
            )
        )
        for index, child in enumerate(node.get("children") or []):
            visit(child, f"{path}.{index}")

    for root_index, root_node in enumerate(tree):
        visit(root_node, str(root_index))
    return nodes


def _coerce_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def normalize(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.casefold().split())


def score_node(node: Node, args: argparse.Namespace) -> int | None:
    if not node.is_visible or not node.enabled:
        return None

    score = 0
    if args.id:
        if node.unique_id == args.id:
            score = 1000
        else:
            return None
    elif args.label:
        if normalize(node.label) == normalize(args.label):
            score = 950
        else:
            return None
    elif args.contains:
        query = normalize(args.contains)
        fields = [
            normalize(node.unique_id),
            normalize(node.label),
            normalize(node.value),
            normalize(node.title),
        ]
        if not any(query in field for field in fields if field):
            return None
        if query == normalize(node.unique_id):
            score = 930
        elif query == normalize(node.label):
            score = 900
        elif query == normalize(node.value):
            score = 870
        elif query == normalize(node.title):
            score = 840
        elif query in normalize(node.unique_id):
            score = 810
        elif query in normalize(node.label):
            score = 780
        elif query in normalize(node.value):
            score = 750
        else:
            score = 720
    else:
        return None

    if node.is_interactive:
        score += 40
    if node.is_switch:
        score += 10
    if node.label:
        score += 5
    return score


def rank_matches(nodes: list[Node], args: argparse.Namespace) -> list[Node]:
    ranked: list[tuple[int, Node]] = []
    for node in nodes:
        score = score_node(node, args)
        if score is None:
            continue
        ranked.append((score, node))

    ranked.sort(
        key=lambda item: (
            -item[0],
            0 if item[1].is_interactive else 1,
            item[1].frame_y,
            item[1].frame_x,
        )
    )
    return [node for _, node in ranked]


def snapshot_fingerprint(tree: list[dict[str, Any]]) -> str:
    payload = json.dumps(tree, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def perform_tap(simulator_id: str, x: int, y: int) -> str:
    return run_command(
        [
            "xcodebuildmcp",
            "ui-automation",
            "tap",
            "--simulator-id",
            simulator_id,
            "-x",
            str(x),
            "-y",
            str(y),
        ]
    )


def perform_direct_tap(simulator_id: str, *, label: str | None = None, unique_id: str | None = None) -> str:
    command = ["xcodebuildmcp", "ui-automation", "tap", "--simulator-id", simulator_id]
    if unique_id:
        command.extend(["--id", unique_id])
    elif label:
        command.extend(["--label", label])
    else:
        raise ValueError("perform_direct_tap requires label or unique_id")
    return run_command(command)


def refresh_tree(simulator_id: str) -> tuple[list[dict[str, Any]], str]:
    tree = extract_snapshot_tree(load_snapshot_text(simulator_id, None))
    return tree, snapshot_fingerprint(tree)


def print_match_summary(node: Node, *, prefix: str = "Match") -> None:
    print(f"{prefix}: {node.description()}")


def handle_find(args: argparse.Namespace) -> int:
    tree = extract_snapshot_tree(load_snapshot_text(args.simulator_id, args.snapshot_file))
    matches = rank_matches(flatten_nodes(tree), args)
    if not matches:
        print("No matching visible elements found.", file=sys.stderr)
        return 1

    for index, node in enumerate(matches[: args.limit]):
        print_match_summary(node, prefix=f"Match {index}")
    return 0


def handle_tap(args: argparse.Namespace) -> int:
    initial_tree = extract_snapshot_tree(load_snapshot_text(args.simulator_id, args.snapshot_file))
    matches = rank_matches(flatten_nodes(initial_tree), args)
    if not matches:
        print("No matching visible elements found.", file=sys.stderr)
        return 1
    if args.index >= len(matches):
        print(
            f"Requested --index {args.index}, but only {len(matches)} matching elements were found.",
            file=sys.stderr,
        )
        return 1

    chosen = matches[args.index]
    print_match_summary(chosen, prefix="Chosen")
    if args.dry_run:
        return 0

    before_fingerprint = snapshot_fingerprint(initial_tree)
    attempts: list[tuple[str, tuple[int, int] | None]] = [("center", (chosen.center_x, chosen.center_y))]
    if chosen.is_switch:
        attempts.append(("switch-right-edge", chosen.right_edge_point()))
    if chosen.unique_id:
        attempts.append(("direct-id", None))
    if chosen.label:
        attempts.append(("direct-label", None))

    seen_attempts: set[tuple[str, tuple[int, int] | None]] = set()
    for attempt_name, point in attempts:
        if (attempt_name, point) in seen_attempts:
            continue
        seen_attempts.add((attempt_name, point))

        if point:
            print(f"Tap attempt '{attempt_name}' at ({point[0]}, {point[1]})")
            perform_tap(args.simulator_id, point[0], point[1])
        elif attempt_name == "direct-id":
            print(f"Tap attempt '{attempt_name}' with accessibility id {chosen.unique_id!r}")
            perform_direct_tap(args.simulator_id, unique_id=chosen.unique_id)
        elif attempt_name == "direct-label":
            print(f"Tap attempt '{attempt_name}' with label {chosen.label!r}")
            perform_direct_tap(args.simulator_id, label=chosen.label)

        if not args.expect_change:
            return 0

        time.sleep(args.post_delay)
        current_tree, current_fingerprint = refresh_tree(args.simulator_id)
        if current_fingerprint != before_fingerprint:
            print(f"UI changed after attempt '{attempt_name}'.")
            return 0
        print(f"UI did not change after attempt '{attempt_name}', retrying...")

    print("Tap completed, but no visible UI change was detected after all retries.", file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()
    if args.command == "find":
        return handle_find(args)
    if args.command == "tap":
        return handle_tap(args)
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
