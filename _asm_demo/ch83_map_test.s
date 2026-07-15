
ch83_map_test.o:     file format pe-x86-64


Disassembly of section .text:

0000000000000000 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]>:
   0:	48 83 ec 38          	sub    rsp,0x38
   4:	49 89 cb             	mov    r11,rcx
   7:	48 8b 4a 10          	mov    rcx,QWORD PTR [rdx+0x10]
   b:	48 85 c9             	test   rcx,rcx
   e:	75 13                	jne    23 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x23>
  10:	eb 4e                	jmp    60 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x60>
  12:	0f 1f 00             	nop    DWORD PTR [rax]
  15:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  1c:	00 00 00 00 
  20:	48 89 c1             	mov    rcx,rax
  23:	44 8b 49 20          	mov    r9d,DWORD PTR [rcx+0x20]
  27:	48 8b 41 18          	mov    rax,QWORD PTR [rcx+0x18]
  2b:	45 39 c8             	cmp    r8d,r9d
  2e:	48 0f 4c 41 10       	cmovl  rax,QWORD PTR [rcx+0x10]
  33:	41 0f 9c c2          	setl   r10b
  37:	48 85 c0             	test   rax,rax
  3a:	75 e4                	jne    20 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x20>
  3c:	48 89 c8             	mov    rax,rcx
  3f:	45 84 d2             	test   r10b,r10b
  42:	75 20                	jne    64 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x64>
  44:	45 39 c8             	cmp    r8d,r9d
  47:	7f 53                	jg     9c <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x9c>
  49:	4c 89 d8             	mov    rax,r11
  4c:	49 89 0b             	mov    QWORD PTR [r11],rcx
  4f:	49 c7 43 08 00 00 00 	mov    QWORD PTR [r11+0x8],0x0
  56:	00 
  57:	48 83 c4 38          	add    rsp,0x38
  5b:	c3                   	ret
  5c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  60:	48 8d 4a 08          	lea    rcx,[rdx+0x8]
  64:	48 3b 4a 18          	cmp    rcx,QWORD PTR [rdx+0x18]
  68:	74 46                	je     b0 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0xb0>
  6a:	44 89 44 24 50       	mov    DWORD PTR [rsp+0x50],r8d
  6f:	4c 89 5c 24 40       	mov    QWORD PTR [rsp+0x40],r11
  74:	48 89 4c 24 28       	mov    QWORD PTR [rsp+0x28],rcx
  79:	e8 00 00 00 00       	call   7e <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x7e>
  7e:	44 8b 44 24 50       	mov    r8d,DWORD PTR [rsp+0x50]
  83:	4c 8b 5c 24 40       	mov    r11,QWORD PTR [rsp+0x40]
  88:	44 8b 48 20          	mov    r9d,DWORD PTR [rax+0x20]
  8c:	48 89 c2             	mov    rdx,rax
  8f:	48 8b 44 24 28       	mov    rax,QWORD PTR [rsp+0x28]
  94:	48 89 d1             	mov    rcx,rdx
  97:	45 39 c8             	cmp    r8d,r9d
  9a:	7e ad                	jle    49 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]+0x49>
  9c:	49 89 43 08          	mov    QWORD PTR [r11+0x8],rax
  a0:	4c 89 d8             	mov    rax,r11
  a3:	49 c7 03 00 00 00 00 	mov    QWORD PTR [r11],0x0
  aa:	48 83 c4 38          	add    rsp,0x38
  ae:	c3                   	ret
  af:	90                   	nop
  b0:	4c 89 d8             	mov    rax,r11
  b3:	49 c7 03 00 00 00 00 	mov    QWORD PTR [r11],0x0
  ba:	49 89 4b 08          	mov    QWORD PTR [r11+0x8],rcx
  be:	48 83 c4 38          	add    rsp,0x38
  c2:	c3                   	ret
  c3:	90                   	nop
  c4:	90                   	nop
  c5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  cc:	00 00 00 00 

