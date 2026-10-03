#include <mutex>
std::mutex m;
int main(){
  m.lock();
  try { throw 1; } catch (int) { return 1; } // <<PLANTED-DEFECT>> 异常路径未 unlock
  m.unlock();
  return 0;
}

