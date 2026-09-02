	.file	"_ch83_map_find.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6lookupRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi
	.def	_Z6lookupRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6lookupRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi
_Z6lookupRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi:
.LFB1251:
	.seh_endprologue
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	je	.L5
	add	rcx, 8
	mov	r10, rcx
	jmp	.L4
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L12:
	mov	rax, r9
	test	rax, rax
	je	.L11
.L4:
	mov	r8, QWORD PTR 16[rax]
	mov	r9, QWORD PTR 24[rax]
	cmp	DWORD PTR 32[rax], edx
	jl	.L12
	mov	r10, rax
	mov	rax, r8
	test	rax, rax
	jne	.L4
.L11:
	mov	eax, -1
	cmp	rcx, r10
	je	.L1
	cmp	DWORD PTR 32[r10], edx
	jle	.L13
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L13:
	mov	eax, DWORD PTR 36[r10]
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	mov	eax, -1
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
