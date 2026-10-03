// sample_B053
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B053.json)

#include <cstdio>
int main(){
  if (true){ int* p = new int(1); std::printf("%d\n", *p); /*DEFECT: leak inside branch, no delete */ }
  return 0;
}