
ch40_nt_noexcept.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <no_throw(int, int)>:
   0:	89 c8                	mov    eax,ecx
   2:	89 d1                	mov    ecx,edx
   4:	99                   	cdq
   5:	f7 f9                	idiv   ecx
   7:	c3                   	ret
   8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   f:	00 

0000000000000010 <use_nt(int, int)>:
  10:	89 c8                	mov    eax,ecx
  12:	89 d1                	mov    ecx,edx
  14:	99                   	cdq
  15:	f7 f9                	idiv   ecx
  17:	c3                   	ret
  18:	90                   	nop
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop
