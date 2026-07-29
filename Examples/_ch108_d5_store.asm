
_ch108_d5_store.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <store_relaxed(long long)>:
   0:	48 85 c9             	test   rcx,rcx
   3:	7e 56                	jle    5b <store_relaxed(long long)+0x5b>
   5:	31 c0                	xor    eax,eax
   7:	f6 c1 01             	test   cl,0x1
   a:	74 34                	je     40 <store_relaxed(long long)+0x40>
   c:	48 c7 05 fc ff ff ff 	mov    QWORD PTR [rip+0xfffffffffffffffc],0x0        # 13 <store_relaxed(long long)+0x13>
  13:	00 00 00 00 
  17:	b8 01 00 00 00       	mov    eax,0x1
  1c:	48 83 f9 01          	cmp    rcx,0x1
  20:	74 39                	je     5b <store_relaxed(long long)+0x5b>
  22:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  29:	00 
  2a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  31:	00 00 00 00 
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 
  40:	48 89 05 00 00 00 00 	mov    QWORD PTR [rip+0x0],rax        # 47 <store_relaxed(long long)+0x47>
  47:	48 8d 50 01          	lea    rdx,[rax+0x1]
  4b:	48 83 c0 02          	add    rax,0x2
  4f:	48 89 15 00 00 00 00 	mov    QWORD PTR [rip+0x0],rdx        # 56 <store_relaxed(long long)+0x56>
  56:	48 39 c1             	cmp    rcx,rax
  59:	75 e5                	jne    40 <store_relaxed(long long)+0x40>
  5b:	c3                   	ret
  5c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000000060 <store_release(long long)>:
  60:	48 85 c9             	test   rcx,rcx
  63:	7e 1b                	jle    80 <store_release(long long)+0x20>
  65:	31 c0                	xor    eax,eax
  67:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  6e:	00 00 
  70:	48 89 05 00 00 00 00 	mov    QWORD PTR [rip+0x0],rax        # 77 <store_release(long long)+0x17>
  77:	48 83 c0 01          	add    rax,0x1
  7b:	48 39 c1             	cmp    rcx,rax
  7e:	75 f0                	jne    70 <store_release(long long)+0x10>
  80:	c3                   	ret
  81:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  85:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  8c:	00 00 00 00 

0000000000000090 <store_seqcst(long long)>:
  90:	48 85 c9             	test   rcx,rcx
  93:	7e 1e                	jle    b3 <store_seqcst(long long)+0x23>
  95:	31 c0                	xor    eax,eax
  97:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  9e:	00 00 
  a0:	48 89 c2             	mov    rdx,rax
  a3:	48 87 15 00 00 00 00 	xchg   QWORD PTR [rip+0x0],rdx        # aa <store_seqcst(long long)+0x1a>
  aa:	48 83 c0 01          	add    rax,0x1
  ae:	48 39 c1             	cmp    rcx,rax
  b1:	75 ed                	jne    a0 <store_seqcst(long long)+0x10>
  b3:	c3                   	ret
  b4:	90                   	nop
  b5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  bc:	00 00 00 00 

00000000000000c0 <fetch_add_relaxed(long long)>:
  c0:	48 85 c9             	test   rcx,rcx
  c3:	7e 3b                	jle    100 <fetch_add_relaxed(long long)+0x40>
  c5:	31 c0                	xor    eax,eax
  c7:	31 d2                	xor    edx,edx
  c9:	90                   	nop
  ca:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  d1:	00 00 00 00 
  d5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  dc:	00 00 00 00 
  e0:	41 b8 01 00 00 00    	mov    r8d,0x1
  e6:	f0 4c 0f c1 05 00 00 	lock xadd QWORD PTR [rip+0x0],r8        # ef <fetch_add_relaxed(long long)+0x2f>
  ed:	00 00 
  ef:	48 83 c0 01          	add    rax,0x1
  f3:	4c 01 c2             	add    rdx,r8
  f6:	48 39 c1             	cmp    rcx,rax
  f9:	75 e5                	jne    e0 <fetch_add_relaxed(long long)+0x20>
  fb:	48 89 d0             	mov    rax,rdx
  fe:	c3                   	ret
  ff:	90                   	nop
 100:	31 d2                	xor    edx,edx
 102:	48 89 d0             	mov    rax,rdx
 105:	c3                   	ret
 106:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 10d:	00 00 00 

0000000000000110 <fetch_add_seqcst(long long)>:
 110:	48 85 c9             	test   rcx,rcx
 113:	7e 2b                	jle    140 <fetch_add_seqcst(long long)+0x30>
 115:	31 c0                	xor    eax,eax
 117:	31 d2                	xor    edx,edx
 119:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 120:	41 b8 01 00 00 00    	mov    r8d,0x1
 126:	f0 4c 0f c1 05 00 00 	lock xadd QWORD PTR [rip+0x0],r8        # 12f <fetch_add_seqcst(long long)+0x1f>
 12d:	00 00 
 12f:	48 83 c0 01          	add    rax,0x1
 133:	4c 01 c2             	add    rdx,r8
 136:	48 39 c1             	cmp    rcx,rax
 139:	75 e5                	jne    120 <fetch_add_seqcst(long long)+0x10>
 13b:	48 89 d0             	mov    rax,rdx
 13e:	c3                   	ret
 13f:	90                   	nop
 140:	31 d2                	xor    edx,edx
 142:	48 89 d0             	mov    rax,rdx
 145:	c3                   	ret
 146:	90                   	nop
 147:	90                   	nop
 148:	90                   	nop
 149:	90                   	nop
 14a:	90                   	nop
 14b:	90                   	nop
 14c:	90                   	nop
 14d:	90                   	nop
 14e:	90                   	nop
 14f:	90                   	nop
 150:	90                   	nop
 151:	90                   	nop
 152:	90                   	nop
 153:	90                   	nop
 154:	90                   	nop
 155:	90                   	nop
 156:	90                   	nop
 157:	90                   	nop
 158:	90                   	nop
 159:	90                   	nop
 15a:	90                   	nop
 15b:	90                   	nop
 15c:	90                   	nop
 15d:	90                   	nop
 15e:	90                   	nop
 15f:	90                   	nop
