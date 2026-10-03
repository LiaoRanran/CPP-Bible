// sample_E076
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E076.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void threadA(){
  wait_go();
  std::lock_guard<std::mutex> l1(m1);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}     // 等对方也拿到 m1
  /*DEFECT: A 的加锁顺序是 m1->m2，与 B 的 m2->m1 相反 ⇒ 循环等待，死锁 */
  std::lock_guard<std::mutex> l2(m2);
  std::printf("E076 A ok\n");
}
static void threadB(){
  wait_go();
  std::lock_guard<std::mutex> l2(m2);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: B 的加锁顺序是 m2->m1，与 A 相反 ⇒ 死锁点 */
  std::lock_guard<std::mutex> l1(m1);
  std::printf("E076 B ok\n");
}
int main(){
  std::thread a(threadA), b(threadB);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
