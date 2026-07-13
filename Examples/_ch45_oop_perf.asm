	.file	"_ch45_oop_perf.cpp"
	.text
	.section	.text$_ZN7Derived4virtEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7Derived4virtEi
	.def	_ZN7Derived4virtEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7Derived4virtEi
_ZN7Derived4virtEi:
.LFB7551:
	.seh_endprologue
	leal	-1(%rdx), %eax
	ret
	.seh_endproc
	.section	.text$_ZN2D24virtEi,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN2D24virtEi
	.def	_ZN2D24virtEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2D24virtEi
_ZN2D24virtEi:
.LFB7552:
	.seh_endprologue
	leal	7(%rdx), %eax
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z7free_fni
	.def	_Z7free_fni;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7free_fni
_Z7free_fni:
.LFB7553:
	.seh_endprologue
	leal	3(%rcx), %eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL9probe_nopi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL9probe_nopi
_ZL9probe_nopi:
.LFB7567:
	.seh_endprologue
	testl	%ecx, %ecx
	jle	.L8
	xorl	%edx, %edx
	xorl	%eax, %eax
	testb	$1, %cl
	je	.L7
	cmpl	$1, %ecx
	movl	$1, %edx
	je	.L15
	.p2align 4,,10
	.p2align 3
.L7:
	leal	1(%rax,%rdx,2), %eax
	addl	$2, %edx
	cmpl	%edx, %ecx
	jne	.L7
.L15:
	cltq
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD1Ev
	.def	_ZN7DerivedD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD1Ev
_ZN7DerivedD1Ev:
.LFB7571:
	.seh_endprologue
	ret
	.seh_endproc
	.text
	.p2align 4
	.def	_ZL12probe_directi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL12probe_directi
_ZL12probe_directi:
.LFB7568:
	.seh_endprologue
	testl	%ecx, %ecx
	jle	.L20
	leal	(%rcx,%rcx), %r8d
	xorl	%edx, %edx
	xorl	%eax, %eax
	andl	$1, %ecx
	je	.L19
	cmpl	$2, %r8d
	movl	$2, %edx
	je	.L27
	.p2align 4,,10
	.p2align 3
.L19:
	leal	2(%rax,%rdx,2), %eax
	addl	$4, %edx
	cmpl	%edx, %r8d
	jne	.L19
.L27:
	cltq
	ret
	.p2align 4,,10
	.p2align 3
.L20:
	xorl	%eax, %eax
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL13probe_virtuali;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL13probe_virtuali
_ZL13probe_virtuali:
.LFB7573:
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
	movq	g_obj(%rip), %rdi
	testl	%ecx, %ecx
	movl	%ecx, %ebp
	jle	.L31
	xorl	%ebx, %ebx
	xorl	%esi, %esi
	.p2align 4,,10
	.p2align 3
.L30:
	movq	(%rdi), %rax
	movl	%ebx, %edx
	movq	%rdi, %rcx
	addl	$1, %ebx
	call	*16(%rax)
	addl	%eax, %esi
	cmpl	%ebx, %ebp
	jne	.L30
	movslq	%esi, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L31:
	xorl	%eax, %eax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL11probe_fnptri;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL11probe_fnptri
_ZL11probe_fnptri:
.LFB7574:
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
	movq	g_fn(%rip), %rbp
	testl	%ecx, %ecx
	movl	%ecx, %edi
	jle	.L36
	xorl	%ebx, %ebx
	xorl	%esi, %esi
	.p2align 4,,10
	.p2align 3
.L35:
	movl	%ebx, %ecx
	addl	$1, %ebx
	call	*%rbp
	addl	%eax, %esi
	cmpl	%ebx, %edi
	jne	.L35
	movslq	%esi, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L36:
	xorl	%eax, %eax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.seh_endproc
	.p2align 4
	.def	_ZL20probe_virtual_reloadi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL20probe_virtual_reloadi
_ZL20probe_virtual_reloadi:
.LFB7575:
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
	testl	%ecx, %ecx
	movl	%ecx, %edi
	jle	.L41
	leaq	g_arr(%rip), %rbp
	xorl	%ebx, %ebx
	xorl	%esi, %esi
	.p2align 4,,10
	.p2align 3
.L40:
	movl	%ebx, %eax
	movl	%ebx, %edx
	addl	$1, %ebx
	andl	$1, %eax
	movq	0(%rbp,%rax,8), %rcx
	movq	(%rcx), %rax
	call	*16(%rax)
	addl	%eax, %esi
	cmpl	%ebx, %edi
	jne	.L40
	movslq	%esi, %rax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.p2align 4,,10
	.p2align 3
.L41:
	xorl	%eax, %eax
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
	.seh_endproc
	.section	.text$_ZN2D2D1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN2D2D1Ev
	.def	_ZN2D2D1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2D2D1Ev
_ZN2D2D1Ev:
.LFB7601:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN7DerivedD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7DerivedD0Ev
	.def	_ZN7DerivedD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7DerivedD0Ev
_ZN7DerivedD0Ev:
.LFB7572:
	.seh_endprologue
	movl	$8, %edx
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN2D2D0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN2D2D0Ev
	.def	_ZN2D2D0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN2D2D0Ev
_ZN2D2D0Ev:
.LFB7602:
	.seh_endprologue
	movl	$8, %edx
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.def	_ZL5benchPFyiEii.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5benchPFyiEii.constprop.0
_ZL5benchPFyiEii.constprop.0:
.LFB7605:
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
.L47:
/APP
 # 15 "_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$10000000, %ecx
	movq	%rax, %rdi
	call	*%rbp
	movq	%rax, g_sink(%rip)
/APP
 # 15 "_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rdi, %rax
	cmpq	%rax, %rbx
	cmova	%rax, %rbx
	subl	$1, %esi
	jne	.L47
	testq	%rbx, %rbx
	js	.L48
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%rbx, %xmm0
.L49:
	divsd	.LC0(%rip), %xmm0
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L48:
	movq	%rbx, %rax
	andl	$1, %ebx
	pxor	%xmm0, %xmm0
	shrq	%rax
	orq	%rbx, %rax
	cvtsi2sdq	%rax, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L49
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
	.ascii "ns/call\0"
.LC4:
	.ascii "cyc/call\0"
.LC5:
	.ascii "call\0"
.LC6:
	.ascii "%-18s %10s %10s %12s\12\0"
.LC7:
	.ascii "raw(cyc)\0"
.LC8:
	.ascii "direct\0"
.LC9:
	.ascii "%-18s %10.2f %10.3f %12.2f\12\0"
.LC10:
	.ascii "virtual(hot)\0"
.LC11:
	.ascii "fnptr\0"
.LC12:
	.ascii "virtual(reload)\0"
	.align 8
.LC13:
	.ascii "virtual(hot)-direct extra = %.2f ns (%.1f cyc)\12\0"
	.align 8
.LC14:
	.ascii "virtual(reload)-direct extra = %.2f ns (%.1f cyc)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB7577:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$256, %rsp
	.seh_stackalloc	256
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
	movaps	%xmm14, 224(%rsp)
	.seh_savexmm	%xmm14, 224
	movaps	%xmm15, 240(%rsp)
	.seh_savexmm	%xmm15, 240
	.seh_endprologue
	call	__main
	leaq	72(%rsp), %rcx
	call	*__imp_QueryPerformanceFrequency(%rip)
	movq	__imp_QueryPerformanceCounter(%rip), %rsi
	leaq	80(%rsp), %rcx
	call	*%rsi
/APP
 # 15 "_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$100, %ecx
	movq	%rax, %rbx
	call	*__imp_Sleep(%rip)
	leaq	88(%rsp), %rcx
	call	*%rsi
/APP
 # 15 "_ch45_oop_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rbx, %rax
	js	.L53
	pxor	%xmm6, %xmm6
	cvtsi2sdq	%rax, %xmm6
.L54:
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
	leaq	_ZL9probe_nopi(%rip), %rcx
	call	_ZL5benchPFyiEii.constprop.0
	leaq	_ZL12probe_directi(%rip), %rcx
	movapd	%xmm0, %xmm7
	call	_ZL5benchPFyiEii.constprop.0
	leaq	_ZL13probe_virtuali(%rip), %rcx
	movapd	%xmm0, %xmm10
	call	_ZL5benchPFyiEii.constprop.0
	leaq	_ZL11probe_fnptri(%rip), %rcx
	movapd	%xmm10, %xmm11
	movapd	%xmm0, %xmm15
	call	_ZL5benchPFyiEii.constprop.0
	leaq	_ZL20probe_virtual_reloadi(%rip), %rcx
	movapd	%xmm15, %xmm9
	movapd	%xmm0, %xmm14
	call	_ZL5benchPFyiEii.constprop.0
	subsd	%xmm7, %xmm11
	leaq	.LC7(%rip), %rax
	movapd	%xmm0, %xmm13
	movapd	%xmm14, %xmm0
	movq	%rax, 32(%rsp)
	subsd	%xmm7, %xmm0
	movapd	%xmm13, %xmm8
	subsd	%xmm7, %xmm9
	movapd	%xmm11, %xmm12
	divsd	%xmm6, %xmm12
	subsd	%xmm7, %xmm8
	movapd	%xmm0, %xmm5
	movsd	%xmm0, 56(%rsp)
	leaq	.LC3(%rip), %r9
	movapd	%xmm9, %xmm4
	leaq	.LC4(%rip), %r8
	movapd	%xmm8, %xmm7
	leaq	.LC5(%rip), %rdx
	leaq	.LC6(%rip), %rcx
	divsd	%xmm6, %xmm4
	divsd	%xmm6, %xmm5
	movq	%xmm4, %rdi
	divsd	%xmm6, %xmm7
	movq	%xmm5, %rsi
	call	_Z6printfPKcz
	movsd	%xmm10, 32(%rsp)
	movapd	%xmm12, %xmm3
	movq	%xmm12, %r9
	movapd	%xmm11, %xmm2
	movq	%xmm11, %r8
	movq	%rbx, %rcx
	leaq	.LC8(%rip), %rdx
	call	_Z6printfPKcz
	movq	%rdi, %xmm3
	movq	%rdi, %r9
	movq	%rbx, %rcx
	movsd	%xmm15, 32(%rsp)
	movapd	%xmm9, %xmm2
	movq	%xmm9, %r8
	leaq	.LC10(%rip), %rdx
	call	_Z6printfPKcz
	movq	%rsi, %xmm3
	movq	%rsi, %r9
	movq	%rbx, %rcx
	movsd	56(%rsp), %xmm0
	movsd	%xmm14, 32(%rsp)
	leaq	.LC11(%rip), %rdx
	movapd	%xmm0, %xmm2
	movq	%xmm0, %r8
	call	_Z6printfPKcz
	movsd	%xmm13, 32(%rsp)
	movapd	%xmm8, %xmm2
	movq	%rbx, %rcx
	leaq	.LC12(%rip), %rdx
	movq	%xmm8, %r8
	movapd	%xmm7, %xmm3
	movq	%xmm7, %r9
	call	_Z6printfPKcz
	movq	%rdi, %xmm1
	subsd	%xmm11, %xmm9
	subsd	%xmm12, %xmm1
	leaq	.LC13(%rip), %rcx
	movq	%xmm9, %r8
	movapd	%xmm9, %xmm2
	movq	%xmm1, %rdx
	call	_Z6printfPKcz
	subsd	%xmm11, %xmm8
	leaq	.LC14(%rip), %rcx
	subsd	%xmm12, %xmm7
	movq	%xmm8, %r8
	movapd	%xmm8, %xmm2
	movapd	%xmm7, %xmm1
	movq	%xmm7, %rdx
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
	movaps	224(%rsp), %xmm14
	movaps	240(%rsp), %xmm15
	addq	$256, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
