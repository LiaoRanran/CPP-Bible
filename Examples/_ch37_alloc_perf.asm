	.file	"_ch37_alloc_perf.cpp"
	.text
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB25:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$56, %rsp
	.seh_stackalloc	56
	.seh_endprologue
	leaq	88(%rsp), %rsi
	movq	%rcx, %rbx
	movq	%rdx, 88(%rsp)
	movl	$1, %ecx
	movq	%r8, 96(%rsp)
	movq	%r9, 104(%rsp)
	movq	%rsi, 40(%rsp)
	call	*__imp___acrt_iob_func(%rip)
	movq	%rsi, %r8
	movq	%rbx, %rdx
	movq	%rax, %rcx
	call	__mingw_vfprintf
	addq	$56, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z10pool_allocv
	.def	_Z10pool_allocv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10pool_allocv
_Z10pool_allocv:
.LFB5572:
	.seh_endprologue
	movq	_ZL10g_pool_ptr(%rip), %rax
	leaq	16(%rax), %rdx
	movq	%rax, g_sink(%rip)
	movq	%rdx, _ZL10g_pool_ptr(%rip)
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z16probe_new_deletev
	.def	_Z16probe_new_deletev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16probe_new_deletev
_Z16probe_new_deletev:
.LFB5573:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movl	$16, %ecx
	call	_Znwy
	movq	%rax, %rcx
	movq	%rax, %rbx
	movq	%rax, g_sink(%rip)
	call	_ZdlPv
	movq	%rbx, g_sink(%rip)
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z17probe_malloc_freev
	.def	_Z17probe_malloc_freev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17probe_malloc_freev
_Z17probe_malloc_freev:
.LFB5574:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movl	$16, %ecx
	call	malloc
	movq	%rax, %rcx
	movq	%rax, %rbx
	movq	%rax, g_sink(%rip)
	call	free
	movq	%rbx, g_sink(%rip)
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z15probe_placementv
	.def	_Z15probe_placementv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_placementv
_Z15probe_placementv:
.LFB5575:
	.seh_endprologue
	leaq	_ZL4g_pb(%rip), %rax
	movq	%rax, g_sink(%rip)
	movq	$1, g_sink(%rip)
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z20probe_new_obj_deletev
	.def	_Z20probe_new_obj_deletev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z20probe_new_obj_deletev
_Z20probe_new_obj_deletev:
.LFB5576:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movl	$16, %ecx
	call	_Znwy
	movl	$16, %edx
	movq	%rax, %rcx
	movq	%rax, g_sink(%rip)
	call	_ZdlPvy
	movq	$1, g_sink(%rip)
	addq	$40, %rsp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
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
.LFB5578:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$152, %rsp
	.seh_stackalloc	152
	movaps	%xmm6, 32(%rsp)
	.seh_savexmm	%xmm6, 32
	movaps	%xmm7, 48(%rsp)
	.seh_savexmm	%xmm7, 48
	movaps	%xmm8, 64(%rsp)
	.seh_savexmm	%xmm8, 64
	movaps	%xmm9, 80(%rsp)
	.seh_savexmm	%xmm9, 80
	movaps	%xmm10, 96(%rsp)
	.seh_savexmm	%xmm10, 96
	movaps	%xmm11, 112(%rsp)
	.seh_savexmm	%xmm11, 112
	movaps	%xmm12, 128(%rsp)
	.seh_savexmm	%xmm12, 128
	.seh_endprologue
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rbx
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	movq	%rdx, %rsi
	orq	%rax, %rsi
	.p2align 4,,10
	.p2align 3
.L9:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	subq	%rbx, %rax
	cmpq	$49999999, %rax
	jle	.L9
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movq	%rax, %rcx
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	orq	%rax, %rdx
	subq	%rsi, %rdx
	js	.L10
	pxor	%xmm6, %xmm6
	cvtsi2sdq	%rdx, %xmm6
.L11:
	subq	%rbx, %rcx
	pxor	%xmm0, %xmm0
	movsd	.LC0(%rip), %xmm1
	movl	$100000, %ebx
	cvtsi2sdq	%rcx, %xmm0
	leaq	.LC1(%rip), %rcx
	divsd	%xmm1, %xmm0
	divsd	%xmm0, %xmm6
	divsd	%xmm1, %xmm6
	movapd	%xmm6, %xmm1
	movq	%xmm6, %rdx
	call	_Z6printfPKcz
	.p2align 4,,10
	.p2align 3
.L12:
	call	_Z16probe_new_deletev
	call	_Z16probe_new_deletev
	subl	$2, %ebx
	jne	.L12
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	movl	$2000000, %ebx
	movq	%rdx, %rsi
	orq	%rax, %rsi
	.p2align 4,,10
	.p2align 3
.L13:
	call	_Z16probe_new_deletev
	call	_Z16probe_new_deletev
	subl	$2, %ebx
	jne	.L13
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	orq	%rax, %rdx
	subq	%rsi, %rdx
	js	.L14
	pxor	%xmm11, %xmm11
	cvtsi2sdq	%rdx, %xmm11
.L15:
	movsd	.LC2(%rip), %xmm12
	movl	$100000, %ebx
	divsd	%xmm12, %xmm11
	.p2align 4,,10
	.p2align 3
.L16:
	call	_Z17probe_malloc_freev
	call	_Z17probe_malloc_freev
	subl	$2, %ebx
	jne	.L16
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	movl	$2000000, %ebx
	movq	%rdx, %rsi
	orq	%rax, %rsi
	.p2align 4,,10
	.p2align 3
.L17:
	call	_Z17probe_malloc_freev
	call	_Z17probe_malloc_freev
	subl	$2, %ebx
	jne	.L17
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	orq	%rax, %rdx
	subq	%rsi, %rdx
	js	.L18
	pxor	%xmm10, %xmm10
	cvtsi2sdq	%rdx, %xmm10
.L19:
	divsd	%xmm12, %xmm10
	movl	$100000, %edx
	.p2align 4,,10
	.p2align 3
.L20:
	call	_Z15probe_placementv
	call	_Z15probe_placementv
	subl	$2, %edx
	jne	.L20
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	movq	%rdx, %rcx
	movl	$2000000, %edx
	orq	%rax, %rcx
	.p2align 4,,10
	.p2align 3
.L21:
	call	_Z15probe_placementv
	call	_Z15probe_placementv
	subl	$2, %edx
	jne	.L21
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	orq	%rax, %rdx
	subq	%rcx, %rdx
	js	.L22
	pxor	%xmm9, %xmm9
	cvtsi2sdq	%rdx, %xmm9
.L23:
	divsd	%xmm12, %xmm9
	movl	$100000, %ebx
	.p2align 4,,10
	.p2align 3
.L24:
	call	_Z20probe_new_obj_deletev
	call	_Z20probe_new_obj_deletev
	subl	$2, %ebx
	jne	.L24
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	movl	$2000000, %ebx
	movq	%rdx, %rsi
	orq	%rax, %rsi
	.p2align 4,,10
	.p2align 3
.L25:
	call	_Z20probe_new_obj_deletev
	call	_Z20probe_new_obj_deletev
	subl	$2, %ebx
	jne	.L25
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	orq	%rax, %rdx
	subq	%rsi, %rdx
	js	.L26
	pxor	%xmm8, %xmm8
	cvtsi2sdq	%rdx, %xmm8
.L27:
	divsd	%xmm12, %xmm8
	movl	$100000, %ecx
	.p2align 4,,10
	.p2align 3
.L28:
	call	_Z10pool_allocv
	call	_Z10pool_allocv
	subl	$2, %ecx
	jne	.L28
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	movl	$2000000, %ecx
	orq	%rax, %rdx
	movq	%rdx, %r8
	.p2align 4,,10
	.p2align 3
