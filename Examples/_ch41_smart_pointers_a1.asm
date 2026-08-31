	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z14raw_new_deleteiii
	.def	_Z14raw_new_deleteiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14raw_new_deleteiii
_Z14raw_new_deleteiii:
.LFB3485:
	.seh_endprologue
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15unique_ptr_testiii
	.def	_Z15unique_ptr_testiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15unique_ptr_testiii
_Z15unique_ptr_testiii:
.LFB3486:
	.seh_endprologue
	add	ecx, edx
	lea	eax, [rcx+r8]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9make_dataiii
	.def	_Z9make_dataiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9make_dataiii
_Z9make_dataiii:
.LFB3533:
	.seh_endprologue
	mov	rax, rcx
	movd	xmm0, edx
	movd	xmm1, r8d
	mov	DWORD PTR 8[rcx], r9d
	punpckldq	xmm0, xmm1
	movq	QWORD PTR [rcx], xmm0
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z18unique_ptr_factoryiii
	.def	_Z18unique_ptr_factoryiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18unique_ptr_factoryiii
_Z18unique_ptr_factoryiii:
.LFB3542:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rbx, rcx
	movd	xmm6, edx
	movd	xmm0, r8d
	mov	ecx, 12
	punpckldq	xmm6, xmm0
	mov	esi, r9d
	call	_Znwy
	movq	QWORD PTR [rax], xmm6
	mov	DWORD PTR 8[rax], esi
	mov	QWORD PTR [rbx], rax
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	rax, rbx
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
