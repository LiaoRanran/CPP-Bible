
ch08_ranges_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>:
   0:	41 57                	push   r15
   2:	41 56                	push   r14
   4:	41 55                	push   r13
   6:	41 54                	push   r12
   8:	55                   	push   rbp
   9:	57                   	push   rdi
   a:	56                   	push   rsi
   b:	53                   	push   rbx
   c:	48 83 ec 28          	sub    rsp,0x28
  10:	48 89 d0             	mov    rax,rdx
  13:	48 89 ce             	mov    rsi,rcx
  16:	4c 89 c7             	mov    rdi,r8
  19:	49 89 d3             	mov    r11,rdx
  1c:	48 29 c8             	sub    rax,rcx
  1f:	48 83 f8 40          	cmp    rax,0x40
  23:	0f 8e 6e 02 00 00    	jle    297 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x297>
  29:	48 89 c5             	mov    rbp,rax
  2c:	48 c1 f8 03          	sar    rax,0x3
  30:	48 c1 fd 02          	sar    rbp,0x2
  34:	48 85 ff             	test   rdi,rdi
  37:	0f 84 08 01 00 00    	je     145 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x145>
  3d:	f3 0f 7e 06          	movq   xmm0,QWORD PTR [rsi]
  41:	4c 8d 14 86          	lea    r10,[rsi+rax*4]
  45:	45 8b 4b fc          	mov    r9d,DWORD PTR [r11-0x4]
  49:	48 83 ef 01          	sub    rdi,0x1
  4d:	45 8b 02             	mov    r8d,DWORD PTR [r10]
  50:	48 8d 46 04          	lea    rax,[rsi+0x4]
  54:	66 0f 70 c8 e5       	pshufd xmm1,xmm0,0xe5
  59:	66 0f 7e ca          	movd   edx,xmm1
  5d:	66 0f 7e c1          	movd   ecx,xmm0
  61:	44 39 c2             	cmp    edx,r8d
  64:	0f 8d fe 01 00 00    	jge    268 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x268>
  6a:	45 39 c8             	cmp    r8d,r9d
  6d:	0f 8c 14 02 00 00    	jl     287 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x287>
  73:	44 39 ca             	cmp    edx,r9d
  76:	0f 8c fa 01 00 00    	jl     276 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x276>
  7c:	66 0f 70 c0 e1       	pshufd xmm0,xmm0,0xe1
  81:	66 0f d6 06          	movq   QWORD PTR [rsi],xmm0
  85:	4d 89 da             	mov    r10,r11
  88:	39 d1                	cmp    ecx,edx
  8a:	7d 5b                	jge    e7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xe7>
  8c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  90:	48 83 c0 04          	add    rax,0x4
  94:	90                   	nop
  95:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  9c:	00 00 00 00 
  a0:	49 89 c1             	mov    r9,rax
  a3:	8b 08                	mov    ecx,DWORD PTR [rax]
  a5:	48 83 c0 04          	add    rax,0x4
  a9:	39 d1                	cmp    ecx,edx
  ab:	7c f3                	jl     a0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xa0>
  ad:	4c 89 cb             	mov    rbx,r9
  b0:	45 8b 4a fc          	mov    r9d,DWORD PTR [r10-0x4]
  b4:	41 39 d1             	cmp    r9d,edx
  b7:	7e 47                	jle    100 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x100>
  b9:	49 8d 42 f8          	lea    rax,[r10-0x8]
  bd:	0f 1f 00             	nop    DWORD PTR [rax]
  c0:	49 89 c2             	mov    r10,rax
  c3:	44 8b 08             	mov    r9d,DWORD PTR [rax]
  c6:	48 83 e8 04          	sub    rax,0x4
  ca:	41 39 d1             	cmp    r9d,edx
  cd:	7f f1                	jg     c0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xc0>
  cf:	4c 39 d3             	cmp    rbx,r10
  d2:	73 3c                	jae    110 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x110>
  d4:	44 89 0b             	mov    DWORD PTR [rbx],r9d
  d7:	48 8d 43 04          	lea    rax,[rbx+0x4]
  db:	41 89 0a             	mov    DWORD PTR [r10],ecx
  de:	8b 16                	mov    edx,DWORD PTR [rsi]
  e0:	8b 4b 04             	mov    ecx,DWORD PTR [rbx+0x4]
  e3:	39 d1                	cmp    ecx,edx
  e5:	7c a9                	jl     90 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x90>
  e7:	45 8b 4a fc          	mov    r9d,DWORD PTR [r10-0x4]
  eb:	48 89 c3             	mov    rbx,rax
  ee:	41 39 d1             	cmp    r9d,edx
  f1:	7f c6                	jg     b9 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xb9>
  f3:	66 90                	xchg   ax,ax
  f5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  fc:	00 00 00 00 
 100:	49 83 ea 04          	sub    r10,0x4
 104:	4c 39 d3             	cmp    rbx,r10
 107:	72 cb                	jb     d4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0xd4>
 109:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 110:	49 89 f8             	mov    r8,rdi
 113:	4c 89 da             	mov    rdx,r11
 116:	48 89 d9             	mov    rcx,rbx
 119:	e8 e2 fe ff ff       	call   0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
 11e:	48 89 d8             	mov    rax,rbx
 121:	48 29 f0             	sub    rax,rsi
 124:	48 83 f8 40          	cmp    rax,0x40
 128:	0f 8e 69 01 00 00    	jle    297 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x297>
 12e:	48 89 c5             	mov    rbp,rax
 131:	49 89 db             	mov    r11,rbx
 134:	48 c1 f8 03          	sar    rax,0x3
 138:	48 c1 fd 02          	sar    rbp,0x2
 13c:	48 85 ff             	test   rdi,rdi
 13f:	0f 85 f8 fe ff ff    	jne    3d <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3d>
 145:	4c 8d 55 ff          	lea    r10,[rbp-0x1]
 149:	48 8d 5c 86 fc       	lea    rbx,[rsi+rax*4-0x4]
 14e:	4c 8d 40 ff          	lea    r8,[rax-0x1]
 152:	49 d1 fa             	sar    r10,1
 155:	44 8b 0b             	mov    r9d,DWORD PTR [rbx]
 158:	48 89 d9             	mov    rcx,rbx
 15b:	4c 89 c7             	mov    rdi,r8
 15e:	4d 39 d0             	cmp    r8,r10
 161:	0f 8d ea 00 00 00    	jge    251 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x251>
 167:	4d 89 c4             	mov    r12,r8
 16a:	eb 17                	jmp    183 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x183>
 16c:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 173:	00 00 
 175:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 17c:	00 00 00 00 
 180:	49 89 c4             	mov    r12,rax
 183:	49 8d 54 24 01       	lea    rdx,[r12+0x1]
 188:	4c 8d 2c 12          	lea    r13,[rdx+rdx*1]
 18c:	4c 8d 34 d6          	lea    r14,[rsi+rdx*8]
 190:	49 8d 45 ff          	lea    rax,[r13-0x1]
 194:	45 8b 3e             	mov    r15d,DWORD PTR [r14]
 197:	48 8d 0c 86          	lea    rcx,[rsi+rax*4]
 19b:	8b 11                	mov    edx,DWORD PTR [rcx]
 19d:	44 39 fa             	cmp    edx,r15d
 1a0:	41 0f 4e d7          	cmovle edx,r15d
 1a4:	49 0f 4e c5          	cmovle rax,r13
 1a8:	49 0f 4e ce          	cmovle rcx,r14
 1ac:	42 89 14 a6          	mov    DWORD PTR [rsi+r12*4],edx
 1b0:	4c 39 d0             	cmp    rax,r10
 1b3:	7c cb                	jl     180 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x180>
 1b5:	40 f6 c5 01          	test   bpl,0x1
 1b9:	75 09                	jne    1c4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1c4>
 1bb:	48 39 c7             	cmp    rdi,rax
 1be:	0f 84 30 02 00 00    	je     3f4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3f4>
 1c4:	48 8d 50 ff          	lea    rdx,[rax-0x1]
 1c8:	48 d1 fa             	sar    rdx,1
 1cb:	49 39 c0             	cmp    r8,rax
 1ce:	7c 51                	jl     221 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x221>
 1d0:	e9 8b 00 00 00       	jmp    260 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x260>
 1d5:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 1dc:	00 00 00 
 1df:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 1e6:	00 00 00 00 
 1ea:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 1f1:	00 00 00 00 
 1f5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 1fc:	00 00 00 00 
 200:	89 08                	mov    DWORD PTR [rax],ecx
 202:	48 8d 42 ff          	lea    rax,[rdx-0x1]
 206:	48 c1 e8 3f          	shr    rax,0x3f
 20a:	48 8d 4c 10 ff       	lea    rcx,[rax+rdx*1-0x1]
 20f:	48 89 d0             	mov    rax,rdx
 212:	49 39 d0             	cmp    r8,rdx
 215:	0f 8d 8d 00 00 00    	jge    2a8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2a8>
 21b:	48 89 ca             	mov    rdx,rcx
 21e:	48 d1 fa             	sar    rdx,1
 221:	4c 8d 24 96          	lea    r12,[rsi+rdx*4]
 225:	48 8d 04 86          	lea    rax,[rsi+rax*4]
 229:	41 8b 0c 24          	mov    ecx,DWORD PTR [r12]
 22d:	41 39 c9             	cmp    r9d,ecx
 230:	7f ce                	jg     200 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x200>
 232:	44 89 08             	mov    DWORD PTR [rax],r9d
 235:	4d 85 c0             	test   r8,r8
 238:	74 79                	je     2b3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2b3>
 23a:	48 83 eb 04          	sub    rbx,0x4
 23e:	49 83 e8 01          	sub    r8,0x1
 242:	44 8b 0b             	mov    r9d,DWORD PTR [rbx]
 245:	48 89 d9             	mov    rcx,rbx
 248:	4d 39 d0             	cmp    r8,r10
 24b:	0f 8c 16 ff ff ff    	jl     167 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x167>
 251:	40 f6 c5 01          	test   bpl,0x1
 255:	75 09                	jne    260 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x260>
 257:	49 39 f8             	cmp    r8,rdi
 25a:	0f 84 91 01 00 00    	je     3f1 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3f1>
 260:	44 89 09             	mov    DWORD PTR [rcx],r9d
 263:	eb d5                	jmp    23a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x23a>
 265:	0f 1f 00             	nop    DWORD PTR [rax]
 268:	44 39 ca             	cmp    edx,r9d
 26b:	0f 8c 0b fe ff ff    	jl     7c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x7c>
 271:	45 39 c8             	cmp    r8d,r9d
 274:	7d 11                	jge    287 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x287>
 276:	44 89 0e             	mov    DWORD PTR [rsi],r9d
 279:	41 89 4b fc          	mov    DWORD PTR [r11-0x4],ecx
 27d:	8b 4e 04             	mov    ecx,DWORD PTR [rsi+0x4]
 280:	8b 16                	mov    edx,DWORD PTR [rsi]
 282:	e9 fe fd ff ff       	jmp    85 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x85>
 287:	44 89 06             	mov    DWORD PTR [rsi],r8d
 28a:	41 89 0a             	mov    DWORD PTR [r10],ecx
 28d:	8b 4e 04             	mov    ecx,DWORD PTR [rsi+0x4]
 290:	8b 16                	mov    edx,DWORD PTR [rsi]
 292:	e9 ee fd ff ff       	jmp    85 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x85>
 297:	48 83 c4 28          	add    rsp,0x28
 29b:	5b                   	pop    rbx
 29c:	5e                   	pop    rsi
 29d:	5f                   	pop    rdi
 29e:	5d                   	pop    rbp
 29f:	41 5c                	pop    r12
 2a1:	41 5d                	pop    r13
 2a3:	41 5e                	pop    r14
 2a5:	41 5f                	pop    r15
 2a7:	c3                   	ret
 2a8:	4c 89 e0             	mov    rax,r12
 2ab:	44 89 08             	mov    DWORD PTR [rax],r9d
 2ae:	4d 85 c0             	test   r8,r8
 2b1:	75 87                	jne    23a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x23a>
 2b3:	4c 89 d8             	mov    rax,r11
 2b6:	4d 8d 4b fc          	lea    r9,[r11-0x4]
 2ba:	48 29 f0             	sub    rax,rsi
 2bd:	48 83 f8 04          	cmp    rax,0x4
 2c1:	7e d4                	jle    297 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x297>
 2c3:	66 90                	xchg   ax,ax
 2c5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 2cc:	00 00 00 00 
 2d0:	4d 89 ca             	mov    r10,r9
 2d3:	8b 06                	mov    eax,DWORD PTR [rsi]
 2d5:	45 8b 01             	mov    r8d,DWORD PTR [r9]
 2d8:	49 29 f2             	sub    r10,rsi
 2db:	4d 89 d5             	mov    r13,r10
 2de:	41 89 01             	mov    DWORD PTR [r9],eax
 2e1:	49 c1 fd 02          	sar    r13,0x2
 2e5:	49 83 fa 08          	cmp    r10,0x8
 2e9:	0f 8e d9 00 00 00    	jle    3c8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3c8>
 2ef:	4d 8d 65 ff          	lea    r12,[r13-0x1]
 2f3:	31 ed                	xor    ebp,ebp
 2f5:	49 d1 fc             	sar    r12,1
 2f8:	eb 09                	jmp    303 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x303>
 2fa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 300:	48 89 c5             	mov    rbp,rax
 303:	48 8d 55 01          	lea    rdx,[rbp+0x1]
 307:	4c 8d 1c 12          	lea    r11,[rdx+rdx*1]
 30b:	48 8d 1c d6          	lea    rbx,[rsi+rdx*8]
 30f:	49 8d 43 ff          	lea    rax,[r11-0x1]
 313:	8b 3b                	mov    edi,DWORD PTR [rbx]
 315:	48 8d 0c 86          	lea    rcx,[rsi+rax*4]
 319:	8b 11                	mov    edx,DWORD PTR [rcx]
 31b:	39 fa                	cmp    edx,edi
 31d:	0f 4e d7             	cmovle edx,edi
 320:	49 0f 4e c3          	cmovle rax,r11
 324:	48 0f 4e cb          	cmovle rcx,rbx
 328:	89 14 ae             	mov    DWORD PTR [rsi+rbp*4],edx
 32b:	49 39 c4             	cmp    r12,rax
 32e:	7f d0                	jg     300 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x300>
 330:	41 83 e5 01          	and    r13d,0x1
 334:	75 14                	jne    34a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x34a>
 336:	4c 89 d2             	mov    rdx,r10
 339:	48 c1 fa 03          	sar    rdx,0x3
 33d:	48 83 ea 01          	sub    rdx,0x1
 341:	48 39 c2             	cmp    rdx,rax
 344:	0f 84 8f 00 00 00    	je     3d9 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3d9>
 34a:	48 8d 50 ff          	lea    rdx,[rax-0x1]
 34e:	48 c1 ea 3f          	shr    rdx,0x3f
 352:	48 8d 54 10 ff       	lea    rdx,[rax+rdx*1-0x1]
 357:	48 d1 fa             	sar    rdx,1
 35a:	48 85 c0             	test   rax,rax
 35d:	75 3e                	jne    39d <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x39d>
 35f:	e9 ab 00 00 00       	jmp    40f <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x40f>
 364:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 36a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 371:	00 00 00 00 
 375:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 37c:	00 00 00 00 
 380:	89 08                	mov    DWORD PTR [rax],ecx
 382:	48 8d 42 ff          	lea    rax,[rdx-0x1]
 386:	48 c1 e8 3f          	shr    rax,0x3f
 38a:	48 8d 4c 10 ff       	lea    rcx,[rax+rdx*1-0x1]
 38f:	48 89 d0             	mov    rax,rdx
 392:	48 85 d2             	test   rdx,rdx
 395:	74 2c                	je     3c3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3c3>
 397:	48 d1 f9             	sar    rcx,1
 39a:	48 89 ca             	mov    rdx,rcx
 39d:	4c 8d 1c 96          	lea    r11,[rsi+rdx*4]
 3a1:	48 8d 04 86          	lea    rax,[rsi+rax*4]
 3a5:	41 8b 0b             	mov    ecx,DWORD PTR [r11]
 3a8:	41 39 c8             	cmp    r8d,ecx
 3ab:	7f d3                	jg     380 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x380>
 3ad:	44 89 00             	mov    DWORD PTR [rax],r8d
 3b0:	49 83 fa 04          	cmp    r10,0x4
 3b4:	0f 8e dd fe ff ff    	jle    297 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x297>
 3ba:	49 83 e9 04          	sub    r9,0x4
 3be:	e9 0d ff ff ff       	jmp    2d0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x2d0>
 3c3:	4c 89 d8             	mov    rax,r11
 3c6:	eb e5                	jmp    3ad <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ad>
 3c8:	41 83 e5 01          	and    r13d,0x1
 3cc:	75 1e                	jne    3ec <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ec>
 3ce:	49 83 fa 08          	cmp    r10,0x8
 3d2:	75 18                	jne    3ec <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ec>
 3d4:	48 89 f1             	mov    rcx,rsi
 3d7:	31 c0                	xor    eax,eax
 3d9:	4c 8d 5c 00 01       	lea    r11,[rax+rax*1+0x1]
 3de:	42 8b 14 9e          	mov    edx,DWORD PTR [rsi+r11*4]
 3e2:	89 11                	mov    DWORD PTR [rcx],edx
 3e4:	48 89 c2             	mov    rdx,rax
 3e7:	4c 89 d8             	mov    rax,r11
 3ea:	eb b1                	jmp    39d <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x39d>
 3ec:	48 89 f0             	mov    rax,rsi
 3ef:	eb bc                	jmp    3ad <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ad>
 3f1:	4c 89 c0             	mov    rax,r8
 3f4:	48 8d 14 00          	lea    rdx,[rax+rax*1]
 3f8:	48 8d 42 01          	lea    rax,[rdx+0x1]
 3fc:	4c 8d 24 86          	lea    r12,[rsi+rax*4]
 400:	45 8b 2c 24          	mov    r13d,DWORD PTR [r12]
 404:	44 89 29             	mov    DWORD PTR [rcx],r13d
 407:	4c 89 e1             	mov    rcx,r12
 40a:	e9 b9 fd ff ff       	jmp    1c8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x1c8>
 40f:	44 89 01             	mov    DWORD PTR [rcx],r8d
 412:	eb a6                	jmp    3ba <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]+0x3ba>
 414:	90                   	nop
 415:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 41c:	00 00 00 00 

