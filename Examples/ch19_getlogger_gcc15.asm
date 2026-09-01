	.file	"ch19_getlogger_gcc15.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	__tcf_ZZ9getLoggervE8instance;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_ZZ9getLoggervE8instance
__tcf_ZZ9getLoggervE8instance:
.LFB2098:
	.seh_endprologue
	mov	rcx, QWORD PTR _ZZ9getLoggervE8instance[rip]
	lea	rax, _ZZ9getLoggervE8instance[rip+16]
	cmp	rcx, rax
	je	.L1
	mov	rax, QWORD PTR _ZZ9getLoggervE8instance[rip+16]
	lea	rdx, 1[rax]
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9getLoggerv
	.def	_Z9getLoggerv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9getLoggerv
_Z9getLoggerv:
.LFB2069:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movzx	eax, BYTE PTR _ZGVZ9getLoggervE8instance[rip]
	test	al, al
	je	.L11
.L6:
	lea	rax, _ZZ9getLoggervE8instance[rip]
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	lea	rcx, _ZGVZ9getLoggervE8instance[rip]
	call	__cxa_guard_acquire
	test	eax, eax
	je	.L6
	lea	rcx, __tcf_ZZ9getLoggervE8instance[rip]
	call	atexit
	lea	rcx, _ZGVZ9getLoggervE8instance[rip]
	call	__cxa_guard_release
	lea	rax, _ZZ9getLoggervE8instance[rip]
	add	rsp, 40
	ret
	.seh_endproc
.lcomm _ZGVZ9getLoggervE8instance,8,8
	.data
	.align 32
_ZZ9getLoggervE8instance:
	.quad	_ZZ9getLoggervE8instance+16
	.quad	6
	.byte	108
	.byte	111
	.byte	103
	.byte	103
	.byte	101
	.byte	114
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.byte	0
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_acquire;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
	.def	__cxa_guard_release;	.scl	2;	.type	32;	.endef
