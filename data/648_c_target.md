# 648 A · C 语言打靶（真编译器实测）

| 编译器 | 版本 | 可用 |
|---|---|---|
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) | ✅ |
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 | ✅ |

## 十张卡的实测输出（主档位 gcc -std=c11 -O2）

| 卡 | 输出 |
|---|---|
| decay | `decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8` |
| malloc | `alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1` |
| strbound | `snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0` |
| fnptr | `bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5` |
| volatile | `sink=0` |
| setjmp | `after_longjmp_plain=0 after_longjmp_volatile=5` |
| intpromo | `char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295` |
| bitfield | `bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4` |
| macro | `i_after=2 max_bad_result=1 sq_bad=7 sq_good=16` |
| signedovf | `signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0` |

失败组合：**0**（无）

