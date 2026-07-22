	.file	"_ch124_vector.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0:
.LFB3074:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sub	rdx, rcx
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10sum_vectorRKSt6vectorIiSaIiEE
	.def	_Z10sum_vectorRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sum_vectorRKSt6vectorIiSaIiEE
_Z10sum_vectorRKSt6vectorIiSaIiEE:
.LFB2392:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rcx, rax
	je	.L4
	.p2align 4
	.p2align 4
	.p2align 3
.L6:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L6
.L4:
	mov	eax, edx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::append\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z13make_greetingB5cxx11PKc
	.def	_Z13make_greetingB5cxx11PKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13make_greetingB5cxx11PKc
_Z13make_greetingB5cxx11PKc:
.LFB2397:
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
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	lea	rbp, 16[rcx]
	mov	DWORD PTR 16[rcx], 1819043144
	mov	rbx, rcx
	mov	rdi, rdx
	mov	QWORD PTR [rcx], rbp
	mov	DWORD PTR 3[rbp], 539783020
	mov	QWORD PTR 8[rcx], 7
	mov	BYTE PTR 23[rcx], 0
	mov	rcx, rdx
	call	strlen
	mov	rsi, rax
	movabs	rax, 9223372036854775799
	cmp	rax, rsi
	jb	.L21
	lea	r9, 7[rsi]
	cmp	r9, 15
	ja	.L11
	test	rsi, rsi
	je	.L13
	cmp	rsi, 1
	je	.L23
	lea	rcx, 23[rbx]
	mov	r8, rsi
	mov	rdx, rdi
	mov	QWORD PTR 32[rsp], r9
	call	memcpy
	mov	r9, QWORD PTR 32[rsp]
.L13:
	mov	rax, rbx
	mov	QWORD PTR 8[rbx], r9
	mov	BYTE PTR 7[rbp+rsi], 0
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r14
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	cmp	r9, 29
	jbe	.L19
	lea	rcx, 8[rsi]
	mov	r14, r9
.L16:
	mov	QWORD PTR 40[rsp], r9
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8, rsi
	mov	rdx, rdi
	mov	r10, rax
	mov	eax, DWORD PTR 16[rbx]
	lea	rcx, 7[r10]
	mov	QWORD PTR 32[rsp], r10
	mov	DWORD PTR [r10], eax
	mov	eax, DWORD PTR 3[rbp]
	mov	DWORD PTR 3[r10], eax
	call	memcpy
	mov	r10, QWORD PTR 32[rsp]
	mov	QWORD PTR 16[rbx], r14
	mov	r9, QWORD PTR 40[rsp]
	mov	QWORD PTR [rbx], r10
	mov	rbp, r10
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L23:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR 23[rbx], al
	jmp	.L13
	.p2align 4,,10
	.p2align 3
.L19:
	mov	r14d, 30
	mov	ecx, 31
	jmp	.L16
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2397:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2397-.LLSDACSB2397
.LLSDACSB2397:
	.uleb128 .LEHB0-.LFB2397
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
.LLSDACSE2397:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z13make_greetingB5cxx11PKc.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13make_greetingB5cxx11PKc.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r14, 80
	.seh_endprologue
_Z13make_greetingB5cxx11PKc.cold:
.L21:
	lea	rcx, .LC0[rip]
.LEHB1:
	call	_ZSt20__throw_length_errorPKc
.LEHE1:
.L20:
	mov	rcx, QWORD PTR [rbx]
	mov	rsi, rax
	cmp	rbp, rcx
	jne	.L24
.L18:
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
.LEHE2:
.L24:
	mov	rdx, QWORD PTR 16[rbx]
	add	rdx, 1
	call	_ZdlPvy
	jmp	.L18
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2397:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2397-.LLSDACSBC2397
.LLSDACSBC2397:
	.uleb128 .LEHB1-.LCOLDB1
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L20-.LCOLDB1
	.uleb128 0
	.uleb128 .LEHB2-.LCOLDB1
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC2397:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section .rdata,"dr"
.LC2:
	.ascii "world\0"
	.section	.text.unlikely,"x"
.LCOLDB3:
	.section	.text.startup,"x"
.LHOTB3:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2418:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	call	__main
	mov	ecx, 20
.LEHB3:
	call	_Znwy
.LEHE3:
	lea	rcx, 32[rsp]
	lea	rdx, .LC2[rip]
	mov	rsi, rax
.LEHB4:
	call	_Z13make_greetingB5cxx11PKc
.LEHE4:
	mov	rcx, QWORD PTR 32[rsp]
	lea	rax, 48[rsp]
	mov	rbx, QWORD PTR 40[rsp]
	cmp	rcx, rax
	je	.L28
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L28:
	lea	rdx, 20[rsi]
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	lea	eax, 15[rbx]
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L31:
	mov	rbx, rax
	jmp	.L27
.L30:
	mov	rbx, rax
	jmp	.L29
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2418:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2418-.LLSDACSB2418
.LLSDACSB2418:
	.uleb128 .LEHB3-.LFB2418
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L31-.LFB2418
	.uleb128 0
	.uleb128 .LEHB4-.LFB2418
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L30-.LFB2418
	.uleb128 0
.LLSDACSE2418:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 64
	.seh_savereg	rsi, 72
	.seh_savereg	rdi, 80
	.seh_endprologue
main.cold:
.L27:
	xor	ecx, ecx
	xor	edx, edx
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rbx
.LEHB5:
	call	_Unwind_Resume
.L29:
	mov	rcx, rsi
	lea	rdx, 20[rsi]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE5:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2418:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2418-.LLSDACSBC2418
.LLSDACSBC2418:
	.uleb128 .LEHB5-.LCOLDB3
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSEC2418:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE3:
	.section	.text.startup,"x"
.LHOTE3:
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
