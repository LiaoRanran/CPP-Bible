	.file	"_atom_lock_cost.cpp"
	.text
#APP
	.globl _ZSt21ios_base_library_initv
#NO_APP
	.section	.text._ZNSt6thread24_M_thread_deps_never_runEv,"axG",@progbits,_ZNSt6thread24_M_thread_deps_never_runEv,comdat
	.p2align 4
	.weak	_ZNSt6thread24_M_thread_deps_never_runEv
	.type	_ZNSt6thread24_M_thread_deps_never_runEv, @function
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB3523:
	.cfi_startproc
	endbr64
	ret
	.cfi_endproc
.LFE3523:
	.size	_ZNSt6thread24_M_thread_deps_never_runEv, .-_ZNSt6thread24_M_thread_deps_never_runEv
	.section	.text._ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv,"axG",@progbits,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv
	.type	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv, @function
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv:
.LFB7929:
	.cfi_startproc
	endbr64
	jmp	*8(%rdi)
	.cfi_endproc
.LFE7929:
	.size	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv, .-_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv
	.text
	.p2align 4
	.globl	_Z11bench_mutexv
	.type	_Z11bench_mutexv, @function
_Z11bench_mutexv:
.LFB6384:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	leaq	g_mutex(%rip), %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	movl	$200000, %ebx
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
	.p2align 4,,10
	.p2align 3
.L6:
	movq	%rbp, %rdi
	call	pthread_mutex_lock@PLT
	testl	%eax, %eax
	jne	.L9
	movq	%rbp, %rdi
	addq	$1, g_mutex_cnt(%rip)
	call	pthread_mutex_unlock@PLT
	subq	$1, %rbx
	jne	.L6
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L9:
	.cfi_restore_state
	movl	%eax, %edi
	call	_ZSt20__throw_system_errori@PLT
	.cfi_endproc
.LFE6384:
	.size	_Z11bench_mutexv, .-_Z11bench_mutexv
	.p2align 4
	.globl	_Z18bench_atomic_fetchv
	.type	_Z18bench_atomic_fetchv, @function
_Z18bench_atomic_fetchv:
.LFB6385:
	.cfi_startproc
	endbr64
	movl	$200000, %eax
	.p2align 4,,10
	.p2align 3
.L11:
	lock addq	$1, g_atomic_cnt(%rip)
	lock addq	$1, g_atomic_cnt(%rip)
	subq	$2, %rax
	jne	.L11
	ret
	.cfi_endproc
.LFE6385:
	.size	_Z18bench_atomic_fetchv, .-_Z18bench_atomic_fetchv
	.p2align 4
	.globl	_Z16bench_atomic_casv
	.type	_Z16bench_atomic_casv, @function
_Z16bench_atomic_casv:
.LFB6386:
	.cfi_startproc
	endbr64
	movl	$200000, %edx
	.p2align 4,,10
	.p2align 3
.L17:
	movq	g_cas_target(%rip), %rax
	leaq	1(%rax), %rcx
	lock cmpxchgq	%rcx, g_cas_target(%rip)
	jne	.L16
.L15:
	subq	$1, %rdx
	jne	.L17
	ret
.L16:
	lock addq	$1, g_cas_retries(%rip)
	leaq	1(%rax), %rcx
	lock cmpxchgq	%rcx, g_cas_target(%rip)
	je	.L15
	jmp	.L16
	.cfi_endproc
.LFE6386:
	.size	_Z16bench_atomic_casv, .-_Z16bench_atomic_casv
	.section	.text._ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev,"axG",@progbits,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED5Ev,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev
	.type	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev, @function
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev:
.LFB7926:
	.cfi_startproc
	endbr64
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rax
	movq	%rax, (%rdi)
	jmp	_ZNSt6thread6_StateD2Ev@PLT
	.cfi_endproc
