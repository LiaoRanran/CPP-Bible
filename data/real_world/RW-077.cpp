// RW-077 | CVE-2024-1086 | Linux kernel | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2024-1086
// project_url: https://www.kernel.org/
// year: 2024 | severity: HIGH | source_type: cve
// mechanism: nf_tables nft_verdict_init 允许正数 drop error 导致双重释放，
//   nf_hook_slow 中对已释放 skb 再次释放（在野利用）。
// notes: 最小重构 —— **用户态复刻** skb 引用计数/哈希表清理顺序。
#include <cstdio>
#include <cstring>

struct Skb {
    int refcnt;
    char payload[24];
};

struct NftHook {
    Skb* pending;     // skb that will be dropped
    bool dropped;     // drop verdict delivered
};

// BUG: positive errno from the verdict path triggers the "drop" branch, then
// the generic cleanup destroys the same skb a second time.
void nf_hook_slow(NftHook& h) {
    if (h.dropped) {
        delete h.pending;              // first free (drop path)
    }
}

int main() {
    NftHook h{};
    h.pending = new Skb{1, {0}};
    std::strcpy(h.pending->payload, "netlink-attacker");
    // crafted verdict: positive error => drop flag set, but pointer not cleared
    h.dropped = true;
    nf_hook_slow(h);
    delete h.pending;                  // second free (generic cleanup)
    std::printf("skb destroyed twice\n");
    return 0;
}
