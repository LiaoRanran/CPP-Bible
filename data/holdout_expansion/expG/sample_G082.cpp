// sample_G082
// defect_type: race_condition
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// source: CVE-2014-0196 (https://nvd.nist.gov/nvd/detail/CVE-2014-0196) [linux-kernel]
// (authoritative annotation in sample_G082.json)
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
