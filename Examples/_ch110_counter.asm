	.file	"_ch110_counter.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z11inc_relaxedv
	.def	_Z11inc_relaxedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11inc_relaxedv
_Z11inc_relaxedv:
.LFB668:
	.seh_endprologue
	lock add	QWORD PTR g_counter[rip], 1
	ret
	.seh_endproc
	.globl	g_counter
	.bss
	.align 8
g_counter:
	.space 8
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
