	.file	"_ch140_if_constexpr.cpp"
	.intel_syntax noprefix
	.text
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "cpu\0"
.LC1:
	.ascii "gpu\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB50:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rcx, .LC0[rip]
	call	puts
	lea	rcx, .LC1[rip]
	call	puts
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	puts;	.scl	2;	.type	32;	.endef
