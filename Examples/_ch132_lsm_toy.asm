	.file	"_ch132_lsm_toy.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z17skiplist_containsPK4Nodeii
	.def	_Z17skiplist_containsPK4Nodeii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17skiplist_containsPK4Nodeii
_Z17skiplist_containsPK4Nodeii:
.LFB5059:
	.seh_endprologue
	mov	rcx, QWORD PTR 8[rcx]
	test	edx, edx
	js	.L2
	movsx	rdx, edx
	xor	r9d, r9d
	sal	rdx, 3
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L14:
	cmp	DWORD PTR [rax], r8d
	jge	.L3
	mov	rcx, QWORD PTR 8[rax]
.L4:
	mov	rax, QWORD PTR [rcx+rdx]
	test	rax, rax
	jne	.L14
.L3:
	lea	rax, -8[rdx]
	cmp	r9, rdx
	je	.L2
	mov	rdx, rax
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L2:
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L9
	cmp	DWORD PTR [rax], r8d
	jne	.L9
	mov	eax, DWORD PTR 4[rax]
	ret
.L9:
	mov	eax, -1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8run_findRK3Runi
	.def	_Z8run_findRK3Runi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8run_findRK3Runi
_Z8run_findRK3Runi:
.LFB5060:
	.seh_endprologue
	mov	r9d, DWORD PTR 16[rcx]
	sub	r9d, 1
	js	.L21
	mov	r11, QWORD PTR [rcx]
	xor	r8d, r8d
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L24:
	lea	r8d, 1[rax]
	cmp	r9d, r8d
	jl	.L21
.L20:
	mov	eax, r9d
	sub	eax, r8d
	sar	eax
	add	eax, r8d
	movsx	r10, eax
	cmp	DWORD PTR [r11+r10*4], edx
	je	.L23
	jl	.L24
	lea	r9d, -1[rax]
	cmp	r9d, r8d
	jge	.L20
.L21:
	mov	eax, -1
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	mov	rax, QWORD PTR 8[rcx]
	mov	eax, DWORD PTR [rax+r10*4]
	ret
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIiSaIiEED2Ev
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev
_ZNSt12_Vector_baseIiSaIiEED2Ev:
.LFB5492:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L25
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L25:
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
.LC1:
	.ascii "vector::_M_realloc_insert\0"
	.text
	.p2align 4
	.globl	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_
	.def	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_
_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_:
.LFB5061:
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
	sub	rsp, 120
	.seh_stackalloc	120
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r12, rdx
	mov	rdx, QWORD PTR 8[rcx]
	mov	r14, rcx
	mov	r13, r8
	movabs	r8, -6148914691236517205
	mov	rcx, rdx
	sub	rcx, rax
	mov	r9, rcx
	sar	r9, 3
	imul	r9, r8
	test	rcx, rcx
	mov	QWORD PTR 40[rsp], r9
	js	.L84
	cmp	QWORD PTR 40[rsp], 0
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 72[rsp], xmm0
	je	.L85
	sal	QWORD PTR 40[rsp], 2
	mov	rdi, QWORD PTR 40[rsp]
	mov	rcx, rdi
.LEHB0:
	call	_Znwy
.LEHE0:
	xor	edx, edx
	mov	r8, rdi
	lea	rbx, [rax+rdi]
	mov	rcx, rax
	mov	rsi, rax
	mov	QWORD PTR 64[rsp], rax
	mov	QWORD PTR 80[rsp], rbx
	call	memset
	mov	rdx, QWORD PTR 8[r14]
	mov	rax, QWORD PTR [r14]
.L30:
	movabs	r15, -6148914691236517205
	mov	QWORD PTR 72[rsp], rbx
	.p2align 4,,10
	.p2align 3
.L58:
	mov	r8, rdx
	sub	r8, rax
	sar	r8, 3
	imul	r8, r15
	cmp	rax, rdx
	je	.L31
	xor	ebp, ebp
	mov	ebx, -1
	xor	edx, edx
	mov	rdi, -1
	.p2align 4,,10
	.p2align 3
.L34:
	movsx	rcx, DWORD PTR [rsi+rdx*4]
	cmp	ecx, DWORD PTR 16[rax]
	jge	.L32
	mov	r9, QWORD PTR [rax]
	mov	r9d, DWORD PTR [r9+rcx*4]
	cmp	r9d, ebx
	jl	.L68
	cmp	ebx, -1
	jne	.L32
