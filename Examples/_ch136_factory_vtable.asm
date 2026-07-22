	.file	"_ch136_factory_vtable.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK6Button4areaEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK6Button4areaEv
	.def	_ZNK6Button4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK6Button4areaEv
_ZNK6Button4areaEv:
.LFB3534:
	.seh_endprologue
	mov	eax, 10
	ret
	.seh_endproc
	.section	.text$_ZNK6Window4areaEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK6Window4areaEv
	.def	_ZNK6Window4areaEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK6Window4areaEv
_ZNK6Window4areaEv:
.LFB3535:
	.seh_endprologue
	mov	eax, 100
	ret
	.seh_endproc
	.section	.text$_ZN6ButtonD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN6ButtonD1Ev
	.def	_ZN6ButtonD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6ButtonD1Ev
_ZN6ButtonD1Ev:
.LFB4040:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN6WindowD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN6WindowD1Ev
	.def	_ZN6WindowD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6WindowD1Ev
_ZN6WindowD1Ev:
.LFB4046:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN6ButtonD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN6ButtonD0Ev
	.def	_ZN6ButtonD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6ButtonD0Ev
_ZN6ButtonD0Ev:
.LFB4041:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN6WindowD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN6WindowD0Ev
	.def	_ZN6WindowD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6WindowD0Ev
_ZN6WindowD0Ev:
.LFB4047:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z4makePKc
	.def	_Z4makePKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4makePKc
_Z4makePKc:
.LFB3545:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 8
	cmp	BYTE PTR [rdx], 66
	je	.L11
	call	_Znwy
	lea	rdx, _ZTV6Window[rip+16]
	mov	QWORD PTR [rax], rdx
	mov	QWORD PTR [rbx], rax
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	call	_Znwy
	lea	rcx, _ZTV6Button[rip+16]
	mov	QWORD PTR [rax], rcx
	mov	QWORD PTR [rbx], rax
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z3runv
	.def	_Z3runv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3runv
_Z3runv:
.LFB3726:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 8
	call	_Znwy
	lea	rdx, _ZTV6Button[rip+16]
	mov	QWORD PTR [rax], rdx
	mov	rcx, rax
	call	_ZN6ButtonD0Ev
	mov	eax, 10
	add	rsp, 40
	ret
	.seh_endproc
	.globl	_ZTS6Widget
	.section	.rdata$_ZTS6Widget,"dr"
	.linkonce same_size
	.align 8
_ZTS6Widget:
	.ascii "6Widget\0"
	.globl	_ZTI6Widget
	.section	.rdata$_ZTI6Widget,"dr"
	.linkonce same_size
	.align 8
_ZTI6Widget:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS6Widget
	.globl	_ZTS6Button
	.section	.rdata$_ZTS6Button,"dr"
	.linkonce same_size
	.align 8
_ZTS6Button:
	.ascii "6Button\0"
	.globl	_ZTI6Button
	.section	.rdata$_ZTI6Button,"dr"
	.linkonce same_size
	.align 8
_ZTI6Button:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS6Button
	.quad	_ZTI6Widget
	.globl	_ZTS6Window
	.section	.rdata$_ZTS6Window,"dr"
	.linkonce same_size
	.align 8
_ZTS6Window:
	.ascii "6Window\0"
	.globl	_ZTI6Window
	.section	.rdata$_ZTI6Window,"dr"
	.linkonce same_size
	.align 8
_ZTI6Window:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS6Window
	.quad	_ZTI6Widget
	.globl	_ZTV6Button
	.section	.rdata$_ZTV6Button,"dr"
	.linkonce same_size
	.align 8
_ZTV6Button:
	.quad	0
	.quad	_ZTI6Button
	.quad	_ZN6ButtonD1Ev
	.quad	_ZN6ButtonD0Ev
	.quad	_ZNK6Button4areaEv
	.globl	_ZTV6Window
	.section	.rdata$_ZTV6Window,"dr"
	.linkonce same_size
	.align 8
_ZTV6Window:
	.quad	0
	.quad	_ZTI6Window
	.quad	_ZN6WindowD1Ev
	.quad	_ZN6WindowD0Ev
	.quad	_ZNK6Window4areaEv
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
