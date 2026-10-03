// sample_G075
// defect_type: state_machine
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2018-10933 (https://nvd.nist.gov/vuln/detail/CVE-2018-10933) [libssh]
// (authoritative annotation in sample_G075.json)
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
