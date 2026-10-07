// RW-058 | CVE-2020-26969 | Firefox | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-26969
// project_url: https://www.mozilla.org/firefox/
// year: 2020 | severity: HIGH | source_type: cve
// mechanism: WebRender 对畸形显示列表（display list）的边界处理缺陷，
//   内存破坏（渲染进程沙箱内）。
// notes: 最小重构。ASan 应报越界。
#include <cstdio>
#include <vector>

struct DisplayItem {
    float x, y, w, h;
    unsigned clip_id;      // crafted: out-of-range clip index
};

struct ClipStack {
    float clips[4][4];     // fixed clip table
    unsigned count;
};

// BUG: clip_id from the display list indexes the fixed clip table unchecked.
void apply_clip(const ClipStack& cs, const DisplayItem& item) {
    const float* clip = cs.clips[item.clip_id];            // OOB index
    std::printf("clip = [%f %f %f %f] for item at (%f,%f)\n",
                clip[0], clip[1], clip[2], clip[3], item.x, item.y);
}

int main() {
    ClipStack cs{};
    cs.count = 4;
    DisplayItem item{0, 0, 100, 100, 9001};                // crafted clip_id
    apply_clip(cs, item);
    return 0;
}
