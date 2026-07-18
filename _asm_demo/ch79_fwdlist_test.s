	.file	"ch79_fwdlist_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt12forward_listIiSaIiEE10push_frontEOi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12forward_listIiSaIiEE10push_frontEOi
	.def	_ZNSt12forward_listIiSaIiEE10push_frontEOi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12forward_listIiSaIiEE10push_frontEOi
_ZNSt12forward_listIiSaIiEE10push_frontEOi:
.LFB1478:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, rcx
	mov	rsi, rdx
	mov	ecx, 16
	call	_Znwy
	mov	edx, DWORD PTR [rsi]
	mov	DWORD PTR 8[rax], edx
	mov	rdx, QWORD PTR [rbx]
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR [rax], rdx
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.section	.text.startup,"x"
.LHOTB0:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1448:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	lea	rdx, 36[rsp]
	lea	rcx, 40[rsp]
	mov	DWORD PTR 36[rsp], 1
	mov	QWORD PTR 40[rsp], 0
.LEHB0:
	call	_ZNSt12forward_listIiSaIiEE10push_frontEOi
.LEHE0:
	lea	rdx, 36[rsp]
	lea	rcx, 40[rsp]
	mov	DWORD PTR 36[rsp], 2
.LEHB1:
	call	_ZNSt12forward_listIiSaIiEE10push_frontEOi
.LEHE1:
	mov	ecx, 16
	mov	rbx, QWORD PTR 40[rsp]
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	rcx, rax
	test	rbx, rbx
	je	.L14
	mov	rdx, rbx
	mov	eax, 42
	.p2align 4
	.p2align 4
	.p2align 3
.L8:
	mov	r8d, DWORD PTR 8[rdx]
	mov	rdx, QWORD PTR [rdx]
	add	eax, r8d
	test	rdx, rdx
	jne	.L8
.L7:
	mov	DWORD PTR 36[rsp], eax
	mov	eax, DWORD PTR 36[rsp]
	jmp	.L10
	.p2align 4,,10
	.p2align 3
.L21:
	mov	rcx, rbx
	mov	rbx, QWORD PTR [rbx]
.L10:
	mov	edx, 16
	call	_ZdlPvy
	test	rbx, rbx
	jne	.L21
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L14:
	mov	eax, 42
	jmp	.L7
.L16:
	mov	rsi, rax
	jmp	.L11
.L15:
	mov	rsi, rax
	jmp	.L12
.L17:
	mov	rsi, rax
	jmp	.L11
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1448:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1448-.LLSDACSB1448
.LLSDACSB1448:
	.uleb128 .LEHB0-.LFB1448
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L16-.LFB1448
	.uleb128 0
	.uleb128 .LEHB1-.LFB1448
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L17-.LFB1448
	.uleb128 0
	.uleb128 .LEHB2-.LFB1448
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L15-.LFB1448
	.uleb128 0
.LLSDACSE1448:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_endprologue
main.cold:
.L11:
	mov	rbx, QWORD PTR 40[rsp]
.L12:
	test	rbx, rbx
	je	.L22
	mov	rax, QWORD PTR [rbx]
	mov	rcx, rbx
	mov	edx, 16
	mov	rbx, rax
	call	_ZdlPvy
	jmp	.L12
.L22:
	mov	rcx, rsi
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1448:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1448-.LLSDACSBC1448
.LLSDACSBC1448:
	.uleb128 .LEHB3-.LCOLDB0
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC1448:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.section	.text.startup,"x"
.LHOTE0:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
