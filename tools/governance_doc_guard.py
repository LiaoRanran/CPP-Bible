#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
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

607 任务 1（**扫描面扩边 + 增量机械登记**）：591 起台账只覆盖 `References/architecture_架构演进/`，
而历轮的调研/过程文档（仓根 `_arch_*/**`、`_auto/inbox/*.md`、根下 `PM_/PUSH_/INDEX_/MATRIX_/CHECKLIST_*.md`）
**从未进过扫描面** ⇒ 既不报"缺"、也永远没人登记。607 把扫描面扩到这些位置，并补上"增量登记"通道：
  * `iter_governed_docs()` 是**唯一真源**（`verify` 与 `auto-update` 共用；若两边扫描面不一致，
    新增条目会被 `verify` 判成"删除"而报红）；
  * `auto_update()`：**只追加**新文档、**只标记**消失文档（`status: "missing"`，保留历史 hash），
    **绝不刷新既有 hash**（刷新 = 全量重签，会把"内容被改过"顺手抹平 ⇒ 仍是人审 `update --force` 的活）；
  * `verify` 比对时**跳过** `status == "missing"` 的条目（否则标记动作会立刻制造"删除"红）。
**边界（诚实）**：`update --force`（全量重签）与 `auto-update`（增量登记）**都不做语义判断**；
弱化扫描 `scan` 仍只扫 `DOCS_ROOT`（投喂词才是可执行政策，`_arch_*` 是过程文档），扩不扩面是另一个决策。

673u 任务 A（**修"manifest 机器相关"的两个口径 bug** —— 这是"漂移 634 处"的真正根因）
====================================================================================
673s 报告 `data/governance_docs_manifest.json` 与真实文档树漂移 **634 处**，并因此 4 处
`residue_present` 型 skip 无法解除。673u 定位到**不是"忘了重算"，而是生成器有两条口径 bug**：

1. **扫描面把 gitignore 的本机落盘口算进了入库 manifest**：607 把 `_auto/inbox/*.md` 并入扫描面，
   但 `.gitignore` 有 `_auto/`（124 行）与 `_arch_v18/`（128 行）——这些目录**只存在于开发机**。
   ⇒ 本地"新增 44 处"、CI 干净检出"删除 30 处"，**同一份 manifest 在两处都不可能一致**。
   修法：`iter_governed_docs()` 默认面按 `git ls-files` **在册过滤**（`_git_tracked()`）；
   `docs_root` 显式注入（591 测试）与非 git 假仓（607 测试）**不过滤**，语义向后兼容。
2. **哈希的是工作区字节（含 CRLF）**：Windows 编辑器回写的 CRLF 让同一文档在开发机与 Linux CI
   算出不同 hash。修法：`_content_bytes()` 按 `.gitattributes` 的 `* text=auto eol=lf` 归一
   （CRLF→LF）。实测：976 份在册受治理文档里 236 份工作区含 CRLF，
   `sha256(归一化) == sha256(git blob)` **逐条成立**（0 处不符）⇒ 归一化等价于"哈希提交内容"。

口径澄清（**不是**放水）：manifest 仍然**逐字节**钉住每份在册文档；改的只是"扫谁、按什么字节算"，
使它**机器无关**。对"投喂词被篡改"的检出能力**不变**（改内容 ⇒ hash 变 ⇒ `verify` 红）。

用法：
  python tools/governance_doc_guard.py verify            # 校验 self_hash + manifest：exit0=一致 / exit1=不一致
  python tools/governance_doc_guard.py update --force    # 更新 manifest（无 --force 拒绝；重算 self_hash）
  python tools/governance_doc_guard.py auto-update       # 607：增量机械登记（只追加 + 标记 missing；无变更不写盘）
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

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
DOCS_ROOT = ROOT / "References" / "architecture_架构演进"
MANIFEST_PATH = ROOT / "data" / "governance_docs_manifest.json"
SCAN_PATH = ROOT / "data" / "governance_weakening_scan.json"
SELF_HASH_KEY = "self_hash"              # 601 任务 0.4：manifest 自校验字段（排除自身后算内容 hash）

