	.file	"_ch163_net_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB14509:
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
.LFB16723:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR 16[rcx]
	mov	rcx, rdx
	rex.W jmp	rax
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z9sock_sendyPKci
	.def	_Z9sock_sendyPKci;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sock_sendyPKci
_Z9sock_sendyPKci:
.LFB14850:
	.seh_endprologue
	xor	r9d, r9d
	rex.W jmp	[QWORD PTR __imp_send[rip]]
	.seh_endproc
	.p2align 4
	.globl	_Z9sock_recvyPci
	.def	_Z9sock_recvyPci;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9sock_recvyPci
_Z9sock_recvyPci:
.LFB14851:
	.seh_endprologue
	xor	r9d, r9d
	rex.W jmp	[QWORD PTR __imp_recv[rip]]
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "127.0.0.1\0"
	.text
	.p2align 4
	.def	_ZL13server_threadPSt6atomicIbE;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL13server_threadPSt6atomicIbE
_ZL13server_threadPSt6atomicIbE:
.LFB14852:
	push	r14
	.seh_pushreg	r14
	mov	eax, 65584
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	call	___chkstk_ms
	sub	rsp, rax
	.seh_stackalloc	65584
	.seh_endprologue
	xor	r8d, r8d
	mov	edx, 1
	mov	rbx, rcx
	mov	ecx, 2
	call	[QWORD PTR __imp_socket[rip]]
	mov	ecx, 54331
	mov	QWORD PTR 34[rsp], 0
	mov	QWORD PTR 40[rsp], 0
	mov	r13, rax
	mov	eax, 2
	mov	WORD PTR 32[rsp], ax
	call	[QWORD PTR __imp_htons[rip]]
	lea	r8, 36[rsp]
	mov	ecx, 2
	lea	rdx, .LC0[rip]
	mov	WORD PTR 34[rsp], ax
	call	[QWORD PTR __imp_inet_pton[rip]]
	mov	r8d, 16
	lea	rdx, 32[rsp]
	mov	rcx, r13
	call	[QWORD PTR __imp_bind[rip]]
	mov	edx, 1
	mov	rcx, r13
	call	[QWORD PTR __imp_listen[rip]]
	mov	eax, 1
	xchg	al, BYTE PTR [rbx]
	xor	r8d, r8d
	xor	edx, edx
	mov	rcx, r13
	lea	rdi, 48[rsp]
	call	[QWORD PTR __imp_accept[rip]]
	mov	r12, QWORD PTR __imp_recv[rip]
	mov	rbp, QWORD PTR __imp_send[rip]
	mov	rsi, rax
	.p2align 4
	.p2align 3
.L10:
	xor	r9d, r9d
	mov	r8d, 65536
	mov	rdx, rdi
	mov	rcx, rsi
	call	r12
	mov	r14d, eax
	test	eax, eax
	jle	.L7
	xor	ebx, ebx
	.p2align 4
	.p2align 3
.L9:
	movsxd	rdx, ebx
	mov	r8d, r14d
	xor	r9d, r9d
	mov	rcx, rsi
	add	rdx, rdi
	sub	r8d, ebx
	call	rbp
	test	eax, eax
	jle	.L10
	add	ebx, eax
	cmp	r14d, ebx
	jg	.L9
	jmp	.L10
.L7:
	mov	rbx, QWORD PTR __imp_closesocket[rip]
	mov	rcx, rsi
	call	rbx
	mov	rcx, r13
	call	rbx
	nop
	add	rsp, 65584
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
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
.LFB16528:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
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
.LFB16529:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt6thread6_StateD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 24
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev:
.LFB16523:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEED0Ev:
.LFB16525:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt6thread6_StateD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	mov	edx, 40
	add	rsp, 56
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.def	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0
_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0:
.LFB17554:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	test	rcx, rcx
	jle	.L17
	movabs	rax, 2361183241434822607
	imul	rcx
	mov	rax, rcx
	sar	rax, 63
	sar	rdx, 7
	sub	rdx, rax
	mov	QWORD PTR 32[rsp], rdx
	imul	rdx, rdx, 1000
	sub	rcx, rdx
	imul	rcx, rcx, 1000000
	mov	DWORD PTR 40[rsp], ecx
.L20:
	lea	rdx, 32[rsp]
	lea	rcx, 32[rsp]
	call	nanosleep64
	cmp	eax, -1
	je	.L23
