	.file	"_ch147_smartptr.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8make_badv
	.def	_Z8make_badv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8make_badv
_Z8make_badv:
.LFB3485:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 4
	call	_Znwy
	mov	DWORD PTR [rax], 0
	add	rsp, 40
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9make_goodv
	.def	_Z9make_goodv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9make_goodv
_Z9make_goodv:
.LFB3497:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 4
	call	_Znwy
	mov	DWORD PTR [rax], 0
	mov	QWORD PTR [rbx], rax
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
