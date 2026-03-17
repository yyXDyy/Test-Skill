#!/usr/bin/env python3
"""Validate minimum runtime artifacts for the PRD-to-UI blackbox workflow."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = {
    "product-module-scope.md": [
        "## 1. 产品识别结果",
        "## 2. PRD中识别到的候选模块",
        "## 3. 本轮锁定模块",
        "## 5. 共用知识判断",
    ],
    "product-shared-context.md": [
        "## 1. 产品级共用能力",
        "## 4. 共用组件 / 共享交互",
        "## 6. 产品级费用 / 配额 / 权限规则",
    ],
    "shared-versions.json": [],
    "platform-context.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 2. 产品语义模型",
        "## 3. 核心业务对象",
        "## 6. PRD术语与UI术语映射",
        "## 8. 用户角色与成功标准",
    ],
    "spec-for-testing.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 3. 术语规范",
        "## 6. Before / After 状态规则",
        "## 6.2 业务结果观察规则",
        "## 8. 自动化边界",
    ],
    "test-model.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 4. 业务结果模型",
        "## 5. 观察点模型",
        "## 9. Reality Check 与 Success Path 分离规则",
    ],
    "requirements-analysis.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 2. 功能点目录",
        "## 3. 原子验收点清单",
        "## 3.1 关键用户旅程",
    ],
    "risk-assessment.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 2. 高价值流程",
        "## 6. 建模风险提示",
        "## 8. 确认状态摘要",
    ],
    "confirmation-status.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 2. 人类确认项清单",
        "## 4. 未确认时采用的默认策略",
        "## 5. 当前允许继续的范围",
    ],
    "exploration-log.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 0. 本轮补证目标",
        "#### 1. 术语与对象观察",
        "#### 3. Before / After 状态对比",
        "#### 4. 与理解层的对照",
    ],
    "coverage-audit.md": [
        "## 基本信息",
        "- 产品名称:",
        "- 模块名称:",
        "| AC# | F# | 优先级 | 对应用例数 | 是否达标 | 业务结果覆盖情况 | 主观察点强度 | 是否依赖未确认项 | 缺口说明 |",
        "## 5. 覆盖质量风险",
        "## 7. 审计结论",
    ],
    "execution-manifest.md": [
        "- 产品名称:",
        "- 模块名称:",
        "| Script Test Title | 脚本位置 | 覆盖Case IDs | 覆盖AC IDs | 覆盖业务对象 | 预期业务结果 | 主观察点 | 是否执行 | 数据影响级别 |",
        "- 断言强度结论: strong / medium / weak",
        "- 依赖的假设 / 未确认项:",
    ],
    "iteration-log.md": [
        "- 产品名称:",
        "- 模块名称:",
        "## 失败记录",
        "## 最终执行清单",
        "## perception_refresh_needed",
    ],
    "versions.json": [],
}

REQUIRED_VERSION_KEYS = {
    "scope",
    "case_version",
    "script_version",
    "based_on",
    "status",
}

REQUIRED_BASED_ON_KEYS = {
    "product_shared",
    "requirements",
    "risk",
    "exploration",
}

REQUIRED_SHARED_VERSION_KEYS = {
    "scope",
    "shared_context_version",
    "based_on",
    "status",
}

REQUIRED_SHARED_BASED_ON_KEYS = {
    "product_module_scope",
}

KV_PATTERN = re.compile(r"^- ([^:]+):\s*(.*)$")
CASE_PACK_SNIPPETS = [
    "- 产品名称:",
    "- 模块名称:",
    "| Case ID | 用例名称 | 所属模块 | 目标业务对象 | 触发动作 | 前置条件 | 步骤描述 | 预期结果 | 主观察点 | 备注 | 用例等级 |",
    "- 来源confirmation status:",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover - surfaced to user
        raise RuntimeError(f"failed to read {path}: {exc}") from exc


def validate_markdown(path: Path, snippets: list[str], errors: list[str]) -> None:
    text = read_text(path)
    for snippet in snippets:
        if snippet not in text:
            errors.append(f"{path.name}: missing required snippet: {snippet}")


def validate_versions(path: Path, errors: list[str]) -> None:
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        return

    missing = sorted(REQUIRED_VERSION_KEYS - payload.keys())
    if missing:
        errors.append(f"{path.name}: missing keys: {', '.join(missing)}")

    based_on = payload.get("based_on")
    if not isinstance(based_on, dict):
        errors.append(f"{path.name}: based_on must be an object")
        return

    missing_based_on = sorted(REQUIRED_BASED_ON_KEYS - based_on.keys())
    if missing_based_on:
        errors.append(
            f"{path.name}: based_on missing keys: {', '.join(missing_based_on)}"
        )


def validate_shared_versions(path: Path, errors: list[str]) -> None:
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        return

    missing = sorted(REQUIRED_SHARED_VERSION_KEYS - payload.keys())
    if missing:
        errors.append(f"{path.name}: missing keys: {', '.join(missing)}")

    scope = payload.get("scope")
    if not isinstance(scope, dict):
        errors.append(f"{path.name}: scope must be an object")
    elif not str(scope.get("product", "")).strip():
        errors.append(f"{path.name}: scope.product must be non-empty")

    based_on = payload.get("based_on")
    if not isinstance(based_on, dict):
        errors.append(f"{path.name}: based_on must be an object")
        return

    missing_based_on = sorted(REQUIRED_SHARED_BASED_ON_KEYS - based_on.keys())
    if missing_based_on:
        errors.append(
            f"{path.name}: based_on missing keys: {', '.join(missing_based_on)}"
        )


def parse_markdown_kv(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in read_text(path).splitlines():
        match = KV_PATTERN.match(line.strip())
        if not match:
            continue
        key, value = match.groups()
        data[key.strip()] = value.strip()
    return data


def load_versions(path: Path) -> dict:
    return json.loads(read_text(path))


def parse_scope_file(path: Path) -> dict[str, str]:
    values = parse_markdown_kv(path)
    return {
        "product_name": values.get("产品名称", "").strip(),
        "current_product": values.get("当前识别的产品", "").strip(),
        "locked_module": values.get("当前锁定模块", "").strip(),
        "module_source": values.get("模块来源", "").strip(),
        "needs_shared_context": values.get("是否需要产品级 shared context", "").strip().lower(),
    }


def get_case_pack_candidates(runtime_dir: Path) -> list[Path]:
    return sorted(runtime_dir.glob("case-pack-v*.md"))


def validate_case_pack(runtime_dir: Path, errors: list[str], warnings: list[str]) -> None:
    case_pack_candidates = get_case_pack_candidates(runtime_dir)
    if not case_pack_candidates:
        errors.append("missing required artifact: case-pack-vN.md")
        return

    latest_case_pack = case_pack_candidates[-1]
    validate_markdown(latest_case_pack, CASE_PACK_SNIPPETS, errors)

    if len(case_pack_candidates) > 1:
        warnings.append(
            f"multiple case packs found, validated latest version: {latest_case_pack.name}"
        )


def product_scope_requires_shared_context(runtime_dir: Path) -> bool:
    scope_path = runtime_dir / "product-module-scope.md"
    if not scope_path.exists():
        return True

    need_shared = parse_scope_file(scope_path)["needs_shared_context"]
    return need_shared in {"yes", "true", "required"}


def validate_product_module_scope_consistency(
    product_runtime_dir: Path,
    module_dirs: list[Path],
    errors: list[str],
    warnings: list[str],
    strict: bool,
) -> None:
    scope_path = product_runtime_dir / "product-module-scope.md"
    if not scope_path.exists():
        return

    scope = parse_scope_file(scope_path)
    scope_product = scope["current_product"] or scope["product_name"]
    locked_module = scope["locked_module"]
    module_source = scope["module_source"]

    if not scope_product:
        add_issue(strict, errors, warnings, "product-module-scope.md: 产品名称 / 当前识别的产品 is empty")

    if not locked_module:
        add_issue(strict, errors, warnings, "product-module-scope.md: 当前锁定模块 is empty")

    if not module_source:
        add_issue(strict, errors, warnings, "product-module-scope.md: 模块来源 is empty")

    module_names = {module_dir.name for module_dir in module_dirs}
    if locked_module and locked_module not in module_names and module_source != "产品级公共范围":
        add_issue(
            strict,
            errors,
            warnings,
            f"product-module-scope.md: 当前锁定模块 '{locked_module}' not found in runtime modules {sorted(module_names)}",
        )

    for module_dir in module_dirs:
        versions_path = module_dir / "versions.json"
        if not versions_path.exists():
            continue
        try:
            versions = load_versions(versions_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{module_dir.name}: versions.json invalid during product scope consistency check: {exc}")
            continue

        scope_json = versions.get("scope", {})
        module_product = str(scope_json.get("product", "")).strip()
        module_name = str(scope_json.get("module", "")).strip()

        if scope_product and module_product and scope_product != module_product:
            errors.append(
                f"{module_dir.name}: versions.json scope.product '{module_product}' does not match product-module-scope '{scope_product}'"
            )

        if locked_module and module_name and module_name == module_dir.name and locked_module != module_name:
            warnings.append(
                f"{module_dir.name}: current locked module in product-module-scope is '{locked_module}', this module runtime targets '{module_name}'"
            )

        req_path = module_dir / "requirements-analysis.md"
        if req_path.exists():
            req_values = parse_markdown_kv(req_path)
            req_product = req_values.get("产品名称", "").strip()
            req_module = req_values.get("模块名称", "").strip()
            if scope_product and req_product and req_product != scope_product:
                errors.append(
                    f"{module_dir.name}: requirements-analysis 产品名称 '{req_product}' differs from product-module-scope '{scope_product}'"
                )
            if locked_module and req_module and req_module != locked_module and req_module == module_dir.name:
                warnings.append(
                    f"{module_dir.name}: requirements-analysis 模块名称 '{req_module}' differs from product-module-scope 当前锁定模块 '{locked_module}'"
                )

        for filename in ("platform-context.md", "confirmation-status.md"):
            path = module_dir / filename
            if not path.exists():
                continue
            values = parse_markdown_kv(path)
            file_product = values.get("产品名称", "").strip()
            if scope_product and file_product and file_product != scope_product:
                errors.append(
                    f"{module_dir.name}: {filename} 产品名称 '{file_product}' differs from product-module-scope '{scope_product}'"
                )


def add_issue(strict: bool, errors: list[str], warnings: list[str], message: str) -> None:
    if strict:
        errors.append(message)
    else:
        warnings.append(message)


def validate_scope_consistency(
    runtime_dir: Path, errors: list[str], warnings: list[str], strict: bool
) -> None:
    versions_path = runtime_dir / "versions.json"
    if not versions_path.exists():
        return

    try:
        versions = load_versions(versions_path)
    except json.JSONDecodeError as exc:
        errors.append(f"{versions_path.name}: invalid JSON during scope consistency check: {exc}")
        return

    scope = versions.get("scope")
    if not isinstance(scope, dict):
        errors.append(f"{versions_path.name}: scope must be an object")
        return

    product = str(scope.get("product", "")).strip()
    module = str(scope.get("module", "")).strip()
    if not product:
        errors.append(f"{versions_path.name}: scope.product must be non-empty")
    if not module:
        errors.append(f"{versions_path.name}: scope.module must be non-empty")

    expected_files = {
        "platform-context.md": ("产品名称", "模块名称"),
        "requirements-analysis.md": ("产品名称", "模块名称", "模块来源"),
        "confirmation-status.md": ("产品名称", "模块名称"),
    }

    for filename, keys in expected_files.items():
        path = runtime_dir / filename
        if not path.exists():
            continue
        values = parse_markdown_kv(path)
        if "产品名称" in keys:
            file_product = values.get("产品名称", "").strip()
            if file_product and product and file_product != product:
                errors.append(
                    f"{filename}: 产品名称 '{file_product}' does not match versions.json scope.product '{product}'"
                )
            elif not file_product:
                add_issue(strict, errors, warnings, f"{filename}: 产品名称 is empty")
        if "模块名称" in keys:
            file_module = values.get("模块名称", "").strip()
            if file_module and module and file_module != module:
                errors.append(
                    f"{filename}: 模块名称 '{file_module}' does not match versions.json scope.module '{module}'"
                )
            elif not file_module:
                add_issue(strict, errors, warnings, f"{filename}: 模块名称 is empty")
        if "模块来源" in keys:
            module_source = values.get("模块来源", "").strip()
            if not module_source:
                add_issue(strict, errors, warnings, f"{filename}: 模块来源 is empty")

    dir_name = runtime_dir.name.strip()
    if module and dir_name and dir_name != module:
        add_issue(
            strict,
            errors,
            warnings,
            f"{runtime_dir.name}: directory name does not match versions.json scope.module '{module}'",
        )


def validate_module_runtime(
    runtime_dir: Path, require_product_shared: bool, strict: bool
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not runtime_dir.exists():
        return [f"runtime directory does not exist: {runtime_dir}"], warnings

    if not runtime_dir.is_dir():
        return [f"runtime path is not a directory: {runtime_dir}"], warnings

    required = dict(REQUIRED_FILES)
    if not require_product_shared:
        required.pop("product-shared-context.md", None)
        required.pop("product-module-scope.md", None)
        required.pop("shared-versions.json", None)

    for filename, snippets in required.items():
        path = runtime_dir / filename
        if not path.exists():
            errors.append(f"missing required artifact: {filename}")
            continue

        if filename.endswith(".md"):
            validate_markdown(path, snippets, errors)
        elif filename == "shared-versions.json":
            validate_shared_versions(path, errors)
        elif filename == "versions.json":
            validate_versions(path, errors)

    validate_case_pack(runtime_dir, errors, warnings)

    script_files = sorted((runtime_dir / "scripts").glob("**/*")) if (runtime_dir / "scripts").exists() else []
    if not script_files:
        warnings.append("no script files found under runtime/blackbox/scripts")

    validate_scope_consistency(runtime_dir, errors, warnings, strict)

    return errors, warnings


def detect_module_dirs(runtime_dir: Path) -> list[Path]:
    module_dirs: list[Path] = []
    for child in sorted(runtime_dir.iterdir()):
        if child.is_dir() and (child / "versions.json").exists():
            module_dirs.append(child)
    return module_dirs


def validate_runtime(runtime_dir: Path, strict: bool) -> tuple[list[str], list[str]]:
    if not runtime_dir.exists():
        return [f"runtime directory does not exist: {runtime_dir}"], []

    if not runtime_dir.is_dir():
        return [f"runtime path is not a directory: {runtime_dir}"], []

    module_dirs = detect_module_dirs(runtime_dir)
    if module_dirs:
        all_errors: list[str] = []
        all_warnings: list[str] = []

        scope_file = runtime_dir / "product-module-scope.md"
        if not scope_file.exists():
            all_errors.append(
                f"missing required product-level artifact for multi-module runtime: {scope_file.name}"
            )
        else:
            validate_markdown(scope_file, REQUIRED_FILES["product-module-scope.md"], all_errors)
            validate_product_module_scope_consistency(
                runtime_dir, module_dirs, all_errors, all_warnings, strict
            )

        product_shared = runtime_dir / "product-shared-context.md"
        shared_versions = runtime_dir / "shared-versions.json"
        if not shared_versions.exists():
            all_errors.append(
                f"missing required product-level artifact for multi-module runtime: {shared_versions.name}"
            )
        else:
            validate_shared_versions(shared_versions, all_errors)

        if product_scope_requires_shared_context(runtime_dir):
            if not product_shared.exists():
                all_errors.append(
                    f"missing required product-level artifact for multi-module runtime: {product_shared.name}"
                )
            else:
                validate_markdown(
                    product_shared,
                    REQUIRED_FILES["product-shared-context.md"],
                    all_errors,
                )
        elif product_shared.exists():
            validate_markdown(
                product_shared,
                REQUIRED_FILES["product-shared-context.md"],
                all_errors,
            )

        for module_dir in module_dirs:
            errors, warnings = validate_module_runtime(
                module_dir, require_product_shared=False, strict=strict
            )
            all_errors.extend([f"{module_dir.name}: {item}" for item in errors])
            all_warnings.extend([f"{module_dir.name}: {item}" for item in warnings])
        return all_errors, all_warnings

    return validate_module_runtime(runtime_dir, require_product_shared=False, strict=strict)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate minimum runtime artifacts for prd-to-ui-blackbox-testing."
    )
    parser.add_argument(
        "runtime_dir",
        nargs="?",
        default="runtime/blackbox",
        help="Path to the runtime artifact directory. Default: runtime/blackbox",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat scope empties and module-directory mismatches as validation errors.",
    )
    args = parser.parse_args()

    runtime_dir = Path(args.runtime_dir).expanduser().resolve()
    errors, warnings = validate_runtime(runtime_dir, strict=args.strict)

    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- {item}")
    else:
        print("VALIDATION PASSED")

    if warnings:
        print("WARNINGS")
        for item in warnings:
            print(f"- {item}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
