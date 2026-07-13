	.file	"_ch18_stack.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z5parsePKcy
	.def	_Z5parsePKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5parsePKcy
_Z5parsePKcy:
.LFB16:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 144
	.seh_stackalloc	144
	.seh_endprologue
	mov	QWORD PTR -104[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR .refptr.__stack_chk_guard[rip]
	mov	rcx, QWORD PTR [rax]
	mov	QWORD PTR -8[rbp], rcx
	xor	ecx, ecx
	mov	QWORD PTR -88[rbp], 0
	jmp	.L2
.L4:
	mov	rdx, QWORD PTR -104[rbp]
	mov	rax, QWORD PTR -88[rbp]
	add	rax, rdx
	movzx	eax, BYTE PTR [rax]
	lea	rdx, -80[rbp]
	mov	rcx, QWORD PTR -88[rbp]
	add	rdx, rcx
	mov	BYTE PTR [rdx], al
	add	QWORD PTR -88[rbp], 1
.L2:
	mov	rax, QWORD PTR -88[rbp]
	cmp	rax, QWORD PTR 24[rbp]
	jnb	.L3
	cmp	QWORD PTR -88[rbp], 63
	jbe	.L4
.L3:
	movzx	eax, BYTE PTR -80[rbp]
	movsx	eax, al
	mov	edx, eax
	mov	rax, QWORD PTR .refptr.__stack_chk_guard[rip]
	mov	rcx, QWORD PTR -8[rbp]
	sub	rcx, QWORD PTR [rax]
	je	.L6
	call	__stack_chk_fail
.L6:
	mov	eax, edx
	add	rsp, 144
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__stack_chk_fail;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr.__stack_chk_guard, "dr"
	.globl	.refptr.__stack_chk_guard
	.linkonce	discard
.refptr.__stack_chk_guard:
	.quad	__stack_chk_guard
