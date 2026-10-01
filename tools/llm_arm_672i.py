#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""llm_arm_672i.py — 672i W4：LLM 裁判臂（第三方裁判 vs FD vs 真值）。

协议（预注册 `data/experiments/prereg_672i.json`，先于任何调用落盘）
====================================================================
* 抽样：真错 12（6 catch + 6 miss，id 升序）+ 对照 8（id 升序）＝ 20 条，**非随机**可复算；
* prompt v1：只给**剥掉注释**的源码（夹具头注释会直接写答案），不给 detector / planted /
  sanitizer 输出 / 文件名；要 JSON 输出；
* 模型：GLM-4（GPT-4/Claude 无 key、DeepSeek key 401 —— 已实测并登记）；temperature 0.01；
* 缓存：逐条落 `data/experiments/llm_arm_672i_raw.jsonl`（命中不重复计费）；
* 失败：重试 1 次仍失败 ⇒ 该样本 unknown（列出原因，不进分分母）。

产物：`data/experiments/llm_arm_672i.json`（+ raw jsonl）

用法
====
    python tools/llm_arm_672i.py --run        # 真调 API（需 .env 的 ZHIPU_API_KEY）
    python tools/llm_arm_672i.py --mock       # 离线确定性假裁判（只给单测/无网场景）
    python tools/llm_arm_672i.py --selftest   # 自检（不联网）
    python tools/llm_arm_672i.py --json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"
HOLDOUT = ROOT / "data" / "holdout" / "holdout.json"
RAW = ROOT / "data" / "experiments" / "llm_arm_672i_raw.jsonl"
OUT = ROOT / "data" / "experiments" / "llm_arm_672i.json"
ENV = ROOT / ".env"

N_ERROR_CATCH = 6
N_ERROR_MISS = 6
N_CONTROL = 8
PROMPT_VERSION = "v1"
MODEL = "glm-4"
TEMP = 0.01

PROMPT_TMPL = """You are a C++ code reviewer. Decide whether the code below contains a defect
that would cause undefined behavior, a memory error, a concurrency error,
or a clear API misuse. Do not assume any build flags or tools are available.

Answer ONLY with a single JSON object, no prose:
{{"has_defect": true|false, "category": "...", "confidence": 0.0-1.0, "reason": "..."}}

```cpp
{code}
```
"""


def _load_env() -> dict[str, str]:
    """读 .env（键值；不落盘、不打印值）。"""
    out: dict[str, str] = {}
    if ENV.is_file():
        for ln in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$", ln)
            if m:
                out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


# ── 抽样（预注册口径：可复算、非随机）────────────────────────────────────────

def select_samples() -> list[dict]:
    det = jload(DETAIL)["per_sample"]
    labels = {s["id"]: s for s in jload(HOLDOUT)["seeds"]}
    err = [r for r in det if labels.get(r["id"], {}).get("planted") is True
           and r["verdict"] in ("catch", "miss")]
    ctrl = [r for r in det if labels.get(r["id"], {}).get("planted") is False]
    err.sort(key=lambda r: r["id"])
    ctrl.sort(key=lambda r: r["id"])
    pick = ([r for r in err if r["verdict"] == "catch"][:N_ERROR_CATCH]
            + [r for r in err if r["verdict"] == "miss"][:N_ERROR_MISS]
            + ctrl[:N_CONTROL])
    out = []
    for r in pick:
        s = labels[r["id"]]
        out.append({
            "id": r["id"], "verdict_fd": r["verdict"], "detector": r["detector"],
            "layer": r.get("layer"), "planted": s.get("planted"),
            "src": str(s.get("atom_ref")),
        })
    out.sort(key=lambda x: x["id"])
    return out


def strip_comments(code: str) -> str:
    """剥离 // 与 /* */ 注释（保留字符串字面量里的内容）。"""
    out, i, n = [], 0, len(code)
    in_s = in_c = None
    while i < n:
        ch = code[i]
        nxt = code[i + 1] if i + 1 < n else ""
        if in_s:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(nxt)
                i += 2
                continue
            if ch == in_s:
                in_s = None
            i += 1
            continue
        if in_c == "block":
            if ch == "*" and nxt == "/":
                in_c = None
                i += 2
                continue
            i += 1
            continue
        if ch in "\"'":
            in_s = ch
            out.append(ch)
            i += 1
            continue
        if ch == "/" and nxt == "/":
            while i < n and code[i] != "\n":
                i += 1
            continue
        if ch == "/" and nxt == "*":
            in_c = "block"
            i += 2
            continue
        out.append(ch)
        i += 1
    txt = "".join(out)
    # 折叠空行（保持可读、省 token）
    return re.sub(r"\n{3,}", "\n\n", "\n".join(ln.rstrip() for ln in txt.splitlines())).strip()


