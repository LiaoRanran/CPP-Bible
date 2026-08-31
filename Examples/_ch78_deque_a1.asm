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
.LFB2852:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB3970:
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
.LFB3963:
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
	.section	.text$_ZNSt5dequeIiSaIiEE4backEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt5dequeIiSaIiEE4backEv
	.def	_ZNSt5dequeIiSaIiEE4backEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE4backEv
_ZNSt5dequeIiSaIiEE4backEv:
.LFB3463:
	.seh_endprologue
	mov	rax, QWORD PTR 48[rcx]
	cmp	rax, QWORD PTR 56[rcx]
	mov	rdx, QWORD PTR 72[rcx]
	je	.L15
	sub	rax, 4
	ret
	.p2align 4,,10
	.p2align 3
.L15:
	mov	rax, QWORD PTR -8[rdx]
	add	rax, 512
	sub	rax, 4
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
.LFB3474:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L16
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L16:
	ret
	.seh_endproc
	.section	.text$_ZStmiRKSt15_Deque_iteratorIiRiPiES4_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZStmiRKSt15_Deque_iteratorIiRiPiES4_
	.def	_ZStmiRKSt15_Deque_iteratorIiRiPiES4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZStmiRKSt15_Deque_iteratorIiRiPiES4_
_ZStmiRKSt15_Deque_iteratorIiRiPiES4_:
.LFB3623:
	.seh_endprologue
	mov	r8, rdx
	mov	rdx, QWORD PTR 24[rcx]
	mov	rax, rdx
	sub	rax, QWORD PTR 24[r8]
	sar	rax, 3
	cmp	rdx, 1
	mov	rdx, QWORD PTR [rcx]
	adc	rax, -1
	sub	rdx, QWORD PTR 8[rcx]
	sal	rax, 7
	sar	rdx, 2
	add	rax, rdx
	mov	rdx, QWORD PTR 16[r8]
	sub	rdx, QWORD PTR [r8]
	sar	rdx, 2
	add	rax, rdx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.section	.text$_ZNSt6vectorIiSaIiEE17_M_realloc_insertIJiEEEvN9__gnu_cxx17__normal_iteratorIPiS1_EEDpOT_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIiSaIiEE17_M_realloc_insertIJiEEEvN9__gnu_cxx17__normal_iteratorIPiS1_EEDpOT_
	.def	_ZNSt6vectorIiSaIiEE17_M_realloc_insertIJiEEEvN9__gnu_cxx17__normal_iteratorIPiS1_EEDpOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIiSaIiEE17_M_realloc_insertIJiEEEvN9__gnu_cxx17__normal_iteratorIPiS1_EEDpOT_
_ZNSt6vectorIiSaIiEE17_M_realloc_insertIJiEEEvN9__gnu_cxx17__normal_iteratorIPiS1_EEDpOT_:
.LFB3762:
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
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, QWORD PTR [rcx]
	mov	rax, rdi
	mov	r12, rdx
	mov	rsi, rcx
	movabs	rdx, 2305843009213693951
	sub	rax, rbp
	mov	r14, r8
	sar	rax, 2
	cmp	rax, rdx
	je	.L40
	mov	r13, r12
	sub	r13, rbp
	cmp	rbp, rdi
	je	.L41
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L34
	test	rdx, rdx
	jne	.L42
	xor	ebx, ebx
	xor	ecx, ecx
.L25:
	mov	eax, DWORD PTR [r14]
	lea	r14, 4[rcx+r13]
	sub	rdi, r12
	movq	xmm6, rcx
	test	r13, r13
	mov	DWORD PTR [rcx+r13], eax
	lea	rax, [r14+rdi]
	movq	xmm0, rax
	punpcklqdq	xmm6, xmm0
	jg	.L43
	test	rdi, rdi
	jle	.L29
	mov	r8, rdi
	mov	rdx, r12
	mov	rcx, r14
	call	memcpy
.L29:
	test	rbp, rbp
	jne	.L28
.L31:
	movups	XMMWORD PTR [rsi], xmm6
	mov	QWORD PTR 16[rsi], rbx
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 48
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
.L34:
	movabs	rbx, 9223372036854775804
