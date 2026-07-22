	.file	"_ch127_inline.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z12add_noinlineii
	.def	_Z12add_noinlineii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12add_noinlineii
_Z12add_noinlineii:
.LFB21:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, DWORD PTR 24[rbp]
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z10add_inlineii,"x"
	.linkonce discard
	.globl	_Z10add_inlineii
	.def	_Z10add_inlineii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10add_inlineii
_Z10add_inlineii:
.LFB22:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR 24[rbp], edx
	mov	edx, DWORD PTR 16[rbp]
	mov	eax, DWORD PTR 24[rbp]
	add	eax, edx
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z11use_inlinedv
	.def	_Z11use_inlinedv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_inlinedv
_Z11use_inlinedv:
.LFB23:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 0
	mov	DWORD PTR -8[rbp], 0
	jmp	.L6
.L7:
	mov	eax, DWORD PTR -8[rbp]
	mov	edx, 1
	mov	ecx, eax
	call	_Z10add_inlineii
	add	DWORD PTR -4[rbp], eax
	add	DWORD PTR -8[rbp], 1
.L6:
	cmp	DWORD PTR -8[rbp], 3
	jle	.L7
	mov	eax, DWORD PTR -4[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z12use_noinlinev
	.def	_Z12use_noinlinev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_noinlinev
_Z12use_noinlinev:
.LFB24:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	edx, 4
	mov	ecx, 3
	call	_Z12add_noinlineii
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%d %d\12\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB25:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	__main
	call	_Z12use_noinlinev
	mov	ebx, eax
	call	_Z11use_inlinedv
	mov	edx, eax
	lea	rax, .LC0[rip]
	mov	r8d, ebx
	mov	rcx, rax
	call	__mingw_printf
	mov	eax, 0
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
