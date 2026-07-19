	.file	"_ch120_coro_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt6thread24_M_thread_deps_never_runEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt6thread24_M_thread_deps_never_runEv
	.def	_ZNSt6thread24_M_thread_deps_never_runEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6thread24_M_thread_deps_never_runEv
_ZNSt6thread24_M_thread_deps_never_runEv:
.LFB6447:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE
	.def	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13resume_handleRNSt7__n486116coroutine_handleIvEE
_Z13resume_handleRNSt7__n486116coroutine_handleIvEE:
.LFB14261:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR [rcx]]
	.seh_endproc
	.p2align 4
	.globl	_Z10yield_stepR3GenIiE
	.def	_Z10yield_stepR3GenIiE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10yield_stepR3GenIiE
_Z10yield_stepR3GenIiE:
.LFB14262:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rcx
	mov	rcx, rax
	call	[QWORD PTR [rax]]
	mov	rax, QWORD PTR [rbx]
	mov	eax, DWORD PTR 16[rax]
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.def	_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor
_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor:
.LFB14256:
	.seh_endprologue
	movzx	eax, WORD PTR 20[rcx]
	test	al, 1
	je	.L6
	cmp	ax, 5
	ja	.L7
	mov	edx, 42
	bt	rdx, rax
	jnc	.L17
.L8:
.L16:
	sub	WORD PTR 22[rcx], 1
	jne	.L5
	cmp	BYTE PTR 24[rcx], 0
	jne	.L18
.L13:
.L5:
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	cmp	ax, 2
	je	.L9
	cmp	ax, 4
	jne	.L19
	mov	eax, DWORD PTR 28[rcx]
	lea	edx, 1[rax]
.L12:
.L14:
.L15:
	mov	DWORD PTR 16[rcx], eax
	mov	eax, 4
	mov	DWORD PTR 28[rcx], edx
	mov	WORD PTR 20[rcx], ax
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	test	ax, ax
	jne	.L20
	add	WORD PTR 22[rcx], 1
	mov	edx, 2
	mov	BYTE PTR 25[rcx], 0
	mov	WORD PTR 20[rcx], dx
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	mov	BYTE PTR 25[rcx], 1
	mov	edx, 1
	xor	eax, eax
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L18:
	jmp	free
.L20:
	jmp	.L7
.L17:
	jmp	.L7
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor.cold
	.seh_endprologue
_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor.cold:
.L7:
	ud2
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.def	_Z16infinite_counterP27_Z16infinite_counterv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterP27_Z16infinite_counterv.Frame.destroy
_Z16infinite_counterP27_Z16infinite_counterv.Frame.destroy:
.LFB14257:
	.seh_endprologue
	or	WORD PTR 20[rcx], 1
	jmp	_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.def	_Z13small_counterP24_Z13small_counteri.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13small_counterP24_Z13small_counteri.Frame.actor
_Z13small_counterP24_Z13small_counteri.Frame.actor:
.LFB14259:
	.seh_endprologue
	movzx	eax, WORD PTR 24[rcx]
	test	al, 1
	je	.L23
	cmp	ax, 7
	ja	.L39
.L25:
.L33:
.L34:
.L35:
	sub	WORD PTR 26[rcx], 1
	jne	.L22
	cmp	BYTE PTR 28[rcx], 0
	jne	.L40
.L30:
.L22:
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	cmp	ax, 4
	je	.L26
	ja	.L27
	test	ax, ax
	je	.L28
.L29:
	xor	eax, eax
	mov	BYTE PTR 29[rcx], 1
	mov	DWORD PTR 32[rcx], eax
	cmp	DWORD PTR 20[rcx], eax
	jle	.L41
.L32:
	mov	edx, 4
	mov	DWORD PTR 16[rcx], eax
	mov	WORD PTR 24[rcx], dx
	ret
	.p2align 4,,10
	.p2align 3
.L40:
	jmp	free
	.p2align 4,,10
	.p2align 3
.L26:
	mov	eax, DWORD PTR 32[rcx]
	add	eax, 1
	mov	DWORD PTR 32[rcx], eax
	cmp	DWORD PTR 20[rcx], eax
	jg	.L32
.L41:
	mov	eax, 6
	mov	QWORD PTR [rcx], 0
	mov	WORD PTR 24[rcx], ax
	ret
	.p2align 4,,10
	.p2align 3
.L28:
	add	WORD PTR 26[rcx], 1
	mov	r8d, 2
	mov	BYTE PTR 29[rcx], 0
	mov	WORD PTR 24[rcx], r8w
	ret
	.p2align 4,,10
	.p2align 3
.L27:
	cmp	ax, 6
	je	.L35
	jmp	.L24
.L39:
	jmp	.L24
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z13small_counterP24_Z13small_counteri.Frame.actor.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13small_counterP24_Z13small_counteri.Frame.actor.cold
	.seh_endprologue
_Z13small_counterP24_Z13small_counteri.Frame.actor.cold:
.L24:
	ud2
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.p2align 4
	.def	_Z13small_counterP24_Z13small_counteri.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13small_counterP24_Z13small_counteri.Frame.destroy
_Z13small_counterP24_Z13small_counteri.Frame.destroy:
.LFB14260:
	.seh_endprologue
	or	WORD PTR 24[rcx], 1
	jmp	_Z13small_counterP24_Z13small_counteri.Frame.actor
	.seh_endproc
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev:
.LFB15937:
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	jmp	_ZNSt6thread6_StateD2Ev
	.seh_endproc
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED1Ev,_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED2Ev
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEED0Ev:
.LFB15939:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE[rip+16]
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 40[rsp], rcx
	call	_ZNSt6thread6_StateD2Ev
	mov	rcx, QWORD PTR 40[rsp]
	add	rsp, 56
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_Z10ready_taskv
	.def	_Z10ready_taskv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10ready_taskv
_Z10ready_taskv:
.LFB14274:
	.seh_endprologue
	cmp	QWORD PTR _ZL11g_max_frame[rip], 39
	ja	.L45
	mov	QWORD PTR _ZL11g_max_frame[rip], 40
.L46:
.L47:
.L48:
.L49:
.L50:
.L51:
.L52:
.L53:
.L54:
.L45:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB14231:
	.seh_endprologue
	cmp	QWORD PTR _ZL11g_max_frame[rip], rcx
	jnb	.L56
	mov	QWORD PTR _ZL11g_max_frame[rip], rcx
.L56:
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB14232:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB14233:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_Z16infinite_counterv
	.def	_Z16infinite_counterv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16infinite_counterv
_Z16infinite_counterv:
.LFB14255:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	cmp	QWORD PTR _ZL11g_max_frame[rip], 39
	mov	rbx, rcx
	ja	.L66
	mov	QWORD PTR _ZL11g_max_frame[rip], 40
.L60:
.L61:
.L62:
.L63:
.L64:
.L65:
.L66:
	mov	ecx, 40
	call	malloc
	lea	rdx, _Z16infinite_counterP27_Z16infinite_counterv.Frame.destroy[rip]
	movq	xmm0, QWORD PTR .LC4[rip]
	movq	xmm1, rdx
	mov	edx, 1
	mov	QWORD PTR [rbx], rax
	punpcklqdq	xmm0, xmm1
	mov	WORD PTR 24[rax], dx
	mov	DWORD PTR 20[rax], 65538
	movups	XMMWORD PTR [rax], xmm0
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13small_counteri
	.def	_Z13small_counteri;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13small_counteri
_Z13small_counteri:
.LFB14258:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	cmp	QWORD PTR _ZL11g_max_frame[rip], 39
	mov	rbx, rcx
	mov	esi, edx
	ja	.L74
	mov	QWORD PTR _ZL11g_max_frame[rip], 40
.L68:
.L69:
.L70:
.L71:
.L72:
.L73:
.L74:
	mov	ecx, 40
	call	malloc
	lea	rdx, _Z13small_counterP24_Z13small_counteri.Frame.destroy[rip]
	movq	xmm0, QWORD PTR .LC5[rip]
	movq	xmm1, rdx
	mov	edx, 1
	mov	DWORD PTR 20[rax], esi
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR [rbx], rax
	mov	WORD PTR 28[rax], dx
	mov	DWORD PTR 24[rax], 65538
	movups	XMMWORD PTR [rax], xmm0
	mov	rax, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
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
.LFB14882:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rdx, rcx
	cmp	BYTE PTR 8[rcx], 0
	je	.L81
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L75
	mov	QWORD PTR 48[rsp], rdx
	call	pthread_mutex_unlock
	mov	rdx, QWORD PTR 48[rsp]
	mov	BYTE PTR 8[rdx], 0
