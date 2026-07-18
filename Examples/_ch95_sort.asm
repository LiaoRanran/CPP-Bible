	.file	"_ch95_sort.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0:
.LFB2557:
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
	mov	rbx, r8
	mov	rdi, r9
	cmp	rdx, rcx
	jne	.L21
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L23:
	mov	eax, r11d
	add	rbx, 4
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	cmp	rdx, rcx
	je	.L2
.L21:
	cmp	rdi, rbx
	je	.L2
	mov	r11d, DWORD PTR [rbx]
	mov	eax, DWORD PTR [rcx]
	cmp	r11d, eax
	jl	.L23
	add	rcx, 4
	mov	DWORD PTR [r10], eax
	add	r10, 4
	cmp	rdx, rcx
	jne	.L21
.L2:
	mov	rsi, rdx
	sub	rsi, rcx
	cmp	rsi, 4
	jle	.L7
	mov	rdx, rcx
	mov	r8, rsi
	mov	rcx, r10
	call	memmove
	lea	r10, [rax+rsi]
.L8:
	sub	rdi, rbx
	cmp	rdi, 4
	jle	.L9
	mov	rcx, r10
	mov	r8, rdi
	mov	rdx, rbx
	call	memmove
	lea	r10, [rax+rdi]
.L10:
	mov	rax, r10
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
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	jmp	.L8
	.p2align 4,,10
	.p2align 3
.L9:
	jne	.L10
	mov	eax, DWORD PTR [rbx]
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	jmp	.L10
	.seh_endproc
	.p2align 4
	.def	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0:
.LFB2558:
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
	mov	rsi, r9
	mov	rdx, rcx
	mov	rbx, r8
	cmp	rcx, r11
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
	cmp	rsi, rbx
	je	.L38
	mov	eax, DWORD PTR [rbx]
	mov	ecx, DWORD PTR [rdx]
	cmp	eax, ecx
	jl	.L32
	mov	eax, ecx
	add	rdx, 4
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	cmp	rdx, r11
	jne	.L25
.L26:
	sub	rsi, rbx
	cmp	rsi, 4
	jle	.L31
	.p2align 4
	.p2align 3
.L40:
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, r10
	call	memmove
	add	rax, rsi
.L24:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L38:
	mov	rdi, r11
	sub	rdi, rdx
	cmp	rdi, 4
	jle	.L39
	mov	rcx, r10
	mov	r8, rdi
	sub	rsi, rbx
	call	memmove
	lea	r10, [rax+rdi]
	cmp	rsi, 4
	jg	.L40
.L31:
	je	.L41
.L35:
	mov	rax, r10
	jmp	.L24
.L41:
	mov	eax, DWORD PTR [rbx]
	mov	DWORD PTR [r10], eax
	lea	rax, 4[r10]
	jmp	.L24
.L39:
	jne	.L35
	mov	eax, DWORD PTR [rdx]
	add	r10, 4
	mov	DWORD PTR -4[r10], eax
	jmp	.L26
	.seh_endproc
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_.isra.0:
.LFB2559:
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
	cmp	rax, 64
	jle	.L42
	mov	rbp, rax
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	je	.L105
.L44:
	movq	xmm0, QWORD PTR [rsi]
	lea	r10, [rsi+rax*4]
	mov	r9d, DWORD PTR -4[r11]
	sub	rdi, 1
	mov	r8d, DWORD PTR [r10]
	lea	rax, 4[rsi]
	pshufd	xmm1, xmm0, 0xe5
	movd	edx, xmm1
	movd	ecx, xmm0
	cmp	edx, r8d
	jle	.L73
	cmp	r8d, r9d
	jg	.L78
	cmp	edx, r9d
	jg	.L104
.L76:
	pshufd	xmm0, xmm0, 225
	movq	QWORD PTR [rsi], xmm0
.L75:
	mov	r10, r11
	cmp	edx, ecx
	jge	.L94
	.p2align 4
	.p2align 3
.L107:
	add	rax, 4
	.p2align 4
	.p2align 4
	.p2align 3
.L80:
	mov	r9, rax
	mov	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jg	.L80
	mov	rbx, r9
	mov	r9d, DWORD PTR -4[r10]
	cmp	r9d, edx
	jge	.L81
.L108:
	lea	rax, -8[r10]
	.p2align 4
	.p2align 4
	.p2align 3
.L82:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	r9d, edx
	jl	.L82
	cmp	rbx, r10
	jnb	.L106
.L84:
	mov	DWORD PTR [rbx], r9d
	lea	rax, 4[rbx]
	mov	DWORD PTR [r10], ecx
	mov	ecx, DWORD PTR 4[rbx]
	mov	edx, DWORD PTR [rsi]
	cmp	edx, ecx
	jl	.L107
.L94:
	mov	r9d, DWORD PTR -4[r10]
	mov	rbx, rax
	cmp	r9d, edx
	jl	.L108
	.p2align 4
	.p2align 3
.L81:
	sub	r10, 4
	cmp	rbx, r10
	jb	.L84
	.p2align 4
	.p2align 3
.L106:
	mov	r8, rdi
	mov	rdx, r11
	mov	rcx, rbx
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_.isra.0
	mov	rax, rbx
	sub	rax, rsi
	cmp	rax, 64
	jle	.L42
	mov	rbp, rax
	mov	r11, rbx
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	jne	.L44
.L105:
	lea	r10, -1[rbp]
	lea	rbx, -4[rsi+rax*4]
	lea	r8, -1[rax]
	sar	r10
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	rdi, r8
	cmp	r8, r10
	jge	.L45
.L111:
	mov	r12, r8
	jmp	.L47
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L88:
	mov	r12, rax
.L47:
	lea	rdx, 1[r12]
	lea	r13, [rdx+rdx]
	lea	r14, [rsi+rdx*8]
	lea	rax, -1[r13]
	mov	r15d, DWORD PTR [r14]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	r15d, edx
	cmovle	edx, r15d
	cmovle	rax, r13
	cmovle	rcx, r14
	mov	DWORD PTR [rsi+r12*4], edx
	cmp	rax, r10
	jl	.L88
	test	bpl, 1
	jne	.L100
	cmp	rdi, rax
	je	.L50
.L100:
	lea	rdx, -1[rax]
.L49:
	sar	rdx
	cmp	r8, rax
	jl	.L53
	jmp	.L51
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L110:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	cmp	r8, rdx
	jge	.L109
	mov	rdx, rcx
	sar	rdx
.L53:
	lea	r12, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r12]
	cmp	r9d, ecx
	jl	.L110
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	je	.L55
.L54:
	sub	rbx, 4
	sub	r8, 1
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	cmp	r8, r10
	jl	.L111
.L45:
	test	bpl, 1
	jne	.L51
	cmp	r8, rdi
	je	.L112
.L51:
	mov	DWORD PTR [rcx], r9d
	jmp	.L54
	.p2align 4,,10
	.p2align 3
.L73:
	cmp	edx, r9d
	jg	.L76
	cmp	r8d, r9d
	jle	.L78
.L104:
	mov	DWORD PTR [rsi], r9d
	mov	DWORD PTR -4[r11], ecx
	mov	edx, DWORD PTR [rsi]
	mov	ecx, DWORD PTR 4[rsi]
	jmp	.L75
.L78:
	mov	DWORD PTR [rsi], r8d
	mov	DWORD PTR [r10], ecx
	mov	edx, DWORD PTR [rsi]
	mov	ecx, DWORD PTR 4[rsi]
	jmp	.L75
.L42:
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
.L109:
	mov	rax, r12
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	jne	.L54
.L55:
	mov	rax, r11
	lea	r9, -4[r11]
	sub	rax, rsi
	cmp	rax, 4
	jle	.L42
	.p2align 4
	.p2align 3
.L72:
	mov	r10, r9
	mov	eax, DWORD PTR [rsi]
	mov	r8d, DWORD PTR [r9]
	sub	r10, rsi
	mov	r13, r10
	mov	DWORD PTR [r9], eax
	sar	r13, 2
	cmp	r10, 8
	jle	.L59
	lea	r12, -1[r13]
	xor	ebp, ebp
	sar	r12
	jmp	.L61
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L91:
	mov	rbp, rax
.L61:
	lea	rdx, 1[rbp]
	lea	r11, [rdx+rdx]
	lea	rbx, [rsi+rdx*8]
	lea	rax, -1[r11]
	mov	edi, DWORD PTR [rbx]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	edi, edx
	cmovle	edx, edi
	cmovle	rax, r11
	cmovle	rcx, rbx
	mov	DWORD PTR [rsi+rbp*4], edx
	cmp	r12, rax
	jg	.L91
	and	r13d, 1
	jne	.L102
	mov	rdx, r10
	sar	rdx, 3
	sub	rdx, 1
	cmp	rdx, rax
	je	.L67
