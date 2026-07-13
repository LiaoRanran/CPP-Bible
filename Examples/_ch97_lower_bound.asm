	.file	"_ch97_lower_bound.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z15lower_bound_idxPKiii
	.def	_Z15lower_bound_idxPKiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15lower_bound_idxPKiii
_Z15lower_bound_idxPKiii:
.LFB1544:
	.seh_endprologue
	movsx	rdx, edx
	mov	rax, rcx
	.p2align 4,,10
	.p2align 3
.L3:
	test	rdx, rdx
	jle	.L7
.L4:
	mov	r9, rdx
	sar	r9
	lea	r10, [rax+r9*4]
	cmp	DWORD PTR [r10], r8d
	jge	.L5
	lea	rax, 4[r10]
	sub	rdx, r9
	sub	rdx, 1
	test	rdx, rdx
	jg	.L4
.L7:
	sub	rax, rcx
	sar	rax, 2
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	mov	rdx, r9
	jmp	.L3
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
