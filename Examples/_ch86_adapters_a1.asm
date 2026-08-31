	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2312:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB4681:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	rbx, rcx
	mov	rsi, QWORD PTR 240[rcx+rax]
	test	rsi, rsi
	je	.L8
	cmp	BYTE PTR 56[rsi], 0
	je	.L5
	movsx	edx, BYTE PTR 67[rsi]
.L6:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L5:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L6
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L6
.L8:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0
_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0:
.LFB4676:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR 72[rcx]
	mov	rbx, QWORD PTR 40[rcx]
	lea	rsi, 8[rax]
	mov	rdi, rcx
	cmp	rbx, rsi
	jnb	.L10
	.p2align 4,,10
	.p2align 3
.L11:
	mov	rcx, QWORD PTR [rbx]
	mov	edx, 512
	add	rbx, 8
	call	_ZdlPvy
	cmp	rbx, rsi
	jb	.L11
.L10:
	mov	rax, QWORD PTR 8[rdi]
	mov	rcx, QWORD PTR [rdi]
	lea	rdx, 0[0+rax*8]
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0:
.LFB4687:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	rcx, rcx
	mov	QWORD PTR 112[rsp], rcx
	je	.L13
.L31:
	mov	rax, QWORD PTR 112[rsp]
	mov	r13, QWORD PTR 24[rax]
	test	r13, r13
	je	.L15
.L30:
	mov	r14, QWORD PTR 24[r13]
	test	r14, r14
	je	.L16
.L29:
	mov	r15, QWORD PTR 24[r14]
	test	r15, r15
	je	.L17
.L28:
	mov	rbx, QWORD PTR 24[r15]
	test	rbx, rbx
	je	.L18
.L27:
	mov	rsi, QWORD PTR 24[rbx]
	test	rsi, rsi
	je	.L19
.L26:
	mov	rbp, QWORD PTR 24[rsi]
	test	rbp, rbp
	je	.L20
.L25:
	mov	rdi, QWORD PTR 24[rbp]
	test	rdi, rdi
	je	.L21
.L24:
	mov	r12, QWORD PTR 24[rdi]
	test	r12, r12
	je	.L22
.L23:
	mov	rcx, QWORD PTR 24[r12]
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
	mov	rcx, r12
	mov	r12, QWORD PTR 16[r12]
	mov	edx, 40
	call	_ZdlPvy
	test	r12, r12
	jne	.L23
.L22:
	mov	r12, QWORD PTR 16[rdi]
	mov	edx, 40
	mov	rcx, rdi
	call	_ZdlPvy
	test	r12, r12
	je	.L21
	mov	rdi, r12
	jmp	.L24
.L19:
	mov	rsi, QWORD PTR 16[rbx]
	mov	edx, 40
	mov	rcx, rbx
	call	_ZdlPvy
	test	rsi, rsi
	je	.L18
	mov	rbx, rsi
	jmp	.L27
	.p2align 4,,10
	.p2align 3
.L20:
	mov	rdi, QWORD PTR 16[rsi]
	mov	edx, 40
	mov	rcx, rsi
	call	_ZdlPvy
	test	rdi, rdi
	je	.L19
	mov	rsi, rdi
	jmp	.L26
.L18:
	mov	rbx, QWORD PTR 16[r15]
	mov	edx, 40
	mov	rcx, r15
	call	_ZdlPvy
	test	rbx, rbx
	je	.L17
	mov	r15, rbx
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L21:
	mov	rdi, QWORD PTR 16[rbp]
	mov	edx, 40
	mov	rcx, rbp
	call	_ZdlPvy
	test	rdi, rdi
	je	.L20
	mov	rbp, rdi
	jmp	.L25
.L17:
	mov	rbx, QWORD PTR 16[r14]
	mov	edx, 40
	mov	rcx, r14
	call	_ZdlPvy
	test	rbx, rbx
	je	.L16
	mov	r14, rbx
	jmp	.L29
.L16:
	mov	rbx, QWORD PTR 16[r13]
	mov	edx, 40
	mov	rcx, r13
	call	_ZdlPvy
	test	rbx, rbx
	je	.L15
	mov	r13, rbx
	jmp	.L30
.L15:
	mov	rax, QWORD PTR 112[rsp]
	mov	edx, 40
	mov	rbx, QWORD PTR 16[rax]
	mov	rcx, rax
	call	_ZdlPvy
	test	rbx, rbx
	je	.L13
	mov	QWORD PTR 112[rsp], rbx
	jmp	.L31
.L13:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIiSaIiEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIiSaIiEED1Ev
	.def	_ZNSt6vectorIiSaIiEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEED1Ev
_ZNSt6vectorIiSaIiEED1Ev:
.LFB3968:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L68
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L68:
	ret
	.seh_endproc
	.section	.text$_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_
	.def	_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_
_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_:
.LFB3988:
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	xor	eax, eax
	cmp	r8, rdx
	mov	rdi, rcx
	mov	r12, r8
	mov	DWORD PTR 8[rcx], 0
	lea	rbp, 8[rcx]
	mov	QWORD PTR 16[rcx], 0
	mov	rsi, rdx
	mov	QWORD PTR 24[rcx], rbp
	mov	QWORD PTR 32[rcx], rbp
	mov	QWORD PTR 40[rcx], 0
	je	.L70
