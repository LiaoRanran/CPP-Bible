# ATOM-MEM-SHARED-002（atom_claim）

## 正面

【MEM】ATOM-MEM-SHARED-002
以下论断是否成立？依据是什么？
shared_ptr 的控制块引用计数用 LOCK 前缀的原子 RMW 修改，因此**各线程持有各自副本**时的并发 拷贝/销毁是安全的；但**被指对象**与**同一个 shared_ptr 实例**都不受这层保护（并发读写同一实例 需外部同步，C++20 起可用 std::atomic<std::shared_ptr<T>>；use_count() 在并发下只是近似值）。 unique_ptr 的所有权转移是纯指针搬运、不含原子 RMW，代价是**不可拷贝**——要共享必须显式改用 shared_ptr，于是"要不要付原子代价"成了编译期可判的选择，而不是运行期祈祷。

## 背面

论断：shared_ptr 的控制块引用计数用 LOCK 前缀的原子 RMW 修改，因此**各线程持有各自副本**时的并发 拷贝/销毁是安全的；但**被指对象**与**同一个 shared_ptr 实例**都不受这层保护（并发读写同一实例 需外部同步，C++20 起可用 std::atomic<std::shared_ptr<T>>；use_count() 在并发下只是近似值）。 unique_ptr 的所有权转移是纯指针搬运、不含原子 RMW，代价是**不可拷贝**——要共享必须显式改用 shared_ptr，于是"要不要付原子代价"成了编译期可判的选择，而不是运行期祈祷。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'stdlib': ['libstdc++'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-034: confirm
  - EV-MEM-035: confirm
