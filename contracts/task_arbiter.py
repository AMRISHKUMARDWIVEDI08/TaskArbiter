from genlayer import *


class TaskArbiter(gl.Contract):
    """Consensus-backed adjudication of deliverables against pre-agreed requirements."""

    tasks: TreeMap[str, str]
    requirements: TreeMap[str, str]
    evidence: TreeMap[str, str]
    verdicts: TreeMap[str, str]

    def create_task(self, task_id: str, requirement_text: str):
        assert task_id != "", "task_id required"
        assert requirement_text != "", "requirements required"
        assert self.tasks[task_id] == "", "task already exists"
        self.tasks[task_id] = "OPEN"
        self.requirements[task_id] = requirement_text

    def submit_evidence(self, task_id: str, evidence_url: str):
        assert self.tasks[task_id] == "OPEN", "task not open"
        assert evidence_url.startswith("http://") or evidence_url.startswith("https://"), "public evidence URL required"
        self.evidence[task_id] = evidence_url

    @gl.public.write
    def evaluate(self, task_id: str):
        assert self.tasks[task_id] == "OPEN", "task not open"
        assert self.evidence[task_id] != "", "evidence required"

        requirement = self.requirements[task_id]
        url = self.evidence[task_id]

        result = gl.nondet.exec_prompt(
            f"""You are an impartial deliverable evaluator.
Task requirements:
{requirement}

Public evidence URL:
{url}

Inspect the evidence and return ONLY JSON with:
status: APPROVED, REVISION_REQUIRED, REJECTED, or UNDETERMINED
requirements_met: integer
critical_failures: integer
reason: short string

Do not invent evidence. If the evidence cannot be inspected reliably, use UNDETERMINED."""
        )

        self.verdicts[task_id] = result
        self.tasks[task_id] = "FINALIZED"

    @gl.public.view
    def get_task(self, task_id: str):
        return {
            "status": self.tasks[task_id],
            "requirements": self.requirements[task_id],
            "evidence": self.evidence[task_id],
            "verdict": self.verdicts[task_id],
        }
