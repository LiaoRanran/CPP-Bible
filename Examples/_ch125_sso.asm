	.file	"_ch125_sso.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL6printfPKcz;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz
_ZL6printfPKcz:
.LFB367:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::_M_create\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0:
.LFB2569:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, r8
	mov	rsi, rcx
	mov	rdi, rdx
	sub	rbx, rdx
	cmp	rbx, 15
	ja	.L13
	mov	rdx, QWORD PTR [rcx]
	cmp	rbx, 1
	mov	rcx, rdx
	jne	.L8
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR [rdx], al
	mov	rdx, QWORD PTR [rsi]
.L9:
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rdx+rbx], 0
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L8:
	test	rbx, rbx
	je	.L9
.L7:
	mov	rdx, rdi
	mov	r8, rbx
	call	memcpy
	mov	rdx, QWORD PTR [rsi]
	jmp	.L9
.L13:
	test	rbx, rbx
	js	.L14
	mov	rcx, rbx
	add	rcx, 1
	js	.L15
	call	_Znwy
	mov	QWORD PTR 16[rsi], rbx
	mov	rcx, rax
	mov	QWORD PTR [rsi], rax
	jmp	.L7
.L15:
	call	_ZSt17__throw_bad_allocv
.L14:
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
.LFB2286:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L16
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L16:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "hello\0"
	.align 8
.LC2:
	.ascii "this string is definitely longer than the sso buffer\0"
.LC3:
	.ascii "a.cap=%zu b.cap=%zu size=%zu\12\0"
.LC4:
	.ascii "a.cap_after_reserve=%zu\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1951:
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
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	lea	rbp, 32[rsp]
	lea	r8, .LC1[rip+5]
	mov	rcx, rbp
	lea	rdx, -5[r8]
	lea	rsi, 48[rsp]
	mov	QWORD PTR 32[rsp], rsi
	lea	rdi, 64[rsp]
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE0:
	lea	r8, .LC2[rip+52]
	mov	rcx, rdi
	lea	rbx, 80[rsp]
	lea	rdx, -52[r8]
	mov	QWORD PTR 64[rsp], rbx
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE1:
	cmp	QWORD PTR 64[rsp], rbx
	je	.L29
	mov	r8, QWORD PTR 80[rsp]
.L19:
	cmp	QWORD PTR 32[rsp], rsi
	je	.L30
	mov	rdx, QWORD PTR 48[rsp]
.L20:
	lea	rcx, .LC3[rip]
	mov	r9d, 32
.LEHB2:
	call	_ZL6printfPKcz
	cmp	QWORD PTR 32[rsp], rsi
	je	.L31
	mov	rdx, QWORD PTR 48[rsp]
	cmp	rdx, 63
	mov	rax, rdx
	jbe	.L21
.L22:
	lea	rcx, .LC4[rip]
	call	_ZL6printfPKcz
	mov	rcx, rdi
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
	pop	r13
	ret
.L31:
	mov	eax, 15
.L21:
	add	rax, rax
	mov	edx, 64
	cmp	rax, rdx
	mov	rbx, rdx
	cmovnb	rbx, rax
	lea	rcx, 1[rbx]
	call	_Znwy
.LEHE2:
	mov	r12, rax
	mov	rax, QWORD PTR 40[rsp]
	mov	r13, QWORD PTR 32[rsp]
	lea	r8, 1[rax]
	test	rax, rax
	je	.L39
	test	r8, r8
	jne	.L40
.L24:
	cmp	r13, rsi
	je	.L25
	mov	rax, QWORD PTR 48[rsp]
	mov	rcx, r13
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L25:
	mov	QWORD PTR 32[rsp], r12
	mov	rdx, rbx
	mov	QWORD PTR 48[rsp], rbx
	jmp	.L22
.L40:
	mov	rdx, r13
	mov	rcx, r12
	call	memcpy
	jmp	.L24
.L29:
	mov	r8d, 15
	jmp	.L19
.L30:
	mov	edx, 15
	jmp	.L20
.L39:
	movzx	eax, BYTE PTR 0[r13]
	mov	BYTE PTR [r12], al
	jmp	.L24
.L33:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L27:
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
.LEHE3:
.L32:
	mov	rbx, rax
	jmp	.L27
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1951:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1951-.LLSDACSB1951
.LLSDACSB1951:
	.uleb128 .LEHB0-.LFB1951
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1951
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L32-.LFB1951
	.uleb128 0
	.uleb128 .LEHB2-.LFB1951
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L33-.LFB1951
	.uleb128 0
	.uleb128 .LEHB3-.LFB1951
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE1951:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
