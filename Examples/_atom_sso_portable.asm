	.file	"_atom_sso_portable.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_create\0"
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc:
.LFB2020:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rsi, rcx
	mov	rbx, rdx
	cmp	rdx, 15
	ja	.L10
	test	rdx, rdx
	je	.L5
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, 1
	je	.L11
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
.L5:
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rax+rbx], 0
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	movabs	rax, 9223372036854775806
	cmp	rax, rdx
	jb	.L12
	lea	rcx, 1[rdx]
	mov	DWORD PTR 44[rsp], r8d
	call	_Znwy
	mov	r8d, DWORD PTR 44[rsp]
	mov	QWORD PTR 16[rsi], rbx
	mov	QWORD PTR [rsi], rax
	mov	rcx, rax
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L11:
	mov	BYTE PTR [rcx], r8b
	jmp	.L5
.L12:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:
.LFB2316:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L13
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L13:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "sizeof_string=%zu\12\0"
.LC2:
	.ascii "sizeof_size_t=%zu\12\0"
.LC3:
	.ascii "capacity_at_len1=%zu\12\0"
.LC4:
	.ascii "capacity_at_len8=%zu\12\0"
.LC5:
	.ascii "first_heap_len=%zu\12\0"
.LC6:
	.ascii "sso_capacity=%zu\12\0"
.LC7:
	.ascii "heap_at_len%zu=%d\12\0"
.LC8:
	.ascii "capacity_at_sso_capacity=%zu\12\0"
.LC9:
	.ascii "size_at_sso_capacity=%zu\12\0"
	.align 8
.LC10:
	.ascii "heap_at_sso_capacity_plus8=%d\12\0"
	.section	.text.unlikely,"x"
.LCOLDB11:
	.section	.text.startup,"x"
.LHOTB11:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2006:
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
	add	rsp, -128
	.seh_stackalloc	128
	.seh_endprologue
	call	__main
	lea	rbx, 48[rsp]
	mov	edx, 32
	lea	rcx, .LC1[rip]
	mov	QWORD PTR 32[rsp], rbx
	mov	QWORD PTR 40[rsp], 0
	mov	BYTE PTR 48[rsp], 0
.LEHB0:
	call	__mingw_printf
	mov	edx, 8
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	mov	rax, QWORD PTR 32[rsp]
	mov	edx, 15
	lea	rcx, .LC3[rip]
	mov	BYTE PTR [rax], 97
	mov	rax, QWORD PTR 32[rsp]
	mov	QWORD PTR 40[rsp], 1
	mov	BYTE PTR 1[rax], 0
	cmp	QWORD PTR 32[rsp], rbx
	cmovne	rdx, QWORD PTR 48[rsp]
	call	__mingw_printf
	lea	rbp, 96[rsp]
	lea	rsi, 112[rsp]
	mov	r8d, 97
	mov	edx, 8
	mov	rcx, rbp
	mov	QWORD PTR 96[rsp], rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE0:
	cmp	QWORD PTR 96[rsp], rsi
	mov	edx, 15
	cmovne	rdx, QWORD PTR 112[rsp]
	lea	rcx, .LC4[rip]
.LEHB1:
	call	__mingw_printf
.LEHE1:
	mov	rcx, rbp
	mov	ebx, 1
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L21:
	mov	r8d, 120
	mov	rdx, rbx
	mov	rcx, rbp
	mov	QWORD PTR 96[rsp], rsi
.LEHB2:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	mov	rax, QWORD PTR 96[rsp]
	mov	rcx, rbp
	cmp	rax, rbp
	jb	.L49
	lea	rdi, 128[rsp]
	cmp	rax, rdi
	jb	.L18
.L49:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	eax, 1
.L20:
	mov	r14, rbx
	mov	rdx, rbx
	lea	rcx, .LC5[rip]
	sub	r14, rax
	call	__mingw_printf
	mov	rdx, r14
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	mov	ebx, 2
	lea	r13, 2[r14]
	cmp	r14, rbx
	cmovnb	rbx, r14
	sub	rbx, 1
	cmp	r13, rbx
	jb	.L32
	mov	QWORD PTR 96[rsp], rsi
	cmp	rbx, 15
	ja	.L33
	cmp	rbx, 1
	jne	.L42
	mov	BYTE PTR 112[rsp], 120
	mov	rax, rsi
	lea	r12, .LC7[rip]
	jmp	.L26
	.p2align 4,,10
	.p2align 3
.L33:
	lea	rcx, 1[rbx]
	call	_Znwy
.LEHE2:
	mov	QWORD PTR 96[rsp], rax
	mov	rdx, rax
	lea	r12, .LC7[rip]
	mov	QWORD PTR 112[rsp], rbx
	jmp	.L25
	.p2align 4,,10
	.p2align 3
.L62:
	test	bl, 4
	jne	.L60
	test	ebx, ebx
	je	.L28
	mov	BYTE PTR [rdx], 120
	test	bl, 2
	jne	.L61
.L28:
	mov	rax, QWORD PTR 96[rsp]