.LFE7926:
	.size	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev, .-_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev
	.weak	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED2Ev
	.section	.text._ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev,"axG",@progbits,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED5Ev,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev
	.type	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev, @function
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev:
.LFB7928:
	.cfi_startproc
	endbr64
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rax
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movq	%rdi, %rbx
	movq	%rax, (%rdi)
	call	_ZNSt6thread6_StateD2Ev@PLT
	movq	%rbx, %rdi
	movl	$16, %esi
	popq	%rbx
	.cfi_def_cfa_offset 8
	jmp	_ZdlPvm@PLT
	.cfi_endproc
.LFE7928:
	.size	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev, .-_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev
	.text
	.p2align 4
	.globl	_Z12bench_singlev
	.type	_Z12bench_singlev, @function
_Z12bench_singlev:
.LFB6383:
	.cfi_startproc
	endbr64
	addq	$200000, g_single(%rip)
	ret
	.cfi_endproc
.LFE6383:
	.size	_Z12bench_singlev, .-_Z12bench_singlev
	.section	.text._ZNSt6vectorISt6threadSaIS0_EED2Ev,"axG",@progbits,_ZNSt6vectorISt6threadSaIS0_EED5Ev,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt6vectorISt6threadSaIS0_EED2Ev
	.type	_ZNSt6vectorISt6threadSaIS0_EED2Ev, @function
_ZNSt6vectorISt6threadSaIS0_EED2Ev:
.LFB7024:
	.cfi_startproc
	endbr64
	movq	8(%rdi), %rdx
	movq	(%rdi), %rcx
	cmpq	%rcx, %rdx
	je	.L26
	movq	%rcx, %rax
	.p2align 4,,10
	.p2align 3
.L28:
	cmpq	$0, (%rax)
	jne	.L34
	addq	$8, %rax
	cmpq	%rax, %rdx
	jne	.L28
.L26:
	testq	%rcx, %rcx
	je	.L25
	movq	16(%rdi), %rsi
	movq	%rcx, %rdi
	subq	%rcx, %rsi
	jmp	_ZdlPvm@PLT
	.p2align 4,,10
	.p2align 3
.L25:
	ret
.L34:
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	call	_ZSt9terminatev@PLT
	.cfi_endproc
.LFE7024:
	.size	_ZNSt6vectorISt6threadSaIS0_EED2Ev, .-_ZNSt6vectorISt6threadSaIS0_EED2Ev
	.weak	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	.set	_ZNSt6vectorISt6threadSaIS0_EED1Ev,_ZNSt6vectorISt6threadSaIS0_EED2Ev
	.section	.text._ZNSt6vectorISt6threadSaIS0_EE5clearEv,"axG",@progbits,_ZNSt6vectorISt6threadSaIS0_EE5clearEv,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	.type	_ZNSt6vectorISt6threadSaIS0_EE5clearEv, @function
_ZNSt6vectorISt6threadSaIS0_EE5clearEv:
.LFB7028:
	.cfi_startproc
	endbr64
	movq	(%rdi), %rcx
	movq	8(%rdi), %rdx
	cmpq	%rdx, %rcx
	je	.L35
	movq	%rcx, %rax
	.p2align 4,,10
	.p2align 3
.L38:
	cmpq	$0, (%rax)
	jne	.L43
	addq	$8, %rax
	cmpq	%rax, %rdx
	jne	.L38
	movq	%rcx, 8(%rdi)
.L35:
	ret
.L43:
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	call	_ZSt9terminatev@PLT
	.cfi_endproc
.LFE7028:
	.size	_ZNSt6vectorISt6threadSaIS0_EE5clearEv, .-_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	.section	.text._ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev,"axG",@progbits,_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED5Ev,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev
	.type	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev, @function
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev:
.LFB7693:
	.cfi_startproc
	endbr64
	movq	(%rdi), %rdi
	testq	%rdi, %rdi
	je	.L44
	movq	(%rdi), %rax
	jmp	*8(%rax)
	.p2align 4,,10
	.p2align 3
.L44:
	ret
	.cfi_endproc
.LFE7693:
	.size	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev, .-_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev
	.weak	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.set	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED2Ev
	.section	.rodata._ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_.str1.1,"aMS",@progbits,1
