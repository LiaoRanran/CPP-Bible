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
	.def	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0:
.LFB6646:
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
	cmp	rcx, rdx
	mov	rdi, rcx
	mov	r12, rdx
	je	.L3
	lea	rbx, 4[rcx]
	cmp	rdx, rbx
	je	.L3
	mov	ebp, 4
	.p2align 4,,10
	.p2align 3
.L12:
	mov	esi, DWORD PTR [rbx]
	mov	rcx, rbx
	mov	eax, DWORD PTR [rdi]
	cmp	esi, eax
	jge	.L6
	mov	r8, rbx
	sub	r8, rdi
	cmp	r8, 4
	jle	.L7
	mov	rcx, rbp
	mov	rdx, rdi
	sub	rcx, r8
	add	rcx, rbx
	call	memmove
.L8:
	mov	DWORD PTR [rdi], esi
.L9:
	add	rbx, 4
	cmp	rbx, r12
	jne	.L12
.L3:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	mov	edx, DWORD PTR -4[rbx]
	lea	rax, -4[rbx]
	cmp	esi, edx
	jge	.L10
	.p2align 4,,10
	.p2align 3
.L11:
	mov	DWORD PTR 4[rax], edx
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	esi, edx
	jl	.L11
.L10:
	mov	DWORD PTR [rcx], esi
	jmp	.L9
.L7:
	jne	.L8
	mov	DWORD PTR [rbx], eax
	jmp	.L8
	.seh_endproc
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB6649:
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
	je	.L20
	cmp	BYTE PTR 56[rsi], 0
	je	.L17
	movsx	edx, BYTE PTR 67[rsi]
.L18:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L17:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L18
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L18
.L20:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.p2align 4
	.def	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0:
.LFB6651:
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
	jle	.L21
	lea	rbx, 4[rcx]
	test	r8, r8
	je	.L65
.L24:
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
	jge	.L51
	cmp	eax, r8d
	jl	.L57
	cmp	ecx, r8d
	jl	.L86
.L54:
	movq	QWORD PTR [rsi], xmm1
	mov	r9d, DWORD PTR -4[rbp]
.L53:
	cmp	ecx, edx
	mov	r10, rbp
	mov	rax, rbx
	jle	.L75
	.p2align 4,,10
	.p2align 3
.L88:
	add	rax, 4
	.p2align 4,,10
	.p2align 3
.L59:
	mov	r11, rax
	mov	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	ecx, edx
	jg	.L59
	cmp	ecx, r9d
	jge	.L60
.L89:
	lea	rax, -8[r10]
	.p2align 4,,10
	.p2align 3
.L61:
	mov	r10, rax
	mov	r9d, DWORD PTR [rax]
	sub	rax, 4
	cmp	ecx, r9d
	jl	.L61
	cmp	r11, r10
	jnb	.L87
.L63:
	mov	DWORD PTR [r11], r9d
	lea	rax, 4[r11]
	mov	r9d, DWORD PTR -4[r10]
	mov	DWORD PTR [r10], edx
	mov	edx, DWORD PTR 4[r11]
	mov	ecx, DWORD PTR [rsi]
	cmp	ecx, edx
	jg	.L88
.L75:
	cmp	ecx, r9d
	mov	r11, rax
	jl	.L89
	.p2align 4,,10
	.p2align 3
.L60:
	sub	r10, 4
	cmp	r11, r10
	jb	.L63
	.p2align 4,,10
	.p2align 3
.L87:
	mov	rcx, r11
	mov	r8, rdi
	mov	rdx, rbp
	mov	QWORD PTR 40[rsp], r11
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	mov	r11, QWORD PTR 40[rsp]
	mov	rax, r11
	sub	rax, rsi
	cmp	rax, 64
	jle	.L21
	test	rdi, rdi
	je	.L65
	mov	rbp, r11
	jmp	.L24
.L51:
	cmp	ecx, r8d
	jl	.L54
	cmp	eax, r8d
	jge	.L57
.L86:
	mov	DWORD PTR [rsi], r8d
	mov	r9d, edx
	mov	DWORD PTR -4[rbp], edx
	mov	ecx, DWORD PTR [rsi]
	mov	edx, DWORD PTR 4[rsi]
	jmp	.L53
.L57:
	mov	DWORD PTR [rsi], eax
	mov	DWORD PTR [r9], edx
	mov	edx, DWORD PTR 4[rsi]
	mov	ecx, DWORD PTR [rsi]
	mov	r9d, DWORD PTR -4[rbp]
	jmp	.L53
.L35:
	sub	r11, 4
	.p2align 4,,10
	.p2align 3
.L50:
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
	jle	.L38
	xor	r10d, r10d
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L72:
	mov	r10, rax
.L40:
	lea	rdx, 1[r10]
	lea	rax, [rdx+rdx]
	lea	rbx, -1[rax]
	lea	rdi, [rsi+rbx*4]
	lea	rdx, [rsi+rdx*8]
	mov	ebp, DWORD PTR [rdi]
	mov	ecx, DWORD PTR [rdx]
	cmp	ebp, ecx
	jle	.L39
	mov	ecx, ebp
	mov	rdx, rdi
	mov	rax, rbx
.L39:
	cmp	rax, r13
	mov	DWORD PTR [rsi+r10*4], ecx
	jl	.L72
	test	r14, r14
	je	.L44
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L48
	jmp	.L90
	.p2align 4,,10
	.p2align 3
.L92:
	mov	DWORD PTR [rdx], r10d
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	test	rcx, rcx
	mov	rdx, rax
	mov	rax, rcx
	je	.L91
	mov	rcx, rdx
.L48:
	lea	rbx, [rsi+rcx*4]
	mov	r10d, DWORD PTR [rbx]
	lea	rdx, [rsi+rax*4]
	cmp	r8d, r10d
	jg	.L92
.L43:
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L50
.L21:
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
.L65:
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
	jge	.L69
