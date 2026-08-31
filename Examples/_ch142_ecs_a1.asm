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
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB3868:
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
	.section	.text$_ZNSt6vectorI8PositionSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI8PositionSaIS0_EED1Ev
	.def	_ZNSt6vectorI8PositionSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8PositionSaIS0_EED1Ev
_ZNSt6vectorI8PositionSaIS0_EED1Ev:
.LFB3338:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L9
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L9:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorI8VelocitySaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI8VelocitySaIS0_EED1Ev
	.def	_ZNSt6vectorI8VelocitySaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8VelocitySaIS0_EED1Ev
_ZNSt6vectorI8VelocitySaIS0_EED1Ev:
.LFB3347:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L11
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L11:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev
	.def	_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev
_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev:
.LFB3356:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L13
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L13:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "vector::_M_default_append\0"
	.section	.text$_ZNSt6vectorI8PositionSaIS0_EE17_M_default_appendEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI8PositionSaIS0_EE17_M_default_appendEy
	.def	_ZNSt6vectorI8PositionSaIS0_EE17_M_default_appendEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8PositionSaIS0_EE17_M_default_appendEy
_ZNSt6vectorI8PositionSaIS0_EE17_M_default_appendEy:
.LFB3486:
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
	test	rdx, rdx
	mov	rdi, rcx
	mov	rbx, rdx
	je	.L15
	movabs	rdx, -6148914691236517205
	mov	r8, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR 16[rcx]
	mov	rbp, QWORD PTR [rcx]
	sub	rax, r8
	sar	rax, 2
	imul	rax, rdx
	cmp	rax, rbx
	jnb	.L47
	mov	rsi, r8
	sub	rsi, rbp
	mov	rax, rsi
	sar	rax, 2
	imul	rax, rdx
	movabs	rdx, 768614336404564650
	sub	rdx, rax
	cmp	rdx, rbx
	jb	.L48
	lea	r15, -1[rbx]
	cmp	rax, rbx
	lea	r12, [rbx+rax]
	jb	.L21
	movabs	rdx, 768614336404564650
	add	rax, rax
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r13, [rax+rax*2]
	sal	r13, 2
	mov	rcx, r13
	call	_Znwy
	cmp	rbx, 1
	lea	rdx, [rax+rsi]
	mov	r14, rax
	mov	QWORD PTR [rdx], 0
	mov	DWORD PTR 8[rdx], 0x00000000
	je	.L22
.L46:
	lea	rax, 12[rdx]
	lea	rcx, [r15+r15*2]
	lea	r8, [rax+rcx*4]
	.p2align 4,,10
	.p2align 3
.L25:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 12
	mov	QWORD PTR -12[rax], rcx
	mov	ecx, DWORD PTR 8[rdx]
	mov	DWORD PTR -4[rax], ecx
	cmp	r8, rax
	jne	.L25
.L24:
	test	rsi, rsi
	jne	.L22
	test	rbp, rbp
	jne	.L49
.L28:
	lea	rax, [r12+r12*2]
	movq	xmm0, r14
	lea	rax, [r14+rax*4]
	add	r14, r13
	movq	xmm1, rax
	mov	QWORD PTR 16[rdi], r14
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR [rdi], xmm0
.L15:
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
.L47:
	mov	QWORD PTR [r8], 0
	lea	r9, 12[r8]
	sub	rbx, 1
	mov	DWORD PTR 8[r8], 0x00000000
	je	.L18
	lea	rax, [rbx+rbx*2]
	lea	rcx, [r9+rax*4]
	mov	rax, r9
	.p2align 4,,10
	.p2align 3
.L19:
	mov	rdx, QWORD PTR [r8]
	add	rax, 12
	mov	QWORD PTR -12[rax], rdx
	mov	edx, DWORD PTR 8[r8]
	mov	DWORD PTR -4[rax], edx
	cmp	rcx, rax
	jne	.L19
	movabs	rdx, 3074457345618258603
	sub	rcx, r8
	lea	rax, -24[rcx]
	shr	rax, 2
	imul	rax, rdx
	movabs	rdx, 4611686018427387903
	and	rax, rdx
	lea	rax, 3[rax+rax*2]
	lea	r9, [r9+rax*4]