.L68:
	mov	r10, QWORD PTR 8[rax]
	movsx	rdi, edx
	mov	ebx, r9d
	mov	ebp, DWORD PTR [r10+rcx*4]
.L32:
	add	rdx, 1
	add	rax, 24
	cmp	rdx, r8
	jb	.L34
	cmp	edi, -1
	je	.L35
	mov	rax, QWORD PTR 8[r12]
	cmp	rax, QWORD PTR 16[r12]
	je	.L36
	mov	DWORD PTR [rax], ebx
	add	rax, 4
	mov	QWORD PTR 8[r12], rax
	mov	rax, QWORD PTR 8[r13]
	cmp	rax, QWORD PTR 16[r13]
	je	.L47
.L91:
	mov	DWORD PTR [rax], ebp
	add	rax, 4
	mov	QWORD PTR 8[r13], rax
.L48:
	add	DWORD PTR [rsi+rdi*4], 1
	mov	rdx, QWORD PTR 8[r14]
	mov	rax, QWORD PTR [r14]
	jmp	.L58
	.p2align 4,,10
	.p2align 3
.L36:
	mov	rcx, QWORD PTR [r12]
	mov	rdx, rax
	sub	rdx, rcx
	mov	QWORD PTR 32[rsp], rcx
	movabs	rcx, 2305843009213693951
	mov	QWORD PTR 56[rsp], rdx
	sar	rdx, 2
	cmp	rdx, rcx
	je	.L86
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rax, rcx
	je	.L87
	lea	rax, [rdx+rdx]
	cmp	rax, rdx
	jb	.L62
	mov	QWORD PTR 48[rsp], 0
	xor	ecx, ecx
	test	rax, rax
	jne	.L88
.L43:
	mov	rax, QWORD PTR 56[rsp]
	movq	xmm6, rcx
	mov	DWORD PTR [rcx+rax], ebx
	mov	rbx, rax
	lea	rax, 4[rcx+rax]
	test	rbx, rbx
	movq	xmm1, rax
	punpcklqdq	xmm6, xmm1
	jg	.L89
	cmp	QWORD PTR 32[rsp], 0
	jne	.L90
.L46:
	mov	rax, QWORD PTR 48[rsp]
	movups	XMMWORD PTR [r12], xmm6
	mov	QWORD PTR 16[r12], rax
	mov	rax, QWORD PTR 8[r13]
	cmp	rax, QWORD PTR 16[r13]
	jne	.L91
	.p2align 4,,10
	.p2align 3
.L47:
	mov	rbx, QWORD PTR 0[r13]
	mov	rcx, rax
	sub	rcx, rbx
	mov	rdx, rcx
	mov	QWORD PTR 48[rsp], rcx
	movabs	rcx, 2305843009213693951
	sar	rdx, 2
	cmp	rdx, rcx
	je	.L92
	cmp	rax, rbx
	je	.L93
	lea	rax, [rdx+rdx]
	cmp	rax, rdx
	jb	.L65
	mov	QWORD PTR 32[rsp], 0
	xor	ecx, ecx
	test	rax, rax
	jne	.L94
.L54:
	mov	rdx, QWORD PTR 48[rsp]
	movq	xmm6, rcx
	lea	rax, 4[rcx+rdx]
	test	rdx, rdx
	mov	DWORD PTR [rcx+rdx], ebp
	movq	xmm2, rax
	punpcklqdq	xmm6, xmm2
	jg	.L95
	test	rbx, rbx
	jne	.L96
.L57:
	mov	rax, QWORD PTR 32[rsp]
	movups	XMMWORD PTR 0[r13], xmm6
	mov	QWORD PTR 16[r13], rax
	jmp	.L48
	.p2align 4,,10
	.p2align 3
.L31:
	test	rsi, rsi
	jne	.L35
	movaps	xmm6, XMMWORD PTR 96[rsp]
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L62:
	movabs	rax, 9223372036854775804
	mov	QWORD PTR 48[rsp], rax
.L42:
	mov	rcx, QWORD PTR 48[rsp]