.L102:
	lea	rdx, -1[rax]
	shr	rdx, 63
	lea	rdx, -1[rax+rdx]
	sar	rdx
	test	rax, rax
	jne	.L70
	jmp	.L113
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L115:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	test	rdx, rdx
	je	.L114
	sar	rcx
	mov	rdx, rcx
.L70:
	lea	r11, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r11]
	cmp	r8d, ecx
	jl	.L115
.L64:
	mov	DWORD PTR [rax], r8d
	cmp	r10, 4
	jle	.L42
.L101:
	sub	r9, 4
	jmp	.L72
.L114:
	mov	rax, r11
	jmp	.L64
.L59:
	and	r13d, 1
	jne	.L103
	cmp	r10, 8
	jne	.L103
	mov	rcx, rsi
	xor	eax, eax
.L67:
	lea	r11, 1[rax+rax]
	mov	edx, DWORD PTR [rsi+r11*4]
	mov	DWORD PTR [rcx], edx
	mov	rdx, rax
	mov	rax, r11
	jmp	.L70
.L103:
	mov	rax, rsi
	jmp	.L64
.L112:
	mov	rax, r8
.L50:
	lea	rdx, [rax+rax]
	lea	rax, 1[rdx]
	lea	r12, [rsi+rax*4]
	mov	r13d, DWORD PTR [r12]
	mov	DWORD PTR [rcx], r13d
	mov	rcx, r12
	jmp	.L49
.L113:
	mov	DWORD PTR [rcx], r8d
	jmp	.L101
	.seh_endproc
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB2565:
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
	cmp	rax, 64
	jle	.L116
	mov	rbp, rax
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	je	.L179
.L118:
	movq	xmm0, QWORD PTR [rsi]
	lea	r10, [rsi+rax*4]
	mov	r9d, DWORD PTR -4[r11]
	sub	rdi, 1
	mov	r8d, DWORD PTR [r10]
	lea	rax, 4[rsi]
	pshufd	xmm1, xmm0, 0xe5
	movd	edx, xmm1
	movd	ecx, xmm0
	cmp	edx, r8d
	jge	.L147
	cmp	r8d, r9d
	jl	.L152
	cmp	edx, r9d
	jl	.L178
.L150:
	pshufd	xmm0, xmm0, 225
	movq	QWORD PTR [rsi], xmm0
.L149:
	mov	r10, r11
	cmp	ecx, edx
	jge	.L168
	.p2align 4
	.p2align 3
.L181:
	add	rax, 4
	.p2align 4
	.p2align 4
	.p2align 3
.L154:
	mov	r9, rax
	mov	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jl	.L154
	mov	rbx, r9
	mov	r9d, DWORD PTR -4[r10]
	cmp	r9d, edx
	jle	.L155
.L182:
	lea	rax, -8[r10]
	.p2align 4
	.p2align 4
	.p2align 3
.L156:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	r9d, edx
	jg	.L156
	cmp	rbx, r10
	jnb	.L180
.L158:
	mov	DWORD PTR [rbx], r9d
	lea	rax, 4[rbx]
	mov	DWORD PTR [r10], ecx
	mov	edx, DWORD PTR [rsi]
	mov	ecx, DWORD PTR 4[rbx]
	cmp	ecx, edx
	jl	.L181
.L168:
	mov	r9d, DWORD PTR -4[r10]
	mov	rbx, rax
	cmp	r9d, edx
	jg	.L182
	.p2align 4
	.p2align 3
.L155:
	sub	r10, 4
	cmp	rbx, r10
	jb	.L158
	.p2align 4
	.p2align 3
.L180:
	mov	r8, rdi
	mov	rdx, r11
	mov	rcx, rbx
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	rax, rbx
	sub	rax, rsi
	cmp	rax, 64
	jle	.L116
	mov	rbp, rax
	mov	r11, rbx
	sar	rax, 3
	sar	rbp, 2
	test	rdi, rdi
	jne	.L118
.L179:
	lea	r10, -1[rbp]
	lea	rbx, -4[rsi+rax*4]
	lea	r8, -1[rax]
	sar	r10
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	rdi, r8
	cmp	r8, r10
	jge	.L119
.L185:
	mov	r12, r8
	jmp	.L121
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L162:
	mov	r12, rax
.L121:
	lea	rdx, 1[r12]
	lea	r13, [rdx+rdx]
	lea	r14, [rsi+rdx*8]
	lea	rax, -1[r13]
	mov	r15d, DWORD PTR [r14]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	edx, r15d
	cmovle	edx, r15d
	cmovle	rax, r13
	cmovle	rcx, r14
	mov	DWORD PTR [rsi+r12*4], edx
	cmp	rax, r10
	jl	.L162
	test	bpl, 1
	jne	.L174
	cmp	rdi, rax
	je	.L124
.L174:
	lea	rdx, -1[rax]
.L123:
	sar	rdx
	cmp	r8, rax
	jl	.L127
	jmp	.L125
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L184:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	cmp	r8, rdx
	jge	.L183
	mov	rdx, rcx
	sar	rdx
.L127:
	lea	r12, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r12]
	cmp	r9d, ecx
	jg	.L184
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	je	.L129
.L128:
	sub	rbx, 4
	sub	r8, 1
	mov	r9d, DWORD PTR [rbx]
	mov	rcx, rbx
	cmp	r8, r10
	jl	.L185
.L119:
	test	bpl, 1
	jne	.L125
	cmp	r8, rdi
	je	.L186
.L125:
	mov	DWORD PTR [rcx], r9d
	jmp	.L128
	.p2align 4,,10
	.p2align 3
.L147:
	cmp	edx, r9d
	jl	.L150
	cmp	r8d, r9d
	jge	.L152
.L178:
	mov	DWORD PTR [rsi], r9d
	mov	DWORD PTR -4[r11], ecx
	mov	ecx, DWORD PTR 4[rsi]
	mov	edx, DWORD PTR [rsi]
	jmp	.L149
.L152:
	mov	DWORD PTR [rsi], r8d
	mov	DWORD PTR [r10], ecx
	mov	ecx, DWORD PTR 4[rsi]
	mov	edx, DWORD PTR [rsi]
	jmp	.L149
.L116:
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
.L183:
	mov	rax, r12
	mov	DWORD PTR [rax], r9d
	test	r8, r8
	jne	.L128
.L129:
	mov	rax, r11
	lea	r9, -4[r11]
	sub	rax, rsi
	cmp	rax, 4
	jle	.L116
	.p2align 4
	.p2align 3
.L146:
	mov	r10, r9
	mov	eax, DWORD PTR [rsi]
	mov	r8d, DWORD PTR [r9]
	sub	r10, rsi
	mov	r13, r10
	mov	DWORD PTR [r9], eax
	sar	r13, 2
	cmp	r10, 8
	jle	.L133
	lea	r12, -1[r13]
	xor	ebp, ebp
	sar	r12
	jmp	.L135
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L165:
	mov	rbp, rax
.L135:
	lea	rdx, 1[rbp]
	lea	r11, [rdx+rdx]
	lea	rbx, [rsi+rdx*8]
	lea	rax, -1[r11]
	mov	edi, DWORD PTR [rbx]
	lea	rcx, [rsi+rax*4]
	mov	edx, DWORD PTR [rcx]
	cmp	edx, edi
	cmovle	edx, edi
	cmovle	rax, r11
	cmovle	rcx, rbx
	mov	DWORD PTR [rsi+rbp*4], edx
	cmp	r12, rax
	jg	.L165
	and	r13d, 1
	jne	.L176
	mov	rdx, r10
	sar	rdx, 3
	sub	rdx, 1
	cmp	rdx, rax
	je	.L141
.L176:
	lea	rdx, -1[rax]
	shr	rdx, 63
	lea	rdx, -1[rax+rdx]
	sar	rdx
	test	rax, rax
	jne	.L144
	jmp	.L187
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L189:
	mov	DWORD PTR [rax], ecx
	lea	rax, -1[rdx]
	shr	rax, 63
	lea	rcx, -1[rax+rdx]
	mov	rax, rdx
	test	rdx, rdx
	je	.L188
	sar	rcx
	mov	rdx, rcx
.L144:
	lea	r11, [rsi+rdx*4]
	lea	rax, [rsi+rax*4]
	mov	ecx, DWORD PTR [r11]
	cmp	r8d, ecx
	jg	.L189
.L138:
	mov	DWORD PTR [rax], r8d
	cmp	r10, 4
	jle	.L116
.L175:
	sub	r9, 4
	jmp	.L146
.L188:
	mov	rax, r11
	jmp	.L138
