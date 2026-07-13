// 标签分发（tag dispatch）取证
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tag.cpp -o _asm_tag.asm
#include <type_traits>
#include <iterator>

int g_count = 0;
int g_step  = 0;

// ① 布尔标签分发：true_type / false_type 选择实现
template <typename T>
void impl(T, std::true_type)  { g_count += 1; }
template <typename T>
void impl(T, std::false_type) { g_count += 100; }

template <typename T>
void dispatch(T v) {
    impl(v, typename std::is_integral<T>::type{});   // 标签类型在编译期决定
}

// ② iterator tag 分发：random_access vs input
template <typename It>
void adv(It, std::random_access_iterator_tag) { g_step += 1; }
template <typename It>
void adv(It, std::input_iterator_tag)         { g_step += 10; }

template <typename It>
void adv_dispatch(It it) {
    adv(it, typename std::iterator_traits<It>::iterator_category{});
}

int use_tag() {
    dispatch(42);                  // 整型 -> true_type  -> +1
    dispatch(2.5);                 // 浮点 -> false_type -> +100
    int arr[3] = {};
    adv_dispatch(arr);             // int* -> random_access -> +1
    return g_count + g_step;       // 102
}
