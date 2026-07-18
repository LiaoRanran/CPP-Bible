	.file	"ch08_generator_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv
	.def	_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv
_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv:
.LFB3829:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZZNSt5__gen14_Promise_allocIvEnwEyENUlPvyE_4_FUNES2_y,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZZNSt5__gen14_Promise_allocIvEnwEyENUlPvyE_4_FUNES2_y
	.def	_ZZNSt5__gen14_Promise_allocIvEnwEyENUlPvyE_4_FUNES2_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZZNSt5__gen14_Promise_allocIvEnwEyENUlPvyE_4_FUNES2_y
_ZZNSt5__gen14_Promise_allocIvEnwEyENUlPvyE_4_FUNES2_y:
.LFB3885:
	.seh_endprologue
	add	rdx, 16
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.def	_Z4iotaP14_Z4iotai.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z4iotaP14_Z4iotai.Frame.actor
_Z4iotaP14_Z4iotai.Frame.actor:
.LFB3928:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	movzx	edx, WORD PTR 52[rcx]
	mov	rax, rcx
	test	dl, 1
	je	.L5
	cmp	dx, 7
	ja	.L37
.L7:
.L23:
.L24:
.L25:
	sub	WORD PTR 54[rax], 1
	jne	.L4
	cmp	QWORD PTR 40[rax], 0
	je	.L27
	lea	rcx, 40[rax]
	mov	QWORD PTR 40[rsp], rax
	call	_ZNSt15__exception_ptr13exception_ptr10_M_releaseEv
	mov	rax, QWORD PTR 40[rsp]
.L27:
	cmp	BYTE PTR 56[rax], 0
	jne	.L38
.L4:
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	cmp	dx, 4
	je	.L8
	ja	.L9
	test	dx, dx
	je	.L10
.L11:
	mov	BYTE PTR 57[rcx], 1
	xor	edx, edx
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L38:
.L12:
	lea	r8, 95[rax]
	mov	edx, 88
	mov	rcx, rax
	shr	r8, 3
	call	[QWORD PTR 0[0+r8*8]]
	nop
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	mov	ecx, DWORD PTR 60[rcx]
	lea	edx, 1[rcx]
.L13:
	mov	DWORD PTR 60[rax], edx
	movzx	ecx, BYTE PTR 32[rax]
	cmp	DWORD PTR 48[rax], edx
	jle	.L19
	mov	DWORD PTR 68[rax], 0
	mov	DWORD PTR 64[rax], edx
	test	cl, cl
	jne	.L14
	lea	rdx, 24[rax]
.L15:
	mov	ecx, 4
	mov	QWORD PTR 72[rax], rdx
	add	rax, 64
	mov	WORD PTR -12[rax], cx
	mov	QWORD PTR [rdx], rax
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	add	WORD PTR 54[rcx], 1
	mov	r8d, 2
	mov	BYTE PTR 57[rcx], 0
	mov	WORD PTR 52[rcx], r8w
	add	rsp, 56
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	cmp	dx, 6
	je	.L25
	jmp	.L36
	.p2align 4,,10
	.p2align 3
.L19:
	mov	edx, 6
	mov	QWORD PTR [rax], 0
	mov	WORD PTR 52[rax], dx
	cmp	cl, 1
	jne	.L30
	lea	r8, 16[rax]
.L21:
	mov	rdx, QWORD PTR [r8]
	movzx	ecx, BYTE PTR 32[rdx]
	lea	r8, 16[rdx]
	cmp	cl, 1
	je	.L21
	test	cl, cl
	jne	.L22
	mov	rcx, QWORD PTR 24[rax]
	mov	QWORD PTR 16[rdx], rcx
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L30:
	lea	rcx, _ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE5_S_frE[rip]
.L20:
	mov	rax, QWORD PTR [rcx]
	add	rsp, 56
.LEHB0:
	rex.W jmp	rax
.LEHE0:
	.p2align 4,,10
	.p2align 3
