// sample_E068
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E068.json)

#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
#include <new>
static std::atomic<long> shared{0};
static std::atomic<bool> go{false}, stop{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void reset_once(){
  wait_go();
  /*DEFECT: 对一个已有生命周期的原子对象重新 placement-new 覆盖：旧对象的生命周期未结束即被销毁，
     另一线程正在进行的 load/store 变成对已结束对象的访问（UB） */
  new (&shared) std::atomic<long>(0);
}
static void spinner(){
  wait_go();
  long acc = 0;
  while (!stop.load(std::memory_order_acquire))
    acc += shared.load(std::memory_order_relaxed);
  std::printf("E068 acc=%ld\n", acc);
}
int main(){
  std::thread a(reset_once), b(spinner);
  go.store(true, std::memory_order_release);
  std::this_thread::sleep_for(std::chrono::milliseconds(20));
  stop.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