.L96:
	mov	rcx, r8
	jmp	.L27
	.p2align 4,,10
	.p2align 3
.L70:
	mov	rcx, rax
.L27:
	lea	rdx, 1[rcx]
	lea	rax, [rdx+rdx]
	lea	r13, -1[rax]
	lea	r14, [rsi+r13*4]
	lea	r12, [rsi+rdx*8]
	mov	r15d, DWORD PTR [r14]
	mov	edx, DWORD PTR [r12]
	cmp	r15d, edx
	jle	.L26
	mov	edx, r15d
	mov	r12, r14
	mov	rax, r13
.L26:
	cmp	rax, rbx
	mov	DWORD PTR [rsi+rcx*4], edx
	jl	.L70
.L25:
	cmp	rbp, rax
	jne	.L77
	test	r9b, r9b
	jne	.L28
.L77:
	lea	rcx, -1[rax]
	sar	rcx
	cmp	r8, rax
	jl	.L33
	jmp	.L93
	.p2align 4,,10
	.p2align 3
.L95:
	mov	DWORD PTR [rax], edx
	lea	rdx, -1[rcx]
	mov	rax, rdx
	shr	rax, 63
	add	rax, rdx
	sar	rax
	cmp	r8, rcx
	mov	rdx, rax
	mov	rax, rcx
	jge	.L94
	mov	rcx, rdx
.L33:
	lea	r12, [rsi+rcx*4]
	mov	edx, DWORD PTR [r12]
	lea	rax, [rsi+rax*4]
	cmp	r10d, edx
	jg	.L95
.L32:
	test	r8, r8
	mov	DWORD PTR [rax], r10d
	je	.L35
.L34:
	sub	r8, 1
	sub	rdi, 4
	mov	r10d, DWORD PTR [rdi]
	cmp	r8, rbx
	mov	r12, rdi
	jl	.L96
.L69:
	mov	rax, r8
	jmp	.L25
.L94:
	mov	rax, r12
	jmp	.L32
.L91:
	mov	rdx, rbx
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L50
	jmp	.L21
.L44:
	lea	rcx, -2[r12]
	sar	rcx
	cmp	rcx, rax
	je	.L47
	lea	r10, -1[rax]
	mov	rcx, r10
	shr	rcx, 63
	add	rcx, r10
	sar	rcx
	test	rax, rax
	jne	.L48
	jmp	.L43
	.p2align 4,,10
	.p2align 3
.L42:
	cmp	rdx, 2
	mov	rdx, rsi
	ja	.L43
	xor	eax, eax
.L47:
	lea	r10, 1[rax+rax]
	mov	ecx, DWORD PTR [rsi+r10*4]
	mov	DWORD PTR [rdx], ecx
	mov	rcx, rax
	mov	rax, r10
	jmp	.L48
.L38:
	test	r14, r14
	je	.L42
	mov	rdx, rsi
	sub	r11, 4
	cmp	r9, 4
	mov	DWORD PTR [rdx], r8d
	jg	.L50
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L28:
	lea	rcx, [rax+rax]
	lea	rax, 1[rcx]
	sar	rcx
	lea	rdx, [rsi+rax*4]
	cmp	r8, rax
	mov	r13d, DWORD PTR [rdx]
	mov	DWORD PTR [r12], r13d
	mov	r12, rdx
	jl	.L33
.L93:
	mov	DWORD PTR [r12], r10d
	jmp	.L34
.L90:
	mov	DWORD PTR [rdx], r8d
	sub	r11, 4
	jmp	.L50
	.seh_endproc
	.section	.text$_ZNSt6vectorIiSaIiEEC1ERKS1_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIiSaIiEEC1ERKS1_
	.def	_ZNSt6vectorIiSaIiEEC1ERKS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEEC1ERKS1_
_ZNSt6vectorIiSaIiEEC1ERKS1_:
.LFB5679:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	pxor	xmm0, xmm0
	mov	rbx, QWORD PTR 8[rdx]
	sub	rbx, QWORD PTR [rdx]
	mov	rsi, rcx
	mov	rdi, rdx
	movups	XMMWORD PTR [rcx], xmm0
	mov	QWORD PTR 16[rcx], 0
	je	.L103
	movabs	rax, 9223372036854775804
	cmp	rax, rbx
	jb	.L104
	mov	rcx, rbx
	call	_Znwy
	mov	rcx, rax
.L98:
	add	rbx, rcx
	movq	xmm1, rcx
	mov	QWORD PTR 16[rsi], rbx
	movddup	xmm0, xmm1
	movups	XMMWORD PTR [rsi], xmm0
	mov	rdx, QWORD PTR [rdi]
	mov	r8, QWORD PTR 8[rdi]
	sub	r8, rdx
	cmp	r8, 4
	jle	.L100
	mov	rbx, r8
	call	memmove
	mov	rcx, rax
.L101:
	add	rcx, rbx
	mov	QWORD PTR 8[rsi], rcx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L103:
	xor	ecx, ecx
	jmp	.L98
	.p2align 4,,10
	.p2align 3
.L100:
	mov	rbx, r8
	jne	.L101
	mov	eax, DWORD PTR [rdx]
	mov	ebx, 4
	mov	DWORD PTR [rcx], eax
	jmp	.L101
	.p2align 4,,10
	.p2align 3
.L104:
	call	_ZSt28__throw_bad_array_new_lengthv
	nop
	.seh_endproc
	.section	.text$_ZNSt6vectorIiSaIiEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIiSaIiEED1Ev
	.def	_ZNSt6vectorIiSaIiEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEED1Ev
_ZNSt6vectorIiSaIiEED1Ev:
.LFB6063:
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
	.section	.text$_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_
	.def	_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_
