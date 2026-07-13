// 见 Examples/_ch149_principle.cpp
// ② CI 四项核心原则枚举化，避免口头约定漂移
#include <cstdio>
enum class CI_Principle { Reproducible, Fast, Hermetic, Observable };
const char* name(CI_Principle p) {
    switch (p) {
        case CI_Principle::Reproducible: return "Reproducible";
        case CI_Principle::Fast:         return "Fast";
        case CI_Principle::Hermetic:     return "Hermetic";
        case CI_Principle::Observable:   return "Observable";
    }
    return "?";
}
int main() {
    std::printf("principle=%s\n", name(CI_Principle::Hermetic));
    return 0;
}
