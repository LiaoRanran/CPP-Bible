	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK7CircleV4areaEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK7CircleV4areaEv
	.def	_ZNK7CircleV4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7CircleV4areaEv
_ZNK7CircleV4areaEv:
.LFB10:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	movsd	xmm1, QWORD PTR 8[rcx]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z9process_vRK6ShapeV
	.def	_Z9process_vRK6ShapeV;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9process_vRK6ShapeV
_Z9process_vRK6ShapeV:
.LFB16:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rdx, _ZNK7CircleV4areaEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rdx
	jne	.L4
	movsd	xmm1, QWORD PTR 8[rcx]
	movsd	xmm0, QWORD PTR .LC0[rip]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	addsd	xmm0, xmm0
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	call	rax
	addsd	xmm0, xmm0
	add	rsp, 40
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9process_cRK6ShapeCI7CircleCE
	.def	_Z9process_cRK6ShapeCI7CircleCE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9process_cRK6ShapeCI7CircleCE
_Z9process_cRK6ShapeCI7CircleCE:
.LFB17:
	.seh_endprologue
	movsd	xmm0, QWORD PTR .LC0[rip]
	movsd	xmm1, QWORD PTR [rcx]
	mulsd	xmm0, xmm1
	mulsd	xmm0, xmm1
	addsd	xmm0, xmm0
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1413754136
	.long	1074340347
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
