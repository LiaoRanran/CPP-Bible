// sample_B050
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// (authoritative annotation in sample_B050.json)

#include <cstdio>
int* gp = new int(99);
int main(){
  std::printf("%d\n", *gp);
  /*DEFECT: resource leak: global allocation never freed */
  return 0;
}