	.file	"_asm_tpl_concepts.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12use_conceptsv
	.def	_Z12use_conceptsv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_conceptsv
_Z12use_conceptsv:
.LFB21:
	sub	rsp, 24
	.seh_stackalloc	24
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	mov	DWORD PTR [rsp], 42
	movsd	QWORD PTR 8[rsp], xmm0
	mov	DWORD PTR 4[rsp], 14
	movsd	xmm0, QWORD PTR 8[rsp]
	mov	ecx, DWORD PTR [rsp]
	cvttsd2si	eax, xmm0
	mov	edx, DWORD PTR 4[rsp]
	add	eax, ecx
	add	eax, edx
	add	rsp, 24
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
