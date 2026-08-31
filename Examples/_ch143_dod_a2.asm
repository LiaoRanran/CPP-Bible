	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2312:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0:
.LFB4798:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movabs	rax, 1152921504606846975
	cmp	rax, rdx
	mov	rbx, rcx
	mov	rsi, rdx
	jb	.L11
	test	rdx, rdx
	pxor	xmm0, xmm0
	mov	QWORD PTR 16[rcx], 0
	movups	XMMWORD PTR [rcx], xmm0
	je	.L12
	lea	rdi, 0[0+rdx*8]
	mov	rcx, rdi
	call	_Znwy
	sub	rsi, 1
	lea	rbp, [rax+rdi]
	mov	QWORD PTR [rbx], rax
	mov	QWORD PTR 16[rbx], rbp
	lea	rcx, 8[rax]
	mov	QWORD PTR [rax], 0x000000000
	je	.L6
	cmp	rbp, rcx
	je	.L7
	lea	r8, -8[rdi]
	xor	edx, edx
	call	memset
.L7:
	mov	rcx, rbp
.L6:
	mov	QWORD PTR 8[rbx], rcx
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L12:
	xor	eax, eax
	mov	QWORD PTR [rcx], rax
	mov	QWORD PTR 16[rcx], rax
	xor	ecx, ecx
	jmp	.L6
.L11:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB4803:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -24[rax]
	mov	rbx, rcx
	mov	rsi, QWORD PTR 240[rcx+rax]
	test	rsi, rsi
	je	.L18
	cmp	BYTE PTR 56[rsi], 0
	je	.L15
	movsx	edx, BYTE PTR 67[rsi]
.L16:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L15:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L16
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L16
.L18:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.section	.text$_ZNSt6vectorI8ParticleSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
	.def	_ZNSt6vectorI8ParticleSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
_ZNSt6vectorI8ParticleSaIS0_EED1Ev:
.LFB4306:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L19
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L19:
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIdSaIdEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIdSaIdEED1Ev
	.def	_ZNSt6vectorIdSaIdEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIdSaIdEED1Ev
_ZNSt6vectorIdSaIdEED1Ev:
.LFB4314:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L21
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L21:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC7:
	.ascii "C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmpwilxuznc\\s.cpp\0"
	.align 8
.LC8:
	.ascii "std::fabs(sum_aos - sum_soa) < 1e-6\0"
.LC9:
	.ascii "AoS sum(x) = \0"
.LC10:
	.ascii "SoA sum(x) = \0"
.LC11:
	.ascii "DOD layout demo ok\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3871:
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
	sub	rsp, 296
	.seh_stackalloc	296
	movaps	XMMWORD PTR 256[rsp], xmm6
	.seh_savexmm	xmm6, 256
	movaps	XMMWORD PTR 272[rsp], xmm7
	.seh_savexmm	xmm7, 272
	.seh_endprologue
	call	__main
	mov	ecx, 65536
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	ecx, 8
	lea	rsi, 65536[rax]
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	xor	eax, eax
	mov	rdi, rbx
	mov	QWORD PTR 48[rsp], rsi
	rep stosq
	lea	rax, 64[rbx]
.L24:
	mov	rdx, QWORD PTR [rbx]
	add	rax, 64
	mov	QWORD PTR -64[rax], rdx
	mov	rdx, QWORD PTR 8[rbx]
	mov	QWORD PTR -56[rax], rdx
	mov	rdx, QWORD PTR 16[rbx]
	mov	QWORD PTR -48[rax], rdx
	mov	rdx, QWORD PTR 24[rbx]
	mov	QWORD PTR -40[rax], rdx
	mov	rdx, QWORD PTR 32[rbx]
	mov	QWORD PTR -32[rax], rdx
	mov	rdx, QWORD PTR 40[rbx]
	mov	QWORD PTR -24[rax], rdx
	mov	rdx, QWORD PTR 48[rbx]
	mov	QWORD PTR -16[rax], rdx
	mov	rdx, QWORD PTR 56[rbx]
	mov	QWORD PTR -8[rax], rdx
	cmp	rsi, rax
	jne	.L24
	lea	rdi, 64[rsp]
	mov	edx, 1024
	mov	QWORD PTR 40[rsp], rsi
	mov	rcx, rdi
.LEHB1:
	call	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
.LEHE1:
	lea	rbp, 96[rsp]
	mov	edx, 1024
	mov	rcx, rbp
.LEHB2:
	call	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
.LEHE2:
	lea	r12, 128[rsp]
	mov	edx, 1024
	mov	rcx, r12
.LEHB3:
	call	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
.LEHE3:
	lea	r13, 160[rsp]
	mov	edx, 1024
	mov	rcx, r13
.LEHB4:
	call	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
.LEHE4:
	lea	r14, 192[rsp]
	mov	edx, 1024
	mov	rcx, r14
.LEHB5:
	call	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
.LEHE5:
	lea	r15, 224[rsp]
	mov	edx, 1024
	mov	rcx, r15
.LEHB6:
	call	_ZNSt6vectorIdSaIdEEC1EyRKS0_.isra.0
.LEHE6:
	mov	rdx, QWORD PTR 64[rsp]
	mov	rcx, rbx
	mov	r9, rbx
	xor	eax, eax
	mov	r8, QWORD PTR 160[rsp]
	movsd	xmm1, QWORD PTR .LC3[rip]
	.p2align 4,,10
	.p2align 3
