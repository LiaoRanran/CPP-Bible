// sample_G080
// defect_type: type_confusion
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-9568 (https://nvd.nist.gov/vuln/detail/CVE-2018-9568) [linux-kernel]
// (authoritative annotation in sample_G080.json)
#include <cstdio>
#include <cstring>
// CVE-2018-9568 (用户态等价): sk_clone_lock 类型混淆 → 按错误尺寸拷贝
struct SockCommon {          // 通用头(所有协议族的基类)
    int family;
    int state;
};

struct SockInet : SockCommon {    // INET socket: 24 字节
    int ports[4];
};

struct SockBluetooth : SockCommon {   // BLUETOOTH socket: 48 字节(更大)
    int bdaddr[6];
    int extra[8];
};

static SockBluetooth* sk_clone_lock(const SockCommon* proto) {
    SockBluetooth* nb = new SockBluetooth;
    std::memset(nb, 0, sizeof(*nb));
    /* DEFECT */ *nb = *static_cast<const SockBluetooth*>(proto);   // 小结构体按大结构体整块拷贝 → 读越界
    return nb;
}

int main() {
    SockInet src{ 2, 1, { 80, 443, 0, 0 } };
    SockBluetooth* cloned = sk_clone_lock(&src);   // 读 src 之后的栈内存 → 越界
    std::printf("cloned family=%d\n", cloned->family);
    delete cloned;
    return 0;
}
