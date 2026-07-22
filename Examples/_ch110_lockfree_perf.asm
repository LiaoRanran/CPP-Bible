	.file	"_ch110_lockfree_perf.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	_ZL9probe_nopy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_nopy
_ZL9probe_nopy:
.LFB10134:
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
	.def	_ZL11probe_fetchy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_fetchy
_ZL11probe_fetchy:
.LFB10137:
	.seh_endprologue
	test	rcx, rcx
	je	.L13
	xor	eax, eax
	test	cl, 1
	je	.L14
	lock add	QWORD PTR g_a[rip], 1
	mov	eax, 1
	cmp	rcx, 1
	je	.L13
	.p2align 5
	.p2align 4
	.p2align 3
.L14:
	lock add	QWORD PTR g_a[rip], 1
	lock add	QWORD PTR g_a[rip], 1
	add	rax, 2
	cmp	rcx, rax
	jne	.L14
.L13:
	xor	eax, eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL9probe_casy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_casy
_ZL9probe_casy:
.LFB10136:
	.seh_endprologue
	test	rcx, rcx
	je	.L25
	xor	edx, edx
	.p2align 5
	.p2align 4
	.p2align 3
.L26:
	mov	rax, QWORD PTR g_a[rip]
	lea	r8, 1[rax]
	lock cmpxchg	QWORD PTR g_a[rip], r8
	add	rdx, 1
	cmp	rcx, rdx
	jne	.L26
.L25:
	xor	eax, eax
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.def	_ZL11probe_mutexy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_mutexy
_ZL11probe_mutexy:
.LFB10135:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	rsi, rcx
	test	rcx, rcx
	je	.L32
	xor	ebx, ebx
	.p2align 4
	.p2align 3
.L34:
	lea	rcx, g_mtx[rip]
	call	pthread_mutex_lock
	test	eax, eax
	jne	.L39
	lea	rcx, g_mtx[rip]
	add	rbx, 1
	call	pthread_mutex_unlock
	cmp	rsi, rbx
	jne	.L34
.L32:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_ZL11probe_mutexy.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_mutexy.cold
	.seh_stackalloc	56
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_endprologue
_ZL11probe_mutexy.cold:
.L39:
	mov	ecx, eax
	call	_ZSt20__throw_system_errori
	nop
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.def	__tcfg_mtx;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcfg_mtx
__tcfg_mtx:
.LFB10362:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, g_mtx[rip]
	call	pthread_mutex_destroy
	nop
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA10362:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE10362-.LLSDACSB10362
.LLSDACSB10362:
.LLSDACSE10362:
	.text
	.seh_endproc
	.p2align 4
	.def	_ZL5benchPFyyEyi.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5benchPFyyEyi.constprop.0
_ZL5benchPFyyEyi.constprop.0:
.LFB10364:
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
.L42:
/APP
 # 16 "Examples\_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 5000000
	mov	rdi, rax
	call	rbp
	mov	QWORD PTR g_sink[rip], rax
/APP
 # 16 "Examples\_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rdi
	cmp	rbx, rax
	cmova	rbx, rax
	sub	esi, 1
	jne	.L42
	test	rbx, rbx
	js	.L43
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rbx
.L44:
	divsd	xmm0, QWORD PTR .LC1[rip]
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L43:
	mov	rax, rbx
	and	ebx, 1
	pxor	xmm0, xmm0
	shr	rax
	or	rax, rbx
	cvtsi2sd	xmm0, rax
	addsd	xmm0, xmm0
	jmp	.L44
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC3:
	.ascii "TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64, uncontended single-thread)\12\0"
.LC4:
	.ascii "ns/op\0"
.LC5:
	.ascii "cyc/op\0"
.LC6:
	.ascii "op\0"
.LC7:
	.ascii "%-12s %10s %10s %12s\12\0"
.LC8:
	.ascii "raw(cyc)\0"
.LC9:
	.ascii "mutex\0"
.LC10:
	.ascii "%-12s %10.2f %10.3f %12.2f\12\0"
.LC11:
	.ascii "CAS\0"
.LC12:
	.ascii "fetch_add\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB10139:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 200
	.seh_stackalloc	200
	movaps	XMMWORD PTR 112[rsp], xmm6
	.seh_savexmm	xmm6, 112
	movaps	XMMWORD PTR 128[rsp], xmm7
	.seh_savexmm	xmm7, 128
	movaps	XMMWORD PTR 144[rsp], xmm8
	.seh_savexmm	xmm8, 144
	movaps	XMMWORD PTR 160[rsp], xmm9
	.seh_savexmm	xmm9, 160
	movaps	XMMWORD PTR 176[rsp], xmm10
	.seh_savexmm	xmm10, 176
	.seh_endprologue
	call	__main
	lea	rcx, 88[rsp]
	call	[QWORD PTR __imp_QueryPerformanceFrequency[rip]]
	mov	rsi, QWORD PTR __imp_QueryPerformanceCounter[rip]
	lea	rcx, 96[rsp]
	call	rsi
/APP
 # 16 "Examples\_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	mov	ecx, 100
	mov	rbx, rax
	call	[QWORD PTR __imp_Sleep[rip]]
	lea	rcx, 104[rsp]
	call	rsi
