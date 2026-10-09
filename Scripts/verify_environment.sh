#!/usr/bin/env bash
# =====================================================================
# 693-B2 · Scripts/verify_environment.sh — 环境体检
#
# 目的：在跑任何复现之前，先确认**本机/容器内的工具版本**与论文声明一致。
# 设计原则（fail-loud）：版本不符就退出非 0，**不做静默降级**。
#
# 用法：
#   bash Scripts/verify_environment.sh              # 严格档：任何不符 → 退出 1
#   bash Scripts/verify_environment.sh --report     # 报告档：只报告，永不因不符退出
#   bash Scripts/verify_environment.sh --profile wsl  # 指定环境画像
#
# 环境画像（与 data/692_environment_paired_experiment.json 对齐）：
#   * wsl-gcc-13.3        → Ubuntu 24.04.4 LTS (WSL2), g++ 13.3.0
#   * windows-native-mingw → Windows 11, MinGW g++ 13.1.0 + clang 22.1.8
#   * docker-ubuntu-22.04  → 693-B1 镜像, gcc/g++ 12.3.0 + clang 14（**未实测构建**）
# =====================================================================
set -uo pipefail

MODE="strict"
PROFILE="auto"
for arg in "$@"; do
  case "$arg" in
    --report) MODE="report" ;;
    --profile=*) PROFILE="${arg#--profile=}" ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "[verify_env] 未知参数: $arg" >&2; exit 2 ;;
  esac
done

PASS=0; FAIL=0; WARN=0; ACQ_GAP=0   # ACQ_GAP=1 表示检测到「获取层能力缺口」（698-B T6，707-C）
note()  { echo "[verify_env] $*"; }
ok()    { echo "  OK   $*"; PASS=$((PASS+1)); }
bad()   { echo "  FAIL $*"; FAIL=$((FAIL+1)); }
warn()  { echo "  WARN $*"; WARN=$((WARN+1)); }

# check <label> <actual> <expected> <required? yes|no>
check() {
  local label="$1" actual="$2" expected="$3" required="${4:-yes}"
  if [ -z "$actual" ]; then
    if [ "$required" = "yes" ]; then bad "$label: MISSING (expected $expected)"
    else warn "$label: MISSING (optional)"; fi
    return
  fi
  if [ "$actual" = "$expected" ]; then ok "$label = $actual"
  else
    if [ "$required" = "yes" ]; then bad "$label = $actual, expected $expected"
    else warn "$label = $actual, expected $expected (optional)"; fi
  fi
}

# ver <cmd> → 取版本号第一行；取不到返回空
ver() { "$@" 2>/dev/null | head -1 || true; }

echo "=============================================="
echo " 693-B2 · 环境体检（mode=$MODE, profile=$PROFILE）"
echo "=============================================="

echo "-- OS / 内核 --"
note "OS: $(uname -s 2>/dev/null) $(uname -r 2>/dev/null)"
if [ -f /etc/os-release ]; then
  note "Distro: $(. /etc/os-release && echo "${PRETTY_NAME:-unknown}")"
fi

echo "-- 编译器 --"
GXX_VER="$(ver g++ --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
GCC_VER="$(ver gcc --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
CLANG_VER="$(ver clang --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"

case "$PROFILE" in
  wsl-gcc-13.3)          check "g++"    "$GXX_VER"   "13.3.0" yes ;;
  windows-native-mingw)  check "g++"    "$GXX_VER"   "13.1.0" yes
                         check "clang"  "$CLANG_VER" "22.1.8" yes ;;
  docker-ubuntu-22.04)   check "g++"    "$GXX_VER"   "12.3.0" yes
                         check "gcc"    "$GCC_VER"   "12.3.0" yes
                         check "clang"  "$CLANG_VER" "14.0.0" yes ;;
  auto)                  note "g++ = ${GXX_VER:-MISSING}（auto 档不比对，只登记）"
                         note "clang = ${CLANG_VER:-MISSING}" ;;
esac

echo "-- 分析器（692-D 公平对比用；缺失只警告，不阻断）--"
CPPCHECK_VER="$(ver cppcheck --version | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)"
# clang-tidy 的版本号在第 2 行（第 1 行是 "LLVM (http://llvm.org):"），故不 head -1
CLANG_TIDY_VER="$(clang-tidy --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
VALGRIND_VER="$(ver valgrind --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
check "cppcheck"   "$CPPCHECK_VER"   "2.21.0" no
check "clang-tidy" "$CLANG_TIDY_VER" "22.1.8" no
check "valgrind"   "$VALGRIND_VER"   "3.18.1" no

echo "-- 构建系统 --"
CMAKE_VER="$(ver cmake --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
check "cmake" "$CMAKE_VER" "3.22.1" no

echo "-- Python --"
PY_VER="$(python3 --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || \
          python --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
