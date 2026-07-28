	.file	"_ch47_d4_vtable.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK4Base1gEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4Base1gEv
	.def	_ZNK4Base1gEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4Base1gEv
_ZNK4Base1gEv:
.LFB1:
	.seh_endprologue
	mov	eax, 2
	ret
	.seh_endproc
	.section	.text$_ZNK7Derived1fEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK7Derived1fEv
	.def	_ZNK7Derived1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7Derived1fEv
_ZNK7Derived1fEv:
.LFB2:
	.seh_endprologue
	mov	eax, 10
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7DerivedD1Ev
	.def	_ZN7DerivedD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD1Ev
_ZN7DerivedD1Ev:
.LFB17:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7DerivedD0Ev
	.def	_ZN7DerivedD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD0Ev
_ZN7DerivedD0Ev:
.LFB18:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	edx, 8
	call	_ZdlPvy
	nop
	add	rsp, 40
	ret
	.seh_endproc
	.text
	.globl	_Z6call_fPK4Base
	.def	_Z6call_fPK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6call_fPK4Base
_Z6call_fPK4Base:
.LFB3:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR [rax]]
	add	rsp, 40
	ret
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rax, _ZTV7Derived[rip+16]
	mov	QWORD PTR 40[rsp], rax
	lea	rcx, 40[rsp]
	call	_Z6call_fPK4Base
	add	rsp, 56
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
	.globl	_ZTS7Derived
	.section	.rdata$_ZTS7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTS7Derived:
	.ascii "7Derived\0"
	.globl	_ZTI7Derived
	.section	.rdata$_ZTI7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTI7Derived:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Derived
	.quad	_ZTI4Base
	.globl	_ZTV7Derived
	.section	.rdata$_ZTV7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTV7Derived:
	.quad	0
	.quad	_ZTI7Derived
	.quad	_ZNK7Derived1fEv
	.quad	_ZNK4Base1gEv
	.quad	_ZN7DerivedD1Ev
	.quad	_ZN7DerivedD0Ev
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
