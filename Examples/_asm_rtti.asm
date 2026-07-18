	.file	"_asm_rtti.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK3Der1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK3Der1fEv
	.def	_ZNK3Der1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3Der1fEv
_ZNK3Der1fEv:
.LFB40:
	.seh_endprologue
	mov	eax, 2
	ret
	.seh_endproc
	.section	.text$_ZN3DerD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DerD1Ev
	.def	_ZN3DerD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DerD1Ev
_ZN3DerD1Ev:
.LFB57:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN3DerD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3DerD0Ev
	.def	_ZN3DerD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3DerD0Ev
_ZN3DerD0Ev:
.LFB58:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z8get_nameRK4Base
	.def	_Z8get_nameRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8get_nameRK4Base
_Z8get_nameRK4Base:
.LFB41:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -8[rax]
	mov	rax, QWORD PTR 8[rax]
	cmp	BYTE PTR [rax], 42
	sete	dl
	add	rax, rdx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9down_castPK4Base
	.def	_Z9down_castPK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9down_castPK4Base
_Z9down_castPK4Base:
.LFB42:
	.seh_endprologue
	test	rcx, rcx
	je	.L8
	xor	r9d, r9d
	lea	r8, _ZTI3Der[rip]
	lea	rdx, _ZTI4Base[rip]
	jmp	__dynamic_cast
	.p2align 4,,10
	.p2align 3
.L8:
	xor	eax, eax
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.globl	_Z13down_cast_refRK4Base
	.def	_Z13down_cast_refRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13down_cast_refRK4Base
_Z13down_cast_refRK4Base:
.LFB43:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	xor	r9d, r9d
	lea	r8, _ZTI3Der[rip]
	lea	rdx, _ZTI4Base[rip]
	call	__dynamic_cast
	test	rax, rax
	je	.L10
	add	rsp, 40
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z13down_cast_refRK4Base.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13down_cast_refRK4Base.cold
	.seh_stackalloc	40
	.seh_endprologue
_Z13down_cast_refRK4Base.cold:
.L10:
	call	__cxa_bad_cast
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.section .rdata,"dr"
.LC1:
	.ascii "%s\12\0"
.LC2:
	.ascii "ok %d\12\0"
.LC3:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB44:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	lea	rax, _ZTV3Der[rip+16]
	lea	rcx, .LC1[rip]
	mov	QWORD PTR 40[rsp], rax
	mov	rax, QWORD PTR _ZTV3Der[rip+8]
	mov	rdx, QWORD PTR 8[rax]
	xor	eax, eax
	cmp	BYTE PTR [rdx], 42
	sete	al
	add	rdx, rax
	call	__mingw_printf
	lea	rcx, 40[rsp]
	call	_Z9down_castPK4Base
	test	rax, rax
	je	.L14
	mov	rdx, QWORD PTR [rax]
	mov	rcx, rax
	call	[QWORD PTR 16[rdx]]
	lea	rcx, .LC2[rip]
	mov	edx, eax
	call	__mingw_printf
.L14:
	lea	rcx, 40[rsp]
	call	_Z13down_cast_refRK4Base
	mov	rdx, QWORD PTR [rax]
	mov	rcx, rax
	call	[QWORD PTR 16[rdx]]
	lea	rcx, .LC3[rip]
	mov	edx, eax
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.globl	_ZTS4Base
	.section	.rdata$_ZTS4Base,"dr"
	.linkonce same_size
_ZTS4Base:
	.ascii "4Base\0"
	.globl	_ZTI4Base
	.section	.rdata$_ZTI4Base,"dr"
	.linkonce same_size
	.align 8
_ZTI4Base:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS4Base
	.globl	_ZTS3Der
	.section	.rdata$_ZTS3Der,"dr"
	.linkonce same_size
_ZTS3Der:
	.ascii "3Der\0"
	.globl	_ZTI3Der
	.section	.rdata$_ZTI3Der,"dr"
	.linkonce same_size
	.align 8
_ZTI3Der:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS3Der
	.quad	_ZTI4Base
	.globl	_ZTV3Der
	.section	.rdata$_ZTV3Der,"dr"
	.linkonce same_size
	.align 8
_ZTV3Der:
	.quad	0
	.quad	_ZTI3Der
	.quad	_ZN3DerD1Ev
	.quad	_ZN3DerD0Ev
	.quad	_ZNK3Der1fEv
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__dynamic_cast;	.scl	2;	.type	32;	.endef
	.def	__cxa_bad_cast;	.scl	2;	.type	32;	.endef