.LEHB1:
	call	_Znwy
	mov	rcx, rax
	mov	rax, QWORD PTR 48[rsp]
	add	rax, rcx
	mov	QWORD PTR 48[rsp], rax
	jmp	.L43
.L65:
	movabs	rax, 9223372036854775804
	mov	QWORD PTR 32[rsp], rax
.L53:
	mov	rcx, QWORD PTR 32[rsp]
	call	_Znwy
	mov	rcx, rax
	mov	rax, QWORD PTR 32[rsp]
	add	rax, rcx
	mov	QWORD PTR 32[rsp], rax
	jmp	.L54
.L35:
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rsi
	movaps	xmm6, XMMWORD PTR 96[rsp]
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	jmp	_ZdlPvy
.L89:
	mov	r8, rbx
	mov	rbx, QWORD PTR 32[rsp]
	mov	rdx, rbx
	call	memmove
	mov	rax, QWORD PTR 16[r12]
	sub	rax, rbx
	mov	rdx, rax
.L45:
	mov	rcx, QWORD PTR 32[rsp]
	call	_ZdlPvy
	jmp	.L46
.L85:
	mov	QWORD PTR 64[rsp], 0
	xor	esi, esi
	xor	ebx, ebx
	mov	QWORD PTR 80[rsp], 0
	jmp	.L30
.L95:
	mov	r8, rdx
	mov	rdx, rbx
	call	memmove
	mov	rdx, QWORD PTR 16[r13]
	sub	rdx, rbx
.L56:
	mov	rcx, rbx
	call	_ZdlPvy
	jmp	.L57
.L87:
	add	rdx, 1
	jc	.L62
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	lea	rax, 0[0+rdx*4]
	mov	QWORD PTR 48[rsp], rax
	jmp	.L42
.L93:
	add	rdx, 1
	jc	.L65
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	lea	rax, 0[0+rdx*4]
	mov	QWORD PTR 32[rsp], rax
	jmp	.L53
.L90:
	mov	rdx, QWORD PTR 16[r12]
	mov	rax, QWORD PTR 32[rsp]
	sub	rdx, rax
	jmp	.L45
.L96:
	mov	rdx, QWORD PTR 16[r13]
	sub	rdx, rbx
	jmp	.L56
.L88:
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	sal	rax, 2
	mov	QWORD PTR 48[rsp], rax
	jmp	.L42
.L94:
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	sal	rax, 2
	mov	QWORD PTR 32[rsp], rax
	jmp	.L53
.L86:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.L92:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE1:
.L84:
	lea	rcx, .LC0[rip]
.LEHB2:
	call	_ZSt20__throw_length_errorPKc