.L75:
	add	rsp, 40
	ret
.L81:
	mov	ecx, 1
	call	_ZSt20__throw_system_errori
	nop
	.seh_endproc
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB6:
	.text
.LHOTB6:
	.align 2
	.p2align 4
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv:
.LFB16132:
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
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rbx, rcx
	mov	rcx, QWORD PTR 8[rcx]
	mov	BYTE PTR 40[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	test	rcx, rcx
	je	.L91
	xor	r12d, r12d
	lea	rbp, 32[rsp]
	jmp	.L83
	.p2align 4,,10
	.p2align 3
.L85:
	mov	rax, QWORD PTR 32[rbx]
	movzx	eax, BYTE PTR [rax]
	test	al, al
	jne	.L87
	mov	rax, QWORD PTR 24[rbx]
	cmp	BYTE PTR 40[rsp], 0
	mov	DWORD PTR [rax], 0
	je	.L115
	mov	rcx, QWORD PTR 32[rsp]
	test	rcx, rcx
	je	.L89
.LEHB0:
	call	pthread_mutex_unlock
.LEHE0:
	mov	BYTE PTR 40[rsp], 0
.L89:
	mov	rcx, QWORD PTR 16[rbx]
	add	r12, 7
	call	_ZNSt18condition_variable10notify_oneEv
	cmp	BYTE PTR 40[rsp], 0
	jne	.L117
.L90:
	mov	rcx, QWORD PTR 8[rbx]
	mov	BYTE PTR 40[rsp], 0
	mov	QWORD PTR 32[rsp], rcx
	test	rcx, rcx
	je	.L118
.L83:
.LEHB1:
	call	pthread_mutex_lock
.LEHE1:
	test	eax, eax
	jne	.L114
	mov	rdi, QWORD PTR 16[rbx]
	mov	rsi, QWORD PTR 24[rbx]
	mov	BYTE PTR 40[rsp], 1
	mov	r13, QWORD PTR 32[rbx]
	.p2align 4
	.p2align 3
.L86:
	cmp	DWORD PTR [rsi], 1
	je	.L85
	movzx	eax, BYTE PTR 0[r13]
	test	al, al
	jne	.L85
	mov	rdx, rbp
	mov	rcx, rdi
.LEHB2:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE2:
	jmp	.L86
	.p2align 4,,10
	.p2align 3
.L117:
	mov	rcx, QWORD PTR 32[rsp]
	test	rcx, rcx
	je	.L90
	call	pthread_mutex_unlock
	jmp	.L90
	.p2align 4,,10
	.p2align 3
.L87:
	cmp	BYTE PTR 40[rsp], 0
	jne	.L119
.L92:
	mov	rax, QWORD PTR 40[rbx]
	lock add	QWORD PTR [rax], r12
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L119:
	mov	rcx, QWORD PTR 32[rsp]
	test	rcx, rcx
	je	.L92
	call	pthread_mutex_unlock
	jmp	.L92
.L118:
	jmp	.L91
.L112:
	jmp	.L113
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA16132:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE16132-.LLSDACSB16132
.LLSDACSB16132:
	.uleb128 .LEHB0-.LFB16132
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L112-.LFB16132
	.uleb128 0
	.uleb128 .LEHB1-.LFB16132
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB2-.LFB16132
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L112-.LFB16132
	.uleb128 0
.LLSDACSE16132:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_savereg	rdi, 72
	.seh_savereg	rbp, 80
	.seh_savereg	r12, 88
	.seh_savereg	r13, 96
	.seh_endprologue
_ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEE6_M_runEv.cold:
.L91:
	mov	ecx, 1
.LEHB3:
	call	_ZSt20__throw_system_errori
.LEHE3:
.L115:
	mov	ecx, 1
.LEHB4:
	call	_ZSt20__throw_system_errori
.LEHE4:
.L114:
	mov	ecx, eax
.LEHB5:
	call	_ZSt20__throw_system_errori
.LEHE5:
.L96:
.L113:
	mov	rbx, rax
	cmp	BYTE PTR 40[rsp], 0
	je	.L94
	lea	rcx, 32[rsp]
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L94:
	mov	rcx, rbx
.LEHB6:
	call	_Unwind_Resume
	nop
.LEHE6:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC16132:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC16132-.LLSDACSBC16132
.LLSDACSBC16132:
	.uleb128 .LEHB3-.LCOLDB6
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB6
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L96-.LCOLDB6
	.uleb128 0
	.uleb128 .LEHB5-.LCOLDB6
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LCOLDB6
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC16132:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.text
.LHOTE6:
	.section	.text$_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	.def	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev:
.LFB15245:
	.seh_endprologue
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L120
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 8[rax]]
	.p2align 4,,10
	.p2align 3
.L120:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC8:
	.ascii "TSC freq: %.3f GHz\12\0"
.LC9:
	.ascii "impossible\12\0"
	.align 8
.LC14:
	.ascii "== \347\254\254"
	.ascii "120\347\253\240 \345\215\217\347\250\213\347\234\237\345\256\236\345\237\272\345\207\206 (GCC 13.1 / MinGW-w64 / x86-64) ==\12\0"
	.align 8
.LC15:
	.ascii "frame_size(max coroutine frame) : %zu B\12\0"
	.align 8
.LC16:
	.ascii "resume+yield per step          : %.2f ns\12\0"
	.align 8
.LC17:
	.ascii "create+first-step+destroy      : %.2f ns\12\0"
	.align 8
.LC18:
	.ascii "thread switch (mutex+cv rt)     : %.2f ns (%.3f us, \345\220\253\345\220\214\346\255\245\345\274\200\351\224\200)\12\0"
	.section	.text.unlikely,"x"
.LCOLDB22:
	.section	.text.startup,"x"
.LHOTB22:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB14289:
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
	sub	rsp, 200
	.seh_stackalloc	200
	movaps	XMMWORD PTR 128[rsp], xmm6
	.seh_savexmm	xmm6, 128
	movaps	XMMWORD PTR 144[rsp], xmm7
	.seh_savexmm	xmm7, 144
	movaps	XMMWORD PTR 160[rsp], xmm8
	.seh_savexmm	xmm8, 160
	movaps	XMMWORD PTR 176[rsp], xmm9
	.seh_savexmm	xmm9, 176
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rsi, rax
	rdtsc
	mov	rbx, QWORD PTR __imp__errno[rip]
	mov	QWORD PTR 112[rsp], 0
	mov	rbp, rax
	sal	rdx, 32
	lea	rdi, 112[rsp]
	mov	DWORD PTR 120[rsp], 120000000
	or	rbp, rdx
.L124:
	mov	rdx, rdi
	mov	rcx, rdi
.LEHB7:
	call	nanosleep64
	cmp	eax, -1
	je	.L173
.L123:
	rdtsc
	sal	rdx, 32
	mov	rbx, rax
	or	rbx, rdx
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rbx, rbp
	js	.L125
	pxor	xmm1, xmm1
	cvtsi2sd	xmm1, rbx
.L126:
	movsd	xmm2, QWORD PTR .LC7[rip]
	sub	rax, rsi
	pxor	xmm0, xmm0
	lea	rcx, .LC8[rip]
	cvtsi2sd	xmm0, rax
	divsd	xmm0, xmm2
	divsd	xmm1, xmm0
	divsd	xmm1, xmm2
	movq	rdx, xmm1
	movsd	QWORD PTR _ZL9g_tsc_ghz[rip], xmm1
	call	__mingw_printf
.LEHE7:
	lea	rcx, 104[rsp]
	call	_Z16infinite_counterv
	mov	rbp, QWORD PTR 104[rsp]
	rdtsc
	mov	r12, rax
	sal	rdx, 32
	or	r12, rdx
	rdtsc
	mov	r13, rax
	sal	rdx, 32
	or	r13, rdx
	rdtsc
	mov	ebx, 2000000
	movabs	rsi, 1999999000000
	mov	r14, rax
	sal	rdx, 32
	or	r14, rdx
	.p2align 4
	.p2align 3
.L127:
	lea	rcx, 104[rsp]
	mov	QWORD PTR 104[rsp], rbp
.LEHB8:
	call	_Z10yield_stepR3GenIiE
.LEHE8:
	cdqe
	add	rsi, rax
	sub	ebx, 1
	jne	.L127
	rdtsc
	movsd	xmm8, QWORD PTR _ZL9g_tsc_ghz[rip]
	mov	r15, rax
	sal	rdx, 32
	or	r15, rdx
	test	rsi, rsi
	je	.L128
.L131:
	test	rbp, rbp
	je	.L130
	mov	rcx, rbp
	call	[QWORD PTR 8[rbp]]
