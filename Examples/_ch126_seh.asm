	.file	"_ch126_seh.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "caught: %s\12\0"
	.section	.text.unlikely,"x"
	.def	_ZL6printfPKcz.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz.constprop.0
_ZL6printfPKcz.constprop.0:
.LFB2611:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	ecx, 1
	lea	rbx, 72[rsp]
	mov	QWORD PTR 72[rsp], rdx
	mov	QWORD PTR 80[rsp], r8
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 40[rsp], rbx
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	lea	rdx, .LC0[rip]
	mov	r8, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "neg\0"
	.text
	.p2align 4
	.globl	_Z9may_throwi
	.def	_Z9may_throwi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9may_throwi
_Z9may_throwi:
.LFB1997:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	ecx, ecx
	js	.L8
	lea	eax, [rcx+rcx]
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
.L8:
	mov	ecx, 16
	call	__cxa_allocate_exception
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	mov	rbx, rax
.LEHB0:
	call	_ZNSt13runtime_errorC1EPKc
.LEHE0:
	lea	r8, _ZNSt13runtime_errorD1Ev[rip]
	mov	rcx, rbx
	lea	rdx, _ZTISt13runtime_error[rip]
.LEHB1:
	call	__cxa_throw
.L5:
	mov	rsi, rax
	mov	rcx, rbx
	call	__cxa_free_exception
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1997:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1997-.LLSDACSB1997
.LLSDACSB1997:
	.uleb128 .LEHB0-.LFB1997
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L5-.LFB1997
	.uleb128 0
	.uleb128 .LEHB1-.LFB1997
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1997:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z9safe_calli
	.def	_Z9safe_calli;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9safe_calli
_Z9safe_calli:
.LFB1998:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
.LEHB2:
	call	_Z9may_throwi
.LEHE2:
	add	eax, 1
.L9:
	add	rsp, 32
	pop	rbx
	ret
.L14:
	sub	rdx, 1
	mov	rcx, rax
	jne	.L16
	call	__cxa_begin_catch
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	call	[QWORD PTR 16[rax]]
	lea	rcx, .LC0[rip]
	mov	rdx, rax
.LEHB3:
	call	_ZL6printfPKcz.constprop.0
.LEHE3:
	call	__cxa_end_catch
	or	eax, -1
	jmp	.L9
.L15:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rcx, rbx
.L16:
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA1998:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT1998-.LLSDATTD1998
.LLSDATTD1998:
	.byte	0x1
	.uleb128 .LLSDACSE1998-.LLSDACSB1998
.LLSDACSB1998:
	.uleb128 .LEHB2-.LFB1998
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L14-.LFB1998
	.uleb128 0x1
	.uleb128 .LEHB3-.LFB1998
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L15-.LFB1998
	.uleb128 0
	.uleb128 .LEHB4-.LFB1998
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE1998:
	.byte	0x1
	.byte	0
	.align 4
	.long	.LDFCM0-.
.LLSDATT1998:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1999:
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorC1EPKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorD1Ev;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	__cxa_free_exception;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZNSt13runtime_errorD1Ev, "dr"
	.globl	.refptr._ZNSt13runtime_errorD1Ev
	.linkonce	discard
.refptr._ZNSt13runtime_errorD1Ev:
	.quad	_ZNSt13runtime_errorD1Ev
