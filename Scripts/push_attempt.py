#!/usr/bin/env python3
"""一键推送尝试 + 网络诊断。

本环境已知问题：SSH 认证通（ssh -T）但 git-receive-pack 数据通道在 22/443
均被远端关闭（exit 141），HTTPS 的 github.com/codeload 被墙。本脚本封装诊断，
不盲目重试。

用法：
    python scripts/push_attempt.py            # 只检查 + 诊断（默认 dry-run，不推）
    python scripts/push_attempt.py --push     # 真的尝试 git push
    python scripts/push_attempt.py --json

退出码：push 成功=0；dry-run 或失败=1（方便 CI 判断）。
"""
from __future__ import annotations
import argparse
import json
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], timeout: int = 30) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
        )
        return p.returncode, ((p.stdout or "") + (p.stderr or "")).strip()
    except subprocess.TimeoutExpired:
        return 124, "[TIMEOUT]"
    except FileNotFoundError as e:
        return 127, f"[NOT FOUND] {e}"


def port_open(host: str, port: int, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true", help="真的执行 git push（默认只诊断）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    diag: dict = {}

    # 1. 基本信息
    diag["branch"] = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])[1]
    diag["ahead"] = int(run(["git", "rev-list", "--count", "origin/master..HEAD"])[1] or 0)
    diag["remote_url"] = run(["git", "remote", "get-url", "origin"])[1]

    # 2. 端口连通性
    diag["port_22"] = port_open("github.com", 22)
    diag["port_443"] = port_open("github.com", 443)
    diag["api_443"] = port_open("api.github.com", 443)

    # 3. SSH 认证（如果 remote 是 SSH）
    if "git@github.com" in diag["remote_url"]:
        rc, out = run(["ssh", "-T", "-o", "StrictHostKeyChecking=no",
                       "-o", "ConnectTimeout=5", "git@github.com"], timeout=10)
        # ssh -T 成功时 exit 1（"Hi user! You've successfully authenticated"）
        diag["ssh_auth_ok"] = ("successfully authenticated" in out) or (rc == 1 and "Hi" in out)
        diag["ssh_auth_output"] = out[:200]
    else:
        diag["ssh_auth_ok"] = None

    # 4. 尝试 push
    if args.push:
        if diag["ahead"] == 0:
            diag["push_result"] = "nothing_to_push"
        else:
            rc, out = run(["git", "push"], timeout=30)
            diag["push_rc"] = rc
            diag["push_output"] = out[:500]
            diag["push_result"] = "success" if rc == 0 else "failed"
            if rc != 0:
                # 诊断失败原因
                if "exit 141" in out or "141" in out:
                    diag["push_diagnosis"] = "SSH 数据通道被远端关闭（exit 141）——需换可连通网络"
                elif "Connection refused" in out or "timed out" in out:
                    diag["push_diagnosis"] = "网络不可达——检查代理/防火墙"
                elif "Permission denied" in out:
                    diag["push_diagnosis"] = "SSH 密钥未授权——检查 ssh key"
                else:
                    diag["push_diagnosis"] = "未知失败，见 push_output"
    else:
        diag["push_result"] = "dry_run (use --push to actually push)"

    if args.json:
        print(json.dumps(diag, ensure_ascii=False, indent=2))
    else:
        print(f"{'='*60}")
        print(f"  推送诊断")
        print(f"{'='*60}")
        print(f"  分支     : {diag['branch']}")
        print(f"  未推送   : {diag['ahead']} 条")
        print(f"  remote   : {diag['remote_url']}")
        print(f"{'─'*60}")
        print(f"  端口连通 :")
        print(f"    github.com:22   {'✅' if diag['port_22'] else '❌'}")
        print(f"    github.com:443  {'✅' if diag['port_443'] else '❌'}")
        print(f"    api.github.com:443 {'✅' if diag['api_443'] else '❌'}")
        if diag["ssh_auth_ok"] is not None:
            print(f"  SSH 认证 : {'✅' if diag['ssh_auth_ok'] else '❌'}")
        print(f"{'─'*60}")
        print(f"  推送结果 : {diag['push_result']}")
        if "push_diagnosis" in diag:
            print(f"  诊断     : {diag['push_diagnosis']}")
        if not args.push and diag["ahead"] > 0:
            print(f"  提示     : 加 --push 真的尝试推送（当前为 dry-run）")
        print(f"{'='*60}")

    if args.push:
        return 0 if diag.get("push_result") == "success" else 1
    return 0 if diag["ahead"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
