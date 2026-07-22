	.file	"_ch25_variant_perf.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN1A1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1A1fEv
	.def	_ZN1A1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1A1fEv
_ZN1A1fEv:
.LFB7301:
	.seh_endprologue
	mov	eax, 1
	ret
	.seh_endproc
	.section	.text$_ZN1B1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1B1fEv
	.def	_ZN1B1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1B1fEv
_ZN1B1fEv:
.LFB7302:
	.seh_endprologue
	mov	eax, 2
	ret
	.seh_endproc
	.section	.text$_ZN1C1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1C1fEv
	.def	_ZN1C1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1C1fEv
_ZN1C1fEv:
.LFB7303:
	.seh_endprologue
	mov	eax, 3
	ret
	.seh_endproc
	.section	.text$_ZN1D1fEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1D1fEv
	.def	_ZN1D1fEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1D1fEv
_ZN1D1fEv:
.LFB7304:
	.seh_endprologue
	mov	eax, 4
	ret
	.seh_endproc
	.section	.text$_ZN1AD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1AD1Ev
	.def	_ZN1AD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1AD1Ev
_ZN1AD1Ev:
.LFB7318:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN1BD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1BD1Ev
	.def	_ZN1BD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1BD1Ev
_ZN1BD1Ev:
.LFB7325:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN1CD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1CD1Ev
	.def	_ZN1CD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1CD1Ev
_ZN1CD1Ev:
.LFB7332:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN1DD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1DD1Ev
	.def	_ZN1DD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1DD1Ev
_ZN1DD1Ev:
.LFB7339:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN1AD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1AD0Ev
	.def	_ZN1AD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1AD0Ev
_ZN1AD0Ev:
.LFB7319:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN1DD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1DD0Ev
	.def	_ZN1DD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1DD0Ev
_ZN1DD0Ev:
.LFB7340:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN1CD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1CD0Ev
	.def	_ZN1CD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1CD0Ev
_ZN1CD0Ev:
.LFB7333:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN1BD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN1BD0Ev
	.def	_ZN1BD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN1BD0Ev
_ZN1BD0Ev:
.LFB7326:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z23probe_variant_visit_hotPKSt7variantIJildcEEPKii
	.def	_Z23probe_variant_visit_hotPKSt7variantIJildcEEPKii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z23probe_variant_visit_hotPKSt7variantIJildcEEPKii
_Z23probe_variant_visit_hotPKSt7variantIJildcEEPKii:
.LFB7305:
	.seh_endprologue
	test	r8d, r8d
	jle	.L21
	movsxd	r8, r8d
	lea	r9, [rdx+r8*4]
	xor	r8d, r8d
	jmp	.L20
	.p2align 4,,10
	.p2align 3
.L23:
	mov	eax, DWORD PTR [rax]
.L19:
	cdqe
	add	rdx, 4
	add	r8, rax
	cmp	r9, rdx
	je	.L14
.L20:
	movsxd	rax, DWORD PTR [rdx]
	sal	rax, 4
	add	rax, rcx
	cmp	BYTE PTR 8[rax], 2
	je	.L16
	jbe	.L23
	movsx	eax, BYTE PTR [rax]
	add	rdx, 4
	cdqe
	add	r8, rax
	cmp	r9, rdx
	jne	.L20
.L14:
	mov	rax, r8
	ret
	.p2align 4,,10
	.p2align 3
.L16:
	cvttsd2si	eax, QWORD PTR [rax]
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L21:
	xor	r8d, r8d
	mov	rax, r8
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17probe_virtual_hotPKP1APKii
	.def	_Z17probe_virtual_hotPKP1APKii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17probe_virtual_hotPKP1APKii
_Z17probe_virtual_hotPKP1APKii:
.LFB7311:
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
	mov	rdi, rcx
	test	r8d, r8d
	jle	.L27
	movsxd	r8, r8d
	mov	rbx, rdx
	xor	esi, esi
	lea	rbp, [rdx+r8*4]
	.p2align 4
	.p2align 3
.L26:
	movsxd	rax, DWORD PTR [rbx]
	add	rbx, 4
	mov	rcx, QWORD PTR [rdi+rax*8]
	mov	rax, QWORD PTR [rcx]
	call	[QWORD PTR [rax]]
	cdqe
	add	rsi, rax
	cmp	rbp, rbx
	jne	.L26
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L27:
	xor	esi, esi
	mov	rax, rsi
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC2:
	.ascii "TSC_freq = %.3f GHz (ns/cycle=%.4f)\12\0"
