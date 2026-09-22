#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tool_integrity.py — 核心工具完整性校验（498 任务 3 / P1-10 / 488 安全性与信任模型）。

为什么（488）：门禁的全部可信度最终落在 5 个核心工具上——它们能改写"什么算通过"。
若工具被静默篡改（供应链攻击 / 本地误改未察觉），后续所有 replay/gate 结论都不可信。
本工具给这 5 个文件建 sha256 基准，把"被改过"变成一条可复现命令。

用法与退出码
============
    python tools/tool_integrity.py --update   # 计算 sha256 写 tools/.tool_checksums，exit 0
    python tools/tool_integrity.py --check    # 独立验证：全匹配 exit 0 / 有改动 exit 1 / 缺基准 exit 2
    python tools/tool_integrity.py            # 同上（无参数的默认动作就是比对，--check 是显式别名）

567 任务 1：`--check` 是**独立验证入口**（此前只有 `--update`，"钉完无法独立复核"）。
567 任务 2：`enforce()` 供**判定入口**（gate_engine / atom_evidence_replay / poison_drill 的
`main()` 首行）强制调用——核心被改动且未重钉就 **fail-loud 拒绝运行**，而不是照跑规则把
"判定核心已被改"静默放行（564 PoC#1/#2 的实锤根因）。

601 任务 1.2：`--check` 默认同时校验**目录级 Merkle 根**（`merkle_integrity.check_all()`），
`--update` 默认**先重建 Merkle 根再钉**（顺序有意义：台账变了它自己的 hash 也变）。
`--no-check-merkle` / `--no-update-merkle` 可跳过；缺 Merkle 台账按"副本/部分检出"当警告。

601 任务 0.3：哈希面从"工具"扩到"**信任根数据**"（`SUPPLY_CHAIN_FILES`，与 CORE_TOOLS 并列不混）：
毒样例豁免台账 / 毒样例覆盖率台账 / 治理文档 manifest / Merkle 根 / in-toto layout ——
改它们不动一行代码却能改"什么算通过"（585 攻击1/2 的真盲点）。判定口径见 `verify_supply_chain()`：
**只有内容变更算红**，未钉/缺文件只警告（副本与部分检出下无判别力）。

诚实边界：`.tool_checksums` 自身**不纳入校验**（否则要签它自己，递归无解）——
它的可信度依赖 git 历史（谁改了基准会留痕）。基准的更新必须在**功能改动 commit 之后**
执行（498 的顺序依赖：任务 2 改 gate_engine.py ⇒ 任务 3 才生成基准）。
由 567 起，改这五个文件后**必须** `--update` 重钉，否则下次任何判定入口自红——这是设计目标
（改判定核心必须显式留痕），不是 bug。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)
from utf8_console import ensure_utf8

ROOT = _queyi_root()
TOOLS = ROOT / "tools"
CHECKSUMS = TOOLS / ".tool_checksums"

# 核心工具（改它们就等于改"什么算通过"）
CORE_TOOLS: tuple[str, ...] = (
    "gate_engine.py",
    "atom_evidence_replay.py",
    "poison_drill.py",
    "toolchain.py",
    "cppbible.py",
)

# 591 任务 3：**测试器配置**（A2 防御）——与 CORE_TOOLS 并列、不合并。
# 病（590）：`tests/conftest.py` 在收集前执行，可通过 `pytest_runtest_makereport` 把 failed 改判
#   passed，但它不在 CORE_TOOLS、无完整性校验 ⇒ 篡改它可让"pytest 全绿"而判决被全面抽空。
#   把"跑测试的配置"也钉进哈希面：conftest（钩子）+ pyproject（pytest markers/addopts/ruff select）。
#   注意它们是 **ROOT 相对路径**（不在 tools/ 下），故走独立的 compute/verify 路径。
TEST_CONFIG_TOOLS: tuple[str, ...] = (
    "tests/conftest.py",
    "pyproject.toml",
)
_TEST_CONFIG_MARK = "# test_config"          # .tool_checksums 里的节标记


# 601 任务 0.3：**信任根数据文件**（方案 A：与 CORE_TOOLS 分开管理，语义不混）。
# 病（600 调研 · 585 攻击1 的真盲点）：tool_integrity 只钉"5 个工具 + 2 个测试配置"，
#   而"什么算通过"还依赖一批**数据**：毒样例豁免台账（攻击2 的"自写自验"面）、毒样例覆盖率台账、
#   治理文档 manifest —— 改它们不动一行代码、checksum 全绿。本批把它们钉进哈希面。
# 路径一律 **ROOT 相对**（与 test_config 节同风格）；**注意**：规则定义**内嵌在 gate_engine.py**
#   里（实测：无独立规则文件）⇒ 规则面的完整性由 CORE_TOOLS 的 gate_engine.py 覆盖，见 worklog D1。
# `data/supply_chain/merkle_roots.json` / `layout.json` 由 601 任务1/2 产出，产出后同 commit 重钉。
SUPPLY_CHAIN_FILES: tuple[str, ...] = (
    "tools/poison_exemptions.yaml",           # 毒样例豁免台账（581）
    "tools/poison_surface_map.json",          # 毒样例覆盖率台账（586）
    "data/governance_docs_manifest.json",     # 治理文档清单（591；自校验见 task 0.4）
    "data/supply_chain/merkle_roots.json",    # 601 任务1：目录 Merkle 根
    "data/supply_chain/layout.json",          # 601 任务2：in-toto layout
)
_SUPPLY_CHAIN_MARK = "# supply_chain"        # .tool_checksums 里的节标记

# 615 B3：**判决尺子**（决定 pass/fail 的逻辑；_arch_v19 探针实测 11 关键尺子中 8 个裸露）。
#   与 CORE_TOOLS 并列：这些尺子改一行即可改"什么算通过"，但此前不在哈希面。
#   `tool_integrity.py` 自身也纳入（"怎么算"即可被篡改）；`.tool_checksums` 仍不纳入（递归无解）。
#   语义：**内容变更或缺失都算红**（尺子必须存在且不被静默改）——同 test_config 节口径。
RULER_TOOLS: tuple[str, ...] = (
    "mutation_fuzz.py",              # 变异发现器（改它可让逃逸样本消失）
    "golden_lock.py",                # 决定质量基线（改它可让恶化不红）
    "replay_invariants.py",          # 决定 replay 不变量
    "d5_compile_gate.py",            # D5 编译门
    "d5_runtime_gate.py",            # D5 运行门
    "d5_source_integrity.py",        # D5 源完整性
    "attack_edge_generator.py",      # 攻击边生成（决定 W2 图）
    "bkt_solver.py",                 # BKT 求解（决定学习者判决）
    "learner_mastery_update_613.py",  # 掌握度更新
    "tool_integrity.py",             # 元校验器自身
)
_RULER_MARK = "# ruler"                      # .tool_checksums 里的节标记


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def compute(tools_dir: Path | None = None,
            names: tuple[str, ...] = CORE_TOOLS) -> dict[str, str]:
    d = tools_dir or TOOLS
    return {n: sha256_of(d / n) for n in names if (d / n).is_file()}


def write_baseline(path: Path | None = None, tools_dir: Path | None = None,
                   names: tuple[str, ...] = CORE_TOOLS) -> Path:
    """写基准。`names` 可覆盖（测试用假工具目录时必须传，否则算出来是空基准）。"""
    dst = path or CHECKSUMS
    rows = compute(tools_dir, names)
    dst.write_text("".join(f"{h}  {n}\n" for n, h in sorted(rows.items())),
                   encoding="utf-8")
    return dst


def load_baseline(path: Path | None = None) -> dict[str, str] | None:
    """解析 `<sha256>  <filename>`（**只读 core 节**）；缺失 → None（调用方须 exit 2，不静默放行）。

    591：遇 `#` 注释/节标记即**停止**——core 节在前，`# test_config` 之后的条目不进 core 基准
    （否则 `verify()` 会把 `tests/conftest.py` 当"tools/ 下缺失"而误报）。
    """
    src = path or CHECKSUMS
    if not src.is_file():
        return None
    out: dict[str, str] = {}
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.lstrip().startswith("#"):
            break
        parts = line.split()
        if len(parts) == 2:
            out[parts[1]] = parts[0]
    return out


def load_test_config_baseline(path: Path | None = None) -> dict[str, str] | None:
    """解析 `.tool_checksums` 的 `# test_config` 节；节缺失 → None。"""
    src = path or CHECKSUMS
    if not src.is_file():
        return None
    out: dict[str, str] = {}
    in_sec = False
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.lstrip().startswith("#"):
            in_sec = _TEST_CONFIG_MARK in line
            continue
        if in_sec:
            parts = line.split()
            if len(parts) == 2:
                out[parts[1]] = parts[0]
    return out or None


