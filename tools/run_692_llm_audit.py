#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_692_llm_audit.py — 692-C：LLM-as-evidence-asset 审计迁移研究（N=80 × 2 模型 × 2 prompt）。

协议先落盘：`data/692_llm_audit_protocol.md`（样本/模型/prompt/四态/四指标/判据，跑之前写死）。
定位：LLM **不是 oracle**，是第 4 类 evidence asset，与 sanitizer 有不同 failure topology；
测的是 **audit protocol 的 modality-independence**，不是谁更准。
红线：凭据只从 .env 读且不打印；逐条落盘可断点续跑；API 不可用如实记 unknown，不编造。

用法：
    python tools/run_692_llm_audit.py            # 跑 + 汇总
    python tools/run_692_llm_audit.py --analyze  # 只汇总
    python tools/run_692_llm_audit.py --limit 2  # 小样调试
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
RAW = ROOT / "data" / "692_llm_audit_raw.jsonl"
OUT = ROOT / "data" / "692_llm_audit_results.json"

SEED = 6921
N_PER_STRATUM = 40
MODELS: tuple[tuple[str, str], ...] = (("A_glm-4.5", "glm-4.5"), ("B_glm-4-flash", "glm-4-flash"))
PROMPTS: tuple[str, ...] = ("p1", "p2")
MAX_LINES = 400
MAX_TOKENS = 700
TIMEOUT_S = 120
DEFECT_WORDS = (
    "double free", "use after free", "use-after-free", "out of bounds", "out-of-bounds",
    "data race", "leak", "uninitialized", "uninitialised", "dangling", "overflow",
    "null deref", "buffer overflow", "dereference", "invalid pointer", "deadlock",
)


