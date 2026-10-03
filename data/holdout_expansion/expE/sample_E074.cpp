// sample_E074
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan,ubsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E074.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int cell = 1;
static std::atomic<unsigned long long> raw{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void shifter(){
  wait_go();
  /*DEFECT: 把对象地址当整数塞进 atomic<unsigned long long> 再做位运算后 reinterpret 回指针：
     整数上不满足指针对齐/表示要求，转回指针解引用是 UB */
  unsigned long long a = reinterpret_cast<unsigned long long>(&cell);
  raw.store((a << 1) | 1ULL, std::memory_order_relaxed);
}
static void dereferencer(){
  wait_go();
  while (raw.load(std::memory_order_relaxed) == 0ULL){}
  /*DEFECT: 由整数位运算结果构造指针并解引用 → 非法指针解引用（UB）*/
  int* p = reinterpret_cast<int*>(static_cast<unsigned long long>(raw.load(std::memory_order_relaxed)));
  std::printf("E074 cell=%d\n", *p);
}
int main(){
  std::thread a(shifter), b(dereferencer);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
