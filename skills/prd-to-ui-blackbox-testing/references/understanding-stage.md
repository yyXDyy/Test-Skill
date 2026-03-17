# Understanding Stage

## Goal

Read the PRD and produce a human-reviewable understanding of what should be tested and what is risky.
This stage must also teach the model what kind of platform it is testing, so later case design uses domain semantics instead of only generic UI structure.
The understanding stage is successful only when it builds a usable product mental model, not when it merely summarizes PRD sections.

## Inputs

- product name
- PRD markdown or PDF
- optional environment notes
- optional user scope constraints

## Steps

1. Confirm what product is being tested.
2. Read the PRD.
3. Extract candidate modules from the PRD and decide whether module scope is clear enough.
4. Build a platform/domain model from the PRD.
5. Extract product flows, modules, and expected user-visible behavior.
6. Extract ambiguity, missing details, and test data assumptions.
7. Model the business objects, object relationships, user roles, and success criteria behind the UI.
8. Normalize terminology that may drift between PRD wording, product UI wording, and domain wording.
9. Assess risk by path, module, and user impact.
10. Ask for human confirmation of understanding and risk priority.

## Product and module identification rule

Do not start module-level artifact production until the product is clear.

Use this order:
1. identify the product from user input or PRD title/context
2. extract candidate modules from the PRD
3. if one module is clearly in scope, proceed with that module
4. if multiple modules are present or the module boundary is unclear, ask the user which module should be the current testing target

Do not guess the target module when:
- the PRD spans multiple modules
- the PRD uses product-level language without clear module ownership
- the same flow touches shared components and more than one module

Record the result in `product-module-scope.md` before writing module-level understanding artifacts.

## Human confirmation protocol

The model must not treat “需要人类确认的点” as a decorative section.

Before moving to perception, provide the human with:
- a one-paragraph summary of the current understanding
- the identified product and target module
- a short list of confirmation items
- the default assumption that will be used if an item remains unanswered
- a clear note on which unanswered items are safe to carry forward and which would block later stages

Then record the outcome explicitly:
- confirmed
- corrected
- unanswered but assumed

Group confirmation items explicitly when possible:
- product / module scope confirmation
- object model confirmation
- terminology confirmation
- success-criteria confirmation
- risky boundary / destructive-action confirmation
- environment / data precondition confirmation

If an unanswered item affects destructive actions, environment switching, or interpretation of success criteria:
- do not proceed with that risky action
- either narrow scope or stop and wait for human input
If an unanswered item affects only wording precision or low-risk object detail:
- record it as `assumed`
- state exactly which later artifacts are affected

## Required outputs

### `product-module-scope.md`
Include:
- identified product
- PRD-derived candidate modules
- current target module
- whether the target module came from PRD extraction or user confirmation
- excluded modules for this run
- whether product-level shared context is needed
- blocking scope ambiguities if any

### `platform-context.md`
Include:
- platform name
- platform type
- platform classification used for testing
- core business entities
- entity relationships
- key business actions
- business-result definition for important actions
- platform-specific terminology
- terms that may be confused with adjacent platforms
- PRD wording that needs later UI verification
- role-specific success criteria
- product-understanding risks and default assumptions

This file should answer questions like:
- what kind of system is this?
- what are its first-class business objects?
- what user-visible actions change those objects?
- what terms must later be normalized if the UI wording differs from the PRD?

### `spec-for-testing.md`
Include:
- normalized terminology
- feature specs rewritten for testing
- acceptance rules with current evidence source
- before/after state rules
- business-result observation rules
- reality gaps between PRD and current UI
- automation boundary

This file should answer:
- what should be tested according to PRD plus observed reality?
- which expected behaviors are fully verified, partially verified, or still blocked?

### `test-model.md`
Include:
- test object model
- object relationships
- business-result model
- observation points
- primary / secondary / weak observation point separation
- test layer model (structure / precondition / business result / linkage / reality-check)
- current coverage layer summary
- next highest-value coverage areas

This file should answer:
- how should the platform be tested?
- which cases belong to visibility, business-result, or state-linkage coverage?

### `requirements-analysis.md`
Include:
- product name
- target module name
- whether the module came from PRD extraction or user confirmation
- summary of target scope
- user journeys
- key pages/modules
- acceptance behavior
- related business objects and expected outcomes
- ambiguity list
- out-of-scope notes if any

### `risk-assessment.md`
Include:
- high-risk flows
- high-value flows
- likely brittle areas
- data/environment dependencies
- modeling risks caused by terminology or object-relationship uncertainty
- recommended execution priority
- points requiring human confirmation
- confirmation status for each point

### `confirmation-status.md`
Include:
- current understanding summary
- categorized confirmation items
- default assumptions for unanswered items
- blocking vs non-blocking distinction
- allowed next-stage scope under current confirmation status
- understanding corrections and which artifacts were updated

## Gate

Do not enter perception until the human has confirmed or corrected the analysis/risk view.
Do not enter perception if the product is still unclear.
Do not enter perception if the target module is still ambiguous for a multi-module PRD.
Do not treat a page as generic CRUD UI if the platform context shows domain-specific semantics such as repo/version/tag/image/artifact/task.
Do not leave the understanding stage with only page-level descriptions. At minimum, the outputs must explain:
- what the core objects are
- what business action changes those objects
- what user-visible evidence proves that the change happened
- which terms are stable and which still need confirmation
Do not record confirmation status as a flat checklist only. The confirmation output must make it obvious:
- what was actually confirmed by the human
- what remained unanswered but was assumed
- what assumptions narrow the safe scope of testing
- which later artifacts need to change if a confirmation item is corrected
If the human has not responded in full, record the assumptions explicitly and state why it is still safe to continue with the reduced scope.
