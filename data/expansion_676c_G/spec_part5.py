# -*- coding: utf-8 -*-
# 676c-G spec part5: OpenSSL 逻辑/并发组 (G021-G025)
PART = [
("G021", dict(
  defect_type="state_machine", func="ssl3_process_ccs", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2014-0224", url="https://nvd.nist.gov/vuln/detail/CVE-2014-0224",
           project="openssl", commit="", simplification="剥离 TLS 记录层与密码套件，以等价握手状态机镜像『CCS 消息不检查当前状态即处理』核心缺陷"),
  trigger="在 ClientHello 之后、ServerHelloDone 之前注入 ChangeCipherSpec",
  notes="CVE-2014-0224 (CCS 注入): 不限制 CCS 消息处理状态（CVE 描述: does not properly restrict processing of ChangeCipherSpec messages）→ MITM 强制零长度 master key。纯状态机逻辑错误，正确=拒绝、实际=接受，sanitizer 无报告 → 诚实标 miss。",
), r'''
#include <cstdio>
// CVE-2014-0224: ChangeCipherSpec 不检查握手状态 → 提前切换密钥
enum HsState { HS_CLIENT_HELLO_SENT, HS_SERVER_HELLO_DONE, HS_ESTABLISHED };
enum HsMsg { MSG_FINISHED = 16, MSG_CCS = 20 };

struct SslSession {
    HsState state;
    bool    ccs_seen;
    int     master_key_len;   // 正常协商 48 字节
};

static void ssl3_process_message(SslSession* s, int msg_type) {
    if (msg_type == MSG_CCS) {
        /* DEFECT */ // 原始缺陷: 不检查 state 是否已到 SERVER_HELLO_DONE
        s->ccs_seen = true;
        s->master_key_len = 0;    // 提前切换 → master key 长度 0
        s->state = HS_ESTABLISHED;
    } else if (msg_type == MSG_FINISHED && s->state == HS_ESTABLISHED) {
        std::printf("finished accepted with key_len=%d\n", s->master_key_len);
    }
}

int main() {
    SslSession s{ HS_CLIENT_HELLO_SENT, false, 48 };
    ssl3_process_message(&s, MSG_CCS);      // MITM 在 ServerHelloDone 之前注入 CCS
    ssl3_process_message(&s, MSG_FINISHED); // 用 0 长度 key 完成握手
    std::printf("state=%d key_len=%d (正确: CCS 应被拒绝, key_len=48)\n",
                (int)s.state, s.master_key_len);
    return 0;
}
'''),

("G022", dict(
  defect_type="logic_error", func="ssl3_get_key_exchange", severity="high", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2015-0204", url="https://nvd.nist.gov/vuln/detail/CVE-2015-0204",
           project="openssl", commit="", simplification="剥离 RSA 密钥交换主体，以等价交换参数检查状态机镜像『服务器提供 export 弱密钥未被拒绝』核心缺陷"),
  trigger="客户端请求普通套件，服务器却返回 512 位 export RSA 临时密钥",
  notes="CVE-2015-0204 (FREAK): ssl3_get_key_exchange 允许 RSA→EXPORT_RSA 降级（CVE 描述: conduct RSA-to-EXPORT_RSA downgrade attacks by offering a weak ephemeral RSA key in a noncompliant way）。纯逻辑错误，正确=拒绝、实际=接受 → 诚实标 miss。",
), r'''
#include <cstdio>
// CVE-2015-0204: 服务器提供 export 弱密钥未被客户端拒绝
struct KeyExchange {
    bool requested_export;   // 客户端实际请求的套件强度
    int  server_key_bits;    // 服务器返回的临时 RSA 密钥强度
};

static bool ssl3_get_key_exchange(const KeyExchange* kx) {
    /* DEFECT */ // 原始缺陷: 未校验 (requested_export && server_key_bits <= 512)
    //             与 (!requested_export && server_key_bits >= 1024) 的一致性
    return true;   // 任何服务器响应都被接受
}

int main() {
    KeyExchange kx{ false, 512 };   // 客户端要普通套件, 服务器只给 512 位 export 密钥
    bool accepted = ssl3_get_key_exchange(&kx);
    std::printf("key exchange %s: server_key_bits=%d requested_export=%d (正确行为: reject)\n",
                accepted ? "ACCEPT[错误]" : "reject", kx.server_key_bits, (int)kx.requested_export);
    return 0;
}
'''),

