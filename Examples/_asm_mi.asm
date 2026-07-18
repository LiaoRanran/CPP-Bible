	.file	"_asm_mi.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.globl	_ZN1D1fEv
	.def	_ZN1D1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1D1fEv
_ZN1D1fEv:
.LFB0:
	.seh_endprologue
	mov	DWORD PTR 16[rcx], 7
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.globl	_ZN1D1gEv
	.def	_ZN1D1gEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1D1gEv
_ZN1D1gEv:
.LFB1:
	.seh_endprologue
	mov	DWORD PTR 16[rcx], 9
	ret
	.seh_endproc
	.section	.text$_ZN1DD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1DD1Ev
	.def	_ZN1DD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1DD1Ev
_ZN1DD1Ev:
.LFB8:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTV1D[rip+64]
	movq	xmm0, QWORD PTR .LC0[rip]
	movq	xmm1, rax
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR [rcx], xmm0
	mov	rbx, rcx
	lea	rcx, 8[rcx]
	call	_ZN2B2D2Ev
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZN2B1D2Ev
	.seh_endproc
	.text
	.p2align 4
	.globl	_ZThn8_N1D1gEv
	.def	_ZThn8_N1D1gEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZThn8_N1D1gEv
_ZThn8_N1D1gEv:
.LFB10:
	.seh_endprologue
	mov	DWORD PTR 8[rcx], 9
	ret
	.seh_endproc
	.section	.text$_ZN1DD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1DD0Ev
	.def	_ZN1DD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1DD0Ev
_ZN1DD0Ev:
.LFB9:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTV1D[rip+64]
	movq	xmm0, QWORD PTR .LC0[rip]
	movq	xmm1, rax
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR [rcx], xmm0
	mov	rbx, rcx
	lea	rcx, 8[rcx]
	call	_ZN2B2D2Ev
	mov	rcx, rbx
	call	_ZN2B1D2Ev
	mov	edx, 24
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZThn8_N1DD0Ev,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZThn8_N1DD0Ev
	.def	_ZThn8_N1DD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZThn8_N1DD0Ev
_ZThn8_N1DD0Ev:
.LFB11:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTV1D[rip+64]
	movq	xmm0, QWORD PTR .LC0[rip]
	movq	xmm1, rax
	punpcklqdq	xmm0, xmm1
	lea	rbx, -8[rcx]
	movups	XMMWORD PTR -8[rcx], xmm0
	call	_ZN2B2D2Ev
	mov	rcx, rbx
	call	_ZN2B1D2Ev
	mov	edx, 24
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZThn8_N1DD1Ev,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZThn8_N1DD1Ev
	.def	_ZThn8_N1DD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZThn8_N1DD1Ev
_ZThn8_N1DD1Ev:
.LFB12:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTV1D[rip+64]
	movq	xmm0, QWORD PTR .LC0[rip]
	movq	xmm1, rax
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR -8[rcx], xmm0
	lea	rbx, -8[rcx]
	call	_ZN2B2D2Ev
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZN2B1D2Ev
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z9call_b2_gP2B2
	.def	_Z9call_b2_gP2B2;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9call_b2_gP2B2
_Z9call_b2_gP2B2:
.LFB2:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR [rax]]
	.seh_endproc
	.p2align 4
	.globl	_Z8call_d_fP1D
	.def	_Z8call_d_fP1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8call_d_fP1D
_Z8call_d_fP1D:
.LFB3:
	.seh_endprologue
	lea	rdx, _ZN1D1fEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rdx
	jne	.L11
	mov	DWORD PTR 16[rcx], 7
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	rex.W jmp	rax
	.seh_endproc
	.p2align 4
	.globl	_Z5as_b2R1D
	.def	_Z5as_b2R1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5as_b2R1D
_Z5as_b2R1D:
.LFB4:
	.seh_endprologue
	lea	rax, 8[rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6read_xP1D
	.def	_Z6read_xP1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6read_xP1D
_Z6read_xP1D:
.LFB5:
	.seh_endprologue
	mov	eax, DWORD PTR 16[rcx]
	ret
	.seh_endproc
	.globl	_ZTS2B1
	.section	.rdata$_ZTS2B1,"dr"
	.linkonce same_size
_ZTS2B1:
	.ascii "2B1\0"
	.globl	_ZTI2B1
	.section	.rdata$_ZTI2B1,"dr"
	.linkonce same_size
	.align 8
_ZTI2B1:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS2B1
	.globl	_ZTS2B2
	.section	.rdata$_ZTS2B2,"dr"
	.linkonce same_size
_ZTS2B2:
	.ascii "2B2\0"
	.globl	_ZTI2B2
	.section	.rdata$_ZTI2B2,"dr"
	.linkonce same_size
	.align 8
_ZTI2B2:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS2B2
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
	.long	2
	.quad	_ZTI2B1
	.quad	2
	.quad	_ZTI2B2
	.quad	2050
	.globl	_ZTV1D
	.section	.rdata$_ZTV1D,"dr"
	.linkonce same_size
	.align 8
_ZTV1D:
	.quad	0
	.quad	_ZTI1D
	.quad	_ZN1D1fEv
	.quad	_ZN1DD1Ev
	.quad	_ZN1DD0Ev
	.quad	_ZN1D1gEv
	.quad	-8
	.quad	_ZTI1D
	.quad	_ZThn8_N1D1gEv
	.quad	_ZThn8_N1DD1Ev
	.quad	_ZThn8_N1DD0Ev
	.section .rdata,"dr"
	.align 8
.LC0:
	.quad	_ZTV1D+16
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZN2B2D2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZN2B1D2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
