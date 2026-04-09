from __future__ import annotations

from app.agents.critic_agent import CriticAgent
from app.agents.coder_agent import CoderAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.router_agent import RouterAgent
from app.agents.verifier_agent import VerifierAgent
from app.core.memory_store import MemoryStore
from app.core.spec_loader import SpecLoader
from app.evals.evaluator import Evaluator
from app.evals.replay import ReplayLogger
from app.runtime.adapter_factory import build_runtime_adapter
from app.superpowers.retry_policy import RetryPolicy
from app.superpowers.self_repair import SelfRepairEngine


class GraphExecutor:
    def __init__(self, spec_loader: SpecLoader, memory_store: MemoryStore, runtime_provider: str | None = None) -> None:
        self.spec_loader = spec_loader
        self.memory_store = memory_store
        self.adapter = build_runtime_adapter(runtime_provider)
        self.retry_policy = RetryPolicy()
        self.repair_engine = SelfRepairEngine(self.adapter)
        self.evaluator = Evaluator()
        self.replay_logger = ReplayLogger(memory_store)

    def execute(self, initial_state: dict) -> dict:
        planner = PlannerAgent(self.spec_loader.load_agent("planner"))
        coder = CoderAgent(self.spec_loader.load_agent("coder"), self.adapter)
        verifier = VerifierAgent(self.spec_loader.load_agent("verifier"), self.adapter)
        critic = CriticAgent(self.spec_loader.load_agent("critic"))
        router = RouterAgent(self.spec_loader.load_agent("router"))

        state = dict(initial_state)
        state["runtime_provider"] = self.adapter.provider_name
        state.update(planner.run(state))
        state.update(coder.run(state))
        state.update(verifier.run(state))
        state.update(critic.run(state))
        state.update(router.run(state))

        attempt = 1
        while self.retry_policy.should_retry(attempt, state.get("critic_issues", [])):
            state.update(self.repair_engine.repair(state, state["critic_issues"]))
            state.update(verifier.run(state))
            state.update(critic.run(state))
            state.update(router.run(state))
            attempt += 1

        state.update(self.evaluator.score(state))
        state["trajectory_path"] = self.replay_logger.persist(state)
        return state
