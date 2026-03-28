---
name: ios-simulator
description: Drive an iOS Simulator from plain-language instructions by discovering the project, launching the app, inspecting the visible UI, and interacting with elements through xcodebuildmcp. Use when the user wants an agent to open Simulator, navigate screens, tap buttons, type into fields, scroll, or capture screenshots and logs.
argument-hint: "[task]"
disable-model-invocation: true
allowed-tools: "Read, Bash(xcodebuildmcp *), Bash(python3 skills/ios-simulator/scripts/ui_helper.py *), Bash(rg *), Bash(find *), Bash(ls *), Bash(pwd), Bash(test *), Bash(sed *)"
---

# iOS Simulator

Use this skill for the requested simulator task:

`$ARGUMENTS`

This is a manual workflow skill. Treat every simulator action as deliberate, verify progress after each step, and pause before risky side effects.

## Quick Start

1. Run `xcodebuildmcp --help` first.
2. If the CLI is missing, stop and provide setup help instead of improvising.
3. Discover the Xcode project or workspace only when the path is not already clear.
4. Resolve the scheme only when it is not obvious.
5. List, boot, or open the simulator only as needed.
6. Prefer `xcodebuildmcp simulator build-and-run` when the app needs to be launched.
7. Inspect the current screen with `snapshot-ui` before the first interaction and after every navigation-changing action.
8. In this repo, prefer `python3 skills/ios-simulator/scripts/ui_helper.py tap ...` for repeated tap flows so the helper can resolve centers and retry fallbacks automatically.
9. Prefer taps by accessibility `id` or `label`. Use coordinates only after a fresh UI snapshot confirms the target is visible.
10. Focus a field before using `type-text`.
11. Capture screenshots or logs when the user asks for proof or when debugging is needed.

## Workflow

### 1. Preflight

- Parse the task for four things:
  - what app or repo to run
  - which simulator, if any
  - which screen flow to follow
  - whether proof is required through screenshots or logs
- Run `xcodebuildmcp --help`.
- If it fails, stop and give short install guidance such as:
  - `brew tap getsentry/xcodebuildmcp`
  - `brew install xcodebuildmcp`
  - `npm install -g xcodebuildmcp@latest`

### 2. Discover The App

- If the repo does not clearly expose a single `.xcworkspace` or `.xcodeproj`, use `project-discovery discover-projects`.
- Prefer a workspace over a project when both exist for the same app.
- If the scheme is unknown, use `project-discovery list-schemes`.
- Ask the user only when there are multiple plausible app targets or schemes and the correct choice is not obvious.

### 3. Prepare The Simulator

- Use `simulator list` to find devices when the task names a preferred device or when you need a simulator id.
- Use `simulator boot` only for manual flows that need an already-booted device.
- Use `simulator open` when the Simulator app should be visible to the user.
- Do not boot a simulator just because you can. `simulator build-and-run` already handles booting when needed.

### 4. Launch The App

- Prefer `simulator build-and-run` for the common path.
- If the app is already built and only a relaunch is needed, use `simulator launch-app`.
- If the bundle id is unknown, resolve it with:
  1. `simulator get-app-path`
  2. `project-discovery get-app-bundle-id`

### 5. Navigate And Interact

- Call `simulator snapshot-ui` before the first tap, type, swipe, or scroll.
- If `skills/ios-simulator/scripts/ui_helper.py` is available, use it as the default fast path for taps on visible elements.
- Match the requested UI target using visible accessibility ids or labels first.
- After any action that could change layout or navigation, run `snapshot-ui` again before the next interaction.
- For navigation-changing or toggle actions, prefer helper invocations with `--expect-change` so failed taps retry automatically.
- For text entry:
  1. focus the field with a tap
  2. verify focus if the UI output changes
  3. use `ui-automation type-text`
- Prefer `ui-automation gesture` for common scrolling.
- Use `ui-automation swipe` only when a preset gesture is not precise enough.
- If an element is missing or not hittable:
  1. refresh the UI snapshot
  2. confirm the target is still expected on the current screen
  3. use coordinate fallback only when the element is visible and uniquely identified

### 6. Capture Proof And Recover

- Use `simulator screenshot` or `ui-automation screenshot` when the user asks for proof or when a failure needs visual confirmation.
- Use simulator log capture when a flow crashes, stalls, or needs console evidence.
- When the flow fails, summarize:
  - what step was attempted
  - what the latest UI snapshot showed
  - what recovery you tried
  - what still blocks progress

## Safety Rules

- Ask for confirmation before destructive or external actions, including delete, purchase, submit, sign-out, account changes, or anything that can alter real data or trigger network side effects.
- Do not erase simulators, reset location, clear app data, or change status bar state unless the user explicitly asks.
- Do not guess between multiple similarly named UI elements without confirming which one is intended.
- Do not use coordinate taps as the first choice when an accessibility id or label is available.
- Prefer explicit command flags over hidden profiles or session defaults unless the user specifically asks to rely on them.

## Examples

- `/ios-simulator Open the simulator, run the current app, go to Settings, and tap Profile`
- `/ios-simulator Launch the app on iPhone 16, finish onboarding, type test@example.com, and take a screenshot`
- `/ios-simulator Open Simulator, reproduce the crash after tapping Continue, and capture logs`

## Reference

For exact command patterns, helper usage, and recovery recipes, see [references/command-recipes.md](references/command-recipes.md).
