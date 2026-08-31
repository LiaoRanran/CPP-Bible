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
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIZ4mainE4NodeSaIS0_EED2Ev;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIZ4mainE4NodeSaIS0_EED2Ev
_ZNSt6vectorIZ4mainE4NodeSaIS0_EED2Ev:
.LFB6124:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L3
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
.L3:
	ret
	.seh_endproc
	.def	_ZNSt6vectorIZ4mainE4NodeSaIS0_EED1Ev;	.scl	3;	.type	32;	.endef
	.set	_ZNSt6vectorIZ4mainE4NodeSaIS0_EED1Ev,_ZNSt6vectorIZ4mainE4NodeSaIS0_EED2Ev
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB7571:
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
	je	.L10
	cmp	BYTE PTR 56[rsi], 0
	je	.L7
	movsx	edx, BYTE PTR 67[rsi]
.L8:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L7:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L8
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L8
.L10:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.section	.text$_ZNSt6vectorIPvSaIS0_EED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIPvSaIS0_EED1Ev
	.def	_ZNSt6vectorIPvSaIS0_EED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIPvSaIS0_EED1Ev
_ZNSt6vectorIPvSaIS0_EED1Ev:
.LFB6105:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L11
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L11:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "default new/delete: \0"
.LC2:
	.ascii " ms\0"
.LC3:
	.ascii "fixed-size pool:    \0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5564:
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
	sub	rsp, 136
	.seh_stackalloc	136
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	movaps	XMMWORD PTR 112[rsp], xmm7
	.seh_savexmm	xmm7, 112
	.seh_endprologue
	call	__main
	mov	ecx, 800000
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 800000
	xor	edx, edx
	lea	rdi, 800000[rax]
	mov	rcx, rax
	mov	rsi, rax
	mov	QWORD PTR 32[rsp], rax
	mov	QWORD PTR 48[rsp], rdi
	mov	rbp, rsi
	mov	rbx, rsi
	call	memset
	mov	QWORD PTR 40[rsp], rdi
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r13, rax
	.p2align 4,,10
	.p2align 3
.L14:
	mov	ecx, 32
.LEHB1:
	call	_Znwy
	mov	QWORD PTR [rbx], rax
	add	rbx, 8
	cmp	rbx, rdi
	jne	.L14
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, rsi
	mov	r12, rax
	.p2align 4,,10
	.p2align 3
.L15:
	mov	rcx, QWORD PTR [rbx]
	add	rbx, 8
	call	_ZdlPv
	cmp	rdi, rbx
	jne	.L15
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdx, r12
	pxor	xmm0, xmm0
	pxor	xmm1, xmm1
	sub	rdx, r13
	sub	rax, r12
	movsd	xmm7, QWORD PTR .LC0[rip]
	cvtsi2sd	xmm0, rdx
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	cvtsi2sd	xmm1, rax
	lea	rdx, .LC1[rip]
	divsd	xmm0, xmm7
	divsd	xmm1, xmm7
	movapd	xmm6, xmm0
	addsd	xmm6, xmm1
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	movapd	xmm1, xmm6
	mov	rdx, QWORD PTR -24[rax]
	add	rdx, rcx
	mov	eax, DWORD PTR 24[rdx]
	mov	QWORD PTR 8[rdx], 3
	and	eax, -261
	or	eax, 4
	mov	DWORD PTR 24[rdx], eax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	r12, .LC2[rip]
	mov	rcx, rax
	mov	rdx, r12
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	ecx, 800000
	pxor	xmm0, xmm0
	movups	XMMWORD PTR 72[rsp], xmm0
	call	_Znwy
.LEHE1:
	lea	rcx, 800000[rax]
	mov	QWORD PTR [rax], 0
	mov	rbx, rax
	mov	QWORD PTR 64[rsp], rax
	lea	rax, 8[rax]
	mov	QWORD PTR 80[rsp], rcx
	mov	rdx, rax
	.p2align 4,,10
	.p2align 3
.L16:
	mov	r8, QWORD PTR [rbx]
	add	rdx, 8
	mov	QWORD PTR -8[rdx], r8
	cmp	rcx, rdx
	jne	.L16
	mov	rdx, rcx
	mov	QWORD PTR 72[rsp], rcx
	sub	rdx, rax
	and	edx, 8
	je	.L17
	mov	QWORD PTR -8[rax], rax
	add	rax, 8
	cmp	rax, rcx
	je	.L36
	.p2align 4,,10
	.p2align 3
.L17:
	mov	QWORD PTR -8[rax], rax
	lea	rdx, 8[rax]
	add	rax, 16
	cmp	rax, rcx
	mov	QWORD PTR -8[rdx], rdx
	jne	.L17
.L36:
	mov	QWORD PTR 799992[rbx], 0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	r13, rax
	mov	rax, rsi
	.p2align 4,,10
	.p2align 3
.L18:
	mov	rdx, rbx
	add	rax, 8
	mov	rbx, QWORD PTR [rbx]
	mov	QWORD PTR -8[rax], rdx
	cmp	rax, rdi
	jne	.L18
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rsi, rax
	.p2align 4,,10
	.p2align 3
.L20:
	mov	rax, rbx
	mov	rbx, QWORD PTR 0[rbp]
	add	rbp, 8
	cmp	rdi, rbp
	mov	QWORD PTR [rbx], rax
	jne	.L20
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm0, xmm0
	pxor	xmm1, xmm1
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC3[rip]
	sub	rax, rsi
	sub	rsi, r13
	cvtsi2sd	xmm0, rax
	cvtsi2sd	xmm1, rsi
	divsd	xmm0, xmm7
	divsd	xmm1, xmm7
	movapd	xmm6, xmm0
	addsd	xmm6, xmm1
.LEHB2:
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	movapd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	mov	rdx, r12
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.LEHE2:
	lea	rcx, 64[rsp]
	call	_ZNSt6vectorIZ4mainE4NodeSaIS0_EED1Ev
	lea	rcx, 32[rsp]
	call	_ZNSt6vectorIPvSaIS0_EED1Ev
	nop
	movaps	xmm6, XMMWORD PTR 96[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 112[rsp]
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L23:
	mov	rbx, rax
	jmp	.L22
.L24:
	lea	rcx, 64[rsp]
	mov	rbx, rax
	call	_ZNSt6vectorIZ4mainE4NodeSaIS0_EED1Ev
.L22:
	lea	rcx, 32[rsp]
	call	_ZNSt6vectorIPvSaIS0_EED1Ev
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5564:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5564-.LLSDACSB5564
.LLSDACSB5564:
	.uleb128 .LEHB0-.LFB5564
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5564
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L23-.LFB5564
	.uleb128 0
	.uleb128 .LEHB2-.LFB5564
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L24-.LFB5564
	.uleb128 0
	.uleb128 .LEHB3-.LFB5564
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE5564:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
