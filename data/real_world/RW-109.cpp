// RW-109 | CVE-2018-10933 | libssh | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2018-10933
// project_url: https://www.libssh.org/
// year: 2018 | severity: HIGH | source_type: cve
// mechanism: 认证状态机缺陷 —— 服务器在接受 SSH_MSG_USERAUTH_SUCCESS（本应只
//   由服务端发出）后直接进入认证成功状态，客户端可伪造认证成功报文绕过。
// notes: 最小重构（消息方向/状态机判定缺失）。
#include <cstdio>

enum AuthState { AUTH_NONE, AUTH_IN_PROGRESS, AUTH_SUCCESS };

struct SshServerSession {
    AuthState state;
    bool msg_from_client;
};

// BUG: on_msg checks message type, not direction; a client-sent
// USERAUTH_SUCCESS flips the session to authenticated.
int on_msg(SshServerSession& s, int msg_type) {
    const int SSH_MSG_USERAUTH_SUCCESS = 52;
    if (msg_type == SSH_MSG_USERAUTH_SUCCESS) {
        // BUG: missing `if (!s.msg_from_client) return -1;` direction check
        s.state = AUTH_SUCCESS;
        std::printf("state := AUTH_SUCCESS (msg_from_client=%s) -- bug\n",
                    s.msg_from_client ? "true" : "false");
        return 0;
    }
    s.state = AUTH_IN_PROGRESS;
    return 0;
}

int main() {
    SshServerSession s{AUTH_NONE, true};    // attacker is the client
    on_msg(s, 52);                           // forged success message
    std::printf("authenticated without credentials: %s\n",
                s.state == AUTH_SUCCESS ? "YES (bug)" : "no");
    return 0;
}
