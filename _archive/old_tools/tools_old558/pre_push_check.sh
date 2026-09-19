#!/usr/bin/env bash
# pre_push_check.sh — 一键 CI 预检（推送前必跑）
# 已升级为 tools/cppbible.py preflight 的薄包装，保留本脚本作为兼容入口。
# 用法: bash tools/pre_push_check.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# POSIX 路径（/c/...）传给 Windows 原生 python.exe 会被误读为 C:\c\...，
# 必须用 cygpath 转成 Windows 原生路径（C:\...）再交给 python。
ROOT_WIN="$(cygpath -w "$ROOT" 2>/dev/null || echo "$ROOT")"
PYTHON="C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  预推送检查  (pre_push_check → cppbible preflight)  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

exec "$PYTHON" "$ROOT_WIN/tools/cppbible.py" preflight
