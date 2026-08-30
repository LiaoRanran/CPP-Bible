# CPP-Bible 开发环境 bootstrap（Windows）
#
# 目标：新克隆仓库后一键就绪 —— 探测工具链 -> 创建 venv -> 安装锁定依赖 -> 全量门禁自检。
# 对应文档：UPGRADE_PLAN_2026-08-30.md §1.5
# 用法：powershell -ExecutionPolicy Bypass -File tools/bootstrap.ps1
param(
    [switch]$SkipInstall,   # 跳过依赖安装（仅探测 + 自检）
    [switch]$SkipGates      # 跳过全量门禁自检
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
Write-Host "[bootstrap] CPP-Bible 开发环境初始化" -ForegroundColor Cyan

# ---- 1. 工具链探测（唯一事实源：toolchain.toml）----
Write-Host "`n[1/4] 工具链探测" -ForegroundColor Yellow
$python = python --version 2>$null
if ($LASTEXITCODE -eq 0) { Write-Host "  python: $python" } else { Write-Host "  [WARN] python 不在 PATH" }
$gpp = g++ --version 2>$null | Select-Object -First 1
if ($gpp) { Write-Host "  g++: $gpp" } else { Write-Host "  [WARN] g++ 不在 PATH（见 toolchain.toml [compiler] prefer 列表）" }

# ---- 2. Python 虚拟环境 ----
Write-Host "`n[2/4] Python 虚拟环境" -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "  已创建 .venv"
} else {
    Write-Host "  .venv 已存在"
}

# ---- 3. 依赖安装（可选跳过）----
# 优先 uv（推荐，见 UPGRADE_PLAN_2026-08-30.md §1.3）；无 uv 时回退 pip。
if (-not $SkipInstall) {
    Write-Host "`n[3/4] 安装依赖" -ForegroundColor Yellow
    $uvVersion = uv --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  使用 uv: $uvVersion"
        & uv sync --extra dev --extra ci
        if ($LASTEXITCODE -ne 0) { Write-Host "[FAIL] uv sync 失败" -ForegroundColor Red; exit 1 }
    } else {
        Write-Host "  [WARN] 未找到 uv，回退 pip"
        & .\.venv\Scripts\python.exe -m pip install --upgrade pip
        if (Test-Path "requirements.lock.txt") {
            & .\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
        } elseif (Test-Path "pyproject.toml") {
            & .\.venv\Scripts\python.exe -m pip install -e ".[dev,ci]"
        }
    }
} else {
    Write-Host "`n[3/4] 跳过依赖安装（--SkipInstall）"
}

# ---- 4. 工具链自检 + 门禁自检（可选跳过）----
if (-not $SkipGates) {
    Write-Host "`n[4/4] 工具链自检 + 门禁（quality）" -ForegroundColor Yellow
    & .\.venv\Scripts\python.exe tools\cppbible.py env
    if ($LASTEXITCODE -ne 0) { Write-Host "[FAIL] 工具链自检未通过" -ForegroundColor Red; exit 1 }
    & .\.venv\Scripts\python.exe tools\cppbible.py check --stage quality
    if ($LASTEXITCODE -ne 0) { Write-Host "[FAIL] quality 未全绿" -ForegroundColor Red; exit 1 }
}

Write-Host "`n[bootstrap] 完成。开发环境就绪。" -ForegroundColor Green