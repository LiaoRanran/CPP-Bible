	.file	"_atom_data_race.cpp"
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB6384:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEE6_M_runEv:
.LFB8471:
	.seh_endprologue
	addl	$100000, _ZL8g_shared(%rip)
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED2Ev:
.LFB8280:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED0Ev:
.LFB8282:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	movq	%rcx, 40(%rsp)
	call	_ZNSt6thread6_StateD2Ev
	movq	40(%rsp), %rcx
	movl	$16, %edx
	addq	$56, %rsp
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED2Ev:
.LFB8276:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED0Ev:
.LFB8278:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	movq	%rcx, 40(%rsp)
	call	_ZNSt6thread6_StateD2Ev
	movq	40(%rsp), %rcx
	movl	$16, %edx
	addq	$56, %rsp
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED2Ev:
.LFB8272:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED0Ev:
.LFB8274:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	movq	%rcx, 40(%rsp)
	call	_ZNSt6thread6_StateD2Ev
	movq	40(%rsp), %rcx
	movl	$16, %edx
	addq	$56, %rsp
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED2Ev:
.LFB8268:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED0Ev:
.LFB8270:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	movq	%rcx, 40(%rsp)
	call	_ZNSt6thread6_StateD2Ev
	movq	40(%rsp), %rcx
	movl	$16, %edx
	addq	$56, %rsp
	jmp	_ZdlPvy
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEE6_M_runEv:
.LFB8468:
	.seh_endprologue
	movl	$100000, %eax
	.p2align 4
	.p2align 4
	.p2align 3
.L13:
	lock addl	$1, _ZL8g_atomic(%rip)
	lock addl	$1, _ZL8g_atomic(%rip)
	subl	$2, %eax
	jne	.L13
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEE6_M_runEv:
.LFB8470:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	$0, 32(%rsp)
	movl	$1000000, 40(%rsp)
.L18:
	leaq	32(%rsp), %rdx
	leaq	32(%rsp), %rcx
	call	nanosleep64
	cmpl	$-1, %eax
	je	.L17
	addl	$100000, _ZL8g_shared(%rip)
	addq	$48, %rsp
	popq	%rbx
	ret
	.p2align 4,,10
	.p2align 3
.L17:
	call	*__imp__errno(%rip)
	cmpl	$4, (%rax)
	je	.L18
	addl	$100000, _ZL8g_shared(%rip)
	addq	$48, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEE6_M_runEv:
.LFB8469:
	.seh_endprologue
	movl	$100000, %eax
	.p2align 4
	.p2align 4
	.p2align 3
.L24:
	lock addl	$1, _ZL8g_atomic(%rip)
	lock addl	$1, _ZL8g_atomic(%rip)
	subl	$2, %eax
	jne	.L24
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "single_total=%d\12\0"
	.text
	.p2align 4
	.globl	_Z12bench_singlev
	.def	_Z12bench_singlev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12bench_singlev
_Z12bench_singlev:
.LFB6618:
	.seh_endprologue
	movl	$100000, %edx
	leaq	.LC0(%rip), %rcx
	jmp	__mingw_printf
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB7570:
	.seh_endprologue
	movq	(%rcx), %rcx
	testq	%rcx, %rcx
	je	.L28
	movq	(%rcx), %rax
	rex.W jmp	*8(%rax)
	.p2align 4,,10
	.p2align 3
.L28:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "safe_ops_total=%d\12\0"
.LC2:
	.ascii "safe_final=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	_Z10bench_safev
	.def	_Z10bench_safev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10bench_safev
_Z10bench_safev:
.LFB6629:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	movl	$16, %ecx
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE(%rip), %rdi
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rbp
	movl	$0, _ZL8g_atomic(%rip)
	movq	$0, 40(%rsp)
.LEHB0:
	call	_Znwy
.LEHE0:
	movq	%rbp, %r8
	leaq	56(%rsp), %rdx
	leaq	40(%rsp), %rcx
	movq	%rdi, (%rax)
	movq	%rax, 56(%rsp)
