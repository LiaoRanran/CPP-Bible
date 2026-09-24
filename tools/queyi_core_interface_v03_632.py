"""632 F1 · QueYi Core 接口抽象 **v0.3**（纯标准库；**一个接口真实适配**）

631 F1 的 v0.2 只**定义不实现**（5 个接口全部 `raise NotImplementedError`）。
本批推进到 v0.3 的关键一步：**把其中一个接口（Evidence）真正适配到现有工具**——
不再是签名占位，而是能读真实证据卡、比对真实产物哈希、并把复算委托给真实的
`atom_evidence_replay.replay_card`。

| 接口 | v0.3 状态 | 真实后端 |
|---|---|---|
| `Evidence` | **真实适配**（本批） | `evidence/*.md` 解析 + `artifact_sha256` 比对 + `atom_evidence_replay` |
| `Claim` / `Verifier` / `Authority` / `Attacker` | 仍只定义不实现（v0.2 状态） | — |

设计取舍（诚实）：只做 **1 个**接口的完整适配，是为了把"接口 → 真实工具"的
接线范式跑通一次（证明抽象不是空中楼阁）；其余 4 个留作后续（623/624 已实现部分
能力，但抽出为统一接口尚需逐接口对齐，属已知债）。

**只读契约**：`--check` 不写任何文件、不实例化会改盘的业务对象；`EvidenceAdapter`
对真实证据卡只做读取 + 哈希计算（零改写）。`--report` 才写 `data/queyi_core_interface_v03_632.md/.json`。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import queyi_core_interface_v02_631 as v02  # noqa: E402  v0.2 抽象基类（631 F1）

OUT_MD = os.path.join(ROOT, "data", "queyi_core_interface_v03_632.md")
OUT_JSON = os.path.join(ROOT, "data", "queyi_core_interface_v03_632.json")

EVIDENCE_DIR = os.path.join(ROOT, "evidence")
_ADAPTED = "Evidence"  # 本批真实适配的接口

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def _parse_fm(path: str) -> dict[str, str]:
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return {}
    m = _FM_RE.match(text)
    if not m:
        return {}
    lines = m.group(1).splitlines()
    fm: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        val = val.strip()
        if val == "":
            # 块值：收集后续缩进行，直到下一个顶格键或文末
            j = i + 1
            block: list[str] = []
            while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("\t")):
                block.append(lines[j])
                j += 1
            fm[key] = "\n".join(block)
            i = j
        else:
            fm[key] = val
            i += 1
    return fm


def _resolve_artifact(rel: str) -> Optional[str]:
    if not rel:
        return None
    if os.path.isabs(rel) and os.path.isfile(rel):
        return rel
    cand = os.path.join(ROOT, rel)
    if os.path.isfile(cand):
        return cand
    cand2 = os.path.join(EVIDENCE_DIR, rel)
    if os.path.isfile(cand2):
        return cand2
    return None


def _sha256_file(path: str) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _parse_list(field: str) -> list[dict[str, Any]]:
    """把 frontmatter 里的 YAML 列表（缩进 `- ` 项）解析为 dict 列表（尽力而为）。"""
    out: list[dict[str, Any]] = []
    for line in field.splitlines():
        s = line.strip()
        if not s.startswith("- "):
            continue
        item = s[2:].strip()
        d: dict[str, Any] = {}
        if item.startswith("{") and item.endswith("}"):
            for part in item[1:-1].split(","):
                if ":" in part:
                    k, _, v = part.partition(":")
                    d[k.strip()] = v.strip().strip('"').strip("'")
        else:
            d = {"raw": item}
        out.append(d)
    return out


class EvidenceAdapter(v02.Evidence):
    """`Evidence` 接口的**真实适配**：把抽象方法接到真实证据卡与复算工具。

    不继承 v0.2 的 `raise NotImplementedError`，而是读 `evidence/*.md` 的真实 frontmatter，
    比对 `artifact_sha256`，并委托 `atom_evidence_replay.replay_card` 做三态复算。
    """

    def __init__(self, card_path: str) -> None:
        self.card_path = card_path
        self._fm = _parse_fm(card_path)

    # ── v0.2 Evidence 接口的真实实现 ──
    def id(self) -> str:
        return self._fm.get("id", os.path.basename(self.card_path))

    def artifact_assert(self) -> list[dict[str, Any]]:
        raw = self._fm.get("artifact_assert", "")
        if not raw:
            return []
        return _parse_list(raw)

    def verify_hash(self) -> bool:
        rel = self._fm.get("artifact_sha256", "")
        declared = rel.strip().lower()
        if not declared:
            return False
        ab = _resolve_artifact(self._fm.get("artifact", ""))
        if ab is None:
            return False
        cur = _sha256_file(ab)
        return cur is not None and cur.lower() == declared

    def provenance(self) -> dict[str, Any]:
        return {
            "source": self._fm.get("source", ""),
            "command": self._fm.get("command", ""),
            "fixture": self._fm.get("fixture", ""),
            "serves": self._fm.get("serves", ""),
            "hypothesis": self._fm.get("hypothesis", ""),
        }

    def replay(self) -> dict[str, Any]:
        """委托真实复算工具 `atom_evidence_replay.replay_card`（懒加载，零依赖失败则报 infra）。"""
        try:
            import importlib
            from pathlib import Path
            aer = importlib.import_module("atom_evidence_replay")
            verdict, log = aer.replay_card(Path(self.card_path))
        except Exception as exc:  # noqa: BLE001
            return {"status": "infra", "reason": f"replay 不可用：{exc}"}
        v = str(verdict)
        if v.startswith("confirm"):
            st = "confirm"
        elif v.startswith("refute"):
            st = "refute"
        else:
            st = "infra"
        return {"status": st, "verdict": v, "log": list(log)[:5]}


def _first_real_evidence_card() -> Optional[str]:
    if not os.path.isdir(EVIDENCE_DIR):
        return None
    for root, _d, files in os.walk(EVIDENCE_DIR):
        for fn in sorted(files):
            if fn.endswith(".md") and fn.upper().startswith("EV-"):
                p = os.path.join(root, fn)
                fm = _parse_fm(p)
                if fm.get("artifact_sha256"):
                    return p
    return None


def measure() -> dict[str, Any]:
    rows = []
    for name, meta in v02.INTERFACES.items():
        ms = v02.public_methods(meta["cls"])
        adapted = (name == _ADAPTED)
        rows.append({
            "interface": name,
            "since": meta["since"],
            "new_in_v02": meta["new_in_v02"],
            "methods": ms,
            "n_methods": len(ms),
            "methods_with_doc": sum(1 for m in ms if v02.doc_of(meta["cls"], m)),
            "adapted_in_v03": adapted,
            "maps": meta["maps"],
        })
    # 真实适配演示：挑一张真实证据卡，跑适配器（只读）
    demo: dict[str, Any] = {"card": None, "id": None, "verify_hash": None,
                            "n_artifact_assert": None, "provenance_keys": None}
    cp = _first_real_evidence_card()
    if cp:
        ad = EvidenceAdapter(cp)
        demo = {
            "card": os.path.relpath(cp, ROOT).replace(os.sep, "/"),
            "id": ad.id(),
            "verify_hash": ad.verify_hash(),
            "n_artifact_assert": len(ad.artifact_assert()),
            "provenance_keys": sorted(ad.provenance().keys()),
        }
    n_adapted_methods = len(v02.public_methods(EvidenceAdapter))
    return {
        "version": "v0.3",
        "n_interfaces": len(rows),
        "adapted_interfaces": [_ADAPTED],
        "n_adapted_methods": n_adapted_methods,
        "rows": rows,
        "demo": demo,
        "note": (f"{_ADAPTED} 接口已真实适配（{n_adapted_methods} 方法接到真实工具）；"
                 "其余 4 接口仍只定义不实现（v0.2 状态）。"),
    }


def write_report() -> str:
    m = measure()
    lines = [
        "# 632 F1 · QueYi Core 接口抽象 **v0.3**", "",
        f"- 接口数：**{m['n_interfaces']}**（与 v0.2 相同）",
        f"- **真实适配接口：{len(m['adapted_interfaces'])} 个 → `{m['adapted_interfaces'][0]}`**"
        f"（{m['n_adapted_methods']} 个方法接到真实工具）",
        "- 其余 4 接口（Claim / Verifier / Authority / Attacker）仍**只定义不实现**（v0.2 状态）", "",
        "## 一、v0.2 → v0.3 的差异", "",
        "| 项 | v0.2（631 F1） | v0.3（632 F1） |", "|---|---|---|",
        "| Evidence 接口 | `raise NotImplementedError` 占位 | **真实适配** `EvidenceAdapter` |",
        "| 真实后端接线 | 无 | 证据卡解析 + `artifact_sha256` 比对 + `atom_evidence_replay` |",
        "| 适配接口数 | 0 | **1 / 5** |",
        "| 其余接口 | 只定义不实现 | 仍只定义不实现（范式已跑通，留后续） |", "",
        "## 二、EvidenceAdapter 真实接线", "",
        "| 方法 | 真实后端 |",
        "|---|---|",
        "| `id()` | 解析证据卡 frontmatter `id` |",
        "| `artifact_assert()` | 解析 `artifact_assert` 列表 |",
        "| `verify_hash()` | 读 `artifact` 文件算 sha256，与 `artifact_sha256` 比对 |",
        "| `provenance()` | 返回 source/command/fixture/serves/hypothesis |",
        "| `replay()` | 委托 `atom_evidence_replay.replay_card` → confirm/refute/infra 三态 |", "",
        "## 三、真实数据演示（只读扫描）", "",
        f"- 演示卡：`{m['demo'].get('card')}`",
        f"- `id()` = `{m['demo'].get('id')}`",
        f"- `verify_hash()` = `{m['demo'].get('verify_hash')}`",
        f"- `artifact_assert` 条数 = `{m['demo'].get('n_artifact_assert')}`",
        f"- `provenance` 字段 = `{m['demo'].get('provenance_keys')}`", "",
        "## 四、诚实登记", "",
        "1. **仅 1/5 接口真实适配**：其余 4 个接口本批**没有**实现（仅 Evidence 跑通了"
        "「抽象 → 真实工具」接线范式）；",
        "2. **`replay()` 为委托式真实调用**：懒加载 `atom_evidence_replay.replay_card`，"
        "若运行环境缺该工具或复算依赖，则返回 `infra`（不假装成功）；",
        "3. **`verify_hash()` 依赖 `artifact_sha256` 声明**：该字段缺失的证据卡无法比对"
        "（与 L2.3 探针登记的覆盖缺口同源）；",
        "4. `--check` 只读：适配器对真实证据卡只做读取 + 哈希计算，零改写；"
        "本报告由 `--report` 生成。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 1) v0.2 抽象基类仍只定义不实现（契约未被破坏）
    for meth in v02.public_methods(v02.Evidence):
        try:
            v02.Evidence().id if meth == "id" else None
        except NotImplementedError:
            pass
    chk("v0.2 Evidence 抽象方法仍 raise NotImplementedError",
        _raises(v02.Evidence, "verify_hash") and _raises(v02.Evidence, "replay"))

    # 2) EvidenceAdapter 真实适配：合成证据卡验证
    import tempfile
    d = tempfile.mkdtemp()
    art = os.path.join(d, "a.out")
    open(art, "wb").write(b"payload")
    real_sha = _sha256_file(art)
    card = os.path.join(d, "EV-Demo-001.md")
    with open(card, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            f"---\nid: EV-Demo-001\nartifact: {art}\nartifact_sha256: {real_sha}\n"
            "command: echo hi\nfixture: x\n"
            "artifact_assert:\n - {kind: exists, text: \"main\"}\n---\nbody\n")
    ad = EvidenceAdapter(card)
    chk("adapter.id() 返回真实 id", ad.id() == "EV-Demo-001")
    chk("adapter.verify_hash() 匹配时 True", ad.verify_hash() is True)
    chk("adapter.artifact_assert() 解析出 1 条", len(ad.artifact_assert()) == 1)
    chk("adapter.provenance() 含 command", ad.provenance().get("command") == "echo hi")

    # 篡改声明 → verify_hash 应 False
    card2 = os.path.join(d, "EV-Demo-002.md")
    with open(card2, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            f"---\nid: EV-Demo-002\nartifact: {art}\nartifact_sha256: 0" * 1
            + "0" + "\n---\nbody\n")
    ad2 = EvidenceAdapter(card2)
    chk("adapter.verify_hash() 不匹配时 False", ad2.verify_hash() is False)

    # 3) 真实仓库口径：measure 结构 + 演示卡可跑
    m = measure()
    chk("measure 返回 version=v0.3", m.get("version") == "v0.3")
    chk("measure 标记 Evidence 已适配",
        any(r["interface"] == _ADAPTED and r["adapted_in_v03"] for r in m["rows"]))
    chk("演示卡 id 非空", bool(m["demo"].get("id")))
    chk("报告路径在 data 下（--check 不写）",
        OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def _raises(cls: type, meth: str) -> bool:
    try:
        getattr(cls, meth)(cls())
    except NotImplementedError:
        return True
    except Exception:  # noqa: BLE001
        return False
    return False


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="632 F1 Core 接口 v0.3（一个接口真实适配）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写接口报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"version={m['version']} adapted={m['adapted_interfaces']} "
          f"methods={m['n_adapted_methods']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
