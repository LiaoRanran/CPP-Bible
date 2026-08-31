	.file	"s.cpp"
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
.LFB2600:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	cmp	rdx, 15
	mov	rsi, rcx
	mov	rbx, rdx
	mov	edi, r8d
	ja	.L11
	test	rdx, rdx
	jne	.L12
.L6:
	mov	rax, QWORD PTR [rsi]
	mov	QWORD PTR 8[rsi], rbx
	mov	BYTE PTR [rax+rbx], 0
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L11:
	test	rdx, rdx
	js	.L13
	mov	rcx, rdx
	add	rcx, 1
	js	.L14
	call	_Znwy
	mov	QWORD PTR 16[rsi], rbx
	mov	rcx, rax
	mov	QWORD PTR [rsi], rax
.L5:
	movsx	edx, dil
	mov	r8, rbx
	call	memset
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L12:
	cmp	rdx, 1
	mov	rcx, QWORD PTR [rcx]
	jne	.L5
	mov	BYTE PTR [rcx], r8b
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L14:
	call	_ZSt17__throw_bad_allocv
.L13:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_
	.def	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_
_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_:
.LFB2611:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rsi, QWORD PTR 8[rdx]
	mov	rbx, rcx
	cmp	rsi, 15
	lea	rcx, 16[rcx]
	mov	QWORD PTR [rbx], rcx
	mov	rdi, QWORD PTR [rdx]
	ja	.L26
	cmp	rsi, 1
	jne	.L20
	movzx	eax, BYTE PTR [rdi]
	mov	BYTE PTR 16[rbx], al
.L21:
	mov	QWORD PTR 8[rbx], rsi
	mov	BYTE PTR [rcx+rsi], 0
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L20:
	test	rsi, rsi
	je	.L21
	mov	r8, rsi
	mov	rdx, rdi
	call	memcpy
	mov	rcx, QWORD PTR [rbx]
.L29:
	mov	QWORD PTR 8[rbx], rsi
	mov	BYTE PTR [rcx+rsi], 0
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L26:
	test	rsi, rsi
	js	.L27
	mov	rcx, rsi
	add	rcx, 1
	js	.L28
	call	_Znwy
	mov	QWORD PTR 16[rbx], rsi
	mov	r8, rsi
	mov	rdx, rdi
	mov	rcx, rax
	mov	QWORD PTR [rbx], rax
	call	memcpy
	mov	rcx, QWORD PTR [rbx]
	jmp	.L29
	.p2align 4,,10
	.p2align 3
.L28:
	call	_ZSt17__throw_bad_allocv
.L27:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_
	.def	_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_
_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_:
.LFB2621:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	xor	eax, eax
	mov	r8, QWORD PTR 8[rcx]
	cmp	r8, QWORD PTR 8[rdx]
	je	.L35
.L30:
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L35:
	test	r8, r8
	mov	eax, 1
	je	.L30
	mov	rdx, QWORD PTR [rdx]
	mov	rcx, QWORD PTR [rcx]
	call	memcmp
	test	eax, eax
	sete	al
	add	rsp, 40
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
.LFB2940:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	lea	rdx, 16[rcx]
	cmp	rax, rdx
	je	.L36
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	add	rdx, 1
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L36:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC1:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmpmkwgkloz\\s.cpp\0"
.LC2:
	.ascii "c == a && d == b\0"
.LC3:
	.ascii "a.size=\0"
.LC4:
	.ascii " b.size=\0"
.LC5:
	.ascii "\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2574:
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
	sub	rsp, 160
	.seh_stackalloc	160
	.seh_endprologue
	call	__main
	lea	rbx, 32[rsp]
	mov	edx, 15
	mov	r8d, 120
	lea	rax, 48[rsp]
	mov	rcx, rbx
	lea	rsi, 64[rsp]
	mov	QWORD PTR 32[rsp], rax
.LEHB0:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE0:
	lea	rax, 80[rsp]
	mov	edx, 40
	mov	rcx, rsi
	mov	r8d, 120
	mov	QWORD PTR 64[rsp], rax
.LEHB1:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE12_M_constructEyc
.LEHE1:
	lea	rdi, 96[rsp]
	mov	rdx, rbx
	mov	rcx, rdi
.LEHB2:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_
.LEHE2:
	lea	rbp, 128[rsp]
	mov	rdx, rsi
	mov	rcx, rbp
.LEHB3:
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1ERKS4_
.LEHE3:
	mov	rdx, rbx
	mov	rcx, rdi
	call	_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_
	test	al, al
	je	.L39
	mov	rdx, rsi
	mov	rcx, rbp
	call	_ZSteqIcSt11char_traitsIcESaIcEEbRKNSt7__cxx1112basic_stringIT_T0_T1_EESA_
	test	al, al
	je	.L39
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC3[rip]
.LEHB4:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, QWORD PTR 40[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, QWORD PTR 72[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC5[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rdi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	xor	eax, eax
	add	rsp, 160
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L39:
	lea	rdx, .LC1[rip]
	mov	r8d, 10
	lea	rcx, .LC2[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE4:
.L47:
	mov	rbp, rax
.L42:
	mov	rcx, rdi
	mov	rdi, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L43:
	mov	rcx, rsi
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
.L44:
	mov	rcx, rbx
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rcx, rdi
.LEHB5:
	call	_Unwind_Resume
.LEHE5:
.L46:
	mov	rdi, rax
	jmp	.L43
.L45:
	mov	rdi, rax
	jmp	.L44
.L48:
	mov	r12, rax
	mov	rcx, rbp
	call	_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE10_M_disposeEv
	mov	rbp, r12
	jmp	.L42
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2574:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2574-.LLSDACSB2574
.LLSDACSB2574:
	.uleb128 .LEHB0-.LFB2574
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB2574
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L45-.LFB2574
	.uleb128 0
	.uleb128 .LEHB2-.LFB2574
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L46-.LFB2574
	.uleb128 0
	.uleb128 .LEHB3-.LFB2574
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L47-.LFB2574
	.uleb128 0
	.uleb128 .LEHB4-.LFB2574
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L48-.LFB2574
	.uleb128 0
	.uleb128 .LEHB5-.LFB2574
	.uleb128 .LEHE5-.LEHB5
	.uleb128 0
	.uleb128 0
.LLSDACSE2574:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt17__throw_bad_allocv;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	memcpy;	.scl	2;	.type	32;	.endef
	.def	memcmp;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
