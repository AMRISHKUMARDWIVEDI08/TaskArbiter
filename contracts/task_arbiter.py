# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class TaskArbiter(gl.Contract):
    next_task_id: u256
    task_creators: TreeMap[u256, Address]
    task_requirements: TreeMap[u256, str]
    task_evidence_urls: TreeMap[u256, str]
    task_status: TreeMap[u256, str]
    task_verdicts: TreeMap[u256, str]
    task_requirements_met: TreeMap[u256, u256]
    task_critical_failures: TreeMap[u256, str]
    task_reasons: TreeMap[u256, str]

    def __init__(self):
        self.next_task_id = 1

    @gl.public.write
    def create_task(self, requirements: str) -> u256:
        if len(requirements.strip()) == 0:
            raise gl.vm.UserError("Requirements are required")

        task_id = self.next_task_id
        self.task_creators[task_id] = gl.message.sender_address
        self.task_requirements[task_id] = requirements
        self.task_evidence_urls[task_id] = ""
        self.task_status[task_id] = "OPEN"
        self.task_verdicts[task_id] = "UNDETERMINED"
        self.task_requirements_met[task_id] = 0
        self.task_critical_failures[task_id] = ""
        self.task_reasons[task_id] = ""

        self.next_task_id = task_id + 1
        return task_id

    @gl.public.write
    def submit_evidence(self, task_id: u256, evidence_url: str):
        if task_id not in self.task_creators:
            raise gl.vm.UserError("Task does not exist")

        if gl.message.sender_address != self.task_creators[task_id]:
            raise gl.vm.UserError("Only the task creator can submit evidence")

        if self.task_status.get(task_id, "") != "OPEN":
            raise gl.vm.UserError("Task is not open")

        if len(evidence_url.strip()) == 0:
            raise gl.vm.UserError("Evidence URL is required")

        self.task_evidence_urls[task_id] = evidence_url
        self.task_status[task_id] = "SUBMITTED"

    @gl.public.write
    def evaluate(self, task_id: u256) -> str:
        if task_id not in self.task_creators:
            raise gl.vm.UserError("Task does not exist")

        if self.task_status.get(task_id, "") != "SUBMITTED":
            raise gl.vm.UserError("Task must have submitted evidence")

        requirements = self.task_requirements[task_id]
        evidence_url = self.task_evidence_urls[task_id]

        def evaluate_once():
            try:
                evidence = gl.nondet.web.render(evidence_url, mode="text")
            except Exception:
                return {
                    "status": "UNDETERMINED",
                    "requirements_met": 0,
                    "critical_failures": "evidence_inaccessible",
                    "reason": "The public evidence could not be accessed."
                }

            prompt = f"""
You are the evaluator for TaskArbiter.

The task requirements are:
{requirements}

The evidence URL is:
{evidence_url}

The evidence content is:
{evidence[:14000]}

Evaluate ONLY against the supplied requirements and evidence.

Requirements should be treated as numbered items if the creator numbered them.
Return JSON with exactly:
{{
  "status": "APPROVED" | "REVISION_REQUIRED" | "REJECTED" | "UNDETERMINED",
  "requirements_met": integer,
  "critical_failures": "comma-separated requirement numbers, or empty string",
  "reason": "short evidence-based explanation"
}}

Rules:
- APPROVED only when all important requirements are satisfied.
- REVISION_REQUIRED when one or more non-critical/fixable requirements are missing.
- REJECTED when a critical requirement is clearly failed or contradicted.
- UNDETERMINED when the evidence is inaccessible or insufficient.
- Never invent evidence.
- Keep critical_failures deterministic: use requirement numbers only, such as "2,4".
- requirements_met must be the count of clearly satisfied requirements.
"""
            result = gl.nondet.exec_prompt(prompt, response_format="json")

            if not isinstance(result, dict):
                raise gl.vm.UserError("Invalid evaluator response")

            status = result.get("status")
            requirements_met = result.get("requirements_met")
            critical_failures = result.get("critical_failures")
            reason = result.get("reason")

            if status not in (
                "APPROVED",
                "REVISION_REQUIRED",
                "REJECTED",
                "UNDETERMINED",
            ):
                raise gl.vm.UserError("Invalid verdict status")

            if (
                not isinstance(requirements_met, int)
                or requirements_met < 0
            ):
                raise gl.vm.UserError("Invalid requirements_met")

            if not isinstance(critical_failures, str):
                raise gl.vm.UserError("Invalid critical_failures")

            if not isinstance(reason, str) or len(reason.strip()) == 0:
                raise gl.vm.UserError("Invalid reason")

            return {
                "status": status,
                "requirements_met": requirements_met,
                "critical_failures": critical_failures.strip(),
                "reason": reason[:1200],
            }

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            leader_data = leader_result.calldata
            if not isinstance(leader_data, dict):
                return False

            validator_data = evaluate_once()
            if not isinstance(validator_data, dict):
                return False

            # Consensus-critical fields must agree.
            return (
                leader_data.get("status") == validator_data.get("status")
                and leader_data.get("requirements_met")
                == validator_data.get("requirements_met")
                and leader_data.get("critical_failures")
                == validator_data.get("critical_failures")
            )

        result = gl.vm.run_nondet_unsafe(evaluate_once, validator_fn)

        self.task_status[task_id] = "FINALIZED"
        self.task_verdicts[task_id] = result["status"]
        self.task_requirements_met[task_id] = result["requirements_met"]
        self.task_critical_failures[task_id] = result["critical_failures"]
        self.task_reasons[task_id] = result["reason"]

        return result["status"]

    @gl.public.view
    def get_task(self, task_id: u256) -> str:
        if task_id not in self.task_creators:
            return "task not found"

        return (
            "creator=" + str(self.task_creators[task_id])
            + " | requirements=" + self.task_requirements.get(task_id, "")
            + " | evidence=" + self.task_evidence_urls.get(task_id, "")
            + " | status=" + self.task_status.get(task_id, "")
            + " | verdict=" + self.task_verdicts.get(task_id, "")
            + " | requirements_met="
            + str(self.task_requirements_met.get(task_id, 0))
            + " | critical_failures="
            + self.task_critical_failures.get(task_id, "")
            + " | reason=" + self.task_reasons.get(task_id, "")
        )

    @gl.public.view
    def get_verdict(self, task_id: u256) -> str:
        return self.task_verdicts.get(task_id, "UNDETERMINED")

    @gl.public.view
    def get_evidence(self, task_id: u256) -> str:
        return self.task_evidence_urls.get(task_id, "")

    @gl.public.view
    def get_requirements(self, task_id: u256) -> str:
        return self.task_requirements.get(task_id, "")
