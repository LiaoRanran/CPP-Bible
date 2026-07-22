	.file	"_ch44_pool_perf.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL9probe_nopy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_nopy
_ZL9probe_nopy:
.LFB9904:
	.seh_endprologue
	test	rcx, rcx
	je	.L4
	xor	eax, eax
	xor	edx, edx
	test	cl, 1
	je	.L3
	mov	eax, 1
	cmp	rcx, 1
	je	.L1
	.p2align 4
	.p2align 4
	.p2align 3
.L3:
	lea	rdx, 1[rdx+rax*2]
	add	rax, 2
	cmp	rcx, rax
	jne	.L3
.L1:
	mov	rax, rdx
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xor	edx, edx
	mov	rax, rdx
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL10probe_bumpy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL10probe_bumpy
_ZL10probe_bumpy:
.LFB9905:
	.seh_endprologue
	test	rcx, rcx
	je	.L13
	mov	rdx, QWORD PTR _ZL6g_bump[rip]
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L14:
	mov	r8, rdx
	add	rax, 1
	add	rdx, 16
	mov	QWORD PTR g_sink[rip], r8
	cmp	rcx, rax
	jne	.L14
.L13:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL14probe_freelisty;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL14probe_freelisty
_ZL14probe_freelisty:
.LFB9906:
	.seh_endprologue
	test	rcx, rcx
	je	.L20
	mov	rdx, QWORD PTR _ZL10g_fl_head0[rip]
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L21:
	mov	r8, rdx
	add	rax, 1
	mov	rdx, QWORD PTR [rdx]
	mov	QWORD PTR g_sink[rip], r8
	cmp	rcx, rax
	jne	.L21
.L20:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL12probe_mallocy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL12probe_mallocy
_ZL12probe_mallocy:
.LFB9907:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, rcx
	test	rcx, rcx
	je	.L27
	xor	ebx, ebx
	.p2align 4
	.p2align 3
.L28:
	mov	ecx, 16
	add	rbx, 1
	call	malloc
	mov	rcx, rax
	mov	QWORD PTR g_sink[rip], rax
	call	free
	cmp	rsi, rbx
	jne	.L28
.L27:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL5benchPFyyEyi.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5benchPFyyEyi.constprop.0
_ZL5benchPFyyEyi.constprop.0:
.LFB9938:
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
	mov	esi, 20
	mov	rbx, -1
	mov	rbp, rcx
	.p2align 4
	.p2align 3
.L34:
/APP
 # 18 "Examples\_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 4000000
	mov	rdi, rax
	call	rbp
	mov	QWORD PTR g_sink[rip], rax
/APP
 # 18 "Examples\_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rdi
	cmp	rbx, rax
	cmova	rbx, rax
	sub	esi, 1
	jne	.L34
	test	rbx, rbx
	js	.L35
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rbx
.L36:
	divsd	xmm0, QWORD PTR .LC0[rip]
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L35:
	mov	rax, rbx
	and	ebx, 1
	pxor	xmm0, xmm0
	shr	rax
	or	rax, rbx
	cvtsi2sd	xmm0, rax
	addsd	xmm0, xmm0
	jmp	.L36
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\12\0"
.LC3:
	.ascii "ns/op\0"
.LC4:
	.ascii "cyc/op\0"
.LC5:
	.ascii "alloc\0"
.LC6:
	.ascii "%-14s %10s %10s %12s\12\0"
.LC7:
	.ascii "raw(cyc)\0"
.LC8:
	.ascii "bump\0"
.LC9:
	.ascii "%-14s %10.2f %10.3f %12.2f\12\0"
.LC10:
	.ascii "freelist\0"
.LC11:
	.ascii "malloc\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB9909:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 232
	.seh_stackalloc	232
	movaps	XMMWORD PTR 96[rsp], xmm6
	.seh_savexmm	xmm6, 96
	movaps	XMMWORD PTR 112[rsp], xmm7
	.seh_savexmm	xmm7, 112
	movaps	XMMWORD PTR 128[rsp], xmm8
	.seh_savexmm	xmm8, 128
	movaps	XMMWORD PTR 144[rsp], xmm9
	.seh_savexmm	xmm9, 144
	movaps	XMMWORD PTR 160[rsp], xmm10
	.seh_savexmm	xmm10, 160
	movaps	XMMWORD PTR 176[rsp], xmm11
	.seh_savexmm	xmm11, 176
	movaps	XMMWORD PTR 192[rsp], xmm12
	.seh_savexmm	xmm12, 192
	movaps	XMMWORD PTR 208[rsp], xmm13
	.seh_savexmm	xmm13, 208
	.seh_endprologue
	call	__main
	lea	rcx, 72[rsp]
	call	[QWORD PTR __imp_QueryPerformanceFrequency[rip]]
	mov	rsi, QWORD PTR __imp_QueryPerformanceCounter[rip]
	lea	rcx, 80[rsp]
	call	rsi
/APP
 # 18 "Examples\_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 100
	mov	rbx, rax
	call	[QWORD PTR __imp_Sleep[rip]]
	lea	rcx, 88[rsp]
	call	rsi
