# GitHub Actions Complete Syntax Reference

## All Trigger Events with Activity Types

### Events with Activity Types

| Event | Activity Types |
|-------|---------------|
| `branch_protection_rule` | `created`, `edited`, `deleted` |
| `check_run` | `created`, `rerequested`, `completed`, `requested_action` |
| `check_suite` | `completed` |
| `discussion` | `created`, `edited`, `deleted`, `transferred`, `pinned`, `unpinned`, `labeled`, `unlabeled`, `locked`, `unlocked`, `category_changed`, `answered`, `unanswered` |
| `discussion_comment` | `created`, `edited`, `deleted` |
| `issue_comment` | `created`, `edited`, `deleted` |
| `issues` | `opened`, `edited`, `deleted`, `transferred`, `pinned`, `unpinned`, `closed`, `reopened`, `assigned`, `unassigned`, `labeled`, `unlabeled`, `locked`, `unlocked`, `milestoned`, `demilestoned` |
| `label` | `created`, `edited`, `deleted` |
| `merge_group` | `checks_requested` |
| `milestone` | `created`, `closed`, `opened`, `edited`, `deleted` |
| `pull_request` | `opened`, `edited`, `closed`, `reopened`, `synchronize`, `converted_to_draft`, `locked`, `unlocked`, `enqueued`, `dequeued`, `milestoned`, `demilestoned`, `ready_for_review`, `review_requested`, `review_request_removed`, `auto_merge_enabled`, `auto_merge_disabled`, `assigned`, `unassigned`, `labeled`, `unlabeled` |
| `pull_request_review` | `submitted`, `edited`, `dismissed` |
| `pull_request_review_comment` | `created`, `edited`, `deleted` |
| `pull_request_target` | Same as `pull_request` (runs in base repo context) |
| `registry_package` | `published`, `updated` |
| `release` | `published`, `unpublished`, `created`, `edited`, `deleted`, `prereleased`, `released` |
| `watch` | `started` |
| `workflow_run` | `completed`, `requested`, `in_progress` |

### Events without Activity Types
`create`, `delete`, `deployment`, `deployment_status`, `fork`, `gollum`, `page_build`, `public`, `push`, `schedule`, `status`, `workflow_call`, `workflow_dispatch`

### Events with Filter Patterns

| Event | Filters |
|-------|---------|
| `push` | `branches`, `branches-ignore`, `tags`, `tags-ignore`, `paths`, `paths-ignore` |
| `pull_request` / `pull_request_target` | `branches`, `branches-ignore`, `paths`, `paths-ignore` |
| `workflow_run` | `branches`, `branches-ignore` |

## Complete Context Properties

### `github` Context

