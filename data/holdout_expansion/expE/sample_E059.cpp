// sample_E059
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E059.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool>* g_at = nullptr;
static std::atomic<bool> escaped{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void publish_and_die(){
  wait_go();
  /*DEFECT: 把一个「生命周期由自己管理」的 atomic 裸指针交给别的线程，
     却不 prolong 它的生命周期：发布之后立刻 delete，
     另一线程对它的访问就变成对已结束对象的访问（UB，dangling atomic） */
  g_at = new std::atomic<bool>(true);
  escaped.store(true, std::memory_order_release);
  delete g_at;
}
static void worker(){
  wait_go();
  while(!escaped.load(std::memory_order_acquire)){}
  /*DEFECT: 通过悬垂的 std::atomic<bool>* 读取一个生命周期已结束的原子对象 → heap-use-after-free */
  std::atomic<bool>* p = reinterpret_cast<std::atomic<bool>*>(g_at);
  std::printf("E059 v=%d\n", (int)p->load(std::memory_order_relaxed));
}
int main(){
  std::thread a(publish_and_die), b(worker);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
