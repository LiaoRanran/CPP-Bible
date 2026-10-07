// RW-059 | CVE-2022-31747 | Firefox | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-31747
// project_url: https://www.mozilla.org/firefox/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: WebRTC 媒体通道关闭竞态：track 已被释放，统计回调仍访问其一
//   （释放后使用）。
// notes: 最小重构（含真实线程竞态窗口）。ASan 可命中 UAF；TSan 也可能报竞争。
#include <cstdio>
#include <cstring>
#include <thread>
#include <vector>

struct MediaTrack {
    int id;
    char kind[16];
};

std::vector<MediaTrack*> g_pending_stats;   // stats polls hold track refs

void stats_poll_once() {
    for (MediaTrack* t : g_pending_stats) {
        std::printf("stats: track %d kind %s\n", t->id, t->kind); // touch after free
    }
}

int main() {
    MediaTrack* track = new MediaTrack{7, {0}};
    std::strcpy(track->kind, "video");
    g_pending_stats.push_back(track);

    std::thread closer([track] {
        // channel closed on another thread while stats poll scheduled
        delete track;                        // freed concurrently
    });
    stats_poll_once();                       // use-after-free read
    closer.join();
    return 0;
}
