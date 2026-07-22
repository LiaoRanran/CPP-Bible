	.file	"_ch126_string.cpp"
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
	.ascii "this string is clearly longer than fifteen bytes!!\0"
.LC4:
	.ascii "small=%s big_len=%zu\12\0"
	.section	.text.unlikely,"x"
.LCOLDB5:
	.section	.text.startup,"x"
.LHOTB5:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2004:
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
	lea	rax, 48[rsp]
	lea	rcx, 32[rsp]
	lea	rdx, .LC2[rip]
	mov	QWORD PTR 32[rsp], rax
	lea	r8, 5[rdx]
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE0:
	lea	rax, 80[rsp]
	lea	rcx, 64[rsp]
	lea	rdx, .LC3[rip]
	mov	QWORD PTR 64[rsp], rax
	lea	r8, 50[rdx]
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE1:
	mov	r8, QWORD PTR 72[rsp]
	mov	rdx, QWORD PTR 32[rsp]
	lea	rcx, .LC4[rip]
.LEHB2:
	call	__mingw_printf
.LEHE2:
	lea	rcx, 64[rsp]
	mov	rbx, QWORD PTR 72[rsp]
	add	ebx, DWORD PTR 40[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	lea	rcx, 32[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	eax, ebx
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L19:
	mov	rbx, rax
	jmp	.L18
.L20:
	mov	rbx, rax
	jmp	.L17
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
	.uleb128 .L19-.LFB2004
	.uleb128 0
	.uleb128 .LEHB2-.LFB2004
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L20-.LFB2004
	.uleb128 0
.LLSDACSE2004:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	120
	.seh_savereg	rbx, 96
	.seh_savereg	rsi, 104
	.seh_savereg	rdi, 112
	.seh_endprologue
main.cold:
.L17:
	lea	rcx, 64[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L18:
	lea	rcx, 32[rsp]
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
	.uleb128 .LEHB3-.LCOLDB5
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSEC2004:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE5:
	.section	.text.startup,"x"
.LHOTE5:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
