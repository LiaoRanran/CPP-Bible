"""629 D2 · 第八轮攻击（沙箱实跑，复用 622 的 apply API 与 6 重护栏）

对 D1 选出的 Top20 种子，用 `tools/sandbox_apply_622.py` 的沙箱逐条实跑 gate 判决：
- 施加前**字节级备份**（内存 + `.622bak`）· `finally` 必还原 · 还原后 sha256 校验
- 并发锁 `data/.622_apply.lock` · gate 子进程 30s 超时 · 路径白名单仅 `atoms/`、`evidence/`

**只读契约**：`--run` 会临时改动受控目录（由沙箱保证还原）；`--check` **只读已保存的结果**
（不跑沙箱、不碰受控目录）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

SEEDS_JSON = os.path.join(ROOT, "data", "attack_objective_629.json")
OUT_JSON = os.path.join(ROOT, "data", "attack_round8_629.json")
OUT_MD = os.path.join(ROOT, "data", "attack_round8_629.md")
RULES_TOTAL = 67
TOUCHED_BASELINE = 36          # §一：623-624 沙箱累计触达 36/67
VFDR_BASELINE = "622 26% → 623 77.5%/65%（双轴逃逸口径）"


def seeds() -> list[dict[str, Any]]:
    d = json.load(open(SEEDS_JSON, encoding="utf-8"))
    return list(d.get("seeds") or [])


def build_mutations(sd: Optional[list[dict[str, Any]]] = None) -> list[dict[str, Any]]:
    """把 D1 种子翻译成沙箱契约（`content` 为 JSON 字符串）。"""
    out = []
    for i, s in enumerate(sd or seeds(), 1):
        content = {"op": s["op"], "target_card": s["card"],
                   "target_rule": s.get("target_rule") or "",
                   "point": s.get("point"), "seed_score": s.get("score")}
        out.append({"mutation_id": f"MUT-629-R8-{i:02d}",
                    "attack_type": "round8_objective",
                    "target_rule": content["target_rule"],
                    "content": json.dumps(content, ensure_ascii=False)})
    return out


def repo_dirty_controlled() -> str:
    p = subprocess.run(["git", "status", "--porcelain", "--", "atoms", "evidence",
                        "Examples", "Book"],
                       capture_output=True, text=True, cwd=ROOT, check=False)
    return (p.stdout or "").strip()


def run_round() -> dict[str, Any]:
    import sandbox_apply_622 as SB

    muts = build_mutations()
    res = SB.run_batch(muts, log=lambda *_a: None)
    touched = sorted({r for row in res["rows"]
                      for r in [*(row.get("new_block_rules") or []),
                                *(row.get("new_nonblock_rules") or [])]})
    out = {"batch": "629", "round": 8,
           "seeds_source": os.path.relpath(SEEDS_JSON, ROOT).replace(os.sep, "/"),
           "mutations": len(muts),
           "distribution": res["distribution"],
           "escaped": [r for r in res["escaped"]],
           "touched_this_round": touched,
           "touched_count": len(touched),
           "touched_baseline": TOUCHED_BASELINE,
           "elapsed_s": res["elapsed_s"],
           "rows": res["rows"],
           "repo_dirty_after": repo_dirty_controlled(),
           "vfdr_baseline": VFDR_BASELINE, "rules_total": RULES_TOTAL}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    return out


def load_saved() -> dict[str, Any]:
    return json.load(open(OUT_JSON, encoding="utf-8")) if os.path.exists(OUT_JSON) else {}


def write_report(d: Optional[dict[str, Any]] = None) -> str:
    d = d or load_saved()
    rows = d.get("rows") or []
    dist = d.get("distribution") or {}
    blocked = [r for r in rows if r["verdict"] == "blocked"]
    nonblock = [r for r in rows if r["verdict"] == "detected_nonblock"]
    neutral = [r for r in rows if r["verdict"] == "neutral"]
    infra = [r for r in rows if r["verdict"] == "infra_error"]
    dirty_txt = ("**空 ✅**" if not d.get("repo_dirty_after")
                 else f"**非空 ❌**：{d.get('repo_dirty_after')}")
    lines = [
        "# 629 D2 · 第八轮攻击（沙箱实跑 Top20 种子）", "",
        "> 工具：`tools/attack_round8_629.py`（复用 `sandbox_apply_622` 的 6 重护栏）",
        f"> 种子来源：`{d.get('seeds_source')}`（D1 目标函数 Top20）· "
        f"耗时 **{d.get('elapsed_s')}s**", "",
        "## 一、判决分布", "",
        "| 判决 | 条数 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(dist.items())],
        f"| **合计** | **{d.get('mutations')}** |", "",
        f"- **escaped（逃逸）：{len(d.get('escaped') or [])}**"
        f"{'（目标 0 ✅）' if not d.get('escaped') else '（⚠️ 需人工复核）'}",
        f"- blocked {len(blocked)} · detected_nonblock {len(nonblock)} · "
        f"neutral {len(neutral)} · infra_error {len(infra)}", "",
        "## 二、触达规则", "",
        f"- 本轮触发规则（去重）：**{d.get('touched_count')}** 条，清单：",
        "  " + "、".join(f"`{r}`" for r in (d.get("touched_this_round") or [])) or "（无）",
        f"- 历史累计触达基线（§一，623-624 六轮）：**{TOUCHED_BASELINE}/{RULES_TOTAL}**",
        "- 本轮相对基线的**新增触达**：见 §四 诚实登记（跨批口径不可直接相减）。", "",
        "## 三、受控目录零污染核验", "",
        f"- 跑批后 `git status -- atoms evidence Examples Book`：{dirty_txt}",
        "- 6 重护栏在位：字节级备份 / `finally` 必还原 / 还原后 sha256 校验 / 并发锁 / "
        "gate 30s 超时 / 路径白名单（`atoms/`、`evidence/`）。", "",
        "## 四、诚实登记（未达目标项）", "",
        f"1. **触达目标未达成**：本轮 20 条种子只触发 {d.get('touched_count')} 条规则"
        f"（{'、'.join('`' + r + '`' for r in (d.get('touched_this_round') or [])) or '无'}），"
        "且是**已有规则**（EV-FM-REQUIRED 早已在 623-624 触达集合里）⇒ "
        "**对 36/67 的盲区没有任何新增覆盖**。任务书目标「新增触达 >36/67」**未达成**。",
        f"2. **{len(neutral)}/{d.get('mutations')} 条种子完全无反应（neutral）**："
        "这些样本施加后 gate **零新增检出**。两种可能（本工具无法区分，如实登记）：",
        "   - (a) 种子**翻译失真**：v7 记录**无 `target_rule` 字段**，本工具从 "
        "`new_block/new_warn` 反推；而沙箱 `plan_edit` 的 M1/M6 要按 `target_rule` 查 "
        "`RULE_FIELD` 决定「删哪个字段」⇒ 反推出的规则可能**不是原变异点删的字段**，"
        "于是「删了一个不影响判决的字段」⇒ neutral。**这是本轮最主要的方法学缺陷。**",
        "   - (b) 该样本在当前 67 规则集下确实不再触发（规则口径变化）。",
        "3. **D1 目标函数的副作用**：`disagreement` 代理奖励「触发规则数」，"
        "而 v7 里触发规则多的样本**本来就是被拦住的**（blocked）⇒ 乘积式排序把"
        "「已知会被拦」的样本排到前面，对**发现新盲区**帮助有限。"
        "下一轮若要以「扩大触达」为目标，`disagreement` 应改为"
        "「两个独立验证器的判决分歧」而不是「规则触发数」。",
        f"2. **VFDR 未重算**：任务书要求记录 VFDR 变化。VFDR 需 624 的 `vfdr_updater_v2_624.py` "
        f"重算并**改写 data/ 基线文件**（§零 禁改基线）⇒ 本批只登记参照值（{d.get('vfdr_baseline')}），"
        "重算留监工/下一批。",
        "3. `touched_this_round` 是**本轮 20 条的并集**，与 §一 的 36/67 跨批口径不同"
        "（不同种子集、不同批次），**不可直接相减**——故不报「新增 X 条」。", "",
        "## 五、局限", "",
        "- 20 条种子只覆盖 evidence 类卡的 M1/M7 两个算子族（D1 排序的必然结果），"
        "**不代表整个攻击面**；",
        "- 沙箱只判「单卡编辑后 gate 是否多报一条」，不判「内容是否真的错了」；",
        "- gate 判决依赖当前规则集（67 条）；规则集变化后本轮数据即过期。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    d = load_saved()
    chk("结果 JSON 已保存（--run 已跑过）", bool(d))
    chk("20 条 mutation 全部有判决",
        len(d.get("rows") or []) == 20
        and all(r.get("verdict") for r in d.get("rows") or []),
        f"({len(d.get('rows') or [])})")
    chk("判决分布合计 = 20", sum((d.get("distribution") or {}).values()) == 20)
    chk("零逃逸（目标 0）", not d.get("escaped"),
        f"({d.get('escaped')})")
    chk("先 build_mutations 覆盖 20 条且契约完整",
        len(build_mutations()) == 20
        and all(json.loads(m["content"]).get("target_card") for m in build_mutations()))
    chk("受控目录跑批后零污染", not repo_dirty_controlled(), f"({repo_dirty_controlled()})")
    chk("无残留并发锁", not os.path.exists(os.path.join(ROOT, "data", ".622_apply.lock")))
    chk("报告存在且含判决分布与诚实登记", os.path.exists(OUT_MD)
        and "判决分布" in open(OUT_MD, encoding="utf-8").read()
        and "诚实登记" in open(OUT_MD, encoding="utf-8").read())
    print(f"D2 attack round8 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 D2 第八轮攻击（沙箱实跑）")
    ap.add_argument("--check", action="store_true", help="只读自检（不跑沙箱）")
    ap.add_argument("--run", action="store_true", help="实跑 Top20（沙箱，含还原）")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.run:
        d = run_round()
        print(json.dumps({k: v for k, v in d.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    d = load_saved()
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(f"mutations={d.get('mutations')} dist={d.get('distribution')} "
          f"escaped={len(d.get('escaped') or [])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
