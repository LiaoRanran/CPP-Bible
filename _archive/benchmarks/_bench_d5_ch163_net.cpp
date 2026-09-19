// _bench_d5_ch163_net.cpp
// D5 benchmark: Serialization — manual byte-pack vs struct memcpy vs length-prefixed framing
#include <cstdio>
#include <chrono>
#include <cstring>

volatile int g_sink = 0;

// --- Manual byte-pack ---
#pragma pack(push, 1)
struct Packet {
    uint32_t len;
    uint16_t type;
    int32_t payload[4];
};
#pragma pack(pop)

[[gnu::noinline]] int bench_manual_pack(int N) {
    char buf[64];
    int acc = 0;
    for (int i = 0; i < N; i++) {
        uint32_t len = 20;
        uint16_t type = 1;
        int32_t data[4] = {i, i+1, i+2, i+3};
        memcpy(buf+0, &len, 4);
        memcpy(buf+4, &type, 2);
        memcpy(buf+6, data, 16);
        acc += buf[6];
    }
    return acc;
}

// --- Struct memcpy ---
[[gnu::noinline]] int bench_struct_memcpy(int N) {
    char buf[64];
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Packet pkt;
        pkt.len = 20;
        pkt.type = 1;
        pkt.payload[0] = i; pkt.payload[1] = i+1;
        pkt.payload[2] = i+2; pkt.payload[3] = i+3;
        memcpy(buf, &pkt, sizeof(pkt));
        acc += buf[6];
    }
    return acc;
}

// --- Length-prefixed framing with header scan ---
[[gnu::noinline]] int bench_length_prefix(int N) {
    char buf[256];
    // Simulate a stream of 4 packets packed together
    int acc = 0;
    for (int i = 0; i < N; i++) {
        int offset = 0;
        for (int j = 0; j < 4; j++) {
            uint32_t len = 20;
            uint16_t type = j;
            memcpy(buf+offset, &len, 4); offset += 4;
            memcpy(buf+offset, &type, 2); offset += 2;
            int32_t val = i + j;
            memcpy(buf+offset, &val, 4); offset += 4;
            memcpy(buf+offset, &val, 4); offset += 4;
            memcpy(buf+offset, &val, 4); offset += 4;
        }
        // Parse back: scan length-prefixed frames
        int pos = 0;
        while (pos < offset) {
            uint32_t flen;
            memcpy(&flen, buf+pos, 4);
            acc += buf[pos + 6];
            pos += flen;
        }
    }
    return acc;
}

// --- Individual field copy (no struct) ---
[[gnu::noinline]] int bench_field_copy(int N) {
    char buf[64];
    int acc = 0;
    for (int i = 0; i < N; i++) {
        buf[0] = 20; buf[1] = 0; buf[2] = 0; buf[3] = 0;
        buf[4] = 1; buf[5] = 0;
        buf[6] = i & 0xFF;
        acc += buf[6];
    }
    return acc;
}

int main() {
    const int N = 5000000;

    volatile int w = bench_manual_pack(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"manual byte-pack",    bench_manual_pack,    0},
        {"struct memcpy",       bench_struct_memcpy,  0},
        {"length-prefix frame", bench_length_prefix,  0},
        {"field-by-field copy", bench_field_copy,     0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(N);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch163 net D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.3f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[1].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
