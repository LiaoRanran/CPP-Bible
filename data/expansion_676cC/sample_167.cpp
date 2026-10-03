int main(){
  int n = 12;
  int a[8] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=8 时越界写
  return 0;
}