# 607 任务 1：新增扫描面（历史上从未纳入台账的位置）
#: 仓根下这些**目录**里的全部 `*.md`（递归）：`_arch_v2`…`_arch_v17`、`_arch_free` 等调研/过程文档
GOVERNED_DIR_GLOBS: tuple[str, ...] = ("_arch_*",)
#: `_auto/inbox/*.md`（各批投喂词的落盘位置）
GOVERNED_INBOX_DIR: tuple[str, ...] = ("_auto", "inbox")
#: 仓根下这些**文件模式**
GOVERNED_ROOT_FILE_GLOBS: tuple[str, ...] = ("PM_*.md", "PUSH_*.md", "INDEX_*.md",
                                             "MATRIX_*.md", "CHECKLIST_*.md")

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


def _content_bytes(path: Path) -> bytes:
    """读取文件内容，并**按 `.gitattributes` 归一换行**（CRLF→LF）。

    673u 修复（换行口径）：manifest 必须在 **Windows 开发机**与 **Linux CI** 上给出同一个值，
    否则同一份文档在两处 hash 不同 ⇒ manifest 永远"漂移"、`verify` 永远红。
    根因：工作区检出可能是 CRLF（Windows 编辑器回写整文件），而 `.gitattributes` 的
    `* text=auto eol=lf` 保证**入库/CI 检出**是 LF。实测（673u）：976 份受治理 tracked 文档里
    236 份工作区含 CRLF，`sha256(归一化工作区字节) == sha256(git blob)` **逐条成立（0 处不符）**
    ⇒ 归一化即等价于"哈希提交内容"，是让 manifest 机器无关的最小改法。
    """
    data = path.read_bytes()
    return data.replace(b"\r\n", b"\n") if b"\r\n" in data else data


def _sha256(path: Path) -> str:
    """文件内容的 sha256（换行归一后；见 `_content_bytes()`）。"""
    return hashlib.sha256(_content_bytes(path)).hexdigest()


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


def _git_tracked(root: Path) -> set[str] | None:
    """`root` 下 git **跟踪**（在册）文件的仓相对路径集合（换行安全的 -z 输出）。

    673u 修复（扫描面口径）：`ROOT` **不是 git 工作树根**（如测试注入的假仓）⇒ 返回 `None`
    （**不启用过滤**，保持 607 起"假仓里全部文件都受治理"的既有语义）；
    git 不可用/超时 ⇒ 同样返回 `None`（宁可退回旧行为，也不静默丢文档）。

    为什么必须过滤（673u 实测）：607 把 `_auto/inbox/*.md` 与 `_arch_*` 并入扫描面，但
    `.gitignore` 里有 `_auto/`（第 124 行）与 `_arch_v18/`（第 128 行）——这些是**本机投喂词
    落盘口/历史归档**，只存在于开发机。把它们算进**入库的** manifest ⇒
    本地报"新增 44 处"、CI（干净检出）报"删除 21+9 处"，同一份 manifest 两处都不可能一致。
    过滤后扫描面 == "提交进仓的文档"，manifest 才机器无关。
    """
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(root),
                             capture_output=True, text=True, timeout=20)
        if top.returncode != 0:
            return None                                  # 非 git 仓（假仓/副本）⇒ 不过滤
        try:
            if Path(top.stdout.strip()).resolve() != Path(root).resolve():
                return None                              # 根 ≠ 工作树根 ⇒ 不过滤（假仓嵌在真仓内）
        except OSError:
            return None
        r = subprocess.run(["git", "-c", "core.quotepath=false", "ls-files", "-z"],
                           cwd=str(root), capture_output=True, timeout=60)
        if r.returncode != 0:
            return None
    except (OSError, subprocess.SubprocessError):
        return None
    return {p for p in r.stdout.decode("utf-8", "replace").split("\0") if p}


