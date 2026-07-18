	.file	"_asm_tpl_sfinae.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10use_sfinaev
	.def	_Z10use_sfinaev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_sfinaev
_Z10use_sfinaev:
.LFB19:
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	mov	DWORD PTR 4[rsp], 42
	movsd	QWORD PTR 8[rsp], xmm0
	movsd	xmm0, QWORD PTR 8[rsp]
	mov	edx, DWORD PTR 4[rsp]
	cvttsd2si	eax, xmm0
	add	eax, edx
	add	rsp, 24
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
