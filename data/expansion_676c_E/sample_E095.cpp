// sample_E095
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E095.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex big, small;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void on_big_ready(){
  /*DEFECT: 回调在 big 已被持有的栈帧上再取 small，且与另一线程的 small->big 顺序相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> s(small);
  std::printf("E095 callback\n");
}
static void big_path(){
  wait_go();
  std::lock_guard<std::mutex> b(big);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  on_big_ready();
}
static void small_path(){
  wait_go();
  std::lock_guard<std::mutex> s(small);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: small->big，与 big_path 里的 big->small 构成循环等待 */
  std::lock_guard<std::mutex> b(big);
  std::printf("E095 small path\n");
}
int main(){
  std::thread a(big_path), b(small_path);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