| Property | Description |
|----------|-------------|
| `github.action` | Current action name or step ID |
| `github.action_path` | Composite action location path |
| `github.action_ref` | Action version reference |
| `github.action_repository` | Action owner/repo |
| `github.actor` | Username that triggered the workflow |
| `github.actor_id` | Account ID of actor |
| `github.api_url` | REST API URL (`https://api.github.com`) |
| `github.base_ref` | PR target branch |
| `github.env` | Path to env file on runner |
| `github.event` | Full webhook event payload object |
| `github.event_name` | Event name that triggered workflow |
| `github.event_path` | Path to webhook payload file |
| `github.graphql_url` | GraphQL API URL |
| `github.head_ref` | PR source branch |
| `github.job` | Current job_id |
| `github.path` | Path to PATH file on runner |
| `github.ref` | Full ref (`refs/heads/main`, `refs/tags/v1.0`) |
| `github.ref_name` | Short ref name (`main`, `v1.0`) |
| `github.ref_protected` | Whether branch has protection rules |
| `github.ref_type` | `branch` or `tag` |
| `github.repository` | `owner/repo` |
| `github.repository_id` | Numeric repo ID |
| `github.repository_owner` | Owner username |
| `github.repository_owner_id` | Owner account ID |
| `github.repositoryUrl` | Git URL (git:// protocol) |
| `github.retention_days` | Artifact retention setting |
| `github.run_id` | Unique numeric run ID |
| `github.run_number` | Sequential run number for the workflow |
| `github.run_attempt` | Re-run attempt number (starts at 1) |
| `github.secret_source` | Source of secrets (`Actions`, `Codespaces`, `Dependabot`) |
| `github.server_url` | GitHub server URL |
| `github.sha` | Commit SHA that triggered the workflow |
| `github.token` | GITHUB_TOKEN value |
| `github.triggering_actor` | User who initiated re-run |
| `github.workflow` | Workflow name |
| `github.workflow_ref` | Workflow file ref path |
| `github.workflow_sha` | Workflow file commit SHA |
| `github.workspace` | Default working directory on runner |

### `job` Context

| Property | Description |
|----------|-------------|
| `job.container.id` | Container ID |
| `job.container.network` | Container network ID |
| `job.services.<service_id>.id` | Service container ID |
| `job.services.<service_id>.network` | Service network ID |
| `job.services.<service_id>.ports` | Exposed port mappings |
| `job.status` | `success`, `failure`, or `cancelled` |

### `steps` Context

| Property | Description |
|----------|-------------|
| `steps.<step_id>.outputs.<name>` | Step output value |
| `steps.<step_id>.outcome` | Result before `continue-on-error` |
| `steps.<step_id>.conclusion` | Result after `continue-on-error` |

### `runner` Context

| Property | Description |
|----------|-------------|
| `runner.name` | Runner name |
| `runner.os` | `Linux`, `Windows`, or `macOS` |
| `runner.arch` | `X86`, `X64`, `ARM`, `ARM64` |
| `runner.temp` | Temp directory path |
| `runner.tool_cache` | Preinstalled tools directory |
| `runner.debug` | `1` if debug logging enabled |
| `runner.environment` | `github-hosted` or `self-hosted` |

### `strategy` Context (matrix jobs)

| Property | Description |
|----------|-------------|
| `strategy.fail-fast` | Boolean |
| `strategy.job-index` | Zero-based current job index |
| `strategy.job-total` | Total number of matrix jobs |
| `strategy.max-parallel` | Max concurrent jobs |

### `needs` Context

| Property | Description |
|----------|-------------|
| `needs.<job_id>.result` | `success`, `failure`, `cancelled`, `skipped` |
| `needs.<job_id>.outputs.<name>` | Output value from dependency |

## Expression Operators

`()`, `[]`, `.`, `!`, `<`, `<=`, `>`, `>=`, `==`, `!=`, `&&`, `||`

Equality comparisons are loose and case-insensitive for strings. Mismatched types are coerced to numbers.

### Object Filters
`myArray.*.property` selects a property from all elements, returning an array.

### Type Casting Rules

| Source | Number | String | Boolean |
|--------|--------|--------|---------|
| Null | `0` | `''` | `false` |
| Boolean true | `1` | `'true'` | -- |
| Boolean false | `0` | `'false'` | -- |
| Number 0 | -- | `'0'` | `false` |
| Number nonzero | -- | string repr | `true` |

## Complete Job Syntax

```yaml
jobs:
  job_id:
    name: "Display Name"
    runs-on: ubuntu-latest
    needs: [other_job]
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
    environment:
      name: production
      url: https://example.com
    timeout-minutes: 30
    continue-on-error: false
    concurrency:
      group: deploy
      cancel-in-progress: false
    env:
      KEY: value
    defaults:
      run:
        shell: bash
        working-directory: ./src
    outputs:
      result: ${{ steps.step1.outputs.value }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20]
        include:
          - os: macos-latest
            node: 20
        exclude:
          - os: windows-latest
            node: 18
      fail-fast: true
      max-parallel: 2
    container:
      image: node:18
      env:
        NODE_ENV: test
      ports: [8080]
      volumes: ['my_docker_volume:/volume_mount']
      options: --cpus 1
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

## Service Containers

```yaml
services:
  redis:
    image: redis:7
    ports: ['6379:6379']
    options: --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 5s --health-retries 5

  postgres:
    image: postgres:15
    env:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    ports: ['5432:5432']
    options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
```

## Artifacts

### Upload
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: my-artifact
    path: |
      dist/
      !dist/**/*.map
    retention-days: 5
    if-no-files-found: error    # warn, ignore, error
```

### Download
```yaml
- uses: actions/download-artifact@v5
  with:
    name: my-artifact
    path: ./downloaded
```

Artifact names must be unique within a workflow run. For matrix jobs, include the matrix value in the name.

## Cron Schedule Syntax

Format: `minute(0-59) hour(0-23) day-of-month(1-31) month(1-12) day-of-week(0-6)`

Operators: `*` (any), `,` (list), `-` (range), `/` (step)

Minimum interval: 5 minutes.

| Schedule | Cron Expression |
|----------|----------------|
| Every 15 minutes | `*/15 * * * *` |
| Daily at midnight UTC | `0 0 * * *` |
| Weekdays at 9 AM UTC | `0 9 * * 1-5` |
| Weekly on Sunday | `0 0 * * 0` |
| First day of month | `0 0 1 * *` |

## Docker Action Definition

```yaml
name: 'My Docker Action'
description: 'Runs in a container'
inputs:
  who-to-greet:
    required: true
outputs:
  time:
    description: 'Execution timestamp'
runs:
  using: docker
  image: Dockerfile           # or docker://alpine:3.18
  entrypoint: entrypoint.sh
  args:
    - ${{ inputs.who-to-greet }}
  env:
    MY_VAR: value
```

Docker actions only run on Linux runners.

## JavaScript Action Definition

```yaml
name: 'My JS Action'
description: 'Cross-platform action'
inputs:
  name:
    required: true
runs:
  using: node20
  main: dist/index.js
  pre: dist/setup.js           # optional, runs before main
  post: dist/cleanup.js        # optional, runs after main
  pre-if: runner.os == 'linux'
  post-if: always()
```

Key toolkit packages: `@actions/core` (inputs, outputs, logging), `@actions/github` (Octokit client, context).

## Reusable Workflow Complete Example

### Caller
```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
      version: "1.2.3"
    secrets:
      deploy_key: ${{ secrets.STAGING_KEY }}
    permissions:
      contents: read
      id-token: write
```

### Callee
```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        type: string
        default: latest
    secrets:
      deploy_key:
        required: true
    outputs:
      deploy_url:
        description: "Deployment URL"
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    outputs:
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - id: deploy
        run: echo "url=https://${{ inputs.environment }}.example.com" >> $GITHUB_OUTPUT
        env:
          DEPLOY_KEY: ${{ secrets.deploy_key }}
```

## Common Workflow Patterns

### CI Pipeline
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: npm
      - run: npm ci
      - run: npm test
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

### Deploy on Release
```yaml
name: Deploy
on:
  release:
    types: [published]
permissions:
  contents: read
  id-token: write
concurrency:
  group: production-deploy
  cancel-in-progress: false
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - run: ./deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

### Conditional Deployment Pipeline
```yaml
name: Pipeline
on:
  push:
    branches: [main, 'release/*']
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.value }}
    steps:
      - uses: actions/checkout@v4
      - id: version
        run: echo "value=$(cat VERSION)" >> $GITHUB_OUTPUT
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
      version: ${{ needs.build.outputs.version }}
    secrets: inherit
  deploy-prod:
    needs: build
    if: startsWith(github.ref, 'refs/heads/release/')
    uses: ./.github/workflows/deploy.yml
    with:
      environment: production
      version: ${{ needs.build.outputs.version }}
    secrets: inherit