.L130:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	esi, 200000
	mov	QWORD PTR 40[rsp], rax
	.p2align 4
	.p2align 3
.L132:
	mov	rcx, rdi
	mov	edx, 4
	call	_Z13small_counteri
	mov	rbx, QWORD PTR 112[rsp]
	mov	rcx, rbx
.LEHB9:
	call	[QWORD PTR [rbx]]
.LEHE9:
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
	sub	esi, 1
	jne	.L132
	lea	rax, _ZTVNSt6thread11_State_implINS_8_InvokerISt5tupleIJZL19bench_thread_switchvEUlvE_EEEEEE[rip+16]
	lea	rsi, 72[rsp]
	movq	xmm7, rax
	lea	rax, 68[rsp]
	movq	xmm4, rsi
	movq	xmm5, rax
	lea	rax, 67[rsp]
	lea	rbp, 80[rsp]
	movq	xmm6, rax
	lea	rax, 88[rsp]
	punpcklqdq	xmm7, xmm4
	movq	xmm9, rbp
	movq	xmm4, rax
	punpcklqdq	xmm9, xmm5
	punpcklqdq	xmm6, xmm4
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xor	edx, edx
	mov	rcx, rsi
	mov	QWORD PTR 48[rsp], rax
	call	pthread_mutex_init
	mov	rcx, rbp
	call	_ZNSt18condition_variableC1Ev
	mov	ecx, 48
	mov	BYTE PTR 67[rsp], 0
	mov	DWORD PTR 68[rsp], 0
	mov	QWORD PTR 88[rsp], 0
	mov	QWORD PTR 96[rsp], 0
	call	_Znwy
	lea	r8, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
	mov	rdx, rdi
	mov	QWORD PTR 112[rsp], rax
	movups	XMMWORD PTR [rax], xmm7
	movups	XMMWORD PTR 16[rax], xmm9
	movups	XMMWORD PTR 32[rax], xmm6
	lea	rax, 96[rsp]
	mov	rcx, rax
	mov	QWORD PTR 32[rsp], rax
.LEHB10:
	call	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE
.LEHE10:
	mov	rcx, rdi
	mov	ebx, 50000
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	QWORD PTR 56[rsp], rax
	.p2align 4
	.p2align 3
.L137:
	mov	rcx, rsi
	mov	QWORD PTR 112[rsp], rsi
	mov	BYTE PTR 120[rsp], 0
.LEHB11:
	call	pthread_mutex_lock
.LEHE11:
	test	eax, eax
	jne	.L169
	mov	rcx, rbp
	mov	BYTE PTR 120[rsp], 1
	mov	DWORD PTR 68[rsp], 1
	call	_ZNSt18condition_variable10notify_oneEv
	jmp	.L141
	.p2align 4,,10
	.p2align 3
.L142:
	mov	rdx, rdi
	mov	rcx, rbp
.LEHB12:
	call	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE
.LEHE12:
.L141:
	mov	eax, DWORD PTR 68[rsp]
	test	eax, eax
	jne	.L142
	cmp	BYTE PTR 120[rsp], 0
	jne	.L174
.L143:
	sub	ebx, 1
	jne	.L137
	add	r13, r14
	mov	rax, r12
	sub	rax, r13
	add	rax, r15
	js	.L144
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
.L145:
	movsd	xmm7, QWORD PTR .LC11[rip]
	mov	rax, QWORD PTR 48[rsp]
	divsd	xmm0, xmm8
	pxor	xmm8, xmm8
	sub	rax, QWORD PTR 40[rsp]
	cvtsi2sd	xmm8, rax
	divsd	xmm8, xmm7
	divsd	xmm0, QWORD PTR .LC10[rip]
	movapd	xmm9, xmm0
	mulsd	xmm8, xmm7
	divsd	xmm8, QWORD PTR .LC12[rip]
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r12, rax
	mov	eax, 1
	xchg	al, BYTE PTR 67[rsp]
	mov	rcx, rsi
.LEHB13:
	call	pthread_mutex_lock
.LEHE13:
	test	eax, eax
	jne	.L170
	mov	rcx, rbp
	call	_ZNSt18condition_variable10notify_oneEv
	mov	rcx, rsi
	call	pthread_mutex_unlock
	mov	rcx, QWORD PTR 32[rsp]
.LEHB14:
	call	_ZNSt6thread4joinEv
.LEHE14:
	sub	r12, QWORD PTR 56[rsp]
	pxor	xmm6, xmm6
	cvtsi2sd	xmm6, r12
	divsd	xmm6, xmm7
	mulsd	xmm6, xmm7
	divsd	xmm6, QWORD PTR .LC13[rip]
	cmp	QWORD PTR 96[rsp], 0
	jne	.L151
	mov	rcx, rbp
	call	_ZNSt18condition_variableD1Ev
	mov	rcx, rsi
	call	pthread_mutex_destroy
	lea	rax, _Z13resume_handleRNSt7__n486116coroutine_handleIvEE[rip]
	mov	rsi, QWORD PTR _ZL11g_max_frame[rip]
	lea	rcx, .LC14[rip]
	mov	QWORD PTR 88[rsp], rax
	lea	rax, _Z10yield_stepR3GenIiE[rip]
	mov	QWORD PTR 96[rsp], rax
	lea	rax, _Z10ready_taskv[rip]
	mov	QWORD PTR 112[rsp], rax
	mov	rax, QWORD PTR 88[rsp]
	mov	rax, QWORD PTR 96[rsp]
	mov	rax, QWORD PTR 112[rsp]
.LEHB15:
	call	__mingw_printf
	mov	rdx, rsi
	lea	rcx, .LC15[rip]
	call	__mingw_printf
	movapd	xmm1, xmm9
	movq	rdx, xmm9
	lea	rcx, .LC16[rip]
	call	__mingw_printf
	movapd	xmm1, xmm8
	movq	rdx, xmm8
	lea	rcx, .LC17[rip]
	call	__mingw_printf
	movapd	xmm3, xmm6
	movapd	xmm1, xmm6
	movq	rdx, xmm6
	divsd	xmm3, xmm7
	lea	rcx, .LC18[rip]
	movq	r8, xmm3
	movapd	xmm2, xmm3
	call	__mingw_printf
	nop
.LEHE15:
	movaps	xmm6, XMMWORD PTR 128[rsp]
	movaps	xmm7, XMMWORD PTR 144[rsp]
	xor	eax, eax
	movaps	xmm8, XMMWORD PTR 160[rsp]
	movaps	xmm9, XMMWORD PTR 176[rsp]
	add	rsp, 200
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
.L174:
	mov	rcx, QWORD PTR 112[rsp]
	test	rcx, rcx
	je	.L143
	call	pthread_mutex_unlock
	jmp	.L143
.L125:
	mov	rdx, rbx
	and	ebx, 1
	pxor	xmm1, xmm1
	shr	rdx
	or	rdx, rbx
	cvtsi2sd	xmm1, rdx
	addsd	xmm1, xmm1
	jmp	.L126
.L173:
.LEHB16:
	call	rbx
.LEHE16:
	cmp	DWORD PTR [rax], 4
	jne	.L123
	jmp	.L124
.L144:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm0, xmm0
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm0, rdx
	addsd	xmm0, xmm0
	jmp	.L145
.L128:
	lea	rcx, .LC9[rip]
.LEHB17:
	call	__mingw_printf
.LEHE17:
	jmp	.L131
.L153:
	mov	rbx, rax
	jmp	.L148
.L155:
	mov	rbx, rax
	jmp	.L133
.L167:
	jmp	.L168
.L156:
	mov	rbx, rax
	jmp	.L138
.L154:
	mov	rsi, rax
	jmp	.L136
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA14289:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE14289-.LLSDACSB14289
.LLSDACSB14289:
	.uleb128 .LEHB7-.LFB14289
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB8-.LFB14289
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L155-.LFB14289
	.uleb128 0
	.uleb128 .LEHB9-.LFB14289
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L154-.LFB14289
	.uleb128 0
	.uleb128 .LEHB10-.LFB14289
	.uleb128 .LEHE10-.LEHB10
	.uleb128 .L156-.LFB14289
	.uleb128 0
	.uleb128 .LEHB11-.LFB14289
	.uleb128 .LEHE11-.LEHB11
	.uleb128 .L167-.LFB14289
	.uleb128 0
	.uleb128 .LEHB12-.LFB14289
	.uleb128 .LEHE12-.LEHB12
	.uleb128 .L153-.LFB14289
	.uleb128 0
	.uleb128 .LEHB13-.LFB14289
	.uleb128 .LEHE13-.LEHB13
	.uleb128 .L167-.LFB14289
	.uleb128 0
	.uleb128 .LEHB14-.LFB14289
	.uleb128 .LEHE14-.LEHB14
	.uleb128 .L167-.LFB14289
	.uleb128 0
	.uleb128 .LEHB15-.LFB14289
	.uleb128 .LEHE15-.LEHB15
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB16-.LFB14289
	.uleb128 .LEHE16-.LEHB16
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB17-.LFB14289
	.uleb128 .LEHE17-.LEHB17
	.uleb128 .L155-.LFB14289
	.uleb128 0
.LLSDACSE14289:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	264
	.seh_savereg	rbx, 200
	.seh_savereg	rsi, 208
	.seh_savereg	rdi, 216
	.seh_savereg	rbp, 224
	.seh_savexmm	xmm6, 128
	.seh_savexmm	xmm7, 144
	.seh_savereg	r12, 232
	.seh_savereg	r13, 240
	.seh_savereg	r14, 248
	.seh_savereg	r15, 256
	.seh_savexmm	xmm8, 160
	.seh_savexmm	xmm9, 176
	.seh_endprologue
main.cold:
.L148:
	cmp	BYTE PTR 120[rsp], 0
	je	.L150
	mov	rcx, rdi
	call	_ZNSt11unique_lockISt5mutexE6unlockEv
.L150:
	cmp	QWORD PTR 96[rsp], 0
	je	.L139
.L151:
	call	_ZSt9terminatev
.L133:
	test	rbp, rbp
	je	.L134
	mov	rcx, rbp
	call	[QWORD PTR 8[rbp]]
.L134:
	mov	rcx, rbx
.LEHB18:
	call	_Unwind_Resume
.LEHE18:
.L138:
	mov	rcx, rdi
	call	_ZNSt10unique_ptrINSt6thread6_StateESt14default_deleteIS1_EED1Ev
.L139:
	mov	rcx, rbp
	call	_ZNSt18condition_variableD1Ev
	mov	rcx, rsi
	call	pthread_mutex_destroy
	mov	rcx, rbx
.LEHB19:
	call	_Unwind_Resume
.LEHE19:
.L169:
	mov	ecx, eax
.LEHB20:
	call	_ZSt20__throw_system_errori
.LEHE20:
.L152:
.L168:
	mov	rbx, rax
	jmp	.L150
.L136:
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
	mov	rcx, rsi
.LEHB21:
	call	_Unwind_Resume
.LEHE21:
.L170:
	mov	ecx, eax
.LEHB22:
	call	_ZSt20__throw_system_errori
	nop
.LEHE22:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC14289:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC14289-.LLSDACSBC14289
.LLSDACSBC14289:
	.uleb128 .LEHB18-.LCOLDB22
	.uleb128 .LEHE18-.LEHB18
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB19-.LCOLDB22
	.uleb128 .LEHE19-.LEHB19
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB20-.LCOLDB22
	.uleb128 .LEHE20-.LEHB20
	.uleb128 .L152-.LCOLDB22
	.uleb128 0
	.uleb128 .LEHB21-.LCOLDB22
	.uleb128 .LEHE21-.LEHB21
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB22-.LCOLDB22
	.uleb128 .LEHE22-.LEHB22
	.uleb128 .L152-.LCOLDB22
	.uleb128 0
.LLSDACSEC14289:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE22:
	.section	.text.startup,"x"
.LHOTE22:
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
.LC4:
	.quad	_Z16infinite_counterP27_Z16infinite_counterv.Frame.actor
	.align 8
.LC5:
	.quad	_Z13small_counterP24_Z13small_counteri.Frame.actor
	.align 8
.LC7:
	.long	0
	.long	1104006501
	.align 8
.LC10:
	.long	0
	.long	1094616192
	.align 8
.LC11:
	.long	0
	.long	1083129856
	.align 8
.LC12:
	.long	0
	.long	1091070464
	.align 8
.LC13:
	.long	0
	.long	1088973312
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread6_StateD2Ev;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variable10notify_oneEv;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variable4waitERSt11unique_lockISt5mutexE;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	nanosleep64;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variableC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread15_M_start_threadESt10unique_ptrINS_6_StateESt14default_deleteIS1_EEPFvvE;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6thread4joinEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt18condition_variableD1Ev;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	_ZSt9terminatev;	.scl	2;	.type	32;	.endef
