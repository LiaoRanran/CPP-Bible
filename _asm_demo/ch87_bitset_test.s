
ch87_bitset_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <bitset_count(std::bitset<64ull> const&)>:
   0:	56                   	push   rsi
   1:	53                   	push   rbx
   2:	48 83 ec 28          	sub    rsp,0x28
   6:	48 89 ce             	mov    rsi,rcx
   9:	8b 09                	mov    ecx,DWORD PTR [rcx]
   b:	e8 00 00 00 00       	call   10 <bitset_count(std::bitset<64ull> const&)+0x10>
  10:	8b 4e 04             	mov    ecx,DWORD PTR [rsi+0x4]
  13:	48 63 d8             	movsxd rbx,eax
  16:	e8 00 00 00 00       	call   1b <bitset_count(std::bitset<64ull> const&)+0x1b>
  1b:	48 98                	cdqe
  1d:	48 01 d8             	add    rax,rbx
  20:	48 83 c4 28          	add    rsp,0x28
  24:	5b                   	pop    rbx
  25:	5e                   	pop    rsi
  26:	c3                   	ret
  27:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  2e:	00 00 

0000000000000030 <bitset_test(std::bitset<64ull> const&, unsigned long long)>:
  30:	48 83 ec 28          	sub    rsp,0x28
  34:	49 89 c8             	mov    r8,rcx
  37:	48 83 fa 3f          	cmp    rdx,0x3f
  3b:	0f 87 00 00 00 00    	ja     41 <bitset_test(std::bitset<64ull> const&, unsigned long long)+0x11>
  41:	49 89 d1             	mov    r9,rdx
  44:	89 d1                	mov    ecx,edx
  46:	b8 01 00 00 00       	mov    eax,0x1
  4b:	49 c1 e9 05          	shr    r9,0x5
  4f:	d3 e0                	shl    eax,cl
  51:	43 23 04 88          	and    eax,DWORD PTR [r8+r9*4]
  55:	0f 95 c0             	setne  al
  58:	48 83 c4 28          	add    rsp,0x28
  5c:	c3                   	ret
  5d:	0f 1f 00             	nop    DWORD PTR [rax]

0000000000000060 <bitset_flip(std::bitset<64ull>)>:
  60:	48 89 c8             	mov    rax,rcx
  63:	48 f7 d0             	not    rax
  66:	c3                   	ret
  67:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  6e:	00 00 

0000000000000070 <bitset_set(std::bitset<64ull>, unsigned long long)>:
  70:	48 83 ec 28          	sub    rsp,0x28
  74:	48 89 4c 24 30       	mov    QWORD PTR [rsp+0x30],rcx
  79:	48 83 fa 3f          	cmp    rdx,0x3f
  7d:	0f 87 1d 00 00 00    	ja     a0 <bitset_set(std::bitset<64ull>, unsigned long long)+0x30>
  83:	49 89 d0             	mov    r8,rdx
  86:	89 d1                	mov    ecx,edx
  88:	b8 01 00 00 00       	mov    eax,0x1
  8d:	49 c1 e8 05          	shr    r8,0x5
  91:	d3 e0                	shl    eax,cl
  93:	42 09 44 84 30       	or     DWORD PTR [rsp+r8*4+0x30],eax
  98:	48 8b 44 24 30       	mov    rax,QWORD PTR [rsp+0x30]
  9d:	48 83 c4 28          	add    rsp,0x28
  a1:	c3                   	ret
  a2:	90                   	nop
  a3:	90                   	nop
  a4:	90                   	nop
  a5:	90                   	nop
  a6:	90                   	nop
  a7:	90                   	nop
  a8:	90                   	nop
  a9:	90                   	nop
  aa:	90                   	nop
  ab:	90                   	nop
  ac:	90                   	nop
  ad:	90                   	nop
  ae:	90                   	nop
  af:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <bitset_test(std::bitset<64ull> const&, unsigned long long) [clone .cold]>:
   0:	49 89 d0             	mov    r8,rdx
   3:	41 b9 40 00 00 00    	mov    r9d,0x40
   9:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 10 <bitset_test(std::bitset<64ull> const&, unsigned long long) [clone .cold]+0x10>
  10:	48 8d 0d 10 00 00 00 	lea    rcx,[rip+0x10]        # 27 <bitset_set(std::bitset<64ull>, unsigned long long) [clone .cold]+0xa>
  17:	e8 00 00 00 00       	call   1c <bitset_test(std::bitset<64ull> const&, unsigned long long) [clone .cold]+0x1c>
  1c:	90                   	nop