0000000000000420 <sort_std(std::vector<int, std::allocator<int> >&)>:
 420:	41 54                	push   r12
 422:	55                   	push   rbp
 423:	57                   	push   rdi
 424:	56                   	push   rsi
 425:	53                   	push   rbx
 426:	48 83 ec 20          	sub    rsp,0x20
 42a:	48 8b 79 08          	mov    rdi,QWORD PTR [rcx+0x8]
 42e:	48 8b 29             	mov    rbp,QWORD PTR [rcx]
 431:	48 39 fd             	cmp    rbp,rdi
 434:	0f 84 23 01 00 00    	je     55d <sort_std(std::vector<int, std::allocator<int> >&)+0x13d>
 43a:	48 89 fe             	mov    rsi,rdi
 43d:	48 8d 5d 04          	lea    rbx,[rbp+0x4]
 441:	48 29 ee             	sub    rsi,rbp
 444:	48 89 f0             	mov    rax,rsi
 447:	48 c1 f8 02          	sar    rax,0x2
 44b:	0f 84 84 01 00 00    	je     5d5 <sort_std(std::vector<int, std::allocator<int> >&)+0x1b5>
 451:	48 0f bd c0          	bsr    rax,rax
 455:	48 89 fa             	mov    rdx,rdi
 458:	48 89 e9             	mov    rcx,rbp
 45b:	4c 63 c0             	movsxd r8,eax
 45e:	4d 01 c0             	add    r8,r8
 461:	e8 9a fb ff ff       	call   0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
 466:	48 83 fe 40          	cmp    rsi,0x40
 46a:	0f 8e 2e 01 00 00    	jle    59e <sort_std(std::vector<int, std::allocator<int> >&)+0x17e>
 470:	48 8d 75 40          	lea    rsi,[rbp+0x40]
 474:	eb 3e                	jmp    4b4 <sort_std(std::vector<int, std::allocator<int> >&)+0x94>
 476:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 47d:	00 00 00 
 480:	49 89 d8             	mov    r8,rbx
 483:	49 29 e8             	sub    r8,rbp
 486:	4c 89 c0             	mov    rax,r8
 489:	48 c1 e0 3e          	shl    rax,0x3e
 48d:	4c 29 c0             	sub    rax,r8
 490:	48 8d 4c 03 04       	lea    rcx,[rbx+rax*1+0x4]
 495:	49 83 f8 04          	cmp    r8,0x4
 499:	0f 8e 69 01 00 00    	jle    608 <sort_std(std::vector<int, std::allocator<int> >&)+0x1e8>
 49f:	48 89 ea             	mov    rdx,rbp
 4a2:	e8 00 00 00 00       	call   4a7 <sort_std(std::vector<int, std::allocator<int> >&)+0x87>
 4a7:	48 83 c3 04          	add    rbx,0x4
 4ab:	44 89 65 00          	mov    DWORD PTR [rbp+0x0],r12d
 4af:	48 39 de             	cmp    rsi,rbx
 4b2:	74 4a                	je     4fe <sort_std(std::vector<int, std::allocator<int> >&)+0xde>
 4b4:	44 8b 23             	mov    r12d,DWORD PTR [rbx]
 4b7:	8b 55 00             	mov    edx,DWORD PTR [rbp+0x0]
 4ba:	41 39 d4             	cmp    r12d,edx
 4bd:	7c c1                	jl     480 <sort_std(std::vector<int, std::allocator<int> >&)+0x60>
 4bf:	8b 53 fc             	mov    edx,DWORD PTR [rbx-0x4]
 4c2:	41 39 d4             	cmp    r12d,edx
 4c5:	0f 8d 57 01 00 00    	jge    622 <sort_std(std::vector<int, std::allocator<int> >&)+0x202>
 4cb:	48 8d 43 fc          	lea    rax,[rbx-0x4]
 4cf:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 4d5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 4dc:	00 00 00 00 
 4e0:	89 50 04             	mov    DWORD PTR [rax+0x4],edx
 4e3:	48 89 c1             	mov    rcx,rax
 4e6:	8b 50 fc             	mov    edx,DWORD PTR [rax-0x4]
 4e9:	48 83 e8 04          	sub    rax,0x4
 4ed:	41 39 d4             	cmp    r12d,edx
 4f0:	7c ee                	jl     4e0 <sort_std(std::vector<int, std::allocator<int> >&)+0xc0>
 4f2:	44 89 21             	mov    DWORD PTR [rcx],r12d
 4f5:	48 83 c3 04          	add    rbx,0x4
 4f9:	48 39 de             	cmp    rsi,rbx
 4fc:	75 b6                	jne    4b4 <sort_std(std::vector<int, std::allocator<int> >&)+0x94>
 4fe:	48 39 f7             	cmp    rdi,rsi
 501:	74 5a                	je     55d <sort_std(std::vector<int, std::allocator<int> >&)+0x13d>
 503:	66 90                	xchg   ax,ax
 505:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 50c:	00 00 00 00 
 510:	8b 0e                	mov    ecx,DWORD PTR [rsi]
 512:	8b 56 fc             	mov    edx,DWORD PTR [rsi-0x4]
 515:	39 d1                	cmp    ecx,edx
 517:	0f 8d d3 00 00 00    	jge    5f0 <sort_std(std::vector<int, std::allocator<int> >&)+0x1d0>
 51d:	48 8d 46 fc          	lea    rax,[rsi-0x4]
 521:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 528:	00 00 
 52a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 531:	00 00 00 00 
 535:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 53c:	00 00 00 00 
 540:	89 50 04             	mov    DWORD PTR [rax+0x4],edx
 543:	49 89 c0             	mov    r8,rax
 546:	8b 50 fc             	mov    edx,DWORD PTR [rax-0x4]
 549:	48 83 e8 04          	sub    rax,0x4
 54d:	39 d1                	cmp    ecx,edx
 54f:	7c ef                	jl     540 <sort_std(std::vector<int, std::allocator<int> >&)+0x120>
 551:	48 83 c6 04          	add    rsi,0x4
 555:	41 89 08             	mov    DWORD PTR [r8],ecx
 558:	48 39 f7             	cmp    rdi,rsi
 55b:	75 b3                	jne    510 <sort_std(std::vector<int, std::allocator<int> >&)+0xf0>
 55d:	48 83 c4 20          	add    rsp,0x20
 561:	5b                   	pop    rbx
 562:	5e                   	pop    rsi
 563:	5f                   	pop    rdi
 564:	5d                   	pop    rbp
 565:	41 5c                	pop    r12
 567:	c3                   	ret
 568:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
 56f:	00 
 570:	49 89 d8             	mov    r8,rbx
 573:	49 29 e8             	sub    r8,rbp
 576:	4c 89 c0             	mov    rax,r8
 579:	48 c1 e0 3e          	shl    rax,0x3e
 57d:	4c 29 c0             	sub    rax,r8
 580:	48 8d 4c 03 04       	lea    rcx,[rbx+rax*1+0x4]
 585:	49 83 f8 04          	cmp    r8,0x4
 589:	0f 8e 86 00 00 00    	jle    615 <sort_std(std::vector<int, std::allocator<int> >&)+0x1f5>
 58f:	48 89 ea             	mov    rdx,rbp
 592:	e8 00 00 00 00       	call   597 <sort_std(std::vector<int, std::allocator<int> >&)+0x177>
 597:	89 75 00             	mov    DWORD PTR [rbp+0x0],esi
 59a:	48 83 c3 04          	add    rbx,0x4
 59e:	48 39 df             	cmp    rdi,rbx
 5a1:	74 ba                	je     55d <sort_std(std::vector<int, std::allocator<int> >&)+0x13d>
 5a3:	8b 33                	mov    esi,DWORD PTR [rbx]
 5a5:	8b 55 00             	mov    edx,DWORD PTR [rbp+0x0]
 5a8:	39 d6                	cmp    esi,edx
 5aa:	7c c4                	jl     570 <sort_std(std::vector<int, std::allocator<int> >&)+0x150>
 5ac:	8b 53 fc             	mov    edx,DWORD PTR [rbx-0x4]
 5af:	39 d6                	cmp    esi,edx
 5b1:	7d 7a                	jge    62d <sort_std(std::vector<int, std::allocator<int> >&)+0x20d>
 5b3:	48 8d 43 fc          	lea    rax,[rbx-0x4]
 5b7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 5be:	00 00 
 5c0:	89 50 04             	mov    DWORD PTR [rax+0x4],edx
 5c3:	48 89 c1             	mov    rcx,rax
 5c6:	8b 50 fc             	mov    edx,DWORD PTR [rax-0x4]
 5c9:	48 83 e8 04          	sub    rax,0x4
 5cd:	39 d6                	cmp    esi,edx
 5cf:	7c ef                	jl     5c0 <sort_std(std::vector<int, std::allocator<int> >&)+0x1a0>
 5d1:	89 31                	mov    DWORD PTR [rcx],esi
 5d3:	eb c5                	jmp    59a <sort_std(std::vector<int, std::allocator<int> >&)+0x17a>
 5d5:	49 c7 c0 fe ff ff ff 	mov    r8,0xfffffffffffffffe
 5dc:	48 89 fa             	mov    rdx,rdi
 5df:	48 89 e9             	mov    rcx,rbp
 5e2:	e8 19 fa ff ff       	call   0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter>(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_less_iter) [clone .isra.0]>
 5e7:	eb b5                	jmp    59e <sort_std(std::vector<int, std::allocator<int> >&)+0x17e>
 5e9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 5f0:	49 89 f0             	mov    r8,rsi
 5f3:	48 83 c6 04          	add    rsi,0x4
 5f7:	41 89 08             	mov    DWORD PTR [r8],ecx
 5fa:	48 39 f7             	cmp    rdi,rsi
 5fd:	0f 85 0d ff ff ff    	jne    510 <sort_std(std::vector<int, std::allocator<int> >&)+0xf0>
 603:	e9 55 ff ff ff       	jmp    55d <sort_std(std::vector<int, std::allocator<int> >&)+0x13d>
 608:	0f 85 99 fe ff ff    	jne    4a7 <sort_std(std::vector<int, std::allocator<int> >&)+0x87>
 60e:	89 11                	mov    DWORD PTR [rcx],edx
 610:	e9 92 fe ff ff       	jmp    4a7 <sort_std(std::vector<int, std::allocator<int> >&)+0x87>
 615:	0f 85 7c ff ff ff    	jne    597 <sort_std(std::vector<int, std::allocator<int> >&)+0x177>
 61b:	89 11                	mov    DWORD PTR [rcx],edx
 61d:	e9 75 ff ff ff       	jmp    597 <sort_std(std::vector<int, std::allocator<int> >&)+0x177>
 622:	48 89 d9             	mov    rcx,rbx
 625:	44 89 21             	mov    DWORD PTR [rcx],r12d
 628:	e9 c8 fe ff ff       	jmp    4f5 <sort_std(std::vector<int, std::allocator<int> >&)+0xd5>
 62d:	48 89 d9             	mov    rcx,rbx
 630:	89 31                	mov    DWORD PTR [rcx],esi
 632:	e9 63 ff ff ff       	jmp    59a <sort_std(std::vector<int, std::allocator<int> >&)+0x17a>
 637:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 63e:	00 00 

