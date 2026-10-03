// sample_B041
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B041.json)

#include <cstdio>
int main(){
  int* p = new int(1);
  std::printf("%d\n", *p);
  /*DEFECT: resource leak: no delete (LSan reports at exit) */
  return 0;
}