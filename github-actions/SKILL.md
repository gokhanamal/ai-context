---
name: github-actions
description: This skill should be used when creating, editing, debugging, or reviewing GitHub Actions workflows and custom actions. Covers workflow syntax, triggers, jobs, matrix strategies, caching, secrets, security hardening, reusable workflows, composite/Docker/JavaScript actions, and deployment environments.
---

# GitHub Actions

Create, edit, debug, and optimize GitHub Actions workflows and custom actions.

## Trigger

Activate when working with:
- Files in `.github/workflows/` (workflow YAML files)
- Files named `action.yml` or `action.yaml` (custom action definitions)
- Any task involving CI/CD pipeline configuration for GitHub repositories
- Debugging failed workflow runs or action errors

## Workflow Fundamentals

### File Location
All workflow files must be in `.github/workflows/`. Subdirectories are not supported.

### Minimal Workflow Structure
```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello"
```

### Top-Level Keys
- `name` -- display name in Actions tab (optional)
- `run-name` -- names the run, supports `github` and `inputs` contexts (optional)
- `on` -- trigger event(s) (required)
- `permissions` -- GITHUB_TOKEN scopes
- `env` -- workflow-level environment variables
- `defaults.run` -- default `shell` and `working-directory` for `run` steps
- `concurrency` -- prevent duplicate runs
- `jobs` -- job definitions (required)

## Events and Triggers

### Common Trigger Patterns
```yaml
# Branch and path filtering
on:
  push:
    branches: [main, 'releases/**']
    paths: ['src/**']
    paths-ignore: ['docs/**']
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

# Scheduled (cron)
on:
  schedule:
    - cron: '30 5 * * 1-5'

# Manual dispatch with typed inputs
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]
        required: true
      dry_run:
        type: boolean
        default: false

# API-triggered
on:
  repository_dispatch:
    types: [deploy]

# Chain workflows
on:
  workflow_run:
    workflows: ["Build"]
    types: [completed]
    branches: [main]
```

### Input Types for `workflow_dispatch`
`boolean`, `choice`, `number`, `environment`, `string`. Max 25 inputs.

### Filter Pattern Syntax
- `*` matches any character except `/`
- `**` matches any character including `/`
- `!` negation (must follow a positive pattern)
- Cannot mix `branches` with `branches-ignore` -- use `!` negation instead

### Key `pull_request` Activity Types
`opened`, `synchronize`, `reopened`, `closed`, `ready_for_review`, `labeled`, `unlabeled`, `review_requested`, `converted_to_draft`

For a full event and activity type reference, consult `references/syntax-reference.md`.

## Jobs

### Job Configuration
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    needs: [lint, test]           # dependencies
    if: github.ref == 'refs/heads/main'
    timeout-minutes: 30           # default: 360
    continue-on-error: false
    permissions:
      contents: read
    environment:
      name: production
      url: https://myapp.example.com
    outputs:
      version: ${{ steps.ver.outputs.value }}
    env:
      NODE_ENV: production
    defaults:
      run:
        shell: bash
    steps:
      - uses: actions/checkout@v4
```

### Steps
```yaml
steps:
  - id: step1
    name: "Display Name"
    if: success()
    uses: actions/checkout@v4
    with:
      ref: main
    env:
      TOKEN: ${{ secrets.MY_TOKEN }}
    continue-on-error: true
    timeout-minutes: 10

  - name: Run commands
    run: |
      npm install
      npm test
    shell: bash
    working-directory: ./app
```

### Setting Outputs
```yaml
# Step output
- id: my_step
  run: echo "result=value" >> $GITHUB_OUTPUT

# Multiline output (use heredoc delimiters)
- run: |
    echo "json<<EOF" >> "$GITHUB_OUTPUT"
    cat result.json >> "$GITHUB_OUTPUT"
    echo "EOF" >> "$GITHUB_OUTPUT"

