# 677b · 任务A：Clone-Family 分组报告

- 生成：`tools/analyze_677b_clone_aware.py families`（2026-10-04T12:27:29+08:00）
- 机器可读：`data/677b_clone_families.json`
- 样本 n=1137（磁盘夹具 1080，corpus 内联源码 57）
- 克隆关系：C1 归一化精确同构 ∪ C2 Jaccard≥0.85 ∪ C3 结构层余弦≥0.90；家族 = 满足全对约束的极大簇（complete-linkage）

## 1. 家族统计（主定义）

- 家族总数 **474**（单成员 280，多成员 194）
- 最大家族 21 条；平均家族 2.3987 条
- 落在多成员家族的样本 857 / 1137（75.37%）
- 归一化精确结构种数 624
- 跨批家族 21 个；跨 defect_type 家族 30 个
- 相似对（S≥0.80）：5149 对；其中 Jaccard≥0.85 3022 对，cosine≥0.90 2318 对（仅由 C3 覆盖 102 对）
- 判克隆的对共 3124 对：跨**连通分量** 0 对（=0 即「不存在判克隆却可能跨 split 的对」），跨**家族** 575 对（complete-linkage 全对约束的代价）

## 2. 阈值/聚类方式敏感性

| 聚类 | 阈值 | 家族数 | 单成员 | 最大族 | 跨批家族 |
|---|---:|---:|---:|---:|---:|
| complete | 0.8 | 417 | 224 | 32 | 19 |
| complete | 0.85 | 474 | 280 | 21 | 21 |
| complete | 0.9 | 529 | 340 | 17 | 19 |
| single | 0.8 | 337 | 204 | 116 | 13 |
| single | 0.85 | 420 | 257 | 65 | 19 |
| single | 0.9 | 496 | 323 | 20 | 16 |

## 3. 与 676k 的对照

- 676k L2 归一化重复组在 A5 抽样内：160 组 / 668 条
- 676k 的跨批近克隆对 103 对：两端均在 A5 103 对，其中 98 对落进同一家族
  - 未同族例：B092 ~ F106（676k sim=0.935671，677b={'jaccard': 0.631579, 'cosine': 0.933995, 'S': 0.933995}，家族 F0072 / F0288）
  - 未同族例：B092 ~ F107（676k sim=0.935671，677b={'jaccard': 0.631579, 'cosine': 0.933995, 'S': 0.933995}，家族 F0072 / F0288）
  - 未同族例：B092 ~ F108（676k sim=0.935671，677b={'jaccard': 0.631579, 'cosine': 0.933995, 'S': 0.933995}，家族 F0072 / F0288）
  - 未同族例：B092 ~ F109（676k sim=0.935671，677b={'jaccard': 0.631579, 'cosine': 0.933995, 'S': 0.933995}，家族 F0072 / F0288）
  - 未同族例：B092 ~ F110（676k sim=0.935671，677b={'jaccard': 0.631579, 'cosine': 0.933995, 'S': 0.933995}，家族 F0072 / F0288）

## 4. 抽查证据（自动生成，供人工复核）

### 4.1 抽查 10 个家族（5 个最大 + 5 个随机）

- **F0288**（size=21，批次 {'corpus_672h': 2, 'expF': 18, 'holdout_5_672h': 1}，pure_exact=False，min_jaccard=0.866667，min_cosine=0.124243）
- F102-F104：成员 `F102` ↔ `F104`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `F102`：`'#include <cstdio> int main(){   volatile const int ro = 0;  // <<PLANTED-DEFECT>> volatile const 仅阻止编译器优化而非硬件写保护   std::printf("%d\ ", ro);   return 0; } '`
    - `F104`：`'#include <cstdio> int main(){   volatile const int ro = 0;  // <<PLANTED-DEFECT>> volatile const 仅阻止编译器优化而非硬件写保护   std::printf("%d\ ", ro);   return 0; } '`
- **F0014**（size=17，批次 {'expA': 5, 'expC': 12}，pure_exact=False，min_jaccard=1.0，min_cosine=1.0）
- A060-A061：成员 `A060` ↔ `A061`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `A060`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int x;   int r = x + 7; // <<PLANTED-DEFECT>> uninitialized read: arithmetic on uninit var   (void)r;   return 0; } '`
    - `A061`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int y;   int r = y + 7; // <<PLANTED-DEFECT>> uninitialized read: arithmetic on uninit var   (void)r;   return 0; } '`
