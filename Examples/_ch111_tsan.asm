	.file	"_ch111_tsan.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6readerv
	.def	_Z6readerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6readerv
_Z6readerv:
.LFB4956:
	.seh_endprologue
	mov	rax, QWORD PTR head[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6writerv
	.def	_Z6writerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6writerv
_Z6writerv:
.LFB4957:
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	mov	QWORD PTR 4[rsp], 0
	mov	DWORD PTR 12[rsp], 0
	mov	DWORD PTR [rsp], 42
	mov	rax, QWORD PTR head[rip]
	mov	QWORD PTR head[rip], rsp
	add	rsp, 24
	ret
	.seh_endproc
	.globl	head
	.bss
	.align 8
head:
	.space 8
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
