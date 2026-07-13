	.file	"_ch96_comparator.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4by_xRK5PointS1_
	.def	_Z4by_xRK5PointS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4by_xRK5PointS1_
_Z4by_xRK5PointS1_:
.LFB2389:
	.seh_endprologue
	mov	eax, DWORD PTR [rdx]
	cmp	DWORD PTR [rcx], eax
	setl	al
	ret
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev
	.def	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev
_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev:
.LFB2450:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L3
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L3:
	ret
	.seh_endproc
	.section	.text$_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_:
.LFB2475:
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
	sub	rsp, 136
	.seh_stackalloc	136
	movaps	XMMWORD PTR 112[rsp], xmm6
	.seh_savexmm	xmm6, 112
	.seh_endprologue
	mov	rax, rdx
	mov	rdi, rcx
	mov	rbx, rdx
	sub	rax, rcx
	mov	r14, r8
	mov	rbp, r9
	cmp	rax, 128
	mov	r15, rdx
	jle	.L5
	lea	r13, 8[rcx]
	test	r8, r8
	je	.L45
.L8:
	sar	rax, 4
	mov	rcx, r13
	sub	r14, 1
	lea	rbx, [rdi+rax*8]
	lea	rsi, -8[r15]
	mov	rdx, rbx
	call	rbp
	mov	rdx, rsi
	test	al, al
	je	.L34
	mov	rcx, rbx
	call	rbp
	test	al, al
	je	.L35
	mov	rax, QWORD PTR [rdi]
	mov	rdx, QWORD PTR [rbx]
	mov	QWORD PTR [rdi], rdx
	mov	QWORD PTR [rbx], rax
.L36:
	mov	r12, r15
	mov	rax, r13
	.p2align 4,,10
	.p2align 3
.L40:
	mov	rbx, rax
	mov	rdx, rdi
	mov	rcx, rax
	call	rbp
	mov	edx, eax
	lea	rax, 8[rbx]
	test	dl, dl
	jne	.L40
	lea	rsi, -8[r12]
	.p2align 4,,10
	.p2align 3
.L41:
	mov	rdx, rsi
	mov	rcx, rdi
	mov	r12, rsi
	call	rbp
	sub	rsi, 8
	test	al, al
	jne	.L41
	cmp	rbx, r12
	jnb	.L82
	mov	rax, QWORD PTR [rbx]
	mov	rdx, QWORD PTR [r12]
	mov	QWORD PTR [rbx], rdx
	mov	QWORD PTR [r12], rax
	lea	rax, 8[rbx]
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L82:
	mov	r9, rbp
	mov	r8, r14
	mov	rdx, r15
	mov	rcx, rbx
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_
	mov	rax, rbx
	sub	rax, rdi
	cmp	rax, 128
	jle	.L5
	test	r14, r14
	je	.L45
	mov	r15, rbx
	jmp	.L8
.L34:
	mov	rcx, r13
	call	rbp
	test	al, al
	je	.L38
	mov	rax, QWORD PTR [rdi]
.L81:
	mov	rdx, QWORD PTR 8[rdi]
	mov	QWORD PTR 8[rdi], rax
	mov	QWORD PTR [rdi], rdx
	jmp	.L36
.L19:
	mov	rbx, QWORD PTR 88[rsp]
	lea	r12, -8[rbx]
	mov	rsi, r12
	.p2align 4,,10
	.p2align 3
.L33:
	mov	rax, QWORD PTR [rdi]
	mov	rbx, rsi
	sub	rbx, rdi
	movq	xmm6, QWORD PTR [rsi]
	mov	QWORD PTR 40[rsp], rbx
	mov	QWORD PTR [rsi], rax
	mov	rax, rbx
	sar	rax, 3
	lea	rdx, -1[rax]
	mov	rcx, rax
	mov	r15, rdx
	and	ecx, 1
	shr	r15, 63
	add	r15, rdx
	sar	r15
	cmp	rbx, 16
	jle	.L22
	xor	r12d, r12d
	mov	QWORD PTR 48[rsp], rsi
	mov	QWORD PTR 56[rsp], rcx
	mov	rsi, r12
	mov	r12, rdi
	mov	QWORD PTR 64[rsp], rax
	mov	QWORD PTR 72[rsp], r13
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L52:
	mov	rsi, rdi
