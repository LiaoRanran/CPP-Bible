	.file	"_atom_false_sharing_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB6568:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEE6_M_runEv:
.LFB8932:
	.seh_endprologue
	mov	eax, 10000000
	.p2align 4
	.p2align 4
	.p2align 3
.L4:
	movsxd	r8, DWORD PTR 16[rcx]
	mov	rdx, QWORD PTR 8[rcx]
	lock add	QWORD PTR [rdx+r8*8], 1
	sub	rax, 1
	jne	.L4
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEE6_M_runEv:
.LFB8931:
	.seh_endprologue
	mov	edx, 10000000
	.p2align 5
	.p2align 4
	.p2align 3
.L7:
	mov	r8, QWORD PTR 8[rcx]
	movsxd	rax, DWORD PTR 16[rcx]
	sal	rax, 6
	add	rax, QWORD PTR [r8]
	lock add	QWORD PTR [rax], 1
	sub	rdx, 1
	jne	.L7
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED2Ev:
.LFB8743:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED0Ev:
.LFB8745:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt6thread6_StateD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 24
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED2Ev:
.LFB8739:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED0Ev:
.LFB8741:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt6thread6_StateD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 24
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.def	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0:
.LFB9757:
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
	mov	rdi, rcx
	mov	rbp, rdx
	cmp	rcx, rdx
	je	.L13
	lea	rsi, 8[rcx]
	cmp	rdx, rsi
	jne	.L21
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L25:
	mov	r8, rsi
	sub	r8, rdi
	mov	rax, r8
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[rsi+rax]
	cmp	r8, 8
	jle	.L16
	mov	rdx, rdi
	call	memmove
.L17:
	add	rsi, 8
	mov	QWORD PTR [rdi], rbx
	cmp	rbp, rsi
	je	.L13