000000000000001d <bitset_set(std::bitset<64ull>, unsigned long long) [clone .cold]>:
  1d:	49 89 d0             	mov    r8,rdx
  20:	41 b9 40 00 00 00    	mov    r9d,0x40
  26:	48 8d 15 44 00 00 00 	lea    rdx,[rip+0x44]        # 71 <bitset_set(std::bitset<64ull>, unsigned long long)+0x1>
  2d:	48 8d 0d 10 00 00 00 	lea    rcx,[rip+0x10]        # 44 <bitset_test(std::bitset<64ull> const&, unsigned long long)+0x14>
  34:	e8 00 00 00 00       	call   39 <bitset_set(std::bitset<64ull>, unsigned long long) [clone .cold]+0x1c>
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	57                   	push   rdi
   1:	56                   	push   rsi
   2:	53                   	push   rbx
   3:	48 83 ec 30          	sub    rsp,0x30
   7:	e8 00 00 00 00       	call   c <main+0xc>
   c:	48 b9 f0 de bc 9a 78 	movabs rcx,0x123456789abcdef0
  13:	56 34 12 
  16:	48 c7 44 24 28 00 00 	mov    QWORD PTR [rsp+0x28],0x0
  1d:	00 00 
  1f:	48 c7 44 24 28 20 00 	mov    QWORD PTR [rsp+0x28],0x20
  26:	00 00 
  28:	48 c7 44 24 28 01 00 	mov    QWORD PTR [rsp+0x28],0x1
  2f:	00 00 
  31:	e8 60 00 00 00       	call   96 <bitset_set(std::bitset<64ull>, unsigned long long)+0x26>
  36:	48 89 c6             	mov    rsi,rax
  39:	89 c1                	mov    ecx,eax
  3b:	e8 00 00 00 00       	call   40 <main+0x40>
  40:	48 89 f1             	mov    rcx,rsi
  43:	48 c1 e9 20          	shr    rcx,0x20
  47:	48 63 d8             	movsxd rbx,eax
  4a:	e8 00 00 00 00       	call   4f <main+0x4f>
  4f:	89 f1                	mov    ecx,esi
  51:	81 c9 80 00 00 00    	or     ecx,0x80
  57:	48 63 f8             	movsxd rdi,eax
  5a:	e8 00 00 00 00       	call   5f <main+0x5f>
  5f:	48 8b 54 24 28       	mov    rdx,QWORD PTR [rsp+0x28]
  64:	48 98                	cdqe
  66:	48 01 c3             	add    rbx,rax
  69:	48 01 d3             	add    rbx,rdx
  6c:	48 8d 04 7b          	lea    rax,[rbx+rdi*2]
  70:	48 89 44 24 28       	mov    QWORD PTR [rsp+0x28],rax
  75:	48 8b 44 24 28       	mov    rax,QWORD PTR [rsp+0x28]
  7a:	48 83 c4 30          	add    rsp,0x30
  7e:	5b                   	pop    rbx
  7f:	5e                   	pop    rsi
  80:	5f                   	pop    rdi
  81:	c3                   	ret
  82:	90                   	nop
  83:	90                   	nop
  84:	90                   	nop
  85:	90                   	nop
  86:	90                   	nop
  87:	90                   	nop
  88:	90                   	nop
  89:	90                   	nop
  8a:	90                   	nop
  8b:	90                   	nop
  8c:	90                   	nop
  8d:	90                   	nop
  8e:	90                   	nop
  8f:	90                   	nop
