"""安全批量替换某章 cpp 块正文（L2 真机深耕管线的通用引擎）。

把每波手写的临时 `_chNNN_deep.py` 固化为一条命令。工程要点（吸取历史教训）：
- 读原始 bytes 判断行尾（CRLF/LF），写回保持原行尾；
- 从大到小替换，前序插入不改变后续块的索引；
- 先完整拼好 payload 再一次写入（避免 join 异常时文件被截断为 0 字节）；
- 允许把 ```cpp 围栏整体换成 ```bash（工具命令块转真命令），自动报 cpp 块数净变化；
- dry-run 默认只打印 diff，--apply 才落盘。

用法：
    python tools/patch_blocks.py Book/partX/chYY.md patch.json           # dry-run
    python tools/patch_blocks.py --apply Book/partX/chYY.md patch.json

patch.json 形如（block = compile_all.extract_blocks 的 1-based cpp 块序号）：
    [
      {"block": 24, "fence": "cpp",  "body": "#include <bit>\\n..."},
      {"block": 27, "fence": "bash", "body": "# 命令\\ncmake ..."}
    ]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Sequence

FENCE_OPEN_RE = re.compile(r"^\s*```(\w+)")
FENCE_CLOSE_RE = re.compile(r"^\s*```\s*$")


def _split_blocks(text: str) -> list[tuple[int, int]]:
    """返回 [(open_line_idx, close_line_idx)]，0-based，只含 ```cpp 围栏。"""
    lines = text.split("\n")
    out: list[tuple[int, int]] = []
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_OPEN_RE.match(lines[i])
        if m and m.group(1).lower() in ("cpp", "c++"):
            j = i + 1
            while j < n and not FENCE_CLOSE_RE.match(lines[j]):
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


def load_patch(patch_file: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(patch_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"patch JSON 解析失败: {e}") from e
    if not isinstance(data, list) or not data:
        raise SystemExit("patch 必须是非空数组")
    for item in data:
        if not isinstance(item, dict) or "block" not in item or "body" not in item:
            raise SystemExit(f"patch 项必须是 {{block, body[, fence]}}: {item}")
        if not isinstance(item["block"], int) or not isinstance(item["body"], str):
            raise SystemExit(f"block 须为 int、body 须为 str: {item}")
    return data


def apply_patch(path: Path, patch: list[dict[str, Any]], do_write: bool) -> int:
    raw = path.read_bytes()
    ending = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    spans = _split_blocks(text)

    target = sorted((p["block"], p) for p in patch)
    max_block = max(p["block"] for p in patch)
    if max_block > len(spans):
        raise SystemExit(f"block#{max_block} 越界（本章共 {len(spans)} 个 cpp/c++ 块）")

    fence_swaps = 0
    for num, item in target:
        if num != int(item["block"]):
            pass
        s, e = spans[int(item["block"]) - 1]
        want = str(item.get("fence", "cpp")).lower()
        nb = item["body"].rstrip("\n").split("\n")
        if nb and nb[-1] == "":
            nb = nb[:-1]
        for ln in nb:
            if FENCE_OPEN_RE.match(ln.strip()) and ln.strip() != "```":
                print(f"  !! 警告: block#{item['block']} 正文含围栏起始行（错位）: {ln[:40]!r}")
        old_body = lines[s + 1:e]
        print(f"[diff] block#{item['block']} lines[{s+1}-{e}] "
              f"body {len(old_body)} -> {len(nb)} lines")
        for ln in old_body[:2]:
            print("  - " + ln[:110])
        for ln in nb[:2]:
            print("  + " + ln[:110])
        if want != "cpp":
            if not lines[s].strip().startswith("```cpp"):
                raise SystemExit(f"block#{item['block']} 开篇围栏不是 ```cpp，不能换语言")
            lines[s] = "```bash"
            fence_swaps += 1
        lines[s + 1:e] = nb

    if not do_write:
        print(f"\n[dry-run] {len(patch)} 处替换预览完成；--apply 落盘。"
              f"（将转 bash {fence_swaps} 处，cpp 块数 -{fence_swaps}）")
        return -fence_swaps

    payload = "\n".join(lines).replace("\n", ending.decode("ascii"))
    # 安全写入：payload 已在内存拼好，写入是最后一步
    path.write_bytes(payload.encode("utf-8"))
    after = len(_split_blocks(payload))
    print(f"[apply] wrote {len(payload.encode('utf-8'))} bytes to {path}")
    print(f"[apply] cpp 块数: 变前 {len(spans)} -> 变后 {after}（转 bash {fence_swaps} 处）")
    return after


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="安全批量替换某章 cpp 块正文")
    ap.add_argument("chapter", help="章 md 路径")
    ap.add_argument("patch", help="patch JSON 路径")
    ap.add_argument("--apply", action="store_true", help="落盘（默认 dry-run）")
    a = ap.parse_args(argv)

    path = Path(a.chapter)
    if not path.exists():
        raise SystemExit(f"文件不存在: {path}")
    apply_patch(path, load_patch(Path(a.patch)), do_write=a.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
