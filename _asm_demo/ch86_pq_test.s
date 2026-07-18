	.file	"ch86_pq_test.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "vector::_M_realloc_append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.section	.text.startup,"x"
.LHOTB1:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4441:
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
	.seh_endprologue
	xor	esi, esi
	xor	r12d, r12d
	xor	ebx, ebx
	movabs	rdi, 2305843009213693951
	xor	ebp, ebp
	call	__main
	.p2align 4
	.p2align 3
.L10:
	cmp	rsi, r12
	je	.L2
	mov	DWORD PTR [r12], ebp
	mov	r8d, ebp
	add	r12, 4
.L3:
	mov	rdx, r12
	sub	rdx, rbx
	mov	rax, rdx
	sar	rax, 2
	lea	rcx, -1[rax]
	test	rcx, rcx
	jle	.L7
	sub	rax, 2
	sar	rax
	jmp	.L9
	.p2align 6
	.p2align 4,,10
	.p2align 3
.L32:
	mov	DWORD PTR [rcx], edx
	lea	rdx, -1[rax]
	mov	rcx, rax
	shr	rdx, 63
	test	rax, rax
	je	.L31
	lea	rax, -1[rax+rdx]
	sar	rax
.L9:
	lea	r9, [rbx+rax*4]
	lea	rcx, [rbx+rcx*4]
	mov	edx, DWORD PTR [r9]
	cmp	r8d, edx
	jg	.L32
.L8:
	add	ebp, 1
	mov	DWORD PTR [rcx], r8d
	cmp	ebp, 100
	jne	.L10
.L33:
	mov	eax, DWORD PTR [rbx]
	sub	rsi, rbx
	mov	rcx, rbx
	mov	rdx, rsi
	mov	DWORD PTR 44[rsp], eax
	mov	eax, DWORD PTR 44[rsp]
	call	_ZdlPvy
	xor	eax, eax
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
.L31:
	mov	rcx, r9
	add	ebp, 1
	mov	DWORD PTR [rcx], r8d
	cmp	ebp, 100
	jne	.L10
	jmp	.L33
	.p2align 4,,10
	.p2align 3
.L2:
	mov	r12, rsi
	sub	r12, rbx
	mov	rdx, r12
	sar	rdx, 2
	cmp	rdx, rdi
	je	.L27
	test	rdx, rdx
	mov	eax, 1
	cmovne	rax, rdx
	add	rax, rdx
	movabs	rdx, 2305843009213693951
	cmp	rax, rdx
	cmova	rax, rdx
	lea	r13, 0[0+rax*4]
	mov	rcx, r13
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	DWORD PTR [rax+r12], ebp
	mov	r14, rax
	test	r12, r12
	je	.L5
	mov	r8, r12
	mov	rdx, rbx
	mov	rcx, rax
	call	memcpy
.L5:
	lea	r12, 4[r14+r12]
	test	rbx, rbx
	je	.L6
	sub	rsi, rbx
	mov	rcx, rbx
	mov	rdx, rsi
	call	_ZdlPvy
.L6:
	mov	r8d, DWORD PTR -4[r12]
	lea	rsi, [r14+r13]
	mov	rbx, r14
	jmp	.L3
.L7:
	lea	rcx, -4[rbx+rdx]
	jmp	.L8
.L25:
	jmp	.L26
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4441:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4441-.LLSDACSB4441
.LLSDACSB4441:
	.uleb128 .LEHB0-.LFB4441
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L25-.LFB4441
	.uleb128 0
.LLSDACSE4441:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r12, 80
	.seh_savereg	r13, 88
	.seh_savereg	r14, 96
	.seh_endprologue
main.cold:
.L27:
	lea	rcx, .LC0[rip]
.LEHB1:
	call	_ZSt20__throw_length_errorPKc
.LEHE1:
.L14:
.L26:
	mov	rdi, rax
	test	rbx, rbx
	je	.L12
	sub	rsi, rbx
	mov	rcx, rbx
	mov	rdx, rsi
	call	_ZdlPvy
.L12:
	mov	rcx, rdi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4441:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4441-.LLSDACSBC4441
.LLSDACSBC4441:
	.uleb128 .LEHB1-.LCOLDB1
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L14-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC4441:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.section	.text.startup,"x"
.LHOTE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
