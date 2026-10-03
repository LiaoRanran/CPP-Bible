# -*- coding: utf-8 -*-
# 676c-G spec part16: 内核/openssl miss 组 + h2 资源耗尽 (G088-G092)
PART = [
("G088", dict(
  defect_type="logic_error", func="pipe_buffer_reuse", severity="high", planted=True,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2022-0847", url="https://nvd.nist.gov/vuln/detail/CVE-2022-0847",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（pipe_buffer.flags 未初始化沿用脏值 → 获得不该有的 CAN_MERGE 权限写穿页缓存）做用户态等价模拟，planted=true"),
  trigger="复用 pipe_buffer 槽位时 flags 未清空，沿用上一轮的 PIPE_BUF_CAN_MERGE → 对他人页面追加写入",
  notes="CVE-2022-0847 (Dirty Pipe): pipe_buffer.flags 缺少初始化（CVE 描述: the 'flags' member of the new pipe buffer structure was lacking proper initialization ... could thus contain stale values）。用户态等价模拟，可观察越权写入 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <cstring>
// CVE-2022-0847 (用户态等价): pipe_buffer.flags 脏值 → 越权合并写
static const int PIPE_BUF_CAN_MERGE = 0x10;

struct PipeBuffer {
    int  flags;       // 原始缺陷: 新槽位未初始化 → 沿用脏值
    char page[32];
    int  page_owner;  // 该页当前归属的"文件"
};

static PipeBuffer g_ring[2];
static int g_victim_content = 0;

static void pipe_write_init_slot(int idx, const char* data, int owner) {
    /* DEFECT */ // 原始缺陷: flags 未初始化(copy_page_to_iter_pipe 路径)
    g_ring[idx].page_owner = owner;
    std::strncpy(g_ring[idx].page, data, 31);
}

int main() {
    // 第 1 轮: 槽位 0 写满, flags 被置为 CAN_MERGE(本轮合法)
    g_ring[0].flags = PIPE_BUF_CAN_MERGE;
    pipe_write_init_slot(0, "DATA-ROUND-1", 1);
    // 页被回收到页池并转分配给"受害文件"(页内容被替换)
    g_ring[0].flags = 0;                     // ← 注意: 真实缺陷是这里【没有】清 flags
    g_ring[0].flags = PIPE_BUF_CAN_MERGE;    // 模拟脏值残留
    pipe_write_init_slot(0, "DATA-ROUND-2", 2);   // 页 now 归属受害文件
    // 第 2 轮: 因为 flags 仍是 CAN_MERGE(脏值), 写入越过本文件数据边界,
    // 直接改写页内"受害文件"的内容 —— 页缓存被穿透
    g_victim_content = 42;
    std::strncpy(g_ring[0].page + 12, "HACKED", 7);   // 越过 round-2 数据边界写
    std::printf("victim page content after write: %s (期望: DATA-ROUND-2 前缀完好)\n",
                g_ring[0].page);
    std::printf("(正确行为: 新 pipe_buffer 的 flags 必须清零, 不可合并写)\n");
    return 0;
}
'''),

("G089", dict(
  defect_type="timing_side_channel", func="dsa_sign_setup", severity="medium", planted=True,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2016-2178", url="https://nvd.nist.gov/vuln/detail/CVE-2016-2178",
           project="openssl", commit="", simplification="基于 CVE 描述（dsa_sign_setup 未确保常量时间操作 → 时序侧信道泄露 DSA 私钥）以数据相关分支计数的等价机制重构，非原始代码镜像，故标 planted=true"),
  trigger="不同 k 值的模乘操作数位模式不同 → 操作计数差异可被测量",
  notes="CVE-2016-2178: dsa_sign_setup 非常量时间（CVE 描述: does not properly ensure the use of constant-time operations ... discover a DSA private key via a timing side-channel attack）。侧信道类，sanitizer 无报告 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <cstdint>
// CVE-2016-2178 (等价重构): 非常量时间模乘 → 时序侧信道
static long g_op_count = 0;    // 模拟可测量的操作计数(时序)

static unsigned int mont_mul_nonct(unsigned int a, unsigned int b, unsigned int n) {
    unsigned int r = 0;
    for (int i = 0; i < 32; ++i) {
        /* DEFECT */ // 原始缺陷: 分支依赖秘密数据的位模式
        if ((b >> i) & 1u) { r = (r + a) % n; g_op_count += 3; }
        else               g_op_count += 1;
        a = (a + a) % n;
    }
    return r;
}

int main() {
    unsigned int n = 0xFFFFFFFBu;
    g_op_count = 0;
    mont_mul_nonct(1234567u, 0x55555555u, n);      // k1: 位模式稀疏
    long ops1 = g_op_count;
    g_op_count = 0;
    mont_mul_nonct(1234567u, 0xFFFFFFFFu, n);      // k2: 位模式全 1
    long ops2 = g_op_count;
    std::printf("ops(k1)=%ld ops(k2)=%ld 差异=%ld (应恒等: 常量时间缺失)\n",
                ops1, ops2, ops2 - ops1);
    return 0;
}
'''),

("G090", dict(
  defect_type="logic_error", func="evp_ocb_encrypt", severity="medium", planted=False,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2022-2097", url="https://nvd.nist.gov/vuln/detail/CVE-2022-2097",
           project="openssl", commit="", simplification="剥离 OCB 主体，按 CVE 描述（部分数据未被加密）保留『非完整块尾部未加密』核心缺陷"),
  trigger="20 字节输入: 前 16 字节加密, 尾部 4 字节明文残留",
  notes="CVE-2022-2097: AES OCB 模式部分数据未加密（CVE 描述: AES OCB mode ... encrypting large amounts of data does not encrypt the entire portion）。逻辑缺陷，正确=全量加密、实际=尾部残留明文 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2022-2097: OCB 加密对非完整块尾部未加密
static const size_t BLK = 16;

static void evp_ocb_encrypt(const unsigned char* in, unsigned char* out, size_t len) {
    size_t full = len - (len % BLK);
    for (size_t i = 0; i < full; ++i)
        out[i] = (unsigned char)(in[i] ^ 0x5A);    // 逐块加密(简化)
    /* DEFECT */ // 原始缺陷: 尾部不完整块被跳过, 明文原样保留在 out
}

int main() {
    unsigned char in[20] = "TOPSECRET-DATA-999";
    unsigned char out[20];
    evp_ocb_encrypt(in, out, 20);
    std::printf("out[0..3]=%c%c%c%c (encrypted)\n", out[0], out[1], out[2], out[3]);
    std::printf("out[16..19]=%c%c%c%c (应为密文, 实为明文残留)\n", out[16], out[17], out[18], out[19]);
    std::printf("(正确行为: 20 字节应全部被加密)\n");
    return 0;
}
'''),

("G091", dict(
  defect_type="resource_exhaustion", func="h2_on_reset_flood", severity="medium", planted=True,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2019-9514", url="https://nvd.nist.gov/vuln/detail/CVE-2019-9514",
           project="http2", commit="", simplification="协议级 DoS 无法在用户态完整复现：按 CVE 描述（reset flood: 攻击者反复开流并发送应触发 RST_STREAM 的请求，服务端无上限处理）做有界等价模拟，planted=true"),
  trigger="攻击者 10000 次开流+立即 reset，服务端为每个 reset 无上限重建流对象",
  notes="CVE-2019-9514: HTTP/2 reset flood（CVE 描述: The attacker opens a number of streams and sends an invalid request over each stream that should solicit a stream of RST_STREAM frames from the peer ... uncontrolled resource consumption, CWE-400）。资源耗尽类，sanitizer 无报告 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <vector>
// CVE-2019-9514 (有界模拟): HTTP/2 reset flood → 流对象无上限增长
struct H2Stream {
    int  id;
    bool reset_pending;
};

static std::vector<H2Stream*> g_open_streams;

static void h2_on_incoming_stream(int id, bool invalid_request) {
    H2Stream* s = new H2Stream{ id, false };
    g_open_streams.push_back(s);
    if (invalid_request) {
        /* DEFECT */ // 原始缺陷: 服务端为每个待 reset 的流保留/重建对象, 无速率限制
        s->reset_pending = true;
        g_open_streams.push_back(new H2Stream{ id + 1000000, false });   // reset 触发新对象
    }
}

int main() {
    // 攻击者: 10000 次开流 + 立即 reset(有界模拟, 原始为持续洪泛)
    for (int i = 0; i < 10000; ++i)
        h2_on_incoming_stream(i, true);
    std::printf("open_streams=%zu (正确行为: 服务端应限流, 例如 <= 100)\n", g_open_streams.size());
    for (H2Stream* s : g_open_streams) delete s;   // 进程结束回收(缺陷本质是运行期无上限)
    return 0;
}
'''),

("G092", dict(
  defect_type="resource_exhaustion", func="h2_on_settings_flood", severity="medium", planted=True,
  verdict="miss", detectors=["ubsan"],
  src=dict(type="cve", id="CVE-2019-9512", url="https://nvd.nist.gov/vuln/detail/CVE-2019-9512",
           project="http2", commit="", simplification="协议级 DoS 无法在用户态完整复现：按 CVE 描述（flood of SETTINGS frames: 对端持续发送 SETTINGS 且无速率限制处理）做有界等价模拟，planted=true"),
  trigger="攻击者持续发送 SETTINGS 帧，服务端为每帧排队处理对象无上限",
  notes="CVE-2019-9512: HTTP/2 SETTINGS flood（CVE 描述: flood of SETTINGS frames ... uncontrolled resource consumption, CWE-400）。资源耗尽类 → 诚实标 miss。",
), r'''
#include <cstdio>
#include <vector>
// CVE-2019-9512 (有界模拟): HTTP/2 SETTINGS 帧洪泛 → 处理队列无上限增长
struct H2SettingsFrame {
    int  n_settings;
    bool ack_required;
};

static std::vector<H2SettingsFrame*> g_pending_settings;

static void h2_on_settings_frame(int n_settings) {
    /* DEFECT */ // 原始缺陷: 每帧都分配处理对象入队, 无速率限制/队列上限
    g_pending_settings.push_back(new H2SettingsFrame{ n_settings, true });
}

int main() {
    // 攻击者: 持续发送 SETTINGS(有界模拟 20000 帧)
    for (int i = 0; i < 20000; ++i)
        h2_on_settings_frame(6);
    std::printf("pending settings frames=%zu (正确行为: 队列应有上限或丢弃策略)\n",
                g_pending_settings.size());
    for (H2SettingsFrame* f : g_pending_settings) delete f;
    return 0;
}
'''),
]
