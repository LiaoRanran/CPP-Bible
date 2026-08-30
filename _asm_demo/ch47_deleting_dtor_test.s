
ch47_deleting_dtor_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <Base::~Base()>:
   0:	48 83 05 ff ff ff ff 	add    QWORD PTR [rip+0xffffffffffffffff],0x1        # 7 <Base::~Base()+0x7>
   7:	01 
   8:	c3                   	ret
   9:	90                   	nop
   a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000000010 <Derived::~Derived()>:
  10:	48 83 05 ff ff ff ff 	add    QWORD PTR [rip+0xffffffffffffffff],0x3        # 17 <Derived::~Derived()+0x7>
  17:	03 
  18:	c3                   	ret
  19:	90                   	nop
  1a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000000020 <Base::~Base()>:
  20:	48 83 05 ff ff ff ff 	add    QWORD PTR [rip+0xffffffffffffffff],0x1        # 27 <Base::~Base()+0x7>
  27:	01 
  28:	ba 10 00 00 00       	mov    edx,0x10
  2d:	e9 00 00 00 00       	jmp    32 <Base::~Base()+0x12>
  32:	0f 1f 00             	nop    DWORD PTR [rax]
  35:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  3c:	00 00 00 00 

0000000000000040 <Derived::~Derived()>:
  40:	48 83 05 ff ff ff ff 	add    QWORD PTR [rip+0xffffffffffffffff],0x3        # 47 <Derived::~Derived()+0x7>
  47:	03 
  48:	ba 10 00 00 00       	mov    edx,0x10
  4d:	e9 00 00 00 00       	jmp    52 <Derived::~Derived()+0x12>
  52:	0f 1f 00             	nop    DWORD PTR [rax]
  55:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  5c:	00 00 00 00 

0000000000000060 <destroy_base(Base*)>:
  60:	48 85 c9             	test   rcx,rcx
  63:	74 0b                	je     70 <destroy_base(Base*)+0x10>
  65:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  68:	48 ff 60 08          	rex.W jmp QWORD PTR [rax+0x8]
  6c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  70:	c3                   	ret
  71:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  75:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  7c:	00 00 00 00 

0000000000000080 <destroy_derived(Derived*)>:
  80:	48 85 c9             	test   rcx,rcx
  83:	74 2b                	je     b0 <destroy_derived(Derived*)+0x30>
  85:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  88:	48 8d 15 b1 ff ff ff 	lea    rdx,[rip+0xffffffffffffffb1]        # 40 <Derived::~Derived()>
  8f:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
  93:	48 39 d0             	cmp    rax,rdx
  96:	75 20                	jne    b8 <destroy_derived(Derived*)+0x38>
  98:	48 83 05 ff ff ff ff 	add    QWORD PTR [rip+0xffffffffffffffff],0x3        # 9f <destroy_derived(Derived*)+0x1f>
  9f:	03 
  a0:	ba 10 00 00 00       	mov    edx,0x10
  a5:	e9 00 00 00 00       	jmp    aa <destroy_derived(Derived*)+0x2a>
  aa:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
  b0:	c3                   	ret
  b1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
  b8:	48 ff e0             	rex.W jmp rax
  bb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

00000000000000c0 <sizeof_base()>:
  c0:	b8 10 00 00 00       	mov    eax,0x10
  c5:	c3                   	ret
  c6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  cd:	00 00 00 

00000000000000d0 <sizeof_derived()>:
  d0:	b8 10 00 00 00       	mov    eax,0x10
  d5:	c3                   	ret
  d6:	90                   	nop
  d7:	90                   	nop
  d8:	90                   	nop
  d9:	90                   	nop
  da:	90                   	nop
  db:	90                   	nop
  dc:	90                   	nop
  dd:	90                   	nop
  de:	90                   	nop
  df:	90                   	nop