_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_:
.LFB6078:
	.seh_endprologue
	mov	r8d, 1
	cmp	rcx, rdx
	je	.L107
	lea	rax, 4[rcx]
	cmp	rax, rdx
	je	.L107
	mov	ecx, DWORD PTR [rcx]
	jmp	.L110
	.p2align 4,,10
	.p2align 3
.L109:
	add	rax, 4
	cmp	rdx, rax
	je	.L114
.L110:
	mov	r8d, ecx
	mov	ecx, DWORD PTR [rax]
	cmp	ecx, r8d
	jge	.L109
	cmp	rax, rdx
	sete	r8b
.L107:
	mov	eax, r8d
	ret
	.p2align 4,,10
	.p2align 3
.L114:
	mov	r8d, 1
	mov	eax, r8d
	ret
	.seh_endproc
	.section	.text$_ZSt14__partial_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt14__partial_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	.def	_ZSt14__partial_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt14__partial_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
_ZSt14__partial_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_:
.LFB6284:
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
	mov	rax, rcx
	mov	r9, rdx
	mov	r10, rdx
	sub	r9, rax
	mov	rcx, r8
	cmp	r9, 4
	jle	.L116
	mov	r14, r9
	mov	QWORD PTR 32[rsp], r9
	sar	r14, 2
	mov	QWORD PTR 24[rsp], rdx
	lea	r11, -2[r14]
	mov	r13, r14
	mov	QWORD PTR 40[rsp], r14
	lea	rsi, -1[r14]
	mov	r8, r11
	and	r13d, 1
	shr	r8, 63
	mov	ebp, r13d
	sar	rsi
	add	r8, r11
	xor	ebp, 1
	mov	r14, r13
	mov	rdi, r8
	mov	r13, rdx
	sar	rdi
	lea	r8, [rax+rdi*4]
	mov	r11, rdi
	cmp	rsi, r11
	mov	r12d, DWORD PTR [r8]
	mov	r9, r8
	jle	.L156
	.p2align 4,,10
	.p2align 3
.L183:
	mov	rbx, r11
	mov	QWORD PTR 8[rsp], r11
	mov	DWORD PTR 20[rsp], r12d
	jmp	.L119
	.p2align 4,,10
	.p2align 3
.L157:
	mov	rbx, rdx
.L119:
	lea	r9, 1[rbx]
	lea	rdx, [r9+r9]
	lea	r11, -1[rdx]
	lea	r12, [rax+r11*4]
	lea	r9, [rax+r9*8]
	mov	r15d, DWORD PTR [r12]
	mov	r10d, DWORD PTR [r9]
	cmp	r15d, r10d
	jle	.L118
	mov	r10d, r15d
	mov	r9, r12
	mov	rdx, r11
.L118:
	cmp	rsi, rdx
	mov	DWORD PTR [rax+rbx*4], r10d
	jg	.L157
	mov	r11, QWORD PTR 8[rsp]
	mov	r12d, DWORD PTR 20[rsp]
.L117:
	cmp	rdi, rdx
	jne	.L165
	test	bpl, bpl
	jne	.L120
.L165:
	lea	rbx, -1[rdx]
	mov	r10, rbx
	shr	r10, 63
	add	r10, rbx
	sar	r10
.L122:
	cmp	r11, rdx
	jge	.L123
	mov	r9, rdx
	jmp	.L124
	.p2align 4,,10
	.p2align 3
.L182:
	mov	DWORD PTR [r9], ebx
	lea	r9, -1[r10]
	mov	rdx, r9
	shr	rdx, 63
	add	rdx, r9
	mov	r9, r10
	sar	rdx
	cmp	r11, r10
	jge	.L181
	mov	r10, rdx
.L124:
	lea	r15, [rax+r10*4]
	mov	ebx, DWORD PTR [r15]
	lea	r9, [rax+r9*4]
	cmp	r12d, ebx
	jg	.L182
.L123:
	sub	r8, 4
	test	r11, r11
	mov	DWORD PTR [r9], r12d
	je	.L125
.L184:
	sub	r11, 1
	mov	r12d, DWORD PTR [r8]
	mov	r9, r8
	cmp	rsi, r11
	jg	.L183
.L156:
	mov	rdx, r11
	jmp	.L117
	.p2align 4,,10
	.p2align 3
.L181:
	mov	r9, r15
	sub	r8, 4
	test	r11, r11
	mov	DWORD PTR [r9], r12d
	jne	.L184
.L125:
	mov	r10, r13
	mov	rdx, QWORD PTR 24[rsp]
	mov	r13, r14
	cmp	r10, rcx
	mov	r9, QWORD PTR 32[rsp]
	mov	r14, QWORD PTR 40[rsp]
	jnb	.L154
.L127:
	lea	r8, -1[r14]
	mov	rdi, r10
	mov	r12, r8
	shr	r12, 63
	add	r12, r8
	lea	r8, -2[r14]
	sar	r12
	mov	rbp, r8
	shr	rbp, 63
	add	rbp, r8
	sar	rbp
	jmp	.L141
	.p2align 4,,10
	.p2align 3
.L130:
	add	rdi, 4
	cmp	rdi, rcx
	jnb	.L185
.L141:
	mov	esi, DWORD PTR [rdi]
	mov	r8d, DWORD PTR [rax]
	cmp	esi, r8d
	jge	.L130
	cmp	r9, 8
	mov	DWORD PTR [rdi], r8d
	jle	.L131
	xor	ebx, ebx
	mov	QWORD PTR 8[rsp], rdx
	jmp	.L133
	.p2align 4,,10
	.p2align 3
.L159:
	mov	rbx, r8
.L133:
	lea	rdx, 1[rbx]
	lea	r8, [rdx+rdx]
	lea	r11, -1[r8]
	lea	r14, [rax+r11*4]
	lea	r10, [rax+rdx*8]
	mov	r15d, DWORD PTR [r14]
	mov	edx, DWORD PTR [r10]
	cmp	r15d, edx
	jle	.L132
	mov	edx, r15d
	mov	r10, r14
	mov	r8, r11
