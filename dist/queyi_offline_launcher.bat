@echo off
chcp 65001 >nul
cd /d "%~dp0.."
title 阙疑 QueYi Protocol — 离线桌面启动器（617 G1）
echo ============================================================
echo   阙疑 QueYi Protocol — 离线桌面启动器
echo   仓库已自包含（git 克隆即离线），本启动器做轻量度量自检
echo ============================================================
echo.
echo [1/2] 度量自检（SNAPSHOT_MANIFEST，只读，不跑全量 --check）...
echo ------------------------------------------------------------
python tools\snapshot_manifest.py
echo ------------------------------------------------------------
echo.
echo [2/2] 项目说明（README.md 头部）...
echo ------------------------------------------------------------
if exist README.md (
  powershell -Command "Get-Content README.md -TotalCount 30 -Encoding UTF8"
) else (
  echo README.md 未找到
)
echo ------------------------------------------------------------
echo.
echo 提示：完整验证请按 README.md 中的门禁命令手动运行（本启动器不自动跑
echo       全量 --check，以免长时占用；离线即可复算上表计数）。
echo.
pause
