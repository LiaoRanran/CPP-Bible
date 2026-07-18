	.file	"ch86_adapters_test.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt11_Deque_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt11_Deque_baseIiSaIiEED2Ev
	.def	_ZNSt11_Deque_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt11_Deque_baseIiSaIiEED2Ev
_ZNSt11_Deque_baseIiSaIiEED2Ev:
.LFB4943:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rdi, rcx
	mov	rcx, QWORD PTR [rcx]
	test	rcx, rcx
	je	.L1
	mov	rax, QWORD PTR 72[rdi]
	mov	rbx, QWORD PTR 40[rdi]
	lea	rsi, 8[rax]
	cmp	rbx, rsi
	jnb	.L3
	.p2align 4
	.p2align 3
.L4:
	mov	rcx, QWORD PTR [rbx]
	mov	edx, 512
	add	rbx, 8
	call	_ZdlPvy
	cmp	rbx, rsi
	jb	.L4
	mov	rcx, QWORD PTR [rdi]
.L3:
	mov	rdx, QWORD PTR 8[rdi]
	sal	rdx, 3
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section	.text$_ZNSt5dequeIiSaIiEE4backEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt5dequeIiSaIiEE4backEv
	.def	_ZNSt5dequeIiSaIiEE4backEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE4backEv
_ZNSt5dequeIiSaIiEE4backEv:
.LFB4952:
	.seh_endprologue
	mov	rax, QWORD PTR 48[rcx]
	cmp	rax, QWORD PTR 56[rcx]
	je	.L9
	sub	rax, 4
	ret
	.p2align 4,,10
	.p2align 3
.L9:
	mov	rax, QWORD PTR 72[rcx]
	mov	rax, QWORD PTR -8[rax]
	add	rax, 512
	sub	rax, 4
	ret
	.seh_endproc
	.section	.text$_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy
	.def	_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy
_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy:
.LFB5042:
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
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	eax, 8
	mov	rbx, rdx
	mov	rsi, rcx
	mov	rdi, rdx
	shr	rbx, 7
	lea	rbp, 1[rbx]
	add	rbx, 3
	cmp	rbx, rax
	cmovb	rbx, rax
	mov	QWORD PTR 8[rcx], rbx
	lea	rcx, 0[0+rbx*8]
	sub	rbx, rbp
	shr	rbx
.LEHB0:
	call	_Znwy
.LEHE0:
	lea	r12, [rax+rbx*8]
	mov	QWORD PTR [rsi], rax
	lea	rbp, [r12+rbp*8]
	cmp	r12, rbp
	jnb	.L11
	mov	rbx, r12
	.p2align 4
	.p2align 3
.L12:
	mov	ecx, 512
.LEHB1:
	call	_Znwy
.LEHE1:
	mov	QWORD PTR [rbx], rax
	add	rbx, 8
	cmp	rbx, rbp
	jb	.L12
.L11:
	mov	rax, QWORD PTR [r12]
	and	edi, 127
	mov	QWORD PTR 40[rsi], r12
	lea	rdx, 512[rax]
	movq	xmm0, rax
	mov	QWORD PTR 32[rsi], rdx
	lea	rdx, -8[rbp]
	punpcklqdq	xmm0, xmm0
	mov	QWORD PTR 72[rsi], rdx
	mov	rdx, QWORD PTR -8[rbp]
	movups	XMMWORD PTR 16[rsi], xmm0
	lea	rcx, 512[rdx]
	lea	rax, [rdx+rdi*4]
	mov	QWORD PTR 56[rsi], rdx
	mov	QWORD PTR 64[rsi], rcx
	mov	QWORD PTR 48[rsi], rax
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L19:
.L13:
	mov	rcx, rax
	call	__cxa_begin_catch
.L14:
	cmp	r12, rbx
	jnb	.L23
	mov	rcx, QWORD PTR [r12]
	mov	edx, 512
	add	r12, 8
	call	_ZdlPvy
	jmp	.L14
.L23:
.LEHB2:
	call	__cxa_rethrow
.LEHE2:
.L20:
	mov	rbx, rax
