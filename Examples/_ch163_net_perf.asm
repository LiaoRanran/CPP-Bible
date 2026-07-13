	.file	"_ch163_net_perf.cpp"
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB9718:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEE6_M_runEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEE6_M_runEv
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEE6_M_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEE6_M_runEv:
.LFB11408:
	.seh_endprologue
	movq	8(%rcx), %rdx
	movq	16(%rcx), %rax
	movq	%rdx, %rcx
	rex.W jmp	*%rax
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z9sock_sendyPKci
	.def	_Z9sock_sendyPKci;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sock_sendyPKci
_Z9sock_sendyPKci:
.LFB10489:
	.seh_endprologue
	xorl	%r9d, %r9d
	rex.W jmp	*__imp_send(%rip)
	.seh_endproc
	.p2align 4
	.globl	_Z9sock_recvyPci
	.def	_Z9sock_recvyPci;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sock_recvyPci
_Z9sock_recvyPci:
.LFB10490:
	.seh_endprologue
	xorl	%r9d, %r9d
	rex.W jmp	*__imp_recv(%rip)
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "127.0.0.1\0"
	.text
	.p2align 4
	.def	_ZL13server_threadPSt6atomicIbE;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL13server_threadPSt6atomicIbE
_ZL13server_threadPSt6atomicIbE:
.LFB10491:
	pushq	%r14
	.seh_pushreg	%r14
	movl	$65584, %eax
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
	call	___chkstk_ms
	subq	%rax, %rsp
	.seh_stackalloc	65584
	.seh_endprologue
	xorl	%r8d, %r8d
	movl	$1, %edx
	leaq	32(%rsp), %rsi
	movq	%rcx, %rbx
	movl	$2, %ecx
	call	*__imp_socket(%rip)
	movl	$54331, %ecx
	movq	$0, 34(%rsp)
	movq	$0, 40(%rsp)
	movq	%rax, %r14
	movl	$2, %eax
	movw	%ax, 32(%rsp)
	call	*__imp_htons(%rip)
	leaq	36(%rsp), %r8
	movl	$2, %ecx
	movw	%ax, 34(%rsp)
	leaq	.LC0(%rip), %rdx
	call	*__imp_inet_pton(%rip)
	movl	$16, %r8d
	movq	%rsi, %rdx
	movq	%r14, %rcx
	call	*__imp_bind(%rip)
	movl	$1, %edx
	movq	%r14, %rcx
	call	*__imp_listen(%rip)
	movl	$1, %eax
	xchgb	(%rbx), %al
	xorl	%r8d, %r8d
	xorl	%edx, %edx
	leaq	48(%rsp), %rbp
	movq	%r14, %rcx
	call	*__imp_accept(%rip)
	movq	__imp_recv(%rip), %r13
	movq	__imp_send(%rip), %r12
	movq	%rax, %rdi
	.p2align 4,,10
	.p2align 3
.L10:
	xorl	%r9d, %r9d
	movl	$65536, %r8d
	movq	%rbp, %rdx
	movq	%rdi, %rcx
	call	*%r13
	testl	%eax, %eax
	movl	%eax, %esi
	jle	.L7
	xorl	%ebx, %ebx
	.p2align 4,,10
	.p2align 3
.L9:
	movslq	%ebx, %rdx
	movl	%esi, %r8d
	xorl	%r9d, %r9d
	addq	%rbp, %rdx
	subl	%ebx, %r8d
	movq	%rdi, %rcx
	call	*%r12
	testl	%eax, %eax
	jle	.L10
	addl	%eax, %ebx
	cmpl	%ebx, %esi
	jg	.L9
	jmp	.L10
.L7:
	movq	__imp_closesocket(%rip), %rbx
	movq	%rdi, %rcx
	call	*%rbx
	movq	%r14, %rcx
	call	*%rbx
	nop
	addq	$65584, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	ret
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED1Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED1Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED1Ev:
.LFB11398:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.section	.text$_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED0Ev
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED0Ev:
.LFB11399:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE(%rip), %rax
	movq	%rcx, %rbx
	movq	%rax, (%rcx)
	call	_ZNSt6thread6_StateD2Ev
	movl	$24, %edx
	movq	%rbx, %rcx
	addq	$32, %rsp
	popq	%rbx
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev:
.LFB11393:
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE(%rip), %rax
	movq	%rax, (%rcx)
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev:
.LFB11395:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE(%rip), %rax
	movq	%rcx, %rbx
	movq	%rax, (%rcx)
	call	_ZNSt6thread6_StateD2Ev
	movl	$40, %edx
	movq	%rbx, %rcx
	addq	$32, %rsp
	popq	%rbx
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.def	_ZL6printfPKcz;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz
_ZL6printfPKcz:
.LFB7541:
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
	.def	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0
