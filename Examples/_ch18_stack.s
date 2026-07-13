	.file	"_ch18_stack.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z5parsePKcy
	.def	_Z5parsePKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5parsePKcy
_Z5parsePKcy:
.LFB16:
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	mov	r10, QWORD PTR .refptr.__stack_chk_guard[rip]
	mov	rax, QWORD PTR [r10]
	mov	QWORD PTR 104[rsp], rax
	xor	eax, eax
	test	rdx, rdx
	je	.L2
	lea	r9, 32[rsp]
	.p2align 4,,10
	.p2align 3
.L3:
	movzx	r8d, BYTE PTR [rcx+rax]
	mov	BYTE PTR [r9+rax], r8b
	add	rax, 1
	cmp	rax, rdx
	jnb	.L2
	cmp	rax, 63
	jbe	.L3
.L2:
	mov	rdx, QWORD PTR 104[rsp]
	sub	rdx, QWORD PTR [r10]
	movsx	eax, BYTE PTR 32[rsp]
	jne	.L14
	add	rsp, 120
	ret
.L14:
	call	__stack_chk_fail
	nop
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__stack_chk_fail;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr.__stack_chk_guard, "dr"
	.globl	.refptr.__stack_chk_guard
	.linkonce	discard
.refptr.__stack_chk_guard:
	.quad	__stack_chk_guard
