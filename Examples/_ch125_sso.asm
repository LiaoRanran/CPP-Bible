	.file	"_ch125_sso.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_create\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB1:
	.text
.LHOTB1:
	.align 2
	.p2align 4
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0:
.LFB2593:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	sub	r8, rdx
	mov	rbx, rcx
	cmp	r8, 15
	ja	.L12
	mov	r9, QWORD PTR [rcx]
	mov	rcx, r9
	cmp	r8, 1
	je	.L13
	test	r8, r8
	jne	.L4
.L6:
	mov	QWORD PTR 8[rbx], r8
	mov	BYTE PTR [r9+r8], 0
	add	rsp, 48
	pop	rbx
	ret
.L13:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [r9], al
	mov	r9, QWORD PTR [rbx]
	jmp	.L6
.L12:
	movabs	rax, 9223372036854775806
	cmp	rax, r8
	jb	.L10
	lea	rcx, 1[r8]
	mov	QWORD PTR 72[rsp], rdx
	mov	QWORD PTR 40[rsp], r8
	call	_Znwy
	mov	r8, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 72[rsp]
	mov	QWORD PTR [rbx], rax
	mov	rcx, rax
	mov	QWORD PTR 16[rbx], r8
.L4:
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r9, QWORD PTR [rbx]
	mov	r8, QWORD PTR 40[rsp]
	jmp	.L6
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0.cold
	.seh_stackalloc	56
	.seh_savereg	rbx, 48
	.seh_endprologue
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0.cold:
.L10:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv:
.LFB2303:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L14
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L14:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "hello\0"
	.align 8
.LC3:
	.ascii "this string is definitely longer than the sso buffer\0"
.LC4:
	.ascii "a.cap=%zu b.cap=%zu size=%zu\12\0"
.LC5:
	.ascii "a.cap_after_reserve=%zu\12\0"
	.section	.text.unlikely,"x"
.LCOLDB6:
	.section	.text.startup,"x"
.LHOTB6:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2004:
	push	r14
	.seh_pushreg	r14
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
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	lea	rbp, 32[rsp]
	lea	rbx, 48[rsp]
	lea	rdx, .LC2[rip]
	mov	rcx, rbp
	mov	QWORD PTR 32[rsp], rbx
	lea	rsi, 80[rsp]
	lea	r8, 5[rdx]
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE0:
	lea	rcx, 64[rsp]
	mov	QWORD PTR 64[rsp], rsi
	lea	rdx, .LC3[rip]
	lea	r8, 52[rdx]
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE1:
	mov	edx, 15
	cmp	QWORD PTR 64[rsp], rsi
	mov	r9d, 32
	mov	r8, rdx
	cmovne	r8, QWORD PTR 80[rsp]
	cmp	QWORD PTR 32[rsp], rbx
	cmovne	rdx, QWORD PTR 48[rsp]
	lea	rcx, .LC4[rip]
.LEHB2:
	call	__mingw_printf
	mov	rdi, QWORD PTR 32[rsp]
	cmp	rdi, rbx
	je	.L30
	mov	rsi, QWORD PTR 48[rsp]
	cmp	rsi, 63
	jbe	.L35
.L20:
	mov	rdx, rsi
	lea	rcx, .LC5[rip]
	call	__mingw_printf
	lea	rcx, 64[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r14
	ret
.L30:
	mov	esi, 64
	mov	ecx, 65
.L19:
	call	_Znwy
.LEHE2:
	mov	r14, rax
	mov	rax, QWORD PTR 40[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L36
	mov	rdx, rdi
	mov	rcx, r14
	call	memcpy
	cmp	rdi, rbx
	je	.L23
.L22:
	mov	rax, QWORD PTR 48[rsp]
	mov	rcx, rdi
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L23:
	mov	QWORD PTR 32[rsp], r14
	mov	QWORD PTR 48[rsp], rsi
	jmp	.L20
.L36:
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR [r14], al
	cmp	rdi, rbx
	jne	.L22
	jmp	.L23
.L35:
	add	rsi, rsi
	cmp	rsi, 64
	jbe	.L30
	lea	rcx, 1[rsi]
	jmp	.L19
.L31:
	mov	rbx, rax
	jmp	.L26
.L32:
	mov	rbx, rax
	jmp	.L25
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2004:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2004-.LLSDACSB2004
.LLSDACSB2004:
	.uleb128 .LEHB0-.LFB2004
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB2004
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L31-.LFB2004
	.uleb128 0
	.uleb128 .LEHB2-.LFB2004
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L32-.LFB2004
	.uleb128 0
.LLSDACSE2004:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	152
	.seh_savereg	rbx, 104
	.seh_savereg	rsi, 112
	.seh_savereg	rdi, 120
	.seh_savereg	rbp, 128
	.seh_savereg	r12, 136
	.seh_savereg	r14, 144
	.seh_endprologue
main.cold:
.L25:
	lea	rcx, 64[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L26:
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2004:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2004-.LLSDACSBC2004
.LLSDACSBC2004:
	.uleb128 .LEHB3-.LCOLDB6
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC2004:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE6:
	.section	.text.startup,"x"
.LHOTE6:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
