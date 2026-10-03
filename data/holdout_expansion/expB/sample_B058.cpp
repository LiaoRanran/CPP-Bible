// sample_B058
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B058.json)

#include <cstdio>
int main(){
  int* p = new int(1);
  p[0] = 5;
  std::printf("%d\n", p[0]);
  /*DEFECT: resource leak: forgot delete */
  return 0;
}