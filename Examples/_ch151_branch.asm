	.file	"_ch151_branch.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC1:
	.ascii "branch: ms=%.3f r=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5831:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	DWORD PTR 44[rsp], 0
	mov	rbx, rax
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L5:
	mov	edx, DWORD PTR 44[rsp]
	test	al, 1
	je	.L2
	lea	edx, [rdx+rax*2]
	add	eax, 1
	mov	DWORD PTR 44[rsp], edx
	cmp	eax, 100000000
	jne	.L5
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r8d, DWORD PTR 44[rsp]
	pxor	xmm1, xmm1
	lea	rcx, .LC1[rip]
	sub	rax, rbx
	cvtsi2sd	xmm1, rax
	divsd	xmm1, QWORD PTR .LC0[rip]
	movq	rdx, xmm1
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	lea	edx, 7[rax+rdx]
	add	eax, 1
	mov	DWORD PTR 44[rsp], edx
	jmp	.L5
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1093567616
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