.L18:
	mov	QWORD PTR 8[rdi], r9
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L21:
	movabs	rax, 768614336404564650
	cmp	r12, rax
	cmovbe	rax, r12
	lea	r13, [rax+rax*2]
	sal	r13, 2
	mov	rcx, r13
	call	_Znwy
	test	r15, r15
	lea	rdx, [rax+rsi]
	mov	r14, rax
	mov	QWORD PTR [rdx], 0
	mov	DWORD PTR 8[rdx], 0x00000000
	jne	.L46
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L22:
	mov	rdx, rbp
	mov	r8, rsi
	mov	rcx, r14
	call	memmove
	mov	rdx, QWORD PTR 16[rdi]
	sub	rdx, rbp
.L27:
	mov	rcx, rbp
	call	_ZdlPvy
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L49:
	mov	rdx, QWORD PTR 16[rdi]
	sub	rdx, rbp
	jmp	.L27
.L48:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt6vectorI8VelocitySaIS0_EE17_M_default_appendEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI8VelocitySaIS0_EE17_M_default_appendEy
	.def	_ZNSt6vectorI8VelocitySaIS0_EE17_M_default_appendEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8VelocitySaIS0_EE17_M_default_appendEy
_ZNSt6vectorI8VelocitySaIS0_EE17_M_default_appendEy:
.LFB3495:
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
	test	rdx, rdx
	mov	rdi, rcx
	mov	rbx, rdx
	je	.L50
	movabs	rdx, -6148914691236517205
	mov	r8, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR 16[rcx]
	mov	rbp, QWORD PTR [rcx]
	sub	rax, r8
	sar	rax, 2
	imul	rax, rdx
	cmp	rax, rbx
	jnb	.L82
	mov	rsi, r8
	sub	rsi, rbp
	mov	rax, rsi
	sar	rax, 2
	imul	rax, rdx
	movabs	rdx, 768614336404564650
	sub	rdx, rax
	cmp	rdx, rbx
	jb	.L83
	lea	r15, -1[rbx]
	cmp	rax, rbx
	lea	r12, [rbx+rax]
	jb	.L56
	movabs	rdx, 768614336404564650
	add	rax, rax
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r13, [rax+rax*2]
	sal	r13, 2
	mov	rcx, r13
	call	_Znwy
	cmp	rbx, 1
	lea	rdx, [rax+rsi]
	mov	r14, rax
	mov	QWORD PTR [rdx], 0
	mov	DWORD PTR 8[rdx], 0x00000000
	je	.L57
.L81:
	lea	rax, 12[rdx]
	lea	rcx, [r15+r15*2]
	lea	r8, [rax+rcx*4]
	.p2align 4,,10
	.p2align 3
.L60:
	mov	rcx, QWORD PTR [rdx]
	add	rax, 12
	mov	QWORD PTR -12[rax], rcx
	mov	ecx, DWORD PTR 8[rdx]
	mov	DWORD PTR -4[rax], ecx
	cmp	r8, rax
	jne	.L60
.L59:
	test	rsi, rsi
	jne	.L57
	test	rbp, rbp
	jne	.L84
.L63:
	lea	rax, [r12+r12*2]
	movq	xmm0, r14
	lea	rax, [r14+rax*4]
	add	r14, r13
	movq	xmm1, rax
	mov	QWORD PTR 16[rdi], r14
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR [rdi], xmm0
.L50:
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
.L82:
	mov	QWORD PTR [r8], 0
	lea	r9, 12[r8]
	sub	rbx, 1
	mov	DWORD PTR 8[r8], 0x00000000
	je	.L53
	lea	rax, [rbx+rbx*2]
	lea	rcx, [r9+rax*4]
	mov	rax, r9
	.p2align 4,,10
	.p2align 3
