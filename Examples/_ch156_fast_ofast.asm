
_ch156_fast_ofast.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <_Z3dotPKdS0_i>:
   0:	45 85 c0             	test   r8d,r8d
   3:	7e 73                	jle    78 <_Z3dotPKdS0_i+0x78>
   5:	41 83 f8 01          	cmp    r8d,0x1
   9:	74 76                	je     81 <_Z3dotPKdS0_i+0x81>
   b:	45 89 c1             	mov    r9d,r8d
   e:	31 c0                	xor    eax,eax
  10:	66 0f ef d2          	pxor   xmm2,xmm2
  14:	41 d1 e9             	shr    r9d,1
  17:	49 c1 e1 04          	shl    r9,0x4
  1b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  20:	f3 0f 7e 04 01       	movq   xmm0,QWORD PTR [rcx+rax*1]
  25:	f3 0f 7e 0c 02       	movq   xmm1,QWORD PTR [rdx+rax*1]
  2a:	66 0f 16 44 01 08    	movhpd xmm0,QWORD PTR [rcx+rax*1+0x8]
  30:	66 0f 16 4c 02 08    	movhpd xmm1,QWORD PTR [rdx+rax*1+0x8]
  36:	48 83 c0 10          	add    rax,0x10
  3a:	66 0f 59 c1          	mulpd  xmm0,xmm1
  3e:	4c 39 c8             	cmp    rax,r9
  41:	66 0f 58 d0          	addpd  xmm2,xmm0
  45:	75 d9                	jne    20 <_Z3dotPKdS0_i+0x20>
  47:	44 89 c0             	mov    eax,r8d
  4a:	66 0f 28 ca          	movapd xmm1,xmm2
  4e:	83 e0 fe             	and    eax,0xfffffffe
  51:	41 83 e0 01          	and    r8d,0x1
  55:	66 0f 15 ca          	unpckhpd xmm1,xmm2
  59:	66 0f 58 ca          	addpd  xmm1,xmm2
  5d:	74 10                	je     6f <_Z3dotPKdS0_i+0x6f>
  5f:	48 98                	cdqe
  61:	f2 0f 10 04 c2       	movsd  xmm0,QWORD PTR [rdx+rax*8]
  66:	f2 0f 59 04 c1       	mulsd  xmm0,QWORD PTR [rcx+rax*8]
  6b:	f2 0f 58 c8          	addsd  xmm1,xmm0
  6f:	66 0f 28 c1          	movapd xmm0,xmm1
  73:	c3                   	ret
  74:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  78:	66 0f ef c9          	pxor   xmm1,xmm1
  7c:	66 0f 28 c1          	movapd xmm0,xmm1
  80:	c3                   	ret
  81:	31 c0                	xor    eax,eax
  83:	66 0f ef c9          	pxor   xmm1,xmm1
  87:	eb d6                	jmp    5f <_Z3dotPKdS0_i+0x5f>
  89:	90                   	nop
  8a:	90                   	nop
  8b:	90                   	nop
  8c:	90                   	nop
  8d:	90                   	nop
  8e:	90                   	nop
  8f:	90                   	nop
