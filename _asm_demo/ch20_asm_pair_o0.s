	.file	"ch20_asm_pair_gcc15.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z6by_refRi
	.def	_Z6by_refRi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6by_refRi
_Z6by_refRi:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	eax, DWORD PTR [rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], edx
	nop
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z6by_ptrPi
	.def	_Z6by_ptrPi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6by_ptrPi
_Z6by_ptrPi:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	cmp	QWORD PTR 16[rbp], 0
	je	.L4
	mov	rax, QWORD PTR 16[rbp]
	mov	eax, DWORD PTR [rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR [rax], edx
.L4:
	nop
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z5firstRiS_
	.def	_Z5firstRiS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5firstRiS_
_Z5firstRiS_:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
