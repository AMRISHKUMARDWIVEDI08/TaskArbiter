# TaskArbiter

TaskArbiter is an original GenLayer-native prototype for adjudicating whether a submitted deliverable satisfies pre-agreed requirements using public evidence and consensus.

## Status

Early MVP — contract and direct-mode test foundation are under active development.

## Core flow

task agreement -> requirements -> public evidence -> intelligent evaluation -> independent validation -> structured verdict -> finalized on-chain state

## Why GenLayer

The consensus-critical outcome requires interpretation of natural-language requirements and public evidence. TaskArbiter is designed so validators can independently inspect the evidence and converge on a structured decision rather than trusting one centralized AI response.

## MVP verdicts

- APPROVED
- REVISION_REQUIRED
- REJECTED
- UNDETERMINED

## Repository

- contracts/ — Intelligent Contracts
- tests/direct/ — fast in-memory tests
- tests/integration/ — real Studio/consensus tests
- docs/ — architecture, specification, and research
- deploy/ — deployment scripts (to be added after integration validation)
- frontend/ — demo UI (to be added after contract validation)

## Development workflow

1. lint
2. direct tests with web/LLM mocks
3. Studio integration tests
4. security/failure-path review
5. testnet deployment
6. evidence package
7. Builder contribution submission

This project is independently implemented. GenLayer repositories are references for tooling and architecture; their code is not copied into TaskArbiter.

## Current scope

The first milestone is a small end-to-end adjudication loop. Automatic real-money payouts, tokens, private credentials, and unnecessary AI chat features are intentionally out of scope until the core decision flow is proven.

## License

MIT
