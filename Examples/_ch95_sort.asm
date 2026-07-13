	.file	"_ch95_sort.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0:
.LFB2596:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	r10, QWORD PTR 96[rsp]
	cmp	rdx, rcx
	mov	rbx, r8
	mov	rsi, r9
	je	.L2
	cmp	r9, r8
	jne	.L5
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L22:
	add	rbx, 4
	mov	eax, r11d
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	cmp	rsi, rbx
	je	.L2
.L23:
	cmp	rdx, rcx
	je	.L2
.L5:
	mov	r11d, DWORD PTR [rbx]
	mov	eax, DWORD PTR [rcx]
	cmp	eax, r11d
	jg	.L22
	mov	DWORD PTR [r10], eax
	add	rcx, 4
	add	r10, 4
	cmp	rsi, rbx
	jne	.L23
.L2:
	mov	rdi, rdx
	sub	rdi, rcx
	cmp	rdi, 4
	jle	.L7
	mov	rdx, rcx
	mov	r8, rdi
	mov	rcx, r10
	call	memmove
	mov	r10, rax
.L8:
	sub	rsi, rbx
	add	r10, rdi
	cmp	rsi, 4
	jle	.L9
	mov	rcx, r10
	mov	r8, rsi
	mov	rdx, rbx
	call	memmove
	mov	r10, rax
.L10:
	lea	rax, [r10+rsi]
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	jne	.L8
	mov	eax, DWORD PTR [rcx]
	mov	DWORD PTR [r10], eax
	jmp	.L8
	.p2align 4,,10
	.p2align 3
.L9:
	jne	.L10
	mov	eax, DWORD PTR [rbx]
	mov	DWORD PTR [r10], eax
	jmp	.L10
	.seh_endproc
	.p2align 4
	.def	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0:
.LFB2597:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	r10, QWORD PTR 96[rsp]
	mov	r11, rdx
	mov	rdi, r9
	mov	rdx, rcx
	cmp	rcx, r11
	mov	rbx, r8
	jne	.L25
	jmp	.L26
	.p2align 4,,10
	.p2align 3
.L32:
	mov	DWORD PTR [r10], eax
	add	rbx, 4
	add	r10, 4
	cmp	rdx, r11
	je	.L26
.L25:
	cmp	rdi, rbx
	je	.L41
	mov	eax, DWORD PTR [rbx]
	mov	ecx, DWORD PTR [rdx]
	cmp	eax, ecx
	jl	.L32
	add	rdx, 4
	mov	eax, ecx
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	cmp	rdx, r11
	jne	.L25
.L26:
	sub	rdi, rbx
	cmp	rdi, 4
	jle	.L36
	.p2align 4,,10
	.p2align 3
.L43:
	mov	rcx, r10
	mov	r8, rdi
	mov	rdx, rbx
	call	memmove
	mov	r10, rax
.L37:
	lea	rax, [r10+rdi]
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L41:
	mov	rsi, r11
	sub	rsi, rdx
	cmp	rsi, 4
	jle	.L42
	mov	rcx, r10
	mov	r8, rsi
	sub	rdi, rbx
	call	memmove
	mov	r10, rax
	add	r10, rsi
	cmp	rdi, 4
	jg	.L43
.L36:
	jne	.L37
	mov	eax, DWORD PTR [rbx]
	mov	DWORD PTR [r10], eax
	jmp	.L37
.L42:
	lea	rcx, [r10+rsi]
	jne	.L35
	mov	eax, DWORD PTR [rdx]
	mov	DWORD PTR [r10], eax
.L35:
	mov	r10, rcx
	jmp	.L26
	.seh_endproc
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB2598:
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
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rax, rdx
	mov	rsi, rcx
	mov	r11, rdx
	sub	rax, rcx
	mov	rdi, r8
	mov	rbp, rdx
	cmp	rax, 64
	jle	.L44
	lea	rbx, 4[rcx]
	test	r8, r8
	je	.L88
.L47:
	sar	rax, 3
	movq	xmm0, QWORD PTR [rsi]
	sub	rdi, 1
	lea	r9, [rsi+rax*4]
	mov	r8d, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR [r9]
	pshufd	xmm2, xmm0, 0xe5
	movd	ecx, xmm2
	movd	edx, xmm0
	pshufd	xmm1, xmm0, 225
	cmp	ecx, eax
	jge	.L74
	cmp	eax, r8d
	jl	.L80
	cmp	ecx, r8d
	jl	.L109
.L77:
	movq	QWORD PTR [rsi], xmm1
	mov	r9d, DWORD PTR -4[rbp]
.L76:
	cmp	ecx, edx
	mov	r10, rbp
	mov	rax, rbx
	jle	.L98
	.p2align 4,,10
	.p2align 3
.L111:
	add	rax, 4
	.p2align 4,,10
	.p2align 3
.L82:
	mov	r11, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jg	.L82
	cmp	ecx, r9d
	jge	.L83
.L112:
	lea	rax, -8[r10]
	.p2align 4,,10
	.p2align 3
.L84:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	ecx, r9d
	jl	.L84
	cmp	r11, r10
	jnb	.L110
.L86:
	mov	DWORD PTR [r11], r9d
	lea	rax, 4[r11]
	mov	r9d, DWORD PTR -4[r10]
	mov	DWORD PTR [r10], edx
	mov	edx, DWORD PTR 4[r11]
	mov	ecx, DWORD PTR [rsi]
	cmp	ecx, edx
	jg	.L111
.L98:
	cmp	ecx, r9d
	mov	r11, rax
	jl	.L112
	.p2align 4,,10
	.p2align 3
.L83:
	sub	r10, 4
	cmp	r11, r10
	jb	.L86
	.p2align 4,,10
	.p2align 3
.L110:
	mov	rcx, r11
	mov	r8, rdi
	mov	rdx, rbp
	mov	QWORD PTR 40[rsp], r11
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	r11, QWORD PTR 40[rsp]
	mov	rax, r11
	sub	rax, rsi
	cmp	rax, 64
	jle	.L44
	test	rdi, rdi
	je	.L88
	mov	rbp, r11
	jmp	.L47
.L74:
	cmp	ecx, r8d
	jl	.L77
	cmp	eax, r8d
	jge	.L80
.L109:
	mov	DWORD PTR [rsi], r8d
	mov	r9d, edx
	mov	DWORD PTR -4[rbp], edx
	mov	ecx, DWORD PTR [rsi]
	mov	edx, DWORD PTR 4[rsi]
	jmp	.L76
.L80:
	mov	DWORD PTR [rsi], eax
	mov	DWORD PTR [r9], edx
	mov	edx, DWORD PTR 4[rsi]
	mov	ecx, DWORD PTR [rsi]
	mov	r9d, DWORD PTR -4[rbp]
	jmp	.L76
.L58:
	sub	r11, 4
	.p2align 4,,10
	.p2align 3
.L73:
	mov	r9, r11
	mov	eax, DWORD PTR [rsi]
	sub	r9, rsi
	mov	r8d, DWORD PTR [r11]
	mov	r12, r9
	sar	r12, 2
	lea	rdx, -1[r12]
	mov	DWORD PTR [r11], eax
	mov	r14, r12
	mov	rax, rdx
	and	r14d, 1
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r9, 8
	mov	r13, rax
	jle	.L61
	xor	r10d, r10d
	jmp	.L63
	.p2align 4,,10
	.p2align 3
.L95:
	mov	r10, rax
.L63:
	lea	rdx, 1[r10]
	lea	rax, [rdx+rdx]
	lea	rbx, -1[rax]
	lea	rdi, [rsi+rbx*4]
	lea	rdx, [rsi+rdx*8]
	mov	ebp, DWORD PTR [rdi]
	mov	ecx, DWORD PTR [rdx]
	cmp	ebp, ecx
	jle	.L62
	mov	ecx, ebp
	mov	rdx, rdi
	mov	rax, rbx
.L62:
	cmp	rax, r13
	mov	DWORD PTR [rsi+r10*4], ecx
	jl	.L95
	test	r14, r14
	je	.L67
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L71
	jmp	.L113
	.p2align 4,,10
	.p2align 3
.L115:
	mov	DWORD PTR [rdx], r10d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	rcx, rcx
	mov	rdx, rax
	mov	rax, rcx
	je	.L114
	mov	rcx, rdx
.L71:
	lea	rbx, [rsi+rcx*4]
	mov	r10d, DWORD PTR [rbx]
	lea	rdx, [rsi+rax*4]
	cmp	r8d, r10d
	jg	.L115
.L66:
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L73
.L44:
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L88:
	sar	rax, 2
	lea	rbp, -2[rax]
	lea	rbx, -1[rax]
	sar	rbp
	not	rax
	sar	rbx
	mov	r9d, eax
	mov	r8, rbp
	lea	rdi, [rsi+rbp*4]
	and	r9d, 1
	cmp	r8, rbx
	mov	r10d, DWORD PTR [rdi]
	mov	r12, rdi
	jge	.L92
.L119:
	mov	rcx, r8
	jmp	.L50
	.p2align 4,,10
	.p2align 3
