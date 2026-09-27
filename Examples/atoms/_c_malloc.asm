	.file	"_c_malloc.c"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	printf;	.scl	3;	.type	32;	.endef
	.seh_proc	printf
printf:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "malloc0_null=%d\12\0"
.LC1:
	.ascii "alloc_aligned=%d\12\0"
.LC2:
	.ascii "dangling_value_nonzero=%d\12\0"
.LC3:
	.ascii "reached_after_free_null=1\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	xor	ecx, ecx
	call	malloc
	mov	rcx, rax
	mov	rsi, rax
	call	free
	mov	ecx, 16
	call	malloc
	mov	rcx, rax
	mov	rbx, rax
	call	free
	lea	rcx, .LC0[rip]
	xor	edx, edx
	test	rsi, rsi
	sete	dl
	call	printf
	lea	rcx, .LC1[rip]
	xor	edx, edx
	test	bl, 15
	sete	dl
	call	printf
	lea	rcx, .LC2[rip]
	xor	edx, edx
	test	rbx, rbx
	setne	dl
	call	printf
	lea	rcx, .LC3[rip]
	call	printf
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
