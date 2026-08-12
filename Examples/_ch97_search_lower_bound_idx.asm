	.file	"_ch97_search_lower_bound_idx.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z15lower_bound_idxPKiii
	.def	_Z15lower_bound_idxPKiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15lower_bound_idxPKiii
_Z15lower_bound_idxPKiii:
.LFB0:
	.seh_endprologue
	mov	rax, rcx
	jmp	.L3
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L4:
	mov	r9d, edx
	sar	r9d
	movsxd	r10, r9d
	cmp	DWORD PTR [rax+r10*4], r8d
	jl	.L7
	mov	edx, r9d
.L3:
	test	edx, edx
	jg	.L4
	sub	rax, rcx
	sar	rax, 2
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	add	r9d, 1
	lea	rax, 4[rax+r10*4]
	sub	edx, r9d
	jmp	.L3
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