.L16:
	call	__cxa_end_catch
	mov	rcx, rbx
	call	__cxa_begin_catch
	mov	rax, QWORD PTR 8[rsi]
	mov	rcx, QWORD PTR [rsi]
	lea	rdx, 0[0+rax*8]
	call	_ZdlPvy
	xor	eax, eax
	mov	QWORD PTR [rsi], rax
	mov	QWORD PTR 8[rsi], rax
.LEHB3:
	call	__cxa_rethrow
.LEHE3:
.L18:
	mov	rbx, rax
.L17:
	call	__cxa_end_catch
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
	.align 4
.LLSDA5042:
	.byte	0xff
	.byte	0x9b
	.uleb128 .LLSDATT5042-.LLSDATTD5042
.LLSDATTD5042:
	.byte	0x1
	.uleb128 .LLSDACSE5042-.LLSDACSB5042
.LLSDACSB5042:
	.uleb128 .LEHB0-.LFB5042
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5042
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L19-.LFB5042
	.uleb128 0x1
	.uleb128 .LEHB2-.LFB5042
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L20-.LFB5042
	.uleb128 0x3
	.uleb128 .LEHB3-.LFB5042
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L18-.LFB5042
	.uleb128 0
	.uleb128 .LEHB4-.LFB5042
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE5042:
	.byte	0x1
	.byte	0
	.byte	0
	.byte	0x7d
	.align 4
	.long	0

.LLSDATT5042:
	.section	.text$_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy,"x"
	.linkonce discard
	.seh_endproc
	.section	.text$_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
	.def	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb:
.LFB5208:
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
	sub	rsp, 72
	.seh_stackalloc	72
	.seh_endprologue
	mov	r9, QWORD PTR 72[rcx]
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, r9
	mov	rsi, rdx
	mov	rdx, QWORD PTR 40[rcx]
	mov	rbx, rcx
	sub	rbp, rdx
	mov	rax, rbp
	sar	rax, 3
	lea	r10, 1[rsi+rax]
	lea	rax, [r10+r10]
	cmp	rax, rdi
	jnb	.L25
	sub	rdi, r10
	shr	rdi
	sal	rdi, 3
	test	r8b, r8b
	lea	r8, 8[r9]
	lea	rax, [rdi+rsi*8]
	cmovne	rdi, rax
	add	rdi, QWORD PTR [rcx]
	sub	r8, rdx
	mov	rsi, rdi
	cmp	rdi, rdx
	jnb	.L27
	cmp	r8, 8
	jle	.L28
	mov	rcx, rdi
	call	memmove
	mov	rax, QWORD PTR [rdi]
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L25:
	cmp	rdi, rsi
	mov	rax, rsi
	mov	DWORD PTR 60[rsp], r8d
	cmovnb	rax, rdi
	mov	QWORD PTR 40[rsp], rdx
	mov	QWORD PTR 32[rsp], r9
	lea	r12, 2[rdi+rax]
	mov	QWORD PTR 48[rsp], r10
	lea	rcx, 0[0+r12*8]
	call	_Znwy
	mov	r9, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	mov	r13, rax
	mov	rax, r12
	sub	rax, QWORD PTR 48[rsp]
	shr	rax
	lea	r8, 8[r9]
	sal	rax, 3
	cmp	BYTE PTR 60[rsp], 0
	lea	rcx, [rax+rsi*8]
	cmovne	rax, rcx
	sub	r8, rdx
	lea	rsi, 0[r13+rax]
	cmp	r8, 8
	jle	.L34
	mov	rcx, rsi
	call	memmove
.L35:
	mov	rcx, QWORD PTR [rbx]
	lea	rdx, 0[0+rdi*8]
	call	_ZdlPvy
	mov	QWORD PTR [rbx], r13
	mov	QWORD PTR 8[rbx], r12
.L36:
	mov	rax, QWORD PTR [rsi]
