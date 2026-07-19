	.file	"ch115_move_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12make_big_rvov
	.def	_Z12make_big_rvov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12make_big_rvov
_Z12make_big_rvov:
.LFB253:
	push	rdi
	.seh_pushreg	rdi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rbx, rcx
	mov	ecx, 1024
	call	_Znay
	mov	QWORD PTR 8[rbx], 1024
	lea	rdx, 8[rax]
	mov	QWORD PTR [rbx], rax
	and	rdx, -8
	mov	QWORD PTR [rax], 0
	mov	QWORD PTR 1016[rax], 0
	sub	rax, rdx
	mov	rdi, rdx
	lea	ecx, 1024[rax]
	xor	eax, eax
	shr	ecx, 3
	rep stosq
	mov	rax, rbx
	add	rsp, 40
	pop	rbx
	pop	rdi
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11consume_big3Big
	.def	_Z11consume_big3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11consume_big3Big
_Z11consume_big3Big:
.LFB254:
	.seh_endprologue
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17move_into_consumeO3Big
	.def	_Z17move_into_consumeO3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17move_into_consumeO3Big
_Z17move_into_consumeO3Big:
.LFB255:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	QWORD PTR 8[rcx], 0
	mov	QWORD PTR [rcx], 0
	test	rax, rax
	je	.L4
	mov	rcx, rax
	jmp	_ZdaPv
	.p2align 4,,10
	.p2align 3
.L4:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE
	.def	_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE
_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE:
.LFB1785:
	push	r14
	.seh_pushreg	r14
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	rbx, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR 16[rcx]
	mov	rsi, rcx
	cmp	rbx, rdx
	je	.L7
	mov	ecx, 512
	add	rbx, 16
.LEHB0:
	call	_Znay
	mov	QWORD PTR -8[rbx], 512
	lea	rdx, 8[rax]
	mov	QWORD PTR -16[rbx], rax
	and	rdx, -8
	mov	QWORD PTR [rax], 0
	mov	QWORD PTR 504[rax], 0
	sub	rax, rdx
	mov	rdi, rdx
	lea	ecx, 512[rax]
	xor	eax, eax
	shr	ecx, 3
	rep stosq
	mov	QWORD PTR 8[rsi], rbx
.L8:
	mov	ecx, 256
	call	_Znay
	lea	rdx, 8[rax]
	mov	rcx, rax
	mov	QWORD PTR [rax], 0
	mov	rbp, rax
	mov	QWORD PTR 248[rax], 0
	and	rdx, -8
	xor	eax, eax
	sub	rcx, rdx
	mov	rdi, rdx
	add	ecx, 256
	shr	ecx, 3
	rep stosq
	cmp	QWORD PTR 16[rsi], rbx
	je	.L14
	mov	QWORD PTR [rbx], rbp
	add	rbx, 16
	mov	QWORD PTR -8[rbx], 256
	mov	QWORD PTR 8[rsi], rbx
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	movabs	rax, 576460752303423487
	mov	r9, QWORD PTR [rcx]
	mov	r8, rbx
	sub	r8, r9
	mov	rcx, r8
	sar	rcx, 4
	cmp	rcx, rax
	je	.L35
	test	rcx, rcx
	mov	eax, 1
	mov	QWORD PTR 40[rsp], r8
	cmovne	rax, rcx
	mov	QWORD PTR 56[rsp], r9
	mov	QWORD PTR 48[rsp], rdx
	add	rax, rcx
	movabs	rcx, 576460752303423487
	cmp	rax, rcx
	cmova	rax, rcx
	sal	rax, 4
	mov	rcx, rax
	mov	r14, rax
	call	_Znwy
.LEHE0:
	mov	r8, QWORD PTR 40[rsp]
	mov	ecx, 512
	mov	rbp, rax
	add	r8, rax
	mov	QWORD PTR 40[rsp], r8
.LEHB1:
	call	_Znay
.LEHE1:
	mov	r8, QWORD PTR 40[rsp]
	mov	QWORD PTR [r8], rax
	mov	QWORD PTR 8[r8], 512
	lea	r8, 8[rax]
	and	r8, -8
	mov	QWORD PTR [rax], 0
	mov	QWORD PTR 504[rax], 0
	sub	rax, r8
	mov	rdi, r8
	lea	ecx, 512[rax]
	xor	eax, eax
	shr	ecx, 3
	rep stosq
	mov	r9, QWORD PTR 56[rsp]
	mov	rdx, QWORD PTR 48[rsp]
	cmp	rbx, r9
	je	.L22
	mov	rax, r9
	mov	rcx, rbp
	.p2align 5
	.p2align 4
	.p2align 3