.L93:
	mov	rcx, rax
.L50:
	lea	rdx, 1[rcx]
	lea	rax, [rdx+rdx]
	lea	r13, -1[rax]
	lea	r14, [rsi+r13*4]
	lea	r12, [rsi+rdx*8]
	mov	r15d, DWORD PTR [r14]
	mov	edx, DWORD PTR [r12]
	cmp	r15d, edx
	jle	.L49
	mov	edx, r15d
	mov	r12, r14
	mov	rax, r13
.L49:
	cmp	rax, rbx
	mov	DWORD PTR [rsi+rcx*4], edx
	jl	.L93
.L48:
	cmp	rbp, rax
	jne	.L100
	test	r9b, r9b
	jne	.L51
.L100:
	lea	rcx, -1[rax]
	sar	rcx
	cmp	r8, rax
	jl	.L56
	jmp	.L116
	.p2align 4,,10
	.p2align 3
.L118:
	mov	DWORD PTR [rax], edx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r8, rcx
	mov	rdx, rax
	mov	rax, rcx
	jge	.L117
	mov	rcx, rdx
.L56:
	lea	r12, [rsi+rcx*4]
	mov	edx, DWORD PTR [r12]
	lea	rax, [rsi+rax*4]
	cmp	r10d, edx
	jg	.L118
.L55:
	test	r8, r8
	mov	DWORD PTR [rax], r10d
	je	.L58
.L57:
	sub	r8, 1
	sub	rdi, 4
	mov	r10d, DWORD PTR [rdi]
	cmp	r8, rbx
	mov	r12, rdi
	jl	.L119
.L92:
	mov	rax, r8
	jmp	.L48
.L117:
	mov	rax, r12
	jmp	.L55
.L114:
	mov	rdx, rbx
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L73
	jmp	.L44
.L67:
	lea	rcx, -2[r12]
	sar	rcx
	cmp	rcx, rax
	je	.L70
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L71
	jmp	.L66
	.p2align 4,,10
	.p2align 3
.L65:
	cmp	rdx, 2
	mov	rdx, rsi
	ja	.L66
	xor	eax, eax
.L70:
	lea	r10, 1[rax+rax]
	mov	ecx, DWORD PTR [rsi+r10*4]
	mov	DWORD PTR [rdx], ecx
	mov	rcx, rax
	mov	rax, r10
	jmp	.L71
.L61:
	test	r14, r14
	je	.L65
	mov	rdx, rsi
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L73
	jmp	.L44
	.p2align 4,,10
	.p2align 3
.L51:
	lea	rcx, [rax+rax]
	lea	rax, 1[rcx]
	sar	rcx
	lea	rdx, [rsi+rax*4]
	cmp	r8, rax
	mov	r13d, DWORD PTR [rdx]
	mov	DWORD PTR [r12], r13d
	mov	r12, rdx
	jl	.L56
.L116:
	mov	DWORD PTR [r12], r10d
	jmp	.L57
.L113:
	mov	DWORD PTR [rdx], r8d
	sub	r11, 4
	jmp	.L73
	.seh_endproc
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_:
.LFB2435:
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
	mov	rdi, rcx
	mov	r12, rdx
	sub	rax, rcx
	mov	rbp, r8
	mov	ebx, r9d
	cmp	rax, 64
	mov	r11, rdx
	jle	.L120
	lea	rsi, 4[rcx]
	test	r8, r8
	je	.L164
.L123:
	sar	rax, 3
	movq	xmm0, QWORD PTR [rdi]
	sub	rbp, 1
	lea	r9, [rdi+rax*4]
	mov	ecx, DWORD PTR -4[r11]
	mov	eax, DWORD PTR [r9]
	pshufd	xmm2, xmm0, 0xe5
	movd	r8d, xmm2
	movd	edx, xmm0
	pshufd	xmm1, xmm0, 225
	cmp	r8d, eax
	jle	.L150
	cmp	eax, ecx
	jg	.L156
	cmp	r8d, ecx
	jg	.L185
.L153:
	movq	QWORD PTR [rdi], xmm1
	mov	ecx, DWORD PTR -4[r11]
.L152:
	cmp	edx, r8d
	mov	r10, r11
	mov	rax, rsi
	jle	.L174
	.p2align 4,,10
	.p2align 3
.L187:
	add	rax, 4
	.p2align 4,,10
	.p2align 3
.L158:
	mov	r9, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	r8d, edx
	jl	.L158
	cmp	ecx, r8d
	mov	r12, r9
	jge	.L159
.L188:
	lea	rax, -8[r10]
	.p2align 4,,10
	.p2align 3
.L160:
	mov	r10, rax
	mov	ecx, DWORD PTR [rax]
	sub	rax, 4
	cmp	r8d, ecx
	jg	.L160
	cmp	r12, r10
	jnb	.L186
.L162:
	mov	DWORD PTR [r12], ecx
	lea	rax, 4[r12]
	mov	ecx, DWORD PTR -4[r10]
	mov	DWORD PTR [r10], edx
	mov	r8d, DWORD PTR [rdi]
	mov	edx, DWORD PTR 4[r12]
	cmp	edx, r8d
	jg	.L187
.L174:
	cmp	ecx, r8d
	mov	r12, rax
	jl	.L188
	.p2align 4,,10
	.p2align 3
.L159:
	sub	r10, 4
	cmp	r12, r10
	jb	.L162
	.p2align 4,,10
	.p2align 3
.L186:
	mov	r9d, ebx
	mov	r8, rbp
	mov	rdx, r11
	mov	rcx, r12
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_
	mov	rax, r12
	sub	rax, rdi
	cmp	rax, 64
	jle	.L120
	test	rbp, rbp
	je	.L164
	mov	r11, r12
	jmp	.L123
.L150:
	cmp	r8d, ecx
	jg	.L153
	cmp	eax, ecx
	jle	.L156
.L185:
	mov	DWORD PTR [rdi], ecx
	mov	ecx, edx
	mov	DWORD PTR -4[r11], edx
	mov	r8d, DWORD PTR [rdi]
	mov	edx, DWORD PTR 4[rdi]
	jmp	.L152
.L156:
	mov	DWORD PTR [rdi], eax
	mov	DWORD PTR [r9], edx
	mov	r8d, DWORD PTR [rdi]
	mov	edx, DWORD PTR 4[rdi]
	mov	ecx, DWORD PTR -4[r11]
	jmp	.L152
.L134:
	lea	r9, -4[r12]
	.p2align 4,,10
	.p2align 3
.L149:
	mov	r10, r9
	mov	eax, DWORD PTR [rdi]
	sub	r10, rdi
	mov	r8d, DWORD PTR [r9]
	mov	r12, r10
	sar	r12, 2
	lea	rdx, -1[r12]
	mov	DWORD PTR [r9], eax
	mov	r14, r12
	mov	rax, rdx
	and	r14d, 1
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r10, 8
	mov	r13, rax
	jle	.L137
	xor	r11d, r11d
	jmp	.L139
	.p2align 4,,10
	.p2align 3
.L171:
	mov	r11, rax
.L139:
	lea	rdx, 1[r11]
	lea	rax, [rdx+rdx]
	lea	rbx, -1[rax]
	lea	rsi, [rdi+rbx*4]
	lea	rdx, [rdi+rdx*8]
	mov	ebp, DWORD PTR [rsi]
	mov	ecx, DWORD PTR [rdx]
	cmp	ecx, ebp
	jle	.L138
	mov	ecx, ebp
	mov	rdx, rsi
	mov	rax, rbx
.L138:
	cmp	rax, r13
	mov	DWORD PTR [rdi+r11*4], ecx
	jl	.L171
	test	r14, r14
	je	.L143
	lea	r11, -1[rax]
	mov	rcx, r11
	shr	rcx, 63
	add	rcx, r11
	sar	rcx
	test	rax, rax
	jne	.L147
	jmp	.L189
	.p2align 4,,10
	.p2align 3
.L191:
	mov	DWORD PTR [rdx], r11d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	rcx, rcx
	mov	rdx, rax
	mov	rax, rcx
	je	.L190
	mov	rcx, rdx
.L147:
	lea	rbx, [rdi+rcx*4]
	mov	r11d, DWORD PTR [rbx]
	lea	rdx, [rdi+rax*4]
	cmp	r8d, r11d
	jl	.L191
.L142:
	sub	r9, 4
	cmp	r10, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L149
.L120:
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
.L164:
	sar	rax, 2
	lea	rsi, -2[rax]
	lea	r11, -1[rax]
	sar	rsi
	not	rax
	sar	r11
	mov	r9d, eax
	mov	r8, rsi
	lea	rbx, [rdi+rsi*4]
	and	r9d, 1
	cmp	r8, r11
	mov	r10d, DWORD PTR [rbx]
	mov	rbp, rbx
	jge	.L168
.L195:
	mov	rcx, r8
	jmp	.L126
	.p2align 4,,10
	.p2align 3
.L169:
	mov	rcx, rax