.LC8:
	.ascii "variant_visit\0"
.LC9:
	.ascii "%-20s : %8.3f ns/op\12\0"
.LC10:
	.ascii "virtual_call\0"
.LC11:
	.ascii "sink=%llu\12\0"
	.section	.text.unlikely,"x"
.LCOLDB13:
	.section	.text.startup,"x"
.LHOTB13:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB7312:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 2720
	.seh_stackalloc	2720
	movaps	XMMWORD PTR 2672[rsp], xmm6
	.seh_savexmm	xmm6, 2672
	movaps	XMMWORD PTR 2688[rsp], xmm7
	.seh_savexmm	xmm7, 2688
	movaps	XMMWORD PTR 2704[rsp], xmm8
	.seh_savexmm	xmm8, 2704
	.seh_endprologue
	call	__main
	lea	rax, 32[rsp]
	movq	xmm8, rax
	lea	rax, 40[rsp]
	movq	xmm7, rax
	lea	rax, 48[rsp]
	movq	xmm6, rax
	lea	rax, 56[rsp]
	punpcklqdq	xmm8, xmm7
	movq	xmm7, rax
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	punpcklqdq	xmm6, xmm7
	mov	rsi, rax
/APP
 # 12 "Examples\_ch25_variant_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	eax, eax
	mov	rdi, rdx
	or	rdi, rax
.L30:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rax, rsi
	cmp	rax, 99999999
	jle	.L30
/APP
 # 12 "Examples\_ch25_variant_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	eax, eax
	mov	rbx, rdx
	or	rbx, rax
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdx, rax
	mov	rax, rbx
	sub	rax, rdi
	js	.L31
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
.L32:
	movsd	xmm2, QWORD PTR .LC0[rip]
	mov	rax, rdx
	pxor	xmm1, xmm1
	movsd	xmm7, QWORD PTR .LC1[rip]
	sub	rax, rsi
	lea	rcx, .LC2[rip]
	cvtsi2sd	xmm1, rax
	divsd	xmm1, xmm2
	divsd	xmm0, xmm1
	movapd	xmm1, xmm0
	divsd	xmm1, xmm2
	divsd	xmm7, xmm1
	movq	rdx, xmm1
	movapd	xmm2, xmm7
	movq	r8, xmm7
.LEHB0:
	call	__mingw_printf
	lea	rax, _ZTV1A[rip+16]
	pxor	xmm0, xmm0
	mov	ecx, 80000000
	mov	QWORD PTR 32[rsp], rax
	lea	rax, _ZTV1B[rip+16]
	mov	QWORD PTR 40[rsp], rax
	lea	rax, _ZTV1C[rip+16]
	mov	QWORD PTR 48[rsp], rax
	lea	rax, _ZTV1D[rip+16]
	mov	QWORD PTR 56[rsp], rax
	mov	rax, QWORD PTR .LC3[rip]
	movups	XMMWORD PTR 132[rsp], xmm0
	movups	XMMWORD PTR 116[rsp], xmm0
	movups	XMMWORD PTR 144[rsp], xmm0
	movups	XMMWORD PTR 100[rsp], xmm0
	mov	DWORD PTR 96[rsp], 1
	mov	DWORD PTR 112[rsp], 2
	mov	BYTE PTR 120[rsp], 1
	mov	QWORD PTR 128[rsp], rax
	mov	BYTE PTR 136[rsp], 2
	mov	BYTE PTR 144[rsp], 4
	mov	BYTE PTR 152[rsp], 3
	movaps	XMMWORD PTR 64[rsp], xmm8
	movaps	XMMWORD PTR 80[rsp], xmm6
	call	_Znwy
.LEHE0:
	xor	edx, edx
	mov	r8d, 79999996
	mov	DWORD PTR [rax], 0
	lea	rcx, 4[rax]
	mov	rbx, rax
	call	memset
	mov	edx, 1
	mov	DWORD PTR 160[rsp], 1
	lea	rcx, 164[rsp]
	mov	r11d, 1
	.p2align 6
	.p2align 4
	.p2align 3