```

## Default Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_ACTION` | Action name |
| `GITHUB_ACTOR` | User who triggered the workflow |
| `GITHUB_BASE_REF` | PR target branch |
| `GITHUB_ENV` | Path to env file |
| `GITHUB_EVENT_NAME` | Event name |
| `GITHUB_EVENT_PATH` | Path to event payload JSON |
| `GITHUB_HEAD_REF` | PR source branch |
| `GITHUB_JOB` | Job ID |
| `GITHUB_OUTPUT` | Path to output file |
| `GITHUB_PATH` | Path to PATH file |
| `GITHUB_REF` | Full ref |
| `GITHUB_REF_NAME` | Short ref name |
| `GITHUB_REPOSITORY` | `owner/repo` |
| `GITHUB_RUN_ATTEMPT` | Re-run attempt number |
| `GITHUB_RUN_ID` | Unique run ID |
| `GITHUB_RUN_NUMBER` | Sequential run number |
| `GITHUB_SERVER_URL` | GitHub server URL |
| `GITHUB_SHA` | Commit SHA |
| `GITHUB_STEP_SUMMARY` | Path to step summary file |
| `GITHUB_TOKEN` | Authentication token |
| `GITHUB_WORKFLOW` | Workflow name |
| `GITHUB_WORKSPACE` | Default working directory |
| `RUNNER_ARCH` | Runner architecture |
| `RUNNER_NAME` | Runner name |
| `RUNNER_OS` | `Linux`, `Windows`, or `macOS` |
| `RUNNER_TEMP` | Temp directory |
| `RUNNER_TOOL_CACHE` | Tool cache directory |

## Secrets via `gh` CLI

```bash
# Repository secret
gh secret set SECRET_NAME
gh secret set SECRET_NAME < secret.txt

# Environment secret
gh secret set --env ENV_NAME SECRET_NAME

# Organization secret
gh secret set --org ORG_NAME SECRET_NAME --visibility all
gh secret set --org ORG_NAME SECRET_NAME --repos REPO1,REPO2

# List secrets
gh secret list
gh secret list --env ENV_NAME
```

## Key Gotchas

- `include` entries that match existing matrix combinations add properties; entries that don't match create new standalone combinations
- `exclude` must match all specified properties of a combination to exclude it
- Matrix values are always strings in expressions; use `fromJSON()` for dynamic matrices
- Outputs from matrix jobs: only the last completed job's output is available (use artifacts instead)
- `shell:` is mandatory on every `run:` step in composite actions
- Composite action inputs are NOT automatically mapped to `INPUT_*` env vars
- `if: always()` runs even on cancellation; prefer `if: success() || failure()` to skip cancelled runs
- When a job is skipped via `if:`, all dependent jobs are skipped too (unless they use `if: always()`)
- Concurrency group names are case-insensitive
- Environment secrets override repository secrets of the same name
- Secrets are NOT passed to workflows triggered from forked repos
- An unset secret returns empty string, not an error
- `GH_TOKEN` must be set as env var for every step using `gh` CLI
