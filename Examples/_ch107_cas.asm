	.file	"_ch107_cas.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7try_setii
	.def	_Z7try_setii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7try_setii
_Z7try_setii:
.LFB668:
	.seh_endprologue
	mov	eax, ecx
	lock cmpxchg	DWORD PTR g[rip], edx
	sete	al
	ret
	.seh_endproc
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
