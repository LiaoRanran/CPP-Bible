	.file	"_ch128_filesystem.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z8snprintfPcyPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8snprintfPcyPKcz
	.def	_Z8snprintfPcyPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8snprintfPcyPKcz
_Z8snprintfPcyPKcz:
.LFB16:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	QWORD PTR 88[rsp], r9
	lea	r9, 88[rsp]
	mov	QWORD PTR 40[rsp], r9
	call	__mingw_vsnprintf
	add	rsp, 56
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%s/%s\0"
	.text
	.p2align 4
	.globl	_Z9join_pathPcPKcS1_i
	.def	_Z9join_pathPcPKcS1_i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9join_pathPcPKcS1_i
_Z9join_pathPcPKcS1_i:
.LFB84:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rax, rdx
	mov	QWORD PTR 32[rsp], r8
	movsx	rdx, r9d
	lea	r8, .LC0[rip]
	mov	r9, rax
	call	_Z8snprintfPcyPKcz
	nop
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
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
.LFB85:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 304
	.seh_stackalloc	304
	.seh_endprologue
	call	__main
	lea	rbx, 48[rsp]
	mov	edx, 256
	lea	rax, .LC2[rip]
	mov	rcx, rbx
	lea	r9, .LC1[rip]
	mov	QWORD PTR 32[rsp], rax
	lea	r8, .LC0[rip]
	call	_Z8snprintfPcyPKcz
	mov	rcx, rbx
	call	strlen
	add	rsp, 304
	pop	rbx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vsnprintf;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
