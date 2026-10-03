# -*- coding: utf-8 -*-
# 676c-G spec part8: curl ubsan/asan/miss 组 (G038-G042)
PART = [
("G038", dict(
  defect_type="heap_overflow", func="sasl_build_login_response", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-16839", url="https://nvd.nist.gov/vuln/detail/CVE-2018-16839",
           project="curl", commit="", simplification="基于 CVE 描述（SASL 认证代码缓冲区过写, CWE-122+CWE-190）以『长度 int 溢出 → 小分配大写入』等价机制重构，非原始代码逐行镜像，故标 planted=true"),
  trigger="用户名+授权 ID 总长 2^30 级别，响应总长 int 溢出为负 → 按真实长度写入 1 字节分配",
  notes="CVE-2018-16839: SASL 认证代码缓冲区过写（CVE 描述: a buffer overrun in the SASL authentication code that may lead to denial of service; CWE-122/CWE-190）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2018-16839: SASL 响应长度 int 溢出 → 小分配 + 大写入
static char* sasl_build_login_response(int userlen, int authzlen) {
    /* DEFECT */ int total = userlen + authzlen + 32;   // 原始缺陷: int 溢出
    char* resp = new char[total > 0 ? total : 1];       // 溢出后分配 1 字节
    size_t real = (size_t)userlen + (size_t)authzlen + 32;
    std::memset(resp, 'A', real);                       // 按真实需求写入 → 堆越界写
    return resp;
}

int main() {
    // crafted 超长用户名/授权 ID(运行时变量绕过常量折叠)
    volatile int ul = 0x40000000, al = 0x40000000;
    char* r = sasl_build_login_response(ul, al);
    std::printf("resp[0]=%c\n", r[0]);
    delete[] r;
    return 0;
}
'''),

("G039", dict(
  defect_type="heap_overread", func="tool_writeout", severity="low", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-7407", url="https://nvd.nist.gov/vuln/detail/CVE-2017-7407",
           project="curl", commit="", simplification="剥离 curl 工具 write-out 全部变量类型，保留『变量解析循环缺少缓冲区终止检查』核心缺陷"),
  trigger="--write-out 参数以未闭合的 %{ 结尾，变量扫描越过堆缓冲",
  notes="CVE-2017-7407: --write-out 以 $ 变量结尾时读取越界（CVE 描述: reading a workstation screen ... obtain sensitive information from process memory via a --write-out argument ending in a variable without terminator）。",
), r'''
#include <cstdio>
// CVE-2017-7407: --write-out 变量解析缺少终止检查 → 越界读
static void tool_writeout(const char* wrd, size_t len) {
    const char* p = wrd;
    const char* end = wrd + len;
    while (p < end) {
        if (*p == '%' && p + 1 < end && p[1] == '{') {
            const char* q = p + 2;
            /* DEFECT */ while (*q && *q != '}') ++q;   // 原始缺陷: 未检查 q < end
            std::printf("var=%.*s\n", (int)(q - (p + 2)), p + 2);
            p = q + 1;
        } else {
            ++p;
        }
    }
}

int main() {
    // crafted write-out: 堆上 5 字节, 以未闭合的 %{ 结尾且无 NUL
    char* w = new char[5]{ '%', '{', 's', 'i', 'z' };
    tool_writeout(w, 5);    // while(*q...) 走过堆缓冲末尾 → 越界读
    delete[] w;
    return 0;
}
'''),

("G040", dict(
  defect_type="integer_overflow", func="curl_easy_escape_alloc", severity="high", planted=False,
  verdict="catch", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-7167", url="https://nvd.nist.gov/vuln/detail/CVE-2016-7167",
           project="curl", commit="", simplification="剥离转义主体，保留『最坏情况下分配尺寸按 int 计算 len+3*2+1』核心缺陷，输入长度由运行时变量给出"),
  trigger="输入字符串长度接近 INT_MAX，+7 分配计算有符号溢出",
  notes="CVE-2016-7167: curl_escape 系列函数整数溢出（CVE 描述: Multiple integer overflows in the (1) curl_escape ... via a string of length 0xffffffff, which triggers a heap-based buffer overflow）。",
), r'''
#include <cstdio>
// CVE-2016-7167: 转义函数分配尺寸 int 溢出
static int escape_alloc_size(int len) {
    /* DEFECT */ int alloc = len + 2 * 3 + 1;   // 最坏情况: 每字符转 3 字节 + NUL
    return alloc;
}

int main() {
    // crafted: 长度接近 0xFFFFFFFF 的待转义字符串(运行时变量绕过常量折叠)
    volatile int len = 2147483647 - 5;
    int alloc = escape_alloc_size(len);
    std::printf("escape alloc=%d (应为 %lld)\n", alloc, (long long)len + 7);
    return 0;
}
'''),

("G041", dict(
  defect_type="logic_error", func="http_referer_build", severity="low", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2021-22876", url="https://nvd.nist.gov/vuln/detail/CVE-2021-22876",
           project="curl", commit="", simplification="剥离 HTTP 传输层，保留『自动填充 Referer 时不剥离 URL 中的用户凭据』核心缺陷"),
  trigger="URL 含 user:password@ 前缀，自动 Referer 未剥离凭据直接发送",
  notes="CVE-2021-22876: Referer 头泄露凭据（CVE 描述: libcurl does not strip off user credentials from the URL when automatically populating the Referer: HTTP header）。信息泄露逻辑错误，正确=剥离凭据、实际=包含，sanitizer 无报告 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2021-22876: 自动 Referer 不剥离 URL 凭据 → 信息泄露
static std::string build_referer(const std::string& url) {
    /* DEFECT */ // 原始缺陷: 直接取 scheme:// 之后整段, 未剥离 user:password@
    size_t scheme_end = url.find("://");
    return url.substr(0, scheme_end + 3) + url.substr(scheme_end + 3, url.find('/', scheme_end + 3) - scheme_end - 3) + "/";
}

int main() {
    // 受害者使用带凭据的 URL 访问, 跳转到第三方页面
    std::string url = "https://alice:hunter2@internal.example.com/secret/page";
    std::string referer = build_referer(url);
    std::printf("Referer: %s\n", referer.c_str());
    std::printf("(正确行为: Referer 不应包含 alice:hunter2)\n");
    return 0;
}
'''),

("G042", dict(
  defect_type="info_leak", func="telnet_send_new_env", severity="medium", planted=False,
  verdict="miss", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-22898", url="https://nvd.nist.gov/vuln/detail/CVE-2021-22898",
           project="curl", commit="", simplification="剥离 TELNET 传输层，保留『NEW_ENV 选项解析器把非用户指定的环境变量一并发送』核心缺陷"),
  trigger="-t NEW_ENV 选项解析时把本机环境变量值(含敏感数据)一并装入发送缓冲",
  notes="CVE-2021-22898: TELNET NEW_ENV 选项解析缺陷导致环境变量发送给服务器（CVE 描述: libcurl could send environment variables to TELNET servers ... information disclosure）。sanitizer 无报告 → 诚实标 miss（信息泄露盲区）。",
), r'''
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2021-22898: TELNET NEW_ENV 解析器把本机环境变量发给服务器
static const char* k_machine_env[] = {
    "USER=alice", "HOME=/home/alice", "SECRET_TOKEN=s3cr3t-value", 0
};

static std::string telnet_send_new_env(const char* user_opt) {
    // 用户指定的变量对: user_opt = "TERM=xterm"
    std::string payload = "NEW_ENV:";
    payload += user_opt;
    /* DEFECT */ // 原始缺陷: 选项解析器把环境块中的变量也当作用户选项装入 payload
    for (int i = 0; k_machine_env[i]; ++i) {
        payload += ";";
        payload += k_machine_env[i];
    }
    return payload;
}

int main() {
    std::string sent = telnet_send_new_env("TERM=xterm");
    std::printf("TELNET 发送: %s\n", sent.c_str());
    std::printf("(正确行为: 仅发送 TERM=xterm, SECRET_TOKEN 不应离开本机)\n");
    return 0;
}
'''),
]