.L77:
	test	rax, rax
	mov	edx, DWORD PTR [rsi]
	je	.L72
	mov	rbx, QWORD PTR 32[rdi]
	cmp	edx, DWORD PTR 32[rbx]
	jl	.L72
	cmp	rbp, rbx
	mov	r13d, 1
	jne	.L89
.L74:
	mov	ecx, 40
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rdx, rax
	mov	eax, DWORD PTR [rsi]
	movzx	ecx, r13b
	mov	r9, rbp
	mov	r8, rbx
	add	rsi, 4
	mov	DWORD PTR 32[rdx], eax
	call	_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_
	mov	rax, QWORD PTR 40[rdi]
	add	rax, 1
	cmp	r12, rsi
	mov	QWORD PTR 40[rdi], rax
	jne	.L77
.L70:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L72:
	mov	rbx, QWORD PTR 16[rdi]
	test	rbx, rbx
	jne	.L76
	jmp	.L90
	.p2align 4,,10
	.p2align 3
.L81:
	mov	rbx, rax
.L76:
	cmp	edx, DWORD PTR 32[rbx]
	mov	rax, QWORD PTR 24[rbx]
	cmovl	rax, QWORD PTR 16[rbx]
	test	rax, rax
	jne	.L81
	cmp	rbp, rbx
	mov	r13d, 1
	je	.L74
.L89:
	cmp	edx, DWORD PTR 32[rbx]
	setl	r13b
	jmp	.L74
.L90:
	mov	rbx, rbp
	mov	r13d, 1
	jmp	.L74
.L83:
	mov	rcx, QWORD PTR 16[rdi]
	mov	rbx, rax
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3988:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3988-.LLSDACSB3988
.LLSDACSB3988:
	.uleb128 .LEHB0-.LFB3988
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L83-.LFB3988
	.uleb128 0
	.uleb128 .LEHB1-.LFB3988
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE3988:
	.section	.text$_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt5dequeIiSaIiEE4backEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt5dequeIiSaIiEE4backEv
	.def	_ZNSt5dequeIiSaIiEE4backEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE4backEv
_ZNSt5dequeIiSaIiEE4backEv:
.LFB4207:
	.seh_endprologue
	mov	rax, QWORD PTR 48[rcx]
	cmp	rax, QWORD PTR 56[rcx]
	mov	rdx, QWORD PTR 72[rcx]
	je	.L93
	sub	rax, 4
	ret
	.p2align 4,,10
	.p2align 3
.L93:
	mov	rax, QWORD PTR -8[rdx]
	add	rax, 512
	sub	rax, 4
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC2:
	.ascii "vector::_M_realloc_insert\0"
.LC3:
	.ascii "priority_queue max-seq size: \0"
.LC4:
	.ascii "multiset    max-seq size: \0"
	.align 8
.LC5:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmp3d8bjow_\\s.cpp\0"
	.align 8
.LC6:
	.ascii "from_pq.size() == from_ms.size()\0"
.LC7:
	.ascii "k=\0"
.LC8:
	.ascii " pq=\0"
.LC9:
	.ascii " ms=\0"
.LC10:
	.ascii "from_pq[i] == from_ms[i]\0"
	.align 8
.LC12:
	.ascii "cannot create std::deque larger than max_size()\0"
.LC13:
	.ascii "stack<vector> top: \0"
.LC14:
	.ascii "stack<deque>  top: \0"
.LC15:
	.ascii "sv.top() == sd.top()\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3589:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 408
	.seh_stackalloc	408
	movaps	XMMWORD PTR 384[rsp], xmm6
	.seh_savexmm	xmm6, 384
	.seh_endprologue
	call	__main
	mov	rax, QWORD PTR .LC1[rip]
	mov	ecx, 28
	mov	DWORD PTR 328[rsp], 7
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	movaps	XMMWORD PTR 304[rsp], xmm0
	mov	QWORD PTR 320[rsp], rax
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	ecx, 28
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 232[rsp], xmm0
	lea	rbp, 28[rax]
	mov	rdi, rax
	mov	QWORD PTR 96[rsp], rax
	mov	rax, QWORD PTR 304[rsp]
	mov	QWORD PTR 112[rsp], rbp
	mov	QWORD PTR 104[rsp], rbp
	mov	QWORD PTR [rdi], rax
	mov	rax, QWORD PTR 312[rsp]
	mov	QWORD PTR 8[rdi], rax
	mov	rax, QWORD PTR 320[rsp]
	mov	QWORD PTR 16[rdi], rax
	mov	eax, DWORD PTR 328[rsp]
	mov	DWORD PTR 24[rdi], eax
.LEHB3:
	call	_Znwy
