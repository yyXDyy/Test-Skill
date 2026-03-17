# Iteration Stage

## Goal

Run generated scripts, diagnose failures, repair what is repairable, and record the outcome.

## Steps

1. Run the script(s).
2. Classify failures.
3. Repair script-level issues.
4. Re-run as needed.
5. Record what changed.
6. Summarize what actually executed and what did not.

## Common failure classes

- locator issue
- waiting/assertion issue
- data/environment issue
- product behavior mismatch
- perception mistake

## Chrome MCP usage in iteration

Chrome MCP is allowed here only to confirm whether the script failed because the UI was misunderstood.

Examples:
- expected text does not exist
- route changed
- control is present under a different label
- UI state differs from what the script assumed

## MVP repair rule

In MVP:
- repair script-level issues directly
- if the root cause is a perception mistake, record `perception_refresh_needed`
- do not automatically restart perception + generation

## Required output

### `iteration-log.md`
Record:
- run timestamp
- script version tested
- failed cases
- root-cause hypothesis
- repair action
- rerun result
- whether `perception_refresh_needed` was raised
- executed script tests
- mapped case IDs / AC IDs per executed test
- skipped / deferred / not-yet-automated cases
- final coverage conclusion: full in-scope coverage or partial prioritized coverage