.L67:
	lea	rcx, 64[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5061:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5061-.LLSDACSB5061
.LLSDACSB5061:
	.uleb128 .LEHB0-.LFB5061
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5061
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L67-.LFB5061
	.uleb128 0
	.uleb128 .LEHB2-.LFB5061
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE5061:
	.text
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	.def	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv:
.LFB5691:
	sub	rsp, 40
	.seh_stackalloc	40
	movaps	XMMWORD PTR [rsp], xmm6
	.seh_savexmm	xmm6, 0
	movaps	XMMWORD PTR 16[rsp], xmm7
	.seh_savexmm	xmm7, 16
	.seh_endprologue
	mov	r8d, DWORD PTR [rcx]
	lea	r9, 908[rcx]
	mov	r10, rcx
	.p2align 4,,10
	.p2align 3
.L98:
	mov	edx, r8d
	mov	r8d, DWORD PTR 4[rcx]
	add	rcx, 4
	and	edx, -2147483648
	mov	eax, r8d
	and	eax, 2147483647
	or	edx, eax
	and	eax, 1
	shr	edx
	xor	edx, DWORD PTR 1584[rcx]
	neg	eax
	and	eax, -1727483681
	xor	eax, edx
	mov	DWORD PTR -4[rcx], eax
	cmp	rcx, r9
	jne	.L98
	movdqa	xmm7, XMMWORD PTR .LC2[rip]
	lea	rax, 2492[r10]
	pxor	xmm3, xmm3
	movdqa	xmm6, XMMWORD PTR .LC3[rip]
	movdqa	xmm5, XMMWORD PTR .LC4[rip]
	movdqa	xmm4, XMMWORD PTR .LC5[rip]
	.p2align 4,,10
	.p2align 3
.L99:
	movdqu	xmm0, XMMWORD PTR [rcx]
	add	rcx, 16
	movdqu	xmm1, XMMWORD PTR -12[rcx]
	movdqu	xmm2, XMMWORD PTR -924[rcx]
	pand	xmm0, xmm7
	pand	xmm1, xmm6
	por	xmm0, xmm1
	movdqa	xmm1, xmm0
	pand	xmm0, xmm5
	psrld	xmm1, 1
	pxor	xmm1, xmm2
	movdqa	xmm2, xmm3
	psubd	xmm2, xmm0
	pand	xmm2, xmm4
	movdqa	xmm0, xmm2
	pxor	xmm0, xmm1
	movups	XMMWORD PTR -16[rcx], xmm0
	cmp	rcx, rax
	jne	.L99
	mov	eax, DWORD PTR 2492[r10]
	mov	QWORD PTR 2496[r10], 0
	mov	edx, DWORD PTR [r10]
	movaps	xmm6, XMMWORD PTR [rsp]
	movaps	xmm7, XMMWORD PTR 16[rsp]
	and	eax, -2147483648
	and	edx, 2147483647
	or	eax, edx
	mov	edx, eax
	and	eax, 1
	shr	edx
	xor	edx, DWORD PTR 1584[r10]
	neg	eax
	and	eax, -1727483681
	xor	eax, edx
	mov	DWORD PTR 2492[r10], eax
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv
	.def	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv
_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv:
.LFB5496:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 2496[rcx]
	cmp	rax, 623
	mov	r11, rcx
	ja	.L104
.L103:
	lea	rdx, 1[rax]
	mov	eax, DWORD PTR [r11+rax*4]
	mov	QWORD PTR 2496[r11], rdx
	mov	edx, eax
	shr	edx, 11
	xor	edx, eax
	mov	eax, edx
	sal	eax, 7
	and	eax, -1658038656
	xor	eax, edx
	mov	edx, eax
	sal	edx, 15
	and	edx, -272236544
	xor	edx, eax
	mov	eax, edx
	shr	eax, 18
	xor	eax, edx
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L104:
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	mov	rax, QWORD PTR 2496[r11]
	jmp	.L103
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev
	.def	_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev
_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev:
.LFB5702:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L105
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L105:
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z4demoi
	.def	_Z4demoi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4demoi
_Z4demoi:
.LFB5062:
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
	sub	rsp, 2856
	.seh_stackalloc	2856
	movaps	XMMWORD PTR 2816[rsp], xmm6
	.seh_savexmm	xmm6, 2816
	movaps	XMMWORD PTR 2832[rsp], xmm7
	.seh_savexmm	xmm7, 2832
	.seh_endprologue
	mov	edx, 1
	mov	DWORD PTR 304[rsp], ecx
	lea	rbx, 304[rsp]
	.p2align 4,,10
	.p2align 3
.L108:
	mov	eax, ecx
	shr	eax, 30
	xor	eax, ecx
	imul	eax, eax, 1812433253
	lea	ecx, [rax+rdx]
	mov	DWORD PTR [rbx+rdx*4], ecx
	add	rdx, 1
	cmp	rdx, 624
	jne	.L108
	mov	ecx, 32
	mov	QWORD PTR 2800[rsp], 624
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	ecx, 32
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 72[rsp], xmm0
	lea	rdx, 32[rax]
	mov	rsi, rax
	mov	DWORD PTR [rax], 0
	mov	QWORD PTR 32[rsp], rax
	lea	rax, 4[rax]
	mov	QWORD PTR 4[rsi], 0
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	DWORD PTR 24[rax], 0
	mov	QWORD PTR 48[rsp], rdx
	mov	QWORD PTR 40[rsp], rdx
.LEHB4:
	call	_Znwy
.LEHE4:
	lea	rdx, 32[rax]
	mov	rdi, rax
	mov	DWORD PTR [rax], 0
	mov	ecx, 32
	mov	QWORD PTR 64[rsp], rax
	lea	rax, 4[rax]
	pxor	xmm0, xmm0
	mov	QWORD PTR 4[rdi], 0
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	DWORD PTR 24[rax], 0
	mov	QWORD PTR 80[rsp], rdx
	mov	QWORD PTR 72[rsp], rdx
	movups	XMMWORD PTR 104[rsp], xmm0
.LEHB5:
	call	_Znwy
.LEHE5:
	lea	rdx, 32[rax]
	mov	rbp, rax
	mov	DWORD PTR [rax], 0
	mov	ecx, 32
	mov	QWORD PTR 96[rsp], rax
	lea	rax, 4[rax]
	pxor	xmm0, xmm0
	mov	QWORD PTR 4[rbp], 0
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR 16[rax], 0
	mov	DWORD PTR 24[rax], 0
	mov	QWORD PTR 112[rsp], rdx
	mov	QWORD PTR 104[rsp], rdx
	movups	XMMWORD PTR 136[rsp], xmm0
.LEHB6:
	call	_Znwy
.LEHE6:
	lea	rdx, 32[rax]
	movq	xmm7, rbp
	movq	xmm1, rax
	mov	QWORD PTR 128[rsp], rax
	mov	r12, rax
	movq	xmm6, rsi
	movq	xmm2, rdi
	mov	QWORD PTR 144[rsp], rdx
	mov	DWORD PTR [rax], 0
	xor	r13d, r13d
	punpcklqdq	xmm7, xmm1
	punpcklqdq	xmm6, xmm2
	mov	QWORD PTR 4[rax], 0
	mov	QWORD PTR 12[rax], 0
	mov	QWORD PTR 20[rax], 0
	mov	DWORD PTR 28[rax], 0
	mov	QWORD PTR 136[rsp], rdx
	.p2align 4,,10
	.p2align 3
.L109:
	lea	eax, [r13+r13]
	mov	rcx, rbx
	mov	DWORD PTR [rsi+r13*4], eax
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv
	mov	edx, eax
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	edx, edx, 100
	sub	eax, edx
	mov	DWORD PTR [rdi+r13*4], eax
	add	r13, 1
	cmp	r13, 8
	jne	.L109
	xor	r14d, r14d
	mov	r13d, 1
	.p2align 4,,10
	.p2align 3
.L110:
	mov	DWORD PTR 0[rbp+r14], r13d
	mov	rcx, rbx
	add	r13d, 2
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv
	mov	edx, eax
	imul	rdx, rdx, 1374389535
	shr	rdx, 37
	imul	edx, edx, 100
	sub	eax, edx
	mov	DWORD PTR [r12+r14], eax
	add	r14, 4
	cmp	r13d, 17
	jne	.L110
	movaps	XMMWORD PTR 160[rsp], xmm6
	mov	ecx, 48
	mov	rax, QWORD PTR 168[rsp]
	pxor	xmm0, xmm0
	movq	QWORD PTR 256[rsp], xmm6
	mov	QWORD PTR 272[rsp], 8
	movups	XMMWORD PTR 280[rsp], xmm7
	mov	QWORD PTR 264[rsp], rax
	mov	DWORD PTR 296[rsp], 8
	movaps	XMMWORD PTR 192[rsp], xmm0
	mov	QWORD PTR 208[rsp], 0
.LEHB7:
	call	_Znwy
.LEHE7:
	mov	rdx, QWORD PTR 256[rsp]
	mov	rbx, rax
	mov	QWORD PTR 192[rsp], rax
	lea	r15, 256[rsp]
	mov	QWORD PTR 224[rsp], 0
	lea	r14, 224[rsp]
	mov	r8, r15
	mov	QWORD PTR 232[rsp], 0
	mov	QWORD PTR 240[rsp], 0
	lea	rax, 48[rax]
	mov	QWORD PTR [rbx], rdx
	mov	rdx, QWORD PTR 264[rsp]
	lea	r13, 192[rsp]
	mov	rcx, r13
	mov	QWORD PTR 208[rsp], rax
	mov	QWORD PTR 200[rsp], rax
	mov	QWORD PTR 256[rsp], 0
	mov	QWORD PTR 8[rbx], rdx
	mov	rdx, QWORD PTR 272[rsp]
	mov	QWORD PTR 264[rsp], 0
	mov	QWORD PTR 272[rsp], 0
	mov	QWORD PTR 16[rbx], rdx
	mov	rdx, QWORD PTR 280[rsp]
	mov	QWORD PTR 24[rbx], rdx
	mov	rdx, QWORD PTR 288[rsp]
	mov	QWORD PTR 32[rbx], rdx
	mov	rdx, QWORD PTR 296[rsp]
	mov	QWORD PTR 40[rbx], rdx
	mov	rdx, r14
.LEHB8:
	call	_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_
.LEHE8:
	xor	edx, edx
	mov	r8d, 7
	jmp	.L111
	.p2align 4,,10
	.p2align 3
.L144:
	lea	edx, 1[rax]
	cmp	edx, r8d
	jg	.L142
.L111:
	mov	eax, r8d
	sub	eax, edx
	sar	eax
	add	eax, edx
	movsx	r9, eax
	mov	ecx, DWORD PTR [rsi+r9*4]
	cmp	ecx, 6
	je	.L143
	cmp	ecx, 5
	jle	.L144
	lea	r8d, -1[rax]
	cmp	edx, r8d
	jle	.L111
.L142:
	mov	r13d, -2
	jmp	.L115
.L143:
	mov	r13d, DWORD PTR [rdi+r9*4]
	sub	r13d, 1
.L115:
	mov	r14, QWORD PTR 224[rsp]
	mov	rax, QWORD PTR 232[rsp]
	mov	rcx, QWORD PTR 256[rsp]
	sub	rax, r14
	sar	rax, 2
	add	r13d, eax
	test	rcx, rcx
	je	.L118
	mov	rdx, QWORD PTR 272[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L118:
	test	r14, r14
	je	.L119
	mov	rdx, QWORD PTR 240[rsp]
	mov	rcx, r14
	sub	rdx, r14
	call	_ZdlPvy
.L119:
	mov	rcx, rbx
	mov	edx, 48
	call	_ZdlPvy
	mov	rcx, r12
	mov	edx, 32
	call	_ZdlPvy
	mov	rcx, rbp
	mov	edx, 32
	call	_ZdlPvy
	mov	rcx, rdi
	mov	edx, 32
	call	_ZdlPvy
	mov	edx, 32
	mov	rcx, rsi
	call	_ZdlPvy
	nop
	movaps	xmm6, XMMWORD PTR 2816[rsp]
	mov	eax, r13d
	movaps	xmm7, XMMWORD PTR 2832[rsp]
	add	rsp, 2856
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L125:
	mov	rbx, rax
	jmp	.L123
.L128:
	mov	rcx, r15
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, r14
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, r13
	call	_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev
.L113:
	lea	rcx, 128[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
.L121:
	lea	rcx, 96[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
.L122:
	lea	rcx, 64[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
.L123:
	lea	rcx, 32[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, rbx
.LEHB9:
	call	_Unwind_Resume
.LEHE9:
.L127:
	mov	rbx, rax
	jmp	.L121
.L129:
	lea	rcx, 192[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseI3RunSaIS0_EED2Ev
	jmp	.L113
.L126:
	mov	rbx, rax
	jmp	.L122
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5062:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5062-.LLSDACSB5062
.LLSDACSB5062:
	.uleb128 .LEHB3-.LFB5062
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB5062
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L125-.LFB5062
	.uleb128 0
	.uleb128 .LEHB5-.LFB5062
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L126-.LFB5062
	.uleb128 0
	.uleb128 .LEHB6-.LFB5062
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L127-.LFB5062
	.uleb128 0
	.uleb128 .LEHB7-.LFB5062
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L129-.LFB5062
	.uleb128 0
	.uleb128 .LEHB8-.LFB5062
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L128-.LFB5062
	.uleb128 0
	.uleb128 .LEHB9-.LFB5062
	.uleb128 .LEHE9-.LEHB9
	.uleb128 0
	.uleb128 0
.LLSDACSE5062:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5113:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	ecx, 42
	add	rsp, 40
	jmp	_Z4demoi
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC2:
	.long	-2147483648
	.long	-2147483648
	.long	-2147483648
	.long	-2147483648
	.align 16
.LC3:
	.long	2147483647
	.long	2147483647
	.long	2147483647
	.long	2147483647
	.align 16
.LC4:
	.long	1
	.long	1
	.long	1
	.long	1
	.align 16
.LC5:
	.long	-1727483681
	.long	-1727483681
	.long	-1727483681
	.long	-1727483681
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