# Job output (declared at job level, references step)
jobs:
  build:
    outputs:
      artifact-id: ${{ steps.upload.outputs.id }}

# Consume in dependent job
  deploy:
    needs: build
    steps:
      - run: echo "${{ needs.build.outputs.artifact-id }}"
```

### Dynamic Environment Variables
```yaml
- run: echo "MY_VAR=hello" >> $GITHUB_ENV
- run: echo "$MY_VAR"    # available in subsequent steps
```

### Job Summaries
```yaml
- run: echo "### Build Results :rocket:" >> $GITHUB_STEP_SUMMARY
```

## Matrix Strategies

```yaml
strategy:
  fail-fast: false
  max-parallel: 4
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
    include:
      - os: ubuntu-latest
        node: 16
        experimental: true
    exclude:
      - os: macos-latest
        node: 18
runs-on: ${{ matrix.os }}
continue-on-error: ${{ matrix.experimental == true }}
```

### Dynamic Matrix from Job Output
```yaml
jobs:
  setup:
    outputs:
      matrix: ${{ steps.set.outputs.matrix }}
    steps:
      - id: set
        run: echo 'matrix=["a","b","c"]' >> "$GITHUB_OUTPUT"
  run:
    needs: setup
    strategy:
      matrix:
        value: ${{ fromJSON(needs.setup.outputs.matrix) }}
```

## Expressions and Contexts

### Status Check Functions (for `if:` conditionals)
- `success()` -- all previous steps succeeded (default)
- `failure()` -- any previous step failed
- `always()` -- runs even if cancelled
- `cancelled()` -- workflow was cancelled

Use `if: success() || failure()` to run on both outcomes but skip cancellation.

### Common Patterns
```yaml
if: github.ref == 'refs/heads/main'
if: github.event_name == 'pull_request'
if: contains(github.event.pull_request.labels.*.name, 'deploy')
if: startsWith(github.ref, 'refs/tags/')
if: always() && needs.build.result == 'success'

# Ternary-like
value: ${{ github.event_name == 'push' && 'production' || 'staging' }}
```

### Key Contexts
- `github.*` -- workflow run info (`ref`, `sha`, `actor`, `event`, `repository`, etc.)
- `env.*` -- environment variables
- `vars.*` -- configuration variables (repo/org/environment level)
- `secrets.*` -- secret values
- `steps.<id>.outputs.*` -- step outputs
- `needs.<job_id>.outputs.*` -- dependent job outputs
- `matrix.*` -- current matrix values
- `runner.*` -- runner info (`os`, `arch`, `temp`)
- `inputs.*` -- workflow_dispatch/workflow_call inputs

### Built-in Functions
- `contains(search, item)`, `startsWith()`, `endsWith()` -- case-insensitive
- `format('{0} {1}', val0, val1)` -- string formatting
- `join(array, separator)` -- default separator `,`
- `toJSON(value)`, `fromJSON(value)` -- JSON serialization
- `hashFiles(pattern)` -- SHA-256 of matching files
- `success()`, `failure()`, `always()`, `cancelled()` -- status checks

For complete context properties, consult `references/syntax-reference.md`.

## Permissions

```yaml
# Workflow-level (applies to all jobs by default)
permissions:
  contents: read
  pull-requests: write

# Job-level override
jobs:
  deploy:
    permissions:
      contents: read
      id-token: write

# Shorthand
permissions: read-all
permissions: {}    # disable all
```

Available scopes: `actions`, `attestations`, `checks`, `contents`, `deployments`, `discussions`, `id-token`, `issues`, `models`, `packages`, `pages`, `pull-requests`, `security-events`, `statuses`.

Access levels: `read`, `write`, `none`.

## Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# For PRs (fallback when github.head_ref is undefined)
concurrency:
  group: ${{ github.head_ref || github.run_id }}
  cancel-in-progress: true
```

Always include `github.workflow` in the group name to avoid cross-workflow cancellation.

