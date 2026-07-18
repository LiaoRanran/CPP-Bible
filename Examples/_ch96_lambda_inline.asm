	.file	"_ch96_lambda_inline.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_.isra.0:
.LFB2514:
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
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rax, rdx
	mov	rbx, rcx
	mov	rsi, r8
	mov	r11, rdx
	sub	rax, rcx
	cmp	rax, 128
	jle	.L1
	mov	rdi, rax
	sar	rax, 4
	sar	rdi, 3
	test	rsi, rsi
	je	.L64
.L3:
	lea	r8, [rbx+rax*8]
	mov	ecx, DWORD PTR 8[rbx]
	mov	r9d, DWORD PTR -8[r11]
	sub	rsi, 1
	mov	edx, DWORD PTR [r8]
	movq	xmm0, QWORD PTR [rbx]
	lea	rax, 8[rbx]
	cmp	ecx, edx
	jge	.L31
	cmp	edx, r9d
	jl	.L36
	cmp	ecx, r9d
	jl	.L62
.L34:
	mov	rcx, QWORD PTR 8[rbx]
	movd	edx, xmm0
	movq	QWORD PTR 8[rbx], xmm0
	mov	QWORD PTR [rbx], rcx
.L33:
	mov	ecx, DWORD PTR [rbx]
	mov	r9, r11
	cmp	edx, ecx
	jge	.L52
	.p2align 4
	.p2align 3
.L66:
	add	rax, 8
	.p2align 4
	.p2align 4
	.p2align 3
.L38:
	mov	r10, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 8
	cmp	ecx, edx
	jg	.L38
	cmp	ecx, DWORD PTR -8[r9]
	jge	.L39
.L67:
	lea	rax, -16[r9]
	.p2align 4
	.p2align 4
	.p2align 3
.L40:
	mov	r9, rax
	sub	rax, 8
	cmp	ecx, DWORD PTR 8[rax]
	jl	.L40
	cmp	r10, r9
	jnb	.L65
.L42:
	movd	xmm1, DWORD PTR 4[r10]
	mov	rax, QWORD PTR [r9]
	movd	xmm0, edx
	punpckldq	xmm0, xmm1
	mov	QWORD PTR [r10], rax
	lea	rax, 8[r10]
	movq	QWORD PTR [r9], xmm0
	mov	edx, DWORD PTR 8[r10]
	mov	ecx, DWORD PTR [rbx]
	cmp	edx, ecx
	jl	.L66
.L52:
	mov	r10, rax
	cmp	ecx, DWORD PTR -8[r9]
	jl	.L67
	.p2align 4
	.p2align 3
.L39:
	sub	r9, 8
	cmp	r10, r9
	jb	.L42
	.p2align 4
	.p2align 3
.L65:
	mov	r8, rsi
	mov	rdx, r11
	mov	rcx, r10
	mov	QWORD PTR 40[rsp], r10
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_.isra.0
	mov	rax, QWORD PTR 40[rsp]
	sub	rax, rbx
	cmp	rax, 128
	jle	.L1
	mov	rdi, rax
	mov	r11, QWORD PTR 40[rsp]
	sar	rax, 4
	sar	rdi, 3
	test	rsi, rsi
	jne	.L3
.L64:
	lea	r8, -1[rax]
	lea	r10, -1[rdi]
	sar	r10
	mov	rbp, r8
	lea	rsi, -8[rbx+rax*8]
.L16:
	movq	xmm0, QWORD PTR [rsi]
	mov	rcx, rsi
	movd	r9d, xmm0
	cmp	r8, r10
	jge	.L4
	mov	r12, r8
	jmp	.L6
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L46:
	mov	r12, rax
.L6:
	lea	rdx, 1[r12]
	lea	r13, [rdx+rdx]
	sal	rdx, 4
	lea	rax, -1[r13]
	add	rdx, rbx
	lea	rcx, [rbx+rax*8]
	mov	r14d, DWORD PTR [rdx]
	cmp	DWORD PTR [rcx], r14d
	cmovle	rcx, rdx
	cmovle	rax, r13
	mov	rdx, QWORD PTR [rcx]
	mov	QWORD PTR [rbx+r12*8], rdx
	cmp	rax, r10
	jl	.L46
	test	dil, 1
	jne	.L58
	cmp	rbp, rax
	je	.L9
.L58:
	lea	rdx, -1[rax]
