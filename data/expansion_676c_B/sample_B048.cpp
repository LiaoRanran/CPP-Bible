// sample_B048
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B048.json)

#include <vector>
#include <cstdio>
int main(){
  std::vector<int*> v;
  for (int i = 0; i < 5; i++) v.push_back(new int(i));
  std::printf("%d\n", v.size());
  /*DEFECT: resource leak: vector of pointers cleared without delete */
  return 0;
}