.L24:
	mov	rcx, rbx
	call	_Znwy
	mov	rcx, rax
	add	rbx, rax
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L43:
	mov	r8, r13
	mov	rdx, rbp
	call	memmove
	test	rdi, rdi
	jg	.L44
.L28:
	mov	rdx, QWORD PTR 16[rsi]
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
	jmp	.L31
	.p2align 4,,10
	.p2align 3
.L41:
	add	rax, 1
	jc	.L34
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	mov	rbx, rdx
	cmovbe	rbx, rax
	sal	rbx, 2
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L44:
	mov	rdx, r12
	mov	rcx, r14
	mov	r8, rdi
	call	memcpy
	mov	rdx, QWORD PTR 16[rsi]
	mov	rcx, rbp
	sub	rdx, rbp
	call	_ZdlPvy
	jmp	.L31
.L42:
	movabs	rax, 2305843009213693951
	cmp	rdx, rax
	cmova	rdx, rax
	lea	rbx, 0[0+rdx*4]
	jmp	.L24
.L40:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
	.def	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb:
.LFB3849:
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
	mov	rax, QWORD PTR 72[rcx]
	mov	rbp, rdx
	mov	rdx, QWORD PTR 40[rcx]
	mov	rdi, rax
	mov	rsi, rcx
	mov	rbx, QWORD PTR 8[rsi]
	mov	r14d, r8d
	sub	rdi, rdx
	mov	rcx, rdi
	sar	rcx, 3
	lea	r15, 1[rbp+rcx]
	lea	rcx, [r15+r15]
	cmp	rcx, rbx
	jnb	.L46
	sub	rbx, r15
	shr	rbx
	sal	rbx, 3
	test	r8b, r8b
	lea	rcx, [rbx+rbp*8]
	cmovne	rbx, rcx
	add	rbx, QWORD PTR [rsi]
	lea	r8, 8[rax]
	sub	r8, rdx
	cmp	rbx, rdx
	jnb	.L48
	cmp	r8, 8
	jle	.L49
	mov	rcx, rbx
	call	memmove
	mov	rax, QWORD PTR [rbx]
	jmp	.L50
	.p2align 4,,10
	.p2align 3
.L46:
	cmp	rbx, rbp
	mov	rax, rbp
	cmovnb	rax, rbx
	lea	r12, 2[rbx+rax]
	movabs	rax, 1152921504606846975
	cmp	rax, r12
	jb	.L60
	lea	rcx, 0[0+r12*8]
	mov	rbx, r12
	call	_Znwy
	sub	rbx, r15
	mov	rdx, QWORD PTR 40[rsi]
	shr	rbx
	mov	r13, rax
	sal	rbx, 3
	test	r14b, r14b
	lea	rax, [rbx+rbp*8]
	cmovne	rbx, rax
	mov	rax, QWORD PTR 72[rsi]
	add	rbx, r13
	lea	r8, 8[rax]
	sub	r8, rdx
	cmp	r8, 8
	jle	.L57
	mov	rcx, rbx
	call	memmove
.L58:
	mov	rax, QWORD PTR 8[rsi]
	mov	rcx, QWORD PTR [rsi]
	lea	rdx, 0[0+rax*8]
	call	_ZdlPvy
	mov	QWORD PTR [rsi], r13
	mov	QWORD PTR 8[rsi], r12
.L59:
	mov	rax, QWORD PTR [rbx]
.L50:
	lea	rdx, 512[rax]
	mov	QWORD PTR 40[rsi], rbx
	movq	xmm0, rax
	add	rbx, rdi
	movq	xmm1, rdx
	mov	QWORD PTR 72[rsi], rbx
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR 24[rsi], xmm0
	mov	rax, QWORD PTR [rbx]
	lea	rdx, 512[rax]
	movq	xmm0, rax
	movq	xmm2, rdx
	punpcklqdq	xmm0, xmm2
	movups	XMMWORD PTR 56[rsi], xmm0
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
	.p2align 4,,10
	.p2align 3
.L48:
	lea	rcx, 8[rbx+rdi]
	cmp	r8, 8
	jle	.L52
	sub	rcx, r8
	call	memmove
	mov	rax, QWORD PTR [rbx]
	jmp	.L50
	.p2align 4,,10
	.p2align 3
.L60:
	movabs	rax, 2305843009213693951
	cmp	rax, r12
	jnb	.L55
	call	_ZSt28__throw_bad_array_new_lengthv
	.p2align 4,,10
	.p2align 3
