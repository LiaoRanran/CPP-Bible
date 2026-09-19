#!/usr/bin/env python3
"""591 任务 2 · 治理文档完整性防护（A1 / D13）。

问题：投喂词（`References/architecture_架构演进/*.md`）事实上是 agent 的可执行政策，却零完整性校验。
攻击者改一份投喂词插入"将 EV-X 降为 warn 并豁免其毒样例"，执行模型按纪律照做，门禁全绿——
不改一行代码、checksum 全绿，比 564 PoC#1 更隐蔽。

本工具提供两件**只读/护栏**能力（纯标准库）：
  (a) manifest 机制：对全部投喂词算 sha256，`verify` 比对、`update --force` 更新；
  (b) 弱化指令扫描器：模式匹配"降为 warn / 豁免毒样例 / 跳过门禁 / 关闭自检"等关键词，产出**人审清单**
      （`needs_human_review: true`；这是模式匹配、不是语义理解，必然有误报）。

**边界诚实**：根仍是人读 diff —— manifest 只能发现"文档变了"，判不了"善意还是恶意"；scan 只能发现
"含弱化关键词"，判不了语义。不做 PKI/数字签名/二人签（单用户阶段无意义）。只扫
`References/architecture_架构演进/`，不扫 docs/README/其他目录。

601 任务 0.4（纵深防御）：manifest **多了 `self_hash` 自校验** —— manifest 自身是信任根的一部分，
此前"谁改了基准谁就能自签"（与 `.tool_checksums` 同类边界）。现在 manifest 内容（排除 `self_hash`
字段本身）的 sha256 写回自身，`verify`/`preflight` **先校 self_hash**：不符即
`manifest self-hash mismatch` ⇒ exit 1。**这不是签名**（单用户阶段无密钥对，攻击者能同时改内容与
self_hash）—— 它的价值是让"改了内容忘了/不想改 hash 的**单点篡改**"必被发现（纵深防御第 1 层），
并与 `tool_integrity` 的 `SUPPLY_CHAIN_FILES` 形成**两条独立**的检出路径（第二条钉的是文件 hash）。

用法：
  python tools/governance_doc_guard.py verify            # 校验 self_hash + manifest：exit0=一致 / exit1=不一致
  python tools/governance_doc_guard.py update --force    # 更新 manifest（无 --force 拒绝；重算 self_hash）
  python tools/governance_doc_guard.py scan              # 扫描弱化指令 → data/governance_weakening_scan.json
  python tools/governance_doc_guard.py preflight         # verify + scan：不一致 exit1 / 有 high 命中 exit2 / 干净 exit0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "References" / "architecture_架构演进"
MANIFEST_PATH = ROOT / "data" / "governance_docs_manifest.json"
SCAN_PATH = ROOT / "data" / "governance_weakening_scan.json"
SELF_HASH_KEY = "self_hash"              # 601 任务 0.4：manifest 自校验字段（排除自身后算内容 hash）

# 风险等级：high = 直接指令弱化判决 / medium = 描述性提及可能弱化 / low = 纪律用语上下文
# 逐模式标注；命中一律 needs_human_review=true。
_PATTERNS: list[tuple[str, str, str]] = [
    (r"降为\s*warn|降级为\s*warn|降\s*warn|block\s*改\s*warn|从\s*block\s*改为\s*warn",
     "high", "直接指令：把（某规则/某卡）降为 warn"),
    (r"豁免.{0,16}(毒样例|规则|门禁|判决)", "high", "直接指令：豁免毒样例/规则"),
    (r"跳过.{0,10}(门禁|判决测试|校验|自检)", "high", "直接指令：跳过门禁/判决测试"),
    (r"不再校验|关闭.{0,8}自检|移除.{0,8}校验|删除.{0,8}(闸|校验)|降低阈值",
     "high", "直接指令：移除/关闭校验或降低阈值"),
    (r"放宽.{0,8}条件|扩大.{0,8}豁免", "medium", "描述性：放宽条件/扩大豁免"),
    (r"豁免", "medium", "提及『豁免』（需人审上下文判定）"),
    (r"warn\s*起步", "low", "纪律用语：warn 起步（观察期），非弱化指令"),
]
_COMPILED = [(re.compile(p, re.IGNORECASE), lv, lab) for p, lv, lab in _PATTERNS]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:                     # 仓外路径（测试注入临时目录时）⇒ 用绝对式
        return path.as_posix()


def _git_commit() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return r.stdout.strip() if r.returncode == 0 else "unknown"


def scan_docs(docs_root: Path | None = None) -> list[dict]:
    """扫描投喂词，返回按路径排序的 [{path, sha256, size}]。"""
    docs_root = docs_root or DOCS_ROOT
    out = []
    for p in sorted(docs_root.rglob("*.md")):
        out.append({"path": _rel(p), "sha256": _sha256(p), "size": p.stat().st_size})
    return out


def generate_manifest(docs_root: Path | None = None) -> dict:
    """生成 manifest（含 `self_hash`：内容去掉 self_hash 字段后的 sha256）。"""
    man = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "git_commit": _git_commit(), "files": scan_docs(docs_root)}
    man[SELF_HASH_KEY] = compute_self_hash(man)
    return man


def compute_self_hash(man: dict) -> str:
    """manifest 内容的 sha256（**排除 `self_hash` 字段本身**；键序/缩进规范化后再算）。

    规范化（`sort_keys=True` + 固定 indent + ensure_ascii=False）是为了让"写出去再读回来"
    得到同一个值——否则 json 键序变化会让自校验无故变红。
    """
    core = {k: v for k, v in man.items() if k != SELF_HASH_KEY}
    blob = json.dumps(core, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def verify_self_hash(manifest_path: Path | None = None) -> tuple[bool, str]:
    """校验 manifest 自身 hash；返回 (通过?, 说明)。**先于**任何文档比对调用。"""
    p = manifest_path or MANIFEST_PATH
    if not p.is_file():
        return False, f"缺 manifest：{_rel(p)}（先跑 update --force）"
    try:
        man = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        return False, f"manifest 不是合法 JSON（{exc}）"
    if not isinstance(man, dict):
        return False, "manifest 不是 JSON 对象"
    got = man.get(SELF_HASH_KEY)
    if not got:
        return False, (f"manifest 缺 `{SELF_HASH_KEY}` 字段（旧格式）⇒ 无法自证，"
                       f"跑 `update --force` 重签")
    want = compute_self_hash(man)
    if got != want:
        return False, (f"manifest self-hash mismatch（期望 {want[:12]}… 实际 {str(got)[:12]}…）"
                       f"⇒ manifest 内容被改过而 hash 未同步")
    return True, ""


def diff_files(old: dict[str, dict], cur: dict[str, dict]) -> list[str]:
    """两份 `{path: 记录}` 的差异清单（新增/删除/内容变更），排序确定。"""
    diffs: list[str] = []
    for path in sorted(set(cur) - set(old)):
        diffs.append(f"新增：{path}")
    for path in sorted(set(old) - set(cur)):
        diffs.append(f"删除：{path}")
    for path in sorted(set(old) & set(cur)):
        if old[path]["sha256"] != cur[path]["sha256"]:
            diffs.append(f"内容变更：{path}")
    return diffs


def verify_manifest(manifest_path: Path | None = None,
                    docs_root: Path | None = None) -> tuple[bool, list[str]]:
    """**先校 self_hash**，再逐条比对文档；返回 (一致?, 差异清单)。"""
    manifest_path = manifest_path or MANIFEST_PATH
    docs_root = docs_root or DOCS_ROOT
    ok_self, why = verify_self_hash(manifest_path)
    if not ok_self:
        return False, [why]
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    old = {f["path"]: f for f in man.get("files", [])}
    cur = {f["path"]: f for f in scan_docs(docs_root)}
    diffs = diff_files(old, cur)
    return (not diffs), diffs


def update_manifest(force: bool = False, manifest_path: Path | None = None,
                    docs_root: Path | None = None) -> tuple[bool, list[str]]:
    """重新生成 manifest（**含 self_hash**）；**需 --force**（防误调用覆盖基准）。

    返回 (写没写, **文档**变更清单)。注意这里**不走** `verify_manifest()`：那条路径会先卡
    自校验（旧格式 manifest 必然报"缺 self_hash"），会把"真实文档变更数"冲掉。
    """
    manifest_path = manifest_path or MANIFEST_PATH
    docs_root = docs_root or DOCS_ROOT
    if not force:
        return False, ["拒绝写入：update 需显式 --force（防误调用覆盖基准）"]
    old: dict[str, dict] = {}
    if manifest_path.is_file():
        try:
            old = {f["path"]: f for f in json.loads(
                manifest_path.read_text(encoding="utf-8")).get("files", [])}
        except (ValueError, KeyError, TypeError):
            old = {}                       # 旧 manifest 坏了 ⇒ 当"无旧基准"重签（不是静默放行：全量重算）
    man = generate_manifest(docs_root)
    dic = diff_files(old, {f["path"]: f for f in man["files"]}) if old else \
        [f"新增：{f['path']}" for f in man["files"]]
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return True, dic


def scan_weakening_instructions(docs_root: Path | None = None,
                                out_path: Path | None = None) -> dict:
    """逐行模式匹配弱化关键词，产出人审清单 JSON。"""
    docs_root = docs_root or DOCS_ROOT
    if out_path is None:
        out_path = SCAN_PATH
    findings: list[dict] = []
    for p in sorted(docs_root.rglob("*.md")):
        rel = _rel(p)
        for ln, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for rx, level, label in _COMPILED:
                m = rx.search(line)
                if m:
                    findings.append({"path": rel, "line": ln, "risk": level, "label": label,
                                     "match": m.group(0), "text": line.strip()[:200],
                                     "needs_human_review": True})
    summary = {lv: sum(1 for f in findings if f["risk"] == lv) for lv in ("high", "medium", "low")}
    res = {"scan_time": datetime.now().isoformat(timespec="seconds"),
           "docs_root": _rel(docs_root), "findings": findings, "summary": summary,
           "note": ("模式匹配、非语义理解 ⇒ 必然有误报（历史投喂词本身也在讨论这些词）；"
                    "全部命中标 needs_human_review=true，是**人审清单**、不是自动判决。")}
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="591 · 治理文档完整性防护（只读/护栏）")
    ap.add_argument("cmd", choices=["verify", "update", "scan", "preflight"])
    ap.add_argument("--force", action="store_true", help="update 专用：显式确认覆盖基准")
    a = ap.parse_args(argv)

    if a.cmd == "verify":
        # 601 任务 0.4：**先校 self_hash**（manifest 是信任根的一部分，自身被改必须先显形）
        ok_self, why = verify_self_hash()
        if not ok_self:
            print(f"[gov] ❌ {why}", file=sys.stderr)
            return 1
        ok, diffs = verify_manifest()
        if ok:
            print("[gov] manifest 一致 ✓（self_hash 已校验）")
            return 0
        print(f"[gov] manifest 不一致（{len(diffs)} 处）：", file=sys.stderr)
        for d in diffs[:20]:
            print(f"[gov]   {d}", file=sys.stderr)
        return 1

    if a.cmd == "update":
        wrote, diffs = update_manifest(force=a.force)
        if not wrote:
            print(f"[gov] {diffs[0]}", file=sys.stderr)
            return 1
        man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        print(f"[gov] manifest 已更新 → {_rel(MANIFEST_PATH)}"
              + (f"（变更 {len(diffs)} 处）" if diffs else "（无变更）")
              + f"（self_hash {str(man.get(SELF_HASH_KEY))[:12]}…）")
        return 0

    if a.cmd == "scan":
        res = scan_weakening_instructions()
        s = res["summary"]
        print(f"[gov] 弱化指令扫描：high={s['high']} medium={s['medium']} low={s['low']}"
              f" → {_rel(SCAN_PATH)}")
        return 0

    # preflight
    ok, diffs = verify_manifest()
    if not ok:
        print(f"[gov] preflight 失败：manifest 不一致（{len(diffs)} 处）", file=sys.stderr)
        for d in diffs[:20]:
            print(f"[gov]   {d}", file=sys.stderr)
        return 1
    res = scan_weakening_instructions()
    high = [f for f in res["findings"] if f["risk"] == "high"]
    if high:
        print(f"[gov] preflight：manifest 一致，但扫描出 {len(high)} 条 high 级弱化关键词"
              "（人审清单，非自动判决）", file=sys.stderr)
        for f in high[:20]:
            print(f"[gov]   {f['path']}:{f['line']} [{f['label']}] {f['match']}", file=sys.stderr)
        return 2
    print("[gov] preflight ✓（manifest 一致，无 high 级弱化关键词）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