.L14:
	cmp	cl, 1
	jne	.L16
	mov	rcx, QWORD PTR 16[rax]
	cmp	BYTE PTR 32[rcx], 0
	lea	rdx, 16[rcx]
	mov	ecx, 0
	cmovne	rdx, rcx
	add	rdx, 8
	jmp	.L15
.L37:
	jmp	.L36
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3928:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3928-.LLSDACSB3928
.LLSDACSB3928:
	.uleb128 .LEHB0-.LFB3928
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
.LLSDACSE3928:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z4iotaP14_Z4iotai.Frame.actor.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z4iotaP14_Z4iotai.Frame.actor.cold
	.seh_stackalloc	56
	.seh_endprologue
_Z4iotaP14_Z4iotai.Frame.actor.cold:
.L16:
	mov	rax, QWORD PTR ds:0
.L36:
	ud2
.L22:
	mov	rax, QWORD PTR 24[rax]
	mov	QWORD PTR ds:0, rax
	ud2
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3928:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3928-.LLSDACSBC3928
.LLSDACSBC3928:
.LLSDACSEC3928:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.def	_Z4iotaP14_Z4iotai.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z4iotaP14_Z4iotai.Frame.destroy
_Z4iotaP14_Z4iotai.Frame.destroy:
.LFB3929:
	.seh_endprologue
	or	WORD PTR 52[rcx], 1
	jmp	_Z4iotaP14_Z4iotai.Frame.actor
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4
	.globl	_Z4iotai
	.def	_Z4iotai;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4iotai
_Z4iotai:
.LFB3907:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, rcx
	mov	ecx, 104
	mov	ebp, edx
.LEHB1:
	call	_Znwy
.LEHE1:
	movq	xmm0, QWORD PTR .LC3[rip]
	lea	rdi, 95[rax]
	mov	rbx, rax
	lea	rax, _ZZNSt5__gen14_Promise_allocIvEnwEyENUlPvyE_4_FUNES2_y[rip]
	shr	rdi, 3
	mov	rcx, rbx
	mov	QWORD PTR 0[0+rdi*8], rax
	lea	rax, _Z4iotaP14_Z4iotai.Frame.destroy[rip]
	movq	xmm1, rax
	mov	BYTE PTR 56[rbx], 1
	punpcklqdq	xmm0, xmm1
	mov	DWORD PTR 48[rbx], ebp
	mov	BYTE PTR 32[rbx], 0
	mov	QWORD PTR 40[rbx], 0
	mov	DWORD PTR 52[rbx], 65536
	mov	QWORD PTR [rsi], rbx
	mov	BYTE PTR 8[rsi], 0
	movups	XMMWORD PTR [rbx], xmm0
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 16[rbx], xmm0
.LEHB2:
	call	_Z4iotaP14_Z4iotai.Frame.actor
.LEHE2:
	sub	WORD PTR 54[rbx], 1
	jne	.L40
	cmp	QWORD PTR 40[rbx], 0
	je	.L44
	lea	rcx, 40[rbx]
	call	_ZNSt15__exception_ptr13exception_ptr10_M_releaseEv
	cmp	WORD PTR 54[rbx], 0
	je	.L44
.L40:
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L44:
	mov	edx, 88
	mov	rcx, rbx
	call	[QWORD PTR 0[0+rdi*8]]
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L51:
	mov	rbp, rax
	jmp	.L46
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3907:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3907-.LLSDACSB3907
.LLSDACSB3907:
	.uleb128 .LEHB1-.LFB3907
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB2-.LFB3907
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L51-.LFB3907
	.uleb128 0
.LLSDACSE3907:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z4iotai.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z4iotai.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_savereg	rdi, 56
	.seh_savereg	rbp, 64
	.seh_endprologue
_Z4iotai.cold:
.L46:
	mov	rax, QWORD PTR [rsi]
	test	rax, rax
	je	.L47
	mov	rcx, rax
	call	[QWORD PTR 8[rax]]
