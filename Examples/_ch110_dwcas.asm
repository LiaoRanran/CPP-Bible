	.file	"_ch110_dwcas.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7swap_dwyy
	.def	_Z7swap_dwyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7swap_dwyy
_Z7swap_dwyy:
.LFB665:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 112
	.seh_stackalloc	112
	movaps	XMMWORD PTR 80[rsp], xmm6
	.seh_savexmm	xmm6, 80
	movaps	XMMWORD PTR 96[rsp], xmm7
	.seh_savexmm	xmm7, 96
	.seh_endprologue
	lea	rbx, g_pair[rip]
	movq	xmm6, rcx
	movq	xmm7, rdx
	mov	rcx, rbx
	xor	edx, edx
	call	__atomic_load_16
	lea	rdx, 64[rsp]
	mov	r9d, 4
	mov	rcx, rbx
	movaps	XMMWORD PTR 64[rsp], xmm0
	lea	r8, 48[rsp]
	movdqa	xmm0, xmm6
	mov	DWORD PTR 32[rsp], 0
	punpcklqdq	xmm0, xmm7
	movaps	XMMWORD PTR 48[rsp], xmm0
	call	__atomic_compare_exchange_16
	nop
	movaps	xmm6, XMMWORD PTR 80[rsp]
	movaps	xmm7, XMMWORD PTR 96[rsp]
	add	rsp, 112
	pop	rbx
	ret
	.seh_endproc
	.globl	g_pair
	.bss
	.align 16
g_pair:
	.space 16
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__atomic_load_16;	.scl	2;	.type	32;	.endef
	.def	__atomic_compare_exchange_16;	.scl	2;	.type	32;	.endef