.L132:
	cmp	r12, r8
	mov	DWORD PTR [rax+rbx*4], edx
	jg	.L159
	test	r13, r13
	mov	rdx, QWORD PTR 8[rsp]
	jne	.L180
	cmp	rbp, r8
	je	.L139
.L180:
	lea	rbx, -1[r8]
	mov	r11, rbx
	shr	r11, 63
	add	r11, rbx
	sar	r11
.L138:
	test	r8, r8
	jle	.L136
	mov	r10, r8
	jmp	.L140
	.p2align 4,,10
	.p2align 3
.L187:
	mov	DWORD PTR [r10], r14d
	lea	r10, -1[r11]
	mov	r8, r10
	shr	r8, 63
	add	r8, r10
	mov	r10, r11
	sar	r8
	test	r11, r11
	je	.L186
	mov	r11, r8
.L140:
	lea	rbx, [rax+r11*4]
	mov	r14d, DWORD PTR [rbx]
	lea	r10, [rax+r10*4]
	cmp	esi, r14d
	jg	.L187
.L136:
	mov	DWORD PTR [r10], esi
.L191:
	add	rdi, 4
	cmp	rdi, rcx
	jb	.L141
.L185:
	cmp	r9, 4
	jle	.L115
	.p2align 4,,10
	.p2align 3
.L154:
	sub	rdx, 4
	mov	ecx, DWORD PTR [rax]
	mov	r11, rdx
	mov	r10d, DWORD PTR [rdx]
	sub	r11, rax
	mov	r13, r11
	sar	r13, 2
	mov	DWORD PTR [rdx], ecx
	lea	rcx, -1[r13]
	mov	r14, r13
	mov	r12, rcx
	and	r14d, 1
	shr	r12, 63
	add	r12, rcx
	sar	r12
	cmp	r11, 8
	jle	.L143
	xor	ebx, ebx
	jmp	.L145
	.p2align 4,,10
	.p2align 3
.L162:
	mov	rbx, rcx
.L145:
	lea	r8, 1[rbx]
	lea	rcx, [r8+r8]
	lea	rsi, -1[rcx]
	lea	rdi, [rax+rsi*4]
	lea	r8, [rax+r8*8]
	mov	ebp, DWORD PTR [rdi]
	mov	r9d, DWORD PTR [r8]
	cmp	ebp, r9d
	jle	.L144
	mov	r9d, ebp
	mov	r8, rdi
	mov	rcx, rsi
.L144:
	cmp	r12, rcx
	mov	DWORD PTR [rax+rbx*4], r9d
	jg	.L162
	test	r14, r14
	je	.L149
	lea	rbx, -1[rcx]
	mov	r9, rbx
	shr	r9, 63
	add	r9, rbx
	sar	r9
	test	rcx, rcx
	jne	.L153
	jmp	.L188
	.p2align 4,,10
	.p2align 3
.L190:
	mov	DWORD PTR [r8], ebx
	lea	r8, -1[r9]
	mov	rcx, r8
	shr	rcx, 63
	add	rcx, r8
	sar	rcx
	test	r9, r9
	mov	r8, rcx
	mov	rcx, r9
	je	.L189
	mov	r9, r8
.L153:
	lea	rsi, [rax+r9*4]
	mov	ebx, DWORD PTR [rsi]
	lea	r8, [rax+rcx*4]
	cmp	r10d, ebx
	jg	.L190
.L148:
	cmp	r11, 4
	mov	DWORD PTR [r8], r10d
	jg	.L154
.L115:
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
.L120:
	lea	rbx, 1[rdx+rdx]
	lea	r10, [rax+rbx*4]
	mov	r15d, DWORD PTR [r10]
	mov	DWORD PTR [r9], r15d
	mov	r9, r10
	mov	r10, rdx
	mov	rdx, rbx
	jmp	.L122
	.p2align 4,,10
	.p2align 3
.L189:
	mov	r8, rsi
	cmp	r11, 4
	mov	DWORD PTR [r8], r10d
	jg	.L154
	jmp	.L115
	.p2align 4,,10
	.p2align 3
.L149:
	lea	r9, -2[r13]
	sar	r9
	cmp	r9, rcx
	je	.L152
	lea	rbx, -1[rcx]
	mov	r9, rbx
	shr	r9, 63
	add	r9, rbx
	sar	r9
	test	rcx, rcx
	jne	.L153
	jmp	.L148
	.p2align 4,,10
	.p2align 3
.L143:
	test	r14, r14
	mov	r8, rax
	jne	.L148
	cmp	rcx, 2
	ja	.L148
	xor	ecx, ecx
	.p2align 4,,10
	.p2align 3
.L152:
	lea	rbx, 1[rcx+rcx]
	mov	r9d, DWORD PTR [rax+rbx*4]
	mov	DWORD PTR [r8], r9d
	mov	r9, rcx
	mov	rcx, rbx
	jmp	.L153
	.p2align 4,,10
	.p2align 3
.L186:
	mov	r10, rbx
	mov	DWORD PTR [r10], esi
	jmp	.L191
.L116:
	cmp	rdx, r8
	jnb	.L115
	mov	r14, r9
	sar	r14, 2
	mov	r13, r14
	and	r13d, 1
	jmp	.L127
.L131:
	test	r13, r13
	mov	r10, rax
	jne	.L136
	test	rbp, rbp
	jne	.L136
	xor	r8d, r8d
.L139:
	lea	rbx, 1[r8+r8]
	lea	r11, [rax+rbx*4]
	mov	r14d, DWORD PTR [r11]
	mov	DWORD PTR [r10], r14d
	mov	r10, r11
	mov	r11, r8
	mov	r8, rbx
	jmp	.L138
.L188:
	mov	DWORD PTR [r8], r10d
	jmp	.L154
	.seh_endproc
	.section	.text$_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	.def	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_:
