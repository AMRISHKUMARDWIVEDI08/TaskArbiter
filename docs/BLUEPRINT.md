# TaskArbiter — Blueprint & Roadmap

## Mission
Build an original GenLayer-native Intelligent Contract that adjudicates whether a submitted deliverable satisfies pre-agreed requirements using independently verifiable evidence and consensus.

## Product flow
Task creator -> task requirements -> deliverable/evidence submission -> Intelligent Contract evaluation -> independent validator evaluation -> structured consensus -> on-chain verdict.

## MVP decision
The contract will decide one clear milestone outcome:
- APPROVED
- REVISION_REQUIRED
- REJECTED
- UNDETERMINED when evidence/execution is insufficient

The exact scoring model will be kept minimal until tests prove it is useful.

## What makes GenLayer necessary
TaskArbiter is not a generic AI reviewer. The consensus-critical decision depends on interpreting natural-language requirements and real-world/public evidence. Multiple validators should independently inspect evidence and converge on a structured result. The final verdict changes shared contract state.

## Blueprint

### On-chain state
- task id
- creator
- requirements
- submission/evidence references
- status
- evaluation result
- timestamps/deadline where needed
- finalized verdict

### Evaluation output
Keep consensus-critical output structured:
- status
- requirements_met
- critical_failures
- optional score
- concise reason/evidence references

Do not require exact equality of free-form reasoning.

### Evidence
Initial evidence sources can include public GitHub links, public web pages, and other publicly inspectable deliverables. Evidence must be independently accessible to validators.

### Contract boundaries
The Intelligent Contract owns:
- task state
- submission state
- consensus-critical evaluation
- verdict/finalization

The frontend owns UX only. No secret API keys belong in the repository.

## Development architecture
Use the current official GenLayer project boilerplate as an architectural reference, not as copied implementation.

Planned structure:
contracts/
tests/direct/
tests/integration/
frontend/
deploy/
docs/
.github/workflows/

## Quality gates

### Gate 1 — Specification
Define exact decision, evidence model, state transitions, and failure behavior.

### Gate 2 — Contract
Implement the smallest working Intelligent Contract.

### Gate 3 — Lint
Run current GenVM linter and resolve all contract errors/warnings that matter.

### Gate 4 — Direct tests
Test create, submit, evaluate, views, access control, malformed inputs, mocked web/LLM responses, and failure cases.

### Gate 5 — Studio integration
Run real consensus-oriented integration tests in GenLayer Studio.

### Gate 6 — Security review
Check permissions, replay/duplicate submission, evidence availability, state transitions, storage types, non-deterministic calls, and secret handling.

### Gate 7 — MVP frontend
Create task -> define requirements -> submit evidence -> request evaluation -> show finalized verdict.

### Gate 8 — Deployment
Deploy only after gates 1–7 pass. Record network, contract address, transaction IDs, and reproducible steps.

### Gate 9 — Public evidence
Prepare GitHub, demo, tests, deployment proof, screenshots, architecture, limitations, and usage documentation.

### Gate 10 — Builder submission
Complete the GenLayer Portal Builder contribution form only after the project is genuinely working. Audit every field and evidence link before submitting.

## Roadmap
1. Research & requirements — complete
2. Final product specification — next
3. Contract interface/data model
4. Intelligent Contract implementation
5. Direct test suite
6. GenLayer Studio integration
7. Frontend/demo
8. Security + failure-path review
9. Testnet deployment
10. Documentation/evidence package
11. Builder contribution submission
12. Post-submission fixes if steward feedback requires them

## Differentiation
Do not clone FactAnchor or other existing projects. TaskArbiter focuses on milestone/deliverable adjudication rather than general fact verification. GitHub is only one possible evidence source, not the product itself.

## Point strategy
Points are not guaranteed. We optimize for a genuine, working, well-documented contribution aligned with current GenLayer requirements. Never fabricate activity, evidence, users, deployments, or results.

## Mobile execution
The user works from Android/mobile. Prefer hosted Studio and lightweight tooling where practical. Use screenshots at important UI states. Avoid unnecessary local dependencies and native compilation.

## Definition of done
TaskArbiter is ready for submission only when:
- contract works;
- tests pass;
- real GenLayer consensus behavior has been exercised;
- deployment proof exists;
- frontend/demo is usable;
- documentation explains why GenLayer is required;
- evidence is reproducible;
- repository is clean;
- submission requirements are satisfied.
