
ch87_bit_test_popcnt.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <popcnt_u(unsigned int)>:
   0:	31 c0                	xor    eax,eax
   2:	f3 0f b8 c1          	popcnt eax,ecx
   6:	c3                   	ret
   7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   e:	00 00 

0000000000000010 <bswap_u(unsigned int)>:
  10:	89 c8                	mov    eax,ecx
  12:	0f c8                	bswap  eax
  14:	c3                   	ret
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 

0000000000000020 <to_float(unsigned int)>:
  20:	66 0f 6e c1          	movd   xmm0,ecx
  24:	c3                   	ret
  25:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  2c:	00 00 00 00 

0000000000000030 <is_pow2(unsigned int)>:
  30:	f3 0f b8 c9          	popcnt ecx,ecx
  34:	83 f9 01             	cmp    ecx,0x1
  37:	0f 94 c0             	sete   al
  3a:	c3                   	ret
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 38          	sub    rsp,0x38
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	c7 44 24 2c 00 00 00 	mov    DWORD PTR [rsp+0x2c],0x0
  10:	00 
  11:	c7 44 24 2c 0f 00 00 	mov    DWORD PTR [rsp+0x2c],0xf
  18:	00 
  19:	c7 44 24 2c 12 34 56 	mov    DWORD PTR [rsp+0x2c],0x78563412
  20:	78 
  21:	c7 44 24 2c 01 00 00 	mov    DWORD PTR [rsp+0x2c],0x1
  28:	00 
  29:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  2d:	83 c0 01             	add    eax,0x1
  30:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  34:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  38:	48 83 c4 38          	add    rsp,0x38
  3c:	c3                   	ret
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop
