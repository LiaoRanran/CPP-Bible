	.file	"_c_intpromo.c"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "cmp_signed_unsigned=%d\12\0"
.LC1:
	.ascii "minus1_as_unsigned=%u\12\0"
.LC2:
	.ascii "char_promoted_sum=%d\12\0"
.LC3:
	.ascii "char_sum_type_size=%zu\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB22:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	xor	edx, edx
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	edx, -1
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 200
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	mov	edx, 4
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
