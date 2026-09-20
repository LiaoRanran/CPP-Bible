#!/usr/bin/env python3
"""613 任务E2 · in-toto link 元数据（供应链步骤证据）。

in-toto 的 link 元数据记录一个步骤的 **materials（输入）/ products（输出）/ command /
byproducts / signature**，使"谁用什么产出了什么"可机器验证。

**诚实口径（本批必须写明）**：
  标准 in-toto 用 **非对称签名**（ed25519/rsa，需 `cryptography`/`nacl`/`ecdsa`）。
  本仓 venv 实测**均无**这些库（cryptography/nacl/ecdsa/rsa 全部 False），
  故本工具以 **HMAC-SHA256（对称）** 代替，并在 `signature.scheme` 显式写
  `hmac-sha256-not-in-toto-standard`：
    * 能证明「link 未被篡改 + 由持钥者生成」（完整性 + 持有证明）；
    * **不能**提供 in-toto 要求的「非否认 / 公钥可验」。
  ⇒ 真正的非对称签名是**交人项**（装 `cryptography` 后换 ed25519，或人工 gpg 签）。

产物：`data/supply_chain/link_613_verify.json` + 报告 `data/in_toto_link_613.md`。

CLI：
  python tools/in_toto_link.py --make --name <step> [--material P]... [--product P]...
                               [--command "..."] [--key-file K] [--key-hex H]
  python tools/in_toto_link.py --verify <link.json> --key-file K
  python tools/in_toto_link.py --check      # 自验证（结构 + 哈希自洽，不依赖密钥）
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_OUT = ROOT / "data" / "supply_chain" / "link_613_verify.json"
REPORT = ROOT / "data" / "in_toto_link_613.md"
SCHEME = "hmac-sha256-not-in-toto-standard"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def _hashes(paths: list[Path]) -> dict[str, dict[str, str]]:
    out = {}
    for p in paths:
        p = Path(p)
        if not p.is_file():
            continue
        try:
            rel = p.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            rel = p.name
        out[rel] = {"sha256": sha256_file(p)}
    return out


def canonical(body: dict) -> bytes:
    return json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def keyid_of(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()[:16]


def build_link(name: str, materials: list[Path], products: list[Path],
               command: list[str], byproducts: dict | None, key: bytes | None) -> dict:
    body = {
        "_type": "link",
        "name": name,
        "materials": _hashes(materials),
        "products": _hashes(products),
        "command": command,
        "byproducts": byproducts or {},
        "environment": {"tool": "in_toto_link.py", "python": sys.version.split()[0]},
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    link = dict(body)
    if key is None:
        link["signature"] = {"scheme": "none", "note": "未签名（未提供密钥）"}
    else:
        link["signature"] = {"scheme": SCHEME, "keyid": keyid_of(key),
                             "sig": hmac.new(key, canonical(body), hashlib.sha256).hexdigest()}
    return link


def verify_link(link: dict, key: bytes | None) -> tuple[bool, list[str]]:
    errs = []
    if link.get("_type") != "link":
        errs.append("不是 link 元数据（_type != link）")
    for sect in ("materials", "products"):
        if sect not in link:
            errs.append(f"缺 {sect} 段")
            continue
        for rel, meta in link[sect].items():
            p = ROOT / rel
            if not p.is_file():
                errs.append(f"{sect} 文件不存在：{rel}")
                continue
            if sha256_file(p) != meta.get("sha256"):
                errs.append(f"{sect} 哈希不符：{rel}")
    sig = link.get("signature") or {}
    if sig.get("scheme") == SCHEME:
        if key is None:
            errs.append("link 带 HMAC 签名但未提供密钥 ⇒ 无法验签")
        else:
            body = {k: v for k, v in link.items() if k != "signature"}
            want = hmac.new(key, canonical(body), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(want, sig.get("sig", "")):
                errs.append("HMAC 验签失败（link 被篡改或密钥不对）")
            if keyid_of(key) != sig.get("keyid"):
                errs.append("keyid 不匹配")
    elif sig.get("scheme") == "none":
        errs.append("未签名 ⇒ 不可作为供应链证据")
    return (not errs), errs


def render(link: dict, ok: bool | None, errs: list[str]) -> str:
    sig = link.get("signature", {})
    L = ["# 613 · in-toto link 元数据（E2）", "",
         f"> 生成：`python tools/in_toto_link.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         f"> 产物：`{LINK_OUT.relative_to(ROOT).as_posix()}`", "",
         "## 一、步骤", "",
         "| 项 | 值 |", "|---|---|",
         f"| name | {link.get('name')} |",
         f"| command | {' '.join(link.get('command', []))} |",
         f"| materials | {len(link.get('materials', {}))} |",
         f"| products | {len(link.get('products', {}))} |",
         f"| signature scheme | **{sig.get('scheme')}** |",
         f"| keyid | {sig.get('keyid', '—')} |", "",
         "## 二、⚠ 签名口径（必读）", "",
         "- 标准 in-toto 要求**非对称签名**（ed25519/rsa）。本仓 venv 实测无 "
         "`cryptography`/`nacl`/`ecdsa`/`rsa` ⇒ 本工具退化为 **HMAC-SHA256（对称）**。",
         "- 可提供：完整性（未篡改）+ 持钥证明；**不可**提供：非否认 / 公钥可验。",
         "- ⇒ 真正非对称签名是**交人项**。", ""]
    if ok is not None:
        L += ["## 三、校验结果", "", f"- {'✅ 通过' if ok else '❌ 失败'}"]
        for e in errs:
            L.append(f"  - {e}")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 E2 · in-toto link 元数据")
    ap.add_argument("--make", action="store_true")
    ap.add_argument("--name", default="613-verify")
    ap.add_argument("--material", action="append", default=[])
    ap.add_argument("--product", action="append", default=[])
    ap.add_argument("--command", default="")
    ap.add_argument("--key-file")
    ap.add_argument("--key-hex")
    ap.add_argument("--verify")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    def _key() -> bytes | None:
        if a.key_hex:
            return bytes.fromhex(a.key_hex)
        if a.key_file and Path(a.key_file).is_file():
            return Path(a.key_file).read_bytes()
        env = os.environ.get("IN_TOTO_HMAC_KEY")
        return env.encode() if env else None

    if a.check:
        errs = []
        link = build_link("selftest", [__file__], [__file__], ["echo", "hi"], {"return-value": 0},
                          b"k")
        ok, e = verify_link(link, b"k")
        if not ok:
            errs += e
        ok2, _ = verify_link(link, b"wrong")
        if ok2:
            errs.append("错误密钥竟验签通过")
        unsigned = build_link("nosig", [], [], [], {}, None)
        ok3, _ = verify_link(unsigned, None)
        if ok3:
            errs.append("未签名 link 不应通过校验")
        for e in errs:
            print(f"[E2] ✗ {e}")
        print("[E2] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    if a.verify:
        link = json.loads(Path(a.verify).read_text(encoding="utf-8"))
        ok, errs = verify_link(link, _key())
        for e in errs:
            print(f"[E2] ✗ {e}")
        print(f"[E2] {'✅ 校验通过' if ok else '❌ 校验失败'}")
        return 0 if ok else 1

    if a.make:
        key = _key()
        link = build_link(a.name, [Path(x) for x in a.material], [Path(x) for x in a.product],
                          a.command.split() if a.command else [], {"return-value": 0}, key)
        LINK_OUT.parent.mkdir(parents=True, exist_ok=True)
        LINK_OUT.write_text(json.dumps(link, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ok, errs = verify_link(link, key)
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(link, ok, errs), encoding="utf-8", newline="\n")
        print(f"[E2] 写入 {LINK_OUT.relative_to(ROOT).as_posix()}（materials "
              f"{len(link['materials'])} / products {len(link['products'])} / "
              f"scheme {link['signature']['scheme']}）")
        return 0

    print("[E2] 需要 --make / --verify / --check")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
