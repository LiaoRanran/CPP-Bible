	.file	"_ch113_co.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt7__n486116coroutine_handleIvE12from_addressEPv,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv
	.def	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv
_ZNSt7__n486116coroutine_handleIvE12from_addressEPv:
.LFB115:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR -8[rbp], 0
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486114suspend_always11await_readyEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486114suspend_always11await_readyEv
	.def	_ZNKSt7__n486114suspend_always11await_readyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486114suspend_always11await_readyEv
_ZNKSt7__n486114suspend_always11await_readyEv:
.LFB151:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, 0
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	.def	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE:
.LFB152:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486114suspend_always12await_resumeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486114suspend_always12await_resumeEv
	.def	_ZNKSt7__n486114suspend_always12await_resumeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486114suspend_always12await_resumeEv
_ZNKSt7__n486114suspend_always12await_resumeEv:
.LFB153:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4task12promise_type17get_return_objectEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4task12promise_type17get_return_objectEv
	.def	_ZN4task12promise_type17get_return_objectEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4task12promise_type17get_return_objectEv
_ZN4task12promise_type17get_return_objectEv:
.LFB316:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN4taskC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4task12promise_type15initial_suspendEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4task12promise_type15initial_suspendEv
	.def	_ZN4task12promise_type15initial_suspendEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4task12promise_type15initial_suspendEv
_ZN4task12promise_type15initial_suspendEv:
.LFB317:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4task12promise_type13final_suspendEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4task12promise_type13final_suspendEv
	.def	_ZN4task12promise_type13final_suspendEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4task12promise_type13final_suspendEv
_ZN4task12promise_type13final_suspendEv:
.LFB318:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4task12promise_type11return_voidEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4task12promise_type11return_voidEv
	.def	_ZN4task12promise_type11return_voidEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4task12promise_type11return_voidEv
_ZN4task12promise_type11return_voidEv:
.LFB319:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4taskC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4taskC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE
	.def	_ZN4taskC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4taskC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE
_ZN4taskC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE:
.LFB323:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN4taskD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN4taskD1Ev
	.def	_ZN4taskD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN4taskD1Ev
_ZN4taskD1Ev:
.LFB326:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvbEv
	test	al, al
	je	.L17
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7destroyEv
.L17:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA326:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE326-.LLSDACSB326
.LLSDACSB326:
.LLSDACSE326:
	.section	.text$_ZN4taskD1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZN9generator12promise_type17get_return_objectEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generator12promise_type17get_return_objectEv
	.def	_ZN9generator12promise_type17get_return_objectEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generator12promise_type17get_return_objectEv