def iter_governed_docs(docs_root: Path | None = None) -> list[Path]:
    """受治理文档路径全集（**唯一真源**：`verify` 与 `auto-update` 必须共用）。

    - `docs_root` **显式给出** ⇒ 只扫那一个目录（591 测试注入语义保持不变，**不做** git 过滤）；
    - 省略（默认）⇒ 扫 607 扩边后的全集：`DOCS_ROOT` + 仓根 `_arch_*/**` + `_auto/inbox` + 根下 5 类文件；
      **673u 起把 607 扩边的位置按 git 在册过滤**（剔除 gitignore 的本机落盘口/归档，
      见 `_git_tracked()`）——否则 manifest 会因开发机残留而机器相关、CI 必红。
      `DOCS_ROOT`（591 原始面）**豁免**该过滤（真仓 345/345 在册 ⇒ 过滤是 no-op；豁免是为了不破坏
      把 `DOCS_ROOT` 注入到 tmp 的既有测试，详见下方 `_collect(exempt=True)` 处的注释）。
      去重（按仓根相对路径）后按路径排序，保证 manifest 顺序确定。
    """
    if docs_root is not None:
        return sorted(p for p in Path(docs_root).rglob("*.md") if p.is_file())
    found: dict[str, Path] = {}
    docs_keys: set[str] = set()          # `DOCS_ROOT`（591 原始治理面）——**豁免** git 在册过滤

    def _collect(paths, exempt: bool = False) -> None:
        for p in paths:
            if p.is_file() and p.suffix == ".md":
                k = _rel(p)
                found.setdefault(k, p)     # 同一路径只留一份（同名不同根也按相对路径区分）
                if exempt:
                    docs_keys.add(k)

    # 591 原始面：投喂词目录。**不**过在册过滤 ——
    #   ① 实测该目录 345 份 .md **全部在册**（过滤在真仓是 no-op，不损失覆盖）；
    #   ② 591/601 的测试把它 `monkeypatch` 到 tmp（此时不在 git 在册集合里），
    #      若一并过滤，注入的临时文档会被静默丢掉 ⇒ 篡改检测失效（673u 实测：591 的
    #      `test_preflight_combinations` 因此由红转绿的假绿）。语义优先级：注入显式 > 在册过滤。
    if DOCS_ROOT.is_dir():
        _collect(DOCS_ROOT.rglob("*.md"), exempt=True)
    inbox = ROOT.joinpath(*GOVERNED_INBOX_DIR)
    if inbox.is_dir():
        _collect(sorted(inbox.glob("*.md")))
    for pat in GOVERNED_DIR_GLOBS:
        for d in sorted(ROOT.glob(pat)):
            if d.is_dir():
                _collect(sorted(d.rglob("*.md")))
    for pat in GOVERNED_ROOT_FILE_GLOBS:
        _collect(sorted(ROOT.glob(pat)))
    tracked = _git_tracked(ROOT)
    if tracked is None:                            # 非 git 仓 ⇒ 退回 607 的"不过滤"语义
        return [found[k] for k in sorted(found)]
    return [found[k] for k in sorted(found) if k in tracked or k in docs_keys]


def scan_docs(docs_root: Path | None = None) -> list[dict]:
    """扫描受治理文档，返回按路径排序的 [{path, sha256, size}]。

    `docs_root` 省略 ⇒ 607 扩边 + **673u 在册过滤**后的全集（见 `iter_governed_docs()`）。
    `size` 与 `sha256` 同源（换行归一后的字节数，见 `_content_bytes()`），避免"hash 归一、size 不归一"的自相矛盾。
    """
    out = []
    for p in iter_governed_docs(docs_root):
        blob = _content_bytes(p)
        out.append({"path": _rel(p), "sha256": hashlib.sha256(blob).hexdigest(), "size": len(blob)})
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
    """**先校 self_hash**，再逐条比对文档；返回 (一致?, 差异清单)。

    607：比对时**跳过** `status == "missing"` 的条目（它们已被 `auto-update` 标记为"文件已消失"，
    仍留在 manifest 里当历史；若不跳过，标记动作本身就会制造一条"删除"红）。
    `docs_root` 省略 ⇒ 用 607 扩边后的全集（与 `auto-update` 同一扫描面）。
    """
    manifest_path = manifest_path or MANIFEST_PATH
    ok_self, why = verify_self_hash(manifest_path)
    if not ok_self:
        return False, [why]
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    old = {f["path"]: f for f in man.get("files", []) if f.get("status") != "missing"}
    cur = {f["path"]: f for f in scan_docs(docs_root)}
    diffs = diff_files(old, cur)
    return (not diffs), diffs


def update_manifest(force: bool = False, manifest_path: Path | None = None,
                    docs_root: Path | None = None) -> tuple[bool, list[str]]:
    """重新生成 manifest（**含 self_hash**）；**需 --force**（防误调用覆盖基准）。

    返回 (写没写, **文档**变更清单)。注意这里**不走** `verify_manifest()`：那条路径会先卡
    自校验（旧格式 manifest 必然报"缺 self_hash"），会把"真实文档变更数"冲掉。
    `docs_root` 省略 ⇒ 用 607 扩边后的全集（与 `verify` 同一扫描面）。

    全量重签 ⇒ 会**抹平**"既有文档内容被改过"的痕迹；607 的日常机械更新走 `auto_update()`（增量）。
    """
    manifest_path = manifest_path or MANIFEST_PATH
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


