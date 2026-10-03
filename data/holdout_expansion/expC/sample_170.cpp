int main(){
  int n = 6;
  int a[3] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=3 时越界写
  return 0;
}

