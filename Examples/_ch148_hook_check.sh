#!/bin/sh
# _ch148_hook_check.sh —— 可直接用作 .git/hooks/pre-commit 的钩子
# 职责：对本提交暂存区中的 .cpp/.h 文件运行 C++ 代码风格检查器。
set -e

# 1) 取出本次暂存的全部源码
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(cpp|h|hpp|cc)$' || true)
[ -z "$FILES" ] && exit 0

# 2) 调用 C++ 检查器（见 _ch148_precommit_lint.cpp）
if command -v _ch148_precommit_lint >/dev/null 2>&1; then
    if ! _ch148_precommit_lint $FILES; then
        echo "pre-commit: 代码风格检查未通过，提交被拒绝。" >&2
        exit 1
    fi
fi

# 3) 确保 clang-format 已应用（可选）
if command -v clang-format >/dev/null 2>&1; then
    for f in $FILES; do
        if ! clang-format --dry-run --Werror "$f" >/dev/null 2>&1; then
            echo "pre-commit: $f 未通过 clang-format，请先格式化。" >&2
            exit 1
        fi
    done
fi
exit 0