_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0:
.LFB11438:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	testq	%rcx, %rcx
	jle	.L18
	movq	__imp__errno(%rip), %rsi
	leaq	32(%rsp), %rbx
	movabsq	$2361183241434822607, %rax
	imulq	%rcx
	movq	%rcx, %rax
	sarq	$63, %rax
	sarq	$7, %rdx
	subq	%rax, %rdx
	movq	%rdx, 32(%rsp)
	imulq	$1000, %rdx, %rdx
	subq	%rdx, %rcx
	imulq	$1000000, %rcx, %rcx
	movl	%ecx, 40(%rsp)
.L21:
	movq	%rbx, %rdx
	movq	%rbx, %rcx
	call	nanosleep
	cmpl	$-1, %eax
	je	.L24
.L18:
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	call	*%rsi
	cmpl	$4, (%rax)
	je	.L21
	addq	$56, %rsp
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
.LFB10905:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	cmpb	$0, 8(%rcx)
	movq	%rcx, %rbx
	je	.L31
	movq	(%rcx), %rcx
	testq	%rcx, %rcx
	je	.L25
	call	pthread_mutex_unlock
	movb	$0, 8(%rbx)
.L25:
	addq	$32, %rsp
	popq	%rbx
	ret
.L31:
	movl	$1, %ecx
	call	_ZSt20__throw_system_errori
	nop
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv:
.LFB11407:
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
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	movq	%rcx, %rbx
	movq	8(%rcx), %rcx
	movb	$0, 40(%rsp)
	testq	%rcx, %rcx
	movq	%rcx, 32(%rsp)
	je	.L41
	leaq	32(%rsp), %rbp
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L35:
	movq	32(%rbx), %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jne	.L37
	movq	24(%rbx), %rax
	cmpb	$0, 40(%rsp)
	movl	$0, (%rax)
	je	.L59
	movq	32(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L39
.LEHB0:
	call	pthread_mutex_unlock
.LEHE0:
	movb	$0, 40(%rsp)
.L39:
	movq	16(%rbx), %rcx
	call	_ZNSt18condition_variable10notify_oneEv
	cmpb	$0, 40(%rsp)
	jne	.L60
.L40:
	movq	8(%rbx), %rcx
	movb	$0, 40(%rsp)
	testq	%rcx, %rcx
	movq	%rcx, 32(%rsp)
	je	.L41
.L33:
.LEHB1:
	call	pthread_mutex_lock
.LEHE1:
	testl	%eax, %eax
	jne	.L61
	movq	16(%rbx), %rdi
	movb	$1, 40(%rsp)
	movq	24(%rbx), %rsi
	movq	32(%rbx), %r12
	.p2align 4,,10
	.p2align 3
.L36:
	cmpl	$1, (%rsi)
	je	.L35
	movzbl	(%r12), %eax
	testb	%al, %al
	jne	.L35
	movq	%rbp, %rdx
	movq	%rdi, %rcx
.LEHB2:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE2:
	jmp	.L36
	.p2align 4,,10
	.p2align 3
.L60:
	movq	32(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L40
	call	pthread_mutex_unlock
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L37:
	cmpb	$0, 40(%rsp)
	jne	.L62
.L32:
	addq	$48, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
.L62:
	movq	32(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L32
	call	pthread_mutex_unlock
	nop
	addq	$48, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
.L41:
	movl	$1, %ecx
.LEHB3:
	call	_ZSt20__throw_system_errori
.LEHE3:
.L59:
	movl	$1, %ecx
.LEHB4:
	call	_ZSt20__throw_system_errori
.LEHE4:
.L61:
	movl	%eax, %ecx
.LEHB5:
	call	_ZSt20__throw_system_errori
.LEHE5:
.L45:
	cmpb	$0, 40(%rsp)
	movq	%rax, %rbx
	je	.L44
	leaq	32(%rsp), %rcx
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L44:
	movq	%rbx, %rcx
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA11407:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE11407-.LLSDACSB11407
.LLSDACSB11407:
	.uleb128 .LEHB0-.LFB11407
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L45-.LFB11407
	.uleb128 0
	.uleb128 .LEHB1-.LFB11407
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB2-.LFB11407
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L45-.LFB11407
	.uleb128 0
	.uleb128 .LEHB3-.LFB11407
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB11407
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L45-.LFB11407
	.uleb128 0
	.uleb128 .LEHB5-.LFB11407
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB11407
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSE11407:
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
.LFB11063:
	.seh_endprologue
	movq	(%rcx), %rcx
	testq	%rcx, %rcx
	je	.L63
	movq	(%rcx), %rax
	rex.W jmp	*8(%rax)
	.p2align 4,,10
	.p2align 3
.L63:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC2:
	.ascii "TSC freq: %.3f GHz\12\0"
	.align 8
.LC4:
	.ascii "localhost TCP connect : %.1f us\12\0"
	.align 8
.LC6:
	.ascii "localhost RTT (1B echo): %.3f us/op\12\0"
	.align 8
.LC9:
	.ascii "localhost bulk xfer : %.1f MB/s (%.2f GB/s)\12\0"
	.align 8
.LC11:
	.ascii "clock-read proxy     : %.2f ns/call (RDTSC, not I/O syscall)\12\0"
	.align 8
.LC14:
	.ascii "thread switch (m+cv) : %.2f us/rt (%.2f us/switch, \345\220\253\345\220\214\346\255\245\345\274\200\351\224\200)\12\0"
	.align 8
.LC15:
	.ascii "== \347\254\254"
	.ascii "163\347\253\240 \347\275\221\347\273\234\347\234\237\345\256\236\345\237\272\345\207\206 (GCC 13.1 / MinGW-w64 / x86-64, localhost) ==\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB10492:
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
	subq	$600, %rsp
	.seh_stackalloc	600
	movaps	%xmm6, 560(%rsp)
	.seh_savexmm	%xmm6, 560
	movaps	%xmm7, 576(%rsp)
	.seh_savexmm	%xmm7, 576
	.seh_endprologue
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE(%rip), %rdi
	movq	%rdi, %xmm6
	call	__main
	leaq	64(%rsp), %rax
	movl	$514, %ecx
	leaq	144(%rsp), %rdx
	movq	%rax, %xmm5
	punpcklqdq	%xmm5, %xmm6
.LEHB7:
	call	*__imp_WSAStartup(%rip)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rsi
	rdtsc
	movl	$120, %ecx
	movq	%rax, %rdi
	salq	$32, %rdx
	orq	%rdx, %rdi
	call	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0
	rdtsc
	salq	$32, %rdx
	movq	%rax, %rbx
	orq	%rdx, %rbx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rdi, %rbx
	js	.L66
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rbx, %xmm0
.L67:
	subq	%rsi, %rax
	pxor	%xmm1, %xmm1
	movsd	.LC1(%rip), %xmm7
	cvtsi2sdq	%rax, %xmm1
	leaq	.LC2(%rip), %rcx
	leaq	_ZL13server_threadPSt6atomicIbE(%rip), %rdi
	leaq	128(%rsp), %rbx
	divsd	%xmm7, %xmm1
	divsd	%xmm1, %xmm0
	divsd	%xmm7, %xmm0
	movq	%xmm0, %rdx
	movapd	%xmm0, %xmm1
	movsd	%xmm0, _ZL9g_tsc_ghz(%rip)
	call	_ZL6printfPKcz
	movl	$24, %ecx
	movb	$0, 64(%rsp)
	movq	$0, 72(%rsp)
	call	_Znwy
.LEHE7:
	leaq	72(%rsp), %rcx
	movq	%rbx, %rdx
	movups	%xmm6, (%rax)
	movq	%rdi, 16(%rax)
	movq	%rax, 128(%rsp)
	leaq	_ZNSt6thread24_M_thread_deps_never_runEv(%rip), %rax
	movq	%rax, %r8
	movq	%rcx, 56(%rsp)
	movq	%rax, 48(%rsp)
.LEHB8:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE8:
	movq	128(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L69
	movq	(%rcx), %rax
	call	*8(%rax)
	jmp	.L69
.L71:
	call	sched_yield
.L69:
	movzbl	64(%rsp), %eax
	testb	%al, %al
	je	.L71
	movl	$20, %ecx
.LEHB9:
	call	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0
	xorl	%r8d, %r8d
	movl	$1, %edx
	movl	$2, %ecx
	call	*__imp_socket(%rip)
	movl	$2, %edx
	movq	%rax, %rdi
	movl	$54331, %ecx
	movq	$0, 114(%rsp)
	movw	%dx, 112(%rsp)
	movq	$0, 120(%rsp)
	call	*__imp_htons(%rip)
	movw	%ax, 114(%rsp)
	leaq	116(%rsp), %r8
	movl	$2, %ecx
	leaq	.LC0(%rip), %rdx
	call	*__imp_inet_pton(%rip)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	leaq	112(%rsp), %rdx
	movl	$16, %r8d
	movq	%rdi, %rcx
	movq	%rax, %rsi
	call	*__imp_connect(%rip)
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	%xmm1, %xmm1
	movsd	.LC3(%rip), %xmm6
	leaq	.LC4(%rip), %rcx
	subq	%rsi, %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm6, %xmm1
	movq	%xmm1, %rdx
	call	_ZL6printfPKcz
	movb	$120, 65(%rsp)
	leaq	65(%rsp), %rbp
	movl	$200000, %esi
	movb	$0, 66(%rsp)
	leaq	66(%rsp), %r14
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	__imp_send(%rip), %r13
	movq	__imp_recv(%rip), %r12
	movq	%rax, %r15
	.p2align 4,,10
	.p2align 3
.L72:
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%rbp, %rdx
	movq	%rdi, %rcx
	call	*%r13
	xorl	%r9d, %r9d
	movl	$1, %r8d
	movq	%r14, %rdx
	movq	%rdi, %rcx
	call	*%r12
	subl	$1, %esi
	jne	.L72
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	%xmm1, %xmm1
	leaq	.LC6(%rip), %rcx
	subq	%r15, %rax
	cvtsi2sdq	%rax, %xmm1
	divsd	%xmm6, %xmm1
	divsd	.LC5(%rip), %xmm1
	movq	%xmm1, %rdx
	call	_ZL6printfPKcz
	movl	$65536, %ecx
	call	_Znay
	movl	$65536, %r8d
	movl	$165, %edx
	movq	%rax, %rcx
	movq	%rax, %r14
	xorl	%r15d, %r15d
	call	memset
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, 40(%rsp)
	.p2align 4,,10
	.p2align 3
.L76:
	xorl	%r9d, %r9d
	movl	$65536, %r8d
	movq	%r14, %rdx
	movq	%rdi, %rcx
	call	*%r13
	testl	%eax, %eax
	movl	%eax, %ebp
	jle	.L73
	cltq
	xorl	%esi, %esi
	addq	%rax, %r15
	jmp	.L75
	.p2align 4,,10
	.p2align 3
.L113:
	addl	%eax, %esi
	cmpl	%esi, %ebp
	jle	.L74
.L75:
	movl	%ebp, %r8d
	xorl	%r9d, %r9d
	movq	%r14, %rdx
	subl	%esi, %r8d
	movq	%rdi, %rcx
	call	*%r12
	testl	%eax, %eax
	jg	.L113
.L74:
	cmpq	$67108863, %r15
	jbe	.L76
.L73:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	40(%rsp), %rdx
	pxor	%xmm0, %xmm0
	leaq	.LC9(%rip), %rcx
	movsd	.LC7(%rip), %xmm1
	movsd	.LC8(%rip), %xmm3
	subq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm0
	divsd	%xmm7, %xmm0
	divsd	%xmm0, %xmm1
	mulsd	%xmm1, %xmm3
	movq	%xmm1, %rdx
	movq	%xmm3, %r8
	movapd	%xmm3, %xmm2
	call	_ZL6printfPKcz
	movq	%r14, %rcx
	call	_ZdaPv
	rdtsc
	movl	$5000000, %esi
	movq	%rax, %rbp
	salq	$32, %rdx
	orq	%rdx, %rbp
	.p2align 4,,10
	.p2align 3
.L77:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subl	$2, %esi
	jne	.L77
	rdtsc
	salq	$32, %rdx
	orq	%rdx, %rax
	subq	%rbp, %rax
	js	.L78
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rax, %xmm0
.L79:
	divsd	_ZL9g_tsc_ghz(%rip), %xmm0
	leaq	.LC11(%rip), %rcx
	divsd	.LC10(%rip), %xmm0
	movapd	%xmm0, %xmm1
	movq	%xmm0, %rdx
	call	_ZL6printfPKcz
.LEHE9:
	leaq	80(%rsp), %r12
	xorl	%edx, %edx
	leaq	88(%rsp), %rsi
	movq	%r12, %rcx
	call	pthread_mutex_init
	movq	%rsi, %rcx
	call	_ZNSt18condition_variableC1Ev
	movl	$40, %ecx
	movb	$0, 67(%rsp)
	movl	$0, 68(%rsp)
	movq	$0, 96(%rsp)
.LEHB10:
	call	_Znwy
.LEHE10:
	movq	48(%rsp), %r8
	leaq	96(%rsp), %r13
	movq	%r12, %xmm2
	movq	%rax, 128(%rsp)
	leaq	16+_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE(%rip), %rdx
	movq	%r13, %rcx
	movq	%rdx, %xmm0
	leaq	68(%rsp), %rdx
	punpcklqdq	%xmm2, %xmm0
	movups	%xmm0, (%rax)
	movq	%rsi, %xmm0
	movq	%rdx, %xmm5
	leaq	67(%rsp), %rdx
	punpcklqdq	%xmm5, %xmm0
	movups	%xmm0, 16(%rax)
	movq	%rdx, 32(%rax)
	movq	%rbx, %rdx
.LEHB11:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE11:
	movq	%rbx, %rcx
	movl	$50000, %ebp
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %r14
	.p2align 4,,10
	.p2align 3
.L80:
	movq	%r12, %rcx
	movq	%r12, 128(%rsp)
	movb	$0, 136(%rsp)
.LEHB12:
	call	pthread_mutex_lock
.LEHE12:
	testl	%eax, %eax
	jne	.L114
	movq	%rsi, %rcx
	movb	$1, 136(%rsp)
	movl	$1, 68(%rsp)
	call	_ZNSt18condition_variable10notify_oneEv
	jmp	.L84
	.p2align 4,,10
	.p2align 3
.L85:
	movq	%rbx, %rdx
	movq	%rsi, %rcx
.LEHB13:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE13:
.L84:
	movl	68(%rsp), %eax
	testl	%eax, %eax
	jne	.L85
	cmpb	$0, 136(%rsp)
	jne	.L115
.L86:
	subl	$1, %ebp
	jne	.L80
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rbx
	movl	$1, %eax
	xchgb	67(%rsp), %al
	movq	%r12, %rcx
.LEHB14:
	call	pthread_mutex_lock
.LEHE14:
	testl	%eax, %eax
	movl	%eax, %ecx
	jne	.L116
	movq	%rsi, %rcx
	call	_ZNSt18condition_variable10notify_oneEv
	movq	%r12, %rcx
	call	pthread_mutex_unlock
	movq	%r13, %rcx
.LEHB15:
	call	_ZNSt6thread4joinEv
	subq	%r14, %rbx
	pxor	%xmm1, %xmm1
	movsd	.LC13(%rip), %xmm4
	cvtsi2sdq	%rbx, %xmm1
	leaq	.LC14(%rip), %rcx
	divsd	%xmm6, %xmm1
	divsd	.LC12(%rip), %xmm1
	mulsd	%xmm1, %xmm4
	movq	%xmm1, %rdx
	movq	%xmm4, %r8
	movapd	%xmm4, %xmm2
	call	_ZL6printfPKcz
	leaq	_Z9sock_sendyPKci(%rip), %rax
	movq	%rdi, %rcx
	movq	%rax, 104(%rsp)
	movq	104(%rsp), %rax
	leaq	_Z9sock_recvyPci(%rip), %rax
	movq	%rax, 128(%rsp)
	movq	128(%rsp), %rax
	call	*__imp_closesocket(%rip)
	call	*__imp_WSACleanup(%rip)
	movq	56(%rsp), %rcx
	call	_ZNSt6thread4joinEv
	leaq	.LC15(%rip), %rcx
	call	_ZL6printfPKcz
.LEHE15:
	cmpq	$0, 96(%rsp)
	jne	.L89
	movq	%rsi, %rcx
	call	_ZNSt18condition_variableD1Ev
	movq	%r12, %rcx
	call	pthread_mutex_destroy
	cmpq	$0, 72(%rsp)
	jne	.L89
	movaps	560(%rsp), %xmm6
	xorl	%eax, %eax
	movaps	576(%rsp), %xmm7
	addq	$600, %rsp
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
.L115:
	movq	128(%rsp), %rcx
	testq	%rcx, %rcx
	je	.L86
	call	pthread_mutex_unlock
	jmp	.L86
.L66:
	movq	%rbx, %rdx
	andl	$1, %ebx
	pxor	%xmm0, %xmm0
	shrq	%rdx
	orq	%rbx, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L67
.L78:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm0, %xmm0
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L79
.L94:
	movq	%rax, %rcx
.L93:
	cmpq	$0, 72(%rsp)
	je	.L117
.L89:
	call	_ZSt9terminatev
.L116:
.LEHB16:
	call	_ZSt20__throw_system_errori
.L114:
	movl	%eax, %ecx
	call	_ZSt20__throw_system_errori
.LEHE16:
.L98:
	movq	%rax, %rsi
	movq	%rbx, %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rsi, %rcx
.LEHB17:
	call	_Unwind_Resume
.LEHE17:
.L95:
	movq	%rax, %rbx
.L82:
	movq	%rsi, %rcx
	call	_ZNSt18condition_variableD1Ev
	movq	%r12, %rcx
	call	pthread_mutex_destroy
	movq	%rbx, %rcx
	jmp	.L93
.L97:
	movq	%rax, %rbx
.L92:
	cmpq	$0, 96(%rsp)
	je	.L82
	jmp	.L89
.L96:
	cmpb	$0, 136(%rsp)
	movq	%rax, %rdi
	je	.L91
	movq	%rbx, %rcx
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L91:
	movq	%rdi, %rbx
	jmp	.L92
.L99:
	movq	%rax, %rdi
	movq	%rbx, %rcx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	movq	%rdi, %rbx
	jmp	.L82
.L117:
.LEHB18:
	call	_Unwind_Resume
	nop
.LEHE18:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA10492:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE10492-.LLSDACSB10492
.LLSDACSB10492:
	.uleb128 .LEHB7-.LFB10492
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB8-.LFB10492
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L98-.LFB10492
	.uleb128 0
	.uleb128 .LEHB9-.LFB10492
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L94-.LFB10492
	.uleb128 0
	.uleb128 .LEHB10-.LFB10492
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L95-.LFB10492
	.uleb128 0
	.uleb128 .LEHB11-.LFB10492
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L99-.LFB10492
	.uleb128 0
	.uleb128 .LEHB12-.LFB10492
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L97-.LFB10492
	.uleb128 0
	.uleb128 .LEHB13-.LFB10492
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L96-.LFB10492
	.uleb128 0
	.uleb128 .LEHB14-.LFB10492
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L97-.LFB10492
	.uleb128 0
	.uleb128 .LEHB15-.LFB10492
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L97-.LFB10492
	.uleb128 0
	.uleb128 .LEHB16-.LFB10492
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L97-.LFB10492
	.uleb128 0
	.uleb128 .LEHB17-.LFB10492
	.uleb128 .LEHE17-.LEHB17
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB18-.LFB10492
	.uleb128 .LEHE18-.LEHB18
	.uleb128 0
	.uleb128 0
.LLSDACSE10492:
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
	.globl	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE
	.section	.rdata$_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE,"dr"
	.linkonce same_size
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE:
	.ascii "NSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE\0"
	.globl	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE
	.section	.rdata$_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.section .rdata,"dr"
	.align 8
_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE
	.quad	_ZTINSt6thread6_StateE
	.align 32
_ZTSNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE:
	.ascii "*NSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE\0"
	.globl	_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE
	.section	.rdata$_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE,"dr"
	.linkonce same_size
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEE6_M_runEv
	.section .rdata,"dr"
	.align 8
_ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE:
	.quad	0
	.quad	_ZTINSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev
	.quad	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv
.lcomm _ZL9g_tsc_ghz,8,8
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.align 8
.LC3:
	.long	0
	.long	1083129856
	.align 8
.LC5:
	.long	0
	.long	1091070464
	.align 8
.LC7:
	.long	0
	.long	1078984704
	.align 8
.LC8:
	.long	0
	.long	1062207488
	.align 8
.LC10:
	.long	0
	.long	1095963344
	.align 8
.LC12:
	.long	0
	.long	1088973312
	.align 8
.LC13:
	.long	0
	.long	1071644672
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	nanosleep;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variable10notify_oneEv;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	sched_yield;	.scl	2;	.type	32;	.endef
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variableC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variableD1Ev;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
