// sample_E052
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E052.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int*> slot{nullptr};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void publish(){
  wait_go();
  int* h = new int(7);
  slot.store(h, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
  /*DEFECT: 原子指针仍指向已释放的堆对象：把「已 delete 的地址」作为原子值发布出去，等于发布了悬垂指针*/
  delete h;
}
static void consume(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  /*DEFECT: 解引用悬垂原子指针 → heap-use-after-free*/
  std::printf("E052 v=%d\n", *slot.load(std::memory_order_relaxed));
}
int main(){
  std::thread a(publish), b(consume);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
