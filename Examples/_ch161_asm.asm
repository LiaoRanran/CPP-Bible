	.file	"_ch161_zerooverhead.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "forced critical message\0"
.LC1:
	.ascii "[lvl%d] %s\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB25:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	r8, .LC0[rip]
	mov	edx, 6
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
