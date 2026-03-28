# iOS Simulator

Human-facing overview for the `ios-simulator` skill.

## What It Does

This skill helps an agent drive an iOS Simulator from plain-language instructions.

It can:

- discover the Xcode project or workspace
- resolve schemes when needed
- open or boot the simulator
- build and launch the app
- inspect the visible UI hierarchy
- auto-resolve visible element centers with the bundled helper script
- tap, type, scroll, and swipe through the app
- capture screenshots and simulator logs

## When To Use It

Use this skill when you want an agent to:

- open Simulator and run the current app
- navigate to a specific screen in an iOS app
- interact with visible UI elements on a simulator
- collect screenshots or logs while reproducing a bug
- follow a short QA or repro flow written in natural language

## How It Helps

The skill keeps simulator automation structured and safe. It verifies that `xcodebuildmcp` is available, discovers the app setup only when needed, inspects the visible UI before interacting, prefers accessibility labels and ids over raw coordinates, and asks before risky actions that could change real data.

## Files

- `SKILL.md` - the agent-facing simulator workflow
- `scripts/ui_helper.py` - local helper that resolves visible elements from `snapshot-ui`, taps their centers, and retries fallbacks
- `references/command-recipes.md` - concrete `xcodebuildmcp` command patterns for discovery, launch, UI automation, screenshots, logs, and recovery
