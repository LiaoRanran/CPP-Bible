	.file	"_ch120_coro_perf.cpp"
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB5958:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE
	.def	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE
_Z13resume_handleRNSt7__n486116coroutine_handleIvEE:
.LFB12897:
	.seh_endprologue
	movq	(%rcx), %rcx
	rex.W jmp	*(%rcx)
	.seh_endproc
	.p2align 4
	.globl	_Z10yield_stepR3GenIiE
	.def	_Z10yield_stepR3GenIiE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10yield_stepR3GenIiE
_Z10yield_stepR3GenIiE:
.LFB12898:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	(%rcx), %rax
	movq	%rcx, %rbx
	movq	%rax, %rcx
	call	*(%rax)
	movq	(%rbx), %rax
	movl	16(%rax), %eax
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.p2align 4
	.def	_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.actor
_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.actor:
.LFB12913:
	.seh_endprologue
	movzwl	32(%rcx), %eax
	testb	$1, %al
	je	.L6
	cmpw	$9, %ax
	ja	.L7
	movl	$682, %edx
	btq	%rax, %rdx
	jnc	.L7
.L8:
	cmpb	$0, 34(%rcx)
	jne	.L15
.L14:
.L5:
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	cmpw	$8, %ax
	ja	.L7
	leaq	.L9(%rip), %rdx
	movslq	(%rdx,%rax,4), %rax
	addq	%rdx, %rax
	jmp	*%rax
	.section .rdata,"dr"
	.align 4
.L9:
	.long	.L13-.L9
	.long	.L7-.L9
	.long	.L12-.L9
	.long	.L7-.L9
	.long	.L11-.L9
	.long	.L7-.L9
	.long	.L10-.L9
	.long	.L7-.L9
	.long	.L8-.L9
	.text
	.p2align 4,,10
	.p2align 3
.L13:
	movq	%rcx, 24(%rcx)
.L12:
	movb	$1, 35(%rcx)
.L11:
	movl	$42, 40(%rcx)
.L10:
	cmpb	$0, 34(%rcx)
	movl	$42, 44(%rcx)
	movq	$0, (%rcx)
	je	.L5
.L15:
	jmp	free
.L7:
	ud2
	.seh_endproc
	.p2align 4
	.def	_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.destroy
_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.destroy:
.LFB12914:
	.seh_endprologue
	orw	$1, 32(%rcx)
	jmp	_Z10ready_taskPZ10ready_taskvE21_Z10ready_taskv.Frame.actor
	.seh_endproc
	.p2align 4
	.def	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.actor
_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.actor:
.LFB12892:
	.seh_endprologue
	movzwl	32(%rcx), %eax
	testb	$1, %al
	je	.L18
	cmpw	$5, %ax
	ja	.L19
	movl	$42, %edx
	btq	%rax, %rdx
	jnc	.L19
	cmpb	$0, 34(%rcx)
	jne	.L27
.L25:
	ret
	.p2align 4,,10
	.p2align 3
.L18:
	cmpw	$2, %ax
	je	.L21
	cmpw	$4, %ax
	jne	.L28
	movl	40(%rcx), %eax
	leal	1(%rax), %edx
.L24:
.L26:
	movl	%eax, 16(%rcx)
	movl	$4, %eax
	movl	%edx, 40(%rcx)
	movw	%ax, 32(%rcx)
	ret
	.p2align 4,,10
	.p2align 3
.L28:
	testw	%ax, %ax
	jne	.L19
	movl	$2, %edx
	movq	%rcx, 24(%rcx)
	movb	$0, 35(%rcx)
	movw	%dx, 32(%rcx)
	ret
	.p2align 4,,10
	.p2align 3
.L27:
	jmp	free
	.p2align 4,,10
	.p2align 3
.L21:
	movb	$1, 35(%rcx)
	movl	$1, %edx
	xorl	%eax, %eax
	jmp	.L26
.L19:
	ud2
	.seh_endproc
	.p2align 4
	.def	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.destroy
