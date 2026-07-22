	.file	"_asm_ranges.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10use_rangesv
	.def	_Z10use_rangesv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_rangesv
_Z10use_rangesv:
.LFB3988:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 24
	call	_Znwy
	movabs	rdx, 17179869187
	mov	r9, rax
	movabs	rax, 8589934593
	mov	QWORD PTR [r9], rax
	lea	r8, 24[r9]
	movabs	rax, 25769803781
	mov	QWORD PTR 16[r9], rax
	mov	rax, r9
	mov	QWORD PTR 8[r9], rdx
	jmp	.L3
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L14:
	add	rax, 4
	cmp	rax, r8
	je	.L13
.L3:
	mov	edx, DWORD PTR [rax]
	mov	rcx, rax
	test	dl, 1
	jne	.L14
	xor	ebx, ebx
	cmp	rax, r8
	je	.L4
	.p2align 4
	.p2align 3
.L7:
	imul	edx, edx
	lea	rax, 4[rcx]
	add	ebx, edx
	cmp	r8, rax
	jne	.L6
	jmp	.L4
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L15:
	add	rax, 4
	cmp	r8, rax
	je	.L4
.L6:
	mov	edx, DWORD PTR [rax]
	mov	rcx, rax
	test	dl, 1
	jne	.L15
	cmp	r8, rax
	jne	.L7
.L4:
	mov	edx, 24
	mov	rcx, r9
	call	_ZdlPvy
	mov	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
.L13:
	xor	ebx, ebx
	jmp	.L4
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
