
ch24_enum_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <use_enum(Color)>:
   0:	31 d2                	xor    edx,edx
   2:	0f b6 c1             	movzx  eax,cl
   5:	83 c0 01             	add    eax,0x1
   8:	80 f9 03             	cmp    cl,0x3
   b:	0f 43 c2             	cmovae eax,edx
   e:	c3                   	ret
   f:	90                   	nop

0000000000000010 <use_plain(Plain)>:
  10:	8d 41 01             	lea    eax,[rcx+0x1]
  13:	c3                   	ret
  14:	90                   	nop
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 

0000000000000020 <enum_underlying(Color)>:
  20:	89 c8                	mov    eax,ecx
  22:	c3                   	ret
  23:	90                   	nop
  24:	90                   	nop
  25:	90                   	nop
  26:	90                   	nop
  27:	90                   	nop
  28:	90                   	nop
  29:	90                   	nop
  2a:	90                   	nop
  2b:	90                   	nop
  2c:	90                   	nop
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 38          	sub    rsp,0x38
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	c7 44 24 2c 00 00 00 	mov    DWORD PTR [rsp+0x2c],0x0
  10:	00 
  11:	c7 44 24 2c 02 00 00 	mov    DWORD PTR [rsp+0x2c],0x2
  18:	00 
  19:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  1d:	83 c0 01             	add    eax,0x1
  20:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  24:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  28:	83 c0 02             	add    eax,0x2
  2b:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  2f:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
  33:	48 83 c4 38          	add    rsp,0x38
  37:	c3                   	ret
  38:	90                   	nop
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop
