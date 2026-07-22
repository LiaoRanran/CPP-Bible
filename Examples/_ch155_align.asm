	.file	"_ch155_align.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12load_alignedPKfS0_Pf
	.def	_Z12load_alignedPKfS0_Pf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12load_alignedPKfS0_Pf
_Z12load_alignedPKfS0_Pf:
.LFB7315:
	.seh_endprologue
	movaps	xmm0, XMMWORD PTR [rcx]
	addps	xmm0, XMMWORD PTR [rdx]
	movaps	XMMWORD PTR [r8], xmm0
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14load_unalignedPKfS0_Pf
	.def	_Z14load_unalignedPKfS0_Pf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14load_unalignedPKfS0_Pf
_Z14load_unalignedPKfS0_Pf:
.LFB7316:
	.seh_endprologue
	movups	xmm0, XMMWORD PTR [rcx]
	movups	xmm1, XMMWORD PTR [rdx]
	addps	xmm0, xmm1
	movups	XMMWORD PTR [r8], xmm0
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
