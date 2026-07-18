	.file	"_ch96_comparator.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4by_xRK5PointS1_
	.def	_Z4by_xRK5PointS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4by_xRK5PointS1_
_Z4by_xRK5PointS1_:
.LFB2347:
	.seh_endprologue
	mov	eax, DWORD PTR [rdx]
	cmp	DWORD PTR [rcx], eax
	setl	al
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev.isra.0
_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev.isra.0:
.LFB2513:
	.seh_endprologue
	test	rcx, rcx
	je	.L3
	sub	rdx, rcx
	jmp	_ZdlPvy
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
.LFB2438:
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
	sub	rsp, 104
	.seh_stackalloc	104
	movaps	XMMWORD PTR 80[rsp], xmm6
	.seh_savexmm	xmm6, 80
	.seh_endprologue
	mov	r14, rdx
	sub	rdx, rcx
	mov	rdi, rcx
	mov	r15, r8
	mov	rbp, r9
	cmp	rdx, 128
	jle	.L5
	mov	rax, rdx
	lea	r13, 8[rcx]
	sar	rdx, 4
	sar	rax, 3
	test	r15, r15
	je	.L75
.L7:
	lea	rsi, [rdi+rdx*8]
	lea	r12, -8[r14]
	mov	rcx, r13
	sub	r15, 1
	mov	rdx, rsi
	mov	rbx, r13
	call	rbp
	mov	rdx, r12
	test	al, al
	je	.L35
	mov	rcx, rsi
	call	rbp
	test	al, al
	je	.L36
	mov	rax, QWORD PTR [rdi]
	mov	rdx, QWORD PTR [rsi]
	mov	QWORD PTR [rdi], rdx
	mov	QWORD PTR [rsi], rax
.L37:
	mov	r12, r14
	.p2align 4
	.p2align 3
.L45:
	mov	rax, rbx
	.p2align 4
	.p2align 3
.L41:
	mov	rsi, rax
	mov	rdx, rdi
	mov	rcx, rax
	call	rbp
	mov	edx, eax
	lea	rax, 8[rsi]
	test	dl, dl
	jne	.L41
	lea	rbx, -8[r12]
	.p2align 4
	.p2align 3
.L42:
	mov	rdx, rbx
	mov	rcx, rdi
	mov	r12, rbx
	sub	rbx, 8
	call	rbp
	test	al, al
	jne	.L42
	cmp	rsi, r12
	jnb	.L76
	mov	rax, QWORD PTR [rsi]
	mov	rdx, QWORD PTR [r12]
	lea	rbx, 8[rsi]
	mov	QWORD PTR [rsi], rdx
	mov	QWORD PTR [r12], rax
	jmp	.L45
	.p2align 4,,10
	.p2align 3
.L76:
	mov	rdx, r14
	mov	r9, rbp
	mov	r8, r15
	mov	rcx, rsi
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_
	mov	rdx, rsi
	sub	rdx, rdi
	cmp	rdx, 128
	jle	.L5
	mov	rax, rdx
	mov	r14, rsi
	sar	rdx, 4
	sar	rax, 3
	test	r15, r15
	jne	.L7
.L75:
	lea	rcx, -8[rdi+rdx*8]
	lea	r13, -1[rdx]
	mov	QWORD PTR 56[rsp], r14
	mov	QWORD PTR 32[rsp], rcx
	lea	rbx, -1[rax]
	lea	rsi, 72[rsp]
	mov	QWORD PTR 40[rsp], rax
	sar	rbx
	mov	QWORD PTR 176[rsp], rdi
	mov	rdi, r13
	mov	QWORD PTR 48[rsp], r13
	mov	r13, QWORD PTR 176[rsp]
.L20:
	mov	rax, QWORD PTR 32[rsp]
	movq	xmm6, QWORD PTR [rax]
	mov	r10, rax
	cmp	rdi, rbx
	jge	.L8
	mov	r14, rdi
	.p2align 4
	.p2align 3
.L9:
	lea	rcx, 1[r14]
	lea	r12, [rcx+rcx]
	sal	rcx, 4
	lea	rdx, -8[r13+r12*8]
	add	rcx, r13
	call	rbp
	mov	rdx, r14
	mov	r14, r12
	movzx	eax, al
	sub	r14, rax
	lea	r12, 0[0+r14*8]
	lea	r10, 0[r13+r12]
	mov	rax, QWORD PTR [r10]
	mov	QWORD PTR 0[r13+rdx*8], rax
	cmp	r14, rbx
	jl	.L9
	test	BYTE PTR 40[rsp], 1
	jne	.L70
	cmp	QWORD PTR 48[rsp], r14
	je	.L12
