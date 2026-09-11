# Integration tests

These tests run against a real GenLayer environment/Studio rather than Direct Mode.

Before adding a test:
- confirm the current GenLayer Studio/testing-suite API;
- deploy the contract in the target environment;
- use a public evidence URL;
- record expected structured verdict behavior.

Integration coverage should include:
1. create task
2. submit evidence
3. evaluate with real consensus
4. read finalized verdict
5. inaccessible evidence -> UNDETERMINED
6. malformed evaluator result / execution failure
7. revision flow after REVISION_REQUIRED

Do not claim integration tests pass until they have actually been run.
