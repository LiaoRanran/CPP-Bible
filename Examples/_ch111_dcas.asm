	.file	"_ch111_dcas.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	dcas_probe
	.def	dcas_probe;	.scl	2;	.type	32;	.endef
	.seh_proc	dcas_probe
dcas_probe:
.LFB669:
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	r9d, 4
	movdqa	xmm0, XMMWORD PTR [rcx]
	movdqa	xmm1, XMMWORD PTR [rdx]
	lea	rcx, g[rip]
	lea	rdx, 64[rsp]
	lea	r8, 48[rsp]
	movaps	XMMWORD PTR 64[rsp], xmm0
	mov	DWORD PTR 32[rsp], 2
	movaps	XMMWORD PTR 48[rsp], xmm1
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
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	__atomic_compare_exchange_16;	.scl	2;	.type	32;	.endef