.L126:
	lea	rdx, 1[rcx]
	lea	rax, [rdx+rdx]
	lea	r13, -1[rax]
	lea	r14, [rdi+r13*4]
	lea	rbp, [rdi+rdx*8]
	mov	r15d, DWORD PTR [r14]
	mov	edx, DWORD PTR 0[rbp]
	cmp	edx, r15d
	jle	.L125
	mov	edx, r15d
	mov	rbp, r14
	mov	rax, r13
.L125:
	cmp	rax, r11
	mov	DWORD PTR [rdi+rcx*4], edx
	jl	.L169
.L124:
	cmp	rsi, rax
	jne	.L176
	test	r9b, r9b
	jne	.L127
.L176:
	lea	rcx, -1[rax]
	sar	rcx
	cmp	r8, rax
	jl	.L132
	jmp	.L192
	.p2align 4,,10
	.p2align 3
.L194:
	mov	DWORD PTR [rax], edx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r8, rcx
	mov	rdx, rax
	mov	rax, rcx
	jge	.L193
	mov	rcx, rdx
.L132:
	lea	rbp, [rdi+rcx*4]
	mov	edx, DWORD PTR 0[rbp]
	lea	rax, [rdi+rax*4]
	cmp	r10d, edx
	jl	.L194
.L131:
	test	r8, r8
	mov	DWORD PTR [rax], r10d
	je	.L134
.L133:
	sub	r8, 1
	sub	rbx, 4
	mov	r10d, DWORD PTR [rbx]
	cmp	r8, r11
	mov	rbp, rbx
	jl	.L195
.L168:
	mov	rax, r8
	jmp	.L124
.L193:
	mov	rax, rbp
	jmp	.L131
.L190:
	mov	rdx, rbx
	sub	r9, 4
	cmp	r10, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L149
	jmp	.L120
.L143:
	lea	rcx, -2[r12]
	sar	rcx
	cmp	rcx, rax
	je	.L146
	lea	r11, -1[rax]
	mov	rcx, r11
	shr	rcx, 63
	add	rcx, r11
	sar	rcx
	test	rax, rax
	jne	.L147
	jmp	.L142
	.p2align 4,,10
	.p2align 3
.L141:
	cmp	rdx, 2
	mov	rdx, rdi
	ja	.L142
	xor	eax, eax
.L146:
	lea	r11, 1[rax+rax]
	mov	ecx, DWORD PTR [rdi+r11*4]
	mov	DWORD PTR [rdx], ecx
	mov	rcx, rax
	mov	rax, r11
	jmp	.L147
.L137:
	test	r14, r14
	je	.L141
	mov	rdx, rdi
	sub	r9, 4
	cmp	r10, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L149
	jmp	.L120
	.p2align 4,,10
	.p2align 3
.L127:
	lea	rcx, [rax+rax]
	lea	rax, 1[rcx]
	sar	rcx
	lea	rdx, [rdi+rax*4]
	cmp	r8, rax
	mov	r13d, DWORD PTR [rdx]
	mov	DWORD PTR 0[rbp], r13d
	mov	rbp, rdx
	jl	.L132
.L192:
	mov	DWORD PTR 0[rbp], r10d
	jmp	.L133
.L189:
	mov	DWORD PTR [rdx], r8d
	sub	r9, 4
	jmp	.L149
	.seh_endproc
	.p2align 4
	.def	_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB2612:
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
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	r15, rdx
	mov	QWORD PTR 144[rsp], rcx
	mov	rbp, rdx
	sub	r15, rcx
	mov	QWORD PTR 160[rsp], r8
	mov	rax, r15
	mov	r13, r15
	sar	rax, 2
	add	r13, r8
	cmp	r15, 24
	mov	QWORD PTR 56[rsp], rax
	jle	.L197
	mov	rdi, rcx
	mov	esi, 4
	.p2align 4,,10
	.p2align 3
.L205:
	mov	rbx, rdi
	add	rdi, 28
	lea	r12, -24[rdi]
	jmp	.L204
	.p2align 4,,10
	.p2align 3
.L236:
	mov	r8, r12
	sub	r8, rbx
	cmp	r8, 4
	jle	.L199
	mov	rcx, rsi
	mov	rdx, rbx
	sub	rcx, r8
	add	rcx, r12
	call	memmove
.L200:
	add	r12, 4
	mov	DWORD PTR -28[rdi], r14d
	cmp	r12, rdi
	je	.L235
.L204:
	mov	r14d, DWORD PTR [r12]
	mov	rcx, r12
	mov	eax, DWORD PTR -28[rdi]
	cmp	r14d, eax
	jl	.L236
	mov	edx, DWORD PTR -4[r12]
	lea	rax, -4[r12]
	cmp	r14d, edx
	jge	.L202
	.p2align 4,,10
	.p2align 3
.L203:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r14d, edx
	jl	.L203
.L202:
	add	r12, 4
	mov	DWORD PTR [rcx], r14d
	cmp	r12, rdi
	jne	.L204
.L235:
	mov	rax, rbp
	sub	rax, rdi
	cmp	rax, 24
	jg	.L205
	cmp	rbp, rdi
	je	.L209
	add	rbx, 32
	cmp	rbp, rbx
	je	.L209
.L222:
	mov	esi, 4
	jmp	.L216
	.p2align 4,,10
	.p2align 3
.L237:
	mov	r8, rbx
	sub	r8, rdi
	cmp	r8, 4
	jle	.L211
	mov	rcx, rsi
	mov	rdx, rdi
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L212:
	add	rbx, 4
	mov	DWORD PTR [rdi], r12d
	cmp	rbp, rbx
	je	.L209
.L216:
	mov	r12d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR [rdi]
	cmp	r12d, eax
	jl	.L237
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	r12d, edx
	jge	.L214
	.p2align 4,,10
	.p2align 3
.L215:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L215
.L214:
	add	rbx, 4
	mov	DWORD PTR [rcx], r12d
	cmp	rbp, rbx
	jne	.L216
.L209:
	cmp	r15, 28
	mov	ebx, 7
	mov	esi, 28
	jle	.L196
	.p2align 4,,10
	.p2align 3
.L207:
	lea	rdi, [rbx+rbx]
	cmp	QWORD PTR 56[rsp], rdi
	jl	.L224
	mov	rcx, QWORD PTR 160[rsp]
	lea	r12, 0[0+rbx*8]
	mov	r14, rsi
	mov	r15, QWORD PTR 144[rsp]
	sub	r14, r12
	.p2align 4,,10
	.p2align 3
.L219:
	mov	rax, r15
	add	r15, r12
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, [r15+r14]
	mov	rcx, rax
	mov	r9, r15
	mov	r8, rdx
	call	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	mov	rcx, rax
	mov	rax, rbp
	sub	rax, r15
	sar	rax, 2
	cmp	rdi, rax
	jle	.L219
.L218:
	cmp	rbx, rax
	mov	QWORD PTR 32[rsp], rcx
	mov	r9, rbp
	mov	rcx, r15
	cmovle	rax, rbx
	mov	rbx, rsi
	lea	rdx, [r15+rax*4]
	mov	r8, rdx
	call	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	cmp	QWORD PTR 56[rsp], rsi
	mov	rcx, QWORD PTR 144[rsp]
	jl	.L220
	mov	r14, QWORD PTR 160[rsp]
	sal	rsi, 2
	lea	r12, 0[0+rdi*4]
	sub	r12, rsi
	.p2align 4,,10
	.p2align 3
.L221:
	mov	rax, r14
	add	r14, rsi
	mov	QWORD PTR 32[rsp], rcx
	lea	rdx, [r14+r12]
	mov	rcx, rax
	mov	r9, r14
	mov	r8, rdx
	call	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	mov	rcx, rax
	mov	rax, r13
	sub	rax, r14
	sar	rax, 2
	cmp	rbx, rax
	jle	.L221
	cmp	rax, rdi
	mov	QWORD PTR 32[rsp], rcx
	mov	r9, r13
	mov	rcx, r14
	cmovg	rax, rdi
	lea	rdx, [r14+rax*4]
	mov	r8, rdx
	call	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	cmp	QWORD PTR 56[rsp], rbx
	jg	.L207
.L196:
	add	rsp, 72
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
.L199:
	jne	.L200
	mov	DWORD PTR [r12], eax
	jmp	.L200
.L220:
	mov	rax, QWORD PTR 56[rsp]
	mov	r9, r13
	mov	rcx, QWORD PTR 160[rsp]
	cmp	rax, rdi
	cmovle	rdi, rax
	mov	rax, QWORD PTR 160[rsp]
	lea	rdx, [rax+rdi*4]
	mov	rax, QWORD PTR 144[rsp]
	mov	r8, rdx
	mov	QWORD PTR 32[rsp], rax
	call	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	jmp	.L196
.L224:
	mov	rax, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 160[rsp]
	mov	r15, QWORD PTR 144[rsp]
	jmp	.L218
.L211:
	jne	.L212
	mov	DWORD PTR [rbx], eax
	jmp	.L212
.L197:
	cmp	rdx, QWORD PTR 144[rsp]
	je	.L196
	mov	rax, QWORD PTR 144[rsp]
	lea	rbx, 4[rax]
	mov	rdi, rax
	cmp	rdx, rbx
	jne	.L222
	jmp	.L196
	.seh_endproc
	.p2align 4
	.def	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0
