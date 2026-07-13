// Policy-Based Design 取证（静态多态 vs 虚函数）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_policy.cpp -o _asm_policy.asm
#include <cstdlib>

// 策略 1：线程策略（编译期选择，无虚函数）
struct SingleThreaded { static void lock() {} static void unlock() {} };
struct MultiThreaded  { static void lock() {} static void unlock() {} };

// 策略 2：创建策略（类模板，作为模板模板参数传入）
template <typename T> struct NewCreator    { static T* create() { return new T(); } };
template <typename T> struct MallocCreator { static T* create() { return static_cast<T*>(std::malloc(sizeof(T))); } };

// 宿主模板：组合两个策略（模板模板参数 CP + 类型策略 TP）
template <typename T, template <typename> class CP, typename TP>
struct Widget {
    static T* make() {
        TP::lock();
        T* p = CP<T>::create();
        TP::unlock();
        return p;
    }
};

using W1 = Widget<int, NewCreator,    SingleThreaded>;   // 策略组合 A
using W2 = Widget<int, MallocCreator, MultiThreaded>;     // 策略组合 B

// 虚函数对照
struct VBase { virtual int* make() = 0; };
struct VNew  : VBase { int* make() override { return new int(); } };

int use_policy() {
    int* a = W1::make();          // new + 单线程（策略内联）
    int* b = W2::make();          // malloc + 多线程（策略内联）
    int r = (a != nullptr) + (b != nullptr);
    delete a;
    std::free(b);
    return r;
}
int use_virtual(VBase& v) { return v.make() != nullptr; }   // 虚函数间接调用
