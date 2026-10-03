// sample_B045
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B045.json)

#include <cstdio>
int main(){
  int* p = new int(1);
  p = new int(2); /*DEFECT: resource leak: old pointer overwritten, lost */
  std::printf("%d\n", *p);
  delete p;
  return 0;
}