.L55:
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L57:
	jne	.L58
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rbx], rax
	jmp	.L58
	.p2align 4,,10
	.p2align 3
.L52:
	jne	.L59
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR -8[rcx], rax
	mov	rax, QWORD PTR [rbx]
	jmp	.L50
	.p2align 4,,10
	.p2align 3
.L49:
	jne	.L59
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rbx], rax
	jmp	.L50
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "cannot create std::deque larger than max_size()\0"
.LC2:
	.ascii "deque front : \0"
.LC3:
	.ascii "deque back  : \0"
.LC4:
	.ascii "deque size  : \0"
	.align 8
.LC5:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmpubfamd0t\\s.cpp\0"
.LC6:
	.ascii "d.front() == -1\0"
.LC7:
	.ascii "d.back() == 4\0"
.LC8:
	.ascii "d.size() == 6\0"
.LC9:
	.ascii "vector front: \0"
.LC10:
	.ascii "vector back : \0"
.LC11:
	.ascii "vector size : \0"
.LC12:
	.ascii "v.front() == -1\0"
.LC13:
	.ascii "v.back() == 4\0"
.LC14:
	.ascii "v.size() == d.size()\0"
.LC15:
	.ascii "sequence equal: \0"
.LC16:
	.ascii "same\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3114:
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
	sub	rsp, 216
	.seh_stackalloc	216
	movaps	XMMWORD PTR 192[rsp], xmm6
	.seh_savexmm	xmm6, 192
	.seh_endprologue
	call	__main
	mov	ecx, 64
	pxor	xmm0, xmm0
	mov	QWORD PTR 120[rsp], 8
	movaps	XMMWORD PTR 128[rsp], xmm0
	movaps	XMMWORD PTR 144[rsp], xmm0
	movaps	XMMWORD PTR 160[rsp], xmm0
	movaps	XMMWORD PTR 176[rsp], xmm0
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	ecx, 512
	mov	QWORD PTR 112[rsp], rax
	lea	rsi, 24[rax]
	mov	rbx, rax
.LEHB1:
	call	_Znwy
.LEHE1:
	lea	rdx, 512[rax]
	movq	xmm3, rsi
	mov	QWORD PTR 24[rbx], rax
	mov	r8, rax
	movq	xmm2, rax
	movq	xmm0, rdx
	xor	esi, esi
	movddup	xmm1, xmm2
	punpcklqdq	xmm0, xmm3
	movaps	XMMWORD PTR 128[rsp], xmm1
	movaps	XMMWORD PTR 144[rsp], xmm0
	movaps	XMMWORD PTR 160[rsp], xmm1
	movaps	XMMWORD PTR 176[rsp], xmm0
	jmp	.L62
	.p2align 4,,10
	.p2align 3
.L127:
	mov	DWORD PTR [rax], esi
	add	rax, 4
	mov	QWORD PTR 160[rsp], rax
.L67:
	add	esi, 1
	cmp	esi, 5
	je	.L126
	mov	rax, QWORD PTR 160[rsp]
	mov	rdx, QWORD PTR 176[rsp]
.L62:
	sub	rdx, 4
	cmp	rax, rdx
	jne	.L127
	mov	rcx, QWORD PTR 184[rsp]
	mov	rdx, rcx
	sub	rdx, QWORD PTR 152[rsp]
	sar	rdx, 3
	cmp	rcx, 1
	adc	rdx, -1
	sub	rax, QWORD PTR 168[rsp]
	sal	rdx, 7
	sar	rax, 2
	add	rax, rdx
	mov	rdx, QWORD PTR 144[rsp]
	sub	rdx, r8
	sar	rdx, 2
	add	rax, rdx
	movabs	rdx, 4611686018427387903
	cmp	rax, rdx
	je	.L128
	mov	rax, QWORD PTR 120[rsp]
	sub	rcx, rbx
	sar	rcx, 3
	sub	rax, rcx
	cmp	rax, 1
	jbe	.L129
.L69:
	mov	ecx, 512
	mov	rbx, QWORD PTR 184[rsp]
