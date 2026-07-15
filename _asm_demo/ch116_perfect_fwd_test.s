
ch116_perfect_fwd_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <sink_l(S&)>:
   0:	c7 05 00 00 00 00 01 	mov    DWORD PTR [rip+0x0],0x1        # a <sink_l(S&)+0xa>
   7:	00 00 00 
   a:	c3                   	ret
   b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000000010 <sink_r(S&&)>:
  10:	c7 05 fc ff ff ff 01 	mov    DWORD PTR [rip+0xfffffffffffffffc],0x1        # 16 <sink_r(S&&)+0x6>
  17:	00 00 00 
  1a:	c3                   	ret
  1b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000000020 <fwd_lvalue(S&)>:
  20:	eb de                	jmp    0 <sink_l(S&)>
  22:	0f 1f 00             	nop    DWORD PTR [rax]
  25:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  2c:	00 00 00 00 

0000000000000030 <fwd_rvalue(S&&)>:
  30:	eb de                	jmp    10 <sink_r(S&&)>
  32:	0f 1f 00             	nop    DWORD PTR [rax]
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 

0000000000000040 <fwd_val(S)>:
  40:	48 83 ec 38          	sub    rsp,0x38
  44:	f3 0f 6f 01          	movdqu xmm0,XMMWORD PTR [rcx]
  48:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
  4d:	0f 29 44 24 20       	movaps XMMWORD PTR [rsp+0x20],xmm0
  52:	e8 b9 ff ff ff       	call   10 <sink_r(S&&)>
  57:	90                   	nop
  58:	48 83 c4 38          	add    rsp,0x38
  5c:	c3                   	ret
  5d:	90                   	nop
  5e:	90                   	nop
  5f:	90                   	nop

Disassembly of section .text$_Z8fwd_tmplIR1SEvOT_:

0000000000000000 <void fwd_tmpl<S&>(S&)>:
   0:	e9 00 00 00 00       	jmp    5 <void fwd_tmpl<S&>(S&)+0x5>
   5:	90                   	nop
   6:	90                   	nop
   7:	90                   	nop
   8:	90                   	nop
   9:	90                   	nop
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_Z8fwd_tmplI1SEvOT_:

0000000000000000 <void fwd_tmpl<S>(S&&)>:
   0:	e9 10 00 00 00       	jmp    15 <sink_r(S&&)+0x5>
   5:	90                   	nop
   6:	90                   	nop
   7:	90                   	nop
   8:	90                   	nop
   9:	90                   	nop
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop
