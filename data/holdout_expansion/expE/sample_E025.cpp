// sample_E025
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E025.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> token{0};
static std::atomic<bool> done{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  token.store(1, std::memory_order_release);
  /*DEFECT: 写侧标志用 relaxed：读侧的 load(memory_order_release) 是无意义用法，无法与 relaxed 配对*/
  done.store(true, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  /*DEFECT: load 上用 release：release 语义只对 store 有效，此处既不发布也不获取*/
  while (!done.load(std::memory_order_release)){}
  std::printf("E025 token=%d\n", token.load(std::memory_order_relaxed));
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
