	.file	"_ch151_dce_good.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB11:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "dce_good: elapsed_ms=%.3f sink=%lld\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5564:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	mov	QWORD PTR 40[rsp], 0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, rax
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L4:
	mov	rdx, QWORD PTR 40[rsp]
	add	rdx, rax
	add	rax, 1
	cmp	rax, 100000000
	mov	QWORD PTR 40[rsp], rdx
	jne	.L4
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r8, QWORD PTR 40[rsp]
	lea	rcx, .LC1[rip]
	pxor	xmm1, xmm1
	sub	rax, rbx
	cvtsi2sd	xmm1, rax
	divsd	xmm1, QWORD PTR .LC0[rip]
	movq	rdx, xmm1
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
