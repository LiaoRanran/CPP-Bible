	.file	"_ch144_auto.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12explicit_sumRKSt6vectorIlSaIlEE
	.def	_Z12explicit_sumRKSt6vectorIlSaIlEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12explicit_sumRKSt6vectorIlSaIlEE
_Z12explicit_sumRKSt6vectorIlSaIlEE:
.LFB1999:
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
	.p2align 4
	.globl	_Z8auto_sumRKSt6vectorIlSaIlEE
	.def	_Z8auto_sumRKSt6vectorIlSaIlEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8auto_sumRKSt6vectorIlSaIlEE
_Z8auto_sumRKSt6vectorIlSaIlEE:
.LFB2093:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rax, rcx
	je	.L7
	.p2align 4,,10
	.p2align 3
.L9:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L9
.L7:
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z4demov
	.def	_Z4demov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4demov
_Z4demov:
.LFB2005:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 4096
	call	_Znwy
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	rcx, rax
	mov	rdx, rax
	mov	r8, rax
	lea	r9, 4096[rax]
.L13:
	movups	XMMWORD PTR [r8], xmm0
	add	r8, 32
	movups	XMMWORD PTR -16[r8], xmm0
	cmp	r9, r8
	jne	.L13
	mov	r8, rcx
	pxor	xmm0, xmm0
	.p2align 4,,10
	.p2align 3
.L14:
	movdqu	xmm2, XMMWORD PTR [r8]
	add	r8, 16
	cmp	r9, r8
	paddd	xmm0, xmm2
	jne	.L14
	movdqa	xmm1, xmm0
	psrldq	xmm1, 8
	paddd	xmm0, xmm1
	movdqa	xmm1, xmm0
	psrldq	xmm1, 4
	paddd	xmm0, xmm1
	movd	r8d, xmm0
	pxor	xmm0, xmm0
	.p2align 4,,10
	.p2align 3
.L15:
	movdqu	xmm3, XMMWORD PTR [rdx]
	add	rdx, 16
	cmp	rdx, r9
	paddd	xmm0, xmm3
	jne	.L15
	movdqa	xmm1, xmm0
	mov	edx, 4096
	psrldq	xmm1, 8
	paddd	xmm0, xmm1
	movdqa	xmm1, xmm0
	psrldq	xmm1, 4
	paddd	xmm0, xmm1
	movd	ebx, xmm0
	add	ebx, r8d
	call	_ZdlPvy
	mov	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	3
	.long	3
	.long	3
	.long	3
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
