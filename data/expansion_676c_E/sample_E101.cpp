// sample_E101
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E101.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex s1, s2, s3;
static std::condition_variable c1, c2, c3;
static bool d1 = false, d2 = false, d3 = false;
static std::atomic<int> ready{0};
static void gate(){ while (ready.load(std::memory_order_acquire) < 3){} }
static void stage1(){
  std::unique_lock<std::mutex> l(s1);
  ready.fetch_add(1, std::memory_order_release); gate();
  /*DEFECT: 持 s1 等 d1；d1 只能由 stage2 在拿到 s2 后设，而 stage2 持 s2 等 d2… ⇒ 环形等待 */
  c1.wait(l, []{ return d1; });
  d3 = true; c3.notify_all();
}
static void stage2(){
  std::unique_lock<std::mutex> l(s2);
  ready.fetch_add(1, std::memory_order_release); gate();
  /*DEFECT: 持 s2 等 d2 */
  c2.wait(l, []{ return d2; });
  d1 = true; c1.notify_all();
}
static void stage3(){
  std::unique_lock<std::mutex> l(s3);
  ready.fetch_add(1, std::memory_order_release); gate();
  /*DEFECT: 持 s3 等 d3，闭合等待环 */
  c3.wait(l, []{ return d3; });
  d2 = true; c2.notify_all();
}
int main(){
  std::thread a(stage1), b(stage2), c(stage3);
  a.join(); b.join(); c.join();
  return 0;
}