.LEHB2:
	call	_Znwy
	mov	rdx, QWORD PTR 160[rsp]
	mov	QWORD PTR 8[rbx], rax
	movq	xmm4, rax
	add	rbx, 8
	add	rax, 512
	movq	xmm5, rbx
	movddup	xmm0, xmm4
	movaps	XMMWORD PTR 160[rsp], xmm0
	movq	xmm0, rax
	mov	r8, QWORD PTR 128[rsp]
	punpcklqdq	xmm0, xmm5
	mov	rbx, QWORD PTR 112[rsp]
	movaps	XMMWORD PTR 176[rsp], xmm0
	mov	DWORD PTR [rdx], esi
	jmp	.L67
.L129:
	lea	rcx, 112[rsp]
	xor	r8d, r8d
	mov	edx, 1
	call	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
	jmp	.L69
.L126:
	cmp	QWORD PTR 136[rsp], r8
	je	.L71
	mov	DWORD PTR -4[r8], -1
	sub	r8, 4
	mov	QWORD PTR 128[rsp], r8
.L72:
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC2[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rbp, QWORD PTR 128[rsp]
	mov	rcx, rax
	mov	edx, DWORD PTR 0[rbp]
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC3[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rbx, rax
	lea	rax, 112[rsp]
	mov	rcx, rax
	mov	QWORD PTR 32[rsp], rax
	call	_ZNSt5dequeIiSaIiEE4backEv
	mov	rcx, rbx
	mov	edx, DWORD PTR [rax]
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC4[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, 128[rsp]
	mov	rsi, rax
	lea	rax, 160[rsp]
	mov	QWORD PTR 48[rsp], rdx
	mov	rcx, rax
	mov	QWORD PTR 56[rsp], rax
	call	_ZStmiRKSt15_Deque_iteratorIiRiPiES4_
	mov	rcx, rsi
	mov	rdx, rax
	mov	rbx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE2:
	cmp	DWORD PTR 0[rbp], -1
	jne	.L130
	mov	rcx, QWORD PTR 32[rsp]
	call	_ZNSt5dequeIiSaIiEE4backEv
	cmp	DWORD PTR [rax], 4
	jne	.L131
	cmp	rbx, 6
	jne	.L132
	xor	eax, eax
	mov	rcx, rbx
	xor	edx, edx
	mov	DWORD PTR 76[rsp], -1
	lea	rdi, 80[rsp]
	rep stosd
	lea	rax, 80[rsp]
	lea	r8, 76[rsp]
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], rax
.LEHB3:
	call	_ZNSt6vectorIiSaIiEE17_M_realloc_insertIJiEEEvN9__gnu_cxx17__normal_iteratorIPiS1_EEDpOT_
	movabs	r15, 2305843009213693951
	xor	esi, esi
	jmp	.L87
	.p2align 4,,10
	.p2align 3
.L134:
	mov	DWORD PTR [rbx], esi
	add	rbx, 4
	mov	QWORD PTR 88[rsp], rbx
.L79:
	add	esi, 1
	cmp	esi, 5
	je	.L133
.L87:
	mov	rbx, QWORD PTR 88[rsp]
	mov	rdi, QWORD PTR 96[rsp]
	cmp	rbx, rdi
	jne	.L134
	mov	r12, QWORD PTR 80[rsp]
	sub	rbx, r12
	mov	rax, rbx
	sar	rax, 2
	cmp	rax, r15
	je	.L135
	cmp	rdi, r12
	je	.L81
	lea	rdx, [rax+rax]
	cmp	rdx, rax
	jb	.L107
	xor	r14d, r14d
	xor	r13d, r13d
	test	rdx, rdx
	jne	.L136
.L83:
	lea	rax, 4[r14+rbx]
	movq	xmm6, r14
	test	rbx, rbx
	mov	DWORD PTR [r14+rbx], esi
	movq	xmm4, rax
	punpcklqdq	xmm6, xmm4
	jg	.L137
	test	r12, r12
	jne	.L85
.L86:
	lea	r9, [r14+r13]
	movaps	XMMWORD PTR 80[rsp], xmm6
	mov	QWORD PTR 96[rsp], r9
	jmp	.L79
.L133:
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC9[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rsi, QWORD PTR 80[rsp]
	mov	rcx, rax
	mov	edx, DWORD PTR [rsi]
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC10[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdi, QWORD PTR 88[rsp]
	mov	rcx, rax
	mov	edx, DWORD PTR -4[rdi]
	call	_ZNSolsEi
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC11[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rbx, rdi
	mov	rcx, rax
	sub	rbx, rsi
	sar	rbx, 2
	mov	rdx, rbx
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	cmp	DWORD PTR [rsi], -1
	jne	.L138
	cmp	DWORD PTR -4[rdi], 4
	jne	.L139
	mov	rdx, QWORD PTR 48[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	call	_ZStmiRKSt15_Deque_iteratorIiRiPiES4_
	cmp	rbx, rax
	jne	.L90
	test	rbx, rbx
	je	.L98
	mov	rax, rbp
	sub	rax, QWORD PTR 136[rsp]
	mov	rcx, QWORD PTR 152[rsp]
	sar	rax, 2
	imul	rdx, rax, -4
	add	rbx, rax
	add	rsi, rdx
	jmp	.L97
	.p2align 4,,10
	.p2align 3
.L140:
	cmp	rax, 127
	mov	rdx, rbp
	jle	.L95
	mov	rdx, rax
	sar	rdx, 7
.L96:
	mov	r9, rdx
	mov	rdx, QWORD PTR [rcx+rdx*8]
	mov	r8, rax
	sal	r9, 7
	sub	r8, r9
	lea	rdx, [rdx+r8*4]
.L95:
	mov	edi, DWORD PTR [rsi+rax*4]
	cmp	DWORD PTR [rdx], edi
	jne	.L109
	add	rax, 1
	add	rbp, 4
	cmp	rbx, rax
	je	.L98
.L97:
	test	rax, rax
	jns	.L140
	mov	rdx, rax
	not	rdx
	shr	rdx, 7
	not	rdx
	jmp	.L96
.L137:
	mov	r8, rbx
	mov	rdx, r12
	mov	rcx, r14
	call	memmove
.L85:
	sub	rdi, r12
	mov	rcx, r12
	mov	rdx, rdi
	call	_ZdlPvy
	jmp	.L86
.L98:
	mov	ebx, 1
.L92:
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC15[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	movzx	edx, bl
	mov	rdi, QWORD PTR -24[rax]
	add	rdi, rcx
	or	DWORD PTR 24[rdi], 1
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	test	bl, bl
	mov	rsi, QWORD PTR 112[rsp]
	je	.L141
	mov	rcx, QWORD PTR 40[rsp]
	call	_ZNSt6vectorIiSaIiEED1Ev
	test	rsi, rsi
	je	.L118
	mov	rcx, QWORD PTR 32[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0
	nop
.L118:
	movaps	xmm6, XMMWORD PTR 192[rsp]
	xor	eax, eax
	add	rsp, 216
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
	xor	ebx, ebx
	jmp	.L92
.L81:
	movabs	r13, 2305843009213693951
	add	rax, 1
	jc	.L82
	cmp	rax, r13
	cmovbe	r13, rax
.L82:
	sal	r13, 2
	mov	rcx, r13
	call	_Znwy
.LEHE3:
	mov	r14, rax
	jmp	.L83
.L71:
	mov	rdx, QWORD PTR 184[rsp]
	mov	rcx, QWORD PTR 152[rsp]
	mov	rax, rdx
	sub	rax, rcx
	sar	rax, 3
	cmp	rdx, 1
	mov	rdx, QWORD PTR 160[rsp]
	adc	rax, -1
	sub	rdx, QWORD PTR 168[rsp]
	sal	rax, 7
	sar	rdx, 2
	add	rax, rdx
	mov	rdx, QWORD PTR 144[rsp]
	sub	rdx, r8
	sar	rdx, 2
	add	rax, rdx
	movabs	rdx, 4611686018427387903
	cmp	rax, rdx
	je	.L142
	cmp	rcx, rbx
	je	.L143
.L74:
	mov	ecx, 512
	mov	rbx, QWORD PTR 152[rsp]
.LEHB4:
	call	_Znwy
	lea	rdi, 508[rax]
	mov	QWORD PTR -8[rbx], rax
	movq	xmm5, rax
	sub	rbx, 8
	mov	DWORD PTR 508[rax], -1
	movq	xmm0, rdi
	lea	rdi, 512[rax]
	punpcklqdq	xmm0, xmm5
	movq	xmm5, rbx
	movaps	XMMWORD PTR 128[rsp], xmm0
	movq	xmm0, rdi
	punpcklqdq	xmm0, xmm5
	movaps	XMMWORD PTR 144[rsp], xmm0
	jmp	.L72
.L143:
	lea	rcx, 112[rsp]
	mov	r8d, 1
	mov	edx, 1
	call	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
	jmp	.L74
.L107:
	movabs	r13, 2305843009213693951
	jmp	.L82
.L128:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.L142:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.L131:
	lea	rdx, .LC5[rip]
	mov	r8d, 15
	lea	rcx, .LC7[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L132:
	lea	rdx, .LC5[rip]
	mov	r8d, 16
	lea	rcx, .LC8[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE4:
.L135:
	lea	rcx, .LC0[rip]
.LEHB5:
	call	_ZSt20__throw_length_errorPKc
.L139:
	lea	rdx, .LC5[rip]
	mov	r8d, 26
	lea	rcx, .LC13[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L90:
	lea	rdx, .LC5[rip]
	mov	r8d, 27
	lea	rcx, .LC14[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L141:
	lea	rdx, .LC5[rip]
	mov	r8d, 35
	lea	rcx, .LC16[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE5:
.L130:
	lea	rdx, .LC5[rip]
	mov	r8d, 14
	lea	rcx, .LC6[rip]
.LEHB6:
	call	[QWORD PTR __imp__assert[rip]]
.LEHE6:
.L136:
	movabs	r13, 2305843009213693951
	cmp	rdx, r13
	cmovbe	r13, rdx
	jmp	.L82
.L138:
	lea	rdx, .LC5[rip]
	mov	r8d, 25
	lea	rcx, .LC12[rip]
.LEHB7:
	call	[QWORD PTR __imp__assert[rip]]
.LEHE7:
.L112:
	mov	rcx, QWORD PTR 40[rsp]
	mov	rbx, rax
	call	_ZNSt6vectorIiSaIiEED1Ev
.L102:
	cmp	QWORD PTR 112[rsp], 0
	je	.L103
	lea	rcx, 112[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev.part.0
.L103:
	mov	rcx, rbx
.LEHB8:
	call	_Unwind_Resume
.LEHE8:
.L114:
	mov	rcx, rax
	call	__cxa_begin_catch
.LEHB9:
	call	__cxa_rethrow
.LEHE9:
.L111:
	mov	rbx, rax
	jmp	.L102
.L115:
	mov	rsi, rax
	call	__cxa_end_catch
	mov	rcx, rsi
	call	__cxa_begin_catch
	mov	edx, 64
	mov	rcx, rbx
	call	_ZdlPvy
.LEHB10:
	call	__cxa_rethrow
.LEHE10:
.L113:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
.LEHB11:
	call	_Unwind_Resume
	nop
.LEHE11:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA3114:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT3114-.LLSDATTD3114
.LLSDATTD3114:
	.byte	0x1
	.uleb128 .LLSDACSE3114-.LLSDACSB3114
.LLSDACSB3114:
	.uleb128 .LEHB0-.LFB3114
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3114
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L114-.LFB3114
	.uleb128 0x1
	.uleb128 .LEHB2-.LFB3114
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L111-.LFB3114
	.uleb128 0
	.uleb128 .LEHB3-.LFB3114
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L112-.LFB3114
	.uleb128 0
	.uleb128 .LEHB4-.LFB3114
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L111-.LFB3114
	.uleb128 0
	.uleb128 .LEHB5-.LFB3114
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L112-.LFB3114
	.uleb128 0
	.uleb128 .LEHB6-.LFB3114
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L111-.LFB3114
	.uleb128 0
	.uleb128 .LEHB7-.LFB3114
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L112-.LFB3114
	.uleb128 0
	.uleb128 .LEHB8-.LFB3114
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB3114
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L115-.LFB3114
	.uleb128 0x3
	.uleb128 .LEHB10-.LFB3114
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L113-.LFB3114
	.uleb128 0
	.uleb128 .LEHB11-.LFB3114
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
.LLSDACSE3114:
	.byte	0x1
	.byte	0
	.byte	0
	.byte	0x7d
	.align 4
	.long	0

.LLSDATT3114:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZSt28__throw_bad_array_new_lengthv;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