.LEHB1:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE1:
	movq	56(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L31
	movq	(%rcx), %rax
	call	*8(%rax)
.L31:
	movq	$0, 48(%rsp)
	movl	$16, %ecx
.LEHB2:
	call	_Znwy
.LEHE2:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE(%rip), %rsi
	movq	%rbp, %r8
	leaq	56(%rsp), %rdx
	movq	%rax, 56(%rsp)
	movq	%rsi, (%rax)
	leaq	48(%rsp), %rcx
.LEHB3:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE3:
	movq	56(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L34
	movq	(%rcx), %rax
	call	*8(%rax)
.L34:
	leaq	40(%rsp), %rcx
.LEHB4:
	call	_ZNSt6thread4joinEv
	leaq	48(%rsp), %rcx
	call	_ZNSt6thread4joinEv
	movl	$200000, %edx
	leaq	.LC1(%rip), %rcx
	call	__mingw_printf
	leaq	.LC2(%rip), %rcx
	movl	_ZL8g_atomic(%rip), %edx
	call	__mingw_printf
.LEHE4:
	cmpq	$0, 48(%rsp)
	jne	.L39
	cmpq	$0, 40(%rsp)
	jne	.L54
	addq	$72, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L44:
	movq	%rax, %rsi
	jmp	.L33
.L54:
	jmp	.L39
.L42:
	jmp	.L40
.L43:
	movq	%rax, %rsi
	jmp	.L36
.L41:
	jmp	.L37
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6629:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6629-.LLSDACSB6629
.LLSDACSB6629:
	.uleb128 .LEHB0-.LFB6629
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB6629
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L44-.LFB6629
	.uleb128 0
	.uleb128 .LEHB2-.LFB6629
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L41-.LFB6629
	.uleb128 0
	.uleb128 .LEHB3-.LFB6629
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L43-.LFB6629
	.uleb128 0
	.uleb128 .LEHB4-.LFB6629
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L42-.LFB6629
	.uleb128 0
.LLSDACSE6629:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z10bench_safev.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10bench_safev.cold
	.seh_stackalloc	104
	.seh_savereg	%rbx, 72
	.seh_savereg	%rsi, 80
	.seh_savereg	%rdi, 88
	.seh_savereg	%rbp, 96
	.seh_endprologue
_Z10bench_safev.cold:
.L33:
	leaq	56(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rsi, %rcx
.LEHB5:
	call	_Unwind_Resume
.L36:
	leaq	56(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rsi, %rax
.L37:
	cmpq	$0, 40(%rsp)
	je	.L55
.L39:
	call	_ZSt9terminatev
.L40:
	cmpq	$0, 48(%rsp)
	je	.L37
	jmp	.L39
.L55:
	movq	%rax, %rcx
	call	_Unwind_Resume
	nop
.LEHE5:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC6629:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6629-.LLSDACSBC6629
.LLSDACSBC6629:
	.uleb128 .LEHB5-.LCOLDB3
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSEC6629:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.text
.LHOTE3:
	.section .rdata,"dr"
.LC4:
	.ascii "race_ops_total=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4
	.globl	_Z10bench_racev
	.def	_Z10bench_racev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10bench_racev
_Z10bench_racev:
.LFB6619:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$72, %rsp
	.seh_stackalloc	72
	.seh_endprologue
	movl	$16, %ecx
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rbp
	movl	$0, _ZL8g_shared(%rip)
	movq	$0, 40(%rsp)
.LEHB6:
	call	_Znwy
.LEHE6:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE(%rip), %rdx
	movq	%rbp, %r8
	leaq	40(%rsp), %rcx
	movq	%rdx, (%rax)
	leaq	56(%rsp), %rdx
	movq	%rax, 56(%rsp)
.LEHB7:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE7:
	movq	56(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L57
	movq	(%rcx), %rax
	call	*8(%rax)
.L57:
	movq	$0, 48(%rsp)
	movl	$16, %ecx
.LEHB8:
	call	_Znwy
.LEHE8:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE(%rip), %rsi
	movq	%rbp, %r8
	leaq	56(%rsp), %rdx
	movq	%rax, 56(%rsp)
	movq	%rsi, (%rax)
	leaq	48(%rsp), %rcx
.LEHB9:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE9:
	movq	56(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L60
	movq	(%rcx), %rax
	call	*8(%rax)
.L60:
	leaq	40(%rsp), %rcx
.LEHB10:
	call	_ZNSt6thread4joinEv
	leaq	48(%rsp), %rcx
	call	_ZNSt6thread4joinEv
	movl	$200000, %edx
	leaq	.LC4(%rip), %rcx
	call	__mingw_printf
.LEHE10:
	cmpq	$0, 48(%rsp)
	jne	.L65
	cmpq	$0, 40(%rsp)
	jne	.L80
	addq	$72, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L70:
	movq	%rax, %rsi
	jmp	.L59
.L80:
	jmp	.L65
.L68:
	jmp	.L66
.L69:
	movq	%rax, %rsi
	jmp	.L62
.L67:
	jmp	.L63
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6619:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6619-.LLSDACSB6619
.LLSDACSB6619:
	.uleb128 .LEHB6-.LFB6619
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB7-.LFB6619
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L70-.LFB6619
	.uleb128 0
	.uleb128 .LEHB8-.LFB6619
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L67-.LFB6619
	.uleb128 0
	.uleb128 .LEHB9-.LFB6619
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L69-.LFB6619
	.uleb128 0
	.uleb128 .LEHB10-.LFB6619
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L68-.LFB6619
	.uleb128 0
.LLSDACSE6619:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z10bench_racev.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10bench_racev.cold
	.seh_stackalloc	104
	.seh_savereg	%rbx, 72
	.seh_savereg	%rsi, 80
	.seh_savereg	%rdi, 88
	.seh_savereg	%rbp, 96
	.seh_endprologue
_Z10bench_racev.cold:
.L59:
	leaq	56(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rsi, %rcx
.LEHB11:
	call	_Unwind_Resume
.L62:
	leaq	56(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rsi, %rax
.L63:
	cmpq	$0, 40(%rsp)
	je	.L81
.L65:
	call	_ZSt9terminatev
.L66:
	cmpq	$0, 48(%rsp)
	je	.L63
	jmp	.L65
.L81:
	movq	%rax, %rcx
	call	_Unwind_Resume
	nop
.LEHE11:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC6619:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6619-.LLSDACSBC6619
.LLSDACSBC6619:
	.uleb128 .LEHB11-.LCOLDB5
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0
	.uleb128 0
.LLSDACSEC6619:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.text
.LHOTE5:
	.section .rdata,"dr"
.LC6:
	.ascii "scenario=single|race|safe\12\0"
.LC7:
	.ascii "kIters=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB6636:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	_Z12bench_singlev
	call	_Z10bench_racev
	call	_Z10bench_safev
	leaq	.LC6(%rip), %rcx
	call	__mingw_printf
	movl	$100000, %edx
	leaq	.LC7(%rip), %rcx
	call	__mingw_printf
	xorl	%eax, %eax
	addq	$40, %rsp
	ret
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
	.section .rdata,"dr"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE\0"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE\0"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE\0"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE\0"
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE_EEEEE6_M_runEv
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_racevEUlvE0_EEEEE6_M_runEv
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE_EEEEE6_M_runEv
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ10bench_safevEUlvE0_EEEEE6_M_runEv
.lcomm _ZL8g_atomic,4,4
.lcomm _ZL8g_shared,4,4
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	nanosleep64;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
