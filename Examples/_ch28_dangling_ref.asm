	.file	"_ch28_dangling_ref.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7bad_ptrv
	.def	_Z7bad_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7bad_ptrv
_Z7bad_ptrv:
.LFB0:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8good_ptrv
	.def	_Z8good_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8good_ptrv
_Z8good_ptrv:
.LFB1:
	.seh_endprologue
	lea	rax, _ZZ8good_ptrvE1x[rip]
	ret
	.seh_endproc
	.data
	.align 4
_ZZ8good_ptrvE1x:
	.long	5
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