.L70:
	lea	r9, -1[r14]
.L11:
	sar	r9
	movq	QWORD PTR 72[rsp], xmm6
	mov	r15, r9
	cmp	rdi, r14
	jl	.L16
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L78:
	mov	rax, QWORD PTR [r14]
	mov	QWORD PTR [r12], rax
	lea	rax, -1[r15]
	shr	rax, 63
	lea	rax, -1[rax+r15]
	cmp	rdi, r15
	jge	.L77
	sar	rax
	lea	r12, 0[0+r15*8]
	mov	r15, rax
.L16:
	lea	r14, 0[r13+r15*8]
	mov	rdx, rsi
	add	r12, r13
	mov	rcx, r14
	call	rbp
	test	al, al
	jne	.L78
	mov	rcx, QWORD PTR 72[rsp]
	mov	rax, r12
	mov	QWORD PTR [rax], rcx
	test	rdi, rdi
	je	.L79
.L17:
	sub	QWORD PTR 32[rsp], 8
	sub	rdi, 1
	jmp	.L20
.L35:
	mov	rcx, r13
	call	rbp
	test	al, al
	je	.L39
	mov	rax, QWORD PTR [rdi]
	mov	rdx, QWORD PTR 8[rdi]
	mov	QWORD PTR 8[rdi], rax
	mov	QWORD PTR [rdi], rdx
	jmp	.L37
.L5:
	movaps	xmm6, XMMWORD PTR 80[rsp]
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L36:
	mov	rdx, r12
	mov	rcx, r13
	call	rbp
	mov	rdx, QWORD PTR [rdi]
	test	al, al
	je	.L38
.L74:
	mov	rax, QWORD PTR -8[r14]
	mov	QWORD PTR [rdi], rax
	mov	QWORD PTR -8[r14], rdx
	jmp	.L37
.L39:
	mov	rdx, r12
	mov	rcx, rsi
	call	rbp
	mov	rdx, QWORD PTR [rdi]
	test	al, al
	jne	.L74
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR [rdi], rax
	mov	QWORD PTR [rsi], rdx
	jmp	.L37
.L38:
	mov	rax, QWORD PTR 8[rdi]
	mov	QWORD PTR 8[rdi], rdx
	mov	QWORD PTR [rdi], rax
	jmp	.L37
.L77:
	mov	rcx, QWORD PTR 72[rsp]
	mov	rax, r14
	mov	QWORD PTR [rax], rcx
	test	rdi, rdi
	jne	.L17
.L79:
	mov	r14, QWORD PTR 56[rsp]
	mov	rdi, r13
	mov	rax, r14
	sub	rax, r13
	lea	r13, -8[r14]
	cmp	rax, 8
	jle	.L5
	.p2align 4
	.p2align 3
.L34:
	mov	rax, QWORD PTR [rdi]
	movq	xmm6, QWORD PTR 0[r13]
	mov	QWORD PTR 0[r13], rax
	mov	rax, r13
	sub	rax, rdi
	mov	r15, rax
	mov	QWORD PTR 32[rsp], rax
	sar	r15, 3
	cmp	rax, 16
	jle	.L21
	lea	r12, -1[r15]
	xor	ebx, ebx
	sar	r12
	.p2align 4
	.p2align 3
.L22:
	lea	rcx, 1[rbx]
	lea	r14, [rcx+rcx]
	sal	rcx, 4
	lea	rdx, -8[rdi+r14*8]
	add	rcx, rdi
	call	rbp
	mov	rdx, rbx
	mov	rbx, r14
	movzx	eax, al
	sub	rbx, rax
	lea	r14, 0[0+rbx*8]
	lea	rax, [rdi+r14]
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR [rdi+rdx*8], rcx
	cmp	rbx, r12
	jl	.L22
	and	r15d, 1
	jne	.L72
	mov	rdx, QWORD PTR 32[rsp]
	sar	rdx, 4
	sub	rdx, 1
	cmp	rdx, rbx
	je	.L28
.L72:
	lea	r12, -1[rbx]
	movq	QWORD PTR 72[rsp], xmm6
	shr	r12, 63
	lea	r12, -1[rbx+r12]
	sar	r12
	test	rbx, rbx
	jne	.L32
	jmp	.L80
	.p2align 4,,10
	.p2align 3
.L82:
	mov	rax, QWORD PTR [r15]
	mov	QWORD PTR [r8], rax
	lea	rax, -1[r12]
	shr	rax, 63
	lea	rax, -1[rax+r12]
	test	r12, r12
	je	.L81
	sar	rax
	lea	r14, 0[0+r12*8]
	mov	r12, rax
