	.file	"_ch147_race.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB3134:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z3incv
	.def	_Z3incv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3incv
_Z3incv:
.LFB3697:
	.seh_endprologue
	add	DWORD PTR g[rip], 100000
	ret
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv:
.LFB4660:
	.seh_endprologue
	rex.W jmp	[QWORD PTR 8[rcx]]
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev:
.LFB4658:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev:
.LFB4659:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE[rip+16]
	mov	rbx, rcx
	mov	QWORD PTR [rcx], rax
	call	_ZNSt6thread6_StateD2Ev
	mov	edx, 16
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_
	.def	_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_
_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_:
.LFB4177:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbx, rcx
	mov	QWORD PTR [rcx], 0
	mov	ecx, 16
	mov	rsi, rdx
.LEHB0:
	call	_Znwy
.LEHE0:
	lea	rdx, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE[rip+16]
	mov	rcx, rbx
	mov	QWORD PTR [rax], rdx
	lea	r8, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	mov	QWORD PTR 8[rax], rsi
	lea	rdx, 40[rsp]
	mov	QWORD PTR 40[rsp], rax
.LEHB1:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE1:
	mov	rcx, QWORD PTR 40[rsp]
	test	rcx, rcx
	je	.L7
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
	nop
.L7:
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
.L11:
	mov	rcx, QWORD PTR 40[rsp]
	mov	rbx, rax
	test	rcx, rcx
	je	.L10
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR 8[rax]]
.L10:
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4177:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4177-.LLSDACSB4177
.LLSDACSB4177:
	.uleb128 .LEHB0-.LFB4177
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB4177
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L11-.LFB4177
	.uleb128 0
	.uleb128 .LEHB2-.LFB4177
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE4177:
	.section	.text$_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_,"x"
	.linkonce discard
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3698:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	lea	rdi, _Z3incv[rip]
	call	__main
	lea	rsi, 32[rsp]
	mov	rdx, rdi
	lea	rbx, 40[rsp]
	mov	rcx, rsi
.LEHB3:
	call	_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_
.LEHE3:
	mov	rdx, rdi
	mov	rcx, rbx
.LEHB4:
	call	_ZNSt6threadC1IRFvvEJEvEEOT_DpOT0_
.LEHE4:
	mov	rcx, rsi
.LEHB5:
	call	_ZNSt6thread4joinEv
	mov	rcx, rbx
	call	_ZNSt6thread4joinEv
.LEHE5:
	cmp	QWORD PTR 40[rsp], 0
	jne	.L20
	cmp	QWORD PTR 32[rsp], 0
	jne	.L20
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L23:
	mov	rcx, rax
.L22:
	cmp	QWORD PTR 32[rsp], 0
	je	.L26
.L20:
	call	_ZSt9terminatev
.L24:
	cmp	QWORD PTR 40[rsp], 0
	mov	rcx, rax
	je	.L22
	jmp	.L20
.L26:
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3698:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3698-.LLSDACSB3698
.LLSDACSB3698:
	.uleb128 .LEHB3-.LFB3698
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB3698
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L23-.LFB3698
	.uleb128 0
	.uleb128 .LEHB5-.LFB3698
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L24-.LFB3698
	.uleb128 0
	.uleb128 .LEHB6-.LFB3698
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSE3698:
	.section	.text.startup,"x"
	.seh_endproc
	.globl	_ZTSNSt6thread6_StateE
	.section	.rdata$_ZTSNSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 16
_ZTSNSt6thread6_StateE:
	.ascii "NSt6thread6_StateE\0"
	.globl	_ZTINSt6thread6_StateE
	.section	.rdata$_ZTINSt6thread6_StateE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread6_StateE:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSNSt6thread6_StateE
	.globl	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.section	.rdata$_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE:
	.ascii "NSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE\0"
	.globl	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.section	.rdata$_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.quad	_ZTINSt6thread6_StateE
	.globl	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.section	.rdata$_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv
	.globl	g
	.bss
	.align 4
g:
	.space 4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
