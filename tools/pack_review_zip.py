"""626 A2 · 人审决策包打包器（**跨平台正斜杠**，纯标准库）

外部大模型发现：原决策包 ZIP 的 36 个 entry 全部使用反斜杠 `\\` 作为路径字符，
Linux 下会被视为文件名中的普通字符而非目录分隔符 ⇒ 不适合作为跨平台发布格式。

本工具：
- 用 `zipfile.ZipInfo` 显式写入 **正斜杠 `/`** 路径（不依赖 `os.sep`）
- 强制 UTF-8，可选控制字符清洗
- 自带 `SNAPSHOT_MANIFEST.json`（git_sha + generated_at + 文件计数/大小）
- `--check` 模式：校验已有 ZIP 的路径分隔符 / 完整性（只读）

**只读源目录**：不修改包内原文件。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TEXT_EXT = (".md", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".html")
CTRL = set(range(0x00, 0x20)) - {0x0A, 0x0D}


def _git_sha() -> str:
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                           text=True, cwd=ROOT, timeout=30)
        return p.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _clean(data: bytes) -> bytes:
    """清洗控制字符（保留 \\n \\r）。"""
    return bytes(b for b in data if b not in CTRL)


def iter_files(src: str) -> list[tuple[str, str]]:
    """返回 [(绝对磁盘路径, 包内相对路径(正斜杠))]。"""
    out: list[tuple[str, str]] = []
    for dirpath, _dn, fns in os.walk(src):
        for fn in sorted(fns):
            disk = os.path.join(dirpath, fn)
            rel = os.path.relpath(disk, src)
            rel = rel.replace(os.sep, "/").replace("\\", "/")
            out.append((disk, rel))
    return sorted(out, key=lambda x: x[1])


def build_manifest(src: str, files: list[tuple[str, str]]) -> dict:
    h = hashlib.sha256()
    total = 0
    for disk, rel in files:
        with open(disk, "rb") as fh:
            b = fh.read()
        total += len(b)
        h.update(rel.encode("utf-8") + b"|" + b)
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_sha": _git_sha(),
        "file_count": len(files),
        "uncompressed_bytes": total,
        "dataset_sha256": h.hexdigest(),
        "path_separator": "/",
        "note": "由 tools/pack_review_zip.py 生成；路径分隔符强制为 / （跨平台）。",
    }


def pack(src: str, out_path: str, clean_ctrl: bool = True) -> dict:
    files = iter_files(src)
    man = build_manifest(src, files)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for disk, rel in files:
            with open(disk, "rb") as fh:
                data = fh.read()
            if clean_ctrl and rel.endswith(TEXT_EXT):
                data = _clean(data)
            zi = zipfile.ZipInfo(rel, date_time=time.localtime()[:6])
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        z.writestr("SNAPSHOT_MANIFEST.json",
                   json.dumps(man, ensure_ascii=False, indent=2).encode("utf-8"))
    return {"out": out_path, "manifest": man,
            "size": os.path.getsize(out_path), "entries": len(files) + 1}


def check(zip_path: str) -> tuple[int, dict]:
    """校验 ZIP：路径分隔符全为正斜杠 / 可正常读取 / 含 SNAPSHOT_MANIFEST。"""
    res: dict = {"ok": True, "entries": 0, "backslash": 0, "has_manifest": False,
                 "bad_crc": 0, "control_chars": 0}
    if not os.path.exists(zip_path):
        res["ok"] = False
        res["error"] = "not found"
        return 1, res
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        res["entries"] = len(names)
        res["backslash"] = sum(1 for n in names if "\\" in n)
        res["has_manifest"] = "SNAPSHOT_MANIFEST.json" in names
        res["bad_crc"] = len(z.testzip() and [z.testzip()] or [])
        for n in names:
            if n.endswith(TEXT_EXT):
                data = z.read(n)
                if any(b in CTRL for b in data):
                    res["control_chars"] += 1
    ok = (res["backslash"] == 0 and res["bad_crc"] == 0
          and res["has_manifest"] and res["control_chars"] == 0)
    res["ok"] = ok
    return (0 if ok else 1), res


def selftest() -> int:
    import tempfile
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "sub"))
        p1 = os.path.join(td, "a.md")
        open(p1, "w", encoding="utf-8").write("hello\n")
        p2 = os.path.join(td, "sub", "b.md")
        open(p2, "wb").write(b"bad\x08ctrl\x0b\n")
        zp = os.path.join(td, "out.zip")
        pack(td, zp)
        chk("打包成功", os.path.exists(zp))
        rc, res = check(zp)
        chk("check 通过", rc == 0, f"(backslash={res['backslash']} ctrl={res['control_chars']})")
        chk("路径全为正斜杠", res["backslash"] == 0)
        chk("控制字符已清洗", res["control_chars"] == 0)
        chk("含 SNAPSHOT_MANIFEST", res["has_manifest"])
        with zipfile.ZipFile(zp) as z:
            chk("子目录 entry 用 /", "sub/b.md" in z.namelist())
        man = json.loads(zipfile.ZipFile(zp).read("SNAPSHOT_MANIFEST.json"))
        chk("manifest 含 git_sha", "git_sha" in man and man["git_sha"])
        chk("manifest path_separator=/", man["path_separator"] == "/")
    print(f"A2 pack selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 A2 人审决策包打包器（正斜杠跨平台）")
    ap.add_argument("--src", help="源目录")
    ap.add_argument("--out", help="输出 ZIP 路径")
    ap.add_argument("--check", action="store_true", help="自检；或配合 --zip 校验已有包")
    ap.add_argument("--zip", help="要校验的 ZIP 路径")
    ap.add_argument("--no-clean", action="store_true", help="不清洗控制字符")
    args = ap.parse_args(argv)

    if args.check and args.zip:
        rc, res = check(args.zip)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return rc
    if args.check:
        return selftest()
    if not (args.src and args.out):
        ap.error("需要 --src 与 --out")
    r = pack(args.src, args.out, clean_ctrl=not args.no_clean)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
