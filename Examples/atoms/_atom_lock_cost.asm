	.file	"_atom_lock_cost.cpp"
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB3615:
	.seh_endprologue
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
.LFB8328:
	.seh_endprologue
	rex.W jmp	*8(%rcx)
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.globl	_Z11bench_mutexv
	.def	_Z11bench_mutexv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11bench_mutexv
_Z11bench_mutexv:
.LFB6681:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movl	$200000, %ebx
	.p2align 4
	.p2align 3
.L6:
	leaq	g_mutex(%rip), %rcx
.LEHB0:
	call	pthread_mutex_lock
.LEHE0:
	testl	%eax, %eax
	jne	.L8
	leaq	g_mutex(%rip), %rcx
	addl	$1, g_mutex_cnt(%rip)
	call	pthread_mutex_unlock
	subl	$1, %ebx
	jne	.L6
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6681:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6681-.LLSDACSB6681
.LLSDACSB6681:
	.uleb128 .LEHB0-.LFB6681
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
.LLSDACSE6681:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z11bench_mutexv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z11bench_mutexv.cold
	.seh_stackalloc	40
	.seh_savereg	%rbx, 32
	.seh_endprologue
_Z11bench_mutexv.cold:
.L8:
	movl	%eax, %ecx
.LEHB1:
	call	_ZSt20__throw_system_errori
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC6681:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6681-.LLSDACSBC6681
.LLSDACSBC6681:
	.uleb128 .LEHB1-.LCOLDB0
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC6681:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.globl	_Z18bench_atomic_fetchv
	.def	_Z18bench_atomic_fetchv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18bench_atomic_fetchv
_Z18bench_atomic_fetchv:
.LFB6682:
	.seh_endprologue
	movl	$200000, %eax
	.p2align 4
	.p2align 4
	.p2align 3
.L10:
	lock addl	$1, g_atomic_cnt(%rip)
	lock addl	$1, g_atomic_cnt(%rip)
	subl	$2, %eax
	jne	.L10
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z16bench_atomic_casv
	.def	_Z16bench_atomic_casv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16bench_atomic_casv
_Z16bench_atomic_casv:
.LFB6683:
	.seh_endprologue
	movl	$200000, %edx
	.p2align 5
	.p2align 4
	.p2align 3
.L16:
	movl	g_cas_target(%rip), %eax
	leal	1(%rax), %ecx
	lock cmpxchgl	%ecx, g_cas_target(%rip)
	jne	.L15
.L14:
	subl	$1, %edx
	jne	.L16
	ret
.L15:
	lock addl	$1, g_cas_retries(%rip)
	leal	1(%rax), %ecx
	lock cmpxchgl	%ecx, g_cas_target(%rip)
	je	.L14
	jmp	.L15
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEED1Ev:
.LFB8324:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rax
	movq	%rax, (%rcx)
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
.LFB8325:
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	movq	%rcx, 40(%rsp)
	call	_ZNSt6thread6_StateD2Ev
	movq	40(%rsp), %rcx
	movl	$16, %edx
	addq	$56, %rsp
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	__tcfg_mutex;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcfg_mutex
__tcfg_mutex:
.LFB8327:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	g_mutex(%rip), %rcx
	call	pthread_mutex_destroy
	nop
	addq	$40, %rsp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA8327:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE8327-.LLSDACSB8327
.LLSDACSB8327:
.LLSDACSE8327:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.align 2
	.def	_ZNSt6vectorISt6threadSaIS0_EE12_Guard_allocD1Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EE12_Guard_allocD1Ev.isra.0
_ZNSt6vectorISt6threadSaIS0_EE12_Guard_allocD1Ev.isra.0:
.LFB9328:
	.seh_endprologue
	testq	%rcx, %rcx
	je	.L23
	salq	$3, %rdx
	jmp	_ZdlPvy
.L23:
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z12bench_singlev
	.def	_Z12bench_singlev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12bench_singlev
