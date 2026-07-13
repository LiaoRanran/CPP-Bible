	.file	"_ch110_counter.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z11inc_relaxedv
	.def	_Z11inc_relaxedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11inc_relaxedv
_Z11inc_relaxedv:
.LFB665:
	.seh_endprologue
	lock add	QWORD PTR g_counter[rip], 1
	ret
	.seh_endproc
	.globl	g_counter
	.bss
	.align 8
g_counter:
	.space 8
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