.L47:
	sub	WORD PTR 54[rbx], 1
	jne	.L48
	cmp	QWORD PTR 40[rbx], 0
	je	.L48
	lea	rcx, 40[rbx]
	call	_ZNSt15__exception_ptr13exception_ptr10_M_releaseEv
.L48:
	cmp	WORD PTR 54[rbx], 0
	jne	.L50
	mov	edx, 88
	mov	rcx, rbx
	call	[QWORD PTR 0[0+rdi*8]]
.L50:
	mov	rcx, rbp
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3907:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3907-.LLSDACSBC3907
.LLSDACSBC3907:
	.uleb128 .LEHB3-.LCOLDB4
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC3907:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.text
.LHOTE4:
	.section .rdata,"dr"
.LC5:
	.ascii "%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3930:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	edx, 5
	lea	rcx, 32[rsp]
.LEHB4:
	call	_Z4iotai
.LEHE4:
	mov	rbx, QWORD PTR 32[rsp]
	movzx	edx, BYTE PTR 32[rbx]
	lea	rax, 16[rbx]
	cmp	dl, 1
	jne	.L56
	mov	r8, rax
.L57:
	mov	rdx, QWORD PTR [r8]
	movzx	ecx, BYTE PTR 32[rdx]
	lea	r8, 16[rdx]
	cmp	cl, 1
	je	.L57
	test	cl, cl
	jne	.L58
	mov	QWORD PTR 16[rdx], rbx
.L59:
	mov	rdx, QWORD PTR [rax]
	lea	rax, 16[rdx]
	movzx	edx, BYTE PTR 32[rdx]
	cmp	dl, 1
	je	.L59
	xor	ecx, ecx
	test	dl, dl
	jne	.L60
.L66:
	mov	rcx, rax
.L60:
	mov	rax, QWORD PTR [rcx]
	mov	rcx, rax
.LEHB5:
	call	[QWORD PTR [rax]]
	xor	esi, esi
	jmp	.L61
	.p2align 4,,10
	.p2align 3
.L63:
	cmp	BYTE PTR 32[rbx], 0
	jne	.L62
	mov	rax, QWORD PTR 24[rbx]
	add	esi, DWORD PTR [rax]
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, rax
	call	[QWORD PTR [rax]]
.LEHE5:
.L61:
	cmp	QWORD PTR [rbx], 0
	jne	.L63
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
	mov	edx, esi
	lea	rcx, .LC5[rip]
.LEHB6:
	call	__mingw_printf
.LEHE6:
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
.L56:
	test	dl, dl
	jne	.L65
	mov	QWORD PTR 16[rbx], rbx
	jmp	.L66
.L65:
	mov	QWORD PTR ds:0, rbx
	ud2
.L69:
	mov	rsi, rax
	jmp	.L64
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3930:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3930-.LLSDACSB3930
.LLSDACSB3930:
	.uleb128 .LEHB4-.LFB3930
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB5-.LFB3930
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L69-.LFB3930
	.uleb128 0
	.uleb128 .LEHB6-.LFB3930
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSE3930:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_endprologue
main.cold:
.L58:
	mov	QWORD PTR ds:0, rbx
	ud2
.L62:
	mov	rax, QWORD PTR ds:8
	ud2
.L64:
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
	mov	rcx, rsi
.LEHB7:
	call	_Unwind_Resume
	nop
.LEHE7:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC3930:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC3930-.LLSDACSBC3930
.LLSDACSBC3930:
	.uleb128 .LEHB7-.LCOLDB6
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSEC3930:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
	.globl	_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE5_S_frE
	.section	.data$_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE5_S_frE,"w"
	.linkonce same_size
	.align 16
_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE5_S_frE:
	.quad	_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv
	.quad	_ZNSt7__n486116coroutine_handleINS_22noop_coroutine_promiseEE7__frame22__dummy_resume_destroyEv
	.space 8
	.section .rdata,"dr"
	.align 8
.LC3:
	.quad	_Z4iotaP14_Z4iotai.Frame.actor
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt15__exception_ptr13exception_ptr10_M_releaseEv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
