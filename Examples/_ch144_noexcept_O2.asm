	.file	"_ch144_noexcept.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_insert\0"
	.text
	.p2align 4
	.globl	_Z9fill_copyv
	.def	_Z9fill_copyv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9fill_copyv
_Z9fill_copyv:
.LFB1721:
	push	r14
	.seh_pushreg	r14
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
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	xor	r8d, r8d
	xor	ebx, ebx
	xor	esi, esi
	movabs	r13, 2305843009213693951
	mov	rdi, rcx
	mov	QWORD PTR [rcx], 0
	mov	QWORD PTR 8[rcx], 0
	mov	QWORD PTR 16[rcx], 0
	jmp	.L15
	.p2align 4,,10
	.p2align 3
.L30:
	mov	DWORD PTR [rbx], esi
	add	esi, 1
	add	rbx, 4
	cmp	esi, 16
	mov	QWORD PTR 8[rdi], rbx
	je	.L1
.L34:
	mov	rbx, QWORD PTR 8[rdi]
	mov	r8, QWORD PTR 16[rdi]
.L15:
	cmp	rbx, r8
	jne	.L30
	mov	r12, QWORD PTR [rdi]
	mov	r14, rbx
	sub	r14, r12
	mov	rbp, r14
	sar	rbp, 2
	cmp	rbp, r13
	je	.L31
	cmp	rbx, r12
	je	.L32
	lea	rax, [rbp+rbp]
	cmp	rax, rbp
	jb	.L19
	test	rax, rax
	jne	.L33
	mov	DWORD PTR [r14], esi
	xor	ebp, ebp
	xor	r9d, r9d
	xor	eax, eax
.L10:
	mov	rdx, r12
	.p2align 4,,10
	.p2align 3
.L12:
	mov	ecx, DWORD PTR [rdx]
	add	rdx, 4
	add	rax, 4
	mov	DWORD PTR -4[rax], ecx
	cmp	rbx, rdx
	jne	.L12
	sub	rbx, r12
	lea	rax, 4[r9+rbx]
.L11:
	movq	xmm6, r9
	movq	xmm0, rax
	test	r12, r12
	punpcklqdq	xmm6, xmm0
	je	.L13
	mov	rdx, r8
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L13:
	add	esi, 1
	movups	XMMWORD PTR [rdi], xmm6
	cmp	esi, 16
	mov	QWORD PTR 16[rdi], rbp
	jne	.L34
.L1:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	rax, rdi
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L32:
	add	rbp, 1
	jc	.L19
	movabs	rax, 2305843009213693951
	cmp	rbp, rax
	cmova	rbp, rax
	sal	rbp, 2
.L8:
	mov	rcx, rbp
.LEHB0:
	call	_Znwy
	add	rbp, rax
	cmp	rbx, r12
	mov	r8, QWORD PTR 16[rdi]
	mov	DWORD PTR [rax+r14], esi
	mov	r9, rax
	jne	.L10
	lea	rax, 4[rax]
	jmp	.L11
	.p2align 4,,10
	.p2align 3
.L19:
	movabs	rbp, 9223372036854775804
	jmp	.L8
.L33:
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rbp, 0[0+rax*4]
	jmp	.L8
.L31:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE0:
.L21:
	mov	rcx, QWORD PTR [rdi]
	mov	rbx, rax
	mov	rdx, QWORD PTR 16[rdi]
	sub	rdx, rcx
	test	rcx, rcx
	je	.L17
	call	_ZdlPvy
.L17:
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1721:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1721-.LLSDACSB1721
.LLSDACSB1721:
	.uleb128 .LEHB0-.LFB1721
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L21-.LFB1721
	.uleb128 0
	.uleb128 .LEHB1-.LFB1721
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1721:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z9fill_movev
	.def	_Z9fill_movev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9fill_movev
_Z9fill_movev:
.LFB1750:
	push	r14
	.seh_pushreg	r14
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
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	xor	r8d, r8d
	xor	ebx, ebx
	xor	esi, esi
	movabs	r13, 2305843009213693951
	mov	rdi, rcx
	mov	QWORD PTR [rcx], 0
	mov	QWORD PTR 8[rcx], 0
	mov	QWORD PTR 16[rcx], 0
	jmp	.L49
	.p2align 4,,10
	.p2align 3
.L63:
	mov	DWORD PTR [rbx], esi
	add	esi, 1
	add	rbx, 4
	cmp	esi, 16
	mov	QWORD PTR 8[rdi], rbx
	je	.L35
.L67:
	mov	rbx, QWORD PTR 8[rdi]
	mov	r8, QWORD PTR 16[rdi]
.L49:
	cmp	rbx, r8
	jne	.L63
	mov	r12, QWORD PTR [rdi]
	mov	r14, rbx
	sub	r14, r12
	mov	rbp, r14
	sar	rbp, 2
	cmp	rbp, r13
	je	.L64
	cmp	rbx, r12
	je	.L65
	lea	rax, [rbp+rbp]
	cmp	rax, rbp
	jb	.L53
	test	rax, rax
	jne	.L66
	mov	DWORD PTR [r14], esi
	xor	ebp, ebp
	xor	r9d, r9d
	xor	eax, eax
.L44:
	mov	rdx, r12
	.p2align 4,,10
	.p2align 3
.L46:
	mov	ecx, DWORD PTR [rdx]
	add	rdx, 4
	add	rax, 4
	mov	DWORD PTR -4[rax], ecx
	cmp	rbx, rdx
	jne	.L46
	sub	rbx, r12
	lea	rax, 4[r9+rbx]
.L45:
	movq	xmm6, r9
	movq	xmm0, rax
	test	r12, r12
	punpcklqdq	xmm6, xmm0
	je	.L47
	mov	rdx, r8
	mov	rcx, r12
	sub	rdx, r12
	call	_ZdlPvy
.L47:
	add	esi, 1
	movups	XMMWORD PTR [rdi], xmm6
	cmp	esi, 16
	mov	QWORD PTR 16[rdi], rbp
	jne	.L67
.L35:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	rax, rdi
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L65:
	add	rbp, 1
	jc	.L53
	movabs	rax, 2305843009213693951
	cmp	rbp, rax
	cmova	rbp, rax
	sal	rbp, 2
.L42:
	mov	rcx, rbp
.LEHB2:
	call	_Znwy
	add	rbp, rax
	cmp	rbx, r12
	mov	r8, QWORD PTR 16[rdi]
	mov	DWORD PTR [rax+r14], esi
	mov	r9, rax
	jne	.L44
	lea	rax, 4[rax]
	jmp	.L45
	.p2align 4,,10
	.p2align 3
.L53:
	movabs	rbp, 9223372036854775804
	jmp	.L42
.L66:
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	rbp, 0[0+rax*4]
	jmp	.L42
.L64:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L55:
	mov	rcx, QWORD PTR [rdi]
	mov	rbx, rax
	mov	rdx, QWORD PTR 16[rdi]
	sub	rdx, rcx
	test	rcx, rcx
	je	.L51
	call	_ZdlPvy
.L51:
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1750:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1750-.LLSDACSB1750
.LLSDACSB1750:
	.uleb128 .LEHB2-.LFB1750
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L55-.LFB1750
	.uleb128 0
	.uleb128 .LEHB3-.LFB1750
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE1750:
	.text
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