.LFB6430:
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
	jle	.L193
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
	jge	.L218
	.p2align 4,,10
	.p2align 3
.L242:
	mov	r10, r11
	mov	QWORD PTR [rsp], rsi
	mov	QWORD PTR 8[rsp], r14
	jmp	.L196
	.p2align 4,,10
	.p2align 3
.L219:
	mov	r10, rdx
.L196:
	lea	rcx, 1[r10]
	lea	rdx, [rcx+rcx]
	lea	rsi, -1[rdx]
	lea	r14, [rax+rsi*4]
	lea	rcx, [rax+rcx*8]
	mov	r15d, DWORD PTR [r14]
	mov	r9d, DWORD PTR [rcx]
	cmp	r15d, r9d
	jle	.L195
	mov	r9d, r15d
	mov	rcx, r14
	mov	rdx, rsi
.L195:
	cmp	rdx, rdi
	mov	DWORD PTR [rax+r10*4], r9d
	jl	.L219
	mov	rsi, QWORD PTR [rsp]
	mov	r14, QWORD PTR 8[rsp]
.L194:
	cmp	rbp, rdx
	jne	.L224
	test	r12b, r12b
	jne	.L197
.L224:
	lea	r10, -1[rdx]
	mov	r9, r10
	shr	r9, 63
	add	r9, r10
	sar	r9
.L199:
	cmp	r11, rdx
	jge	.L200
	mov	rcx, rdx
	jmp	.L201
	.p2align 4,,10
	.p2align 3
.L241:
	mov	DWORD PTR [rcx], r15d
	lea	rcx, -1[r9]
	mov	rdx, rcx
	shr	rdx, 63
	add	rdx, rcx
	mov	rcx, r9
	sar	rdx
	cmp	r11, r9
	jge	.L240
	mov	r9, rdx
.L201:
	lea	r10, [rax+r9*4]
	mov	r15d, DWORD PTR [r10]
	lea	rcx, [rax+rcx*4]
	cmp	ebx, r15d
	jg	.L241
.L200:
	sub	rsi, 4
	test	r11, r11
	mov	DWORD PTR [rcx], ebx
	je	.L238
.L243:
	sub	r11, 1
	mov	ebx, DWORD PTR [rsi]
	mov	rcx, rsi
	cmp	r11, rdi
	jl	.L242
.L218:
	mov	rdx, r11
	jmp	.L194
	.p2align 4,,10
	.p2align 3
.L240:
	mov	rcx, r10
	sub	rsi, 4
	test	r11, r11
	mov	DWORD PTR [rcx], ebx
	jne	.L243
.L238:
	mov	rdx, r14
	mov	rcx, r13
.L193:
	cmp	rcx, r8
	jnb	.L192
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
	jmp	.L216
	.p2align 4,,10
	.p2align 3
.L204:
	add	rbp, 4
	cmp	rbp, r8
	jnb	.L192
.L216:
	mov	r11d, DWORD PTR 0[rbp]
	mov	ecx, DWORD PTR [rax]
	cmp	r11d, ecx
	jge	.L204
	cmp	rdx, 8
	mov	DWORD PTR 0[rbp], ecx
	jle	.L205
	xor	r12d, r12d
	jmp	.L207
	.p2align 4,,10
	.p2align 3
.L221:
	mov	r12, rcx
.L207:
	lea	r9, 1[r12]
	lea	rcx, [r9+r9]
	lea	r13, -1[rcx]
	lea	r14, [rax+r13*4]
	lea	r9, [rax+r9*8]
	mov	r15d, DWORD PTR [r14]
	mov	r10d, DWORD PTR [r9]
	cmp	r15d, r10d
	jle	.L206
	mov	r10d, r15d
	mov	r9, r14
	mov	rcx, r13
.L206:
	cmp	rbx, rcx
	mov	DWORD PTR [rax+r12*4], r10d
	jg	.L221
	test	rdi, rdi
	jne	.L239
	cmp	rsi, rcx
	je	.L213
.L239:
	lea	r12, -1[rcx]
	mov	r10, r12
	shr	r10, 63
	add	r10, r12
	sar	r10
	test	rcx, rcx
	jne	.L215
	jmp	.L210
	.p2align 4,,10
	.p2align 3
.L245:
	mov	DWORD PTR [r9], r13d
	lea	r9, -1[r10]
	mov	rcx, r9
	shr	rcx, 63
	add	rcx, r9
	sar	rcx
	test	r10, r10
	mov	r9, rcx
	mov	rcx, r10
	je	.L244
	mov	r10, r9
.L215:
	lea	r12, [rax+r10*4]
	mov	r13d, DWORD PTR [r12]
	lea	r9, [rax+rcx*4]
	cmp	r11d, r13d
	jg	.L245
.L210:
	mov	DWORD PTR [r9], r11d
.L246:
	add	rbp, 4
	cmp	rbp, r8
	jb	.L216
.L192:
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
.L244:
	mov	r9, r12
	mov	DWORD PTR [r9], r11d
	jmp	.L246
	.p2align 4,,10
	.p2align 3
.L197:
	lea	r10, 1[rdx+rdx]
	lea	r9, [rax+r10*4]
	mov	r15d, DWORD PTR [r9]
	mov	DWORD PTR [rcx], r15d
	mov	rcx, r9
	mov	r9, rdx
	mov	rdx, r10
	jmp	.L199
.L205:
	test	rdi, rdi
	mov	r9, rax
	jne	.L210
	test	rsi, rsi
	jne	.L210
	xor	ecx, ecx
	.p2align 4,,10
	.p2align 3