# ── 调用与解析 ───────────────────────────────────────────────────────────────

def call_glm(prompt: str, env: dict[str, str], timeout: int = 90) -> dict:
    key = env.get("ZHIPU_API_KEY", "")
    base = env.get("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4").rstrip("/")
    body = {"model": MODEL, "temperature": TEMP, "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(base + "/chat/completions",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + key}, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode("utf-8"))
    return {"text": d["choices"][0]["message"]["content"], "usage": d.get("usage") or {},
            "latency_s": round(time.time() - t0, 2)}


def mock_judge(code: str, sid: str) -> dict:
    """离线确定性假裁判（**只用于单测/无网**）：按内容关键词给判决，不冒充真模型。"""
    h = hashlib.sha256((sid + code).encode("utf-8")).hexdigest()[:8]
    risky = any(k in code for k in ("delete", "free(", "new ", "thread", "malloc",
                                    "reinterpret_cast", "strcpy", "memcpy", "printf("))
    return {"text": json.dumps({"has_defect": bool(risky), "category": "mock",
                                "confidence": 0.5, "reason": f"mock judge {h}"}),
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "latency_s": 0.0, "mock": True}


def parse_verdict(text: str) -> dict | None:
    """从模型输出里抽 JSON（容忍围栏/前后缀）。"""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:  # noqa: BLE001
        return None
    if not isinstance(d, dict) or "has_defect" not in d:
        return None
    d["has_defect"] = bool(d["has_defect"])
    return d


def load_cache() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if RAW.is_file():
        for ln in RAW.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln)
                out[r["id"]] = r
    return out


