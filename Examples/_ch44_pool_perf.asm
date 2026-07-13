	.file	"_ch44_pool_perf.cpp"
	.text
	.p2align 4
	.def	_ZL9probe_nopy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_nopy
_ZL9probe_nopy:
.LFB9071:
	.seh_endprologue
	testq	%rcx, %rcx
	je	.L4
	xorl	%eax, %eax
	xorl	%edx, %edx
	testb	$1, %cl
	je	.L3
	cmpq	$1, %rcx
	movl	$1, %eax
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	leaq	1(%rdx,%rax,2), %rdx
	addq	$2, %rax
	cmpq	%rax, %rcx
	jne	.L3
.L1:
	movq	%rdx, %rax
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xorl	%edx, %edx
	movq	%rdx, %rax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL10probe_bumpy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL10probe_bumpy
_ZL10probe_bumpy:
.LFB9072:
	.seh_endprologue
	movq	_ZL6g_bump(%rip), %rax
	testq	%rcx, %rcx
	je	.L13
	xorl	%edx, %edx
	.p2align 4,,10
	.p2align 3
.L14:
	addq	$1, %rdx
	movq	%rax, %r8
	addq	$16, %rax
	cmpq	%rdx, %rcx
	movq	%r8, g_sink(%rip)
	jne	.L14
.L13:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL14probe_freelisty;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL14probe_freelisty
_ZL14probe_freelisty:
.LFB9073:
	.seh_endprologue
	movq	_ZL10g_fl_head0(%rip), %rax
	testq	%rcx, %rcx
	je	.L20
	xorl	%edx, %edx
	.p2align 4,,10
	.p2align 3
.L21:
	addq	$1, %rdx
	movq	%rax, %r8
	movq	(%rax), %rax
	cmpq	%rdx, %rcx
	movq	%r8, g_sink(%rip)
	jne	.L21
.L20:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL12probe_mallocy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL12probe_mallocy
_ZL12probe_mallocy:
.LFB9074:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	testq	%rcx, %rcx
	movq	%rcx, %rsi
	je	.L27
	xorl	%ebx, %ebx
	.p2align 4,,10
	.p2align 3
.L28:
	movl	$16, %ecx
	addq	$1, %rbx
	call	malloc
	movq	%rax, %rcx
	movq	%rax, g_sink(%rip)
	call	free
	cmpq	%rbx, %rsi
	jne	.L28
.L27:
	xorl	%eax, %eax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL5benchPFyyEyi.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5benchPFyyEyi.constprop.0
_ZL5benchPFyyEyi.constprop.0:
.LFB9103:
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	movl	$20, %esi
	movq	$-1, %rbx
	movq	%rcx, %rbp
	.p2align 4,,10
	.p2align 3
.L34:
/APP
 # 18 "_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$4000000, %ecx
	movq	%rax, %rdi
	call	*%rbp
	movq	%rax, g_sink(%rip)
/APP
 # 18 "_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rdi, %rax
	cmpq	%rax, %rbx
	cmova	%rax, %rbx
	subl	$1, %esi
	jne	.L34
	testq	%rbx, %rbx
	js	.L35
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rbx, %xmm0
.L36:
	divsd	.LC0(%rip), %xmm0
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L35:
	movq	%rbx, %rax
	andl	$1, %ebx
	pxor	%xmm0, %xmm0
	shrq	%rax
	orq	%rbx, %rax
	cvtsi2sdq	%rax, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L36
	.seh_endproc
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB11:
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
	.def	__main;	.scl	2;	.type	32;	.endef
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
.LFB9076:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$232, %rsp
	.seh_stackalloc	232
	movaps	%xmm6, 96(%rsp)
	.seh_savexmm	%xmm6, 96
	movaps	%xmm7, 112(%rsp)
	.seh_savexmm	%xmm7, 112
	movaps	%xmm8, 128(%rsp)
	.seh_savexmm	%xmm8, 128
	movaps	%xmm9, 144(%rsp)
	.seh_savexmm	%xmm9, 144
	movaps	%xmm10, 160(%rsp)
	.seh_savexmm	%xmm10, 160
	movaps	%xmm11, 176(%rsp)
	.seh_savexmm	%xmm11, 176
	movaps	%xmm12, 192(%rsp)
	.seh_savexmm	%xmm12, 192
	movaps	%xmm13, 208(%rsp)
	.seh_savexmm	%xmm13, 208
	.seh_endprologue
	call	__main
	leaq	72(%rsp), %rcx
	call	*__imp_QueryPerformanceFrequency(%rip)
	movq	__imp_QueryPerformanceCounter(%rip), %rsi
	leaq	80(%rsp), %rcx
	call	*%rsi
/APP
 # 18 "_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$100, %ecx
	movq	%rax, %rbx
	call	*__imp_Sleep(%rip)
	leaq	88(%rsp), %rcx
	call	*%rsi
