	.file	"_ch111_tsan.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6readerv
	.def	_Z6readerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6readerv
_Z6readerv:
.LFB3703:
	.seh_endprologue
	mov	rax, QWORD PTR head[rip]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6writerv
	.def	_Z6writerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6writerv
_Z6writerv:
.LFB3704:
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	mov	DWORD PTR [rsp], 42
	mov	QWORD PTR 8[rsp], 0
	mov	rax, QWORD PTR head[rip]
	mov	rax, rsp
	mov	QWORD PTR head[rip], rax
	add	rsp, 24
	ret
	.seh_endproc
	.globl	head
	.bss
	.align 8
head:
	.space 8
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
