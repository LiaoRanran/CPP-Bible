	.file	"_ch110_lockfree_perf.cpp"
	.text
	.p2align 4
	.def	_ZL9probe_nopy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_nopy
_ZL9probe_nopy:
.LFB9333:
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
	.def	_ZL11probe_fetchy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_fetchy
_ZL11probe_fetchy:
.LFB9336:
	.seh_endprologue
	testq	%rcx, %rcx
	je	.L13
	xorl	%eax, %eax
	testb	$1, %cl
	je	.L14
	lock addq	$1, g_a(%rip)
	movl	$1, %eax
	cmpq	$1, %rcx
	je	.L13
	.p2align 4,,10
	.p2align 3
.L14:
	lock addq	$1, g_a(%rip)
	lock addq	$1, g_a(%rip)
	addq	$2, %rax
	cmpq	%rax, %rcx
	jne	.L14
.L13:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL9probe_casy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_casy
_ZL9probe_casy:
.LFB9335:
	.seh_endprologue
	testq	%rcx, %rcx
	je	.L25
	xorl	%edx, %edx
	.p2align 4,,10
	.p2align 3
.L26:
	movq	g_a(%rip), %rax
	leaq	1(%rax), %r8
	lock cmpxchgq	%r8, g_a(%rip)
	addq	$1, %rdx
	cmpq	%rdx, %rcx
	jne	.L26
.L25:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL11probe_mutexy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_mutexy
_ZL11probe_mutexy:
.LFB9334:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	testq	%rcx, %rcx
	movq	%rcx, %rdi
	je	.L32
	leaq	g_mtx(%rip), %rsi
	xorl	%ebx, %ebx
	.p2align 4,,10
	.p2align 3
.L34:
	movq	%rsi, %rcx
	call	pthread_mutex_lock
	testl	%eax, %eax
	jne	.L39
	movq	%rsi, %rcx
	addq	$1, %rbx
	call	pthread_mutex_unlock
	cmpq	%rbx, %rdi
	jne	.L34
.L32:
	xorl	%eax, %eax
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
.L39:
	movl	%eax, %ecx
	call	_ZSt20__throw_system_errori
	nop
	.seh_endproc
	.p2align 4
	.def	__tcf_1;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_1
__tcf_1:
.LFB9549:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	g_mtx(%rip), %rcx
	call	pthread_mutex_destroy
	nop
	addq	$40, %rsp
	ret
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA9549:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9549-.LLSDACSB9549
.LLSDACSB9549:
.LLSDACSE9549:
	.text
	.seh_endproc
	.p2align 4
	.def	_ZL5benchPFyyEyi.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5benchPFyyEyi.constprop.0
_ZL5benchPFyyEyi.constprop.0:
.LFB9551:
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
.L42:
/APP
 # 16 "_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$5000000, %ecx
	movq	%rax, %rdi
	call	*%rbp
	movq	%rax, g_sink(%rip)
/APP
 # 16 "_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rdi, %rax
	cmpq	%rax, %rbx
	cmova	%rax, %rbx
	subl	$1, %esi
	jne	.L42
	testq	%rbx, %rbx
	js	.L43
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rbx, %xmm0
.L44:
	divsd	.LC0(%rip), %xmm0
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L43:
	movq	%rbx, %rax
	andl	$1, %ebx
	pxor	%xmm0, %xmm0
	shrq	%rax
	orq	%rbx, %rax
	cvtsi2sdq	%rax, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L44
	.seh_endproc
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB1982:
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
	.ascii "TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64, uncontended single-thread)\12\0"
.LC3:
	.ascii "ns/op\0"
.LC4:
	.ascii "cyc/op\0"
.LC5:
	.ascii "op\0"
.LC6:
	.ascii "%-12s %10s %10s %12s\12\0"
.LC7:
	.ascii "raw(cyc)\0"
.LC8:
	.ascii "mutex\0"
.LC9:
	.ascii "%-12s %10.2f %10.3f %12.2f\12\0"
.LC10:
	.ascii "CAS\0"
.LC11:
	.ascii "fetch_add\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB9338:
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
 # 16 "_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$100, %ecx
	movq	%rax, %rbx
	call	*__imp_Sleep(%rip)
	leaq	88(%rsp), %rcx
	call	*%rsi
