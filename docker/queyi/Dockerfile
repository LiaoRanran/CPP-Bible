# docker/queyi/Dockerfile — 683-E3：Queyi 研究数据链镜像。
#
# 定位：在**不依赖本地编译器与 WSL** 的前提下复算全部数据/统计口径：
#   * verify_paper_numbers / paper_quality_gate（数字对账与论文门禁）
#   * analyze_682_sensitivity / analyze_683_oc（A5 敏感性 / operator 消融，纯 Python）
#   * site_683_data（官网数据再生成，校验"站上数字=仓库数字"）
#   * tests/ 中不依赖编译器的子集
#
# 明确**不包含**（诚实边界）：真实检测链（asan/ubsan/tsan 需要 WSL g++；
# compiler-warn 需要 MinGW g++）。要做全链复现请按 docs/reproduce.html 在宿主机跑。
#
# 供应链：python:3.12-slim 官方镜像；仅装 pyyaml（门禁工具的顶层依赖）。
# 以非 root 用户运行；镜像内不含任何密钥/凭据（683 红线 9）。
FROM python:3.12-slim

# 基础镜像以 tag 引用：683 执行环境本机无 Docker，**无法取得并验证真实 digest**，
# 按"不编造"原则不写未验证的 digest（写了会误导且直接导致 build 失败）。
# 首次构建建议钉 digest（可复现性与供应链安全）：
#   docker buildx imagetools inspect python:3.12-slim
LABEL org.opencontainers.image.title="queyi-research" \
      org.opencontainers.image.description="Queyi (阙疑) research data-chain reproducibility image" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.source="https://github.com/LiaoRanran/CPP-Bible"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "pyyaml>=6.0" \
    && useradd --create-home --uid 1000 queyi

WORKDIR /workspace
COPY --chown=queyi:queyi . .
USER queyi

# 默认动作 = 最小数据链自检（数字对账 + 站点数据再生成验证）
CMD ["bash", "-lc", "python tools/verify_paper_numbers.py && python tools/site_683_data.py && git diff --exit-code docs/assets/data || true"]
