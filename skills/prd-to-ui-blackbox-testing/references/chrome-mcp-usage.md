# Chrome MCP Usage Rules

## Goal

Define when Chrome MCP should be used during PRD-driven black-box UI testing, what it should collect, and what it should not be used for.

## Core principle

Use Chrome MCP as a **perception and verification tool**, not as the final delivery layer.

That means:
- use it to understand the real product UI
- use it to reduce ambiguity before script writing
- use it to verify whether script failures come from incorrect UI understanding
- do not treat raw exploration output as the final test script deliverable
- use it to gather evidence that can update or validate the understanding-layer product model

---

## 1. When Chrome MCP should be used

Use Chrome MCP in these situations:

### A. Perception stage is active
Use Chrome MCP to:
- navigate the real product UI
- inspect routes, pages, dialogs, forms, and visible state
- verify whether PRD expectations match what exists in the environment
- collect browser-native evidence that the AI can reason about
- validate terminology, object relationships, and success evidence used later in case design

### B. Iteration stage indicates possible understanding error
Use Chrome MCP to confirm whether a failure came from:
- wrong route assumption
- wrong control label or location
- wrong visible text expectation
- wrong state transition assumption
- actual product/PRD mismatch

### C. Mixed UI/API disagreement needs browser-side evidence
Use Chrome MCP when browser-side facts are needed for conflict review, especially:
- screenshot evidence
- console error evidence
- network request evidence

---

## 2. When Chrome MCP should NOT be the default choice

Do not prefer Chrome MCP when the main task is:

- producing the final maintainable regression script after the flow is already well understood
- organizing large-scale test suites, fixtures, projects, retries, or CI execution
- writing long-term maintainable Playwright test code as the primary activity
- replacing formal case design with free-form exploration

In those cases, use Chrome MCP only as supporting evidence or reality-check input.

---

## 3. Default perception workflow

Use this default sequence during perception:

```text
navigate -> snapshot -> inspect -> optional interaction -> verify -> log
```

### Step 1: navigate
Open the relevant route or page.

### Step 2: snapshot
Capture a text-structured view of the page first.

### Step 3: inspect
Identify:
- major regions
- visible controls
- expected action entry points
- text and state relevant to the PRD

### Step 4: optional interaction
Only interact when needed to reveal the next UI state.

### Step 5: verify
Confirm whether the observed state matches the intended PRD flow.

### Step 6: log
Record the exploration result in `exploration-log.md`.

---

## 4. Preferred evidence order

Use evidence in this order of preference:

1. snapshot
2. screenshot, only when visual proof matters
3. console data, when failure or ambiguity suggests frontend issues
4. network data, when request/response behavior matters

### Why this order

- snapshot is lightweight and AI-readable
- screenshot helps humans verify visual reality
- console/network are more expensive and should be collected intentionally

---

## 5. What to collect in perception

Collect facts, not guesses.

Good perception outputs include:
- route reached
- page title or visible heading
- visible buttons/links/inputs relevant to the flow
- required preconditions discovered in the UI
- state transitions after key actions
- mismatches between PRD wording and real UI wording
- discovered ambiguity that will affect case assembly or scripting
- evidence that confirms or weakens the current object model
- evidence that shows whether a business-result claim has strong or weak UI proof

Bad perception outputs include:
- inferred backend behavior without evidence
- final verdicts about requirements without human confirmation
- script-level assumptions presented as observed fact

---

## 6. Rules for optional interaction

Interaction is allowed during perception, but keep it minimal and purposeful.

Allowed purposes:
- reveal the next step in a user flow
- confirm whether an expected control or dialog appears
- verify whether a state transition exists
- confirm whether visible labels/text differ from PRD assumptions

Avoid:
- destructive actions unless explicitly approved
- broad uncontrolled exploration with no logging
- treating perception as unscripted manual QA wandering

---

## 7. Iteration-stage usage rules

During iteration, Chrome MCP should be used only to reduce uncertainty.

Use it to answer questions like:
- does the expected text actually exist?
- did the route change?
- did the control label change?
- is the script waiting for the wrong state?
- is the UI behaving differently than the PRD implied?

Do not use it to hide poor script discipline.
If the problem is clearly a locator/wait/assertion issue already visible from test output, repair the script directly.

---

## 8. Relation to script production

Chrome MCP informs script production, but does not replace it.

Use Chrome MCP outputs as inputs to:
- test element decomposition
- case assembly
- locator strategy decisions
- expected visible-state decisions

Then write the actual script separately.

---

## 9. Minimum logging requirement

Every Chrome MCP exploration pass should leave a trace in `exploration-log.md`.

Record at minimum:
- timestamp
- objective
- route/page visited
- observed UI facts
- interactions performed
- mismatch against PRD, if any
- mismatch against current understanding artifacts, if any
- understanding gaps reduced or still open
- artifact refs captured

If no log entry was made, the perception work is incomplete.

---

## 10. MVP constraints

For MVP:
- run one intentional perception pass
- avoid broad exploratory branching
- prefer snapshot-first inspection
- only collect screenshot/console/network when needed
- if iteration reveals a perception problem, record `perception_refresh_needed` instead of auto-looping

---

## 11. Decision summary

### Use Chrome MCP when:
- real UI understanding is incomplete
- PRD needs validation against the actual product
- browser-side evidence is needed
- script failure may come from misunderstanding the UI

### Do not default to Chrome MCP when:
- the task is now primarily script engineering
- the flow is already understood
- the need is maintainable regression code rather than exploration
