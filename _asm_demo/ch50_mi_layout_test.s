
ch50_mi_layout_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <D::f2()>:
   0:	8b 41 1c             	mov    eax,DWORD PTR [rcx+0x1c]
   3:	83 c0 16             	add    eax,0x16
   6:	c3                   	ret
   7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   e:	00 00 

0000000000000010 <non-virtual thunk to D::f2()>:
  10:	8b 41 0c             	mov    eax,DWORD PTR [rcx+0xc]
  13:	83 c0 16             	add    eax,0x16
  16:	c3                   	ret
  17:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  1e:	00 00 

0000000000000020 <call_f2_via_b2(B2*)>:
  20:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  23:	48 ff 60 10          	rex.W jmp QWORD PTR [rax+0x10]
  27:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  2e:	00 00 

0000000000000030 <b2_offset()>:
  30:	b8 10 00 00 00       	mov    eax,0x10
  35:	c3                   	ret
  36:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  3d:	00 00 00 

0000000000000040 <sizeof_D()>:
  40:	b8 20 00 00 00       	mov    eax,0x20
  45:	c3                   	ret
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

Disassembly of section .text$_ZN1D2f1Ev:

0000000000000000 <D::f1()>:
   0:	b8 0b 00 00 00       	mov    eax,0xb
   5:	c3                   	ret
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

Disassembly of section .text$_ZN1DD1Ev:

0000000000000000 <D::~D()>:
   0:	c3                   	ret
   1:	90                   	nop
   2:	90                   	nop
   3:	90                   	nop
   4:	90                   	nop
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

Disassembly of section .text$_ZN1DD0Ev:

0000000000000000 <D::~D()>:
   0:	ba 20 00 00 00       	mov    edx,0x20
   5:	e9 00 00 00 00       	jmp    a <D::~D()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_ZThn16_N1DD1Ev:

0000000000000000 <non-virtual thunk to D::~D()>:
   0:	c3                   	ret
   1:	90                   	nop
   2:	90                   	nop
   3:	90                   	nop
   4:	90                   	nop
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

Disassembly of section .text$_ZThn16_N1DD0Ev:

0000000000000000 <non-virtual thunk to D::~D()>:
   0:	ba 20 00 00 00       	mov    edx,0x20
   5:	48 83 e9 10          	sub    rcx,0x10
   9:	e9 00 00 00 00       	jmp    e <non-virtual thunk to D::~D()+0xe>
   e:	90                   	nop
   f:	90                   	nop
