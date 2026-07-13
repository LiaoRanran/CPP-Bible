// 见 Examples/_ch149_package.cpp
// ⑨ 制品清单：名称/版本/哈希，发布门禁据此校验完整性
#include <cstdio>
#include <string>
struct Artifact {
    std::string name;
    std::string version;
    std::string sha256;
};
int main() {
    Artifact a{"libcore", "1.4.2", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b"};
    std::printf("package %s@%s (%s)\n", a.name.c_str(), a.version.c_str(), a.sha256.c_str());
    return 0;
}
