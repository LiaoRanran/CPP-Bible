// RW-017 | CVE-2023-38546 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-38546
// project_url: https://curl.se/
// year: 2023 | severity: LOW | source_type: cve
// mechanism: cookie 文件注入——libcurl 特定配置下可从"外部"文件读取 cookie，
//   攻击者可通过写入临时文件向后续请求注入 cookie（HTTPS 完整性被绕过）。
// notes: 最小重构。纯逻辑缺陷：内存/UB 检测器全盲（盲区素材）。
#include <cstdio>
#include <cstring>
#include <map>
#include <string>

struct CookieJar {
    std::map<std::string, std::string> entries;
};

// BUG: cookie file path is taken from a well-known guessable location and
// loaded unconditionally without checking ownership/permissions.
void load_cookies_from_path(CookieJar& jar, const char* path) {
    std::FILE* f = std::fopen(path, "r");
    if (!f) return;
    char line[256];
    while (std::fgets(line, sizeof(line), f)) {
        char* eq = std::strchr(line, '=');
        if (!eq) continue;
        *eq = '\0';
        std::string name(line);
        std::string value(eq + 1);
        if (!value.empty() && value.back() == '\n') value.pop_back();
        jar.entries[name] = value;   // attacker-planted cookie enters the jar
    }
    std::fclose(f);
}

int main() {
    CookieJar jar;
    load_cookies_from_path(jar, "/tmp/curl-cookies-attacker-planted.txt");
    std::printf("cookies loaded: %zu\n", jar.entries.size());
    return 0;
}
