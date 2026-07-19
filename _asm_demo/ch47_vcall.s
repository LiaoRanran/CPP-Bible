	.file	"_asm_vcall.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN4BaseD2Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4BaseD2Ev
	.def	_ZN4BaseD2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4BaseD2Ev
_ZN4BaseD2Ev:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV4Base[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4BaseD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4BaseD1Ev
	.def	_ZN4BaseD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4BaseD1Ev
_ZN4BaseD1Ev:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV4Base[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4BaseD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4BaseD0Ev
	.def	_ZN4BaseD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4BaseD0Ev
_ZN4BaseD0Ev:
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
	call	_ZN4BaseD1Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK4Base3fooEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4Base3fooEv
	.def	_ZNK4Base3fooEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4Base3fooEv
_ZNK4Base3fooEv:
.LFB4:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, 1
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK4Base3barEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK4Base3barEv
	.def	_ZNK4Base3barEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK4Base3barEv
_ZNK4Base3barEv:
.LFB5:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, 2
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK7Derived3fooEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK7Derived3fooEv
	.def	_ZNK7Derived3fooEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7Derived3fooEv
_ZNK7Derived3fooEv:
.LFB6:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, 3
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z12call_virtualRK4Base
	.def	_Z12call_virtualRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12call_virtualRK4Base
_Z12call_virtualRK4Base:
.LFB7:
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
	add	rax, 16
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z15call_nonvirtualRK4Base
	.def	_Z15call_nonvirtualRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15call_nonvirtualRK4Base
_Z15call_nonvirtualRK4Base:
.LFB8:
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
	call	_ZNK4Base3barEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7DerivedD1Ev
	.def	_ZN7DerivedD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD1Ev
_ZN7DerivedD1Ev:
.LFB18:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	lea	rdx, _ZTV7Derived[rip+16]
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN4BaseD2Ev
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD0Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN7DerivedD0Ev
	.def	_ZN7DerivedD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD0Ev
_ZN7DerivedD0Ev:
.LFB19:
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
	call	_ZN7DerivedD1Ev
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, 8
	mov	rcx, rax
	call	_ZdlPvy
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB9:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	call	__main
	lea	rax, _ZTV7Derived[rip+16]
	mov	QWORD PTR -8[rbp], rax
	lea	rax, -8[rbp]
	mov	rcx, rax
.LEHB0:
	call	_Z12call_virtualRK4Base
.LEHE0:
	mov	ebx, eax
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_Z15call_nonvirtualRK4Base
	add	ebx, eax
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZN7DerivedD1Ev
	mov	eax, ebx
	jmp	.L20
.L19:
	mov	rbx, rax
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZN7DerivedD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L20:
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA9:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9-.LLSDACSB9
.LLSDACSB9:
	.uleb128 .LEHB0-.LFB9
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L19-.LFB9
	.uleb128 0
	.uleb128 .LEHB1-.LFB9
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE9:
	.text
	.seh_endproc
	.globl	_ZTV7Derived
	.section	.rdata$_ZTV7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTV7Derived:
	.quad	0
	.quad	_ZTI7Derived
	.quad	_ZN7DerivedD1Ev
	.quad	_ZN7DerivedD0Ev
	.quad	_ZNK7Derived3fooEv
	.globl	_ZTV4Base
	.section	.rdata$_ZTV4Base,"dr"
	.linkonce same_size
	.align 8
_ZTV4Base:
	.quad	0
	.quad	_ZTI4Base
	.quad	_ZN4BaseD1Ev
	.quad	_ZN4BaseD0Ev
	.quad	_ZNK4Base3fooEv
	.globl	_ZTI7Derived
	.section	.rdata$_ZTI7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTI7Derived:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Derived
	.quad	_ZTI4Base
	.globl	_ZTS7Derived
	.section	.rdata$_ZTS7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTS7Derived:
	.ascii "7Derived\0"
	.globl	_ZTI4Base
	.section	.rdata$_ZTI4Base,"dr"
	.linkonce same_size
	.align 8
_ZTI4Base:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS4Base
	.globl	_ZTS4Base
	.section	.rdata$_ZTS4Base,"dr"
	.linkonce same_size
_ZTS4Base:
	.ascii "4Base\0"
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
