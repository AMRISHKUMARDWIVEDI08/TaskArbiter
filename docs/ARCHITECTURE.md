# TaskArbiter architecture

## Components
- Intelligent Contract: consensus-critical task lifecycle and verdict.
- Public evidence: URL-addressable deliverable evidence.
- GenLayer non-deterministic execution: evidence interpretation.
- Equivalence Principle: validator agreement on the structured decision.
- Frontend: task creation, evidence submission, evaluation request, and verdict display.
- Tests: direct mocked tests plus real Studio integration tests.

## Trust boundary
Only consensus-critical facts belong in the contract. Frontend/backend services must not be trusted to decide the final verdict.

## Data flow
1. creator publishes requirements
2. submitter publishes evidence URL
3. evaluator reads evidence
4. structured verdict is produced
5. validators independently execute/check the result
6. finalized verdict becomes shared state

## MVP security assumptions
Evidence must be public and stable enough for validators. Private credentials are never stored on-chain or in GitHub.
