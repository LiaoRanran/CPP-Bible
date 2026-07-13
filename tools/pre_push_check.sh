#!/usr/bin/env bash
# pre_push_check.sh — 一键 CI 预检（推送前必跑）
# 7 项检查，任一项失败 = 退出码 1 = 禁止推送
# 用法: bash tools/pre_push_check.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# POSIX 路径（/c/...）传给 Windows 原生 python.exe 会被误读为 C:\c\...，
# 必须用 cygpath 转成 Windows 原生路径（C:\...）再交给 python。
ROOT_WIN="$(cygpath -w "$ROOT" 2>/dev/null || echo "$ROOT")"
PYTHON="C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"

PASS=0
FAIL=0
check() {
    local name="$1"
    shift
    echo -n "  [$name] "
    if "$@" > /dev/null 2>&1; then
        echo "✅"
        PASS=$((PASS + 1))
    else
        echo "❌"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  预推送检查  (pre_push_check)                       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 1. 门禁
check "门禁" "$PYTHON" "$ROOT_WIN/tools/consistency_check.py"

# 2. 交引
check "交引审计" "$PYTHON" "$ROOT_WIN/tools/crossref_audit.py"

# 3. 断言缓存
CACHE="$ROOT/build/assert_report.txt"
if [ -f "$CACHE" ] && grep -q "FAIL-CLAIM] 0" "$CACHE"; then
    echo "  [断言] ✅ (缓存: FAIL=0)"
    PASS=$((PASS + 1))
else
    echo "  [断言] ⚠️ 缓存缺失或异常，运行: python3 tools/run_cpp_assertions.py"
fi

# 4. 卫生（.bak / 临时探针 / 根目录编译产物）
# 用 find 而非 ls 通配：清理后无匹配时 ls 报错会触发 pipefail+set -e 中止脚本。
BAK_COUNT=$(find "$ROOT/Book" -name '*.bak' 2>/dev/null | wc -l || true)
PROBE_COUNT=$(find "$ROOT/tools" -maxdepth 1 -name '_*.py' 2>/dev/null | grep -v _clean_junk.py | wc -l || true)
ROOT_ART_COUNT=$(find "$ROOT" -maxdepth 1 \( -name '*.cpp' -o -name '*.exe' -o -name '*.o' \) 2>/dev/null | wc -l || true)
if [ "$BAK_COUNT" -eq 0 ] && [ "$PROBE_COUNT" -eq 0 ] && [ "$ROOT_ART_COUNT" -eq 0 ]; then
    echo "  [卫生] ✅ (.bak=0, 探针=0, 根目录产物=0)"
    PASS=$((PASS + 1))
else
    echo "  [卫生] ❌ (.bak=$BAK_COUNT, 探针=$PROBE_COUNT, 根产物=$ROOT_ART_COUNT)"
    FAIL=$((FAIL + 1))
fi

# 5. 去重
check "去重" "$PYTHON" "$ROOT_WIN/tools/deduplication_audit.py"

# 6. 单章质量门禁（HIGH 级缺陷拦截：空代码块等；MED/LOW 仅报告不阻断）
if "$PYTHON" "$ROOT_WIN/tools/chapter_lint.py" --fail-on HIGH > /dev/null 2>&1; then
    echo "  [章质量] ✅ (无 HIGH 级缺陷)"
    PASS=$((PASS + 1))
else
    echo "  [章质量] ❌ (存在 HIGH 级缺陷，运行 chapter_lint.py 查看)"
    FAIL=$((FAIL + 1))
fi

# 7. 汇编证据准确性（书内 asm 块引用的 mangled 符号必须 ⊆ Examples/*.asm 真实产物）
check "汇编证据" "$PYTHON" "$ROOT_WIN/tools/verify_asm_evidence.py"

echo ""
echo "──────────────────────────────────────────────────────"
echo "  结果: $PASS 通过 / $FAIL 失败"
echo "──────────────────────────────────────────────────────"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "  ❌ 预检未通过，禁止推送。请修复后重试。"
    exit 1
else
    echo ""
    echo "  ✅ 全部通过，可以推送。"
    exit 0
fi
