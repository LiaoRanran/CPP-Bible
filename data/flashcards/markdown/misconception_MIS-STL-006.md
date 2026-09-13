# MIS-STL-006（misconception）

## 正面

【误解】MIS-STL-006 set/multiset 的比较器写成 <= 也没问题
触发说法：用 <= 当比较器，反正能排

## 背面

为什么错：比较器必须满足**严格弱序**（irreflexive：comp(a,a) 必须为 false）；<= 违反该条 → UB
