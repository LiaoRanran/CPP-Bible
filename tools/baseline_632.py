"""632 任务0 · 基线台账（纯标准库，只读）

记录 632 批次 §一 standing baseline 到 data/632_baseline.md，并在 --check 模式下
额外测量（不写盘）：CI pytest 剩余 5 项用例名、代理 7990 端口状态、
data/vsa/vsa_secret.key 是否存在。

铁律（沿用 631 §零）：纯标准库、新工具必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import re
import socket
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CI_FINAL = ROOT / "data" / "ci_pytest_final_631.md"
VSA_DIR = ROOT / "data" / "vsa"
PROXY_PORT = 7990

# §一 Standing Baseline（快照值，不重算）
BASELINE: dict[str, str] = {
    "gate 规则数": "67",
    "gate 命中": "191（block=0 warn=186 advice=5）",
    "poison": "124/124",
    "replay": "confirm=56 refute=0 infra=0",
    "tool_integrity": "22 尺子",
    "W2": "IN114/OUT7/UNDEC0",
    "PCK": "83 张，authorized 27/83",
    "Authority V2 ledger": "452 条",
    "透明日志": "data/transparency_log.jsonl",
    "触达规则": "37/67",
    "逃逸率": "1/1406（CS 0.9062%）",
    "自身免疫率": "100%（warn 92，human 90 待填）",
    "coverage": "51.4%（18/35）",
    "CI pytest": "❌ 5 项红（环境依赖 4 + UTF-16 1）",
    "HEAD": "04088899",
    "远程": "1438cd5e（落后 31）",
    "雷1 触发标准": "3/5（路径解耦✅ v0.1✅ v0.2✅ 治理裁定⛔ 余量⛔）",
}


def ci_remaining_items(md_path: Path | None = None) -> list[str]:
    """从 631 A4 报告提取 CI 剩余 5 项用例名（形如 `tests/x.py::test_y`）。

    去重保序；若报告缺文件返回空列表（便于单测用临时文件覆盖）。
    """
    p = md_path or CI_FINAL
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8")
    found = re.findall(r"`([^`]*?::[^`]+)`", text)
    seen: list[str] = []
    for f in found:
        if f not in seen:
            seen.append(f)
    return seen


def proxy_up(host: str = "127.0.0.1", port: int = PROXY_PORT,
             timeout: float = 2.0) -> bool:
    """代理端口是否可连（A1 用：UP 才 push）。"""
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def vsa_secret_key_exists(vsa_dir: Path | None = None) -> bool:
    """data/vsa 下是否存在密钥文件（*.key 或 vsa_secret.key）。"""
    d = vsa_dir or VSA_DIR
    if not d.is_dir():
        return False
    return (d / "vsa_secret.key").exists() or any(d.glob("*.key"))


def write_baseline_md(out: Path | None = None) -> Path:
    """记录 §一 baseline + 额外测量到 data/632_baseline.md。"""
    out = out or (ROOT / "data" / "632_baseline.md")
    proxy = proxy_up()
    key = vsa_secret_key_exists()
    items = ci_remaining_items()
    lines = ["# 632 基线台账", "", "## §一 Standing Baseline", "",
             "| 指标 | 值 |"]
    for k, v in BASELINE.items():
        lines.append(f"| {k} | {v} |")
    lines += [
        "", "## 额外测量（任务0.2）", "",
        f"- 代理 7990 端口：`{'UP' if proxy else 'DOWN'}`",
        f"- `data/vsa/vsa_secret.key` 存在：`{key}`",
        f"- CI pytest 剩余 {len(items)} 项（来源：data/ci_pytest_final_631.md）：",
    ]
    for it in items:
        lines.append(f"  - `{it}`")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 任务0 基线台账")
    ap.add_argument("--check", action="store_true", help="只读测量，exit 0=通过")
    ap.add_argument("--out", default=str(ROOT / "data" / "632_baseline.md"))
    args = ap.parse_args(argv)
    if args.check:
        items = ci_remaining_items()
        print("632 任务0 --check OK：CI剩余 %d 项，代理 %s，vsa_secret.key %s"
              % (len(items), "UP" if proxy_up() else "DOWN",
                 "存在" if vsa_secret_key_exists() else "不存在"))
        return 0
    p = write_baseline_md(Path(args.out))
    print("已写", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