.L53:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm6, %xmm6
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm6
	addsd	%xmm6, %xmm6
	jmp	.L54
	.seh_endproc
	.p2align 4
	.def	_GLOBAL__sub_I__Z7free_fni;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I__Z7free_fni
_GLOBAL__sub_I__Z7free_fni:
.LFB7604:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	leaq	16+_ZTV7Derived(%rip), %rbx
	movl	$8, %ecx
	call	_Znwy
	movl	$8, %ecx
	movq	%rbx, (%rax)
	movq	%rax, g_obj(%rip)
	call	_Znwy
	movl	$8, %ecx
	movq	%rbx, (%rax)
	movq	%rax, g_arr(%rip)
	call	_Znwy
	leaq	16+_ZTV2D2(%rip), %rdx
	movq	%rdx, (%rax)
	movq	%rax, 8+g_arr(%rip)
	addq	$32, %rsp
	popq	%rbx
	ret
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I__Z7free_fni
	.globl	_ZTS4Base
	.section	.rdata$_ZTS4Base,"dr"
	.linkonce same_size
_ZTS4Base:
	.ascii "4Base\0"
	.globl	_ZTI4Base
	.section	.rdata$_ZTI4Base,"dr"
	.linkonce same_size
	.align 8
_ZTI4Base:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTS4Base
	.globl	_ZTS7Derived
	.section	.rdata$_ZTS7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTS7Derived:
	.ascii "7Derived\0"
	.globl	_ZTI7Derived
	.section	.rdata$_ZTI7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTI7Derived:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS7Derived
	.quad	_ZTI4Base
	.globl	_ZTS2D2
	.section	.rdata$_ZTS2D2,"dr"
	.linkonce same_size
_ZTS2D2:
	.ascii "2D2\0"
	.globl	_ZTI2D2
	.section	.rdata$_ZTI2D2,"dr"
	.linkonce same_size
	.align 8
_ZTI2D2:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTS2D2
	.quad	_ZTI4Base
	.globl	_ZTV7Derived
	.section	.rdata$_ZTV7Derived,"dr"
	.linkonce same_size
	.align 8
_ZTV7Derived:
	.quad	0
	.quad	_ZTI7Derived
	.quad	_ZN7DerivedD1Ev
	.quad	_ZN7DerivedD0Ev
	.quad	_ZN7Derived4virtEi
	.globl	_ZTV2D2
	.section	.rdata$_ZTV2D2,"dr"
	.linkonce same_size
	.align 8
_ZTV2D2:
	.quad	0
	.quad	_ZTI2D2
	.quad	_ZN2D2D1Ev
	.quad	_ZN2D2D0Ev
	.quad	_ZN2D24virtEi
	.globl	g_sink
	.bss
	.align 8
g_sink:
	.space 8
	.globl	g_fn
	.data
	.align 8
g_fn:
	.quad	_Z7free_fni
	.globl	g_arr
	.bss
	.align 16
g_arr:
	.space 16
	.globl	g_obj
	.align 8
g_obj:
	.space 8
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1097011920
	.align 8
.LC1:
	.long	0
	.long	1104006501
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
