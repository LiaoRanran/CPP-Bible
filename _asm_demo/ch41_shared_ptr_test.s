
ch41_shared_ptr_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <clone(std::shared_ptr<S> const&)>:
   0:	f3 0f 6f 02          	movdqu xmm0,XMMWORD PTR [rdx]
   4:	0f 12 c8             	movhlps xmm1,xmm0
   7:	66 48 0f 7e ca       	movq   rdx,xmm1
   c:	48 89 c8             	mov    rax,rcx
   f:	0f 11 01             	movups XMMWORD PTR [rcx],xmm0
  12:	48 85 d2             	test   rdx,rdx
  15:	74 05                	je     1c <clone(std::shared_ptr<S> const&)+0x1c>
  17:	f0 83 42 08 01       	lock add DWORD PTR [rdx+0x8],0x1
  1c:	c3                   	ret
  1d:	0f 1f 00             	nop    DWORD PTR [rax]

0000000000000020 <make_one()>:
  20:	53                   	push   rbx
  21:	48 83 ec 20          	sub    rsp,0x20
  25:	48 89 cb             	mov    rbx,rcx
  28:	b9 18 00 00 00       	mov    ecx,0x18
  2d:	e8 00 00 00 00       	call   32 <make_one()+0x12>
  32:	48 8b 15 00 00 00 00 	mov    rdx,QWORD PTR [rip+0x0]        # 39 <make_one()+0x19>
  39:	c7 40 10 2a 00 00 00 	mov    DWORD PTR [rax+0x10],0x2a
  40:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  44:	48 8d 15 10 00 00 00 	lea    rdx,[rip+0x10]        # 5b <make_one()+0x3b>
  4b:	48 89 10             	mov    QWORD PTR [rax],rdx
  4e:	48 89 43 08          	mov    QWORD PTR [rbx+0x8],rax
  52:	48 83 c0 10          	add    rax,0x10
  56:	48 89 03             	mov    QWORD PTR [rbx],rax
  59:	48 89 d8             	mov    rax,rbx
  5c:	48 83 c4 20          	add    rsp,0x20
  60:	5b                   	pop    rbx
  61:	c3                   	ret
  62:	90                   	nop
  63:	90                   	nop
  64:	90                   	nop
  65:	90                   	nop
  66:	90                   	nop
  67:	90                   	nop
  68:	90                   	nop
  69:	90                   	nop
  6a:	90                   	nop
  6b:	90                   	nop
  6c:	90                   	nop
  6d:	90                   	nop
  6e:	90                   	nop
  6f:	90                   	nop

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI1SSaIvELN9__gnu_cxx12_Lock_policyE2EED1Ev:

0000000000000000 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr_inplace()>:
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

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI1SSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_disposeEv:

0000000000000000 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose()>:
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

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI1SSaIvELN9__gnu_cxx12_Lock_policyE2EE14_M_get_deleterERKSt9type_info:

0000000000000000 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)>:
   0:	48 83 ec 28          	sub    rsp,0x28
   4:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # b <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0xb>
   b:	49 89 c8             	mov    r8,rcx
   e:	48 89 d1             	mov    rcx,rdx
  11:	48 39 c2             	cmp    rdx,rax
  14:	74 27                	je     3d <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x3d>
  16:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # 1d <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x1d>
  1d:	48 39 42 08          	cmp    QWORD PTR [rdx+0x8],rax
  21:	74 1a                	je     3d <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x3d>
  23:	48 8d 15 00 00 00 00 	lea    rdx,[rip+0x0]        # 2a <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x2a>
  2a:	4c 89 44 24 30       	mov    QWORD PTR [rsp+0x30],r8
  2f:	e8 00 00 00 00       	call   34 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x34>
  34:	4c 8b 44 24 30       	mov    r8,QWORD PTR [rsp+0x30]
  39:	84 c0                	test   al,al
  3b:	74 13                	je     50 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_get_deleter(std::type_info const&)+0x50>
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

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI1SSaIvELN9__gnu_cxx12_Lock_policyE2EED0Ev:

0000000000000000 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr_inplace()>:
   0:	ba 18 00 00 00       	mov    edx,0x18
   5:	e9 00 00 00 00       	jmp    a <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::~_Sp_counted_ptr_inplace()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_ZNSt23_Sp_counted_ptr_inplaceI1SSaIvELN9__gnu_cxx12_Lock_policyE2EE10_M_destroyEv:

0000000000000000 <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_destroy()>:
   0:	ba 18 00 00 00       	mov    edx,0x18
   5:	e9 00 00 00 00       	jmp    a <std::_Sp_counted_ptr_inplace<S, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_destroy()+0xa>
   a:	90                   	nop
   b:	90                   	nop
   c:	90                   	nop
   d:	90                   	nop
   e:	90                   	nop
   f:	90                   	nop

Disassembly of section .text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE24_M_release_last_use_coldEv:

0000000000000000 <std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release_last_use_cold()>:
   0:	53                   	push   rbx
   1:	48 83 ec 20          	sub    rsp,0x20
   5:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   8:	48 89 cb             	mov    rbx,rcx
   b:	ff 50 10             	call   QWORD PTR [rax+0x10]
   e:	f0 83 6b 0c 01       	lock sub DWORD PTR [rbx+0xc],0x1
  13:	75 1b                	jne    30 <std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release_last_use_cold()+0x30>
  15:	48 8b 03             	mov    rax,QWORD PTR [rbx]
  18:	48 89 d9             	mov    rcx,rbx
  1b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
  1f:	48 83 c4 20          	add    rsp,0x20
  23:	5b                   	pop    rbx
  24:	48 ff e0             	rex.W jmp rax
  27:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  2e:	00 00 
  30:	48 83 c4 20          	add    rsp,0x20
  34:	5b                   	pop    rbx
  35:	c3                   	ret
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

Disassembly of section .text$_ZNSt16_Sp_counted_baseILN9__gnu_cxx12_Lock_policyE2EE10_M_releaseEv:

0000000000000000 <std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release()>:
   0:	48 83 ec 38          	sub    rsp,0x38
   4:	48 ba 01 00 00 00 01 	movabs rdx,0x100000001
   b:	00 00 00 
   e:	4c 8b 41 08          	mov    r8,QWORD PTR [rcx+0x8]
  12:	48 8d 41 08          	lea    rax,[rcx+0x8]
  16:	49 39 d0             	cmp    r8,rdx
  19:	74 15                	je     30 <std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release()+0x30>
  1b:	f0 83 28 01          	lock sub DWORD PTR [rax],0x1
  1f:	74 3f                	je     60 <std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release()+0x60>
  21:	48 83 c4 38          	add    rsp,0x38
  25:	c3                   	ret
  26:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  2d:	00 00 00 
  30:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  33:	48 89 4c 24 28       	mov    QWORD PTR [rsp+0x28],rcx
  38:	48 c7 41 08 00 00 00 	mov    QWORD PTR [rcx+0x8],0x0
  3f:	00 
  40:	ff 50 10             	call   QWORD PTR [rax+0x10]
  43:	48 8b 4c 24 28       	mov    rcx,QWORD PTR [rsp+0x28]
  48:	48 8b 01             	mov    rax,QWORD PTR [rcx]
  4b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
  4f:	48 83 c4 38          	add    rsp,0x38
  53:	48 ff e0             	rex.W jmp rax
  56:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  5d:	00 00 00 
  60:	48 83 c4 38          	add    rsp,0x38
  64:	e9 00 00 00 00       	jmp    69 <std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release()+0x69>
  69:	90                   	nop
  6a:	90                   	nop
  6b:	90                   	nop
  6c:	90                   	nop
  6d:	90                   	nop
  6e:	90                   	nop
  6f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	53                   	push   rbx
   1:	48 83 ec 40          	sub    rsp,0x40
   5:	e8 00 00 00 00       	call   a <main+0xa>
   a:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
   f:	e8 20 00 00 00       	call   34 <main+0x34>
  14:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
  19:	48 8d 54 24 20       	lea    rdx,[rsp+0x20]
  1e:	e8 00 00 00 00       	call   23 <main+0x23>
  23:	48 8b 44 24 30       	mov    rax,QWORD PTR [rsp+0x30]
  28:	48 8b 4c 24 38       	mov    rcx,QWORD PTR [rsp+0x38]
  2d:	8b 18                	mov    ebx,DWORD PTR [rax]
  2f:	48 85 c9             	test   rcx,rcx
  32:	74 05                	je     39 <main+0x39>
  34:	e8 00 00 00 00       	call   39 <main+0x39>
  39:	48 8b 4c 24 28       	mov    rcx,QWORD PTR [rsp+0x28]
  3e:	48 85 c9             	test   rcx,rcx
  41:	74 05                	je     48 <main+0x48>
  43:	e8 00 00 00 00       	call   48 <main+0x48>
  48:	89 d8                	mov    eax,ebx
  4a:	48 83 c4 40          	add    rsp,0x40
  4e:	5b                   	pop    rbx
  4f:	c3                   	ret