0000000000000640 <count_even(std::vector<int, std::allocator<int> > const&)>:
 640:	4c 8b 41 08          	mov    r8,QWORD PTR [rcx+0x8]
 644:	48 8b 09             	mov    rcx,QWORD PTR [rcx]
 647:	49 39 c8             	cmp    r8,rcx
 64a:	75 0d                	jne    659 <count_even(std::vector<int, std::allocator<int> > const&)+0x19>
 64c:	eb 4e                	jmp    69c <count_even(std::vector<int, std::allocator<int> > const&)+0x5c>
 64e:	66 90                	xchg   ax,ax
 650:	48 83 c1 04          	add    rcx,0x4
 654:	49 39 c8             	cmp    r8,rcx
 657:	74 43                	je     69c <count_even(std::vector<int, std::allocator<int> > const&)+0x5c>
 659:	8b 11                	mov    edx,DWORD PTR [rcx]
 65b:	f6 c2 01             	test   dl,0x1
 65e:	75 f0                	jne    650 <count_even(std::vector<int, std::allocator<int> > const&)+0x10>
 660:	45 31 c9             	xor    r9d,r9d
 663:	49 39 c8             	cmp    r8,rcx
 666:	74 30                	je     698 <count_even(std::vector<int, std::allocator<int> > const&)+0x58>
 668:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
 66f:	00 
 670:	48 8d 41 04          	lea    rax,[rcx+0x4]
 674:	41 01 d1             	add    r9d,edx
 677:	49 39 c0             	cmp    r8,rax
 67a:	75 0d                	jne    689 <count_even(std::vector<int, std::allocator<int> > const&)+0x49>
 67c:	eb 1a                	jmp    698 <count_even(std::vector<int, std::allocator<int> > const&)+0x58>
 67e:	66 90                	xchg   ax,ax
 680:	48 83 c0 04          	add    rax,0x4
 684:	49 39 c0             	cmp    r8,rax
 687:	74 0f                	je     698 <count_even(std::vector<int, std::allocator<int> > const&)+0x58>
 689:	8b 10                	mov    edx,DWORD PTR [rax]
 68b:	48 89 c1             	mov    rcx,rax
 68e:	f6 c2 01             	test   dl,0x1
 691:	75 ed                	jne    680 <count_even(std::vector<int, std::allocator<int> > const&)+0x40>
 693:	4c 39 c0             	cmp    rax,r8
 696:	75 d8                	jne    670 <count_even(std::vector<int, std::allocator<int> > const&)+0x30>
 698:	44 89 c8             	mov    eax,r9d
 69b:	c3                   	ret
 69c:	45 31 c9             	xor    r9d,r9d
 69f:	44 89 c8             	mov    eax,r9d
 6a2:	c3                   	ret
 6a3:	66 90                	xchg   ax,ax
 6a5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 6ac:	00 00 00 00 