_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0:
.LFB2617:
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
	cmp	rcx, rdx
	mov	rbx, rcx
	mov	rax, r8
	je	.L240
	cmp	rdx, r8
	mov	rax, rcx
	je	.L240
	mov	rax, r8
	mov	r10, rdx
	sub	r8, rdx
	lea	rsi, [rcx+r8]
	sub	rax, rcx
	sub	r10, rcx
	sar	rax, 2
	mov	r9, r10
	sar	r9, 2
	mov	r11, rax
	sub	r11, r9
	cmp	r9, r11
	je	.L265
	.p2align 4,,10
	.p2align 3
.L244:
	mov	r10, rax
	sub	r10, r9
	cmp	r9, r10
	jge	.L245
.L267:
	cmp	r9, 1
	je	.L266
	lea	rdx, [rbx+r9*4]
	test	r10, r10
	jle	.L249
	xor	ecx, ecx
	.p2align 4,,10
	.p2align 3
.L250:
	mov	r8d, DWORD PTR [rbx+rcx*4]
	mov	r11d, DWORD PTR [rdx+rcx*4]
	mov	DWORD PTR [rbx+rcx*4], r11d
	mov	DWORD PTR [rdx+rcx*4], r8d
	add	rcx, 1
	cmp	r10, rcx
	jne	.L250
	lea	rbx, [rbx+r10*4]
.L249:
	cqo
	idiv	r9
	test	rdx, rdx
	je	.L264
	mov	rax, r9
	sub	r9, rdx
	mov	r10, rax
	sub	r10, r9
	cmp	r9, r10
	jl	.L267
.L245:
	lea	rcx, [rbx+rax*4]
	cmp	r10, 1
	je	.L268
	lea	r11, [rbx+r9*4]
	test	r9, r9
	jle	.L258
	mov	r8, -4
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L257:
	mov	edi, DWORD PTR [r11+r8]
	add	rdx, 1
	mov	ebp, DWORD PTR [rcx+r8]
	mov	DWORD PTR [r11+r8], ebp
	mov	DWORD PTR [rcx+r8], edi
	sub	r8, 4
	cmp	r9, rdx
	jne	.L257
.L256:
	cqo
	idiv	r10
	test	rdx, rdx
	mov	r9, rdx
	je	.L264
	mov	rax, r10
	jmp	.L244
.L265:
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L243:
	mov	r8d, DWORD PTR [rcx+rax]
	mov	r9d, DWORD PTR [rdx+rax]
	mov	DWORD PTR [rcx+rax], r9d
	mov	DWORD PTR [rdx+rax], r8d
	add	rax, 4
	cmp	r10, rax
	jne	.L243
	mov	rax, rdx
.L240:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L258:
	mov	rbx, r11
	jmp	.L256
.L264:
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L268:
	lea	r8, -4[rcx]
	mov	edi, DWORD PTR -4[rcx]
	sub	r8, rbx
	cmp	r8, 4
	jle	.L254
	sub	rcx, r8
	mov	rdx, rbx
	call	memmove
.L255:
	mov	DWORD PTR [rbx], edi
	mov	rax, rsi
	jmp	.L240
.L266:
	mov	ebp, DWORD PTR [rbx]
	lea	rdx, 4[rbx]
	sal	rax, 2
	lea	r8, -4[rax]
	lea	rdi, [rbx+rax]
	cmp	r8, 4
	jle	.L247
	mov	rcx, rbx
	call	memmove
.L248:
	mov	DWORD PTR -4[rdi], ebp
	mov	rax, rsi
	jmp	.L240
.L254:
	jne	.L255
	mov	eax, DWORD PTR [rbx]
	mov	DWORD PTR -4[rcx], eax
	jmp	.L255
.L247:
	jne	.L248
	mov	eax, DWORD PTR 4[rbx]
	mov	DWORD PTR [rbx], eax
	jmp	.L248
	.seh_endproc
	.p2align 4
	.def	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0:
.LFB2618:
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
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbp, QWORD PTR 160[rsp]
	test	r9, r9
	mov	r12, rcx
	mov	r13, r8
	mov	rbx, r9
	je	.L269
	test	rbp, rbp
	je	.L269
	lea	rax, [r9+rbp]
	cmp	rax, 2
	je	.L286
	cmp	r9, rbp
	jle	.L272
	mov	r10, r9
	mov	rsi, rdx
	shr	r10, 63
	add	r10, r9
	sar	r10
	lea	rdi, [rcx+r10*4]
	mov	rcx, r8
	mov	r14, r10
	sub	rcx, rdx
	mov	r9d, DWORD PTR [rdi]
	mov	rax, rcx
	sar	rax, 2
	test	rcx, rcx
	jg	.L275
	jmp	.L280
	.p2align 4,,10
	.p2align 3
.L288:
	lea	rsi, 4[r8]
	sub	rax, rcx
	sub	rax, 1
	test	rax, rax
	jle	.L287
.L275:
	mov	rcx, rax
	sar	rcx
	lea	r8, [rsi+rcx*4]
	cmp	r9d, DWORD PTR [r8]
	jg	.L288
	mov	rax, rcx
	test	rax, rax
	jg	.L275
.L287:
	mov	r9, rsi
	sub	r9, rdx
	mov	r15, r9
	sar	r15, 2
	sub	rbp, r15
.L273:
	sub	rbx, r10
	jmp	.L276
	.p2align 4,,10
	.p2align 3
.L272:
	mov	r11, rbp
	mov	rcx, rdx
	mov	rdi, r12
	shr	r11, 63
	sub	rcx, r12
	add	r11, rbp
	mov	rax, rcx
	sar	r11
	sar	rax, 2
	test	rcx, rcx
	lea	rsi, [rdx+r11*4]
	mov	r15, r11
	mov	r10d, DWORD PTR [rsi]
	jg	.L279
	jmp	.L282
	.p2align 4,,10
	.p2align 3
.L290:
	lea	rdi, 4[r8]
	sub	rax, rcx
	sub	rax, 1
	test	rax, rax
	jle	.L289
.L279:
	mov	rcx, rax
	sar	rcx
	lea	r8, [rdi+rcx*4]
	cmp	DWORD PTR [r8], r10d
	jle	.L290
	mov	rax, rcx
	test	rax, rax
	jg	.L279
.L289:
	mov	r14, rdi
	sub	r14, r12
	sar	r14, 2
	sub	rbx, r14
.L277:
	sub	rbp, r11
.L276:
	mov	r8, rsi
	mov	rcx, rdi
	call	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0
	mov	QWORD PTR 32[rsp], r15
	mov	r9, r14
	mov	rdx, rdi
	mov	r15, rax
	mov	r8, rax
	mov	rcx, r12
	call	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
	mov	r9, rbx
	mov	r8, r13
	mov	rdx, rsi
	mov	rcx, r15
	mov	QWORD PTR 160[rsp], rbp
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	jmp	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
	.p2align 4,,10
	.p2align 3
.L286:
	mov	ecx, DWORD PTR [rdx]
	mov	eax, DWORD PTR [r12]
	cmp	ecx, eax
	jge	.L269
	mov	DWORD PTR [r12], ecx
	mov	DWORD PTR [rdx], eax
.L269:
	add	rsp, 56
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
.L280:
	xor	r15d, r15d
	jmp	.L273
	.p2align 4,,10
	.p2align 3
.L282:
	xor	r14d, r14d
	jmp	.L277
	.seh_endproc
	.p2align 4
	.def	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0:
.LFB2622:
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
	mov	r9, rdx
	mov	rdi, rcx
	mov	rbp, rdx
	sub	r9, rcx
	cmp	r9, 56
	jle	.L306
	sar	r9, 3
	lea	rbx, 0[0+r9*4]
	lea	rsi, [rcx+rbx]
	sar	rbx, 2
	mov	rdx, rsi
	call	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	mov	rdx, rbp
	mov	rcx, rsi
	call	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	mov	rax, rbp
	mov	r9, rbx
	mov	r8, rbp
	sub	rax, rsi
	mov	rdx, rsi
	mov	rcx, rdi
	sar	rax, 2
	mov	QWORD PTR 32[rsp], rax
	call	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
	nop
.L291:
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L306:
	cmp	rcx, rdx
	je	.L291
	lea	rbx, 4[rcx]
	cmp	rdx, rbx
	je	.L291
	mov	esi, DWORD PTR [rbx]
	mov	r12d, 4
	mov	rcx, rbx
	mov	eax, DWORD PTR [rdi]
	cmp	esi, eax
	jge	.L296
	.p2align 4,,10
	.p2align 3
.L307:
	mov	r8, rbx
	sub	r8, rdi
	cmp	r8, 4
	jle	.L297
	mov	rcx, r12
	mov	rdx, rdi
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L298:
	mov	DWORD PTR [rdi], esi
.L299:
	add	rbx, 4
	cmp	rbp, rbx
	je	.L291
	mov	esi, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR [rdi]
	cmp	esi, eax
	jl	.L307
