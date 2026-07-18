	.file	"ch50_vi_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN1D1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1D1fEv
	.def	_ZN1D1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1D1fEv
_ZN1D1fEv:
.LFB25:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rdx, QWORD PTR -24[rax]
	mov	eax, DWORD PTR 8[rcx]
	add	eax, DWORD PTR 8[rcx+rdx]
	ret
	.seh_endproc
	.section	.text$_ZTv0_n24_N1D1fEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZTv0_n24_N1D1fEv
	.def	_ZTv0_n24_N1D1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZTv0_n24_N1D1fEv
_ZTv0_n24_N1D1fEv:
.LFB35:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	add	rcx, QWORD PTR -24[rax]
	mov	rax, QWORD PTR [rcx]
	mov	rdx, QWORD PTR -24[rax]
	mov	eax, DWORD PTR 8[rcx]
	add	eax, DWORD PTR 8[rcx+rdx]
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z5callDP1D
	.def	_Z5callDP1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5callDP1D
_Z5callDP1D:
.LFB26:
	.seh_endprologue
	lea	r8, _ZN1D1fEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rdx, QWORD PTR [rax]
	cmp	rdx, r8
	jne	.L9
	mov	rdx, QWORD PTR -24[rax]
	mov	eax, DWORD PTR 8[rcx]
	add	eax, DWORD PTR 8[rcx+rdx]
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	rex.W jmp	rdx
	.seh_endproc
	.p2align 4
	.globl	_Z5callBP1B
	.def	_Z5callBP1B;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5callBP1B
_Z5callBP1B:
.LFB27:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR [rax]]
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB28:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	call	__main
	lea	rax, _ZTV1D[rip+24]
	lea	rcx, 32[rsp]
	mov	DWORD PTR 56[rsp], 100
	mov	QWORD PTR 32[rsp], rax
	add	rax, 32
	mov	QWORD PTR 48[rsp], rax
	mov	DWORD PTR 40[rsp], 7
	call	_Z5callDP1D
	lea	rcx, 48[rsp]
	mov	ebx, eax
	call	_Z5callBP1B
	lea	rcx, .LC0[rip]
	lea	edx, [rbx+rax]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 64
	pop	rbx
	ret
	.seh_endproc
	.globl	_ZTS1B
	.section	.rdata$_ZTS1B,"dr"
	.linkonce same_size
_ZTS1B:
	.ascii "1B\0"
	.globl	_ZTI1B
	.section	.rdata$_ZTI1B,"dr"
	.linkonce same_size
	.align 8
_ZTI1B:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS1B
	.globl	_ZTS1D
	.section	.rdata$_ZTS1D,"dr"
	.linkonce same_size
_ZTS1D:
	.ascii "1D\0"
	.globl	_ZTI1D
	.section	.rdata$_ZTI1D,"dr"
	.linkonce same_size
	.align 8
_ZTI1D:
	.quad	_ZTVN10__cxxabiv121__vmi_class_type_infoE+16
	.quad	_ZTS1D
	.long	0
	.long	1
	.quad	_ZTI1B
	.quad	-6141
	.globl	_ZTT1D
	.section	.rdata$_ZTT1D,"dr"
	.linkonce same_size
	.align 8
_ZTT1D:
	.quad	_ZTV1D+24
	.quad	_ZTV1D+56
	.globl	_ZTV1D
	.section	.rdata$_ZTV1D,"dr"
	.linkonce same_size
	.align 8
_ZTV1D:
	.quad	16
	.quad	0
	.quad	_ZTI1D
	.quad	_ZN1D1fEv
	.quad	-16
	.quad	-16
	.quad	_ZTI1D
	.quad	_ZTv0_n24_N1D1fEv
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
