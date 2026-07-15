
ch109_fence_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <fence_seqcst()>:
   0:	f0 48 83 0c 24 00    	lock or QWORD PTR [rsp],0x0
   6:	c3                   	ret
   7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   e:	00 00 

0000000000000010 <fence_acquire()>:
  10:	c3                   	ret
  11:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 

0000000000000020 <fence_release()>:
  20:	c3                   	ret
  21:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  25:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  2c:	00 00 00 00 

0000000000000030 <fence_acq_rel()>:
  30:	c3                   	ret
  31:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 

0000000000000040 <fence_signal()>:
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
