	.file	"_ch100_custom_view.cpp"
	.intel_syntax noprefix
	.text
	.align 2
	.p2align 4
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0:
.LFB7770:
	.seh_endprologue
	test	rcx, rcx
	je	.L1
	sub	rdx, rcx
	jmp	_ZdlPvy
.L1:
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.section	.text.startup,"x"
.LHOTB0:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5523:
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
	call	__main
	mov	ecx, 16
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r12, rax
	lea	rdi, 16[rax]
	movabs	rdx, 17179869187
	movabs	rax, 8589934593
	mov	QWORD PTR [r12], rax
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	mov	rbx, r12
	lea	rbp, 46[rsp]
	mov	QWORD PTR 8[r12], rdx
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L19:
	mov	r8d, 1
	mov	rdx, rbp
	mov	rcx, rax
.LEHB1:
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	add	rbx, 4
	cmp	rdi, rbx
	je	.L18
.L5:
	mov	eax, DWORD PTR [rbx]
	mov	rcx, rsi
	lea	edx, [rax+rax*4]
	add	edx, edx
	call	_ZNSolsEi
	mov	rdx, QWORD PTR [rax]
	mov	BYTE PTR 46[rsp], 32
	mov	rdx, QWORD PTR -24[rdx]
	cmp	QWORD PTR 16[rax+rdx], 0
	jne	.L19
	mov	edx, 32
	mov	rcx, rax
	call	_ZNSo3putEc
	add	rbx, 4
	cmp	rdi, rbx
	jne	.L5
.L18:
	mov	rax, QWORD PTR [rsi]
	mov	BYTE PTR 47[rsp], 10
	mov	rax, QWORD PTR -24[rax]
	cmp	QWORD PTR 16[rsi+rax], 0
	je	.L10
	lea	rdx, 47[rsp]
	mov	r8d, 1
	mov	rcx, rsi
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L11:
	mov	rdx, rdi
	mov	rcx, r12
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L10:
	mov	edx, 10
	mov	rcx, rsi
	call	_ZNSo3putEc
.LEHE1:
	jmp	.L11
.L14:
	mov	rbx, rax
	jmp	.L6
.L13:
	mov	rbx, rax
	jmp	.L12
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5523:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5523-.LLSDACSB5523
.LLSDACSB5523:
	.uleb128 .LEHB0-.LFB5523
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L14-.LFB5523
	.uleb128 0
	.uleb128 .LEHB1-.LFB5523
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L13-.LFB5523
	.uleb128 0
.LLSDACSE5523:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_savereg	rbp, 72
	.seh_savereg	r12, 80
	.seh_endprologue
main.cold:
.L6:
	xor	ecx, ecx
	xor	edx, edx
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
.L12:
	mov	rcx, r12
	mov	rdx, rdi
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev.isra.0
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5523:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5523-.LLSDACSBC5523
.LLSDACSBC5523:
	.uleb128 .LEHB2-.LCOLDB0
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC5523:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.section	.text.startup,"x"
.LHOTE0:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
