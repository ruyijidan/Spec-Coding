# Spec Coding Starter

[中文说明](./README.md)

A runnable starter repo for engineering-oriented Spec Coding and multi-agent execution.

The current project is designed to make the following loop executable end to end:

`Spec -> Plan -> Execute -> Verify -> Repair -> Replay`

In this repository:

- `Spec` defines task contracts, inputs, outputs, constraints, and acceptance criteria
- `Planner / Graph` turns a task into an executable flow
- `Runtime` actually edits files, runs commands, and executes tests
- `Verifier / Critic / Repair` checks results, detects failures, and attempts recovery
- `Replay / Eval` stores trajectories for later analysis

## Status

The project is currently at a runnable starter stage:

- Phase 1 is mostly done: the minimal closed loop works
- Phase 2 has started: `Critic`, `Router`, and `Repair` exist, but the graph is still mostly linear
- Full infra work is not done yet: real runtime providers, orchestration, dashboards, and scheduling are still pending

Starter task types currently included:

- `implement_feature`
- `fix_bug`
- `write_tests`
- `investigate_issue`

## Core Capabilities

### 1. Spec-driven task execution

Task specs live in [`specs/tasks`](./specs/tasks).

Each task spec currently defines:

- `goal`
- `inputs`
- `outputs`
- `constraints`
- `tools`
- `done_when`

Spec loading starts in [`app/core/spec_loader.py`](./app/core/spec_loader.py).

### 2. Runnable minimal multi-agent loop

The default execution flow in [`app/graph/executor.py`](./app/graph/executor.py) is:

1. `PlannerAgent`
2. `CoderAgent`
3. `VerifierAgent`
4. `CriticAgent`
5. `RouterAgent`
6. `SelfRepairEngine` when needed
7. `ReplayLogger` to persist the trajectory

### 3. Switchable runtime providers

Runtime is already organized around providers:

- [`app/runtime/ecc_adapter.py`](./app/runtime/ecc_adapter.py): default local mock runtime
- [`app/runtime/adapter_factory.py`](./app/runtime/adapter_factory.py): provider factory
- [`app/runtime/cli_adapter.py`](./app/runtime/cli_adapter.py): placeholder adapters for `claude_code` and `codex_cli`

The `claude_code` and `codex_cli` providers are still placeholders. Wiring them into real command execution is the next major step.

### 4. Repair loop and replay logging

When verification fails, the system can enter a repair loop:

- repair logic: [`app/superpowers/self_repair.py`](./app/superpowers/self_repair.py)
- retry policy: [`app/superpowers/retry_policy.py`](./app/superpowers/retry_policy.py)
- trajectory persistence: [`app/evals/replay.py`](./app/evals/replay.py)

Run artifacts are written to [`logs/trajectories`](./logs/trajectories).

## Quick Start

### Requirements

- Python 3.10+

### Run examples

```bash
cd /data/ji/code/spec_coding
python3 -m examples.run_feature_task
python3 -m examples.run_fix_bug
python3 -m examples.run_investigate_issue
```

### Run tests

```bash
cd /data/ji/code/spec_coding
python3 -m unittest discover -s tests
```

## Structure

```text
spec_coding/
├── app/
│   ├── agents/
│   ├── core/
│   ├── evals/
│   ├── graph/
│   ├── runtime/
│   ├── superpowers/
│   └── tools/
├── examples/
├── logs/
├── specs/
│   ├── agents/
│   └── tasks/
└── tests/
```

Key directories:

- [`app/core`](./app/core): models, spec loading, and basic shared primitives
- [`app/agents`](./app/agents): planner / coder / verifier / critic / router
- [`app/graph`](./app/graph): orchestration entry point
- [`app/runtime`](./app/runtime): executors and provider abstraction
- [`app/superpowers`](./app/superpowers): retry / repair logic
- [`app/evals`](./app/evals): scoring and replay
- [`examples`](./examples): runnable examples
- [`specs`](./specs): task and agent contracts
- [`tests`](./tests): regression coverage for the starter loop

## Key Entry Points

- main entry: [`app/main.py`](./app/main.py)
- execution graph: [`app/graph/executor.py`](./app/graph/executor.py)
- task templates: [`app/core/task_templates.py`](./app/core/task_templates.py)
- runtime factory: [`app/runtime/adapter_factory.py`](./app/runtime/adapter_factory.py)
- repair engine: [`app/superpowers/self_repair.py`](./app/superpowers/self_repair.py)

## Verified So Far

This repository has been validated locally with:

- `python3 -m unittest discover -s tests`
- `python3 -m examples.run_feature_task`
- `python3 -m examples.run_fix_bug`
- `python3 -m examples.run_investigate_issue`

## Recommended Next Steps

### P0

- Wire `claude_code` / `codex_cli` into real runtime execution
- Add tool contracts under `specs/tools/`
- Strengthen verifier checks for change boundaries and constraints

### P1

- Upgrade the current linear executor into an explicit graph / state machine
- Support different flows for different task types
- Add clearer routing, fallback, and repair branches

### P2

- Expand trace / replay schema
- Add richer evaluator metrics
- Add API, scheduling, sandboxing, and multi-workspace support