.L8:
	sar	rdx
	cmp	r8, rax
	jl	.L12
	jmp	.L10
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L69:
	mov	rcx, QWORD PTR [r12]
	mov	QWORD PTR [rax], rcx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	cmp	r8, rdx
	jge	.L68
	sar	rcx
	mov	rdx, rcx
.L12:
	lea	r12, [rbx+rdx*8]
	lea	rax, [rbx+rax*8]
	cmp	DWORD PTR [r12], r9d
	jl	.L69
	movq	QWORD PTR [rax], xmm0
	test	r8, r8
	je	.L70
.L13:
	sub	r8, 1
	sub	rsi, 8
	jmp	.L16
.L31:
	cmp	ecx, r9d
	jl	.L34
	cmp	edx, r9d
	jge	.L36
.L62:
	mov	rdx, QWORD PTR -8[r11]
	mov	QWORD PTR [rbx], rdx
	movq	QWORD PTR -8[r11], xmm0
	mov	edx, DWORD PTR 8[rbx]
	jmp	.L33
.L36:
	mov	rdx, QWORD PTR [r8]
	mov	QWORD PTR [rbx], rdx
	movq	QWORD PTR [r8], xmm0
	mov	edx, DWORD PTR 8[rbx]
	jmp	.L33
.L1:
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L68:
	mov	rax, r12
	movq	QWORD PTR [rax], xmm0
	test	r8, r8
	jne	.L13
.L70:
	mov	rax, r11
	sub	r11, 8
	sub	rax, rbx
	cmp	rax, 8
	jle	.L1
	.p2align 4
	.p2align 3
.L30:
	mov	r8, r11
	mov	rax, QWORD PTR [rbx]
	movq	xmm0, QWORD PTR [r11]
	sub	r8, rbx
	mov	rdi, r8
	mov	QWORD PTR [r11], rax
	sar	rdi, 3
	cmp	r8, 16
	jle	.L17
	lea	rsi, -1[rdi]
	xor	r10d, r10d
	sar	rsi
	jmp	.L19
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L49:
	mov	r10, rax
.L19:
	lea	rdx, 1[r10]
	lea	r9, [rdx+rdx]
	sal	rdx, 4
	lea	rax, -1[r9]
	add	rdx, rbx
	lea	rcx, [rbx+rax*8]
	mov	ebp, DWORD PTR [rdx]
	cmp	DWORD PTR [rcx], ebp
	cmovle	rcx, rdx
	cmovle	rax, r9
	mov	rdx, QWORD PTR [rcx]
	mov	QWORD PTR [rbx+r10*8], rdx
	cmp	rax, rsi
	jl	.L49
	and	edi, 1
	jne	.L60
	mov	rdx, r8
	sar	rdx, 4
	sub	rdx, 1
	cmp	rdx, rax
	je	.L25
.L60:
	lea	rdx, -1[rax]
	shr	rdx, 63
	lea	rdx, -1[rax+rdx]
	sar	rdx
	test	rax, rax
	je	.L27
.L26:
	movd	r10d, xmm0
	jmp	.L28
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L72:
	mov	rcx, QWORD PTR [r9]
	mov	QWORD PTR [rax], rcx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	test	rdx, rdx
	je	.L71
	sar	rcx
	mov	rdx, rcx
.L28:
	lea	r9, [rbx+rdx*8]
	lea	rax, [rbx+rax*8]
	cmp	r10d, DWORD PTR [r9]
	jg	.L72
.L22:
	movq	QWORD PTR [rax], xmm0
	cmp	r8, 8
	jle	.L1
.L59:
	sub	r11, 8
	jmp	.L30
.L71:
	mov	rax, r9
	jmp	.L22
.L17:
	and	edi, 1
	jne	.L61
	cmp	r8, 16
	jne	.L61
	mov	rcx, rbx
	xor	eax, eax
.L25:
	lea	r9, 1[rax+rax]
	mov	rdx, QWORD PTR [rbx+r9*8]
	mov	QWORD PTR [rcx], rdx
	mov	rdx, rax
	mov	rax, r9
	jmp	.L26
.L61:
	mov	rax, rbx
	jmp	.L22
.L4:
	test	dil, 1
	jne	.L10
	cmp	r8, rbp
	jne	.L10
	mov	rax, r8
.L9:
	lea	rdx, [rax+rax]
	lea	rax, 1[rdx]
	lea	r12, [rbx+rax*8]
	mov	r13, QWORD PTR [r12]
	mov	QWORD PTR [rcx], r13
	mov	rcx, r12
	jmp	.L8
