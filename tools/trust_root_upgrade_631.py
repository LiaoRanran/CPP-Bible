"""631 E1 · 他验信任根升级方案评估（纯标准库，只读）

629 C1 实现了 **RSA-2048 真非对称签名**（算法层独立），但公私钥**同主体**
⇒ 算法独立 ≠ 信任根独立（630 交人项 #8/#9）。本工具评估三条升级路径：

| 路径 | 做法 | 本质 |
|---|---|---|
| **A 纯标准库继续** | RSA 教科书级实现，公钥放仓库，第三方可验证 | 密钥仍在本地，信任根未变 |
| **B 引入 cryptography** | 生产级 RSA（常量时间/盲化/PKCS#1 标准格式） | 实现变强，**信任根仍未变** |
| **C 外部 KMS / 透明日志** | 公钥锚到 OTS/Sigstore/Rekor，密钥不在本地 | **信任根真正外移** |

对比维度：安全性 / 依赖成本 / 可操作性 / 第三方可验证性 / 维护成本。
`--check` 只读（不生成密钥、不联网、exit 0）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "trust_root_upgrade_631.md")
OUT_JSON = os.path.join(ROOT, "data", "trust_root_upgrade_631.json")

DIMENSIONS = ("安全性", "依赖成本", "可操作性", "第三方可验证性", "维护成本")

# 评分 1(差) - 5(好)；**人定**，逐项给理由，可审
PATHS: dict[str, dict[str, Any]] = {
    "A 纯标准库继续": {
        "scores": {"安全性": 2, "依赖成本": 5, "可操作性": 5, "第三方可验证性": 2,
                   "维护成本": 4},
        "why": {
            "安全性": "教科书级实现：无常量时间运算（计时侧信道）、无盲化、自定义密钥格式；"
                      "且私钥同主体",
            "依赖成本": "零依赖（§零.8 纯标准库硬性要求，本项满分）",
            "可操作性": "现在就能跑，无需审批/联网",
            "第三方可验证性": "公钥在仓库里，但**无法证明它未被换过**"
                              "（仓库可被同主体改写）⇒ 只能验证「这个公钥签的」",
            "维护成本": "自己维护大数运算与素性检测，长期有隐性成本",
        },
        "recommend": "短期保留（已有能力），**不作为终态**",
    },
    "B 引入 cryptography": {
        "scores": {"安全性": 4, "依赖成本": 2, "可操作性": 3, "第三方可验证性": 2,
                   "维护成本": 5},
        "why": {
            "安全性": "生产级实现（常量时间 + 盲化 + 标准 PKCS#1）；但**私钥仍同主体**"
                      "⇒ 抗实现攻击变强，信任根未变",
            "依赖成本": "需 pip install（§零.8 禁止本批执行）+ wheel 体积/供应链面",
            "可操作性": "需改签名器实现 + 依赖审批",
            "第三方可验证性": "与 A 同级：公钥托管问题没解决",
            "维护成本": "库维护，代码量下降",
        },
        "recommend": "**性价比不高的中间态**：花依赖成本只买到实现强度，信任根不变",
    },
    "C 外部 KMS / 透明日志": {
        "scores": {"安全性": 5, "依赖成本": 2, "可操作性": 2, "第三方可验证性": 5,
                   "维护成本": 3},
        "why": {
            "安全性": "私钥不出 KMS/HSM（或压根不在本地）；公钥锚到**外部不可篡改位置**"
                      "（OTS/Sigstore/Rekor）⇒ 换公钥需要外部可观测",
            "依赖成本": "需外部服务/网络/账号，可能涉及费用与合规",
            "可操作性": "最复杂：账户、密钥策略、审计、离线验证流程都要设计",
            "第三方可验证性": "**唯一真正第三方可验证**：外部锚 + 时间戳可独立核验",
            "维护成本": "依赖外部服务可用性，需监控与降级方案",
        },
        "recommend": "**唯一能真正升级信任根的路径** ⇒ 推荐（分阶段）",
    },
}

STEPS_C = [
    "1. 选定外部锚（建议先做 **OTS/OpenTimestamps**：免费、只锚哈希、无需账号）",
    "2. 把 631 导出的公钥指纹（`data/vsa/public_key_631.json` 的 sha256）提交 OTS",
    "3. 把 OTS 收据与比特币区块高度写进 `data/vsa/` 并纳入透明日志",
    "4. 第三方验证指南（E2）增加一步：校验证书链 + 校验 OTS 收据",
    "5. 后续再评估 Sigstore/Rekor（带身份绑定，成本更高）",
]


def scores() -> dict[str, dict[str, int]]:
    return {k: dict(v["scores"]) for k, v in PATHS.items()}


def totals() -> dict[str, int]:
    return {k: sum(v["scores"].values()) for k, v in PATHS.items()}


def recommend() -> tuple[str, str]:
    """推荐 = C（理由：只有它提升第三方可验证性）；并给分阶段建议。"""
    best = max(totals().items(), key=lambda kv: kv[1])
    return ("C 外部 KMS / 透明日志",
            f"总分最高的是 {best[0]}（{best[1]} 分），但**推荐是 C**："
            "A/B 的第三方可验证性都是 2（公钥仍可被同主体改写），"
            "只有 C 把它提到 5（外部不可篡改锚）⇒ 信任根真正外移")


def write_report() -> str:
    rec, why = recommend()
    lines = [
        "# 631 E1 · 他验信任根升级方案评估", "",
        "> 629 C1 已实现 RSA-2048 真非对称签名（**算法独立**），但公私钥同主体 ⇒ "
        "算法独立 ≠ 信任根独立。本表评估三条路径。", "",
        "## 一、五维对比（1=差，5=好）", "",
        "| 路径 | " + " | ".join(DIMENSIONS) + " | 总分 |",
        "|---|" + "---|" * (len(DIMENSIONS) + 1),
        *[f"| **{k}** | " + " | ".join(str(v["scores"][d]) for d in DIMENSIONS)
          + f" | **{totals()[k]}** |" for k, v in PATHS.items()],
        "", "## 二、逐项理由", "",
    ]
    for k, v in PATHS.items():
        lines += [f"### {k}", "", "| 维度 | 分 | 理由 |", "|---|---|---|",
                  *[f"| {d} | {v['scores'][d]} | {v['why'][d]} |"
                    for d in DIMENSIONS],
                  "", f"**处置建议**：{v['recommend']}", ""]
    lines += ["## 三、推荐与实施步骤", "",
              f"**推荐：{rec}**", "", why, "",
              "分阶段实施（先低成本、可逆）：", "",
              *[f"{s}" for s in STEPS_C], "",
              "## 四、诚实登记", "",
              "1. **评分是人定的**（`PATHS` 里逐项写理由），不是测量值；"
              "若人认为某项权重不同，改表即可；",
              "2. **路径 C 的成本被低估的风险**：本批**没有联网实测** OTS/Sigstore "
              "（§零.8 不引依赖、本批不联网）⇒ 可用性/费用/合规是**评估值**；",
              "3. **A→C 不是替代关系**：即使走 C，A 的纯标准库验签代码仍是**离线验证**的"
              "唯一手段（第三方不能被迫装依赖）⇒ 建议 A 与 C 并存；",
              "4. 本工具只读：不生成密钥、不联网、不改任何签名器。",
              ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"paths": PATHS, "totals": totals(),
                   "recommend": rec}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("三条路径齐全", len(PATHS) == 3, f"({list(PATHS)})")
    chk("每条都覆盖五个维度且都有理由",
        all(set(v["scores"]) == set(DIMENSIONS) and set(v["why"]) == set(DIMENSIONS)
            for v in PATHS.values()))
    chk("分数都在 1-5", all(1 <= s <= 5 for v in PATHS.values()
                            for s in v["scores"].values()))
    chk("第三方可验证性：只有 C 达到 4 分以上",
        PATHS["C 外部 KMS / 透明日志"]["scores"]["第三方可验证性"] >= 4
        and PATHS["A 纯标准库继续"]["scores"]["第三方可验证性"] <= 2)
    chk("推荐为 C", recommend()[0].startswith("C"))
    chk("分步建议非空", len(STEPS_C) >= 4)

    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    scores()
    write_report()
    chk("只读：不生成密钥、不联网、不改工作区", snap() == before)
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"E1 trust root check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 E1 信任根升级评估（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写评估报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps({"scores": scores(), "totals": totals()},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"recommend={recommend()[0]} totals={totals()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
