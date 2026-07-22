	.file	"_ch110_dwcas.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7swap_dwyy
	.def	_Z7swap_dwyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7swap_dwyy
_Z7swap_dwyy:
.LFB668:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	rbx, rcx
	mov	rsi, rdx
	lea	rcx, g_pair[rip]
	xor	edx, edx
	call	__atomic_load_16
	lea	rdx, 64[rsp]
	mov	r9d, 4
	mov	DWORD PTR 32[rsp], 0
	lea	r8, 48[rsp]
	lea	rcx, g_pair[rip]
	mov	QWORD PTR 48[rsp], rbx
	mov	QWORD PTR 56[rsp], rsi
	movaps	XMMWORD PTR 64[rsp], xmm0
	call	__atomic_compare_exchange_16
	nop
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.globl	g_pair
	.bss
	.align 16
g_pair:
	.space 16
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	__atomic_load_16;	.scl	2;	.type	32;	.endef
	.def	__atomic_compare_exchange_16;	.scl	2;	.type	32;	.endef
