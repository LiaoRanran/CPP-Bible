	.file	"_ch37_alloc_perf.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10pool_allocv
	.def	_Z10pool_allocv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10pool_allocv
_Z10pool_allocv:
.LFB5839:
	.seh_endprologue
	mov	rax, QWORD PTR _ZL10g_pool_ptr[rip]
	lea	rdx, 16[rax]
	mov	QWORD PTR g_sink[rip], rax
	mov	QWORD PTR _ZL10g_pool_ptr[rip], rdx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z16probe_new_deletev
	.def	_Z16probe_new_deletev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16probe_new_deletev
_Z16probe_new_deletev:
.LFB5840:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 16
	call	_Znwy
	mov	rcx, rax
	mov	rbx, rax
	mov	QWORD PTR g_sink[rip], rax
	call	_ZdlPv
	mov	QWORD PTR g_sink[rip], rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17probe_malloc_freev
	.def	_Z17probe_malloc_freev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17probe_malloc_freev
_Z17probe_malloc_freev:
.LFB5841:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	ecx, 16
	call	malloc
	mov	rcx, rax
	mov	rbx, rax
	mov	QWORD PTR g_sink[rip], rax
	call	free
	mov	QWORD PTR g_sink[rip], rbx
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15probe_placementv
	.def	_Z15probe_placementv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_placementv
_Z15probe_placementv:
.LFB5842:
	.seh_endprologue
	lea	rax, _ZL4g_pb[rip]
	mov	QWORD PTR g_sink[rip], rax
	mov	QWORD PTR g_sink[rip], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z20probe_new_obj_deletev
	.def	_Z20probe_new_obj_deletev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z20probe_new_obj_deletev
_Z20probe_new_obj_deletev:
.LFB5843:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 16
	call	_Znwy
	mov	edx, 16
	mov	rcx, rax
	mov	QWORD PTR g_sink[rip], rax
	call	_ZdlPvy
	mov	QWORD PTR g_sink[rip], 1
	add	rsp, 40
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "TSC calibrated = %.4f GHz\12\0"
	.align 8
.LC3:
	.ascii "operator new + delete : %6.2f cy  %7.3f ns  (round-trip)\12\0"
	.align 8
.LC4:
	.ascii "malloc + free         : %6.2f cy  %7.3f ns  (round-trip)\12\0"
	.align 8
.LC5:
	.ascii "placement new+dtor    : %6.2f cy  %7.3f ns  (no alloc)\12\0"
	.align 8
.LC6:
	.ascii "new Obj + delete      : %6.2f cy  %7.3f ns  (round-trip)\12\0"
	.align 8
.LC7:
	.ascii "pool alloc (bump)     : %6.2f cy  %7.3f ns  (pointer bump)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5845:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 152
	.seh_stackalloc	152
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	movaps	XMMWORD PTR 48[rsp], xmm7
	.seh_savexmm	xmm7, 48
	movaps	XMMWORD PTR 64[rsp], xmm8
	.seh_savexmm	xmm8, 64
	movaps	XMMWORD PTR 80[rsp], xmm9
	.seh_savexmm	xmm9, 80
	movaps	XMMWORD PTR 96[rsp], xmm10
	.seh_savexmm	xmm10, 96
	movaps	XMMWORD PTR 112[rsp], xmm11
	.seh_savexmm	xmm11, 112
	movaps	XMMWORD PTR 128[rsp], xmm12
	.seh_savexmm	xmm12, 128
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbx, rax
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	rsi, rdx
	or	rsi, rax
	.p2align 4
	.p2align 3
.L8:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	sub	rax, rbx
	cmp	rax, 49999999
	jle	.L8
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rcx, rax
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	or	rdx, rax
	sub	rdx, rsi
	js	.L9
	pxor	xmm6, xmm6
	cvtsi2sd	xmm6, rdx