.L11:
	mov	r8, QWORD PTR [rax]
	add	rax, 16
	add	rcx, 16
	mov	QWORD PTR -16[rcx], r8
	mov	r8, QWORD PTR -8[rax]
	mov	QWORD PTR -8[rcx], r8
	cmp	rbx, rax
	jne	.L11
	sub	rbx, r9
	add	rbx, rbp
.L10:
	add	rbx, 16
	test	r9, r9
	je	.L12
	sub	rdx, r9
	mov	rcx, r9
	call	_ZdlPvy
.L12:
	mov	QWORD PTR [rsi], rbp
	add	rbp, r14
	mov	QWORD PTR 8[rsi], rbx
	mov	QWORD PTR 16[rsi], rbp
	jmp	.L8
	.p2align 4,,10
	.p2align 3
.L14:
	movabs	rax, 576460752303423487
	mov	r8, QWORD PTR [rsi]
	mov	r9, rbx
	sub	r9, r8
	mov	rdx, r9
	sar	rdx, 4
	cmp	rdx, rax
	je	.L36
	test	rdx, rdx
	mov	eax, 1
	mov	QWORD PTR 48[rsp], r9
	cmovne	rax, rdx
	mov	QWORD PTR 40[rsp], r8
	add	rax, rdx
	movabs	rdx, 576460752303423487
	cmp	rax, rdx
	cmova	rax, rdx
	sal	rax, 4
	mov	rcx, rax
	mov	rdi, rax
.LEHB2:
	call	_Znwy
.LEHE2:
	mov	r9, QWORD PTR 48[rsp]
	mov	r8, QWORD PTR 40[rsp]
	mov	r10, rax
	mov	QWORD PTR [rax+r9], rbp
	mov	QWORD PTR 8[rax+r9], 256
	cmp	r8, rbx
	je	.L17
	mov	rax, r8
	mov	rdx, r10
	.p2align 5
	.p2align 4
	.p2align 3
.L18:
	mov	rcx, QWORD PTR [rax]
	add	rax, 16
	add	rdx, 16
	mov	QWORD PTR -16[rdx], rcx
	mov	rcx, QWORD PTR -8[rax]
	mov	QWORD PTR -8[rdx], rcx
	cmp	rax, rbx
	jne	.L18
	sub	rax, r8
	lea	rbx, 16[r10+rax]
	test	r8, r8
	je	.L19
.L21:
	mov	rdx, r9
	mov	rcx, r8
	mov	QWORD PTR 40[rsp], r10
	call	_ZdlPvy
	mov	r10, QWORD PTR 40[rsp]
.L19:
	mov	QWORD PTR [rsi], r10
	add	r10, rdi
	mov	QWORD PTR 8[rsi], rbx
	mov	QWORD PTR 16[rsi], r10
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L22:
	mov	rbx, rbp
	jmp	.L10
.L17:
	lea	rbx, 16[rax]
	jmp	.L21
.L33:
	jmp	.L34
.L24:
	mov	rbx, rax
	jmp	.L13
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1785:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1785-.LLSDACSB1785
.LLSDACSB1785:
	.uleb128 .LEHB0-.LFB1785
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1785
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L24-.LFB1785
	.uleb128 0
	.uleb128 .LEHB2-.LFB1785
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L33-.LFB1785
	.uleb128 0
.LLSDACSE1785:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 64
	.seh_savereg	rsi, 72
	.seh_savereg	rdi, 80
	.seh_savereg	rbp, 88
	.seh_savereg	r14, 96
	.seh_endprologue
_Z15emplace_vs_pushRSt6vectorI3BigSaIS0_EE.cold:
.L36:
	lea	rcx, .LC0[rip]
.LEHB3:
	call	_ZSt20__throw_length_errorPKc
.LEHE3:
.L23:
.L34:
	mov	rbx, rax
	mov	rcx, rbp
	call	_ZdaPv
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.L35:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.L13:
	mov	rcx, rbp
	mov	rdx, r14
	call	_ZdlPvy
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC1785:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC1785-.LLSDACSBC1785
.LLSDACSBC1785:
	.uleb128 .LEHB3-.LCOLDB1
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L23-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB4-.LCOLDB1
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSEC1785:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
