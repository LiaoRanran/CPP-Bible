// sample_B042
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B042.json)

#include <cstdio>
int main(){
  int* a = new int[10];
  a[0] = 1;
  std::printf("%d\n", a[0]);
  /*DEFECT: resource leak: array new not deleted[] */
  return 0;
}