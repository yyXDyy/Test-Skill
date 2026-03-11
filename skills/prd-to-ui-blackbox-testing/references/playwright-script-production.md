# Playwright Script Production

## Goal

Turn understanding outputs and perception outputs into black-box UI automation scripts that are usable, reviewable, and maintainable.

This stage produces the script deliverable. Chrome MCP informs the script, but the final output here is Playwright code or an equivalent black-box UI automation script artifact.

---

## 1. Required inputs

Do not write the script from memory alone. Use these inputs explicitly:

- `requirements-analysis.md`
- `risk-assessment.md`
- `exploration-log.md`
- the selected case pack version

If one of these inputs is missing, say so and stop or ask for clarification.

---

## 2. What script production must do

Script production should:
- convert observed UI behavior into executable black-box steps
- preserve traceability back to requirements and perception
- use stable locator and waiting practices
- avoid guessing when the UI is still ambiguous
- produce versioned script output

Script production should not:
- replace missing perception with invented selectors
- replace missing requirements with assumed assertions
- silently downgrade risky assertions into weak checks

---

## 3. Production order

Follow this order:

1. read the selected requirement/risk/perception artifacts
2. select the target cases for scripting
3. convert each case into:
   - preconditions
   - navigation steps
   - action steps
   - visible assertions
4. choose locator strategy
5. choose waiting/assertion strategy
6. write the script
7. update version metadata

---

## 4. Locator rules

Use Playwright locator strategy in this order of preference:

1. role-based locators
2. label/placeholder/text locators
3. test ids
4. CSS/XPath only as last resort

Examples of preferred patterns:
- `getByRole()`
- `getByLabel()`
- `getByPlaceholder()`
- `getByText()`
- `getByTestId()`

Avoid:
- long brittle CSS chains
- index-heavy selectors unless unavoidable
- selectors invented without support from perception evidence

If a selector is uncertain, record that uncertainty instead of pretending confidence.

---

## 5. Waiting and assertion rules

Prefer Playwright web-first assertions over arbitrary sleeps.

Preferred patterns:
- `await expect(locator).toBeVisible()`
- `await expect(locator).toHaveText(...)`
- `await expect(page).toHaveURL(...)`
- explicit wait-for-response only when network behavior is central to the case

Avoid:
- `waitForTimeout()` as a primary strategy
- fixed sleeps in place of UI or network conditions
- weak assertions that only check that the page did not crash

If the script depends on a state transition, assert the state transition explicitly.

---

## 6. Black-box boundary rules

Keep the produced script black-box by default.

That means:
- assert user-visible states first
- prefer visible text, role, label, URL, enabled/disabled state, count, and presence
- do not default to internal JS state checks
- do not default to browser-side `evaluate()` style checks unless the user explicitly wants hybrid or debug-oriented coverage

Chrome MCP exploration can discover facts, but the script should still validate the product from the user's perspective whenever possible.

---

## 7. Script structure rules

Each generated script should clearly show:
- scenario goal
- preconditions or setup assumptions
- action sequence
- assertions
- any known fragile point

At minimum, keep the script understandable enough that a QA engineer can review it quickly.

If multiple cases are generated, organize them by:
- smoke / core / edge
or
- feature / page / journey

---

## 8. Versioning rules

Every script production pass should update version metadata.

Track at least:
- `case_version`
- `script_version`
- the requirement/risk/perception artifacts used as source
- current status (`draft`, `repairing`, `ready_for_delivery`)

If the script changed because of a failed run, reflect that in version/status notes.

---

## 9. Failure-aware writing

When writing the first version of a script, proactively avoid common flaky-test causes:

- brittle selectors
- implicit timing assumptions
- hidden dependency on shared data
- assertions that depend on unstable copy without noting it
- navigation assumptions without URL or visible-state verification

If a step seems likely to be flaky, call it out in the case/script notes.

---

## 10. Interaction with Chrome MCP

Chrome MCP is allowed to inform script production, but should not become the script itself.

Use Chrome MCP outputs to answer questions like:
- what route is correct?
- what label does the button actually use?
- what visible state appears after the action?
- what controls exist on the real page?

Then write the script in Playwright.

---

## 11. MVP delivery standard

For MVP, a script is considered acceptable for delivery when:
- it maps back to a defined case
- it uses supported locator and waiting practices
- it has at least one clear user-visible assertion per important step
- known limitations are stated
- version metadata is updated

---

## 12. Recommended reference themes from Playwright best practices

When strengthening this stage, prefer guidance in these areas:
- locator strategy
- assertions and waiting
- flaky-test prevention
- debugging
- console error handling where relevant

These themes are more useful to MVP black-box script production than the broader Playwright surface area.
