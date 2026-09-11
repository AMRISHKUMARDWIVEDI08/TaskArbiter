import json


def test_create_and_submit(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice

    task_id = contract.create_task("1. working README\n2. public demo link")
    assert int(task_id) == 1

    contract.submit_evidence(task_id, "https://example.com/demo")
    task = contract.get_task(task_id)

    assert "status=SUBMITTED" in task
    assert "requirements=1. working README" in task
    assert "evidence=https://example.com/demo" in task
    assert "verdict=UNDETERMINED" in task


def test_create_requires_requirements(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("Requirements are required"):
        contract.create_task("")


def test_creator_only_can_submit_evidence(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/task_arbiter.py")

    direct_vm.sender = direct_alice
    task_id = contract.create_task("public demo required")

    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only the task creator can submit evidence"):
        contract.submit_evidence(task_id, "https://example.com/demo")


def test_evidence_requires_existing_task(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("Task does not exist"):
        contract.submit_evidence(999, "https://example.com/demo")


def test_evaluation_with_web_and_llm_mocks(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice

    task_id = contract.create_task(
        "1. README exists\n2. public demo exists"
    )
    contract.submit_evidence(task_id, "https://example.com/demo")

    direct_vm.mock_web(
        r"example\.com/demo",
        {
            "status": 200,
            "body": "README exists. Public demo exists at https://demo.example.com",
        },
    )
    direct_vm.mock_llm(
        r"impartial deliverable evaluator",
        json.dumps(
            {
                "status": "APPROVED",
                "requirements_met": 2,
                "critical_failures": "",
                "reason": "Both required deliverables are present in the public evidence.",
            }
        ),
    )

    result = contract.evaluate(task_id)
    assert result == "APPROVED"

    task = contract.get_task(task_id)
    assert "status=FINALIZED" in task
    assert "verdict=APPROVED" in task
    assert "requirements_met=2" in task


def test_getters_for_missing_task_return_safe_defaults(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/task_arbiter.py")

    assert contract.get_verdict(404) == "UNDETERMINED"
    assert contract.get_evidence(404) == ""
    assert contract.get_requirements(404) == ""
    assert contract.get_task(404) == "task not found"
