
ch85_unordered_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)>:
   0:	53                   	push   rbx
   1:	41 89 d0             	mov    r8d,edx
   4:	48 83 79 18 00       	cmp    QWORD PTR [rcx+0x18],0x0
   9:	74 6d                	je     78 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x78>
   b:	4c 8b 59 08          	mov    r11,QWORD PTR [rcx+0x8]
   f:	48 63 c2             	movsxd rax,edx
  12:	31 d2                	xor    edx,edx
  14:	49 f7 f3             	div    r11
  17:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  1a:	48 8b 0c d0          	mov    rcx,QWORD PTR [rax+rdx*8]
  1e:	48 89 d3             	mov    rbx,rdx
  21:	48 85 c9             	test   rcx,rcx
  24:	74 5b                	je     81 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x81>
  26:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  29:	44 8b 50 08          	mov    r10d,DWORD PTR [rax+0x8]
  2d:	45 39 c2             	cmp    r10d,r8d
  30:	74 2e                	je     60 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x60>
  32:	4c 8b 08             	mov    r9,QWORD PTR [rax]
  35:	4d 85 c9             	test   r9,r9
  38:	74 47                	je     81 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x81>
  3a:	45 8b 51 08          	mov    r10d,DWORD PTR [r9+0x8]
  3e:	48 89 c1             	mov    rcx,rax
  41:	31 d2                	xor    edx,edx
  43:	49 63 c2             	movsxd rax,r10d
  46:	49 f7 f3             	div    r11
  49:	48 39 da             	cmp    rdx,rbx
  4c:	75 33                	jne    81 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x81>
  4e:	4c 89 c8             	mov    rax,r9
  51:	45 39 c2             	cmp    r10d,r8d
  54:	75 dc                	jne    32 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x32>
  56:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  5d:	00 00 00 
  60:	48 8b 11             	mov    rdx,QWORD PTR [rcx]
  63:	b8 ff ff ff ff       	mov    eax,0xffffffff
  68:	48 85 d2             	test   rdx,rdx
  6b:	74 03                	je     70 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x70>
  6d:	8b 42 0c             	mov    eax,DWORD PTR [rdx+0xc]
  70:	5b                   	pop    rbx
  71:	c3                   	ret
  72:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
  78:	48 8b 41 10          	mov    rax,QWORD PTR [rcx+0x10]
  7c:	48 85 c0             	test   rax,rax
  7f:	75 0f                	jne    90 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x90>
  81:	b8 ff ff ff ff       	mov    eax,0xffffffff
  86:	5b                   	pop    rbx
  87:	c3                   	ret
  88:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  8f:	00 
  90:	48 83 c1 10          	add    rcx,0x10
  94:	eb 18                	jmp    ae <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0xae>
  96:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  9d:	00 00 00 
  a0:	48 8b 10             	mov    rdx,QWORD PTR [rax]
  a3:	48 89 c1             	mov    rcx,rax
  a6:	48 85 d2             	test   rdx,rdx
  a9:	74 d6                	je     81 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x81>
  ab:	48 89 d0             	mov    rax,rdx
  ae:	44 39 40 08          	cmp    DWORD PTR [rax+0x8],r8d
  b2:	75 ec                	jne    a0 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0xa0>
  b4:	eb aa                	jmp    60 <find_it(std::unordered_map<int, int, std::hash<int>, std::equal_to<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x60>
  b6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  bd:	00 00 00 

00000000000000c0 <build()>:
  c0:	56                   	push   rsi
  c1:	53                   	push   rbx
  c2:	48 83 ec 38          	sub    rsp,0x38
  c6:	48 8d 41 30          	lea    rax,[rcx+0x30]
  ca:	48 c7 41 08 01 00 00 	mov    QWORD PTR [rcx+0x8],0x1
  d1:	00 
  d2:	48 8d 54 24 2c       	lea    rdx,[rsp+0x2c]
  d7:	48 89 cb             	mov    rbx,rcx
  da:	48 89 01             	mov    QWORD PTR [rcx],rax
  dd:	48 c7 41 10 00 00 00 	mov    QWORD PTR [rcx+0x10],0x0
  e4:	00 
  e5:	48 c7 41 18 00 00 00 	mov    QWORD PTR [rcx+0x18],0x0
  ec:	00 
  ed:	c7 41 20 00 00 80 3f 	mov    DWORD PTR [rcx+0x20],0x3f800000
  f4:	48 c7 41 28 00 00 00 	mov    QWORD PTR [rcx+0x28],0x0
  fb:	00 
  fc:	48 c7 41 30 00 00 00 	mov    QWORD PTR [rcx+0x30],0x0
 103:	00 
 104:	c7 44 24 2c 01 00 00 	mov    DWORD PTR [rsp+0x2c],0x1
 10b:	00 
 10c:	e8 00 00 00 00       	call   111 <build()+0x51>
 111:	c7 00 0a 00 00 00    	mov    DWORD PTR [rax],0xa
 117:	48 8d 54 24 2c       	lea    rdx,[rsp+0x2c]
 11c:	48 89 d9             	mov    rcx,rbx
 11f:	c7 44 24 2c 02 00 00 	mov    DWORD PTR [rsp+0x2c],0x2
 126:	00 
 127:	e8 00 00 00 00       	call   12c <build()+0x6c>
 12c:	c7 00 14 00 00 00    	mov    DWORD PTR [rax],0x14
 132:	48 8d 54 24 2c       	lea    rdx,[rsp+0x2c]
 137:	48 89 d9             	mov    rcx,rbx
 13a:	c7 44 24 2c 03 00 00 	mov    DWORD PTR [rsp+0x2c],0x3
 141:	00 
 142:	e8 00 00 00 00       	call   147 <build()+0x87>
 147:	c7 00 1e 00 00 00    	mov    DWORD PTR [rax],0x1e
 14d:	48 89 d8             	mov    rax,rbx
 150:	48 83 c4 38          	add    rsp,0x38
 154:	5b                   	pop    rbx
 155:	5e                   	pop    rsi
 156:	c3                   	ret
 157:	48 89 c6             	mov    rsi,rax
 15a:	e9 00 00 00 00       	jmp    15f <build()+0x9f>
 15f:	90                   	nop

Disassembly of section .text$_ZNSt10_HashtableIiSt4pairIKiiESaIS2_ENSt8__detail10_Select1stESt8equal_toIiESt4hashIiENS4_18_Mod_range_hashingENS4_20_Default_ranged_hashENS4_20_Prime_rehash_policyENS4_17_Hashtable_traitsILb0ELb0ELb1EEEED1Ev:

0000000000000000 <std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable()>:
   0:	56                   	push   rsi
   1:	53                   	push   rbx
   2:	48 83 ec 28          	sub    rsp,0x28
   6:	48 8b 59 10          	mov    rbx,QWORD PTR [rcx+0x10]
   a:	48 89 ce             	mov    rsi,rcx
   d:	48 85 db             	test   rbx,rbx
  10:	74 23                	je     35 <std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable()+0x35>
  12:	0f 1f 00             	nop    DWORD PTR [rax]
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 
  20:	48 89 d9             	mov    rcx,rbx
  23:	48 8b 1b             	mov    rbx,QWORD PTR [rbx]
  26:	ba 10 00 00 00       	mov    edx,0x10
  2b:	e8 00 00 00 00       	call   30 <std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable()+0x30>
  30:	48 85 db             	test   rbx,rbx
  33:	75 eb                	jne    20 <std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable()+0x20>
  35:	48 8b 0e             	mov    rcx,QWORD PTR [rsi]
  38:	48 8d 46 30          	lea    rax,[rsi+0x30]
  3c:	48 39 c1             	cmp    rcx,rax
  3f:	74 17                	je     58 <std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable()+0x58>
  41:	48 8b 56 08          	mov    rdx,QWORD PTR [rsi+0x8]
  45:	48 c1 e2 03          	shl    rdx,0x3
  49:	48 83 c4 28          	add    rsp,0x28
  4d:	5b                   	pop    rbx
  4e:	5e                   	pop    rsi
  4f:	e9 00 00 00 00       	jmp    54 <std::_Hashtable<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable()+0x54>
  54:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  58:	48 83 c4 28          	add    rsp,0x28
  5c:	5b                   	pop    rbx
  5d:	5e                   	pop    rsi
  5e:	c3                   	ret
  5f:	90                   	nop

Disassembly of section .text$_ZNSt8__detail9_Map_baseIiSt4pairIKiiESaIS3_ENS_10_Select1stESt8equal_toIiESt4hashIiENS_18_Mod_range_hashingENS_20_Default_ranged_hashENS_20_Prime_rehash_policyENS_17_Hashtable_traitsILb0ELb0ELb1EEELb1EEixEOi:

0000000000000000 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)>:
   0:	41 55                	push   r13
   2:	41 54                	push   r12
   4:	55                   	push   rbp
   5:	57                   	push   rdi
   6:	56                   	push   rsi
   7:	53                   	push   rbx
   8:	48 83 ec 58          	sub    rsp,0x58
   c:	48 63 32             	movsxd rsi,DWORD PTR [rdx]
   f:	4c 8b 41 08          	mov    r8,QWORD PTR [rcx+0x8]
  13:	48 89 f0             	mov    rax,rsi
  16:	49 89 f5             	mov    r13,rsi
  19:	49 89 d4             	mov    r12,rdx
  1c:	31 d2                	xor    edx,edx
  1e:	48 89 cb             	mov    rbx,rcx
  21:	49 f7 f0             	div    r8
  24:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  27:	4c 8b 1c d0          	mov    r11,QWORD PTR [rax+rdx*8]
  2b:	48 89 d5             	mov    rbp,rdx
  2e:	48 8d 3c d5 00 00 00 	lea    rdi,[rdx*8+0x0]
  35:	00 
  36:	4d 85 db             	test   r11,r11
  39:	74 4d                	je     88 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x88>
  3b:	4d 8b 0b             	mov    r9,QWORD PTR [r11]
  3e:	45 8b 51 08          	mov    r10d,DWORD PTR [r9+0x8]
  42:	45 39 d5             	cmp    r13d,r10d
  45:	74 24                	je     6b <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x6b>
  47:	49 8b 09             	mov    rcx,QWORD PTR [r9]
  4a:	48 85 c9             	test   rcx,rcx
  4d:	74 39                	je     88 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x88>
  4f:	48 63 41 08          	movsxd rax,DWORD PTR [rcx+0x8]
  53:	31 d2                	xor    edx,edx
  55:	4d 89 cb             	mov    r11,r9
  58:	49 89 c2             	mov    r10,rax
  5b:	49 f7 f0             	div    r8
  5e:	48 39 d5             	cmp    rbp,rdx
  61:	75 25                	jne    88 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x88>
  63:	49 89 c9             	mov    r9,rcx
  66:	45 39 d5             	cmp    r13d,r10d
  69:	75 dc                	jne    47 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x47>
  6b:	49 8b 13             	mov    rdx,QWORD PTR [r11]
  6e:	48 8d 42 0c          	lea    rax,[rdx+0xc]
  72:	48 85 d2             	test   rdx,rdx
  75:	74 11                	je     88 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x88>
  77:	48 83 c4 58          	add    rsp,0x58
  7b:	5b                   	pop    rbx
  7c:	5e                   	pop    rsi
  7d:	5f                   	pop    rdi
  7e:	5d                   	pop    rbp
  7f:	41 5c                	pop    r12
  81:	41 5d                	pop    r13
  83:	c3                   	ret
  84:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  88:	b9 10 00 00 00       	mov    ecx,0x10
  8d:	4c 89 44 24 38       	mov    QWORD PTR [rsp+0x38],r8
  92:	e8 00 00 00 00       	call   97 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x97>
  97:	4c 8b 6b 28          	mov    r13,QWORD PTR [rbx+0x28]
  9b:	4c 8b 44 24 38       	mov    r8,QWORD PTR [rsp+0x38]
  a0:	48 8d 4c 24 40       	lea    rcx,[rsp+0x40]
  a5:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
  ac:	48 89 c5             	mov    rbp,rax
  af:	41 8b 04 24          	mov    eax,DWORD PTR [r12]
  b3:	48 8d 53 20          	lea    rdx,[rbx+0x20]
  b7:	c7 45 0c 00 00 00 00 	mov    DWORD PTR [rbp+0xc],0x0
  be:	89 45 08             	mov    DWORD PTR [rbp+0x8],eax
  c1:	48 c7 44 24 20 01 00 	mov    QWORD PTR [rsp+0x20],0x1
  c8:	00 00 
  ca:	4c 8b 4b 18          	mov    r9,QWORD PTR [rbx+0x18]
  ce:	e8 00 00 00 00       	call   d3 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0xd3>
  d3:	4c 8b 64 24 48       	mov    r12,QWORD PTR [rsp+0x48]
  d8:	80 7c 24 40 00       	cmp    BYTE PTR [rsp+0x40],0x0
  dd:	75 39                	jne    118 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x118>
  df:	4c 8b 2b             	mov    r13,QWORD PTR [rbx]
  e2:	4c 01 ef             	add    rdi,r13
  e5:	48 8b 07             	mov    rax,QWORD PTR [rdi]
  e8:	48 85 c0             	test   rax,rax
  eb:	0f 84 e8 00 00 00    	je     1d9 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x1d9>
  f1:	48 8b 00             	mov    rax,QWORD PTR [rax]
  f4:	48 89 45 00          	mov    QWORD PTR [rbp+0x0],rax
  f8:	48 8b 07             	mov    rax,QWORD PTR [rdi]
  fb:	48 89 28             	mov    QWORD PTR [rax],rbp
  fe:	48 83 43 18 01       	add    QWORD PTR [rbx+0x18],0x1
 103:	48 8d 45 0c          	lea    rax,[rbp+0xc]
 107:	48 83 c4 58          	add    rsp,0x58
 10b:	5b                   	pop    rbx
 10c:	5e                   	pop    rsi
 10d:	5f                   	pop    rdi
 10e:	5d                   	pop    rbp
 10f:	41 5c                	pop    r12
 111:	41 5d                	pop    r13
 113:	c3                   	ret
 114:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 118:	49 83 fc 01          	cmp    r12,0x1
 11c:	0f 84 12 01 00 00    	je     234 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x234>
 122:	4c 89 e0             	mov    rax,r12
 125:	48 c1 e8 3c          	shr    rax,0x3c
 129:	0f 85 fa 00 00 00    	jne    229 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x229>
 12f:	4a 8d 0c e5 00 00 00 	lea    rcx,[r12*8+0x0]
 136:	00 
 137:	e8 00 00 00 00       	call   13c <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x13c>
 13c:	4e 8d 04 e5 00 00 00 	lea    r8,[r12*8+0x0]
 143:	00 
 144:	31 d2                	xor    edx,edx
 146:	48 89 c1             	mov    rcx,rax
 149:	49 89 c5             	mov    r13,rax
 14c:	e8 00 00 00 00       	call   151 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x151>
 151:	4c 8d 5b 30          	lea    r11,[rbx+0x30]
 155:	4c 8b 43 10          	mov    r8,QWORD PTR [rbx+0x10]
 159:	48 c7 43 10 00 00 00 	mov    QWORD PTR [rbx+0x10],0x0
 160:	00 
 161:	45 31 d2             	xor    r10d,r10d
 164:	4c 8d 4b 10          	lea    r9,[rbx+0x10]
 168:	4d 85 c0             	test   r8,r8
 16b:	74 2d                	je     19a <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x19a>
 16d:	4c 89 c1             	mov    rcx,r8
 170:	31 d2                	xor    edx,edx
 172:	4d 8b 00             	mov    r8,QWORD PTR [r8]
 175:	48 63 41 08          	movsxd rax,DWORD PTR [rcx+0x8]
 179:	49 f7 f4             	div    r12
 17c:	49 8d 44 d5 00       	lea    rax,[r13+rdx*8+0x0]
 181:	48 8b 38             	mov    rdi,QWORD PTR [rax]
 184:	48 85 ff             	test   rdi,rdi
 187:	74 7f                	je     208 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x208>
 189:	48 8b 17             	mov    rdx,QWORD PTR [rdi]
 18c:	48 89 11             	mov    QWORD PTR [rcx],rdx
 18f:	48 8b 00             	mov    rax,QWORD PTR [rax]
 192:	48 89 08             	mov    QWORD PTR [rax],rcx
 195:	4d 85 c0             	test   r8,r8
 198:	75 d3                	jne    16d <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x16d>
 19a:	48 8b 0b             	mov    rcx,QWORD PTR [rbx]
 19d:	4c 39 d9             	cmp    rcx,r11
 1a0:	74 11                	je     1b3 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x1b3>
 1a2:	48 8b 43 08          	mov    rax,QWORD PTR [rbx+0x8]
 1a6:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
 1ad:	00 
 1ae:	e8 00 00 00 00       	call   1b3 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x1b3>
 1b3:	48 89 f0             	mov    rax,rsi
 1b6:	31 d2                	xor    edx,edx
 1b8:	4c 89 63 08          	mov    QWORD PTR [rbx+0x8],r12
 1bc:	49 f7 f4             	div    r12
 1bf:	4c 89 2b             	mov    QWORD PTR [rbx],r13
 1c2:	48 8d 3c d5 00 00 00 	lea    rdi,[rdx*8+0x0]
 1c9:	00 
 1ca:	4c 01 ef             	add    rdi,r13
 1cd:	48 8b 07             	mov    rax,QWORD PTR [rdi]
 1d0:	48 85 c0             	test   rax,rax
 1d3:	0f 85 18 ff ff ff    	jne    f1 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0xf1>
 1d9:	48 8b 43 10          	mov    rax,QWORD PTR [rbx+0x10]
 1dd:	48 89 6b 10          	mov    QWORD PTR [rbx+0x10],rbp
 1e1:	48 89 45 00          	mov    QWORD PTR [rbp+0x0],rax
 1e5:	48 85 c0             	test   rax,rax
 1e8:	74 0f                	je     1f9 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x1f9>
 1ea:	48 63 40 08          	movsxd rax,DWORD PTR [rax+0x8]
 1ee:	31 d2                	xor    edx,edx
 1f0:	48 f7 73 08          	div    QWORD PTR [rbx+0x8]
 1f4:	49 89 6c d5 00       	mov    QWORD PTR [r13+rdx*8+0x0],rbp
 1f9:	48 8d 43 10          	lea    rax,[rbx+0x10]
 1fd:	48 89 07             	mov    QWORD PTR [rdi],rax
 200:	e9 f9 fe ff ff       	jmp    fe <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0xfe>
 205:	0f 1f 00             	nop    DWORD PTR [rax]
 208:	48 8b 7b 10          	mov    rdi,QWORD PTR [rbx+0x10]
 20c:	48 89 39             	mov    QWORD PTR [rcx],rdi
 20f:	48 89 4b 10          	mov    QWORD PTR [rbx+0x10],rcx
 213:	4c 89 08             	mov    QWORD PTR [rax],r9
 216:	48 83 39 00          	cmp    QWORD PTR [rcx],0x0
 21a:	74 05                	je     221 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x221>
 21c:	4b 89 4c d5 00       	mov    QWORD PTR [r13+r10*8+0x0],rcx
 221:	49 89 d2             	mov    r10,rdx
 224:	e9 3f ff ff ff       	jmp    168 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x168>
 229:	49 c1 ec 3d          	shr    r12,0x3d
 22d:	74 19                	je     248 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x248>
 22f:	e8 00 00 00 00       	call   234 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x234>
 234:	4c 8d 5b 30          	lea    r11,[rbx+0x30]
 238:	48 c7 43 30 00 00 00 	mov    QWORD PTR [rbx+0x30],0x0
 23f:	00 
 240:	4d 89 dd             	mov    r13,r11
 243:	e9 0d ff ff ff       	jmp    155 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x155>
 248:	e8 00 00 00 00       	call   24d <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x24d>
 24d:	48 89 c6             	mov    rsi,rax
 250:	4c 89 6b 28          	mov    QWORD PTR [rbx+0x28],r13
 254:	48 89 e9             	mov    rcx,rbp
 257:	ba 10 00 00 00       	mov    edx,0x10
 25c:	e8 00 00 00 00       	call   261 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x261>
 261:	48 89 f1             	mov    rcx,rsi
 264:	e8 00 00 00 00       	call   269 <std::__detail::_Map_base<int, std::pair<int const, int>, std::allocator<std::pair<int const, int> >, std::__detail::_Select1st, std::equal_to<int>, std::hash<int>, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true>, true>::operator[](int&&)+0x269>
 269:	90                   	nop
 26a:	90                   	nop
 26b:	90                   	nop
 26c:	90                   	nop
 26d:	90                   	nop
 26e:	90                   	nop
 26f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <build() [clone .cold]>:
   0:	48 89 d9             	mov    rcx,rbx
   3:	e8 00 00 00 00       	call   8 <build() [clone .cold]+0x8>
   8:	48 89 f1             	mov    rcx,rsi
   b:	e8 00 00 00 00       	call   10 <build() [clone .cold]+0x10>
  10:	90                   	nop
  11:	90                   	nop
  12:	90                   	nop
  13:	90                   	nop
  14:	90                   	nop
  15:	90                   	nop
  16:	90                   	nop
  17:	90                   	nop
  18:	90                   	nop
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	56                   	push   rsi
   1:	53                   	push   rbx
   2:	48 83 ec 78          	sub    rsp,0x78
   6:	e8 00 00 00 00       	call   b <main+0xb>
   b:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
  10:	e8 c0 00 00 00       	call   d5 <build()+0x15>
  15:	ba 02 00 00 00       	mov    edx,0x2
  1a:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
  1f:	e8 00 00 00 00       	call   24 <main+0x24>
  24:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
  29:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  2d:	8b 74 24 2c          	mov    esi,DWORD PTR [rsp+0x2c]
  31:	e8 00 00 00 00       	call   36 <main+0x36>
  36:	89 f0                	mov    eax,esi
  38:	48 83 c4 78          	add    rsp,0x78
  3c:	5b                   	pop    rbx
  3d:	5e                   	pop    rsi
  3e:	c3                   	ret
  3f:	90                   	nop
