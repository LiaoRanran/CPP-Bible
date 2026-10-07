// sample_E020
// [redacted]
// severity: high
// [redacted]
// expected_verdict: catch
// [redacted]
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E020.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Cfg { int id; char name[16]; int cached; };
static std::atomic<Cfg*> pub{nullptr};
static std::atomic<bool> live{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  Cfg* c = new Cfg{};
  c->id = 1;
  for (int i = 0; i < 16; ++i) c->name[i] = 'a' + (i % 26);
  c->cached = 0;                          // 非原子字段
  pub.store(c, std::memory_order_relaxed);
  live.store(true, std::memory_order_release);
  /* [redacted]
*/
  c->cached = 4242;
}
static void reader(){
  wait_go();
  while(!live.load(std::memory_order_acquire)){}
  Cfg* c = pub.load(std::memory_order_relaxed);
  /* [redacted]*/
  std::printf("E020 id=%d cached=%d\n", c->id, c->cached);
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
