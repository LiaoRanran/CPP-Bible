// sample_E133
// defect_type: aba_problem
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E133.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Item { int id; Item* next; };
static Item arena[2];
static std::atomic<Item*> head{nullptr};
static std::atomic<int> step{0}, consumed{0};
static int consumed_ids[4] = {0, 0, 0, 0};
int main(){
  arena[0].id = 1; arena[0].next = nullptr;
  arena[1].id = 2; arena[1].next = &arena[0];
  head.store(&arena[1], std::memory_order_release);
  std::thread a([&]{
    Item* p = head.load(std::memory_order_acquire);
    Item* nxt = p->next;
    step.store(1, std::memory_order_release);
    while (step.load(std::memory_order_acquire) != 2){}
    /*DEFECT: p 已被出队并回队（同一槽位、id 变了），CAS 仍按「同一元素」处理 ⇒ 同一 Item 被消费两次 */
    if (head.compare_exchange_strong(p, nxt, std::memory_order_acq_rel, std::memory_order_acquire)){
      int k = consumed.fetch_add(1, std::memory_order_relaxed);
      if (k < 4) consumed_ids[k] = p->id;
    }
  });
  while (step.load(std::memory_order_acquire) != 1){}
  head.store(&arena[0], std::memory_order_release);
  arena[1].id = 3; arena[1].next = &arena[0];
  head.store(&arena[1], std::memory_order_release);
  step.store(2, std::memory_order_release);
  a.join();
  std::printf("E133 consumed=%d ids=%d,%d\n", consumed.load(), consumed_ids[0], consumed_ids[1]);
  return 0;
}
