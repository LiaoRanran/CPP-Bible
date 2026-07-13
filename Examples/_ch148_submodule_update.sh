#!/bin/sh
# _ch148_submodule_update.sh —— 递归初始化并更新全部子模块到远程最新
# 适用：CI 拉取带 submodule 的仓库，或新成员首次克隆。
set -e

git submodule sync --recursive
git submodule update --init --recursive --remote
git submodule status --recursive
