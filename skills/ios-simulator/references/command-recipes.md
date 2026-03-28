# iOS Simulator Command Recipes

Use these recipes when the `ios-simulator` skill needs exact `xcodebuildmcp` commands instead of higher-level guidance.

## Fast Local Helper

When this repository is available locally, prefer the bundled helper for visible taps before doing manual coordinate math.

Find likely matches:

```bash
python3 skills/ios-simulator/scripts/ui_helper.py \
  find \
  --simulator-id <SIMULATOR_ID> \
  --contains "Automatic only"
```

Tap a visible element and retry if the UI does not change:

```bash
python3 skills/ios-simulator/scripts/ui_helper.py \
  tap \
  --simulator-id <SIMULATOR_ID> \
  --label "Done" \
  --expect-change
```

Tap a substring match when the full label is long:

```bash
python3 skills/ios-simulator/scripts/ui_helper.py \
  tap \
  --simulator-id <SIMULATOR_ID> \
  --contains "BMW M3 Competition" \
  --expect-change
```

Use `--dry-run` to resolve the chosen target without tapping:

```bash
python3 skills/ios-simulator/scripts/ui_helper.py \
  tap \
  --simulator-id <SIMULATOR_ID> \
  --contains "Filters active" \
  --dry-run
```

## Project Discovery

Discover candidate projects from the current repo:

```bash
xcodebuildmcp project-discovery discover-projects --workspace-root "$(pwd)"
```

List schemes from a workspace:

```bash
xcodebuildmcp project-discovery list-schemes --workspace-path MyApp.xcworkspace
```

List schemes from a project:

```bash
xcodebuildmcp project-discovery list-schemes --project-path MyApp.xcodeproj
```

## Simulator List, Boot, And Open

List available simulators:

```bash
xcodebuildmcp simulator list
```

Boot a named simulator for a manual flow:

```bash
xcodebuildmcp simulator boot --simulator-name "iPhone 16"
```

Open Simulator.app:

```bash
xcodebuildmcp simulator open
```

## Build And Run

Build, install, and launch from a workspace:

```bash
xcodebuildmcp simulator build-and-run \
  --workspace-path MyApp.xcworkspace \
  --scheme MyApp \
  --simulator-name "iPhone 16" \
  --use-latest-os
```

Build, install, and launch from a project:

```bash
xcodebuildmcp simulator build-and-run \
  --project-path MyApp.xcodeproj \
  --scheme MyApp \
  --simulator-name "iPhone 16" \
  --use-latest-os
```

Launch an already built app when the bundle id is known:

```bash
xcodebuildmcp simulator launch-app \
  --simulator-name "iPhone 16" \
  --bundle-id com.example.myapp
```

## UI Snapshot And Interaction

Print the visible view hierarchy with coordinates:

```bash
xcodebuildmcp simulator snapshot-ui --simulator-id <SIMULATOR_ID>
```

Tap by accessibility label:

```bash
xcodebuildmcp ui-automation tap \
  --simulator-id <SIMULATOR_ID> \
  --label "Settings"
```

Tap by accessibility id:

```bash
xcodebuildmcp ui-automation tap \
  --simulator-id <SIMULATOR_ID> \
  --id profile-button
```

Coordinate fallback when the element is visible but not addressable by id or label:

```bash
xcodebuildmcp ui-automation tap \
  --simulator-id <SIMULATOR_ID> \
  -x 180 \
  -y 320
```

Type into the currently focused field:

```bash
xcodebuildmcp ui-automation type-text \
  --simulator-id <SIMULATOR_ID> \
  --text "test@example.com"
```

Use a preset scroll gesture:

```bash
xcodebuildmcp ui-automation gesture \
  --simulator-id <SIMULATOR_ID> \
  --preset scroll-down
```

Use a precise swipe when needed:

```bash
xcodebuildmcp ui-automation swipe \
  --simulator-id <SIMULATOR_ID> \
  --x1 200 \
  --y1 700 \
  --x2 200 \
  --y2 220
```

## Screenshots

Capture a screenshot and return a saved path:

```bash
xcodebuildmcp simulator screenshot \
  --simulator-id <SIMULATOR_ID> \
  --return-format path
```

Equivalent UI automation screenshot command:

```bash
xcodebuildmcp ui-automation screenshot \
  --simulator-id <SIMULATOR_ID> \
  --return-format path
```

## Bundle Id And Log Capture

Resolve the built app path:

```bash
xcodebuildmcp simulator get-app-path \
  --workspace-path MyApp.xcworkspace \
  --scheme MyApp \
  --platform "iOS Simulator" \
  --simulator-name "iPhone 16" \
  --use-latest-os
```

Extract the bundle id from the built app:

```bash
xcodebuildmcp project-discovery get-app-bundle-id --app-path /path/to/MyApp.app
```

Start simulator log capture:

```bash
xcodebuildmcp logging start-simulator-log-capture \
  --simulator-id <SIMULATOR_ID> \
  --bundle-id com.example.myapp \
  --capture-console
```

Stop log capture and return the logs:

```bash
xcodebuildmcp logging stop-simulator-log-capture --log-session-id <LOG_SESSION_ID>
```

## Common Recovery Steps

If project discovery is unclear:

```bash
xcodebuildmcp project-discovery discover-projects --workspace-root "$(pwd)"
```

If the scheme is unclear:

```bash
xcodebuildmcp project-discovery list-schemes --workspace-path MyApp.xcworkspace
```

If the simulator needs to be visible:

```bash
xcodebuildmcp simulator open
```

If the current screen may have changed after a tap:

```bash
xcodebuildmcp simulator snapshot-ui --simulator-id <SIMULATOR_ID>
```

If the bundle id is unknown:

```bash
xcodebuildmcp simulator get-app-path \
  --workspace-path MyApp.xcworkspace \
  --scheme MyApp \
  --platform "iOS Simulator" \
  --simulator-name "iPhone 16" \
  --use-latest-os
```

```bash
xcodebuildmcp project-discovery get-app-bundle-id --app-path /path/to/MyApp.app
```

If a label-based tap fails but the element is clearly visible:

```bash
xcodebuildmcp simulator snapshot-ui --simulator-id <SIMULATOR_ID>
```

```bash
xcodebuildmcp ui-automation tap --simulator-id <SIMULATOR_ID> -x 180 -y 320
```
