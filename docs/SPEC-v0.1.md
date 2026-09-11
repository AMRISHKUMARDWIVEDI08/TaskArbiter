# TaskArbiter — Technical Specification v0.1

## Core decision
Given a task with pre-agreed requirements and a submitted deliverable/evidence set, determine whether the requirements are satisfied.

## Verdict states
APPROVED: all critical requirements satisfied.
REVISION_REQUIRED: some requirements are not satisfied but the task is potentially fixable.
REJECTED: a critical requirement is clearly failed or evidence contradicts the requirement.
UNDETERMINED: evidence is inaccessible/insufficient or execution cannot establish a reliable result.

## Consensus-critical fields
status
requirements_met
critical_failures

Optional:
score
reason

Free-form reasoning is informational and must not be the primary equivalence key.

## First MVP scope
- create a task
- store requirements
- accept a public evidence reference
- evaluate evidence through non-deterministic operations
- validate the structured result through GenLayer consensus
- finalize the verdict
- expose read-only task/verdict views

## Explicit exclusions from v0.1
- automatic real-money payouts
- private GitHub credentials
- complex reputation system
- multi-party arbitration marketplace
- token economics
- unnecessary AI chat UI

These can be considered only after the core adjudication loop is proven.

## Failure requirements
Handle:
- empty requirements
- malformed evidence URL
- inaccessible evidence
- ambiguous requirement
- invalid evaluator output
- validator disagreement
- duplicate/late submission
- re-evaluation after finalization

## Design principle
The smallest feature that demonstrates a real GenLayer consensus-critical decision is preferred over a large feature set.
