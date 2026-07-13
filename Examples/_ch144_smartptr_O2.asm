	.file	"_ch144_smartptr.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4openi
	.def	_Z4openi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4openi
_Z4openi:
.LFB3514:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 4
	mov	esi, edx
	call	_Znwy
	mov	DWORD PTR [rax], esi
	mov	QWORD PTR [rbx], rax
	mov	rax, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8transferv
	.def	_Z8transferv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8transferv
_Z8transferv:
.LFB3515:
	.seh_endprologue
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
