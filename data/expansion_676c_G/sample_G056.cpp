// sample_G056
// defect_type: logic_error
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2016-6153 (https://nvd.nist.gov/vuln/detail/CVE-2016-6153) [sqlite]
// (authoritative annotation in sample_G056.json)
#include <cstdio>
// CVE-2016-6153: 临时目录搜索算法实现不当 → 使用攻击者可控目录
struct DirCandidate {
    const char* path;
    bool        world_writable;
    bool        user_owned;    // 是否当前用户所有
};

static const DirCandidate k_dirs[] = {
    { "/var/tmp",      false, true  },   // 正确顺序应优先安全目录
    { "/tmp",          true,  false },   // 世界可写 → 攻击者可控
    { "/usr/tmp",      true,  false },
};

static const char* pick_tmpdir_vulnerable() {
    /* DEFECT */ // 原始缺陷: 搜索顺序未按世界可写位降权
    for (const DirCandidate& d : k_dirs)
        return d.path;   // 直接返回第一个候选(未检查 world_writable)
    return 0;
}

int main() {
    const char* dir = pick_tmpdir_vulnerable();
    std::printf("SQLite 临时数据库目录: %s (该目录 world_writable=true)\n", dir);
    std::printf("(正确行为: 跳过世界可写目录, 防止 DB 文件被攻击者读取/替换)\n");
    return 0;
}
