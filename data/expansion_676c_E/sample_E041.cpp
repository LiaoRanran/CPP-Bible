// sample_E041
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan,asan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E041.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool> go{false};
int main(){
  std::atomic<int> x;                 /* 故意不给初值：默认构造是 trivial，x 的值不确定 */
  std::thread t([&]{
    while(!go.load(std::memory_order_acquire)){}
    /*DEFECT: 从不确定值开始 fetch_add：读取未初始化原子的值是 UB（C++17 下 atomic 构造不做值初始化）*/
    x.fetch_add(1, std::memory_order_relaxed);
  });
  go.store(true, std::memory_order_release);
  t.join();
  std::printf("E041 x=%d\n", x.load(std::memory_order_relaxed));
  return 0;
}
