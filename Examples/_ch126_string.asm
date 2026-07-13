	.file	"_ch126_string.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "small=%s big_len=%zu\12\0"
	.text
	.p2align 4
	.def	_ZL6printfPKcz.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz.constprop.0
_ZL6printfPKcz.constprop.0:
.LFB2567:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	ecx, 1
	lea	rbx, 72[rsp]
	mov	QWORD PTR 72[rsp], rdx
	mov	QWORD PTR 80[rsp], r8
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 40[rsp], rbx
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	lea	rdx, .LC0[rip]
	mov	r8, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "basic_string::_M_create\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0:
.LFB2568:
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
	lea	rcx, .LC1[rip]
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
.LFB2284:
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
.LC2:
	.ascii "hello\0"
	.align 8
.LC3:
	.ascii "this string is clearly longer than fifteen bytes!!\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1951:
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
	lea	rsi, 32[rsp]
	lea	r8, .LC2[rip+5]
	mov	rcx, rsi
	lea	rax, 48[rsp]
	lea	rdx, -5[r8]
	mov	QWORD PTR 32[rsp], rax
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE0:
	lea	rdi, 64[rsp]
	lea	r8, .LC3[rip+50]
	mov	rcx, rdi
	lea	rax, 80[rsp]
	lea	rdx, -50[r8]
	mov	QWORD PTR 64[rsp], rax
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructIPKcEEvT_S8_St20forward_iterator_tag.isra.0
.LEHE1:
	mov	r8, QWORD PTR 72[rsp]
	lea	rcx, .LC0[rip]
	mov	rdx, QWORD PTR 32[rsp]
.LEHB2:
	call	_ZL6printfPKcz.constprop.0
.LEHE2:
	mov	rbx, QWORD PTR 72[rsp]
	mov	rcx, rdi
	add	ebx, DWORD PTR 40[rsp]
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	eax, ebx
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L21:
	mov	rbx, rax
	jmp	.L20
.L22:
	mov	rcx, rdi
	mov	rbx, rax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L20:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
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
	.uleb128 .L21-.LFB1951
	.uleb128 0
	.uleb128 .LEHB2-.LFB1951
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L22-.LFB1951
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
