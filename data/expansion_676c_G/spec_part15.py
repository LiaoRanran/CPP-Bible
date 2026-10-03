# -*- coding: utf-8 -*-
# 676c-G spec part15: 内核 CVE 用户态等价 asan/tsan 组 (G081-G087)
PART = [
("G081", dict(
  defect_type="use_after_free", func="join_session_keyring", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-0728", url="https://nvd.nist.gov/vuln/detail/CVE-2016-0728",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（join_session_keyring 在错误路径 mishandles object references → 引用计数泄漏 + UAF）做用户态等价模拟，planted=true"),
  trigger="多次 join 失败泄漏引用计数，维护方按计数归零释放对象，残留 join 路径继续使用",
  notes="CVE-2016-0728: 内核 keyring 引用计数错误 → UAF/提权。本样本为用户态等价模拟：失败路径不回滚引用计数，对象被提前释放后仍被使用。",
), r'''
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
'''),

("G082", dict(
  defect_type="use_after_free", func="mq_notify_retry", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2017-11176", url="https://nvd.nist.gov/vuln/detail/CVE-2017-11176",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（mq_notify 进入重试逻辑时未把 sock 指针置 NULL → socket close 后 UAF）做用户态等价模拟，planted=true"),
  trigger="netlink socket 关闭释放 sock 对象后，通知重试路径仍解引用该指针",
  notes="CVE-2017-11176: mq_notify 未在重试路径置空 sock 指针 → UAF。用户态等价模拟：close 路径释放对象，retry 路径仍使用。",
), r'''
#include <cstdio>
// CVE-2017-11176 (用户态等价): mq_notify 重试路径未置空 sock → UAF
struct NetlinkSock {
    int fd;
    int state;
};

struct Notify {
    NetlinkSock* sock;   // 原始缺陷: 进入重试逻辑时未置 NULL
    bool retrying;
};

static void netlink_sock_close(Notify* n) {
    delete n->sock;      // 用户态 close: 释放 socket 对象
    std::printf("sock closed\n");
}

static void mq_notify_retry(Notify* n) {
    /* DEFECT */ if (n->sock->fd >= 0)        // sock 已释放仍解引用 → UAF
        n->sock->state = 1;
    std::printf("retry done, state=%d\n", n->sock->state);
}

int main() {
    Notify n{ new NetlinkSock{ 7, 0 }, true };
    netlink_sock_close(&n);    // 关闭 socket
    mq_notify_retry(&n);       // 重试路径仍使用已释放的 sock
    return 0;
}
'''),

("G083", dict(
  defect_type="type_confusion", func="sk_clone_lock", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2018-9568", url="https://nvd.nist.gov/vuln/detail/CVE-2018-9568",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（sk_clone_lock 因类型混淆导致内存损坏）做用户态等价模拟：小结构体按大结构体整块拷贝，planted=true"),
  trigger="INET socket 克隆按 Bluetooth 大结构体整块拷贝 → 读越界",
  notes="CVE-2018-9568 (WrongSize): sk_clone_lock 类型混淆内存损坏。用户态等价模拟：以大结构体尺寸拷贝小结构体。",
), r'''
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
'''),

("G084", dict(
  defect_type="double_free", func="snd_usbmidi_create", severity="high", planted=True,
  verdict="catch", detectors=["asan"],
  src=dict(type="cve", id="CVE-2016-2384", url="https://nvd.nist.gov/vuln/detail/CVE-2016-2384",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（snd_usbmidi_create 无效 USB 描述符错误路径 double free）做用户态等价模拟，planted=true"),
  trigger="无效 USB 描述符触发错误路径释放接口对象，调用方再次释放",
  notes="CVE-2016-2384: snd_usbmidi_create double free（CVE 描述: Double free vulnerability in the snd_usbmidi_create function ... via vectors involving an invalid USB descriptor）。用户态等价模拟。",
), r'''
#include <cstdio>
// CVE-2016-2384 (用户态等价): 错误路径与调用方双重释放 USB 接口对象
struct UsbInterface {
    int refs;
};

static void usb_if_put(UsbInterface* iface) {
    delete iface;
}

static int snd_usbmidi_create(UsbInterface* iface, bool invalid_descriptor) {
    if (invalid_descriptor) {
        /* DEFECT */ usb_if_put(iface);   // 错误路径释放(第一次)
        std::printf("usbmidi: error path freed interface\n");
        return -1;
    }
    return 0;
}

int main() {
    UsbInterface* iface = new UsbInterface{ 1 };
    // crafted USB 设备: MIDI 端点描述符无效
    if (snd_usbmidi_create(iface, true) < 0) {
        usb_if_put(iface);   /* DEFECT */ // 调用方错误处理再次释放 → double free
    }
    return 0;
}
'''),

("G085", dict(
  defect_type="race_condition", func="n_tty_write", severity="high", planted=True,
  verdict="catch", detectors=["tsan"],
  src=dict(type="cve", id="CVE-2014-0196", url="https://nvd.nist.gov/nvd/detail/CVE-2014-0196",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（n_tty_write 未正确管理 tty 访问 → 并发写内存损坏）做用户态等价模拟：两线程无锁并发写共享 tty 缓冲与游标，planted=true"),
  trigger="两个线程同时向同一 tty 缓冲无锁写入",
  notes="CVE-2014-0196: n_tty_write 并发写竞争（CVE 描述: does not properly manage tty driver access in the LECHO & !OPOST case ... memory corruption）。用户态等价模拟，TSan 捕获。",
), r'''
#include <cstdio>
#include <cstring>
#include <thread>
// CVE-2014-0196 (用户态等价): n_tty_write 无锁并发写 tty 缓冲
struct Tty {
    char  write_buf[256];
    int   write_cnt;      // 游标(应由锁保护)
};

static Tty g_tty;

static void n_tty_write(const char* data, int len) {
    for (int i = 0; i < len; ++i) {
        /* DEFECT */ // 原始缺陷: 无锁访问 tty 缓冲
        g_tty.write_buf[g_tty.write_cnt++ % 256] = data[i];   // 并发 RMW 竞争
    }
}

int main() {
    std::thread a([]{ for (int i = 0; i < 200000; ++i) n_tty_write("AAAA", 4); });
    std::thread b([]{ for (int i = 0; i < 200000; ++i) n_tty_write("BBBB", 4); });
    a.join();
    b.join();
    std::printf("write_cnt=%d\n", g_tty.write_cnt);
    return 0;
}
'''),

("G086", dict(
  defect_type="race_condition", func="n_hdlc_release", severity="high", planted=True,
  verdict="catch", detectors=["tsan"],
  src=dict(type="cve", id="CVE-2017-2636", url="https://nvd.nist.gov/vuln/detail/CVE-2017-2636",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（n_hdlc 竞态 → double free）做用户态等价模拟：两线程无锁竞争释放同一缓冲块，planted=true"),
  trigger="两线程同时检查 busy 标志并释放同一 flip buffer → 竞争 + 双重释放",
  notes="CVE-2017-2636: n_hdlc 竞态条件（CVE 描述: Race condition in drivers/tty/n_hdlc.c ... gain privileges or cause a denial of service (double free) by setting the HDLC line discipline）。用户态等价模拟，TSan 捕获。",
), r'''
#include <cstdio>
#include <thread>
// CVE-2017-2636 (用户态等价): n_hdlc flip buffer 无锁竞争释放
struct HdlcBuf {
    bool busy;
    int  len;
};

static HdlcBuf* g_active = new HdlcBuf{ true, 128 };
static HdlcBuf* g_free_list = 0;

static void n_hdlc_flush(bool writer) {
    /* DEFECT */ // 原始缺陷: busy 标志的检查与释放无锁
    if (g_active->busy && writer) {
        HdlcBuf* b = g_active;
        g_active = 0;
        delete b;                          // 线程 A 释放
    } else if (g_active) {
        delete g_active;                   // 线程 B 也释放同一对象 → double free / UAF
        g_active = 0;
    }
}

int main() {
    std::thread a([]{ for (int i = 0; i < 100000; ++i) if (!g_active) g_active = new HdlcBuf{ true, 128 }; n_hdlc_flush(true); });
    std::thread b([]{ for (int i = 0; i < 100000; ++i) { if (g_active) n_hdlc_flush(false); } });
    a.join();
    b.join();
    std::printf("done\n");
    return 0;
}
'''),

("G087", dict(
  defect_type="race_condition", func="gup_cow_write", severity="high", planted=True,
  verdict="catch", detectors=["tsan"],
  src=dict(type="cve", id="CVE-2016-5195", url="https://nvd.nist.gov/vuln/detail/CVE-2016-5195",
           project="linux-kernel", commit="", simplification="内核漏洞无法在用户态直接复现：按 CVE 描述（GUP 与 COW 处理的竞态允许写只读映射）做用户态等价模拟：写线程与 COW 失效线程无锁竞争同一页对象，planted=true"),
  trigger="写线程反复写共享页，失效线程反复置只读标志，两者无锁竞争",
  notes="CVE-2016-5195 (Dirty COW): GUP/COW 竞态（CVE 描述: Race condition in mm/gup.c ... leveraging incorrect handling of a copy-on-write (COW) feature to write to a read-only memory mapping）。用户态等价模拟，TSan 捕获。",
), r'''
#include <cstdio>
#include <thread>
// CVE-2016-5195 (用户态等价): 写线程与 COW 失效线程竞争页状态
struct Page {
    bool readonly;      // 页状态(应由锁保护)
    int  content;
};

static Page g_page{ true, 0 };

static void attacker_write_thread() {
    for (int i = 0; i < 300000; ++i) {
        /* DEFECT */ // 原始缺陷: GUP 取到的页在写入前可被 COW 失效, 无一致性检查
        if (!g_page.readonly)
            g_page.content = 0x1337;    // 写"只读"映射
        else
            g_page.content = 1;
    }
}

static void cow_invalidate_thread() {
    for (int i = 0; i < 300000; ++i) {
        g_page.readonly = true;         // COW 失效: 置只读(与写线程竞争)
        g_page.readonly = false;
    }
}

int main() {
    std::thread a(attacker_write_thread);
    std::thread b(cow_invalidate_thread);
    a.join();
    b.join();
    std::printf("content=%d\n", g_page.content);
    return 0;
}
'''),
]
