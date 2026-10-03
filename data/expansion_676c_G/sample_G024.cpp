// sample_G024
// defect_type: race_condition
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: tsan
// source: CVE-2015-1791 (https://nvd.nist.gov/vuln/detail/CVE-2015-1791) [openssl]
// (authoritative annotation in sample_G024.json)
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
