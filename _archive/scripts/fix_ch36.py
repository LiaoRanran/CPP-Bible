import re

p = "_insert_exercises.py"
s = open(p, encoding="utf-8").read()

key = '"Book/part04_memory/ch36_stack_heap.md": ['
i = s.index(key)
rest = s[i:]
m = re.search(r'\n\],', rest)
assert m, "closing ], not found"
end = i + m.end()

new_block = r""""Book/part04_memory/ch36_stack_heap.md": [
r'''### 练习 4（难度 ★★）

**真实场景：函数内的大对象必须上堆，否则会爆栈。** 你在函数里声明了一个很大的局部数组或容器（比如 100 万个 `long long`），运行到一半直接段错误。请用代码演示"大对象放堆上、由容器/智能指针管理"的正确做法，并说明线程栈容量通常是有限且固定的，超出即未定义行为。

<details><summary>答案与解析</summary>

自动存储期对象（局部变量）分配在调用栈上，而栈的容量由实现和线程决定、通常很小（常见默认仅几 MB）。在栈上直接放一个几十 KB 以上的大对象，或递归过深，都会超出栈容量导致**栈溢出**——这是未定义行为，典型表现为段错误/访问冲突。

正确做法：大对象（大数组、大结构体、深容器）一律用堆分配——`std::vector`、`std::string` 的内容本就在堆上，或用 `std::unique_ptr` 持有动态对象。这样既绕开栈上限，又由 RAII 自动回收，不必手写 `new/delete`。

> **示例 __NEXT__** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 4（难度 ★★）
```cpp
#include <iostream>
#include <memory>
#include <vector>

void process() {
    // 错误: 100 万个 long long 在栈上约 8MB，可能超过线程栈上限
    // long long buf[1'000'000];
    auto big = std::make_unique<std::vector<long long>>(1'000'000, 0);
    std::cout << big->size() << "\n";
}

int main() { process(); }
```

<span class="badge badge-std">标准</span> 自动存储期对象的分配与生命周期见 `[basic.stc.auto]`；动态存储期（堆）由 `new`/`delete` 管理见 `[basic.stc.dynamic]`。栈容量是实现定义的，超出自动存储区域的边界是未定义行为（典型表现为段错误）。

<span class="badge badge-exp">经验</span> 经验法则：栈只放"小且短命"的对象；数组、大结构体、深容器一律交给堆（优先 `std::vector`/`std::string`/`std::unique_ptr`）。递归函数也要警惕栈深度，必要时改迭代或把累加状态放堆上。

</details>

### 练习 5（难度 ★★★）

**真实场景：多个栈对象的构造/析构顺序决定资源获取次序。** 你在函数里按顺序声明了 A、B 两个局部对象，B 的构造依赖 A 已经就绪，且二者析构时有资源释放次序要求。请用代码演示"构造顺序 = 声明顺序、析构顺序 = 逆声明顺序"，并说明为什么这条规则对异常安全至关重要。

<details><summary>答案与解析</summary>

在同一作用域内，具名自动对象的**初始化按声明顺序发生**；当作用域结束或发生异常栈展开时，它们的**销毁按构造的逆序进行**。这正是你需要的保证：若 B 依赖 A 先存在，只要把 A 声明在 B 之前，A 就必定先构造、后析构——B 整个生命周期内 A 都有效，资源释放次序也天然正确。

这条逆序规则在异常安全上尤为关键：若 A 的构造成功后 B 的构造抛异常，栈展开会按逆序把已构造的 A 正确销毁，不会出现"依赖者已死、被依赖者悬空"的半初始化状态。反观用裸指针延迟 `new` 出来的对象，一旦顺序被手写打乱，就极易引入悬垂或泄漏。

> **示例 __NEXT__** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 5（难度 ★★★）
```cpp
#include <iostream>

struct A { A() { std::cout << "A ctor\n"; } ~A() { std::cout << "A dtor\n"; } };
struct B { B() { std::cout << "B ctor\n"; } ~B() { std::cout << "B dtor\n"; } };

int main() {
    A a;
    B b;   // 输出: A ctor, B ctor, B dtor, A dtor
}
```

<span class="badge badge-std">标准</span> 块作用域内具名对象的初始化顺序见 `[stmt.dcl]`；同一作用域对象的销毁按其构造的逆序进行（`[stmt.dcl]`、`[dcl.init]`）。异常栈展开时按逆构造序销毁见 `[except.handle]`。

<span class="badge badge-exp">经验</span> 写"后声明者依赖先声明者"是安全惯例：把被依赖者（A）声明在前，依赖者（B）在后。这样构造顺序与析构逆序自动保证 A 活得比 B 长。若因特殊原因必须用指针延迟构造，务必手写配对的保护（如 `unique_ptr`）来维持释放次序，不要依赖直觉。

</details>''',
],
"""

s2 = s[:i] + new_block + s[end:]
open(p, "w", encoding="utf-8", newline="\n").write(s2)
print("ch36 entry replaced; new file length:", len(s2))