.L33:
	mov	eax, edx
	add	rcx, 4
	shr	eax, 30
	xor	eax, edx
	imul	eax, eax, 1812433253
	lea	edx, [rax+r11]
	add	r11, 1
	mov	DWORD PTR -4[rcx], edx
	cmp	r11, 624
	jne	.L33
	pcmpeqd	xmm3, xmm3
	mov	r8, rbx
	lea	r10, 80000000[rbx]
	movdqa	xmm5, xmm3
	movdqa	xmm4, xmm3
	lea	rcx, 1056[rsp]
	psrld	xmm5, 1
	pslld	xmm4, 31
	lea	r9, 172[rsp]
	psrld	xmm3, 31
	lea	rdx, 2652[rsp]
	jmp	.L39
	.p2align 4,,10
	.p2align 3
.L55:
	mov	esi, DWORD PTR 160[rsp+r11*4]
	add	r11, 1
.L35:
	mov	eax, esi
	add	r8, 4
	shr	eax, 11
	xor	eax, esi
	mov	esi, eax
	sal	esi, 7
	and	esi, -1658038656
	xor	eax, esi
	mov	esi, eax
	sal	esi, 15
	and	esi, -272236544
	xor	eax, esi
	mov	esi, eax
	shr	esi, 18
	xor	eax, esi
	and	eax, 3
	mov	DWORD PTR -4[r8], eax
	cmp	r8, r10
	je	.L54
.L39:
	cmp	r11, 624
	jne	.L55
	lea	rax, 160[rsp]
	.p2align 4
	.p2align 3
.L36:
	movdqu	xmm1, XMMWORD PTR 4[rax]
	movdqa	xmm0, XMMWORD PTR [rax]
	add	rax, 16
	movdqu	xmm2, XMMWORD PTR 1572[rax]
	pand	xmm0, xmm4
	pand	xmm1, xmm5
	por	xmm1, xmm0
	movdqa	xmm0, xmm1
	pand	xmm1, xmm3
	psrld	xmm0, 1
	pxor	xmm2, xmm0
	movdqa	xmm0, xmm1
	pslld	xmm0, 3
	paddd	xmm0, xmm1
	pslld	xmm0, 9
	paddd	xmm0, xmm1
	pslld	xmm0, 5
	paddd	xmm0, xmm1
	pslld	xmm0, 2
	psubd	xmm0, xmm1
	pslld	xmm0, 3
	psubd	xmm0, xmm1
	movdqa	xmm6, xmm0
	pslld	xmm6, 4
	paddd	xmm0, xmm6
	pslld	xmm0, 5
	psubd	xmm0, xmm1
	pxor	xmm2, xmm0
	movaps	XMMWORD PTR -16[rax], xmm2
	cmp	rax, rcx
	jne	.L36
	mov	edi, DWORD PTR 1056[rsp]
	lea	r11, 160[rsp]
.L37:
	and	edi, -2147483648
	add	r11, 4
	mov	esi, edi
	mov	edi, DWORD PTR 896[r11]
	mov	eax, edi
	and	eax, 2147483647
	or	eax, esi
	mov	esi, eax
	and	eax, 1
	neg	eax
	shr	esi
	xor	esi, DWORD PTR 2480[r11]
	and	eax, -1727483681
	xor	eax, esi
	mov	DWORD PTR 892[r11], eax
	cmp	r9, r11
	jne	.L37
	lea	rax, 1068[rsp]
	.p2align 4
	.p2align 3
.L38:
	movdqa	xmm1, XMMWORD PTR 4[rax]
	movdqu	xmm0, XMMWORD PTR [rax]
	add	rax, 16
	pand	xmm0, xmm4
	pand	xmm1, xmm5
	por	xmm1, xmm0
	movdqa	xmm2, xmm1
	pand	xmm1, xmm3
	movdqa	xmm0, xmm1
	psrld	xmm2, 1
	pxor	xmm2, XMMWORD PTR -924[rax]
	pslld	xmm0, 3
	paddd	xmm0, xmm1
	pslld	xmm0, 9
	paddd	xmm0, xmm1
	pslld	xmm0, 5
	paddd	xmm0, xmm1
	pslld	xmm0, 2
	psubd	xmm0, xmm1
	pslld	xmm0, 3
	psubd	xmm0, xmm1
	movdqa	xmm6, xmm0
	pslld	xmm6, 4
	paddd	xmm0, xmm6
	pslld	xmm0, 5
	psubd	xmm0, xmm1
	pxor	xmm2, xmm0
	movups	XMMWORD PTR -16[rax], xmm2
	cmp	rdx, rax
	jne	.L38
	mov	esi, DWORD PTR 160[rsp]
	mov	eax, DWORD PTR 2652[rsp]
	mov	r11d, esi
	and	eax, -2147483648
	and	r11d, 2147483647
	or	eax, r11d
	mov	r11d, eax
	and	eax, 1
	neg	eax
	shr	r11d
	xor	r11d, DWORD PTR 1744[rsp]
	and	eax, -1727483681
	xor	eax, r11d
	mov	r11d, 1
	mov	DWORD PTR 2652[rsp], eax
	jmp	.L35
.L54:
	mov	rdx, rbx
	lea	rcx, 96[rsp]
	mov	r8d, 1000
	call	_Z23probe_variant_visit_hotPKSt7variantIJildcEEPKii
	mov	rdx, rax
	mov	rax, QWORD PTR _ZL6g_sink[rip]
	add	rax, rdx
	mov	QWORD PTR _ZL6g_sink[rip], rax
/APP
 # 12 "Examples\_ch25_variant_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	eax, eax
	mov	r8d, 20000000
	or	rdx, rax
	mov	r10, rdx
	mov	rdx, rbx
	call	_Z23probe_variant_visit_hotPKSt7variantIJildcEEPKii
	mov	rsi, rax
/APP
 # 12 "Examples\_ch25_variant_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	eax, eax
	or	rax, rdx
	sub	rax, r10
	js	.L40
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
.L41:
	mulsd	xmm0, xmm7
	movsd	xmm6, QWORD PTR .LC7[rip]
	lea	rdx, .LC8[rip]
	lea	rcx, .LC9[rip]
	divsd	xmm0, xmm6
	movq	r8, xmm0
	movapd	xmm2, xmm0
.LEHB1:
	call	__mingw_printf
	mov	rax, QWORD PTR _ZL6g_sink[rip]
	mov	r8d, 1000
	mov	rdx, rbx
	lea	rcx, 64[rsp]
	add	rax, rsi
	mov	QWORD PTR _ZL6g_sink[rip], rax
	call	_Z17probe_virtual_hotPKP1APKii
	mov	rdx, rax
	mov	rax, QWORD PTR _ZL6g_sink[rip]
	add	rax, rdx
	mov	QWORD PTR _ZL6g_sink[rip], rax
/APP
 # 12 "Examples\_ch25_variant_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	eax, eax
	mov	r8d, 20000000
	mov	rdi, rdx
	lea	rcx, 64[rsp]
	mov	rdx, rbx
	or	rdi, rax
	call	_Z17probe_virtual_hotPKP1APKii
	mov	rsi, rax
/APP
 # 12 "Examples\_ch25_variant_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	eax, eax
	or	rax, rdx
	sub	rax, rdi
	js	.L42
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
.L43:
	mulsd	xmm0, xmm7
	lea	rdx, .LC10[rip]
	lea	rcx, .LC9[rip]
	divsd	xmm0, xmm6
	movq	r8, xmm0
	movapd	xmm2, xmm0
	call	__mingw_printf
	mov	rax, QWORD PTR _ZL6g_sink[rip]
	lea	rcx, .LC11[rip]
	add	rax, rsi
	mov	QWORD PTR _ZL6g_sink[rip], rax
	mov	rdx, QWORD PTR _ZL6g_sink[rip]
	call	__mingw_printf
.LEHE1:
	mov	edx, 80000000
	mov	rcx, rbx
	call	_ZdlPvy
	nop
	movaps	xmm6, XMMWORD PTR 2672[rsp]
	movaps	xmm7, XMMWORD PTR 2688[rsp]
	xor	eax, eax
	movaps	xmm8, XMMWORD PTR 2704[rsp]
	add	rsp, 2720
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L31:
	mov	rcx, rax
	and	eax, 1
	pxor	xmm0, xmm0
	shr	rcx
	or	rcx, rax
	cvtsi2sd	xmm0, rcx
	addsd	xmm0, xmm0
	jmp	.L32
