	.file	"_ch113_co.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.def	_Z5rangeP15_Z5rangei.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangeP15_Z5rangei.Frame.actor
_Z5rangeP15_Z5rangei.Frame.actor:
.LFB344:
	.seh_endprologue
	movzx	eax, WORD PTR 24[rcx]
	test	al, 1
	je	.L2
	cmp	ax, 7
	ja	.L19
.L4:
.L12:
.L13:
.L14:
	sub	WORD PTR 26[rcx], 1
	jne	.L1
	cmp	BYTE PTR 28[rcx], 0
	jne	.L20
.L9:
.L1:
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	cmp	ax, 4
	je	.L5
	ja	.L6
	test	ax, ax
	je	.L7
.L8:
	xor	eax, eax
	mov	BYTE PTR 29[rcx], 1
	mov	DWORD PTR 32[rcx], eax
	cmp	DWORD PTR 20[rcx], eax
	jle	.L21
.L11:
	mov	edx, 4
	mov	DWORD PTR 16[rcx], eax
	mov	WORD PTR 24[rcx], dx
	ret
	.p2align 4,,10
	.p2align 3
.L20:
	mov	edx, 40
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L5:
	mov	eax, DWORD PTR 32[rcx]
	add	eax, 1
	mov	DWORD PTR 32[rcx], eax
	cmp	DWORD PTR 20[rcx], eax
	jg	.L11
.L21:
	mov	eax, 6
	mov	QWORD PTR [rcx], 0
	mov	WORD PTR 24[rcx], ax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	add	WORD PTR 26[rcx], 1
	mov	r8d, 2
	mov	BYTE PTR 29[rcx], 0
	mov	WORD PTR 24[rcx], r8w
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	cmp	ax, 6
	je	.L14
	jmp	.L3
.L19:
	jmp	.L3
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z5rangeP15_Z5rangei.Frame.actor.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangeP15_Z5rangei.Frame.actor.cold
	.seh_endprologue
_Z5rangeP15_Z5rangei.Frame.actor.cold:
.L3:
	ud2
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.def	_Z5rangeP15_Z5rangei.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangeP15_Z5rangei.Frame.destroy
_Z5rangeP15_Z5rangei.Frame.destroy:
.LFB345:
	.seh_endprologue
	or	WORD PTR 24[rcx], 1
	jmp	_Z5rangeP15_Z5rangei.Frame.actor
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.def	_Z8count_upP18_Z8count_upv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upP18_Z8count_upv.Frame.actor
_Z8count_upP18_Z8count_upv.Frame.actor:
.LFB347:
	.seh_endprologue
	movzx	eax, WORD PTR 18[rcx]
	test	al, 1
	je	.L24
	cmp	ax, 7
	ja	.L39
.L26:
.L33:
.L34:
.L35:
	sub	WORD PTR 20[rcx], 1
	jne	.L23
	cmp	BYTE PTR 22[rcx], 0
	jne	.L40
.L31:
.L23:
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	cmp	ax, 4
	je	.L27
	ja	.L28
	test	ax, ax
	je	.L29
.L30:
	mov	BYTE PTR 23[rcx], 1
	mov	DWORD PTR 28[rcx], 0
.L32:
	mov	edx, 4
	mov	WORD PTR 18[rcx], dx
	ret
	.p2align 4,,10
	.p2align 3
.L40:
	mov	edx, 40
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L27:
	mov	eax, DWORD PTR 28[rcx]
	add	eax, 1
	mov	DWORD PTR 28[rcx], eax
	cmp	eax, 2
	jle	.L32
	mov	eax, 6
	mov	QWORD PTR [rcx], 0
	mov	WORD PTR 18[rcx], ax
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	add	WORD PTR 20[rcx], 1
	mov	r8d, 2
	mov	BYTE PTR 23[rcx], 0
	mov	WORD PTR 18[rcx], r8w
	ret
	.p2align 4,,10
	.p2align 3
.L28:
	cmp	ax, 6
	je	.L35
	jmp	.L25
.L39:
	jmp	.L25
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z8count_upP18_Z8count_upv.Frame.actor.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upP18_Z8count_upv.Frame.actor.cold
	.seh_endprologue
_Z8count_upP18_Z8count_upv.Frame.actor.cold:
.L25:
	ud2
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.p2align 4
	.def	_Z8count_upP18_Z8count_upv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upP18_Z8count_upv.Frame.destroy
_Z8count_upP18_Z8count_upv.Frame.destroy:
.LFB348:
	.seh_endprologue
	or	WORD PTR 18[rcx], 1
	jmp	_Z8count_upP18_Z8count_upv.Frame.actor
	.seh_endproc
	.p2align 4
	.globl	_Z5rangei
	.def	_Z5rangei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5rangei
_Z5rangei:
.LFB343:
.L43:
.L44:
.L45:
.L46:
.L47:
.L48:
.L49:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rbx, rcx
	movd	xmm1, edx
	mov	ecx, 40
	pshufd	xmm6, xmm1, 0xe0
	call	_Znwy
	lea	rdx, _Z5rangeP15_Z5rangei.Frame.destroy[rip]
	movq	xmm0, QWORD PTR .LC4[rip]
	movq	xmm2, rdx
	mov	edx, 1
	mov	QWORD PTR [rbx], rax
	punpcklqdq	xmm0, xmm2
	mov	WORD PTR 28[rax], dx
	mov	DWORD PTR 24[rax], 65538
	movups	XMMWORD PTR [rax], xmm0
	movq	QWORD PTR 16[rax], xmm6
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	rax, rbx
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8count_upv
	.def	_Z8count_upv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8count_upv
_Z8count_upv:
.LFB346:
.L51:
.L52:
.L53:
.L54:
.L55:
.L56:
.L57:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 40
	call	_Znwy
	lea	rdx, _Z8count_upP18_Z8count_upv.Frame.destroy[rip]
	movq	xmm0, QWORD PTR .LC5[rip]
	movq	xmm1, rdx
	mov	edx, 1
	mov	QWORD PTR [rbx], rax
	punpcklqdq	xmm0, xmm1
	mov	WORD PTR 22[rax], dx
	mov	DWORD PTR 18[rax], 65538
	movups	XMMWORD PTR [rax], xmm0
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB349:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rcx, 40[rsp]
	mov	edx, 5
.LEHB0:
	call	_Z5rangei
.LEHE0:
	mov	rbx, QWORD PTR 40[rsp]
	test	rbx, rbx
	je	.L64
	mov	rax, QWORD PTR [rbx]
	xor	esi, esi
	test	rax, rax
	jne	.L61
.L60:
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
.L58:
	mov	eax, esi
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L62:
	add	esi, DWORD PTR 16[rbx]
.L61:
	mov	rcx, rbx
.LEHB1:
	call	rax
.LEHE1:
	mov	rax, QWORD PTR [rbx]
	test	rax, rax
	jne	.L62
	jmp	.L60
.L64:
	xor	esi, esi
	jmp	.L58
.L66:
	mov	rsi, rax
	jmp	.L63
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA349:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE349-.LLSDACSB349
.LLSDACSB349:
	.uleb128 .LEHB0-.LFB349
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB349
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L66-.LFB349
	.uleb128 0
.LLSDACSE349:
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
.L63:
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC349:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC349-.LLSDACSBC349
.LLSDACSBC349:
	.uleb128 .LEHB2-.LCOLDB6
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC349:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
	.section .rdata,"dr"
	.align 8
.LC4:
	.quad	_Z5rangeP15_Z5rangei.Frame.actor
	.align 8
.LC5:
	.quad	_Z8count_upP18_Z8count_upv.Frame.actor
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