00000000000006b0 <sort_ranges(std::vector<int, std::allocator<int> >&)>:
 6b0:	41 54                	push   r12
 6b2:	55                   	push   rbp
 6b3:	57                   	push   rdi
 6b4:	56                   	push   rsi
 6b5:	53                   	push   rbx
 6b6:	48 83 ec 40          	sub    rsp,0x40
 6ba:	48 8b 71 08          	mov    rsi,QWORD PTR [rcx+0x8]
 6be:	48 8b 29             	mov    rbp,QWORD PTR [rcx]
 6c1:	48 8d 54 24 3e       	lea    rdx,[rsp+0x3e]
 6c6:	48 8d 44 24 3f       	lea    rax,[rsp+0x3f]
 6cb:	48 92                	xchg   rdx,rax
 6cd:	48 39 ee             	cmp    rsi,rbp
 6d0:	0f 84 27 01 00 00    	je     7fd <sort_ranges(std::vector<int, std::allocator<int> >&)+0x14d>
 6d6:	48 89 f7             	mov    rdi,rsi
 6d9:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
 6de:	48 29 ef             	sub    rdi,rbp
 6e1:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
 6e6:	48 89 f9             	mov    rcx,rdi
 6e9:	48 c1 f9 02          	sar    rcx,0x2
 6ed:	0f 84 82 01 00 00    	je     875 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x1c5>
 6f3:	48 0f bd c9          	bsr    rcx,rcx
 6f7:	4c 8d 4c 24 20       	lea    r9,[rsp+0x20]
 6fc:	48 8d 5d 04          	lea    rbx,[rbp+0x4]
 700:	48 89 f2             	mov    rdx,rsi
 703:	48 63 c9             	movsxd rcx,ecx
 706:	4c 8d 04 09          	lea    r8,[rcx+rcx*1]
 70a:	48 89 e9             	mov    rcx,rbp
 70d:	e8 00 00 00 00       	call   712 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x62>
 712:	48 83 ff 40          	cmp    rdi,0x40
 716:	0f 8e 22 01 00 00    	jle    83e <sort_ranges(std::vector<int, std::allocator<int> >&)+0x18e>
 71c:	48 8d 7d 40          	lea    rdi,[rbp+0x40]
 720:	eb 3a                	jmp    75c <sort_ranges(std::vector<int, std::allocator<int> >&)+0xac>
 722:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 728:	49 89 d8             	mov    r8,rbx
 72b:	49 29 e8             	sub    r8,rbp
 72e:	4c 89 c0             	mov    rax,r8
 731:	48 c1 e0 3e          	shl    rax,0x3e
 735:	4c 29 c0             	sub    rax,r8
 738:	48 8d 4c 03 04       	lea    rcx,[rbx+rax*1+0x4]
 73d:	49 83 f8 04          	cmp    r8,0x4
 741:	0f 8e 69 01 00 00    	jle    8b0 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x200>
 747:	48 89 ea             	mov    rdx,rbp
 74a:	e8 00 00 00 00       	call   74f <sort_ranges(std::vector<int, std::allocator<int> >&)+0x9f>
 74f:	48 83 c3 04          	add    rbx,0x4
 753:	44 89 65 00          	mov    DWORD PTR [rbp+0x0],r12d
 757:	48 39 df             	cmp    rdi,rbx
 75a:	74 42                	je     79e <sort_ranges(std::vector<int, std::allocator<int> >&)+0xee>
 75c:	44 8b 23             	mov    r12d,DWORD PTR [rbx]
 75f:	8b 55 00             	mov    edx,DWORD PTR [rbp+0x0]
 762:	41 39 d4             	cmp    r12d,edx
 765:	7c c1                	jl     728 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x78>
 767:	8b 53 fc             	mov    edx,DWORD PTR [rbx-0x4]
 76a:	41 39 d4             	cmp    r12d,edx
 76d:	0f 8d 57 01 00 00    	jge    8ca <sort_ranges(std::vector<int, std::allocator<int> >&)+0x21a>
 773:	48 8d 43 fc          	lea    rax,[rbx-0x4]
 777:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 77e:	00 00 
 780:	89 50 04             	mov    DWORD PTR [rax+0x4],edx
 783:	48 89 c1             	mov    rcx,rax
 786:	8b 50 fc             	mov    edx,DWORD PTR [rax-0x4]
 789:	48 83 e8 04          	sub    rax,0x4
 78d:	41 39 d4             	cmp    r12d,edx
 790:	7c ee                	jl     780 <sort_ranges(std::vector<int, std::allocator<int> >&)+0xd0>
 792:	44 89 21             	mov    DWORD PTR [rcx],r12d
 795:	48 83 c3 04          	add    rbx,0x4
 799:	48 39 df             	cmp    rdi,rbx
 79c:	75 be                	jne    75c <sort_ranges(std::vector<int, std::allocator<int> >&)+0xac>
 79e:	48 39 fe             	cmp    rsi,rdi
 7a1:	74 5a                	je     7fd <sort_ranges(std::vector<int, std::allocator<int> >&)+0x14d>
 7a3:	66 90                	xchg   ax,ax
 7a5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 7ac:	00 00 00 00 
 7b0:	8b 0f                	mov    ecx,DWORD PTR [rdi]
 7b2:	8b 57 fc             	mov    edx,DWORD PTR [rdi-0x4]
 7b5:	39 d1                	cmp    ecx,edx
 7b7:	0f 8d db 00 00 00    	jge    898 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x1e8>
 7bd:	48 8d 47 fc          	lea    rax,[rdi-0x4]
 7c1:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 7c8:	00 00 
 7ca:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 7d1:	00 00 00 00 
 7d5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 7dc:	00 00 00 00 
 7e0:	89 50 04             	mov    DWORD PTR [rax+0x4],edx
 7e3:	49 89 c0             	mov    r8,rax
 7e6:	8b 50 fc             	mov    edx,DWORD PTR [rax-0x4]
 7e9:	48 83 e8 04          	sub    rax,0x4
 7ed:	39 d1                	cmp    ecx,edx
 7ef:	7c ef                	jl     7e0 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x130>
 7f1:	48 83 c7 04          	add    rdi,0x4
 7f5:	41 89 08             	mov    DWORD PTR [r8],ecx
 7f8:	48 39 fe             	cmp    rsi,rdi
 7fb:	75 b3                	jne    7b0 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x100>
 7fd:	48 83 c4 40          	add    rsp,0x40
 801:	5b                   	pop    rbx
 802:	5e                   	pop    rsi
 803:	5f                   	pop    rdi
 804:	5d                   	pop    rbp
 805:	41 5c                	pop    r12
 807:	c3                   	ret
 808:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
 80f:	00 
 810:	49 89 d8             	mov    r8,rbx
 813:	49 29 e8             	sub    r8,rbp
 816:	4c 89 c0             	mov    rax,r8
 819:	48 c1 e0 3e          	shl    rax,0x3e
 81d:	4c 29 c0             	sub    rax,r8
 820:	48 8d 4c 03 04       	lea    rcx,[rbx+rax*1+0x4]
 825:	49 83 f8 04          	cmp    r8,0x4
 829:	0f 8e 8e 00 00 00    	jle    8bd <sort_ranges(std::vector<int, std::allocator<int> >&)+0x20d>
 82f:	48 89 ea             	mov    rdx,rbp
 832:	e8 00 00 00 00       	call   837 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x187>
 837:	89 7d 00             	mov    DWORD PTR [rbp+0x0],edi
 83a:	48 83 c3 04          	add    rbx,0x4
 83e:	48 39 de             	cmp    rsi,rbx
 841:	74 ba                	je     7fd <sort_ranges(std::vector<int, std::allocator<int> >&)+0x14d>
 843:	8b 3b                	mov    edi,DWORD PTR [rbx]
 845:	8b 55 00             	mov    edx,DWORD PTR [rbp+0x0]
 848:	39 d7                	cmp    edi,edx
 84a:	7c c4                	jl     810 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x160>
 84c:	8b 53 fc             	mov    edx,DWORD PTR [rbx-0x4]
 84f:	39 d7                	cmp    edi,edx
 851:	0f 8d 7e 00 00 00    	jge    8d5 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x225>
 857:	48 8d 43 fc          	lea    rax,[rbx-0x4]
 85b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
 860:	89 50 04             	mov    DWORD PTR [rax+0x4],edx
 863:	48 89 c1             	mov    rcx,rax
 866:	8b 50 fc             	mov    edx,DWORD PTR [rax-0x4]
 869:	48 83 e8 04          	sub    rax,0x4
 86d:	39 d7                	cmp    edi,edx
 86f:	7c ef                	jl     860 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x1b0>
 871:	89 39                	mov    DWORD PTR [rcx],edi
 873:	eb c5                	jmp    83a <sort_ranges(std::vector<int, std::allocator<int> >&)+0x18a>
 875:	4c 8d 4c 24 20       	lea    r9,[rsp+0x20]
 87a:	48 89 f2             	mov    rdx,rsi
 87d:	48 8d 5d 04          	lea    rbx,[rbp+0x4]
 881:	48 89 e9             	mov    rcx,rbp
 884:	49 c7 c0 fe ff ff ff 	mov    r8,0xfffffffffffffffe
 88b:	e8 00 00 00 00       	call   890 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x1e0>
 890:	eb ac                	jmp    83e <sort_ranges(std::vector<int, std::allocator<int> >&)+0x18e>
 892:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 898:	49 89 f8             	mov    r8,rdi
 89b:	48 83 c7 04          	add    rdi,0x4
 89f:	41 89 08             	mov    DWORD PTR [r8],ecx
 8a2:	48 39 fe             	cmp    rsi,rdi
 8a5:	0f 85 05 ff ff ff    	jne    7b0 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x100>
 8ab:	e9 4d ff ff ff       	jmp    7fd <sort_ranges(std::vector<int, std::allocator<int> >&)+0x14d>
 8b0:	0f 85 99 fe ff ff    	jne    74f <sort_ranges(std::vector<int, std::allocator<int> >&)+0x9f>
 8b6:	89 11                	mov    DWORD PTR [rcx],edx
 8b8:	e9 92 fe ff ff       	jmp    74f <sort_ranges(std::vector<int, std::allocator<int> >&)+0x9f>
 8bd:	0f 85 74 ff ff ff    	jne    837 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x187>
 8c3:	89 11                	mov    DWORD PTR [rcx],edx
 8c5:	e9 6d ff ff ff       	jmp    837 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x187>
 8ca:	48 89 d9             	mov    rcx,rbx
 8cd:	44 89 21             	mov    DWORD PTR [rcx],r12d
 8d0:	e9 c0 fe ff ff       	jmp    795 <sort_ranges(std::vector<int, std::allocator<int> >&)+0xe5>
 8d5:	48 89 d9             	mov    rcx,rbx
 8d8:	89 39                	mov    DWORD PTR [rcx],edi
 8da:	e9 5b ff ff ff       	jmp    83a <sort_ranges(std::vector<int, std::allocator<int> >&)+0x18a>
 8df:	90                   	nop
 8e0:	90                   	nop
 8e1:	90                   	nop
 8e2:	90                   	nop
 8e3:	90                   	nop
 8e4:	90                   	nop
 8e5:	90                   	nop
 8e6:	90                   	nop
 8e7:	90                   	nop
 8e8:	90                   	nop
 8e9:	90                   	nop
 8ea:	90                   	nop
 8eb:	90                   	nop
 8ec:	90                   	nop
 8ed:	90                   	nop
 8ee:	90                   	nop
 8ef:	90                   	nop
 8f0:	90                   	nop
 8f1:	90                   	nop
 8f2:	90                   	nop
 8f3:	90                   	nop
 8f4:	90                   	nop
 8f5:	90                   	nop
 8f6:	90                   	nop
 8f7:	90                   	nop
 8f8:	90                   	nop
 8f9:	90                   	nop
 8fa:	90                   	nop
 8fb:	90                   	nop
 8fc:	90                   	nop
 8fd:	90                   	nop
 8fe:	90                   	nop
 8ff:	90                   	nop

