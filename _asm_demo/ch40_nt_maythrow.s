
ch40_nt_maythrow.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <may_throw(int, int)>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	89 c8                	mov    eax,ecx
   6:	89 d1                	mov    ecx,edx
   8:	85 d2                	test   edx,edx
   a:	0f 84 27 00 00 00    	je     37 <use_mt(int, int)+0x17>
  10:	99                   	cdq
  11:	f7 f9                	idiv   ecx
  13:	48 83 c4 28          	add    rsp,0x28
  17:	c3                   	ret
  18:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
  1f:	00 

0000000000000020 <use_mt(int, int)>:
  20:	48 83 ec 28          	sub    rsp,0x28
  24:	89 c8                	mov    eax,ecx
  26:	89 d1                	mov    ecx,edx
  28:	85 d2                	test   edx,edx
  2a:	0f 84 2d 00 00 00    	je     5d <use_mt(int, int) [clone .cold]+0x30>
  30:	99                   	cdq
  31:	f7 f9                	idiv   ecx
  33:	48 83 c4 28          	add    rsp,0x28
  37:	c3                   	ret
  38:	90                   	nop
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <may_throw(int, int) [clone .part.0]>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	b9 04 00 00 00       	mov    ecx,0x4
   9:	e8 00 00 00 00       	call   e <may_throw(int, int) [clone .part.0]+0xe>
   e:	48 8b 15 00 00 00 00 	mov    rdx,QWORD PTR [rip+0x0]        # 15 <may_throw(int, int) [clone .part.0]+0x15>
  15:	45 31 c0             	xor    r8d,r8d
  18:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
  1e:	48 89 c1             	mov    rcx,rax
  21:	e8 00 00 00 00       	call   26 <may_throw(int, int) [clone .part.0]+0x26>
  26:	90                   	nop

0000000000000027 <may_throw(int, int) [clone .cold]>:
  27:	e8 d4 ff ff ff       	call   0 <may_throw(int, int) [clone .part.0]>
  2c:	90                   	nop

000000000000002d <use_mt(int, int) [clone .cold]>:
  2d:	e8 ce ff ff ff       	call   0 <may_throw(int, int) [clone .part.0]>
  32:	90                   	nop
  33:	90                   	nop
  34:	90                   	nop
  35:	90                   	nop
  36:	90                   	nop
  37:	90                   	nop
  38:	90                   	nop
  39:	90                   	nop
  3a:	90                   	nop
  3b:	90                   	nop
  3c:	90                   	nop
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop
