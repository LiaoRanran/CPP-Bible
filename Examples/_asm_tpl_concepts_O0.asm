	.file	"_asm_tpl_concepts.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z12use_conceptsv
	.def	_Z12use_conceptsv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_conceptsv
_Z12use_conceptsv:
.LFB21:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	ecx, 21
	call	_Z9concept_fIiET_S0_
	mov	DWORD PTR -4[rbp], eax
	mov	rax, QWORD PTR .LC0[rip]
	movq	xmm0, rax
	call	_Z9concept_fIdET_S0_
	movq	rax, xmm0
	mov	QWORD PTR -16[rbp], rax
	mov	ecx, 7
	call	_Z9add_twiceIiET_S0_
	mov	DWORD PTR -20[rbp], eax
	movsd	xmm0, QWORD PTR -16[rbp]
	cvttsd2si	eax, xmm0
	mov	edx, DWORD PTR -4[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -20[rbp]
	add	eax, edx
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z9concept_fIiET_S0_,"x"
	.linkonce discard
	.globl	_Z9concept_fIiET_S0_
	.def	_Z9concept_fIiET_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9concept_fIiET_S0_
_Z9concept_fIiET_S0_:
.LFB22:
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
	.section	.text$_Z9concept_fIdET_S0_,"x"
	.linkonce discard
	.globl	_Z9concept_fIdET_S0_
	.def	_Z9concept_fIdET_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9concept_fIdET_S0_
_Z9concept_fIdET_S0_:
.LFB23:
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
	.section	.text$_Z9add_twiceIiET_S0_,"x"
	.linkonce discard
	.globl	_Z9add_twiceIiET_S0_
	.def	_Z9add_twiceIiET_S0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9add_twiceIiET_S0_
_Z9add_twiceIiET_S0_:
.LFB24:
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
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