.LEHE3:
	lea	rsi, 28[rax]
	mov	rbx, rax
	mov	QWORD PTR 224[rsp], rax
	mov	rax, QWORD PTR [rdi]
	mov	QWORD PTR 240[rsp], rsi
	mov	r8d, 2
	mov	QWORD PTR 232[rsp], rsi
	mov	QWORD PTR [rbx], rax
	mov	rax, QWORD PTR 8[rdi]
	mov	QWORD PTR 8[rbx], rax
	mov	rax, QWORD PTR 16[rdi]
	mov	QWORD PTR 16[rbx], rax
	mov	eax, DWORD PTR 24[rdi]
	mov	DWORD PTR 24[rbx], eax
.L100:
	mov	r9d, DWORD PTR [rbx+r8*4]
	mov	r10, r8
	jmp	.L96
	.p2align 4,,10
	.p2align 3
.L194:
	mov	r10, rax
.L96:
	lea	rcx, 2[r10+r10]
	lea	rax, -1[rcx]
	mov	r11d, DWORD PTR [rbx+rcx*4]
	mov	edx, DWORD PTR [rbx+rax*4]
	cmp	edx, r11d
	jg	.L95
	mov	edx, r11d
	mov	rax, rcx
.L95:
	cmp	rax, 2
	mov	DWORD PTR [rbx+r10*4], edx
	jle	.L194
	lea	rcx, -1[rax]
	sar	rcx
	jmp	.L98
	.p2align 4,,10
	.p2align 3
.L247:
	mov	DWORD PTR [rax], edx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r8, rcx
	mov	rdx, rax
	mov	rax, rcx
	jge	.L246
	mov	rcx, rdx
.L98:
	lea	r10, [rbx+rcx*4]
	mov	edx, DWORD PTR [r10]
	lea	rax, [rbx+rax*4]
	cmp	r9d, edx
	jg	.L247
	test	r8, r8
	mov	DWORD PTR [rax], r9d
	je	.L99
.L248:
	sub	r8, 1
	jmp	.L100
	.p2align 4,,10
	.p2align 3
.L246:
	mov	rax, r10
	test	r8, r8
	mov	DWORD PTR [rax], r9d
	jne	.L248
.L99:
	mov	QWORD PTR 128[rsp], 0
	xor	r13d, r13d
	xor	r12d, r12d
	mov	QWORD PTR 136[rsp], 0
	mov	QWORD PTR 144[rsp], 0
	jmp	.L123
	.p2align 4,,10
	.p2align 3
.L112:
	cmp	rsi, rbx
	mov	QWORD PTR 232[rsp], rsi
	je	.L122
.L252:
	mov	r12, QWORD PTR 136[rsp]
	mov	r13, QWORD PTR 144[rsp]
.L123:
	cmp	r12, r13
	je	.L101
	mov	eax, DWORD PTR [rbx]
	add	r12, 4
	mov	DWORD PTR -4[r12], eax
	mov	QWORD PTR 136[rsp], r12
.L102:
	mov	rax, rsi
	sub	rsi, 4
	sub	rax, rbx
	cmp	rax, 4
	jle	.L112
	mov	eax, DWORD PTR [rbx]
	mov	r9d, DWORD PTR [rsi]
	mov	DWORD PTR [rsi], eax
	mov	rax, rsi
	sub	rax, rbx
	mov	r10, rax
	sar	r10, 2
	lea	rdx, -1[r10]
	mov	r11, r10
	mov	r12, rdx
	and	r11d, 1
	shr	r12, 63
	add	r12, rdx
	sar	r12
	cmp	rax, 8
	jle	.L113
	xor	r8d, r8d
	jmp	.L115
	.p2align 4,,10
	.p2align 3
.L199:
	mov	r8, rax
.L115:
	lea	rcx, 1[r8]
	lea	r13, [rcx+rcx]
	lea	rax, -1[r13]
	lea	r14, [rbx+rcx*8]
	lea	rdx, [rbx+rax*4]
	mov	r15d, DWORD PTR [r14]
	mov	ecx, DWORD PTR [rdx]
	cmp	ecx, r15d
	jg	.L114
	mov	ecx, r15d
	mov	rdx, r14
	mov	rax, r13
.L114:
	cmp	rax, r12
	mov	DWORD PTR [rbx+r8*4], ecx
	jl	.L199
	test	r11, r11
	jne	.L119
.L117:
	sub	r10, 2
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	cmp	rcx, rax
	je	.L249
.L119:
	lea	r8, -1[rax]
	mov	rcx, r8
	shr	rcx, 63
	add	rcx, r8
	sar	rcx
	test	rax, rax
	je	.L118
	mov	rdx, rax
	jmp	.L121
	.p2align 4,,10
	.p2align 3
.L251:
	mov	DWORD PTR [rdx], r8d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	mov	rdx, rcx
	sar	rax
	test	rcx, rcx
	je	.L250
	mov	rcx, rax
.L121:
	lea	r10, [rbx+rcx*4]
	mov	r8d, DWORD PTR [r10]
	lea	rdx, [rbx+rdx*4]
	cmp	r9d, r8d
	jg	.L251
.L118:
	mov	DWORD PTR [rdx], r9d
.L262:
	cmp	rsi, rbx
	mov	QWORD PTR 232[rsp], rsi
	jne	.L252
.L122:
	lea	rcx, 256[rsp]
	mov	r8, rbp
	mov	rdx, rdi
