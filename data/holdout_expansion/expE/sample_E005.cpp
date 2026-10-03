// sample_E005
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E005.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Payload { int arr[8]; };
static std::atomic<Payload*> pub{nullptr};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void writer(){
  wait_go();
  Payload* p = new Payload{};
  for (int i = 0; i < 8; ++i) p->arr[i] = i * i;
  /*DEFECT: 指针本身用 relaxed 发布：读侧 acquire 也无法与之配对，对象内容可能未初始化可见*/
  pub.store(p, std::memory_order_relaxed);
}
static void reader(){
  wait_go();
  Payload* p = nullptr;
  /*DEFECT: relaxed 轮询指针：即使随后 acquire 读，也可能在 relaxed 轮询阶段拿到半成品指针*/
  while ((p = pub.load(std::memory_order_relaxed)) == nullptr){}
  std::printf("E005 p7=%d\n", p->arr[7]);
}
int main(){
  std::thread w(writer), r(reader);
  go.store(true, std::memory_order_release);
  w.join(); r.join();
  return 0;
}