.L24:
	lea	rbx, 1[rsi]
	lea	r14, [rbx+rbx]
	sal	rbx, 4
	lea	rdi, -1[r14]
	add	rbx, r12
	lea	r13, [r12+rdi*8]
	mov	rcx, rbx
	mov	rdx, r13
	call	rbp
	test	al, al
	cmove	r13, rbx
	cmove	rdi, r14
	mov	rax, QWORD PTR 0[r13]
	cmp	rdi, r15
	mov	QWORD PTR [r12+rsi*8], rax
	jl	.L52
	mov	rcx, QWORD PTR 56[rsp]
	mov	rbx, rdi
	mov	r14, r13
	mov	rdi, r12
	mov	rsi, QWORD PTR 48[rsp]
	mov	rax, QWORD PTR 64[rsp]
	mov	r13, QWORD PTR 72[rsp]
	test	rcx, rcx
	je	.L26
	lea	rax, -1[rbx]
	movq	QWORD PTR 104[rsp], xmm6
	mov	r12, rax
	shr	r12, 63
	add	r12, rax
	sar	r12
	test	rbx, rbx
	jne	.L31
	jmp	.L83
	.p2align 4,,10
	.p2align 3
.L85:
	mov	rax, QWORD PTR [r15]
	lea	rdx, -1[r12]
	mov	rbx, r12
	mov	QWORD PTR [r14], rax
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	r12, r12
	je	.L84
	mov	r12, rax
.L31:
	lea	r15, [rdi+r12*8]
	mov	rdx, r13
	lea	r14, [rdi+rbx*8]
	mov	rcx, r15
	call	rbp
	test	al, al
	jne	.L85
.L27:
	mov	rax, QWORD PTR 104[rsp]
	sub	rsi, 8
	cmp	QWORD PTR 40[rsp], 8
	mov	QWORD PTR [r14], rax
	jg	.L33
.L5:
	movaps	xmm6, XMMWORD PTR 112[rsp]
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L35:
	mov	rdx, rsi
	mov	rcx, r13
	call	rbp
	test	al, al
	mov	rax, QWORD PTR [rdi]
	je	.L81
.L80:
	mov	rdx, QWORD PTR -8[r15]
	mov	QWORD PTR [rdi], rdx
	mov	QWORD PTR -8[r15], rax
	jmp	.L36
.L38:
	mov	rdx, rsi
	mov	rcx, rbx
	call	rbp
	test	al, al
	mov	rax, QWORD PTR [rdi]
	jne	.L80
	mov	rdx, QWORD PTR [rbx]
	mov	QWORD PTR [rdi], rdx
	mov	QWORD PTR [rbx], rax
	jmp	.L36
.L45:
	lea	r13, 104[rsp]
	sar	rax, 3
	mov	QWORD PTR 88[rsp], rbx
	lea	rcx, -2[rax]
	lea	r14, -1[rax]
	not	rax
	sar	rcx
	and	eax, 1
	sar	r14
	mov	r12, rcx
	mov	QWORD PTR 72[rsp], rcx
	mov	BYTE PTR 87[rsp], al
	lea	rax, [rdi+rcx*8]
	mov	QWORD PTR 64[rsp], r14
	mov	QWORD PTR 40[rsp], rax
.L21:
	mov	rax, QWORD PTR 40[rsp]
	movq	xmm6, QWORD PTR [rax]
	mov	r15, rax
	mov	rax, QWORD PTR 64[rsp]
	cmp	r12, rax
	jge	.L49
	mov	QWORD PTR 48[rsp], r12
	mov	r14, rax
	mov	QWORD PTR 56[rsp], r13
	jmp	.L11
	.p2align 4,,10
	.p2align 3
.L50:
	mov	r12, rsi
.L11:
	lea	rbx, 1[r12]
	lea	r13, [rbx+rbx]
	sal	rbx, 4
	lea	rsi, -1[r13]
	add	rbx, rdi
	lea	r15, [rdi+rsi*8]
	mov	rcx, rbx
	mov	rdx, r15
	call	rbp
	test	al, al
	cmove	r15, rbx
	cmove	rsi, r13
	mov	rax, QWORD PTR [r15]
	cmp	rsi, r14
	mov	QWORD PTR [rdi+r12*8], rax
	jl	.L50
	mov	r12, QWORD PTR 48[rsp]
	mov	r13, QWORD PTR 56[rsp]
.L9:
	cmp	QWORD PTR 72[rsp], rsi
	jne	.L56
	cmp	BYTE PTR 87[rsp], 0
	jne	.L12
.L56:
	lea	r9, -1[rsi]
.L14:
	mov	rbx, r9
	movq	QWORD PTR 104[rsp], xmm6
	sar	rbx
	cmp	r12, rsi
	jl	.L17
	jmp	.L86
	.p2align 4,,10
	.p2align 3
