// 文件：Examples/_ch15_scalar_vs_accum.cpp
// 行号：14（scalar_sum）/ 21（four_acc_sum）
// 朴素标量累加：单累加器，依赖链长度 = N
long scalar_sum(const long* a, long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += a[i];
    return s;
}
// 多累加器：4 条独立依赖链（向量化雏形，缩短 loop-carried 依赖）
long four_acc_sum(const long* a, long n) {
    long s0=0,s1=0,s2=0,s3=0; long i=0;
    for (; i+4<=n; i+=4){ s0+=a[i]; s1+=a[i+1]; s2+=a[i+2]; s3+=a[i+3]; }
    for (; i<n; ++i) s0+=a[i];
    return s0+s1+s2+s3;
}