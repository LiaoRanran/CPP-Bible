	.file	"_ch108_relaxed.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4bumpv
	.def	_Z4bumpv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4bumpv
_Z4bumpv:
.LFB668:
	.seh_endprologue
	lock add	DWORD PTR c[rip], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z3getv
	.def	_Z3getv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3getv
_Z3getv:
.LFB669:
	.seh_endprologue
	mov	eax, DWORD PTR c[rip]
	ret
	.seh_endproc
	.globl	c
	.bss
	.align 4
c:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
