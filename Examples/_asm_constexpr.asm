	.file	"_asm_constexpr.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13use_constexprv
	.def	_Z13use_constexprv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13use_constexprv
_Z13use_constexprv:
.LFB19:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	mov	DWORD PTR 8[rsp], 49
	mov	DWORD PTR 12[rsp], 120
	mov	DWORD PTR 16[rsp], 42
	movsd	QWORD PTR 24[rsp], xmm0
	mov	DWORD PTR 20[rsp], 16
	mov	eax, DWORD PTR 8[rsp]
	mov	r8d, DWORD PTR 12[rsp]
	mov	ecx, DWORD PTR 16[rsp]
	movsd	xmm0, QWORD PTR 24[rsp]
	mov	edx, DWORD PTR 20[rsp]
	add	eax, r8d
	add	eax, ecx
	cvttsd2si	ecx, xmm0
	add	eax, ecx
	add	eax, edx
	add	eax, DWORD PTR g_global[rip]
	add	rsp, 40
	ret
	.seh_endproc
	.globl	g_global
	.data
	.align 4
g_global:
	.long	100
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
