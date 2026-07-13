	.file	"_ch113_co.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt7__n486116coroutine_handleIvE12from_addressEPv,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv
	.def	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIvE12from_addressEPv
_ZNSt7__n486116coroutine_handleIvE12from_addressEPv:
.LFB114:
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
.LFB150:
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
.LFB151:
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
.LFB152:
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
.LFB293:
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
.LFB294:
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
.LFB295:
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
.LFB296:
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
.LFB300:
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
.LFB303:
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
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA303:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE303-.LLSDACSB303
.LLSDACSB303:
.LLSDACSE303:
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
.LFB305:
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
.LFB306:
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
.LFB307:
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
.LFB308:
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
.LFB309:
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
.LFB313:
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
.LFB316:
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
.LLSDA316:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE316-.LLSDACSB316
.LLSDACSB316:
.LLSDACSE316:
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
.LFB317:
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
.LFB318:
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
.LFB319:
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
	mov	QWORD PTR -8[rbp], 0
	mov	BYTE PTR -9[rbp], 0
	mov	BYTE PTR -10[rbp], 0
	mov	eax, 56
	mov	rcx, rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	BYTE PTR 38[rax], 1
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z5rangePZ5rangeiE15_Z5rangei.Frame.actor[rip]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy[rip]
	mov	QWORD PTR 8[rax], rdx
	mov	edx, DWORD PTR 40[rbp]
	mov	rax, QWORD PTR -8[rbp]
	mov	DWORD PTR 32[rax], edx
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, DWORD PTR 32[rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	DWORD PTR 16[rax], edx
	mov	BYTE PTR -9[rbp], 1
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, 16[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN9generator12promise_type17get_return_objectEv
	mov	BYTE PTR -10[rbp], 1
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 36[rax], 0
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
.LEHB1:
	call	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor
.LEHE1:
	jmp	.L47
.L45:
	mov	rcx, rax
	call	__cxa_begin_catch
	cmp	BYTE PTR -10[rbp], 0
	je	.L42
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN9generatorD1Ev
.L42:
	cmp	BYTE PTR -9[rbp], 0
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZdlPv
.LEHB2:
	call	__cxa_rethrow
.LEHE2:
.L46:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rax, rbx
	mov	rcx, rax
.LEHB3:
	call	_Unwind_Resume
.LEHE3:
.L47:
	mov	rax, QWORD PTR 32[rbp]
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA319:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT319-.LLSDATTD319
.LLSDATTD319:
	.byte	0x1
	.uleb128 .LLSDACSE319-.LLSDACSB319
.LLSDACSB319:
	.uleb128 .LEHB0-.LFB319
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB319
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L45-.LFB319
	.uleb128 0x1
	.uleb128 .LEHB2-.LFB319
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L46-.LFB319
	.uleb128 0
	.uleb128 .LEHB3-.LFB319
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE319:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT319:
	.text
	.seh_endproc
	.def	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor
_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor:
.LFB320:
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
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 36[rax]
	and	eax, 1
	test	ax, ax
	je	.L49
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 36[rax]
	movzx	eax, ax
	cmp	eax, 7
	je	.L58
	cmp	eax, 7
	jg	.L51
	cmp	eax, 5
	je	.L57
	cmp	eax, 5
	jg	.L51
	cmp	eax, 1
	je	.L74
	cmp	eax, 3
	je	.L56
.L51:
	ud2
.L49:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 36[rax]
	movzx	eax, ax
	cmp	eax, 6
	je	.L67
	cmp	eax, 6
	jg	.L60
	cmp	eax, 4
	je	.L66
	cmp	eax, 4
	jg	.L60
	test	eax, eax
	je	.L62
	cmp	eax, 2
	je	.L65
	jmp	.L60
.L62:
	mov	rbx, QWORD PTR 32[rbp]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN9generator12promise_typeEE12from_addressEPv
	mov	QWORD PTR 24[rbx], rax
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 39[rax], 0
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN9generator12promise_type15initial_suspendEv
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 40
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	jne	.L64
	jmp	.L65
.L60:
	ud2
.L64:
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 36[rax], 2
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 40[rax]
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L68
.L56:
	jmp	.L55
.L65:
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 39[rax], 1
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 40
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 44[rax], 0
	jmp	.L69
.L70:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rdx, QWORD PTR 32[rbp]
	mov	edx, DWORD PTR 44[rdx]
	mov	rcx, rax
	call	_ZN9generator12promise_type11yield_valueEi
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 48
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L66
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 36[rax], 4
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 48[rax]
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L68
.L57:
	jmp	.L55
.L66:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 48
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 44[rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 44[rax], edx
.L69:
	mov	rax, QWORD PTR 32[rbp]
	mov	edx, DWORD PTR 44[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 32[rax]
	cmp	edx, eax
	jl	.L70
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
	add	rax, 49
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L67
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 36[rax], 6
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 49[rax]
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN9generator12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L68
.L58:
	jmp	.L55
.L67:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 49
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	jmp	.L55
.L74:
	nop
.L55:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, BYTE PTR 38[rax]
	movzx	eax, al
	test	eax, eax
	je	.L75
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZdlPv
	jmp	.L75
.L68:
.L75:
	nop
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.def	_Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy
_Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy:
.LFB321:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	movzx	eax, WORD PTR 36[rax]
	or	eax, 1
	mov	edx, eax
	mov	rax, QWORD PTR 16[rbp]
	mov	WORD PTR 36[rax], dx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z8count_upv
	.def	_Z8count_upv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8count_upv
_Z8count_upv:
.LFB322:
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
	mov	QWORD PTR -8[rbp], 0
	mov	BYTE PTR -9[rbp], 0
	mov	BYTE PTR -10[rbp], 0
	mov	eax, 48
	mov	rcx, rax
.LEHB4:
	call	_Znwy
.LEHE4:
	mov	QWORD PTR -8[rbp], rax
	mov	rax, QWORD PTR -8[rbp]
	mov	BYTE PTR 34[rax], 1
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor[rip]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, _Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy[rip]
	mov	QWORD PTR 8[rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, 16[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN4task12promise_type17get_return_objectEv
	mov	BYTE PTR -10[rbp], 1
	mov	rax, QWORD PTR -8[rbp]
	mov	WORD PTR 32[rax], 0
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
.LEHB5:
	call	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor
.LEHE5:
	jmp	.L85
.L83:
	mov	rcx, rax
	call	__cxa_begin_catch
	cmp	BYTE PTR -10[rbp], 0
	je	.L81
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZN4taskD1Ev
.L81:
	mov	rax, QWORD PTR -8[rbp]
	mov	rcx, rax
	call	_ZdlPv
.LEHB6:
	call	__cxa_rethrow
.LEHE6:
.L84:
	mov	rbx, rax
	call	__cxa_end_catch
	mov	rax, rbx
	mov	rcx, rax
.LEHB7:
	call	_Unwind_Resume
.LEHE7:
.L85:
	mov	rax, QWORD PTR 32[rbp]
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA322:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT322-.LLSDATTD322
.LLSDATTD322:
	.byte	0x1
	.uleb128 .LLSDACSE322-.LLSDACSB322
.LLSDACSB322:
	.uleb128 .LEHB4-.LFB322
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB5-.LFB322
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L83-.LFB322
	.uleb128 0x1
	.uleb128 .LEHB6-.LFB322
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L84-.LFB322
	.uleb128 0
	.uleb128 .LEHB7-.LFB322
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSE322:
	.byte	0x1
	.byte	0
	.align 4
	.long	0

.LLSDATT322:
	.text
	.seh_endproc
	.def	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor
_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor:
.LFB323:
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
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 32[rax]
	and	eax, 1
	test	ax, ax
	je	.L87
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 32[rax]
	movzx	eax, ax
	cmp	eax, 7
	je	.L96
	cmp	eax, 7
	jg	.L89
	cmp	eax, 5
	je	.L95
	cmp	eax, 5
	jg	.L89
	cmp	eax, 1
	je	.L112
	cmp	eax, 3
	je	.L94
.L89:
	ud2
.L87:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, WORD PTR 32[rax]
	movzx	eax, ax
	cmp	eax, 6
	je	.L105
	cmp	eax, 6
	jg	.L98
	cmp	eax, 4
	je	.L104
	cmp	eax, 4
	jg	.L98
	test	eax, eax
	je	.L100
	cmp	eax, 2
	je	.L103
	jmp	.L98
.L100:
	mov	rbx, QWORD PTR 32[rbp]
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_addressEPv
	mov	QWORD PTR 24[rbx], rax
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 35[rax], 0
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 16
	mov	rcx, rax
	call	_ZN4task12promise_type15initial_suspendEv
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 36
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	jne	.L102
	jmp	.L103
.L98:
	ud2
.L102:
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 32[rax], 2
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 36[rax]
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L106
.L94:
	jmp	.L93
.L103:
	mov	rax, QWORD PTR 32[rbp]
	mov	BYTE PTR 35[rax], 1
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 36
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 40[rax], 0
	jmp	.L107
.L108:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 44
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L104
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 32[rax], 4
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 44[rax]
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L106
.L95:
	jmp	.L93
.L104:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 44
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 40[rax]
	lea	edx, 1[rax]
	mov	rax, QWORD PTR 32[rbp]
	mov	DWORD PTR 40[rax], edx
.L107:
	mov	rax, QWORD PTR 32[rbp]
	mov	eax, DWORD PTR 40[rax]
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
	add	rax, 45
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always11await_readyEv
	xor	eax, 1
	test	al, al
	je	.L105
	mov	rax, QWORD PTR 32[rbp]
	mov	WORD PTR 32[rax], 6
	mov	rax, QWORD PTR 32[rbp]
	lea	rbx, 45[rax]
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 24
	mov	rcx, rax
	call	_ZNKSt7__n486116coroutine_handleIN4task12promise_typeEEcvNS0_IvEEEv
	mov	rdx, rax
	mov	rcx, rbx
	call	_ZNKSt7__n486114suspend_always13await_suspendENS_16coroutine_handleIvEE
	jmp	.L106
.L96:
	jmp	.L93
.L105:
	mov	rax, QWORD PTR 32[rbp]
	add	rax, 45
	mov	rcx, rax
	call	_ZNKSt7__n486114suspend_always12await_resumeEv
	jmp	.L93
.L112:
	nop
.L93:
	mov	rax, QWORD PTR 32[rbp]
	movzx	eax, BYTE PTR 34[rax]
	movzx	eax, al
	test	eax, eax
	je	.L113
	mov	rax, QWORD PTR 32[rbp]
	mov	rcx, rax
	call	_ZdlPv
	jmp	.L113
.L106:
.L113:
	nop
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.def	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy
_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy:
.LFB324:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	movzx	eax, WORD PTR 32[rax]
	or	eax, 1
	mov	edx, eax
	mov	rax, QWORD PTR 16[rbp]
	mov	WORD PTR 32[rax], dx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB325:
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
.LEHB8:
	call	_Z5rangei
.LEHE8:
	mov	DWORD PTR -4[rbp], 0
	jmp	.L117
.L118:
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZNK9generator5valueEv
	add	DWORD PTR -4[rbp], eax
.L117:
	lea	rax, -16[rbp]
	mov	rcx, rax
.LEHB9:
	call	_ZN9generator4nextEv
.LEHE9:
	test	al, al
	jne	.L118
	mov	ebx, DWORD PTR -4[rbp]
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN9generatorD1Ev
	mov	eax, ebx
	jmp	.L122
.L121:
	mov	rbx, rax
	lea	rax, -16[rbp]
	mov	rcx, rax
	call	_ZN9generatorD1Ev
	mov	rax, rbx
	mov	rcx, rax
.LEHB10:
	call	_Unwind_Resume
.LEHE10:
.L122:
	add	rsp, 56
	pop	rbx
	pop	rbp
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA325:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE325-.LLSDACSB325
.LLSDACSB325:
	.uleb128 .LEHB8-.LFB325
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB9-.LFB325
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L121-.LFB325
	.uleb128 0
	.uleb128 .LEHB10-.LFB325
	.uleb128 .LEHE10-.LEHB10
	.uleb128 0
	.uleb128 0
.LLSDACSE325:
	.text
	.seh_endproc
	.section	.text$_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_,"x"
	.linkonce discard
	.globl	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_
	.def	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_
_ZNSt7__n486116coroutine_handleIN4task12promise_typeEE12from_promiseERS2_:
.LFB329:
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
.LFB330:
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
.LFB331:
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
.LFB337:
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
.LFB338:
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
.LFB340:
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
.LFB342:
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
.LFB343:
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
.LFB344:
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
.LFB345:
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
.LFB346:
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
.LFB347:
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
.LFB348:
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