_Z12bench_singlev:
.LFB6680:
	.seh_endprologue
	addl	$200000, g_single(%rip)
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	.def	_ZNSt6vectorISt6threadSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EED1Ev
_ZNSt6vectorISt6threadSaIS0_EED1Ev:
.LFB7286:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	8(%rcx), %rdx
	movq	%rcx, %r8
	movq	(%rcx), %rcx
	cmpq	%rcx, %rdx
	je	.L27
	movq	%rcx, %rax
	.p2align 4
	.p2align 4
	.p2align 3
.L29:
	cmpq	$0, (%rax)
	jne	.L32
	addq	$8, %rax
	cmpq	%rax, %rdx
	jne	.L29
.L27:
	testq	%rcx, %rcx
	je	.L26
	movq	16(%r8), %rdx
	subq	%rcx, %rdx
	addq	$40, %rsp
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L26:
	addq	$40, %rsp
	ret
.L32:
	call	_ZSt9terminatev
	nop
	.seh_endproc
	.section	.text$_ZNSt6vectorISt6threadSaIS0_EE5clearEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	.def	_ZNSt6vectorISt6threadSaIS0_EE5clearEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
_ZNSt6vectorISt6threadSaIS0_EE5clearEv:
.LFB7289:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movq	(%rcx), %r8
	movq	8(%rcx), %rdx
	cmpq	%rdx, %r8
	je	.L33
	movq	%r8, %rax
	.p2align 4
	.p2align 4
	.p2align 3
.L36:
	cmpq	$0, (%rax)
	jne	.L38
	addq	$8, %rax
	cmpq	%rax, %rdx
	jne	.L36
	movq	%r8, 8(%rcx)
.L33:
	addq	$40, %rsp
	ret
.L38:
	call	_ZSt9terminatev
	nop
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB8074:
	.seh_endprologue
	movq	(%rcx), %rcx
	testq	%rcx, %rcx
	je	.L39
	movq	(%rcx), %rax
	rex.W jmp	*8(%rax)
	.p2align 4,,10
	.p2align 3
.L39:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "nproc=\0"
.LC2:
	.ascii "\12\0"
.LC3:
	.ascii "single_thread_baseline=1\12\0"
.LC4:
	.ascii "single_result=\0"
.LC5:
	.ascii "vector::_M_realloc_append\0"
.LC6:
	.ascii "mutex_fastpath_exists=1\12\0"
.LC7:
	.ascii "mutex_result=\0"
.LC8:
	.ascii "atomic_rmw_exists=1\12\0"
.LC9:
	.ascii "atomic_result=\0"
.LC10:
	.ascii "cas_retry_observed=\0"
.LC11:
	.ascii "cas_result=\0"
.LC12:
	.ascii "insufficient_cores=1\12\0"
.LC13:
	.ascii "cas_high_contention_tested=1\12\0"
.LC14:
	.ascii "atomic_fetch_ns=\0"
	.section	.text.unlikely,"x"
.LCOLDB15:
	.section	.text.startup,"x"
.LHOTB15:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB6684:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$136, %rsp
	.seh_stackalloc	136
	.seh_endprologue
	xorl	%r12d, %r12d
	xorl	%ebx, %ebx
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvvEEEEEEE(%rip), %r14
	call	__main
	call	_ZNSt6thread20hardware_concurrencyEv
	movq	.refptr._ZSt4cout(%rip), %rsi
	leaq	.LC1(%rip), %rdx
	movl	%eax, %edi
	movl	%eax, 76(%rsp)
	movq	%rsi, %rcx
	movq	%rsi, 48(%rsp)
