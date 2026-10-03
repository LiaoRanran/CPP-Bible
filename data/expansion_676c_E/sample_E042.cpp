// sample_E042
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E042.json)

#include <atomic>
#include <thread>
#include <cstdio>
int main(){
  /*DEFECT: new std::atomic<int> 走默认构造（trivial），对象的值不确定；下面直接参与 RMW 是 UB*/
  std::atomic<int>* p = new std::atomic<int>();
  std::thread t([p]{
    int old = p->fetch_add(5, std::memory_order_relaxed);
    std::printf("E042 old=%d\n", old);
  });
  t.join();
  delete p;
  return 0;
}