.L21:
	mov	rbx, QWORD PTR [rsi]
	mov	rdx, QWORD PTR [rdi]
	cmp	rbx, rdx
	jl	.L25
	mov	rdx, QWORD PTR -8[rsi]
	cmp	rbx, rdx
	jge	.L22
	lea	rax, -8[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L20:
	mov	QWORD PTR 8[rax], rdx
	mov	rcx, rax
	mov	rdx, QWORD PTR -8[rax]
	sub	rax, 8
	cmp	rbx, rdx
	jl	.L20
.L19:
	add	rsi, 8
	mov	QWORD PTR [rcx], rbx
	cmp	rbp, rsi
	jne	.L21
.L13:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L16:
	jne	.L17
	mov	QWORD PTR [rcx], rdx
	jmp	.L17
.L22:
	mov	rcx, rsi
	jmp	.L19
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0:
.LFB9760:
	.seh_endprologue
	test	rcx, rcx
	je	.L26
	sub	rdx, rcx
	jmp	_ZdlPvy
.L26:
	ret
	.seh_endproc
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB9761:
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
	mov	rax, rdx
	mov	rsi, rcx
	mov	rdi, r8
	mov	r11, rdx
	sub	rax, rcx
	cmp	rax, 128
	jle	.L28
	mov	r12, rax
	sar	rax, 4
	sar	r12, 3
	test	rdi, rdi
	je	.L91
.L30:
	movdqu	xmm0, XMMWORD PTR [rsi]
	lea	r10, [rsi+rax*8]
	mov	r9, QWORD PTR -8[r11]
	sub	rdi, 1
	mov	r8, QWORD PTR [r10]
	lea	rax, 8[rsi]
	movhlps	xmm1, xmm0
	movq	rcx, xmm0
	movq	rdx, xmm1
	cmp	rdx, r8
	jge	.L59
	cmp	r8, r9
	jl	.L64
	cmp	rdx, r9
	jl	.L90
.L62:
	shufpd	xmm0, xmm0, 1
	movups	XMMWORD PTR [rsi], xmm0
.L61:
	mov	r10, r11
	cmp	rcx, rdx
	jge	.L80
	.p2align 4
	.p2align 3
.L93:
	add	rax, 8
	.p2align 4
	.p2align 4
	.p2align 3
.L66:
	mov	r9, rax
	mov	rcx, QWORD PTR [rax]
	add	rax, 8
	cmp	rcx, rdx
	jl	.L66
	mov	rbx, r9
	mov	r9, QWORD PTR -8[r10]
	cmp	r9, rdx
	jle	.L67
.L94:
	lea	rax, -16[r10]
	.p2align 4
	.p2align 4
	.p2align 3
.L68:
	mov	r10, rax
	mov	r9, QWORD PTR [rax]
	sub	rax, 8
	cmp	r9, rdx
	jg	.L68
	cmp	rbx, r10
	jnb	.L92
.L70:
	mov	QWORD PTR [rbx], r9
	lea	rax, 8[rbx]
	mov	QWORD PTR [r10], rcx
	mov	rdx, QWORD PTR [rsi]
	mov	rcx, QWORD PTR 8[rbx]
	cmp	rcx, rdx
	jl	.L93
.L80:
	mov	r9, QWORD PTR -8[r10]
	mov	rbx, rax
	cmp	r9, rdx
	jg	.L94
	.p2align 4
	.p2align 3
.L67:
	sub	r10, 8
	cmp	rbx, r10
	jb	.L70
	.p2align 4
	.p2align 3
.L92:
	mov	r8, rdi
	mov	rdx, r11
	mov	rcx, rbx
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	rax, rbx
	sub	rax, rsi
	cmp	rax, 128
	jle	.L28
	mov	r12, rax
	mov	r11, rbx
	sar	rax, 4
	sar	r12, 3
	test	rdi, rdi
	jne	.L30
.L91:
	lea	rdi, -1[r12]
	lea	rbp, -8[rsi+rax*8]
	lea	r10, -1[rax]
	sar	rdi
	mov	rbx, QWORD PTR 0[rbp]
	mov	rcx, rbp
	mov	r13, r10
	cmp	r10, rdi
	jge	.L31
.L97:
	mov	r8, r10
	jmp	.L33
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L74:
	mov	r8, rax
.L33:
	lea	rdx, 1[r8]
	lea	r9, [rdx+rdx]
	sal	rdx, 4
	lea	rax, -1[r9]
	add	rdx, rsi
	lea	rcx, [rsi+rax*8]
	mov	r15, QWORD PTR [rdx]
	mov	r14, QWORD PTR [rcx]
	cmp	r14, r15
	cmovle	r14, r15
	cmovle	rax, r9
	cmovle	rcx, rdx
	mov	QWORD PTR [rsi+r8*8], r14
	cmp	rax, rdi
	jl	.L74
	test	r12b, 1
	jne	.L86
	cmp	r13, rax
	je	.L36
.L86:
	lea	rdx, -1[rax]
.L35:
	sar	rdx
	cmp	r10, rax
	jl	.L39
	jmp	.L37
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L96:
	mov	QWORD PTR [rax], rcx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	cmp	r10, rdx
	jge	.L95
	mov	rdx, rcx
	sar	rdx
.L39:
	lea	r8, [rsi+rdx*8]
	lea	rax, [rsi+rax*8]
	mov	rcx, QWORD PTR [r8]
	cmp	rbx, rcx
	jg	.L96
	mov	QWORD PTR [rax], rbx
	test	r10, r10
	je	.L41
.L40:
	sub	rbp, 8
	sub	r10, 1
	mov	rbx, QWORD PTR 0[rbp]
	mov	rcx, rbp
	cmp	r10, rdi
	jl	.L97
.L31:
	test	r12b, 1
	jne	.L37
	cmp	r10, r13
	je	.L98
.L37:
	mov	QWORD PTR [rcx], rbx
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L59:
	cmp	rdx, r9
	jl	.L62
	cmp	r8, r9
	jge	.L64
.L90:
	mov	QWORD PTR [rsi], r9
	mov	QWORD PTR -8[r11], rcx
	mov	rcx, QWORD PTR 8[rsi]
	mov	rdx, QWORD PTR [rsi]
	jmp	.L61
.L64:
	mov	QWORD PTR [rsi], r8
	mov	QWORD PTR [r10], rcx
	mov	rcx, QWORD PTR 8[rsi]
	mov	rdx, QWORD PTR [rsi]
	jmp	.L61
.L28:
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
.L95:
	mov	rax, r8
	mov	QWORD PTR [rax], rbx
	test	r10, r10
	jne	.L40
.L41:
	mov	rax, r11
	sub	r11, 8
	sub	rax, rsi
	cmp	rax, 8
	jle	.L28
	.p2align 4
	.p2align 3
.L58:
	mov	r9, r11
	mov	rax, QWORD PTR [rsi]
	mov	r8, QWORD PTR [r11]
	sub	r9, rsi
	mov	r13, r9
	mov	QWORD PTR [r11], rax
	sar	r13, 3
	cmp	r9, 16
	jle	.L45
	lea	r12, -1[r13]
	xor	ebp, ebp
	sar	r12
	jmp	.L47
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L77:
	mov	rbp, rax
.L47:
	lea	rdx, 1[rbp]
	lea	rbx, [rdx+rdx]
	sal	rdx, 4
	lea	rax, -1[rbx]
	add	rdx, rsi
	lea	r10, [rsi+rax*8]
	mov	rdi, QWORD PTR [rdx]
	mov	rcx, QWORD PTR [r10]
	cmp	rcx, rdi
	cmovle	rcx, rdi
	cmovle	rax, rbx
	cmovle	r10, rdx
	mov	QWORD PTR [rsi+rbp*8], rcx
	cmp	r12, rax
	jg	.L77
	and	r13d, 1
	jne	.L88
	mov	rdx, r9
	sar	rdx, 4
	sub	rdx, 1
	cmp	rdx, rax
	je	.L53
.L88:
	lea	rdx, -1[rax]
	shr	rdx, 63
	lea	rdx, -1[rax+rdx]
	sar	rdx
	test	rax, rax
	jne	.L56
	jmp	.L99
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L101:
	mov	QWORD PTR [rax], rcx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	test	rdx, rdx
	je	.L100
	sar	rcx
	mov	rdx, rcx
.L56:
	lea	r10, [rsi+rdx*8]
	lea	rax, [rsi+rax*8]
	mov	rcx, QWORD PTR [r10]
	cmp	r8, rcx
	jg	.L101
.L50:
	mov	QWORD PTR [rax], r8
	cmp	r9, 8
	jle	.L28
.L87:
	sub	r11, 8
	jmp	.L58
.L100:
	mov	rax, r10
	jmp	.L50
.L45:
	and	r13d, 1
	jne	.L89
	cmp	r9, 16
	jne	.L89
	mov	r10, rsi
	xor	eax, eax
.L53:
	lea	rcx, 1[rax+rax]
	mov	rdx, QWORD PTR [rsi+rcx*8]
	mov	QWORD PTR [r10], rdx
	mov	rdx, rax
	mov	rax, rcx
	jmp	.L56
.L89:
	mov	rax, rsi
	jmp	.L50
.L98:
	mov	rax, r10
.L36:
	lea	rdx, [rax+rax]
	lea	rax, 1[rdx]
	lea	r8, [rsi+rax*8]
	mov	r9, QWORD PTR [r8]
	mov	QWORD PTR [rcx], r9
	mov	rcx, r8
	jmp	.L35
.L99:
	mov	QWORD PTR [r10], r8
	jmp	.L87
	.seh_endproc
	.p2align 4
	.def	_ZN12_GLOBAL__N_1L9median_ofESt6vectorIxSaIxEE;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZN12_GLOBAL__N_1L9median_ofESt6vectorIxSaIxEE
_ZN12_GLOBAL__N_1L9median_ofESt6vectorIxSaIxEE:
.LFB6800:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbx, rcx
	mov	rcx, QWORD PTR [rcx]
	cmp	rcx, rsi
	je	.L103
	mov	rdi, rsi
	mov	r8d, 63
	mov	QWORD PTR 40[rsp], rcx
	sub	rdi, rcx
	mov	rax, rdi
	sar	rax, 3
	bsr	rdx, rax
	xor	rdx, 63
	test	rax, rax
	mov	eax, 64
	cmovne	eax, edx
	mov	rdx, rsi
	sub	r8d, eax
	movsxd	r8, r8d
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	cmp	rdi, 128
	mov	rcx, QWORD PTR 40[rsp]
	jle	.L105
	lea	rdi, 128[rcx]
	mov	rdx, rdi
	call	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	cmp	rsi, rdi
	je	.L103
	.p2align 4
	.p2align 3
.L106:
	mov	rcx, QWORD PTR [rdi]
	mov	rdx, QWORD PTR -8[rdi]
	cmp	rcx, rdx
	jge	.L112
	lea	rax, -8[rdi]
	.p2align 5
	.p2align 4
	.p2align 3
.L109:
	mov	QWORD PTR 8[rax], rdx
	mov	r8, rax
	mov	rdx, QWORD PTR -8[rax]
	sub	rax, 8
	cmp	rcx, rdx
	jl	.L109
.L108:
	add	rdi, 8
	mov	QWORD PTR [r8], rcx
	cmp	rsi, rdi
	jne	.L106
.L103:
	mov	rdx, QWORD PTR [rbx]
	mov	rax, QWORD PTR 8[rbx]
	sub	rax, rdx
	sar	rax, 3
	shr	rax
	mov	rax, QWORD PTR [rdx+rax*8]
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L105:
	mov	rdx, rsi
	call	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPxSt6vectorIxSaIxEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	jmp	.L103
.L112:
	mov	r8, rdi
	jmp	.L108
	.seh_endproc
	.section	.text$_ZNSt6vectorIxSaIxEEC1ERKS1_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIxSaIxEEC1ERKS1_
	.def	_ZNSt6vectorIxSaIxEEC1ERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIxSaIxEEC1ERKS1_
_ZNSt6vectorIxSaIxEEC1ERKS1_:
.LFB6845:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	xor	r9d, r9d
	mov	rax, QWORD PTR 8[rdx]
	sub	rax, QWORD PTR [rdx]
	mov	r8, rax
	mov	rbx, rcx
	mov	rsi, rdx
	je	.L117
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
	call	_Znwy
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, rax
.L117:
	movq	xmm0, r9
	lea	rax, [r9+r8]
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 16[rbx], rax
	movups	XMMWORD PTR [rbx], xmm0
	mov	rax, QWORD PTR [rsi]
	mov	rsi, QWORD PTR 8[rsi]
	sub	rsi, rax
	test	rsi, rsi
	jle	.L118
	mov	rcx, r9
	mov	r8, rsi
	mov	rdx, rax
	call	memcpy
	lea	r9, [rax+rsi]
.L118:
	mov	QWORD PTR 8[rbx], r9
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB7845:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L121
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L121:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	.def	_ZNSt6vectorISt6threadSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EED1Ev
_ZNSt6vectorISt6threadSaIS0_EED1Ev:
.LFB7860:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	r8, rcx
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, rcx
	je	.L124
	mov	rax, rcx
	.p2align 4
	.p2align 4
	.p2align 3
.L126:
	cmp	QWORD PTR [rax], 0
	jne	.L129
	add	rax, 8
	cmp	rdx, rax
	jne	.L126
.L124:
	test	rcx, rcx
	je	.L123
	mov	rdx, QWORD PTR 16[r8]
	sub	rdx, rcx
	add	rsp, 40
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L123:
	add	rsp, 40
	ret
.L129:
	call	_ZSt9terminatev
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
.LC1:
	.ascii "threads=%d\12\0"
.LC2:
	.ascii "iters_per_thread=%lld\12\0"
.LC3:
	.ascii "rounds=%d\12\0"
.LC4:
	.ascii "cache_line_size=%zu\12\0"
.LC5:
	.ascii "tight_stride_bytes=%zu\12\0"
.LC6:
	.ascii "padded_stride_bytes=%zu\12\0"
.LC7:
	.ascii "tight_shares_line=%d\12\0"
.LC8:
	.ascii "padded_shares_line=%d\12\0"
.LC9:
	.ascii "sharing_is_slower=%d\12\0"
.LC10:
	.ascii "counters_all_advanced=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB11:
	.section	.text.startup,"x"
.LHOTB11:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB6807:
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
	sub	rsp, 328
	.seh_stackalloc	328
	.seh_endprologue
	call	__main
	pxor	xmm0, xmm0
	mov	ecx, 256
	mov	edx, 64
	movaps	XMMWORD PTR 288[rsp], xmm0
	movaps	XMMWORD PTR 304[rsp], xmm0
.LEHB0:
	call	_ZnwySt11align_val_t
.LEHE0:
	mov	ecx, 32
	mov	DWORD PTR 108[rsp], 7
	lea	r8, 256[rax]
	mov	rdi, rax
	mov	QWORD PTR 128[rsp], rax
	xor	eax, eax
	rep stosq
	lea	rax, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	mov	QWORD PTR 144[rsp], r8
	mov	QWORD PTR 136[rsp], r8
	mov	QWORD PTR 88[rsp], 0
	mov	QWORD PTR 56[rsp], 0
	mov	QWORD PTR 120[rsp], 0
	mov	QWORD PTR 80[rsp], 0
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 112[rsp], 0
	mov	QWORD PTR 32[rsp], rax
	.p2align 4
	.p2align 3
.L184:
	mov	ecx, 32
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	rbx, rax
	lea	rbp, 32[rax]
	xor	esi, esi
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdi, rbx
	lea	r14, 288[rsp]
	mov	QWORD PTR 40[rsp], rax
.L144:
	mov	r12d, esi
	mov	ecx, 24
	mov	QWORD PTR 192[rsp], 0
	mov	r13, r12
.LEHB2:
	call	_Znwy
.LEHE2:
	lea	rdx, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR 8[rax], r14
	mov	r8, QWORD PTR 32[rsp]
	mov	QWORD PTR [rax], rdx
	lea	rdx, 256[rsp]
	mov	QWORD PTR 16[rax], r13
	mov	QWORD PTR 256[rsp], rax
	lea	rax, 192[rsp]
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
.LEHB3:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE3:
	mov	rcx, QWORD PTR 256[rsp]
	test	rcx, rcx
	je	.L134
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L134:
	cmp	rbp, rbx
	je	.L261
	mov	rax, QWORD PTR 192[rsp]
	add	rbx, 8
	mov	QWORD PTR -8[rbx], rax
.L138:
	add	esi, 1
	cmp	esi, 4
	jne	.L144
	cmp	rbx, rdi
	je	.L145
	mov	rsi, rdi
	.p2align 4
	.p2align 3
.L146:
	mov	rcx, rsi
.LEHB4:
	call	_ZNSt6thread4joinEv
.LEHE4:
	add	rsi, 8
	cmp	rbx, rsi
	jne	.L146
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rsi, rax
	mov	rax, rdi
	.p2align 4
	.p2align 4
	.p2align 3
.L148:
	cmp	QWORD PTR [rax], 0
	jne	.L153
	add	rax, 8
	cmp	rbx, rax
	jne	.L148
	sub	rsi, QWORD PTR 40[rsp]
	test	rdi, rdi
	je	.L149
	mov	rdx, rbp
	sub	rdx, rdi
.L191:
	mov	rcx, rdi
	call	_ZdlPvy
.L149:
	mov	rdi, QWORD PTR 80[rsp]
	cmp	QWORD PTR 64[rsp], rdi
	je	.L262
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR [rax], rsi
	add	rax, 8
	mov	QWORD PTR 64[rsp], rax
.L155:
	mov	ecx, 32
.LEHB5:
	call	_Znwy
.LEHE5:
	mov	rbx, rax
	lea	r13, 32[rax]
	xor	ebp, ebp
	xor	r14d, r14d
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r12, rbx
	mov	QWORD PTR 72[rsp], rax
	lea	rax, 128[rsp]
	mov	QWORD PTR 40[rsp], rax
.L172:
	movabs	rcx, -4294967296
	mov	rax, r14
	mov	edx, ebp
	mov	QWORD PTR 224[rsp], 0
	and	rax, rcx
	mov	ecx, 24
	mov	rsi, QWORD PTR 40[rsp]
	or	rax, rdx
	mov	rdi, rax
.LEHB6:
	call	_Znwy
.LEHE6:
	lea	rdx, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR 8[rax], rsi
	mov	r8, QWORD PTR 32[rsp]
	lea	rcx, 224[rsp]
	mov	QWORD PTR [rax], rdx
	lea	rdx, 256[rsp]
	mov	QWORD PTR 16[rax], rdi
	mov	QWORD PTR 256[rsp], rax
.LEHB7:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE7:
	mov	rcx, QWORD PTR 256[rsp]
	test	rcx, rcx
	je	.L162
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L162:
	cmp	rbx, r13
	je	.L263
	mov	rax, QWORD PTR 224[rsp]
	add	rbx, 8
	mov	QWORD PTR -8[rbx], rax
.L166:
	add	ebp, 1
	cmp	ebp, 4
	jne	.L172
	cmp	rbx, r12
	je	.L173
	mov	rsi, r12
	.p2align 4
	.p2align 3
.L174:
	mov	rcx, rsi
.LEHB8:
	call	_ZNSt6thread4joinEv
.LEHE8:
	add	rsi, 8
	cmp	rbx, rsi
	jne	.L174
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rsi, rax
	mov	rax, r12
	.p2align 4
	.p2align 4
	.p2align 3
.L175:
	cmp	QWORD PTR [rax], 0
	jne	.L153
	add	rax, 8
	cmp	rax, rbx
	jne	.L175
	sub	rsi, QWORD PTR 72[rsp]
	test	r12, r12
	je	.L176
	mov	rdx, r13
	sub	rdx, r12
.L190:
	mov	rcx, r12
	call	_ZdlPvy
.L176:
	mov	rdi, QWORD PTR 88[rsp]
	cmp	QWORD PTR 56[rsp], rdi
	je	.L264
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR [rax], rsi
	add	rax, 8
	mov	QWORD PTR 56[rsp], rax
.L180:
	sub	DWORD PTR 108[rsp], 1
	jne	.L184
	mov	rax, QWORD PTR 112[rsp]
	lea	rdx, 160[rsp]
	lea	rcx, 256[rsp]
	mov	QWORD PTR 160[rsp], rax
	mov	rax, QWORD PTR 64[rsp]
	mov	QWORD PTR 168[rsp], rax
	mov	rax, QWORD PTR 80[rsp]
	mov	QWORD PTR 176[rsp], rax
.LEHB9:
	call	_ZNSt6vectorIxSaIxEEC1ERKS1_
	lea	rcx, 256[rsp]
	call	_ZN12_GLOBAL__N_1L9median_ofESt6vectorIxSaIxEE
	mov	rdx, QWORD PTR 272[rsp]
	mov	rcx, QWORD PTR 256[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rax, QWORD PTR 120[rsp]
	mov	rdx, QWORD PTR 48[rsp]
	lea	rcx, 256[rsp]
	mov	QWORD PTR 192[rsp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 200[rsp], rax
	mov	rax, QWORD PTR 88[rsp]
	mov	QWORD PTR 208[rsp], rax
	call	_ZNSt6vectorIxSaIxEEC1ERKS1_
	lea	rcx, 256[rsp]
	call	_ZN12_GLOBAL__N_1L9median_ofESt6vectorIxSaIxEE
	mov	rdx, QWORD PTR 272[rsp]
	mov	rcx, QWORD PTR 256[rsp]
	mov	rsi, rax
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	edx, 4
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 10000000
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	mov	edx, 7
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	mov	edx, 64
	lea	rcx, .LC4[rip]
	call	__mingw_printf
	mov	edx, 8
	lea	rcx, .LC5[rip]
	call	__mingw_printf
	mov	edx, 64
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	mov	edx, 1
	lea	rcx, .LC7[rip]
	call	__mingw_printf
	mov	rax, QWORD PTR 128[rsp]
	lea	rcx, .LC8[rip]
	lea	rdx, 64[rax]
	shr	rax, 6
	shr	rdx, 6
	cmp	rdx, rax
	sete	dl
	movzx	edx, dl
	call	__mingw_printf
	xor	edx, edx
	cmp	rbx, rsi
	lea	rcx, .LC9[rip]
	setg	dl
	call	__mingw_printf
	mov	rax, QWORD PTR 288[rsp]
	test	rax, rax
	jg	.L185
.L187:
	xor	edx, edx
.L186:
	lea	rcx, .LC10[rip]
	call	__mingw_printf
.LEHE9:
	mov	rdx, QWORD PTR 88[rsp]
	mov	rcx, QWORD PTR 120[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, QWORD PTR 112[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, QWORD PTR 128[rsp]
	test	rcx, rcx
	je	.L213
	mov	rdx, QWORD PTR 144[rsp]
	mov	r8d, 64
	sub	rdx, rcx
	call	_ZdlPvySt11align_val_t
.L213:
	xor	eax, eax
	add	rsp, 328
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
.L263:
	movabs	rdi, 1152921504606846975
	mov	rdx, rbx
	sub	rdx, r12
	mov	rax, rdx
	sar	rax, 3
	cmp	rax, rdi
	je	.L255
	test	rax, rax
	mov	esi, 1
	mov	QWORD PTR 96[rsp], rdx
	cmovne	rsi, rax
	add	rsi, rax
	movabs	rax, 1152921504606846975
	cmp	rsi, rax
	cmova	rsi, rax
	sal	rsi, 3
	mov	rcx, rsi
.LEHB10:
	call	_Znwy
.LEHE10:
	mov	rdi, rax
	mov	rdx, QWORD PTR 96[rsp]
	mov	rax, QWORD PTR 224[rsp]
	mov	QWORD PTR [rdi+rdx], rax
	cmp	rbx, r12
	je	.L265
	mov	r8, rbx
	mov	rdx, r12
	mov	rax, rdi
	sub	r8, r12
	add	r8, rdi
	.p2align 5
	.p2align 4
	.p2align 3
.L170:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 8
	add	rdx, 8
	mov	QWORD PTR -8[rax], rcx
	cmp	rax, r8
	jne	.L170
	sub	rbx, r12
	lea	rbx, 8[rdi+rbx]
	test	r12, r12
	je	.L171
.L169:
	mov	rdx, r13
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L171:
	lea	r13, [rdi+rsi]
	mov	r12, rdi
	jmp	.L166
	.p2align 4,,10
	.p2align 3
.L261:
	movabs	rcx, 1152921504606846975
	mov	rdx, rbp
	sub	rdx, rdi
	mov	rax, rdx
	sar	rax, 3
	cmp	rax, rcx
	je	.L253
	test	rax, rax
	mov	r12d, 1
	mov	QWORD PTR 72[rsp], rdx
	cmovne	r12, rax
	add	r12, rax
	movabs	rax, 1152921504606846975
	cmp	r12, rax
	cmova	r12, rax
	sal	r12, 3
	mov	rcx, r12
.LEHB11:
	call	_Znwy
.LEHE11:
	mov	r13, rax
	mov	rdx, QWORD PTR 72[rsp]
	mov	rax, QWORD PTR 192[rsp]
	mov	QWORD PTR 0[r13+rdx], rax
	cmp	rbx, rdi
	je	.L266
	mov	r8, rbx
	mov	rdx, rdi
	mov	rax, r13
	sub	r8, rdi
	add	r8, r13
	.p2align 5
	.p2align 4
	.p2align 3
.L142:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 8
	add	rdx, 8
	mov	QWORD PTR -8[rax], rcx
	cmp	rax, r8
	jne	.L142
	sub	rbx, 8
	sub	rbx, rdi
	lea	rbx, 16[r13+rbx]
	test	rdi, rdi
	je	.L143
.L141:
	mov	rdx, rbp
	mov	rcx, rdi
	sub	rdx, rdi
	call	_ZdlPvy
.L143:
	lea	rbp, 0[r13+r12]
	mov	rdi, r13
	jmp	.L138
	.p2align 4,,10
	.p2align 3
.L262:
	movabs	rbx, 1152921504606846975
	mov	rdi, QWORD PTR 80[rsp]
	sub	rdi, QWORD PTR 112[rsp]
	mov	rax, rdi
	sar	rax, 3
	cmp	rax, rbx
	je	.L254
	test	rax, rax
	mov	ebx, 1
	cmovne	rbx, rax
	add	rbx, rax
	movabs	rax, 1152921504606846975
	cmp	rbx, rax
	cmova	rbx, rax
	sal	rbx, 3
	mov	rcx, rbx
.LEHB12:
	call	_Znwy
	mov	QWORD PTR [rax+rdi], rsi
	mov	rbp, rax
	test	rdi, rdi
	je	.L157
	mov	rdx, QWORD PTR 112[rsp]
	mov	r8, rdi
	mov	rcx, rax
	call	memcpy
.L157:
	mov	rcx, QWORD PTR 112[rsp]
	lea	rax, 8[rbp+rdi]
	mov	QWORD PTR 64[rsp], rax
	test	rcx, rcx
	je	.L158
	mov	rdx, QWORD PTR 80[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L158:
	lea	rax, 0[rbp+rbx]
	mov	QWORD PTR 112[rsp], rbp
	mov	QWORD PTR 80[rsp], rax
	jmp	.L155
	.p2align 4,,10
	.p2align 3
.L264:
	movabs	rbx, 1152921504606846975
	mov	rdi, QWORD PTR 88[rsp]
	sub	rdi, QWORD PTR 120[rsp]
	mov	rax, rdi
	sar	rax, 3
	cmp	rax, rbx
	je	.L256
	test	rax, rax
	mov	ebx, 1
	cmovne	rbx, rax
	add	rbx, rax
	movabs	rax, 1152921504606846975
	cmp	rbx, rax
	cmova	rbx, rax
	sal	rbx, 3
	mov	rcx, rbx
	call	_Znwy
.LEHE12:
	mov	QWORD PTR [rax+rdi], rsi
	mov	rbp, rax
	test	rdi, rdi
	je	.L182
	mov	rdx, QWORD PTR 120[rsp]
	mov	r8, rdi
	mov	rcx, rax
	call	memcpy
.L182:
	mov	rcx, QWORD PTR 120[rsp]
	lea	rax, 8[rbp+rdi]
	mov	QWORD PTR 56[rsp], rax
	test	rcx, rcx
	je	.L183
	mov	rdx, QWORD PTR 88[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L183:
	lea	rax, 0[rbp+rbx]
	mov	QWORD PTR 120[rsp], rbp
	mov	QWORD PTR 88[rsp], rax
	jmp	.L180
	.p2align 4,,10
	.p2align 3
.L173:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdx, r13
	sub	rax, QWORD PTR 72[rsp]
	mov	rsi, rax
	sub	rdx, r12
	jmp	.L190
	.p2align 4,,10
	.p2align 3
.L145:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdx, rbp
	sub	rax, QWORD PTR 40[rsp]
	mov	rsi, rax
	sub	rdx, rdi
	jmp	.L191
.L265:
	lea	rbx, 8[rdi]
	jmp	.L169
.L266:
	lea	rbx, 8[r13]
	jmp	.L141
.L185:
	mov	rax, QWORD PTR 296[rsp]
	test	rax, rax
	jle	.L187
	mov	rax, QWORD PTR 304[rsp]
	test	rax, rax
	jle	.L187
	xor	edx, edx
	mov	rax, QWORD PTR 312[rsp]
	test	rax, rax
	setg	dl
	jmp	.L186
.L251:
	jmp	.L252
.L195:
	mov	rsi, rax
	jmp	.L165
.L197:
	mov	rsi, rax
	jmp	.L161
.L200:
	mov	rsi, rax
	jmp	.L160
.L193:
	mov	rsi, rax
	jmp	.L137
.L196:
	mov	rsi, rax
	jmp	.L133
.L199:
	mov	rsi, rax
	jmp	.L132
.L247:
	jmp	.L248
.L249:
	jmp	.L250
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6807:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6807-.LLSDACSB6807
.LLSDACSB6807:
	.uleb128 .LEHB0-.LFB6807
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB6807
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L199-.LFB6807
	.uleb128 0
	.uleb128 .LEHB2-.LFB6807
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L196-.LFB6807
	.uleb128 0
	.uleb128 .LEHB3-.LFB6807
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L193-.LFB6807
	.uleb128 0
	.uleb128 .LEHB4-.LFB6807
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L196-.LFB6807
	.uleb128 0
	.uleb128 .LEHB5-.LFB6807
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L200-.LFB6807
	.uleb128 0
	.uleb128 .LEHB6-.LFB6807
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L197-.LFB6807
	.uleb128 0
	.uleb128 .LEHB7-.LFB6807
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L195-.LFB6807
	.uleb128 0
	.uleb128 .LEHB8-.LFB6807
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L197-.LFB6807
	.uleb128 0
	.uleb128 .LEHB9-.LFB6807
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L251-.LFB6807
	.uleb128 0
	.uleb128 .LEHB10-.LFB6807
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L249-.LFB6807
	.uleb128 0
	.uleb128 .LEHB11-.LFB6807
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L247-.LFB6807
	.uleb128 0
	.uleb128 .LEHB12-.LFB6807
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L251-.LFB6807
	.uleb128 0
.LLSDACSE6807:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	392
	.seh_savereg	rbx, 328
	.seh_savereg	rsi, 336
	.seh_savereg	rdi, 344
	.seh_savereg	rbp, 352
	.seh_savereg	r12, 360
	.seh_savereg	r13, 368
	.seh_savereg	r14, 376
	.seh_savereg	r15, 384
	.seh_endprologue
main.cold:
.L255:
	lea	rcx, .LC0[rip]
.LEHB13:
	call	_ZSt20__throw_length_errorPKc
.LEHE13:
.L194:
.L250:
	mov	rsi, rax
	cmp	QWORD PTR 224[rsp], 0
	jne	.L153
.L161:
	lea	rcx, 256[rsp]
	mov	QWORD PTR 256[rsp], r12
	mov	QWORD PTR 264[rsp], rbx
	mov	QWORD PTR 272[rsp], r13
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
.L154:
	mov	rdx, QWORD PTR 88[rsp]
	mov	rcx, QWORD PTR 120[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, QWORD PTR 112[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	call	_ZNSt12_Vector_baseIxSaIxEED2Ev.isra.0
	mov	rcx, QWORD PTR 128[rsp]
	test	rcx, rcx
	je	.L189
	mov	rdx, QWORD PTR 144[rsp]
	mov	r8d, 64
	sub	rdx, rcx
	call	_ZdlPvySt11align_val_t
.L189:
	mov	rcx, rsi
.LEHB14:
	call	_Unwind_Resume
.LEHE14:
.L198:
.L252:
	mov	rsi, rax
	jmp	.L154
.L165:
	lea	rcx, 256[rsp]
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L161
.L192:
.L248:
	mov	rsi, rax
	cmp	QWORD PTR 192[rsp], 0
	je	.L133
.L153:
	call	_ZSt9terminatev
.L160:
	xor	r13d, r13d
	xor	ebx, ebx
	xor	r12d, r12d
	jmp	.L161
.L137:
	lea	rcx, 256[rsp]
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L133:
	lea	rcx, 224[rsp]
	mov	QWORD PTR 224[rsp], rdi
	mov	QWORD PTR 232[rsp], rbx
	mov	QWORD PTR 240[rsp], rbp
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	jmp	.L154
.L256:
	lea	rcx, .LC0[rip]
.LEHB15:
	call	_ZSt20__throw_length_errorPKc
.L132:
	xor	ebp, ebp
	xor	ebx, ebx
	xor	edi, edi
	jmp	.L133
.L254:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE15:
.L253:
	lea	rcx, .LC0[rip]
.LEHB16:
	call	_ZSt20__throw_length_errorPKc
	nop
.LEHE16:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC6807:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6807-.LLSDACSBC6807
.LLSDACSBC6807:
	.uleb128 .LEHB13-.LCOLDB11
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L194-.LCOLDB11
	.uleb128 0
	.uleb128 .LEHB14-.LCOLDB11
	.uleb128 .LEHE14-.LEHB14
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB15-.LCOLDB11
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L198-.LCOLDB11
	.uleb128 0
	.uleb128 .LEHB16-.LCOLDB11
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L192-.LCOLDB11
	.uleb128 0
.LLSDACSEC6807:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE11:
	.section	.text.startup,"x"
.LHOTE11:
	.globl	_ZTSNSt6thread6_StateE
	.section	.rdata$_ZTSNSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt6thread6_StateE:
	.ascii "NSt6thread6_StateE\0"
	.globl	_ZTINSt6thread6_StateE
	.section	.rdata$_ZTINSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread6_StateE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt6thread6_StateE
	.section .rdata,"dr"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE\0"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE\0"
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE_clEiEUlvE_EEEEE6_M_runEv
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZZ4mainENKUliE0_clEiEUlvE_EEEEE6_M_runEv
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
	.def	_ZnwySt11align_val_t;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvySt11align_val_t;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