.LEHB4:
	call	_ZNSt8multisetIiSt4lessIiESaIiEEC1IN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiS2_EEEEET_SB_
.LEHE4:
	cmp	QWORD PTR 296[rsp], 0
	mov	QWORD PTR 160[rsp], 0
	mov	QWORD PTR 168[rsp], 0
	mov	QWORD PTR 176[rsp], 0
	je	.L124
	lea	rdi, 264[rsp]
	xor	r12d, r12d
	xor	ebx, ebx
	movabs	rbp, 2305843009213693951
	jmp	.L136
	.p2align 4,,10
	.p2align 3
.L253:
	mov	eax, DWORD PTR 32[rax]
	add	rbx, 4
	mov	DWORD PTR -4[rbx], eax
	mov	QWORD PTR 168[rsp], rbx
.L126:
	mov	rdx, rdi
	mov	rcx, rsi
	call	_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
	sub	QWORD PTR 296[rsp], 1
	je	.L124
	mov	rbx, QWORD PTR 168[rsp]
	mov	r12, QWORD PTR 176[rsp]
.L136:
	mov	rcx, rdi
	call	_ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base
	cmp	rbx, r12
	mov	rsi, rax
	jne	.L253
	mov	r14, QWORD PTR 160[rsp]
	sub	rbx, r14
	mov	rax, rbx
	sar	rax, 2
	cmp	rax, rbp
	je	.L254
	cmp	r14, r12
	je	.L255
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L203
	xor	r13d, r13d
	xor	r15d, r15d
	test	rdx, rdx
	jne	.L256
.L132:
	mov	eax, DWORD PTR 32[rsi]
	movq	xmm6, r13
	test	rbx, rbx
	mov	DWORD PTR 0[r13+rbx], eax
	lea	rax, 4[r13+rbx]
	movq	xmm5, rax
	punpcklqdq	xmm6, xmm5
	jg	.L257
	test	r14, r14
	jne	.L134
.L135:
	add	r13, r15
	movaps	XMMWORD PTR 160[rsp], xmm6
	mov	QWORD PTR 176[rsp], r13
	jmp	.L126
	.p2align 4,,10
	.p2align 3
.L101:
	mov	r14, QWORD PTR 128[rsp]
	movabs	rcx, 2305843009213693951
	sub	r12, r14
	mov	rax, r12
	sar	rax, 2
	cmp	rax, rcx
	je	.L258
	cmp	r14, r13
	je	.L259
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L197
	xor	ecx, ecx
	xor	r15d, r15d
	test	rdx, rdx
	mov	QWORD PTR 32[rsp], rcx
	jne	.L260
.L108:
	mov	eax, DWORD PTR [rbx]
	movq	xmm6, r15
	test	r12, r12
	mov	DWORD PTR [r15+r12], eax
	lea	rax, 4[r15+r12]
	movq	xmm4, rax
	punpcklqdq	xmm6, xmm4
	jg	.L261
	test	r14, r14
	jne	.L110
.L111:
	mov	r9, QWORD PTR 32[rsp]
	movaps	XMMWORD PTR 128[rsp], xmm6
	add	r9, r15
	mov	QWORD PTR 144[rsp], r9
	jmp	.L102
	.p2align 4,,10
	.p2align 3
.L250:
	mov	rdx, r10
	mov	DWORD PTR [rdx], r9d
	jmp	.L262
	.p2align 4,,10
	.p2align 3
.L124:
	mov	rbp, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC3[rip]
	mov	rcx, rbp
.LEHB5:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	r13, QWORD PTR 128[rsp]
	mov	rcx, rax
	mov	rsi, QWORD PTR 136[rsp]
	sub	rsi, r13
	mov	r14, rsi
	sar	r14, 2
	mov	rdx, r14
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC4[rip]
	mov	rcx, rbp
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	r12, QWORD PTR 160[rsp]
	mov	rcx, rax
	mov	rbx, QWORD PTR 168[rsp]
	sub	rbx, r12
	mov	rdx, rbx
	sar	rdx, 2
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	cmp	rsi, rbx
	jne	.L137
	lea	rax, _ZNKSt5ctypeIcE8do_widenEc[rip]
	xor	ebx, ebx
	test	rsi, rsi
	lea	r15, .LC9[rip]
	mov	QWORD PTR 32[rsp], rax
	jne	.L138
	jmp	.L144
	.p2align 4,,10
	.p2align 3
.L265:
	movsx	edx, BYTE PTR 67[rdi]
.L142:
	mov	rcx, rsi
	call	_ZNSo3putEc
	mov	rcx, rax
	call	_ZNSo5flushEv
	mov	eax, DWORD PTR [r12+rbx*4]
	cmp	DWORD PTR 0[r13+rbx*4], eax
	jne	.L263
	add	rbx, 1
	cmp	rbx, r14
	jnb	.L144
