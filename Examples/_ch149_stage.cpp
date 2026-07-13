// 见 Examples/_ch149_stage.cpp
// ③ 流水线阶段枚举 + 调度：build -> test -> static -> package
#include <cstdio>
#include <initializer_list>
enum class Stage { Build, Test, Static, Package };
const char* stage_name(Stage s) {
    if (s == Stage::Build)   return "build";
    if (s == Stage::Test)    return "test";
    if (s == Stage::Static)  return "static";
    return "package";
}
int main() {
    for (Stage s : {Stage::Build, Stage::Test, Stage::Static, Stage::Package})
        std::printf("stage: %s\n", stage_name(s));
    return 0;
}