.L133:
	and	r13d, 1
	jne	.L177
	cmp	r10, 8
	jne	.L177
	mov	rcx, rsi
	xor	eax, eax
.L141:
	lea	r11, 1[rax+rax]
	mov	edx, DWORD PTR [rsi+r11*4]
	mov	DWORD PTR [rcx], edx
	mov	rdx, rax
	mov	rax, r11
	jmp	.L144
.L177:
	mov	rax, rsi
	jmp	.L138
.L186:
	mov	rax, r8
.L124:
	lea	rdx, [rax+rax]
	lea	rax, 1[rdx]
	lea	r12, [rsi+rax*4]
	mov	r13d, DWORD PTR [r12]
	mov	DWORD PTR [rcx], r13d
	mov	rcx, r12
	jmp	.L123
.L187:
	mov	DWORD PTR [rcx], r8d
	jmp	.L175
	.seh_endproc
	.p2align 4
	.def	_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt24__merge_sort_with_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB2574:
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
	mov	r13, rdx
	mov	QWORD PTR 144[rsp], rcx
	mov	rbp, rdx
	sub	r13, rcx
	mov	QWORD PTR 160[rsp], r8
	cmp	r13, 24
	jle	.L191
	mov	rdi, rcx
	.p2align 4
	.p2align 3
.L199:
	mov	r12, rdi
	add	rdi, 28
	lea	rsi, -24[rdi]
	jmp	.L198
	.p2align 4,,10
	.p2align 3
.L229:
	mov	r8, rsi
	sub	r8, r12
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rsi+rax]
	cmp	r8, 4
	jle	.L193
	mov	rdx, r12
	call	memmove
.L194:
	add	rsi, 4
	mov	DWORD PTR -28[rdi], ebx
	cmp	rdi, rsi
	je	.L228
.L198:
	mov	ebx, DWORD PTR [rsi]
	mov	edx, DWORD PTR -28[rdi]
	cmp	ebx, edx
	jl	.L229
	mov	edx, DWORD PTR -4[rsi]
	cmp	ebx, edx
	jge	.L216
	lea	rax, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L197:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ebx, edx
	jl	.L197
	mov	DWORD PTR [rcx], ebx
.L230:
	add	rsi, 4
	cmp	rdi, rsi
	jne	.L198
.L228:
	mov	rax, rbp
	sub	rax, rdi
	cmp	rax, 24
	jg	.L199
	cmp	rbp, rdi
	je	.L200
	add	r12, 32
	cmp	rbp, r12
	je	.L200
	.p2align 4
	.p2align 3
.L207:
	mov	ebx, DWORD PTR [r12]
	mov	edx, DWORD PTR [rdi]
	cmp	ebx, edx
	jge	.L201
	mov	r8, r12
	sub	r8, rdi
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[r12+rax]
	cmp	r8, 4
	jle	.L202
	mov	rdx, rdi
	call	memmove
.L203:
	mov	DWORD PTR [rdi], ebx
.L204:
	add	r12, 4
	cmp	rbp, r12
	jne	.L207
.L200:
	cmp	r13, 28
	jle	.L190
	mov	rax, r13
	mov	ebx, 7
	mov	esi, 28
	add	r13, QWORD PTR 160[rsp]
	sar	rax, 2
	mov	QWORD PTR 56[rsp], rax
	.p2align 4
	.p2align 3
.L213:
	lea	rdi, [rbx+rbx]
	cmp	QWORD PTR 56[rsp], rdi
	jl	.L218
	lea	r12, 0[0+rbx*8]
	mov	r14, rsi
	mov	rcx, QWORD PTR 160[rsp]
	mov	r15, QWORD PTR 144[rsp]
	sub	r14, r12
	.p2align 4
	.p2align 3
.L210:
	mov	rax, r15
	mov	QWORD PTR 32[rsp], rcx
	add	r15, r12
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
	jle	.L210
.L209:
	cmp	rax, rbx
	mov	QWORD PTR 32[rsp], rcx
	mov	r9, rbp
	mov	rcx, r15
	cmovg	rax, rbx
	mov	rbx, rsi
	lea	rdx, [r15+rax*4]
	mov	r8, rdx
	call	_ZSt12__move_mergeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	mov	rcx, QWORD PTR 144[rsp]
	cmp	QWORD PTR 56[rsp], rsi
	jl	.L211
	sal	rsi, 2
	lea	r12, 0[0+rdi*4]
	mov	r14, QWORD PTR 160[rsp]
	sub	r12, rsi
	.p2align 4
	.p2align 3
.L212:
	mov	rax, r14
	mov	QWORD PTR 32[rsp], rcx
	add	r14, rsi
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
	jle	.L212
	cmp	rax, rdi
	mov	QWORD PTR 32[rsp], rcx
	mov	r9, r13
	mov	rcx, r14
	cmovg	rax, rdi
	lea	rdx, [r14+rax*4]
	mov	r8, rdx
	call	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	cmp	QWORD PTR 56[rsp], rbx
	jg	.L213
.L190:
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
.L193:
	jne	.L194
	mov	DWORD PTR [rcx], edx
	jmp	.L194
	.p2align 4,,10
	.p2align 3
.L201:
	mov	edx, DWORD PTR -4[r12]
	cmp	edx, ebx
	jle	.L217
	lea	rax, -4[r12]
	.p2align 5
	.p2align 4
	.p2align 3
.L206:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ebx, edx
	jl	.L206
	mov	DWORD PTR [rcx], ebx
	jmp	.L204
	.p2align 4,,10
	.p2align 3
.L216:
	mov	rcx, rsi
	mov	DWORD PTR [rcx], ebx
	jmp	.L230
.L211:
	mov	rax, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 160[rsp]
	mov	r9, r13
	cmp	rax, rdi
	mov	r15, rax
	mov	rax, QWORD PTR 160[rsp]
	cmovg	r15, rdi
	lea	rdx, [rax+r15*4]
	mov	rax, QWORD PTR 144[rsp]
	mov	r8, rdx
	mov	QWORD PTR 32[rsp], rax
	call	_ZSt12__move_mergeIPiN9__gnu_cxx17__normal_iteratorIS0_St6vectorIiSaIiEEEENS1_5__ops15_Iter_less_iterEET0_T_SA_SA_SA_S9_T1_.isra.0
	jmp	.L190
.L218:
	mov	rax, QWORD PTR 56[rsp]
	mov	rcx, QWORD PTR 160[rsp]
	mov	r15, QWORD PTR 144[rsp]
	jmp	.L209
.L202:
	jne	.L203
	mov	DWORD PTR [rcx], edx
	jmp	.L203
.L217:
	mov	rcx, r12
	mov	DWORD PTR [rcx], ebx
	jmp	.L204
.L191:
	cmp	rdx, QWORD PTR 144[rsp]
	je	.L190
	mov	rax, QWORD PTR 144[rsp]
	lea	r12, 4[rax]
	mov	rdi, rax
	cmp	rdx, r12
	jne	.L207
	jmp	.L190
	.seh_endproc
	.p2align 4
	.def	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0
_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0:
.LFB2580:
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	r9, rcx
	mov	rax, r8
	cmp	rcx, rdx
	je	.L233
	mov	rax, rcx
	cmp	rdx, r8
	je	.L233
	mov	rax, r8
	mov	r11, rdx
	sub	r8, rdx
	sub	rax, rcx
	sub	r11, rcx
	lea	r14, [rcx+r8]
	sar	rax, 2
	mov	r10, r11
	sar	r10, 2
	mov	rbx, rax
	sub	rbx, r10
	cmp	r10, rbx
	je	.L257
	.p2align 4
	.p2align 3
.L237:
	mov	r8, rax
	sub	r8, r10
	cmp	r10, r8
	jge	.L238
.L259:
	cmp	r10, 1
	je	.L258
	test	r8, r8
	jle	.L242
	lea	rdx, [r9+r10*4]
	xor	ecx, ecx
	.p2align 5
	.p2align 4
	.p2align 3
.L243:
	mov	r11d, DWORD PTR [r9+rcx*4]
	mov	ebx, DWORD PTR [rdx+rcx*4]
	mov	DWORD PTR [r9+rcx*4], ebx
	mov	DWORD PTR [rdx+rcx*4], r11d
	add	rcx, 1
	cmp	r8, rcx
	jne	.L243
	lea	r9, [r9+r8*4]
.L242:
	xor	edx, edx
	div	r10
	test	rdx, rdx
	je	.L256
	mov	rax, r10
	sub	r10, rdx
	mov	r8, rax
	sub	r8, r10
	cmp	r10, r8
	jl	.L259
