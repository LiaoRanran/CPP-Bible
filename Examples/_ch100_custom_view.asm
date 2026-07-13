	.file	"_ch100_custom_view.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNSt12_Vector_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIiSaIiEED2Ev
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev
_ZNSt12_Vector_baseIiSaIiEED2Ev:
.LFB4561:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L1
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L1:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4172:
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
	sub	rsp, 96
	.seh_stackalloc	96
	.seh_endprologue
	call	__main
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	ecx, 16
	mov	QWORD PTR 80[rsp], 0
	movaps	XMMWORD PTR 48[rsp], xmm0
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR 64[rsp], xmm0
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rbp, rax
	mov	QWORD PTR 64[rsp], rax
	mov	rsi, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdi, 16[rax]
	mov	rax, QWORD PTR 48[rsp]
	mov	rbx, rbp
	mov	QWORD PTR 80[rsp], rdi
	lea	r12, 47[rsp]
	mov	QWORD PTR 72[rsp], rdi
	mov	QWORD PTR 0[rbp], rax
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR 8[rbp], rax
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L19:
	mov	r8d, 1
	mov	rdx, r12
.LEHB1:
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
	add	rbx, 4
	cmp	rbx, rdi
	je	.L18
.L5:
	mov	eax, DWORD PTR [rbx]
	mov	rcx, rsi
	lea	edx, [rax+rax*4]
	add	edx, edx
	call	_ZNSolsEi
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	mov	BYTE PTR 47[rsp], 32
	mov	rax, QWORD PTR -24[rax]
	cmp	QWORD PTR 16[rcx+rax], 0
	jne	.L19
	mov	edx, 32
	call	_ZNSo3putEc
	add	rbx, 4
	cmp	rbx, rdi
	jne	.L5
.L18:
	mov	rax, QWORD PTR [rsi]
	mov	BYTE PTR 48[rsp], 10
	mov	rax, QWORD PTR -24[rax]
	cmp	QWORD PTR 16[rsi+rax], 0
	jne	.L20
	mov	edx, 10
	mov	rcx, rsi
	call	_ZNSo3putEc
.L11:
	lea	rcx, 64[rsp]
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	xor	eax, eax
	add	rsp, 96
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L20:
	lea	rdx, 48[rsp]
	mov	r8d, 1
	mov	rcx, rsi
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.LEHE1:
	jmp	.L11
.L13:
	mov	rbx, rax
	mov	rcx, rbp
	mov	edx, 16
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
.L14:
	lea	rcx, 64[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, rbx
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA4172:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE4172-.LLSDACSB4172
.LLSDACSB4172:
	.uleb128 .LEHB0-.LFB4172
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L14-.LFB4172
	.uleb128 0
	.uleb128 .LEHB1-.LFB4172
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L13-.LFB4172
	.uleb128 0
	.uleb128 .LEHB2-.LFB4172
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE4172:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	1
	.long	2
	.long	3
	.long	4
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
