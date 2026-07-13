	.file	"_ch96_lambda_inline.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_:
.LFB2477:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, rdx
	mov	rdi, rcx
	mov	r12, rdx
	sub	rax, rcx
	mov	rbp, r8
	mov	ebx, r9d
	cmp	rax, 128
	mov	r11, rdx
	jle	.L1
	lea	rsi, 8[rcx]
	test	r8, r8
	je	.L45
.L4:
	sar	rax, 4
	mov	ecx, DWORD PTR 8[rdi]
	sub	rbp, 1
	lea	r8, [rdi+rax*8]
	movq	xmm0, QWORD PTR [rdi]
	mov	eax, DWORD PTR [r8]
	mov	r9d, DWORD PTR -8[r11]
	movd	edx, xmm0
	cmp	ecx, eax
	jge	.L31
	cmp	eax, r9d
	jl	.L37
	cmp	ecx, r9d
	jl	.L67
.L34:
	mov	rax, QWORD PTR 8[rdi]
	movq	QWORD PTR 8[rdi], xmm0
	mov	QWORD PTR [rdi], rax
	mov	r8d, DWORD PTR -8[r11]
.L33:
	mov	ecx, DWORD PTR [rdi]
	mov	r10, r11
	mov	rax, rsi
	cmp	edx, ecx
	jge	.L55
	.p2align 4,,10
	.p2align 3
.L70:
	add	rax, 8
	.p2align 4,,10
	.p2align 3
.L39:
	mov	r9, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 8
	cmp	edx, ecx
	jl	.L39
	cmp	r8d, ecx
	mov	r12, r9
	jle	.L40
.L71:
	lea	rax, -16[r10]
	.p2align 4,,10
	.p2align 3
.L41:
	mov	r10, rax
	sub	rax, 8
	cmp	DWORD PTR 8[rax], ecx
	jg	.L41
	cmp	r12, r10
	jnb	.L69
.L43:
	mov	rax, QWORD PTR [r10]
	movd	xmm0, edx
	movd	xmm1, DWORD PTR 4[r12]
	punpckldq	xmm0, xmm1
	mov	QWORD PTR [r12], rax
	lea	rax, 8[r12]
	mov	r8d, DWORD PTR -8[r10]
	movq	QWORD PTR [r10], xmm0
	mov	edx, DWORD PTR 8[r12]
	mov	ecx, DWORD PTR [rdi]
	cmp	edx, ecx
	jl	.L70
.L55:
	cmp	r8d, ecx
	mov	r12, rax
	jg	.L71
	.p2align 4,,10
	.p2align 3
.L40:
	sub	r10, 8
	cmp	r12, r10
	jb	.L43
	.p2align 4,,10
	.p2align 3
.L69:
	mov	r9d, ebx
	mov	r8, rbp
	mov	rdx, r11
	mov	rcx, r12
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_
	mov	rax, r12
	sub	rax, rdi
	cmp	rax, 128
	jle	.L1
	test	rbp, rbp
	je	.L45
	mov	r11, r12
	jmp	.L4
.L31:
	cmp	ecx, r9d
	jl	.L34
	cmp	eax, r9d
	jge	.L37
.L67:
	mov	rax, QWORD PTR -8[r11]
	mov	r8d, edx
	mov	QWORD PTR [rdi], rax
	movq	QWORD PTR -8[r11], xmm0
	mov	edx, DWORD PTR 8[rdi]
	jmp	.L33
.L37:
	mov	rax, QWORD PTR [r8]
	mov	QWORD PTR [rdi], rax
	movq	QWORD PTR [r8], xmm0
	mov	edx, DWORD PTR 8[rdi]
	mov	r8d, DWORD PTR -8[r11]
	jmp	.L33
.L15:
	lea	r9, -8[r12]
	.p2align 4,,10
	.p2align 3
.L30:
	mov	rax, QWORD PTR [rdi]
	mov	r10, r9
	sub	r10, rdi
	movq	xmm0, QWORD PTR [r9]
	mov	rbp, r10
	sar	rbp, 3
	movd	r8d, xmm0
	mov	QWORD PTR [r9], rax
	lea	rax, -1[rbp]
	mov	r12, rbp
	mov	rsi, rax
	and	r12d, 1
	shr	rsi, 63
	add	rsi, rax
	sar	rsi
	cmp	r10, 16
	jle	.L18
	xor	ebx, ebx
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L52:
	mov	rbx, rdx
.L20:
	lea	rax, 1[rbx]
	lea	rdx, [rax+rax]
	sal	rax, 4
	lea	rcx, -1[rdx]
	add	rax, rdi
	lea	r11, [rdi+rcx*8]
	mov	r13d, DWORD PTR [rax]
	cmp	DWORD PTR [r11], r13d
	jle	.L19
	mov	rax, r11
	mov	rdx, rcx
