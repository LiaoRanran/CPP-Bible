#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""collect_realworld_683.py — 683-A1：真实靶场候选清单 + 在线验证（NVD API v2）。

红线遵守
========
* 候选清单是**待验证假设**，不是结论：每条必须经 NVD API 在线查询，
  只有 API 返回了该 CVE 的真实记录（含官方英文描述）才进入 verified 集。
* 输出里 CVE 描述、CVSS、发布时间、参考链接**全部来自 API 应答原文**，
  不由本脚本或作者转述 —— 从源头排除"编造"。
* 无网络的条目一律保留 not_verified 状态、绝不静默升级为"存在"。

用法
====
    python tools/collect_realworld_683.py --stage verify   # 逐条 NVD API 查询（限速 6s/条，增量落盘）
    python tools/collect_realworld_683.py --stage report   # 汇总统计
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "683_real_world_candidates_verified.json"
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId="
RATE_S = 6.2   # NVD 无 key 限速：5 req / 30s

# ─────────────────────────────────────────────────────────────────────────────
# 候选清单（130 条；source_type: cve / ghsa / issue / commit / pwn）
# 每条 = (cve_or_id, project, stype, defect_type_guess, mechanism)
# defect_type 使用 1147 样本同一套 34 类规范词表；mechanism 为作者对漏洞类别的
# 待验证描述（验证阶段由 NVD 描述原文覆盖/核对）。
# ─────────────────────────────────────────────────────────────────────────────
CANDIDATES: list[tuple[str, str, str, str, str]] = [
    # ── OpenSSL（系统级加密库；C 实现、C++ 生态调用）──────────────────────
    ("CVE-2014-0160", "OpenSSL", "cve", "out_of_bounds", "Heartbleed：TLS heartbeat 长度字段未校验导致越界读"),
    ("CVE-2022-0778", "OpenSSL", "cve", "logic_error", "BN_mod_sqrt 对非素数模无限循环（DoS）"),
    ("CVE-2021-3711", "OpenSSL", "cve", "out_of_bounds", "SM2 解密缓冲区溢出"),
    ("CVE-2021-3712", "OpenSSL", "cve", "out_of_bounds", "ASN1_STRING 越界读"),
    ("CVE-2023-0286", "OpenSSL", "cve", "type_punning", "X.400 地址类型混淆（GENERAL_NAME 联合体误用）"),
    ("CVE-2022-4450", "OpenSSL", "cve", "double_free", "PEM_read_bio_ex 双重释放"),
    ("CVE-2023-0215", "OpenSSL", "cve", "use_after_free", "BIO 清理后释放后使用"),
    ("CVE-2022-3602", "OpenSSL", "cve", "out_of_bounds", "X.509 punycode 4 字节栈溢出"),
    ("CVE-2022-3786", "OpenSSL", "cve", "out_of_bounds", "X.509 punycode 任意长度栈溢出"),
    ("CVE-2015-1793", "OpenSSL", "cve", "logic_error", "证书链验证绕过（替代链）"),
    ("CVE-2016-2107", "OpenSSL", "cve", "logic_error", "AES-NI CBC padding oracle（填充检查与 MAC 顺序）"),
    # ── glibc（C++ 运行时底座）───────────────────────────────────────────
    ("CVE-2015-7547", "glibc", "cve", "out_of_bounds", "getaddrinfo 栈缓冲区溢出"),
    ("CVE-2023-4911", "glibc", "cve", "out_of_bounds", "Looney Tunables：GLIBC_TUNABLES 环境变量解析缓冲区溢出"),
    ("CVE-2021-33574", "glibc", "cve", "use_after_free", "mq_notify 释放后使用"),
    ("CVE-2022-23218", "glibc", "cve", "out_of_bounds", "svcunix_create 栈缓冲区溢出"),
    ("CVE-2023-6246", "glibc", "cve", "out_of_bounds", "syslog __vsyslog_internal 堆缓冲区溢出"),
    ("CVE-2021-3999", "glibc", "cve", "out_of_bounds", "getcwd 单字节缓冲区下溢"),
    # ── curl ────────────────────────────────────────────────────────────
    ("CVE-2023-38545", "curl", "cve", "out_of_bounds", "SOCKS5 握手堆缓冲区溢出（主机名过长回退本地解析）"),
    ("CVE-2023-38546", "curl", "cve", "logic_error", "cookie 文件注入"),
    ("CVE-2022-32221", "curl", "cve", "logic_error", "307/308 重定向后 POST 方法/请求体错误复用"),
    ("CVE-2021-22947", "curl", "cve", "logic_error", "STARTTLS 响应注入"),
    ("CVE-2021-22898", "curl", "cve", "out_of_bounds", "TELNET 栈溢出"),
    # ── Web 服务器 / 网络 ────────────────────────────────────────────────
    ("CVE-2021-23017", "nginx", "cve", "out_of_bounds", "DNS resolver off-by-one 堆写"),
    ("CVE-2019-20372", "nginx", "cve", "logic_error", "error_page 请求走私"),
    ("CVE-2021-41773", "Apache HTTP Server", "cve", "logic_error", "路径规范化缺陷导致目录穿越"),
    ("CVE-2021-42013", "Apache HTTP Server", "cve", "logic_error", "路径穿越修复绕过"),
    ("CVE-2024-6387", "OpenSSH", "cve", "data_race", "regreSSHion：信号处理器竞争导致远程代码执行"),
    ("CVE-2018-15473", "OpenSSH", "cve", "logic_error", "用户名枚举（认证时延差异）"),
    # ── XML / 压缩 / 图像 ───────────────────────────────────────────────
    ("CVE-2022-23308", "libxml2", "cve", "use_after_free", "xmlXPtrRangeToFunction 释放后使用"),
    ("CVE-2022-29824", "libxml2", "cve", "integer_overflow", "buf 长度整数溢出导致越界写"),
    ("CVE-2023-28484", "libxml2", "cve", "null_pointer_deref", "schema 解析 NULL 指针解引用"),
    ("CVE-2017-9047", "libxml2", "cve", "out_of_bounds", "xmlSnprintfElementContent 栈缓冲区溢出"),
    ("CVE-2022-37434", "zlib", "cve", "out_of_bounds", "inflateGetHeader 堆缓冲区溢出"),
    ("CVE-2018-25032", "zlib", "cve", "out_of_bounds", "deflate 内存破坏（未跟踪块）"),
    ("CVE-2018-13785", "libpng", "cve", "integer_overflow", "pngrutil 整数溢出致堆越界写"),
    ("CVE-2016-10087", "libpng", "cve", "null_pointer_deref", "png_set_text_2 NULL 解引用"),
    ("CVE-2019-7317", "libpng", "cve", "use_after_free", "png_image_free 释放后使用"),
    ("CVE-2023-4863", "libwebp", "cve", "out_of_bounds", "WebP lossless 堆缓冲区溢出（2023 全行业影响）"),
    ("CVE-2020-15999", "FreeType", "cve", "out_of_bounds", "Pwn2Own 2020：PNG 位图堆缓冲区溢出"),
    ("CVE-2022-27404", "FreeType", "cve", "out_of_bounds", "sfnt_init_face 堆缓冲区溢出"),
    ("CVE-2022-0561", "libtiff", "cve", "null_pointer_deref", "TIFFReadDirectory NULL 解引用"),
    ("CVE-2022-0562", "libtiff", "cve", "null_pointer_deref", "TIFFReadDirectory NULL 解引用"),
    ("CVE-2016-5321", "libtiff", "cve", "out_of_bounds", "DumpModeDecode 越界读"),
    ("CVE-2022-25315", "expat", "cve", "integer_overflow", "storeAtts 整数溢出致越界"),
    ("CVE-2016-0718", "expat", "cve", "out_of_bounds", "XML 解析堆缓冲区溢出"),
    ("CVE-2022-40674", "expat", "cve", "use_after_free", "doContent 释放后使用"),
    ("CVE-2016-3714", "ImageMagick", "cve", "logic_error", "ImageTragick：外部委托命令注入"),
    ("CVE-2021-20309", "ImageMagick", "cve", "integer_overflow", "WriteTHUMBNAILImage 整数溢出"),
    ("CVE-2020-12284", "FFmpeg", "cve", "out_of_bounds", "cbs_jpeg 堆缓冲区溢出"),
    ("CVE-2016-1897", "FFmpeg", "cve", "logic_error", "HLS 播放列表任意文件读取"),
    ("CVE-2023-49502", "FFmpeg", "cve", "out_of_bounds", "avfilter vf_bwdif 堆缓冲区溢出"),
    # ── 编译器 / 浏览器 / 运行时（C++ 主战场）────────────────────────────
    ("CVE-2021-42574", "LLVM/GCC 生态（Trojan Source）", "cve", "logic_error", "Unicode 双向控制字符在注释/字符串中隐藏恶意代码"),
    ("CVE-2021-30551", "Chromium/V8", "cve", "type_punning", "V8 类型混淆"),
    ("CVE-2020-16040", "Chromium/V8", "cve", "type_punning", "V8 类型混淆致越界访问"),
    ("CVE-2021-21224", "Chromium/V8", "cve", "type_punning", "Pwn2Own 2021：V8 类型混淆"),
    ("CVE-2021-37975", "Chromium", "cve", "use_after_free", "V8 释放后使用"),
    ("CVE-2019-5786", "Chromium", "cve", "use_after_free", "FileReader 释放后使用（在野利用）"),
    ("CVE-2021-30663", "WebKit", "cve", "integer_overflow", "WebKit 整数溢出"),
    ("CVE-2020-26969", "Firefox", "cve", "out_of_bounds", "WebRender 内存破坏"),
    ("CVE-2022-31747", "Firefox", "cve", "use_after_free", "WebRTC 释放后使用"),
    # ── 数据库 ──────────────────────────────────────────────────────────
    ("CVE-2022-35737", "SQLite", "cve", "integer_overflow", "printf %lld 整数溢出致崩溃/越界"),
    ("CVE-2020-15358", "SQLite", "cve", "out_of_bounds", "multiSelectOrderBy 堆缓冲区溢出"),
    ("CVE-2019-13750", "SQLite（Chromium 内置）", "cve", "out_of_bounds", "fts3 片段边界校验缺失"),
    ("CVE-2022-1552", "PostgreSQL", "cve", "logic_error", "autovacuum 权限提升"),
    ("CVE-2023-5868", "PostgreSQL", "cve", "memory_leak", "ECDSA 签名计算内存泄露"),
    ("CVE-2021-41099", "Redis", "cve", "integer_overflow", "proto-max-bulk-len 整数溢出"),
    # ── C++ 库 / 框架 ───────────────────────────────────────────────────
    ("CVE-2021-22570", "protobuf", "cve", "null_pointer_deref", "解析器 NULL 指针解引用"),
    ("CVE-2022-1941", "protobuf", "cve", "logic_error", "解析器超长消息 DoS"),
    ("CVE-2021-22569", "protobuf", "cve", "logic_error", "解析歧义 DoS"),
    ("CVE-2012-2677", "Boost", "cve", "integer_overflow", "pool 分配器整数溢出"),
    ("CVE-2023-34410", "Qt", "cve", "logic_error", "TLS 证书验证策略绕过"),
    ("CVE-2021-38593", "Qt", "cve", "integer_overflow", "图像处理整数溢出"),
    ("CVE-2023-32762", "Qt", "cve", "logic_error", "HTTP/2 帧处理 DoS"),
    ("CVE-2022-3432", "Godot Engine", "cve", "use_after_free", "编辑器/运行时释放后使用"),
    # ── 内核 / 系统（PoC 以 C++ 重构）────────────────────────────────────
    ("CVE-2022-0847", "Linux kernel", "cve", "logic_error", "Dirty Pipe：管道缓冲标志未初始化致页面缓存写"),
    ("CVE-2016-5195", "Linux kernel", "cve", "data_race", "Dirty COW：COW 竞态"),
    ("CVE-2022-0185", "Linux kernel", "cve", "out_of_bounds", "fs_context 堆缓冲区溢出"),
    ("CVE-2024-1086", "Linux kernel", "cve", "use_after_free", "nf_tables 释放后使用（在野利用）"),
    ("CVE-2021-33909", "Linux kernel", "cve", "integer_overflow", "Sequoia：size_t 下溢致越界写"),
    ("CVE-2021-3156", "sudo", "cve", "out_of_bounds", "Baron Samedit：参数解析堆缓冲区溢出"),
    ("CVE-2019-18634", "sudo", "cve", "out_of_bounds", "pwfeedback 栈缓冲区溢出"),
    ("CVE-2021-4034", "polkit", "cve", "out_of_bounds", "PwnKit：argv 越界写"),
    ("CVE-2024-2961", "glibc", "cve", "out_of_bounds", "iconv ISO-2022-CN-EXT 越界写（PHP 利用链）"),
    # ── FreeBSD ─────────────────────────────────────────────────────────
    ("CVE-2019-5596", "FreeBSD", "cve", "logic_error", "capsicum 文件描述符泄露"),
    ("CVE-2020-7457", "FreeBSD", "cve", "logic_error", "TCP 连接状态处理缺陷"),
    ("CVE-2021-29628", "FreeBSD", "cve", "logic_error", "ktls 信息泄露"),
    # ── Pwn / 竞赛场景（真实可利用；PoC 可独立编译）──────────────────────
    ("CVE-2017-16995", "Linux kernel", "pwn", "integer_overflow", "eBPF 签名/边界检查整数溢出（CTF 常考）"),
    ("CVE-2019-13272", "Linux kernel", "pwn", "logic_error", "PTRACE_TRACEME 权限提升"),
    ("CVE-2021-3490", "Linux kernel", "pwn", "integer_overflow", "eBPF ALU32 边界跟踪缺陷"),
    ("CVE-2016-8655", "Linux kernel", "pwn", "data_race", "AF_PACKET 竞态 UAF"),
    ("CVE-2021-26708", "Linux kernel", "pwn", "data_race", "vsock 竞态（Virtio）"),
    # ── 补充（2022-2024 C++ 生态）───────────────────────────────────────
    ("CVE-2023-29491", "ncurses", "cve", "out_of_bounds", "terminfo 环境变量堆溢出"),
    ("CVE-2022-26691", "CUPS", "cve", "logic_error", "认证绕过"),
    ("CVE-2022-1271", "XZ Utils", "cve", "out_of_bounds", "任意文件写（多目标命令）"),
    ("CVE-2022-40674", "expat", "cve", "use_after_free", "doContent 释放后使用"),
    ("CVE-2021-45960", "expat", "cve", "integer_overflow", "storeAtts 再分配整数溢出"),
    ("CVE-2021-45943", "expat", "cve", "null_pointer_deref", "XML_GetBuffer NULL 解引用"),
    ("CVE-2021-46143", "expat", "cve", "integer_overflow", "doProlog 整数溢出"),
    ("CVE-2016-8618", "curl", "cve", "double_free", "curl_maprintf 双重释放"),
    ("CVE-2017-1000257", "curl", "cve", "out_of_bounds", "FTP 通配符堆溢出"),
    ("CVE-2022-32208", "curl", "cve", "logic_error", "FTP PASV 响应混淆"),
    ("CVE-2023-27534", "curl", "cve", "logic_error", "SFTP 路径穿越"),
    ("CVE-2023-27536", "curl", "cve", "logic_error", "GSSAPI 凭据复用"),
    ("CVE-2018-1000005", "curl", "cve", "out_of_bounds", "FTP 路径堆溢出"),
    ("CVE-2019-5482", "curl", "cve", "out_of_bounds", "TFTP 堆缓冲区溢出"),
    ("CVE-2020-8231", "curl", "cve", "use_after_free", "连接复用释放后使用"),
    ("CVE-2021-22946", "curl", "cve", "logic_error", "协议降级绕过"),
    ("CVE-2020-8177", "curl", "cve", "logic_error", "-J 与 -i 组合覆盖本地文件"),
    ("CVE-2018-0500", "curl", "cve", "out_of_bounds", "SMTP 堆越界写"),
    ("CVE-2020-11022", "jQuery", "cve", "logic_error", "XSS（前端生态对照项）"),
    ("CVE-2014-0160", "OpenSSL", "pwn", "out_of_bounds", "Heartbleed 在 CTF 靶场中的经典越界读利用"),
    ("CVE-2021-3156", "sudo", "pwn", "out_of_bounds", "Baron Samedit 在 CTF 权限提升题的经典原型"),
    # ── 683 补充（RW-107/108/109/110 用；写 PoC 时新引入，回填候选清单）─────
    ("CVE-2023-44487", "HTTP/2 协议栈", "cve", "logic_error", "HTTP/2 Rapid Reset 协议级 DoS（RST_STREAM 重置循环）"),
    ("CVE-2015-0235", "glibc", "cve", "out_of_bounds", "GHOST：gethostbyname 超长主机名整数长度截断致堆溢出"),
    ("CVE-2018-10933", "libssh", "cve", "logic_error", "认证状态机缺陷：伪造 USERAUTH_SUCCESS 绕过认证"),
    ("CVE-2016-0778", "OpenSSH", "cve", "out_of_bounds", "roaming 客户端堆缓冲区溢出"),
]

