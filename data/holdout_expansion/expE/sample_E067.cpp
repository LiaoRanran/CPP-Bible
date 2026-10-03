// sample_E067
// defect_type: atomic_ub
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E067.json)

#include <atomic>
#include <thread>
#include <cstdio>
#include <cstring>
struct SpinLock {
  std::atomic_flag f = ATOMIC_FLAG_INIT;
  int counter = 0;
};
static std::atomic<bool> g_go{false};
static void wait_go(){ while(!g_go.load(std::memory_order_acquire)){} }
static void worker(SpinLock* dst){
  wait_go();
  /*DEFECT: memcpy 复制含 atomic_flag 的对象：两个锁实例共享同一份「被占用」状态拷贝，互斥完全失效 */
  SpinLock copy;
  std::memcpy(&copy, dst, sizeof(SpinLock));
  while (copy.f.test_and_set(std::memory_order_acquire)){}
  copy.counter++;
  copy.f.clear(std::memory_order_release);
}
int main(){
  SpinLock lk;
  std::thread a(worker, &lk), b(worker, &lk);
  g_go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E067 counter=%d\n", lk.counter);
  return 0;
}