.L296:
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	esi, edx
	jge	.L300
	.p2align 4,,10
	.p2align 3
.L301:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	esi, edx
	jl	.L301
.L300:
	mov	DWORD PTR [rcx], esi
	jmp	.L299
	.p2align 4,,10
	.p2align 3
.L297:
	jne	.L298
	mov	DWORD PTR [rbx], eax
	jmp	.L298
	.seh_endproc
	.p2align 4
	.def	_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0
_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0:
.LFB2623:
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
	cmp	r9, QWORD PTR 128[rsp]
	mov	r10, QWORD PTR 136[rsp]
	mov	rbp, rcx
	mov	rbx, rdx
	mov	r13, r8
	mov	r12, rdx
	mov	rsi, r8
	mov	rdi, rcx
	jg	.L309
	sub	rbx, rcx
	cmp	rbx, 4
	jle	.L310
	mov	rdx, rcx
	mov	r8, rbx
	mov	rcx, r10
	call	memmove
	mov	r10, rax
.L311:
	lea	r8, [r10+rbx]
	cmp	r10, r8
	jne	.L312
	jmp	.L308
	.p2align 4,,10
	.p2align 3
.L317:
	mov	DWORD PTR [rdi], eax
	add	r12, 4
	add	rdi, 4
	cmp	r10, r8
	je	.L308
.L312:
	cmp	r12, r13
	je	.L316
	mov	eax, DWORD PTR [r12]
	mov	edx, DWORD PTR [r10]
	cmp	eax, edx
	jl	.L317
	add	r10, 4
	mov	eax, edx
	add	rdi, 4
	mov	DWORD PTR -4[rdi], eax
	cmp	r10, r8
	jne	.L312
.L308:
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
.L309:
	mov	r12, r8
	sub	r12, rdx
	lea	rdi, [r10+r12]
	cmp	r12, 4
	jle	.L320
	mov	rcx, r10
	mov	r8, r12
	call	memmove
	cmp	rbp, rbx
	mov	r10, rax
	je	.L334
.L322:
	cmp	r10, rdi
	je	.L308
	lea	rax, -4[rbx]
	lea	rdx, -4[rdi]
	jmp	.L325
	.p2align 4,,10
	.p2align 3
.L336:
	cmp	rax, rbp
	mov	DWORD PTR -4[rsi], r9d
	je	.L335
	sub	rax, 4
.L329:
	mov	rsi, rcx
.L325:
	mov	r8d, DWORD PTR [rdx]
	lea	rcx, -4[rsi]
	mov	r9d, DWORD PTR [rax]
	cmp	r8d, r9d
	jl	.L336
	cmp	r10, rdx
	mov	DWORD PTR -4[rsi], r8d
	je	.L308
	sub	rdx, 4
	jmp	.L329
	.p2align 4,,10
	.p2align 3
.L316:
	cmp	r8, r10
	je	.L308
	sub	r8, r10
	cmp	r8, 4
	jle	.L319
	mov	rdx, r10
	mov	rcx, rdi
.L332:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	jmp	memmove
.L320:
	je	.L323
	cmp	rcx, rdx
	jne	.L322
	jmp	.L308
	.p2align 4,,10
	.p2align 3
.L310:
	jne	.L311
	mov	eax, DWORD PTR [rcx]
	mov	DWORD PTR [r10], eax
	jmp	.L311
	.p2align 4,,10
	.p2align 3
.L335:
	lea	r8, 4[rdx]
	sub	r8, r10
	cmp	r8, 4
	jle	.L328
	sub	rcx, r8
.L333:
	mov	rdx, r10
	jmp	.L332
.L323:
	mov	eax, DWORD PTR [rdx]
	cmp	rcx, rdx
	mov	DWORD PTR [r10], eax
	jne	.L322
	mov	DWORD PTR -4[r8], eax
	jmp	.L308
	.p2align 4,,10
	.p2align 3
.L334:
	mov	rcx, r13
	mov	r8, r12
	sub	rcx, r12
	jmp	.L333
.L319:
	jne	.L308
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR [rdi], eax
	jmp	.L308
.L328:
	jne	.L308
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR -8[rsi], eax
	jmp	.L308
	.seh_endproc
	.p2align 4
	.def	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0
_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0:
.LFB2626:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbx, rdx
	mov	rbp, r9
	mov	rdi, r8
	mov	r8, r9
	mov	rsi, rcx
	call	_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	r8, rbp
	mov	rdx, rdi
	mov	rcx, rbx
	call	_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	rax, rdi
	mov	r9, rbx
	mov	QWORD PTR 40[rsp], rbp
	sub	rax, rbx
	sub	r9, rsi
	mov	r8, rdi
	sar	rax, 2
	sar	r9, 2
	mov	rdx, rbx
	mov	QWORD PTR 32[rsp], rax
	mov	rcx, rsi
	call	_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0
	nop
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.p2align 4
	.def	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0:
.LFB2627:
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
	.seh_endprologue
	mov	rbp, QWORD PTR 224[rsp]
	mov	r15, QWORD PTR 240[rsp]
	mov	r14, QWORD PTR 232[rsp]
	cmp	r9, rbp
	mov	rax, rbp
	mov	r13, rcx
	mov	QWORD PTR 64[rsp], r8
	cmovle	rax, r9
	mov	r12, rdx
	mov	rbx, r9
	cmp	rax, r15
	jle	.L401
	cmp	r9, rbp
	jle	.L340
	mov	rdx, r9
	mov	rdi, r12
	shr	rdx, 63
	add	rdx, r9
	sar	rdx
	lea	rsi, [rcx+rdx*4]
	mov	rcx, QWORD PTR 64[rsp]
	mov	QWORD PTR 80[rsp], rdx
	mov	r8d, DWORD PTR [rsi]
	sub	rcx, r12
	mov	rax, rcx
	sar	rax, 2
	test	rcx, rcx
	jg	.L343
	jmp	.L379
	.p2align 4,,10
	.p2align 3
.L403:
	lea	rdi, 4[r9]
	sub	rax, rcx
	sub	rax, 1
	test	rax, rax
	jle	.L402
.L343:
	mov	rcx, rax
	sar	rcx
	lea	r9, [rdi+rcx*4]
	cmp	r8d, DWORD PTR [r9]
	jg	.L403
	mov	rax, rcx
	test	rax, rax
	jg	.L343
.L402:
	mov	r9, rdi
	sub	r9, r12
	sar	r9, 2
	sub	rbp, r9
.L341:
	sub	rbx, rdx
	cmp	r9, rbx
	jge	.L348
.L407:
	cmp	r15, r9
	jl	.L348
	test	r9, r9
	mov	QWORD PTR 72[rsp], rsi
	jne	.L404
.L349:
	mov	r12, QWORD PTR 72[rsp]
	mov	QWORD PTR 32[rsp], r9
	mov	rdx, rsi
	mov	rcx, r13
	mov	r9, QWORD PTR 80[rsp]
	mov	QWORD PTR 48[rsp], r15
	mov	QWORD PTR 40[rsp], r14
	mov	r8, r12
	call	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
	mov	r8, QWORD PTR 64[rsp]
	mov	r9, rbx
	mov	rdx, rdi
	mov	rcx, r12
	mov	QWORD PTR 240[rsp], r15
	mov	QWORD PTR 232[rsp], r14
	mov	QWORD PTR 224[rsp], rbp
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	jmp	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
	.p2align 4,,10
	.p2align 3
.L340:
	mov	rcx, rbp
	mov	rsi, r13
	shr	rcx, 63
	add	rcx, rbp
	sar	rcx
	lea	rdi, [rdx+rcx*4]
	sub	rdx, r13
	mov	r9, rcx
	mov	rax, rdx
	mov	r8d, DWORD PTR [rdi]
	sar	rax, 2
	test	rdx, rdx
	jg	.L347
	jmp	.L381
	.p2align 4,,10
	.p2align 3
.L406:
	lea	rsi, 4[r10]
	sub	rax, rdx
	sub	rax, 1
	test	rax, rax
	jle	.L405
.L347:
	mov	rdx, rax
	sar	rdx
	lea	r10, [rsi+rdx*4]
	cmp	r8d, DWORD PTR [r10]
	jge	.L406
	mov	rax, rdx
	test	rax, rax
	jg	.L347
.L405:
	mov	rax, rsi
	sub	rax, r13
	sar	rax, 2
	mov	QWORD PTR 80[rsp], rax
	sub	rbx, rax
.L345:
	sub	rbp, rcx
	cmp	r9, rbx
	jl	.L407
