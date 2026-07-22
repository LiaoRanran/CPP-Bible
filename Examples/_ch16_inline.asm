	.file	"_ch16_inline.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6calleri
	.def	_Z6calleri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6calleri
_Z6calleri:
.LFB1:
	.seh_endprologue
	lea	eax, 2[rcx+rcx]
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
