#!/usr/bin/env bash
# 701 一键构建脚本：遍历案例库中全部 case 的 clone_build.sh
# 用法: bash build_all.sh [results_dir]
# 说明: 699 的 22 个已在 WSL 实测（结果见 ../../../701_build_results.md）；本脚本供在干净 Linux 上全量重跑。
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE/build_results}"
mkdir -p "$OUT"
TOTAL=0; OK=0; FAIL=0
for cve in \
  CVE-2023-4863 \
  CVE-2023-38545 \
  CVE-2014-0160 \
  CVE-2022-3602 \
  CVE-2022-3786 \
  CVE-2022-37434 \
  CVE-2021-4034 \
  CVE-2022-4304 \
  CVE-2022-2509 \
  CVE-2023-28484 \
  CVE-2022-40303 \
  CVE-2024-3094 \
  CVE-2023-0464 \
  CVE-2023-0286 \
  CVE-2020-13777 \
  CVE-2022-23219 \
  CVE-2016-5195 \
  CVE-2015-0235 \
  CVE-2018-1000001 \
  CVE-2016-10190 \
  CVE-2021-23840 \
  CVE-2019-8457 \
  CVE-2021-3156 \
  CVE-2014-6271 \
  CVE-2023-44487 \
  CVE-2022-0543 \
  CVE-2017-7529 \
  CVE-2019-11043 \
  CVE-2024-6387 \
  CVE-2021-38001 \
  CVE-2016-8655 \
  CVE-2017-1000367 \
  CVE-2022-42898 \
  CVE-2020-10735 \
  CVE-2021-35937 \
  CVE-2017-15277 \
  CVE-2022-38784 \
  CVE-2019-7310 \
  CVE-2021-44790 \
  CVE-2022-0847 \
  ; do
  TOTAL=$((TOTAL+1))
  sh="$HERE/$cve/clone_build.sh"
  log="$OUT/$cve.log"
  if [ ! -f "$sh" ]; then echo "$cve SKIP (no script)" | tee -a "$OUT/summary.tsv"; FAIL=$((FAIL+1)); continue; fi
  if timeout 1800 bash "$sh" >"$log" 2>&1; then
    echo -e "$cve\tbuilt_true" >> "$OUT/summary.tsv"; OK=$((OK+1))
  else
    echo -e "$cve\tbuilt_false\tsee $log" >> "$OUT/summary.tsv"; FAIL=$((FAIL+1))
  fi
done
echo "DONE total=$TOTAL ok=$OK fail=$FAIL  (summary: $OUT/summary.tsv)"
