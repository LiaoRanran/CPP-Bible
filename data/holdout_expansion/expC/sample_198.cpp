int main(){
  int total = 10, n = 3;
  int avg = total / n; // <<PLANTED-DEFECT>> 整数除法：avg=3 而非 3.33（特定输入下语义错误）
  (void)avg;
  return 0;
}

