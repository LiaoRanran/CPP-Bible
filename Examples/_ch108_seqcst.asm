	.file	"_ch108_seqcst.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6writerv
	.def	_Z6writerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6writerv
_Z6writerv:
.LFB668:
	.seh_endprologue
	mov	eax, 1
	xchg	eax, DWORD PTR x[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6readerv
	.def	_Z6readerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6readerv
_Z6readerv:
.LFB669:
	.seh_endprologue
	mov	eax, DWORD PTR x[rip]
	ret
	.seh_endproc
	.globl	x
	.bss
	.align 4
x:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
