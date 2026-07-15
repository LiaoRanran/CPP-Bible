
ch108_memory_order_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <store_relaxed()>:
   0:	c7 05 fc ff ff ff 01 	mov    DWORD PTR [rip+0xfffffffffffffffc],0x1        # 6 <store_relaxed()+0x6>
   7:	00 00 00 
   a:	c3                   	ret
   b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000000010 <store_release()>:
  10:	c7 05 fc ff ff ff 01 	mov    DWORD PTR [rip+0xfffffffffffffffc],0x1        # 16 <store_release()+0x6>
  17:	00 00 00 
  1a:	c3                   	ret
  1b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000000020 <store_seqcst()>:
  20:	b8 01 00 00 00       	mov    eax,0x1
  25:	87 05 00 00 00 00    	xchg   DWORD PTR [rip+0x0],eax        # 2b <store_seqcst()+0xb>
  2b:	c3                   	ret
  2c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000000030 <load_acquire()>:
  30:	8b 05 00 00 00 00    	mov    eax,DWORD PTR [rip+0x0]        # 36 <load_acquire()+0x6>
  36:	c3                   	ret
  37:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  3e:	00 00 

0000000000000040 <load_seqcst()>:
  40:	8b 05 00 00 00 00    	mov    eax,DWORD PTR [rip+0x0]        # 46 <load_seqcst()+0x6>
  46:	c3                   	ret
  47:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  4e:	00 00 

0000000000000050 <fadd_relaxed()>:
  50:	b8 01 00 00 00       	mov    eax,0x1
  55:	f0 0f c1 05 00 00 00 	lock xadd DWORD PTR [rip+0x0],eax        # 5d <fadd_relaxed()+0xd>
  5c:	00 
  5d:	c3                   	ret
  5e:	66 90                	xchg   ax,ax

0000000000000060 <fadd_seqcst()>:
  60:	b8 01 00 00 00       	mov    eax,0x1
  65:	f0 0f c1 05 00 00 00 	lock xadd DWORD PTR [rip+0x0],eax        # 6d <fadd_seqcst()+0xd>
  6c:	00 
  6d:	c3                   	ret
  6e:	90                   	nop
  6f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	e8 00 00 00 00       	call   9 <main+0x9>
   9:	e8 00 00 00 00       	call   e <main+0xe>
   e:	e8 10 00 00 00       	call   23 <main+0x23>
  13:	e8 20 00 00 00       	call   38 <main+0x38>
  18:	e8 30 00 00 00       	call   4d <load_seqcst()+0xd>
  1d:	e8 40 00 00 00       	call   62 <fadd_seqcst()+0x2>
  22:	e8 50 00 00 00       	call   77 <fadd_seqcst()+0x17>
  27:	e8 60 00 00 00       	call   8c <fadd_seqcst()+0x2c>
  2c:	31 c0                	xor    eax,eax
  2e:	48 83 c4 28          	add    rsp,0x28
  32:	c3                   	ret
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