.L42:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm0, xmm0
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm0, rdx
	addsd	xmm0, xmm0
	jmp	.L43
.L40:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm0, xmm0
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm0, rdx
	addsd	xmm0, xmm0
	jmp	.L41
.L45:
	mov	rsi, rax
	jmp	.L44
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA7312:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE7312-.LLSDACSB7312
.LLSDACSB7312:
	.uleb128 .LEHB0-.LFB7312
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB7312
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L45-.LFB7312
	.uleb128 0
.LLSDACSE7312:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	2744
	.seh_savereg	rbx, 2720
	.seh_savereg	rsi, 2728
	.seh_savereg	rdi, 2736
	.seh_savexmm	xmm6, 2672
	.seh_savexmm	xmm7, 2688
	.seh_savexmm	xmm8, 2704
	.seh_endprologue
main.cold:
.L44:
	mov	rcx, rbx
	mov	edx, 80000000
	call	_ZdlPvy
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC7312:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC7312-.LLSDACSBC7312
.LLSDACSBC7312:
	.uleb128 .LEHB2-.LCOLDB13
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC7312:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE13:
	.section	.text.startup,"x"
.LHOTE13:
	.globl	_ZTS1A
	.section	.rdata$_ZTS1A,"dr"
	.linkonce same_size
_ZTS1A:
	.ascii "1A\0"
	.globl	_ZTI1A
	.section	.rdata$_ZTI1A,"dr"
	.linkonce same_size
	.align 8
_ZTI1A:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS1A
	.globl	_ZTS1B
	.section	.rdata$_ZTS1B,"dr"
	.linkonce same_size
_ZTS1B:
	.ascii "1B\0"
	.globl	_ZTI1B
	.section	.rdata$_ZTI1B,"dr"
	.linkonce same_size
	.align 8
_ZTI1B:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS1B
	.quad	_ZTI1A
	.globl	_ZTS1C
	.section	.rdata$_ZTS1C,"dr"
	.linkonce same_size
_ZTS1C:
	.ascii "1C\0"
	.globl	_ZTI1C
	.section	.rdata$_ZTI1C,"dr"
	.linkonce same_size
	.align 8
_ZTI1C:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS1C
	.quad	_ZTI1A
	.globl	_ZTS1D
	.section	.rdata$_ZTS1D,"dr"
	.linkonce same_size
_ZTS1D:
	.ascii "1D\0"
	.globl	_ZTI1D
	.section	.rdata$_ZTI1D,"dr"
	.linkonce same_size
	.align 8
_ZTI1D:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS1D
	.quad	_ZTI1A
	.globl	_ZTV1A
	.section	.rdata$_ZTV1A,"dr"
	.linkonce same_size
	.align 8
_ZTV1A:
	.quad	0
	.quad	_ZTI1A
	.quad	_ZN1A1fEv
	.quad	_ZN1AD1Ev
	.quad	_ZN1AD0Ev
	.globl	_ZTV1B
	.section	.rdata$_ZTV1B,"dr"
	.linkonce same_size
	.align 8
_ZTV1B:
	.quad	0
	.quad	_ZTI1B
	.quad	_ZN1B1fEv
	.quad	_ZN1BD1Ev
	.quad	_ZN1BD0Ev
	.globl	_ZTV1C
	.section	.rdata$_ZTV1C,"dr"
	.linkonce same_size
	.align 8
_ZTV1C:
	.quad	0
	.quad	_ZTI1C
	.quad	_ZN1C1fEv
	.quad	_ZN1CD1Ev
	.quad	_ZN1CD0Ev
	.globl	_ZTV1D
	.section	.rdata$_ZTV1D,"dr"
	.linkonce same_size
	.align 8
_ZTV1D:
	.quad	0
	.quad	_ZTI1D
	.quad	_ZN1D1fEv
	.quad	_ZN1DD1Ev
	.quad	_ZN1DD0Ev
.lcomm _ZL6g_sink,8,8
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1104006501
	.align 8
.LC1:
	.long	0
	.long	1072693248
	.align 8
.LC3:
	.long	0
	.long	1074266112
	.align 8
.LC7:
	.long	0
	.long	1098060496
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