/APP
 # 18 "Examples\_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rbx
	js	.L39
	pxor	xmm9, xmm9
	cvtsi2sd	xmm9, rax
.L40:
	mov	rax, QWORD PTR 88[rsp]
	pxor	xmm0, xmm0
	sub	rax, QWORD PTR 80[rsp]
	pxor	xmm1, xmm1
	cvtsi2sd	xmm0, rax
	cvtsi2sd	xmm1, QWORD PTR 72[rsp]
	divsd	xmm0, xmm1
	lea	rcx, .LC2[rip]
	divsd	xmm9, xmm0
	divsd	xmm9, QWORD PTR .LC1[rip]
	movapd	xmm1, xmm9
	movq	rdx, xmm9
	call	__mingw_printf
	mov	ecx, 64000064
	call	malloc
	mov	ecx, 64000000
	mov	QWORD PTR _ZL6g_bump[rip+16], 64000000
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm0
	movaps	XMMWORD PTR _ZL6g_bump[rip], xmm0
	call	malloc
	mov	r8, rax
	lea	rax, 16[rax]
	lea	rcx, 64000000[r8]
	.p2align 5
	.p2align 4
	.p2align 3
.L41:
	mov	QWORD PTR -16[rax], rax
	lea	rdx, 16[rax]
	add	rax, 32
	mov	QWORD PTR -16[rdx], rdx
	mov	QWORD PTR -16[rax], rax
	lea	rax, 32[rdx]
	cmp	rax, rcx
	jne	.L41
	lea	rcx, _ZL9probe_nopy[rip]
	mov	QWORD PTR _ZL10g_fl_head0[rip], r8
	mov	QWORD PTR 63999984[r8], 0
	call	_ZL5benchPFyyEyi.constprop.0
	lea	rcx, _ZL10probe_bumpy[rip]
	movapd	xmm8, xmm0
	call	_ZL5benchPFyyEyi.constprop.0
	lea	rcx, _ZL14probe_freelisty[rip]
	movapd	xmm13, xmm0
	call	_ZL5benchPFyyEyi.constprop.0
	lea	rcx, _ZL12probe_mallocy[rip]
	movapd	xmm12, xmm0
	call	_ZL5benchPFyyEyi.constprop.0
	movapd	xmm2, xmm13
	movapd	xmm7, xmm12
	lea	rax, .LC7[rip]
	subsd	xmm2, xmm8
	movapd	xmm6, xmm0
	subsd	xmm7, xmm8
	mov	QWORD PTR 32[rsp], rax
	subsd	xmm6, xmm8
	lea	r9, .LC3[rip]
	movapd	xmm10, xmm0
	lea	r8, .LC4[rip]
	lea	rdx, .LC5[rip]
	movapd	xmm3, xmm2
	movapd	xmm11, xmm7
	lea	rcx, .LC6[rip]
	movsd	QWORD PTR 56[rsp], xmm2
	divsd	xmm3, xmm9
	movapd	xmm8, xmm6
	divsd	xmm11, xmm9
	movsd	QWORD PTR 48[rsp], xmm3
	call	__mingw_printf
	movsd	xmm3, QWORD PTR 48[rsp]
	movsd	xmm2, QWORD PTR 56[rsp]
	movsd	QWORD PTR 32[rsp], xmm13
	lea	rdx, .LC8[rip]
	lea	rcx, .LC9[rip]
	movq	r9, xmm3
	movq	r8, xmm2
	call	__mingw_printf
	movsd	QWORD PTR 32[rsp], xmm12
	movapd	xmm2, xmm7
	movq	r8, xmm7
	lea	rdx, .LC10[rip]
	lea	rcx, .LC9[rip]
	divsd	xmm8, xmm9
	movapd	xmm3, xmm11
	movq	r9, xmm11
	call	__mingw_printf
	movsd	QWORD PTR 32[rsp], xmm10
	movapd	xmm2, xmm6
	movq	r8, xmm6
	lea	rdx, .LC11[rip]
	lea	rcx, .LC9[rip]
	movapd	xmm3, xmm8
	movq	r9, xmm8
	call	__mingw_printf
	nop
	movaps	xmm6, XMMWORD PTR 96[rsp]
	movaps	xmm7, XMMWORD PTR 112[rsp]
	xor	eax, eax
	movaps	xmm8, XMMWORD PTR 128[rsp]
	movaps	xmm9, XMMWORD PTR 144[rsp]
	movaps	xmm10, XMMWORD PTR 160[rsp]
	movaps	xmm11, XMMWORD PTR 176[rsp]
	movaps	xmm12, XMMWORD PTR 192[rsp]
	movaps	xmm13, XMMWORD PTR 208[rsp]
	add	rsp, 232
	pop	rbx
	pop	rsi
	ret
.L39:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm9, xmm9
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm9, rdx
	addsd	xmm9, xmm9
	jmp	.L40
	.seh_endproc
	.globl	g_sink
	.bss
	.align 8
g_sink:
	.space 8
.lcomm _ZL10g_fl_head0,8,8
.lcomm _ZL6g_bump,24,16
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1095664768
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
