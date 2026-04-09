# Spec Coding Starter

[English Version](./README.en.md)

一个可运行的、面向工程化落地的 Spec Coding 多 Agent Starter Repo。

它的目标不是只演示 prompt，而是先把下面这条最小闭环跑通：

`Spec -> Plan -> Execute -> Verify -> Repair -> Replay`

你可以把这套项目理解成：

- `Spec` 负责定义任务契约、输入输出、约束和验收标准
- `Planner / Graph` 负责把任务拆解成可执行流程
- `Runtime` 负责真正改文件、跑命令、跑测试
- `Verifier / Critic / Repair` 负责校验、自修复和重试
- `Replay / Eval` 负责记录轨迹，支持后续分析和优化

## 当前状态

当前仓库已经达到“可运行 starter”阶段，属于：

- Phase 1 基本完成：最小闭环已跑通
- Phase 2 起步：已经有 `Critic`、`Router`、`Repair`，但 graph 还不是完整状态机
- 还未进入完整 infra 阶段：真实 runtime provider、调度、多 workspace、dashboard 还没接完

目前已经支持 4 类 starter task：

- `implement_feature`
- `fix_bug`
- `write_tests`
- `investigate_issue`

## 核心能力

### 1. Spec 驱动任务执行

任务定义位于 [`specs/tasks`](./specs/tasks)。

当前每个任务 spec 都至少描述了：

- `goal`
- `inputs`
- `outputs`
- `constraints`
- `tools`
- `done_when`

入口加载逻辑在 [`app/core/spec_loader.py`](./app/core/spec_loader.py)。

### 2. 可运行的最小多 Agent 闭环

当前默认执行链路在 [`app/graph/executor.py`](./app/graph/executor.py)：

1. `PlannerAgent`
2. `CoderAgent`
3. `VerifierAgent`
4. `CriticAgent`
5. `RouterAgent`
6. `SelfRepairEngine` 按需重试
7. `ReplayLogger` 持久化 trajectory

### 3. Runtime Provider 可切换

当前 runtime 已经抽成 provider-based 结构：

- [`app/runtime/ecc_adapter.py`](./app/runtime/ecc_adapter.py)：默认本地 mock runtime
- [`app/runtime/adapter_factory.py`](./app/runtime/adapter_factory.py)：provider 构造入口
- [`app/runtime/cli_adapter.py`](./app/runtime/cli_adapter.py)：`claude_code` / `codex_cli` 占位适配器

现在的 `claude_code` 和 `codex_cli` 还是接口壳，还没有接真实命令执行逻辑。这一层是下一阶段重点。

### 4. 自修复与轨迹记录

当验证失败时，系统会进入 repair loop：

- 修复逻辑在 [`app/superpowers/self_repair.py`](./app/superpowers/self_repair.py)
- 重试策略在 [`app/superpowers/retry_policy.py`](./app/superpowers/retry_policy.py)
- 轨迹记录在 [`app/evals/replay.py`](./app/evals/replay.py)

执行结果会落到 [`logs/trajectories`](./logs/trajectories)。

## 快速开始

### 环境要求

- Python 3.10+

### 运行示例

```bash
cd /data/ji/code/spec_coding
python3 -m examples.run_feature_task
python3 -m examples.run_fix_bug
python3 -m examples.run_investigate_issue
```

### 运行测试

```bash
cd /data/ji/code/spec_coding
python3 -m unittest discover -s tests
```

## 项目结构

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

关键目录说明：

- [`app/core`](./app/core)：任务模型、spec 加载、上下文和基础数据结构
- [`app/agents`](./app/agents)：planner / coder / verifier / critic / router
- [`app/graph`](./app/graph)：当前执行编排入口
- [`app/runtime`](./app/runtime)：执行器与 provider 抽象
- [`app/superpowers`](./app/superpowers)：retry / repair 能力
- [`app/evals`](./app/evals)：评分与 replay
- [`examples`](./examples)：示例任务入口
- [`specs`](./specs)：任务与 agent 契约
- [`tests`](./tests)：最小回归测试集

## 关键入口

- 主入口：[`app/main.py`](./app/main.py)
- 执行编排：[`app/graph/executor.py`](./app/graph/executor.py)
- 任务模板：[`app/core/task_templates.py`](./app/core/task_templates.py)
- Runtime 工厂：[`app/runtime/adapter_factory.py`](./app/runtime/adapter_factory.py)
- Repair：[`app/superpowers/self_repair.py`](./app/superpowers/self_repair.py)

## 已验证内容

当前仓库已通过以下本地验证：

- `python3 -m unittest discover -s tests`
- `python3 -m examples.run_feature_task`
- `python3 -m examples.run_fix_bug`
- `python3 -m examples.run_investigate_issue`

## 适合怎么继续扩展

推荐下一步按下面顺序推进：

### P0

- 把 `claude_code` / `codex_cli` provider 接成真实执行器
- 增加 `specs/tools/` 的 tool contract
- 强化 verifier，补充改动范围与约束校验

### P1

- 把当前线性 executor 升级成显式 graph / state machine
- 为不同 task type 配置不同的 agent flow
- 支持更明确的 route / fallback / repair 分支

### P2

- 增强 trace / replay schema
- 增加 evaluator 细分指标
- 增加 API / 调度 / sandbox / 多 workspace

## 文档约定

- 默认文档语言为中文
- 英文版见 [`README.en.md`](./README.en.md)

