// sample_B013
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B013.json)

#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race in parallel loop */ }
int main(){
  std::thread t1(f), t2(f), t3(f);
  t1.join(); t2.join(); t3.join();
  std::printf("%d\n", g);
  return 0;
}