
ch107_atomic_rmw_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <fetch_add_relaxed()>:
   0:	b8 01 00 00 00       	mov    eax,0x1
   5:	f0 0f c1 05 08 00 00 	lock xadd DWORD PTR [rip+0x8],eax        # 15 <fetch_add_seqcst()+0x5>
   c:	00 
   d:	c3                   	ret
   e:	66 90                	xchg   ax,ax

0000000000000010 <fetch_add_seqcst()>:
  10:	b8 01 00 00 00       	mov    eax,0x1
  15:	f0 0f c1 05 08 00 00 	lock xadd DWORD PTR [rip+0x8],eax        # 25 <fetch_add64()+0x5>
  1c:	00 
  1d:	c3                   	ret
  1e:	66 90                	xchg   ax,ax

0000000000000020 <fetch_add64()>:
  20:	b8 01 00 00 00       	mov    eax,0x1
  25:	f0 48 0f c1 05 00 00 	lock xadd QWORD PTR [rip+0x0],rax        # 2e <fetch_add64()+0xe>
  2c:	00 00 
  2e:	c3                   	ret
  2f:	90                   	nop

0000000000000030 <exchange_seqcst()>:
  30:	b8 63 00 00 00       	mov    eax,0x63
  35:	87 05 08 00 00 00    	xchg   DWORD PTR [rip+0x8],eax        # 43 <cas_inc()+0x3>
  3b:	c3                   	ret
  3c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000000040 <cas_inc()>:
  40:	8b 05 08 00 00 00    	mov    eax,DWORD PTR [rip+0x8]        # 4e <cas_inc()+0xe>
  46:	8d 50 01             	lea    edx,[rax+0x1]
  49:	f0 0f b1 15 08 00 00 	lock cmpxchg DWORD PTR [rip+0x8],edx        # 59 <cas_inc()+0x19>
  50:	00 
  51:	75 f3                	jne    46 <cas_inc()+0x6>
  53:	c3                   	ret
  54:	90                   	nop
  55:	90                   	nop
  56:	90                   	nop
  57:	90                   	nop
  58:	90                   	nop
  59:	90                   	nop
  5a:	90                   	nop
  5b:	90                   	nop
  5c:	90                   	nop
  5d:	90                   	nop
  5e:	90                   	nop
  5f:	90                   	nop
