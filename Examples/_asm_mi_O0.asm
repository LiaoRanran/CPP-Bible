	.file	"_asm_mi.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.globl	_ZN1D1fEv
	.def	_ZN1D1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1D1fEv
_ZN1D1fEv:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR 16[rax], 7
	nop
	pop	rbp
	ret
	.seh_endproc
	.align 2
	.globl	_ZN1D1gEv
	.def	_ZN1D1gEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1D1gEv
_ZN1D1gEv:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	DWORD PTR 16[rax], 9
	nop
	pop	rbp
	ret
	.seh_endproc
	.def	.LTHUNK0;	.scl	3;	.type	32;	.endef
	.set	.LTHUNK0,_ZN1D1gEv
	.globl	_ZThn8_N1D1gEv
	.def	_ZThn8_N1D1gEv;	.scl	2;	.type	32;	.endef
_ZThn8_N1D1gEv:
.LFB10:
	sub	rcx, 8
	jmp	.LTHUNK0
	.globl	_Z9call_b2_gP2B2
	.def	_Z9call_b2_gP2B2;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9call_b2_gP2B2
_Z9call_b2_gP2B2:
.LFB2:
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
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z8call_d_fP1D
	.def	_Z8call_d_fP1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8call_d_fP1D
_Z8call_d_fP1D:
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
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z5as_b2R1D
	.def	_Z5as_b2R1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5as_b2R1D
_Z5as_b2R1D:
.LFB4:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z6read_xP1D
	.def	_Z6read_xP1D;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6read_xP1D
_Z6read_xP1D:
.LFB5:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	eax, DWORD PTR 16[rax]
	pop	rbp
	ret
	.seh_endproc
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
	.section	.text$_ZN1DD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN1DD1Ev
	.def	_ZN1DD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1DD1Ev
_ZN1DD1Ev:
.LFB8:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV1D[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	lea	rdx, _ZTV1D[rip+64]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR 8[rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	add	rax, 8
	mov	rcx, rax
	call	_ZN2B2D2Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN2B1D2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZThn8_N1DD1Ev,"x"
	.linkonce discard
	.globl	_ZThn8_N1DD1Ev
	.def	_ZThn8_N1DD1Ev;	.scl	2;	.type	32;	.endef
_ZThn8_N1DD1Ev:
.LFB11:
	sub	rcx, 8
	jmp	_ZN1DD1Ev
	.section	.text$_ZN1DD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN1DD0Ev
	.def	_ZN1DD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1DD0Ev
_ZN1DD0Ev:
.LFB9:
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
	call	_ZN1DD1Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 24
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZThn8_N1DD0Ev,"x"
	.linkonce discard
	.globl	_ZThn8_N1DD0Ev
	.def	_ZThn8_N1DD0Ev;	.scl	2;	.type	32;	.endef
_ZThn8_N1DD0Ev:
.LFB12:
	sub	rcx, 8
	jmp	_ZN1DD0Ev
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
	.globl	_ZTS1D
	.section	.rdata$_ZTS1D,"dr"
	.linkonce same_size
_ZTS1D:
	.ascii "1D\0"
	.globl	_ZTI2B2
	.section	.rdata$_ZTI2B2,"dr"
	.linkonce same_size
	.align 8
_ZTI2B2:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS2B2
	.globl	_ZTS2B2
	.section	.rdata$_ZTS2B2,"dr"
	.linkonce same_size
_ZTS2B2:
	.ascii "2B2\0"
	.globl	_ZTI2B1
	.section	.rdata$_ZTI2B1,"dr"
	.linkonce same_size
	.align 8
_ZTI2B1:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS2B1
	.globl	_ZTS2B1
	.section	.rdata$_ZTS2B1,"dr"
	.linkonce same_size
_ZTS2B1:
	.ascii "2B1\0"
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZN2B2D2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZN2B1D2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