.L138:
	lea	rdx, .LC7[rip]
	mov	r8d, 2
	mov	rcx, rbp
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	rdx, rbx
	mov	rcx, rbp
	call	_ZNSo9_M_insertIyEERSoT_
	mov	r8d, 4
	mov	rcx, rax
	mov	rsi, rax
	lea	rdx, .LC8[rip]
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	edx, DWORD PTR 0[r13+rbx*4]
	mov	rcx, rsi
	call	_ZNSolsEi
	mov	r8d, 4
	mov	rdx, r15
	mov	rcx, rax
	mov	rsi, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	mov	edx, DWORD PTR [r12+rbx*4]
	mov	rcx, rsi
	call	_ZNSolsEi
	mov	rsi, rax
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR -24[rax]
	mov	rdi, QWORD PTR 240[rsi+rax]
	test	rdi, rdi
	je	.L264
	cmp	BYTE PTR 56[rdi], 0
	jne	.L265
	mov	rcx, rdi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rdi]
	mov	edx, 10
	mov	rcx, QWORD PTR 32[rsp]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L142
	mov	rcx, rdi
	call	rax
.LEHE5:
	movsx	edx, al
	jmp	.L142
	.p2align 4,,10
	.p2align 3
.L144:
	mov	ecx, 64
	pxor	xmm0, xmm0
	mov	QWORD PTR 208[rsp], 0
	movaps	XMMWORD PTR 192[rsp], xmm0
	movaps	XMMWORD PTR 320[rsp], xmm0
	movaps	XMMWORD PTR 336[rsp], xmm0
	movaps	XMMWORD PTR 352[rsp], xmm0
	movaps	XMMWORD PTR 368[rsp], xmm0
	mov	QWORD PTR 312[rsp], 8
.LEHB6:
	call	_Znwy
.LEHE6:
	mov	ecx, 512
	mov	rdi, rax
	mov	QWORD PTR 304[rsp], rax
	lea	rbx, 24[rax]
.LEHB7:
	call	_Znwy
.LEHE7:
	movq	xmm1, rax
	mov	r14, rax
	mov	QWORD PTR 24[rdi], rax
	xor	r13d, r13d
	lea	rax, 512[rax]
	movq	xmm5, rbx
	xor	ebx, ebx
	punpcklqdq	xmm1, xmm1
	movq	xmm0, rax
	mov	rax, QWORD PTR .LC11[rip]
	cmp	rbx, r13
	mov	DWORD PTR 88[rsp], 3
	lea	rsi, 80[rsp]
	punpcklqdq	xmm0, xmm5
	movaps	XMMWORD PTR 320[rsp], xmm1
	movaps	XMMWORD PTR 336[rsp], xmm0
	lea	r15, 92[rsp]
	movaps	XMMWORD PTR 352[rsp], xmm1
	mov	QWORD PTR 80[rsp], rax
	mov	r12d, DWORD PTR [rsi]
	movaps	XMMWORD PTR 368[rsp], xmm0
	je	.L150
.L267:
	mov	DWORD PTR [rbx], r12d
	add	rbx, 4
	mov	QWORD PTR 200[rsp], rbx
.L151:
	mov	rax, QWORD PTR 368[rsp]
	mov	rbx, QWORD PTR 352[rsp]
	sub	rax, 4
	cmp	rbx, rax
	je	.L159
	mov	DWORD PTR [rbx], r12d
	add	rbx, 4
	mov	QWORD PTR 352[rsp], rbx
.L160:
	add	rsi, 4
	cmp	r15, rsi
	je	.L266
	mov	rbx, QWORD PTR 200[rsp]
	mov	r13, QWORD PTR 208[rsp]
	mov	r12d, DWORD PTR [rsi]
	cmp	rbx, r13
	jne	.L267
.L150:
	mov	rax, QWORD PTR 192[rsp]
	movabs	rcx, 2305843009213693951
	sub	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	mov	rax, rbx
	sar	rax, 2
	cmp	rax, rcx
	je	.L268
	cmp	QWORD PTR 32[rsp], r13
	je	.L153
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L209
	xor	eax, eax
	xor	r9d, r9d
	test	rdx, rdx
	mov	QWORD PTR 40[rsp], rax
	jne	.L193
.L155:
	lea	rax, 4[r9+rbx]
	movq	xmm6, r9
	test	rbx, rbx
	mov	DWORD PTR [r9+rbx], r12d
	movq	xmm4, rax
	punpcklqdq	xmm6, xmm4
	jg	.L269
	cmp	QWORD PTR 32[rsp], 0
	jne	.L157
.L158:
	mov	rax, QWORD PTR 40[rsp]
	movaps	XMMWORD PTR 192[rsp], xmm6
	add	r9, rax
	mov	QWORD PTR 208[rsp], r9
	jmp	.L151
.L266:
	lea	rdx, .LC13[rip]
	mov	rcx, rbp
.LEHB8:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	r13, QWORD PTR 200[rsp]
	mov	rcx, rax
	mov	edx, DWORD PTR -4[r13]
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC14[rip]
	mov	rcx, rbp
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rsi, 304[rsp]
	mov	rbx, rax
	mov	rcx, rsi
	call	_ZNSt5dequeIiSaIiEE4backEv
	mov	rcx, rbx
	mov	edx, DWORD PTR [rax]
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, rsi
	mov	ebx, DWORD PTR -4[r13]
	call	_ZNSt5dequeIiSaIiEE4backEv
	cmp	ebx, DWORD PTR [rax]
	jne	.L175
	mov	r12, QWORD PTR 192[rsp]
	lea	rbx, -4[r13]
	cmp	r13, r12
	jne	.L181
	jmp	.L182
	.p2align 4,,10
	.p2align 3
