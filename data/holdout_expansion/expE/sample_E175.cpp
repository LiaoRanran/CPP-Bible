// sample_E175
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E175.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static std::atomic<int> notified{0}, finished{0};
static void consumer(){
  std::unique_lock<std::mutex> lk(m);
  while (!ready) cv.wait(lk);          // 谓词本身是对的
  finished.store(1, std::memory_order_release);
}
static void producer(){
  /*DEFECT: 谓词 ready 完全在锁外写 —— 这才是丢失唤醒的真正根因：
     consumer「检查谓词 → 真正阻塞进 wait」之间存在窗口，
     ready=true + notify_all 可以整个从窗口里滑过去，
     于是 consumer 带着（它以为没变过的）谓词进入阻塞，再也收不到通知。
     注意：如果谓词是在锁内写的，notify 的先后顺序其实无关紧要——
     正是「谓词不受锁保护」让这条通知变得不可靠。 */
  notified.store(1, std::memory_order_release);
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(consumer), b(producer);
  a.join(); b.join();
  std::printf("E175 finished=%d\n", finished.load());
  return 0;
}
