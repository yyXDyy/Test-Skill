# Artifacts and Versioning

## Runtime working area

Use:

```text
runtime/<product>/
├── product-module-scope.md
├── product-shared-context.md
├── shared-versions.json
├── <module-a>/
│   ├── platform-context.md
│   ├── spec-for-testing.md
│   ├── test-model.md
│   ├── requirements-analysis.md
│   ├── risk-assessment.md
│   ├── confirmation-status.md
│   ├── exploration-log.md
│   ├── case-pack-v1.md
│   ├── coverage-audit.md
│   ├── execution-manifest.md
│   ├── iteration-log.md
│   └── versions.json
└── <module-b>/
    └── ...
```

If the task is truly single-module and no product-level shared knowledge is needed yet, `runtime/blackbox/` is still acceptable for MVP.

## Minimum required artifacts

### Understanding
- `product-module-scope.md`
- `product-shared-context.md` when multiple modules share product knowledge
- `platform-context.md`
- `spec-for-testing.md`
- `test-model.md`
- `requirements-analysis.md`
- `risk-assessment.md`
- `confirmation-status.md`

### Perception
- `exploration-log.md`

### Generation
- `case-pack-vN.md`
- `coverage-audit.md`
- `execution-manifest.md`
- script files
- `versions.json`

### Iteration
- `iteration-log.md`

## Version rules

Track versions at minimum for:
- case pack
- script output
- shared product context when product-level context exists

A simple JSON shape is enough for MVP:

```json
{
  "scope": {
    "product": "sealos",
    "module": "Admin"
  },
  "case_version": "v1",
  "script_version": "v1",
  "based_on": {
    "product_shared": "../product-shared-context.md",
    "requirements": "requirements-analysis.md",
    "risk": "risk-assessment.md",
    "exploration": "exploration-log.md"
  },
  "status": "draft"
}
```

For product-level shared context, use a separate metadata file:

```json
{
  "scope": {
    "product": "sealos"
  },
  "shared_context_version": "v1",
  "based_on": {
    "product_module_scope": "product-module-scope.md"
  },
  "status": "draft"
}
```

## Delivery check

Before claiming delivery, verify that:
- strict runtime validation has been run:
  - `cd <skill-root> && python3 scripts/validate_runtime.py runtime/<product> --strict`
- product/module scope is recorded clearly before module-level artifact production
- product-level shared context exists when multiple modules share business rules, terminology, billing, permissions, or components
- product-level shared versions metadata exists for multi-module product runs
- all stage artifacts exist
- script version is identified
- coverage audit exists and has no hidden gaps
- execution manifest exists and explains what was actually automated
- platform context exists and explains what system is being tested
- spec for testing exists and normalizes PRD + UI reality
- test model exists and explains how the platform should be tested
- confirmation status exists and makes the human interaction outcome explicit
- known limitations are stated
- open ambiguities are stated
- if coverage is partial, the uncovered scope is listed explicitly
- if product-level rules affect the module, the module artifacts reference that shared context explicitly

In strict mode, at minimum these become blocking errors:
- empty product name in module artifacts
- empty module name in module artifacts
- empty module source in `requirements-analysis.md`
- module directory name not matching `versions.json.scope.module`
- product/module scope facts conflicting across `product-module-scope.md`, module artifacts, and `versions.json`
