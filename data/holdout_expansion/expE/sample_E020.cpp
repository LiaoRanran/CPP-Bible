// sample_E020
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan,asan
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
  /*DEFECT: 在 live 的 release 之后又改写普通字段 cached：
     读侧 acquire(live) 覆盖不到这批写 ⇒ 数据竞争 */
  c->cached = 4242;
}
static void reader(){
  wait_go();
  while(!live.load(std::memory_order_acquire)){}
  Cfg* c = pub.load(std::memory_order_relaxed);
  /*DEFECT: 只对 live 做了 acquire，c->cached 是普通字段；写入发生在 release 之后，读侧无同步*/
  std::printf("E020 id=%d cached=%d\n", c->id, c->cached);
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
