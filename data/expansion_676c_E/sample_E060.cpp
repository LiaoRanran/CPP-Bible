// sample_E060
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E060.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int>* cell = nullptr;
static std::atomic<bool> made{false}, quit{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void poller(){
  wait_go();
  while(!made.load(std::memory_order_acquire)){}
  while(!quit.load(std::memory_order_acquire)){
    /*DEFECT: 轮询一个可能已经被 delete 的 atomic 对象 → heap-use-after-free*/
    if (cell->load(std::memory_order_relaxed) == 42) break;
  }
}
static void releaser(){
  wait_go();
  /*DEFECT: 在 poller 还在通过 cell 访问时 delete cell：原子对象生命周期未结束即被销毁 */
  delete cell;
  cell = nullptr;
  quit.store(true, std::memory_order_release);
}
int main(){
  cell = new std::atomic<int>(0);
  made.store(true, std::memory_order_release);
  std::thread a(poller), b(releaser);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
