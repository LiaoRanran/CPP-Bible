#!/bin/sh
# _ch148_sparse_checkout.sh —— 大型仓库稀疏检出：只拉取需要的目录
# 适用：monorepo / 单仓多模块，避免全量检出数 GB 源码。
set -e

REPO_URL="$1"
DIR="$2"
SUBDIR="$3"   # 例如 src/engine

git clone --filter=blob:none --no-checkout "$REPO_URL" "$DIR"
cd "$DIR"
git sparse-checkout init --cone
git sparse-checkout set "$SUBDIR"
git checkout
echo "稀疏检出完成，仅工作树含: $SUBDIR"
