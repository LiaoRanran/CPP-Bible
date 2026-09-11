	.file	"_atom_raii.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "boom\0"
	.section	.text.unlikely,"x"
	.globl	_Z9safe_pathv
	.def	_Z9safe_pathv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9safe_pathv
_Z9safe_pathv:
.LFB4080:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	eax, DWORD PTR g_live[rip]
	mov	ecx, 16
	inc	eax
	mov	DWORD PTR g_live[rip], eax
	call	__cxa_allocate_exception
	lea	rdx, .LC0[rip]
	mov	rcx, rax
	mov	rsi, rax
.LEHB0:
	call	_ZNSt13runtime_errorC1EPKc
.LEHE0:
	lea	r8, _ZNSt13runtime_errorD1Ev[rip]
	lea	rdx, _ZTISt13runtime_error[rip]
	mov	rcx, rsi
.LEHB1:
	call	__cxa_throw
.LEHE1:
.L4:
	mov	rbx, rax
.L2:
	mov	rcx, rsi
	call	__cxa_free_exception
	mov	rcx, rbx
	jmp	.L3
.L5:
	mov	rcx, rax
.L3:
	mov	eax, DWORD PTR g_live[rip]
	dec	eax
	mov	DWORD PTR g_live[rip], eax
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4080:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4080-.LLSDACSB4080
.LLSDACSB4080:
	.uleb128 .LEHB0-.LFB4080
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L4-.LFB4080
	.uleb128 0
	.uleb128 .LEHB1-.LFB4080
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L5-.LFB4080
	.uleb128 0
	.uleb128 .LEHB2-.LFB4080
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE4080:
	.section	.text.unlikely,"x"
	.seh_endproc
	.globl	_Z9leak_pathv
	.def	_Z9leak_pathv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9leak_pathv
_Z9leak_pathv:
.LFB4081:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	eax, DWORD PTR g_live[rip]
	mov	ecx, 16
	inc	eax
	mov	DWORD PTR g_live[rip], eax
	call	__cxa_allocate_exception
	lea	rdx, .LC0[rip]
	mov	rcx, rax
	mov	rbx, rax
.LEHB3:
	call	_ZNSt13runtime_errorC1EPKc
.LEHE3:
	lea	r8, _ZNSt13runtime_errorD1Ev[rip]
	lea	rdx, _ZTISt13runtime_error[rip]
	mov	rcx, rbx
.LEHB4:
	call	__cxa_throw
.L9:
	mov	rsi, rax
.L8:
	mov	rcx, rbx
	call	__cxa_free_exception
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4081:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4081-.LLSDACSB4081
.LLSDACSB4081:
	.uleb128 .LEHB3-.LFB4081
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L9-.LFB4081
	.uleb128 0
	.uleb128 .LEHB4-.LFB4081
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE4081:
	.section	.text.unlikely,"x"
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "after safe_path g_live=\0"
.LC2:
	.ascii "\12\0"
.LC3:
	.ascii "after leak_path g_live=\0"
	.section	.text.unlikely,"x"
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4082:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
.LEHB5:
	call	_Z9safe_pathv
.LEHE5:
.L13:
.L11:
	mov	rcx, rax
	call	__cxa_begin_catch
.LEHB6:
	call	__cxa_end_catch
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC1[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_live[rip]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE6:
.LEHB7:
	call	_Z9leak_pathv
.LEHE7:
.L14:
.L12:
	mov	rcx, rax
	call	__cxa_begin_catch
.LEHB8:
	call	__cxa_end_catch
	mov	rcx, rbx
	lea	rdx, .LC3[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_live[rip]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE8:
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA4082:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT4082-.LLSDATTD4082
.LLSDATTD4082:
	.byte	0x1
	.uleb128 .LLSDACSE4082-.LLSDACSB4082
.LLSDACSB4082:
	.uleb128 .LEHB5-.LFB4082
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L13-.LFB4082
	.uleb128 0x1
	.uleb128 .LEHB6-.LFB4082
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB7-.LFB4082
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L14-.LFB4082
	.uleb128 0x1
	.uleb128 .LEHB8-.LFB4082
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
.LLSDACSE4082:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT4082:
	.section	.text.unlikely,"x"
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
	.globl	g_live
	.bss
	.align 4
g_live:
	.space 4
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
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
	.section	.rdata$.refptr._ZNSt13runtime_errorD1Ev, "dr"
	.p2align	3, 0
	.globl	.refptr._ZNSt13runtime_errorD1Ev
	.linkonce	discard
.refptr._ZNSt13runtime_errorD1Ev:
	.quad	_ZNSt13runtime_errorD1Ev