.L32:
	lea	r15, [rdi+r12*8]
	mov	rdx, rsi
	mov	rcx, r15
	call	rbp
	lea	r8, [rdi+r14]
	test	al, al
	jne	.L82
.L31:
	mov	rax, QWORD PTR 72[rsp]
	mov	QWORD PTR [r8], rax
	cmp	QWORD PTR 32[rsp], 8
	jle	.L5
.L71:
	sub	r13, 8
	jmp	.L34
.L81:
	mov	r8, r15
	jmp	.L31
.L21:
	and	r15d, 1
	jne	.L73
	cmp	QWORD PTR 32[rsp], 16
	jne	.L73
	xor	ebx, ebx
	mov	rax, rdi
.L28:
	lea	rdx, 1[rbx+rbx]
	mov	r12, rbx
	mov	rcx, QWORD PTR [rdi+rdx*8]
	lea	r14, 0[0+rdx*8]
	mov	QWORD PTR [rax], rcx
	movq	QWORD PTR 72[rsp], xmm6
	jmp	.L32
.L73:
	movq	QWORD PTR 72[rsp], xmm6
	mov	r8, rdi
	jmp	.L31
.L8:
	test	BYTE PTR 40[rsp], 1
	jne	.L66
	cmp	rdi, QWORD PTR 48[rsp]
	jne	.L66
	mov	r14, rdi
.L12:
	lea	r9, [r14+r14]
	lea	r14, 1[r9]
	lea	r12, 0[0+r14*8]
	mov	r11, QWORD PTR 0[r13+r12]
	mov	QWORD PTR [r10], r11
	lea	r10, 0[r13+r12]
	jmp	.L11
.L66:
	movq	QWORD PTR 72[rsp], xmm6
.L14:
	mov	rax, QWORD PTR 72[rsp]
	mov	QWORD PTR [r10], rax
	jmp	.L17
.L80:
	mov	rdx, QWORD PTR 72[rsp]
	mov	QWORD PTR [rax], rdx
	jmp	.L71
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE
	.def	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE
_Z11sort_pointsRSt6vectorI5PointSaIS0_EE:
.LFB2348:
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
	sub	rsp, 64
	.seh_stackalloc	64
	movaps	XMMWORD PTR 48[rsp], xmm6
	.seh_savexmm	xmm6, 48
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbx, QWORD PTR [rcx]
	cmp	rbx, rsi
	je	.L83
	mov	rdi, rsi
	mov	r8, -2
	sub	rdi, rbx
	mov	rax, rdi
	sar	rax, 3
	je	.L85
	bsr	rax, rax
	cdqe
	lea	r8, [rax+rax]
.L85:
	lea	r9, _Z4by_xRK5PointS1_[rip]
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIP5PointSt6vectorIS2_SaIS2_EEEExNS0_5__ops15_Iter_comp_iterIPFbRKS2_SB_EEEEvT_SF_T0_T1_
	cmp	rdi, 128
	jg	.L113
	lea	rdi, 8[rbx]
	cmp	rsi, rdi
	je	.L83
	lea	rbp, 40[rsp]
	jmp	.L106
	.p2align 4,,10
	.p2align 3
.L114:
	mov	r8, rdi
	movd	xmm6, eax
	movd	xmm1, DWORD PTR 4[rdi]
	sub	r8, rbx
	mov	rax, r8
	punpckldq	xmm6, xmm1
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[rdi+rax]
	cmp	r8, 8
	jle	.L101
	mov	rdx, rbx
	call	memmove
.L102:
	add	rdi, 8
	movq	QWORD PTR [rbx], xmm6
	cmp	rsi, rdi
	je	.L83
.L106:
	mov	eax, DWORD PTR [rdi]
	cmp	eax, DWORD PTR [rbx]
	jl	.L114
	mov	rax, QWORD PTR [rdi]
	lea	rdx, -8[rdi]
	mov	QWORD PTR 40[rsp], rax
	jmp	.L104
	.p2align 4,,10
	.p2align 3
.L105:
	mov	rax, QWORD PTR [rdx]
	sub	rdx, 8
	mov	QWORD PTR 16[rdx], rax
.L104:
	mov	rcx, rbp
	call	_Z4by_xRK5PointS1_
	test	al, al
	jne	.L105
	mov	rax, QWORD PTR 40[rsp]
	add	rdi, 8
	mov	QWORD PTR 8[rdx], rax
	cmp	rsi, rdi
	jne	.L106
.L83:
	movaps	xmm6, XMMWORD PTR 48[rsp]
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L113:
	lea	rbp, 128[rbx]
	lea	rdi, 8[rbx]
	jmp	.L93
	.p2align 4,,10
	.p2align 3
