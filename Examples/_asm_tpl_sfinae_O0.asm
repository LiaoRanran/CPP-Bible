	.file	"_asm_tpl_sfinae.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z10use_sfinaev
	.def	_Z10use_sfinaev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_sfinaev
_Z10use_sfinaev:
.LFB17:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	ecx, 21
	call	_Z8sfinae_fIiLi0EET_S0_
	mov	DWORD PTR -4[rbp], eax
	mov	rax, QWORD PTR .LC0[rip]
	movq	xmm0, rax
	call	_Z8sfinae_fIdLi0EET_S0_
	movq	rax, xmm0
	mov	QWORD PTR -16[rbp], rax
	movsd	xmm0, QWORD PTR -16[rbp]
	cvttsd2si	eax, xmm0
	mov	edx, DWORD PTR -4[rbp]
	add	eax, edx
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z8sfinae_fIiLi0EET_S0_,"x"
	.linkonce discard
	.globl	_Z8sfinae_fIiLi0EET_S0_
	.def	_Z8sfinae_fIiLi0EET_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sfinae_fIiLi0EET_S0_
_Z8sfinae_fIiLi0EET_S0_:
.LFB18:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	eax, DWORD PTR 16[rbp]
	add	eax, eax
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z8sfinae_fIdLi0EET_S0_,"x"
	.linkonce discard
	.globl	_Z8sfinae_fIdLi0EET_S0_
	.def	_Z8sfinae_fIdLi0EET_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sfinae_fIdLi0EET_S0_
_Z8sfinae_fIdLi0EET_S0_:
.LFB19:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	movsd	QWORD PTR 16[rbp], xmm0
	movsd	xmm0, QWORD PTR 16[rbp]
	movq	rax, xmm0
	movq	xmm0, rax
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
