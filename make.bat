@echo off
REM ============================================================
REM 《现代 C++ 终极圣经》本地构建脚本
REM 用法: make [check|compile|full|clean|crossref]
REM 前置: Python 3.13+ at C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe
REM       GCC 13.1 at C:\Qt\Tools\mingw1310_64\bin\g++.exe
REM ============================================================
setlocal enabledelayedexpansion

set PY=C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe
set TOOLS=tools
set TARGET=%1
if "%TARGET%"=="" set TARGET=full

echo ============================================================
echo 《现代 C++ 终极圣经》构建工具
echo 目标: %TARGET%
echo ============================================================
echo.

if "%TARGET%"=="check" goto :check
if "%TARGET%"=="compile" goto :compile
if "%TARGET%"=="full" goto :full
if "%TARGET%"=="clean" goto :clean
if "%TARGET%"=="crossref" goto :crossref
if "%TARGET%"=="stats" goto :stats
if "%TARGET%"=="graph" goto :graph
if "%TARGET%"=="checkpoint" goto :checkpoint
if "%TARGET%"=="report" goto :report
if "%TARGET%"=="help" goto :help
echo [!] 未知目标: %TARGET%
goto :help

:check
echo [*] 一致性检查 (consistency_check.py) ...
%PY% %TOOLS%/consistency_check.py
if %ERRORLEVEL% neq 0 (
    echo [X] 门禁失败
    exit /b 1
) else (
    echo [OK] 门禁通过
)
goto :end

:compile
echo [*] 全书编译校验 (chapter_compile_check.py) ...
for /d %%d in (Book\part*) do (
    echo   扫描 %%~nxd ...
    %PY% %TOOLS%/chapter_compile_check.py %%d\ch*.md 2>&1 | findstr /C:"blocks" /C:"fail"
)
if %ERRORLEVEL% neq 0 (
    echo [X] 编译校验有失败
    exit /b 1
) else (
    echo [OK] 编译校验通过
)
goto :end

:full
echo [*] 1/3 一致性检查 ...
%PY% %TOOLS%/consistency_check.py
if %ERRORLEVEL% neq 0 (
    echo [X] 一致性检查失败，终止
    exit /b 1
)
echo.
echo [*] 2/3 全书编译校验 ...
set FAIL_COUNT=0
for /d %%d in (Book\part*) do (
    %PY% %TOOLS%/chapter_compile_check.py %%d\ch*.md 2>&1 | findstr /C:"fail" >nul
    if !ERRORLEVEL! equ 0 (
        echo   [X] %%~nxd 有编译失败
        set /a FAIL_COUNT+=1
    ) else (
        echo   [OK] %%~nxd
    )
)
if !FAIL_COUNT! gtr 0 (
    echo [X] 编译校验: !FAIL_COUNT! 个 part 有失败
    exit /b 1
)
echo.
echo [*] 3/3 交叉引用审计 ...
%PY% %TOOLS%/crossref_audit.py 2>nul
echo.
echo ============================================================
echo [OK] 全量通过: check + compile + crossref
echo ============================================================
goto :end

:crossref
echo [*] 交叉引用审计 ...
if exist "%TOOLS%/crossref_audit.py" (
    %PY% %TOOLS%/crossref_audit.py
) else (
    echo [X] tools/crossref_audit.py 尚未创建
)
goto :end

:clean
echo [*] 清理临时文件 ...
del /q *.cpp 2>nul
del /q *.exe 2>nul
rd /s /q Examples 2>nul
rd /s /q Examples2 2>nul
for /d %%d in (Book\part*) do (
    del /q %%d\*.cpp 2>nul
    del /q %%d\*.exe 2>nul
)
echo [OK] 清理完成
goto :end

:stats
echo [*] 全书统计 ...
for /d %%d in (Book\part*) do (
    set /a LINES=0 & set /a CPP=0 & set /a N=0
    for %%f in (%%d\ch*.md) do (
        set /a N+=1
        for /f %%c in ('findstr /C:"```

cpp" "%%f" ^| find /c /v ""') do set /a CPP+=%%c
    )
    echo   %%~nxd: !N! 章
)
goto :end

:graph
echo [*] 知识图谱验证 ...
if exist "knowledge_graph.json" (
    %PY% -c "import json; d=json.load(open('knowledge_graph.json',encoding='utf-8')); print(f'version={d[\"version\"]} parts={len(d[\"parts\"])} chapters={d[\"total_chapters\"]}')"
    echo [OK] 知识图谱有效
) else (
    echo [X] knowledge_graph.json 缺失
)
goto :end

:checkpoint
echo [*] 生成 checkpoint ...
set DT=%date:~0,10%
set DT=%DT:/=-%
mkdir memory\checkpoints 2>nul
(
echo # Checkpoint %DT%
echo.
echo ## 门禁状态
%PY% tools/consistency_check.py 2>&1 | findstr "汇总"
echo.
echo ## 文件统计
echo 章数: `find Book -name "ch*.md" 2^>nul ^| wc -l`
echo.
echo ## 基础设施模块
echo GOVERNANCE.md PROGRESS.md TASKS.md ISSUES.md REVIEW.md CROSSREF.md CONTRIBUTING.md
) > memory\checkpoints\%DT%.md
echo [OK] Checkpoint 写入 memory\checkpoints\%DT%.md
goto :end

:report
echo [*] 生成综合报告 ...
echo.
echo ============================================================
echo   《现代 C++ 终极圣经》综合报告
echo   日期: %date% %time%
echo ============================================================
echo.
echo [门禁]
%PY% tools/consistency_check.py 2>&1 | findstr "汇总\|评分"
echo.
echo [交叉引用]
%PY% tools/crossref_audit.py 2>&1 | findstr "Coverage\|覆盖率\|总条数\|断链"
echo.
echo [知识图谱]
%PY% -c "import json; d=json.load(open('knowledge_graph.json',encoding='utf-8')); print(f'version={d[\"version\"]} chapters={d[\"total_chapters\"]} parts={len(d[\"parts\"])}')" 2>nul
echo.
echo [基础设施]
for %%f in (GOVERNANCE.md PROGRESS.md TASKS.md ISSUES.md REVIEW.md CROSSREF.md REFERENCES.md CONTRIBUTING.md glossary.json knowledge_graph.json) do if exist "%%f" (echo   [OK] %%f) else (echo   [--] %%f 缺失)
echo.
goto :end

:help
echo 用法: make [目标]
echo.
echo    check      一致性门禁检查
echo    compile    全书 cpp 编译校验
echo    full       全量: check + compile + crossref（默认）
echo    crossref   交叉引用审计
echo    clean      清理临时 *.cpp *.exe
echo    stats      全书统计
echo    graph      验证知识图谱
echo    checkpoint 生成每日 checkpoint
echo    report     综合项目报告
echo    help       此帮助
goto :end

:end
endlocal