.L238:
	lea	r11, [r9+rax*4]
	cmp	r8, 1
	je	.L260
	lea	rsi, 0[0+r10*4]
	add	r9, rsi
	test	r10, r10
	jle	.L249
	xor	ecx, ecx
	xor	edx, edx
	.p2align 6
	.p2align 4
	.p2align 3
.L250:
	mov	ebx, DWORD PTR -4[r9+rcx]
	mov	edi, DWORD PTR -4[r11+rcx]
	add	rdx, 1
	mov	DWORD PTR -4[r9+rcx], edi
	mov	DWORD PTR -4[r11+rcx], ebx
	sub	rcx, 4
	cmp	r10, rdx
	jne	.L250
	sub	r9, rsi
.L249:
	xor	edx, edx
	div	r8
	mov	r10, rdx
	test	rdx, rdx
	je	.L256
	mov	rax, r8
	jmp	.L237
.L257:
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L236:
	mov	r8d, DWORD PTR [rcx+rax]
	mov	r9d, DWORD PTR [rdx+rax]
	mov	DWORD PTR [rcx+rax], r9d
	mov	DWORD PTR [rdx+rax], r8d
	add	rax, 4
	cmp	r11, rax
	jne	.L236
	mov	rax, rdx
.L233:
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
.L256:
	mov	rax, r14
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	ret
.L260:
	lea	r8, -4[r11]
	mov	ebx, DWORD PTR -4[r11]
	sub	r8, r9
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, [r11+rax]
	cmp	r8, 4
	jle	.L247
	mov	rdx, r9
	mov	QWORD PTR 40[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 40[rsp]
.L248:
	mov	DWORD PTR [r9], ebx
	mov	rax, r14
	jmp	.L233
.L258:
	lea	r8, -4[0+rax*4]
	mov	esi, DWORD PTR [r9]
	lea	rbx, [r9+rax*4]
	cmp	r8, 4
	jle	.L240
	lea	rdx, 4[r9]
	mov	rcx, r9
	call	memmove
.L241:
	mov	DWORD PTR -4[rbx], esi
	mov	rax, r14
	jmp	.L233
.L247:
	jne	.L248
	mov	eax, DWORD PTR [r9]
	mov	DWORD PTR [rcx], eax
	jmp	.L248
.L240:
	jne	.L241
	mov	eax, DWORD PTR 4[r9]
	mov	DWORD PTR [r9], eax
	jmp	.L241
	.seh_endproc
	.p2align 4
	.def	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0:
.LFB2581:
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
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	rbx, QWORD PTR 176[rsp]
	mov	rsi, rcx
	mov	rdi, r8
	mov	r10, r9
	test	r9, r9
	je	.L261
	test	rbx, rbx
	je	.L261
	lea	rax, [r9+rbx]
	cmp	rax, 2
	je	.L278
	cmp	r9, rbx
	jle	.L264
	mov	r12, r9
	mov	rax, r8
	shr	r12, 63
	sub	rax, rdx
	add	r12, r9
	sar	r12
	mov	r9, r12
	lea	rcx, [rcx+r12*4]
	test	rax, rax
	jle	.L272
	mov	r13d, DWORD PTR [rcx]
	sar	rax, 2
	mov	r11, rdx
	jmp	.L267
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L280:
	sub	rax, r8
	lea	r11, 4[rbp]
	sub	rax, 1
	test	rax, rax
	jle	.L279
.L267:
	mov	r8, rax
	sar	r8
	lea	rbp, [r11+r8*4]
	cmp	r13d, DWORD PTR 0[rbp]
	jg	.L280
	mov	rax, r8
	test	rax, rax
	jg	.L267
.L279:
	mov	rbp, r11
	sub	rbp, rdx
	sar	rbp, 2
	sub	rbx, rbp
.L265:
	sub	r10, r12
	jmp	.L268
	.p2align 4,,10
	.p2align 3
.L264:
	mov	rax, rbx
	shr	rax, 63
	add	rax, rbx
	sar	rax
	mov	r13, rax
	mov	rbp, rax
	lea	r11, [rdx+rax*4]
	mov	rax, rdx
	sub	rax, rcx
	test	rax, rax
	jle	.L274
	mov	r12d, DWORD PTR [r11]
	sar	rax, 2
	jmp	.L271
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L282:
	sub	rax, r8
	lea	rcx, 4[rcx+r8*4]
	sub	rax, 1
	test	rax, rax
	jle	.L281
.L271:
	mov	r8, rax
	sar	r8
	cmp	DWORD PTR [rcx+r8*4], r12d
	jle	.L282
	mov	rax, r8
	test	rax, rax
	jg	.L271
.L281:
	mov	r9, rcx
	sub	r9, rsi
	sar	r9, 2
	sub	r10, r9
.L269:
	sub	rbx, r13
.L268:
	mov	r8, r11
	mov	QWORD PTR 72[rsp], r10
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 56[rsp], r11
	mov	QWORD PTR 48[rsp], rcx
	call	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0
	mov	QWORD PTR 32[rsp], rbp
	mov	r9, QWORD PTR 64[rsp]
	mov	rcx, rsi
	mov	rdx, QWORD PTR 48[rsp]
	mov	r8, rax
	mov	r12, rax
	call	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
	mov	r9, QWORD PTR 72[rsp]
	mov	r8, rdi
	mov	rcx, r12
	mov	rdx, QWORD PTR 56[rsp]
	mov	QWORD PTR 176[rsp], rbx
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	jmp	_ZSt22__merge_without_bufferIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_.isra.0
	.p2align 4,,10
	.p2align 3
.L278:
	mov	ecx, DWORD PTR [rdx]
	mov	eax, DWORD PTR [rsi]
	cmp	ecx, eax
	jge	.L261
	mov	DWORD PTR [rsi], ecx
	mov	DWORD PTR [rdx], eax
.L261:
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L272:
	mov	r11, rdx
	xor	ebp, ebp
	jmp	.L265
	.p2align 4,,10
	.p2align 3
.L274:
	xor	r9d, r9d
	jmp	.L269
	.seh_endproc
	.p2align 4
	.def	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0:
.LFB2585:
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
	mov	r9, rdx
	mov	rdi, rcx
	mov	rbp, rdx
	sub	r9, rcx
	cmp	r9, 56
	jle	.L299
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
.L283:
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L299:
	cmp	rcx, rdx
	je	.L283
	lea	rsi, 4[rcx]
	cmp	rdx, rsi
	je	.L283
	mov	ebx, DWORD PTR [rsi]
	mov	edx, DWORD PTR [rdi]
	cmp	ebx, edx
	jge	.L288
	.p2align 4
	.p2align 3
.L300:
	mov	r8, rsi
	sub	r8, rdi
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rsi+rax]
	cmp	r8, 4
	jle	.L289
	mov	rdx, rdi
	call	memmove
.L290:
	mov	DWORD PTR [rdi], ebx
.L291:
	add	rsi, 4
	cmp	rbp, rsi
	je	.L283
	mov	ebx, DWORD PTR [rsi]
	mov	edx, DWORD PTR [rdi]
	cmp	ebx, edx
	jl	.L300
.L288:
	mov	edx, DWORD PTR -4[rsi]
	cmp	edx, ebx
	jle	.L295
	lea	rax, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L293:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ebx, edx
	jl	.L293
	mov	DWORD PTR [rcx], ebx
	jmp	.L291
	.p2align 4,,10
	.p2align 3
.L289:
	jne	.L290
	mov	DWORD PTR [rcx], edx
	jmp	.L290
	.p2align 4,,10
	.p2align 3
.L295:
	mov	rcx, rsi
	mov	DWORD PTR [rcx], ebx
	jmp	.L291
	.seh_endproc
	.p2align 4
	.def	_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0
_ZSt16__merge_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_T2_.isra.0:
.LFB2586:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	r10, QWORD PTR 120[rsp]
	mov	r11, rcx
	mov	rbx, r8
	mov	rdi, rdx
	mov	rsi, rcx
	cmp	r9, QWORD PTR 112[rsp]
	jg	.L302
	mov	r8, rdx
	sub	r8, rcx
	cmp	r8, 4
	jle	.L303
	mov	rdx, rcx
	mov	rcx, r10
	mov	QWORD PTR 32[rsp], r8
	call	memmove
	mov	r8, QWORD PTR 32[rsp]
	mov	r10, rax
	add	r8, rax
	jmp	.L325
	.p2align 4,,10
	.p2align 3
.L310:
	add	rdi, 4
.L307:
	mov	DWORD PTR [rsi], eax
	add	rsi, 4
.L325:
	cmp	r10, r8
	je	.L301
	cmp	rbx, rdi
	je	.L309
	mov	eax, DWORD PTR [rdi]
	mov	edx, DWORD PTR [r10]
	cmp	eax, edx
	jl	.L310
	add	r10, 4
	mov	eax, edx
	jmp	.L307
	.p2align 4,,10
	.p2align 3
