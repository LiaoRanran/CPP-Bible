// RW-050 | CVE-2016-1897 | FFmpeg | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-1897
// project_url: https://ffmpeg.org/
// year: 2016 | severity: MEDIUM | source_type: cve
// mechanism: HLS 播放列表解析允许 "concat:" 协议 + 本地文件路径，攻击者控制的
//   播放列表可读取服务器本地文件（SSRF/文件泄露）。
// notes: 最小重构（只演示路径判定缺陷）。
#include <cstdio>
#include <string>

struct HlsPlaylist {
    std::string base_url;
    std::string segment_uri;    // attacker-controlled line in the m3u8
};

// BUG: the "protocol allow-list" check only rejects plain "file:" URIs;
// "concat:file:///etc/passwd" and relative escapes slip through.
bool uri_allowed(const std::string& uri) {
    if (uri.rfind("file:", 0) == 0) return false;   // naive check
    return true;                                     // concat:/http:-with-host tricks pass
}

std::string resolve_uri(const HlsPlaylist& p) {
    if (!uri_allowed(p.segment_uri)) return "";
    if (p.segment_uri.find("://") == std::string::npos) {
        return p.base_url + "/" + p.segment_uri;     // no traversal normalization
    }
    return p.segment_uri;
}

int main() {
    HlsPlaylist p{"http://cdn.example/hls", "concat:file:///etc/passwd|file:///etc/shadow"};
    std::string resolved = resolve_uri(p);
    std::printf("resolved URI: %s\n", resolved.c_str());
    std::printf("local file content would be exposed: %s\n",
                resolved.find("etc/passwd") != std::string::npos ? "YES" : "no");
    return 0;
}