.L213:
	lea	r12, 1[rcx+rcx]
	mov	r10d, DWORD PTR [rax+r12*4]
	mov	DWORD PTR [r9], r10d
	mov	r10, rcx
	mov	rcx, r12
	jmp	.L215
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	.def	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv:
.LFB6525:
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
.L248:
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
	jne	.L248
	movdqa	xmm7, XMMWORD PTR .LC0[rip]
	lea	rax, 2492[r10]
	pxor	xmm3, xmm3
	movdqa	xmm6, XMMWORD PTR .LC1[rip]
	movdqa	xmm5, XMMWORD PTR .LC2[rip]
	movdqa	xmm4, XMMWORD PTR .LC3[rip]
	.p2align 4,,10
	.p2align 3
.L249:
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
	jne	.L249
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
.LFB6421:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 2496[rcx]
	cmp	rax, 623
	mov	r11, rcx
	ja	.L254
.L253:
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
.L254:
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EE11_M_gen_randEv
	mov	rax, QWORD PTR 2496[r11]
	jmp	.L253
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC4:
	.ascii "SORT FAIL\0"
.LC5:
	.ascii "PARTIAL FAIL\0"
.LC6:
	.ascii "PARTIAL BOUND FAIL\0"
.LC7:
	.ascii "NTH LEFT FAIL\0"
.LC8:
	.ascii "NTH RIGHT FAIL\0"
.LC9:
	.ascii "sort ok: is_sorted=\0"
.LC10:
	.ascii "partial top10[0]=\0"
.LC11:
	.ascii " (should be global min)\0"
.LC12:
	.ascii "nth median c[500]=\0"
.LC13:
	.ascii "functional checks passed\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5635:
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
	sub	rsp, 2728
	.seh_stackalloc	2728
	.seh_endprologue
	call	__main
	mov	ecx, 4000
.LEHB0:
	call	_Znwy
.LEHE0:
	xor	edx, edx
	mov	r8d, 3996
	lea	rbx, 4000[rax]
	mov	DWORD PTR [rax], 0
	mov	rsi, rax
	lea	rcx, 4[rax]
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 96[rsp], rbx
	lea	rdi, 208[rsp]
	call	memset
	mov	eax, 42
	mov	QWORD PTR 88[rsp], rbx
	mov	ecx, 1
	mov	DWORD PTR 208[rsp], 42
	mov	edx, eax
	.p2align 4,,10
	.p2align 3
.L256:
	mov	eax, edx
	shr	eax, 30
	xor	eax, edx
	imul	eax, eax, 1812433253
	lea	edx, [rax+rcx]
	mov	DWORD PTR [rdi+rcx*4], edx
	add	rcx, 1
	cmp	rcx, 624
	jne	.L256
	mov	QWORD PTR 2704[rsp], 624
	.p2align 4,,10
	.p2align 3
.L259:
	mov	rcx, rdi
	call	_ZNSt23mersenne_twister_engineIjLy32ELy624ELy397ELy31ELj2567483615ELy11ELj4294967295ELy7ELj2636928640ELy15ELj4022730752ELy18ELj1812433253EEclEv
	mov	eax, eax
	imul	rax, rax, 1000001
	cmp	eax, 963001
	jbe	.L259
	shr	rax, 32
	add	rsi, 4
	mov	DWORD PTR -4[rsi], eax
	cmp	rsi, rbx
	jne	.L259
	lea	rax, 112[rsp]
	lea	rbp, 80[rsp]
	mov	rcx, rax
	mov	QWORD PTR 32[rsp], rax
	mov	rdx, rbp
.LEHB1:
	call	_ZNSt6vectorIiSaIiEEC1ERKS1_
.LEHE1:
	mov	rbx, QWORD PTR 120[rsp]
	mov	rsi, QWORD PTR 112[rsp]
	cmp	rbx, rsi
	je	.L260
	mov	rdi, rbx
	mov	r8d, 63
	mov	rcx, rsi
	sub	rdi, rsi
	mov	rax, rdi
	sar	rax, 2
	bsr	rdx, rax
	xor	rdx, 63
	test	rax, rax
	mov	eax, 64
	cmovne	eax, edx
	mov	rdx, rbx
	sub	r8d, eax
	movsx	r8, r8d
	add	r8, r8
	call	_ZSt16__introsort_loopIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEExNS0_5__ops15_Iter_less_iterEEvT_S9_T0_T1_.isra.0
	cmp	rdi, 64
	jle	.L262
	lea	rdi, 64[rsi]
	mov	rcx, rsi
	mov	rdx, rdi
	call	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	cmp	rbx, rdi
	mov	r9, rdi
	je	.L260
	.p2align 4,,10
	.p2align 3
.L267:
	mov	ecx, DWORD PTR [r9]
	lea	rax, -4[r9]
	mov	r8, r9
	mov	edx, DWORD PTR -4[r9]
	cmp	edx, ecx
	jle	.L265
	.p2align 4,,10
	.p2align 3
.L266:
	mov	DWORD PTR 4[rax], edx
	mov	r8, rax
	mov	edx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	ecx, edx
	jl	.L266
.L265:
	add	r9, 4
	mov	DWORD PTR [r8], ecx
	cmp	r9, rbx
	jne	.L267
.L260:
	mov	rdx, rbx
	mov	rcx, rsi
	call	_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_
	test	al, al
	je	.L351
	lea	rax, 144[rsp]
	mov	rdx, rbp
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
.LEHB2:
	call	_ZNSt6vectorIiSaIiEEC1ERKS1_
.LEHE2:
	mov	rdi, QWORD PTR 144[rsp]
	xor	r9d, r9d
	mov	r13, QWORD PTR 152[rsp]
	lea	r12, 40[rdi]
	mov	rcx, rdi
	mov	r8, r13
	mov	rdx, r12
	call	_ZSt14__partial_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	mov	rdx, r12
	mov	rcx, rdi
	call	_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_
	test	al, al
	je	.L271
	sub	r13, rdi
	sar	r13, 2
	cmp	r13d, 10
	jle	.L273
	lea	ecx, -11[r13]
	mov	edx, DWORD PTR 36[rdi]
	mov	rax, r12
	lea	rcx, 44[rdi+rcx*4]
	jmp	.L277
	.p2align 4,,10
	.p2align 3