.L302:
	mov	rsi, r8
	sub	rsi, rdx
	cmp	rsi, 4
	jle	.L313
	mov	QWORD PTR 40[rsp], rcx
	mov	r8, rsi
	mov	rcx, r10
	mov	QWORD PTR 32[rsp], rdx
	call	memmove
	mov	rdx, QWORD PTR 32[rsp]
	mov	r11, QWORD PTR 40[rsp]
	mov	r10, rax
	lea	r8, [rax+rsi]
.L314:
	cmp	rdx, r11
	je	.L329
	cmp	r10, r8
	je	.L301
	sub	rdx, 4
	lea	rax, -4[r8]
	lea	rcx, -4[rbx]
	jmp	.L318
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L331:
	mov	DWORD PTR [rcx], r9d
	cmp	rdx, r11
	je	.L330
	sub	rdx, 4
.L322:
	sub	rcx, 4
.L318:
	mov	r8d, DWORD PTR [rax]
	mov	r9d, DWORD PTR [rdx]
	cmp	r8d, r9d
	jl	.L331
	mov	DWORD PTR [rcx], r8d
	cmp	r10, rax
	je	.L301
	sub	rax, 4
	jmp	.L322
.L303:
	je	.L332
.L301:
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L309:
	cmp	r8, r10
	je	.L301
	sub	r8, r10
	cmp	r8, 4
	jle	.L312
	mov	rdx, r10
	mov	rcx, rsi
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	memmove
.L313:
	jne	.L301
	mov	eax, DWORD PTR [rdx]
	lea	r8, 4[r10]
	mov	DWORD PTR [r10], eax
	jmp	.L314
	.p2align 4,,10
	.p2align 3
.L330:
	lea	r8, 4[rax]
	sub	r8, r10
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	add	rcx, rax
	cmp	r8, 4
	jle	.L321
.L328:
	mov	rdx, r10
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	memmove
.L332:
	mov	eax, DWORD PTR [rcx]
	lea	r8, 4[r10]
	mov	DWORD PTR [r10], eax
	jmp	.L325
.L329:
	sub	r8, r10
	mov	rcx, r8
	sal	rcx, 62
	sub	rcx, r8
	add	rcx, rbx
	cmp	r8, 4
	jg	.L328
	jne	.L301
.L326:
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR [rcx], eax
	jmp	.L301
.L312:
	jne	.L301
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR [rsi], eax
	jmp	.L301
.L321:
	jne	.L301
	jmp	.L326
	.seh_endproc
	.p2align 4
	.def	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0:
.LFB2589:
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
	.seh_endprologue
	mov	rbp, QWORD PTR 208[rsp]
	mov	r12, QWORD PTR 224[rsp]
	mov	r15, QWORD PTR 216[rsp]
	mov	rax, rbp
	cmp	r9, rbp
	mov	QWORD PTR 64[rsp], r8
	mov	r13, rcx
	mov	r10, rdx
	cmovle	rax, r9
	mov	rbx, r9
	cmp	rax, r12
	jle	.L388
	cmp	r9, rbp
	jle	.L335
	mov	rdx, r9
	mov	rax, QWORD PTR 64[rsp]
	shr	rdx, 63
	add	rdx, r9
	sub	rax, r10
	sar	rdx
	mov	r14, rdx
	lea	rsi, [rcx+rdx*4]
	test	rax, rax
	jle	.L389
	mov	ecx, DWORD PTR [rsi]
	sar	rax, 2
	mov	rdi, r10
	jmp	.L341
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L391:
	sub	rax, r8
	lea	rdi, 4[rdi+r8*4]
	sub	rax, 1
	test	rax, rax
	jle	.L390
.L341:
	mov	r8, rax
	sar	r8
	cmp	ecx, DWORD PTR [rdi+r8*4]
	jg	.L391
	mov	rax, r8
	test	rax, rax
	jg	.L341
.L390:
	mov	r9, rdi
	sub	rbx, rdx
	sub	r9, r10
	sar	r9, 2
	sub	rbp, r9
	cmp	r9, rbx
	jge	.L339
.L395:
	cmp	r12, r9
	jl	.L339
	mov	r11, rsi
	test	r9, r9
	jne	.L392
.L337:
	mov	QWORD PTR 32[rsp], r9
	mov	r8, r11
	mov	r9, r14
	mov	rdx, rsi
	mov	QWORD PTR 48[rsp], r12
	mov	rcx, r13
	mov	QWORD PTR 40[rsp], r15
	mov	QWORD PTR 72[rsp], r11
	call	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
	mov	r8, QWORD PTR 64[rsp]
	mov	r9, rbx
	mov	rdx, rdi
	mov	rcx, QWORD PTR 72[rsp]
	mov	QWORD PTR 224[rsp], r12
	mov	QWORD PTR 216[rsp], r15
	mov	QWORD PTR 208[rsp], rbp
	add	rsp, 104
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
.L335:
	mov	rdx, rbp
	mov	rax, r10
	shr	rdx, 63
	sub	rax, rcx
	add	rdx, rbp
	sar	rdx
	mov	r9, rdx
	lea	rdi, [r10+rdx*4]
	test	rax, rax
	jle	.L371
	mov	ecx, DWORD PTR [rdi]
	sar	rax, 2
	mov	rsi, r13
	jmp	.L345
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L394:
	sub	rax, r8
	lea	rsi, 4[rsi+r8*4]
	sub	rax, 1
	test	rax, rax
	jle	.L393
.L345:
	mov	r8, rax
	sar	r8
	cmp	ecx, DWORD PTR [rsi+r8*4]
	jge	.L394
	mov	rax, r8
	test	rax, rax
	jg	.L345
.L393:
	mov	rax, rsi
	sub	rax, r13
	sar	rax, 2
	mov	r14, rax
	sub	rbx, rax
.L343:
	sub	rbp, rdx
	cmp	r9, rbx
	jl	.L395