#: NVD 有记录但后续以 GitHub Security Advisory 为主要来源的判定规则
GHSA_SOURCE = "security-advisories@github.com"


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _fetch_nvd(cve: str, timeout: int = 40) -> dict:
    req = urllib.request.Request(NVD_API + cve, headers={
        "User-Agent": "queyi-683-realworld-collector/1.0 (research; contact 1026708211@qq.com)",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"http_status": r.status, "body": json.loads(r.read().decode("utf-8", "replace"))}
    except urllib.error.HTTPError as e:
        return {"http_status": e.code, "error": f"HTTPError: {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"http_status": None, "error": f"{type(e).__name__}: {e}"}


def _extract(body: dict) -> dict:
    """从 NVD 应答中抽取客观字段（原文照录，不做转述）。"""
    vulns = body.get("vulnerabilities") or []
    if not vulns:
        return {"found": False}
    cve = vulns[0]["cve"]
    desc_en = next((d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"), "")
    cvss = None
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        m = (cve.get("metrics") or {}).get(key)
        if m:
            d = m[0]["cvssData"]
            cvss = {"version": d.get("version"), "baseScore": d.get("baseScore"),
                    "baseSeverity": d.get("baseSeverity") or m[0].get("baseSeverity"),
                    "vectorString": d.get("vectorString")}
            break
    refs = []
    for r in cve.get("references", []):
        refs.append({"url": r.get("url"), "source": r.get("source"), "tags": r.get("tags", [])})
    return {
        "found": True,
        "cve_id": cve.get("id"),
        "published": cve.get("published"),
        "last_modified": cve.get("lastModified"),
        "vuln_status": cve.get("vulnStatus"),
        "source_identifier": cve.get("sourceIdentifier"),
        "description_en": desc_en,
        "cvss": cvss,
        "references": refs,
        "n_references": len(refs),
    }


def stage_verify(resume: bool = True) -> int:
    doc = {"schema": "queyi-683-realworld-candidates/v1", "generated_at": _now(),
           "source": "NVD API v2.0 (services.nvd.nist.gov/rest/json/cves/2.0)", "items": []}
    done: dict[str, dict] = {}
    if resume and OUT.is_file():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        done = {it["cve"]: it for it in old.get("items", [])}
        print(f"[683-A1] 断点续跑：已有 {len(done)} 条结果")

    uniq: dict[str, list[tuple[str, str, str, str]]] = {}
    for cve, proj, stype, dtype, mech in CANDIDATES:
        uniq.setdefault(cve, []).append((proj, stype, dtype, mech))

    for i, (cve, entries) in enumerate(uniq.items(), 1):
        if cve in done and done[cve].get("nvd", {}).get("found") is not None:
            continue
        t0 = time.time()
        raw = _fetch_nvd(cve)
        nvd = _extract(raw.get("body") or {}) if raw.get("body") else {"found": None,
                                                                       "error": raw.get("error")}
        item = {"cve": cve,
                "projects": sorted({e[0] for e in entries}),
                "source_types": sorted({e[1] for e in entries}),
                "defect_type_guess": entries[0][2],
                "mechanism_guess": entries[0][3],
                "nvd": nvd,
                "http_status": raw.get("http_status"),
                "checked_at": _now()}
        done[cve] = item
        doc["items"] = [done[k] for k in sorted(done)]
        doc["generated_at"] = _now()
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        st = "FOUND" if nvd.get("found") else ("HTTP %s" % raw.get("http_status"))
        print(f"[683-A1] {i}/{len(uniq)} {cve:<18} {st}  ({time.time()-t0:.1f}s)", flush=True)
        if i < len(uniq):
            time.sleep(RATE_S)
    print(f"[683-A1] 完成：{OUT.relative_to(ROOT).as_posix()}")
    return 0


def stage_report() -> int:
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    items = doc["items"]
    found = [it for it in items if it["nvd"].get("found")]
    miss = [it for it in items if not it["nvd"].get("found")]
    ghsa = [it for it in found if it["nvd"].get("source_identifier") == GHSA_SOURCE]
    print(f"候选 {len(items)} 条：NVD 在线确认 {len(found)}，未确认 {len(miss)}")
    print(f"其中 source=GitHub Security Advisory 的 {len(ghsa)} 条")
    for it in miss:
        print(f"  NOT FOUND: {it['cve']} (http={it['http_status']}) {it['mechanism_guess'][:50]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("verify", "report"), required=True)
    a = ap.parse_args()
    return {"verify": stage_verify, "report": stage_report}[a.stage]()


if __name__ == "__main__":
    sys.exit(main())