.L275:
	add	rax, 4
	cmp	rax, rcx
	je	.L273
.L277:
	cmp	DWORD PTR [rax], edx
	jge	.L275
	mov	rcx, QWORD PTR .refptr._ZSt4cerr[rip]
	lea	rdx, .LC6[rip]
.LEHB3:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.L346:
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE3:
	mov	ebx, 1
.L274:
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
.L270:
	mov	rcx, QWORD PTR 32[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rbp
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	eax, ebx
	add	rsp, 2728
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L262:
	mov	rdx, rbx
	mov	rcx, rsi
	call	_ZSt16__insertion_sortIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_T0_.isra.0
	jmp	.L260
.L351:
	mov	rcx, QWORD PTR .refptr._ZSt4cerr[rip]
	lea	rdx, .LC4[rip]
.LEHB4:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE4:
	mov	ebx, 1
	jmp	.L270
.L273:
	lea	rax, 176[rsp]
	mov	rdx, rbp
	mov	rcx, rax
	mov	QWORD PTR 48[rsp], rax
.LEHB5:
	call	_ZNSt6vectorIiSaIiEEC1ERKS1_
.LEHE5:
	mov	r12, QWORD PTR 176[rsp]
	mov	r10, QWORD PTR 184[rsp]
	lea	r13, 2000[r12]
	cmp	r13, r10
	je	.L278
	cmp	r12, r10
	je	.L278
	mov	rax, r10
	sub	rax, r12
	mov	rdx, rax
	sar	rdx, 2
	test	rdx, rdx
	je	.L279
	bsr	r8, rdx
	movsx	r8, r8d
	add	r8, r8
	cmp	rax, 12
	jle	.L348
.L280:
	mov	r15, r10
	mov	r14, r12
	mov	QWORD PTR 56[rsp], rbx
	.p2align 4,,10
	.p2align 3
.L282:
	sar	rax, 3
	movq	xmm0, QWORD PTR [r14]
	sub	r8, 1
	lea	rbx, [r14+rax*4]
	mov	r11d, DWORD PTR -4[r15]
	mov	ecx, DWORD PTR [rbx]
	pshufd	xmm2, xmm0, 0xe5
	movd	r9d, xmm2
	movd	edx, xmm0
	lea	rax, 4[r14]
	pshufd	xmm1, xmm0, 225
	cmp	ecx, r9d
	jle	.L284
	cmp	r11d, ecx
	jg	.L290
	cmp	r11d, r9d
	jle	.L287
.L347:
	mov	DWORD PTR [r14], r11d
	mov	DWORD PTR -4[r15], edx
.L286:
	mov	rcx, r15
	.p2align 4,,10
	.p2align 3
.L288:
	mov	ebx, DWORD PTR [rax]
	mov	r11d, DWORD PTR [r14]
	cmp	r11d, ebx
	jle	.L291
	lea	r9, 4[rax]
	.p2align 4,,10
	.p2align 3
.L292:
	mov	rax, r9
	mov	ebx, DWORD PTR [r9]
	add	r9, 4
	cmp	ebx, r11d
	jl	.L292
.L291:
	mov	r9d, DWORD PTR -4[rcx]
	cmp	r11d, r9d
	jge	.L293
	lea	rdx, -8[rcx]
	.p2align 4,,10
	.p2align 3
.L294:
	mov	rcx, rdx
	mov	r9d, DWORD PTR [rdx]
	sub	rdx, 4
	cmp	r9d, r11d
	jg	.L294
.L295:
	cmp	rax, rcx
	jnb	.L352
	mov	DWORD PTR [rax], r9d
	add	rax, 4
	mov	DWORD PTR [rcx], ebx
	jmp	.L288
	.p2align 4,,10
	.p2align 3
.L352:
	cmp	r13, rax
	cmovb	r15, rax
	cmovnb	r14, rax
	mov	rax, r15
	sub	rax, r14
	cmp	rax, 12
	jle	.L353
	test	r8, r8
	jne	.L282
	xor	r9d, r9d
	mov	r8, r15
	mov	rcx, r14
	mov	rbx, QWORD PTR 56[rsp]
	lea	rdx, 2004[r12]
	mov	QWORD PTR 56[rsp], r10
	call	_ZSt13__heap_selectIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEENS0_5__ops15_Iter_less_iterEEvT_S9_S9_T0_
	mov	eax, DWORD PTR [r14]
	mov	edx, DWORD PTR 2000[r12]
	mov	r10, QWORD PTR 56[rsp]
	mov	DWORD PTR [r14], edx
	mov	DWORD PTR 2000[r12], eax
.L278:
	mov	edx, DWORD PTR 2000[r12]
	mov	rax, r12
	jmp	.L310
	.p2align 4,,10
	.p2align 3
.L308:
	add	rax, 4
	cmp	rax, r13
	je	.L354
.L310:
	cmp	DWORD PTR [rax], edx
	jle	.L308
	mov	rcx, QWORD PTR .refptr._ZSt4cerr[rip]
	lea	rdx, .LC7[rip]
.LEHB6:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.L350:
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE6:
	mov	ebx, 1
.L313:
	mov	rcx, QWORD PTR 48[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	jmp	.L274
.L271:
	mov	rcx, QWORD PTR .refptr._ZSt4cerr[rip]
	lea	rdx, .LC5[rip]
.LEHB7:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE7:
	jmp	.L346
	.p2align 4,,10
	.p2align 3
.L293:
	sub	rcx, 4
	jmp	.L295
.L284:
	cmp	r11d, r9d
	jg	.L287
	cmp	r11d, ecx
	jg	.L347
.L290:
	mov	DWORD PTR [r14], ecx
	mov	DWORD PTR [rbx], edx
	jmp	.L286
.L287:
	movq	QWORD PTR [r14], xmm1
	jmp	.L286
.L353:
	cmp	r15, r14
	mov	rbx, QWORD PTR 56[rsp]
	je	.L278
.L281:
	lea	r9, 4[r14]
	mov	QWORD PTR 56[rsp], rbx
	mov	rbx, r15
	mov	QWORD PTR 64[rsp], rsi
	mov	r15, r9
	mov	rsi, r14
	mov	r14, rbp
	mov	QWORD PTR 72[rsp], rdi
	mov	rbp, r10
.L299:
	cmp	rbx, r15
	mov	r8, r15
	je	.L355
	mov	edi, DWORD PTR [r15]
	mov	eax, DWORD PTR [rsi]
	cmp	edi, eax
	jge	.L300
	mov	r8, r15
	sub	r8, rsi
	cmp	r8, 4
	jle	.L301
	mov	ecx, 4
	mov	rdx, rsi
	sub	rcx, r8
	add	rcx, r15
	call	memmove
.L302:
	mov	DWORD PTR [rsi], edi
.L303:
	add	r15, 4
	jmp	.L299
.L300:
	mov	ecx, DWORD PTR -4[r15]
	lea	rax, -4[r15]
	cmp	ecx, edi
	jle	.L304
	.p2align 4,,10
	.p2align 3
.L305:
	mov	DWORD PTR 4[rax], ecx
	mov	r8, rax
	mov	ecx, DWORD PTR -4[rax]
	sub	rax, 4
	cmp	edi, ecx
	jl	.L305
.L304:
	mov	DWORD PTR [r8], edi
	jmp	.L303
.L355:
	mov	r10, rbp
	mov	rbx, QWORD PTR 56[rsp]
	mov	rbp, r14
	mov	rsi, QWORD PTR 64[rsp]
	mov	rdi, QWORD PTR 72[rsp]
	jmp	.L278
.L279:
	cmp	rax, 12
	mov	r8, -2
	jg	.L280
.L348:
	mov	r15, r10
	mov	r14, r12
	jmp	.L281
.L354:
	mov	rcx, r10
	mov	eax, 501
	sub	rcx, r12
	sar	rcx, 2
	jmp	.L311
.L312:
	add	rax, 1
	cmp	edx, DWORD PTR -4[r12+rax*4]
	jg	.L356
.L311:
	cmp	ecx, eax
	jg	.L312
	mov	r13, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC9[rip]
	mov	rcx, r13
.LEHB8:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	r14, rax
	mov	rax, QWORD PTR [rax]
	mov	rdx, rbx
	mov	rcx, QWORD PTR -24[rax]
	add	rcx, r14
	or	DWORD PTR 24[rcx], 1
	mov	rcx, rsi
	call	_ZSt9is_sortedIN9__gnu_cxx17__normal_iteratorIPiSt6vectorIiSaIiEEEEEbT_S7_
	mov	rcx, r14
	movzx	edx, al
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC10[rip]
	mov	rcx, r13
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR [rdi]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC11[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC12[rip]
	mov	rcx, r13
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR 2000[r12]
	mov	rcx, rax
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC13[rip]
	mov	rcx, r13
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	xor	ebx, ebx
	jmp	.L313
.L301:
	jne	.L302
	mov	DWORD PTR [r15], eax
	jmp	.L302
.L356:
	mov	rcx, QWORD PTR .refptr._ZSt4cerr[rip]
	lea	rdx, .LC8[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE8:
	jmp	.L350
.L325:
	mov	rbx, rax
.L315:
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
.L316:
	mov	rcx, QWORD PTR 32[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
.L317:
	mov	rcx, rbp
	call	_ZNSt6vectorIiSaIiEED1Ev
	mov	rcx, rbx
.LEHB9:
	call	_Unwind_Resume
.LEHE9:
.L323:
	mov	rbx, rax
	jmp	.L317
.L324:
	mov	rbx, rax
	jmp	.L316
.L326:
	mov	rcx, QWORD PTR 48[rsp]
	mov	rbx, rax
	call	_ZNSt6vectorIiSaIiEED1Ev
	jmp	.L315
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5635:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5635-.LLSDACSB5635
.LLSDACSB5635:
	.uleb128 .LEHB0-.LFB5635
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5635
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L323-.LFB5635
	.uleb128 0
	.uleb128 .LEHB2-.LFB5635
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L324-.LFB5635
	.uleb128 0
	.uleb128 .LEHB3-.LFB5635
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L325-.LFB5635
	.uleb128 0
	.uleb128 .LEHB4-.LFB5635
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L324-.LFB5635
	.uleb128 0
	.uleb128 .LEHB5-.LFB5635
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L325-.LFB5635
	.uleb128 0
	.uleb128 .LEHB6-.LFB5635
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L326-.LFB5635
	.uleb128 0
	.uleb128 .LEHB7-.LFB5635
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L325-.LFB5635
	.uleb128 0
	.uleb128 .LEHB8-.LFB5635
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L326-.LFB5635
	.uleb128 0
	.uleb128 .LEHB9-.LFB5635
	.uleb128 .LEHE9-.LEHB9
	.uleb128 0
	.uleb128 0
.LLSDACSE5635:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	-2147483648
	.long	-2147483648
	.long	-2147483648
	.long	-2147483648
	.align 16
.LC1:
	.long	2147483647
	.long	2147483647
	.long	2147483647
	.long	2147483647
	.align 16
.LC2:
	.long	1
	.long	1
	.long	1
	.long	1
	.align 16
.LC3:
	.long	-1727483681
	.long	-1727483681
	.long	-1727483681
	.long	-1727483681
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
	.section	.rdata$.refptr._ZSt4cerr, "dr"
	.globl	.refptr._ZSt4cerr
	.linkonce	discard
.refptr._ZSt4cerr:
	.quad	_ZSt4cerr
