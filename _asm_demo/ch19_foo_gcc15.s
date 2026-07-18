	.file	"ch19_foo_gcc15.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z3fooi
	.def	_Z3fooi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3fooi
_Z3fooi:
.LFB0:
	.seh_endprologue
	lea	eax, 3[rcx]
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
