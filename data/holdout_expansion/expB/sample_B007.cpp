// sample_B007
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B007.json)

#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race (compound RMW) */ }
int main(){
  std::thread t[2] = { std::thread(f), std::thread(f) };
  t[0].join(); t[1].join();
  std::printf("%d\n", g);
  return 0;
}