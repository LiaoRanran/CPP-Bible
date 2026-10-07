<#
  build.ps1 — 一键编译 + 论文质量门禁（670c2 B6）
  用法：
      pwsh -File research/latex/build.ps1
      # 或指定引擎：
      $env:TECTONIC = "C:\path\to\tectonic.exe"; pwsh -File research/latex/build.ps1

  流程：tectonic 编译（含 BibTeX 通过）→ 报告页数 → 跑 5 项检查
        （paper_sync / bib_audit / figure_data / anonymity / paper_quality_gate）
  任一检查失败 ⇒ 退出码 1。
#>
$ErrorActionPreference = "Stop"

$Here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root   = Resolve-Path (Join-Path $Here "..\..")
$Tex    = Join-Path $Here "queyi_neurips2027_v1.1.tex"

# 1. 定位 tectonic
$Tectonic = $env:TECTONIC
if (-not $Tectonic) {
    $cmd = Get-Command tectonic -ErrorAction SilentlyContinue
    if ($cmd) { $Tectonic = $cmd.Source }
}
if (-not $Tectonic) {
    Write-Host "[build] 未找到 tectonic。请安装 tectonic 或设置 `$env:TECTONIC 指向 tectonic.exe" -ForegroundColor Red
    exit 2
}
Write-Host "[build] 引擎: $Tectonic"

# 2. 编译（保留 aux/log 供质量门禁读取）
Push-Location $Here
try {
    & $Tectonic --keep-logs --keep-intermediates $Tex
    if ($LASTEXITCODE -ne 0) { Write-Host "[build] 编译失败" -ForegroundColor Red; exit 1 }
} finally {
    Pop-Location
}

# 3. 页数报告
$Log = Join-Path $Here "queyi_neurips2027_v1.1.log"
if (Test-Path $Log) {
    $m = Select-String -Path $Log -Pattern "Output written on .*\((\d+) pages" | Select-Object -First 1
    if ($m) { Write-Host "[build] 总页数: $($m.Matches[0].Groups[1].Value)" }
}

# 4. 五项检查
$Py = "python"
$Checks = @(
    "tools/paper_sync_check_670c2.py",
    "tools/bib_audit_670c2.py",
    "tools/figure_data_check_670c2.py",
    "tools/anonymity_check_670c2.py",
    "tools/paper_quality_gate_670c2.py"
)
$Fail = 0
foreach ($c in $Checks) {
    Write-Host "`n[build] ---- $c ----"
    & $Py (Join-Path $Root $c)
    if ($LASTEXITCODE -ne 0) { $Fail++ }
}

if ($Fail -gt 0) {
    Write-Host "`n[build] 有 $Fail 项检查失败" -ForegroundColor Red
    exit 1
}
Write-Host "`n[build] 全部通过 ✅" -ForegroundColor Green
exit 0
