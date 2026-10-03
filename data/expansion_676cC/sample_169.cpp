int main(){
  int n = 9;
  int a[5] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=5 时越界写
  return 0;
}

