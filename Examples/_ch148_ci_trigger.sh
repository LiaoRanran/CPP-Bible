#!/bin/sh
# _ch148_ci_trigger.sh —— CI 依据分支/标签决定构建矩阵（预告 ch149 CI/CD）
# 该脚本在流水线中执行，输出本次应跑的构建目标。
set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")
TAG=$(git describe --tags --exact-match 2>/dev/null || echo "")

case "$BRANCH" in
  main)
    echo "target=release-build";;       # 主线：完整构建 + 测试 + 发布产物
  develop)
    echo "target=debug-build+tests";;   # 开发线：调试构建 + 单测
  feature/*)
    echo "target=partial-build+tests";; # 特性分支：增量构建
  *)
    echo "target=default";;
esac

if [ -n "$TAG" ]; then
  echo "release-tag=$TAG"               # 打 tag 触发发布流水线
fi
