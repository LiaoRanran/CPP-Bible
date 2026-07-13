	.file	"_ch17_callconv.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4sum6llllll
	.def	_Z4sum6llllll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4sum6llllll
_Z4sum6llllll:
.LFB0:
	.seh_endprologue
	add	ecx, edx
	add	ecx, r8d
	lea	eax, [rcx+r9]
	add	eax, DWORD PTR 40[rsp]
	add	eax, DWORD PTR 48[rsp]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9manhattan5Point
	.def	_Z9manhattan5Point;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9manhattan5Point
_Z9manhattan5Point:
.LFB1:
	.seh_endprologue
	mov	rax, rcx
	shr	rax, 32
	add	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10make_pointll
	.def	_Z10make_pointll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10make_pointll
_Z10make_pointll:
.LFB2:
	.seh_endprologue
	movd	xmm0, ecx
	movd	xmm1, edx
	punpckldq	xmm0, xmm1
	movq	rax, xmm0
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 44[rsp], 21
	mov	eax, DWORD PTR 44[rsp]
	add	eax, 30
	mov	DWORD PTR 44[rsp], eax
	mov	eax, DWORD PTR 44[rsp]
	add	eax, 15
	mov	DWORD PTR 44[rsp], eax
	mov	eax, DWORD PTR 44[rsp]
	add	rsp, 56
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