00000000000000d0 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]>:
  d0:	41 54                	push   r12
  d2:	55                   	push   rbp
  d3:	57                   	push   rdi
  d4:	56                   	push   rsi
  d5:	53                   	push   rbx
  d6:	48 83 ec 40          	sub    rsp,0x40
  da:	48 89 ce             	mov    rsi,rcx
  dd:	b9 28 00 00 00       	mov    ecx,0x28
  e2:	4c 89 c5             	mov    rbp,r8
  e5:	48 89 d3             	mov    rbx,rdx
  e8:	e8 00 00 00 00       	call   ed <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x1d>
  ed:	4c 8d 66 08          	lea    r12,[rsi+0x8]
  f1:	48 89 da             	mov    rdx,rbx
  f4:	48 89 c7             	mov    rdi,rax
  f7:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
  fb:	c7 47 24 00 00 00 00 	mov    DWORD PTR [rdi+0x24],0x0
 102:	8b 28                	mov    ebp,DWORD PTR [rax]
 104:	89 6f 20             	mov    DWORD PTR [rdi+0x20],ebp
 107:	49 39 dc             	cmp    r12,rbx
 10a:	0f 84 b0 00 00 00    	je     1c0 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xf0>
 110:	3b 6b 20             	cmp    ebp,DWORD PTR [rbx+0x20]
 113:	7d 3b                	jge    150 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x80>
 115:	4c 8b 46 18          	mov    r8,QWORD PTR [rsi+0x18]
 119:	49 39 d8             	cmp    r8,rbx
 11c:	74 72                	je     190 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xc0>
 11e:	48 89 d9             	mov    rcx,rbx
 121:	e8 00 00 00 00       	call   126 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x56>
 126:	49 89 c0             	mov    r8,rax
 129:	3b 68 20             	cmp    ebp,DWORD PTR [rax+0x20]
 12c:	0f 8e 95 00 00 00    	jle    1c7 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xf7>
 132:	48 83 78 18 00       	cmp    QWORD PTR [rax+0x18],0x0
 137:	0f 84 dd 00 00 00    	je     21a <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x14a>
 13d:	49 89 d8             	mov    r8,rbx
 140:	b9 01 00 00 00       	mov    ecx,0x1
 145:	eb 4e                	jmp    195 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xc5>
 147:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 14e:	00 00 
 150:	0f 8e 96 00 00 00    	jle    1ec <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x11c>
 156:	48 39 5e 20          	cmp    QWORD PTR [rsi+0x20],rbx
 15a:	0f 84 da 00 00 00    	je     23a <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x16a>
 160:	48 89 d9             	mov    rcx,rbx
 163:	48 89 5c 24 28       	mov    QWORD PTR [rsp+0x28],rbx
 168:	e8 00 00 00 00       	call   16d <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x9d>
 16d:	49 89 c0             	mov    r8,rax
 170:	3b 68 20             	cmp    ebp,DWORD PTR [rax+0x20]
 173:	7d 52                	jge    1c7 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xf7>
 175:	48 83 7b 18 00       	cmp    QWORD PTR [rbx+0x18],0x0
 17a:	48 8b 54 24 28       	mov    rdx,QWORD PTR [rsp+0x28]
 17f:	0f 84 b5 00 00 00    	je     23a <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x16a>
 185:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 18c:	00 00 00 00 
 190:	b9 01 00 00 00       	mov    ecx,0x1
 195:	4d 89 e1             	mov    r9,r12
 198:	48 89 fa             	mov    rdx,rdi
 19b:	48 89 fb             	mov    rbx,rdi
 19e:	e8 00 00 00 00       	call   1a3 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xd3>
 1a3:	48 83 46 28 01       	add    QWORD PTR [rsi+0x28],0x1
 1a8:	48 89 d8             	mov    rax,rbx
 1ab:	48 83 c4 40          	add    rsp,0x40
 1af:	5b                   	pop    rbx
 1b0:	5e                   	pop    rsi
 1b1:	5f                   	pop    rdi
 1b2:	5d                   	pop    rbp
 1b3:	41 5c                	pop    r12
 1b5:	c3                   	ret
 1b6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 1bd:	00 00 00 
 1c0:	48 83 7e 28 00       	cmp    QWORD PTR [rsi+0x28],0x0
 1c5:	75 49                	jne    210 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x140>
 1c7:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
 1cc:	41 89 e8             	mov    r8d,ebp
 1cf:	48 89 f2             	mov    rdx,rsi
 1d2:	e8 29 fe ff ff       	call   0 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_get_insert_unique_pos(int const&) [clone .isra.0]>
 1d7:	48 8b 4c 24 30       	mov    rcx,QWORD PTR [rsp+0x30]
 1dc:	48 8b 44 24 38       	mov    rax,QWORD PTR [rsp+0x38]
 1e1:	48 89 ca             	mov    rdx,rcx
 1e4:	49 89 c0             	mov    r8,rax
 1e7:	48 85 c0             	test   rax,rax
 1ea:	75 34                	jne    220 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x150>
 1ec:	48 89 d3             	mov    rbx,rdx
 1ef:	48 89 f9             	mov    rcx,rdi
 1f2:	ba 28 00 00 00       	mov    edx,0x28
 1f7:	e8 00 00 00 00       	call   1fc <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x12c>
 1fc:	48 89 d8             	mov    rax,rbx
 1ff:	48 83 c4 40          	add    rsp,0x40
 203:	5b                   	pop    rbx
 204:	5e                   	pop    rsi
 205:	5f                   	pop    rdi
 206:	5d                   	pop    rbp
 207:	41 5c                	pop    r12
 209:	c3                   	ret
 20a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 210:	4c 8b 46 20          	mov    r8,QWORD PTR [rsi+0x20]
 214:	41 3b 68 20          	cmp    ebp,DWORD PTR [r8+0x20]
 218:	7e ad                	jle    1c7 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xf7>
 21a:	31 c0                	xor    eax,eax
 21c:	eb 08                	jmp    226 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0x156>
 21e:	66 90                	xchg   ax,ax
 220:	48 85 c9             	test   rcx,rcx
 223:	0f 95 c0             	setne  al
 226:	4d 39 c4             	cmp    r12,r8
 229:	0f 84 61 ff ff ff    	je     190 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xc0>
 22f:	84 c0                	test   al,al
 231:	0f 85 59 ff ff ff    	jne    190 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xc0>
 237:	4c 89 c2             	mov    rdx,r8
 23a:	31 c9                	xor    ecx,ecx
 23c:	3b 6a 20             	cmp    ebp,DWORD PTR [rdx+0x20]
 23f:	49 89 d0             	mov    r8,rdx
 242:	0f 9c c1             	setl   cl
 245:	e9 4b ff ff ff       	jmp    195 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]+0xc5>
 24a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000000250 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]>:
 250:	41 57                	push   r15
 252:	41 56                	push   r14
 254:	41 55                	push   r13
 256:	41 54                	push   r12
 258:	55                   	push   rbp
 259:	57                   	push   rdi
 25a:	56                   	push   rsi
 25b:	53                   	push   rbx
 25c:	48 83 ec 28          	sub    rsp,0x28
 260:	48 89 4c 24 70       	mov    QWORD PTR [rsp+0x70],rcx
 265:	48 85 c9             	test   rcx,rcx
 268:	0f 84 81 01 00 00    	je     3ef <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x19f>
 26e:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
 273:	4c 8b 68 18          	mov    r13,QWORD PTR [rax+0x18]
 277:	4d 85 ed             	test   r13,r13
 27a:	0f 84 4a 01 00 00    	je     3ca <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x17a>
 280:	4d 8b 75 18          	mov    r14,QWORD PTR [r13+0x18]
 284:	4d 85 f6             	test   r14,r14
 287:	0f 84 1f 01 00 00    	je     3ac <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x15c>
 28d:	4d 8b 7e 18          	mov    r15,QWORD PTR [r14+0x18]
 291:	4d 85 ff             	test   r15,r15
 294:	0f 84 f4 00 00 00    	je     38e <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x13e>
 29a:	49 8b 5f 18          	mov    rbx,QWORD PTR [r15+0x18]
 29e:	48 85 db             	test   rbx,rbx
 2a1:	0f 84 a7 00 00 00    	je     34e <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xfe>
 2a7:	48 8b 7b 18          	mov    rdi,QWORD PTR [rbx+0x18]
 2ab:	48 85 ff             	test   rdi,rdi
 2ae:	74 5b                	je     30b <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xbb>
 2b0:	48 8b 6f 18          	mov    rbp,QWORD PTR [rdi+0x18]
 2b4:	48 85 ed             	test   rbp,rbp
 2b7:	74 77                	je     330 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xe0>
 2b9:	48 8b 75 18          	mov    rsi,QWORD PTR [rbp+0x18]
 2bd:	48 85 f6             	test   rsi,rsi
 2c0:	0f 84 aa 00 00 00    	je     370 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x120>
 2c6:	4c 8b 66 18          	mov    r12,QWORD PTR [rsi+0x18]
 2ca:	4d 85 e4             	test   r12,r12
 2cd:	74 21                	je     2f0 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xa0>
 2cf:	49 8b 4c 24 18       	mov    rcx,QWORD PTR [r12+0x18]
 2d4:	e8 77 ff ff ff       	call   250 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]>
 2d9:	4c 89 e1             	mov    rcx,r12
 2dc:	4d 8b 64 24 10       	mov    r12,QWORD PTR [r12+0x10]
 2e1:	ba 28 00 00 00       	mov    edx,0x28
 2e6:	e8 00 00 00 00       	call   2eb <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x9b>
 2eb:	4d 85 e4             	test   r12,r12
 2ee:	75 df                	jne    2cf <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x7f>
 2f0:	4c 8b 66 10          	mov    r12,QWORD PTR [rsi+0x10]
 2f4:	ba 28 00 00 00       	mov    edx,0x28
 2f9:	48 89 f1             	mov    rcx,rsi
 2fc:	e8 00 00 00 00       	call   301 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xb1>
 301:	4d 85 e4             	test   r12,r12
 304:	74 6a                	je     370 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x120>
 306:	4c 89 e6             	mov    rsi,r12
 309:	eb bb                	jmp    2c6 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x76>
 30b:	48 8b 73 10          	mov    rsi,QWORD PTR [rbx+0x10]
 30f:	ba 28 00 00 00       	mov    edx,0x28
 314:	48 89 d9             	mov    rcx,rbx
 317:	e8 00 00 00 00       	call   31c <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xcc>
 31c:	48 85 f6             	test   rsi,rsi
 31f:	74 2d                	je     34e <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xfe>
 321:	48 89 f3             	mov    rbx,rsi
 324:	eb 81                	jmp    2a7 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x57>
 326:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 32d:	00 00 00 
 330:	48 8b 77 10          	mov    rsi,QWORD PTR [rdi+0x10]
 334:	ba 28 00 00 00       	mov    edx,0x28
 339:	48 89 f9             	mov    rcx,rdi
 33c:	e8 00 00 00 00       	call   341 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xf1>
 341:	48 85 f6             	test   rsi,rsi
 344:	74 c5                	je     30b <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xbb>
 346:	48 89 f7             	mov    rdi,rsi
 349:	e9 62 ff ff ff       	jmp    2b0 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x60>
 34e:	49 8b 5f 10          	mov    rbx,QWORD PTR [r15+0x10]
 352:	ba 28 00 00 00       	mov    edx,0x28
 357:	4c 89 f9             	mov    rcx,r15
 35a:	e8 00 00 00 00       	call   35f <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x10f>
 35f:	48 85 db             	test   rbx,rbx
 362:	74 2a                	je     38e <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x13e>
 364:	49 89 df             	mov    r15,rbx
 367:	e9 2e ff ff ff       	jmp    29a <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x4a>
 36c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 370:	48 8b 75 10          	mov    rsi,QWORD PTR [rbp+0x10]
 374:	ba 28 00 00 00       	mov    edx,0x28
 379:	48 89 e9             	mov    rcx,rbp
 37c:	e8 00 00 00 00       	call   381 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x131>
 381:	48 85 f6             	test   rsi,rsi
 384:	74 aa                	je     330 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0xe0>
 386:	48 89 f5             	mov    rbp,rsi
 389:	e9 2b ff ff ff       	jmp    2b9 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x69>
 38e:	49 8b 5e 10          	mov    rbx,QWORD PTR [r14+0x10]
 392:	ba 28 00 00 00       	mov    edx,0x28
 397:	4c 89 f1             	mov    rcx,r14
 39a:	e8 00 00 00 00       	call   39f <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x14f>
 39f:	48 85 db             	test   rbx,rbx
 3a2:	74 08                	je     3ac <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x15c>
 3a4:	49 89 de             	mov    r14,rbx
 3a7:	e9 e1 fe ff ff       	jmp    28d <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x3d>
 3ac:	49 8b 5d 10          	mov    rbx,QWORD PTR [r13+0x10]
 3b0:	ba 28 00 00 00       	mov    edx,0x28
 3b5:	4c 89 e9             	mov    rcx,r13
 3b8:	e8 00 00 00 00       	call   3bd <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x16d>
 3bd:	48 85 db             	test   rbx,rbx
 3c0:	74 08                	je     3ca <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x17a>
 3c2:	49 89 dd             	mov    r13,rbx
 3c5:	e9 b6 fe ff ff       	jmp    280 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x30>
 3ca:	48 8b 44 24 70       	mov    rax,QWORD PTR [rsp+0x70]
 3cf:	ba 28 00 00 00       	mov    edx,0x28
 3d4:	48 8b 58 10          	mov    rbx,QWORD PTR [rax+0x10]
 3d8:	48 89 c1             	mov    rcx,rax
 3db:	e8 00 00 00 00       	call   3e0 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x190>
 3e0:	48 85 db             	test   rbx,rbx
 3e3:	74 0a                	je     3ef <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x19f>
 3e5:	48 89 5c 24 70       	mov    QWORD PTR [rsp+0x70],rbx
 3ea:	e9 7f fe ff ff       	jmp    26e <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x1e>
 3ef:	48 83 c4 28          	add    rsp,0x28
 3f3:	5b                   	pop    rbx
 3f4:	5e                   	pop    rsi
 3f5:	5f                   	pop    rdi
 3f6:	5d                   	pop    rbp
 3f7:	41 5c                	pop    r12
 3f9:	41 5d                	pop    r13
 3fb:	41 5e                	pop    r14
 3fd:	41 5f                	pop    r15
 3ff:	c3                   	ret

