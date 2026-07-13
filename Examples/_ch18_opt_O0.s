	.file	"_ch18_opt.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z3addii
	.def	_Z3addii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3addii
_Z3addii:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, DWORD PTR 24[rbp]
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z4mul3i
	.def	_Z4mul3i;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4mul3i
_Z4mul3i:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, edx
	add	eax, eax
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z6callerv
	.def	_Z6callerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6callerv
_Z6callerv:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	mov	edx, 5
	mov	ecx, 4
	call	_Z3addii
	mov	ebx, eax
	mov	ecx, 2
	call	_Z4mul3i
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z7sum_arrPKii
	.def	_Z7sum_arrPKii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7sum_arrPKii
_Z7sum_arrPKii:
.LFB3:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	mov	DWORD PTR -4[rbp], 0
	mov	DWORD PTR -8[rbp], 0
	jmp	.L8
.L9:
	mov	eax, DWORD PTR -8[rbp]
	cdqe
	lea	rdx, 0[0+rax*4]
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	mov	eax, DWORD PTR [rax]
	add	DWORD PTR -4[rbp], eax
	add	DWORD PTR -8[rbp], 1
.L8:
	mov	eax, DWORD PTR -8[rbp]
	cmp	eax, DWORD PTR 24[rbp]
	jl	.L9
	mov	eax, DWORD PTR -4[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