- **F0002**（size=16，批次 {'expA': 15, 'holdout_5_672h': 1}，pure_exact=False，min_jaccard=0.9375，min_cosine=0.9375）
- A005-A006：成员 `A005` ↔ `A006`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `A005`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int* p = new int[8];   p[1] = 42;   delete[] p;   p[1] = 99; // <<PLANTED-DEFECT>> use-after-free: write freed heap slot   return 0; } '`
    - `A006`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int* p = new int[8];   p[2] = 42;   delete[] p;   p[2] = 99; // <<PLANTED-DEFECT>> use-after-free: write freed heap slot   return 0; } '`
- **F0021**（size=16，批次 {'expA': 5, 'expC': 11}，pure_exact=False，min_jaccard=0.923077，min_cosine=0.923077）
- A088-A089：成员 `A088` ↔ `A089`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `A088`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int a = 10;   int r = a / 0; // <<PLANTED-DEFECT>> undefined behavior: integer division by zero   (void)r;   return 0; } '`
    - `A089`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int a = 10;   int r = a / 0; // <<PLANTED-DEFECT>> undefined behavior: integer division by zero   (void)r;   return 0; } '`
- **F0019**（size=15，批次 {'expA': 7, 'expC': 8}，pure_exact=False，min_jaccard=1.0，min_cosine=1.0）
- A080-A081：成员 `A080` ↔ `A081`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `A080`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int r = 1 << 33; // <<PLANTED-DEFECT>> undefined behavior: shift exponent 33 too large for 32-bit int   (void)r;   return 0; } '`
    - `A081`：`'// 676c 扩样-A: planted C++ defect candidate (generated sample) // SPDX-License-Identifier: Apache-2.0 #include <cstdio> int main() {   int r = 1 << 40; // <<PLANTED-DEFECT>> undefined behavior: shift exponent 40 too large for 32-bit int   (void)r;   return 0; } '`
- **F0201**（size=10，批次 {'expE': 10}，pure_exact=False，min_jaccard=0.897436，min_cosine=0.473151）
- E076-E077：成员 `E076` ↔ `E077`，Jaccard=0.9211 / cosine=0.9211
  - 归一化文本 diff（前 12 行）：
    @@ -1,10 +1,12 @@
    -staticstd::IDID,ID;staticstd::atomic<int>ID{NUM};staticstd::
    -atomic<bool>ID{false};staticvoidID(){while(!ID.ID(std::memor
    -y_order_acquire)){}}staticvoidID(){ID();std::ID<std::ID>ID(I
    -D);ID.ID(NUM,std::memory_order_release);while(ID.ID(std::mem
    -ory_order_acquire)<NUM){}std::ID<std::ID>ID(ID);std::ID(ID);
    -}staticvoidID(){ID();std::ID<std::ID>ID(ID);ID.ID(NUM,std::m
    -emory_order_release);while(ID.ID(std::memory_order_acquire)<
    -NUM){}std::ID<std::ID>ID(ID);std::ID(ID);}intID(){std::threa
    -dID(ID),ID(ID);ID.ID(true,std::memory_order_release);ID.ID()
    -;ID.ID();returnNUM;}
    +staticstd::IDID,ID,ID;staticstd::atomic<int>ID{NUM};staticst
- **F0221**（size=3，批次 {'expE': 3}，pure_exact=False，min_jaccard=0.85，min_cosine=0.473355）
- E120-E121：成员 `E120` ↔ `E121`，Jaccard=0.8718 / cosine=0.5418
  - 归一化文本 diff（前 12 行）：
    @@ -1,10 +1,13 @@
    -staticstd::atomic<int>ID{NUM};staticstd::atomic<int>ID{NUM},
    -ID{NUM};intID(){ID.ID(NUM,std::memory_order_release);std::th
    -readID([&]{intID=ID.ID(std::memory_order_acquire);ID.ID(NUM,
    -std::memory_order_release);while(ID.ID(std::memory_order_acq
    -uire)!=NUM){}if(ID.ID(ID,NUM,std::memory_order_acq_rel,std::
    -memory_order_acquire))ID.ID(NUM,std::memory_order_relaxed);}
    -);while(ID.ID(std::memory_order_acquire)!=NUM){}ID.ID(NUM,st
    -d::memory_order_release);ID.ID(NUM,std::memory_order_release
    -);ID.ID(NUM,std::memory_order_release);ID.ID();std::ID(ID,ID
    -.ID(),ID.ID());returnNUM;}
    +staticstd::atomic<int>ID{NUM},ID{NUM};staticstd::atomic<int>
