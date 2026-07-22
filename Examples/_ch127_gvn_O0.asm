	.file	"_ch127_gvn.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z7computei
	.def	_Z7computei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7computei
_Z7computei:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	eax, DWORD PTR 16[rbp]
	add	eax, eax
	mov	DWORD PTR -4[rbp], eax
	mov	eax, DWORD PTR 16[rbp]
	add	eax, eax
	mov	DWORD PTR -8[rbp], eax
	mov	eax, DWORD PTR 16[rbp]
	lea	edx, 1[rax]
	mov	eax, DWORD PTR 16[rbp]
	add	eax, 1
	imul	eax, edx
	mov	DWORD PTR -12[rbp], eax
	mov	edx, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR -8[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -12[rbp]
	add	eax, edx
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z6callerv
	.def	_Z6callerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6callerv
_Z6callerv:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 7
	call	_Z7computei
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
