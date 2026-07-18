	.file	"_ch97_lower_bound.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z15lower_bound_idxPKiii
	.def	_Z15lower_bound_idxPKiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15lower_bound_idxPKiii
_Z15lower_bound_idxPKiii:
.LFB1516:
	.seh_endprologue
	movsxd	rdx, edx
	mov	rax, rcx
	.p2align 4
	.p2align 3
.L3:
	test	rdx, rdx
	jle	.L7
.L4:
	mov	r9, rdx
	sar	r9
	cmp	DWORD PTR [rax+r9*4], r8d
	jge	.L5
	sub	rdx, r9
	lea	rax, 4[rax+r9*4]
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
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
