	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10add_arraysPfS_S_i
	.def	_Z10add_arraysPfS_S_i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10add_arraysPfS_S_i
_Z10add_arraysPfS_S_i:
.LFB0:
	.seh_endprologue
	test	r9d, r9d
	jle	.L1
	movsx	r9, r9d
	xor	eax, eax
	sal	r9, 2
	.p2align 4,,10
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR [rcx+rax]
	addss	xmm0, DWORD PTR [rdx+rax]
	movss	DWORD PTR [r8+rax], xmm0
	add	rax, 4
	cmp	r9, rax
	jne	.L3
.L1:
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
