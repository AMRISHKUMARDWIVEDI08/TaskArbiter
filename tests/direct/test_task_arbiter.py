import json


def test_create_and_submit(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice

    contract.create_task(
        "task-1",
        "deliverable must contain a working README and a public demo link",
    )
    contract.submit_evidence("task-1", "https://example.com/demo")

    task = contract.get_task("task-1")
    assert task["status"] == "OPEN"
    assert "working README" in task["requirements"]
    assert task["evidence"] == "https://example.com/demo"
    assert task["verdict"] == ""


def test_empty_task_id_rejected(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("task_id required"):
        contract.create_task("", "some requirement")


def test_empty_requirements_rejected(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("requirements required"):
        contract.create_task("task-1", "")


def test_invalid_evidence_url_rejected(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice
    contract.create_task("task-1", "public demo required")
    with direct_vm.expect_revert("public evidence URL required"):
        contract.submit_evidence("task-1", "not-a-url")


def test_duplicate_task_rejected(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice
    contract.create_task("task-1", "public demo required")
    with direct_vm.expect_revert("task already exists"):
        contract.create_task("task-1", "different requirement")


def test_evaluation_with_web_and_llm_mocks(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/task_arbiter.py")
    direct_vm.sender = direct_alice
    contract.create_task("task-1", "README and demo are present")
    contract.submit_evidence("task-1", "https://example.com/demo")

    direct_vm.mock_web(
        r"example\.com/demo",
        {"status": 200, "body": "README present. Demo: https://demo.example.com"},
    )
    direct_vm.mock_llm(
        r"impartial deliverable evaluator",
        json.dumps({
            "status": "APPROVED",
            "requirements_met": 2,
            "critical_failures": 0,
            "reason": "The public evidence contains the required README and demo.",
        }),
    )

    contract.evaluate("task-1")
    task = contract.get_task("task-1")
    assert task["status"] == "FINALIZED"
    verdict = json.loads(task["verdict"])
    assert verdict["status"] == "APPROVED"
    assert verdict["requirements_met"] == 2
    assert verdict["critical_failures"] == 0