_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.destroy:
.LFB12893:
	.seh_endprologue
	orw	$1, 32(%rcx)
	jmp	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.actor
	.seh_endproc
	.p2align 4
	.def	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.actor
_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.actor:
.LFB12895:
	.seh_endprologue
	movzwl	36(%rcx), %eax
	testb	$1, %al
	je	.L31
	cmpw	$7, %ax
	ja	.L32
	movl	$170, %edx
	btq	%rax, %rdx
	jnc	.L32
.L33:
	cmpb	$0, 38(%rcx)
	jne	.L45
.L38:
	ret
	.p2align 4,,10
	.p2align 3
.L31:
	cmpw	$4, %ax
	je	.L34
	ja	.L35
	testw	%ax, %ax
	je	.L36
	xorl	%eax, %eax
	cmpl	%eax, 32(%rcx)
	movb	$1, 39(%rcx)
	movl	%eax, 44(%rcx)
	jg	.L40
.L46:
	movl	$6, %eax
	movq	$0, (%rcx)
	movw	%ax, 36(%rcx)
	ret
	.p2align 4,,10
	.p2align 3
.L45:
	jmp	free
	.p2align 4,,10
	.p2align 3
.L36:
	movl	$2, %r8d
	movq	%rcx, 24(%rcx)
	movb	$0, 39(%rcx)
	movw	%r8w, 36(%rcx)
	ret
	.p2align 4,,10
	.p2align 3
.L34:
	movl	44(%rcx), %eax
	addl	$1, %eax
	cmpl	%eax, 32(%rcx)
	movl	%eax, 44(%rcx)
	jle	.L46
.L40:
	movl	$4, %edx
	movl	%eax, 16(%rcx)
	movw	%dx, 36(%rcx)
	ret
	.p2align 4,,10
	.p2align 3
.L35:
	cmpw	$6, %ax
	je	.L33
.L32:
	ud2
	.seh_endproc
	.p2align 4
	.def	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.destroy
_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.destroy:
.LFB12896:
	.seh_endprologue
	orw	$1, 36(%rcx)
	jmp	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.actor
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev:
.LFB14487:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev:
.LFB14489:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE(%rip), %rax
	movq	%rcx, %rbx
	movq	%rax, (%rcx)
	call	_ZNSt6thread6_StateD2Ev
	movq	%rbx, %rcx
	addq	$32, %rsp
	popq	%rbx
	jmp	free
	.seh_endproc
	.p2align 4
	.def	_ZL6printfPKcz;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz
_ZL6printfPKcz:
.LFB443:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	88(%rsp), %rsi
	movq	%rcx, %rbx
	movq	%rdx, 88(%rsp)
	movl	$1, %ecx
	movq	%r8, 96(%rsp)
	movq	%r9, 104(%rsp)
	movq	%rsi, 40(%rsp)
	call	*__imp___acrt_iob_func(%rip)
	movq	%rsi, %r8
	movq	%rbx, %rdx
	movq	%rax, %rcx
	call	__mingw_vfprintf
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10ready_taskv
	.def	_Z10ready_taskv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10ready_taskv
_Z10ready_taskv:
.LFB12910:
	.seh_endprologue
	cmpq	$55, _ZL11g_max_frame(%rip)
	ja	.L51
	movq	$56, _ZL11g_max_frame(%rip)
.L52:
.L51:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB12870:
	.seh_endprologue
	cmpq	%rcx, _ZL11g_max_frame(%rip)
	jnb	.L54
	movq	%rcx, _ZL11g_max_frame(%rip)
.L54:
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB12871:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB12872:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_Z16infinite_counterv
	.def	_Z16infinite_counterv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterv
_Z16infinite_counterv:
.LFB12891:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	cmpq	$47, _ZL11g_max_frame(%rip)
	movq	%rcx, %rbx
	ja	.L60
	movq	$48, _ZL11g_max_frame(%rip)
