// sample_G043
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2020-8177 (https://nvd.nist.gov/vuln/detail/CVE-2020-8177) [curl]
// (authoritative annotation in sample_G043.json)
#include <cstdio>
#include <string>
// CVE-2020-8177: -J 使用服务器提供的文件名且不做覆盖检查
struct Download {
    std::string out_file;          // 用户指定的输出文件
    bool        content_dispo;     // 服务器是否返回 Content-Disposition
    std::string server_filename;   // 服务器提供的文件名
};

static std::string choose_output_name(const Download* d, bool file_exists) {
    if (d->content_dispo && !d->server_filename.empty()) {
        /* DEFECT */ // 原始缺陷: -J 时直接采用服务器文件名, 不检查 file_exists
        return d->server_filename;
    }
    return d->out_file;
}

int main() {
    Download d{ ".bashrc", true, ".bashrc" };   // 恶意服务器指向用户已有文件
    bool exists = true;
    std::string target = choose_output_name(&d, exists);
    std::printf("写入目标: %s (文件已存在: %s)\n", target.c_str(), exists ? "是" : "否");
    std::printf("(正确行为: 目标已存在时应中止或改名, 不覆盖)\n");
    return 0;
}
