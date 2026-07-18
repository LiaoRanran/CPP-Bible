	.file	"ch08_expected_test.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "empty\0"
.LC1:
	.ascii "not digit\0"
	.text
	.p2align 4
	.globl	_Z11parse_digitPKc
	.def	_Z11parse_digitPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11parse_digitPKc
_Z11parse_digitPKc:
.LFB273:
	.seh_endprologue
	mov	rax, rcx
	test	rdx, rdx
	je	.L2
	movsx	edx, BYTE PTR [rdx]
	test	dl, dl
	jne	.L3
.L2:
	lea	rcx, .LC0[rip]
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR [rax], rcx
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	lea	ecx, -48[rdx]
	cmp	cl, 9
	jbe	.L5
	lea	rcx, .LC1[rip]
	mov	QWORD PTR 8[rax], 0
	mov	QWORD PTR [rax], rcx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	sub	edx, 48
	mov	BYTE PTR 8[rax], 1
	mov	DWORD PTR [rax], edx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "7\0"
.LC3:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB288:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rcx, 32[rsp]
	lea	rdx, .LC2[rip]
	call	_Z11parse_digitPKc
	cmp	BYTE PTR 40[rsp], 0
	je	.L11
	mov	edx, DWORD PTR 32[rsp]
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	xor	eax, eax
.L12:
	add	rsp, 56
	ret
.L11:
	mov	edx, -1
	lea	rcx, .LC3[rip]
	call	__mingw_printf
	mov	eax, 1
	jmp	.L12
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
