	.file	"_ch145_return.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8by_valuev
	.def	_Z8by_valuev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8by_valuev
_Z8by_valuev:
.LFB394:
	.seh_endprologue
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	movups	XMMWORD PTR [rcx], xmm0
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	mov	rax, rcx
	movups	XMMWORD PTR 16[rcx], xmm0
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6by_refRK3Big
	.def	_Z6by_refRK3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6by_refRK3Big
_Z6by_refRK3Big:
.LFB395:
	.seh_endprologue
	mov	rax, rcx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6by_optv
	.def	_Z6by_optv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6by_optv
_Z6by_optv:
.LFB398:
	.seh_endprologue
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	movups	XMMWORD PTR [rcx], xmm0
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	mov	rax, rcx
	mov	DWORD PTR 32[rcx], 1
	movups	XMMWORD PTR 16[rcx], xmm0
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9use_valuev
	.def	_Z9use_valuev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_valuev
_Z9use_valuev:
.LFB399:
	.seh_endprologue
	mov	eax, 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7use_refRK3Big
	.def	_Z7use_refRK3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_refRK3Big
_Z7use_refRK3Big:
.LFB400:
	.seh_endprologue
	mov	eax, DWORD PTR [rcx]
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB421:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, 1
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	1
	.long	2
	.long	3
	.long	4
	.align 16
.LC1:
	.long	5
	.long	6
	.long	7
	.long	8
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