def compute_test_config(root: Path | None = None,
                        names: tuple[str, ...] = TEST_CONFIG_TOOLS) -> dict[str, str]:
    d = root or ROOT
    return {n: sha256_of(d / n) for n in names if (d / n).is_file()}


def write_test_config_baseline(path: Path | None = None, root: Path | None = None,
                               names: tuple[str, ...] = TEST_CONFIG_TOOLS) -> Path:
    """把 test_config 节**追加**到基准文件末（须先 `write_baseline` 覆盖 core 段 ⇒ 不重复）。"""
    dst = path or CHECKSUMS
    rows = compute_test_config(root, names)
    with dst.open("a", encoding="utf-8") as f:
        f.write(_TEST_CONFIG_MARK + "\n")
        for n, h in sorted(rows.items()):
            f.write(f"{h}  {n}\n")
    return dst


def verify_test_config(path: Path | None = None, root: Path | None = None
                       ) -> tuple[list[tuple[str, str, str]], list[str], int]:
    """校验 test_config 节；返回 (changed, missing, exit_code)（缺节/缺基准 → 2）。"""
    base = load_test_config_baseline(path)
    if base is None:
        return [], [], 2
    d = root or ROOT
    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []
    for name, want in sorted(base.items()):
        f = d / name
        if not f.is_file():
            missing.append(name)
            continue
        got = sha256_of(f)
        if got != want:
            changed.append((name, want, got))
    return changed, missing, (0 if not changed and not missing else 1)


def load_supply_chain_baseline(path: Path | None = None) -> dict[str, str] | None:
    """解析 `.tool_checksums` 的 `# supply_chain` 节；节缺失 → None（旧格式，向后兼容）。"""
    src = path or CHECKSUMS
    if not src.is_file():
        return None
    out: dict[str, str] = {}
    in_sec = False
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.lstrip().startswith("#"):
            in_sec = _SUPPLY_CHAIN_MARK in line
            continue
        if in_sec:
            parts = line.split()
            if len(parts) == 2:
                out[parts[1]] = parts[0]
    return out or None


def compute_supply_chain(root: Path | None = None,
                         names: tuple[str, ...] = SUPPLY_CHAIN_FILES) -> dict[str, str]:
    """信任根数据文件的 sha256（**不存在的跳过** —— 任务1/2 的产出在各自 commit 才出现）。"""
    d = root or ROOT
    return {n: sha256_of(d / n) for n in names if (d / n).is_file()}


def write_supply_chain_baseline(path: Path | None = None, root: Path | None = None,
                                names: tuple[str, ...] = SUPPLY_CHAIN_FILES) -> Path:
    """把 supply_chain 节**追加**到基准文件末（须先 write_baseline/write_test_config_baseline）。"""
    dst = path or CHECKSUMS
    rows = compute_supply_chain(root, names)
    with dst.open("a", encoding="utf-8") as f:
        f.write(_SUPPLY_CHAIN_MARK + "\n")
        for n, h in sorted(rows.items()):
            f.write(f"{h}  {n}\n")
    return dst


def verify_supply_chain(path: Path | None = None, root: Path | None = None,
                        names: tuple[str, ...] = SUPPLY_CHAIN_FILES
                        ) -> tuple[list[tuple[str, str, str]], list[str], int]:
    """校验信任根数据文件；返回 (changed[(name, want, got)], warnings, exit_code)。

    判定口径（**只有内容变更算红**，理由写在下面每条）：
      * 磁盘有 + 已钉 + hash 不符 ⇒ **changed**（exit 1）—— 这是要抓的攻击面（篡改台账/manifest）；
      * 磁盘有但**未钉**（新出现的覆盖文件 / 旧格式基准）⇒ **warning**，不算红：
        否则"任务1 刚产出 merkle_roots.json"这类**正常新增**会把中间 commit 判红；
      * 已钉但磁盘上没有 ⇒ **warning**：在仓库副本/部分检出里无判别力，
        而"工具文件缺失"已由 core 节单独管（那里 missing = 红）；
      * 列了但磁盘上没有且未钉 ⇒ **warning**（正常状态：任务1/2 的产出还没生成）。
    """
    base = load_supply_chain_baseline(path) or {}
    d = root or ROOT
    changed: list[tuple[str, str, str]] = []
    warnings: list[str] = []
    for name in names:
        f = d / name
        want = base.get(name)
        if not f.is_file():
            if want is not None:
                warnings.append(f"{name}：基准里有、磁盘上没有 ⇒ 跳过（副本/部分检出下无判别力）")
            else:
                warnings.append(f"{name}：不存在 ⇒ 跳过（该产出尚未生成，如任务1/2 的 Merkle 根/layout）")
            continue
        got = sha256_of(f)
        if want is None:
            warnings.append(f"{name}：已存在但**未钉**（旧格式基准或新覆盖文件）⇒ 跑 --update")
        elif got != want:
            changed.append((name, want, got))
    return changed, warnings, (1 if changed else 0)


