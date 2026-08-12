	.file	"_ch90_view_asm.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8sum_evenRKSt6vectorIiSaIiEE
	.def	_Z8sum_evenRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sum_evenRKSt6vectorIiSaIiEE
_Z8sum_evenRKSt6vectorIiSaIiEE:
.LFB5521:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rcx]
	cmp	r8, rcx
	jne	.L4
	jmp	.L8
	.p2align 4
	.p2align 4,,10
	.p2align 3
.L14:
	add	rcx, 4
	cmp	r8, rcx
	je	.L8
.L4:
	mov	edx, DWORD PTR [rcx]
	test	dl, 1
	jne	.L14
	xor	r9d, r9d
	cmp	r8, rcx
	je	.L1
	.p2align 4
	.p2align 3
.L7:
	lea	rax, 4[rcx]
	add	r9d, edx
	cmp	r8, rax
	jne	.L6
	jmp	.L1
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L15:
	add	rax, 4
	cmp	r8, rax
	je	.L1
.L6:
	mov	edx, DWORD PTR [rax]
	mov	rcx, rax
	test	dl, 1
	jne	.L15
	cmp	rax, r8
	jne	.L7
.L1:
	mov	eax, r9d
	ret
.L8:
	xor	r9d, r9d
	mov	eax, r9d
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5599:
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	call	__main
	mov	ecx, 20
	call	_Znwy
	lea	rcx, 48[rsp]
	movabs	rdx, 17179869187
	mov	r10, rax
	mov	QWORD PTR 48[rsp], rax
	movabs	rax, 8589934593
	mov	QWORD PTR [r10], rax
	lea	rax, 20[r10]
	mov	QWORD PTR 8[r10], rdx
	mov	DWORD PTR 16[r10], 5
	mov	QWORD PTR 56[rsp], rax
	call	_Z8sum_evenRKSt6vectorIiSaIiEE
	mov	edx, 20
	mov	rcx, r10
	mov	DWORD PTR 44[rsp], eax
	call	_ZdlPvy
	mov	eax, DWORD PTR 44[rsp]
	add	rsp, 88
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
