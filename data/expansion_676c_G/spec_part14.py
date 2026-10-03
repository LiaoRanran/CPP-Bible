# -*- coding: utf-8 -*-
# 676c-G spec part14: glibc/sudo/polkit/logic 组 (G074-G080)
PART = [
("G074", dict(
  defect_type="heap_underflow", func="realpath_mirror", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-1000001", url="https://nvd.nist.gov/vuln/detail/CVE-2018-1000001",
           project="glibc", commit="", simplification="基于 CVE 描述（realpath 对 getcwd 的用法混乱导致向目的缓冲区之前写入 buffer underflow）以等价的指针前移机制重构，非原始代码镜像，故标 planted=true"),
  trigger="深层 cwd 前缀(300 字节) + 相对路径解析 → 目的指针越过缓冲区起点写 300 字节",
  notes="CVE-2018-1000001: realpath 向目的缓冲区之前写入（CVE 描述: confusion in the usage of getcwd() by realpath() which can be used to write before the destination buffer leading to a buffer underflow）。用户态等价重构（planted=true）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2018-1000001: realpath 写到目的缓冲区之前 → 堆缓冲下溢
static const char* k_cwd_prefix = "/very/deeply/nested/directory/prefix/that/is/quite/long/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

static char* realpath_mirror(const char* rel_path, char* resolved, size_t dest_cap) {
    size_t prefix_len = std::strlen(k_cwd_prefix);
    size_t rel_len = std::strlen(rel_path);
    char* dest_end = resolved + dest_cap;
    /* DEFECT */ // 原始缺陷: 前缀+路径超长时指针越过起点而未中止
    char* p = dest_end - rel_len - 1 - prefix_len;
    std::memcpy(p, k_cwd_prefix, prefix_len);        // 向 resolved 之前写入 → 下溢
    std::memcpy(p + prefix_len, rel_path, rel_len);
    return p;
}

int main() {
    char* resolved = new char[256];
    realpath_mirror("/etc/passwd", resolved, 256);   // 前缀 300 字节 → 起点前移 ~265 字节
    delete[] resolved;
    return 0;
}
'''),

("G075", dict(
  defect_type="heap_overflow", func="sudo_set_cmnd", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-3156", url="https://nvd.nist.gov/vuln/detail/CVE-2021-3156",
           project="sudo", commit="", simplification="剥离 sudo 命令行解析，保留『user_args 按原始长度分配、转义拷贝时反斜杠翻倍』核心缺陷（与原始 set_cmnd 循环同构）"),
  trigger="sudoedit -s 参数含 100 个反斜杠：分配按 strlen+1，写入时每个反斜杠占 2 槽 → 溢出",
  notes="CVE-2021-3156 (Baron Samedit): sudo 堆溢出。原始缺陷：user_args 尺寸按原始长度计算，但 sudoedit 模式转义循环把每个 '\\' 复制为两个，写入超出分配。",
), r'''
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2021-3156: user_args 分配尺寸未计入反斜杠转义翻倍 → 堆溢出
static char* sudo_set_cmnd(const char* args) {
    size_t size = std::strlen(args) + 1;      // 原始缺陷: 未按转义后长度计算
    char* user_args = new char[size];
    size_t j = 0;
    for (size_t i = 0; args[i]; ++i) {
        user_args[j++] = args[i];
        /* DEFECT */ if (args[i] == '\\')
            user_args[j++] = '\\';            // sudoedit 模式: 反斜杠翻倍 → j 超过 size
    }
    return user_args;
}

int main() {
    // crafted 参数: 100 组 "\\x" (200 字符, 含 100 个反斜杠)
    std::string args;
    for (int i = 0; i < 100; ++i) args += "\\x";
    char* ua = sudo_set_cmnd(args.c_str());   // 分配 201, 写入 ~300 → 溢出
    std::printf("user_args=%.10s...\n", ua);
    delete[] ua;
    return 0;
}
'''),

("G076", dict(
  defect_type="stack_overflow_write", func="pkexec_main", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-4034", url="https://nvd.nist.gov/vuln/detail/CVE-2021-4034",
           project="polkit", commit="", simplification="基于 CVE 描述（pkexec 未处理 argc==0 的调用约定，把 envp 当 argv 使用导致越界写入）以等价的参数循环重构，非原始代码镜像，故标 planted=true"),
  trigger="execve 传 argc=0：参数循环把 3 个环境字符串写入只有 1 槽的本地 argv 数组",
  notes="CVE-2021-4034 (PwnKit): pkexec 本地提权（CVE 描述: doesn't handle the calling convention correctly ... CWE-787/CWE-125）。用户态等价重构（planted=true）。",
), r'''
#include <cstdio>
// CVE-2021-4034: argc==0 时 envp 被当作 argv 使用 → 越界写
static int pkexec_main(int argc, char** envp) {
    char* local_argv[1];      // argc==0: argv 数组实际没有可用槽位
    int n = 0;
    if (argc == 0) {
        /* DEFECT */ // 原始缺陷: 未处理 argc==0, 继续枚举 argv[1..] —— 实际读到 envp 区
        // 简化镜像: 把 envp 字符串写入本地 argv 槽位(模拟对 argv 区的越界写)
        for (n = 0; envp[n]; ++n)
            local_argv[n] = envp[n];          // n>=1 越过 1 槽数组 → 栈越界写
    }
    return n;
}

int main() {
    char* env[] = { "PATH=/usr/bin", "LD_PRELOAD=/tmp/evil.so", "X=1", 0 };
    std::printf("written=%d\n", pkexec_main(0, env));   // 3 个字符串写入 1 槽数组
    return 0;
}
'''),

("G077", dict(
  defect_type="logic_error", func="bash_import_function", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2014-6271", url="https://nvd.nist.gov/vuln/detail/CVE-2014-6271",
           project="bash", commit="", simplification="剥离 bash 词法/执行主体，以等价导入解析器镜像『函数定义之后的尾随字符串被继续执行』核心缺陷"),
  trigger="环境变量值 '() { :; }; echo pwned' → 尾随 'echo pwned' 被当作命令执行",
  notes="CVE-2014-6271 (Shellshock): 函数定义后尾随串被执行（CVE 描述: processes trailing strings after function definitions in the values of environment variables, which allows remote attackers to execute arbitrary code）。纯解析逻辑错误 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
// CVE-2014-6271: bash 函数导入解析器执行尾随命令
static std::vector<std::string> g_executed;

static bool bash_import_function(const char* env_value) {
    if (std::strncmp(env_value, "() {", 4) != 0) return false;
    const char* body_end = std::strstr(env_value, "};");
    if (!body_end) return false;
    // 1) 函数体被注册
    g_executed.push_back(std::string("define func: ") + std::string(env_value + 4, body_end - env_value - 4));
    /* DEFECT */ // 原始缺陷: 定义之后的尾随字符串未丢弃, 被解析器继续当作命令执行
    const char* trailing = body_end + 2;
    if (*trailing)
        g_executed.push_back(std::string("EXECUTE: ") + (trailing + 1));
    return true;
}

int main() {
    bash_import_function("() { :; }; echo pwned; cat /etc/shadow");
    for (const std::string& e : g_executed)
        std::printf("%s\n", e.c_str());
    std::printf("(正确行为: 只注册函数体, 尾随命令必须被丢弃)\n");
    return 0;
}
'''),

("G078", dict(
  defect_type="state_machine", func="ssh_server_handle_packet", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2018-10933", url="https://nvd.nist.gov/vuln/detail/CVE-2018-10933",
           project="libssh", commit="", simplification="剥离 libssh 分组加密/传输层，以等价服务端状态机镜像『未认证即可处理 CHANNEL_OPEN』核心缺陷"),
  trigger="认证完成前客户端发送 SSH_MSG_CHANNEL_OPEN(90) → 通道被创建",
  notes="CVE-2018-10933: libssh 服务端状态机缺陷（CVE 描述: A malicious client could create channels without first performing authentication, resulting in unauthorized access）。状态机逻辑错误 → 诚实标 miss。",
), r'''
#include <cstdio>
// CVE-2018-10933: 服务端在认证前接受 CHANNEL_OPEN
enum SshState { ST_BANNER, ST_KEX, ST_USERAUTH, ST_AUTHENTICATED };
enum SshMsg { MSG_CHANNEL_OPEN = 90, MSG_USERAUTH_SUCCESS = 60 };

static bool g_channel_opened = false;

static void ssh_server_handle_packet(SshState* st, int msg_type) {
    if (msg_type == MSG_USERAUTH_SUCCESS) {
        *st = ST_AUTHENTICATED;
    } else if (msg_type == MSG_CHANNEL_OPEN) {
        /* DEFECT */ // 原始缺陷: 不检查 *st == ST_AUTHENTICATED
        g_channel_opened = true;    // 未认证客户端创建通道
    }
}

int main() {
    SshState st = ST_BANNER;                 // 攻击者刚连上, 未做任何认证
    ssh_server_handle_packet(&st, MSG_CHANNEL_OPEN);
    std::printf("channel_opened=%d state=%d (正确行为: 未认证必须拒绝 CHANNEL_OPEN)\n",
                (int)g_channel_opened, (int)st);
    return 0;
}
'''),