note "python = ${PY_VER:-MISSING}"
case "$PY_VER" in
  3.13.*) ok "python 主版本 3.13（产物生成环境口径）" ;;
  3.10.*) ok "python 主版本 3.10（容器口径）" ;;
  "")     bad "python: MISSING" ;;
  *)      warn "python $PY_VER 既非 3.13.x（产物环境）亦非 3.10.x（容器环境），请自行确认" ;;
esac

echo "-- sanitizer 运行时（决定性：没有它 asan/ubsan/tsan 全是假 miss）--"
TMPD="$(mktemp -d 2>/dev/null || echo /tmp/queyi_env_probe)"
trap 'rm -rf "$TMPD"' EXIT
printf 'int main(){return 0;}\n' > "$TMPD/p.c"
CXX_BIN="$(command -v g++ || command -v g++-12 || command -v g++-13 || true)"
if [ -n "$CXX_BIN" ]; then
  for san in address undefined thread; do
    if "$CXX_BIN" -fsanitize="$san" "$TMPD/p.c" -o "$TMPD/p.$san" >/dev/null 2>&1 \
       && "$TMPD/p.$san" >/dev/null 2>&1; then
      ok "-fsanitize=$san 编译+运行通过"
    elif [ "$PROFILE" = "wsl-gcc-13.3" ] || [ "$PROFILE" = "docker-ubuntu-22.04" ]; then
      # 画像明确声称支持 sanitizer 却不可用 ⇒ 真 FAIL
      bad "-fsanitize=$san 不可用，但画像 $PROFILE 声明支持该资产 ⇒ 该资产会系统性假 miss"
      ACQ_GAP=1
    else
      # Windows native (MinGW) 无 sanitizer 运行时是**已知预期**（689/692 已实测登记），
      # 不是环境配置错误 ⇒ 警告而非失败。
      warn "-fsanitize=$san 在当前画像下不可用（MinGW 无 sanitizer 运行时，属已知预期）；"
      warn "    ⇒ asan/ubsan/tsan 必须在 WSL(13.3.0) 或容器内跑，否则系统性假 miss"
      ACQ_GAP=1
    fi
  done
else
  bad "g++: MISSING ⇒ 无法检测 sanitizer 运行时"
fi

echo "-- 已知坑位自检 --"
# 坑 1：MinGW g++ 不认 -Wunsequenced（673u 判据）
if [ -n "$CXX_BIN" ]; then
  if "$CXX_BIN" -Wunsequenced -fsyntax-only "$TMPD/p.c" >/dev/null 2>&1; then
    ok "-Wunsequenced 被接受（clang 系或支持该选项的 gcc）"
  else
    warn "-Wunsequenced 不被接受 ⇒ 该资产恒 unknown（673u 已登记的 MinGW 坑，属预期）"
    ACQ_GAP=1
  fi
fi
# 坑 2：WSL UTF-16LE 横幅（本机测量环境的已知坑；容器内不适用）
if command -v wsl.exe >/dev/null 2>&1 || command -v wsl >/dev/null 2>&1; then
  warn "检测到 WSL：调用 wsl.exe 时必须 export WSL_UTF8=1 + WSLENV=WSL_UTF8/u，"
  warn "            否则 stderr 解码失败会让 ASan/UBSan 报告全丢（系统性假 miss）。"
else
  ok "未检测到 WSL（容器内预期如此）"
fi

# ── 707-C / 698-B 定理 T6：可纠错边界警告 ──────────────────────────────
# 科研依据（698-B 定理 T6）：可纠正 ⟺ 漂移只作用于后处理层；**获取层漂移必须重测**。
# 当本环境缺失某个**环境门控**资产（asan/ubsan/tsan 等）时，该缺口属获取层 ——
# 原始矩阵里根本没有这次测量 ⇒ 事后校正不可靠（实测残留误差 asan 30.04% / ubsan 21.38%
# / tsan 21.73%）⇒ **必须重测**，不要靠事后校正。检查器：tools/check_drift_correctability.py
echo "-- 707-C / 698-B T6：可纠错边界 --"
if [ "$ACQ_GAP" -gt 0 ]; then
  warn "检测到【获取层能力缺口】：缺失资产/工具 ⇒ 按 698-B 定理 T6，此漂移【不可事后纠正】，"
  warn "     必须【重测】（re-measure），不要靠事后校正；详见 tools/check_drift_correctability.py"
else
  ok "未检测到获取层能力缺口（按 T6 无需强制重测）"
fi

echo "=============================================="
echo " 结果：OK=$PASS  FAIL=$FAIL  WARN=$WARN  (mode=$MODE)"
echo "=============================================="

if [ "$MODE" = "strict" ] && [ "$FAIL" -gt 0 ]; then
  echo "[verify_env] 严格档：存在 FAIL ⇒ 退出 1。改用 --report 可只报告不阻断。"
  exit 1
fi
exit 0