def auto_update(manifest_path: Path | None = None,
                docs_root: Path | None = None) -> tuple[dict, list[str]]:
    """607 任务 1：**增量机械登记**（日常通道；替代"每次都全量重签"的 `update --force`）。

    与 `update --force` 的**关键差别**（这是本函数存在的理由）：
      * 只**追加**新发现的文档（算 sha256 后追加）；
      * 只把"manifest 里有、磁盘上没了"的条目**标记** `status = "missing"`（**保留**历史 hash，不删条目）；
      * **绝不刷新既有条目的 hash** ⇒ 既有文档被改过时 `verify` 依旧报"内容变更"（fail-closed）。
        想接受内容变更必须走人审 `update --force`（全量重签）。

    返回 `(统计, 人类可读变更清单)`；统计键：`added / reappeared / missing / changed / total / wrote`。
    **无变更时不写盘**（保证可重复执行且不污染工作区）。
    """
    manifest_path = manifest_path or MANIFEST_PATH
    man: dict = {}
    if manifest_path.is_file():
        try:
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
            man = loaded if isinstance(loaded, dict) else {}
        except ValueError:
            man = {}                        # manifest 坏了 ⇒ 当空基准；既有信息无法恢复，如实报告
    records: list[dict] = [f for f in man.get("files", []) if isinstance(f, dict) and f.get("path")]
    by_path: dict[str, dict] = {f["path"]: f for f in records}

    cur = {f["path"]: f for f in scan_docs(docs_root)}
    added: list[str] = []
    reappeared: list[str] = []
    missing: list[str] = []
    changed: list[str] = []

    for path in sorted(cur):
        rec = by_path.get(path)
        if rec is None:
            records.append(dict(cur[path]))
            added.append(path)
            continue
        if rec.get("status") == "missing":          # 之前标记消失，现在又出现了
            rec.pop("status", None)                 # 回到受治理范围（先恢复状态，hash 见下）
            reappeared.append(path)
        if rec.get("sha256") != cur[path]["sha256"]:
            changed.append(path)                    # **不改 hash**：留给人审 update --force
    for path in sorted(by_path):
        if path not in cur and by_path[path].get("status") != "missing":
            by_path[path]["status"] = "missing"
            missing.append(path)

    stats = {"added": len(added), "reappeared": len(reappeared), "missing": len(missing),
             "changed": len(changed), "total": len(records), "wrote": False}
    if not (added or reappeared or missing):
        return stats, []                            # 无变更 ⇒ 不写盘（幂等；也避免无谓改 self_hash）

    man = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "git_commit": _git_commit(), "files": records}
    man[SELF_HASH_KEY] = compute_self_hash(man)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    stats["wrote"] = True

    diffs = [f"新增：{p}" for p in added] + [f"复现：{p}" for p in reappeared] \
        + [f"标记 missing：{p}" for p in missing] \
        + [f"内容变更（**未**自动重签，需人审 `update --force`）：{p}" for p in changed]
    return stats, diffs


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
    ap.add_argument("cmd", choices=["verify", "update", "auto-update", "scan", "preflight"])
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

    if a.cmd == "auto-update":                    # 607 任务 1
        stats, diffs = auto_update()
        if not stats["wrote"]:
            print(f"[gov] auto-update：无变更（未写盘；manifest 共 {stats['total']} 条）")
            return 0
        print(f"[gov] auto-update：新增 {stats['added']} / 标记 missing {stats['missing']}"
              f" / 复现 {stats['reappeared']}（共 {stats['total']} 条）→ {_rel(MANIFEST_PATH)}")
        for d in diffs[:20]:
            print(f"[gov]   {d}")
        if len(diffs) > 20:
            print(f"[gov]   …（共 {len(diffs)} 处）")
        if stats["changed"]:
            print(f"[gov] ⚠ 内容变更 {stats['changed']} 处**未**自动重签（增量通道只登记新增/消失）"
                  "⇒ `verify` 会报红，须人审后 `update --force`", file=sys.stderr)
            return 1
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

if "--check" in sys.argv:
    print("OK: governance_doc_guard --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
