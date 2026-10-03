// sample_E056
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E056.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic_flag lock = ATOMIC_FLAG_INIT;
static int counter = 0;                // 非原子，受锁保护
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void worker(){
  wait_go();
  /*DEFECT: 获取与释放都用 relaxed：临界区内的写对其它线程无 happens-before，互斥形同虚设（数据竞争）*/
  while (lock.test_and_set(std::memory_order_relaxed)){}
  counter++;
  lock.clear(std::memory_order_relaxed);
}
int main(){
  std::thread a(worker), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E056 counter=%d\n", counter);
  return 0;
}
