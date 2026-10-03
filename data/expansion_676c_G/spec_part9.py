# -*- coding: utf-8 -*-
# 676c-G spec part9: curl 逻辑 miss 组 (G043-G048)
PART = [
("G043", dict(
  defect_type="logic_error", func="ftp_pasv_connect", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2020-8284", url="https://nvd.nist.gov/vuln/detail/CVE-2020-8284",
           project="curl", commit="", simplification="剥离 FTP 控制通道，PASV 响应硬编码，保留『信任服务器提供的 PASV IP/端口回连』核心缺陷"),
  trigger="恶意服务器在 PASV 响应中提供攻击者 IP:port，curl 回连该地址",
  notes="CVE-2020-8284: FTP PASV 响应被恶意服务器利用让 curl 回连任意地址（CVE 描述: A malicious server can use the FTP PASV response to trick curl ... into connecting back to a given IP address and port）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2020-8284: FTP PASV 响应中的地址被无条件信任
struct FtpConn {
    std::string host;        // 用户连接的主机
    std::string data_ip;     // 数据通道 IP(应来自 host)
    int         data_port;
};

static void ftp_parse_pasv(FtpConn* c, const std::string& pasv_reply) {
    // PASV 回复: "227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)"
    int h1, h2, h3, h4, p1, p2;
    /* DEFECT */ // 原始缺陷: 不校验回复 IP 与控制连接主机是否一致
    std::sscanf(pasv_reply.c_str(), "227 Entering Passive Mode (%d,%d,%d,%d,%d,%d)",
                &h1, &h2, &h3, &h4, &p1, &p2);
    char ip[32];
    std::snprintf(ip, sizeof(ip), "%d.%d.%d.%d", h1, h2, h3, h4);
    c->data_ip = ip;
    c->data_port = p1 * 256 + p2;
}

int main() {
    FtpConn c{ "ftp.victim.example", "", 0 };
    // 恶意服务器的 PASV 响应: 指向攻击者的内网扫描地址
    ftp_parse_pasv(&c, "227 Entering Passive Mode (10,0,0,169,1,144)");
    std::printf("数据通道连接: %s:%d (用户意图: 连接 %s)\n",
                c.data_ip.c_str(), c.data_port, c.host.c_str());
    std::printf("(正确行为: 拒绝与控制连接主机不一致的 PASV 地址)\n");
    return 0;
}
'''),

("G044", dict(
  defect_type="logic_error", func="http_download_with_J", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2020-8177", url="https://nvd.nist.gov/vuln/detail/CVE-2020-8177",
           project="curl", commit="", simplification="剥离 HTTP 下载流程，Content-Disposition 硬编码，保留『-J 使用服务器提供文件名时不做覆盖检查』核心缺陷"),
  trigger="服务器返回 Content-Disposition filename 指向已存在的本地文件 → 被覆盖",
  notes="CVE-2020-8177: -J 选项导致本地文件被覆盖（CVE 描述: improper restriction of names for files ... that can lead to overwriting a local file when the -J flag is used）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2020-8177: -J 使用服务器提供的文件名且不做覆盖检查
struct Download {
    std::string out_file;          // 用户指定的输出文件
    bool        content_dispo;     // 服务器是否返回 Content-Disposition
    std::string server_filename;   // 服务器提供的文件名
};

static std::string choose_output_name(const Download* d, bool file_exists) {
    if (d->content_dispo && !d->server_filename.empty()) {
        /* DEFECT */ // 原始缺陷: -J 时直接采用服务器文件名, 不检查 file_exists
        return d->server_filename;
    }
    return d->out_file;
}

int main() {
    Download d{ ".bashrc", true, ".bashrc" };   // 恶意服务器指向用户已有文件
    bool exists = true;
    std::string target = choose_output_name(&d, exists);
    std::printf("写入目标: %s (文件已存在: %s)\n", target.c_str(), exists ? "是" : "否");
    std::printf("(正确行为: 目标已存在时应中止或改名, 不覆盖)\n");
    return 0;
}
'''),

("G045", dict(
  defect_type="state_machine", func="http_post_after_put", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2022-32221", url="https://nvd.nist.gov/vuln/detail/CVE-2022-32221",
           project="curl", commit="", simplification="剥离连接复用层，保留『同一 handle 先做 PUT(读回调) 再 POST(POSTFIELDS) 时错误调用读回调』核心状态缺陷"),
  trigger="同一 handle 先 PUT(读回调) 再 POST(POSTFIELDS)，发送阶段错误调用读回调",
  notes="CVE-2022-32221: PUT 之后复用 handle 发 POST 时错误调用读回调（CVE 描述: might erroneously use the read callback ... even when CURLOPT_POSTFIELDS has been set, if the same handle previously was used to issue a PUT request）。状态逻辑错误 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2022-32221: PUT 后复用 handle 发 POST → 错误使用读回调
enum HttpMethod { HTTP_NONE, HTTP_PUT, HTTP_POST };

struct EasyHandle {
    HttpMethod last_method;
    std::string postfields;       // POST 正文(直接发送)
    bool        read_callback_set;
};

static std::string http_perform(EasyHandle* h, HttpMethod method) {
    h->last_method = method;
    if (method == HTTP_POST && !h->postfields.empty()) {
        // 应直接发送 POSTFIELDS
        if (h->read_callback_set && h->last_method == HTTP_PUT) {
            /* DEFECT */ // 原始缺陷: 之前 PUT 设置的读回调状态残留, 错误走读回调路径
            return "READ-CALLBACK-DATA[stale]";
        }
        return h->postfields;
    }
    return "PUT-BODY";
}

int main() {
    EasyHandle h{ HTTP_NONE, "POST-REQUEST-BODY", true };
    http_perform(&h, HTTP_PUT);                     // 第一个请求: PUT 用读回调
    std::string sent = http_perform(&h, HTTP_POST); // 第二个请求: POST 用 POSTFIELDS
    std::printf("POST 实际发送: %s\n", sent.c_str());
    std::printf("(正确行为: 发送 POST-REQUEST-BODY, 不应调用已废弃的读回调)\n");
    return 0;
}
'''),

("G046", dict(
  defect_type="logic_error", func="negotiate_reuse_check", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2015-3148", url="https://nvd.nist.gov/vuln/detail/CVE-2015-3148",
           project="curl", commit="", simplification="剥离 Negotiate 认证流程，保留『连接复用不检查认证身份一致性』核心缺陷"),
  trigger="user1 完成 Negotiate 认证后，user2 的请求错误复用该已认证连接",
  notes="CVE-2015-3148: Negotiate 认证连接被错误复用（CVE 描述: do not properly re-use authenticated Negotiate connections, which allows remote attackers to connect as other users via a request）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2015-3148: Negotiate 已认证连接被其他用户复用
struct Connection {
    std::string authenticated_as;   // 完成认证的用户
    bool        in_pool;
};

static Connection* pick_connection(Connection* pool, int n, const std::string& wanted_user) {
    /* DEFECT */ // 原始缺陷: 复用判定只看主机/端口, 不看 authenticated_as
    for (int i = 0; i < n; ++i)
        if (pool[i].in_pool) return &pool[i];
    return 0;
}

int main() {
    Connection pool[1] = { { "user1", true } };   // user1 的已认证连接
    Connection* c = pick_connection(pool, 1, "user2");
    std::printf("user2 的请求复用连接: authenticated_as=%s (正确行为: 不应复用)\n",
                c ? c->authenticated_as.c_str() : "(新建)");
    return 0;
}
'''),

("G047", dict(
  defect_type="logic_error", func="sftp_expand_tilde", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2023-27534", url="https://nvd.nist.gov/vuln/detail/CVE-2023-27534",
           project="curl", commit="", simplification="剥离 SFTP 传输层，保留『~ 前缀被错误展开导致路径穿越』核心缺陷"),
  trigger="SFTP 路径首段以 ~ 开头且含 /../，被展开到用户主目录之外",
  notes="CVE-2023-27534: SFTP 路径穿越（CVE 描述: the tilde (~) character to be wrongly replaced when used as a prefix in the first path element ... path traversal vulnerability, CWE-22）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <string>
// CVE-2023-27534: SFTP ~ 前缀错误展开 → 路径穿越
static std::string sftp_resolve(const std::string& remote_path, const std::string& home) {
    if (!remote_path.empty() && remote_path[0] == '~') {
        /* DEFECT */ // 原始缺陷: 首元素 ~ 与后续 /.. 组合时未按安全规则展开
        // "~~~poor-~/../../etc/passwd" → ~ 之后整段拼接, .. 未规范化
        return home + remote_path.substr(1);
    }
    return remote_path;
}

int main() {
    std::string resolved = sftp_resolve("~~~poor-~/../../etc/passwd", "/home/victim");
    std::printf("SFTP 实际访问: %s\n", resolved.c_str());
    std::printf("(正确行为: 不应展开到 /home/victim 之外)\n");
    return 0;
}
'''),

("G048", dict(
  defect_type="logic_error", func="ocsp_check_response", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2020-8286", url="https://nvd.nist.gov/vuln/detail/CVE-2020-8286",
           project="curl", commit="", simplification="剥离 TLS/OCSP 主体，保留『OCSP 响应校验不足 → 撤销状态检查失效』核心缺陷"),
  trigger="OCSP 响应状态字段异常，检查函数仍返回证书有效",
  notes="CVE-2020-8286: 证书撤销检查不足（CVE 描述: improper check for certificate revocation due to insufficient verification of the OCSP response, CWE-295）。逻辑缺陷 → 诚实标 miss。",
), r'''
#include <cstdio>
// CVE-2020-8286: OCSP 响应校验不足 → 撤销检查失效
struct OcspResponse {
    int  status;          // 0=good 1=revoked 2=unknown
    bool malformed;
};

static bool certificate_revoked(const OcspResponse* r) {
    /* DEFECT */ // 原始缺陷: malformed 响应未按"校验失败"处理, 而是当作"未撤销"
    if (r->malformed) return false;   // 应当: 校验失败 → 视为验证不通过
    return r->status == 1;
}

int main() {
    OcspResponse r{ 2, true };   // 恶意服务器返回畸形 OCSP 响应
    std::printf("证书已撤销? %s (响应畸形: %s)\n",
                certificate_revoked(&r) ? "是" : "否[错误: 校验失败应阻断连接]",
                r.malformed ? "是" : "否");
    return 0;
}
'''),
]
