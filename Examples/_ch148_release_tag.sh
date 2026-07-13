#!/bin/sh
# _ch148_release_tag.sh —— 创建带注释的语义化版本标签并推送
# 用法：./_ch148_release_tag.sh 2.4.1 "修复调度器空指针"
set -e

VERSION="$1"
MESSAGE="$2"

case "$VERSION" in
  [0-9].[0-9].[0-9]) ;;
  *) echo "版本号必须为 X.Y.Z 形式" >&2; exit 1;;
esac

TAG="v$VERSION"
git tag -a "$TAG" -m "Release $TAG: $MESSAGE"
git push origin "$TAG"
echo "已推送标签 $TAG"