def append_raw(rows: list[dict]) -> None:
    RAW.parent.mkdir(parents=True, exist_ok=True)
    with RAW.open("a", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


# ── 主流程 ───────────────────────────────────────────────────────────────────

def run(use_mock: bool, write: bool = True) -> dict:
    env = _load_env()
    cache = load_cache()
    samples = select_samples()
    new_rows: list[dict] = []
    per_sample: list[dict] = []
    for s in samples:
        src = ROOT / s["src"]
        code = strip_comments(src.read_text(encoding="utf-8", errors="replace"))
        leaked = bool(re.search(r"leak|double_free|race|oob|use_after|bug", s["src"], re.I))
        cached = cache.get(s["id"])
        if cached and cached.get("prompt_version") == PROMPT_VERSION \
                and cached.get("model") == ("mock" if use_mock else MODEL):
            got, note = cached["raw"], "cache"
        else:
            prompt = PROMPT_TMPL.format(code=code)
            try:
                resp = (mock_judge(code, s["id"]) if use_mock else call_glm(prompt, env))
                got = resp["text"]
                row = {"id": s["id"], "model": "mock" if use_mock else MODEL,
                       "prompt_version": PROMPT_VERSION, "raw": got,
                       "usage": resp.get("usage") or {},
                       "latency_s": resp.get("latency_s"),
                       "at": _dt.datetime.now().isoformat(timespec="seconds"),
                       "mock": bool(resp.get("mock"))}
                new_rows.append(row)
                note = "mock" if use_mock else "api"
            except Exception as e:  # noqa: BLE001
                time.sleep(1.0)
                try:
                    resp = mock_judge(code, s["id"]) if use_mock else call_glm(prompt, env)
                    got = resp["text"]
                    new_rows.append({"id": s["id"], "model": "mock" if use_mock else MODEL,
                                     "prompt_version": PROMPT_VERSION, "raw": got,
                                     "usage": resp.get("usage") or {},
                                     "latency_s": resp.get("latency_s"),
                                     "at": _dt.datetime.now().isoformat(timespec="seconds"),
                                     "retry": True, "mock": bool(resp.get("mock"))})
                    note = "retry"
                except Exception as e2:  # noqa: BLE001
                    got, note = "", f"api_error: {type(e2).__name__}: {str(e2)[:80]}"
        v = parse_verdict(got) if got else None
        per_sample.append({
            "id": s["id"], "fd": s["verdict_fd"], "llm": (v or {}).get("has_defect"),
            "llm_category": (v or {}).get("category"), "llm_confidence": (v or {}).get("confidence"),
            "truth": "error" if s["planted"] is True else "control",
            "detector": s["detector"], "layer": s["layer"], "note": note,
            "answer_leak_risk": leaked,
        })
    if new_rows and write:
        append_raw(new_rows)

    # ── 统计 ──
    err = [r for r in per_sample if r["truth"] == "error" and r["llm"] is not None]
    err_unknown = [r for r in per_sample if r["truth"] == "error" and r["llm"] is None]
    ctrl = [r for r in per_sample if r["truth"] == "control" and r["llm"] is not None]
    llm_k = sum(1 for r in err if r["llm"] is True)
    fd_k = sum(1 for r in err if r["fd"] == "catch")
    llm_fp = sum(1 for r in ctrl if r["llm"] is True)

    # 配对（FD vs LLM）：只在真错且两者都有判决的样本上
    b = sum(1 for r in err if r["fd"] == "catch" and r["llm"] is False)   # FD 独有
    c = sum(1 for r in err if r["fd"] == "miss" and r["llm"] is True)     # LLM 独有
    import ablation_stats_671b as A
    mcn = A.mcnemar_exact(b, c)
    agree = sum(1 for r in per_sample if r["llm"] is not None
                and ((r["fd"] == "catch") == r["llm"]))
    n_pair = sum(1 for r in per_sample if r["llm"] is not None)

    def rate(k: int, n: int) -> float | None:
        return round(k / n * 100, 1) if n else None

    def by_layer(kinds: set[str]) -> dict:
        sub = [r for r in err if r["detector"] in kinds]
        return {"n": len(sub), "llm_catch": sum(1 for r in sub if r["llm"] is True),
                "fd_catch": sum(1 for r in sub if r["fd"] == "catch"),
                "llm_rate_pct": rate(sum(1 for r in sub if r["llm"] is True), len(sub)),
                "fd_rate_pct": rate(sum(1 for r in sub if r["fd"] == "catch"), len(sub))}

    runtime = by_layer({"asan", "ubsan", "tsan"})
    static = by_layer({"compiler-warn", "cross-compile", "wunsequenced", "linker"})
    h4_delta = (None if (runtime["llm_rate_pct"] is None or static["llm_rate_pct"] is None)
                else round(runtime["llm_rate_pct"] - static["llm_rate_pct"], 1))

    usage: dict[str, int] = {}
    for r in new_rows:
        for k, v in (r.get("usage") or {}).items():
            usage[str(k)] = usage.get(str(k), 0) + int(v or 0)

    rep = {
        "schema": "queyi-llm-arm/672i",
        "generated_by": "tools/llm_arm_672i.py（W4 第三方裁判臂）",
        "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prereg": "data/experiments/prereg_672i.json",
        "mode": "mock（离线假裁判，仅供单测/无网）" if use_mock else "live_api",
        "model": {"name": "mock" if use_mock else MODEL, "temperature": TEMP,
                  "prompt_version": PROMPT_VERSION,
                  "availability_note": "GPT-4/Claude 无 key；DeepSeek key 401；GLM-4 实测可用 ⇒ 本臂用 GLM-4，"
                                       "结论只声称该模型在该 prompt 下的表现"},
        "sampling": {"n_error": len(err) + len(err_unknown), "n_control": len(ctrl),
                     "rule": "6 catch + 6 miss + 8 control（id 升序，非随机）",
                     "detail": "data/holdout/reveal_5_detail_672h.json"},
        "metrics": {
            "llm_detect_rate_pct": rate(llm_k, len(err)), "llm_k": llm_k, "llm_n": len(err),
            "fd_detect_rate_pct": rate(fd_k, len(err)), "fd_k": fd_k,
            "delta_fd_minus_llm_pp": (round((fd_k - llm_k) / len(err) * 100, 1) if err else None),
            "llm_false_positive": {"fp": llm_fp, "n": len(ctrl), "rate_pct": rate(llm_fp, len(ctrl))},
            "agreement": {"agree": agree, "n": n_pair, "rate": (round(agree / n_pair, 3)
                                                                if n_pair else None)},
            "paired_mcnemar_fd_vs_llm": {"b_fd_only": b, "c_llm_only": c,
                                         "p_value": mcn["p_value"], "method": mcn["method"]},
            "by_layer": {"runtime_sanitizer": runtime, "static_compiler": static,
                         "h4_layer_delta_pp": h4_delta},
        },
        "hypothesis_verdicts": {
            "H1_fd_minus_llm_gt_20pp": ("成立" if (fd_k - llm_k) / max(len(err), 1) > 0.20
                                        and mcn["p_value"] < 0.05 else "不成立"),
            "H2_llm_fp_lt_25pct": ("成立" if (len(ctrl) and llm_fp / len(ctrl) < 0.25)
                                   else "不成立"),
            "H3_agreement_ge_0.6": ("成立" if (n_pair and agree / n_pair >= 0.6) else "不成立"),
            "H4_layer_delta_gt_20pp": ("未判定" if h4_delta is None else
                                       ("成立" if abs(h4_delta) > 20 else "不成立（探索性）")),
        },
        "per_sample": per_sample,
        "unknown_samples": [{"id": r["id"], "note": r["note"]} for r in per_sample
                            if r["llm"] is None],
        "usage_total": usage,
        "answer_leak_risk_samples": [r["id"] for r in per_sample if r["answer_leak_risk"]],
        "honest_note": "LLM 只看**剥注释**的源码，无编译/无 sanitizer 证据；"
                       "本臂是第三方对照读法，不得与 FD 混成同一类证据。",
        "raw_log": str(RAW.relative_to(ROOT).as_posix()),
    }
    if write and not use_mock:
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
    return rep


def render(rep: dict) -> str:
    m = rep["metrics"]
    lines = [f"[llm-arm-672i] mode={rep['mode']} model={rep['model']['name']}",
             f"  LLM 检出 {m['llm_k']}/{m['llm_n']} = {m['llm_detect_rate_pct']}%"
             f"  | FD 同子集 {m['fd_k']}/{m['llm_n']} = {m['fd_detect_rate_pct']}%"
             f"  | Δ={m['delta_fd_minus_llm_pp']}pp",
             f"  LLM 假阳性 {m['llm_false_positive']['fp']}/{m['llm_false_positive']['n']}"
             f" = {m['llm_false_positive']['rate_pct']}%",
             f"  一致率 {m['agreement']['agree']}/{m['agreement']['n']}"
             f" = {m['agreement']['rate']}  | McNemar b={m['paired_mcnemar_fd_vs_llm']['b_fd_only']}"
             f" c={m['paired_mcnemar_fd_vs_llm']['c_llm_only']}"
             f" p={m['paired_mcnemar_fd_vs_llm']['p_value']:.3g}",
             f"  分层：runtime LLM {m['by_layer']['runtime_sanitizer']['llm_rate_pct']}%"
             f" vs static LLM {m['by_layer']['static_compiler']['llm_rate_pct']}%"
             f"  Δ={m['by_layer']['h4_layer_delta_pp']}pp",
             "  假设判定：" + json.dumps(rep["hypothesis_verdicts"], ensure_ascii=False)]
    if rep["unknown_samples"]:
        lines.append(f"  unknown：{rep['unknown_samples']}")
    if rep["usage_total"]:
        lines.append(f"  token 合计：{rep['usage_total']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672i W4：LLM 裁判臂")
    ap.add_argument("--run", action="store_true", help="真调 API")
    ap.add_argument("--mock", action="store_true", help="离线假裁判（单测用）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.run or a.mock):
        ap.print_help()
        return 2
    rep = run(use_mock=a.mock, write=True)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else render(rep))
    return 0


def selftest() -> int:
    ok = 0
    # 抽样口径
    s = select_samples()
    assert len(s) == 20, len(s)
    assert sum(1 for x in s if x["planted"] is True) == 12
    assert sum(1 for x in s if x["planted"] is False) == 8
    assert sum(1 for x in s if x["planted"] is True and x["verdict_fd"] == "catch") == 6
    assert sum(1 for x in s if x["planted"] is True and x["verdict_fd"] == "miss") == 6
    ids = [x["id"] for x in s]
    assert ids == sorted(ids), "样本顺序必须是 id 升序（可复算）"
    ok += 5
    # 注释剥离：行注释、块注释、字符串内的 // 保留
    code = '// 答案：故意双重释放（ASan 取证）\nint x = 1; /* blk */\nconst char* u = "http://a";\n'
    out = strip_comments(code)
    assert "答案" not in out and "blk" not in out
    assert '"http://a"' in out and "int x = 1;" in out
    ok += 2
    # JSON 解析：围栏与前后缀
    v = parse_verdict('```json\n{"has_defect": true, "category": "UB", "confidence": 0.9}\n```')
    assert v and v["has_defect"] is True and v["category"] == "UB"
    assert parse_verdict("no json here") is None
    assert parse_verdict('{"category": "x"}') is None      # 缺 has_defect 字段
    ok += 3
    # 假裁判确定性（同输入同输出）
    assert mock_judge("int main(){}", "h1") == mock_judge("int main(){}", "h1")
    ok += 1
    # 真跑路径的产物口径（读已落盘产物）
    if OUT.is_file():
        rep = jload(OUT)
        m = rep["metrics"]
        assert rep["schema"] == "queyi-llm-arm/672i"
        assert m["llm_n"] + len(rep["unknown_samples"]) == 12
        assert m["llm_false_positive"]["n"] <= 8
        assert 0 <= m["agreement"]["rate"] <= 1
        assert rep["per_sample"] and all("fd" in r and "llm" in r for r in rep["per_sample"])
        ok += 5
    print(f"[llm-arm-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
