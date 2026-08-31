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
	.globl	_Z8by_value3Big
	.def	_Z8by_value3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8by_value3Big
_Z8by_value3Big:
.LFB2574:
	.seh_endprologue
	pxor	xmm0, xmm0
	lea	rax, 64[rcx]
.L4:
	addsd	xmm0, QWORD PTR [rcx]
	add	rcx, 16
	addsd	xmm0, QWORD PTR -8[rcx]
	cmp	rcx, rax
	jne	.L4
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7by_crefRK3Big
	.def	_Z7by_crefRK3Big;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7by_crefRK3Big
_Z7by_crefRK3Big:
.LFB2575:
	.seh_endprologue
	pxor	xmm0, xmm0
	lea	rax, 64[rcx]
.L7:
	addsd	xmm0, QWORD PTR [rcx]
	add	rcx, 16
	addsd	xmm0, QWORD PTR -8[rcx]
	cmp	rcx, rax
	jne	.L7
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC5:
	.ascii "by_value sum = \0"
.LC6:
	.ascii ", by_cref sum = \0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2576:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 200
	.seh_stackalloc	200
	movaps	XMMWORD PTR 176[rsp], xmm6
	.seh_savexmm	xmm6, 176
	.seh_endprologue
	call	__main
	lea	rdx, 112[rsp]
	pxor	xmm1, xmm1
	movapd	xmm0, XMMWORD PTR .LC1[rip]
	movabs	rax, 4607182418800017408
	mov	QWORD PTR 112[rsp], rax
	lea	rcx, 176[rsp]
	movabs	rax, 4611686018427387904
	movaps	XMMWORD PTR 48[rsp], xmm0
	movapd	xmm0, XMMWORD PTR .LC2[rip]
	mov	QWORD PTR 120[rsp], rax
	movabs	rax, 4613937818241073152
	mov	QWORD PTR 128[rsp], rax
	movabs	rax, 4616189618054758400
	movaps	XMMWORD PTR 64[rsp], xmm0
	movapd	xmm0, XMMWORD PTR .LC3[rip]
	mov	QWORD PTR 136[rsp], rax
	movabs	rax, 4617315517961601024
	mov	QWORD PTR 144[rsp], rax
	movabs	rax, 4618441417868443648
	movaps	XMMWORD PTR 80[rsp], xmm0
	movapd	xmm0, XMMWORD PTR .LC4[rip]
	mov	QWORD PTR 152[rsp], rax
	movabs	rax, 4619567317775286272
	mov	QWORD PTR 160[rsp], rax
	movabs	rax, 4620693217682128896
	mov	QWORD PTR 168[rsp], rax
	mov	rax, rdx
	movaps	XMMWORD PTR 96[rsp], xmm0
.L10:
	addsd	xmm1, QWORD PTR [rax]
	add	rax, 16
	addsd	xmm1, QWORD PTR -8[rax]
	cmp	rax, rcx
	jne	.L10
	lea	rax, 48[rsp]
	pxor	xmm6, xmm6
.L11:
	addsd	xmm6, QWORD PTR [rax]
	add	rax, 16
	addsd	xmm6, QWORD PTR -8[rax]
	cmp	rdx, rax
	jne	.L11
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC5[rip]
	movsd	QWORD PTR 40[rsp], xmm1
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm1, QWORD PTR 40[rsp]
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC6[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rbx, rax
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR -24[rax]
	mov	rsi, QWORD PTR 240[rbx+rax]
	test	rsi, rsi
	je	.L18
	cmp	BYTE PTR 56[rsi], 0
	je	.L13
	movsx	edx, BYTE PTR 67[rsi]
.L14:
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	call	_ZNSo5flushEv
	nop
	movaps	xmm6, XMMWORD PTR 176[rsp]
	xor	eax, eax
	add	rsp, 200
	pop	rbx
	pop	rsi
	ret
.L13:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	mov	edx, 10
	lea	rcx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	rax, QWORD PTR 48[rax]
	cmp	rax, rcx
	je	.L14
	mov	edx, 10
	mov	rcx, rsi
	call	rax
	movsx	edx, al
	jmp	.L14
.L18:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC1:
	.long	0
	.long	1072693248
	.long	0
	.long	1073741824
	.align 16
.LC2:
	.long	0
	.long	1074266112
	.long	0
	.long	1074790400
	.align 16
.LC3:
	.long	0
	.long	1075052544
	.long	0
	.long	1075314688
	.align 16
.LC4:
	.long	0
	.long	1075576832
	.long	0
	.long	1075838976
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
