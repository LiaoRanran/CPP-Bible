int main(){
  int n = 3;
  int a[2] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=2 时越界写
  return 0;
}