/APP
 # 18 "_ch44_pool_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rbx, %rax
	js	.L40
	pxor	%xmm12, %xmm12
	cvtsi2sdq	%rax, %xmm12
.L41:
	movq	88(%rsp), %rax
	pxor	%xmm0, %xmm0
	pxor	%xmm1, %xmm1
	leaq	.LC2(%rip), %rcx
	cvtsi2sdq	72(%rsp), %xmm1
	subq	80(%rsp), %rax
	cvtsi2sdq	%rax, %xmm0
	divsd	%xmm1, %xmm0
	divsd	%xmm0, %xmm12
	divsd	.LC1(%rip), %xmm12
	movq	%xmm12, %rdx
	movapd	%xmm12, %xmm1
	call	_Z6printfPKcz
	movl	$64000064, %ecx
	call	malloc
	movl	$64000000, %ecx
	movq	$64000000, 16+_ZL6g_bump(%rip)
	movq	%rax, %xmm0
	punpcklqdq	%xmm0, %xmm0
	movaps	%xmm0, _ZL6g_bump(%rip)
	call	malloc
	leaq	16(%rax), %rdx
	leaq	64000000(%rax), %r8
	.p2align 4,,10
	.p2align 3
.L42:
	movq	%rdx, -16(%rdx)
	leaq	16(%rdx), %rcx
	addq	$32, %rdx
	movq	%rcx, -16(%rcx)
	movq	%rdx, -16(%rdx)
	leaq	32(%rcx), %rdx
	cmpq	%r8, %rdx
	jne	.L42
	leaq	_ZL9probe_nopy(%rip), %rcx
	movq	%rax, _ZL10g_fl_head0(%rip)
	movq	$0, 63999984(%rax)
	leaq	.LC9(%rip), %rbx
	call	_ZL5benchPFyyEyi.constprop.0
	leaq	_ZL10probe_bumpy(%rip), %rcx
	movapd	%xmm0, %xmm6
	call	_ZL5benchPFyyEyi.constprop.0
	leaq	_ZL14probe_freelisty(%rip), %rcx
	movapd	%xmm0, %xmm9
	call	_ZL5benchPFyyEyi.constprop.0
	leaq	_ZL12probe_mallocy(%rip), %rcx
	movapd	%xmm0, %xmm8
	call	_ZL5benchPFyyEyi.constprop.0
	movapd	%xmm9, %xmm2
	movapd	%xmm8, %xmm11
	subsd	%xmm6, %xmm2
	movapd	%xmm0, %xmm10
	movapd	%xmm0, %xmm7
	subsd	%xmm6, %xmm11
	leaq	.LC7(%rip), %rax
	subsd	%xmm6, %xmm10
	movq	%rax, 32(%rsp)
	leaq	.LC3(%rip), %r9
	movapd	%xmm2, %xmm3
	movsd	%xmm2, 56(%rsp)
	divsd	%xmm12, %xmm3
	movapd	%xmm11, %xmm13
	leaq	.LC4(%rip), %r8
	movapd	%xmm10, %xmm6
	leaq	.LC5(%rip), %rdx
	leaq	.LC6(%rip), %rcx
	divsd	%xmm12, %xmm13
	movsd	%xmm3, 48(%rsp)
	call	_Z6printfPKcz
	movsd	48(%rsp), %xmm3
	movsd	%xmm9, 32(%rsp)
	movq	%rbx, %rcx
	movsd	56(%rsp), %xmm2
	leaq	.LC8(%rip), %rdx
	movq	%xmm3, %r9
	movq	%xmm2, %r8
	call	_Z6printfPKcz
	movsd	%xmm8, 32(%rsp)
	movapd	%xmm11, %xmm2
	movq	%rbx, %rcx
	leaq	.LC10(%rip), %rdx
	movq	%xmm11, %r8
	divsd	%xmm12, %xmm6
	movapd	%xmm13, %xmm3
	movq	%xmm13, %r9
	call	_Z6printfPKcz
	movsd	%xmm7, 32(%rsp)
	movq	%rbx, %rcx
	movapd	%xmm10, %xmm2
	leaq	.LC11(%rip), %rdx
	movq	%xmm10, %r8
	movapd	%xmm6, %xmm3
	movq	%xmm6, %r9
	call	_Z6printfPKcz
	nop
	movaps	96(%rsp), %xmm6
	xorl	%eax, %eax
	movaps	112(%rsp), %xmm7
	movaps	128(%rsp), %xmm8
	movaps	144(%rsp), %xmm9
	movaps	160(%rsp), %xmm10
	movaps	176(%rsp), %xmm11
	movaps	192(%rsp), %xmm12
	movaps	208(%rsp), %xmm13
	addq	$232, %rsp
	popq	%rbx
	popq	%rsi
	ret
.L40:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm12, %xmm12
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm12
	addsd	%xmm12, %xmm12
	jmp	.L41
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