.LC0:
	.string	"vector::_M_realloc_insert"
	.section	.text._ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"axG",@progbits,_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,comdat
	.align 2
	.p2align 4
	.weak	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	.type	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_, @function
_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_:
.LFB7031:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA7031
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$40, %rsp
	.cfi_def_cfa_offset 96
	movq	8(%rdi), %r13
	movq	(%rdi), %rbp
	movq	%rdx, (%rsp)
	movabsq	$1152921504606846975, %rdx
	movq	%fs:40, %rax
	movq	%rax, 24(%rsp)
	xorl	%eax, %eax
	movq	%r13, %rax
	subq	%rbp, %rax
	sarq	$3, %rax
	cmpq	%rdx, %rax
	je	.L85
	movq	%rsi, %rcx
	movq	%rdi, %r12
	movq	%rsi, %rbx
	subq	%rbp, %rcx
	cmpq	%r13, %rbp
	je	.L86
	leaq	(%rax,%rax), %r15
	cmpq	%rax, %r15
	jb	.L69
	testq	%r15, %r15
	jne	.L87
	xorl	%r14d, %r14d
.L53:
	leaq	(%r14,%rcx), %rax
	movl	$16, %edi
	movq	$0, (%rax)
	movq	%rax, 8(%rsp)
.LEHB0:
	call	_Znwm@PLT
.LEHE0:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rsi
	movq	8(%rsp), %rdi
	movq	%rax, 16(%rsp)
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rdx
	movq	%rsi, (%rax)
	movq	(%rsp), %rsi
	movq	%rsi, 8(%rax)
	leaq	16(%rsp), %rsi
	movq	%rsi, (%rsp)
.LEHB1:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE@PLT
.LEHE1:
	movq	16(%rsp), %rdi
	testq	%rdi, %rdi
	je	.L54
	movq	(%rdi), %rax
	call	*8(%rax)
.L54:
	movq	%rbx, %rsi
	movq	%rbp, %rdx
	movq	%r14, %rax
	movq	%r14, %rcx
	subq	%rbp, %rsi
	cmpq	%rbp, %rbx
	je	.L56
	.p2align 4,,10
	.p2align 3
.L59:
	movq	$0, (%rax)
	movq	(%rdx), %rcx
	addq	$8, %rdx
	addq	$8, %rax
	movq	%rcx, -8(%rax)
	cmpq	%rbx, %rdx
	jne	.L59
	leaq	(%r14,%rsi), %rcx
.L56:
	addq	$8, %rcx
	cmpq	%r13, %rbx
	je	.L60
	subq	%rbx, %r13
	movq	%rcx, %rdi
	movq	%rbx, %rsi
	movq	%r13, %rdx
	call	memcpy@PLT
	movq	%rax, %rcx
	addq	%r13, %rcx
.L60:
	testq	%rbp, %rbp
	je	.L61
	movq	16(%r12), %rsi
	movq	%rbp, %rdi
	movq	%rcx, (%rsp)
	subq	%rbp, %rsi
	call	_ZdlPvm@PLT
	movq	(%rsp), %rcx
