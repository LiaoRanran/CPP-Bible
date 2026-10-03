// sample_B018
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B018.json)

#include <thread>
#include <cstdio>
int main(){
  int v = 0;
  auto f = [&]{ for (int i = 0; i < 2000000; i++) v++; /*DEFECT: data race on captured local v */ };
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\n", v);
  return 0;
}