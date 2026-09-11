# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
from genlayer import *


class TaskArbiter(gl.Contract):
    """Consensus-backed adjudication of a public deliverable against requirements."""

    tasks: TreeMap[str, str]
    requirements: TreeMap[str, str]
    evidence: TreeMap[str, str]
    verdicts: TreeMap[str, str]

    def __init__(self):
        pass

    @gl.public.write
    def create_task(self, task_id: str, requirement_text: str) -> None:
        assert task_id != "", "task_id required"
        assert requirement_text != "", "requirements required"
        assert self.tasks[task_id] == "", "task already exists"
        self.tasks[task_id] = "OPEN"
        self.requirements[task_id] = requirement_text

    @gl.public.write
    def submit_evidence(self, task_id: str, evidence_url: str) -> None:
        assert self.tasks[task_id] == "OPEN", "task not open"
        assert evidence_url.startswith("http://") or evidence_url.startswith("https://"), "public evidence URL required"
        self.evidence[task_id] = evidence_url

    def _evaluate(self, requirement: str, url: str) -> dict:
        def evaluate_once() -> str:
            page = gl.nondet.web.render(url, mode="text")
            prompt = f"""You are an impartial deliverable evaluator.

Task requirements:
{requirement}

Public evidence:
{page}

Return ONLY JSON:
{{
  "status": "APPROVED" | "REVISION_REQUIRED" | "REJECTED" | "UNDETERMINED",
  "requirements_met": integer,
  "critical_failures": integer,
  "reason": "short evidence-based explanation"
}}

Do not invent evidence. If the page cannot be inspected reliably, use UNDETERMINED.
"""
            return json.dumps(
                gl.nondet.exec_prompt(prompt, response_format="json"),
                sort_keys=True,
            )

        return json.loads(gl.eq_principle.strict_eq(evaluate_once))

    @gl.public.write
    def evaluate(self, task_id: str) -> None:
        assert self.tasks[task_id] == "OPEN", "task not open"
        assert self.evidence[task_id] != "", "evidence required"

        result = self._evaluate(
            self.requirements[task_id],
            self.evidence[task_id],
        )
        self.verdicts[task_id] = json.dumps(result, sort_keys=True)
        self.tasks[task_id] = "FINALIZED"

    @gl.public.view
    def get_task(self, task_id: str) -> dict:
        return {
            "status": self.tasks[task_id],
            "requirements": self.requirements[task_id],
            "evidence": self.evidence[task_id],
            "verdict": self.verdicts[task_id],
        }
