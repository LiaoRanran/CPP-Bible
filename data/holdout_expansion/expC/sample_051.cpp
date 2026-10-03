#include <mutex>
std::mutex m;
int worker(){
  m.lock();
  if (true) return -1; // <<PLANTED-DEFECT>> 提前返回，未 unlock -> 锁泄漏
  m.unlock();
  return 0;
}
int main(){ return worker(); }

