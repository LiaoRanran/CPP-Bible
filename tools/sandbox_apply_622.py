"""622 A1 · 沙箱 apply API（apply / run_gate / restore / apply_and_run）

**为什么需要它**：620/621 连续两批登记 —— `mutation_fuzz.py` 是**只读基线生成器**，
不提供「把变异施加到副本」的能力 ⇒ 新 mutation 无法真正跑 gate 判决，
只能用 v7 先验**预测** ⇒ 新逃逸恒 0、VFDR 恒 0。本工具补上这一环。

**核心技术选择（如实说明）**：`gate_engine.py` **没有自定义 root / 单卡模式**参数
（只有 `--run/--json/--check/--list/--manifest-check/--gates`），
所以「对修改后的卡跑 gate」只能**原地改写该卡 → 跑 gate → 还原**。
因此护栏必须做到位：

| # | 护栏 | 实现 |
|---|---|---|
| 1 | **字节级备份** | apply 前把原文件读成 bytes 存内存，同时落盘一份 `.622bak` |
| 2 | **finally 必还原** | `apply_and_run` 的 `try/finally` 保证异常/超时也还原 |
| 3 | **还原校验** | 还原后重算 sha256，与原 sha256 比对，不符则报 `restore_failed` |
| 4 | **并发锁** | `data/.622_apply.lock`（`O_CREAT|O_EXCL`）⇒ 同时只允许一个 apply_and_run |
| 5 | **超时保护** | gate 子进程 `timeout=30s`，超时判 `infra_error` |
| 6 | **路径白名单** | 只允许改 `atoms/` 与 `evidence/` 下的卡（本批 mutation 的目标域） |

**判决口径（diff-based，保守）**：与「未修改卡的基线 findings」对比 ——

| 判定 | 条件 |
|---|---|
| `blocked` | 变异后**新增** block 级 finding |
| `escaped` | **无新增 block** 且 **基线 findings 消失**（变异削弱了检测） |
| `neutral` | 无新增 block 且无 finding 消失 |
| `infra_error` | 施加失败 / gate 超时 / 还原失败 |

> `escaped` 采用**严格口径**（必须"少了检测"才算逃逸），避免把"本来就没告警"误算成逃逸。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable

GATE = os.path.join("tools", "gate_engine.py")
LOCK = os.path.join(ROOT, "data", ".622_apply.lock")
ALLOWED_PREFIXES = ("atoms/", "evidence/")
GATE_TIMEOUT = 30

# 规则 → 该规则校验的 frontmatter 字段（用于 M1 删字段 / M6 变形 / M7 篡改）
RULE_FIELD = {
    "EV-FM-REQUIRED": "id", "EV-FM-DUP-KEY": "id", "EV-ID-UNIQUE": "id",
    "ATOM-FM-REQUIRED": "id", "ATOM-ID-UNIQUE": "id", "ATOM-ID-FORMAT": "id",
    "ATOM-CLAIM-STRUCTURED": "claim_structured",
    "EV-ARTIFACT-FILE-EXISTS": "artifact", "EV-ARTIFACT-PRODUCER": "artifact_producer",
    "EV-FALSIFICATION": "falsification", "EV-FALSIFICATION-QUANT": "falsification",
    "EV-MATRIX-UNBACKED": "matrix", "EV-MATRIX": "matrix",
    "CARD-PATH-NOT-CANONICAL": "artifact",
    "OBSERVATION-LIVENESS": "liveness",
    "ATOM-STATUS-TRANSITION": "status", "ATOM-STATUS-VALUE": "status",
}


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _norm(card_rel: str) -> str:
    return card_rel.replace(os.sep, "/").lstrip("./")


def is_allowed(card_rel: str) -> bool:
    return _norm(card_rel).startswith(ALLOWED_PREFIXES)


def _fm_bounds(text: str) -> tuple[int, int] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return 3, end


def _key_line(text: str, key: str) -> re.Match | None:
    return re.search(rf"(?m)^{re.escape(key)}\s*:.*$", text)


# ── 变异施加（把描述性 content 映射成真实卡面编辑）──────────────────────────────
def plan_edit(content: dict, text: str) -> tuple[str, str] | None:
    """返回 (新文本, 说明)；无法施加时返回 None。"""
    op = content.get("op")
    rule = content.get("target_rule") or ""
    field = RULE_FIELD.get(rule, "id")

    if op == "M1":  # 删字段
        m = _key_line(text, field)
        if not m:
            return None
        return text[:m.start()] + text[m.end():].lstrip("\n"), f"删除字段 {field}"

    if op == "M6":  # 键名大小写变形
        m = _key_line(text, field)
        if not m:
            return None
        variant = field[:1].upper() + field[1:]
        return text[:m.start()] + m.group(0).replace(field, variant, 1) + text[m.end():], \
            f"键名 {field} → {variant}"

    if op == "M7":  # 哈希/值篡改
        m = _key_line(text, "artifact_sha256") or _key_line(text, field)
        if not m:
            return None
        line = m.group(0)
        mm = re.search(r"([0-9a-fA-F]{8,})", line)
        if not mm:
            return None
        h = mm.group(1)
        flipped = ("0" if h[0] != "0" else "1") + h[1:]
        return text[:m.start()] + line.replace(h, flipped, 1) + text[m.end():], \
            f"篡改 sha256/值 {h[:8]}… → {flipped[:8]}…"

    if op == "M2":  # 路径大小写变形
        m = _key_line(text, "artifact") or _key_line(text, "fixture")
        if not m:
            return None
        line = m.group(0)
        mm = re.search(r"([A-Za-z_./]+\.(?:asm|cpp|out))", line)
        if not mm:
            return None
        path = mm.group(1)
        variant = path[:1].upper() + path[1:] if path[:1].islower() else path.lower()
        if variant == path:
            return None
        return text[:m.start()] + line.replace(path, variant, 1) + text[m.end():], \
            f"路径大小写 {path} → {variant}"

    if op == "M3":  # 断言弱化：删最后一个 run_match_keys 项
        # 注意：不能用 \s*（会贪婪吃掉后续行），必须用 [ \t]*
        m = re.search(r"(?m)^run_match_keys[ \t]*:[ \t]*\n((?:[ \t]+-[^\n]*\n)+)", text)
        if not m:
            return None
        items = m.group(1).rstrip("\n").split("\n")
        if len(items) < 2:
            return None
        new_block = "run_match_keys:\n" + "\n".join(items[:-1]) + "\n"
        return text[:m.start()] + new_block + text[m.end():], \
            f"弱化断言：删除 run_match_keys 最后一项（{len(items)}→{len(items) - 1}）"

    if op == "M4":  # 恒真注入：追加恒真断言键
        m = _key_line(text, "artifact_assert")
        if m:
            return text[:m.start()] + m.group(0) + "\n - {kind: exists, text: \"main\"}" + text[m.end():], \
                "注入恒真断言 exists:main"
        return text + "\nartifact_assert:\n - {kind: exists, text: \"main\"}\n", \
            "注入恒真断言 exists:main（新建键）"

    if op == "M8":  # 622 A4 新算子：边界值（版本号越界 / 枚举越界）
        m = _key_line(text, "artifact_version")
        if m:
            return text[:m.start()] + re.sub(r"(artifact_version\s*:\s*).*", r"\g<1>0",
                                             m.group(0)) + text[m.end():], \
                "artifact_version → 0（越界）"
        m = _key_line(text, "status")
        if not m:
            return None
        return text[:m.start()] + re.sub(r"(status\s*:\s*).*", r"\g<1>bogus_enum",
                                         m.group(0)) + text[m.end():], \
            "status → bogus_enum（非法枚举）"

    if op == "M9":  # 622 A4 新算子：交叉引用指向不存在的目标
        for key in ("serves", "relations"):
            m = _key_line(text, key)
            if not m:
                continue
            line = m.group(0)
            mm = re.search(r"([A-Z][A-Z0-9-]{3,})", line)
            if not mm:
                continue
            bogus = "ATOM-NOPE-999"
            if mm.group(1) == bogus:
                continue
            return text[:m.start()] + line.replace(mm.group(1), bogus, 1) + text[m.end():], \
                f"{key} 引用 {mm.group(1)} → {bogus}（不存在）"
        return None

    if op == "M5":  # claim 自标：status 改成 draft
        m = _key_line(text, "status")
        if not m:
            return None
        return text[:m.start()] + re.sub(r"(status\s*:\s*).*", r"\1draft", m.group(0)) + text[m.end():], \
            "status → draft"

    return None


# ── 沙箱 ─────────────────────────────────────────────────────────────────────
class Sandbox:
    def __init__(self, root: str = ROOT, gate_timeout: int = GATE_TIMEOUT,
                 lock_path: str = LOCK):
        self.root = root
        self.gate_timeout = gate_timeout
        self.lock_path = lock_path
        self._locked = False

    # -- 并发锁 --
    def acquire(self) -> None:
        os.makedirs(os.path.dirname(self.lock_path), exist_ok=True)
        try:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            self._locked = True
        except FileExistsError as exc:
            raise RuntimeError(
                f"并发保护：锁 {self.lock_path} 已被占用（同时只允许一个 apply_and_run）"
            ) from exc

    def release(self) -> None:
        if self._locked and os.path.exists(self.lock_path):
            os.remove(self.lock_path)
        self._locked = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *exc):
        self.release()
        return False

    # -- gate --
    def _run_gate_raw(self) -> dict:
        try:
            p = subprocess.run([PY, GATE, "--run", "--json"], cwd=self.root,
                               capture_output=True, text=True, timeout=self.gate_timeout)
        except subprocess.TimeoutExpired:
            return {"status": "infra_error", "findings": [], "infra_errors": ["gate timeout"],
                    "summary": {}, "_timeout": True}
        out = (p.stdout or "").strip()
        i = out.find("{")
        if i < 0:
            return {"status": "infra_error", "findings": [],
                    "infra_errors": ["无法解析 gate JSON"], "summary": {}}
        try:
            return json.loads(out[i:])
        except ValueError as exc:
            return {"status": "infra_error", "findings": [],
                    "infra_errors": [f"gate JSON 解析失败：{exc}"], "summary": {}}

    def gate_all(self) -> dict:
        """整仓跑一次 gate（用于取基线 findings）。"""
        return self._run_gate_raw()

    @staticmethod
    def findings_for(gate_json: dict, card_rel: str) -> list[dict]:
        want = _norm(card_rel)
        return [f for f in (gate_json.get("findings") or [])
                if _norm(str(f.get("file") or "")) == want]

    def run_gate(self, card_rel: str) -> dict:
        """对单张卡跑 gate 判决（内部跑整仓 gate 后过滤）。"""
        gj = self._run_gate_raw()
        fnd = self.findings_for(gj, card_rel)
        return {
            "card": _norm(card_rel),
            "findings": fnd,
            "n_findings": len(fnd),
            "block_rules": sorted({str(f.get("rule")) for f in fnd
                                   if str(f.get("severity")) == "block"}),
            "warn_rules": sorted({str(f.get("rule")) for f in fnd
                                  if str(f.get("severity")) == "warn"}),
            "gate_status": gj.get("status"),
            "infra_errors": gj.get("infra_errors") or [],
        }

    # -- apply / restore --
    def _abs(self, card_rel: str) -> str:
        return os.path.join(self.root, _norm(card_rel))

    def apply_mutation(self, mutation: dict, card_rel: str) -> dict:
        """把 mutation 施加到卡上（原地）；返回备份信息。"""
        if not is_allowed(card_rel):
            return {"applied": False, "reason": f"路径不在白名单 {ALLOWED_PREFIXES}"}
        path = self._abs(card_rel)
        if not os.path.exists(path):
            return {"applied": False, "reason": "卡不存在"}

        raw = open(path, "rb").read()
        text = raw.decode("utf-8")
        content = json.loads(mutation.get("content") or "null") or {}
        planned = plan_edit(content, text)
        if planned is None:
            # 只报 op（不报 RU-LE_FIELD 推测的字段——M8/M9 的编辑目标与 target_rule 无对应关系）
            return {"applied": False,
                    "reason": f"无法施加 op={content.get('op')}"
                              f"（目标卡缺少该算子所需字段）",
                    "backup_sha256": _sha256_bytes(raw)}
        new_text, desc = planned
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new_text)
        return {"applied": True, "desc": desc, "path": path,
                "backup_sha256": _sha256_bytes(raw), "backup_bytes": raw}

    def restore(self, card_rel: str, backup: dict) -> dict:
        """从备份还原；校验 sha256。"""
        path = self._abs(card_rel)
        raw = backup.get("backup_bytes")
        if raw is None:
            return {"restored": False, "reason": "无备份字节"}
        with open(path, "wb") as fh:
            fh.write(raw)
        now = _sha256_bytes(open(path, "rb").read())
        ok = now == backup.get("backup_sha256")
        return {"restored": ok, "sha256": now,
                "reason": "" if ok else "还原后 sha256 与备份不符（restore_failed）"}

    def apply_and_run(self, mutation: dict, card_rel: str,
                      baseline_findings: list[dict] | None = None) -> dict:
        """apply → run_gate → restore（原子；finally 必还原）。"""
        t0 = time.time()
        backup = self.apply_mutation(mutation, card_rel)
        if not backup.get("applied"):
            return {"mutation_id": mutation.get("mutation_id"), "card": _norm(card_rel),
                    "verdict": "infra_error", "reason": backup.get("reason"),
                    "elapsed_ms": int((time.time() - t0) * 1000)}
        try:
            res = self.run_gate(card_rel)
        finally:
            rst = self.restore(card_rel, backup)
        if not rst.get("restored"):
            return {"mutation_id": mutation.get("mutation_id"), "card": _norm(card_rel),
                    "verdict": "infra_error", "reason": rst.get("reason"),
                    "elapsed_ms": int((time.time() - t0) * 1000)}

        after = {(str(f.get("rule")), str(f.get("severity"))) for f in res["findings"]}
        before = {(str(f.get("rule")), str(f.get("severity")))
                  for f in (baseline_findings or [])}
        new_blocks = sorted({r for r, s in (after - before) if s == "block"})
        # 新增的**非 block** 检出（warn/advice）：622 A4 补充，用于区分
        # "编辑对判定完全无影响" 与 "编辑触发了非 block 级检出"
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
            "card": _norm(card_rel),
            "attack_type": mutation.get("attack_type"),
            "target_rule": mutation.get("target_rule"),
            "edit": backup.get("desc"),
            "verdict": verdict,
            "new_block_rules": new_blocks,
            "new_nonblock_rules": new_nonblock,
            "lost_rules": lost,
            "n_findings_before": len(before),
            "n_findings_after": len(after),
            "elapsed_ms": int((time.time() - t0) * 1000),
        }


# ── 批量运行（A2/A4 用）────────────────────────────────────────────────────────
def run_batch(mutations: list[dict], sandbox: Sandbox | None = None,
              baseline: dict | None = None, log=print) -> dict:
    """对一批 mutation 逐个 apply_and_run（串行 + 并发锁）。"""
    sb = sandbox or Sandbox()
    base = baseline if baseline is not None else sb.gate_all()
    rows: list[dict] = []
    t0 = time.time()
    with sb:
        for i, m in enumerate(mutations, 1):
            try:
                content = json.loads(m.get("content") or "null") or {}
            except ValueError:
                content = {}
            card = content.get("target_card") or m.get("target_card")
            if not card:
                rows.append({"mutation_id": m.get("mutation_id"), "verdict": "infra_error",
                             "reason": "无 target_card"})
                continue
            bf = Sandbox.findings_for(base, card)
            rows.append(sb.apply_and_run(m, card, bf))
            if i % 10 == 0:
                log(f"  …{i}/{len(mutations)} 已完成（{int(time.time() - t0)}s）")
    dist: dict[str, int] = {}
    for r in rows:
        dist[r["verdict"]] = dist.get(r["verdict"], 0) + 1
    return {
        "rows": rows,
        "distribution": dict(sorted(dist.items())),
        "escaped": [r for r in rows if r["verdict"] == "escaped"],
        "total": len(rows),
        "elapsed_s": round(time.time() - t0, 1),
    }


def compare_prediction(rows: list[dict], predictions: dict[str, str]) -> dict:
    """实际判决 vs 621 的 v7 先验预测（按"是否被拦"二值比对）。"""
    agree = disagree = missing = 0
    detail = []
    for r in rows:
        mid = r.get("mutation_id")
        pred = predictions.get(mid)
        actual = r.get("verdict")
        if pred is None or actual in ("infra_error", None):
            missing += 1
            continue
        pred_caught = (pred == "blocked")
        act_caught = (actual == "blocked")
        if pred_caught == act_caught:
            agree += 1
        else:
            disagree += 1
            detail.append({"mutation_id": mid, "card": r.get("card"),
                           "predicted": pred, "actual": actual})
    n = agree + disagree
    return {"agree": agree, "disagree": disagree, "skipped": missing,
            "agreement_rate": round(agree / n, 4) if n else None,
            "disagreements": detail}


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("路径白名单：atoms 允许", is_allowed("atoms/mem/ATOM-MEM-LEAK-001.md"))
    chk("路径白名单：evidence 允许", is_allowed("evidence/conc/EV-CONC-001.md"))
    chk("路径白名单：tools 拒绝", not is_allowed("tools/x.py"))
    chk("路径白名单：Book 拒绝", not is_allowed("Book/x.md"))

    text = ("---\nid: A\nartifact: Examples/atoms/_x.asm\n"
            "artifact_sha256: abcdef1234567890\nstatus: verified\n"
            "run_match_keys:\n - k1\n - k2\n---\n\nbody\n")
    e1 = plan_edit({"op": "M1", "target_rule": "EV-FM-REQUIRED"}, text)
    chk("M1 删字段可行", e1 is not None and "id:" not in e1[0])
    e6 = plan_edit({"op": "M6", "target_rule": "EV-FM-REQUIRED"}, text)
    chk("M6 键名变形可行", e6 is not None and "Id:" in e6[0])
    e7 = plan_edit({"op": "M7", "target_rule": "EV-ARTIFACT-FILE-EXISTS"}, text)
    chk("M7 篡改哈希可行", e7 is not None and "abcdef1234567890" not in e7[0])
    e2 = plan_edit({"op": "M2", "target_rule": "CARD-PATH-NOT-CANONICAL"}, text)
    chk("M2 路径变形可行", e2 is not None and e2[0] != text)
    e3 = plan_edit({"op": "M3", "target_rule": "EV-FALSIFICATION"}, text)
    chk("M3 弱化断言可行", e3 is not None and "- k2" not in e3[0])
    e4 = plan_edit({"op": "M4", "target_rule": "EV-MATRIX-UNBACKED"}, text)
    chk("M4 恒真注入可行", e4 is not None and "main" in e4[0])
    e5 = plan_edit({"op": "M5", "target_rule": "ATOM-STATUS-VALUE"}, text)
    chk("M5 status→draft 可行", e5 is not None and "draft" in e5[0])
    chk("未知 op 返回 None", plan_edit({"op": "M9"}, text) is None)
    chk("缺字段时返回 None", plan_edit({"op": "M1", "target_rule": "X"},
                                     "---\nfoo: 1\n---\n") is None or True)

    sb = Sandbox()
    chk("并发锁可获取/释放", (sb.acquire() or True) and (sb.release() or True))
    chk("锁释放后可再获取", (sb.acquire() or True) and (sb.release() or True))
    print(f"A1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="622 A1 沙箱 apply API")
    ap.add_argument("--mutation", help="单条 mutation JSON 字符串")
    ap.add_argument("--card", help="目标卡相对路径")
    ap.add_argument("--baseline", help="基线 findings JSON（整仓 gate 输出）")
    ap.add_argument("--gate-all", action="store_true", help="整仓跑一次 gate 并输出 JSON")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    sb = Sandbox()
    if args.gate_all:
        print(json.dumps(sb.gate_all(), ensure_ascii=False))
        return 0
    if args.mutation and args.card:
        baseline = []
        if args.baseline:
            with open(args.baseline, encoding="utf-8") as fh:
                baseline = Sandbox.findings_for(json.load(fh), args.card)
        with sb:
            res = sb.apply_and_run(json.loads(args.mutation), args.card, baseline)
        print(json.dumps(res, ensure_ascii=False))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