.L179:
	cmp	eax, DWORD PTR -4[rcx]
	jne	.L190
	sub	rcx, 4
	mov	QWORD PTR 200[rsp], rbx
	sub	rbx, 4
	cmp	r12, rbp
	mov	QWORD PTR 352[rsp], rcx
	je	.L182
.L181:
	mov	rcx, QWORD PTR 352[rsp]
	mov	rbp, rbx
	cmp	rcx, QWORD PTR 360[rsp]
	mov	eax, DWORD PTR [rbx]
	mov	r13, QWORD PTR 376[rsp]
	jne	.L179
	mov	rdx, QWORD PTR -8[r13]
	cmp	eax, DWORD PTR 508[rdx]
	jne	.L190
	mov	edx, 512
	mov	QWORD PTR 200[rsp], rbx
	sub	r13, 8
	sub	rbx, 4
	call	_ZdlPvy
	mov	rax, QWORD PTR 0[r13]
	movq	xmm3, r13
	lea	rcx, 508[rax]
	movq	xmm2, rax
	add	rax, 512
	movq	xmm0, rcx
	cmp	r12, rbp
	punpcklqdq	xmm0, xmm2
	movaps	XMMWORD PTR 352[rsp], xmm0
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm3
	movaps	XMMWORD PTR 368[rsp], xmm0
	jne	.L181
