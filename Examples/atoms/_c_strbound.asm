	.file	"_c_strbound.c"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "1234567890\0"
.LC1:
	.ascii "%s\0"
.LC2:
	.ascii "snprintf_ret=%d\12\0"
.LC3:
	.ascii "snprintf_written=%d\12\0"
.LC4:
	.ascii "snprintf_truncated=%d\12\0"
.LC5:
	.ascii "strncpy_nul_terminated=%d\12\0"
.LC6:
	.ascii "strncpy_last_byte=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB52:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rcx, 40[rsp]
	mov	edx, 8
	lea	r9, .LC0[rip]
	lea	r8, .LC1[rip]
	call	__mingw_snprintf
	lea	rcx, .LC2[rip]
	mov	edx, eax
	mov	ebx, eax
	call	__mingw_printf
	lea	rcx, 40[rsp]
	call	strlen
	lea	rcx, .LC3[rip]
	mov	edx, eax
	call	__mingw_printf
	xor	edx, edx
	cmp	ebx, 7
	lea	rcx, .LC4[rip]
	setg	dl
	call	__mingw_printf
	xor	edx, edx
	lea	rcx, .LC5[rip]
	call	__mingw_printf
	mov	edx, 56
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	strlen;	.scl	2;	.type	32;	.endef
