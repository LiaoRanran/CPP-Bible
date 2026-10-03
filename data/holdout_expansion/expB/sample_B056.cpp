// sample_B056
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B056.json)

#include <cstdio>
int recurse(int n){ int* p = new int(n); std::printf("%d\n", *p); if (n>0) recurse(n-1); /*DEFECT: each frame leaks p */ return 0; }
int main(){ recurse(4); return 0; }