.L348:
	cmp	r15, rbx
	jl	.L364
	test	rbx, rbx
	mov	QWORD PTR 72[rsp], rdi
	je	.L349
	mov	rax, r12
	mov	r11, rdi
	sub	rax, rsi
	sub	r11, r12
	cmp	rax, 4
	mov	QWORD PTR 88[rsp], rax
	jle	.L365
	mov	r8, rax
	mov	rdx, rsi
	mov	rcx, r14
	mov	QWORD PTR 104[rsp], r11
	mov	QWORD PTR 96[rsp], r9
	call	memmove
	mov	rax, QWORD PTR 88[rsp]
	mov	r11, QWORD PTR 104[rsp]
	mov	r9, QWORD PTR 96[rsp]
	neg	rax
	cmp	r11, 4
	mov	QWORD PTR 72[rsp], rax
	jle	.L408
	mov	r8, r11
	mov	rdx, r12
	mov	rcx, rsi
	mov	QWORD PTR 96[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 96[rsp]
.L376:
	mov	rax, QWORD PTR 72[rsp]
	mov	rdx, r14
	mov	QWORD PTR 96[rsp], r9
	mov	r8, QWORD PTR 88[rsp]
	add	rax, rdi
	mov	rcx, rax
	mov	QWORD PTR 72[rsp], rax
	call	memmove
	mov	r9, QWORD PTR 96[rsp]
	jmp	.L349
	.p2align 4,,10
	.p2align 3
.L401:
	mov	QWORD PTR 232[rsp], r14
	mov	QWORD PTR 224[rsp], rbp
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	jmp	_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0
	.p2align 4,,10
	.p2align 3
.L364:
	mov	r8, rdi
	mov	rdx, r12
	mov	rcx, rsi
	mov	QWORD PTR 88[rsp], r9
	call	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0
	mov	r9, QWORD PTR 88[rsp]
	mov	QWORD PTR 72[rsp], rax
	jmp	.L349
	.p2align 4,,10
	.p2align 3
.L404:
	mov	r8, rdi
	mov	r10, r12
	sub	r8, r12
	sub	r10, rsi
	cmp	r8, 4
	mov	QWORD PTR 72[rsp], r8
	jle	.L350
	mov	rdx, r12
	mov	rcx, r14
	mov	QWORD PTR 96[rsp], r10
	mov	QWORD PTR 88[rsp], r9
	call	memmove
	mov	r10, QWORD PTR 96[rsp]
	mov	r9, QWORD PTR 88[rsp]
	cmp	r10, 4
	jle	.L409
	mov	rcx, rdi
	mov	r8, r10
	mov	rdx, rsi
	mov	QWORD PTR 88[rsp], r9
	sub	rcx, r10
	call	memmove
	mov	r9, QWORD PTR 88[rsp]
.L356:
	mov	r8, QWORD PTR 72[rsp]
	mov	rdx, r14
	mov	rcx, rsi
	mov	QWORD PTR 88[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 88[rsp]
.L358:
	mov	rax, QWORD PTR 72[rsp]
	add	rax, rsi
	mov	QWORD PTR 72[rsp], rax
	jmp	.L349
	.p2align 4,,10
	.p2align 3
.L379:
	xor	r9d, r9d
	jmp	.L341
	.p2align 4,,10
	.p2align 3
.L381:
	mov	QWORD PTR 80[rsp], 0
	jmp	.L345
.L350:
	je	.L353
	cmp	r10, 4
	jle	.L354
	mov	rcx, rdi
	mov	r8, r10
	mov	rdx, rsi
	mov	QWORD PTR 88[rsp], r9
	sub	rcx, r10
	call	memmove
	mov	r9, QWORD PTR 88[rsp]
	jmp	.L358
.L409:
	jne	.L356
	mov	eax, DWORD PTR [rsi]
	mov	DWORD PTR -4[rdi], eax
	jmp	.L356
.L365:
	je	.L368
	mov	r10, QWORD PTR 88[rsp]
	neg	r10
	cmp	r11, 4
	jle	.L410
	mov	r8, r11
	mov	rdx, r12
	mov	rcx, rsi
	mov	QWORD PTR 88[rsp], r10
	mov	QWORD PTR 72[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 88[rsp]
.L400:
	lea	rax, [rdi+r10]
	mov	QWORD PTR 72[rsp], rax
	jmp	.L349
.L408:
	jne	.L376
	mov	eax, DWORD PTR [r12]
	mov	DWORD PTR [rsi], eax
	jmp	.L376
.L353:
	mov	eax, DWORD PTR [r12]
	cmp	r10, 4
	mov	DWORD PTR [r14], eax
	jle	.L411
	mov	rcx, rdi
	mov	r8, r10
	mov	rdx, rsi
	mov	QWORD PTR 88[rsp], r9
	sub	rcx, r10
	call	memmove
	mov	r9, QWORD PTR 88[rsp]
.L359:
	mov	eax, DWORD PTR [r14]
	mov	DWORD PTR [rsi], eax
	jmp	.L358
.L368:
	mov	eax, DWORD PTR [rsi]
	cmp	r11, 4
	mov	DWORD PTR [r14], eax
	jle	.L412
	mov	r8, r11
	mov	rdx, r12
	mov	rcx, rsi
	mov	QWORD PTR 72[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 72[rsp]
	mov	r10, -4
.L378:
	mov	eax, DWORD PTR [r14]
	mov	DWORD PTR -4[rdi], eax
	jmp	.L400
.L354:
	jne	.L358
	mov	eax, DWORD PTR [rsi]
	mov	DWORD PTR -4[rdi], eax
	jmp	.L358
.L410:
	lea	rax, [rdi+r10]
	mov	QWORD PTR 72[rsp], rax
	jne	.L349
	mov	eax, DWORD PTR [r12]
	mov	DWORD PTR [rsi], eax
	jmp	.L400
.L412:
	jne	.L374
	mov	eax, DWORD PTR [r12]
	mov	DWORD PTR [rsi], eax
.L374:
	mov	r10, -4
	jmp	.L378
.L411:
	jne	.L359
	mov	eax, DWORD PTR [rsi]
	mov	DWORD PTR -4[rdi], eax
	jmp	.L359
	.seh_endproc
	.p2align 4
	.def	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0:
.LFB2628:
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
	.seh_endprologue
	mov	rsi, rdx
	sub	rdx, rcx
	mov	rbx, rcx
	sar	rdx, 2
	mov	rbp, r8
	mov	rdi, r9
	add	rdx, 1
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	lea	r13, 0[0+rax*4]
	cmp	rax, r9
	lea	r12, [rcx+r13]
	jle	.L414
	mov	rdx, r12
	call	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
	mov	r9, rdi
	mov	r8, rbp
	mov	rdx, rsi
	mov	rcx, r12
	call	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
	mov	rax, rsi
	mov	r9, r13
	mov	QWORD PTR 48[rsp], rdi
	sub	rax, r12
	mov	QWORD PTR 40[rsp], rbp
	sar	r9, 2
	mov	r8, rsi
	sar	rax, 2
	mov	rdx, r12
	mov	rcx, rbx
	mov	QWORD PTR 32[rsp], rax
	call	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
	nop
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
.L414:
	mov	r9, r8
	mov	rdx, r12
	mov	r8, rsi
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	jmp	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0
	.seh_endproc
	.p2align 4
	.globl	_Z8sort_ascRSt6vectorIiSaIiEE
	.def	_Z8sort_ascRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sort_ascRSt6vectorIiSaIiEE
_Z8sort_ascRSt6vectorIiSaIiEE:
.LFB2389:
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
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rsi
	je	.L417
	mov	rdi, rsi
	sub	rdi, rbp
	mov	rax, rdi
	sar	rax, 2
	test	rax, rax
	je	.L448
	bsr	rax, rax
	mov	rdx, rsi
	mov	rcx, rbp
	lea	rbx, 4[rbp]
	movsx	r8, eax
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	cmp	rdi, 64
	jle	.L420
	lea	rdi, 64[rbp]
	mov	r13d, 4
	jmp	.L427
	.p2align 4,,10
	.p2align 3
.L450:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L422
	mov	rcx, r13
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L423:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rbx, rdi
	je	.L449
.L427:
	mov	r12d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR 0[rbp]
	cmp	r12d, eax
	jl	.L450
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	r12d, edx
	jge	.L425
	.p2align 4,,10
	.p2align 3
.L426:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L426
.L425:
	add	rbx, 4
	mov	DWORD PTR [rcx], r12d
	cmp	rbx, rdi
	jne	.L427
.L449:
	cmp	rsi, rdi
	je	.L417
	.p2align 4,,10
	.p2align 3
.L428:
	mov	ecx, DWORD PTR [rdi]
	lea	rax, -4[rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jge	.L440
	.p2align 4,,10
	.p2align 3
.L431:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L431
	add	rdi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rsi, rdi
	jne	.L428
.L417:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L448:
	mov	r8, -2
	mov	rdx, rsi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	lea	rbx, 4[rbp]
.L420:
	cmp	rsi, rbx
	je	.L417
	mov	r12d, 4
	jmp	.L439
	.p2align 4,,10
	.p2align 3
.L451:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L434
	mov	rcx, r12
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L435:
	mov	DWORD PTR 0[rbp], edi
.L436:
	add	rbx, 4
	cmp	rsi, rbx
	je	.L417
.L439:
	mov	edi, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR 0[rbp]
	cmp	edi, eax
	jl	.L451
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	edx, edi
	jle	.L437
	.p2align 4,,10
	.p2align 3
.L438:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	edi, edx
	jl	.L438
.L437:
	mov	DWORD PTR [rcx], edi
	jmp	.L436
	.p2align 4,,10
	.p2align 3
.L440:
	mov	r8, rdi
	add	rdi, 4
	cmp	rsi, rdi
	mov	DWORD PTR [r8], ecx
	jne	.L428
	jmp	.L417
.L434:
	jne	.L435
	mov	DWORD PTR [rbx], eax
	jmp	.L435
.L422:
	jne	.L423
	mov	DWORD PTR [rbx], eax
	jmp	.L423
	.seh_endproc
	.p2align 4
	.globl	_Z9sort_descRSt6vectorIiSaIiEE
	.def	_Z9sort_descRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sort_descRSt6vectorIiSaIiEE
_Z9sort_descRSt6vectorIiSaIiEE:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rsi
	je	.L452
	mov	rdi, rsi
	mov	r8, -2
	sub	rdi, rbp
	mov	rax, rdi
	sar	rax, 2
	test	rax, rax
	je	.L454
	bsr	rax, rax
	cdqe
	lea	r8, [rax+rax]
.L454:
	xor	r9d, r9d
	mov	rdx, rsi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_
	lea	rbx, 4[rbp]
	cmp	rdi, 64
	jg	.L486
	cmp	rsi, rbx
	je	.L452
	mov	r12d, 4
	jmp	.L474
	.p2align 4,,10
	.p2align 3
.L487:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L469
	mov	rcx, r12
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L470:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], edi
	cmp	rsi, rbx
	je	.L452
.L474:
	mov	eax, DWORD PTR 0[rbp]
	mov	rcx, rbx
	mov	edi, DWORD PTR [rbx]
	cmp	eax, edi
	jl	.L487
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	edx, edi
	jge	.L472
	.p2align 4,,10
	.p2align 3
.L473:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	edi, edx
	jg	.L473
.L472:
	add	rbx, 4
	mov	DWORD PTR [rcx], edi
	cmp	rsi, rbx
	jne	.L474
.L452:
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
.L486:
	lea	rdi, 64[rbp]
	mov	r13d, 4
	jmp	.L462
	.p2align 4,,10
	.p2align 3
.L489:
	mov	r8, rbx
	sub	r8, rbp
	cmp	r8, 4
	jle	.L457
	mov	rcx, r13
	mov	rdx, rbp
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L458:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rbx, rdi
	je	.L488
.L462:
	mov	eax, DWORD PTR 0[rbp]
	mov	rcx, rbx
	mov	r12d, DWORD PTR [rbx]
	cmp	eax, r12d
	jl	.L489
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	r12d, edx
	jle	.L460
	.p2align 4,,10
	.p2align 3
.L461:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jg	.L461
.L460:
	add	rbx, 4
	mov	DWORD PTR [rcx], r12d
	cmp	rbx, rdi
	jne	.L462
.L488:
	cmp	rsi, rdi
	je	.L452
	mov	ecx, DWORD PTR [rdi]
	lea	rax, -4[rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jle	.L476
	.p2align 4,,10
	.p2align 3
.L466:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jg	.L466
	add	rdi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rsi, rdi
	je	.L452
.L485:
	mov	ecx, DWORD PTR [rdi]
	lea	rax, -4[rdi]
	mov	edx, DWORD PTR -4[rdi]
	cmp	ecx, edx
	jg	.L466
.L476:
	mov	r8, rdi
	add	rdi, 4
	cmp	rsi, rdi
	mov	DWORD PTR [r8], ecx
	jne	.L485
	jmp	.L452
.L469:
	jne	.L470
	mov	DWORD PTR [rbx], eax
	jmp	.L470
.L457:
	jne	.L458
	mov	DWORD PTR [rbx], eax
	jmp	.L458
	.seh_endproc
	.p2align 4
	.globl	_Z15stable_sort_ascRSt6vectorIiSaIiEE
	.def	_Z15stable_sort_ascRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15stable_sort_ascRSt6vectorIiSaIiEE
_Z15stable_sort_ascRSt6vectorIiSaIiEE:
.LFB2394:
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
	mov	rbx, QWORD PTR [rcx]
	mov	r12, QWORD PTR 8[rcx]
	mov	rbp, rbx
	cmp	rbx, r12
	je	.L490
	mov	rdx, r12
	sub	rdx, rbx
	mov	rax, rdx
	sar	rax, 2
	add	rax, 1
	mov	rsi, rax
	shr	rsi, 63
	add	rsi, rax
	sar	rsi
	test	rdx, rdx
	jle	.L492
	mov	r14, rsi
.L496:
	mov	rdx, QWORD PTR .refptr._ZSt7nothrow[rip]
	lea	r13, 0[0+r14*4]
	mov	rcx, r13
	call	_ZnwyRKSt9nothrow_t
	test	rax, rax
	mov	rdi, rax
	je	.L493
	cmp	rsi, r14
	jne	.L507
	add	rbx, r13
.L497:
	mov	r9, rdi
	mov	r8, r12
	mov	rdx, rbx
	mov	rcx, rbp
	call	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0
.L499:
	mov	rdx, r13
	mov	rcx, rdi
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L490:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L492:
	xor	r13d, r13d
	xor	edi, edi
	test	rsi, rsi
	je	.L497
	mov	rdx, r12
	mov	rcx, rbx
	call	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	jmp	.L499
	.p2align 4,,10
	.p2align 3
.L507:
	mov	r9, r14
	mov	r8, rax
	mov	rdx, r12
	mov	rcx, rbx
	call	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
	jmp	.L499
.L493:
	cmp	r14, 1
	je	.L492
	add	r14, 1
	sar	r14
	jmp	.L496
	.seh_endproc
	.section	.text$_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	.def	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_:
.LFB2458:
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
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	mov	rax, rcx
	mov	rcx, rdx
	sub	rdx, rax
	cmp	rdx, 4
	jle	.L509
	mov	r9, rdx
	mov	r13, rcx
	mov	r14, rdx
	sar	r9, 2
	lea	r10, -2[r9]
	lea	rdi, -1[r9]
	mov	rbp, r10
	not	r9
	shr	rbp, 63
	sar	rdi
	mov	r12d, r9d
	add	rbp, r10
	and	r12d, 1
	sar	rbp
	lea	rsi, [rax+rbp*4]
	mov	r11, rbp
	cmp	r11, rdi
	mov	ebx, DWORD PTR [rsi]
	mov	rcx, rsi
	jge	.L534
	.p2align 4,,10
	.p2align 3
.L558:
	mov	r10, r11
	mov	QWORD PTR [rsp], rsi
	mov	QWORD PTR 8[rsp], r14
	jmp	.L512
	.p2align 4,,10
	.p2align 3
.L535:
	mov	r10, rdx
.L512:
	lea	rcx, 1[r10]
	lea	rdx, [rcx+rcx]
	lea	rsi, -1[rdx]
	lea	r14, [rax+rsi*4]
	lea	rcx, [rax+rcx*8]
	mov	r15d, DWORD PTR [r14]
	mov	r9d, DWORD PTR [rcx]
	cmp	r15d, r9d
	jle	.L511
	mov	r9d, r15d
	mov	rcx, r14
	mov	rdx, rsi
.L511:
	cmp	rdx, rdi
	mov	DWORD PTR [rax+r10*4], r9d
	jl	.L535
	mov	rsi, QWORD PTR [rsp]
	mov	r14, QWORD PTR 8[rsp]
.L510:
	cmp	rbp, rdx
	jne	.L540
	test	r12b, r12b
	jne	.L513
.L540:
	lea	r10, -1[rdx]
	mov	r9, r10
	shr	r9, 63
	add	r9, r10
	sar	r9
.L515:
	cmp	r11, rdx
	jge	.L516
	mov	rcx, rdx
	jmp	.L517
	.p2align 4,,10
	.p2align 3
.L557:
	mov	DWORD PTR [rcx], r15d
	lea	rcx, -1[r9]
	mov	rdx, rcx
	shr	rdx, 63
	add	rdx, rcx
	mov	rcx, r9
	sar	rdx
	cmp	r11, r9
	jge	.L556
	mov	r9, rdx
.L517:
	lea	r10, [rax+r9*4]
	mov	r15d, DWORD PTR [r10]
	lea	rcx, [rax+rcx*4]
	cmp	ebx, r15d
	jg	.L557
.L516:
	sub	rsi, 4
	test	r11, r11
	mov	DWORD PTR [rcx], ebx
	je	.L554
.L559:
	sub	r11, 1
	mov	ebx, DWORD PTR [rsi]
	mov	rcx, rsi
	cmp	r11, rdi
	jl	.L558
.L534:
	mov	rdx, r11
	jmp	.L510
	.p2align 4,,10
	.p2align 3
.L556:
	mov	rcx, r10
	sub	rsi, 4
	test	r11, r11
	mov	DWORD PTR [rcx], ebx
	jne	.L559
.L554:
	mov	rdx, r14
	mov	rcx, r13
.L509:
	cmp	rcx, r8
	jnb	.L508
	mov	r9, rdx
	mov	rbp, rcx
	sar	r9, 2
	lea	r10, -1[r9]
	mov	rdi, r9
	sub	r9, 2
	mov	rbx, r10
	mov	rsi, r9
	and	edi, 1
	shr	rbx, 63
	shr	rsi, 63
	add	rbx, r10
	add	rsi, r9
	sar	rbx
	sar	rsi
	jmp	.L532
	.p2align 4,,10
	.p2align 3
.L520:
	add	rbp, 4
	cmp	rbp, r8
	jnb	.L508
.L532:
	mov	r11d, DWORD PTR 0[rbp]
	mov	ecx, DWORD PTR [rax]
	cmp	r11d, ecx
	jge	.L520
	cmp	rdx, 8
	mov	DWORD PTR 0[rbp], ecx
	jle	.L521
	xor	r12d, r12d
	jmp	.L523
	.p2align 4,,10
	.p2align 3
.L537:
	mov	r12, rcx
.L523:
	lea	r9, 1[r12]
	lea	rcx, [r9+r9]
	lea	r13, -1[rcx]
	lea	r14, [rax+r13*4]
	lea	r9, [rax+r9*8]
	mov	r15d, DWORD PTR [r14]
	mov	r10d, DWORD PTR [r9]
	cmp	r15d, r10d
	jle	.L522
	mov	r10d, r15d
	mov	r9, r14
	mov	rcx, r13
.L522:
	cmp	rbx, rcx
	mov	DWORD PTR [rax+r12*4], r10d
	jg	.L537
	test	rdi, rdi
	jne	.L555
	cmp	rsi, rcx
	je	.L529
.L555:
	lea	r12, -1[rcx]
	mov	r10, r12
	shr	r10, 63
	add	r10, r12
	sar	r10
	test	rcx, rcx
	jne	.L531
	jmp	.L526
	.p2align 4,,10
	.p2align 3
.L561:
	mov	DWORD PTR [r9], r13d
	lea	r9, -1[r10]
	mov	rcx, r9
	shr	rcx, 63
	add	rcx, r9
	sar	rcx
	test	r10, r10
	mov	r9, rcx
	mov	rcx, r10
	je	.L560
	mov	r10, r9
.L531:
	lea	r12, [rax+r10*4]
	mov	r13d, DWORD PTR [r12]
	lea	r9, [rax+rcx*4]
	cmp	r11d, r13d
	jg	.L561
.L526:
	mov	DWORD PTR [r9], r11d
.L562:
	add	rbp, 4
	cmp	rbp, r8
	jb	.L532
.L508:
	add	rsp, 24
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
.L560:
	mov	r9, r12
	mov	DWORD PTR [r9], r11d
	jmp	.L562
	.p2align 4,,10
	.p2align 3
.L513:
	lea	r10, 1[rdx+rdx]
	lea	r9, [rax+r10*4]
	mov	r15d, DWORD PTR [r9]
	mov	DWORD PTR [rcx], r15d
	mov	rcx, r9
	mov	r9, rdx
	mov	rdx, r10
	jmp	.L515
.L521:
	test	rdi, rdi
	mov	r9, rax
	jne	.L526
	test	rsi, rsi
	jne	.L526
	xor	ecx, ecx
	.p2align 4,,10
	.p2align 3
.L529:
	lea	r12, 1[rcx+rcx]
	mov	r10d, DWORD PTR [rax+r12*4]
	mov	DWORD PTR [r9], r10d
	mov	r10, rcx
	mov	rcx, r12
	jmp	.L531
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z16median_partitionRSt6vectorIiSaIiEE
	.def	_Z16median_partitionRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16median_partitionRSt6vectorIiSaIiEE
_Z16median_partitionRSt6vectorIiSaIiEE:
.LFB2395:
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
	mov	rsi, QWORD PTR 8[rcx]
	mov	rbx, QWORD PTR [rcx]
	cmp	rbx, rsi
	je	.L563
	mov	rax, rsi
	sub	rax, rbx
	mov	rdx, rax
	sar	rdx, 2
	mov	rcx, rdx
	shr	rcx
	lea	rdi, [rbx+rcx*4]
	cmp	rsi, rdi
	je	.L563
	test	rdx, rdx
	je	.L603
	bsr	r11, rdx
	movsx	r11, r11d
	add	r11, r11
	cmp	rax, 12
	jle	.L567
	.p2align 4,,10
	.p2align 3
.L568:
	sar	rax, 3
	movq	xmm0, QWORD PTR [rbx]
	sub	r11, 1
	lea	r10, [rbx+rax*4]
	mov	r9d, DWORD PTR -4[rsi]
	mov	edx, DWORD PTR [r10]
	pshufd	xmm2, xmm0, 0xe5
	movd	r8d, xmm2
	movd	ecx, xmm0
	lea	rax, 4[rbx]
	pshufd	xmm1, xmm0, 225
	cmp	edx, r8d
	jle	.L570
	cmp	edx, r9d
	jl	.L576
	cmp	r8d, r9d
	jge	.L573
.L601:
	mov	DWORD PTR [rbx], r9d
	mov	r9d, ecx
	mov	DWORD PTR -4[rsi], ecx
	mov	r8d, DWORD PTR [rbx]
	mov	ecx, DWORD PTR 4[rbx]
.L572:
	cmp	r8d, ecx
	mov	rdx, rsi
	jle	.L593
	.p2align 4,,10
	.p2align 3
.L605:
	add	rax, 4
	.p2align 4,,10
	.p2align 3
.L578:
	mov	r10, rax
	mov	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, r8d
	jl	.L578
.L577:
	sub	rdx, 4
	cmp	r8d, r9d
	jge	.L579
	.p2align 4,,10
	.p2align 3
.L580:
	mov	r9d, DWORD PTR -4[rdx]
	sub	rdx, 4
	cmp	r9d, r8d
	jg	.L580
.L579:
	cmp	r10, rdx
	jnb	.L604
	mov	DWORD PTR [r10], r9d
	lea	rax, 4[r10]
	mov	r9d, DWORD PTR -4[rdx]
	mov	DWORD PTR [rdx], ecx
	mov	r8d, DWORD PTR [rbx]
	mov	ecx, DWORD PTR 4[r10]
	cmp	r8d, ecx
	jg	.L605
.L593:
	mov	r10, rax
	jmp	.L577
	.p2align 4,,10
	.p2align 3
.L604:
	cmp	rdi, r10
	cmovb	rsi, r10
	cmovnb	rbx, r10
	mov	rax, rsi
	sub	rax, rbx
	cmp	rax, 12
	jle	.L606
	test	r11, r11
	jne	.L568
	lea	rdx, 4[rdi]
	xor	r9d, r9d
	mov	r8, rsi
	mov	rcx, rbx
	call	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	mov	eax, DWORD PTR [rbx]
	mov	edx, DWORD PTR [rdi]
	mov	DWORD PTR [rbx], edx
	mov	DWORD PTR [rdi], eax
.L563:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L570:
	cmp	r8d, r9d
	jl	.L573
	cmp	edx, r9d
	jl	.L601
.L576:
	mov	DWORD PTR [rbx], edx
	mov	DWORD PTR [r10], ecx
	mov	ecx, DWORD PTR 4[rbx]
	mov	r8d, DWORD PTR [rbx]
	mov	r9d, DWORD PTR -4[rsi]
	jmp	.L572
.L573:
	movq	QWORD PTR [rbx], xmm1
	mov	r9d, DWORD PTR -4[rsi]
	jmp	.L572
.L606:
	cmp	rsi, rbx
	je	.L563
.L567:
	lea	rdi, 4[rbx]
	cmp	rsi, rdi
	je	.L563
	mov	ebp, DWORD PTR [rdi]
	mov	r12d, 4
	mov	rcx, rdi
	mov	eax, DWORD PTR [rbx]
	cmp	ebp, eax
	jge	.L585
.L607:
	mov	r8, rdi
	sub	r8, rbx
	cmp	r8, 4
	jle	.L586
	mov	rcx, r12
	mov	rdx, rbx
	sub	rcx, r8
	add	rcx, rdi
	call	memmove
.L587:
	mov	DWORD PTR [rbx], ebp
.L588:
	add	rdi, 4
	cmp	rsi, rdi
	je	.L563
	mov	ebp, DWORD PTR [rdi]
	mov	rcx, rdi
	mov	eax, DWORD PTR [rbx]
	cmp	ebp, eax
	jl	.L607
.L585:
	mov	edx, DWORD PTR -4[rdi]
	lea	rax, -4[rdi]
	cmp	edx, ebp
	jle	.L589
	.p2align 4,,10
	.p2align 3
.L590:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ebp, edx
	jl	.L590
.L589:
	mov	DWORD PTR [rcx], ebp
	jmp	.L588
.L586:
	jne	.L587
	mov	DWORD PTR [rdi], eax
	jmp	.L587
.L603:
	cmp	rax, 12
	mov	r11, -2
	jg	.L568
	jmp	.L567
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZnwyRKSt9nothrow_t;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt7nothrow, "dr"
	.globl	.refptr._ZSt7nothrow
	.linkonce	discard
.refptr._ZSt7nothrow:
	.quad	_ZSt7nothrow