.L61:
	leaq	(%r14,%r15,8), %rax
	movq	%r14, (%r12)
	movq	%rcx, 8(%r12)
	movq	%rax, 16(%r12)
	movq	24(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L82
	addq	$40, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L69:
	.cfi_restore_state
	movabsq	$9223372036854775800, %rdi
	movq	%rdx, %r15
.L52:
	movq	%rcx, 8(%rsp)
.LEHB2:
	call	_Znwm@PLT
	movq	8(%rsp), %rcx
	movq	%rax, %r14
	jmp	.L53
	.p2align 4,,10
	.p2align 3
.L86:
	addq	$1, %rax
	jc	.L69
	movabsq	$1152921504606846975, %r15
	cmpq	%r15, %rax
	cmovbe	%rax, %r15
	leaq	0(,%r15,8), %rdi
	jmp	.L52
.L87:
	movabsq	$1152921504606846975, %rax
	cmpq	%rax, %r15
	cmova	%rax, %r15
	leaq	0(,%r15,8), %rdi
	jmp	.L52
.L57:
	movq	(%rsp), %rdi
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rbx, %rdi
.L58:
	call	__cxa_begin_catch@PLT
	testq	%r14, %r14
	je	.L88
	leaq	0(,%r15,8), %rsi
	movq	%r14, %rdi
	call	_ZdlPvm@PLT
.L63:
	movq	24(%rsp), %rax
	subq	%fs:40, %rax
	je	.L64
.L82:
	call	__stack_chk_fail@PLT
.L85:
	movq	24(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L82
	leaq	.LC0(%rip), %rdi
	call	_ZSt20__throw_length_errorPKc@PLT
.LEHE2:
.L71:
	endbr64
	movq	%rax, %rdi
	jmp	.L58
.L73:
	endbr64
	movq	%rax, %rbx
	jmp	.L57
.L88:
	movq	8(%rsp), %rax
	cmpq	$0, (%rax)
	je	.L63
	call	_ZSt9terminatev@PLT
.L64:
.LEHB3:
	call	__cxa_rethrow@PLT
.LEHE3:
.L72:
	endbr64
	movq	%rax, %rbx
.L65:
	call	__cxa_end_catch@PLT
	movq	24(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L82
	movq	%rbx, %rdi
.LEHB4:
	call	_Unwind_Resume@PLT
.LEHE4:
	.cfi_endproc
.LFE7031:
	.globl	__gxx_personality_v0
	.section	.gcc_except_table._ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"aG",@progbits,_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,comdat
	.align 4
.LLSDA7031:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT7031-.LLSDATTD7031
.LLSDATTD7031:
	.byte	0x1
	.uleb128 .LLSDACSE7031-.LLSDACSB7031
.LLSDACSB7031:
	.uleb128 .LEHB0-.LFB7031
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L71-.LFB7031
	.uleb128 0x1
	.uleb128 .LEHB1-.LFB7031
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L73-.LFB7031
	.uleb128 0x3
	.uleb128 .LEHB2-.LFB7031
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB7031
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L72-.LFB7031
	.uleb128 0
	.uleb128 .LEHB4-.LFB7031
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE7031:
	.byte	0x1
	.byte	0
	.byte	0
	.byte	0x7d
	.align 4
	.long	0

.LLSDATT7031:
	.section	.text._ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,"axG",@progbits,_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_,comdat
	.size	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_, .-_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC1:
	.string	"nproc="
.LC2:
	.string	"\n"
.LC3:
	.string	"single_thread_baseline=1\n"
.LC4:
	.string	"single_result="
.LC5:
	.string	"mutex_fastpath_exists=1\n"
.LC6:
	.string	"mutex_result="
.LC7:
	.string	"atomic_rmw_exists=1\n"
.LC8:
	.string	"atomic_result="
.LC9:
	.string	"cas_retry_observed="
.LC10:
	.string	"cas_result="
.LC11:
	.string	"insufficient_cores=1\n"
.LC12:
	.string	"cas_high_contention_tested=1\n"
.LC13:
	.string	"atomic_fetch_ns="
	.section	.text.unlikely,"ax",@progbits
.LCOLDB14:
	.section	.text.startup,"ax",@progbits
.LHOTB14:
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB6387:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA6387
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	leaq	_Z11bench_mutexv(%rip), %r15
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	leaq	.LC2(%rip), %r13
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	leaq	_ZSt4cout(%rip), %r12
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	movl	$4, %ebp
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$72, %rsp
	.cfi_def_cfa_offset 128
	movq	%fs:40, %rax
	movq	%rax, 56(%rsp)
	xorl	%eax, %eax
	leaq	32(%rsp), %r14
	call	_ZNSt6thread20hardware_concurrencyEv@PLT
	leaq	.LC1(%rip), %rsi
	movq	%r12, %rdi
	movl	%eax, %ebx
	movl	%eax, 12(%rsp)
.LEHB5:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movl	%ebx, %esi
	xorl	%ebx, %ebx
	movq	%rax, %rdi
	call	_ZNSo9_M_insertImEERSoT_@PLT
	movq	%r13, %rsi
	movq	%rax, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	leaq	.LC3(%rip), %rsi
	movq	%r12, %rdi
	addq	$200000, g_single(%rip)
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	leaq	.LC4(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	g_single(%rip), %rsi
	movq	%rax, %rdi
	call	_ZNSo9_M_insertIlEERSoT_@PLT
	movq	%r13, %rsi
	movq	%rax, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
.LEHE5:
	pxor	%xmm0, %xmm0
	leaq	24(%rsp), %rdx
	xorl	%eax, %eax
	movq	$0, 48(%rsp)
	movq	%rdx, (%rsp)
	movaps	%xmm0, 32(%rsp)
	cmpq	%rax, %rbx
	je	.L90
.L149:
	movq	$0, (%rbx)
	movl	$16, %edi
.LEHB6:
	call	_Znwm@PLT
.LEHE6:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rcx
	movq	%r15, 8(%rax)
	movq	(%rsp), %rsi
	movq	%rbx, %rdi
	movq	%rcx, (%rax)
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rdx
	movq	%rax, 24(%rsp)
.LEHB7:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE@PLT
.LEHE7:
	movq	24(%rsp), %rdi
	testq	%rdi, %rdi
	je	.L91
	movq	(%rdi), %rax
	call	*8(%rax)
.L91:
	addq	$8, %rbx
	movq	%rbx, 40(%rsp)
	subl	$1, %ebp
	je	.L95
.L150:
	movq	48(%rsp), %rax
	cmpq	%rax, %rbx
	jne	.L149
.L90:
	movq	%r15, %rdx
	movq	%rbx, %rsi
	movq	%r14, %rdi
.LEHB8:
	call	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	movq	40(%rsp), %rbx
	subl	$1, %ebp
	jne	.L150
.L95:
	movq	32(%rsp), %rbp
	cmpq	%rbp, %rbx
	je	.L100
	.p2align 4,,10
	.p2align 3
.L99:
	movq	%rbp, %rdi
	call	_ZNSt6thread4joinEv@PLT
	addq	$8, %rbp
	cmpq	%rbp, %rbx
	jne	.L99
.L100:
	leaq	.LC5(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	leaq	.LC6(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	g_mutex_cnt(%rip), %rsi
	movq	%rax, %rdi
	call	_ZNSo9_M_insertIlEERSoT_@PLT
	movq	%rax, %rdi
	movq	%r13, %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%r14, %rdi
	movl	$4, %ebp
	leaq	_Z18bench_atomic_fetchv(%rip), %r15
	call	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	leaq	24(%rsp), %rax
	movq	40(%rsp), %rbx
	movq	%rax, (%rsp)
.L105:
	cmpq	48(%rsp), %rbx
	je	.L101
	movq	$0, (%rbx)
	movl	$16, %edi
	call	_Znwm@PLT
.LEHE8:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rcx
	movq	%r15, 8(%rax)
	movq	(%rsp), %rsi
	movq	%rbx, %rdi
	movq	%rcx, (%rax)
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rdx
	movq	%rax, 24(%rsp)
.LEHB9:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE@PLT
.LEHE9:
	movq	24(%rsp), %rdi
	testq	%rdi, %rdi
	je	.L102
	movq	(%rdi), %rax
	call	*8(%rax)
.L102:
	addq	$8, %rbx
	movq	%rbx, 40(%rsp)
.L103:
	subl	$1, %ebp
	jne	.L105
	movq	32(%rsp), %rbp
	cmpq	%rbp, %rbx
	je	.L109
	.p2align 4,,10
	.p2align 3
.L108:
	movq	%rbp, %rdi
.LEHB10:
	call	_ZNSt6thread4joinEv@PLT
	addq	$8, %rbp
	cmpq	%rbp, %rbx
	jne	.L108
.L109:
	leaq	.LC7(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	leaq	.LC8(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%rax, %rdi
	movq	g_atomic_cnt(%rip), %rsi
	call	_ZNSo9_M_insertIlEERSoT_@PLT
	movq	%rax, %rdi
	movq	%r13, %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%r14, %rdi
	movl	$4, %ebp
	leaq	_Z16bench_atomic_casv(%rip), %r15
	call	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	leaq	24(%rsp), %rax
	movq	40(%rsp), %rbx
	movq	%rax, (%rsp)
.L114:
	cmpq	48(%rsp), %rbx
	je	.L110
	movq	$0, (%rbx)
	movl	$16, %edi
	call	_Znwm@PLT
.LEHE10:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rcx
	movq	%r15, 8(%rax)
	movq	(%rsp), %rsi
	movq	%rbx, %rdi
	movq	%rcx, (%rax)
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rdx
	movq	%rax, 24(%rsp)
.LEHB11:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE@PLT
.LEHE11:
	movq	24(%rsp), %rdi
	testq	%rdi, %rdi
	je	.L111
	movq	(%rdi), %rax
	call	*8(%rax)
.L111:
	addq	$8, %rbx
	movq	%rbx, 40(%rsp)
.L112:
	subl	$1, %ebp
	jne	.L114
	movq	32(%rsp), %rbp
	cmpq	%rbx, %rbp
	je	.L118
	.p2align 4,,10
	.p2align 3
.L117:
	movq	%rbp, %rdi
.LEHB12:
	call	_ZNSt6thread4joinEv@PLT
	addq	$8, %rbp
	cmpq	%rbp, %rbx
	jne	.L117
.L118:
	leaq	.LC9(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%rax, %rdi
	xorl	%esi, %esi
	movq	g_cas_retries(%rip), %rax
	testq	%rax, %rax
	setg	%sil
	call	_ZNSolsEi@PLT
	movq	%rax, %rdi
	movq	%r13, %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	leaq	.LC10(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%rax, %rdi
	movq	g_cas_target(%rip), %rsi
	call	_ZNSo9_M_insertIlEERSoT_@PLT
	movq	%rax, %rdi
	movq	%r13, %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	cmpl	$3, 12(%rsp)
	ja	.L119
	leaq	.LC11(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
.L120:
	call	_ZNSt6chrono3_V212steady_clock3nowEv@PLT
	movq	%rax, %rbp
	call	_Z18bench_atomic_fetchv
	call	_ZNSt6chrono3_V212steady_clock3nowEv@PLT
	leaq	.LC13(%rip), %rsi
	movq	%r12, %rdi
	movq	%rax, %rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%rbx, %rsi
	movq	%rax, %rdi
	subq	%rbp, %rsi
	call	_ZNSo9_M_insertIlEERSoT_@PLT
	movq	%rax, %rdi
	movq	%r13, %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
	movq	%r14, %rdi
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	movq	56(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L151
	addq	$72, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L110:
	.cfi_restore_state
	movq	%r15, %rdx
	movq	%rbx, %rsi
	movq	%r14, %rdi
	call	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	movq	40(%rsp), %rbx
	jmp	.L112
	.p2align 4,,10
	.p2align 3
.L101:
	movq	%r15, %rdx
	movq	%rbx, %rsi
	movq	%r14, %rdi
	call	_ZNSt6vectorISt6threadSaIS0_EE17_M_realloc_insertIJRFvvEEEEvN9__gnu_cxx17__normal_iteratorIPS0_S2_EEDpOT_
	movq	40(%rsp), %rbx
	jmp	.L103
.L119:
	leaq	.LC12(%rip), %rsi
	movq	%r12, %rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@PLT
.LEHE12:
	jmp	.L120
.L151:
	call	__stack_chk_fail@PLT
.L126:
	endbr64
	movq	%rax, %rbx
	jmp	.L113
.L125:
	endbr64
	movq	%rax, %rbx
	jmp	.L104
.L124:
	endbr64
	movq	%rax, %rbx
	jmp	.L93
.L123:
	endbr64
	movq	%rax, %rbx
	jmp	.L94
	.section	.gcc_except_table,"a",@progbits
.LLSDA6387:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6387-.LLSDACSB6387
.LLSDACSB6387:
	.uleb128 .LEHB5-.LFB6387
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB6387
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L123-.LFB6387
	.uleb128 0
	.uleb128 .LEHB7-.LFB6387
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L124-.LFB6387
	.uleb128 0
	.uleb128 .LEHB8-.LFB6387
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L123-.LFB6387
	.uleb128 0
	.uleb128 .LEHB9-.LFB6387
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L125-.LFB6387
	.uleb128 0
	.uleb128 .LEHB10-.LFB6387
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L123-.LFB6387
	.uleb128 0
	.uleb128 .LEHB11-.LFB6387
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L126-.LFB6387
	.uleb128 0
	.uleb128 .LEHB12-.LFB6387
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L123-.LFB6387
	.uleb128 0
.LLSDACSE6387:
	.section	.text.startup
	.cfi_endproc
	.section	.text.unlikely
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDAC6387
	.type	main.cold, @function
main.cold:
.LFSB6387:
.L113:
	.cfi_def_cfa_offset 128
	.cfi_offset 3, -56
	.cfi_offset 6, -48
	.cfi_offset 12, -40
	.cfi_offset 13, -32
	.cfi_offset 14, -24
	.cfi_offset 15, -16
	movq	(%rsp), %rdi
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L94:
	movq	%r14, %rdi
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	movq	56(%rsp), %rax
	subq	%fs:40, %rax
	jne	.L152
	movq	%rbx, %rdi
.LEHB13:
	call	_Unwind_Resume@PLT
.LEHE13:
.L104:
	movq	(%rsp), %rdi
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L94
.L152:
	call	__stack_chk_fail@PLT
.L93:
	movq	(%rsp), %rdi
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L94
	.cfi_endproc
.LFE6387:
	.section	.gcc_except_table
.LLSDAC6387:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6387-.LLSDACSBC6387
.LLSDACSBC6387:
	.uleb128 .LEHB13-.LCOLDB14
	.uleb128 .LEHE13-.LEHB13
	.uleb128 0
	.uleb128 0
.LLSDACSEC6387:
	.section	.text.unlikely
	.section	.text.startup
	.size	main, .-main
	.section	.text.unlikely
	.size	main.cold, .-main.cold
.LCOLDE14:
	.section	.text.startup
.LHOTE14:
	.weak	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.section	.rodata._ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,"aG",@progbits,_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,comdat
	.align 32
	.type	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE, @object
	.size	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE, 59
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE:
	.string	"NSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE"
	.weak	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.section	.data.rel.ro._ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,"awG",@progbits,_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,comdat
	.align 8
	.type	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE, @object
	.size	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE, 24
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.quad	_ZTINSt6thread6_StateE
	.weak	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.section	.data.rel.ro.local._ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,"awG",@progbits,_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE,comdat
	.align 8
	.type	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE, @object
	.size	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE, 40
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEE6_M_runEv
	.globl	g_single
	.bss
	.align 8
	.type	g_single, @object
	.size	g_single, 8
g_single:
	.zero	8
	.globl	g_cas_retries
	.align 8
	.type	g_cas_retries, @object
	.size	g_cas_retries, 8
g_cas_retries:
	.zero	8
	.globl	g_cas_target
	.align 8
	.type	g_cas_target, @object
	.size	g_cas_target, 8
g_cas_target:
	.zero	8
	.globl	g_atomic_cnt
	.align 8
	.type	g_atomic_cnt, @object
	.size	g_atomic_cnt, 8
g_atomic_cnt:
	.zero	8
	.globl	g_mutex_cnt
	.align 8
	.type	g_mutex_cnt, @object
	.size	g_mutex_cnt, 8
g_mutex_cnt:
	.zero	8
	.globl	g_mutex
	.align 32
	.type	g_mutex, @object
	.size	g_mutex, 40
g_mutex:
	.zero	40
	.hidden	DW.ref.__gxx_personality_v0
	.weak	DW.ref.__gxx_personality_v0
	.section	.data.rel.local.DW.ref.__gxx_personality_v0,"awG",@progbits,DW.ref.__gxx_personality_v0,comdat
	.align 8
	.type	DW.ref.__gxx_personality_v0, @object
	.size	DW.ref.__gxx_personality_v0, 8
DW.ref.__gxx_personality_v0:
	.quad	__gxx_personality_v0
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