("G079", dict(
  defect_type="state_machine", func="ssh_transport_process_packet", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2023-48795", url="https://nvd.nist.gov/vuln/detail/CVE-2023-48795",
           project="openssh", commit="", simplification="剥离 SSH 二进制分组层，以等价序号/前缀校验状态机镜像『非预期包推进序号使 EXT_INFO 前缀校验失效』核心缺陷"),
  trigger="MITM 注入额外 KEXINIT 包后转发被截断的协商 → 客户端认为 EXT_INFO 完整到达",
  notes="CVE-2023-48795 (Terrapin): SSH 传输协议前缀截断（CVE 描述: allows remote attackers to bypass integrity checks such that some packets are omitted (from the extension negotiation message)）。状态机逻辑错误 → 诚实标 miss。",
), r'''
#include <cstdio>
// CVE-2023-48795 (Terrapin): 非预期包推进序号 → 前缀截断不被察觉
struct SshTransport {
    unsigned long seq;          // 包序号(所有包无条件 +1)
    bool strict_kex;            // 是否启用严格 KEX 模式
    bool ext_info_received;     // 是否按正确前缀收到 EXT_INFO
};

static const int MSG_KEXINIT = 20, MSG_EXT_INFO = 7, MSG_IGNORE = 2;

static void transport_process_packet(SshTransport* t, int msg_type) {
    t->seq++;
    if (msg_type == MSG_KEXINIT) {
        /* DEFECT */ // 原始缺陷: 严格模式下, 非预期 KEXINIT 也推进序号,
        //             使后续 EXT_INFO 的前缀位置校验失效
        t->seq += 0;
    } else if (msg_type == MSG_EXT_INFO && t->strict_kex) {
        // 校验: EXT_INFO 必须是 KEXINIT 之后第 2 个包(seq==2)
        // 但被注入的 IGNORE/KEXINIT 包已把 seq 推高 → 校验被错误放行
        t->ext_info_received = true;   // 未按预期前缀到达, 却被接受
    }
}

int main() {
    SshTransport t{ 0, true, false };
    transport_process_packet(&t, MSG_KEXINIT);   // 合法 KEXINIT (seq=1)
    transport_process_packet(&t, MSG_EXT_INFO);  // MITM 截断: 客户端以为这是首包后的 EXT_INFO
    std::printf("ext_info_received=%d seq=%lu (正确行为: EXT_INFO 必须在 seq==2 到达且无插入包)\n",
                (int)t.ext_info_received, t.seq);
    return 0;
}
'''),

