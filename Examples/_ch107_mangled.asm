	.file	"_ch107_mangled.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7add_onev
	.def	_Z7add_onev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7add_onev
_Z7add_onev:
.LFB668:
	.seh_endprologue
	lock add	DWORD PTR g[rip], 1
	ret
	.seh_endproc
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
