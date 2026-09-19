"""609 D1 · OpenTimestamps 锚定：**生成 .ots 待上链文件 + 离线校验**（**不上日历、不上链**）。

铁律承接 609 任务书第 9 条：**不实际上链**。本工具只做两件事：
  * `stamp`：算摘要 ⇒ 序列化 `.ots`（**待上链**凭据），明确写下"还没膏历回执"；
  * `verify`：拿原始文件 + `.ots` **离线**复核摘要链是否闭合 ⇒ `sha256(file)` 必须等于
    `.ots` 里记的 file digest；链上 attestation 若仍是占位零 ⇒ 诚实报 `pending`（不是"通过"）。

字节布局（**OTS 兼容子集**，按 OpenTimestamps 文档实现；未经真实日历回执交叉校验，
故 verify 只验到 file digest + 操作链内部一致，比特币 attestation 一律报 pending）：

    <header>       magic("?OpenTimestamps??proof?" + 5B 定界) + version(0x01)
    <body>         varuint(len) + ops…
      OP_SHA256    0x08 <32B file digest>
      OP_APPEND    0x0f <32B arg>
    <attestation>  0x00 0x08 <32B>   （**占位零** ⇒ 待日历回执回填）

⚠️ 这是**结构化占位**不是伪造：attestation 段为占位零且 verify 会报 pending，
   任何人拿到这份 .ots 都能算出它**还没上链**，不会被误当成时间戳证明用。

CLI：
    stamp <file> [--out FILE.ots]      0 ok / 2 文件不存在
    verify <file> --ots FILE.ots       0 链闭合 / 1 摘要不符 / 2 文件缺失 / 3 .ots 结构非法
    --check                            0 结构自洽 / 1 破
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
_MAGIC = (bytes([0x00]) + b"OpenTimestamps" + bytes([0x00]) + bytes([0x00]) +
          b"proof" + bytes([0x00]) + bytes([0xBF, 0x89, 0xE2, 0xE8, 0x84, 0x8F]))
HEADER = _MAGIC
VERSION_BYTE = bytes([0x01])

#: 操作码表（OTS 文档 §Operations 的**子集**）
OP_SHA256 = 0x08
OP_APPEND = 0x0F
ATTESTATION = 0x00
ATTESTATION_BITCOIN = 0x08
OPS = {OP_SHA256: "sha256", OP_APPEND: "append"}


def file_digest(path: Path | str) -> bytes:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[ots] 文件不存在：{p}")
    return hashlib.sha256(p.read_bytes()).digest()


def _varuint(n: int) -> bytes:
    """OTS varuint：7 位一组，高位 continuation bit。"""
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0x00))
        if not n:
            return bytes(out)


def _read_varuint(buf: bytes, i: int) -> tuple[int, int]:
    shift, val = 0, 0
    while True:
        if i >= len(buf):
            raise ValueError("varuint 越界（.ots 被截断）")
        b = buf[i]
        i += 1
        val |= (b & 0x7F) << shift
        if not b & 0x80:
            return val, i
        shift += 7


# ── 序列化 ────────────────────────────────────────────────────────────────────
def build_ots(digest: bytes, *, placeholder: bytes | None = None) -> bytes:
    """按 OTS 兼容布局序列化：`sha256(file)` 的操作链 +（占位）比特币证明。"""
    body = bytearray()
    body.append(OP_SHA256)                       # FileHashOp：对文件内容取 sha256
    body.extend(digest)
    body.append(OP_APPEND)                       # OP_APPEND <arg>
    body.extend(digest)
    body.append(ATTESTATION)                     # attestation 段
    body.append(ATTESTATION_BITCOIN)
    body.extend(placeholder if placeholder is not None else bytes(32))
    return HEADER + VERSION_BYTE + _varuint(len(body)) + bytes(body)


def stamp(path: Path | str, *, out: Path | str | None = None) -> dict:
    p = Path(path)
    digest = file_digest(p)
    ots = build_ots(digest)
    target = Path(out) if out else p.with_suffix(p.suffix + ".ots")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(ots)
    return {"file": str(p), "sha256": digest.hex(), "ots": str(target),
            "ots_bytes": len(ots), "attestation": "pending",
            "created_at": datetime.now(timezone(timedelta(hours=8))).replace(
                microsecond=0).isoformat(),
            "note": "本 .ots 是**待上链**凭据：比特币 attestation 段是占位零 ⇒ 尚未上日历，"
                    "不得当作时间戳证明使用（609 铁律：不实际 submit）"}


# ── 校验 ──────────────────────────────────────────────────────────────────────
def parse_ots(raw: bytes) -> dict:
    """解析 `.ots`；结构非法 ⇒ ValueError。"""
    if len(raw) < len(HEADER) or raw[: len(HEADER)] != HEADER:
        raise ValueError("不是 OTS 文件（magic 头不匹配）")
    i = len(HEADER)
    ver = raw[i]
    i += 1
    if ver != 1:
        raise ValueError(f"不支持的 OTS 版本：{ver}")
    n, i = _read_varuint(raw, i)
    body = raw[i: i + n]
    if len(body) != n:
        raise ValueError(f"OTS 主体被截断：期望 {n}B，实得 {len(body)}B")
    ops: list[str] = []
    digest: bytes | None = None
    att_raw: bytes | None = None
    att_kind = None
    j = 0
    while j < len(body):
        op = body[j]
        if op == OP_SHA256:
            ops.append(OPS[op])
            digest = body[j + 1: j + 33]
            j += 33
        elif op == OP_APPEND:
            ops.append(OPS[op])
            j += 33
        elif op == ATTESTATION:
            kind = body[j + 1] if j + 1 < len(body) else None
            att_kind = "bitcoin" if kind == ATTESTATION_BITCOIN else f"unknown({kind:#x})"
            att_raw = body[j + 2:]                 # 跳过 kind 字节 ⇒ 32B 承诺才是判据
            break
        else:
            raise ValueError(f"未知操作码 {op:#x}（偏移 {j}）")
    return {"version": ver, "ops": ops,
            "file_digest": digest.hex() if digest else None,
            "attestation_kind": att_kind,
            "attestation_bytes": att_raw.hex() if att_raw is not None else None,
            "attestation_pending": bool(att_raw is None or set(att_raw) <= {0}),
            "body_len": n}


def verify(path: Path | str, ots_path: Path | str) -> dict:
    """离线复核：`.ots` 记的 file digest 必须等于 `sha256(file)`。"""
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[ots] 原始文件不存在：{p}")
    if not Path(ots_path).is_file():
        raise SystemExit(f"[ots] .ots 不存在：{ots_path}")
    try:
        parsed = parse_ots(Path(ots_path).read_bytes())
    except ValueError as exc:
        raise SystemExit(f"[ots] .ots 结构非法：{exc}") from exc
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    matched = parsed["file_digest"] == actual
    return {"file": str(p), "ots": str(ots_path), "sha256": actual,
            "expected": parsed["file_digest"], "digest_matches": matched,
            "attestation_pending": parsed["attestation_pending"],
            "ops": parsed["ops"],
            "verdict": "digest_ok_pending_anchor" if matched else "digest_mismatch"}


def check() -> list[str]:
    """结构自检（round-trip）+ 仓内已有 .ots 是否可解析。"""
    problems: list[str] = []
    sample = bytes([0x11]) * 32
    try:
        parsed = parse_ots(build_ots(sample))
    except Exception as exc:                       # 自检都 ⇒ fail-loud
        return [f"OTS 自检异常：{exc!r}"]
    if parsed["file_digest"] != sample.hex():
        problems.append(f"round-trip 摘要不一致：{parsed['file_digest']}")
    if parsed["ops"] != ["sha256", "append"]:
        problems.append(f"操作链解析异常：{parsed['ops']}")
    if not parsed["attestation_pending"]:
        problems.append("默认生成的 .ots 必须标记 attestation pending（占位零）")
    for p in sorted((ROOT / "data").rglob("*.ots")):
        try:
            parse_ots(p.read_bytes())
        except ValueError as exc:
            problems.append(f"{p}: {exc}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="opentimestamps_anchor",
                                 description="609 D1 OpenTimestamps 锚定（生成待上链 .ots + 离线校验）")
    ap.add_argument("--version", action="version", version=f"opentimestamps_anchor {VERSION}")
    ap.add_argument("--check", action="store_true", help="结构自检 + 仓内已有 .ots 可解析")
    sub = ap.add_subparsers(dest="cmd")

    sp = sub.add_parser("stamp", help="生成待上链 .ots（不 submit）")
    sp.add_argument("file")
    sp.add_argument("--out", default=None)

    sp = sub.add_parser("verify", help="离线复核摘要链")
    sp.add_argument("file")
    sp.add_argument("--ots", required=True)
    sp.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[ots] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[ots] --check OK：magic/版本/操作链 round-trip 自洽，"
              f"仓内 .ots {len(list((ROOT / 'data').rglob('*.ots')))} 份全部可解析")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    if a.cmd == "stamp":
        try:
            info = stamp(a.file, out=a.out)
        except SystemExit as exc:
            print(exc, file=sys.stderr)
            return 2
        print(f"STAMPED(pending): {info['sha256'][:16]}… → {info['ots']}"
              f"（{info['ots_bytes']}B · attestation={info['attestation']}）")
        return 0

    try:
        res = verify(a.file, a.ots)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        code = str(exc)
        return 3 if "结构非法" in code else 2
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    if not res["digest_matches"]:
        print(f"[ots] ❌ 摘要不符：ots 记 {res['expected']}，文件实为 {res['sha256']}",
              file=sys.stderr)
        return 1
    tail = "attestation 仍是**占位零** ⇒ 尚未上日历（不得当时间戳证明用）" \
        if res["attestation_pending"] else "attestation 已回填（需人工/监工核验来源）"
    print(f"[ots] ✓ 摘要链闭合 {res['sha256'][:16]}… · {tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