def compute_ruler(tools_dir: Path | None = None,
                  names: tuple[str, ...] = RULER_TOOLS) -> dict[str, str]:
    """判决尺子文件的 sha256（不存在的跳过）。"""
    d = tools_dir or TOOLS
    return {n: sha256_of(d / n) for n in names if (d / n).is_file()}


def write_ruler_baseline(path: Path | None = None, tools_dir: Path | None = None,
                         names: tuple[str, ...] = RULER_TOOLS) -> Path:
    """把 ruler 节**追加**到基准文件末（须在 core/test_config/supply_chain 之后）。"""
    dst = path or CHECKSUMS
    rows = compute_ruler(tools_dir, names)
    with dst.open("a", encoding="utf-8") as f:
        f.write(_RULER_MARK + "\n")
        for n, h in sorted(rows.items()):
            f.write(f"{h}  {n}\n")
    return dst


def load_ruler_baseline(path: Path | None = None) -> dict[str, str] | None:
    """解析 `.tool_checksums` 的 `# ruler` 节；节缺失 ⇒ None（旧格式，向后兼容）。"""
    src = path or CHECKSUMS
    if not src.is_file():
        return None
    out: dict[str, str] = {}
    in_sec = False
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.lstrip().startswith("#"):
            in_sec = _RULER_MARK in line
            continue
        if in_sec:
            parts = line.split()
            if len(parts) == 2:
                out[parts[1]] = parts[0]
    return out or None


def verify_ruler(path: Path | None = None, tools_dir: Path | None = None
                 ) -> tuple[list[tuple[str, str, str]], list[str], int]:
    """校验 ruler 节；**内容变更或缺失都算红**（尺子必须存在且不被静默改）。缺节 ⇒ exit 2。"""
    base = load_ruler_baseline(path)
    if base is None:
        return [], [], 2
    d = tools_dir or TOOLS
    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []
    for name, want in sorted(base.items()):
        f = d / name
        if not f.is_file():
            missing.append(name)
            continue
        got = sha256_of(f)
        if got != want:
            changed.append((name, want, got))
    return changed, missing, (0 if not changed and not missing else 1)


def verify_merkle(roots_path: Path | None = None) -> tuple[list[str], list[str], int]:
    """目录级 Merkle 根校验（601 任务1.2）：委派给 `merkle_integrity.check_all()`。

    局部导入：核心校验路径（`enforce()`）不该在 import 期就拉起 Merkle 模块（也无循环依赖）。
    缺台账 ⇒ exit 2（调用方按"副本/部分检出"当**警告**处理，不误红）。
    """
    import merkle_integrity as mi

    return mi.check_all(roots_path or mi.ROOTS_PATH)


