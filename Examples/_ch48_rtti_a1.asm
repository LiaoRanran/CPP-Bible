	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2312:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.section	.text$_ZNK7Derived2opEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK7Derived2opEi
	.def	_ZNK7Derived2opEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK7Derived2opEi
_ZNK7Derived2opEi:
.LFB2575:
	.seh_endprologue
	lea	eax, 1[rdx]
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD1Ev
	.def	_ZN7DerivedD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD1Ev
_ZN7DerivedD1Ev:
.LFB2590:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD0Ev
	.def	_ZN7DerivedD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD0Ev
_ZN7DerivedD0Ev:
.LFB2591:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB3244:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	rbx, rcx
	mov	rsi, QWORD PTR 240[rcx+rax]
	test	rsi, rsi
	je	.L11
	cmp	BYTE PTR 56[rsi], 0
	je	.L8
	movsx	edx, BYTE PTR 67[rsi]
.L9:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L8:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L9
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L9
.L11:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmp3irzm_5d\\s.cpp\0"
.LC1:
	.ascii "pd != nullptr\0"
.LC2:
	.ascii "pd->op(10) == 11\0"
.LC3:
	.ascii "po == nullptr\0"
.LC4:
	.ascii "(typeid(*pb) == td)\0"
	.align 8
.LC5:
	.ascii "!(typeid(*pb) == typeid(Other))\0"
.LC6:
	.ascii "!(typeid(b) == td)\0"
.LC7:
	.ascii "dynamic_cast ok : \0"
.LC8:
	.ascii "cross cast null : \0"
.LC9:
	.ascii "all functional checks passed\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2577:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rbx, _ZTI4Base[rip]
	call	__main
	lea	rsi, 40[rsp]
	xor	r9d, r9d
	mov	rdx, rbx
	lea	rax, _ZTV7Derived[rip+16]
	mov	rcx, rsi
	lea	r8, _ZTI7Derived[rip]
	mov	QWORD PTR 40[rsp], rax
	call	__dynamic_cast
	test	rax, rax
	mov	rcx, rax
	je	.L20
	mov	rax, QWORD PTR [rax]
	mov	edx, 10
	call	[QWORD PTR 16[rax]]
	cmp	eax, 11
	jne	.L21
	xor	r9d, r9d
	mov	rdx, rbx
	mov	rcx, rsi
	lea	r8, _ZTI5Other[rip]
	call	__dynamic_cast
	test	rax, rax
	jne	.L22
	mov	rax, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR -8[rax]
	lea	rax, _ZTS7Derived[rip]
	cmp	QWORD PTR 8[rcx], rax
	je	.L16
	lea	rdx, _ZTI7Derived[rip]
	call	_ZNKSt9type_info7__equalERKS_
	test	al, al
	je	.L23
	mov	rax, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR -8[rax]
	lea	rax, _ZTS5Other[rip]
	cmp	QWORD PTR 8[rcx], rax
	je	.L18
.L16:
	lea	rdx, _ZTI5Other[rip]
	call	_ZNKSt9type_info7__equalERKS_
	test	al, al
	jne	.L18
	lea	rdx, _ZTI7Derived[rip]
	mov	rcx, rbx
	call	_ZNKSt9type_info7__equalERKS_
	test	al, al
	jne	.L24
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC7[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC8[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 1
	mov	rcx, rax
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC9[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
.L18:
	lea	rdx, .LC0[rip]
	mov	r8d, 25
	lea	rcx, .LC5[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L22:
	lea	rdx, .LC0[rip]
	mov	r8d, 20
	lea	rcx, .LC3[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L21:
	lea	rdx, .LC0[rip]
	mov	r8d, 16
	lea	rcx, .LC2[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L20:
	lea	rdx, .LC0[rip]
	mov	r8d, 15
	lea	rcx, .LC1[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L23:
	lea	rdx, .LC0[rip]
	mov	r8d, 24
	lea	rcx, .LC4[rip]
	call	[QWORD PTR __imp__assert[rip]]
.L24:
	lea	rdx, .LC0[rip]
	mov	r8d, 29
	lea	rcx, .LC6[rip]
	call	[QWORD PTR __imp__assert[rip]]
	nop
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
	.globl	_ZTS5Other
	.section	.rdata$_ZTS5Other,"dr"
	.linkonce same_size
_ZTS5Other:
	.ascii "5Other\0"
	.globl	_ZTI5Other
	.section	.rdata$_ZTI5Other,"dr"
	.linkonce same_size
	.align 8
_ZTI5Other:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS5Other
	.quad	_ZTI4Base
	.globl	_ZTV7Derived
	.section	.rdata$_ZTV7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTV7Derived:
	.quad	0
	.quad	_ZTI7Derived
	.quad	_ZN7DerivedD1Ev
	.quad	_ZN7DerivedD0Ev
	.quad	_ZNK7Derived2opEi
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	__dynamic_cast;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt9type_info7__equalERKS_;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
