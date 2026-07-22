	.file	"_ch107_fetch_add.cpp"
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
	.p2align 4
	.globl	_Z4readv
	.def	_Z4readv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4readv
_Z4readv:
.LFB669:
	.seh_endprologue
	mov	eax, DWORD PTR g[rip]
	ret
	.seh_endproc
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