def load_dotenv() -> dict[str, str]:
    env: dict[str, str] = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def strip_comments(src: str) -> str:
    """剥离 // 与 /* */ 注释（答案泄漏控制），保留字符串/字符字面量。"""
    out: list[str] = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'":
            quote = c
            out.append(c)
            i += 1
            while i < n:
                if src[i] == "\\" and i + 1 < n:
                    out.append(src[i:i + 2])
                    i += 2
                    continue
                out.append(src[i])
                if src[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            while i < n and src[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            i = (j + 2) if j >= 0 else n
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _av(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell)


def build_pool() -> list[dict[str, Any]]:
    d = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for s in d["samples"]:
        if s.get("split") != "evaluation":
            continue
        fp = s.get("file_path") or ""
        if not fp or fp == "(inline_code)":
            continue
        ap = ROOT / fp
        if not ap.exists():
            continue
        pa = s.get("per_asset", {})
        san = "catch" if any(_av(pa.get(a, "unknown")) == "catch" for a in ("asan", "ubsan", "tsan")) else "miss"
        rows.append({
            "uid": s["sample_id"], "file_rel": fp, "file_abs": str(ap),
            "expected_verdict": s.get("expected_verdict"), "defect_group": s.get("defect_group"),
            "defect_type": s.get("defect_type"), "or_verdict": s.get("or_verdict"), "san_or": san,
            "planted": bool(s.get("planted", True)),
        })
    rows.sort(key=lambda r: r["uid"])
    return rows


def select_sample(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pos = [r for r in rows if r["expected_verdict"] == "catch"]
    neg = [r for r in rows if r["expected_verdict"] == "miss"]
    rng = random.Random(SEED)
    sel = rng.sample(pos, N_PER_STRATUM) + rng.sample(neg, N_PER_STRATUM)
    sel.sort(key=lambda r: r["uid"])
    return sel


def read_code(row: dict[str, Any]) -> tuple[str, bool]:
    txt = strip_comments(Path(row["file_abs"]).read_text(encoding="utf-8", errors="replace"))
    lines = txt.splitlines()
    truncated = len(lines) > MAX_LINES
    if truncated:
        lines = lines[:MAX_LINES] + ["/*[truncated]*/"]
    return "\n".join(lines), truncated


def make_prompt(kind: str, code: str) -> str:
    if kind == "p1":
        return (
            "You are a C++ code reviewer. Decide whether the code below contains a defect that can cause "
            "undefined behavior, a memory error, a concurrency error, or a clear API misuse.\n"
            "Reply with ONLY a JSON object, no prose, exactly these keys:\n"
            '{"has_defect": <true|false>, "category": "<short label>", "confidence": <0..1>, "reason": "<one sentence>"}\n'
            "Do not guess file names, provenance, or which tool would detect anything.\n"
            "Code:\n```cpp\n" + code + "\n```\n"
        )
    return (
        "Task: judge whether the following C++ snippet has a defect that can cause undefined behavior, a memory "
        "error, a concurrency error, or a clear API misuse.\n"
        "Answer as compact JSON only (no text outside the JSON), keys in this order: "
        '"confidence" (<0..1>), "has_defect" (<true|false>), "category" ("<short label>"), "reason" ("<one sentence>").\n'
        "Do not speculate about file names, provenance, or detectors.\n"
        "Snippet:\n```cpp\n" + code + "\n```\n"
    )


def call_model(base: str, key: str, model: str, prompt: str, max_tokens: int = MAX_TOKENS) -> dict[str, Any]:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body,
                                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            d = json.loads(r.read().decode())
        return {"status": "ok", "content": d["choices"][0]["message"].get("content") or "",
                "latency_s": round(time.time() - t0, 2), "usage": d.get("usage"),
                "finish_reason": d["choices"][0].get("finish_reason")}
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read()[:300].decode(errors="replace")
        except Exception:  # noqa: BLE001
            pass
        return {"status": "http_error", "http_status": e.code, "error": detail, "latency_s": round(time.time() - t0, 2)}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": f"{type(e).__name__}: {e}"[:200], "latency_s": round(time.time() - t0, 2)}


JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_verdict(resp: dict[str, Any]) -> dict[str, Any]:
    """四态判定（判据写死，见协议 §4）。"""
    if resp.get("status") != "ok":
        return {"state": "unknown", "why": f"api_{resp.get('status')}"}
    content = str(resp.get("content", ""))
    m = JSON_RE.search(content)
    if not m:
        return {"state": "unknown", "why": "no_json", "content_head": content[:200]}
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"state": "unknown", "why": "bad_json", "content_head": content[:200]}
    hd = obj.get("has_defect")
    if not isinstance(hd, bool):
        return {"state": "unknown", "why": "no_bool", "content_head": content[:200]}
    cat = str(obj.get("category", "")).strip()
    reason = str(obj.get("reason", ""))
    try:
        conff = min(1.0, max(0.0, float(obj.get("confidence"))))
    except (TypeError, ValueError):
        conff = None
    low = reason.lower()
    if hd is False and any(w in low for w in DEFECT_WORDS):
        return {"state": "contradiction", "why": "reason_names_defect", "confidence": conff,
                "category": cat, "reason": reason[:300]}
    if hd is True and cat.lower() in ("", "none", "n/a", "no"):
        return {"state": "contradiction", "why": "catch_without_category", "confidence": conff,
                "category": cat, "reason": reason[:300]}
    return {"state": "catch" if hd else "miss", "confidence": conff, "category": cat, "reason": reason[:300]}


def done_keys(retry_only: bool = False) -> set[tuple[str, str, str, str]]:
    """已完成的缓存键。``retry_only=True`` 时**只把 API 成功的记录算作已完成**（失败可重试）。"""
    keys: set[tuple[str, str, str, str]] = set()
    if RAW.exists():
        for line in RAW.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if retry_only and str(r.get("api_status")) != "ok":
                continue
            keys.add((str(r["uid"]), str(r["model_slot"]), str(r["prompt"]), str(r.get("run_tag", "default"))))
    return keys


def do_run(limit: int | None, tag: str = "default", max_tokens: int = MAX_TOKENS,
           only_slots: tuple[str, ...] = (), retry_failed: bool = False, delay: float = 0.0) -> int:
    """``tag`` 区分不同补全预算的轮次（协议 §7 修订 A1），缓存键含 tag ⇒ 两轮互不覆盖。

    ``retry_failed=True`` 只把 API 成功的记录当作已完成 ⇒ 失败（限流/超时）会被重试；
    ``delay`` 为两次调用之间的礼貌间隔（限流恢复用）。
    """
    env = load_dotenv()
    base, key = env.get("ZHIPU_BASE_URL", ""), env.get("ZHIPU_API_KEY", "")
    if not base or not key:
        print("!! ZHIPU_BASE_URL / ZHIPU_API_KEY 缺失 ⇒ 无法执行（如实登记，不编造）")
        return 2
    sel = select_sample(build_pool())
    if limit:
        sel = sel[:limit]
    have = done_keys(retry_only=retry_failed)
    codes = {r["uid"]: read_code(r) for r in sel}
    slots = tuple(s for s, _ in MODELS if not only_slots or s in only_slots)
    print(f"selected={len(sel)} cached_calls={len(have)} tag={tag} max_tokens={max_tokens} slots={slots}",
          flush=True)
    n_done = 0
    with RAW.open("a", encoding="utf-8") as fh:
        for r in sel:
            code, trunc = codes[r["uid"]]
            for slot, model in MODELS:
                if slot not in slots:
                    continue
                for p in PROMPTS:
                    if (r["uid"], slot, p, tag) in have:
                        continue
                    resp = call_model(base, key, model, make_prompt(p, code), max_tokens)
                    parsed = parse_verdict(resp)
                    fh.write(json.dumps({
                        "uid": r["uid"], "model_slot": slot, "model_id": model, "prompt": p,
                        "run_tag": tag, "max_tokens": max_tokens,
                        "truncated": trunc, "code_lines": len(code.splitlines()),
                        "api_status": resp.get("status"), "latency_s": resp.get("latency_s"),
                        "error": resp.get("error"), "http_status": resp.get("http_status"),
                        "usage": resp.get("usage"), "finish_reason": resp.get("finish_reason"),
                        "verdict": parsed, "ts": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                    }, ensure_ascii=False) + "\n")
                    fh.flush()
                    n_done += 1
                    if delay:
                        time.sleep(delay)
                    if n_done % 20 == 0:
                        print(f"  calls={n_done} last={r['uid']}/{slot}/{p} -> {parsed['state']}", flush=True)
    print(f"done, new calls={n_done}", flush=True)
    return 0


# --------------------------------------------------------------------------------------
# 汇总
# --------------------------------------------------------------------------------------
def _ece(rows: list[tuple[float, bool]]) -> tuple[float | None, list[dict[str, Any]]]:
    bins = [(0.0, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.01)]
    table: list[dict[str, Any]] = []
    ece = 0.0
    n = len(rows)
    if not n:
        return None, []
    for lo, hi in bins:
        sel = [(c, ok) for c, ok in rows if lo <= c < hi]
        if not sel:
            table.append({"bin": f"[{lo},{hi})", "n": 0, "mean_conf": None, "empirical_acc": None})
            continue
        mc = sum(c for c, _ in sel) / len(sel)
        acc = sum(1 for _, ok in sel if ok) / len(sel)
        ece += len(sel) / n * abs(mc - acc)
        table.append({"bin": f"[{lo},{hi})", "n": len(sel), "mean_conf": round(mc, 4),
                      "empirical_acc": round(acc, 4)})
    return round(ece, 4), table


def _majority(p1: str, p2: str) -> str:
    if p1 == "catch" and p2 == "catch":
        return "catch"
    if p1 == "miss" and p2 == "miss":
        return "miss"
    if p1 in ("catch", "miss") and p2 in ("catch", "miss"):
        return p1  # 平票取 p1（协议 §5.4）
    return "unknown"


def _or_rule(p1: str, p2: str) -> str:
    """与 8 资产 OR **同构**的聚合：任一 prompt 报 catch ⇒ catch；全 unknown/fail ⇒ unknown；否则 miss。

    与预注册口径（``_majority``：不一致时取 p1）并排报告 —— 聚合口径本身就是一个可移动的读数。
    """
    if "catch" in (p1, p2):
        return "catch"
    if p1 == "miss" or p2 == "miss":
        return "miss"
    if p1 in ("contradiction",) or p2 in ("contradiction",):
        return "unknown"
    return "unknown"


def _gc(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    o: dict[str, int] = {}
    for x in rows:
        o[str(x[key])] = o.get(str(x[key]), 0) + 1
    return dict(sorted(o.items(), key=lambda kv: (-kv[1], kv[0])))


def analyze() -> int:
    sel = select_sample(build_pool())
    sel_by_uid = {r["uid"]: r for r in sel}
    raw = [json.loads(x) for x in RAW.read_text(encoding="utf-8").splitlines() if x.strip()] if RAW.exists() else []
    # 重试会产生同键多行：同一 (uid, slot, prompt, tag) 只保留**最后一条成功的**；无成功则留最后一条。
    best: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for r in raw:
        key = (str(r["uid"]), str(r["model_slot"]), str(r["prompt"]), str(r.get("run_tag", "default")))
        cur = best.get(key)
        if (cur is None
                or (str(cur.get("api_status")) != "ok" and str(r.get("api_status")) == "ok")
                or (str(cur.get("api_status")) == str(r.get("api_status")))):
            best[key] = r
    n_raw = len(raw)
    raw = list(best.values())

    out: dict[str, Any] = {
        "schema": "queyi-692/llm-audit/v1",
        "generated_by": "tools/run_692_llm_audit.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "protocol": "data/692_llm_audit_protocol.md",
        "design": {"seed": SEED, "n_per_stratum": N_PER_STRATUM, "n_selected": len(sel),
                   "selected_uids": [r["uid"] for r in sel],
                   "models": [{"slot": s, "model_id": m} for s, m in MODELS],
                   "prompts": list(PROMPTS), "temperature": 0, "max_tokens": MAX_TOKENS,
                   "max_lines": MAX_LINES, "calls_recorded": len(raw),
                   "raw_lines_including_retries": n_raw,
                   "dedup_rule": "同一 (uid, slot, prompt, tag) 只保留最后一条 API 成功的记录（重试产生多行）",
                   "api_base": "ZHIPU_BASE_URL（OpenAI 兼容；凭据不落盘）"},
        "positioning": "LLM 不是 oracle，是第 4 类 evidence asset；测 audit protocol 的模态可迁移性，不比较谁更准。",
        "per_model": {}, "cross_asset": {},
        "honest_limits": [
            "truth 参照 = 冻结矩阵 expected_verdict（声明可检出性标签）；人类 IAA 仍为 0。",
            "任务书原定 41 holdout + 64 corpus 框架不可执行（corpus 源路径已不在盘上，实测）⇒ 改用 A5 evaluation 538 有源池；偏差登记于协议 §6。",
            "两家族 = 推理型(glm-4.5) vs 非推理型(glm-4-flash)，不是两家公司（DeepSeek 密钥 401 已实测）。",
            "contradiction / confidence 为模型自报告，属操作性启发式（探索性），不可当证据强度。",
        ],
    }

    def _tag_of(rec: dict[str, Any]) -> str:
        return str(rec.get("run_tag", "default"))

    # 协议 §7 修订 A1：同一槽可能有多个补全预算轮次。主表口径（确定性，先写死）：
    # ① 优先取**跑满**的轮次（调用数 == 选中样本数 × prompt 数）；② 其中取**预算最大**者；
    # ③ 若没有跑满的轮次，取调用数最多者（并在产物里登记 incomplete=True，不假装完整）。
    tags_by_slot: dict[str, dict[str, int]] = {}
    calls_by_slot: dict[str, dict[str, int]] = {}
    for r in raw:
        s = str(r["model_slot"])
        t = _tag_of(r)
        d = tags_by_slot.setdefault(s, {})
        d[t] = max(d.get(t, 0), int(r.get("max_tokens") or MAX_TOKENS))
        calls_by_slot.setdefault(s, {})
        calls_by_slot[s][t] = calls_by_slot[s].get(t, 0) + 1
    expected_calls = len(sel) * len(PROMPTS)

    def _pick(slot: str) -> str:
        d = tags_by_slot.get(slot, {})
        if not d:
            return "default"
        # 覆盖度门槛 95% ⇒ 未过门槛的轮次不得当主表（避免用半轮数据冒充主口径）
        ok = [t for t in d if calls_by_slot.get(slot, {}).get(t, 0) >= 0.95 * expected_calls]
        pool = ok or [max(d, key=lambda t: (calls_by_slot.get(slot, {}).get(t, 0), d[t]))]
        return max(pool, key=lambda t: (d[t], t))

    primary_tag = {s: _pick(s) for s in tags_by_slot}
    out["design"]["run_tags"] = {
        s: {"primary": primary_tag.get(s), "max_tokens_by_tag": d,
            "calls_by_tag": calls_by_slot.get(s, {}), "expected_calls": expected_calls,
            "coverage_threshold": round(0.95 * expected_calls, 1),
            "primary_incomplete": calls_by_slot.get(s, {}).get(primary_tag.get(s, ""), 0) < 0.95 * expected_calls}
        for s, d in tags_by_slot.items()}

    for slot, model in MODELS:
        recs = [r for r in raw if r["model_slot"] == slot and _tag_of(r) == primary_tag.get(slot, "default")]
        states: dict[str, int] = {}
        for r in recs:
            st = str(r["verdict"]["state"])
            states[st] = states.get(st, 0) + 1
        per_uid: dict[str, dict[str, Any]] = {}
        for r in recs:
            per_uid.setdefault(r["uid"], {})[r["prompt"]] = r["verdict"]
        catch = miss = unknown = contr = 0
        unk_pos = unk_neg = 0
        fp = tn = 0
        ctrl_rep = ctrl_sil = ctrl_unk = 0
        pris_rep = pris_sil = pris_unk = 0
        inv_agree = inv_total = 0
        per_group: dict[str, dict[str, int]] = {}
        contradictions: list[dict[str, Any]] = []
        conf_rows: list[tuple[float, bool]] = []
        llm_map: dict[str, str] = {}
        for uid, pr in per_uid.items():
            tr = sel_by_uid.get(uid)
            if tr is None:
                continue
            s1 = str(pr.get("p1", {}).get("state", "unknown"))
            s2 = str(pr.get("p2", {}).get("state", "unknown"))
            inv_total += 1
            inv_agree += int(s1 == s2)
            v = _majority(s1, s2)
            llm_map[uid] = v
            g = str(tr["defect_group"])
            per_group.setdefault(g, {"catch": 0, "miss": 0, "unknown": 0, "contradiction": 0})
            if "contradiction" in (s1, s2):
                contr += 1
                per_group[g]["contradiction"] += 1
                contradictions.append({"uid": uid, "p1": s1, "p2": s2,
                                       "why": str(pr.get("p1", {}).get("why", ""))})
            if v == "unknown":
                unknown += 1
                per_group[g]["unknown"] += 1
                if not tr["planted"]:
                    ctrl_unk += 1
                    if tr["expected_verdict"] == "miss":
                        pris_unk += 1
                if tr["expected_verdict"] == "catch":
                    unk_pos += 1
                else:
                    unk_neg += 1
                continue
            if not tr["planted"]:
                if v == "catch":
                    ctrl_rep += 1
                    if tr["expected_verdict"] == "miss":
                        pris_rep += 1
                else:
                    ctrl_sil += 1
                    if tr["expected_verdict"] == "miss":
                        pris_sil += 1
            if tr["expected_verdict"] == "catch":
                if v == "catch":
                    catch += 1
                    per_group[g]["catch"] += 1
                else:
                    miss += 1
                    per_group[g]["miss"] += 1
            else:
                if v == "catch":
                    fp += 1
                else:
                    tn += 1
            cf = pr.get("p1", {}).get("confidence")
            if isinstance(cf, (int, float)):
                conf_rows.append((float(cf), v == tr["expected_verdict"]))
        denom = catch + miss
        ece, table = _ece(conf_rows)
        out["per_model"][slot] = {
            "model_id": model, "n_calls": len(recs), "state_counts_all_calls": states,
            "run_tag": primary_tag.get(slot, "default"),
            "max_tokens": tags_by_slot.get(slot, {}).get(primary_tag.get(slot, "default"), MAX_TOKENS),
            "caliber": "逐样本多数票（p1/p2 一致 ⇒ 该判定；不一致 ⇒ 取 p1；见协议 §5.4）",
            "three_components_on_declared_positives": {
                "catch": catch, "miss": miss, "unknown": unknown,
                "conditional_recall_pct": round(catch / denom * 100, 4) if denom else None},
            "false_report": {"on_expected_miss": fp, "silent_on_expected_miss": tn,
                             "unknown_on_expected_miss": unk_neg,
                             "false_report_rate_pct": round(fp / (fp + tn) * 100, 4) if (fp + tn) else None},
            "strata": {"declared_positives": catch + miss + unk_pos, "declared_negatives": fp + tn + unk_neg,
                       "unknown_on_positives": unk_pos, "unknown_on_negatives": unk_neg},
            "control_stratum_planted_false": {
                "n": ctrl_rep + ctrl_sil + ctrl_unk, "reported": ctrl_rep, "silent": ctrl_sil,
                "unknown": ctrl_unk,
                "report_rate_pct": round(ctrl_rep / (ctrl_rep + ctrl_sil) * 100, 4)
                if (ctrl_rep + ctrl_sil) else None},
            "pristine_negative_stratum": {
                "n": pris_rep + pris_sil + pris_unk, "reported": pris_rep, "silent": pris_sil,
                "unknown": pris_unk,
                "report_rate_pct": round(pris_rep / (pris_rep + pris_sil) * 100, 4)
                if (pris_rep + pris_sil) else None,
                "note": "planted=false 且 expected=miss：本批唯一能读作 FP 的干净对照层"},
            "prompt_invariance": {
                "agree": inv_agree, "total": inv_total,
                "rate_pct": round(inv_agree / inv_total * 100, 4) if inv_total else None,
                "disagreements": [{"uid": u, "p1": str(p.get("p1", {}).get("state", "")),
                                   "p2": str(p.get("p2", {}).get("state", ""))}
                                  for u, p in per_uid.items()
                                  if str(p.get("p1", {}).get("state")) != str(p.get("p2", {}).get("state"))]},
            "contradiction_n": contr, "contradiction_samples": contradictions,
            "calibration": {"ece": ece, "bins": table, "n_with_confidence": len(conf_rows)},
            "per_defect_group": {k: v for k, v in sorted(per_group.items())},
            "latency_s_mean": round(sum(float(r.get("latency_s") or 0) for r in recs) / len(recs), 3) if recs else None,
            "tokens_total": sum(int((r.get("usage") or {}).get("total_tokens") or 0) for r in recs),
            "api_failures": _gc([{"s": str(r["api_status"])} for r in recs], "s"),
        }
        out["cross_asset"][slot] = _cross_asset(sel_by_uid, llm_map)

    # ---- 协议 §7 修订 A1：补全预算敏感性（并排报告，不删任一轮）----
    sens: dict[str, Any] = {}
    for slot, _model in MODELS:
        for tag in sorted(tags_by_slot.get(slot, {})):
            rs = [r for r in raw if r["model_slot"] == slot and _tag_of(r) == tag]
            per_uid_t: dict[str, dict[str, Any]] = {}
            for r in rs:
                per_uid_t.setdefault(r["uid"], {})[r["prompt"]] = r["verdict"]
            c = m = u = 0
            fpx = tnx = 0
            for uid, pr in per_uid_t.items():
                tr = sel_by_uid.get(uid)
                if tr is None:
                    continue
                v = _majority(str(pr.get("p1", {}).get("state", "unknown")),
                              str(pr.get("p2", {}).get("state", "unknown")))
                if v == "unknown":
                    u += 1
                elif tr["expected_verdict"] == "catch":
                    c += 1 if v == "catch" else 0
                    m += 0 if v == "catch" else 1
                else:
                    fpx += 1 if v == "catch" else 0
                    tnx += 0 if v == "catch" else 1
            sens.setdefault(slot, {})[tag] = {
                "max_tokens": tags_by_slot.get(slot, {}).get(tag, MAX_TOKENS),
                "n_calls": len(rs),
                "conditional_recall_pct": round(c / (c + m) * 100, 4) if (c + m) else None,
                "false_report_rate_pct": round(fpx / (fpx + tnx) * 100, 4) if (fpx + tnx) else None,
                "unknown_n": u,
                "finish_reason_length_n": sum(1 for r in rs if str(r.get("finish_reason")) == "length"),
                "unknown_rate_pct": round(u / (c + m + u) * 100, 4) if (c + m + u) else None,
            }
    out["budget_sensitivity"] = sens
    # ---- 聚合口径敏感性：预注册（不一致取 p1） vs 资产一致 OR ----
    agg_sens: dict[str, Any] = {}
    for slot, _model in MODELS:
        recs = [r for r in raw if r["model_slot"] == slot and _tag_of(r) == primary_tag.get(slot, "default")]
        per_uid_a: dict[str, dict[str, Any]] = {}
        for r in recs:
            per_uid_a.setdefault(r["uid"], {})[r["prompt"]] = r["verdict"]
        for rule_name, fn in (("prereg_p1_tiebreak", _majority), ("asset_consistent_or", _or_rule)):
            c = m = u = 0
            fpx = tnx = 0
            for uid, pr in per_uid_a.items():
                tr = sel_by_uid.get(uid)
                if tr is None:
                    continue
                v = fn(str(pr.get("p1", {}).get("state", "unknown")),
                       str(pr.get("p2", {}).get("state", "unknown")))
                if v == "unknown":
                    u += 1
                elif tr["expected_verdict"] == "catch":
                    c += 1 if v == "catch" else 0
                    m += 0 if v == "catch" else 1
                else:
                    fpx += 1 if v == "catch" else 0
                    tnx += 0 if v == "catch" else 1
            agg_sens.setdefault(slot, {})[rule_name] = {
                "conditional_recall_pct": round(c / (c + m) * 100, 4) if (c + m) else None,
                "false_report_rate_pct": round(fpx / (fpx + tnx) * 100, 4) if (fpx + tnx) else None,
                "unknown_n": u, "n_judged": c + m + fpx + tnx,
            }
    out["aggregation_sensitivity"] = agg_sens
    out["aggregation_sensitivity_note"] = (
        "预注册口径 = 两 prompt 不一致时取 p1（协议 §5.4）；资产一致 OR = 任一 prompt 报 catch 即 catch，"
        "与 8 资产 OR 同构。两者并排报告：同一份测量在不同聚合口径下读数不同。OR 口径为事后补充，标探索性。"
    )
    out["budget_sensitivity_note"] = (
        "协议 §7 修订 A1：Model A 在 700 预算下出现 finish_reason=length 截断（推理 token 吃掉补全预算），"
        "故增跑 2000 预算一轮；两轮并排报告，主表用预算最大者。判据/样本/prompt 未变。"
    )

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for slot, _m in MODELS:
        pm = out["per_model"][slot]
        ca = out["cross_asset"][slot]
        print(f"{slot}: recall={pm['three_components_on_declared_positives']['conditional_recall_pct']} "
              f"fp_rate={pm['false_report']['false_report_rate_pct']} "
              f"inv={pm['prompt_invariance']['rate_pct']} ece={pm['calibration']['ece']} "
              f"unk={pm['three_components_on_declared_positives']['unknown']} agree_san={ca['agreement_pct']}")
    print("wrote", OUT)
    return 0


def _cross_asset(sel_by_uid: dict[str, dict[str, Any]], llm_map: dict[str, str]) -> dict[str, Any]:
    pairs = {"llm_catch_san_catch": 0, "llm_catch_san_no": 0, "llm_no_san_catch": 0, "llm_no_san_no": 0}
    llm_only: list[dict[str, Any]] = []
    san_only: list[dict[str, Any]] = []
    for uid, v in llm_map.items():
        tr = sel_by_uid.get(uid)
        if tr is None or v not in ("catch", "miss"):
            continue
        lc, sc = v == "catch", tr["san_or"] == "catch"
        pairs[f"llm_{'catch' if lc else 'no'}_san_{'catch' if sc else 'no'}"] += 1
        if lc and not sc:
            llm_only.append({"uid": uid, "group": tr["defect_group"], "expected": tr["expected_verdict"]})
        if sc and not lc:
            san_only.append({"uid": uid, "group": tr["defect_group"], "expected": tr["expected_verdict"]})
    n = sum(pairs.values())
    agree = pairs["llm_catch_san_catch"] + pairs["llm_no_san_no"]
    union = pairs["llm_catch_san_catch"] + pairs["llm_catch_san_no"] + pairs["llm_no_san_catch"]
    return {
        "sanitizer_ref": "冻结矩阵 asan/ubsan/tsan 的 OR（V_sanitizer）",
        "pairs": pairs, "n_judged": n,
        "agreement_pct": round(agree / n * 100, 4) if n else None,
        "jaccard_catch": round(pairs["llm_catch_san_catch"] / union, 4) if union else None,
        "llm_only_catch": {"n": len(llm_only), "by_group": _gc(llm_only, "group"),
                           "right_share_pct": round(sum(1 for x in llm_only if x["expected"] == "catch")
                                                    / len(llm_only) * 100, 4) if llm_only else None},
        "sanitizer_only_catch": {"n": len(san_only), "by_group": _gc(san_only, "group"),
                                 "right_share_pct": round(sum(1 for x in san_only if x["expected"] == "catch")
                                                          / len(san_only) * 100, 4) if san_only else None},
        "who_is_right_note": "以 expected_verdict（声明可检出性）为参照；分母为各自独有的分歧样本数。",
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--tag", default="default", help="轮次标签（协议 §7 修订 A1 用 a2000 区分预算）")
    ap.add_argument("--max-tokens", type=int, default=MAX_TOKENS)
    ap.add_argument("--slots", default="", help="逗号分隔的槽名，如 A_glm-4.5")
    ap.add_argument("--retry-failed", action="store_true", help="只重试 API 未成功的记录（限流恢复用）")
    ap.add_argument("--delay", type=float, default=0.0, help="两次调用之间的间隔秒数（礼貌限速）")
    a = ap.parse_args(argv)
    if a.analyze:
        return analyze()
    slots = tuple(x.strip() for x in a.slots.split(",") if x.strip())
    rc = do_run(a.limit, tag=a.tag, max_tokens=a.max_tokens, only_slots=slots,
                retry_failed=a.retry_failed, delay=a.delay)
    if rc != 0:
        return rc
    return analyze()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
