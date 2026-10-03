// sample_E169
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E169.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <vector>
#include <cstdio>
static std::mutex alloc_lock;
static std::vector<int*> pool;
static std::atomic<int> stage{0};
static void churn(){
  std::lock_guard<std::mutex> lk(alloc_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做分配/释放风暴：分配器内部还有自己的锁，
     一旦与别的线程的分配路径形成锁序反转，反转会级联放大 */
  for (int i = 0; i < 5000; ++i){
    int* p = new int[256];
    p[0] = i;
    pool.push_back(p);
  }
  stage.store(2, std::memory_order_release);
}
static void reporter(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级统计线程等锁 */
  std::lock_guard<std::mutex> lk(alloc_lock);
  std::printf("E169 pool=%zu\n", pool.size());
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(churn), b(reporter);
  a.join(); b.join();
  for (int* p : pool) delete[] p;
  return 0;
}
