
ch41_make_shared_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <via_make_shared(int)>:
   0:	56                   	push   rsi
   1:	53                   	push   rbx
   2:	48 83 ec 28          	sub    rsp,0x28
   6:	48 89 ce             	mov    rsi,rcx
   9:	b9 20 00 00 00       	mov    ecx,0x20
   e:	89 d3                	mov    ebx,edx
  10:	e8 00 00 00 00       	call   15 <via_make_shared(int)+0x15>
  15:	48 8b 15 00 00 00 00 	mov    rdx,QWORD PTR [rip+0x0]        # 1c <via_make_shared(int)+0x1c>
  1c:	48 8d 0d 10 00 00 00 	lea    rcx,[rip+0x10]        # 33 <via_make_shared(int)+0x33>
  23:	89 58 10             	mov    DWORD PTR [rax+0x10],ebx
  26:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  2a:	8d 53 01             	lea    edx,[rbx+0x1]
  2d:	83 c3 02             	add    ebx,0x2
  30:	48 89 08             	mov    QWORD PTR [rax],rcx
  33:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
  36:	89 58 18             	mov    DWORD PTR [rax+0x18],ebx
  39:	48 89 46 08          	mov    QWORD PTR [rsi+0x8],rax
  3d:	48 83 c0 10          	add    rax,0x10
  41:	48 89 06             	mov    QWORD PTR [rsi],rax
  44:	48 89 f0             	mov    rax,rsi
  47:	48 83 c4 28          	add    rsp,0x28
  4b:	5b                   	pop    rbx
  4c:	5e                   	pop    rsi
  4d:	c3                   	ret
  4e:	66 90                	xchg   ax,ax

0000000000000050 <via_new(int)>:
  50:	57                   	push   rdi
  51:	56                   	push   rsi
  52:	53                   	push   rbx
  53:	48 83 ec 20          	sub    rsp,0x20
  57:	48 89 ce             	mov    rsi,rcx
  5a:	b9 0c 00 00 00       	mov    ecx,0xc
  5f:	89 d3                	mov    ebx,edx
  61:	e8 00 00 00 00       	call   66 <via_new(int)+0x16>
  66:	48 c7 46 08 00 00 00 	mov    QWORD PTR [rsi+0x8],0x0
  6d:	00 
  6e:	b9 18 00 00 00       	mov    ecx,0x18
  73:	89 18                	mov    DWORD PTR [rax],ebx
  75:	48 89 c7             	mov    rdi,rax
  78:	8d 43 01             	lea    eax,[rbx+0x1]
  7b:	83 c3 02             	add    ebx,0x2
  7e:	89 47 04             	mov    DWORD PTR [rdi+0x4],eax
  81:	89 5f 08             	mov    DWORD PTR [rdi+0x8],ebx
  84:	48 89 3e             	mov    QWORD PTR [rsi],rdi
  87:	e8 00 00 00 00       	call   8c <via_new(int)+0x3c>
  8c:	48 8b 15 00 00 00 00 	mov    rdx,QWORD PTR [rip+0x0]        # 93 <via_new(int)+0x43>
  93:	48 89 78 10          	mov    QWORD PTR [rax+0x10],rdi
  97:	48 89 46 08          	mov    QWORD PTR [rsi+0x8],rax
  9b:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  9f:	48 8d 15 10 00 00 00 	lea    rdx,[rip+0x10]        # b6 <via_new(int)+0x66>
  a6:	48 89 10             	mov    QWORD PTR [rax],rdx
  a9:	48 89 f0             	mov    rax,rsi
  ac:	48 83 c4 20          	add    rsp,0x20
  b0:	5b                   	pop    rbx
  b1:	5e                   	pop    rsi
  b2:	5f                   	pop    rdi
  b3:	c3                   	ret
  b4:	e9 00 00 00 00       	jmp    b9 <via_new(int)+0x69>
  b9:	90                   	nop
  ba:	90                   	nop
  bb:	90                   	nop
  bc:	90                   	nop
  bd:	90                   	nop
  be:	90                   	nop
  bf:	90                   	nop

Disassembly of section .text$_ZNSt15_Sp_counted_ptrIP6WidgetLN9__gnu_cxx12_Lock_policyE2EED1Ev:

0000000000000000 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr()>:
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

Disassembly of section .text$_ZNSt15_Sp_counted_ptrIP6WidgetLN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:

0000000000000000 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)>:
   0:	31 c0                	xor    eax,eax
   2:	c3                   	ret
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

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI6WidgetSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:

0000000000000000 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr_inplace()>:
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

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI6WidgetSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:

0000000000000000 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose()>:
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

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI6WidgetSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:

0000000000000000 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # b <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0xb>
   b:	49 89 c8             	mov    r8,rcx
   e:	48 89 d1             	mov    rcx,rdx
  11:	48 39 c2             	cmp    rdx,rax
  14:	74 27                	je     3d <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x3d>
  16:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # 1d <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x1d>
  1d:	48 39 42 08          	cmp    QWORD PTR [rdx+0x8],rax
  21:	74 1a                	je     3d <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x3d>
  23:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 2a <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x2a>
  2a:	4c 89 44 24 30       	mov    QWORD PTR [rsp+0x30],r8
  2f:	e8 00 00 00 00       	call   34 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x34>
  34:	4c 8b 44 24 30       	mov    r8,QWORD PTR [rsp+0x30]
  39:	84 c0                	test   al,al
  3b:	74 13                	je     50 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x50>
  3d:	49 8d 40 10          	lea    rax,[r8+0x10]
  41:	48 83 c4 28          	add    rsp,0x28
  45:	c3                   	ret
  46:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  4d:	00 00 00 
  50:	31 c0                	xor    eax,eax
  52:	48 83 c4 28          	add    rsp,0x28
  56:	c3                   	ret
  57:	90                   	nop
  58:	90                   	nop
  59:	90                   	nop
  5a:	90                   	nop
  5b:	90                   	nop
  5c:	90                   	nop
  5d:	90                   	nop
  5e:	90                   	nop
  5f:	90                   	nop

Disassembly of section .text$_ZNSt15_Sp_counted_ptrIP6WidgetLN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:

0000000000000000 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::_M_dispose()>:
   0:	48 8b 49 10          	mov    rcx,QWORD PTR [rcx+0x10]
   4:	48 85 c9             	test   rcx,rcx
   7:	74 0f                	je     18 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::_M_dispose()+0x18>
   9:	ba 0c 00 00 00       	mov    edx,0xc
   e:	e9 00 00 00 00       	jmp    13 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::_M_dispose()+0x13>
  13:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  18:	c3                   	ret
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI6WidgetSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:

0000000000000000 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr_inplace()>:
   0:	ba 20 00 00 00       	mov    edx,0x20
   5:	e9 00 00 00 00       	jmp    a <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr_inplace()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_ZNSt15_Sp_counted_ptrIP6WidgetLN9__gnu_cxx12_Lock_policyE2EED0Ev:

0000000000000000 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr()>:
   0:	ba 18 00 00 00       	mov    edx,0x18
   5:	e9 00 00 00 00       	jmp    a <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_ZNSt15_Sp_counted_ptrIP6WidgetLN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:

0000000000000000 <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::_M_destroy()>:
   0:	ba 18 00 00 00       	mov    edx,0x18
   5:	e9 00 00 00 00       	jmp    a <std::_Sp_counted_ptr<Widget*, (__gnu_cxx::_Lock_policy)2>::_M_destroy()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI6WidgetSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:

0000000000000000 <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_destroy()>:
   0:	ba 20 00 00 00       	mov    edx,0x20
   5:	e9 00 00 00 00       	jmp    a <std::_Sp_counted_ptr_inplace<Widget, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_destroy()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <via_new(int) [clone .cold]>:
   0:	48 89 c1             	mov    rcx,rax
   3:	e8 00 00 00 00       	call   8 <via_new(int) [clone .cold]+0x8>
   8:	ba 0c 00 00 00       	mov    edx,0xc
   d:	48 89 f9             	mov    rcx,rdi
  10:	e8 00 00 00 00       	call   15 <via_new(int) [clone .cold]+0x15>
  15:	e8 00 00 00 00       	call   1a <via_new(int) [clone .cold]+0x1a>
  1a:	48 89 c3             	mov    rbx,rax
  1d:	e8 00 00 00 00       	call   22 <via_new(int) [clone .cold]+0x22>
  22:	48 89 d9             	mov    rcx,rbx
  25:	e8 00 00 00 00       	call   2a <via_new(int) [clone .cold]+0x2a>
  2a:	90                   	nop
  2b:	90                   	nop
  2c:	90                   	nop
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop
