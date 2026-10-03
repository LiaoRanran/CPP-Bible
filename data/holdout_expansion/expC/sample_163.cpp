int main(){
  int n = 10;
  int a[6] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=6 时越界写
  return 0;
}

