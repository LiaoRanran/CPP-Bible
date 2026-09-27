	.file	"_c_setjmp.c"
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
	.section .rdata,"dr"
.LC0:
	.ascii "after_longjmp_plain=%d\12\0"
.LC1:
	.ascii "after_longjmp_volatile=%d\12\0"
	.text
	.p2align 4
	.def	setjmp_probe;	.scl	3;	.type	32;	.endef
	.seh_proc	setjmp_probe
setjmp_probe:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	lea	rcx, env[rip]
	mov	rdx, rbp
	mov	DWORD PTR -4[rbp], 0
	call	_setjmp
	test	eax, eax
	je	.L6
	lea	rcx, .LC0[rip]
	xor	edx, edx
	call	printf
	mov	edx, DWORD PTR -4[rbp]
	lea	rcx, .LC1[rip]
	call	printf
	nop
	add	rsp, 48
	pop	rbp
	ret
.L6:
	mov	DWORD PTR -4[rbp], 5
	mov	edx, 1
	lea	rcx, env[rip]
	call	[QWORD PTR __imp_longjmp[rip]]
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	setjmp_probe
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
.lcomm env,256,32
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_setjmp;	.scl	2;	.type	32;	.endef