.L25:
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, eax
	add	r9, 64
	movsd	QWORD PTR [rdx+rax*8], xmm0
	movsd	QWORD PTR -64[r9], xmm0
	mulsd	xmm0, xmm1
	movsd	QWORD PTR [r8+rax*8], xmm0
	add	rax, 1
	movsd	QWORD PTR -40[r9], xmm0
	cmp	rax, 1024
	jne	.L25
	movsd	xmm1, QWORD PTR .LC4[rip]
	.p2align 4,,10
	.p2align 3
.L26:
	movsd	xmm0, QWORD PTR 24[rbx]
	add	rbx, 64
	addsd	xmm0, xmm1
	movsd	QWORD PTR -40[rbx], xmm0
	mulsd	xmm0, xmm1
	addsd	xmm0, QWORD PTR -64[rbx]
	movsd	QWORD PTR -64[rbx], xmm0
	cmp	rsi, rbx
	jne	.L26
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L27:
	movsd	xmm0, QWORD PTR [r8+rax]
	addsd	xmm0, xmm1
	movsd	QWORD PTR [r8+rax], xmm0
	mulsd	xmm0, xmm1
	addsd	xmm0, QWORD PTR [rdx+rax]
	movsd	QWORD PTR [rdx+rax], xmm0
	add	rax, 8
	cmp	rax, 8192
	jne	.L27
	pxor	xmm6, xmm6
	movapd	xmm7, xmm6
	.p2align 4,,10
	.p2align 3
.L28:
	addsd	xmm7, QWORD PTR [rcx]
	add	rcx, 64
	add	rdx, 8
	addsd	xmm6, QWORD PTR -8[rdx]
	cmp	rsi, rcx
	jne	.L28
	movsd	xmm1, QWORD PTR .LC6[rip]
	movapd	xmm0, xmm7
	subsd	xmm0, xmm6
	andpd	xmm0, XMMWORD PTR .LC5[rip]
	comisd	xmm1, xmm0
	jbe	.L51
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC9[rip]
	mov	rcx, rbx
.LEHB7:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	movapd	xmm1, xmm7
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC10[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	movapd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	lea	rdx, .LC11[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, r15
	call	_ZNSt6vectorIdSaIdEED1Ev
	mov	rcx, r14
	call	_ZNSt6vectorIdSaIdEED1Ev
	mov	rcx, r13
	call	_ZNSt6vectorIdSaIdEED1Ev
	mov	rcx, r12
	call	_ZNSt6vectorIdSaIdEED1Ev
	mov	rcx, rbp
	call	_ZNSt6vectorIdSaIdEED1Ev
	mov	rcx, rdi
	call	_ZNSt6vectorIdSaIdEED1Ev
	lea	rcx, 32[rsp]
	call	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
	nop
	movaps	xmm6, XMMWORD PTR 256[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 272[rsp]
	add	rsp, 296
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
.L51:
	lea	rdx, .LC7[rip]
	mov	r8d, 43
	lea	rcx, .LC8[rip]
	call	[QWORD PTR __imp__assert[rip]]
.LEHE7:
.L42:
	mov	rbx, rax
.L31:
	mov	rcx, r14
	call	_ZNSt6vectorIdSaIdEED1Ev
.L32:
	mov	rcx, r13
	call	_ZNSt6vectorIdSaIdEED1Ev
.L33:
	mov	rcx, r12
	call	_ZNSt6vectorIdSaIdEED1Ev
.L34:
	mov	rcx, rbp
	call	_ZNSt6vectorIdSaIdEED1Ev
.L35:
	mov	rcx, rdi
	call	_ZNSt6vectorIdSaIdEED1Ev
.L36:
	lea	rcx, 32[rsp]
	call	_ZNSt6vectorI8ParticleSaIS0_EED1Ev
	mov	rcx, rbx
.LEHB8:
	call	_Unwind_Resume
.LEHE8:
.L41:
	mov	rbx, rax
	jmp	.L32
.L40:
	mov	rbx, rax
	jmp	.L33
.L39:
	mov	rbx, rax
	jmp	.L34
.L38:
	mov	rbx, rax
	jmp	.L35
.L37:
	mov	rbx, rax
	jmp	.L36
.L43:
	mov	rcx, r15
	mov	rbx, rax
	call	_ZNSt6vectorIdSaIdEED1Ev
	jmp	.L31
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3871:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3871-.LLSDACSB3871
.LLSDACSB3871:
	.uleb128 .LEHB0-.LFB3871
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3871
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L37-.LFB3871
	.uleb128 0
	.uleb128 .LEHB2-.LFB3871
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L38-.LFB3871
	.uleb128 0
	.uleb128 .LEHB3-.LFB3871
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L39-.LFB3871
	.uleb128 0
	.uleb128 .LEHB4-.LFB3871
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L40-.LFB3871
	.uleb128 0
	.uleb128 .LEHB5-.LFB3871
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L41-.LFB3871
	.uleb128 0
	.uleb128 .LEHB6-.LFB3871
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L42-.LFB3871
	.uleb128 0
	.uleb128 .LEHB7-.LFB3871
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L43-.LFB3871
	.uleb128 0
	.uleb128 .LEHB8-.LFB3871
	.uleb128 .LEHE8-.LEHB8
	.uleb128 0
	.uleb128 0
.LLSDACSE3871:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC3:
	.long	0
	.long	1071644672
	.align 8
.LC4:
	.long	1202590843
	.long	1065646817
	.align 16
.LC5:
	.long	-1
	.long	2147483647
	.long	0
	.long	0
	.align 8
.LC6:
	.long	-1598689907
	.long	1051772663
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
