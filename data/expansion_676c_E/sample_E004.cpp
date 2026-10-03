// sample_E004
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E004.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Node { int v; Node* next; };
static Node* g_node = nullptr;              // 非原子裸指针
static std::atomic<bool> g_init{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static Node* acquire_node(){
  if (g_init.load(std::memory_order_acquire)){
    /*DEFECT: 二次检查用 relaxed，且直接读非原子裸指针：发布前的中间态对读线程可见*/
    if (g_init.load(std::memory_order_relaxed)) return g_node;
  }
  Node* n = new Node{7, nullptr};
  g_node = n;
  g_init.store(true, std::memory_order_release);
  return n;
}
int main(){
  std::thread t1([]{ wait_go(); std::printf("E004 v=%d\n", acquire_node()->v); });
  std::thread t2([]{ wait_go(); std::printf("E004 v=%d\n", acquire_node()->v); });
  go.store(true, std::memory_order_release);
  t1.join(); t2.join();
  return 0;
}
