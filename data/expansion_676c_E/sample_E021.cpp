// sample_E021
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E021.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Row { int a; int b; };
static Row g_row{0, 0};
static std::atomic<bool> filled{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void filler(){
  wait_go();
  g_row.a = 11; g_row.b = 22;
  filled.store(true, std::memory_order_relaxed);
}
static void consumer(){
  wait_go();
  /*DEFECT: filled 用 relaxed 轮询：无 acquire 语义，随后读非原子 g_row 构成数据竞争*/
  while (!filled.load(std::memory_order_relaxed)){}
  std::printf("E021 a=%d b=%d\n", g_row.a, g_row.b);
}
int main(){
  std::thread f(filler), c(consumer);
  go.store(true, std::memory_order_release);
  f.join(); c.join();
  return 0;
}
