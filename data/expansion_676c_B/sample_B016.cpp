// sample_B016
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B016.json)

#include <thread>
#include <cstdio>
long long g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race on long long g */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%lld\n", g);
  return 0;
}