.L29:
	mov	QWORD PTR 24[rbx], rax
	add	rax, 512
	mov	QWORD PTR 40[rbx], rsi
	add	rsi, rbp
	mov	QWORD PTR 32[rbx], rax
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 72[rbx], rsi
	lea	rdx, 512[rax]
	movq	xmm0, rax
	movq	xmm1, rdx
	punpcklqdq	xmm0, xmm1
	movups	XMMWORD PTR 56[rbx], xmm0
	add	rsp, 72
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L27:
	mov	rax, r8
	sal	rax, 61
	sub	rax, r8
	lea	rcx, 8[rbp+rax]
	add	rcx, rdi
	cmp	r8, 8
	jle	.L31
	call	memmove
	mov	rax, QWORD PTR [rdi]
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L34:
	jne	.L35
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rsi], rax
	jmp	.L35
	.p2align 4,,10
	.p2align 3
.L31:
	jne	.L36
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rcx], rax
	mov	rax, QWORD PTR [rdi]
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L28:
	jne	.L36
	mov	rax, QWORD PTR [rdx]
	mov	QWORD PTR [rdi], rax
	jmp	.L29
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::deque larger than max_size()\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB1:
	.text
.LHOTB1:
	.align 2
	.p2align 4
	.def	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0
_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0:
.LFB5255:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rax, QWORD PTR 48[rcx]
	mov	r9, rcx
	mov	rcx, QWORD PTR 64[rcx]
	mov	r10, rdx
	lea	rdx, -4[rcx]
	cmp	rax, rdx
	je	.L38
	mov	edx, DWORD PTR [r10]
	add	rax, 4
	mov	DWORD PTR -4[rax], edx
.L39:
	mov	QWORD PTR 48[r9], rax
	add	rsp, 56
	ret
.L38:
	mov	rcx, QWORD PTR 72[r9]
	mov	rdx, rcx
	sub	rdx, QWORD PTR 40[r9]
	sar	rdx, 3
	cmp	rcx, 1
	adc	rdx, -1
	sub	rax, QWORD PTR 56[r9]
	sal	rdx, 7
	sar	rax, 2
	add	rax, rdx
	mov	rdx, QWORD PTR 32[r9]
	sub	rdx, QWORD PTR 16[r9]
	sar	rdx, 2
	add	rax, rdx
	movabs	rdx, 4611686018427387903
	cmp	rax, rdx
	je	.L42
	mov	rax, QWORD PTR 8[r9]
	sub	rcx, QWORD PTR [r9]
	sar	rcx, 3
	sub	rax, rcx
	cmp	rax, 1
	jbe	.L43
.L41:
	mov	rdx, QWORD PTR 72[r9]
	mov	ecx, 512
	mov	QWORD PTR 72[rsp], r10
	mov	QWORD PTR 64[rsp], r9
	mov	QWORD PTR 40[rsp], rdx
	call	_Znwy
	mov	r9, QWORD PTR 64[rsp]
	mov	rdx, QWORD PTR 40[rsp]
	mov	r10, QWORD PTR 72[rsp]
	mov	QWORD PTR 8[rdx], rax
	mov	rcx, QWORD PTR 48[r9]
	add	rdx, 8
	mov	r8d, DWORD PTR [r10]
	mov	DWORD PTR [rcx], r8d
	mov	QWORD PTR 72[r9], rdx
	lea	rdx, 512[rax]
	mov	QWORD PTR 56[r9], rax
	mov	QWORD PTR 64[r9], rdx
	jmp	.L39
.L43:
	mov	rcx, r9
	xor	r8d, r8d
	mov	edx, 1
	mov	QWORD PTR 72[rsp], r10
	mov	QWORD PTR 64[rsp], r9
	call	_ZNSt5dequeIiSaIiEE17_M_reallocate_mapEyb
	mov	r10, QWORD PTR 72[rsp]
	mov	r9, QWORD PTR 64[rsp]
	jmp	.L41
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0.cold
	.seh_stackalloc	56
	.seh_endprologue
_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0.cold:
.L42:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely,"x"
.LCOLDB2:
	.section	.text.startup,"x"
.LHOTB2:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4473:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 208
	.seh_stackalloc	208
	.seh_endprologue
	call	__main
	pxor	xmm0, xmm0
	xor	edx, edx
	lea	rcx, 48[rsp]
	mov	QWORD PTR 48[rsp], 0
	mov	QWORD PTR 56[rsp], 0
	movaps	XMMWORD PTR 64[rsp], xmm0
	movaps	XMMWORD PTR 80[rsp], xmm0
	movaps	XMMWORD PTR 96[rsp], xmm0
	movaps	XMMWORD PTR 112[rsp], xmm0
