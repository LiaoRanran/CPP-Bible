	.file	"_ch111_aba.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10pop_unsafev
	.def	_Z10pop_unsafev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10pop_unsafev
_Z10pop_unsafev:
.LFB671:
	.seh_endprologue
	mov	rax, QWORD PTR top[rip]
.L2:
	test	rax, rax
	je	.L1
	mov	rdx, QWORD PTR 8[rax]
	lock cmpxchg	QWORD PTR top[rip], rdx
	jne	.L2
.L1:
	ret
	.seh_endproc
	.globl	top
	.bss
	.align 8
top:
	.space 8
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
