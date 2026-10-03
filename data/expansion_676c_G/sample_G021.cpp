// sample_G021
// defect_type: state_machine
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2014-0224 (https://nvd.nist.gov/vuln/detail/CVE-2014-0224) [openssl]
// (authoritative annotation in sample_G021.json)
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
