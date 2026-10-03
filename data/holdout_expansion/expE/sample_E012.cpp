// sample_E012
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan,asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E012.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Res { int payload; };
static std::atomic<int> refs{1};
static std::atomic<bool> go{false};
static Res* g = nullptr;
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void owner(){
  wait_go();
  g = new Res{5};
  refs.store(2, std::memory_order_relaxed);
}
static void dropper(){
  wait_go();
  /*DEFECT: 以 relaxed 读取引用计数并据此 delete：与其他线程的 relaxed 增减之间无同步，读到 2 不代表对象已构造完*/
  while (refs.load(std::memory_order_relaxed) < 2){}
  if (refs.fetch_sub(1, std::memory_order_relaxed) == 2){ /* 误判：以为自己是最后一个引用 */
    delete g; g = nullptr;
  }
}
int main(){
  std::thread a(owner), b(dropper);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E012 done\n");
  return 0;
}