("G080", dict(
  defect_type="logic_error", func="cgi_proxy_env", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-5385", url="https://nvd.nist.gov/vuln/detail/CVE-2016-5385",
           project="php", commit="", simplification="剥离 CGI 层与 HTTP 客户端，保留『HTTP_PROXY 环境变量来自客户端可注入的 Proxy 头且被直接信任』核心缺陷"),
  trigger="客户端发送 Proxy: attacker.example 头 → CGI 环境出现 HTTP_PROXY → 出站请求被劫持",
  notes="CVE-2016-5385 (HTTPoxy): RFC 3875 命名空间冲突未处理（CVE 描述: does not attempt to address RFC 3875 section 4.1.18 namespace conflicts ... untrusted client data in the HTTP_PROXY environment variable）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2016-5385 (HTTPoxy): HTTP_PROXY 环境变量被客户端注入并直接信任
static std::string http_get_with_proxy(const std::string& target_host, const std::string& env_http_proxy) {
    /* DEFECT */ // 原始缺陷: 未区分服务器配置的代理与客户端注入的 HTTP_PROXY
    if (!env_http_proxy.empty())
        return "proxy://" + env_http_proxy + " -> " + target_host;
    return "direct://" + target_host;
}

int main() {
    // 攻击者请求头: "Proxy: attacker.example:8080"
    // CGI 按 RFC 3875 把 HTTP 头映射为 HTTP_PROXY 环境变量
    std::string env_http_proxy = "attacker.example:8080";
    std::string result = http_get_with_proxy("api.internal.example", env_http_proxy);
    std::printf("出站请求: %s\n", result.c_str());
    std::printf("(正确行为: 忽略客户端注入的 HTTP_PROXY, 使用直连或服务器配置代理)\n");
    return 0;
}
'''),
]