.L54:
	mov	rdx, QWORD PTR [r8]
	add	rax, 12
	mov	QWORD PTR -12[rax], rdx
	mov	edx, DWORD PTR 8[r8]
	mov	DWORD PTR -4[rax], edx
	cmp	rcx, rax
	jne	.L54
	movabs	rdx, 3074457345618258603
	sub	rcx, r8
	lea	rax, -24[rcx]
	shr	rax, 2
	imul	rax, rdx
	movabs	rdx, 4611686018427387903
	and	rax, rdx
	lea	rax, 3[rax+rax*2]
	lea	r9, [r9+rax*4]
.L53:
	mov	QWORD PTR 8[rdi], r9
	jmp	.L50
	.p2align 4,,10
	.p2align 3
.L56:
	movabs	rax, 768614336404564650
	cmp	r12, rax
	cmovbe	rax, r12
	lea	r13, [rax+rax*2]
	sal	r13, 2
	mov	rcx, r13
	call	_Znwy
	test	r15, r15
	lea	rdx, [rax+rsi]
	mov	r14, rax
	mov	QWORD PTR [rdx], 0
	mov	DWORD PTR 8[rdx], 0x00000000
	jne	.L81
	jmp	.L59
	.p2align 4,,10
	.p2align 3
.L57:
	mov	rdx, rbp
	mov	r8, rsi
	mov	rcx, r14
	call	memmove
	mov	rdx, QWORD PTR 16[rdi]
	sub	rdx, rbp
.L62:
	mov	rcx, rbp
	call	_ZdlPvy
	jmp	.L63
	.p2align 4,,10
	.p2align 3
.L84:
	mov	rdx, QWORD PTR 16[rdi]
	sub	rdx, rbp
	jmp	.L62
.L83:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC6:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmpln857kp6\\s.cpp\0"
.LC7:
	.ascii "arch.pos[0].x > 0\0"
.LC8:
	.ascii "naive[0]->pos.x > 0\0"
.LC9:
	.ascii "archetype entities : \0"
.LC10:
	.ascii "naive entities     : \0"
.LC11:
	.ascii "sink (arch+naive)  : \0"
.LC12:
	.ascii "sink (pos-only)    : \0"
.LC13:
	.ascii "all assertions passed\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2936:
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
	sub	rsp, 184
	.seh_stackalloc	184
	movaps	XMMWORD PTR 128[rsp], xmm6
	.seh_savexmm	xmm6, 128
	movaps	XMMWORD PTR 144[rsp], xmm7
	.seh_savexmm	xmm7, 144
	movaps	XMMWORD PTR 160[rsp], xmm8
	.seh_savexmm	xmm8, 160
	.seh_endprologue
	call	__main
	lea	rdi, 64[rsp]
	mov	ecx, 7
	xor	eax, eax
	rep stosq
	lea	r12, 64[rsp]
	mov	edx, 100000
	lea	rbp, 88[rsp]
	mov	rcx, r12
.LEHB0:
	call	_ZNSt6vectorI8PositionSaIS0_EE17_M_default_appendEy
	mov	rdx, QWORD PTR 96[rsp]
	mov	rsi, QWORD PTR 88[rsp]
	mov	rax, rdx
	sub	rax, rsi
	cmp	rax, 1199988
	jbe	.L115
	lea	rbp, 88[rsp]
	cmp	rax, 1200000
	ja	.L116
.L87:
	mov	rdi, QWORD PTR 64[rsp]
	xor	eax, eax
	xor	edx, edx
	mov	QWORD PTR 112[rsp], 100000
	mov	r15, QWORD PTR .LC3[rip]
	movss	xmm6, DWORD PTR .LC4[rip]
	.p2align 4,,10
	.p2align 3
