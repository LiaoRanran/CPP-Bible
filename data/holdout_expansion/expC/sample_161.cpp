int main(){
  int n = 8;
  int a[4] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=4 时越界写
  return 0;
}