.L19:
	mov	rcx, QWORD PTR [rax]
	cmp	rdx, rsi
	mov	QWORD PTR [rdi+rbx*8], rcx
	jl	.L52
	test	r12, r12
	je	.L24
	lea	r11, -1[rdx]
	mov	rcx, r11
	shr	rcx, 63
	add	rcx, r11
	sar	rcx
	test	rdx, rdx
	jne	.L28
	jmp	.L72
	.p2align 4,,10
	.p2align 3
.L74:
	mov	rdx, QWORD PTR [r11]
	mov	QWORD PTR [rax], rdx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	mov	rdx, rcx
	sar	rax
	test	rcx, rcx
	je	.L73
	mov	rcx, rax
.L28:
	lea	r11, [rdi+rcx*8]
	cmp	r8d, DWORD PTR [r11]
	lea	rax, [rdi+rdx*8]
	jg	.L74
.L23:
	sub	r9, 8
	cmp	r10, 8
	movq	QWORD PTR [rax], xmm0
	jg	.L30
.L1:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L45:
	sar	rax, 3
	lea	rbx, -2[rax]
	lea	r10, -1[rax]
	not	rax
	sar	rbx
	mov	r8d, eax
	sar	r10
	mov	rcx, rbx
	lea	r11, [rdi+rbx*8]
	and	r8d, 1
.L17:
	movq	xmm0, QWORD PTR [r11]
	cmp	rcx, r10
	mov	rax, r11
	movd	r9d, xmm0
	jge	.L49
	mov	rsi, rcx
	jmp	.L7
	.p2align 4,,10
	.p2align 3
.L50:
	mov	rsi, rdx
.L7:
	lea	rax, 1[rsi]
	lea	rdx, [rax+rax]
	sal	rax, 4
	lea	rbp, -1[rdx]
	add	rax, rdi
	lea	r13, [rdi+rbp*8]
	mov	r14d, DWORD PTR [rax]
	cmp	DWORD PTR 0[r13], r14d
	jle	.L6
	mov	rax, r13
	mov	rdx, rbp
.L6:
	mov	rbp, QWORD PTR [rax]
	cmp	rdx, r10
	mov	QWORD PTR [rdi+rsi*8], rbp
	jl	.L50
.L5:
	cmp	rbx, rdx
	jne	.L57
	test	r8b, r8b
	jne	.L8
.L57:
	lea	rsi, -1[rdx]
	sar	rsi
	cmp	rcx, rdx
	jl	.L13
	jmp	.L75
	.p2align 4,,10
	.p2align 3
.L77:
	mov	rdx, QWORD PTR 0[rbp]
	mov	QWORD PTR [rax], rdx
	lea	rdx, -1[rsi]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	mov	rdx, rsi
	sar	rax
	cmp	rcx, rsi
	jge	.L76
	mov	rsi, rax
.L13:
	lea	rbp, [rdi+rsi*8]
	cmp	DWORD PTR 0[rbp], r9d
	lea	rax, [rdi+rdx*8]
	jl	.L77
.L12:
	test	rcx, rcx
	movq	QWORD PTR [rax], xmm0
	je	.L15
.L14:
	sub	rcx, 1
	sub	r11, 8
	jmp	.L17
.L76:
	mov	rax, rbp
	jmp	.L12
.L73:
	mov	rax, r11
	sub	r9, 8
	cmp	r10, 8
	movq	QWORD PTR [rax], xmm0
	jg	.L30
	jmp	.L1
.L24:
	lea	rcx, -2[rbp]
	sar	rcx
	cmp	rcx, rdx
	je	.L27
	lea	r11, -1[rdx]
	mov	rcx, r11
	shr	rcx, 63
	add	rcx, r11
	sar	rcx
	test	rdx, rdx
	jne	.L28
	jmp	.L23
	.p2align 4,,10
	.p2align 3
.L18:
	test	r12, r12
	jne	.L66
	cmp	rax, 2
	ja	.L66
	xor	edx, edx
	mov	rax, rdi
.L27:
	lea	r11, 1[rdx+rdx]
	mov	rcx, QWORD PTR [rdi+r11*8]
	mov	QWORD PTR [rax], rcx
	mov	rcx, rdx
	mov	rdx, r11
	jmp	.L28
.L66:
	mov	rax, rdi
	sub	r9, 8
	cmp	r10, 8
	movq	QWORD PTR [rax], xmm0
	jg	.L30
	jmp	.L1
.L8:
	lea	rsi, [rdx+rdx]
	lea	rdx, 1[rsi]
	sar	rsi
	lea	rbp, [rdi+rdx*8]
	cmp	rcx, rdx
	mov	r13, QWORD PTR 0[rbp]
	mov	QWORD PTR [rax], r13
	mov	rax, rbp
	jl	.L13
.L75:
	movq	QWORD PTR [rax], xmm0
	jmp	.L14
.L49:
	mov	rdx, rcx
	jmp	.L5
.L72:
	movq	QWORD PTR [rax], xmm0
	sub	r9, 8
	jmp	.L30
	.seh_endproc
	.p2align 4
	.globl	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE
	.def	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE
_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE:
.LFB2389:
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
	mov	rbx, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rbx
	je	.L78
	mov	rdi, rbx
	sub	rdi, rbp
	mov	rax, rdi
	sar	rax, 3
	test	rax, rax
	je	.L106
	bsr	rax, rax
	xor	r9d, r9d
	mov	rdx, rbx
	lea	rsi, 8[rbp]
	cdqe
	mov	rcx, rbp
	lea	r8, [rax+rax]
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_
	add	rdi, -128
	jle	.L81
	lea	rdi, 128[rbp]
	mov	r12d, 8
	jmp	.L88
	.p2align 4,,10
	.p2align 3
.L108:
	mov	r8, rsi
	sub	r8, rbp
	cmp	r8, 8
	jle	.L83
	mov	rcx, r12
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rsi
	call	memmove
.L84:
	add	rsi, 8
	movq	QWORD PTR 0[rbp], xmm6
	cmp	rdi, rsi
	je	.L107
.L88:
	movq	xmm6, QWORD PTR [rsi]
	mov	rdx, rsi
	movd	ecx, xmm6
	cmp	DWORD PTR 0[rbp], ecx
	jg	.L108
	cmp	ecx, DWORD PTR -8[rsi]
	lea	rax, -8[rsi]
	jge	.L86
	.p2align 4,,10
	.p2align 3
.L87:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, rax
	sub	rax, 8
	cmp	DWORD PTR [rax], ecx
	jg	.L87
.L86:
	add	rsi, 8
	movq	QWORD PTR [rdx], xmm6
	cmp	rdi, rsi
	jne	.L88
.L107:
	cmp	rbx, rdi
	je	.L78
	mov	r8, rdi
	.p2align 4,,10
	.p2align 3
.L92:
	movq	xmm0, QWORD PTR [r8]
	lea	rax, -8[r8]
	mov	rdx, r8
	movd	ecx, xmm0
	cmp	ecx, DWORD PTR -8[r8]
	jge	.L90
	.p2align 4,,10
	.p2align 3
.L91:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, rax
	sub	rax, 8
	cmp	ecx, DWORD PTR [rax]
	jl	.L91
.L90:
	add	r8, 8
	movq	QWORD PTR [rdx], xmm0
	cmp	r8, rbx
	jne	.L92
.L78:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L106:
	xor	r9d, r9d
	mov	r8, -2
	mov	rdx, rbx
	lea	rsi, 8[rbp]
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIZ18sort_points_inlineRS6_EUlRKS2_SC_E_EEEvT_SF_T0_T1_
.L81:
	cmp	rbx, rsi
	je	.L78
	mov	edi, 8
	jmp	.L99
	.p2align 4,,10
	.p2align 3
.L109:
	mov	r8, rsi
	sub	r8, rbp
	cmp	r8, 8
	jle	.L94
	mov	rcx, rdi
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rsi
	call	memmove
.L95:
	movq	QWORD PTR 0[rbp], xmm6
.L96:
	add	rsi, 8
	cmp	rsi, rbx
	je	.L78
.L99:
	movq	xmm6, QWORD PTR [rsi]
	mov	rdx, rsi
	movd	ecx, xmm6
	cmp	ecx, DWORD PTR 0[rbp]
	jl	.L109
	cmp	ecx, DWORD PTR -8[rsi]
	lea	rax, -8[rsi]
	jge	.L97
	.p2align 4,,10
	.p2align 3
.L98:
	mov	rdx, QWORD PTR [rax]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, rax
	sub	rax, 8
	cmp	ecx, DWORD PTR [rax]
	jl	.L98
.L97:
	movq	QWORD PTR [rdx], xmm6
	jmp	.L96
.L94:
	jne	.L95
	mov	rax, QWORD PTR 0[rbp]
	mov	QWORD PTR [rsi], rax
	jmp	.L95
.L83:
	jne	.L84
	mov	rax, QWORD PTR 0[rbp]
	mov	QWORD PTR [rsi], rax
	jmp	.L84
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2393:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	ecx, 32
	movaps	XMMWORD PTR 64[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	movaps	XMMWORD PTR 80[rsp], xmm0
	call	_Znwy
	mov	rdx, QWORD PTR 64[rsp]
	lea	rcx, 32[rsp]
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	lea	rax, 32[rax]
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR [rbx], rdx
	mov	rdx, QWORD PTR 72[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 8[rbx], rdx
	mov	rdx, QWORD PTR 80[rsp]
	mov	QWORD PTR 16[rbx], rdx
	mov	rdx, QWORD PTR 88[rsp]
	mov	QWORD PTR 24[rbx], rdx
	call	_Z18sort_points_inlineRSt6vectorI5PointSaIS0_EE
	mov	esi, DWORD PTR [rbx]
	mov	edx, 32
	mov	rcx, rbx
	call	_ZdlPvy
	mov	eax, esi
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	3
	.long	1
	.long	1
	.long	9
	.align 16
.LC1:
	.long	2
	.long	5
	.long	4
	.long	0
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