0000000000000400 <build()>:
 400:	57                   	push   rdi
 401:	56                   	push   rsi
 402:	53                   	push   rbx
 403:	48 83 ec 50          	sub    rsp,0x50
 407:	48 8d 79 08          	lea    rdi,[rcx+0x8]
 40b:	48 8d 74 24 48       	lea    rsi,[rsp+0x48]
 410:	48 89 cb             	mov    rbx,rcx
 413:	c7 41 08 00 00 00 00 	mov    DWORD PTR [rcx+0x8],0x0
 41a:	48 c7 41 10 00 00 00 	mov    QWORD PTR [rcx+0x10],0x0
 421:	00 
 422:	4c 8d 44 24 38       	lea    r8,[rsp+0x38]
 427:	48 89 fa             	mov    rdx,rdi
 42a:	48 89 79 18          	mov    QWORD PTR [rcx+0x18],rdi
 42e:	48 89 79 20          	mov    QWORD PTR [rcx+0x20],rdi
 432:	48 c7 41 28 00 00 00 	mov    QWORD PTR [rcx+0x28],0x0
 439:	00 
 43a:	c7 44 24 48 01 00 00 	mov    DWORD PTR [rsp+0x48],0x1
 441:	00 
 442:	48 89 74 24 38       	mov    QWORD PTR [rsp+0x38],rsi
 447:	e8 84 fc ff ff       	call   d0 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]>
 44c:	48 8b 4b 10          	mov    rcx,QWORD PTR [rbx+0x10]
 450:	c7 40 24 0a 00 00 00 	mov    DWORD PTR [rax+0x24],0xa
 457:	49 89 f9             	mov    r9,rdi
 45a:	c7 44 24 48 02 00 00 	mov    DWORD PTR [rsp+0x48],0x2
 461:	00 
 462:	48 85 c9             	test   rcx,rcx
 465:	74 4a                	je     4b1 <build()+0xb1>
 467:	48 89 c8             	mov    rax,rcx
 46a:	eb 1f                	jmp    48b <build()+0x8b>
 46c:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 473:	00 00 
 475:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 47c:	00 00 00 00 
 480:	49 89 c1             	mov    r9,rax
 483:	4c 89 c0             	mov    rax,r8
 486:	48 85 c0             	test   rax,rax
 489:	74 16                	je     4a1 <build()+0xa1>
 48b:	4c 8b 40 10          	mov    r8,QWORD PTR [rax+0x10]
 48f:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
 493:	83 78 20 01          	cmp    DWORD PTR [rax+0x20],0x1
 497:	7f e7                	jg     480 <build()+0x80>
 499:	48 89 d0             	mov    rax,rdx
 49c:	48 85 c0             	test   rax,rax
 49f:	75 ea                	jne    48b <build()+0x8b>
 4a1:	4c 39 cf             	cmp    rdi,r9
 4a4:	74 0b                	je     4b1 <build()+0xb1>
 4a6:	41 83 79 20 02       	cmp    DWORD PTR [r9+0x20],0x2
 4ab:	0f 8e af 00 00 00    	jle    560 <build()+0x160>
 4b1:	4c 8d 44 24 40       	lea    r8,[rsp+0x40]
 4b6:	4c 89 ca             	mov    rdx,r9
 4b9:	48 89 d9             	mov    rcx,rbx
 4bc:	48 89 74 24 40       	mov    QWORD PTR [rsp+0x40],rsi
 4c1:	4c 89 44 24 28       	mov    QWORD PTR [rsp+0x28],r8
 4c6:	e8 05 fc ff ff       	call   d0 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]>
 4cb:	48 8b 4b 10          	mov    rcx,QWORD PTR [rbx+0x10]
 4cf:	4c 8b 44 24 28       	mov    r8,QWORD PTR [rsp+0x28]
 4d4:	c7 40 24 14 00 00 00 	mov    DWORD PTR [rax+0x24],0x14
 4db:	c7 44 24 40 03 00 00 	mov    DWORD PTR [rsp+0x40],0x3
 4e2:	00 
 4e3:	48 85 c9             	test   rcx,rcx
 4e6:	0f 84 8c 00 00 00    	je     578 <build()+0x178>
 4ec:	48 89 fa             	mov    rdx,rdi
 4ef:	eb 1a                	jmp    50b <build()+0x10b>
 4f1:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 4f5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 4fc:	00 00 00 00 
 500:	48 89 ca             	mov    rdx,rcx
 503:	4c 89 c9             	mov    rcx,r9
 506:	48 85 c9             	test   rcx,rcx
 509:	74 16                	je     521 <build()+0x121>
 50b:	4c 8b 49 10          	mov    r9,QWORD PTR [rcx+0x10]
 50f:	4c 8b 41 18          	mov    r8,QWORD PTR [rcx+0x18]
 513:	83 79 20 02          	cmp    DWORD PTR [rcx+0x20],0x2
 517:	7f e7                	jg     500 <build()+0x100>
 519:	4c 89 c1             	mov    rcx,r8
 51c:	48 85 c9             	test   rcx,rcx
 51f:	75 ea                	jne    50b <build()+0x10b>
 521:	48 39 d7             	cmp    rdi,rdx
 524:	74 06                	je     52c <build()+0x12c>
 526:	83 7a 20 03          	cmp    DWORD PTR [rdx+0x20],0x3
 52a:	7e 18                	jle    544 <build()+0x144>
 52c:	4c 8d 44 24 40       	lea    r8,[rsp+0x40]
 531:	4c 89 44 24 48       	mov    QWORD PTR [rsp+0x48],r8
 536:	48 89 d9             	mov    rcx,rbx
 539:	49 89 f0             	mov    r8,rsi
 53c:	e8 8f fb ff ff       	call   d0 <std::_Rb_tree_iterator<std::pair<int const, int> > std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_emplace_hint_unique<std::piecewise_construct_t const&, std::tuple<int&&>, std::tuple<> >(std::_Rb_tree_const_iterator<std::pair<int const, int> >, std::piecewise_construct_t const&, std::tuple<int&&>&&, std::tuple<>&&) [clone .isra.0]>
 541:	48 89 c2             	mov    rdx,rax
 544:	48 89 d8             	mov    rax,rbx
 547:	c7 42 24 1e 00 00 00 	mov    DWORD PTR [rdx+0x24],0x1e
 54e:	48 83 c4 50          	add    rsp,0x50
 552:	5b                   	pop    rbx
 553:	5e                   	pop    rsi
 554:	5f                   	pop    rdi
 555:	c3                   	ret
 556:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
 55d:	00 00 00 
 560:	41 c7 41 24 14 00 00 	mov    DWORD PTR [r9+0x24],0x14
 567:	00 
 568:	c7 44 24 40 03 00 00 	mov    DWORD PTR [rsp+0x40],0x3
 56f:	00 
 570:	e9 77 ff ff ff       	jmp    4ec <build()+0xec>
 575:	0f 1f 00             	nop    DWORD PTR [rax]
 578:	48 89 fa             	mov    rdx,rdi
 57b:	eb b4                	jmp    531 <build()+0x131>
 57d:	48 89 c6             	mov    rsi,rax
 580:	e9 00 00 00 00       	jmp    585 <build()+0x185>
 585:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 58c:	00 00 00 00 

