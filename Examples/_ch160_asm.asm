	.file	"_ch160_asm.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN4PoolD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN4PoolD1Ev
	.def	_ZN4PoolD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4PoolD1Ev
_ZN4PoolD1Ev:
.LFB1735:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, QWORD PTR 8[rcx]
	mov	rsi, QWORD PTR 16[rcx]
	mov	rdi, rcx
	cmp	rsi, rbx
	je	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	mov	rcx, QWORD PTR [rbx]
	add	rbx, 8
	call	_ZdlPv
	cmp	rsi, rbx
	jne	.L3
	mov	rbx, QWORD PTR 8[rdi]
.L2:
	test	rbx, rbx
	je	.L1
	mov	rdx, QWORD PTR 24[rdi]
	mov	rcx, rbx
	sub	rdx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.text
	.p2align 4
	.globl	_Z12hot_allocateR4Pool
	.def	_Z12hot_allocateR4Pool;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12hot_allocateR4Pool
_Z12hot_allocateR4Pool:
.LFB1737:
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
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rsi, QWORD PTR [rcx]
	test	rsi, rsi
	mov	rbx, rcx
	je	.L8
	mov	rcx, QWORD PTR [rsi]
.L9:
	mov	QWORD PTR [rbx], rcx
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	rax, rsi
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	mov	rcx, QWORD PTR 32[rcx]
	sal	rcx, 12
	call	_Znwy
	mov	rdi, rax
	mov	rax, QWORD PTR 16[rbx]
	cmp	rax, QWORD PTR 24[rbx]
	je	.L10
	mov	QWORD PTR [rax], rdi
	add	QWORD PTR 16[rbx], 8
.L11:
	mov	r9, QWORD PTR 32[rbx]
	mov	rax, rdi
	mov	edx, 4096
	mov	r8, QWORD PTR [rbx]
	.p2align 4,,10
	.p2align 3
.L21:
	mov	rcx, r8
	mov	r8, rax
	mov	QWORD PTR [rax], rcx
	add	rax, r9
	sub	rdx, 1
	jne	.L21
	mov	rsi, r9
	sal	rsi, 12
	sub	rsi, r9
	add	rsi, rdi
	jmp	.L9
.L10:
	mov	r12, QWORD PTR 8[rbx]
	mov	r13, rax
	movabs	rcx, 1152921504606846975
	sub	r13, r12
	mov	rdx, r13
	sar	rdx, 3
	cmp	rdx, rcx
	je	.L30
	cmp	rax, r12
	je	.L31
	lea	rax, [rdx+rdx]
	cmp	rax, rdx
	jb	.L23
	test	rax, rax
	jne	.L29
	xor	ebp, ebp
.L17:
	lea	rax, 8[rsi+r13]
	movq	xmm6, rsi
	test	r13, r13
	mov	QWORD PTR [rsi+r13], rdi
	movq	xmm0, rax
	punpcklqdq	xmm6, xmm0
	jg	.L32
	test	r12, r12
	jne	.L33
.L20:
	movups	XMMWORD PTR 8[rbx], xmm6
	mov	QWORD PTR 24[rbx], rbp
	jmp	.L11
.L32:
	mov	rdx, r12
	mov	r8, r13
	mov	rcx, rsi
	call	memmove
	mov	rdx, QWORD PTR 24[rbx]
	sub	rdx, r12
.L19:
	mov	rcx, r12
	call	_ZdlPvy
	jmp	.L20
.L29:
	movabs	rdx, 1152921504606846975
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rbp, 0[0+rax*8]
.L16:
	mov	rcx, rbp
	call	_Znwy
	mov	rsi, rax
	add	rbp, rax
	jmp	.L17
.L31:
	mov	rax, rdx
	add	rax, 1
	jnc	.L29
.L23:
	movabs	rbp, 9223372036854775800
	jmp	.L16
.L33:
	mov	rdx, QWORD PTR 24[rbx]
	sub	rdx, r12
	jmp	.L19
.L30:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1738:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	call	__main
	mov	ecx, 262144
	pxor	xmm0, xmm0
	mov	QWORD PTR 64[rsp], 64
	movaps	XMMWORD PTR 32[rsp], xmm0
	movaps	XMMWORD PTR 48[rsp], xmm0
.LEHB0:
	call	_Znwy
	mov	ecx, 8
	mov	rbx, rax
	call	_Znwy
.LEHE0:
	lea	rdx, 8[rax]
	movq	xmm0, rax
	mov	QWORD PTR [rax], rbx
	xor	ecx, ecx
	movq	xmm1, rdx
	mov	QWORD PTR 56[rsp], rdx
	mov	rax, rbx
	punpcklqdq	xmm0, xmm1
	lea	r8, 262144[rbx]
	movups	XMMWORD PTR 40[rsp], xmm0
	.p2align 4,,10
	.p2align 3
.L35:
	mov	rdx, rcx
	mov	rcx, rax
	add	rax, 64
	mov	QWORD PTR -64[rax], rdx
	cmp	r8, rax
	jne	.L35
	lea	rcx, 32[rsp]
	mov	QWORD PTR 32[rsp], rdx
	call	_ZN4PoolD1Ev
	xor	eax, eax
	add	rsp, 80
	pop	rbx
	ret
.L37:
	lea	rcx, 32[rsp]
	mov	rbx, rax
	call	_ZN4PoolD1Ev
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1738:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1738-.LLSDACSB1738
.LLSDACSB1738:
	.uleb128 .LEHB0-.LFB1738
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L37-.LFB1738
	.uleb128 0
	.uleb128 .LEHB1-.LFB1738
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1738:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