.L89:
	lea	rcx, [rdx+rdx]
	pxor	xmm0, xmm0
	pxor	xmm1, xmm1
	cvtsi2ss	xmm0, rdx
	cvtsi2ss	xmm1, rcx
	add	rdx, 1
	unpcklps	xmm0, xmm1
	movlps	QWORD PTR [rdi+rax*4], xmm0
	pxor	xmm0, xmm0
	cvtsi2ss	xmm0, rax
	movss	DWORD PTR 8[rdi+rax*4], xmm0
	mov	QWORD PTR [rsi+rax*4], r15
	movss	DWORD PTR 8[rsi+rax*4], xmm6
	add	rax, 3
	cmp	rdx, 100000
	jne	.L89
	mov	ecx, 800000
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 40[rsp], xmm0
	call	_Znwy
.LEHE0:
	lea	r14, 800000[rax]
	xor	edx, edx
	mov	QWORD PTR 32[rsp], rax
	xor	ebx, ebx
	mov	QWORD PTR [rax], 0
	lea	rcx, 8[rax]
	mov	r8d, 799992
	mov	r13, rax
	mov	QWORD PTR 48[rsp], r14
	call	memset
	mov	QWORD PTR 40[rsp], r14
	movq	xmm7, QWORD PTR .LC5[rip]
	.p2align 4,,10
	.p2align 3
.L90:
	mov	ecx, 40
.LEHB1:
	call	_Znwy
	lea	rdx, [rbx+rbx]
	pxor	xmm0, xmm0
	pxor	xmm1, xmm1
	cvtsi2ss	xmm0, rbx
	cvtsi2ss	xmm1, rdx
	add	rdx, rbx
	mov	QWORD PTR 0[r13+rbx*8], rax
	mov	QWORD PTR 12[rax], r15
	movss	DWORD PTR 20[rax], xmm6
	movq	QWORD PTR 24[rax], xmm7
	unpcklps	xmm0, xmm1
	movlps	QWORD PTR [rax], xmm0
	pxor	xmm0, xmm0
	cvtsi2ss	xmm0, rdx
	lea	edx, 1[rbx]
	movd	xmm2, edx
	movss	DWORD PTR 8[rax], xmm0
	movd	xmm0, ebx
	add	rbx, 1
	cmp	rbx, 100000
	punpckldq	xmm0, xmm2
	movq	QWORD PTR 32[rax], xmm0
	jne	.L90
	mov	rcx, rdi
	mov	rax, rdi
	pxor	xmm6, xmm6
	lea	r8, 1200000[rdi]
	.p2align 4,,10
	.p2align 3
.L91:
	movq	xmm0, QWORD PTR [rsi]
	add	rax, 12
	add	rsi, 12
	movq	xmm1, QWORD PTR -12[rax]
	addps	xmm0, xmm1
	movss	xmm1, DWORD PTR -4[rax]
	movlps	QWORD PTR -12[rax], xmm0
	addss	xmm1, DWORD PTR -4[rsi]
	cvtss2sd	xmm0, xmm0
	addsd	xmm6, xmm0
	movss	DWORD PTR -4[rax], xmm1
	cmp	rax, r8
	jne	.L91
	movsd	xmm0, QWORD PTR _ZL6g_sink[rip]
	mov	rbx, r13
	mov	rdx, r13
	pxor	xmm8, xmm8
	addsd	xmm0, xmm6
	movsd	QWORD PTR _ZL6g_sink[rip], xmm0
	.p2align 4,,10
	.p2align 3
.L92:
	mov	rax, QWORD PTR [rdx]
	add	rdx, 8
	cmp	r14, rdx
	movq	xmm1, QWORD PTR [rax]
	movq	xmm0, QWORD PTR 12[rax]
	addps	xmm0, xmm1
	movss	xmm1, DWORD PTR 8[rax]
	addss	xmm1, DWORD PTR 20[rax]
	movlps	QWORD PTR [rax], xmm0
	cvtss2sd	xmm0, xmm0
	addsd	xmm8, xmm0
	movss	DWORD PTR 8[rax], xmm1
	jne	.L92
	movsd	xmm0, QWORD PTR _ZL6g_sink[rip]
	pxor	xmm7, xmm7
	addsd	xmm0, xmm8
	movsd	QWORD PTR _ZL6g_sink[rip], xmm0
	.p2align 4,,10
	.p2align 3
