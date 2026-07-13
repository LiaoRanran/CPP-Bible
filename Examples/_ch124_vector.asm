	.file	"_ch124_vector.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10sum_vectorRKSt6vectorIiSaIiEE
	.def	_Z10sum_vectorRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10sum_vectorRKSt6vectorIiSaIiEE
_Z10sum_vectorRKSt6vectorIiSaIiEE:
.LFB2313:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rcx, rax
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L3
.L1:
	mov	eax, edx
	ret
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:
.LFB2693:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L7
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L7:
	ret
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIiSaIiEED2Ev
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev
_ZNSt12_Vector_baseIiSaIiEED2Ev:
.LFB2697:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L9
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L9:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_create\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy:
.LFB2959:
	push	r15
	.seh_pushreg	r15
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rsi, QWORD PTR 144[rsp]
	lea	r13, [rdx+r8]
	mov	r15, rax
	mov	rbx, rcx
	sub	rsi, r8
	sub	r15, r13
	mov	r12, rdx
	lea	r14, 16[rcx]
	add	rsi, rax
	cmp	r14, QWORD PTR [rcx]
	mov	rbp, r9
	je	.L24
	mov	rax, QWORD PTR 16[rcx]
.L12:
	test	rsi, rsi
	js	.L37
	cmp	rax, rsi
	jnb	.L14
	add	rax, rax
	cmp	rsi, rax
	jnb	.L14
	test	rax, rax
	js	.L15
	lea	rcx, 1[rax]
	mov	rsi, rax
	call	_Znwy
	test	r12, r12
	mov	rdi, rax
	je	.L17
	cmp	r12, 1
	mov	rdx, QWORD PTR [rbx]
	je	.L38
	.p2align 4,,10
	.p2align 3
.L18:
	mov	r8, r12
	mov	rcx, rax
	call	memcpy
.L17:
	test	rbp, rbp
	je	.L19
	cmp	QWORD PTR 144[rsp], 0
	je	.L19
	cmp	QWORD PTR 144[rsp], 1
	lea	rcx, [rdi+r12]
	je	.L39
	mov	r8, QWORD PTR 144[rsp]
	mov	rdx, rbp
	call	memcpy
.L19:
	test	r15, r15
	mov	rbp, QWORD PTR [rbx]
	jne	.L40
.L21:
	cmp	rbp, r14
	je	.L23
	mov	rax, QWORD PTR 16[rbx]
	mov	rcx, rbp
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L23:
	mov	QWORD PTR [rbx], rdi
	mov	QWORD PTR 16[rbx], rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.p2align 4,,10
	.p2align 3
.L14:
	mov	rcx, rsi
	add	rcx, 1
	js	.L15
	call	_Znwy
	test	r12, r12
	mov	rdi, rax
	je	.L17
	cmp	r12, 1
	mov	rdx, QWORD PTR [rbx]
	jne	.L18
.L38:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rdi], al
	jmp	.L17
	.p2align 4,,10
	.p2align 3
.L40:
	mov	r10, QWORD PTR 144[rsp]
	lea	rdx, 0[rbp+r13]
	add	r10, r12
	cmp	r15, 1
	lea	rcx, [rdi+r10]
	je	.L41
	mov	r8, r15
	call	memcpy
	jmp	.L21
	.p2align 4,,10
	.p2align 3
.L15:
	call	_ZSt17__throw_bad_allocv
	.p2align 4,,10
	.p2align 3
.L24:
	mov	eax, 15
	jmp	.L12
	.p2align 4,,10
	.p2align 3
.L39:
	movzx	eax, BYTE PTR 0[rbp]
	test	r15, r15
	mov	rbp, QWORD PTR [rbx]
	mov	BYTE PTR [rcx], al
	je	.L21
	jmp	.L40
	.p2align 4,,10
	.p2align 3
.L41:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	jmp	.L21
.L37:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "basic_string::append\0"
	.text
	.p2align 4
	.globl	_Z13make_greetingB5cxx11PKc
	.def	_Z13make_greetingB5cxx11PKc;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13make_greetingB5cxx11PKc
_Z13make_greetingB5cxx11PKc:
.LFB2318:
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
	movabs	rax, 9223372036854775800
	cmp	rax, rsi
	jb	.L52
	lea	r12, 7[rsi]
	cmp	r12, 15
	ja	.L44
	test	rsi, rsi
	je	.L46
	cmp	rsi, 1
	je	.L53
	lea	rcx, 23[rbx]
	mov	r8, rsi
	mov	rdx, rdi
	call	memcpy
.L46:
	mov	rax, rbx
	mov	QWORD PTR 8[rbx], r12
	mov	BYTE PTR 7[rbp+rsi], 0
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
	.p2align 4,,10
	.p2align 3
.L44:
	mov	QWORD PTR 32[rsp], rsi
	mov	r9, rdi
	xor	r8d, r8d
	mov	edx, 7
	mov	rcx, rbx
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE9_M_mutateEyyPKcy
	mov	rbp, QWORD PTR [rbx]
	jmp	.L46
	.p2align 4,,10
	.p2align 3
.L53:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR 23[rbx], al
	jmp	.L46
.L52:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE0:
.L50:
	mov	rsi, rax
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2318:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2318-.LLSDACSB2318
.LLSDACSB2318:
	.uleb128 .LEHB0-.LFB2318
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L50-.LFB2318
	.uleb128 0
	.uleb128 .LEHB1-.LFB2318
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE2318:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC3:
	.ascii "world\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2357:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	call	__main
	movdqa	xmm0, XMMWORD PTR .LC2[rip]
	mov	ecx, 20
	mov	DWORD PTR 80[rsp], 5
	mov	QWORD PTR 48[rsp], 0
	movaps	XMMWORD PTR 64[rsp], xmm0
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 32[rsp], xmm0
.LEHB2:
	call	_Znwy
.LEHE2:
	lea	rsi, 20[rax]
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	mov	rax, QWORD PTR 64[rsp]
	lea	rdi, 64[rsp]
	mov	QWORD PTR 48[rsp], rsi
	lea	rdx, .LC3[rip]
	mov	rcx, rdi
	mov	QWORD PTR 40[rsp], rsi
	mov	QWORD PTR [rbx], rax
	mov	rax, QWORD PTR 72[rsp]
	mov	QWORD PTR 8[rbx], rax
	mov	eax, DWORD PTR 80[rsp]
	mov	DWORD PTR 16[rbx], eax
.LEHB3:
	call	_Z13make_greetingB5cxx11PKc
.LEHE3:
	mov	rdx, rbx
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L57:
	add	eax, DWORD PTR [rdx]
	add	rdx, 4
	cmp	rdx, rsi
	jne	.L57
	add	eax, DWORD PTR 72[rsp]
	mov	rcx, rdi
	mov	ebx, eax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	lea	rcx, 32[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	eax, ebx
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L60:
	lea	rcx, 32[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.L59:
	mov	rsi, rax
	mov	rcx, rbx
	mov	edx, 20
	call	_ZdlPvy
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE4:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2357:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2357-.LLSDACSB2357
.LLSDACSB2357:
	.uleb128 .LEHB2-.LFB2357
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L60-.LFB2357
	.uleb128 0
	.uleb128 .LEHB3-.LFB2357
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L59-.LFB2357
	.uleb128 0
	.uleb128 .LEHB4-.LFB2357
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE2357:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC2:
	.long	1
	.long	2
	.long	3
	.long	4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	strlen;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
