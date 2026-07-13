	.file	"_ch144_move.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z11make_bufferv
	.def	_Z11make_bufferv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11make_bufferv
_Z11make_bufferv:
.LFB1715:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	pxor	xmm0, xmm0
	mov	rbx, rcx
	movups	XMMWORD PTR [rcx], xmm0
	mov	QWORD PTR 16[rcx], 0
	mov	ecx, 16384
	call	_Znwy
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	lea	rdx, 16384[rax]
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 16[rbx], rdx
.L2:
	movups	XMMWORD PTR [rax], xmm0
	add	rax, 32
	movups	XMMWORD PTR -16[rax], xmm0
	cmp	rax, rdx
	jne	.L2
	mov	QWORD PTR 8[rbx], rax
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7consumev
	.def	_Z7consumev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7consumev
_Z7consumev:
.LFB1760:
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
	pxor	xmm0, xmm0
	mov	rbx, rcx
	movups	XMMWORD PTR [rcx], xmm0
	mov	QWORD PTR 16[rcx], 0
	mov	ecx, 16384
.LEHB0:
	call	_Znwy
.LEHE0:
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	lea	rdx, 16384[rax]
	mov	rdi, rax
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 16[rbx], rdx
.L7:
	movups	XMMWORD PTR [rax], xmm0
	add	rax, 32
	movups	XMMWORD PTR -16[rax], xmm0
	cmp	rdx, rax
	jne	.L7
	mov	QWORD PTR 8[rbx], rdx
	mov	ecx, 32768
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	r8d, 16384
	mov	rdx, rdi
	mov	rcx, rax
	mov	DWORD PTR 16384[rax], 1
	mov	rsi, rax
	call	memcpy
	mov	rdx, QWORD PTR 16[rbx]
	movq	xmm6, rsi
	mov	rcx, rdi
	lea	rax, 16388[rsi]
	add	rsi, 32768
	movq	xmm1, rax
	punpcklqdq	xmm6, xmm1
	sub	rdx, rdi
	call	_ZdlPvy
	movups	XMMWORD PTR [rbx], xmm6
	mov	rax, rbx
	mov	QWORD PTR 16[rbx], rsi
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L10:
	mov	rcx, QWORD PTR [rbx]
	mov	rsi, rax
	mov	rdx, QWORD PTR 16[rbx]
	sub	rdx, rcx
	test	rcx, rcx
	je	.L9
	call	_ZdlPvy
.L9:
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1760:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1760-.LLSDACSB1760
.LLSDACSB1760:
	.uleb128 .LEHB0-.LFB1760
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1760
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L10-.LFB1760
	.uleb128 0
	.uleb128 .LEHB2-.LFB1760
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE1760:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z4demov
	.def	_Z4demov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4demov
_Z4demov:
.LFB1761:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	lea	rcx, 32[rsp]
	call	_Z7consumev
	mov	rcx, QWORD PTR 32[rsp]
	mov	rbx, QWORD PTR 40[rsp]
	sub	rbx, rcx
	sar	rbx, 2
	test	rcx, rcx
	je	.L18
	mov	rdx, QWORD PTR 48[rsp]
	sub	rdx, rcx
	call	_ZdlPvy
.L18:
	mov	eax, ebx
	add	rsp, 64
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	7
	.long	7
	.long	7
	.long	7
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