.L10:
	movsd	xmm1, QWORD PTR .LC0[rip]
	sub	rcx, rbx
	pxor	xmm0, xmm0
	mov	ebx, 100000
	cvtsi2sd	xmm0, rcx
	lea	rcx, .LC1[rip]
	divsd	xmm0, xmm1
	divsd	xmm6, xmm0
	divsd	xmm6, xmm1
	movapd	xmm1, xmm6
	movq	rdx, xmm6
	call	__mingw_printf
	.p2align 4
	.p2align 3
.L11:
	call	_Z16probe_new_deletev
	call	_Z16probe_new_deletev
	sub	ebx, 2
	jne	.L11
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	ebx, 2000000
	mov	rsi, rdx
	or	rsi, rax
	.p2align 4
	.p2align 3
.L12:
	call	_Z16probe_new_deletev
	call	_Z16probe_new_deletev
	sub	ebx, 2
	jne	.L12
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	or	rdx, rax
	sub	rdx, rsi
	js	.L13
	pxor	xmm11, xmm11
	cvtsi2sd	xmm11, rdx
.L14:
	movsd	xmm12, QWORD PTR .LC2[rip]
	mov	ebx, 100000
	divsd	xmm11, xmm12
	.p2align 4
	.p2align 3
.L15:
	call	_Z17probe_malloc_freev
	call	_Z17probe_malloc_freev
	sub	ebx, 2
	jne	.L15
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	ebx, 2000000
	mov	rsi, rdx
	or	rsi, rax
	.p2align 4
	.p2align 3
.L16:
	call	_Z17probe_malloc_freev
	call	_Z17probe_malloc_freev
	sub	ebx, 2
	jne	.L16
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	or	rdx, rax
	sub	rdx, rsi
	js	.L17
	pxor	xmm10, xmm10
	cvtsi2sd	xmm10, rdx
.L18:
	divsd	xmm10, xmm12
	mov	edx, 100000
	.p2align 4
	.p2align 3
.L19:
	call	_Z15probe_placementv
	call	_Z15probe_placementv
	sub	edx, 2
	jne	.L19
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	rcx, rdx
	mov	edx, 2000000
	or	rcx, rax
	.p2align 4
	.p2align 3
.L20:
	call	_Z15probe_placementv
	call	_Z15probe_placementv
	sub	edx, 2
	jne	.L20
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	or	rdx, rax
	sub	rdx, rcx
	js	.L21
	pxor	xmm9, xmm9
	cvtsi2sd	xmm9, rdx
.L22:
	divsd	xmm9, xmm12
	mov	ebx, 100000
	.p2align 4
	.p2align 3
.L23:
	call	_Z20probe_new_obj_deletev
	call	_Z20probe_new_obj_deletev
	sub	ebx, 2
	jne	.L23
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	ebx, 2000000
	mov	rsi, rdx
	or	rsi, rax
	.p2align 4
	.p2align 3
.L24:
	call	_Z20probe_new_obj_deletev
	call	_Z20probe_new_obj_deletev
	sub	ebx, 2
	jne	.L24
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	or	rdx, rax
	sub	rdx, rsi
	js	.L25
	pxor	xmm8, xmm8
	cvtsi2sd	xmm8, rdx
.L26:
	divsd	xmm8, xmm12
	mov	ecx, 100000
	.p2align 4
	.p2align 3
.L27:
	call	_Z10pool_allocv
	call	_Z10pool_allocv
	sub	ecx, 2
	jne	.L27
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	mov	ecx, 2000000
	or	rdx, rax
	mov	r8, rdx
	.p2align 4
	.p2align 3
.L28:
	call	_Z10pool_allocv
	call	_Z10pool_allocv
	sub	ecx, 2
	jne	.L28
/APP
 # 17 "Examples\_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	sal	rdx, 32
	or	rdx, rax
	sub	rdx, r8
	js	.L29
	pxor	xmm7, xmm7
	cvtsi2sd	xmm7, rdx
