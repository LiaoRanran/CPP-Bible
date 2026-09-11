	.file	"_atom_sso_size.cpp"
	.intel_syntax noprefix
	.text
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
.LFB4085:
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
	ja	.L13
	test	rdx, rdx
	je	.L9
	mov	rcx, QWORD PTR [rcx]
	cmp	rdx, 1
	je	.L14
	movsx	edx, r8b
	mov	r8, rbx
	call	memset
.L9:
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rax+rbx], 0
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L13:
	movabs	rax, 9223372036854775806
	cmp	rax, rdx
	jb	.L15
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
	jmp	.L9
	.p2align 4,,10
	.p2align 3
.L14:
	mov	BYTE PTR [rcx], r8b
	jmp	.L9
.L15:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "sizeof(std::string)=\0"
.LC2:
	.ascii "\12\0"
.LC3:
	.ascii "empty capacity=\0"
.LC4:
	.ascii " (SSO buffer chars)\12\0"
.LC5:
	.ascii "len=15 allocs=\0"
.LC6:
	.ascii " len=16 allocs=\0"
	.section	.text.unlikely,"x"
.LCOLDB7:
	.section	.text.startup,"x"
.LHOTB7:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4077:
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
	lea	rsi, 48[rsp]
	lea	rbx, 80[rsp]
	mov	r8d, 120
	mov	edx, 15
	lea	rcx, 64[rsp]
	mov	QWORD PTR 32[rsp], rsi
	mov	QWORD PTR 40[rsp], 0
	mov	BYTE PTR 48[rsp], 0
	mov	DWORD PTR g_allocs[rip], 0
	mov	QWORD PTR 64[rsp], rbx
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	mov	rcx, QWORD PTR 64[rsp]
	cmp	rcx, rbx
	je	.L17
	call	free
.L17:
	mov	r8d, 120
	mov	edx, 16
	lea	rcx, 64[rsp]
	mov	ebp, DWORD PTR g_allocs[rip]
	mov	QWORD PTR 64[rsp], rbx
	mov	DWORD PTR g_allocs[rip], 0
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
	mov	rcx, QWORD PTR 64[rsp]
	cmp	rcx, rbx
	je	.L18
	call	free
.L18:
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC1[rip]
	mov	edi, DWORD PTR g_allocs[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 32
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC3[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 15
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC5[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, ebp
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, edi
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
.LEHE0:
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rsi
	je	.L23
	call	free
.L23:
	xor	eax, eax
	add	rsp, 104
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L22:
	mov	rbx, rax
	jmp	.L20
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
	.uleb128 .L22-.LFB4077
	.uleb128 0
.LLSDACSE4077:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	136
	.seh_savereg	rbx, 104
	.seh_savereg	rsi, 112
	.seh_savereg	rdi, 120
	.seh_savereg	rbp, 128
	.seh_endprologue
main.cold:
.L20:
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rsi
	jne	.L24
.L21:
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L24:
	call	free
	jmp	.L21
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC4077:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC4077-.LLSDACSBC4077
.LLSDACSBC4077:
	.uleb128 .LEHB1-.LCOLDB7
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC4077:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE7:
	.section	.text.startup,"x"
.LHOTE7:
	.globl	g_allocs
	.bss
	.align 4
g_allocs:
	.space 4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
