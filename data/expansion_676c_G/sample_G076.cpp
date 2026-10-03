// sample_G076
// defect_type: state_machine
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2023-48795 (https://nvd.nist.gov/vuln/detail/CVE-2023-48795) [openssh]
// (authoritative annotation in sample_G076.json)
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
