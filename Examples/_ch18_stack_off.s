	.file	"_ch18_stack.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z5parsePKcy
	.def	_Z5parsePKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5parsePKcy
_Z5parsePKcy:
.LFB16:
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	test	rdx, rdx
	je	.L2
	xor	eax, eax
	mov	r9, rsp
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
	movsx	eax, BYTE PTR [rsp]
	add	rsp, 72
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
