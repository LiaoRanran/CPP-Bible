// RW-102 | CVE-2020-8177 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-8177
// project_url: https://curl.se/
// year: 2020 | severity: MEDIUM | source_type: cve
// mechanism: curl -J（Content-Disposition 文件名）与 -i 组合时用服务器提供的
//   文件名覆盖本地已有文件（本地文件覆盖）。
// notes: 最小重构（文件名选取逻辑）。
#include <cstdio>
#include <string>

struct HttpResp {
    std::string content_disposition_filename;   // attacker-controlled header
    bool include_headers_flag;                  // user passed -i
};

// BUG: with -i, curl wrote headers to the file first and used the server name
// with overwrite; crafted filename "existing.txt" clobbers local files.
std::string choose_output_file(const HttpResp& r, const std::string& local_default) {
    if (!r.content_disposition_filename.empty()) {
        // BUG: no check whether the file exists; server controls the name
        return r.content_disposition_filename;
    }
    return local_default;
}

int main() {
    HttpResp r{"important-local-file.conf", true};
    std::string f = choose_output_file(r, "download.bin");
    std::printf("writing to: %s (server-chosen, overwrite)\n", f.c_str());
    return 0;
}