.L93:
	add	rcx, 12
	pxor	xmm0, xmm0
	cvtss2sd	xmm0, DWORD PTR -12[rcx]
	addsd	xmm7, xmm0
	cmp	rcx, r8
	jne	.L93
	movsd	xmm0, QWORD PTR _ZL6g_sink[rip]
	movss	xmm1, DWORD PTR [rdi]
	addsd	xmm0, xmm7
	movsd	QWORD PTR _ZL6g_sink[rip], xmm0
	pxor	xmm0, xmm0
	comiss	xmm1, xmm0
	jbe	.L117
	mov	rax, QWORD PTR 0[r13]
	movss	xmm1, DWORD PTR [rax]
	comiss	xmm1, xmm0
	jbe	.L118
	.p2align 4,,10
	.p2align 3
.L95:
	mov	rcx, QWORD PTR [rbx]
	test	rcx, rcx
	je	.L96
	mov	edx, 40
	call	_ZdlPvy
.L96:
	add	rbx, 8
	cmp	rbx, r14
	jne	.L95
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC9[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	edx, 100000
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC10[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	edx, 100000
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC11[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm8
	mov	rcx, rax
	addsd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC12[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	movapd	xmm1, xmm7
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC13[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE1:
	lea	rcx, 32[rsp]
	call	_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev
	mov	rcx, rbp
	call	_ZNSt6vectorI8VelocitySaIS0_EED1Ev
	mov	rcx, r12
	call	_ZNSt6vectorI8PositionSaIS0_EED1Ev
	nop
	movaps	xmm6, XMMWORD PTR 128[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 144[rsp]
	movaps	xmm8, XMMWORD PTR 160[rsp]
	add	rsp, 184
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L116:
	lea	rax, 1200000[rsi]
	cmp	rdx, rax
	je	.L87
	mov	QWORD PTR 96[rsp], rax
	jmp	.L87
.L115:
	movabs	rdx, -6148914691236517205
	sar	rax, 2
	mov	rcx, rbp
	imul	rax, rdx
	mov	edx, 100000
	sub	rdx, rax
.LEHB2:
	call	_ZNSt6vectorI8VelocitySaIS0_EE17_M_default_appendEy
.LEHE2:
	mov	rsi, QWORD PTR 88[rsp]
	jmp	.L87
.L117:
	lea	rdx, .LC6[rip]
	mov	r8d, 83
	lea	rcx, .LC7[rip]
.LEHB3:
	call	[QWORD PTR __imp__assert[rip]]
.L118:
	lea	rdx, .LC6[rip]
	mov	r8d, 84
	lea	rcx, .LC8[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE3:
.L99:
	mov	rbx, rax
	jmp	.L98
.L100:
	lea	rcx, 32[rsp]
	mov	rbx, rax
	call	_ZNSt6vectorIP11NaiveEntitySaIS1_EED1Ev
.L98:
	mov	rcx, rbp
	call	_ZNSt6vectorI8VelocitySaIS0_EED1Ev
	mov	rcx, r12
	call	_ZNSt6vectorI8PositionSaIS0_EED1Ev
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2936:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2936-.LLSDACSB2936
.LLSDACSB2936:
	.uleb128 .LEHB0-.LFB2936
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L99-.LFB2936
	.uleb128 0
	.uleb128 .LEHB1-.LFB2936
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L100-.LFB2936
	.uleb128 0
	.uleb128 .LEHB2-.LFB2936
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L99-.LFB2936
	.uleb128 0
	.uleb128 .LEHB3-.LFB2936
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L100-.LFB2936
	.uleb128 0
	.uleb128 .LEHB4-.LFB2936
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE2936:
	.section	.text.startup,"x"
	.seh_endproc
.lcomm _ZL6g_sink,8,8
	.section .rdata,"dr"
	.align 8
.LC3:
	.long	1036831949
	.long	1045220557
	.align 4
.LC4:
	.long	1050253722
	.align 8
.LC5:
	.long	100
	.long	100
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
