// sample_G045
// defect_type: logic_error
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2015-3148 (https://nvd.nist.gov/vuln/detail/CVE-2015-3148) [curl]
// (authoritative annotation in sample_G045.json)
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
