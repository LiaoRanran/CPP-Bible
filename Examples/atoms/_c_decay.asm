	.file	"_c_decay.c"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "decay_sizeof_array=%zu\12\0"
.LC1:
	.ascii "decay_len_true=%zu\12\0"
.LC2:
	.ascii "decay_sizeof_param=%zu\12\0"
.LC3:
	.ascii "decay_len_wrong_inside=%zu\12\0"
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
	mov	edx, 40
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	edx, 10
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 8
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	mov	edx, 2
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
