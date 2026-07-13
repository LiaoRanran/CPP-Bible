	.file	"_ch143_novirtual.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK6Circle4areaEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK6Circle4areaEv
	.def	_ZNK6Circle4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK6Circle4areaEv
_ZNK6Circle4areaEv:
.LFB0:
	.seh_endprologue
	movss	xmm0, DWORD PTR .LC0[rip]
	movss	xmm1, DWORD PTR 8[rcx]
	mulss	xmm0, xmm1
	mulss	xmm0, xmm1
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11sum_virtualRK5Shape
	.def	_Z11sum_virtualRK5Shape;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11sum_virtualRK5Shape
_Z11sum_virtualRK5Shape:
.LFB1:
	.seh_endprologue
	lea	rdx, _ZNK6Circle4areaEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rdx
	jne	.L8
	movss	xmm1, DWORD PTR 8[rcx]
	movss	xmm0, DWORD PTR .LC0[rip]
	mulss	xmm0, xmm1
	mulss	xmm0, xmm1
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	rex.W jmp	rax
	.seh_endproc
	.p2align 4
	.globl	_Z10sum_staticRK7Circle2
	.def	_Z10sum_staticRK7Circle2;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sum_staticRK7Circle2
_Z10sum_staticRK7Circle2:
.LFB3:
	.seh_endprologue
	movss	xmm0, DWORD PTR .LC0[rip]
	movss	xmm1, DWORD PTR [rcx]
	mulss	xmm0, xmm1
	mulss	xmm0, xmm1
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1078530000
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