_ZN9generator12promise_type17get_return_objectEv:
.LFB328:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 24[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_promiseERS2_
	mov	rdx, rax
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZN9generatorC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE
	mov	rax, QWORD PTR 16[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9generator12promise_type15initial_suspendEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generator12promise_type15initial_suspendEv
	.def	_ZN9generator12promise_type15initial_suspendEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generator12promise_type15initial_suspendEv
_ZN9generator12promise_type15initial_suspendEv:
.LFB329:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9generator12promise_type13final_suspendEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generator12promise_type13final_suspendEv
	.def	_ZN9generator12promise_type13final_suspendEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generator12promise_type13final_suspendEv
_ZN9generator12promise_type13final_suspendEv:
.LFB330:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9generator12promise_type11yield_valueEi,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generator12promise_type11yield_valueEi
	.def	_ZN9generator12promise_type11yield_valueEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generator12promise_type11yield_valueEi
_ZN9generator12promise_type11yield_valueEi:
.LFB331:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	DWORD PTR 24[rbp], edx
	mov	rax, QWORD PTR 16[rbp]
	mov	edx, DWORD PTR 24[rbp]
	mov	DWORD PTR [rax], edx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9generator12promise_type11return_voidEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generator12promise_type11return_voidEv
	.def	_ZN9generator12promise_type11return_voidEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generator12promise_type11return_voidEv
_ZN9generator12promise_type11return_voidEv:
.LFB332:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9generatorC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generatorC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE
	.def	_ZN9generatorC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generatorC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE
_ZN9generatorC1ENSt7__n486116coroutine_handleINS_12promise_typeEEE:
.LFB336:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	rax, QWORD PTR 16[rbp]
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN9generatorD1Ev,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generatorD1Ev
	.def	_ZN9generatorD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generatorD1Ev
_ZN9generatorD1Ev:
.LFB339:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv
	test	al, al
	je	.L30
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7destroyEv
.L30:
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA339:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE339-.LLSDACSB339
.LLSDACSB339:
.LLSDACSE339:
	.section	.text$_ZN9generatorD1Ev,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZN9generator4nextEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZN9generator4nextEv
	.def	_ZN9generator4nextEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN9generator4nextEv
_ZN9generator4nextEv:
.LFB340:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv
	xor	eax, 1
	test	al, al
	jne	.L32
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv
	test	al, al
	je	.L33
.L32:
	mov	eax, 1
	jmp	.L34
.L33:
	mov	eax, 0
.L34:
	test	al, al
	je	.L35
	mov	eax, 0
	jmp	.L36
.L35:
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE6resumeEv
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv
	xor	eax, 1
.L36:
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNK9generator5valueEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNK9generator5valueEv
	.def	_ZNK9generator5valueEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK9generator5valueEv
_ZNK9generator5valueEv:
.LFB341:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7promiseEv
	mov	eax, DWORD PTR [rax]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z5rangei
	.def	_Z5rangei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5rangei
_Z5rangei:
.LFB342:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	DWORD PTR 40[rbp], edx
	mov	eax, 40
	mov	rcx, rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	BYTE PTR 28[rax], 1
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z5rangeP15_Z5rangei.Frame.actor[rip]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z5rangeP15_Z5rangei.Frame.destroy[rip]
	mov	QWORD PTR 8[rax], rdx
	mov	edx, DWORD PTR 40[rbp]
	mov	rax, QWORD PTR -8[rbp]
	mov	DWORD PTR 20[rax], edx
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, DWORD PTR 20[rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	DWORD PTR 16[rax], edx
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 26[rax], 1
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 24[rax], 0
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, 16[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN9generator12promise_type17get_return_objectEv
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
.LEHB1:
	call	_Z5rangeP15_Z5rangei.Frame.actor
.LEHE1:
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 26[rax]
	lea	edx, -1[rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 26[rax], dx
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 26[rax]
	test	ax, ax
	jne	.L45
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
	jmp	.L45
.L44:
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN9generatorD1Ev
	mov	rcx, rbx
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 26[rax]
	lea	edx, -1[rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 26[rax], dx
	mov	rbx, rcx
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 26[rax]
	test	ax, ax
	jne	.L43
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
.L43:
	mov	rax, rbx
	mov	rcx, rax
.LEHB2:
	call	_Unwind_Resume
.LEHE2:
.L45:
	mov	rax, QWORD PTR 32[rbp]
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA342:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE342-.LLSDACSB342
.LLSDACSB342:
	.uleb128 .LEHB0-.LFB342
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB342
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L44-.LFB342
	.uleb128 0
	.uleb128 .LEHB2-.LFB342
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE342:
	.text
	.seh_endproc
	.def	_Z5rangeP15_Z5rangei.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangeP15_Z5rangei.Frame.actor
_Z5rangeP15_Z5rangei.Frame.actor:
.LFB343:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	lea	rbp, 64[rsp]
	.seh_setframe	rbp, 64
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 24[rax]
	and	eax, 1
	test	ax, ax
	je	.L47
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 24[rax]
	movzx	eax, ax
	cmp	eax, 7
	je	.L56
	cmp	eax, 7
	jg	.L57
	cmp	eax, 5
	je	.L55
	cmp	eax, 5
	jg	.L57
	cmp	eax, 1
	je	.L74
	cmp	eax, 3
	je	.L54
	jmp	.L57
.L47:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 24[rax]
	movzx	eax, ax
	cmp	eax, 6
	je	.L66
	cmp	eax, 6
	jg	.L57
	cmp	eax, 4
	je	.L65
	cmp	eax, 4
	jg	.L57
	test	eax, eax
	je	.L61
	cmp	eax, 2
	je	.L64
	jmp	.L57
.L61:
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 29[rax], 0
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 26[rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 26[rax], dx
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN9generator12promise_type15initial_suspendEv
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 24[rax], 2
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 30
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	jne	.L63
	jmp	.L64
.L57:
	ud2
.L63:
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 30[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv
	mov	QWORD PTR -24[rbp], rax
	lea	rax, -24[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L67
.L54:
	jmp	.L53
.L64:
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 29[rax], 1
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 30
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 32[rax], 0
	jmp	.L68
.L69:
	mov	rax, QWORD PTR 32[rbp]
	lea	rcx, 16[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 32[rax]
	mov	edx, eax
	call	_ZN9generator12promise_type11yield_valueEi
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 24[rax], 4
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 36
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L65
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 36[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv
	mov	QWORD PTR -16[rbp], rax
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L67
.L55:
	jmp	.L53
.L65:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 36
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 32[rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 32[rax], edx
.L68:
	mov	rax, QWORD PTR 32[rbp]
	mov	edx, DWORD PTR 32[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 20[rax]
	cmp	edx, eax
	jl	.L69
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN9generator12promise_type11return_voidEv
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR [rax], 0
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN9generator12promise_type13final_suspendEv
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 24[rax], 6
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 37
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L66
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 37[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv
	mov	QWORD PTR -8[rbp], rax
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L67
.L56:
	jmp	.L53
.L66:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 37
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	jmp	.L53
.L74:
	nop
.L53:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 26[rax]
	lea	edx, -1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 26[rax], dx
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 26[rax]
	test	ax, ax
	jne	.L75
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, BYTE PTR 28[rax]
	test	al, al
	je	.L75
	mov	rax, QWORD PTR 32[rbp]
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
	jmp	.L75
.L67:
.L75:
	nop
	add	rsp, 72
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.def	_Z5rangeP15_Z5rangei.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangeP15_Z5rangei.Frame.destroy
_Z5rangeP15_Z5rangei.Frame.destroy:
.LFB344:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	movzx	eax, WORD PTR 24[rax]
	or	eax, 1
	mov	edx, eax
	mov	rax, QWORD PTR 16[rbp]
	mov	WORD PTR 24[rax], dx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_Z5rangeP15_Z5rangei.Frame.actor
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z8count_upv
	.def	_Z8count_upv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8count_upv
_Z8count_upv:
.LFB345:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	eax, 40
	mov	rcx, rax
.LEHB3:
	call	_Znwy
.LEHE3:
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	BYTE PTR 22[rax], 1
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z8count_upP18_Z8count_upv.Frame.actor[rip]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z8count_upP18_Z8count_upv.Frame.destroy[rip]
	mov	QWORD PTR 8[rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 20[rax], 1
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 18[rax], 0
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, 16[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN4task12promise_type17get_return_objectEv
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
.LEHB4:
	call	_Z8count_upP18_Z8count_upv.Frame.actor
.LEHE4:
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 20[rax]
	lea	edx, -1[rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 20[rax], dx
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 20[rax]
	test	ax, ax
	jne	.L84
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
	jmp	.L84
.L83:
	mov	rbx, rax
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN4taskD1Ev
	mov	rcx, rbx
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 20[rax]
	lea	edx, -1[rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 20[rax], dx
	mov	rbx, rcx
	mov	rax, QWORD PTR -8[rbp]
	movzx	eax, WORD PTR 20[rax]
	test	ax, ax
	jne	.L82
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
.L82:
	mov	rax, rbx
	mov	rcx, rax
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L84:
	mov	rax, QWORD PTR 32[rbp]
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA345:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE345-.LLSDACSB345
.LLSDACSB345:
	.uleb128 .LEHB3-.LFB345
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB4-.LFB345
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L83-.LFB345
	.uleb128 0
	.uleb128 .LEHB5-.LFB345
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE345:
	.text
	.seh_endproc
	.def	_Z8count_upP18_Z8count_upv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upP18_Z8count_upv.Frame.actor
_Z8count_upP18_Z8count_upv.Frame.actor:
.LFB346:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 72
	.seh_stackalloc	72
	lea	rbp, 64[rsp]
	.seh_setframe	rbp, 64
	.seh_endprologue
	mov	QWORD PTR 32[rbp], rcx
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 18[rax]
	and	eax, 1
	test	ax, ax
	je	.L86
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 18[rax]
	movzx	eax, ax
	cmp	eax, 7
	je	.L95
	cmp	eax, 7
	jg	.L96
	cmp	eax, 5
	je	.L94
	cmp	eax, 5
	jg	.L96
	cmp	eax, 1
	je	.L113
	cmp	eax, 3
	je	.L93
	jmp	.L96
.L86:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 18[rax]
	movzx	eax, ax
	cmp	eax, 6
	je	.L105
	cmp	eax, 6
	jg	.L96
	cmp	eax, 4
	je	.L104
	cmp	eax, 4
	jg	.L96
	test	eax, eax
	je	.L100
	cmp	eax, 2
	je	.L103
	jmp	.L96
.L100:
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 23[rax], 0
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 20[rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 20[rax], dx
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN4task12promise_type15initial_suspendEv
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 18[rax], 2
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	jne	.L102
	jmp	.L103
.L96:
	ud2
.L102:
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 24[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv
	mov	QWORD PTR -24[rbp], rax
	lea	rax, -24[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L106
.L93:
	jmp	.L92
.L103:
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 23[rax], 1
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 28[rax], 0
	jmp	.L107
.L108:
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 18[rax], 4
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 32
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L104
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 32[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv
	mov	QWORD PTR -16[rbp], rax
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L106
.L94:
	jmp	.L92
.L104:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 32
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 28[rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 28[rax], edx
.L107:
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 28[rax]
	cmp	eax, 2
	jle	.L108
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN4task12promise_type11return_voidEv
	mov	rax, QWORD PTR 32[rbp]
	mov	QWORD PTR [rax], 0
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN4task12promise_type13final_suspendEv
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 18[rax], 6
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 33
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L105
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 33[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv
	mov	QWORD PTR -8[rbp], rax
	lea	rax, -8[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L106
.L95:
	jmp	.L92
.L105:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 33
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	jmp	.L92
.L113:
	nop
.L92:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 20[rax]
	lea	edx, -1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 20[rax], dx
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 20[rax]
	test	ax, ax
	jne	.L114
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, BYTE PTR 22[rax]
	test	al, al
	je	.L114
	mov	rax, QWORD PTR 32[rbp]
	mov	edx, 40
	mov	rcx, rax
	call	_ZdlPvy
	jmp	.L114
.L106:
.L114:
	nop
	add	rsp, 72
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.def	_Z8count_upP18_Z8count_upv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upP18_Z8count_upv.Frame.destroy
_Z8count_upP18_Z8count_upv.Frame.destroy:
.LFB347:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	movzx	eax, WORD PTR 18[rax]
	or	eax, 1
	mov	edx, eax
	mov	rax, QWORD PTR 16[rbp]
	mov	WORD PTR 18[rax], dx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_Z8count_upP18_Z8count_upv.Frame.actor
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB348:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	lea	rbp, 48[rsp]
	.seh_setframe	rbp, 48
	.seh_endprologue
	call	__main
	lea	rax, -16[rbp]
	mov	edx, 5
	mov	rcx, rax
.LEHB6:
	call	_Z5rangei
.LEHE6:
	mov	DWORD PTR -4[rbp], 0
	jmp	.L118
.L119:
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNK9generator5valueEv
	add	DWORD PTR -4[rbp], eax
.L118:
	lea	rax, -16[rbp]
	mov	rcx, rax
.LEHB7:
	call	_ZN9generator4nextEv
.LEHE7:
	test	al, al
	jne	.L119
	mov	ebx, DWORD PTR -4[rbp]
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN9generatorD1Ev
	mov	eax, ebx
	jmp	.L123
.L122:
	mov	rbx, rax
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN9generatorD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB8:
	call	_Unwind_Resume
.LEHE8:
.L123:
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA348:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE348-.LLSDACSB348
.LLSDACSB348:
	.uleb128 .LEHB6-.LFB348
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB7-.LFB348
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L122-.LFB348
	.uleb128 0
	.uleb128 .LEHB8-.LFB348
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
.LLSDACSE348:
	.text
	.seh_endproc
	.section	.text$_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_
	.def	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_
_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_:
.LFB352:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR -8[rbp], 0
	mov	rax, QWORD PTR 16[rbp]
	sub	rax, 16
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvbEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvbEv
	.def	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvbEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvbEv
_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvbEv:
.LFB353:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	setne	al
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7destroyEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7destroyEv
	.def	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7destroyEv
_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7destroyEv:
.LFB354:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR 8[rax]
	mov	rcx, rax
	call	rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_promiseERS2_,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_promiseERS2_
	.def	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_promiseERS2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_promiseERS2_
_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_promiseERS2_:
.LFB360:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR -8[rbp], 0
	mov	rax, QWORD PTR 16[rbp]
	sub	rax, 16
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvbEv:
.LFB361:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	setne	al
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7destroyEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7destroyEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7destroyEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7destroyEv:
.LFB362:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR 8[rax]
	mov	rcx, rax
	call	rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE4doneEv:
.LFB363:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	sete	al
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE6resumeEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE6resumeEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE6resumeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE6resumeEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE6resumeEv:
.LFB364:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rcx, rax
	call	rdx
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7promiseEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7promiseEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7promiseEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7promiseEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7promiseEv:
.LFB365:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	add	rax, 16
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv:
.LFB366:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7addressEv
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv
	.def	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv
_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv:
.LFB367:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR -8[rbp], 0
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	.def	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv:
.LFB368:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7addressEv
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv
	.def	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv
_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv:
.LFB369:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR -8[rbp], 0
	mov	rax, QWORD PTR 16[rbp]
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7addressEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7addressEv
	.def	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7addressEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7addressEv
_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEE7addressEv:
.LFB370:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7addressEv,"x"
	.linkonce discard
	.align 2
	.globl	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7addressEv
	.def	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7addressEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7addressEv
_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEE7addressEv:
.LFB371:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rax, QWORD PTR [rax]
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
