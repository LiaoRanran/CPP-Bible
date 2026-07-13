	.file	"_ch113_co.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor
_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor:
.LFB320:
	.seh_endprologue
	movzx	eax, WORD PTR 36[rcx]
	test	al, 1
	je	.L2
	cmp	ax, 7
	ja	.L3
	mov	edx, 170
	bt	rdx, rax
	jnc	.L3
.L4:
	cmp	BYTE PTR 38[rcx], 0
	jne	.L17
.L9:
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	cmp	ax, 4
	je	.L5
	ja	.L6
	test	ax, ax
	je	.L7
	xor	eax, eax
	cmp	DWORD PTR 32[rcx], eax
	mov	BYTE PTR 39[rcx], 1
	mov	DWORD PTR 44[rcx], eax
	jg	.L11
.L18:
	mov	eax, 6
	mov	QWORD PTR [rcx], 0
	mov	WORD PTR 36[rcx], ax
	ret
	.p2align 4,,10
	.p2align 3
.L17:
	jmp	_ZdlPv
	.p2align 4,,10
	.p2align 3
.L7:
	mov	r8d, 2
	mov	QWORD PTR 24[rcx], rcx
	mov	BYTE PTR 39[rcx], 0
	mov	WORD PTR 36[rcx], r8w
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	mov	eax, DWORD PTR 44[rcx]
	add	eax, 1
	cmp	DWORD PTR 32[rcx], eax
	mov	DWORD PTR 44[rcx], eax
	jle	.L18
.L11:
	mov	edx, 4
	mov	DWORD PTR 16[rcx], eax
	mov	WORD PTR 36[rcx], dx
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	cmp	ax, 6
	je	.L4
.L3:
	ud2
	.seh_endproc
	.p2align 4
	.def	_Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy
_Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy:
.LFB321:
	.seh_endprologue
	or	WORD PTR 36[rcx], 1
	jmp	_Z5rangePZ5rangeiE15_Z5rangei.Frame.actor
	.seh_endproc
	.p2align 4
	.def	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor
_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor:
.LFB323:
	.seh_endprologue
	movzx	eax, WORD PTR 32[rcx]
	test	al, 1
	je	.L21
	cmp	ax, 7
	ja	.L22
	mov	edx, 170
	bt	rdx, rax
	jnc	.L22
.L23:
	cmp	BYTE PTR 34[rcx], 0
	jne	.L34
.L28:
	ret
	.p2align 4,,10
	.p2align 3
.L21:
	cmp	ax, 4
	je	.L24
	ja	.L25
	test	ax, ax
	je	.L26
	mov	BYTE PTR 35[rcx], 1
	mov	DWORD PTR 40[rcx], 0
.L29:
	mov	edx, 4
	mov	WORD PTR 32[rcx], dx
	ret
	.p2align 4,,10
	.p2align 3
.L34:
	jmp	_ZdlPv
	.p2align 4,,10
	.p2align 3
.L26:
	mov	r8d, 2
	mov	QWORD PTR 24[rcx], rcx
	mov	BYTE PTR 35[rcx], 0
	mov	WORD PTR 32[rcx], r8w
	ret
	.p2align 4,,10
	.p2align 3
.L24:
	mov	eax, DWORD PTR 40[rcx]
	add	eax, 1
	cmp	eax, 2
	mov	DWORD PTR 40[rcx], eax
	jle	.L29
	mov	eax, 6
	mov	QWORD PTR [rcx], 0
	mov	WORD PTR 32[rcx], ax
	ret
	.p2align 4,,10
	.p2align 3
.L25:
	cmp	ax, 6
	je	.L23
.L22:
	ud2
	.seh_endproc
	.p2align 4
	.def	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy
_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy:
.LFB324:
	.seh_endprologue
	or	WORD PTR 32[rcx], 1
	jmp	_Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor
	.seh_endproc
	.p2align 4
	.globl	_Z5rangei
	.def	_Z5rangei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5rangei
_Z5rangei:
.LFB319:
.L37:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 56
	mov	esi, edx
	call	_Znwy
	lea	rdx, _Z5rangePZ5rangeiE15_Z5rangei.Frame.destroy[rip]
	lea	rcx, _Z5rangePZ5rangeiE15_Z5rangei.Frame.actor[rip]
	movq	xmm1, rdx
	mov	DWORD PTR 32[rax], esi
	movq	xmm0, rcx
	mov	DWORD PTR 16[rax], esi
	mov	QWORD PTR [rbx], rax
	punpcklqdq	xmm0, xmm1
	mov	QWORD PTR 24[rax], rax
	movups	XMMWORD PTR [rax], xmm0
	mov	DWORD PTR 36[rax], 65538
	mov	rax, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z8count_upv
	.def	_Z8count_upv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8count_upv
_Z8count_upv:
.LFB322:
.L39:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 48
	call	_Znwy
	lea	rdx, _Z8count_upPZ8count_upvE18_Z8count_upv.Frame.destroy[rip]
	lea	rcx, _Z8count_upPZ8count_upvE18_Z8count_upv.Frame.actor[rip]
	movq	xmm1, rdx
	mov	QWORD PTR [rbx], rax
	movq	xmm0, rcx
	mov	QWORD PTR 24[rax], rax
	mov	DWORD PTR 32[rax], 65538
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR [rax], xmm0
	mov	rax, rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB325:
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
	je	.L46
	mov	rax, QWORD PTR [rbx]
	xor	esi, esi
	test	rax, rax
	jne	.L43
.L42:
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
.L40:
	mov	eax, esi
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L44:
	add	esi, DWORD PTR 16[rbx]
.L43:
	mov	rcx, rbx
.LEHB1:
	call	rax
.LEHE1:
	mov	rax, QWORD PTR [rbx]
	test	rax, rax
	jne	.L44
	jmp	.L42
.L46:
	xor	esi, esi
	jmp	.L40
.L48:
	mov	rsi, rax
	mov	rcx, rbx
	call	[QWORD PTR 8[rbx]]
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA325:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE325-.LLSDACSB325
.LLSDACSB325:
	.uleb128 .LEHB0-.LFB325
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB325
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L48-.LFB325
	.uleb128 0
	.uleb128 .LEHB2-.LFB325
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE325:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