.L17:
	add	rsp, 48
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	call	[QWORD PTR __imp__errno[rip]]
	cmp	DWORD PTR [rax], 4
	je	.L20
	add	rsp, 48
	pop	rbx
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
.LFB15456:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, rcx
	cmp	BYTE PTR 8[rcx], 0
	je	.L30
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L24
	mov	QWORD PTR 48[rsp], rdx
	call	pthread_mutex_unlock
	mov	rdx, QWORD PTR 48[rsp]
	mov	BYTE PTR 8[rdx], 0
.L24:
	add	rsp, 40
	ret
.L30:
	mov	ecx, 1
	call	_ZSt20__throw_system_errori
	nop
	.seh_endproc
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB1:
	.text
.LHOTB1:
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv:
.LFB16722:
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	rbx, rcx
	mov	rcx, QWORD PTR 8[rcx]
	mov	BYTE PTR 40[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	test	rcx, rcx
	je	.L40
	lea	rbp, 32[rsp]
	jmp	.L32
	.p2align 4,,10
	.p2align 3
.L34:
	mov	rax, QWORD PTR 32[rbx]
	movzx	eax, BYTE PTR [rax]
	test	al, al
	jne	.L36
	mov	rax, QWORD PTR 24[rbx]
	cmp	BYTE PTR 40[rsp], 0
	mov	DWORD PTR [rax], 0
	je	.L64
	mov	rcx, QWORD PTR 32[rsp]
	test	rcx, rcx
	je	.L38
.LEHB0:
	call	pthread_mutex_unlock
.LEHE0:
	mov	BYTE PTR 40[rsp], 0
.L38:
	mov	rcx, QWORD PTR 16[rbx]
	call	_ZNSt18condition_variable10notify_oneEv
	cmp	BYTE PTR 40[rsp], 0
	jne	.L65
.L39:
	mov	rcx, QWORD PTR 8[rbx]
	mov	BYTE PTR 40[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	test	rcx, rcx
	je	.L66
.L32:
.LEHB1:
	call	pthread_mutex_lock
.LEHE1:
	test	eax, eax
	jne	.L63
	mov	rdi, QWORD PTR 16[rbx]
	mov	rsi, QWORD PTR 24[rbx]
	mov	BYTE PTR 40[rsp], 1
	mov	r12, QWORD PTR 32[rbx]
	.p2align 4
	.p2align 3
.L35:
	cmp	DWORD PTR [rsi], 1
	je	.L34
	movzx	eax, BYTE PTR [r12]
	test	al, al
	jne	.L34
	mov	rdx, rbp
	mov	rcx, rdi
.LEHB2:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE2:
	jmp	.L35
	.p2align 4,,10
	.p2align 3
.L65:
	mov	rcx, QWORD PTR 32[rsp]
	test	rcx, rcx
	je	.L39
	call	pthread_mutex_unlock
	jmp	.L39
	.p2align 4,,10
	.p2align 3
.L36:
	cmp	BYTE PTR 40[rsp], 0
	jne	.L67
.L31:
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L67:
	mov	rcx, QWORD PTR 32[rsp]
	test	rcx, rcx
	je	.L31
	call	pthread_mutex_unlock
	nop
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L66:
	jmp	.L40
.L61:
	jmp	.L62
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA16722:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE16722-.LLSDACSB16722
.LLSDACSB16722:
	.uleb128 .LEHB0-.LFB16722
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L61-.LFB16722
	.uleb128 0
	.uleb128 .LEHB1-.LFB16722
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB2-.LFB16722
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L61-.LFB16722
	.uleb128 0
.LLSDACSE16722:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r12, 80
	.seh_endprologue
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEE6_M_runEv.cold:
.L40:
	mov	ecx, 1
.LEHB3:
	call	_ZSt20__throw_system_errori
.LEHE3:
.L64:
	mov	ecx, 1
.LEHB4:
	call	_ZSt20__throw_system_errori
.LEHE4:
.L63:
	mov	ecx, eax
.LEHB5:
	call	_ZSt20__throw_system_errori
.LEHE5:
.L44:
.L62:
	mov	rbx, rax
	cmp	BYTE PTR 40[rsp], 0
	je	.L43
	lea	rcx, 32[rsp]
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L43:
	mov	rcx, rbx
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC16722:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC16722-.LLSDACSBC16722
.LLSDACSBC16722:
	.uleb128 .LEHB3-.LCOLDB1
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB1
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L44-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB5-.LCOLDB1
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LCOLDB1
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC16722:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB15796:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L68
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L68:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC3:
	.ascii "TSC freq: %.3f GHz\12\0"
	.align 8
.LC5:
	.ascii "localhost TCP connect : %.1f us\12\0"
	.align 8
.LC7:
	.ascii "localhost RTT (1B echo): %.3f us/op\12\0"
	.align 8
.LC10:
	.ascii "localhost bulk xfer : %.1f MB/s (%.2f GB/s)\12\0"
	.align 8
.LC12:
	.ascii "clock-read proxy     : %.2f ns/call (RDTSC, not I/O syscall)\12\0"
	.align 8
.LC15:
	.ascii "thread switch (m+cv) : %.2f us/rt (%.2f us/switch, \345\220\253\345\220\214\346\255\245\345\274\200\351\224\200)\12\0"
	.align 8
.LC16:
	.ascii "== \347\254\254"
	.ascii "163\347\253\240 \347\275\221\347\273\234\347\234\237\345\256\236\345\237\272\345\207\206 (GCC 13.1 / MinGW-w64 / x86-64, localhost) ==\12\0"
	.section	.text.unlikely,"x"
.LCOLDB19:
	.section	.text.startup,"x"
.LHOTB19:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB14853:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 584
	.seh_stackalloc	584
	movaps	XMMWORD PTR 560[rsp], xmm6
	.seh_savexmm	xmm6, 560
	.seh_endprologue
	lea	rdi, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJPFvPSt6atomicIbEES5_EEEEEE[rip+16]
	movq	xmm6, rdi
	call	__main
	lea	rax, 64[rsp]
	mov	ecx, 514
	lea	rdx, 144[rsp]
	movq	xmm5, rax
	punpcklqdq	xmm6, xmm5
.LEHB7:
	call	[QWORD PTR __imp_WSAStartup[rip]]
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdi, rax
	rdtsc
	mov	ecx, 120
	mov	rsi, rax
	sal	rdx, 32
	or	rsi, rdx
	call	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0
	rdtsc
	sal	rdx, 32
	mov	rbx, rax
	or	rbx, rdx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rbx, rsi
	js	.L71
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rbx
.L72:
	sub	rax, rdi
	pxor	xmm1, xmm1
	lea	rcx, .LC3[rip]
	cvtsi2sd	xmm1, rax
	divsd	xmm1, QWORD PTR .LC2[rip]
	divsd	xmm0, xmm1
	lea	rdi, _ZL13server_threadPSt6atomicIbE[rip]
	lea	rbx, 128[rsp]
	divsd	xmm0, QWORD PTR .LC2[rip]
	movq	rdx, xmm0
	movapd	xmm1, xmm0
	movsd	QWORD PTR _ZL9g_tsc_ghz[rip], xmm0
	call	__mingw_printf
	mov	ecx, 24
	mov	BYTE PTR 64[rsp], 0
	mov	QWORD PTR 72[rsp], 0
	call	_Znwy
.LEHE7:
	lea	r8, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	mov	rdx, rbx
	mov	QWORD PTR 16[rax], rdi
	movups	XMMWORD PTR [rax], xmm6
	mov	QWORD PTR 128[rsp], rax
	lea	rax, 72[rsp]
	mov	rcx, rax
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 48[rsp], rax
.LEHB8:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE8:
	mov	rcx, rbx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	jmp	.L73
.L75:
	call	sched_yield
.L73:
	movzx	eax, BYTE PTR 64[rsp]
	test	al, al
	je	.L75
	mov	ecx, 20
.LEHB9:
	call	_ZNSt11this_thread9sleep_forIxSt5ratioILx1ELx1000EEEEvRKNSt6chrono8durationIT_T0_EE.isra.0
	xor	r8d, r8d
	mov	edx, 1
	mov	ecx, 2
	call	[QWORD PTR __imp_socket[rip]]
	mov	edx, 2
	mov	rdi, rax
	mov	ecx, 54331
	mov	QWORD PTR 114[rsp], 0
	mov	WORD PTR 112[rsp], dx
	mov	QWORD PTR 120[rsp], 0
	call	[QWORD PTR __imp_htons[rip]]
	mov	WORD PTR 114[rsp], ax
	lea	r8, 116[rsp]
	mov	ecx, 2
	lea	rdx, .LC0[rip]
	call	[QWORD PTR __imp_inet_pton[rip]]
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	lea	rdx, 112[rsp]
	mov	r8d, 16
	mov	rcx, rdi
	mov	rsi, rax
	call	[QWORD PTR __imp_connect[rip]]
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm1, xmm1
	movsd	xmm6, QWORD PTR .LC4[rip]
	lea	rcx, .LC5[rip]
	sub	rax, rsi
	cvtsi2sd	xmm1, rax
	divsd	xmm1, xmm6
	movq	rdx, xmm1
	call	__mingw_printf
	mov	BYTE PTR 65[rsp], 120
	mov	esi, 200000
	mov	BYTE PTR 66[rsp], 0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r12, QWORD PTR __imp_send[rip]
	mov	rbp, QWORD PTR __imp_recv[rip]
	mov	r14, rax
	.p2align 4
	.p2align 3
.L76:
	xor	r9d, r9d
	mov	r8d, 1
	lea	rdx, 65[rsp]
	mov	rcx, rdi
	call	r12
	xor	r9d, r9d
	mov	r8d, 1
	lea	rdx, 66[rsp]
	mov	rcx, rdi
	call	rbp
	sub	esi, 1
	jne	.L76
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm1, xmm1
	lea	rcx, .LC7[rip]
	sub	rax, r14
	cvtsi2sd	xmm1, rax
	divsd	xmm1, xmm6
	divsd	xmm1, QWORD PTR .LC6[rip]
	movq	rdx, xmm1
	call	__mingw_printf
	mov	ecx, 65536
	call	_Znay
	mov	r8d, 65536
	mov	rcx, rax
	mov	r13, rax
	xor	r15d, r15d
	mov	edx, 165
	call	memset
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	QWORD PTR 56[rsp], rax
.L80:
	xor	r9d, r9d
	mov	r8d, 65536
	mov	rdx, r13
	mov	rcx, rdi
	call	r12
	movsxd	rsi, eax
	test	esi, esi
	jle	.L77
	xor	r14d, r14d
	.p2align 4
	.p2align 3
.L79:
	mov	r8d, esi
	xor	r9d, r9d
	mov	rdx, r13
	mov	rcx, rdi
	sub	r8d, r14d
	call	rbp
	test	eax, eax
	jle	.L78
	add	r14d, eax
	cmp	esi, r14d
	jg	.L79
.L78:
	add	r15, rsi
	cmp	r15, 67108863
	jbe	.L80
.L77:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm0, xmm0
	movsd	xmm1, QWORD PTR .LC8[rip]
	sub	rax, QWORD PTR 56[rsp]
	cvtsi2sd	xmm0, rax
	divsd	xmm0, QWORD PTR .LC2[rip]
	movsd	xmm3, QWORD PTR .LC9[rip]
	lea	rcx, .LC10[rip]
	divsd	xmm1, xmm0
	mulsd	xmm3, xmm1
	movq	rdx, xmm1
	movq	r8, xmm3
	movapd	xmm2, xmm3
	call	__mingw_printf
	mov	rcx, r13
	call	_ZdaPv
	rdtsc
	mov	esi, 5000000
	mov	rbp, rax
	sal	rdx, 32
	or	rbp, rdx
	.p2align 4
	.p2align 3
.L81:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	esi, 2
	jne	.L81
	rdtsc
	sal	rdx, 32
	or	rax, rdx
	sub	rax, rbp
	js	.L82
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
.L83:
	divsd	xmm0, QWORD PTR _ZL9g_tsc_ghz[rip]
	lea	rcx, .LC12[rip]
	divsd	xmm0, QWORD PTR .LC11[rip]
	movapd	xmm1, xmm0
	movq	rdx, xmm0
	call	__mingw_printf
.LEHE9:
	lea	r12, 80[rsp]
	xor	edx, edx
	lea	rsi, 88[rsp]
	mov	rcx, r12
	call	pthread_mutex_init
	mov	rcx, rsi
	call	_ZNSt18condition_variableC1Ev
	mov	ecx, 40
	mov	BYTE PTR 67[rsp], 0
	mov	DWORD PTR 68[rsp], 0
	mov	QWORD PTR 96[rsp], 0
.LEHB10:
	call	_Znwy
.LEHE10:
	movq	xmm2, r12
	mov	r8, QWORD PTR 40[rsp]
	lea	rcx, 96[rsp]
	lea	rdx, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ4mainEUlvE_EEEEEE[rip+16]
	movq	xmm0, rdx
	lea	rdx, 68[rsp]
	punpcklqdq	xmm0, xmm2
	movq	xmm5, rdx
	lea	rdx, 67[rsp]
	mov	QWORD PTR 32[rax], rdx
	mov	rdx, rbx
	movups	XMMWORD PTR [rax], xmm0
	movq	xmm0, rsi
	punpcklqdq	xmm0, xmm5
	movups	XMMWORD PTR 16[rax], xmm0
	mov	QWORD PTR 128[rsp], rax
.LEHB11:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE11:
	mov	rcx, rbx
	mov	ebp, 50000
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r14, rax
	.p2align 4
	.p2align 3
.L84:
	mov	rcx, r12
	mov	QWORD PTR 128[rsp], r12
	mov	BYTE PTR 136[rsp], 0
.LEHB12:
	call	pthread_mutex_lock
.LEHE12:
	test	eax, eax
	jne	.L115
	mov	rcx, rsi
	mov	BYTE PTR 136[rsp], 1
	mov	DWORD PTR 68[rsp], 1
	call	_ZNSt18condition_variable10notify_oneEv
	jmp	.L88
	.p2align 4,,10
	.p2align 3
.L89:
	mov	rdx, rbx
	mov	rcx, rsi
.LEHB13:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE13:
.L88:
	mov	eax, DWORD PTR 68[rsp]
	test	eax, eax
	jne	.L89
	cmp	BYTE PTR 136[rsp], 0
	jne	.L118
.L90:
	sub	ebp, 1
	jne	.L84
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, rax
	mov	eax, 1
	xchg	al, BYTE PTR 67[rsp]
	mov	rcx, r12
.LEHB14:
	call	pthread_mutex_lock
.LEHE14:
	test	eax, eax
	jne	.L116
	mov	rcx, rsi
	call	_ZNSt18condition_variable10notify_oneEv
	mov	rcx, r12
	call	pthread_mutex_unlock
	lea	rcx, 96[rsp]
.LEHB15:
	call	_ZNSt6thread4joinEv
	sub	rbx, r14
	pxor	xmm1, xmm1
	movsd	xmm4, QWORD PTR .LC14[rip]
	lea	rcx, .LC15[rip]
	cvtsi2sd	xmm1, rbx
	divsd	xmm1, xmm6
	divsd	xmm1, QWORD PTR .LC13[rip]
	mulsd	xmm4, xmm1
	movq	rdx, xmm1
	movq	r8, xmm4
	movapd	xmm2, xmm4
	call	__mingw_printf
	lea	rax, _Z9sock_sendyPKci[rip]
	mov	rcx, rdi
	mov	QWORD PTR 104[rsp], rax
	mov	rax, QWORD PTR 104[rsp]
	lea	rax, _Z9sock_recvyPci[rip]
	mov	QWORD PTR 128[rsp], rax
	mov	rax, QWORD PTR 128[rsp]
	call	[QWORD PTR __imp_closesocket[rip]]
	call	[QWORD PTR __imp_WSACleanup[rip]]
	mov	rcx, QWORD PTR 48[rsp]
	call	_ZNSt6thread4joinEv
	lea	rcx, .LC16[rip]
	call	__mingw_printf
.LEHE15:
	cmp	QWORD PTR 96[rsp], 0
	jne	.L93
	mov	rcx, rsi
	call	_ZNSt18condition_variableD1Ev
	mov	rcx, r12
	call	pthread_mutex_destroy
	cmp	QWORD PTR 72[rsp], 0
	jne	.L119
	movaps	xmm6, XMMWORD PTR 560[rsp]
	xor	eax, eax
	add	rsp, 584
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L118:
	mov	rcx, QWORD PTR 128[rsp]
	test	rcx, rcx
	je	.L90
	call	pthread_mutex_unlock
	jmp	.L90
.L71:
	mov	rdx, rbx
	and	ebx, 1
	pxor	xmm0, xmm0
	shr	rdx
	or	rdx, rbx
	cvtsi2sd	xmm0, rdx
	addsd	xmm0, xmm0
	jmp	.L72
.L82:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm0, xmm0
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm0, rdx
	addsd	xmm0, xmm0
	jmp	.L83
.L119:
	jmp	.L93
.L100:
	mov	rdi, rax
	jmp	.L94
.L113:
	jmp	.L114
.L103:
	jmp	.L85
.L98:
	mov	rcx, rax
	jmp	.L97
.L102:
	mov	rsi, rax
	jmp	.L74
.L99:
	mov	rbx, rax
	jmp	.L86
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA14853:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE14853-.LLSDACSB14853
.LLSDACSB14853:
	.uleb128 .LEHB7-.LFB14853
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB8-.LFB14853
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L102-.LFB14853
	.uleb128 0
	.uleb128 .LEHB9-.LFB14853
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L98-.LFB14853
	.uleb128 0
	.uleb128 .LEHB10-.LFB14853
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L99-.LFB14853
	.uleb128 0
	.uleb128 .LEHB11-.LFB14853
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L103-.LFB14853
	.uleb128 0
	.uleb128 .LEHB12-.LFB14853
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L113-.LFB14853
	.uleb128 0
	.uleb128 .LEHB13-.LFB14853
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L100-.LFB14853
	.uleb128 0
	.uleb128 .LEHB14-.LFB14853
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L113-.LFB14853
	.uleb128 0
	.uleb128 .LEHB15-.LFB14853
	.uleb128 .LEHE15-.LEHB15
	.uleb128 .L113-.LFB14853
	.uleb128 0
.LLSDACSE14853:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	648
	.seh_savereg	rbx, 584
	.seh_savereg	rsi, 592
	.seh_savereg	rdi, 600
	.seh_savereg	rbp, 608
	.seh_savexmm	xmm6, 560
	.seh_savereg	r12, 616
	.seh_savereg	r13, 624
	.seh_savereg	r14, 632
	.seh_savereg	r15, 640
	.seh_endprologue
main.cold:
.L85:
	mov	rcx, rbx
	mov	rbx, rax
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L86:
	mov	rcx, rsi
	call	_ZNSt18condition_variableD1Ev
	mov	rcx, r12
	call	pthread_mutex_destroy
	mov	rcx, rbx
.L97:
	cmp	QWORD PTR 72[rsp], 0
	je	.L120
.L93:
	call	_ZSt9terminatev
.L116:
	mov	ecx, eax
.LEHB16:
	call	_ZSt20__throw_system_errori
.L115:
	mov	ecx, eax
	call	_ZSt20__throw_system_errori
.LEHE16:
.L94:
	cmp	BYTE PTR 136[rsp], 0
	je	.L95
	mov	rcx, rbx
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L95:
	mov	rbx, rdi
.L96:
	cmp	QWORD PTR 96[rsp], 0
	je	.L86
	jmp	.L93
.L101:
.L114:
	mov	rbx, rax
	jmp	.L96
.L120:
.LEHB17:
	call	_Unwind_Resume
.L74:
	mov	rcx, rbx
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE17:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC14853:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC14853-.LLSDACSBC14853
.LLSDACSBC14853:
	.uleb128 .LEHB16-.LCOLDB19
	.uleb128 .LEHE16-.LEHB16
	.uleb128 .L101-.LCOLDB19
	.uleb128 0
	.uleb128 .LEHB17-.LCOLDB19
	.uleb128 .LEHE17-.LEHB17
	.uleb128 0
	.uleb128 0
.LLSDACSEC14853:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE19:
	.section	.text.startup,"x"
.LHOTE19:
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
.LC2:
	.long	0
	.long	1104006501
	.align 8
.LC4:
	.long	0
	.long	1083129856
	.align 8
.LC6:
	.long	0
	.long	1091070464
	.align 8
.LC8:
	.long	0
	.long	1078984704
	.align 8
.LC9:
	.long	0
	.long	1062207488
	.align 8
.LC11:
	.long	0
	.long	1095963344
	.align 8
.LC13:
	.long	0
	.long	1088973312
	.align 8
.LC14:
	.long	0
	.long	1071644672
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	nanosleep64;	.scl	2;	.type	32;	.endef
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
