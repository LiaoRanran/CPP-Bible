	.file	"_asm_ranges.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10use_rangesv
	.def	_Z10use_rangesv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_rangesv
_Z10use_rangesv:
.LFB3882:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rax, QWORD PTR .LC1[rip]
	mov	ecx, 24
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	QWORD PTR 48[rsp], rax
	movaps	XMMWORD PTR 32[rsp], xmm0
	call	_Znwy
	mov	rdx, QWORD PTR 32[rsp]
	lea	r9, 24[rax]
	mov	QWORD PTR [rax], rdx
	mov	rdx, QWORD PTR 40[rsp]
	mov	QWORD PTR 8[rax], rdx
	mov	rdx, QWORD PTR 48[rsp]
	mov	QWORD PTR 16[rax], rdx
	mov	rdx, rax
	jmp	.L3
	.p2align 4,,10
	.p2align 3
.L14:
	add	rdx, 4
	cmp	r9, rdx
	je	.L5
.L3:
	mov	ecx, DWORD PTR [rdx]
	mov	r8, rdx
	test	cl, 1
	jne	.L14
	cmp	r9, rdx
	je	.L5
	xor	ebx, ebx
	.p2align 4,,10
	.p2align 3
.L9:
	imul	ecx, ecx
	lea	rdx, 4[r8]
	add	ebx, ecx
	cmp	r9, rdx
	jne	.L8
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L15:
	add	rdx, 4
	cmp	r9, rdx
	je	.L6
.L8:
	mov	ecx, DWORD PTR [rdx]
	mov	r8, rdx
	test	cl, 1
	jne	.L15
	cmp	rdx, r9
	jne	.L9
.L6:
	mov	rcx, rax
	mov	edx, 24
	call	_ZdlPvy
	mov	eax, ebx
	add	rsp, 64
	pop	rbx
	ret
.L5:
	xor	ebx, ebx
	jmp	.L6
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	1
	.long	2
	.long	3
	.long	4
	.align 8
.LC1:
	.long	5
	.long	6
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