.L116:
	mov	r8, rdi
	movd	xmm6, eax
	movd	xmm0, DWORD PTR 4[rdi]
	sub	r8, rbx
	mov	rax, r8
	punpckldq	xmm6, xmm0
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[rdi+rax]
	cmp	r8, 8
	jle	.L88
	mov	rdx, rbx
	call	memmove
.L89:
	add	rdi, 8
	movq	QWORD PTR [rbx], xmm6
	cmp	rbp, rdi
	je	.L115
.L93:
	mov	eax, DWORD PTR [rdi]
	cmp	eax, DWORD PTR [rbx]
	jl	.L116
	mov	rax, QWORD PTR [rdi]
	lea	rdx, -8[rdi]
	mov	QWORD PTR 40[rsp], rax
	jmp	.L91
	.p2align 4,,10
	.p2align 3
.L92:
	mov	rax, QWORD PTR [rdx]
	sub	rdx, 8
	mov	QWORD PTR 16[rdx], rax
.L91:
	lea	rcx, 40[rsp]
	call	_Z4by_xRK5PointS1_
	test	al, al
	jne	.L92
	mov	rax, QWORD PTR 40[rsp]
	add	rdi, 8
	mov	QWORD PTR 8[rdx], rax
	cmp	rbp, rdi
	jne	.L93
.L115:
	add	rbx, 120
	lea	r8, -8[rsi]
	lea	rcx, 40[rsp]
	cmp	rsi, rbp
	je	.L83
	.p2align 4
	.p2align 3
.L98:
	mov	rax, QWORD PTR 8[rbx]
	mov	rdx, rbx
	mov	QWORD PTR 40[rsp], rax
	jmp	.L96
	.p2align 4,,10
	.p2align 3
.L97:
	mov	rax, QWORD PTR [rdx]
	sub	rdx, 8
	mov	QWORD PTR 16[rdx], rax
.L96:
	call	_Z4by_xRK5PointS1_
	test	al, al
	jne	.L97
	mov	rax, QWORD PTR 40[rsp]
	add	rbx, 8
	mov	QWORD PTR 8[rdx], rax
	cmp	rbx, r8
	jne	.L98
	movaps	xmm6, XMMWORD PTR 48[rsp]
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L101:
	jne	.L102
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR [rcx], rax
	jmp	.L102
.L88:
	jne	.L89
	mov	rax, QWORD PTR [rbx]
	mov	QWORD PTR [rcx], rax
	jmp	.L89
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.section	.text.startup,"x"
.LHOTB0:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2349:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	call	__main
	mov	ecx, 32
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rbx, rax
	lea	rsi, 32[rax]
	mov	QWORD PTR 32[rsp], rax
	movabs	rdx, 38654705665
	movabs	rax, 4294967299
	mov	QWORD PTR 8[rbx], rdx
	mov	edx, 4
	lea	rcx, 32[rsp]
	mov	QWORD PTR [rbx], rax
	movabs	rax, 21474836482
	mov	QWORD PTR 16[rbx], rax
	mov	QWORD PTR 24[rbx], rdx
	mov	QWORD PTR 48[rsp], rsi
	mov	QWORD PTR 40[rsp], rsi
.LEHB1:
	call	_Z11sort_pointsRSt6vectorI5PointSaIS0_EE
.LEHE1:
	mov	edi, DWORD PTR [rbx]
	mov	rdx, rsi
	mov	rcx, rbx
	call	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev.isra.0
	mov	eax, edi
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L122:
	mov	rbx, rax
	jmp	.L119
.L121:
	mov	rdi, rax
	jmp	.L120
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2349:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2349-.LLSDACSB2349
.LLSDACSB2349:
	.uleb128 .LEHB0-.LFB2349
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L122-.LFB2349
	.uleb128 0
	.uleb128 .LEHB1-.LFB2349
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L121-.LFB2349
	.uleb128 0
.LLSDACSE2349:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 64
	.seh_savereg	rsi, 72
	.seh_savereg	rdi, 80
	.seh_endprologue
main.cold:
.L119:
	xor	ecx, ecx
	xor	edx, edx
	call	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev.isra.0
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
.L120:
	mov	rcx, rbx
	mov	rdx, rsi
	call	_ZNSt12_Vector_baseI5PointSaIS0_EED2Ev.isra.0
	mov	rcx, rdi
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2349:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2349-.LLSDACSBC2349
.LLSDACSBC2349:
	.uleb128 .LEHB2-.LCOLDB0
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC2349:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.section	.text.startup,"x"
.LHOTE0:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