/APP
 # 16 "Examples\_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sub	rax, rbx
	js	.L47
	pxor	xmm1, xmm1
	cvtsi2sd	xmm1, rax
.L48:
	mov	rax, QWORD PTR 104[rsp]
	pxor	xmm0, xmm0
	sub	rax, QWORD PTR 96[rsp]
	pxor	xmm2, xmm2
	cvtsi2sd	xmm0, rax
	cvtsi2sd	xmm2, QWORD PTR 88[rsp]
	divsd	xmm0, xmm2
	lea	rcx, .LC3[rip]
	divsd	xmm1, xmm0
	divsd	xmm1, QWORD PTR .LC2[rip]
	movq	rdx, xmm1
	movsd	QWORD PTR 56[rsp], xmm1
	call	__mingw_printf
	lea	rcx, _ZL9probe_nopy[rip]
	call	_ZL5benchPFyyEyi.constprop.0
	lea	rcx, _ZL11probe_mutexy[rip]
	movapd	xmm8, xmm0
	call	_ZL5benchPFyyEyi.constprop.0
	lea	rcx, _ZL9probe_casy[rip]
	movapd	xmm10, xmm0
	call	_ZL5benchPFyyEyi.constprop.0
	lea	rcx, _ZL11probe_fetchy[rip]
	movapd	xmm9, xmm0
	call	_ZL5benchPFyyEyi.constprop.0
	movapd	xmm7, xmm9
	movapd	xmm2, xmm10
	movsd	xmm1, QWORD PTR 56[rsp]
	subsd	xmm2, xmm8
	subsd	xmm7, xmm8
	movapd	xmm6, xmm0
	movsd	QWORD PTR 56[rsp], xmm0
	subsd	xmm6, xmm8
	lea	rax, .LC8[rip]
	mov	QWORD PTR 32[rsp], rax
	lea	r9, .LC4[rip]
	lea	r8, .LC5[rip]
	movapd	xmm3, xmm2
	movapd	xmm4, xmm7
	lea	rdx, .LC6[rip]
	movsd	QWORD PTR 72[rsp], xmm2
	divsd	xmm3, xmm1
	movapd	xmm8, xmm6
	lea	rcx, .LC7[rip]
	divsd	xmm4, xmm1
	movsd	QWORD PTR 64[rsp], xmm3
	divsd	xmm8, xmm1
	movq	rbx, xmm4
	call	__mingw_printf
	movsd	xmm3, QWORD PTR 64[rsp]
	movsd	xmm2, QWORD PTR 72[rsp]
	movsd	QWORD PTR 32[rsp], xmm10
	lea	rdx, .LC9[rip]
	lea	rcx, .LC10[rip]
	movq	r9, xmm3
	movq	r8, xmm2
	call	__mingw_printf
	movsd	QWORD PTR 32[rsp], xmm9
	mov	r9, rbx
	movapd	xmm2, xmm7
	movq	xmm3, rbx
	movq	r8, xmm7
	lea	rdx, .LC11[rip]
	lea	rcx, .LC10[rip]
	call	__mingw_printf
	movsd	xmm0, QWORD PTR 56[rsp]
	movapd	xmm2, xmm6
	movq	r8, xmm6
	lea	rdx, .LC12[rip]
	lea	rcx, .LC10[rip]
	movsd	QWORD PTR 32[rsp], xmm0
	movapd	xmm3, xmm8
	movq	r9, xmm8
	call	__mingw_printf
	nop
	movaps	xmm6, XMMWORD PTR 112[rsp]
	movaps	xmm7, XMMWORD PTR 128[rsp]
	xor	eax, eax
	movaps	xmm8, XMMWORD PTR 144[rsp]
	movaps	xmm9, XMMWORD PTR 160[rsp]
	movaps	xmm10, XMMWORD PTR 176[rsp]
	add	rsp, 200
	pop	rbx
	pop	rsi
	ret
.L47:
	mov	rdx, rax
	and	eax, 1
	pxor	xmm1, xmm1
	shr	rdx
	or	rdx, rax
	cvtsi2sd	xmm1, rdx
	addsd	xmm1, xmm1
	jmp	.L48
	.seh_endproc
	.p2align 4
	.def	_GLOBAL__sub_I_g_mtx;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I_g_mtx
_GLOBAL__sub_I_g_mtx:
.LFB10363:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	xor	edx, edx
	lea	rcx, g_mtx[rip]
	call	pthread_mutex_init
	lea	rcx, __tcfg_mtx[rip]
	add	rsp, 40
.LEHB0:
	jmp	atexit
.LEHE0:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA10363:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE10363-.LLSDACSB10363
.LLSDACSB10363:
	.uleb128 .LEHB0-.LFB10363
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
.LLSDACSE10363:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I_g_mtx
	.globl	g_sink
	.bss
	.align 8
g_sink:
	.space 8
	.globl	g_a
	.align 8
g_a:
	.space 8
	.globl	g_mtx
	.align 8
g_mtx:
	.space 8
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	0
	.long	1095963344
	.align 8
.LC2:
	.long	0
	.long	1104006501
	.def	__main;	.scl	2;	.type	32;	.endef
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
