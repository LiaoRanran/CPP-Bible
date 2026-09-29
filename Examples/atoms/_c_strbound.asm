	.file	"_c_strbound.c"
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
	.ascii "%s\0"
	.text
	.p2align 4
	.def	snprintf.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	snprintf.constprop.0
snprintf.constprop.0:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	r8, .LC0[rip]
	mov	edx, 8
	mov	QWORD PTR 88[rsp], r9
	lea	r9, 88[rsp]
	mov	QWORD PTR 40[rsp], r9
	call	__mingw_vsnprintf
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "1234567890\0"
.LC2:
	.ascii "snprintf_ret=%d\12\0"
.LC3:
	.ascii "snprintf_written=%d\12\0"
.LC4:
	.ascii "snprintf_truncated=%d\12\0"
.LC5:
	.ascii "strncpy_nul_terminated=%d\12\0"
.LC6:
	.ascii "strncpy_last_byte=%d\12\0"
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
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rsi, 32[rsp]
	mov	edx, 8
	lea	r8, .LC0[rip]
	mov	rcx, rsi
	lea	r9, .LC1[rip]
	call	snprintf.constprop.0
	lea	rcx, .LC2[rip]
	mov	edx, eax
	mov	ebx, eax
	call	printf
	mov	rcx, rsi
	call	strlen
	lea	rcx, .LC3[rip]
	mov	edx, eax
	call	printf
	lea	rcx, .LC4[rip]
	xor	edx, edx
	cmp	ebx, 7
	setg	dl
	call	printf
	lea	r8, 48[rsp]
	xor	edx, edx
	movabs	rax, 4050765991979987505
	mov	QWORD PTR 40[rsp], rax
	lea	rax, 40[rsp]
	mov	ecx, 1
	.p2align 4,,10
	.p2align 3
.L6:
	cmp	BYTE PTR [rax], 0
	cmove	edx, ecx
	add	rax, 1
	cmp	rax, r8
	jne	.L6
	lea	rcx, .LC5[rip]
	call	printf
	mov	edx, 56
	lea	rcx, .LC6[rip]
	call	printf
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	__mingw_vsnprintf;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
