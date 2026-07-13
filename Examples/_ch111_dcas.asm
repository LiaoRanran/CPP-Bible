	.file	"_ch111_dcas.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	dcas_probe
	.def	dcas_probe;	.scl	2;	.type	32;	.endef
	.seh_proc	dcas_probe
dcas_probe:
.LFB666:
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	r8, QWORD PTR [rcx]
	vmovdqa	xmm0, XMMWORD PTR [rdx]
	mov	r9, QWORD PTR 8[rcx]
	lea	rdx, 64[rsp]
	lea	rcx, g[rip]
	mov	DWORD PTR 32[rsp], 2
	mov	QWORD PTR 64[rsp], r8
	mov	QWORD PTR 72[rsp], r9
	lea	r8, 48[rsp]
	mov	r9d, 4
	vmovdqa	XMMWORD PTR 48[rsp], xmm0
	call	__atomic_compare_exchange_16
	movzx	eax, al
	add	rsp, 88
	ret
	.seh_endproc
	.globl	g
	.bss
	.align 16
g:
	.space 16
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__atomic_compare_exchange_16;	.scl	2;	.type	32;	.endef
