#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""654 · 前端依赖本地化（web/vendor/）：把 cosmos.gl v3 的 ESM 依赖树抓到本地，
**版本统一**并**重写为相对导入**，使星图可离线 GPU 渲染；不需要网络、不依赖 CDN。

为什么（654）：
653 的 starmap 直接 `import('https://cdn.jsdelivr.net/npm/@cosmograph/cosmos@3/+esm')`。
jsDelivr 的 `+esm` 产物把依赖写死成**绝对 URL**，而其中同时出现
`@luma.gl/core@9.3.5`（由 `@luma.gl/shadertools@9.3.5` 拉入）与 `@luma.gl/core@9.3.6`
⇒ **同一份 luma.gl 被加载两次**（两个 `luma` 单例）⇒ 运行时报错，页面降级 2D。
import map 治不了这个（它只映射裸说明符，映射不了绝对 URL）。

本脚本的做法：
1. 从 ENTRY 出发 BFS 抓取所有 `/npm/...` 依赖（写内存）；
2. **版本统一**：把 `@luma.gl/*@9.3.5` 一律改写为 `@9.3.6`（9.3.6 全家桶都在，避免双份）；
3. 把每份产物里的导入全部改写成**相对路径** `./<name>.js`；
4. 落盘到 `web/vendor/`，entry 命名为 `cosmos.js`。

只用标准库。用法：`python web/vendor/_fetch_vendor.py`
（前端工具，放 web/ 下；不碰仓库 tools/ 与 tests/。）
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://cdn.jsdelivr.net"
ENTRY = "/npm/@cosmograph/cosmos@3.4.1/+esm"
OUT = Path(__file__).resolve().parent
ENTRY_NAME = "cosmos.js"
TIMEOUT = 30

# 版本统一表（正则 → 替换）：消掉 luma.gl 的 9.3.5/9.3.6 双份
UNIFY: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"@luma\.gl/([a-z0-9-]+)@9\.3\.5"), r"@luma.gl/\1@9.3.6"),
]

_IMPORT_RE = re.compile(r"""((?:from|import)\s*\(?\s*["'])([^"']+)(["'])""")


def unify(spec: str) -> str:
    for pat, rep in UNIFY:
        spec = pat.sub(rep, spec)
    return spec


def name_for(spec: str) -> str:
    """把 /npm/... 变成可读、确定、跨平台安全的文件名。"""
    s = spec[5:] if spec.startswith("/npm/") else spec
    s = s.replace("/+esm", "").replace("+esm", "")
    s = s.strip("/")
    s = s.replace("@", "").replace("/", "-")
    s = re.sub(r"[^A-Za-z0-9._-]", "-", s)
    return s + ".js"


def fetch(spec: str) -> str:
    url = BASE + spec
    req = urllib.request.Request(url, headers={"User-Agent": "CPP-Bible/654 vendor"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def resolve(base_spec: str, target: str) -> str | None:
    """把一份产物里的导入目标解析成绝对 `/npm/...`；裸说明符返回 None。"""
    if target.startswith("http://") or target.startswith("https://"):
        if not target.startswith(BASE):
            return None
        return urllib.parse.urlparse(target).path
    if target.startswith("/npm/"):
        return target
    if target.startswith("./") or target.startswith("../"):
        joined = urllib.parse.urljoin("https://cdn.jsdelivr.net" + base_spec, target)
        return urllib.parse.urlparse(joined).path
    return None  # 裸说明符（本依赖树里不应出现）


def main() -> int:
    raw: dict[str, str] = {}
    deps: dict[str, list[str]] = {}
    queue = [ENTRY]
    skipped: list[str] = []

    while queue:
        spec = unify(queue.pop(0))
        if spec in raw:
            continue
        try:
            body = fetch(spec)
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {spec}: {e}")
            return 2
        raw[spec] = body
        found: list[str] = []
        for _, target, _ in _IMPORT_RE.findall(body):
            r = resolve(spec, target)
            if r is None:
                skipped.append(f"{spec} -> {target}")
                continue
            r = unify(r)
            found.append(r)
            if r not in raw:
                queue.append(r)
        deps[spec] = sorted(set(found))

    # 组装映射 + 重写
    mapping = {spec: (ENTRY_NAME if spec == ENTRY else name_for(spec)) for spec in raw}
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for spec, body in raw.items():
        def _sub(m: re.Match[str]) -> str:
            prefix, target, suffix = m.group(1), m.group(2), m.group(3)
            r = resolve(spec, target)
            if r is None:
                return m.group(0)
            return prefix + "./" + mapping[unify(r)] + suffix

        text = _IMPORT_RE.sub(_sub, body)
        (OUT / mapping[spec]).write_text(text, encoding="utf-8")
        written += 1

    manifest = {
        "note": "654 本地化：由 web/vendor/_fetch_vendor.py 生成（BFS 抓取 + luma.gl 统一 9.3.6 + 相对导入重写）",
        "entry": ENTRY_NAME,
        "entry_spec": ENTRY,
        "files": written,
        "luma_gl_unified_to": "9.3.6",
        "modules": {k: mapping[k] for k in sorted(mapping)},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    total = sum((OUT / f).stat().st_size for f in set(mapping.values()))
    print(f"OK：{written} 个模块，共 {total/1024:.0f} KB → {OUT}")
    print("入口：web/vendor/" + ENTRY_NAME)
    luma = sorted({s for s in raw if "luma.gl" in s})
    print("luma.gl 模块（应全为 9.3.6）：")
    for s in luma:
        print("   ", s)
    if skipped:
        print("\n未解析（裸说明符，需人工确认）：")
        for s in skipped[:10]:
            print("   ", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
