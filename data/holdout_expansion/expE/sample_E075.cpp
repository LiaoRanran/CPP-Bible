// sample_E075
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan,tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E075.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Rec { int key; int val; char pad[8]; };
static std::atomic<Rec*> slot{nullptr};
static std::atomic<bool> ready{false}, go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void mutator(){
  wait_go();
  Rec* r = new Rec{5, 0, "abcdefg"};
  slot.store(r, std::memory_order_relaxed);
  ready.store(true, std::memory_order_release);
  /*DEFECT: 结构体内容在「发布」之后仍被非原子地改写：CAS/load 只能原子地取指针，取不到内容快照*/
  r->val = 99;
  r->key = 6;
}
static void cas_user(){
  wait_go();
  while(!ready.load(std::memory_order_acquire)){}
  Rec* exp = slot.load(std::memory_order_acquire);
  if (slot.compare_exchange_strong(exp, nullptr, std::memory_order_acq_rel)){
    /*DEFECT: 读到的 key/val 来自一次「非原子的多字段读」，可能撕裂；这里再把已释放风险叠加进来*/
    std::printf("E075 key=%d val=%d\n", exp->key, exp->val);
    delete exp;
  }
}
int main(){
  std::thread a(mutator), b(cas_user);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
