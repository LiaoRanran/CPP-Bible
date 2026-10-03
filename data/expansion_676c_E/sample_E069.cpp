// sample_E069
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E069.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Item { int id; int weight; };
static std::atomic<Item*> head{nullptr};
static std::atomic<bool> seeded{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void retire(){
  wait_go();
  Item* old = head.exchange(nullptr, std::memory_order_acq_rel);
  /*DEFECT: 换出后立刻 delete，但 head 这个「唯一的发布点」没有版本/生命周期保护：
     另一线程可能已在此之前读到同一个指针并准备 CAS 取出它 */
  delete old;
}
static void take(){
  wait_go();
  while(!seeded.load(std::memory_order_acquire)){}
  Item* exp = head.load(std::memory_order_acquire);
  if (exp != nullptr && head.compare_exchange_strong(exp, nullptr, std::memory_order_acq_rel)){
    /*DEFECT: CAS 成功不代表对象仍存活：retire() 可能刚刚 delete 了它 → heap-use-after-free */
    std::printf("E069 weight=%d\n", exp->weight);
  }
}
int main(){
  head.store(new Item{1, 5}, std::memory_order_release);
  seeded.store(true, std::memory_order_release);
  std::thread a(retire), b(take);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