.L339:
	cmp	r12, rbx
	jl	.L356
	mov	r11, rdi
	test	rbx, rbx
	je	.L337
	mov	rax, r10
	sub	rax, rsi
	mov	QWORD PTR 72[rsp], rax
	cmp	rax, 4
	jle	.L357
	mov	r8, rax
	mov	rdx, rsi
	mov	rcx, r15
	mov	QWORD PTR 88[rsp], r10
	mov	QWORD PTR 80[rsp], r9
	call	memmove
	mov	rax, QWORD PTR 72[rsp]
	mov	r10, QWORD PTR 88[rsp]
	mov	r8, rdi
	mov	r9, QWORD PTR 80[rsp]
	mov	r11, rax
	sub	r8, r10
	sal	r11, 62
	sub	r11, rax
	add	r11, rdi
	cmp	r8, 4
	jle	.L396
	mov	rdx, r10
	mov	rcx, rsi
	mov	QWORD PTR 88[rsp], r11
	mov	QWORD PTR 80[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 80[rsp]
	mov	r11, QWORD PTR 88[rsp]
.L367:
	mov	r8, QWORD PTR 72[rsp]
	mov	rcx, r11
	mov	rdx, r15
	mov	QWORD PTR 80[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 80[rsp]
	mov	r11, rax
	jmp	.L337
	.p2align 4,,10
	.p2align 3
.L388:
	mov	QWORD PTR 216[rsp], r15
	mov	QWORD PTR 208[rsp], rbp
	add	rsp, 104
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
.L356:
	mov	r8, rdi
	mov	rdx, r10
	mov	rcx, rsi
	mov	QWORD PTR 72[rsp], r9
	call	_ZNSt3_V28__rotateIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEET_S8_S8_S8_St26random_access_iterator_tag.isra.0
	mov	r9, QWORD PTR 72[rsp]
	mov	r11, rax
	jmp	.L337
	.p2align 4,,10
	.p2align 3
.L392:
	mov	r8, rdi
	sub	r8, r10
	mov	QWORD PTR 72[rsp], r8
	cmp	r8, 4
	jle	.L346
	mov	rdx, r10
	mov	rcx, r15
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 80[rsp], r10
	call	memmove
	mov	r10, QWORD PTR 80[rsp]
	mov	r9, QWORD PTR 88[rsp]
	sub	r10, rsi
	mov	rax, r10
	mov	r8, r10
	sal	rax, 62
	sub	rax, r10
	cmp	r10, 4
	lea	rcx, [rdi+rax]
	jle	.L397
	mov	rdx, rsi
	mov	QWORD PTR 80[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 80[rsp]
.L354:
	mov	r8, QWORD PTR 72[rsp]
	mov	rdx, r15
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r9
	call	memmove
	mov	r11, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 80[rsp]
	add	r11, rsi
	jmp	.L337
	.p2align 4,,10
	.p2align 3
.L389:
	sub	rbx, rdx
	mov	rdi, r10
	test	r12, r12
	js	.L375
	mov	r11, rsi
	xor	r9d, r9d
	test	rbx, rbx
	jg	.L337
.L375:
	xor	r9d, r9d
	jmp	.L339
	.p2align 4,,10
	.p2align 3
.L371:
	mov	rsi, rcx
	xor	r14d, r14d
	jmp	.L343
.L346:
	je	.L398
	sub	r10, rsi
	mov	rcx, r10
	mov	r8, r10
	sal	rcx, 62
	sub	rcx, r10
	add	rcx, rdi
	cmp	r10, 4
	jle	.L399
	mov	rdx, rsi
	mov	QWORD PTR 72[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 72[rsp]
.L353:
	mov	r11, rsi
	jmp	.L337
	.p2align 4,,10
	.p2align 3
.L397:
	jne	.L354
	mov	eax, DWORD PTR [rsi]
	mov	DWORD PTR [rcx], eax
	jmp	.L354
.L357:
	je	.L400
	mov	r8, rdi
	sub	r8, r10
	cmp	r8, 4
	jle	.L364
	mov	rdx, r10
	mov	rcx, rsi
	mov	QWORD PTR 72[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 72[rsp]
.L366:
	mov	r11, rdi
	jmp	.L337
	.p2align 4,,10
	.p2align 3
.L396:
	jne	.L367
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR [rsi], eax
	jmp	.L367
.L398:
	mov	eax, DWORD PTR [r10]
	sub	r10, rsi
	mov	rcx, r10
	mov	r8, r10
	sal	rcx, 62
	mov	DWORD PTR [r15], eax
	sub	rcx, r10
	add	rcx, rdi
	cmp	r10, 4
	jle	.L401
	mov	rdx, rsi
	mov	QWORD PTR 72[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 72[rsp]
.L351:
	mov	eax, DWORD PTR [r15]
	lea	r11, 4[rsi]
	mov	DWORD PTR [rsi], eax
	jmp	.L337
.L400:
	mov	eax, DWORD PTR [rsi]
	mov	r8, rdi
	lea	r11, -4[rdi]
	sub	r8, r10
	mov	DWORD PTR [r15], eax
	cmp	r8, 4
	jle	.L361
	mov	rdx, r10
	mov	rcx, rsi
	mov	QWORD PTR 80[rsp], r11
	mov	QWORD PTR 72[rsp], r9
	call	memmove
	mov	r9, QWORD PTR 72[rsp]
	mov	r11, QWORD PTR 80[rsp]
.L363:
	mov	eax, DWORD PTR [r15]
	mov	DWORD PTR -4[rdi], eax
	jmp	.L337
.L399:
	jne	.L353
	mov	eax, DWORD PTR [rsi]
	mov	DWORD PTR [rcx], eax
	jmp	.L353
.L364:
	jne	.L366
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR [rsi], eax
	jmp	.L366
.L361:
	jne	.L363
	mov	eax, DWORD PTR [r10]
	mov	DWORD PTR [rsi], eax
	jmp	.L363
.L401:
	jne	.L351
	mov	eax, DWORD PTR [rsi]
	mov	DWORD PTR [rcx], eax
	jmp	.L351
	.seh_endproc
	.p2align 4
	.def	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0
_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0:
.LFB2590:
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
	mov	QWORD PTR 40[rsp], rbp
	mov	r9, rbx
	sub	rax, rbx
	sub	r9, rsi
	mov	r8, rdi
	mov	rdx, rbx
	sar	rax, 2
	sar	r9, 2
	mov	rcx, rsi
	mov	QWORD PTR 32[rsp], rax
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
	.def	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0:
.LFB2591:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	mov	rbx, rdx
	sub	rdx, rcx
	sar	rdx, 2
	lea	rax, 1[rdx]
	shr	rax, 63
	lea	rax, 1[rax+rdx]
	sar	rax
	lea	r11, 0[0+rax*4]
	lea	rsi, [rcx+r11]
	cmp	rax, r9
	jle	.L404
	mov	rdx, rsi
	mov	QWORD PTR 88[rsp], r11
	mov	QWORD PTR 72[rsp], r9
	mov	QWORD PTR 64[rsp], r8
	mov	QWORD PTR 80[rsp], rcx
	call	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
	mov	r9, QWORD PTR 72[rsp]
	mov	rdx, rbx
	mov	rcx, rsi
	mov	r8, QWORD PTR 64[rsp]
	call	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
	mov	rax, rbx
	mov	r9, QWORD PTR 72[rsp]
	mov	rdx, rsi
	mov	r8, QWORD PTR 64[rsp]
	sub	rax, rsi
	mov	r11, QWORD PTR 88[rsp]
	sar	rax, 2
	mov	QWORD PTR 48[rsp], r9
	mov	rcx, QWORD PTR 80[rsp]
	mov	QWORD PTR 40[rsp], r8
	sar	r11, 2
	mov	r8, rbx
	mov	QWORD PTR 32[rsp], rax
	mov	r9, r11
	call	_ZSt23__merge_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExS2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_SA_T1_SA_T2_.isra.0
	nop
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L404:
	mov	r9, r8
	mov	rdx, rsi
	mov	r8, rbx
	add	rsp, 104
	pop	rbx
	pop	rsi
	jmp	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0
	.seh_endproc
	.p2align 4
	.globl	_Z8sort_ascRSt6vectorIiSaIiEE
	.def	_Z8sort_ascRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sort_ascRSt6vectorIiSaIiEE
_Z8sort_ascRSt6vectorIiSaIiEE:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rdi
	je	.L407
	mov	rsi, rdi
	lea	rbx, 4[rbp]
	sub	rsi, rbp
	mov	rax, rsi
	sar	rax, 2
	je	.L441
	bsr	rax, rax
	mov	rdx, rdi
	mov	rcx, rbp
	movsxd	r8, eax
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	cmp	rsi, 64
	jle	.L440
	lea	rsi, 64[rbp]
	jmp	.L417
	.p2align 4,,10
	.p2align 3
.L443:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L412
	mov	rdx, rbp
	call	memmove
.L413:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rsi, rbx
	je	.L442
.L417:
	mov	r12d, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	cmp	r12d, edx
	jl	.L443
	mov	edx, DWORD PTR -4[rbx]
	cmp	r12d, edx
	jge	.L430
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L416:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jl	.L416
	mov	DWORD PTR [rcx], r12d
.L445:
	add	rbx, 4
	cmp	rsi, rbx
	jne	.L417
.L442:
	cmp	rdi, rsi
	je	.L407
	.p2align 4
	.p2align 3
.L418:
	mov	ecx, DWORD PTR [rsi]
	mov	edx, DWORD PTR -4[rsi]
	cmp	ecx, edx
	jge	.L431
	lea	rax, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L421:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L421
	add	rsi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rdi, rsi
	jne	.L418
.L407:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L444:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L424
	mov	rdx, rbp
	call	memmove
.L425:
	mov	DWORD PTR 0[rbp], esi
.L426:
	add	rbx, 4
.L440:
	cmp	rdi, rbx
	je	.L407
	mov	esi, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	cmp	esi, edx
	jl	.L444
	mov	edx, DWORD PTR -4[rbx]
	cmp	esi, edx
	jge	.L432
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L428:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	esi, edx
	jl	.L428
	mov	DWORD PTR [rcx], esi
	jmp	.L426
.L441:
	mov	r8, -2
	mov	rdx, rdi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	jmp	.L440
	.p2align 4,,10
	.p2align 3
.L431:
	mov	r8, rsi
	add	rsi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rdi, rsi
	jne	.L418
	jmp	.L407
.L412:
	jne	.L413
	mov	DWORD PTR [rcx], edx
	jmp	.L413
.L424:
	jne	.L425
	mov	DWORD PTR [rcx], edx
	jmp	.L425
.L430:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], r12d
	jmp	.L445
.L432:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], esi
	jmp	.L426
	.seh_endproc
	.p2align 4
	.globl	_Z9sort_descRSt6vectorIiSaIiEE
	.def	_Z9sort_descRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sort_descRSt6vectorIiSaIiEE
_Z9sort_descRSt6vectorIiSaIiEE:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	cmp	rbp, rdi
	je	.L446
	mov	rsi, rdi
	lea	rbx, 4[rbp]
	sub	rsi, rbp
	mov	rax, rsi
	sar	rax, 2
	je	.L480
	bsr	rax, rax
	mov	rdx, rdi
	mov	rcx, rbp
	movsxd	r8, eax
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_.isra.0
	cmp	rsi, 64
	jle	.L479
	lea	rsi, 64[rbp]
	jmp	.L456
	.p2align 4,,10
	.p2align 3
.L482:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L451
	mov	rdx, rbp
	call	memmove
.L452:
	add	rbx, 4
	mov	DWORD PTR 0[rbp], r12d
	cmp	rsi, rbx
	je	.L481
.L456:
	mov	edx, DWORD PTR 0[rbp]
	mov	r12d, DWORD PTR [rbx]
	cmp	edx, r12d
	jl	.L482
	mov	edx, DWORD PTR -4[rbx]
	cmp	r12d, edx
	jle	.L469
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L455:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	r12d, edx
	jg	.L455
	mov	DWORD PTR [rcx], r12d
.L484:
	add	rbx, 4
	cmp	rsi, rbx
	jne	.L456
.L481:
	cmp	rdi, rsi
	je	.L446
	.p2align 4
	.p2align 3
.L457:
	mov	ecx, DWORD PTR [rsi]
	mov	edx, DWORD PTR -4[rsi]
	cmp	ecx, edx
	jle	.L470
	lea	rax, -4[rsi]
	.p2align 5
	.p2align 4
	.p2align 3
.L460:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jg	.L460
	add	rsi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rdi, rsi
	jne	.L457
.L446:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L483:
	mov	r8, rbx
	sub	r8, rbp
	mov	rax, r8
	sal	rax, 62
	sub	rax, r8
	lea	rcx, 4[rbx+rax]
	cmp	r8, 4
	jle	.L463
	mov	rdx, rbp
	call	memmove
.L464:
	mov	DWORD PTR 0[rbp], esi
.L465:
	add	rbx, 4
.L479:
	cmp	rdi, rbx
	je	.L446
	mov	edx, DWORD PTR 0[rbp]
	mov	esi, DWORD PTR [rbx]
	cmp	edx, esi
	jl	.L483
	mov	edx, DWORD PTR -4[rbx]
	cmp	esi, edx
	jle	.L471
	lea	rax, -4[rbx]
	.p2align 5
	.p2align 4
	.p2align 3
.L467:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	esi, edx
	jg	.L467
	mov	DWORD PTR [rcx], esi
	jmp	.L465
.L480:
	mov	r8, -2
	mov	rdx, rdi
	mov	rcx, rbp
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_comp_iterIZ9sort_descRS5_EUliiE_EEEvT_SC_T0_T1_.isra.0
	jmp	.L479
	.p2align 4,,10
	.p2align 3
.L470:
	mov	r8, rsi
	add	rsi, 4
	mov	DWORD PTR [r8], ecx
	cmp	rdi, rsi
	jne	.L457
	jmp	.L446
.L451:
	jne	.L452
	mov	DWORD PTR [rcx], edx
	jmp	.L452
.L463:
	jne	.L464
	mov	DWORD PTR [rcx], edx
	jmp	.L464
.L469:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], r12d
	jmp	.L484
.L471:
	mov	rcx, rbx
	mov	DWORD PTR [rcx], esi
	jmp	.L465
	.seh_endproc
	.p2align 4
	.globl	_Z15stable_sort_ascRSt6vectorIiSaIiEE
	.def	_Z15stable_sort_ascRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15stable_sort_ascRSt6vectorIiSaIiEE
_Z15stable_sort_ascRSt6vectorIiSaIiEE:
.LFB2352:
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
	mov	rbx, QWORD PTR [rcx]
	mov	rbp, QWORD PTR 8[rcx]
	mov	r12, rbx
	cmp	rbx, rbp
	je	.L485
	mov	rdx, rbp
	sub	rdx, rbx
	mov	rax, rdx
	sar	rax, 2
	lea	rsi, 1[rax]
	shr	rsi, 63
	lea	rsi, 1[rax+rsi]
	sar	rsi
	test	rdx, rdx
	jle	.L487
	mov	r14, rsi
.L491:
	lea	r13, 0[0+r14*4]
	lea	rdx, 47[rsp]
	mov	rcx, r13
	call	_ZnwyRKSt9nothrow_t
	mov	rdi, rax
	test	rax, rax
	je	.L488
	cmp	rsi, r14
	jne	.L489
	add	rbx, r13
.L490:
	mov	r9, rdi
	mov	r8, rbp
	mov	rdx, rbx
	mov	rcx, r12
	call	_ZSt22__stable_sort_adaptiveIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_NS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_T1_.isra.0
.L493:
	mov	rdx, r13
	mov	rcx, rdi
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L485:
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
.L489:
	mov	r9, r14
	mov	r8, rax
	mov	rdx, rbp
	mov	rcx, rbx
	call	_ZSt29__stable_sort_adaptive_resizeIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEES2_xNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_T2_.isra.0
	jmp	.L493
	.p2align 4,,10
	.p2align 3
.L487:
	test	rsi, rsi
	jne	.L492
	xor	r13d, r13d
	xor	edi, edi
	jmp	.L490
.L492:
	mov	rdx, rbp
	mov	rcx, rbx
	xor	r13d, r13d
	xor	edi, edi
	call	_ZSt21__inplace_stable_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	jmp	.L493
.L488:
	cmp	r14, 1
	je	.L487
	add	r14, 1
	sar	r14
	jmp	.L491
	.seh_endproc
	.section	.text$_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	.def	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_:
.LFB2412:
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
	mov	r9, rdx
	mov	rax, rcx
	mov	rdx, r8
	mov	rcx, r9
	sub	rcx, rax
	cmp	rcx, 4
	jle	.L498
	mov	rdi, rcx
	mov	r14, rcx
	mov	r13, r9
	sar	rdi, 2
	lea	r8, -2[rdi]
	lea	rsi, -1[rdi]
	shr	r8, 63
	sar	rsi
	lea	r8, -2[rdi+r8]
	sar	r8
	mov	rbp, r8
	mov	r11, r8
	lea	r8, [rax+r8*4]
	mov	r12d, DWORD PTR [r8]
	mov	rcx, r8
	cmp	r11, rsi
	jge	.L499
	.p2align 4
	.p2align 3
.L548:
	mov	QWORD PTR [rsp], r14
	mov	rbx, r11
	mov	QWORD PTR 8[rsp], r11
	jmp	.L501
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L526:
	mov	rbx, r9
.L501:
	lea	rcx, 1[rbx]
	lea	r9, [rcx+rcx]
	lea	rcx, [rax+rcx*8]
	lea	r11, -1[r9]
	mov	r10d, DWORD PTR [rcx]
	lea	r14, [rax+r11*4]
	mov	r15d, DWORD PTR [r14]
	cmp	r15d, r10d
	cmovg	r10d, r15d
	cmovg	r9, r11
	cmovg	rcx, r14
	mov	DWORD PTR [rax+rbx*4], r10d
	cmp	r9, rsi
	jl	.L526
	mov	r14, QWORD PTR [rsp]
	mov	r11, QWORD PTR 8[rsp]
	test	dil, 1
	jne	.L544
	cmp	rbp, r9
	je	.L528
.L544:
	lea	r10, -1[r9]
	shr	r10, 63
	lea	r10, -1[r9+r10]
	sar	r10
	mov	QWORD PTR [rsp], r10
	cmp	r11, r9
	jge	.L505
.L541:
	mov	r10, QWORD PTR [rsp]
	lea	rcx, 0[0+r9*4]
	jmp	.L508
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L547:
	mov	DWORD PTR [rcx], ebx
	lea	rcx, -1[r10]
	mov	rbx, r10
	shr	rcx, 63
	lea	rcx, -1[rcx+r10]
	cmp	r11, r10
	jge	.L546
	sar	rcx
	mov	r10, rcx
	lea	rcx, 0[0+rbx*4]
.L508:
	lea	r9, [rax+r10*4]
	add	rcx, rax
	mov	ebx, DWORD PTR [r9]
	cmp	r12d, ebx
	jg	.L547
.L505:
	mov	DWORD PTR [rcx], r12d
	test	r11, r11
	je	.L543
.L549:
	sub	r8, 4
.L507:
	sub	r11, 1
	mov	r12d, DWORD PTR [r8]
	mov	rcx, r8
	cmp	r11, rsi
	jl	.L548
.L499:
	test	dil, 1
	jne	.L505
	cmp	r11, rbp
	jne	.L505
	mov	QWORD PTR [rsp], r11
	jmp	.L504
	.p2align 4,,10
	.p2align 3
.L546:
	mov	rcx, r9
	mov	DWORD PTR [rcx], r12d
	test	r11, r11
	jne	.L549
.L543:
	mov	rcx, r14
	mov	r9, r13
.L498:
	cmp	r9, rdx
	jnb	.L497
	mov	rdi, rcx
	mov	r12, r9
	sar	rdi, 2
	lea	rsi, -1[rdi]
	lea	rbp, -2[rdi]
	shr	rsi, 63
	sar	rbp
	lea	rsi, -1[rsi+rdi]
	sar	rsi
	jmp	.L523
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L511:
	add	r12, 4
	cmp	r12, rdx
	jnb	.L497
.L523:
	mov	ebx, DWORD PTR [r12]
	mov	r8d, DWORD PTR [rax]
	cmp	ebx, r8d
	jge	.L511
	mov	DWORD PTR [r12], r8d
	cmp	rcx, 8
	jle	.L512
	xor	r15d, r15d
	jmp	.L514
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L530:
	mov	r15, r8
.L514:
	lea	r9, 1[r15]
	lea	r8, [r9+r9]
	lea	r9, [rax+r9*8]
	lea	r11, -1[r8]
	mov	r10d, DWORD PTR [r9]
	lea	r13, [rax+r11*4]
	mov	r14d, DWORD PTR 0[r13]
	cmp	r14d, r10d
	cmovg	r10d, r14d
	cmovg	r8, r11
	cmovg	r9, r13
	mov	DWORD PTR [rax+r15*4], r10d
	cmp	rsi, r8
	jg	.L530
	test	dil, 1
	jne	.L545
	cmp	rbp, r8
	je	.L520
.L545:
	lea	r10, -1[r8]
	shr	r10, 63
	lea	r10, -1[r8+r10]
	sar	r10
	test	r8, r8
	jne	.L522
	jmp	.L517
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L551:
	lea	r8, -1[r10]
	mov	DWORD PTR [r9], r11d
	shr	r8, 63
	lea	r9, -1[r8+r10]
	mov	r8, r10
	test	r10, r10
	je	.L550
	mov	r10, r9
	sar	r10
.L522:
	lea	r13, [rax+r10*4]
	lea	r9, [rax+r8*4]
	mov	r11d, DWORD PTR 0[r13]
	cmp	ebx, r11d
	jg	.L551
.L517:
	mov	DWORD PTR [r9], ebx
.L552:
	add	r12, 4
	cmp	r12, rdx
	jb	.L523
.L497:
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
.L550:
	mov	r9, r13
	mov	DWORD PTR [r9], ebx
	jmp	.L552
	.p2align 4,,10
	.p2align 3
.L528:
	mov	QWORD PTR [rsp], rbp
.L504:
	mov	rbx, QWORD PTR [rsp]
	lea	r9, 1[rbx+rbx]
	mov	r10d, DWORD PTR [rax+r9*4]
	mov	DWORD PTR [rcx], r10d
	cmp	r11, r9
	jl	.L541
	mov	DWORD PTR [rax+r9*4], r12d
	sub	r8, 4
	jmp	.L507
	.p2align 4,,10
	.p2align 3
.L512:
	mov	r9, rax
	test	dil, 1
	jne	.L517
	cmp	rdi, 2
	jne	.L517
	xor	r8d, r8d
	.p2align 4
	.p2align 3
.L520:
	lea	r11, 1[r8+r8]
	mov	r10d, DWORD PTR [rax+r11*4]
	mov	DWORD PTR [r9], r10d
	mov	r10, r8
	mov	r8, r11
	jmp	.L522
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z16median_partitionRSt6vectorIiSaIiEE
	.def	_Z16median_partitionRSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16median_partitionRSt6vectorIiSaIiEE
_Z16median_partitionRSt6vectorIiSaIiEE:
.LFB2353:
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
	mov	rbx, QWORD PTR [rcx]
	cmp	rsi, rbx
	je	.L553
	mov	rax, rsi
	sub	rax, rbx
	mov	rdx, rax
	sar	rdx, 2
	mov	rcx, rdx
	shr	rcx
	lea	rbp, [rbx+rcx*4]
	cmp	rbp, rsi
	je	.L553
	cmp	rax, 12
	jle	.L555
	bsr	r11, rdx
	movsxd	r11, r11d
	add	r11, r11
	.p2align 4
	.p2align 3
.L556:
	sar	rax, 3
	movq	xmm0, QWORD PTR [rbx]
	mov	edx, DWORD PTR -4[rsi]
	lea	r9, 4[rbx]
	lea	rdi, [rbx+rax*4]
	mov	eax, DWORD PTR [rdi]
	pshufd	xmm1, xmm0, 0xe5
	movd	ecx, xmm1
	movd	r8d, xmm0
	cmp	eax, ecx
	jle	.L558
	cmp	edx, eax
	jg	.L563
	cmp	edx, ecx
	jg	.L588
.L561:
	pshufd	xmm0, xmm0, 225
	movq	QWORD PTR [rbx], xmm0
.L560:
	mov	rax, rsi
	cmp	ecx, r8d
	jle	.L580
	.p2align 4
	.p2align 3
.L591:
	lea	rdx, 4[r9]
	jmp	.L565
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L581:
	add	rdx, 4
.L565:
	mov	r8d, DWORD PTR [rdx]
	cmp	r8d, ecx
	jl	.L581
	mov	r9d, DWORD PTR -4[rax]
	cmp	ecx, r9d
	jge	.L566
.L592:
	sub	rax, 8
	jmp	.L567
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L582:
	sub	rax, 4
.L567:
	mov	r9d, DWORD PTR [rax]
	cmp	r9d, ecx
	jg	.L582
	cmp	rdx, rax
	jnb	.L590
.L569:
	mov	DWORD PTR [rdx], r9d
	lea	r9, 4[rdx]
	mov	DWORD PTR [rax], r8d
	mov	ecx, DWORD PTR [rbx]
	mov	r8d, DWORD PTR 4[rdx]
	cmp	ecx, r8d
	jg	.L591
.L580:
	mov	rdx, r9
	mov	r9d, DWORD PTR -4[rax]
	cmp	ecx, r9d
	jl	.L592
	.p2align 4
	.p2align 3
.L566:
	sub	rax, 4
	cmp	rdx, rax
	jb	.L569
	.p2align 4
	.p2align 3
.L590:
	cmp	rbp, rdx
	cmovb	rsi, rdx
	cmovnb	rbx, rdx
	mov	rax, rsi
	sub	rax, rbx
	cmp	rax, 12
	jle	.L593
	sub	r11, 1
	jne	.L556
	lea	rdx, 4[rbp]
	xor	r9d, r9d
	mov	r8, rsi
	mov	rcx, rbx
	call	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	mov	eax, DWORD PTR [rbx]
	mov	edx, DWORD PTR 0[rbp]
	mov	DWORD PTR [rbx], edx
	mov	DWORD PTR 0[rbp], eax
.L553:
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L558:
	cmp	edx, ecx
	jg	.L561
	cmp	edx, eax
	jle	.L563
.L588:
	mov	DWORD PTR [rbx], edx
	mov	DWORD PTR -4[rsi], r8d
	mov	r8d, DWORD PTR 4[rbx]
	mov	ecx, DWORD PTR [rbx]
	jmp	.L560
.L563:
	mov	DWORD PTR [rbx], eax
	mov	DWORD PTR [rdi], r8d
	mov	r8d, DWORD PTR 4[rbx]
	mov	ecx, DWORD PTR [rbx]
	jmp	.L560
.L593:
	cmp	rsi, rbx
	je	.L553
.L555:
	lea	rdi, 4[rbx]
	cmp	rsi, rdi
	je	.L553
	mov	ebp, DWORD PTR [rdi]
	mov	eax, DWORD PTR [rbx]
	mov	rcx, rdi
	cmp	ebp, eax
	jge	.L573
.L594:
	mov	r8, rdi
	sub	r8, rbx
	mov	rdx, r8
	sal	rdx, 62
	sub	rdx, r8
	lea	rcx, 4[rdi+rdx]
	cmp	r8, 4
	jle	.L574
	mov	rdx, rbx
	call	memmove
.L575:
	mov	DWORD PTR [rbx], ebp
.L576:
	add	rdi, 4
	cmp	rsi, rdi
	je	.L553
	mov	ebp, DWORD PTR [rdi]
	mov	eax, DWORD PTR [rbx]
	mov	rcx, rdi
	cmp	ebp, eax
	jl	.L594
.L573:
	mov	edx, DWORD PTR -4[rdi]
	cmp	edx, ebp
	jle	.L577
	lea	rax, -4[rdi]
	.p2align 5
	.p2align 4
	.p2align 3
.L578:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ebp, edx
	jl	.L578
.L577:
	mov	DWORD PTR [rcx], ebp
	jmp	.L576
.L574:
	jne	.L575
	mov	DWORD PTR [rcx], eax
	jmp	.L575
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZnwyRKSt9nothrow_t;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
