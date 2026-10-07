#include <mutex>
std::mutex m;
int main(){
  m.lock();
  try { throw 1; } catch (int) { return 1; } // [redacted]
  m.unlock();
  return 0;
}