.L26:
	mov	QWORD PTR 104[rsp], rbx
	lea	rdi, 128[rsp]
	mov	rdx, rbx
	mov	rcx, r12
	mov	BYTE PTR [rax+rbx], 0
	mov	rax, QWORD PTR 96[rsp]
	cmp	rax, rdi
	setb	r8b
	cmp	rax, rbp
	setnb	al
	and	r8d, eax
	xor	r8d, 1
	and	r8d, 1
.LEHB3:
	call	__mingw_printf
.LEHE3:
	mov	rcx, QWORD PTR 96[rsp]
	cmp	rcx, rsi
	je	.L31
	mov	rax, QWORD PTR 112[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L31:
	add	rbx, 1
	cmp	r13, rbx
	jb	.L32
	mov	QWORD PTR 96[rsp], rsi
	lea	rsi, 112[rsp]
	mov	rdx, rsi
	cmp	rbx, 15
	ja	.L33
.L25:
	movabs	rax, 8680820740569200760
	mov	ecx, ebx
	cmp	ebx, 8
	jb	.L62
	lea	rdi, 8[rdx]
	mov	ecx, ebx
	mov	QWORD PTR [rdx], rax
	and	rdi, -8
	mov	QWORD PTR -8[rdx+rcx], rax
	sub	rdx, rdi
	lea	ecx, [rbx+rdx]
	shr	ecx, 3
	rep stosq
	jmp	.L28
	.p2align 4,,10
	.p2align 3
.L32:
	lea	rdi, 80[rsp]
	mov	r8d, 121
	mov	rdx, r14
	lea	rcx, 64[rsp]
	mov	QWORD PTR 64[rsp], rdi
.LEHB4:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE4:
	cmp	QWORD PTR 64[rsp], rdi
	mov	edx, 15
	cmovne	rdx, QWORD PTR 80[rsp]
	lea	rcx, .LC8[rip]
.LEHB5:
	call	__mingw_printf
	mov	rdx, QWORD PTR 72[rsp]
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	lea	rdx, 8[r14]
	mov	r8d, 122
	mov	rcx, rbp
	mov	QWORD PTR 96[rsp], rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE5:
	mov	rax, QWORD PTR 96[rsp]
	lea	rdi, 128[rsp]
	lea	rcx, .LC10[rip]
	cmp	rax, rdi
	setb	dl
	cmp	rax, rbp
	setnb	al
	and	edx, eax
	xor	edx, 1
	movzx	edx, dl
.LEHB6:
	call	__mingw_printf
.LEHE6:
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	lea	rcx, 64[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	lea	rcx, 32[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	sub	rsp, -128
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	ret
.L18:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	add	rbx, 1
	cmp	rbx, 65
	jne	.L21
	xor	eax, eax
	xor	ebx, ebx
	jmp	.L20
.L42:
	mov	rdx, rsi
	lea	r12, .LC7[rip]
	jmp	.L25
.L60:
	mov	DWORD PTR [rdx], 2021161080
	mov	DWORD PTR -4[rdx+rcx], 2021161080
	jmp	.L28
.L61:
	mov	WORD PTR -2[rdx+rcx], 30840
	jmp	.L28
.L46:
	mov	rbx, rax
	jmp	.L37
.L45:
	mov	rbx, rax
	jmp	.L35
.L48:
	mov	rsi, rax
	jmp	.L38
.L44:
	mov	rbx, rax
	jmp	.L36
.L47:
	mov	rsi, rax
	jmp	.L39
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2006:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2006-.LLSDACSB2006
.LLSDACSB2006:
	.uleb128 .LEHB0-.LFB2006
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L44-.LFB2006
	.uleb128 0
	.uleb128 .LEHB1-.LFB2006
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L45-.LFB2006
	.uleb128 0
	.uleb128 .LEHB2-.LFB2006
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L44-.LFB2006
	.uleb128 0
	.uleb128 .LEHB3-.LFB2006
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L46-.LFB2006
	.uleb128 0
	.uleb128 .LEHB4-.LFB2006
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L44-.LFB2006
	.uleb128 0
	.uleb128 .LEHB5-.LFB2006
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L47-.LFB2006
	.uleb128 0
	.uleb128 .LEHB6-.LFB2006
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L48-.LFB2006
	.uleb128 0
.LLSDACSE2006:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	184
	.seh_savereg	rbx, 128
	.seh_savereg	rsi, 136
	.seh_savereg	rdi, 144
	.seh_savereg	rbp, 152
	.seh_savereg	r12, 160
	.seh_savereg	r13, 168
	.seh_savereg	r14, 176
	.seh_endprologue
main.cold:
.L37:
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L36:
	lea	rcx, 32[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB7:
	call	_Unwind_Resume
.LEHE7:
.L35:
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L36
.L38:
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L39:
	lea	rcx, 64[rsp]
	mov	rbx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	jmp	.L36
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2006:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2006-.LLSDACSBC2006
.LLSDACSBC2006:
	.uleb128 .LEHB7-.LCOLDB11
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0
	.uleb128 0
.LLSDACSEC2006:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE11:
	.section	.text.startup,"x"
.LHOTE11:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
