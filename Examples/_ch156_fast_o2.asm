
_ch156_fast_o2.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <_Z3dotPKdS0_i>:
   0:	45 85 c0             	test   r8d,r8d
   3:	7e 33                	jle    38 <_Z3dotPKdS0_i+0x38>
   5:	4d 63 c0             	movsxd r8,r8d
   8:	31 c0                	xor    eax,eax
   a:	66 0f ef c9          	pxor   xmm1,xmm1
   e:	49 c1 e0 03          	shl    r8,0x3
  12:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
  18:	f2 0f 10 04 01       	movsd  xmm0,QWORD PTR [rcx+rax*1]
  1d:	f2 0f 59 04 02       	mulsd  xmm0,QWORD PTR [rdx+rax*1]
  22:	48 83 c0 08          	add    rax,0x8
  26:	49 39 c0             	cmp    r8,rax
  29:	f2 0f 58 c8          	addsd  xmm1,xmm0
  2d:	75 e9                	jne    18 <_Z3dotPKdS0_i+0x18>
  2f:	66 0f 28 c1          	movapd xmm0,xmm1
  33:	c3                   	ret
  34:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  38:	66 0f ef c9          	pxor   xmm1,xmm1
  3c:	66 0f 28 c1          	movapd xmm0,xmm1
  40:	c3                   	ret
  41:	90                   	nop
  42:	90                   	nop
  43:	90                   	nop
  44:	90                   	nop
  45:	90                   	nop
  46:	90                   	nop
  47:	90                   	nop
  48:	90                   	nop
  49:	90                   	nop
  4a:	90                   	nop
  4b:	90                   	nop
  4c:	90                   	nop
  4d:	90                   	nop
  4e:	90                   	nop
  4f:	90                   	nop