/APP
 # 16 "_ch110_lockfree_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rbx, %rax
	js	.L48
	pxor	%xmm6, %xmm6
	cvtsi2sdq	%rax, %xmm6
.L49:
	movq	88(%rsp), %rax
	pxor	%xmm0, %xmm0
	pxor	%xmm1, %xmm1
	leaq	.LC2(%rip), %rcx
	subq	80(%rsp), %rax
	leaq	.LC9(%rip), %rbx
	cvtsi2sdq	72(%rsp), %xmm1
	cvtsi2sdq	%rax, %xmm0
	divsd	%xmm1, %xmm0
	divsd	%xmm0, %xmm6
	divsd	.LC1(%rip), %xmm6
	movapd	%xmm6, %xmm1
	movq	%xmm6, %rdx
	call	_Z6printfPKcz
	leaq	_ZL9probe_nopy(%rip), %rcx
	call	_ZL5benchPFyyEyi.constprop.0
	leaq	_ZL11probe_mutexy(%rip), %rcx
	movapd	%xmm0, %xmm7
	call	_ZL5benchPFyyEyi.constprop.0
	leaq	_ZL9probe_casy(%rip), %rcx
	movapd	%xmm0, %xmm10
	call	_ZL5benchPFyyEyi.constprop.0
	leaq	_ZL11probe_fetchy(%rip), %rcx
	movapd	%xmm0, %xmm9
	call	_ZL5benchPFyyEyi.constprop.0
	movapd	%xmm10, %xmm2
	movapd	%xmm9, %xmm12
	subsd	%xmm7, %xmm2
	movapd	%xmm0, %xmm11
	movapd	%xmm0, %xmm8
	subsd	%xmm7, %xmm12
	leaq	.LC7(%rip), %rax
	subsd	%xmm7, %xmm11
	movq	%rax, 32(%rsp)
	leaq	.LC3(%rip), %r9
	movapd	%xmm2, %xmm3
	movsd	%xmm2, 56(%rsp)
	divsd	%xmm6, %xmm3
	movapd	%xmm12, %xmm13
	leaq	.LC4(%rip), %r8
	movapd	%xmm11, %xmm7
	leaq	.LC5(%rip), %rdx
	leaq	.LC6(%rip), %rcx
	divsd	%xmm6, %xmm13
	movsd	%xmm3, 48(%rsp)
	call	_Z6printfPKcz
	movsd	48(%rsp), %xmm3
	movsd	%xmm10, 32(%rsp)
	movq	%rbx, %rcx
	movsd	56(%rsp), %xmm2
	leaq	.LC8(%rip), %rdx
	movq	%xmm3, %r9
	movq	%xmm2, %r8
	call	_Z6printfPKcz
	movsd	%xmm9, 32(%rsp)
	movapd	%xmm12, %xmm2
	movq	%rbx, %rcx
	leaq	.LC10(%rip), %rdx
	movq	%xmm12, %r8
	divsd	%xmm6, %xmm7
	movapd	%xmm13, %xmm3
	movq	%xmm13, %r9
	call	_Z6printfPKcz
	movsd	%xmm8, 32(%rsp)
	movq	%rbx, %rcx
	movapd	%xmm11, %xmm2
	leaq	.LC11(%rip), %rdx
	movq	%xmm11, %r8
	movapd	%xmm7, %xmm3
	movq	%xmm7, %r9
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
.L48:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm6, %xmm6
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm6
	addsd	%xmm6, %xmm6
	jmp	.L49
	.seh_endproc
	.p2align 4
	.def	_GLOBAL__sub_I_g_mtx;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I_g_mtx
_GLOBAL__sub_I_g_mtx:
.LFB9550:
	subq	$40, %rsp
	.seh_stackalloc	40
	.seh_endprologue
	leaq	g_mtx(%rip), %rcx
	xorl	%edx, %edx
	call	pthread_mutex_init
	leaq	__tcf_1(%rip), %rcx
	addq	$40, %rsp
	jmp	atexit
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA9550:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9550-.LLSDACSB9550
.LLSDACSB9550:
.LLSDACSE9550:
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
.LC0:
	.long	0
	.long	1095963344
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
