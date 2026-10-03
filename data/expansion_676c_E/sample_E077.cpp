// sample_E077
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E077.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2, m3;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void spin_for(int n){ while (held.load(std::memory_order_acquire) < n){} }
static void alpha(){
  wait_go();
  std::lock_guard<std::mutex> a(m1);
  held.fetch_add(1, std::memory_order_release); spin_for(3);
  /*DEFECT: m1->m2->（隐含 m3 由 beta/gamma 持有）形成环形等待 ⇒ 死锁 */
  std::lock_guard<std::mutex> b(m2);
  std::printf("E077 alpha\n");
}
static void beta(){
  wait_go();
  std::lock_guard<std::mutex> b(m2);
  held.fetch_add(1, std::memory_order_release); spin_for(3);
  /*DEFECT: m2->m3 顺序，与 gamma 的 m3->m1->m2 构成环 ⇒ 死锁点 */
  std::lock_guard<std::mutex> c(m3);
  std::printf("E077 beta\n");
}
static void gamma(){
  wait_go();
  std::lock_guard<std::mutex> c(m3);
  held.fetch_add(1, std::memory_order_release); spin_for(3);
  /*DEFECT: m3->m1 与 alpha 的 m1->m2->m3 构成环 ⇒ 死锁点 */
  std::lock_guard<std::mutex> a(m1);
  std::printf("E077 gamma\n");
}
int main(){
  std::thread x(alpha), y(beta), z(gamma);
  go.store(true, std::memory_order_release);
  x.join(); y.join(); z.join();
  return 0;
}
