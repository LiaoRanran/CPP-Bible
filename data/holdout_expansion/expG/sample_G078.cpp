// sample_G078
// defect_type: use_after_free
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2016-0728 (https://nvd.nist.gov/vuln/detail/CVE-2016-0728) [linux-kernel]
// (authoritative annotation in sample_G078.json)
#include <cstdio>
// CVE-2016-0728 (用户态等价): 失败路径引用计数未回滚 → 对象提前释放后仍被使用
struct SessionKeyring {
    int ref;
};

static SessionKeyring* g_ring = 0;

static bool join_session_keyring(bool fail) {
    /* DEFECT */ g_ring->ref++;       // 原始缺陷: 失败路径不回滚引用计数
    if (fail) return false;
    return true;
}

int main() {
    g_ring = new SessionKeyring{ 1 };
    join_session_keyring(true);      // 引用计数泄漏
    join_session_keyring(true);
    g_ring->ref = 0;                 // 会话重置: 维护方按 ref==0 释放
    delete g_ring;
    join_session_keyring(false);     /* DEFECT */ // 残留 join 路径使用已释放对象 → UAF
    std::printf("ref=%d\n", g_ring->ref);
    return 0;
}