.L182:
	test	rdi, rdi
	je	.L178
	mov	rcx, rsi
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0
.L178:
	lea	rcx, 192[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	lea	rcx, 160[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, QWORD PTR 272[rsp]
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
	lea	rcx, 128[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	lea	rcx, 224[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	lea	rcx, 96[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	nop
	movaps	xmm6, XMMWORD PTR 384[rsp]
	xor	eax, eax
	add	rsp, 408
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L190:
	lea	rdx, .LC5[rip]
	mov	r8d, 42
	lea	rcx, .LC15[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE8:
.L261:
	mov	r8, r12
	mov	rdx, r14
	mov	rcx, r15
	call	memmove
.L110:
	mov	rdx, r13
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
	jmp	.L111
.L203:
	movabs	rdx, 2305843009213693951
.L131:
	lea	r15, 0[0+rdx*4]
	mov	rcx, r15
.LEHB9:
	call	_Znwy
.LEHE9:
	mov	r13, rax
	jmp	.L132
.L257:
	mov	r8, rbx
	mov	rdx, r14
	mov	rcx, r13
	call	memmove
.L134:
	mov	rdx, r12
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
	jmp	.L135
.L259:
	movabs	rdx, 2305843009213693951
	add	rax, 1
	jc	.L107
	cmp	rax, rdx
	cmovbe	rdx, rax
.L107:
	lea	rax, 0[0+rdx*4]
	mov	rcx, rax
	mov	QWORD PTR 32[rsp], rax
.LEHB10:
	call	_Znwy
.LEHE10:
	mov	r15, rax
	jmp	.L108
.L249:
	lea	rcx, [rax+rax]
	lea	rax, 1[rcx]
	sar	rcx
	mov	r8d, DWORD PTR [rbx+rax*4]
	mov	DWORD PTR [rdx], r8d
	mov	rdx, rax
	jmp	.L121
.L255:
	movabs	rdx, 2305843009213693951
	add	rax, 1
	jc	.L131
	cmp	rax, rdx
	cmovbe	rdx, rax
	jmp	.L131
.L159:
	mov	r13, QWORD PTR 376[rsp]
	mov	rdx, rbx
	mov	rcx, QWORD PTR 344[rsp]
	mov	rax, r13
	sub	rax, rcx
	mov	QWORD PTR 32[rsp], rcx
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
	sar	rcx, 3
	cmp	r13, 1
	mov	rax, rcx
	adc	rax, -1
	sub	rdx, QWORD PTR 360[rsp]
	sal	rax, 7
	sar	rdx, 2
	add	rax, rdx
	mov	rdx, QWORD PTR 336[rsp]
	sub	rdx, r14
	sar	rdx, 2
	add	rax, rdx
	movabs	rdx, 4611686018427387903
	cmp	rax, rdx
	je	.L270
	mov	rdx, QWORD PTR 312[rsp]
	mov	rax, r13
	sub	rax, rdi
	sar	rax, 3
	mov	QWORD PTR 40[rsp], rdx
	sub	rdx, rax
	cmp	rdx, 1
	jbe	.L271
.L162:
	mov	ecx, 512
	mov	rdi, QWORD PTR 376[rsp]
.LEHB11:
	call	_Znwy
	mov	QWORD PTR 8[rdi], rax
	movq	xmm4, rax
	add	rdi, 8
	add	rax, 512
	movq	xmm1, rdi
	movddup	xmm0, xmm4
	mov	DWORD PTR [rbx], r12d
	mov	rdi, QWORD PTR 304[rsp]
	movaps	XMMWORD PTR 352[rsp], xmm0
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm1
	movaps	XMMWORD PTR 368[rsp], xmm0
	jmp	.L160
.L197:
	movabs	rdx, 2305843009213693951
	jmp	.L107
.L113:
	test	r11, r11
	mov	rdx, rbx
	jne	.L118
	xor	eax, eax
	jmp	.L117
.L269:
	mov	rdx, QWORD PTR 32[rsp]
	mov	rcx, r9
	mov	r8, rbx
	call	memmove
	mov	r9, rax
.L157:
	mov	rcx, QWORD PTR 32[rsp]
	mov	rdx, r13
	mov	QWORD PTR 48[rsp], r9
	sub	rdx, rcx
	call	_ZdlPvy
	mov	r9, QWORD PTR 48[rsp]
	jmp	.L158
.L153:
	add	rax, 1
	mov	rdx, rax
	jnc	.L193
.L209:
	mov	rdx, rcx
.L154:
	lea	rax, 0[0+rdx*4]
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
	call	_Znwy
	mov	r9, rax
	jmp	.L155
.L271:
	mov	rdx, QWORD PTR 40[rsp]
	add	rcx, 2
	lea	rax, [rcx+rcx]
	mov	QWORD PTR 64[rsp], rcx
	cmp	rax, rdx
	jnb	.L163
	lea	r8, 8[r13]
	mov	rax, rdx
	mov	rdx, QWORD PTR 32[rsp]
	sub	rax, rcx
	shr	rax
	lea	r9, [rdi+rax*8]
	sub	r8, rdx
	cmp	r9, rdx
	jnb	.L164
	cmp	r8, 8
	jle	.L165
	mov	rcx, r9
	call	memmove
	mov	r9, rax
	jmp	.L169
.L163:
	mov	rcx, QWORD PTR 40[rsp]
	mov	eax, 1
	test	rcx, rcx
	cmovne	rax, rcx
	lea	rax, 2[rcx+rax]
	mov	rcx, rax
	mov	QWORD PTR 56[rsp], rax
	movabs	rax, 1152921504606846975
	cmp	rax, rcx
	jb	.L272
	mov	rax, QWORD PTR 56[rsp]
	lea	rcx, 0[0+rax*8]
	call	_Znwy
	mov	rdx, QWORD PTR 64[rsp]
	mov	QWORD PTR 72[rsp], rax
	lea	r8, 8[r13]
	mov	rcx, rax
	mov	rax, QWORD PTR 56[rsp]
	sub	rax, rdx
	mov	rdx, QWORD PTR 32[rsp]
	shr	rax
	lea	r9, [rcx+rax*8]
	sub	r8, rdx
	cmp	r8, 8
	jle	.L172
	mov	rcx, r9
	call	memmove
	mov	r9, rax
.L173:
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rdi
	mov	QWORD PTR 32[rsp], r9
	sal	rdx, 3
	call	_ZdlPvy
	mov	rax, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 32[rsp]
	mov	QWORD PTR 304[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 312[rsp], rax
.L169:
	mov	rax, QWORD PTR [r9]
	mov	QWORD PTR 344[rsp], r9
	lea	rdx, 512[rax]
	movq	xmm0, rax
	mov	rax, QWORD PTR 48[rsp]
	movq	xmm4, rdx
	punpcklqdq	xmm0, xmm4
	movups	XMMWORD PTR 328[rsp], xmm0
	add	r9, rax
	mov	rax, QWORD PTR [r9]
	mov	QWORD PTR 376[rsp], r9
	lea	rdx, 512[rax]
	movq	xmm0, rax
	movq	xmm5, rdx
	punpcklqdq	xmm0, xmm5
	movups	XMMWORD PTR 360[rsp], xmm0
	jmp	.L162
.L164:
	mov	rax, QWORD PTR 48[rsp]
	cmp	r8, 8
	lea	rax, 8[r9+rax]
	jle	.L167
	mov	rdx, QWORD PTR 32[rsp]
	sub	rax, r8
	mov	QWORD PTR 40[rsp], r9
	mov	rcx, rax
	call	memmove
	mov	r9, QWORD PTR 40[rsp]
	jmp	.L169
.L193:
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	jmp	.L154
.L260:
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	jmp	.L107
.L172:
	jne	.L173
	mov	rax, QWORD PTR 32[rsp]
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR [r9], rax
	jmp	.L173
.L256:
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	jmp	.L131
.L165:
	jne	.L169
	mov	rax, QWORD PTR 32[rsp]
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR [r9], rax
	jmp	.L169
.L272:
	movabs	rax, 2305843009213693951
	cmp	rax, rcx
	jnb	.L171
	call	_ZSt28__throw_bad_array_new_lengthv
.L167:
	jne	.L169
	mov	rdi, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR [rdi]
	mov	QWORD PTR -8[rax], rdx
	jmp	.L169
.L171:
	call	_ZSt17__throw_bad_allocv
.LEHE11:
.L263:
	lea	rdx, .LC5[rip]
	mov	r8d, 32
	lea	rcx, .LC10[rip]
.LEHB12:
	call	[QWORD PTR __imp__assert[rip]]
.L264:
	call	_ZSt16__throw_bad_castv
.L137:
	lea	rdx, .LC5[rip]
	mov	r8d, 28
	lea	rcx, .LC6[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE12:
.L258:
	lea	rcx, .LC2[rip]
.LEHB13:
	call	_ZSt20__throw_length_errorPKc
.LEHE13:
.L268:
	lea	rcx, .LC2[rip]
.LEHB14:
	call	_ZSt20__throw_length_errorPKc
.L270:
	lea	rcx, .LC12[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE14:
.L254:
	lea	rcx, .LC2[rip]
.LEHB15:
	call	_ZSt20__throw_length_errorPKc
.LEHE15:
.L175:
	lea	rdx, .LC5[rip]
	mov	r8d, 41
	lea	rcx, .LC15[rip]
.LEHB16:
	call	[QWORD PTR __imp__assert[rip]]
.LEHE16:
.L210:
	mov	rbx, rax
.L187:
	lea	rcx, 96[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rbx
.LEHB17:
	call	_Unwind_Resume
.LEHE17:
.L214:
	cmp	QWORD PTR 304[rsp], 0
	mov	rbx, rax
	jne	.L273
.L149:
	lea	rcx, 192[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
.L185:
	lea	rcx, 160[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, QWORD PTR 272[rsp]
	call	_ZNSt8_Rb_treeIiiSt9_IdentityIiESt4lessIiESaIiEE8_M_eraseEPSt13_Rb_tree_nodeIiE.isra.0
.L186:
	lea	rcx, 128[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	lea	rcx, 224[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	jmp	.L187
.L273:
	lea	rcx, 304[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0
	jmp	.L149
.L212:
	mov	rbx, rax
	jmp	.L185
.L211:
	mov	rbx, rax
	jmp	.L186
.L216:
	mov	rcx, rax
	call	__cxa_begin_catch
.LEHB18:
	call	__cxa_rethrow
.LEHE18:
.L213:
	mov	rbx, rax
	jmp	.L149
.L217:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
	call	__cxa_begin_catch
	mov	edx, 64
	mov	rcx, rdi
	call	_ZdlPvy
.LEHB19:
	call	__cxa_rethrow
.LEHE19:
.L215:
	mov	rbx, rax
	call	__cxa_end_catch
	jmp	.L149
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA3589:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT3589-.LLSDATTD3589
.LLSDATTD3589:
	.byte	0x1
	.uleb128 .LLSDACSE3589-.LLSDACSB3589
.LLSDACSB3589:
	.uleb128 .LEHB2-.LFB3589
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB3589
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L210-.LFB3589
	.uleb128 0
	.uleb128 .LEHB4-.LFB3589
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L211-.LFB3589
	.uleb128 0
	.uleb128 .LEHB5-.LFB3589
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L212-.LFB3589
	.uleb128 0
	.uleb128 .LEHB6-.LFB3589
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L213-.LFB3589
	.uleb128 0
	.uleb128 .LEHB7-.LFB3589
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L216-.LFB3589
	.uleb128 0x1
	.uleb128 .LEHB8-.LFB3589
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L214-.LFB3589
	.uleb128 0
	.uleb128 .LEHB9-.LFB3589
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L212-.LFB3589
	.uleb128 0
	.uleb128 .LEHB10-.LFB3589
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L211-.LFB3589
	.uleb128 0
	.uleb128 .LEHB11-.LFB3589
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L214-.LFB3589
	.uleb128 0
	.uleb128 .LEHB12-.LFB3589
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L212-.LFB3589
	.uleb128 0
	.uleb128 .LEHB13-.LFB3589
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L211-.LFB3589
	.uleb128 0
	.uleb128 .LEHB14-.LFB3589
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L214-.LFB3589
	.uleb128 0
	.uleb128 .LEHB15-.LFB3589
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L212-.LFB3589
	.uleb128 0
	.uleb128 .LEHB16-.LFB3589
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L214-.LFB3589
	.uleb128 0
	.uleb128 .LEHB17-.LFB3589
	.uleb128 .LEHE17-.LEHB17
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB18-.LFB3589
	.uleb128 .LEHE18-.LEHB18
	.uleb128 .L217-.LFB3589
	.uleb128 0x1
	.uleb128 .LEHB19-.LFB3589
	.uleb128 .LEHE19-.LEHB19
	.uleb128 .L215-.LFB3589
	.uleb128 0
.LLSDACSE3589:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT3589:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	5
	.long	3
	.long	8
	.long	1
	.align 8
.LC1:
	.long	9
	.long	2
	.align 8
.LC11:
	.long	1
	.long	2
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt29_Rb_tree_insert_and_rebalancebPSt18_Rb_tree_node_baseS0_RS_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt28_Rb_tree_rebalance_for_erasePSt18_Rb_tree_node_baseRS_;	.scl	2;	.type	32;	.endef
	.def	_ZSt18_Rb_tree_decrementPKSt18_Rb_tree_node_base;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