("G023", dict(
  defect_type="null_deref", func="tls12_choose_sig_alg", severity="high", planted=False,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2021-3449", url="https://nvd.nist.gov/vuln/detail/CVE-2021-3449",
           project="openssl", commit="", simplification="剥离 TLSv1.2 重协商全流程，保留『重协商 ClientHello 缺 signature_algorithms 扩展时保存指针为 NULL 仍被解引用』核心缺陷"),
  trigger="重协商 ClientHello 省略 signature_algorithms 扩展 → sig_algs 为 NULL",
  notes="CVE-2021-3449: TLSv1.2 重协商 ClientHello 省略 signature_algorithms 扩展时服务器崩溃（CVE 描述: may crash if sent a maliciously crafted renegotiation ClientHello ... omits the signature_algorithms extension）。",
), r'''
#include <cstdio>
// CVE-2021-3449: 重协商缺少 signature_algorithms 扩展 → NULL 解引用
struct ClientHello {
    const int* sig_algs;   // signature_algorithms 扩展内容
    int        sig_algs_len;
};

static int tls12_choose_sig_alg(const ClientHello* ch) {
    /* DEFECT */ // 原始缺陷: 重协商路径直接使用上次保存的指针, 未检查扩展是否存在
    return ch->sig_algs[0];
}

int main() {
    ClientHello initial{ new int[2]{ 4, 8 }, 2 };   // 首次握手带扩展
    ClientHello renego { 0, 0 };                    // crafted 重协商: 省略扩展
    tls12_choose_sig_alg(&initial);
    tls12_choose_sig_alg(&renego);                  // NULL[0] → SEGV
    delete[] initial.sig_algs;
    return 0;
}
'''),

("G024", dict(
  defect_type="race_condition", func="ssl3_get_new_session_ticket", severity="high", planted=False,
  verdict="catch", detectors=["tsan"],
  src=dict(type="cve", id="CVE-2015-1791", url="https://nvd.nist.gov/vuln/detail/CVE-2015-1791",
           project="openssl", commit="", simplification="剥离 SSL 连接层，保留『多线程客户端并发处理 NewSessionTicket 时会话对象无锁替换/释放』核心竞争"),
  trigger="两个线程同时处理 NewSessionTicket：无锁读写共享会话指针与成员",
  notes="CVE-2015-1791: ssl3_get_new_session_ticket 多线程客户端竞争（CVE 描述: Race condition in the ssl3_get_new_session_ticket ... double free and use-after-free）。TSan 捕获数据竞争。",
), r'''
#include <cstdio>
#include <thread>
// CVE-2015-1791: 多线程客户端并发处理 NewSessionTicket → 会话对象竞争
struct SslSession {
    int refcount;
    int ticket_age;
};

static SslSession* g_session = new SslSession{ 1, 0 };

static void ssl3_get_new_session_ticket(bool renew) {
    if (renew) {
        /* DEFECT */ // 原始缺陷: 无锁地读旧会话 → 构造新会话 → 替换 → 释放旧会话
        SslSession* ns = new SslSession{ 1, g_session->ticket_age + 1 };   // 竞争读
        SslSession* old = g_session;
        g_session = ns;                 // 竞争写
        delete old;                     // 并发线程同时走到这里 → double free / UAF
    } else {
        g_session->ticket_age++;        // 无锁读-改-写竞争
    }
}

int main() {
    std::thread a([]{ for (int i = 0; i < 200000; ++i) ssl3_get_new_session_ticket(i % 4 == 0); });
    std::thread b([]{ for (int i = 0; i < 200000; ++i) ssl3_get_new_session_ticket(i % 4 == 1); });
    a.join();
    b.join();
    std::printf("session age=%d\n", g_session->ticket_age);
    delete g_session;
    return 0;
}
'''),

("G025", dict(
  defect_type="heap_overflow", func="SSL_set_SSL_CTX", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2026-72897", url="https://nvd.nist.gov/vuln/detail/CVE-2026-72897",
           project="openssl", commit="", simplification="基于 2026-09-29 官方公告描述（握手中途 SSL_set_SSL_CTX 且新上下文签名算法更多时证书槽位数组越界读写）以用户态等价结构重构，非原始代码镜像，故标 planted=true"),
  trigger="握手中途把 SSL_CTX 切换为签名算法更多的上下文，证书槽位按新数量写入旧容量数组",
  notes="CVE-2026-72897: SSL_set_SSL_CTX 证书槽位越界读写 → 堆损坏（官方公告: certificate slot array out-of-bounds read/write, heap corruption）。用户态等价重构（planted=true）。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2026-72897: SSL_set_SSL_CTX 证书槽位数组越界（用户态等价重构）
struct SslCtx {
    int            num_sig_algs;   // 该上下文支持的签名算法数
    unsigned char* cert_slots;     // 证书槽位数组(每个签名算法一个槽)
    int            slots_cap;
};

static void SSL_set_SSL_CTX(SslCtx** cur, SslCtx* new_ctx) {
    *cur = new_ctx;
    /* DEFECT */ // 原始缺陷: 之后按 new_ctx->num_sig_algs 索引/填充证书槽位,
    //             但槽位数组可能仍按旧上下文容量分配
}

int main() {
    SslCtx old_ctx{ 2, new unsigned char[2]{ 0, 0 }, 2 };
    SslCtx new_ctx{ 8, new unsigned char[2]{ 0, 0 }, 2 };   // 新上下文算法更多, 槽位同样只有 2
    SslCtx* active = &old_ctx;
    SSL_set_SSL_CTX(&active, &new_ctx);
    for (int i = 0; i < active->num_sig_algs; ++i)
        active->cert_slots[i] = (unsigned char)i;   /* DEFECT */ // i>=2 越界写 → 堆溢出
    std::printf("slots[0]=%d\n", active->cert_slots[0]);
    return 0;
}
'''),
]
