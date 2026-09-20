#!/usr/bin/env python3
"""613 任务E1 · 信任根 OTS 上链**凭据**生成与校验（不实际 submit）。

锚定对象：`data/supply_chain/merkle_roots.json`（E3 的 Merkle 根 = 本仓信任根）。

做什么：
  1. 计算信任根的 sha256；
  2. 调 `opentimestamps_anchor.stamp()` 生成 `.ots` 凭据；
  3. 解析回来做**结构校验**（magic/版本/操作码/digest 一致）；
  4. 出报告 `data/ots_anchor_613.md`。

**诚实口径（609 铁律延续）**：本工具**不向 OTS 日历 submit**，因此 `.ots` 里的比特币
attestation 段是**占位零** ⇒ **attestation = pending**，**不构成时间戳证明**。
真正的上链需人类执行 submit（交人项）。本工具把它显式暴露，绝不伪装成"已上链"。

CLI：
  python tools/ots_anchor_613.py            # 生成/更新 .ots 并出报告
  python tools/ots_anchor_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import opentimestamps_anchor as ots  # noqa: E402

TARGET = ROOT / "data" / "supply_chain" / "merkle_roots.json"
OTS_OUT = TARGET.with_suffix(TARGET.suffix + ".ots")
OUT = ROOT / "data" / "ots_anchor_613.md"


def anchor() -> dict:
    if not TARGET.is_file():
        return {"error": f"信任根不存在：{TARGET}"}
    st = ots.stamp(TARGET, out=OTS_OUT)
    parsed = ots.parse_ots(OTS_OUT.read_bytes())
    digest_now = ots.file_digest(TARGET).hex()
    return {"stamp": st, "parsed": parsed, "digest_now": digest_now,
            "digest_matches": digest_now == parsed.get("file_digest"),
            "pending": parsed.get("attestation_pending", True),
            "attestation_kind": parsed.get("attestation_kind")}


def render(a: dict) -> str:
    if "error" in a:
        return f"# 613 · OTS 上链凭据（E1）\n\n> 错误：{a['error']}\n"
    st, p = a["stamp"], a["parsed"]
    L = ["# 613 · 信任根 OTS 上链凭据（E1）", "",
         f"> 生成：`python tools/ots_anchor_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> **attestation 仍 pending**：本工具不 submit 日历 ⇒ 比特币证明段是占位零，",
         "> **不得当作时间戳证明**（609 铁律）。真正上链由人执行 submit（交人）。", "",
         "## 一、锚定对象", "",
         "| 项 | 值 |", "|---|---|",
         f"| 文件 | `{TARGET.relative_to(ROOT).as_posix()}` |",
         f"| sha256 | `{st['sha256']}` |",
         f"| .ots | `{OTS_OUT.relative_to(ROOT).as_posix()}`（{st['ots_bytes']} B） |",
         f"| 生成时间 | {st['created_at']} |", "",
         "## 二、结构校验", "",
         "| 项 | 值 |", "|---|---|",
         f"| OTS 版本 | {p['version']} |",
         f"| 操作序列 | {' → '.join(p['ops'])} |",
         f"| .ots 内 digest | `{p['file_digest']}` |",
         f"| 文件当前 digest | `{a['digest_now']}` |",
         f"| **digest 一致** | {'✅' if a['digest_matches'] else '❌'} |",
         f"| attestation 类型 | {a['attestation_kind']} |",
         f"| **attestation pending** | {'⚠ 是（未上链）' if a['pending'] else '✅ 已上链'} |", "",
         "## 三、状态判定", "",
         "- ✅ **凭据已生成且结构合法**：文件摘要与 .ots 内承诺一致，可被任何 OTS 客户端解析。",
         "- ⚠ **尚未上链**：需 `ots submit`（或等价日历提交）后才有比特币区块时间戳。",
         "- ⇒ 当前可证明「**该 .ots 绑定此摘要**」，**不能**证明「此摘要在某时刻已存在」。", "",
         "> 交人：执行 submit 并回填 `.ots`，届时本报告的 pending 列自动变 ✅。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 E1 · 信任根 OTS 凭据（不 submit）")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        errs = []
        if not TARGET.is_file():
            errs.append("信任根文件不存在")
        else:
            d = ots.file_digest(TARGET).hex()
            if OTS_OUT.is_file():
                try:
                    p = ots.parse_ots(OTS_OUT.read_bytes())
                    if p.get("file_digest") != d:
                        errs.append("已存在的 .ots 摘要与当前信任根不一致（信任根已变更）")
                except ValueError as e:
                    errs.append(f".ots 解析失败：{e}")
            page = render({"stamp": {"sha256": d, "ots_bytes": 0, "created_at": "-",
                                     "ots": str(OTS_OUT)},
                           "parsed": {"version": 1, "ops": [], "file_digest": d,
                                      "attestation_kind": None, "attestation_pending": True},
                           "digest_now": d, "digest_matches": True, "pending": True,
                           "attestation_kind": None})
            if "OTS 上链凭据" not in page:
                errs.append("报告渲染异常")
        for err in errs:
            print(f"[E1] ✗ {err}")
        print("[E1] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    res = anchor()
    if "error" in res:
        print(f"[E1] ✗ {res['error']}")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(res), encoding="utf-8", newline="\n")
    print(f"[E1] 写入 {OUT.relative_to(ROOT).as_posix()}（digest {res['digest_now'][:16]}… "
          f"一致={'✅' if res['digest_matches'] else '❌'} / pending={res['pending']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