0000000000000590 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)>:
 590:	48 8b 41 10          	mov    rax,QWORD PTR [rcx+0x10]
 594:	48 85 c0             	test   rax,rax
 597:	74 67                	je     600 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x70>
 599:	48 83 c1 08          	add    rcx,0x8
 59d:	49 89 ca             	mov    r10,rcx
 5a0:	eb 26                	jmp    5c8 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x38>
 5a2:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
 5a9:	00 
 5aa:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 5b1:	00 00 00 00 
 5b5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
 5bc:	00 00 00 00 
 5c0:	4c 89 c8             	mov    rax,r9
 5c3:	48 85 c0             	test   rax,rax
 5c6:	74 18                	je     5e0 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x50>
 5c8:	4c 8b 40 10          	mov    r8,QWORD PTR [rax+0x10]
 5cc:	4c 8b 48 18          	mov    r9,QWORD PTR [rax+0x18]
 5d0:	39 50 20             	cmp    DWORD PTR [rax+0x20],edx
 5d3:	7c eb                	jl     5c0 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x30>
 5d5:	49 89 c2             	mov    r10,rax
 5d8:	4c 89 c0             	mov    rax,r8
 5db:	48 85 c0             	test   rax,rax
 5de:	75 e8                	jne    5c8 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x38>
 5e0:	b8 ff ff ff ff       	mov    eax,0xffffffff
 5e5:	4c 39 d1             	cmp    rcx,r10
 5e8:	74 06                	je     5f0 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x60>
 5ea:	41 39 52 20          	cmp    DWORD PTR [r10+0x20],edx
 5ee:	7e 08                	jle    5f8 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x68>
 5f0:	c3                   	ret
 5f1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 5f8:	41 8b 42 24          	mov    eax,DWORD PTR [r10+0x24]
 5fc:	c3                   	ret
 5fd:	0f 1f 00             	nop    DWORD PTR [rax]
 600:	b8 ff ff ff ff       	mov    eax,0xffffffff
 605:	c3                   	ret
 606:	90                   	nop
 607:	90                   	nop
 608:	90                   	nop
 609:	90                   	nop
 60a:	90                   	nop
 60b:	90                   	nop
 60c:	90                   	nop
 60d:	90                   	nop
 60e:	90                   	nop
 60f:	90                   	nop
 610:	90                   	nop
 611:	90                   	nop
 612:	90                   	nop
 613:	90                   	nop
 614:	90                   	nop
 615:	90                   	nop
 616:	90                   	nop
 617:	90                   	nop
 618:	90                   	nop
 619:	90                   	nop
 61a:	90                   	nop
 61b:	90                   	nop
 61c:	90                   	nop
 61d:	90                   	nop
 61e:	90                   	nop
 61f:	90                   	nop

