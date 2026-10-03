// sample_E028
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E028.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Session { int id; int step; };
static Session* volatile g_sess = nullptr;   // 非原子指针
static std::atomic<bool> open{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void opener(){
  wait_go();
  Session* s = new Session{1, 0};
  s->step = 3;
  g_sess = s;
  open.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  /*DEFECT: open 用 relaxed 轮询，随后读非原子 g_sess 指向的对象 → 竞争 + 可能读到半构造对象*/
  while(!open.load(std::memory_order_relaxed)){}
  std::printf("E028 step=%d\n", g_sess->step);
}
int main(){
  std::thread o(opener), c(consumer);
  go.store(true, std::memory_order_release);
  o.join(); c.join();
  return 0;
}