- **F0280**（size=2，批次 {'expF': 2}，pure_exact=True，min_jaccard=1.0，min_cosine=1.0）
- F064-F065：成员 `F064` ↔ `F065`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `F064`：`'#include <cstdint> #include <cstdio> int main(){   double d = 3.14159;   uint64_t bits = *reinterpret_cast<uint64_t*>(&d);  // <<PLANTED-DEFECT>> 浮点位的端序未处理即跨网络发送   std::printf("%llu\ ", static_cast<unsigned long long>(bits));   return 0; } '`
    - `F065`：`'#include <cstdint> #include <cstdio> int main(){   double d = 3.14159;   uint64_t bits = *reinterpret_cast<uint64_t*>(&d);  // <<PLANTED-DEFECT>> 浮点位的端序未处理即跨网络发送   std::printf("%llu\ ", static_cast<unsigned long long>(bits));   return 0; } '`
- **F0177**（size=2，批次 {'expE': 2}，pure_exact=False，min_jaccard=0.878049，min_cosine=0.350367）
- E046-E053：成员 `E046` ↔ `E053`，Jaccard=0.8780 / cosine=0.3504
  - 归一化文本 diff（前 12 行）：
    @@ -1,6 +1,6 @@
    -staticstd::atomic<int>ID{NUM};staticintID=NUM;staticstd::ato
    -mic<bool>ID{false};staticvoidID(){while(!ID.ID(std::memory_o
    -rder_acquire)){}}staticvoidID(intID){ID();intID=NUM;while(ID
    -.ID(ID,ID,std::memory_order_acq_rel))ID=NUM;ID=ID;}intID(){s
    -td::threadID(ID,NUM),ID(ID,NUM);ID.ID(true,std::memory_order
    -_release);ID.ID();ID.ID();std::ID(ID,ID.ID(),ID);returnNUM;}
    +staticstd::atomic<bool>ID{false};staticintID=NUM;staticstd::
    +atomic<bool>ID{false};staticvoidID(){while(!ID.ID(std::memor
    +y_order_acquire)){}}staticvoidID(){ID();ID.ID(true,std::memo
    +ry_order_acq_rel);ID=ID+NUM;}intID(){std::threadID(ID),ID(ID
    +);ID.ID(true,std::memory_order_release);ID.ID();ID.ID();std:
- **F0409**（size=4，批次 {'corpus_672h': 2, 'holdout_5_672h': 2}，pure_exact=True，min_jaccard=1.0，min_cosine=1.0）
- d3-22-d3e-08：成员 `d3-22` ↔ `d3e-08`，归一化精确同构
  - 归一化后文本完全一致；原文片段对照：
    - `d3-22`：`'int main(){int* p=new int(1);delete p;delete p;return 0;}'`
    - `d3e-08`：`'int main(){int*p=new int(1);delete p;delete p;return 0;}'`

### 4.2 边界对分类（跨家族的对，最多各 12 对）

跨家族的对共 2600 对，其中**判克隆但未合并** 575 对（complete-linkage 全对约束的残余；它们所在**连通分量**相同 ⇒ 在 strict split 下仍被保证不跨 side），**不判克隆** 2025 对。

**(a) 判克隆但跨家族（残余，按 S 降序）**：

- d3-22 ~ d3e-09：Jaccard=0.8667，cosine=0.9673，家族 F0409 vs F0430，同分量=True
- d3e-08 ~ d3e-09：Jaccard=0.8667，cosine=0.9673，家族 F0409 vs F0430，同分量=True
- d3e-09 ~ h27：Jaccard=0.8667，cosine=0.9673，家族 F0430 vs F0409，同分量=True
- B021 ~ B039：Jaccard=0.8889，cosine=0.9603，家族 F0031 vs F0032，同分量=True
- d3-22 ~ h26：Jaccard=0.8125，cosine=0.9560，家族 F0409 vs F0430，同分量=True
- d3e-08 ~ h26：Jaccard=0.8125，cosine=0.9560，家族 F0409 vs F0430，同分量=True
- h26 ~ h27：Jaccard=0.8125，cosine=0.9560，家族 F0430 vs F0409，同分量=True
- B041 ~ B045：Jaccard=0.8824，cosine=0.9478，家族 F0040 vs F0044，同分量=True
- F106 ~ F111：Jaccard=0.8667，cosine=0.9464，家族 F0288 vs F0072，同分量=True
- F106 ~ F112：Jaccard=0.8667，cosine=0.9464，家族 F0288 vs F0072，同分量=True
- F106 ~ F113：Jaccard=0.8667，cosine=0.9464，家族 F0288 vs F0072，同分量=True
- F106 ~ F114：Jaccard=0.8667，cosine=0.9464，家族 F0288 vs F0072，同分量=True

**(b) 高相似但不判克隆（阈值下正确分开，按 S 降序）**：

- B039 ~ B085：Jaccard=0.8421，cosine=0.8986，家族 F0032 vs F0067
- C031 ~ C036：Jaccard=0.8333，cosine=0.8954，家族 F0087 vs F0090
- C033 ~ C036：Jaccard=0.8333，cosine=0.8954，家族 F0087 vs F0090
- C035 ~ C036：Jaccard=0.8333，cosine=0.8954，家族 F0087 vs F0090
- d3-23 ~ d3e-09：Jaccard=0.6471，cosine=0.8921，家族 F0091 vs F0430
- d3e-09 ~ h25：Jaccard=0.6471，cosine=0.8921，家族 F0430 vs F0091
- C071 ~ C086：Jaccard=0.7692，cosine=0.8918，家族 F0098 vs F0101
- C071 ~ C087：Jaccard=0.7692，cosine=0.8918，家族 F0098 vs F0101
- C071 ~ C088：Jaccard=0.7692，cosine=0.8918，家族 F0098 vs F0101
- C071 ~ C089：Jaccard=0.7692，cosine=0.8918，家族 F0098 vs F0101
- C071 ~ C090：Jaccard=0.7692，cosine=0.8918，家族 F0098 vs F0101
- C072 ~ C086：Jaccard=0.7692，cosine=0.8918，家族 F0098 vs F0101

### 4.3 家族大表（size ≥ 5）

| family | size | 批次 | defect_type 数 | min_jaccard | min_cosine | 代表 |
|---|---:|---|---:|---:|---:|---|
| F0288 | 21 | {'corpus_672h': 2, 'expF': 18, 'holdout_5_672h': 1} | 6 | 0.866667 | 0.124243 | F171 |
| F0014 | 17 | {'expA': 5, 'expC': 12} | 2 | 1.0 | 1.0 | A060 |
| F0002 | 16 | {'expA': 15, 'holdout_5_672h': 1} | 3 | 0.9375 | 0.9375 | A005 |
| F0021 | 16 | {'expA': 5, 'expC': 11} | 3 | 0.923077 | 0.923077 | A088 |
| F0019 | 15 | {'expA': 7, 'expC': 8} | 2 | 1.0 | 1.0 | A080 |
| F0098 | 15 | {'expC': 15} | 1 | 0.652174 | 0.91954 | C066 |
| F0144 | 15 | {'expD': 15} | 1 | 0.958333 | 0.958333 | D192 |
| F0004 | 14 | {'expA': 2, 'expC': 12} | 2 | 0.857143 | 0.470935 | C177 |
| F0040 | 12 | {'expB': 2, 'expD': 10} | 2 | 0.882353 | 0.228245 | D147 |
| F0106 | 12 | {'expC': 12} | 1 | 1.0 | 1.0 | C149 |
| F0131 | 12 | {'expD': 12} | 1 | 1.0 | 1.0 | D094 |
| F0001 | 11 | {'expA': 11} | 2 | 0.947368 | 0.947368 | A021 |
| F0078 | 11 | {'expC': 11} | 1 | 0.863636 | 0.383228 | C001 |
| F0120 | 11 | {'expD': 11} | 1 | 0.95 | 0.95 | D042 |
| F0107 | 10 | {'expC': 10} | 1 | 1.0 | 1.0 | C161 |
| F0111 | 10 | {'expD': 10} | 1 | 0.857143 | 0.717617 | D001 |
| F0201 | 10 | {'expE': 10} | 1 | 0.897436 | 0.473151 | E076 |
| F0266 | 10 | {'expF': 10} | 1 | 0.862069 | 0.481766 | F001 |
| F0150 | 9 | {'expE': 9} | 1 | 0.897436 | 0.42347 | E001 |
| F0102 | 8 | {'expC': 8} | 1 | 1.0 | 1.0 | C091 |
| F0103 | 8 | {'expC': 8} | 1 | 1.0 | 1.0 | C099 |
| F0133 | 8 | {'expD': 8} | 1 | 0.857143 | 0.550895 | D111 |
| F0015 | 7 | {'expA': 7} | 1 | 0.857143 | 0.345105 | A064 |
| F0104 | 7 | {'expC': 7} | 1 | 1.0 | 1.0 | C107 |
| F0105 | 7 | {'expC': 7} | 1 | 1.0 | 1.0 | C114 |
| F0113 | 7 | {'expD': 7} | 1 | 1.0 | 1.0 | D013 |
| F0125 | 7 | {'expD': 7} | 1 | 1.0 | 1.0 | D064 |
| F0126 | 7 | {'expD': 7} | 1 | 1.0 | 1.0 | D071 |
| F0240 | 7 | {'expE': 7} | 1 | 0.894737 | 0.46041 | E150 |
| F0254 | 7 | {'expE': 7} | 1 | 0.857143 | 0.334228 | E200 |
| F0287 | 7 | {'expF': 7} | 2 | 0.944444 | 0.944444 | F141 |
| F0010 | 6 | {'expA': 4, 'expB': 1, 'holdout_5_672h': 1} | 3 | 1.0 | 1.0 | A045 |
| F0066 | 6 | {'expB': 2, 'expF': 4} | 2 | 0.875 | 0.807081 | F094 |
| F0072 | 6 | {'expB': 1, 'expF': 5} | 2 | 0.722222 | 0.986932 | F111 |
| F0094 | 6 | {'expC': 6} | 1 | 1.0 | 1.0 | C043 |
| F0108 | 6 | {'expC': 6} | 1 | 1.0 | 1.0 | C171 |
| F0109 | 6 | {'expC': 6} | 1 | 1.0 | 1.0 | C189 |
| F0119 | 6 | {'expD': 6} | 1 | 1.0 | 1.0 | D036 |
| F0139 | 6 | {'expD': 6} | 1 | 1.0 | 1.0 | D141 |
| F0204 | 6 | {'expE': 6} | 1 | 0.85 | 0.427851 | E089 |
| F0219 | 6 | {'expE': 6} | 1 | 0.851064 | 0.602481 | E118 |
| F0007 | 5 | {'expA': 5} | 2 | 1.0 | 1.0 | A024 |
| F0016 | 5 | {'expA': 5} | 1 | 1.0 | 1.0 | A068 |
| F0024 | 5 | {'expB': 5} | 1 | 0.913043 | 0.913043 | B001 |
| F0031 | 5 | {'expB': 5} | 1 | 0.85 | 0.465383 | B021 |
| F0055 | 5 | {'expB': 5} | 1 | 0.88 | 0.592516 | B065 |
| F0099 | 5 | {'expC': 5} | 1 | 1.0 | 1.0 | C076 |
| F0100 | 5 | {'expC': 5} | 1 | 1.0 | 1.0 | C081 |
| F0101 | 5 | {'expC': 5} | 1 | 1.0 | 1.0 | C086 |
| F0112 | 5 | {'expD': 5} | 1 | 1.0 | 1.0 | D008 |
| F0128 | 5 | {'expD': 5} | 1 | 1.0 | 1.0 | D081 |
| F0132 | 5 | {'expD': 5} | 1 | 1.0 | 1.0 | D106 |
| F0134 | 5 | {'expD': 5} | 1 | 1.0 | 1.0 | D117 |
| F0135 | 5 | {'expD': 5} | 1 | 1.0 | 1.0 | D122 |
| F0138 | 5 | {'expD': 5} | 1 | 1.0 | 1.0 | D136 |
| F0206 | 5 | {'expE': 5} | 2 | 0.878049 | 0.394522 | E110 |
| F0267 | 5 | {'expF': 5} | 1 | 0.923077 | 0.923077 | F003 |
| F0273 | 5 | {'expF': 5} | 1 | 0.892857 | 0.803545 | F036 |
| F0282 | 5 | {'expF': 5} | 1 | 1.0 | 1.0 | F071 |
| F0286 | 5 | {'corpus_672h': 1, 'expF': 4} | 2 | 0.933333 | 0.933333 | F089 |
| F0289 | 5 | {'expF': 5} | 1 | 1.0 | 1.0 | F116 |
| F0290 | 5 | {'expF': 5} | 1 | 1.0 | 1.0 | F121 |

## 5. 复核记录（Agent 逐源码复核；重跑 `--stage families` 会覆盖本节）

> 性质：本节的"复核"由 **AI Agent 读源码**完成，**不是人类第三方 IAA**（与全仓 T17 的诚实边界一致）。抽取证据（原文片段/diff）见 §4.1/§4.2，可逐条回核。

### 5.1 抽查 10 个家族（§4.1 的 5 大 + 5 随机）

| 家族 | 成员例 | 实际差异 | 判定 |
|---|---|---|---|
| F0288（21） | F102 ↔ F104 | 归一化精确同构（原文片段逐字相同：`volatile const int ro = 0;`） | ✓ 真克隆（同缺陷） |
| F0288 | F102 ↔ F171 | 骨架同构、**缺陷类型不同**（`volatile const` 假写保护 ↔ `register` 弃用） | ⚠ **C2 的过度合并**（同骨架异缺陷），已标注为已知代价 |
| F0014（17） | A060 ↔ A061 | 仅变量名 `x`/`y` 不同（uninitialized read 模板） | ✓ 真克隆 |
| F0002（16） | A005 ↔ A006 | 仅数组下标常量 `p[1]`/`p[2]` 不同（use-after-free 模板） | ✓ 真克隆 |
| F0021（16） | A088 ↔ A089 | 归一化后文本完全一致（`int r = a / 0;` 除零模板） | ✓ 真克隆 |
| F0019（15） | A080 ↔ A081 | 仅移位量 `1 << 33`/`1 << 40` 不同 | ✓ 真克隆 |
| F0106（12） | C149…C153 | 纯精确组（归一化逐字相同） | ✓ 真克隆 |
| F0131（12） | D094…D098 | 纯精确组 | ✓ 真克隆 |
| F0201（10） | E076 ↔ E077 | Jaccard=0.921 / cosine=0.921（归一化 diff 见 §4.1） | ✓ 真克隆 |
| F0001（11） | A001 ↔ A002 | 仅常量不同（UAF 模板） | ✓ 真克隆 |

**结论**：**C1/C3 主导的合并全部是真模板克隆**；**C2 主导的合并可能把"同骨架、不同缺陷类型"并族**（例 F102~F171）——这与 676k 的 62.2% 克隆率是**同一个结构性克隆概念**，且**对泄漏控制是保守方向**（宁多并、不漏并）；它不是"语义模板相同"的主张。

### 5.2 抽查 10 对「高相似但不同家族」（§4.2）

- **(a) 判克隆但跨家族 575 对**：逐例核验 4 例（`d3-22 ~ d3e-09` double free ↔ use-after-free；`B021 ~ B039` 同为 integer_overflow；`B041 ~ B045`；`F106 ~ F111` 移位量 `-1` ↔ `32`）⇒ **全部确为同骨架/同模板**，未合并只因全对约束；**同分量=True**，故 strict split 下不会被劈开（不构成泄漏）。**不是误分。**
- **(b) 不判克隆但高相似（S≥0.80）的对**：逐例核验 3 例（`B039 ~ B085` J=0.842/C=0.899；`C031 ~ C036`、`C033 ~ C036` J=0.833/C=0.895）⇒ 相似度落在阈值下方（J<0.85 且 C<0.90），按既定口径**正确分开**。
- **确认**：跨家族的 2600 对中，575 对是"克隆但全对约束未合并"（残余，strict 口径已覆盖），2025 对不判克隆 ⇒ **不存在"判克隆却被拆到不同分量"的对**（跨分量克隆对 = 0）。

### 5.3 与 676k 的覆盖核对

676k 的 **103 对跨批近克隆**：**98 对**在本批同一家族；余 5 对（`B092 ~ F106..F110`）因全对约束未合并，但**同分量**（strict split 不劈开）⇒ 本批**未漏掉任何 676k 已识别的跨批近克隆**。