.LEHB5:
	call	_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy
.LEHE5:
	lea	rdx, 128[rsp]
	lea	rcx, 48[rsp]
	mov	DWORD PTR 128[rsp], 1
.LEHB6:
	call	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0
	lea	rdx, 128[rsp]
	lea	rcx, 48[rsp]
	mov	DWORD PTR 128[rsp], 2
	call	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0
	lea	rcx, 48[rsp]
	call	_ZNSt5dequeIiSaIiEE4backEv
	pxor	xmm0, xmm0
	xor	edx, edx
	lea	rcx, 128[rsp]
	mov	eax, DWORD PTR [rax]
	movaps	XMMWORD PTR 144[rsp], xmm0
	mov	QWORD PTR 128[rsp], 0
	mov	DWORD PTR 36[rsp], eax
	mov	eax, DWORD PTR 36[rsp]
	mov	QWORD PTR 136[rsp], 0
	movaps	XMMWORD PTR 160[rsp], xmm0
	movaps	XMMWORD PTR 176[rsp], xmm0
	movaps	XMMWORD PTR 192[rsp], xmm0
	call	_ZNSt11_Deque_baseIiSaIiEE17_M_initialize_mapEy
.LEHE6:
	lea	rdx, 44[rsp]
	lea	rcx, 128[rsp]
	mov	DWORD PTR 44[rsp], 1
.LEHB7:
	call	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0
.LEHE7:
	lea	rdx, 44[rsp]
	lea	rcx, 128[rsp]
	mov	DWORD PTR 44[rsp], 2
.LEHB8:
	call	_ZNSt5dequeIiSaIiEE12emplace_backIJiEEERiDpOT_.isra.0
.LEHE8:
	mov	rax, QWORD PTR 144[rsp]
	lea	rcx, 128[rsp]
	mov	eax, DWORD PTR [rax]
	mov	DWORD PTR 40[rsp], eax
	mov	eax, DWORD PTR 40[rsp]
	call	_ZNSt5dequeIiSaIiEE4backEv
	lea	rcx, 128[rsp]
	mov	eax, DWORD PTR [rax]
	mov	DWORD PTR 44[rsp], eax
	mov	eax, DWORD PTR 44[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev
	lea	rcx, 48[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev
	xor	eax, eax
	add	rsp, 208
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L50:
	mov	rdi, rax
	jmp	.L49
.L51:
	mov	rdi, rax
	jmp	.L48
.L52:
	mov	rdi, rax
	jmp	.L48
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4473:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4473-.LLSDACSB4473
.LLSDACSB4473:
	.uleb128 .LEHB5-.LFB4473
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB6-.LFB4473
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L50-.LFB4473
	.uleb128 0
	.uleb128 .LEHB7-.LFB4473
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L52-.LFB4473
	.uleb128 0
	.uleb128 .LEHB8-.LFB4473
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L51-.LFB4473
	.uleb128 0
.LLSDACSE4473:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	232
	.seh_savereg	rbx, 208
	.seh_savereg	rsi, 216
	.seh_savereg	rdi, 224
	.seh_endprologue
main.cold:
.L48:
	lea	rcx, 128[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev
.L49:
	lea	rcx, 48[rsp]
	call	_ZNSt11_Deque_baseIiSaIiEED2Ev
	mov	rcx, rdi
.LEHB9:
	call	_Unwind_Resume
	nop
.LEHE9:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4473:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4473-.LLSDACSBC4473
.LLSDACSBC4473:
	.uleb128 .LEHB9-.LCOLDB2
	.uleb128 .LEHE9-.LEHB9
	.uleb128 0
	.uleb128 0
.LLSDACSEC4473:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.section	.text.startup,"x"
.LHOTE2:
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	__cxa_begin_catch;	.scl	2;	.type	32;	.endef
	.def	__cxa_rethrow;	.scl	2;	.type	32;	.endef
	.def	__cxa_end_catch;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	memmove;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
