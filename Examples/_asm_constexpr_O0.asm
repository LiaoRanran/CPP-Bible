	.file	"_asm_constexpr.cpp"
	.intel_syntax noprefix
	.text
	.globl	g_global
	.data
	.align 4
g_global:
	.long	100
	.text
	.globl	_Z13use_constexprv
	.def	_Z13use_constexprv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13use_constexprv
_Z13use_constexprv:
.LFB20:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 49
	mov	DWORD PTR -8[rbp], 120
	mov	DWORD PTR -12[rbp], 42
	movsd	xmm0, QWORD PTR .LC0[rip]
	movsd	QWORD PTR -24[rbp], xmm0
	mov	DWORD PTR -28[rbp], 16
	mov	edx, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR -8[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -12[rbp]
	add	edx, eax
	movsd	xmm0, QWORD PTR -24[rbp]
	cvttsd2si	eax, xmm0
	add	edx, eax
	mov	eax, DWORD PTR -28[rbp]
	add	edx, eax
	mov	eax, DWORD PTR g_global[rip]
	add	eax, edx
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
