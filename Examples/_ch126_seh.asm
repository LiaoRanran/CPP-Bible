	.file	"_ch126_seh.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "neg\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z9may_throwi
	.def	_Z9may_throwi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9may_throwi
_Z9may_throwi:
.LFB2050:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	ecx, ecx
	js	.L5
	lea	eax, [rcx+rcx]
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2050:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2050-.LLSDACSB2050
.LLSDACSB2050:
.LLSDACSE2050:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z9may_throwi.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z9may_throwi.cold
	.seh_stackalloc	56
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_endprologue
_Z9may_throwi.cold:
.L5:
	mov	ecx, 16
	call	__cxa_allocate_exception
	lea	rdx, .LC0[rip]
	mov	rcx, rax
	mov	rbx, rax
.LEHB0:
	call	_ZNSt13runtime_errorC1EPKc
.LEHE0:
	lea	r8, _ZNSt13runtime_errorD1Ev[rip]
	lea	rdx, _ZTISt13runtime_error[rip]
	mov	rcx, rbx
.LEHB1:
	call	__cxa_throw
.L4:
	mov	rsi, rax
	mov	rcx, rbx
	call	__cxa_free_exception
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2050:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2050-.LLSDACSBC2050
.LLSDACSBC2050:
	.uleb128 .LEHB0-.LCOLDB1
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L4-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB1-.LCOLDB1
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC2050:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section .rdata,"dr"
.LC2:
	.ascii "caught: %s\12\0"
	.section	.text.unlikely,"x"
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	_Z9safe_calli
	.def	_Z9safe_calli;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9safe_calli
_Z9safe_calli:
.LFB2051:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
.LEHB2:
	call	_Z9may_throwi
.LEHE2:
	add	eax, 1
.L8:
	add	rsp, 32
	pop	rbx
	ret
.L13:
	mov	rcx, rax
	jmp	.L9
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA2051:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT2051-.LLSDATTD2051
.LLSDATTD2051:
	.byte	0x1
	.uleb128 .LLSDACSE2051-.LLSDACSB2051
.LLSDACSB2051:
	.uleb128 .LEHB2-.LFB2051
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L13-.LFB2051
	.uleb128 0x1
.LLSDACSE2051:
	.byte	0x1
	.byte	0
	.align 4
	.long	.LDFCM0-.
.LLSDATT2051:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z9safe_calli.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z9safe_calli.cold
	.seh_stackalloc	40
	.seh_savereg	rbx, 32
	.seh_endprologue
_Z9safe_calli.cold:
.L9:
	sub	rdx, 1
	jne	.L15
	call	__cxa_begin_catch
	mov	rdx, QWORD PTR [rax]
	mov	rcx, rax
	call	[QWORD PTR 16[rdx]]
	lea	rcx, .LC2[rip]
	mov	rdx, rax
.LEHB3:
	call	__mingw_printf
.LEHE3:
	call	__cxa_end_catch
	mov	eax, -1
	jmp	.L8
.L15:
.LEHB4:
	call	_Unwind_Resume
.L14:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDAC2051:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATTC2051-.LLSDATTDC2051
.LLSDATTDC2051:
	.byte	0x1
	.uleb128 .LLSDACSEC2051-.LLSDACSBC2051
.LLSDACSBC2051:
	.uleb128 .LEHB3-.LCOLDB3
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L14-.LCOLDB3
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB3
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC2051:
	.byte	0x1
	.byte	0
	.align 4
	.long	.LDFCM0-.
.LLSDATTC2051:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2052:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	mov	ecx, 10
	call	_Z9safe_calli
	mov	ecx, -3
	mov	ebx, eax
	call	_Z9safe_calli
	add	eax, ebx
	add	rsp, 32
	pop	rbx
	ret
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
	.globl	_ZTSSt13runtime_error
	.section	.rdata$_ZTSSt13runtime_error,"dr"
	.linkonce same_size
	.align 16
_ZTSSt13runtime_error:
	.ascii "St13runtime_error\0"
	.globl	_ZTISt13runtime_error
	.section	.rdata$_ZTISt13runtime_error,"dr"
	.linkonce same_size
	.align 8
_ZTISt13runtime_error:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt13runtime_error
	.quad	_ZTISt9exception
	.data
	.align 8
.LDFCM0:
	.quad	_ZTISt9exception
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorC1EPKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorD1Ev;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	__cxa_free_exception;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZNSt13runtime_errorD1Ev, "dr"
	.p2align	3, 0
	.globl	.refptr._ZNSt13runtime_errorD1Ev
	.linkonce	discard
.refptr._ZNSt13runtime_errorD1Ev:
	.quad	_ZNSt13runtime_errorD1Ev
