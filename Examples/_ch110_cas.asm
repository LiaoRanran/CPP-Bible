	.file	"_ch110_cas.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4pushi
	.def	_Z4pushi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4pushi
_Z4pushi:
.LFB671:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ebx, ecx
	mov	ecx, 16
	call	_Znwy
	mov	QWORD PTR [rax], 0
	mov	rdx, rax
	mov	QWORD PTR 8[rax], 0
	mov	DWORD PTR [rax], ebx
	mov	rax, QWORD PTR head[rip]
.L2:
	mov	QWORD PTR 8[rdx], rax
	lock cmpxchg	QWORD PTR head[rip], rdx
	jne	.L2
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.globl	head
	.bss
	.align 8
head:
	.space 8
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