## Caching

Prefer setup actions with built-in caching over raw `actions/cache`:
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm
```

Manual caching:
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

## Secrets

```yaml
# Use as environment variable (preferred -- avoids leaking via process args)
- env:
    API_KEY: ${{ secrets.API_KEY }}
  run: curl -H "Authorization: Bearer $API_KEY" https://api.example.com

# Pass as action input
- uses: some/action@v1
  with:
    token: ${{ secrets.MY_TOKEN }}
```

Key rules:
- Always pass secrets via `env:`, never interpolate directly in `run:` scripts
- Secrets cannot be used in `if:` conditionals -- set as env var first
- Secrets are not passed to workflows triggered from forks
- Secrets must be explicitly passed to reusable workflows (or use `secrets: inherit`)
- GITHUB_TOKEN is automatic and scoped to the repo

## Reusable Workflows

### Define (`workflow_call`)
```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true
    outputs:
      url:
        value: ${{ jobs.deploy.outputs.url }}
```

### Call
```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
    secrets:
      deploy_key: ${{ secrets.STAGING_KEY }}

  # Or pass all secrets
  deploy-alt:
    uses: org/repo/.github/workflows/deploy.yml@main
    secrets: inherit
```

Limitations: max 9 levels nesting, no loops, `uses` must be at job level (not in steps).

## Custom Actions

### Three Types

| Type | Platform | Speed | `runs.using` |
|------|----------|-------|--------------|
| Composite | All | Fast | `composite` |
| JavaScript | All | Fast | `node20` |
| Docker | Linux only | Slower | `docker` |

### Composite Action (`action.yml`)
```yaml
name: 'My Action'
description: 'Does something useful'
inputs:
  name:
    required: true
outputs:
  result:
    value: ${{ steps.run.outputs.result }}
runs:
  using: composite
  steps:
    - id: run
      run: echo "result=done" >> $GITHUB_OUTPUT
      shell: bash    # shell is MANDATORY on every run step
```

### Referencing Actions
```yaml
- uses: actions/checkout@8e5e7e5ab8b370d2c5cb812c4b306480e4a84920  # SHA (most secure)
- uses: actions/checkout@v4          # tag
- uses: ./.github/actions/my-action  # local
- uses: docker://alpine:3.18        # Docker image
```

## Deployment Environments

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://myapp.example.com
    runs-on: ubuntu-latest
```

Features (configured in repo Settings > Environments): required reviewers, wait timers, deployment branch restrictions, environment-scoped secrets and variables.

## Security Hardening

### Critical Rules
1. **Pin actions to full SHA** -- tags can be moved maliciously
2. **Use least-privilege permissions** -- start with `permissions: {}`, add back per-job
3. **Never interpolate untrusted input in `run:` scripts** -- use intermediate env vars

### Script Injection Prevention
```yaml
# VULNERABLE
- run: echo "Title: ${{ github.event.pull_request.title }}"

# SECURE
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $TITLE"
```

### Dangerous Contexts (always treat as untrusted)
`github.event.pull_request.title`, `github.event.pull_request.body`, `github.event.comment.body`, `github.event.issue.title`, `github.event.issue.body`, `github.head_ref`, `github.event.head_commit.message`

### Additional Security Measures
- Use OIDC for cloud auth instead of long-lived credentials
- Protect `.github/workflows/` with CODEOWNERS
- Enable Dependabot for action version updates
- Never use self-hosted runners for public repos
- Never store structured data (JSON/XML) as secrets -- redaction relies on exact string matching

## Using `gh` CLI in Workflows

GitHub CLI is pre-installed on all runners. Set `GH_TOKEN` for auth:
```yaml
- run: gh pr comment $PR --body "LGTM"
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    PR: ${{ github.event.pull_request.number }}
```

## References

For the complete syntax reference including all trigger events with activity types, all context properties, and detailed examples, consult `references/syntax-reference.md`.