.L58:
.L59:
.L60:
	movl	$48, %ecx
	call	malloc
	leaq	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.destroy(%rip), %rdx
	leaq	_Z16infinite_counterPZ16infinite_countervE27_Z16infinite_counterv.Frame.actor(%rip), %rcx
	movq	%rdx, %xmm1
	movq	%rax, (%rbx)
	movq	%rcx, %xmm0
	movq	%rax, 24(%rax)
	movl	$65538, 32(%rax)
	punpcklqdq	%xmm1, %xmm0
	movups	%xmm0, (%rax)
	movq	%rbx, %rax
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13small_counteri
	.def	_Z13small_counteri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13small_counteri
_Z13small_counteri:
.LFB12894:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	cmpq	$55, _ZL11g_max_frame(%rip)
	movq	%rcx, %rbx
	movl	%edx, %esi
	ja	.L62
	movq	$56, _ZL11g_max_frame(%rip)
.L62:
	movl	$56, %ecx
	call	malloc
	leaq	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.destroy(%rip), %rdx
	leaq	_Z13small_counterPZ13small_counteriE24_Z13small_counteri.Frame.actor(%rip), %rcx
	movq	%rdx, %xmm1
	movl	%esi, 32(%rax)
	movq	%rcx, %xmm0
	movq	%rax, (%rbx)
	movq	%rax, 24(%rax)
	punpcklqdq	%xmm1, %xmm0
	movl	$65538, 36(%rax)
	movups	%xmm0, (%rax)
	movq	%rbx, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.seh_endproc
	.section	.text$_ZNSt11unique_lockISt5mutexE6unlockEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt11unique_lockISt5mutexE6unlockEv
	.def	_ZNSt11unique_lockISt5mutexE6unlockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt11unique_lockISt5mutexE6unlockEv
_ZNSt11unique_lockISt5mutexE6unlockEv:
.LFB13540:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	cmpb	$0, 8(%rcx)
	movq	%rcx, %rbx
	je	.L69
	movq	(%rcx), %rcx
	testq	%rcx, %rcx
	je	.L63
	call	pthread_mutex_unlock
	movb	$0, 8(%rbx)
.L63:
	addq	$32, %rsp
	popq	%rbx
	ret
.L69:
	movl	$1, %ecx
	call	_ZSt20__throw_system_errori
	nop
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv:
.LFB14663:
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
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	movq	%rcx, %rbx
	movq	8(%rcx), %rcx
	movb	$0, 40(%rsp)
	testq	%rcx, %rcx
	movq	%rcx, 32(%rsp)
	je	.L79
	leaq	32(%rsp), %rbp
	xorl	%r12d, %r12d
	jmp	.L71
	.p2align 4,,10
	.p2align 3
