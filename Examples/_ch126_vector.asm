	.file	"_ch126_vector.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10sum_vectorRKSt6vectorIiSaIiEE
	.def	_Z10sum_vectorRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sum_vectorRKSt6vectorIiSaIiEE
_Z10sum_vectorRKSt6vectorIiSaIiEE:
.LFB1715:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rcx, rax
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L3
.L1:
	mov	eax, edx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1720:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	xor	ebx, ebx
	call	__main
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	ecx, 20
	mov	DWORD PTR 48[rsp], 5
	movaps	XMMWORD PTR 32[rsp], xmm0
	call	_Znwy
	mov	rcx, rax
	mov	rax, QWORD PTR 32[rsp]
	mov	rdx, rcx
	mov	QWORD PTR [rcx], rax
	mov	rax, QWORD PTR 40[rsp]
	mov	QWORD PTR 8[rcx], rax
	mov	eax, DWORD PTR 48[rsp]
	mov	DWORD PTR 16[rcx], eax
	lea	rax, 20[rcx]
	.p2align 4,,10
	.p2align 3
.L8:
	add	ebx, DWORD PTR [rdx]
	add	rdx, 4
	cmp	rdx, rax
	jne	.L8
	mov	edx, 20
	call	_ZdlPvy
	mov	eax, ebx
	add	rsp, 64
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	1
	.long	2
	.long	3
	.long	4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