.L29:
	call	_Z10pool_allocv
	call	_Z10pool_allocv
	subl	$2, %ecx
	jne	.L29
/APP
 # 17 "_ch37_alloc_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	salq	$32, %rdx
	orq	%rax, %rdx
	subq	%r8, %rdx
	js	.L30
	pxor	%xmm7, %xmm7
	cvtsi2sdq	%rdx, %xmm7
.L31:
	movapd	%xmm11, %xmm3
	movapd	%xmm11, %xmm1
	movq	%xmm11, %rdx
	divsd	%xmm6, %xmm3
	leaq	.LC3(%rip), %rcx
	divsd	%xmm12, %xmm7
	movq	%xmm3, %r8
	movapd	%xmm3, %xmm2
	call	_Z6printfPKcz
	movapd	%xmm10, %xmm4
	movapd	%xmm10, %xmm1
	movq	%xmm10, %rdx
	leaq	.LC4(%rip), %rcx
	divsd	%xmm6, %xmm4
	movq	%xmm4, %r8
	movapd	%xmm4, %xmm2
	call	_Z6printfPKcz
	movapd	%xmm9, %xmm5
	movapd	%xmm9, %xmm1
	movq	%xmm9, %rdx
	divsd	%xmm6, %xmm5
	leaq	.LC5(%rip), %rcx
	movq	%xmm5, %r8
	movapd	%xmm5, %xmm2
	call	_Z6printfPKcz
	movapd	%xmm8, %xmm3
	movapd	%xmm8, %xmm1
	movq	%xmm8, %rdx
	divsd	%xmm6, %xmm3
	leaq	.LC6(%rip), %rcx
	movq	%xmm3, %r8
	movapd	%xmm3, %xmm2
	call	_Z6printfPKcz
	movapd	%xmm7, %xmm4
	movapd	%xmm7, %xmm1
	movq	%xmm7, %rdx
	divsd	%xmm6, %xmm4
	leaq	.LC7(%rip), %rcx
	movq	%xmm4, %r8
	movapd	%xmm4, %xmm2
	call	_Z6printfPKcz
	nop
	movaps	32(%rsp), %xmm6
	xorl	%eax, %eax
	movaps	48(%rsp), %xmm7
	movaps	64(%rsp), %xmm8
	movaps	80(%rsp), %xmm9
	movaps	96(%rsp), %xmm10
	movaps	112(%rsp), %xmm11
	movaps	128(%rsp), %xmm12
	addq	$152, %rsp
	popq	%rbx
	popq	%rsi
	ret
.L10:
	movq	%rdx, %rax
	andl	$1, %edx
	pxor	%xmm6, %xmm6
	shrq	%rax
	orq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm6
	addsd	%xmm6, %xmm6
	jmp	.L11
.L30:
	movq	%rdx, %rax
	andl	$1, %edx
	pxor	%xmm7, %xmm7
	shrq	%rax
	orq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm7
	addsd	%xmm7, %xmm7
	jmp	.L31
.L26:
	movq	%rdx, %rax
	andl	$1, %edx
	pxor	%xmm8, %xmm8
	shrq	%rax
	orq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm8
	addsd	%xmm8, %xmm8
	jmp	.L27
.L22:
	movq	%rdx, %rax
	andl	$1, %edx
	pxor	%xmm9, %xmm9
	shrq	%rax
	orq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm9
	addsd	%xmm9, %xmm9
	jmp	.L23
.L18:
	movq	%rdx, %rax
	andl	$1, %edx
	pxor	%xmm10, %xmm10
	shrq	%rax
	orq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm10
	addsd	%xmm10, %xmm10
	jmp	.L19
.L14:
	movq	%rdx, %rax
	andl	$1, %edx
	pxor	%xmm11, %xmm11
	shrq	%rax
	orq	%rdx, %rax
	cvtsi2sdq	%rax, %xmm11
	addsd	%xmm11, %xmm11
	jmp	.L15
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