.L10:
	movq	QWORD PTR [rcx], xmm0
	jmp	.L13
.L27:
	movq	QWORD PTR [rcx], xmm0
	jmp	.L59
	.seh_endproc
	.p2align 4
	.globl	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE
	.def	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE
_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE:
.LFB2347:
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
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rsi
	je	.L73
	mov	rbx, rsi
	sub	rbx, rbp
	mov	rax, rbx
	sar	rax, 3
	je	.L101
	bsr	rax, rax
	mov	rdx, rsi
	mov	rcx, rbp
	movsxd	r8, eax
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_.isra.0
	cmp	rbx, 128
	jle	.L76
	lea	r12, 128[rbp]
	lea	rdi, 8[rbp]
	mov	rbx, r12
	jmp	.L83
	.p2align 4,,10
	.p2align 3
.L103:
	mov	r8, rdi
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[rdi+rax]
	cmp	r8, 8
	jle	.L78
	mov	rdx, rbp
	call	memmove
.L79:
	add	rdi, 8
	movq	QWORD PTR 0[rbp], xmm6
	cmp	r12, rdi
	je	.L102
.L83:
	movq	xmm6, QWORD PTR [rdi]
	mov	rdx, rdi
	movd	ecx, xmm6
	cmp	DWORD PTR 0[rbp], ecx
	jg	.L103
	cmp	DWORD PTR -8[rdi], ecx
	jle	.L81
	lea	rax, -8[rdi]
	.p2align 5
	.p2align 4
	.p2align 3
.L82:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, rax
	sub	rax, 8
	cmp	DWORD PTR [rax], ecx
	jg	.L82
.L81:
	add	rdi, 8
	movq	QWORD PTR [rdx], xmm6
	cmp	r12, rdi
	jne	.L83
.L102:
	cmp	rsi, r12
	je	.L73
	.p2align 4
	.p2align 3
.L87:
	movq	xmm0, QWORD PTR [rbx]
	mov	rdx, rbx
	movd	ecx, xmm0
	cmp	ecx, DWORD PTR -8[rbx]
	jge	.L85
	lea	rax, -8[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L86:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, rax
	sub	rax, 8
	cmp	ecx, DWORD PTR [rax]
	jl	.L86
.L85:
	add	rbx, 8
	movq	QWORD PTR [rdx], xmm0
	cmp	rbx, rsi
	jne	.L87
.L73:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L101:
	mov	r8, -2
	mov	rdx, rsi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_.isra.0
.L76:
	lea	rbx, 8[rbp]
	cmp	rsi, rbx
	jne	.L94
	jmp	.L73
	.p2align 4,,10
	.p2align 3
.L104:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[rbx+rax]
	cmp	r8, 8
	jle	.L89
	mov	rdx, rbp
	call	memmove
.L90:
	movq	QWORD PTR 0[rbp], xmm6
.L91:
	add	rbx, 8
	cmp	rbx, rsi
	je	.L73
.L94:
	movq	xmm6, QWORD PTR [rbx]
	mov	rdx, rbx
	movd	ecx, xmm6
	cmp	DWORD PTR 0[rbp], ecx
	jg	.L104
	cmp	DWORD PTR -8[rbx], ecx
	jle	.L92
	lea	rax, -8[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L93:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, rax
	sub	rax, 8
	cmp	DWORD PTR [rax], ecx
	jg	.L93
.L92:
	movq	QWORD PTR [rdx], xmm6
	jmp	.L91
.L78:
	jne	.L79
	mov	rax, QWORD PTR 0[rbp]
	mov	QWORD PTR [rcx], rax
	jmp	.L79
.L89:
	jne	.L90
	mov	rax, QWORD PTR 0[rbp]
	mov	QWORD PTR [rcx], rax
	jmp	.L90
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2351:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	call	__main
	mov	ecx, 32
	call	_Znwy
	movabs	rdx, 4294967299
	movabs	rcx, 38654705665
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	lea	rax, 32[rax]
	mov	QWORD PTR [rbx], rdx
	movabs	rdx, 21474836482
	mov	QWORD PTR 8[rbx], rcx
	mov	ecx, 4
	mov	QWORD PTR 16[rbx], rdx
	mov	QWORD PTR 24[rbx], rcx
	lea	rcx, 32[rsp]
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 40[rsp], rax
	call	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE
	mov	esi, DWORD PTR [rbx]
	mov	edx, 32
	mov	rcx, rbx
	call	_ZdlPvy
	mov	eax, esi
	add	rsp, 72
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
