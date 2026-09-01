	.file	"ch05_generic_lambda.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z7twice_ii
	.def	_Z7twice_ii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7twice_ii
_Z7twice_ii:
.LFB0:
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
	.align 2
	.def	_ZZ11use_genericvENKUlT_E_clIiEEDaS_;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZZ11use_genericvENKUlT_E_clIiEEDaS_
_ZZ11use_genericvENKUlT_E_clIiEEDaS_:
.LFB5:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	mov	eax, DWORD PTR 24[rbp]
	add	eax, eax
	pop	rbp
	ret
	.seh_endproc
	.align 2
	.def	_ZZ11use_genericvENKUlT_E_clIdEEDaS_;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZZ11use_genericvENKUlT_E_clIdEEDaS_
_ZZ11use_genericvENKUlT_E_clIdEEDaS_:
.LFB6:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	movsd	QWORD PTR 24[rbp], xmm1
	movsd	xmm0, QWORD PTR 24[rbp]
	addsd	xmm0, xmm0
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z11use_genericv
	.def	_Z11use_genericv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_genericv
_Z11use_genericv:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	lea	rax, -1[rbp]
	mov	edx, 7
	mov	rcx, rax
	call	_ZZ11use_genericvENKUlT_E_clIiEEDaS_
	mov	ebx, eax
	movsd	xmm0, QWORD PTR .LC0[rip]
	lea	rax, -1[rbp]
	movapd	xmm1, xmm0
	mov	rcx, rax
	call	_ZZ11use_genericvENKUlT_E_clIdEEDaS_
	cvttsd2si	eax, xmm0
	add	eax, ebx
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB7:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	call	_Z11use_genericv
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