.L30:
	movapd	xmm3, xmm11
	movapd	xmm1, xmm11
	movq	rdx, xmm11
	divsd	xmm3, xmm6
	lea	rcx, .LC3[rip]
	divsd	xmm7, xmm12
	movq	r8, xmm3
	movapd	xmm2, xmm3
	call	__mingw_printf
	movapd	xmm4, xmm10
	movapd	xmm1, xmm10
	movq	rdx, xmm10
	lea	rcx, .LC4[rip]
	divsd	xmm4, xmm6
	movq	r8, xmm4
	movapd	xmm2, xmm4
	call	__mingw_printf
	movapd	xmm5, xmm9
	movapd	xmm1, xmm9
	movq	rdx, xmm9
	divsd	xmm5, xmm6
	lea	rcx, .LC5[rip]
	movq	r8, xmm5
	movapd	xmm2, xmm5
	call	__mingw_printf
	movapd	xmm3, xmm8
	movapd	xmm1, xmm8
	movq	rdx, xmm8
	divsd	xmm3, xmm6
	lea	rcx, .LC6[rip]
	movq	r8, xmm3
	movapd	xmm2, xmm3
	call	__mingw_printf
	movapd	xmm4, xmm7
	movapd	xmm1, xmm7
	movq	rdx, xmm7
	divsd	xmm4, xmm6
	lea	rcx, .LC7[rip]
	movq	r8, xmm4
	movapd	xmm2, xmm4
	call	__mingw_printf
	nop
	movaps	xmm6, XMMWORD PTR 32[rsp]
	movaps	xmm7, XMMWORD PTR 48[rsp]
	xor	eax, eax
	movaps	xmm8, XMMWORD PTR 64[rsp]
	movaps	xmm9, XMMWORD PTR 80[rsp]
	movaps	xmm10, XMMWORD PTR 96[rsp]
	movaps	xmm11, XMMWORD PTR 112[rsp]
	movaps	xmm12, XMMWORD PTR 128[rsp]
	add	rsp, 152
	pop	rbx
	pop	rsi
	ret
.L9:
	mov	rax, rdx
	and	edx, 1
	pxor	xmm6, xmm6
	shr	rax
	or	rax, rdx
	cvtsi2sd	xmm6, rax
	addsd	xmm6, xmm6
	jmp	.L10
.L29:
	mov	rax, rdx
	and	edx, 1
	pxor	xmm7, xmm7
	shr	rax
	or	rax, rdx
	cvtsi2sd	xmm7, rax
	addsd	xmm7, xmm7
	jmp	.L30
.L25:
	mov	rax, rdx
	and	edx, 1
	pxor	xmm8, xmm8
	shr	rax
	or	rax, rdx
	cvtsi2sd	xmm8, rax
	addsd	xmm8, xmm8
	jmp	.L26
.L21:
	mov	rax, rdx
	and	edx, 1
	pxor	xmm9, xmm9
	shr	rax
	or	rax, rdx
	cvtsi2sd	xmm9, rax
	addsd	xmm9, xmm9
	jmp	.L22
.L17:
	mov	rax, rdx
	and	edx, 1
	pxor	xmm10, xmm10
	shr	rax
	or	rax, rdx
	cvtsi2sd	xmm10, rax
	addsd	xmm10, xmm10
	jmp	.L18
.L13:
	mov	rax, rdx
	and	edx, 1
	pxor	xmm11, xmm11
	shr	rax
	or	rax, rdx
	cvtsi2sd	xmm11, rax
	addsd	xmm11, xmm11
	jmp	.L14
	.seh_endproc
.lcomm _ZL4g_pb,16,4
	.data
	.align 8
_ZL10g_pool_ptr:
	.quad	_ZL6g_pool
.lcomm _ZL6g_pool,32000000,16
	.globl	g_sink
	.bss
	.align 8
g_sink:
	.space 8
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1104006501
	.align 8
.LC2:
	.long	0
	.long	1094616192
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