Disassembly of section .text$_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZNSt6ranges8__detail16__make_comp_projINS9_4lessESt8identityEEDaRT_RT0_EUlOSE_OSG_E_EEEvSE_SE_SG_T1_:

0000000000000000 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)>:
   0:	41 57                	push   r15
   2:	41 56                	push   r14
   4:	41 55                	push   r13
   6:	41 54                	push   r12
   8:	55                   	push   rbp
   9:	57                   	push   rdi
   a:	56                   	push   rsi
   b:	53                   	push   rbx
   c:	48 83 ec 38          	sub    rsp,0x38
  10:	4d 8b 21             	mov    r12,QWORD PTR [r9]
  13:	4d 8b 69 08          	mov    r13,QWORD PTR [r9+0x8]
  17:	48 89 d0             	mov    rax,rdx
  1a:	48 89 ce             	mov    rsi,rcx
  1d:	4c 89 c7             	mov    rdi,r8
  20:	49 89 d3             	mov    r11,rdx
  23:	48 29 c8             	sub    rax,rcx
  26:	48 83 f8 40          	cmp    rax,0x40
  2a:	0f 8e a7 02 00 00    	jle    2d7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2d7>
  30:	48 89 c5             	mov    rbp,rax
  33:	48 c1 f8 03          	sar    rax,0x3
  37:	48 c1 fd 02          	sar    rbp,0x2
  3b:	48 85 ff             	test   rdi,rdi
  3e:	0f 84 20 01 00 00    	je     164 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x164>
  44:	f3 0f 7e 06          	movq   xmm0,QWORD PTR [rsi]
  48:	4c 8d 14 86          	lea    r10,[rsi+rax*4]
  4c:	45 8b 4b fc          	mov    r9d,DWORD PTR [r11-0x4]
  50:	48 83 ef 01          	sub    rdi,0x1
  54:	45 8b 02             	mov    r8d,DWORD PTR [r10]
  57:	48 8d 46 04          	lea    rax,[rsi+0x4]
  5b:	66 0f 70 c8 e5       	pshufd xmm1,xmm0,0xe5
  60:	66 0f 7e ca          	movd   edx,xmm1
  64:	66 0f 7e c1          	movd   ecx,xmm0
  68:	44 39 c2             	cmp    edx,r8d
  6b:	0f 8d 37 02 00 00    	jge    2a8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2a8>
  71:	45 39 c8             	cmp    r8d,r9d
  74:	0f 8c 4d 02 00 00    	jl     2c7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2c7>
  7a:	44 39 ca             	cmp    edx,r9d
  7d:	0f 8c 33 02 00 00    	jl     2b6 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2b6>
  83:	66 0f 70 c0 e1       	pshufd xmm0,xmm0,0xe1
  88:	66 0f d6 06          	movq   QWORD PTR [rsi],xmm0
  8c:	4d 89 da             	mov    r10,r11
  8f:	39 d1                	cmp    ecx,edx
  91:	7d 65                	jge    f8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0xf8>
  93:	66 90                	xchg   ax,ax
  95:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  9c:	00 00 00 00 
  a0:	48 83 c0 04          	add    rax,0x4
  a4:	90                   	nop
  a5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  ac:	00 00 00 00 
  b0:	49 89 c1             	mov    r9,rax
  b3:	8b 08                	mov    ecx,DWORD PTR [rax]
  b5:	48 83 c0 04          	add    rax,0x4
  b9:	39 d1                	cmp    ecx,edx
  bb:	7c f3                	jl     b0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0xb0>
  bd:	4c 89 cd             	mov    rbp,r9
  c0:	45 8b 4a fc          	mov    r9d,DWORD PTR [r10-0x4]
  c4:	44 39 ca             	cmp    edx,r9d
  c7:	7d 47                	jge    110 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x110>
  c9:	49 8d 42 f8          	lea    rax,[r10-0x8]
  cd:	0f 1f 00             	nop    DWORD PTR [rax]
  d0:	49 89 c2             	mov    r10,rax
  d3:	44 8b 08             	mov    r9d,DWORD PTR [rax]
  d6:	48 83 e8 04          	sub    rax,0x4
  da:	41 39 d1             	cmp    r9d,edx
  dd:	7f f1                	jg     d0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0xd0>
  df:	4c 39 d5             	cmp    rbp,r10
  e2:	73 3c                	jae    120 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x120>
  e4:	44 89 4d 00          	mov    DWORD PTR [rbp+0x0],r9d
  e8:	48 8d 45 04          	lea    rax,[rbp+0x4]
  ec:	41 89 0a             	mov    DWORD PTR [r10],ecx
  ef:	8b 16                	mov    edx,DWORD PTR [rsi]
  f1:	8b 4d 04             	mov    ecx,DWORD PTR [rbp+0x4]
  f4:	39 d1                	cmp    ecx,edx
  f6:	7c a8                	jl     a0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0xa0>
  f8:	45 8b 4a fc          	mov    r9d,DWORD PTR [r10-0x4]
  fc:	48 89 c5             	mov    rbp,rax
  ff:	44 39 ca             	cmp    edx,r9d
 102:	7c c5                	jl     c9 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0xc9>
 104:	90                   	nop
 105:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 10c:	00 00 00 00 
 110:	49 83 ea 04          	sub    r10,0x4
 114:	4c 39 d5             	cmp    rbp,r10
 117:	72 cb                	jb     e4 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0xe4>
 119:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 120:	4c 8d 4c 24 20       	lea    r9,[rsp+0x20]
 125:	49 89 f8             	mov    r8,rdi
 128:	4c 89 da             	mov    rdx,r11
 12b:	48 89 e9             	mov    rcx,rbp
 12e:	4c 89 64 24 20       	mov    QWORD PTR [rsp+0x20],r12
 133:	4c 89 6c 24 28       	mov    QWORD PTR [rsp+0x28],r13
 138:	e8 c3 fe ff ff       	call   0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)>
 13d:	48 89 e8             	mov    rax,rbp
 140:	48 29 f0             	sub    rax,rsi
 143:	48 83 f8 40          	cmp    rax,0x40
 147:	0f 8e 8a 01 00 00    	jle    2d7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2d7>
 14d:	49 89 eb             	mov    r11,rbp
 150:	48 89 c5             	mov    rbp,rax
 153:	48 c1 f8 03          	sar    rax,0x3
 157:	48 c1 fd 02          	sar    rbp,0x2
 15b:	48 85 ff             	test   rdi,rdi
 15e:	0f 85 e0 fe ff ff    	jne    44 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x44>
 164:	4c 8d 55 ff          	lea    r10,[rbp-0x1]
 168:	48 8d 5c 86 fc       	lea    rbx,[rsi+rax*4-0x4]
 16d:	4c 8d 40 ff          	lea    r8,[rax-0x1]
 171:	49 d1 fa             	sar    r10,1
 174:	44 8b 0b             	mov    r9d,DWORD PTR [rbx]
 177:	48 89 d9             	mov    rcx,rbx
 17a:	4c 89 c7             	mov    rdi,r8
 17d:	4d 39 d0             	cmp    r8,r10
 180:	0f 8d 0b 01 00 00    	jge    291 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x291>
 186:	4d 89 c4             	mov    r12,r8
 189:	eb 38                	jmp    1c3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x1c3>
 18b:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 192:	00 00 
 194:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 19b:	00 00 00 00 
 19f:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 1a6:	00 00 00 00 
 1aa:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 1b1:	00 00 00 00 
 1b5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 1bc:	00 00 00 00 
 1c0:	49 89 c4             	mov    r12,rax
 1c3:	49 8d 54 24 01       	lea    rdx,[r12+0x1]
 1c8:	4c 8d 2c 12          	lea    r13,[rdx+rdx*1]
 1cc:	4c 8d 34 d6          	lea    r14,[rsi+rdx*8]
 1d0:	49 8d 45 ff          	lea    rax,[r13-0x1]
 1d4:	45 8b 3e             	mov    r15d,DWORD PTR [r14]
 1d7:	48 8d 0c 86          	lea    rcx,[rsi+rax*4]
 1db:	8b 11                	mov    edx,DWORD PTR [rcx]
 1dd:	44 39 fa             	cmp    edx,r15d
 1e0:	41 0f 4e d7          	cmovle edx,r15d
 1e4:	49 0f 4e c5          	cmovle rax,r13
 1e8:	49 0f 4e ce          	cmovle rcx,r14
 1ec:	42 89 14 a6          	mov    DWORD PTR [rsi+r12*4],edx
 1f0:	4c 39 d0             	cmp    rax,r10
 1f3:	7c cb                	jl     1c0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x1c0>
 1f5:	40 f6 c5 01          	test   bpl,0x1
 1f9:	75 09                	jne    204 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x204>
 1fb:	48 39 c7             	cmp    rdi,rax
 1fe:	0f 84 30 02 00 00    	je     434 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x434>
 204:	48 8d 50 ff          	lea    rdx,[rax-0x1]
 208:	48 d1 fa             	sar    rdx,1
 20b:	49 39 c0             	cmp    r8,rax
 20e:	7c 51                	jl     261 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x261>
 210:	e9 8b 00 00 00       	jmp    2a0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2a0>
 215:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 21c:	00 00 00 
 21f:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 226:	00 00 00 00 
 22a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 231:	00 00 00 00 
 235:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 23c:	00 00 00 00 
 240:	89 08                	mov    DWORD PTR [rax],ecx
 242:	48 8d 42 ff          	lea    rax,[rdx-0x1]
 246:	48 c1 e8 3f          	shr    rax,0x3f
 24a:	48 8d 4c 10 ff       	lea    rcx,[rax+rdx*1-0x1]
 24f:	48 89 d0             	mov    rax,rdx
 252:	49 39 d0             	cmp    r8,rdx
 255:	0f 8d 8d 00 00 00    	jge    2e8 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2e8>
 25b:	48 89 ca             	mov    rdx,rcx
 25e:	48 d1 fa             	sar    rdx,1
 261:	4c 8d 24 96          	lea    r12,[rsi+rdx*4]
 265:	48 8d 04 86          	lea    rax,[rsi+rax*4]
 269:	41 8b 0c 24          	mov    ecx,DWORD PTR [r12]
 26d:	41 39 c9             	cmp    r9d,ecx
 270:	7f ce                	jg     240 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x240>
 272:	44 89 08             	mov    DWORD PTR [rax],r9d
 275:	4d 85 c0             	test   r8,r8
 278:	74 79                	je     2f3 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2f3>
 27a:	48 83 eb 04          	sub    rbx,0x4
 27e:	49 83 e8 01          	sub    r8,0x1
 282:	44 8b 0b             	mov    r9d,DWORD PTR [rbx]
 285:	48 89 d9             	mov    rcx,rbx
 288:	4d 39 d0             	cmp    r8,r10
 28b:	0f 8c f5 fe ff ff    	jl     186 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x186>
 291:	40 f6 c5 01          	test   bpl,0x1
 295:	75 09                	jne    2a0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2a0>
 297:	49 39 f8             	cmp    r8,rdi
 29a:	0f 84 91 01 00 00    	je     431 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x431>
 2a0:	44 89 09             	mov    DWORD PTR [rcx],r9d
 2a3:	eb d5                	jmp    27a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x27a>
 2a5:	0f 1f 00             	nop    DWORD PTR [rax]
 2a8:	44 39 ca             	cmp    edx,r9d
 2ab:	0f 8c d2 fd ff ff    	jl     83 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x83>
 2b1:	45 39 c8             	cmp    r8d,r9d
 2b4:	7d 11                	jge    2c7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2c7>
 2b6:	44 89 0e             	mov    DWORD PTR [rsi],r9d
 2b9:	41 89 4b fc          	mov    DWORD PTR [r11-0x4],ecx
 2bd:	8b 4e 04             	mov    ecx,DWORD PTR [rsi+0x4]
 2c0:	8b 16                	mov    edx,DWORD PTR [rsi]
 2c2:	e9 c5 fd ff ff       	jmp    8c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x8c>
 2c7:	44 89 06             	mov    DWORD PTR [rsi],r8d
 2ca:	41 89 0a             	mov    DWORD PTR [r10],ecx
 2cd:	8b 4e 04             	mov    ecx,DWORD PTR [rsi+0x4]
 2d0:	8b 16                	mov    edx,DWORD PTR [rsi]
 2d2:	e9 b5 fd ff ff       	jmp    8c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x8c>
 2d7:	48 83 c4 38          	add    rsp,0x38
 2db:	5b                   	pop    rbx
 2dc:	5e                   	pop    rsi
 2dd:	5f                   	pop    rdi
 2de:	5d                   	pop    rbp
 2df:	41 5c                	pop    r12
 2e1:	41 5d                	pop    r13
 2e3:	41 5e                	pop    r14
 2e5:	41 5f                	pop    r15
 2e7:	c3                   	ret
 2e8:	4c 89 e0             	mov    rax,r12
 2eb:	44 89 08             	mov    DWORD PTR [rax],r9d
 2ee:	4d 85 c0             	test   r8,r8
 2f1:	75 87                	jne    27a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x27a>
 2f3:	4c 89 d8             	mov    rax,r11
 2f6:	49 83 eb 04          	sub    r11,0x4
 2fa:	48 29 f0             	sub    rax,rsi
 2fd:	48 83 f8 04          	cmp    rax,0x4
 301:	7e d4                	jle    2d7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2d7>
 303:	66 90                	xchg   ax,ax
 305:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 30c:	00 00 00 00 
 310:	4d 89 d9             	mov    r9,r11
 313:	8b 06                	mov    eax,DWORD PTR [rsi]
 315:	45 8b 03             	mov    r8d,DWORD PTR [r11]
 318:	49 29 f1             	sub    r9,rsi
 31b:	4d 89 cd             	mov    r13,r9
 31e:	41 89 03             	mov    DWORD PTR [r11],eax
 321:	49 c1 fd 02          	sar    r13,0x2
 325:	49 83 f9 08          	cmp    r9,0x8
 329:	0f 8e d9 00 00 00    	jle    408 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x408>
 32f:	4d 8d 65 ff          	lea    r12,[r13-0x1]
 333:	31 ed                	xor    ebp,ebp
 335:	49 d1 fc             	sar    r12,1
 338:	eb 09                	jmp    343 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x343>
 33a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 340:	48 89 c5             	mov    rbp,rax
 343:	48 8d 55 01          	lea    rdx,[rbp+0x1]
 347:	4c 8d 14 12          	lea    r10,[rdx+rdx*1]
 34b:	48 8d 1c d6          	lea    rbx,[rsi+rdx*8]
 34f:	49 8d 42 ff          	lea    rax,[r10-0x1]
 353:	8b 3b                	mov    edi,DWORD PTR [rbx]
 355:	48 8d 0c 86          	lea    rcx,[rsi+rax*4]
 359:	8b 11                	mov    edx,DWORD PTR [rcx]
 35b:	39 fa                	cmp    edx,edi
 35d:	0f 4e d7             	cmovle edx,edi
 360:	49 0f 4e c2          	cmovle rax,r10
 364:	48 0f 4e cb          	cmovle rcx,rbx
 368:	89 14 ae             	mov    DWORD PTR [rsi+rbp*4],edx
 36b:	49 39 c4             	cmp    r12,rax
 36e:	7f d0                	jg     340 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x340>
 370:	41 83 e5 01          	and    r13d,0x1
 374:	75 14                	jne    38a <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x38a>
 376:	4c 89 ca             	mov    rdx,r9
 379:	48 c1 fa 03          	sar    rdx,0x3
 37d:	48 83 ea 01          	sub    rdx,0x1
 381:	48 39 c2             	cmp    rdx,rax
 384:	0f 84 8f 00 00 00    	je     419 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x419>
 38a:	48 8d 50 ff          	lea    rdx,[rax-0x1]
 38e:	48 c1 ea 3f          	shr    rdx,0x3f
 392:	48 8d 54 10 ff       	lea    rdx,[rax+rdx*1-0x1]
 397:	48 d1 fa             	sar    rdx,1
 39a:	48 85 c0             	test   rax,rax
 39d:	75 3e                	jne    3dd <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x3dd>
 39f:	e9 ab 00 00 00       	jmp    44f <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x44f>
 3a4:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 3aa:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 3b1:	00 00 00 00 
 3b5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 3bc:	00 00 00 00 
 3c0:	89 08                	mov    DWORD PTR [rax],ecx
 3c2:	48 8d 42 ff          	lea    rax,[rdx-0x1]
 3c6:	48 c1 e8 3f          	shr    rax,0x3f
 3ca:	48 8d 4c 10 ff       	lea    rcx,[rax+rdx*1-0x1]
 3cf:	48 89 d0             	mov    rax,rdx
 3d2:	48 85 d2             	test   rdx,rdx
 3d5:	74 2c                	je     403 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x403>
 3d7:	48 d1 f9             	sar    rcx,1
 3da:	48 89 ca             	mov    rdx,rcx
 3dd:	4c 8d 14 96          	lea    r10,[rsi+rdx*4]
 3e1:	48 8d 04 86          	lea    rax,[rsi+rax*4]
 3e5:	41 8b 0a             	mov    ecx,DWORD PTR [r10]
 3e8:	41 39 c8             	cmp    r8d,ecx
 3eb:	7f d3                	jg     3c0 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x3c0>
 3ed:	44 89 00             	mov    DWORD PTR [rax],r8d
 3f0:	49 83 f9 04          	cmp    r9,0x4
 3f4:	0f 8e dd fe ff ff    	jle    2d7 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x2d7>
 3fa:	49 83 eb 04          	sub    r11,0x4
 3fe:	e9 0d ff ff ff       	jmp    310 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x310>
 403:	4c 89 d0             	mov    rax,r10
 406:	eb e5                	jmp    3ed <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x3ed>
 408:	41 83 e5 01          	and    r13d,0x1
 40c:	75 1e                	jne    42c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x42c>
 40e:	49 83 f9 08          	cmp    r9,0x8
 412:	75 18                	jne    42c <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x42c>
 414:	48 89 f1             	mov    rcx,rsi
 417:	31 c0                	xor    eax,eax
 419:	4c 8d 54 00 01       	lea    r10,[rax+rax*1+0x1]
 41e:	42 8b 14 96          	mov    edx,DWORD PTR [rsi+r10*4]
 422:	89 11                	mov    DWORD PTR [rcx],edx
 424:	48 89 c2             	mov    rdx,rax
 427:	4c 89 d0             	mov    rax,r10
 42a:	eb b1                	jmp    3dd <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x3dd>
 42c:	48 89 f0             	mov    rax,rsi
 42f:	eb bc                	jmp    3ed <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x3ed>
 431:	4c 89 c0             	mov    rax,r8
 434:	48 8d 14 00          	lea    rdx,[rax+rax*1]
 438:	48 8d 42 01          	lea    rax,[rdx+0x1]
 43c:	4c 8d 24 86          	lea    r12,[rsi+rax*4]
 440:	45 8b 2c 24          	mov    r13d,DWORD PTR [r12]
 444:	44 89 29             	mov    DWORD PTR [rcx],r13d
 447:	4c 89 e1             	mov    rcx,r12
 44a:	e9 b9 fd ff ff       	jmp    208 <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x208>
 44f:	44 89 01             	mov    DWORD PTR [rcx],r8d
 452:	eb a6                	jmp    3fa <void std::__introsort_loop<__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}> >(__gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, __gnu_cxx::__normal_iterator<int*, std::vector<int, std::allocator<int> > >, long long, __gnu_cxx::__ops::_Iter_comp_iter<std::ranges::__detail::__make_comp_proj<std::ranges::less, std::identity>(std::ranges::less&, std::identity&)::{lambda(auto:1&&, auto:2&&)#1}>)+0x3fa>
 454:	90                   	nop
 455:	90                   	nop
 456:	90                   	nop
 457:	90                   	nop
 458:	90                   	nop
 459:	90                   	nop
 45a:	90                   	nop
 45b:	90                   	nop
 45c:	90                   	nop
 45d:	90                   	nop
 45e:	90                   	nop
 45f:	90                   	nop
 460:	90                   	nop
 461:	90                   	nop
 462:	90                   	nop
 463:	90                   	nop
 464:	90                   	nop
 465:	90                   	nop
 466:	90                   	nop
 467:	90                   	nop
 468:	90                   	nop
 469:	90                   	nop
 46a:	90                   	nop
 46b:	90                   	nop
 46c:	90                   	nop
 46d:	90                   	nop
 46e:	90                   	nop
 46f:	90                   	nop
 470:	90                   	nop
 471:	90                   	nop
 472:	90                   	nop
 473:	90                   	nop
 474:	90                   	nop
 475:	90                   	nop
 476:	90                   	nop
 477:	90                   	nop
 478:	90                   	nop
 479:	90                   	nop
 47a:	90                   	nop
 47b:	90                   	nop
 47c:	90                   	nop
 47d:	90                   	nop
 47e:	90                   	nop
 47f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <main.cold>:
   0:	48 89 d9             	mov    rcx,rbx
   3:	ba 00 01 00 00       	mov    edx,0x100
   8:	e8 00 00 00 00       	call   d <main.cold+0xd>
   d:	48 89 f1             	mov    rcx,rsi
  10:	e8 00 00 00 00       	call   15 <main.cold+0x15>
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
   0:	57                   	push   rdi
   1:	56                   	push   rsi
   2:	53                   	push   rbx
   3:	48 83 ec 40          	sub    rsp,0x40
   7:	e8 00 00 00 00       	call   c <main+0xc>
   c:	b9 00 01 00 00       	mov    ecx,0x100
  11:	e8 00 00 00 00       	call   16 <main+0x16>
  16:	66 0f 6f 05 10 00 00 	movdqa xmm0,XMMWORD PTR [rip+0x10]        # 2e <main+0x2e>
  1d:	00 
  1e:	4c 8d 40 0c          	lea    r8,[rax+0xc]
  22:	48 8d 90 00 01 00 00 	lea    rdx,[rax+0x100]
  29:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
  2e:	48 89 c3             	mov    rbx,rax
  31:	49 83 e0 f8          	and    r8,0xfffffffffffffff8
  35:	48 89 54 24 30       	mov    QWORD PTR [rsp+0x30],rdx
  3a:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
  40:	4c 89 c7             	mov    rdi,r8
  43:	48 c7 40 04 00 00 00 	mov    QWORD PTR [rax+0x4],0x0
  4a:	00 
  4b:	48 c7 80 f8 00 00 00 	mov    QWORD PTR [rax+0xf8],0x0
  52:	00 00 00 00 
  56:	44 29 c0             	sub    eax,r8d
  59:	8d 88 00 01 00 00    	lea    ecx,[rax+0x100]
  5f:	31 c0                	xor    eax,eax
  61:	c1 e9 03             	shr    ecx,0x3
  64:	f3 48 ab             	rep stos QWORD PTR [rdi],rax
  67:	bf 40 00 00 00       	mov    edi,0x40
  6c:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
  71:	48 89 d8             	mov    rax,rbx
  74:	66 0f 6e df          	movd   xmm3,edi
  78:	bf 04 00 00 00       	mov    edi,0x4
  7d:	66 0f 6e d7          	movd   xmm2,edi
  81:	66 0f 70 db 00       	pshufd xmm3,xmm3,0x0
  86:	66 0f 70 d2 00       	pshufd xmm2,xmm2,0x0
  8b:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  92:	00 00 00 
  95:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  9c:	00 00 00 00 
  a0:	66 0f 6f cb          	movdqa xmm1,xmm3
  a4:	48 83 c0 10          	add    rax,0x10
  a8:	66 0f fa c8          	psubd  xmm1,xmm0
  ac:	66 0f fe c2          	paddd  xmm0,xmm2
  b0:	0f 11 48 f0          	movups XMMWORD PTR [rax-0x10],xmm1
  b4:	48 39 c2             	cmp    rdx,rax
  b7:	75 e7                	jne    a0 <main+0xa0>
  b9:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  be:	e8 20 04 00 00       	call   4e3 <sort_std(std::vector<int, std::allocator<int> >&)+0xc3>
  c3:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  c8:	e8 b0 06 00 00       	call   77d <sort_ranges(std::vector<int, std::allocator<int> >&)+0xcd>
  cd:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  d2:	e8 40 06 00 00       	call   717 <sort_ranges(std::vector<int, std::allocator<int> >&)+0x67>
  d7:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # de <main+0xde>
  de:	89 c2                	mov    edx,eax
  e0:	e8 00 00 00 00       	call   e5 <main+0xe5>
  e5:	ba 00 01 00 00       	mov    edx,0x100
  ea:	48 89 d9             	mov    rcx,rbx
  ed:	e8 00 00 00 00       	call   f2 <main+0xf2>
  f2:	31 c0                	xor    eax,eax
  f4:	48 83 c4 40          	add    rsp,0x40
  f8:	5b                   	pop    rbx
  f9:	5e                   	pop    rsi
  fa:	5f                   	pop    rdi
  fb:	c3                   	ret
  fc:	48 89 c6             	mov    rsi,rax
  ff:	e9 00 00 00 00       	jmp    104 <main+0x104>
 104:	90                   	nop
 105:	90                   	nop
 106:	90                   	nop
 107:	90                   	nop
 108:	90                   	nop
 109:	90                   	nop
 10a:	90                   	nop
 10b:	90                   	nop
 10c:	90                   	nop
 10d:	90                   	nop
 10e:	90                   	nop
 10f:	90                   	nop
 110:	90                   	nop
 111:	90                   	nop
 112:	90                   	nop
 113:	90                   	nop
 114:	90                   	nop
 115:	90                   	nop
 116:	90                   	nop
 117:	90                   	nop
 118:	90                   	nop
 119:	90                   	nop
 11a:	90                   	nop
 11b:	90                   	nop
 11c:	90                   	nop
 11d:	90                   	nop
 11e:	90                   	nop
 11f:	90                   	nop
