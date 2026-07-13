#include <cstddef>

// 内联命名空间：外层无需写版本号即可访问
inline namespace v2 {
    struct Api { int version = 2; };
}

namespace v1 {
    struct Api { int version = 1; };
}

Api current() { return Api{}; }   // 解析到 v2::Api