.L73:
	movq	32(%rbx), %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jne	.L75
	movq	24(%rbx), %rax
	addq	$7, %r12
	cmpb	$0, 40(%rsp)
	movl	$0, (%rax)
	je	.L98
	movq	32(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L77
.LEHB0:
	call	pthread_mutex_unlock
.LEHE0:
	movb	$0, 40(%rsp)
.L77:
	movq	16(%rbx), %rcx
	call	_ZNSt18condition_variable10notify_oneEv
	cmpb	$0, 40(%rsp)
	jne	.L99
.L78:
	movq	8(%rbx), %rcx
	movb	$0, 40(%rsp)
	testq	%rcx, %rcx
	movq	%rcx, 32(%rsp)
	je	.L79
.L71:
.LEHB1:
	call	pthread_mutex_lock
.LEHE1:
	testl	%eax, %eax
	jne	.L100
	movq	16(%rbx), %rdi
	movb	$1, 40(%rsp)
	movq	24(%rbx), %rsi
	movq	32(%rbx), %r13
	.p2align 4,,10
	.p2align 3
.L74:
	cmpl	$1, (%rsi)
	je	.L73
	movzbl	0(%r13), %eax
	testb	%al, %al
	jne	.L73
	movq	%rbp, %rdx
	movq	%rdi, %rcx
.LEHB2:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE2:
	jmp	.L74
	.p2align 4,,10
	.p2align 3
.L99:
	movq	32(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L78
	call	pthread_mutex_unlock
	jmp	.L78
	.p2align 4,,10
	.p2align 3
.L75:
	cmpb	$0, 40(%rsp)
	jne	.L101
.L80:
	movq	40(%rbx), %rax
	lock addq	%r12, (%rax)
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
.L101:
	movq	32(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L80
	call	pthread_mutex_unlock
	jmp	.L80
.L79:
	movl	$1, %ecx
.LEHB3:
	call	_ZSt20__throw_system_errori
.LEHE3:
.L98:
	movl	$1, %ecx
.LEHB4:
	call	_ZSt20__throw_system_errori
.LEHE4:
.L100:
	movl	%eax, %ecx
.LEHB5:
	call	_ZSt20__throw_system_errori
.LEHE5:
.L84:
	cmpb	$0, 40(%rsp)
	movq	%rax, %rbx
	je	.L82
	leaq	32(%rsp), %rcx
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L82:
	movq	%rbx, %rcx
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA14663:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE14663-.LLSDACSB14663
.LLSDACSB14663:
	.uleb128 .LEHB0-.LFB14663
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L84-.LFB14663
	.uleb128 0
	.uleb128 .LEHB1-.LFB14663
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB2-.LFB14663
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L84-.LFB14663
	.uleb128 0
	.uleb128 .LEHB3-.LFB14663
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB14663
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L84-.LFB14663
	.uleb128 0
	.uleb128 .LEHB5-.LFB14663
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB14663
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSE14663:
	.text
	.seh_endproc
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB13846:
	.seh_endprologue
	movq	(%rcx), %rcx
	testq	%rcx, %rcx
	je	.L102
	movq	(%rcx), %rax
	rex.W jmp	*8(%rax)
	.p2align 4,,10
	.p2align 3
.L102:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "TSC freq: %.3f GHz\12\0"
.LC3:
	.ascii "impossible\12\0"
	.align 8
.LC7:
	.ascii "== \347\254\254"
	.ascii "120\347\253\240 \345\215\217\347\250\213\347\234\237\345\256\236\345\237\272\345\207\206 (GCC 13.1 / MinGW-w64 / x86-64) ==\12\0"
	.align 8
.LC8:
	.ascii "frame_size(max coroutine frame) : %zu B\12\0"
	.align 8
.LC9:
	.ascii "resume+yield per step          : %.2f ns\12\0"
	.align 8
.LC10:
	.ascii "create+first-step+destroy      : %.2f ns\12\0"
	.align 8
.LC11:
	.ascii "thread switch (mutex+cv rt)     : %.2f ns (%.3f us, \345\220\253\345\220\214\346\255\245\345\274\200\351\224\200)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB12925:
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
	subq	$200, %rsp
	.seh_stackalloc	200
	movaps	%xmm6, 96(%rsp)
	.seh_savexmm	%xmm6, 96
	movaps	%xmm7, 112(%rsp)
	.seh_savexmm	%xmm7, 112
	movaps	%xmm8, 128(%rsp)
	.seh_savexmm	%xmm8, 128
	movaps	%xmm9, 144(%rsp)
	.seh_savexmm	%xmm9, 144
	movaps	%xmm10, 160(%rsp)
	.seh_savexmm	%xmm10, 160
	movaps	%xmm11, 176(%rsp)
	.seh_savexmm	%xmm11, 176
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rdi
	rdtsc
	movq	__imp__errno(%rip), %rbx
	movq	%rax, %rbp
	salq	$32, %rdx
	movq	$0, 80(%rsp)
	movl	$120000000, 88(%rsp)
	leaq	80(%rsp), %rsi
	orq	%rdx, %rbp
.L106:
	movq	%rsi, %rdx
	movq	%rsi, %rcx
.LEHB7:
	call	nanosleep
	cmpl	$-1, %eax
	je	.L152
.L105:
	rdtsc
	salq	$32, %rdx
	movq	%rax, %rbx
	orq	%rdx, %rbx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbp, %rbx
	js	.L107
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%rbx, %xmm1
.L108:
	subq	%rdi, %rax
	pxor	%xmm0, %xmm0
	movsd	.LC0(%rip), %xmm2
	cvtsi2sdq	%rax, %xmm0
	leaq	.LC1(%rip), %rcx
	divsd	%xmm2, %xmm0
	divsd	%xmm0, %xmm1
	divsd	%xmm2, %xmm1
	movq	%xmm1, %rdx
	movsd	%xmm1, _ZL9g_tsc_ghz(%rip)
	call	_ZL6printfPKcz
.LEHE7:
	movq	%rsi, %rcx
	call	_Z16infinite_counterv
	rdtsc
	movq	%rax, %rbp
	salq	$32, %rdx
	orq	%rdx, %rbp
	rdtsc
	movq	%rax, %r13
	salq	$32, %rdx
	orq	%rdx, %r13
	rdtsc
	movl	$2000000, %ebx
	movabsq	$1999999000000, %rdi
	movq	%rax, %r12
	salq	$32, %rdx
	orq	%rdx, %r12
	.p2align 4,,10
	.p2align 3
.L109:
	movq	%rsi, %rcx
.LEHB8:
	call	_Z10yield_stepR3GenIiE
.LEHE8:
	cltq
	addq	%rax, %rdi
	subl	$1, %ebx
	jne	.L109
	rdtsc
	salq	$32, %rdx
	orq	%rdx, %rax
	movq	%rbp, %rdx
	subq	%r13, %rdx
	subq	%r12, %rdx
	addq	%rdx, %rax
	js	.L110
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
.L111:
	testq	%rdi, %rdi
	divsd	_ZL9g_tsc_ghz(%rip), %xmm0
	divsd	.LC2(%rip), %xmm0
	movapd	%xmm0, %xmm11
	je	.L112
.L115:
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE(%rip), %rax
	leaq	48(%rsp), %r12
	movq	%rax, %xmm8
	leaq	44(%rsp), %rax
	movq	%r12, %xmm4
	punpcklqdq	%xmm4, %xmm8
	leaq	56(%rsp), %rbp
	movq	%rax, %xmm5
	leaq	43(%rsp), %rax
	movq	%rbp, %xmm9
	movq	%rax, %xmm6
	punpcklqdq	%xmm5, %xmm9
	leaq	64(%rsp), %rax
	movq	%rax, %xmm4
	movq	80(%rsp), %rax
	punpcklqdq	%xmm4, %xmm6
	testq	%rax, %rax
	je	.L114
	movq	%rax, %rcx
	call	*8(%rax)
.L114:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movl	$200000, %edi
	movq	%rax, %r13
	.p2align 4,,10
	.p2align 3
.L116:
	movq	%rsi, %rcx
	movl	$4, %edx
	call	_Z13small_counteri
	movq	80(%rsp), %rbx
	movq	%rbx, %rcx
.LEHB9:
	call	*(%rbx)
.LEHE9:
	movq	%rbx, %rcx
	call	*8(%rbx)
	subl	$1, %edi
	jne	.L116
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	%xmm0, %xmm0
	xorl	%edx, %edx
	movq	%r12, %rcx
	subq	%r13, %rax
	movsd	.LC4(%rip), %xmm7
	cvtsi2sdq	%rax, %xmm0
	leaq	72(%rsp), %r13
	divsd	%xmm7, %xmm0
	mulsd	%xmm7, %xmm0
	divsd	.LC5(%rip), %xmm0
	movapd	%xmm0, %xmm10
	call	pthread_mutex_init
	movq	%rbp, %rcx
	call	_ZNSt18condition_variableC1Ev
	movl	$48, %ecx
	movb	$0, 43(%rsp)
	movl	$0, 44(%rsp)
	movq	$0, 64(%rsp)
	movq	$0, 72(%rsp)
	call	_Znwy
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %r8
	movq	%rsi, %rdx
	movq	%r13, %rcx
	movups	%xmm8, (%rax)
	movups	%xmm9, 16(%rax)
	movups	%xmm6, 32(%rax)
	movq	%rax, 80(%rsp)
.LEHB10:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE10:
	movq	%rsi, %rcx
	movl	$50000, %ebx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rdi
	.p2align 4,,10
	.p2align 3
.L121:
	movq	%r12, %rcx
	movq	%r12, 80(%rsp)
	movb	$0, 88(%rsp)
.LEHB11:
	call	pthread_mutex_lock
.LEHE11:
	testl	%eax, %eax
	jne	.L153
	movq	%rbp, %rcx
	movb	$1, 88(%rsp)
	movl	$1, 44(%rsp)
	call	_ZNSt18condition_variable10notify_oneEv
	jmp	.L125
	.p2align 4,,10
	.p2align 3
.L126:
	movq	%rsi, %rdx
	movq	%rbp, %rcx
.LEHB12:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE12:
.L125:
	movl	44(%rsp), %eax
	testl	%eax, %eax
	jne	.L126
	cmpb	$0, 88(%rsp)
	jne	.L154
.L127:
	subl	$1, %ebx
	jne	.L121
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rbx
	movl	$1, %eax
	xchgb	43(%rsp), %al
	movq	%r12, %rcx
.LEHB13:
	call	pthread_mutex_lock
.LEHE13:
	testl	%eax, %eax
	movl	%eax, %ecx
	jne	.L155
	movq	%rbp, %rcx
	call	_ZNSt18condition_variable10notify_oneEv
	movq	%r12, %rcx
	call	pthread_mutex_unlock
	movq	%r13, %rcx
.LEHB14:
	call	_ZNSt6thread4joinEv
.LEHE14:
	subq	%rdi, %rbx
	pxor	%xmm6, %xmm6
	cmpq	$0, 72(%rsp)
	cvtsi2sdq	%rbx, %xmm6
	divsd	%xmm7, %xmm6
	mulsd	%xmm7, %xmm6
	divsd	.LC6(%rip), %xmm6
	jne	.L133
	movq	%rbp, %rcx
	call	_ZNSt18condition_variableD1Ev
	movq	%r12, %rcx
	call	pthread_mutex_destroy
	movq	_ZL11g_max_frame(%rip), %rbx
	leaq	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE(%rip), %rax
	movq	%rax, 64(%rsp)
	leaq	_Z10yield_stepR3GenIiE(%rip), %rax
	movq	%rax, 72(%rsp)
	leaq	.LC7(%rip), %rcx
	leaq	_Z10ready_taskv(%rip), %rax
	movq	%rax, 80(%rsp)
	movq	64(%rsp), %rax
	movq	72(%rsp), %rax
	movq	80(%rsp), %rax
.LEHB15:
	call	_ZL6printfPKcz
	leaq	.LC8(%rip), %rcx
	movq	%rbx, %rdx
	call	_ZL6printfPKcz
	movapd	%xmm11, %xmm1
	movq	%xmm11, %rdx
	leaq	.LC9(%rip), %rcx
	call	_ZL6printfPKcz
	movapd	%xmm10, %xmm1
	movq	%xmm10, %rdx
	leaq	.LC10(%rip), %rcx
	call	_ZL6printfPKcz
	movapd	%xmm6, %xmm3
	movapd	%xmm6, %xmm1
	movq	%xmm6, %rdx
	divsd	%xmm7, %xmm3
	leaq	.LC11(%rip), %rcx
	movq	%xmm3, %r8
	movapd	%xmm3, %xmm2
	call	_ZL6printfPKcz
	nop
.LEHE15:
	movaps	96(%rsp), %xmm6
	xorl	%eax, %eax
	movaps	112(%rsp), %xmm7
	movaps	128(%rsp), %xmm8
	movaps	144(%rsp), %xmm9
	movaps	160(%rsp), %xmm10
	movaps	176(%rsp), %xmm11
	addq	$200, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	ret
	.p2align 4,,10
	.p2align 3
.L154:
	movq	80(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L127
	call	pthread_mutex_unlock
	jmp	.L127
.L107:
	movq	%rbx, %rdx
	andl	$1, %ebx
	pxor	%xmm1, %xmm1
	shrq	%rdx
	orq	%rbx, %rdx
	cvtsi2sdq	%rdx, %xmm1
	addsd	%xmm1, %xmm1
	jmp	.L108
.L152:
.LEHB16:
	call	*%rbx
.LEHE16:
	cmpl	$4, (%rax)
	jne	.L105
	jmp	.L106
.L110:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm0, %xmm0
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L111
.L112:
	leaq	.LC3(%rip), %rcx
.LEHB17:
	call	_ZL6printfPKcz
.LEHE17:
	jmp	.L115
.L134:
	movq	%rax, %rbx
.L132:
	cmpq	$0, 72(%rsp)
	je	.L123
.L133:
	call	_ZSt9terminatev
.L155:
.LEHB18:
	call	_ZSt20__throw_system_errori
.L153:
	movl	%eax, %ecx
	call	_ZSt20__throw_system_errori
.LEHE18:
.L135:
	cmpb	$0, 88(%rsp)
	movq	%rax, %rbx
	je	.L132
	movq	%rsi, %rcx
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
	jmp	.L132
.L137:
	movq	%rax, %rbx
	movq	80(%rsp), %rax
	testq	%rax, %rax
	je	.L151
	movq	%rax, %rcx
	call	*8(%rax)
.L151:
	movq	%rbx, %rcx
.LEHB19:
	call	_Unwind_Resume
.LEHE19:
.L136:
	movq	%rax, %rsi
	movq	%rbx, %rcx
	call	*8(%rbx)
	movq	%rsi, %rcx
.LEHB20:
	call	_Unwind_Resume
.LEHE20:
.L138:
	movq	%rsi, %rcx
	movq	%rax, %rbx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L123:
	movq	%rbp, %rcx
	call	_ZNSt18condition_variableD1Ev
	movq	%r12, %rcx
	call	pthread_mutex_destroy
	jmp	.L151
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA12925:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE12925-.LLSDACSB12925
.LLSDACSB12925:
	.uleb128 .LEHB7-.LFB12925
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB8-.LFB12925
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L137-.LFB12925
	.uleb128 0
	.uleb128 .LEHB9-.LFB12925
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L136-.LFB12925
	.uleb128 0
	.uleb128 .LEHB10-.LFB12925
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L138-.LFB12925
	.uleb128 0
	.uleb128 .LEHB11-.LFB12925
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L134-.LFB12925
	.uleb128 0
	.uleb128 .LEHB12-.LFB12925
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L135-.LFB12925
	.uleb128 0
	.uleb128 .LEHB13-.LFB12925
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L134-.LFB12925
	.uleb128 0
	.uleb128 .LEHB14-.LFB12925
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L134-.LFB12925
	.uleb128 0
	.uleb128 .LEHB15-.LFB12925
	.uleb128 .LEHE15-.LEHB15
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB16-.LFB12925
	.uleb128 .LEHE16-.LEHB16
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB17-.LFB12925
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L137-.LFB12925
	.uleb128 0
	.uleb128 .LEHB18-.LFB12925
	.uleb128 .LEHE18-.LEHB18
	.uleb128 .L134-.LFB12925
	.uleb128 0
	.uleb128 .LEHB19-.LFB12925
	.uleb128 .LEHE19-.LEHB19
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB20-.LFB12925
	.uleb128 .LEHE20-.LEHB20
	.uleb128 0
	.uleb128 0
.LLSDACSE12925:
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
	.section .rdata,"dr"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE\0"
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv
.lcomm _ZL9g_tsc_ghz,8,8
.lcomm _ZL11g_max_frame,8,8
	.align 8
.LC0:
	.long	0
	.long	1104006501
	.align 8
.LC2:
	.long	0
	.long	1094616192
	.align 8
.LC4:
	.long	0
	.long	1083129856
	.align 8
.LC5:
	.long	0
	.long	1091070464
	.align 8
.LC6:
	.long	0
	.long	1088973312
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variable10notify_oneEv;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	nanosleep;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variableC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variableD1Ev;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
