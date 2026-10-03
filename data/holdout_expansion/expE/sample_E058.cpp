// sample_E058
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan,asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E058.json)

#include <atomic>
#include <thread>
#include <cstdio>
#include <new>
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void work(int v){
  wait_go();
  /*DEFECT: 在 char 缓冲的 offset 1 处 placement-new 一个 alignof 为 4 的 atomic<int>：对象未对齐，访问是 UB */
  alignas(8) unsigned char buf[sizeof(std::atomic<int>) + 2];
  std::atomic<int>* a = new (buf + 1) std::atomic<int>(0);
  a->fetch_add(v, std::memory_order_relaxed);
  std::printf("E058 v=%d\n", a->load(std::memory_order_relaxed));
}
int main(){
  std::thread a(work, 1), b(work, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