Disassembly of section .text.unlikely:

0000000000000000 <build() [clone .cold]>:
   0:	48 8b 4b 10          	mov    rcx,QWORD PTR [rbx+0x10]
   4:	e8 50 02 00 00       	call   259 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x9>
   9:	48 89 f1             	mov    rcx,rsi
   c:	e8 00 00 00 00       	call   11 <build() [clone .cold]+0x11>
  11:	90                   	nop
  12:	90                   	nop
  13:	90                   	nop
  14:	90                   	nop
  15:	90                   	nop
  16:	90                   	nop
  17:	90                   	nop
  18:	90                   	nop
  19:	90                   	nop
  1a:	90                   	nop
  1b:	90                   	nop
  1c:	90                   	nop
  1d:	90                   	nop
  1e:	90                   	nop
  1f:	90                   	nop

Disassembly of section .text.startup:

0000000000000000 <main>:
   0:	53                   	push   rbx
   1:	48 83 ec 60          	sub    rsp,0x60
   5:	e8 00 00 00 00       	call   a <main+0xa>
   a:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   f:	e8 00 04 00 00       	call   414 <build()+0x14>
  14:	ba 02 00 00 00       	mov    edx,0x2
  19:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
  1e:	e8 90 05 00 00       	call   5b3 <find_it(std::map<int, int, std::less<int>, std::allocator<std::pair<int const, int> > > const&, int)+0x23>
  23:	48 8b 4c 24 40       	mov    rcx,QWORD PTR [rsp+0x40]
  28:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
  2c:	8b 5c 24 2c          	mov    ebx,DWORD PTR [rsp+0x2c]
  30:	e8 50 02 00 00       	call   285 <std::_Rb_tree<int, std::pair<int const, int>, std::_Select1st<std::pair<int const, int> >, std::less<int>, std::allocator<std::pair<int const, int> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, int> >*) [clone .isra.0]+0x35>
  35:	89 d8                	mov    eax,ebx
  37:	48 83 c4 60          	add    rsp,0x60
  3b:	5b                   	pop    rbx
  3c:	c3                   	ret
  3d:	90                   	nop
  3e:	90                   	nop
  3f:	90                   	nop
