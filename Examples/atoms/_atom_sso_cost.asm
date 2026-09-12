	.file	"_atom_sso_cost.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "basic_string::append\0"
.LC1:
	.ascii "basic_string::_M_create\0"
	.section	.text.unlikely,"x"
	.align 2
.LCOLDB2:
	.text
.LHOTB2:
	.align 2
	.p2align 4
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0:
.LFB6179:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	movabs	rax, 9223372036854775806
	mov	r9, r8
	mov	r8, QWORD PTR 8[rcx]
	mov	rbx, rcx
	mov	r10, rdx
	sub	rax, r8
	cmp	rax, r9
	jb	.L24
	mov	rdx, QWORD PTR [rcx]
	lea	r11, 16[rcx]
	lea	rsi, [r8+r9]
	cmp	rdx, r11
	je	.L28
	mov	rax, QWORD PTR 16[rcx]
	cmp	rax, rsi
	jb	.L5
.L4:
	test	r9, r9
	je	.L6
	lea	rcx, [rdx+r8]
	cmp	r9, 1
	je	.L29
	mov	rdx, r10
	mov	r8, r9
	call	memcpy
	mov	rdx, QWORD PTR [rbx]
.L6:
	mov	QWORD PTR 8[rbx], rsi
	mov	BYTE PTR [rdx+rsi], 0
	add	rsp, 64
	pop	rbx
	pop	rsi
	pop	rdi
	pop	r14
	pop	r15
	ret
.L28:
	mov	eax, 15
	cmp	rsi, 15
	jbe	.L4
.L5:
	movabs	rcx, 9223372036854775806
	cmp	rcx, rsi
	jb	.L25
	add	rax, rax
	mov	r14, rax
	cmp	rsi, rax
	jb	.L9
	lea	rcx, 1[rsi]
	mov	r14, rsi
.L10:
	mov	eax, DWORD PTR g_allocs[rip]
	mov	QWORD PTR 128[rsp], r9
	mov	QWORD PTR 120[rsp], r10
	add	eax, 1
	mov	QWORD PTR 48[rsp], r11
	mov	QWORD PTR 40[rsp], r8
	mov	QWORD PTR 56[rsp], rdx
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	r10, QWORD PTR 120[rsp]
	mov	r8, QWORD PTR 40[rsp]
	mov	r9, QWORD PTR 128[rsp]
	mov	rdi, rax
	mov	r11, QWORD PTR 48[rsp]
	test	r9, r9
	setne	al
	test	r10, r10
	setne	cl
	and	eax, ecx
	test	r8, r8
	mov	r15d, eax
	je	.L11
	cmp	r8, 1
	mov	rdx, QWORD PTR 56[rsp]
	je	.L30
	mov	rcx, rdi
	mov	QWORD PTR 128[rsp], r9
	mov	QWORD PTR 120[rsp], r10
	mov	QWORD PTR 48[rsp], r11
	mov	QWORD PTR 40[rsp], r8
	call	memcpy
	mov	r10, QWORD PTR 120[rsp]
	mov	r11, QWORD PTR 48[rsp]
	mov	r9, QWORD PTR 128[rsp]
	mov	r8, QWORD PTR 40[rsp]
.L13:
	test	r15b, r15b
	je	.L15
	lea	rcx, [rdi+r8]
	cmp	r9, 1
	jne	.L16
	movzx	eax, BYTE PTR [r10]
	mov	BYTE PTR [rcx], al
.L15:
	mov	rcx, QWORD PTR [rbx]
	cmp	r11, rcx
	je	.L17
	call	free
.L17:
	mov	QWORD PTR [rbx], rdi
	mov	rdx, rdi
	mov	QWORD PTR 16[rbx], r14
	jmp	.L6
.L9:
	cmp	rcx, rax
	jnb	.L31
	mov	r14, rcx
	movabs	rcx, 9223372036854775807
	jmp	.L10
.L11:
	test	al, al
	je	.L15
	mov	rcx, rdi
.L16:
	mov	r8, r9
	mov	rdx, r10
	mov	QWORD PTR 40[rsp], r11
	call	memcpy
	mov	r11, QWORD PTR 40[rsp]
	jmp	.L15
.L29:
	movzx	eax, BYTE PTR [r10]
	mov	BYTE PTR [rcx], al
	mov	rdx, QWORD PTR [rbx]
	jmp	.L6
.L30:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rdi], al
	jmp	.L13
.L31:
	lea	rcx, 1[rax]
	jmp	.L10
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0.cold
	.seh_stackalloc	104
	.seh_savereg	rbx, 64
	.seh_savereg	rsi, 72
	.seh_savereg	rdi, 80
	.seh_savereg	r14, 88
	.seh_savereg	r15, 96
	.seh_endprologue
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0.cold:
.L24:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.L25:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.text
.LHOTE2:
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB4074:
	.seh_endprologue
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB4075:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB4076:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc:
.LFB4084:
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
	ja	.L43
	test	rdx, rdx
	je	.L39
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, 1
	je	.L44
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
.L39:
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rax+rbx], 0
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L43:
	movabs	rax, 9223372036854775806
	cmp	rax, rdx
	jb	.L45
	mov	eax, DWORD PTR g_allocs[rip]
	lea	rcx, 1[rdx]
	mov	DWORD PTR 44[rsp], r8d
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	r8d, DWORD PTR 44[rsp]
	mov	QWORD PTR 16[rsi], rbx
	mov	QWORD PTR [rsi], rax
	mov	rcx, rax
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
	jmp	.L39
	.p2align 4,,10
	.p2align 3