.LEHB2:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	%edi, %edx
	movl	$4, %edi
	movq	%rax, %rcx
	call	_ZNSo9_M_insertImEERSoT_
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	leaq	.LC3(%rip), %rdx
	movq	%rsi, %rcx
	addl	$200000, g_single(%rip)
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	leaq	.LC4(%rip), %rdx
	movq	%rsi, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	g_single(%rip), %edx
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIlEERSoT_
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE2:
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rax
	pxor	%xmm0, %xmm0
	movq	$0, 112(%rsp)
	movq	%rax, 40(%rsp)
	leaq	88(%rsp), %rax
	movq	%rax, 32(%rsp)
	movaps	%xmm0, 96(%rsp)
	cmpq	%r12, %rbx
	je	.L42
.L159:
	movq	$0, (%rbx)
	movl	$16, %ecx
	leaq	96(%rsp), %rsi
.LEHB3:
	call	_Znwy
.LEHE3:
	movq	40(%rsp), %r8
	movq	32(%rsp), %rdx
	movq	%r14, (%rax)
	movq	%rbx, %rcx
	leaq	_Z11bench_mutexv(%rip), %rsi
	movq	%rax, 88(%rsp)
	movq	%rsi, 8(%rax)
.LEHB4:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE4:
	movq	88(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L43
	movq	(%rcx), %rax
	call	*8(%rax)
.L43:
	addq	$8, %rbx
	movq	%rbx, 104(%rsp)
	subl	$1, %edi
	je	.L55
.L160:
	movq	112(%rsp), %r12
	cmpq	%r12, %rbx
	jne	.L159
.L42:
	movq	96(%rsp), %r13
	movq	%rbx, %r9
	movabsq	$1152921504606846975, %rsi
	subq	%r13, %r9
	movq	%r9, %rax
	sarq	$3, %rax
	cmpq	%rsi, %rax
	je	.L149
	testq	%rax, %rax
	movl	$1, %ebp
	movq	%r9, 56(%rsp)
	leaq	96(%rsp), %rsi
	cmovne	%rax, %rbp
	addq	%rax, %rbp
	movabsq	$1152921504606846975, %rax
	cmpq	%rax, %rbp
	cmova	%rax, %rbp
	leaq	0(,%rbp,8), %r15
	movq	%r15, %rcx
.LEHB5:
	call	_Znwy
.LEHE5:
	movq	56(%rsp), %r9
	movl	$16, %ecx
	movq	%rax, %rsi
	addq	%rax, %r9
	movq	$0, (%r9)
	movq	%r9, 56(%rsp)
.LEHB6:
	call	_Znwy
.LEHE6:
	leaq	_Z11bench_mutexv(%rip), %rdx
	movq	%r14, (%rax)
	movq	40(%rsp), %r8
	movq	%rdx, 8(%rax)
	movq	56(%rsp), %rcx
	movq	32(%rsp), %rdx
	movq	%rax, 88(%rsp)
.LEHB7:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE7:
	movq	88(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L48
	movq	(%rcx), %rax
	call	*8(%rax)
.L48:
	movq	%rsi, %rax
	cmpq	%r13, %rbx
	je	.L50
	subq	%r13, %rbx
	movq	%r13, %rdx
	leaq	(%rsi,%rbx), %r8
	.p2align 5
	.p2align 4
	.p2align 3
.L53:
	movq	(%rdx), %rcx
	addq	$8, %rax
	addq	$8, %rdx
	movq	%rcx, -8(%rax)
	cmpq	%r8, %rax
	jne	.L53
.L50:
	leaq	8(%rax), %rbx
	testq	%r13, %r13
	je	.L54
	movq	%r12, %rdx
	movq	%r13, %rcx
	subq	%r13, %rdx
	call	_ZdlPvy
.L54:
	leaq	(%rsi,%r15), %rax
	movq	%rsi, 96(%rsp)
	movq	%rbx, 104(%rsp)
	movq	%rax, 112(%rsp)
	subl	$1, %edi
	jne	.L160
.L55:
	movq	96(%rsp), %rdi
	cmpq	%rbx, %rdi
	je	.L60
	.p2align 4
	.p2align 3
.L59:
	movq	%rdi, %rcx
	leaq	96(%rsp), %rsi
.LEHB8:
	call	_ZNSt6thread4joinEv
	addq	$8, %rdi
	cmpq	%rdi, %rbx
	jne	.L59
.L60:
	movq	48(%rsp), %rcx
	leaq	.LC6(%rip), %rdx
	leaq	96(%rsp), %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	48(%rsp), %rcx
	leaq	.LC7(%rip), %rdx
	leaq	96(%rsp), %rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movl	g_mutex_cnt(%rip), %edx
	movq	%rax, %rcx
	call	_ZNSo9_M_insertIlEERSoT_
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	%rsi, %rcx
	movl	$4, %edi
	call	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	movq	104(%rsp), %rbx
.L72:
	cmpq	%rbx, 112(%rsp)
	je	.L61
	movq	$0, (%rbx)
	movl	$16, %ecx
	call	_Znwy
.LEHE8:
	leaq	_Z18bench_atomic_fetchv(%rip), %rdx
	movq	%r14, (%rax)
	movq	40(%rsp), %r8
	movq	%rbx, %rcx
	movq	%rdx, 8(%rax)
	movq	32(%rsp), %rdx
	movq	%rax, 88(%rsp)
.LEHB9:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE9:
	movq	88(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L62
	movq	(%rcx), %rax
	call	*8(%rax)
.L62:
	addq	$8, %rbx
	movq	%rbx, 104(%rsp)
.L63:
	subl	$1, %edi
	jne	.L72
	movq	96(%rsp), %rdi
	cmpq	%rbx, %rdi
	je	.L76
	.p2align 4
	.p2align 3
.L75:
	movq	%rdi, %rcx
.LEHB10:
	call	_ZNSt6thread4joinEv
	addq	$8, %rdi
	cmpq	%rdi, %rbx
	jne	.L75
.L76:
	movq	48(%rsp), %rcx
	leaq	.LC8(%rip), %rdx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	48(%rsp), %rcx
	leaq	.LC9(%rip), %rdx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	%rax, %rcx
	movl	g_atomic_cnt(%rip), %edx
	call	_ZNSo9_M_insertIlEERSoT_
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	%rsi, %rcx
	movl	$4, %edi
	call	_ZNSt6vectorISt6threadSaIS0_EE5clearEv
	movq	104(%rsp), %rbx
.L88:
	cmpq	%rbx, 112(%rsp)
	je	.L77
	movq	$0, (%rbx)
	movl	$16, %ecx
	call	_Znwy
.LEHE10:
	leaq	_Z16bench_atomic_casv(%rip), %rdx
	movq	%r14, (%rax)
	movq	40(%rsp), %r8
	movq	%rbx, %rcx
	movq	%rdx, 8(%rax)
	movq	32(%rsp), %rdx
	movq	%rax, 88(%rsp)
.LEHB11:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE11:
	movq	88(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L78
	movq	(%rcx), %rax
	call	*8(%rax)
.L78:
	addq	$8, %rbx
	movq	%rbx, 104(%rsp)
.L79:
	subl	$1, %edi
	jne	.L88
	movq	96(%rsp), %rdi
	cmpq	%rdi, %rbx
	je	.L92
	.p2align 4
	.p2align 3
.L91:
	movq	%rdi, %rcx
.LEHB12:
	call	_ZNSt6thread4joinEv
	addq	$8, %rdi
	cmpq	%rdi, %rbx
	jne	.L91
.L92:
	movq	48(%rsp), %rcx
	leaq	.LC10(%rip), %rdx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	%rax, %rcx
	movl	g_cas_retries(%rip), %edx
	testl	%edx, %edx
	setg	%dl
	movzbl	%dl, %edx
	call	_ZNSolsEi
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	48(%rsp), %rdi
	leaq	.LC11(%rip), %rdx
	movq	%rdi, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	%rax, %rcx
	movl	g_cas_target(%rip), %edx
	call	_ZNSo9_M_insertIlEERSoT_
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	cmpl	$3, 76(%rsp)
	ja	.L93
	leaq	.LC12(%rip), %rdx
	movq	%rdi, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.L94:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rdi
	call	_Z18bench_atomic_fetchv
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	48(%rsp), %rcx
	leaq	.LC14(%rip), %rdx
	movq	%rax, %rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	subq	%rdi, %rbx
	movq	%rax, %rcx
	movq	%rbx, %rdx
	call	_ZNSo9_M_insertIxEERSoT_
	leaq	.LC2(%rip), %rdx
	movq	%rax, %rcx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movq	%rsi, %rcx
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	xorl	%eax, %eax
	addq	$136, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
	.p2align 4,,10
	.p2align 3
.L77:
	movq	96(%rsp), %r12
	movq	%rbx, %r15
	movabsq	$1152921504606846975, %rdx
	subq	%r12, %r15
	movq	%r15, %rax
	sarq	$3, %rax
	cmpq	%rdx, %rax
	je	.L151
	testq	%rax, %rax
	movl	$1, %ebp
	cmovne	%rax, %rbp
	addq	%rax, %rbp
	movabsq	$1152921504606846975, %rax
	cmpq	%rax, %rbp
	cmova	%rax, %rbp
	leaq	0(,%rbp,8), %rax
	movq	%rax, %rcx
	movq	%rax, 56(%rsp)
	call	_Znwy
.LEHE12:
	leaq	(%rax,%r15), %r9
	movl	$16, %ecx
	movq	%rax, %r13
	movq	$0, (%r9)
	movq	%r9, 64(%rsp)
.LEHB13:
	call	_Znwy
.LEHE13:
	leaq	_Z16bench_atomic_casv(%rip), %rdx
	movq	%r14, (%rax)
	movq	40(%rsp), %r8
	movq	%rdx, 8(%rax)
	movq	64(%rsp), %rcx
	movq	32(%rsp), %rdx
	movq	%rax, 88(%rsp)
.LEHB14:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE14:
	movq	88(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L82
	movq	(%rcx), %rax
	call	*8(%rax)
.L82:
	movq	%r12, %rax
	movq	%r13, %rdx
	cmpq	%rbx, %r12
	je	.L161
	.p2align 5
	.p2align 4
	.p2align 3
.L83:
	movq	(%rax), %rcx
	addq	$8, %rax
	addq	$8, %rdx
	movq	%rcx, -8(%rdx)
	cmpq	%rbx, %rax
	jne	.L83
	subq	%r12, %rax
	addq	%r13, %rax
.L84:
	leaq	8(%rax), %rbx
	testq	%r12, %r12
	je	.L87
	movq	%r15, %rdx
	movq	%r12, %rcx
	call	_ZdlPvy
.L87:
	movq	56(%rsp), %r15
	movq	%r13, 96(%rsp)
	movq	%rbx, 104(%rsp)
	addq	%r13, %r15
	movq	%r15, 112(%rsp)
	jmp	.L79
	.p2align 4,,10
	.p2align 3
.L61:
	movq	96(%rsp), %r12
	movq	%rbx, %r15
	movabsq	$1152921504606846975, %rdx
	subq	%r12, %r15
	movq	%r15, %rax
	sarq	$3, %rax
	cmpq	%rdx, %rax
	je	.L150
	testq	%rax, %rax
	movl	$1, %ebp
	cmovne	%rax, %rbp
	addq	%rax, %rbp
	movabsq	$1152921504606846975, %rax
	cmpq	%rax, %rbp
	cmova	%rax, %rbp
	leaq	0(,%rbp,8), %rax
	movq	%rax, %rcx
	movq	%rax, 56(%rsp)
.LEHB15:
	call	_Znwy
.LEHE15:
	leaq	(%rax,%r15), %r9
	movl	$16, %ecx
	movq	%rax, %r13
	movq	$0, (%r9)
	movq	%r9, 64(%rsp)
.LEHB16:
	call	_Znwy
.LEHE16:
	leaq	_Z18bench_atomic_fetchv(%rip), %rdx
	movq	%r14, (%rax)
	movq	40(%rsp), %r8
	movq	%rdx, 8(%rax)
	movq	64(%rsp), %rcx
	movq	32(%rsp), %rdx
	movq	%rax, 88(%rsp)
.LEHB17:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE17:
	movq	88(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L66
	movq	(%rcx), %rax
	call	*8(%rax)
.L66:
	movq	%r12, %rax
	movq	%r13, %rdx
	cmpq	%rbx, %r12
	je	.L162
	.p2align 5
	.p2align 4
	.p2align 3
.L67:
	movq	(%rax), %rcx
	addq	$8, %rax
	addq	$8, %rdx
	movq	%rcx, -8(%rdx)
	cmpq	%rbx, %rax
	jne	.L67
	subq	%r12, %rax
	addq	%r13, %rax
.L68:
	leaq	8(%rax), %rbx
	testq	%r12, %r12
	je	.L71
	movq	%r15, %rdx
	movq	%r12, %rcx
	call	_ZdlPvy
.L71:
	movq	56(%rsp), %r15
	movq	%r13, 96(%rsp)
	movq	%rbx, 104(%rsp)
	addq	%r13, %r15
	movq	%r15, 112(%rsp)
	jmp	.L63
.L93:
	movq	48(%rsp), %rcx
	leaq	.LC13(%rip), %rdx
.LEHB18:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE18:
	jmp	.L94
.L161:
	movq	%r13, %rax
	jmp	.L84
.L162:
	movq	%r13, %rax
	jmp	.L68
.L103:
	movq	%rax, %rbx
	jmp	.L69
.L101:
	movq	%rax, %rbx
	jmp	.L80
.L106:
	movq	%rax, %rbx
	jmp	.L85
.L100:
	movq	%rax, %rbx
	jmp	.L51
.L105:
	movq	%rax, %rbx
	jmp	.L86
.L104:
	movq	%rax, %rbx
	jmp	.L80
.L98:
	movq	%rax, %rbx
	jmp	.L45
.L147:
	jmp	.L148
.L102:
	movq	%rax, %rbx
	jmp	.L86
.L99:
	movq	%rax, %rbx
	jmp	.L52
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA6684:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE6684-.LLSDACSB6684
.LLSDACSB6684:
	.uleb128 .LEHB2-.LFB6684
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB3-.LFB6684
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L147-.LFB6684
	.uleb128 0
	.uleb128 .LEHB4-.LFB6684
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L98-.LFB6684
	.uleb128 0
	.uleb128 .LEHB5-.LFB6684
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L147-.LFB6684
	.uleb128 0
	.uleb128 .LEHB6-.LFB6684
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L99-.LFB6684
	.uleb128 0
	.uleb128 .LEHB7-.LFB6684
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L100-.LFB6684
	.uleb128 0
	.uleb128 .LEHB8-.LFB6684
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L147-.LFB6684
	.uleb128 0
	.uleb128 .LEHB9-.LFB6684
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L101-.LFB6684
	.uleb128 0
	.uleb128 .LEHB10-.LFB6684
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L147-.LFB6684
	.uleb128 0
	.uleb128 .LEHB11-.LFB6684
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L104-.LFB6684
	.uleb128 0
	.uleb128 .LEHB12-.LFB6684
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L147-.LFB6684
	.uleb128 0
	.uleb128 .LEHB13-.LFB6684
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L105-.LFB6684
	.uleb128 0
	.uleb128 .LEHB14-.LFB6684
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L106-.LFB6684
	.uleb128 0
	.uleb128 .LEHB15-.LFB6684
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L147-.LFB6684
	.uleb128 0
	.uleb128 .LEHB16-.LFB6684
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L102-.LFB6684
	.uleb128 0
	.uleb128 .LEHB17-.LFB6684
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L103-.LFB6684
	.uleb128 0
	.uleb128 .LEHB18-.LFB6684
	.uleb128 .LEHE18-.LEHB18
	.uleb128 .L147-.LFB6684
	.uleb128 0
.LLSDACSE6684:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	200
	.seh_savereg	%rbx, 136
	.seh_savereg	%rsi, 144
	.seh_savereg	%rdi, 152
	.seh_savereg	%rbp, 160
	.seh_savereg	%r12, 168
	.seh_savereg	%r13, 176
	.seh_savereg	%r14, 184
	.seh_savereg	%r15, 192
	.seh_endprologue
main.cold:
.L69:
	movq	32(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L86:
	movq	%rbp, %rdx
	movq	%r13, %rcx
	call	_ZNSt6vectorISt6threadSaIS0_EE12_Guard_allocD1Ev.isra.0
.L46:
	movq	%rsi, %rcx
	call	_ZNSt6vectorISt6threadSaIS0_EED1Ev
	movq	%rbx, %rcx
.LEHB19:
	call	_Unwind_Resume
.LEHE19:
.L80:
	movq	32(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L46
.L85:
	movq	32(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L86
.L51:
	movq	32(%rsp), %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L52:
	movq	%rsi, %rcx
	movq	%rbp, %rdx
	leaq	96(%rsp), %rsi
	call	_ZNSt6vectorISt6threadSaIS0_EE12_Guard_allocD1Ev.isra.0
	jmp	.L46
.L151:
	leaq	.LC5(%rip), %rcx
.LEHB20:
	call	_ZSt20__throw_length_errorPKc
.L97:
.L148:
	movq	%rax, %rbx
	jmp	.L46
.L45:
	movq	32(%rsp), %rcx
	leaq	96(%rsp), %rsi
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L46
.L150:
	leaq	.LC5(%rip), %rcx
	call	_ZSt20__throw_length_errorPKc
.L149:
	leaq	.LC5(%rip), %rcx
	leaq	96(%rsp), %rsi
	call	_ZSt20__throw_length_errorPKc
	nop
.LEHE20:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC6684:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC6684-.LLSDACSBC6684
.LLSDACSBC6684:
	.uleb128 .LEHB19-.LCOLDB15
	.uleb128 .LEHE19-.LEHB19
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB20-.LCOLDB15
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L97-.LCOLDB15
	.uleb128 0
.LLSDACSEC6684:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE15:
	.section	.text.startup,"x"
.LHOTE15:
	.p2align 4
	.def	_GLOBAL__sub_I_g_mutex;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I_g_mutex
_GLOBAL__sub_I_g_mutex:
.LFB9325:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	xorl	%edx, %edx
	leaq	g_mutex(%rip), %rcx
	call	pthread_mutex_init
	leaq	__tcfg_mutex(%rip), %rcx
	addq	$40, %rsp
.LEHB21:
	jmp	atexit
.LEHE21:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA9325:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9325-.LLSDACSB9325
.LLSDACSB9325:
	.uleb128 .LEHB21-.LFB9325
	.uleb128 .LEHE21-.LEHB21
	.uleb128 0
	.uleb128 0
.LLSDACSE9325:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I_g_mutex
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
	.globl	g_single
	.bss
	.align 4
g_single:
	.space 4
	.globl	g_cas_retries
	.align 4
g_cas_retries:
	.space 4
	.globl	g_cas_target
	.align 4
g_cas_target:
	.space 4
	.globl	g_atomic_cnt
	.align 4
g_atomic_cnt:
	.space 4
	.globl	g_mutex_cnt
	.align 4
g_mutex_cnt:
	.space 4
	.globl	g_mutex
	.align 8
g_mutex:
	.space 8
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread20hardware_concurrencyEv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertImEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIxEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
