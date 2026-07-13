	.file	"_ch108_acqrel.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7publishi
	.def	_Z7publishi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7publishi
_Z7publishi:
.LFB665:
	.seh_endprologue
	mov	DWORD PTR g[rip], ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7consumev
	.def	_Z7consumev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7consumev
_Z7consumev:
.LFB666:
	.seh_endprologue
	mov	eax, DWORD PTR g[rip]
	ret
	.seh_endproc
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
