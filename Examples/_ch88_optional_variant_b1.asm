	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt18bad_variant_access4whatEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt18bad_variant_access4whatEv
	.def	_ZNKSt18bad_variant_access4whatEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt18bad_variant_access4whatEv
_ZNKSt18bad_variant_access4whatEv:
.LFB308:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	ret
	.seh_endproc
	.section	.text$_ZNSt18bad_variant_accessD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt18bad_variant_accessD1Ev
	.def	_ZNSt18bad_variant_accessD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt18bad_variant_accessD1Ev
_ZNSt18bad_variant_accessD1Ev:
.LFB315:
	.seh_endprologue
	lea	rax, _ZTVSt18bad_variant_access[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt9exceptionD2Ev
	.seh_endproc
	.section	.text$_ZNSt18bad_variant_accessD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt18bad_variant_accessD0Ev
	.def	_ZNSt18bad_variant_accessD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt18bad_variant_accessD0Ev
_ZNSt18bad_variant_accessD0Ev:
.LFB316:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTVSt18bad_variant_access[rip+16]
	mov	rbx, rcx
	mov	QWORD PTR [rcx], rax
	call	_ZNSt9exceptionD2Ev
	mov	edx, 16
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	_ZSt10__do_visitIvZNSt8__detail9__variant16_Variant_storageILb0EJiNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE8_M_resetEvEUlOT_E_JRSt7variantIJiS8_EEEEDcOT0_DpOT1_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt10__do_visitIvZNSt8__detail9__variant16_Variant_storageILb0EJiNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE8_M_resetEvEUlOT_E_JRSt7variantIJiS8_EEEEDcOT0_DpOT1_.isra.0
_ZSt10__do_visitIvZNSt8__detail9__variant16_Variant_storageILb0EJiNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE8_M_resetEvEUlOT_E_JRSt7variantIJiS8_EEEEDcOT0_DpOT1_.isra.0:
.LFB3630:
	.seh_endprologue
	cmp	BYTE PTR 32[rcx], 0
	jne	.L8
.L5:
	ret
.L8:
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L5
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZSt26__throw_bad_variant_accessPKc,"x"
	.linkonce discard
	.globl	_ZSt26__throw_bad_variant_accessPKc
	.def	_ZSt26__throw_bad_variant_accessPKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt26__throw_bad_variant_accessPKc
_ZSt26__throw_bad_variant_accessPKc:
.LFB312:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 16
	call	__cxa_allocate_exception
	lea	r8, _ZNSt18bad_variant_accessD1Ev[rip]
	lea	rdx, _ZTISt18bad_variant_access[rip]
	mov	rcx, rax
	lea	rax, _ZTVSt18bad_variant_access[rip+16]
	mov	QWORD PTR 8[rcx], rbx
	mov	QWORD PTR [rcx], rax
	call	__cxa_throw
	nop
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "index=\0"
.LC1:
	.ascii "\12\0"
.LC2:
	.ascii "index after string=\0"
.LC3:
	.ascii "valueless=\0"
.LC4:
	.ascii "optional engaged=\0"
	.align 8
.LC5:
	.ascii "optional engaged after assign=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2822:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	call	__main
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC0[rip]
	mov	QWORD PTR 68[rsp], 0
	mov	QWORD PTR 76[rsp], 0
	mov	QWORD PTR 84[rsp], 0
	mov	QWORD PTR 92[rsp], 0
	mov	rcx, rsi
	mov	DWORD PTR 100[rsp], 0
	mov	DWORD PTR 64[rsp], 42
.LEHB0:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movzx	edx, BYTE PTR 96[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rbx, .LC1[rip]
	mov	rcx, rax
	mov	rdx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	cmp	BYTE PTR 96[rsp], 1
	lea	rax, 48[rsp]
	mov	r8d, 26984
	mov	QWORD PTR 40[rsp], 2
	mov	QWORD PTR 32[rsp], rax
	mov	WORD PTR 48[rsp], r8w
	mov	BYTE PTR 50[rsp], 0
	je	.L19
	lea	rax, 80[rsp]
	mov	WORD PTR 80[rsp], 26984
	mov	QWORD PTR 64[rsp], rax
	mov	BYTE PTR 82[rsp], 0
	mov	QWORD PTR 72[rsp], 2
	mov	BYTE PTR 96[rsp], 1
.L12:
	lea	rdx, .LC2[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movzx	edx, BYTE PTR 96[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	mov	rcx, rax
	mov	rdx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC3[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR -24[rax]
	add	rdx, rcx
	or	DWORD PTR 24[rdx], 1
	xor	edx, edx
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	mov	rdx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC4[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	xor	edx, edx
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	mov	rdx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC5[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	edx, 1
	call	_ZNSo9_M_insertIbEERSoT_
	mov	rcx, rax
	mov	rdx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE0:
	lea	rcx, 64[rsp]
	call	_ZSt10__do_visitIvZNSt8__detail9__variant16_Variant_storageILb0EJiNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE8_M_resetEvEUlOT_E_JRSt7variantIJiS8_EEEEDcOT0_DpOT1_.isra.0
	xor	eax, eax
	add	rsp, 120
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	mov	rdx, QWORD PTR 64[rsp]
	mov	ecx, 26984
	mov	WORD PTR [rdx], cx
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, QWORD PTR 64[rsp]
	mov	QWORD PTR 72[rsp], rdx
	mov	BYTE PTR [rcx+rdx], 0
	mov	rdx, QWORD PTR 32[rsp]
	mov	QWORD PTR 40[rsp], 0
	mov	BYTE PTR [rdx], 0
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rax
	je	.L12
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L12
.L15:
	lea	rcx, 64[rsp]
	mov	rbx, rax
	call	_ZSt10__do_visitIvZNSt8__detail9__variant16_Variant_storageILb0EJiNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEEE8_M_resetEvEUlOT_E_JRSt7variantIJiS8_EEEEDcOT0_DpOT1_.isra.0
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2822:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2822-.LLSDACSB2822
.LLSDACSB2822:
	.uleb128 .LEHB0-.LFB2822
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L15-.LFB2822
	.uleb128 0
	.uleb128 .LEHB1-.LFB2822
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE2822:
	.section	.text.startup,"x"
	.seh_endproc
	.globl	_ZTSSt9exception
	.section	.rdata$_ZTSSt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTSSt9exception:
	.ascii "St9exception\0"
	.globl	_ZTISt9exception
	.section	.rdata$_ZTISt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTISt9exception:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt9exception
	.globl	_ZTSSt18bad_variant_access
	.section	.rdata$_ZTSSt18bad_variant_access,"dr"
	.linkonce same_size
	.align 16
_ZTSSt18bad_variant_access:
	.ascii "St18bad_variant_access\0"
	.globl	_ZTISt18bad_variant_access
	.section	.rdata$_ZTISt18bad_variant_access,"dr"
	.linkonce same_size
	.align 8
_ZTISt18bad_variant_access:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt18bad_variant_access
	.quad	_ZTISt9exception
	.globl	_ZTVSt18bad_variant_access
	.section	.rdata$_ZTVSt18bad_variant_access,"dr"
	.linkonce same_size
	.align 8
_ZTVSt18bad_variant_access:
	.quad	0
	.quad	_ZTISt18bad_variant_access
	.quad	_ZNSt18bad_variant_accessD1Ev
	.quad	_ZNSt18bad_variant_accessD0Ev
	.quad	_ZNKSt18bad_variant_access4whatEv
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSt9exceptionD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
