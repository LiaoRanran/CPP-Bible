// sample_B055
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B055.json)

#include <cstdio>
int main(){
  int* p = new int(1);
  try { throw 1; } catch (...) { }
  std::printf("%d\n", *p);
  /*DEFECT: resource leak: p not freed after exception path */
  return 0;
}