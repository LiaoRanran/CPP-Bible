	.file	"_ch143_novirtual.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z11sum_virtualRK5Shape
	.def	_Z11sum_virtualRK5Shape;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11sum_virtualRK5Shape
_Z11sum_virtualRK5Shape:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK7Circle24areaEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK7Circle24areaEv
	.def	_ZNK7Circle24areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7Circle24areaEv
_ZNK7Circle24areaEv:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	movss	xmm1, DWORD PTR [rax]
	movss	xmm0, DWORD PTR .LC0[rip]
	mulss	xmm1, xmm0
	mov	rax, QWORD PTR 16[rbp]
	movss	xmm0, DWORD PTR [rax]
	mulss	xmm0, xmm1
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z10sum_staticRK7Circle2
	.def	_Z10sum_staticRK7Circle2;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sum_staticRK7Circle2
_Z10sum_staticRK7Circle2:
.LFB3:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNK7Circle24areaEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1078530000
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
