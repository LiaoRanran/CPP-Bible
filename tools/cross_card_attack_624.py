"""624 A1 · 跨卡一致性攻击（H4 策略升级：多卡修改）

**为什么需要它**：623 撞上「载体天花板」——`sandbox_apply_622.py` 的 apply API 只改**单卡字段**
（原地改 + 必还原），触达仅 26/63 规则。剩余 37 条盲区里有一整类**跨卡一致性规则**
（ATOM-REL-CONFLICT / EV-ARTIFACT-FILE-EXISTS / ATOM-MISCONCEPTION-REF / S2-EVIDENCE-VERDICT …）
需要「同时修改多张卡、构造卡间不一致」才能触达。本工具把 apply API 从单卡扩展到**多卡**。

**跨卡修改机制（继承 622 六重护栏并扩展到 N 卡）**：
| # | 护栏 | 实现 |
|---|---|---|
| 1 | 字节级备份 | apply 前把每张卡读成 bytes 存内存 |
| 2 | finally 必还原 | apply_and_run_multi 的 try/finally 保证异常/超时也还原**所有**被改卡 |
| 3 | 还原校验 | 逐卡还原后重算 sha256 与原比对，不符则 restore_failed |
| 4 | 并发锁 | 复用 `data/.622_apply.lock` |
| 5 | 超时保护 | gate 子进程 timeout=30s |
| 6 | 路径白名单 | 只允许改 `atoms/`、`evidence/` 下的卡（多卡同规则） |

**4 种跨卡攻击策略**：
- **X1 悬空引用**：A 引用 B 的命题/证据，但把 B 的 id 改掉 ⇒ A 的引用悬空、B 成孤儿。
- **X2 循环引用**：A 追加依赖 B、B 追加依赖 A ⇒ 制造依赖环（ATOM-REL-DAG）。
- **X3 矛盾引用**：A 声明 supports B、B 声明 contradicts A ⇒ 卡间矛盾（ATOM-REL-CONFLICT）。
- **X4 孤儿引用**：证据卡 serves 指向不存在原子 / 原子引不存在的误解 id / artifact 指向不存在文件。

**判决口径**（与 622 沙箱一致，多卡取并集）：blocked / detected_nonblock / neutral / escaped / infra_error。

铁律：新工具必有 `--check`（只读自检，exit 0 = 通过）；跨卡修改只在沙箱临时模式（备份+还原），
不修改 gate_engine，不永久改动原始卡。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import sandbox_apply_622 as base  # noqa: E402  （复用单卡沙箱与 gate JSON 工具）

ATOMS = os.path.join(ROOT, "atoms")
EVIDENCE = os.path.join(ROOT, "evidence")
ALLOWED_PREFIXES = ("atoms/", "evidence/")

# 每策略预测触达规则（用于 A2 预测准确率比对）
STRATEGY_PREDICT = {
    "X1": ["ATOM-REL-TARGET", "ATOM-ID-UNIQUE", "EV-SERVES-EXIST"],
    "X2": ["ATOM-REL-DAG", "ATOM-REL-TARGET"],
    "X3": ["ATOM-REL-CONFLICT", "ATOM-REL-TARGET", "ATOM-REL-DAG"],
    "X4": ["EV-SERVES-EXIST", "ATOM-MISCONCEPTION-REF", "EV-ARTIFACT-FILE-EXISTS"],
}


# ── 卡面解析（只读）────────────────────────────────────────────────────────────
def _read(path: str) -> str:
    return open(path, encoding="utf-8").read()


def _fm_bounds(text: str) -> tuple[int, int] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return 3, end


def _scalar(fm: str, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}\s*:\s*(.+?)\s*$", fm)
    return m.group(1) if m else ""


def _inline_list(fm: str, key: str) -> list[str]:
    m = re.search(rf"(?m)^{re.escape(key)}\s*:\s*\[([^\]]*)\]", fm)
    return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []


def _relations(fm: str) -> list[dict]:
    out: list[dict] = []
    m = re.search(r"(?m)^relations\s*:\s*([^\n]*)\n((?:[ \t]+-[^\n]*\n)*)", fm)
    if not m:
        return out
    inline = m.group(1).strip()
    if inline.startswith("["):
        for seg in re.findall(r"\{([^}]*)\}", inline):
            t = re.search(r"type\s*:\s*([^,}\s]+)", seg)
            g = re.search(r"target\s*:\s*([^,}\s]+)", seg)
            out.append({"type": t.group(1) if t else "", "target": g.group(1) if g else ""})
        return out
    for line in m.group(2).splitlines():
        t = re.search(r"type\s*:\s*([^,}\s]+)", line)
        g = re.search(r"target\s*:\s*([^,}\s]+)", line)
        if t or g:
            out.append({"type": t.group(1) if t else "", "target": g.group(1) if g else ""})
    return out


def parse_card(text: str) -> dict:
    b = _fm_bounds(text)
    fm = text[b[0]:b[1]] if b else ""
    return {
        "id": _scalar(fm, "id"),
        "status": _scalar(fm, "status"),
        "artifact": _scalar(fm, "artifact"),
        "serves": _inline_list(fm, "serves"),
        "misconceptions": _inline_list(fm, "misconceptions"),
        "relations": _relations(fm),
        "has_relations_key": bool(re.search(r"(?m)^relations\s*:", fm)),
    }


def load_inventory() -> dict:
    atoms, evidence = [], []
    for d in (ATOMS,):
        for root, _sub, files in os.walk(d):
            for fn in sorted(files):
                if fn.startswith("ATOM-") and fn.endswith(".md"):
                    p = os.path.join(root, fn)
                    rel = base._norm(os.path.relpath(p, ROOT))
                    c = parse_card(_read(p))
                    if c["id"]:
                        atoms.append({"card": rel, **c})
    for root, _sub, files in os.walk(EVIDENCE):
        for fn in sorted(files):
            if fn.startswith("EV-") and fn.endswith(".md"):
                p = os.path.join(root, fn)
                rel = base._norm(os.path.relpath(p, ROOT))
                c = parse_card(_read(p))
                if c["id"]:
                    evidence.append({"card": rel, **c})
    return {"atoms": atoms, "evidence": evidence,
            "ids": {c["id"] for c in atoms} | {c["id"] for c in evidence}}


# ── 卡面编辑（多卡 ops；文本级，只动 frontmatter）──────────────────────────────
def _key_line(text: str, key: str) -> re.Match | None:
    return re.search(rf"(?m)^{re.escape(key)}\s*:.*$", text)


def plan_edit_624(content: dict, text: str) -> tuple[str, str] | None:
    """返回 (新文本, 说明)；无法施加返回 None。先试 622 单卡原语，再试 624 跨卡原语。"""
    op = content.get("op")

    if op == "SET_ID":  # 改 id（用于制造悬空引用/孤儿）
        val = content.get("value")
        m = _key_line(text, "id")
        if not m or not val:
            return None
        return text[:m.start()] + re.sub(r"(?m)^(id\s*:\s*).*$", rf"\g<1>{val}",
                                         m.group(0)) + text[m.end():], f"id → {val}"

    if op == "APPEND_REL":  # 追加一条 relations（无 key 则新建）
        rtype = content.get("rtype", "prerequisite")
        target = content.get("target")
        if not target:
            return None
        rel = f"  - {{type: {rtype}, target: {target}}}"
        m = re.search(r"(?m)^relations\s*:\s*\[\s*\]\s*$", text)
        if m:
            return text[:m.start()] + f"relations:\n{rel}" + text[m.end():], \
                f"relations(空)→追加 {rtype}:{target}"
        m2 = _key_line(text, "relations")
        if m2:
            return text[:m2.end()] + f"\n{rel}" + text[m2.end():], \
                f"relations 追加 {rtype}:{target}"
        m3 = _key_line(text, "id")
        if not m3:
            return None
        return text[:m3.end()] + f"\nrelations:\n{rel}" + text[m3.end():], \
            f"新建 relations {rtype}:{target}"

    if op == "SET_REL_TARGET":  # 把第一条关系目标改为不存在
        val = content.get("value")
        m = re.search(r"(?m)^relations\s*:\s*\n((?:[ \t]+-[^\n]*\n)+)", text)
        if not m or not val:
            return None
        block = m.group(1)
        first = re.search(r"target\s*:\s*([A-Za-z0-9_-]+)", block)
        if not first:
            return None
        new_block = block[:first.start(1)] + val + block[first.end(1):]
        return text[:m.start(1)] + new_block + text[m.end(1):], f"关系目标 → {val}"

    if op == "SET_SERVES":  # 改证据卡 serves 为不存在原子
        val = content.get("value")
        m = _key_line(text, "serves")
        if not m or not val:
            return None
        return text[:m.start()] + f"serves: [{val}]" + text[m.end():], f"serves → {val}"

    if op == "SET_MIS":  # 原子卡 misconceptions 指向不存在误解
        val = content.get("value")
        if not val:
            return None
        m = _key_line(text, "misconceptions")
        if m:
            return text[:m.start()] + f"misconceptions: [{val}]" + text[m.end():], \
                f"misconceptions → {val}"
        m2 = _key_line(text, "id")
        if not m2:
            return None
        return text[:m2.end()] + f"\nmisconceptions: [{val}]" + text[m2.end():], \
            f"新建 misconceptions → {val}"

    if op == "SET_ARTIFACT":  # 工件路径指向不存在文件（孤儿 provenance）
        val = content.get("value")
        m = _key_line(text, "artifact")
        if not m or not val:
            return None
        return text[:m.start()] + f"artifact: {val}" + text[m.end():], f"artifact → {val}"

    # 回落到 622 单卡原语
    return base.plan_edit(content, text)


# ── 跨卡沙箱 ─────────────────────────────────────────────────────────────────
class CrossCardSandbox(base.Sandbox):
    """多卡 apply/restore（继承 622 的单卡 Sandbox：并发锁/gate/校验/白名单）。"""

    def _plan(self, content: dict, text: str) -> tuple[str, str] | None:
        """编辑原语（子类可覆盖，如 A4 的 X5–X8）。"""
        return plan_edit_624(content, text)

    def apply_mutation(self, mutation: dict, card_rel: str) -> dict:  # noqa: D102
        if not base.is_allowed(card_rel):
            return {"applied": False, "reason": f"路径不在白名单 {ALLOWED_PREFIXES}"}
        path = self._abs(card_rel)
        if not os.path.exists(path):
            return {"applied": False, "reason": "卡不存在"}
        raw = open(path, "rb").read()
        text = raw.decode("utf-8")
        content = json.loads(mutation.get("content") or "null") or {}
        planned = self._plan(content, text)
        if planned is None:
            return {"applied": False, "reason": f"无法施加 op={content.get('op')}",
                    "backup_sha256": base._sha256_bytes(raw)}
        new_text, desc = planned
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new_text)
        return {"applied": True, "desc": desc, "path": path,
                "backup_sha256": base._sha256_bytes(raw), "backup_bytes": raw}

    def apply_multi(self, edits: list[dict]) -> dict:
        """把一组 edits（多卡）一次性施加；任一失败则回滚已施加的卡。

        **关键修复（624 A1 修正）**：同一张卡可能被多条 edit 命中（如 X4 对同一证据卡
        同时改 serves 与 artifact）。必须**每张卡只备份一次原始字节**、把多条 edit 顺序
        施加到同一文本上；否则 restore 按 edit 逐条还原时，会把中间态写回 ⇒ 受控目录残留。
        """
        order: list[str] = []
        by: dict[str, list[dict]] = {}
        for e in edits:
            c = e.get("card")
            if not c:
                return {"applied": False, "reason": "edit 缺 card", "n_edits": len(edits)}
            if c not in by:
                by[c] = []
                order.append(c)
            by[c].append(e)

        backups: list[dict] = []

        def _rollback() -> None:
            for b in reversed(backups):
                self.restore(b["card"], b)

        for c in order:
            if not base.is_allowed(c):
                _rollback()
                return {"applied": False, "reason": f"路径不在白名单 {ALLOWED_PREFIXES}",
                        "failed_card": c, "n_edits": len(edits)}
            path = self._abs(c)
            if not os.path.exists(path):
                _rollback()
                return {"applied": False, "reason": "卡不存在", "failed_card": c,
                        "n_edits": len(edits)}
            raw = open(path, "rb").read()
            text = raw.decode("utf-8")
            descs: list[str] = []
            for e in by[c]:
                planned = self._plan(e, text)
                if planned is None:
                    _rollback()
                    return {"applied": False, "reason": f"无法施加 op={e.get('op')}",
                            "failed_card": c, "n_edits": len(edits)}
                text, d = planned
                descs.append(d)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
            backups.append({"card": c, "applied": True, "desc": "; ".join(descs), "path": path,
                            "backup_bytes": raw, "backup_sha256": base._sha256_bytes(raw)})
        return {"applied": True, "backups": backups, "n_edits": len(edits)}

    def restore_multi(self, backups: list[dict]) -> dict:
        """还原所有被改卡；校验每张 sha256。"""
        bad: list[str] = []
        for b in backups:
            if not b.get("applied"):
                continue
            r = self.restore(b["card"], b)
            if not r.get("restored"):
                bad.append(b["card"])
        return {"restored": not bad, "bad": bad,
                "reason": "" if not bad else f"还原后 sha256 不符：{bad}"}

    def apply_and_run_multi(self, mutation: dict, baseline: dict | None = None) -> dict:
        """apply 多卡 → 跑 gate → 还原所有卡（finally 必还原）。"""
        t0 = time.time()
        edits = mutation.get("edits") or []
        if not edits:
            return {"mutation_id": mutation.get("mutation_id"), "verdict": "infra_error",
                    "reason": "无 edits", "elapsed_ms": 0}
        applied = self.apply_multi(edits)
        if not applied.get("applied"):
            return {"mutation_id": mutation.get("mutation_id"),
                    "strategy": mutation.get("strategy"),
                    "verdict": "infra_error", "reason": applied.get("reason"),
                    "failed_card": applied.get("failed_card"),
                    "elapsed_ms": int((time.time() - t0) * 1000)}
        cards = [e["card"] for e in edits]
        try:
            gj = self._run_gate_raw()
        finally:
            rst = self.restore_multi(applied["backups"])
        if not rst.get("restored"):
            return {"mutation_id": mutation.get("mutation_id"),
                    "strategy": mutation.get("strategy"),
                    "verdict": "infra_error", "reason": rst.get("reason"),
                    "elapsed_ms": int((time.time() - t0) * 1000)}

        after: set[tuple[str, str]] = set()
        before: set[tuple[str, str]] = set()
        for c in cards:
            for f in self.findings_for(gj, c):
                after.add((str(f.get("rule")), str(f.get("severity"))))
            for f in self.findings_for(baseline or {}, c):
                before.add((str(f.get("rule")), str(f.get("severity"))))
        new_blocks = sorted({r for r, s in (after - before) if s == "block"})
        new_nonblock = sorted({r for r, s in (after - before) if s != "block"})
        lost = sorted({r for r, s in (before - after)})
        if new_blocks:
            verdict = "blocked"
        elif lost:
            verdict = "escaped"
        elif new_nonblock:
            verdict = "detected_nonblock"
        else:
            verdict = "neutral"
        return {
            "mutation_id": mutation.get("mutation_id"),
            "strategy": mutation.get("strategy"),
            "cards": cards,
            "verdict": verdict,
            "new_block_rules": new_blocks,
            "new_nonblock_rules": new_nonblock,
            "lost_rules": lost,
            "n_findings_before": len(before),
            "n_findings_after": len(after),
            "elapsed_ms": int((time.time() - t0) * 1000),
        }


# ── 生成器 ───────────────────────────────────────────────────────────────────
def _complexity(strategy: str, n_edits: int) -> int:
    """跨卡攻击需理解卡间关系 ⇒ 复杂度高于单卡 field-edit（目标 >60）。"""
    base_score = {"X1": 66, "X2": 72, "X3": 78, "X4": 70}.get(strategy, 65)
    return min(100, base_score + 3 * (n_edits - 2))


def _pick(seq, i):
    return seq[i % len(seq)] if seq else None


def generate_mutations(inv: dict, per_strategy: int = 15) -> list[dict]:
    atoms = inv["atoms"]
    evidence = inv["evidence"]
    ids = inv["ids"]
    out: list[dict] = []
    n = 0

    # X1 悬空引用：A 引用 B（真实存在），把 B 的 id 改掉 ⇒ A 悬空 + B 孤儿
    x1_src = [a for a in atoms if any(r.get("target") in ids for r in a["relations"])]
    x1_src = x1_src or [a for a in atoms if a["relations"]]
    x1_src = x1_src or atoms
    for i in range(per_strategy):
        a = _pick(x1_src, i)
        tgt_id = next((r["target"] for r in a["relations"] if r.get("target")), None)
        b = next((c for c in atoms + evidence if c["id"] == tgt_id), None)
        if a is None:
            break
        n += 1
        b = b or _pick(atoms, i + 1)
        edits = [{"card": a["card"], "op": "SET_REL_TARGET", "value": "ATOM-NOPE-999"}]
        if b and b["card"] != a["card"]:
            edits.append({"card": b["card"], "op": "SET_ID", "value": "ATOM-ORPHAN-999"})
        out.append(_mk(f"X1-{i+1:03d}", "X1", "悬空引用", edits))

    # X2 循环引用：A 依赖 B、B 依赖 A
    for i in range(per_strategy):
        a = _pick(atoms, i * 2)
        b = _pick(atoms, i * 2 + 1)
        if not a or not b or a["card"] == b["card"]:
            continue
        edits = [{"card": a["card"], "op": "APPEND_REL", "rtype": "prerequisite",
                  "target": b["id"]},
                 {"card": b["card"], "op": "APPEND_REL", "rtype": "prerequisite",
                  "target": a["id"]}]
        out.append(_mk(f"X2-{i+1:03d}", "X2", "循环引用", edits))

    # X3 矛盾引用：A supports B、B contradicts A
    for i in range(per_strategy):
        a = _pick(atoms, i * 2 + 1)
        b = _pick(atoms, i * 2 + 2)
        if not a or not b or a["card"] == b["card"]:
            continue
        edits = [{"card": a["card"], "op": "APPEND_REL", "rtype": "supports", "target": b["id"]},
                 {"card": b["card"], "op": "APPEND_REL", "rtype": "contradicts", "target": a["id"]}]
        out.append(_mk(f"X3-{i+1:03d}", "X3", "矛盾引用", edits))

    # X4 孤儿引用：证据 serves 不存在原子 + 原子引不存在误解 + artifact 指向不存在文件
    for i in range(per_strategy):
        e = _pick(evidence, i)
        a = _pick(atoms, i)
        if not e or not a:
            continue
        edits = [{"card": e["card"], "op": "SET_SERVES", "value": "ATOM-NOPE-999"},
                 {"card": e["card"], "op": "SET_ARTIFACT",
                  "value": "Examples/nonexistent_zzz_624.asm"},
                 {"card": a["card"], "op": "SET_MIS", "value": "MIS-NOPE-999"}]
        out.append(_mk(f"X4-{i+1:03d}", "X4", "孤儿引用", edits))

    return out


def _mk(mid: str, strategy: str, attack_type: str, edits: list[dict]) -> dict:
    return {"mutation_id": mid, "strategy": strategy, "attack_type": attack_type,
            "complexity": _complexity(strategy, len(edits)),
            "predicted_rules": STRATEGY_PREDICT.get(strategy, []),
            "edits": edits}


# ── 批量运行 ─────────────────────────────────────────────────────────────────
def run_batch(mutations: list[dict], sb: CrossCardSandbox | None = None,
              baseline: dict | None = None, log=print) -> dict:
    sb = sb or CrossCardSandbox()
    base_json = baseline if baseline is not None else sb.gate_all()
    rows: list[dict] = []
    t0 = time.time()
    with sb:
        for i, m in enumerate(mutations, 1):
            rows.append(sb.apply_and_run_multi(m, base_json))
            if i % 10 == 0:
                log(f"  …{i}/{len(mutations)} 完成（{int(time.time() - t0)}s）")
    dist: dict[str, int] = {}
    for r in rows:
        dist[r["verdict"]] = dist.get(r["verdict"], 0) + 1
    touched_block: set[str] = set()
    touched_nonblock: set[str] = set()
    for r in rows:
        touched_block |= set(r.get("new_block_rules") or [])
        touched_nonblock |= set(r.get("new_nonblock_rules") or [])
    return {"rows": rows, "distribution": dict(sorted(dist.items())),
            "escaped": [r for r in rows if r["verdict"] == "escaped"],
            "touched_block": sorted(touched_block),
            "touched_nonblock": sorted(touched_nonblock),
            "touched_all": sorted(touched_block | touched_nonblock),
            "total": len(rows), "elapsed_s": round(time.time() - t0, 1)}


# ── 自检（只读 + 临时改必还原）─────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    inv = load_inventory()
    chk("枚举原子卡", len(inv["atoms"]) >= 20)
    chk("枚举证据卡", len(inv["evidence"]) >= 30)

    muts = generate_mutations(inv, per_strategy=15)
    by = {}
    for m in muts:
        by.setdefault(m["strategy"], []).append(m)
    chk("生成 60 条（4 策略各 15）", len(muts) == 60)
    chk("X1 生成 15 条且多卡", len(by.get("X1", [])) == 15 and all(len(m["edits"]) >= 1 for m in by["X1"]))
    chk("X2 循环=双卡互指", any(len(m["edits"]) == 2 for m in by.get("X2", [])))
    chk("X3 矛盾=supports+contradicts", any(
        {e["rtype"] for e in m["edits"]} == {"supports", "contradicts"} for m in by.get("X3", [])))
    chk("X4 孤儿含 serves 不存在", any(
        any(e["op"] == "SET_SERVES" for e in m["edits"]) for m in by.get("X4", [])))
    chk("跨卡复杂度 >60", all(m["complexity"] > 60 for m in muts))

    # 多卡编辑原语
    text = "---\nid: ATOM-X\nrelations: []\nmisconceptions: [MIS-A]\n---\nbody\n"
    e1 = plan_edit_624({"op": "APPEND_REL", "rtype": "supports", "target": "ATOM-Y"}, text)
    chk("APPEND_REL 可行", e1 is not None and "target: ATOM-Y" in e1[0])
    e2 = plan_edit_624({"op": "SET_MIS", "value": "MIS-NOPE-999"}, text)
    chk("SET_MIS 可行", e2 is not None and "MIS-NOPE-999" in e2[0])
    chk("路径白名单：tools 拒绝", not base.is_allowed("tools/x.py"))
    chk("路径白名单：atoms 允许", base.is_allowed("atoms/conc/ATOM-CONC-FENCE-001.md"))

    # 多卡备份/还原（临时改必还原，校验 sha256 不变）
    sb = CrossCardSandbox()
    target = inv["atoms"][0]["card"]
    original = open(sb._abs(target), "rb").read()
    sha_before = base._sha256_bytes(original)
    applied = sb.apply_multi([{"card": target, "op": "APPEND_REL", "rtype": "supports",
                               "target": "ATOM-SELFTEST-999"}])
    restored = sb.restore_multi(applied.get("backups", [])) if applied.get("applied") else {"restored": False}
    sha_after = base._sha256_bytes(open(sb._abs(target), "rb").read())
    chk("多卡 apply+restore 后 sha256 不变",
        bool(applied.get("applied")) and restored.get("restored") and sha_before == sha_after)

    # 同一张卡多编辑（X4 场景）：必须只备份一次、还原后 sha256 不变
    sha_b1 = base._sha256_bytes(open(sb._abs(target), "rb").read())
    applied2 = sb.apply_multi([
        {"card": target, "op": "APPEND_REL", "rtype": "supports", "target": "ATOM-SELFTEST-998"},
        {"card": target, "op": "APPEND_REL", "rtype": "contradicts", "target": "ATOM-SELFTEST-997"},
    ])
    restored2 = sb.restore_multi(applied2.get("backups", [])) if applied2.get("applied") else {"restored": False}
    sha_b2 = base._sha256_bytes(open(sb._abs(target), "rb").read())
    chk("同卡多编辑 apply+restore 后 sha256 不变（备份去重）",
        bool(applied2.get("applied")) and len(applied2.get("backups", [])) == 1
        and restored2.get("restored") and sha_b1 == sha_b2)

    print(f"A1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="624 A1 跨卡一致性攻击")
    ap.add_argument("--check", action="store_true", help="只读自检，exit 0 = 通过")
    ap.add_argument("--gen", action="store_true", help="生成 60 条跨卡 mutation 并打印")
    ap.add_argument("--run", action="store_true", help="沙箱实跑（真跑 gate）")
    ap.add_argument("--out", help="结果 JSON 输出路径")
    ap.add_argument("--per-strategy", type=int, default=15)
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    inv = load_inventory()
    muts = generate_mutations(inv, per_strategy=args.per_strategy)

    if args.gen:
        print(json.dumps(muts, ensure_ascii=False, indent=2))
        return 0

    if args.run:
        res = run_batch(muts)
        res["predicted_rules"] = sorted({r for m in muts for r in m["predicted_rules"]})
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump({"mutations": muts, **res}, fh, ensure_ascii=False, indent=2)
        print(json.dumps({k: v for k, v in res.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
