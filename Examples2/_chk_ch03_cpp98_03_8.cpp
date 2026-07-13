#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include <map>
#include <set>
#include <functional>
#include <thread>
#include <future>
#include <atomic>
#include <tuple>
#include <utility>
#include <initializer_list>
#include <array>
#include <stdexcept>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <limits>
#include <ciso646>
#include <iomanip>
#include <iterator>
#include <filesystem>
#include <variant>
#include <any>
#include <optional>
#include <ranges>
#include <bit>
#include <chrono>
#include <execution>
#include <type_traits>
#include <concepts>
#include <span>
#include <expected>
#include <format>
#include <version>
#include <string_view>
#include <cwchar>

namespace chk_ch03_cpp98_03_8 {
// 算法 for_each + 函数对象
struct Inc{ void operator()(int&x)const{ ++x; } }; void f(){ std::vector<int> v(2); std::for_each(v.begin(),v.end(),Inc()); }
}
int main(){ return 0; }
