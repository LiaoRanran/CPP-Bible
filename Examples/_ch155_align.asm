	.file	"_ch155_align.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12load_alignedPKfS0_Pf
	.def	_Z12load_alignedPKfS0_Pf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12load_alignedPKfS0_Pf
_Z12load_alignedPKfS0_Pf:
.LFB6457:
	.seh_endprologue
	vmovaps	xmm0, XMMWORD PTR [rcx]
	vaddps	xmm0, xmm0, XMMWORD PTR [rdx]
	vmovaps	XMMWORD PTR [r8], xmm0
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z14load_unalignedPKfS0_Pf
	.def	_Z14load_unalignedPKfS0_Pf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14load_unalignedPKfS0_Pf
_Z14load_unalignedPKfS0_Pf:
.LFB6458:
	.seh_endprologue
	vmovups	xmm0, XMMWORD PTR [rdx]
	vaddps	xmm0, xmm0, XMMWORD PTR [rcx]
	vmovups	XMMWORD PTR [r8], xmm0
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