.L88:
	mov	rax, QWORD PTR [r15]
	mov	rsi, rbx
	mov	QWORD PTR [rdx], rax
	lea	rdx, -1[rbx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r12, rbx
	jge	.L87
	mov	rbx, rax
.L17:
	lea	r15, [rdi+rbx*8]
	mov	rdx, r13
	mov	rcx, r15
	call	rbp
	lea	rdx, [rdi+rsi*8]
	test	al, al
	jne	.L88
.L16:
	mov	rcx, QWORD PTR 104[rsp]
	test	r12, r12
	mov	QWORD PTR [rdx], rcx
	je	.L19
.L18:
	sub	QWORD PTR 40[rsp], 8
	sub	r12, 1
	jmp	.L21
.L87:
	mov	rdx, r15
	jmp	.L16
.L53:
	mov	r14, rdi
	xor	ebx, ebx
.L26:
	sub	rax, 2
	mov	rcx, rax
	shr	rcx, 63
	add	rax, rcx
	sar	rax
	cmp	rax, rbx
	je	.L30
	lea	rax, -1[rbx]
	movq	QWORD PTR 104[rsp], xmm6
	mov	r12, rax
	shr	r12, 63
	add	r12, rax
	sar	r12
	test	rbx, rbx
	jne	.L31
	jmp	.L27
	.p2align 4,,10
	.p2align 3
.L84:
	mov	r14, r15
	jmp	.L27
.L30:
	lea	rax, 1[rbx+rbx]
	mov	r12, rbx
	movq	QWORD PTR 104[rsp], xmm6
	mov	rcx, QWORD PTR [rdi+rax*8]
	mov	rbx, rax
	mov	QWORD PTR [r14], rcx
	jmp	.L31
.L22:
	test	rcx, rcx
	je	.L53
	movq	QWORD PTR 104[rsp], xmm6
	mov	r14, rdi
	jmp	.L27
.L12:
	lea	r9, [rsi+rsi]
	lea	rsi, 1[r9]
	lea	rcx, [rdi+rsi*8]
	mov	r10, QWORD PTR [rcx]
	mov	QWORD PTR [r15], r10
	mov	r15, rcx
	jmp	.L14
.L49:
	mov	rsi, r12
	jmp	.L9
.L86:
	mov	rcx, QWORD PTR 104[rsp]
	mov	QWORD PTR [r15], rcx
	jmp	.L18
.L83:
	mov	rax, QWORD PTR 104[rsp]
	sub	rsi, 8
	mov	QWORD PTR [r14], rax
	jmp	.L33
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE
	.def	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE
_Z11sort_pointsRSt6vectorI5PointSaIS0_EE:
.LFB2390:
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
	sub	rsp, 72
	.seh_stackalloc	72
	movaps	XMMWORD PTR 48[rsp], xmm6
	.seh_savexmm	xmm6, 48
	.seh_endprologue
	mov	rdi, QWORD PTR 8[rcx]
	mov	rsi, QWORD PTR [rcx]
	cmp	rsi, rdi
	je	.L89
	mov	rbp, rdi
	mov	r8, -2
	sub	rbp, rsi
	mov	rax, rbp
	sar	rax, 3
	test	rax, rax
	je	.L91
	bsr	rax, rax
	cdqe
	lea	r8, [rax+rax]
.L91:
	lea	r9, _Z4by_xRK5PointS1_[rip]
	mov	rdx, rdi
	mov	rcx, rsi
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_
	lea	rbx, 8[rsi]
	add	rbp, -128
	jg	.L119
	cmp	rdi, rbx
	je	.L89
	lea	rbp, 40[rsp]
	mov	r12d, 8
	jmp	.L112
	.p2align 4,,10
	.p2align 3
.L120:
	mov	r8, rbx
	movd	xmm0, DWORD PTR 4[rbx]
	movd	xmm6, eax
	sub	r8, rsi
	cmp	r8, 8
	punpckldq	xmm6, xmm0
	jle	.L107
	mov	rcx, r12
	mov	rdx, rsi
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L108:
	add	rbx, 8
	movq	QWORD PTR [rsi], xmm6
	cmp	rdi, rbx
	je	.L89
.L112:
	mov	eax, DWORD PTR [rbx]
	cmp	eax, DWORD PTR [rsi]
	jl	.L120
	mov	rax, QWORD PTR [rbx]
	lea	rdx, -8[rbx]
	mov	QWORD PTR 40[rsp], rax
	jmp	.L110
	.p2align 4,,10
	.p2align 3
.L111:
	mov	rax, QWORD PTR [rdx]
	sub	rdx, 8
	mov	QWORD PTR 16[rdx], rax
.L110:
	mov	rcx, rbp
	call	_Z4by_xRK5PointS1_
	test	al, al
	jne	.L111
	mov	rax, QWORD PTR 40[rsp]
	add	rbx, 8
	cmp	rdi, rbx
	mov	QWORD PTR 8[rdx], rax
	jne	.L112
.L89:
	movaps	xmm6, XMMWORD PTR 48[rsp]
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L119:
	lea	r12, 128[rsi]
	mov	r13d, 8
	lea	rbp, 40[rsp]
	jmp	.L99
	.p2align 4,,10
	.p2align 3
.L122:
	mov	r8, rbx
	movd	xmm0, DWORD PTR 4[rbx]
	movd	xmm6, eax
	sub	r8, rsi
	cmp	r8, 8
	punpckldq	xmm6, xmm0
	jle	.L94
	mov	rcx, r13
	mov	rdx, rsi
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L95:
	add	rbx, 8
	movq	QWORD PTR [rsi], xmm6
	cmp	rbx, r12
	je	.L121
.L99:
	mov	eax, DWORD PTR [rbx]
	cmp	eax, DWORD PTR [rsi]
	jl	.L122
	mov	rax, QWORD PTR [rbx]
	lea	rdx, -8[rbx]
	mov	QWORD PTR 40[rsp], rax
	jmp	.L97
	.p2align 4,,10
	.p2align 3
.L98:
	mov	rax, QWORD PTR [rdx]
	sub	rdx, 8
	mov	QWORD PTR 16[rdx], rax
.L97:
	mov	rcx, rbp
	call	_Z4by_xRK5PointS1_
	test	al, al
	jne	.L98
	mov	rax, QWORD PTR 40[rsp]
	add	rbx, 8
	cmp	rbx, r12
	mov	QWORD PTR 8[rdx], rax
	jne	.L99
.L121:
	lea	r8, -8[rdi]
	add	rsi, 120
	cmp	rdi, rbx
	lea	rcx, 40[rsp]
	je	.L89
	.p2align 4,,10
	.p2align 3
.L104:
	mov	rax, QWORD PTR 8[rsi]
	mov	rdx, rsi
	mov	QWORD PTR 40[rsp], rax
	jmp	.L102
	.p2align 4,,10
	.p2align 3
.L103:
	mov	rax, QWORD PTR [rdx]
	sub	rdx, 8
	mov	QWORD PTR 16[rdx], rax
.L102:
	call	_Z4by_xRK5PointS1_
	test	al, al
	jne	.L103
	mov	rax, QWORD PTR 40[rsp]
	add	rsi, 8
	cmp	rsi, r8
	mov	QWORD PTR 8[rdx], rax
	jne	.L104
	jmp	.L89
.L107:
	jne	.L108
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR [rbx], rax
	jmp	.L108
.L94:
	jne	.L95
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR [rbx], rax
	jmp	.L95
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2391:
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
	mov	QWORD PTR 48[rsp], 0
	movaps	XMMWORD PTR 64[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	movaps	XMMWORD PTR 80[rsp], xmm0
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 32[rsp], xmm0
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rdx, QWORD PTR 64[rsp]
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	lea	rsi, 32[rsp]
	lea	rax, 32[rax]
	mov	rcx, rsi
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR [rbx], rdx
	mov	rdx, QWORD PTR 72[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	QWORD PTR 8[rbx], rdx
	mov	rdx, QWORD PTR 80[rsp]
	mov	QWORD PTR 16[rbx], rdx
	mov	rdx, QWORD PTR 88[rsp]
	mov	QWORD PTR 24[rbx], rdx
.LEHB1:
	call	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE
.LEHE1:
	mov	ebx, DWORD PTR [rbx]
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev
	mov	eax, ebx
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
.L128:
	lea	rcx, 32[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
.L127:
	mov	rsi, rax
	mov	rcx, rbx
	mov	edx, 32
	call	_ZdlPvy
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2391:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2391-.LLSDACSB2391
.LLSDACSB2391:
	.uleb128 .LEHB0-.LFB2391
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L128-.LFB2391
	.uleb128 0
	.uleb128 .LEHB1-.LFB2391
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L127-.LFB2391
	.uleb128 0
	.uleb128 .LEHB2-.LFB2391
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE2391:
	.section	.text.startup,"x"
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
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
