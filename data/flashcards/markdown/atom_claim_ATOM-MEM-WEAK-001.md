# ATOM-MEM-WEAK-001（atom_claim）

## 正面

【MEM】ATOM-MEM-WEAK-001
以下论断是否成立？依据是什么？
std::weak_ptr 是非拥有观察者：指向 shared_ptr 管理的对象但不增加引用计数；.lock() 临时提升为 shared_ptr（对象活着则成功、计数 +1），对象已销毁则 .lock() 返回空（expired）。它用来在"需要旁观共享对象 但不延长其寿命"的场景（尤其子->父反向引用）打破 shared_ptr 的循环引用，避免泄漏。

## 背面

论断：std::weak_ptr 是非拥有观察者：指向 shared_ptr 管理的对象但不增加引用计数；.lock() 临时提升为 shared_ptr（对象活着则成功、计数 +1），对象已销毁则 .lock() 返回空（expired）。它用来在"需要旁观共享对象 但不延长其寿命"的场景（尤其子->父反向引用）打破 shared_ptr 的循环引用，避免泄漏。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-015: confirm
  - EV-MEM-016: confirm
