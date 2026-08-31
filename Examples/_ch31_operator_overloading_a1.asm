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
	.p2align 4
	.def	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB3229:
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
	je	.L8
	cmp	BYTE PTR 56[rsi], 0
	je	.L5
	movsx	edx, BYTE PTR 67[rsi]
.L6:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZNSo5flushEv
.L5:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L6
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L6
.L8:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.p2align 4
	.globl	_ZplRK3VecS1_
	.def	_ZplRK3VecS1_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZplRK3VecS1_
_ZplRK3VecS1_:
.LFB2574:
	.seh_endprologue
	movq	xmm0, QWORD PTR [rdx]
	movq	xmm1, QWORD PTR [r8]
	movhpd	xmm0, QWORD PTR 8[rdx]
	movhpd	xmm1, QWORD PTR 8[r8]
	mov	rax, rcx
	addpd	xmm0, xmm1
	movlpd	QWORD PTR [rcx], xmm0
	movhpd	QWORD PTR 8[rcx], xmm0
	movsd	xmm0, QWORD PTR 16[rdx]
	addsd	xmm0, QWORD PTR 16[r8]
	movsd	QWORD PTR 16[rcx], xmm0
	ret
	.seh_endproc
	.p2align 4
	.globl	_ZpLR3VecRKS_
	.def	_ZpLR3VecRKS_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZpLR3VecRKS_
_ZpLR3VecRKS_:
.LFB2575:
	.seh_endprologue
	movq	xmm1, QWORD PTR [rdx]
	movq	xmm0, QWORD PTR [rcx]
	movhpd	xmm1, QWORD PTR 8[rdx]
	movhpd	xmm0, QWORD PTR 8[rcx]
	mov	rax, rcx
	addpd	xmm0, xmm1
	movlpd	QWORD PTR [rcx], xmm0
	movhpd	QWORD PTR 8[rcx], xmm0
	movsd	xmm0, QWORD PTR 16[rcx]
	addsd	xmm0, QWORD PTR 16[rdx]
	movsd	QWORD PTR 16[rcx], xmm0
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii "chained: \0"
.LC2:
	.ascii ",\0"
.LC5:
	.ascii "in-place: \0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2576:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 80
	.seh_stackalloc	80
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	movaps	XMMWORD PTR 48[rsp], xmm7
	.seh_savexmm	xmm7, 48
	movaps	XMMWORD PTR 64[rsp], xmm8
	.seh_savexmm	xmm8, 64
	.seh_endprologue
	lea	rbx, .LC2[rip]
	call	__main
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC0[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm8, QWORD PTR .LC1[rip]
	mov	rcx, rax
	movapd	xmm1, xmm8
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rbx
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm7, QWORD PTR .LC3[rip]
	mov	rcx, rax
	movapd	xmm1, xmm7
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rbx
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm6, QWORD PTR .LC4[rip]
	mov	rcx, rax
	movapd	xmm1, xmm6
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC5[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm8
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rbx
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rbx
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rcx, rax
	call	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	nop
	movaps	xmm6, XMMWORD PTR 32[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 48[rsp]
	movaps	xmm8, XMMWORD PTR 64[rsp]
	add	rsp, 80
	pop	rbx
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	0
	.long	1076494336
	.align 8
.LC3:
	.long	0
	.long	1076887552
	.align 8
.LC4:
	.long	0
	.long	1077084160
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
