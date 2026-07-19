	.file	"ch09_contracts_test.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z5clampiii
	.def	_Z5clampiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5clampiii
_Z5clampiii:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	mov	DWORD PTR 32[rbp], ecx
	mov	DWORD PTR 40[rbp], edx
	mov	DWORD PTR 48[rbp], r8d
	mov	ecx, DWORD PTR 48[rbp]
	mov	edx, DWORD PTR 40[rbp]
	mov	eax, DWORD PTR 32[rbp]
	mov	r8d, ecx
	mov	ecx, eax
	call	_Z5clampiii.pre
	mov	eax, DWORD PTR 32[rbp]
	cmp	eax, DWORD PTR 40[rbp]
	jge	.L2
	mov	ebx, DWORD PTR 40[rbp]
	jmp	.L3
.L2:
	mov	eax, DWORD PTR 32[rbp]
	cmp	eax, DWORD PTR 48[rbp]
	jle	.L4
	mov	ebx, DWORD PTR 48[rbp]
	jmp	.L3
.L4:
	mov	ebx, DWORD PTR 32[rbp]
.L3:
	mov	ecx, DWORD PTR 48[rbp]
	mov	edx, DWORD PTR 40[rbp]
	mov	eax, DWORD PTR 32[rbp]
	mov	r9d, ebx
	mov	r8d, ecx
	mov	ecx, eax
	call	_Z5clampiiii.post
	mov	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "_asm_demo/ch09_contracts_test.cpp\0"
.LC1:
	.ascii "clamp\0"
.LC2:
	.ascii "lo <= hi\0"
.LC3:
	.ascii "default\0"
	.text
	.def	_Z5clampiii.pre;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5clampiii.pre
_Z5clampiii.pre:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	DWORD PTR 32[rbp], r8d
	mov	eax, DWORD PTR 24[rbp]
	cmp	eax, DWORD PTR 32[rbp]
	jle	.L6
	lea	rax, .LC0[rip]
	mov	QWORD PTR -48[rbp], rax
	lea	rax, .LC1[rip]
	mov	QWORD PTR -40[rbp], rax
	lea	rax, .LC2[rip]
	mov	QWORD PTR -32[rbp], rax
	lea	rax, .LC3[rip]
	mov	QWORD PTR -24[rbp], rax
	lea	rax, .LC3[rip]
	mov	QWORD PTR -16[rbp], rax
	mov	DWORD PTR -8[rbp], 4
	mov	BYTE PTR -4[rbp], 0
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_Z25handle_contract_violationRKNSt12experimental18contract_violationE
	call	_ZSt9terminatev
	nop
.L6:
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC4:
	.ascii "r >= lo && r <= hi\0"
	.text
	.def	_Z5clampiiii.post;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5clampiiii.post
_Z5clampiiii.post:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 80
	.seh_stackalloc	80
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	DWORD PTR 32[rbp], r8d
	mov	DWORD PTR 40[rbp], r9d
	mov	eax, DWORD PTR 40[rbp]
	cmp	eax, DWORD PTR 24[rbp]
	jl	.L9
	mov	eax, DWORD PTR 40[rbp]
	cmp	eax, DWORD PTR 32[rbp]
	jle	.L11
.L9:
	lea	rax, .LC0[rip]
	mov	QWORD PTR -48[rbp], rax
	lea	rax, .LC1[rip]
	mov	QWORD PTR -40[rbp], rax
	lea	rax, .LC4[rip]
	mov	QWORD PTR -32[rbp], rax
	lea	rax, .LC3[rip]
	mov	QWORD PTR -24[rbp], rax
	lea	rax, .LC3[rip]
	mov	QWORD PTR -16[rbp], rax
	mov	DWORD PTR -8[rbp], 5
	mov	BYTE PTR -4[rbp], 0
	lea	rax, -48[rbp]
	mov	rcx, rax
	call	_Z25handle_contract_violationRKNSt12experimental18contract_violationE
	call	_ZSt9terminatev
.L11:
	nop
	add	rsp, 80
	pop	rbp
	ret
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	mov	r8d, 10
	mov	edx, 0
	mov	ecx, 5
	call	_Z5clampiii
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Z25handle_contract_violationRKNSt12experimental18contract_violationE;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