.L44:
	mov	BYTE PTR [rcx], r8b
	jmp	.L39
.L45:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy:
.LFB4473:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	mov	rsi, rcx
	mov	rbx, r8
	cmp	r8, 15
	ja	.L51
	mov	rcx, QWORD PTR [rcx]
	lea	r8, 1[r8]
	test	rbx, rbx
	je	.L52
.L49:
	call	memcpy
	mov	QWORD PTR 8[rsi], rbx
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L52:
	movzx	eax, BYTE PTR [rdx]
	mov	BYTE PTR [rcx], al
	mov	QWORD PTR 8[rsi], rbx
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L51:
	movabs	rax, 9223372036854775806
	cmp	rax, r8
	jb	.L53
	mov	eax, DWORD PTR g_allocs[rip]
	lea	r8, 1[r8]
	mov	QWORD PTR 88[rsp], rdx
	mov	rcx, r8
	mov	QWORD PTR 40[rsp], r8
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	QWORD PTR 16[rsi], rbx
	mov	r8, QWORD PTR 40[rsp]
	mov	QWORD PTR [rsi], rax
	mov	rdx, QWORD PTR 88[rsp]
	mov	rcx, rax
	jmp	.L49
.L53:
	lea	rcx, .LC1[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC3:
	.ascii "copy short(len=10): allocs=\0"
.LC4:
	.ascii "\12\0"
.LC5:
	.ascii "copy long (len=100): allocs=\0"
.LC6:
	.ascii "assign long: allocs=\0"
.LC7:
	.ascii "concat 10+10=20chars: allocs=\0"
	.section	.text.unlikely,"x"
.LCOLDB8:
	.section	.text.startup,"x"
.LHOTB8:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4077:
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
	sub	rsp, 184
	.seh_stackalloc	184
	.seh_endprologue
	call	__main
	lea	rdi, 96[rsp]
	lea	rcx, 80[rsp]
	mov	r8d, 97
	mov	edx, 10
	mov	QWORD PTR 80[rsp], rdi
	lea	rbp, 128[rsp]
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE0:
	lea	rcx, 112[rsp]
	mov	r8d, 98
	mov	edx, 100
	mov	QWORD PTR 112[rsp], rbp
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE1:
	lea	rsi, 144[rsp]
	mov	r8, QWORD PTR 88[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	lea	rbx, 160[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 144[rsp], rbx
	mov	r15d, DWORD PTR g_allocs[rip]
.LEHB2:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rbx
	je	.L55
	call	free
.L55:
	mov	eax, DWORD PTR g_allocs[rip]
	mov	r8, QWORD PTR 120[rsp]
	mov	rcx, rsi
	mov	QWORD PTR 144[rsp], rbx
	mov	rdx, QWORD PTR 112[rsp]
	mov	DWORD PTR 44[rsp], eax
	mov	eax, DWORD PTR g_allocs[rip]
	mov	DWORD PTR 52[rsp], eax
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructILb1EEEvPKcy
.LEHE2:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rbx
	je	.L56
	call	free
.L56:
	mov	eax, DWORD PTR g_allocs[rip]
	mov	r13, QWORD PTR 120[rsp]
	mov	QWORD PTR 144[rsp], rbx
	mov	QWORD PTR 152[rsp], 0
	mov	DWORD PTR 48[rsp], eax
	mov	eax, DWORD PTR g_allocs[rip]
	mov	BYTE PTR 160[rsp], 0
	mov	DWORD PTR 56[rsp], eax
	cmp	r13, 15
	ja	.L92
	test	r13, r13
	jne	.L93
.L60:
	mov	rax, QWORD PTR 144[rsp]
	mov	BYTE PTR [rax+r13], 0
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rbx
	je	.L61
	call	free
.L61:
	mov	r13, QWORD PTR 88[rsp]
	mov	r14d, DWORD PTR g_allocs[rip]
	mov	QWORD PTR 144[rsp], rbx
	mov	eax, DWORD PTR g_allocs[rip]
	mov	BYTE PTR 160[rsp], 0
	lea	rdx, [r13+r13]
	mov	r12, QWORD PTR 80[rsp]
	mov	QWORD PTR 152[rsp], 0
	mov	DWORD PTR 60[rsp], eax
	cmp	rdx, 15
	ja	.L94
.L62:
	mov	r8, r13
	mov	rdx, r12
	mov	rcx, rsi
.LEHB3:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0
	mov	r8, r13
	mov	rdx, r12
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6appendEPKcy.isra.0
.LEHE3:
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rbx
	je	.L70
	call	free
.L70:
	mov	ebx, DWORD PTR 44[rsp]
	lea	rdx, .LC3[rip]
	mov	esi, DWORD PTR 48[rsp]
	mov	r12, QWORD PTR .refptr._ZSt4cout[rip]
	mov	r13d, DWORD PTR g_allocs[rip]
	sub	ebx, r15d
	sub	esi, DWORD PTR 52[rsp]
	sub	r14d, DWORD PTR 56[rsp]
	mov	rcx, r12
	sub	r13d, DWORD PTR 60[rsp]
.LEHB4:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebx
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC5[rip]
	mov	rcx, r12
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, esi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC6[rip]
	mov	rcx, r12
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r14d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC7[rip]
	mov	rcx, r12
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, r13d
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE4:
	mov	rcx, QWORD PTR 112[rsp]
	cmp	rcx, rbp
	je	.L71
	call	free
.L71:
	mov	rcx, QWORD PTR 80[rsp]
	cmp	rcx, rdi
	je	.L83
	call	free
.L83:
	xor	eax, eax
	add	rsp, 184
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L94:
	movabs	rax, 9223372036854775806
	cmp	rax, rdx
	jb	.L90
	lea	rcx, 1[rdx]
	cmp	rdx, 29
	jbe	.L95
.L64:
	mov	eax, DWORD PTR g_allocs[rip]
	mov	QWORD PTR 64[rsp], rdx
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	rdx, QWORD PTR 64[rsp]
	mov	BYTE PTR [rax], 0
	mov	rcx, QWORD PTR 144[rsp]
	cmp	rcx, rbx
	je	.L65
	mov	QWORD PTR 72[rsp], rax
	call	free
	mov	rax, QWORD PTR 72[rsp]
	mov	rdx, QWORD PTR 64[rsp]
.L65:
	mov	QWORD PTR 144[rsp], rax
	mov	QWORD PTR 160[rsp], rdx
	jmp	.L62
.L93:
	cmp	r13, 1
	je	.L60
	mov	rdx, QWORD PTR 112[rsp]
	mov	rcx, rbx
.L59:
	mov	r8, r13
	call	memcpy
	jmp	.L60
.L95:
	mov	edx, 30
	mov	ecx, 31
	jmp	.L64
.L92:
	cmp	r13, 29
	jbe	.L76
	lea	rcx, 1[r13]
	mov	r12, r13
.L58:
	mov	eax, DWORD PTR g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR g_allocs[rip], eax
	call	malloc
	mov	QWORD PTR 160[rsp], r12
	mov	rdx, QWORD PTR 112[rsp]
	mov	QWORD PTR 144[rsp], rax
	mov	rcx, rax
	jmp	.L59
.L76:
	mov	r12d, 30
	mov	ecx, 31
	jmp	.L58
.L78:
	mov	rbx, rax
	jmp	.L74
.L88:
	jmp	.L89
.L79:
	mov	rbx, rax
	jmp	.L69
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4077:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4077-.LLSDACSB4077
.LLSDACSB4077:
	.uleb128 .LEHB0-.LFB4077
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB4077
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L78-.LFB4077
	.uleb128 0
	.uleb128 .LEHB2-.LFB4077
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L79-.LFB4077
	.uleb128 0
	.uleb128 .LEHB3-.LFB4077
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L88-.LFB4077
	.uleb128 0
	.uleb128 .LEHB4-.LFB4077
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L79-.LFB4077
	.uleb128 0
.LLSDACSE4077:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	248
	.seh_savereg	rbx, 184
	.seh_savereg	rsi, 192
	.seh_savereg	rdi, 200
	.seh_savereg	rbp, 208
	.seh_savereg	r12, 216
	.seh_savereg	r13, 224
	.seh_savereg	r14, 232
	.seh_savereg	r15, 240
	.seh_endprologue
main.cold:
.L90:
	lea	rcx, .LC1[rip]
.LEHB5:
	call	_ZSt20__throw_length_errorPKc
.LEHE5:
.L80:
.L89:
	mov	rcx, QWORD PTR 144[rsp]
	mov	rsi, rax
	cmp	rcx, rbx
	je	.L68
	call	free
.L68:
	mov	rbx, rsi
.L69:
	mov	rcx, QWORD PTR 112[rsp]
	cmp	rcx, rbp
	jne	.L96
.L74:
	mov	rcx, QWORD PTR 80[rsp]
	cmp	rcx, rdi
	je	.L75
	call	free
.L75:
	mov	rcx, rbx
.LEHB6:
	call	_Unwind_Resume
.LEHE6:
.L96:
	call	free
	jmp	.L74
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4077:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4077-.LLSDACSBC4077
.LLSDACSBC4077:
	.uleb128 .LEHB5-.LCOLDB8
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L80-.LCOLDB8
	.uleb128 0
	.uleb128 .LEHB6-.LCOLDB8
	.uleb128 .LEHE6-.LEHB6
	.uleb128 0
	.uleb128 0
.LLSDACSEC4077:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE8:
	.section	.text.startup,"x"
.LHOTE8:
	.globl	g_allocs
	.bss
	.align 4
g_allocs:
	.space 4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