def update_merkle(roots_path: Path | None = None) -> Path:
    """重建全部 Merkle 根并写台账（601 任务1.2）。**必须在写 supply_chain 基准之前调用**。"""
    import merkle_integrity as mi

    out = Path(roots_path or mi.ROOTS_PATH)
    doc = mi.build_all(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    return out


def verify(path: Path | None = None, tools_dir: Path | None = None
           ) -> tuple[list[tuple[str, str, str]], list[str], int]:
    """返回 (changed[(name, want, got)], missing_names, exit_code)。"""
    base = load_baseline(path)
    if base is None:
        return [], [], 2
    d = tools_dir or TOOLS
    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []
    for name, want in sorted(base.items()):
        f = d / name
        if not f.is_file():
            missing.append(name)
            continue
        got = sha256_of(f)
        if got != want:
            changed.append((name, want, got))
    return changed, missing, (0 if not changed and not missing else 1)


def enforce(tool_name: str, path: Path | None = None, tools_dir: Path | None = None) -> None:
    """**判定入口强制自检**（567 任务 2）：校验不过 ⇒ 立刻 fail-loud 拒绝运行。

    调用纪律（三个判定入口都把这一行放在 `main()` 的**第一句**）：
      * **顺序**：必须在**读库 / 编译 / 跑任何规则之前**——否则"已跑一半才发现核心被改"；
      * **fail-closed**：缺基准（exit 2）/ 文件缺失 / **校验自身异常**一律当"不可信"⇒ 拒绝运行。
        绝不因为校验代码自己出错而静默放行——那会把"没查"伪装成"查过且通过"；
      * **不掩盖真红灯**：拒绝时只报完整性问题（SystemExit(1)），不影响调用方原有的失败路径
        （它根本走不到），也不吞掉任何输出。
    通过时**静默返回**（不打印），免得污染各入口的 stdout 契约（`--json` 等）。
    """
    try:
        changed, missing, code = verify(path, tools_dir)
    except Exception as e:                      # noqa: BLE001 —— 校验自身异常也必须 fail-closed
        print(f"[integrity] ❌ 自检自身异常（{type(e).__name__}: {e}）⇒ 保守拒绝运行",
              file=sys.stderr)
        raise SystemExit(1) from None
    if code == 0:
        return
    lines = [f"[integrity] ❌ 判定核心被改动且未重钉，拒绝运行（{tool_name} 不执行任何规则/判决）"]
    if code == 2:
        lines.append("    缺基准 tools/.tool_checksums ⇒ 无法自证 ⇒ 一律拒绝（不得静默放行）")
    for name, want, got in changed:
        lines.append(f"    {name}：期望 {want[:12]}… 实际 {got[:12]}…")
    for name in missing:
        lines.append(f"    {name}：基准里有、磁盘上缺失")
    lines.append("    修法：确认改动**有意为之**后跑 "
                 "`.venv\\Scripts\\python.exe tools/tool_integrity.py --update` 重钉"
                 "（改判定核心必须显式留痕 —— 这正是本机制的设计目标）")
    print("\n".join(lines), file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="核心工具完整性校验（498 任务 3 / 567 任务 1-2 / 591 任务 3 / "
                                             "601 任务 0.3）")
    ap.add_argument("--update", action="store_true",
                    help="计算并写入 tools/.tool_checksums（core 节 + test_config 节 + supply_chain 节；"
                         "须在功能改动 commit 之后跑）")
    ap.add_argument("--check", action="store_true",
                    help="独立验证（= 无参数的默认动作）：core + supply_chain 全匹配 exit 0 / "
                         "改动或缺失 exit 1 / 缺核心基准 exit 2")
    ap.add_argument("--check-test-config", action="store_true",
                    help="591：只校验**测试器配置**（conftest/pyproject）的 test_config 节；exit 0/1/2")
    ap.add_argument("--check-supply-chain", action="store_true",
                    help="601：只校验**信任根数据文件**（豁免台账/覆盖率台账/manifest/Merkle 根/layout）；"
                         "内容变更 exit 1（未钉/缺文件只警告，理由见 verify_supply_chain）")
    ap.add_argument("--check-merkle", dest="check_merkle", action="store_true", default=True,
                    help="601：`--check` 时同时校验目录级 Merkle 根（默认开）")
    ap.add_argument("--no-check-merkle", dest="check_merkle", action="store_false",
                    help="跳过 Merkle 校验（急用时；正常验收不该用）")
    ap.add_argument("--update-merkle", dest="update_merkle", action="store_true", default=True,
                    help="601：`--update` 时重建全部 Merkle 根（默认开；须在写 supply_chain 基准之前）")
    ap.add_argument("--no-update-merkle", dest="update_merkle", action="store_false",
                    help="不重建 Merkle 根（如只想重钉文件 hash）")
    a = ap.parse_args(argv)

    if a.update:
        # 顺序有意义：Merkle 台账变了 ⇒ 它的 hash 变了 ⇒ 必须**先**重建再钉 supply_chain 基准
        if a.update_merkle:
            mp = update_merkle()
            print(f"[tool_integrity] Merkle 根已重建：{mp.relative_to(ROOT).as_posix()}")
        dst = write_baseline()
        write_test_config_baseline()
        write_supply_chain_baseline()
        write_ruler_baseline()
        print(f"[tool_integrity] 基准已更新：{dst.relative_to(ROOT).as_posix()}"
              f"（core {len(compute())} 个 + test_config {len(compute_test_config())} 个 + "
              f"supply_chain {len(compute_supply_chain())} 个 + ruler {len(compute_ruler())} 个文件）")
        return 0

    if a.check_test_config:
        changed, missing, code = verify_test_config()
        if code == 2:
            print("[tool_integrity] 缺 test_config 节（tools/.tool_checksums）—— "
                  "先跑 `python tools/tool_integrity.py --update`", file=sys.stderr)
            return 2
        for name, want, got in changed:
            print(f"[tool_integrity] ❌ {name} 被改动（期望 {want[:12]}… 实际 {got[:12]}…）")
        for name in missing:
            print(f"[tool_integrity] ❌ {name} 缺失（基准里有、磁盘上没有）")
        if code == 0:
            print(f"[tool_integrity] OK：{len(compute_test_config())} 个测试器配置与基准一致")
        return code

    if a.check_supply_chain:
        changed, warnings, code = verify_supply_chain()
        for name, want, got in changed:
            print(f"[tool_integrity] ❌ [supply_chain] {name} 被改动"
                  f"（期望 {want[:12]}… 实际 {got[:12]}…）")
        for w in warnings:
            print(f"[tool_integrity] ⚠ [supply_chain] {w}")
        if code == 0:
            print(f"[tool_integrity] OK：信任根数据文件与基准一致"
                  f"（{len(compute_supply_chain())} 个已存在，警告 {len(warnings)} 条）")
        return code

    changed, missing, code = verify()
    if code == 2:
        print("[tool_integrity] 缺基准文件 tools/.tool_checksums —— "
              "先跑 `python tools/tool_integrity.py --update`", file=sys.stderr)
        return 2
    for name, want, got in changed:
        # 567 任务 1：按提示词只打**前缀**（12 位足够人眼比对/贴工单；全量哈希在 .tool_checksums 里）
        print(f"[tool_integrity] ❌ {name} 被改动（期望 {want[:12]}… 实际 {got[:12]}…）")
    for name in missing:
        print(f"[tool_integrity] ❌ {name} 缺失（基准里有、磁盘上没有）")
    if code == 0:
        print(f"[tool_integrity] OK：{len(compute())} 个核心工具与基准一致")
    # 601 任务 0.3：`--check` 同时校验信任根数据文件（core 绿 + supply_chain 绿 ⇒ 才是真绿）
    sc_changed, sc_warnings, sc_code = verify_supply_chain()
    for name, want, got in sc_changed:
        print(f"[tool_integrity] ❌ [supply_chain] {name} 被改动"
              f"（期望 {want[:12]}… 实际 {got[:12]}…）")
    for w in sc_warnings:
        print(f"[tool_integrity] ⚠ [supply_chain] {w}")
    if sc_code == 0 and code == 0:
        print(f"[tool_integrity] OK：信任根数据文件与基准一致"
              f"（{len(compute_supply_chain())} 个已存在，警告 {len(sc_warnings)} 条）")
    m_code = 0
    if a.check_merkle:
        m_problems, m_skipped, m_code = verify_merkle()
        for x in m_skipped:
            print(f"[tool_integrity] ⚠ [merkle] {x}")
        for x in m_problems:
            print(f"[tool_integrity] ❌ [merkle] {x}")
        if m_code == 0:
            print(f"[tool_integrity] OK：目录级 Merkle 根与当前内容一致"
                  f"（警告 {len(m_skipped)} 条）")
        elif m_code == 2:
            m_code = 0            # 缺台账（副本/部分检出）⇒ 警告而非红，理由同 supply_chain
    # 615 B3：`--check` 同时校验**判决尺子**节（尺子被改/缺失 ⇒ 红）
    r_changed, r_missing, r_code = verify_ruler()
    for name, want, got in r_changed:
        print(f"[tool_integrity] ❌ [ruler] {name} 被改动（期望 {want[:12]}… 实际 {got[:12]}…）")
    for name in r_missing:
        print(f"[tool_integrity] ❌ [ruler] {name} 缺失（基准里有、磁盘上没有）")
    if r_code == 0:
        print(f"[tool_integrity] OK：判决尺子与基准一致（{len(compute_ruler())} 个）")
    elif r_code == 2:
        print("[tool_integrity] ⚠ [ruler] 缺 ruler 节（旧格式基准）—— 跑 --update 补齐")
        r_code = 0            # 旧格式向后兼容：缺节只警告
    return 1 if (code != 0 or sc_code != 0 or m_code != 0 or r_code != 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
