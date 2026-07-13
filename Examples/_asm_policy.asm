	.file	"_asm_policy.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN4VNew4makeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN4VNew4makeEv
	.def	_ZN4VNew4makeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4VNew4makeEv
_ZN4VNew4makeEv:
.LFB49:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 4
	call	_Znwy
	mov	DWORD PTR [rax], 0
	add	rsp, 40
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z10use_policyv
	.def	_Z10use_policyv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_policyv
_Z10use_policyv:
.LFB50:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 4
	call	malloc
	mov	rbx, rax
	mov	rcx, rax
	call	free
	cmp	rbx, 1
	mov	eax, 1
	sbb	eax, -1
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11use_virtualR5VBase
	.def	_Z11use_virtualR5VBase;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_virtualR5VBase
_Z11use_virtualR5VBase:
.LFB51:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rdx, _ZN4VNew4makeEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rdx
	jne	.L5
	mov	ecx, 4
	call	_Znwy
	test	rax, rax
	setne	al
	movzx	eax, al
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	call	rax
	test	rax, rax
	setne	al
	movzx	eax, al
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
