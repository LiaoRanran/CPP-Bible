// sample_E037
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E037.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Acc { long id; double balance; };
static Acc g_acc{0, 0.0};
static std::atomic<bool> synced{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void updater(){
  wait_go();
  g_acc.id = 9001; g_acc.balance = 12.5;
  synced.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  /*DEFECT: synced 用 relaxed 轮询：无 acquire，随后读非原子 g_acc 成员 → 数据竞争*/
  while (!synced.load(std::memory_order_relaxed)){}
  std::printf("E037 id=%ld bal=%f\n", g_acc.id, g_acc.balance);
}
int main(){
  std::thread u(updater), c(consumer);
  go.store(true, std::memory_order_release);
  u.join(); c.join();
  return 0;
}
