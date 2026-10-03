// sample_E116
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E116.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Cell { int v; Cell* next; };
static Cell ring[4];
static std::atomic<Cell*> head{nullptr}, tail{nullptr};
static std::atomic<int> step{0};
static std::atomic<int> dequeued{0}, enqueued{0};
static void enqueue(int v){
  Cell* c = &ring[v % 4];
  c->v = v;
  Cell* t = tail.exchange(c, std::memory_order_acq_rel);
  if (t) t->next = c;
  head.store(c, std::memory_order_release);
  enqueued.fetch_add(1, std::memory_order_relaxed);
}
static int dequeue(){
  Cell* h = head.load(std::memory_order_acquire);
  Cell* nx = h->next;
  if (head.compare_exchange_strong(h, nx, std::memory_order_acq_rel, std::memory_order_acquire))
    dequeued.fetch_add(1, std::memory_order_relaxed);
  return h->v;
}
int main(){
  enqueue(1);
  enqueue(2);
  std::thread a([&]{
    Cell* h = head.load(std::memory_order_acquire);
    Cell* nx = h->next;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: 无锁队列 dequeue 缺少版本号：head 回到同一 Cell 地址后 CAS 误成功，元素被重复/丢失 */
    if (head.compare_exchange_strong(h, nx, std::memory_order_acq_rel, std::memory_order_acquire))
      dequeued.fetch_add(1, std::memory_order_relaxed);
  });
  while (step.load(std::memory_order_acquire) != 1){}
  head.store(&ring[3], std::memory_order_release);
  head.store((&ring[1]), std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E116 in=%d out=%d\n", enqueued.load(), dequeued.load());
  return 0;
}
