	.file	"_ch128_filesystem.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "%s/%s\0"
	.text
	.p2align 4
	.globl	_Z9join_pathPcPKcS1_i
	.def	_Z9join_pathPcPKcS1_i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9join_pathPcPKcS1_i
_Z9join_pathPcPKcS1_i:
.LFB59:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	QWORD PTR 32[rsp], r8
	mov	rax, rdx
	lea	r8, .LC0[rip]
	movsxd	rdx, r9d
	mov	r9, rax
	call	__mingw_snprintf
	nop
	add	rsp, 56
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "/var/log\0"
.LC2:
	.ascii "app.log\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB60:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 304
	.seh_stackalloc	304
	.seh_endprologue
	call	__main
	mov	edx, 256
	lea	rcx, 48[rsp]
	lea	rax, .LC2[rip]
	mov	QWORD PTR 32[rsp], rax
	lea	r9, .LC1[rip]
	lea	r8, .LC0[rip]
	call	__mingw_snprintf
	lea	rcx, 48[rsp]
	call	strlen
	add	rsp, 304
	pop	rbx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	strlen;	.scl	2;	.type	32;	.endef
