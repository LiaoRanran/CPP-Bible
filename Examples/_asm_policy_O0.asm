	.file	"_asm_policy.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN14SingleThreaded4lockEv,"x"
	.linkonce discard
	.globl	_ZN14SingleThreaded4lockEv
	.def	_ZN14SingleThreaded4lockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14SingleThreaded4lockEv
_ZN14SingleThreaded4lockEv:
.LFB41:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN14SingleThreaded6unlockEv,"x"
	.linkonce discard
	.globl	_ZN14SingleThreaded6unlockEv
	.def	_ZN14SingleThreaded6unlockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN14SingleThreaded6unlockEv
_ZN14SingleThreaded6unlockEv:
.LFB42:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN13MultiThreaded4lockEv,"x"
	.linkonce discard
	.globl	_ZN13MultiThreaded4lockEv
	.def	_ZN13MultiThreaded4lockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13MultiThreaded4lockEv
_ZN13MultiThreaded4lockEv:
.LFB43:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN13MultiThreaded6unlockEv,"x"
	.linkonce discard
	.globl	_ZN13MultiThreaded6unlockEv
	.def	_ZN13MultiThreaded6unlockEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13MultiThreaded6unlockEv
_ZN13MultiThreaded6unlockEv:
.LFB44:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	nop
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z10use_policyv
	.def	_Z10use_policyv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_policyv
_Z10use_policyv:
.LFB49:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	call	_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv
	mov	QWORD PTR -8[rbp], rax
	call	_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv
	mov	QWORD PTR -16[rbp], rax
	cmp	QWORD PTR -8[rbp], 0
	setne	al
	movzx	edx, al
	cmp	QWORD PTR -16[rbp], 0
	setne	al
	movzx	eax, al
	add	eax, edx
	mov	DWORD PTR -20[rbp], eax
	mov	rax, QWORD PTR -8[rbp]
	test	rax, rax
	je	.L6
	mov	edx, 4
	mov	rcx, rax
	call	_ZdlPvy
.L6:
	mov	rax, QWORD PTR -16[rbp]
	mov	rcx, rax
	call	free
	mov	eax, DWORD PTR -20[rbp]
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.globl	_Z11use_virtualR5VBase
	.def	_Z11use_virtualR5VBase;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_virtualR5VBase
_Z11use_virtualR5VBase:
.LFB50:
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
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	rdx
	test	rax, rax
	setne	al
	movzx	eax, al
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv,"x"
	.linkonce discard
	.globl	_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv
	.def	_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv
_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv:
.LFB51:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	_ZN14SingleThreaded4lockEv
	call	_ZN10NewCreatorIiE6createEv
	mov	QWORD PTR -8[rbp], rax
	call	_ZN14SingleThreaded6unlockEv
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv,"x"
	.linkonce discard
	.globl	_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv
	.def	_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv
_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv:
.LFB52:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	_ZN13MultiThreaded4lockEv
	call	_ZN13MallocCreatorIiE6createEv
	mov	QWORD PTR -8[rbp], rax
	call	_ZN13MultiThreaded6unlockEv
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN10NewCreatorIiE6createEv,"x"
	.linkonce discard
	.globl	_ZN10NewCreatorIiE6createEv
	.def	_ZN10NewCreatorIiE6createEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN10NewCreatorIiE6createEv
_ZN10NewCreatorIiE6createEv:
.LFB53:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	mov	ecx, 4
	call	_Znwy
	mov	rbx, rax
	mov	DWORD PTR [rbx], 0
	mov	eax, 0
	test	al, al
	je	.L16
	mov	edx, 4
	mov	rcx, rbx
	call	_ZdlPvy
.L16:
	mov	rax, rbx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN13MallocCreatorIiE6createEv,"x"
	.linkonce discard
	.globl	_ZN13MallocCreatorIiE6createEv
	.def	_ZN13MallocCreatorIiE6createEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN13MallocCreatorIiE6createEv
_ZN13MallocCreatorIiE6createEv:
.LFB54:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 4
	call	malloc
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
