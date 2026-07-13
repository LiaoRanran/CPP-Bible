	.file	"_ch43_cache_perf.cpp"
	.text
	.p2align 4
	.def	_ZL5chasePyy;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL5chasePyy
_ZL5chasePyy:
.LFB11787:
	.seh_endprologue
	movq	(%rcx), %rax
	testq	%rdx, %rdx
	je	.L4
	xorl	%ecx, %ecx
	xorl	%r8d, %r8d
	.p2align 4,,10
	.p2align 3
.L3:
	movq	(%rax), %rax
	addq	$1, %rcx
	addq	%rax, %r8
	cmpq	%rcx, %rdx
	jne	.L3
	movq	%r8, %rax
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xorl	%r8d, %r8d
	movq	%r8, %rax
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.text
	.align 2
	.p2align 4
	.def	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0
_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0:
.LFB12696:
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
	movabsq	$1152921504606846975, %rax
	cmpq	%rdx, %rax
	movq	%rcx, %rbx
	movq	%rdx, %rsi
	jb	.L15
	testq	%rdx, %rdx
	pxor	%xmm0, %xmm0
	movq	$0, 16(%rcx)
	movups	%xmm0, (%rcx)
	je	.L16
	leaq	0(,%rdx,8), %rdi
	movq	%rdi, %rcx
	call	_Znwy
	xorl	%edx, %edx
	subq	$1, %rsi
	leaq	(%rax,%rdi), %rbp
	movq	%rax, (%rbx)
	movq	%rbp, 16(%rbx)
	leaq	8(%rax), %rcx
	movq	%rdx, (%rax)
	je	.L10
	cmpq	%rcx, %rbp
	je	.L11
	leaq	-8(%rdi), %r8
	xorl	%edx, %edx
	call	memset
.L11:
	movq	%rbp, %rcx
.L10:
	movq	%rcx, 8(%rbx)
	addq	$40, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	ret
.L16:
	xorl	%ecx, %ecx
	movq	%rcx, (%rbx)
	movq	%rcx, 16(%rbx)
	xorl	%ecx, %ecx
	jmp	.L10
.L15:
	leaq	.LC0(%rip), %rcx
	call	_ZSt20__throw_length_errorPKc
	nop
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
	.section	.text$_ZNSt12_Vector_baseIySaIyEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIySaIyEED2Ev
	.def	_ZNSt12_Vector_baseIySaIyEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIySaIyEED2Ev
_ZNSt12_Vector_baseIySaIyEED2Ev:
.LFB12359:
	.seh_endprologue
	movq	(%rcx), %rax
	testq	%rax, %rax
	je	.L18
	movq	16(%rcx), %rdx
	movq	%rax, %rcx
	subq	%rax, %rdx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L18:
	ret
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
	.def	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv:
.LFB12614:
	subq	$40, %rsp
	.seh_stackalloc	40
	movaps	%xmm6, (%rsp)
	.seh_savexmm	%xmm6, 0
	movaps	%xmm7, 16(%rsp)
	.seh_savexmm	%xmm7, 16
	.seh_endprologue
	movdqa	.LC1(%rip), %xmm7
	pxor	%xmm3, %xmm3
	movdqa	.LC2(%rip), %xmm6
	movdqa	.LC3(%rip), %xmm5
	movdqa	.LC4(%rip), %xmm4
	movq	%rcx, %r11
	movq	%rcx, %rdx
	leaq	1248(%rcx), %rcx
	movq	%r11, %rax
	.p2align 4,,10
	.p2align 3
.L21:
	movdqu	(%rax), %xmm0
	addq	$16, %rax
	movdqu	-8(%rax), %xmm1
	movdqu	1232(%rax), %xmm2
	pand	%xmm7, %xmm0
	pand	%xmm6, %xmm1
	por	%xmm1, %xmm0
	movdqa	%xmm0, %xmm1
	pand	%xmm5, %xmm0
	psrlq	$1, %xmm1
	pxor	%xmm2, %xmm1
	movdqa	%xmm3, %xmm2
	psubq	%xmm0, %xmm2
	pand	%xmm4, %xmm2
	movdqa	%xmm2, %xmm0
	pxor	%xmm1, %xmm0
	movups	%xmm0, -16(%rax)
	cmpq	%rcx, %rax
	jne	.L21
	movq	1248(%r11), %r8
	leaq	1240(%r11), %r10
	movabsq	$-5403634167711393303, %r9
	.p2align 4,,10
	.p2align 3
.L22:
	movq	%r8, %rcx
	movq	1256(%rdx), %r8
	addq	$8, %rdx
	andq	$-2147483648, %rcx
	movq	%r8, %rax
	andl	$2147483647, %eax
	orq	%rcx, %rax
	movq	%rax, %rcx
	andl	$1, %eax
	shrq	%rcx
	xorq	-8(%rdx), %rcx
	negq	%rax
	andq	%r9, %rax
	xorq	%rcx, %rax
	movq	%rax, 1240(%rdx)
	cmpq	%r10, %rdx
	jne	.L22
	movq	2488(%r11), %rax
	movq	$0, 2496(%r11)
	movq	(%r11), %rdx
	movaps	(%rsp), %xmm6
	movaps	16(%rsp), %xmm7
	andq	$-2147483648, %rax
	andl	$2147483647, %edx
	orq	%rdx, %rax
	movq	%rax, %rdx
	andl	$1, %eax
	shrq	%rdx
	xorq	1240(%r11), %rdx
	negq	%rax
	andq	%r9, %rax
	xorq	%rdx, %rax
	movq	%rax, 2488(%r11)
	addq	$40, %rsp
	ret
	.seh_endproc
	.section	.text$_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	.def	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv:
.LFB12520:
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	2496(%rcx), %rax
	cmpq	$311, %rax
	movq	%rcx, %rbx
	ja	.L27
.L26:
	leaq	1(%rax), %rdx
	movq	(%rbx,%rax,8), %rax
	movabsq	$6148914691236517205, %rcx
	movq	%rdx, 2496(%rbx)
	movq	%rax, %rdx
	shrq	$29, %rdx
	andq	%rcx, %rdx
	movabsq	$8202884508482404352, %rcx
	xorq	%rax, %rdx
	movq	%rdx, %rax
	salq	$17, %rax
	andq	%rcx, %rax
	movabsq	$-2270628950310912, %rcx
	xorq	%rdx, %rax
	movq	%rax, %rdx
	salq	$37, %rdx
	andq	%rcx, %rdx
	xorq	%rax, %rdx
	movq	%rdx, %rax
	shrq	$43, %rax
	xorq	%rdx, %rax
	addq	$32, %rsp
	popq	%rbx
	ret
	.p2align 4,,10
	.p2align 3
.L27:
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
	movq	2496(%rbx), %rax
	jmp	.L26
	.seh_endproc
	.text
	.align 2
	.p2align 4
	.def	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0
_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0:
.LFB12703:
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	movq	%r8, %rsi
	movq	%rcx, %rbx
	movq	%rdx, %rdi
	subq	%rdx, %rsi
	movq	%r8, %rbp
	cmpq	$-1, %rsi
	je	.L29
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	addq	$1, %rsi
	mulq	%rsi
	cmpq	%rsi, %rax
	movq	%rax, %r10
	movq	%rdx, %r11
	jnb	.L30
	leaq	-1(%rdi), %rax
	xorl	%edx, %edx
	subq	%rbp, %rax
	divq	%rsi
	cmpq	%rdx, %r10
	movq	%rdx, %rbp
	jnb	.L30
	movq	2496(%rbx), %rcx
	movabsq	$6148914691236517205, %r14
	movabsq	$8202884508482404352, %r13
	movabsq	$-2270628950310912, %r12
	jmp	.L32
	.p2align 4,,10
	.p2align 3
.L31:
	movq	(%rbx,%rax,8), %r10
	leaq	1(%rax), %rcx
	movq	%rcx, 2496(%rbx)
	movq	%r10, %rax
	shrq	$29, %rax
	andq	%r14, %rax
	xorq	%rax, %r10
	movq	%r10, %rax
	salq	$17, %rax
	andq	%r13, %rax
	xorq	%rax, %r10
	movq	%r10, %rax
	salq	$37, %rax
	andq	%r12, %rax
	xorq	%rax, %r10
	movq	%r10, %rax
	shrq	$43, %rax
	xorq	%rax, %r10
	movq	%r10, %rax
	mulq	%rsi
	cmpq	%rbp, %rax
	movq	%rdx, %r11
	jnb	.L30
.L32:
	cmpq	$311, %rcx
	movq	%rcx, %rax
	jbe	.L31
	movq	%rbx, %rcx
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EE11_M_gen_randEv
	movq	2496(%rbx), %rax
	jmp	.L31
	.p2align 4,,10
	.p2align 3
.L30:
	movq	%r11, %rax
.L33:
	addq	%rdi, %rax
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	ret
	.p2align 4,,10
	.p2align 3
.L29:
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	jmp	.L33
	.seh_endproc
	.section	.text$_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_,"x"
	.linkonce discard
	.p2align 4
	.globl	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_
	.def	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_
_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_:
.LFB12174:
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	cmpq	%rdx, %rcx
	movq	%rcx, %rsi
	movq	%rdx, %rdi
	movq	%r8, %rbp
	je	.L36
	leaq	8(%rsi), %rbx
	movq	%rdx, %rcx
	subq	%rsi, %rcx
	sarq	$3, %rcx
	movq	%rcx, %rax
	mulq	%rcx
	seto	%al
	movzbl	%al, %eax
	testq	%rax, %rax
	jne	.L47
	jmp	.L48
	.p2align 4,,10
	.p2align 3
.L44:
	movq	%rbx, %r8
	xorl	%edx, %edx
	movq	%rbp, %rcx
	subq	%rsi, %r8
	addq	$8, %rbx
	sarq	$3, %r8
	call	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0
	movq	-8(%rbx), %rdx
	leaq	(%rsi,%rax,8), %rax
	movq	(%rax), %rcx
	movq	%rcx, -8(%rbx)
	movq	%rdx, (%rax)
.L47:
	cmpq	%rbx, %rdi
	jne	.L44
.L36:
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
	.p2align 4,,10
	.p2align 3
.L48:
	andl	$1, %ecx
	je	.L49
.L41:
	cmpq	%rbx, %rdi
	je	.L36
	.p2align 4,,10
	.p2align 3
.L43:
	movq	%rbx, %rax
	xorl	%edx, %edx
	movq	%rbp, %rcx
	subq	%rsi, %rax
	addq	$16, %rbx
	sarq	$3, %rax
	leaq	2(%rax), %r12
	addq	$1, %rax
	imulq	%r12, %rax
	leaq	-1(%rax), %r8
	call	_ZNSt24uniform_int_distributionIyEclISt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEEyRT_RKNS0_10param_typeE.isra.0
	xorl	%edx, %edx
	movq	-16(%rbx), %rcx
	divq	%r12
	leaq	(%rsi,%rax,8), %rax
	movq	(%rax), %r8
	movq	%r8, -16(%rbx)
	movq	%rcx, (%rax)
	leaq	(%rsi,%rdx,8), %rax
	movq	-8(%rbx), %rdx
	movq	(%rax), %rcx
	movq	%rcx, -8(%rbx)
	cmpq	%rbx, %rdi
	movq	%rdx, (%rax)
	jne	.L43
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	ret
	.p2align 4,,10
	.p2align 3
.L49:
	leaq	16(%rsi), %rbx
	movq	%r8, %rcx
	call	_ZNSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEclEv
	movl	$2, %edx
	mulq	%rdx
	leaq	(%rsi,%rdx,8), %rax
	movq	8(%rsi), %rdx
	movq	(%rax), %rcx
	movq	%rcx, 8(%rsi)
	movq	%rdx, (%rax)
	jmp	.L41
	.seh_endproc
	.section .rdata,"dr"
.LC5:
	.ascii "\0"
	.text
	.p2align 4
	.def	_ZL7measureydi;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL7measureydi
_ZL7measureydi:
.LFB11788:
	pushq	%r15
	.seh_pushreg	%r15
	pushq	%r14
	.seh_pushreg	%r14
	pushq	%r13
	.seh_pushreg	%r13
	pushq	%r12
	.seh_pushreg	%r12
	pushq	%rbp
	.seh_pushreg	%rbp
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$2664, %rsp
	.seh_stackalloc	2664
	movaps	%xmm6, 2640(%rsp)
	.seh_savexmm	%xmm6, 2640
	.seh_endprologue
	movq	%rdx, %rbx
	movq	%rcx, %rbp
	movapd	%xmm2, %xmm6
	leaq	64(%rsp), %rax
	shrq	$3, %rbx
	movl	%r9d, %edi
	movq	%rax, %rcx
	movq	%rbx, %rdx
	movq	%rax, 40(%rsp)
.LEHB0:
	call	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0
.LEHE0:
	movq	64(%rsp), %rsi
	testb	$1, %bl
	leaq	(%rsi,%rbx,8), %rcx
	movq	%rsi, %rax
	je	.L51
	leaq	8(%rsi), %rax
	movq	%rsi, (%rsi)
	cmpq	%rcx, %rax
	je	.L81
	.p2align 4,,10
	.p2align 3
.L51:
	movq	%rax, (%rax)
	leaq	8(%rax), %rdx
	addq	$16, %rax
	cmpq	%rcx, %rax
	movq	%rdx, (%rdx)
	jne	.L51
.L81:
	leaq	96(%rsp), %r13
	movq	%rbx, %rdx
	movq	%r13, %rcx
.LEHB1:
	call	_ZNSt6vectorIySaIyEEC1EyRKS0_.isra.0
.LEHE1:
	xorl	%eax, %eax
	testb	$1, %bl
	movq	96(%rsp), %r14
	je	.L52
	xorl	%eax, %eax
	cmpq	$1, %rbx
	movq	%rax, (%r14)
	movl	$1, %eax
	je	.L80
	.p2align 4,,10
	.p2align 3
.L52:
	movq	%rax, (%r14,%rax,8)
	leaq	1(%rax), %rdx
	addq	$2, %rax
	cmpq	%rax, %rbx
	movq	%rdx, (%r14,%rdx,8)
	jne	.L52
.L80:
	movabsq	$-7046029254386353131, %rcx
	movl	$1, %edx
	movabsq	$6364136223846793005, %r9
	movq	%rcx, 128(%rsp)
	leaq	128(%rsp), %r8
	.p2align 4,,10
	.p2align 3
.L53:
	movq	%rcx, %rax
	shrq	$62, %rax
	xorq	%rcx, %rax
	imulq	%r9, %rax
	leaq	(%rax,%rdx), %rcx
	movq	%rcx, (%r8,%rdx,8)
	addq	$1, %rdx
	cmpq	$312, %rdx
	jne	.L53
	movq	104(%rsp), %rdx
	movq	%r14, %rcx
	movq	$312, 2624(%rsp)
	call	_ZSt7shuffleIN9__gnu_cxx17__normal_iteratorIPySt6vectorIySaIyEEEERSt23mersenne_twister_engineIyLy64ELy312ELy156ELy31ELy13043109905998158313ELy29ELy6148914691236517205ELy17ELy8202884508482404352ELy37ELy18444473444759240704ELy43ELy6364136223846793005EEEvT_SA_OT0_
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L54:
	movq	(%r14,%rax,8), %rdx
	leaq	(%rsi,%rdx,8), %rdx
	movq	%rdx, (%rsi,%rax,8)
	addq	$1, %rax
	cmpq	%rax, %rbx
	jne	.L54
	movq	$0, 56(%rsp)
	xorl	%r12d, %r12d
	movq	$-1, %r14
	.p2align 4,,10
	.p2align 3
.L55:
/APP
 # 20 "_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movq	%rbx, %rdx
	movq	%rsi, %rcx
	movq	%rax, %r15
	call	_ZL5chasePyy
	movq	%rax, %rdx
	movq	56(%rsp), %rax
	addq	%rdx, %rax
	movq	%rax, 56(%rsp)
/APP
 # 20 "_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%r15, %rax
	cmpq	%rax, %r14
	cmova	%rax, %r14
	addl	$1, %r12d
	cmpl	%r12d, %edi
	jne	.L55
	movq	56(%rsp), %rax
	testq	%rax, %rax
	jne	.L59
	leaq	.LC5(%rip), %rcx
.LEHB2:
	call	_Z6printfPKcz
.LEHE2:
.L59:
	testq	%r14, %r14
	js	.L57
	pxor	%xmm0, %xmm0
	cvtsi2sdq	%r14, %xmm0
.L58:
	pxor	%xmm1, %xmm1
	cvtsi2sdq	%rbx, %xmm1
	movq	%r13, %rcx
	divsd	%xmm1, %xmm0
	movapd	%xmm0, %xmm1
	movsd	%xmm0, 0(%rbp)
	divsd	%xmm6, %xmm1
	movsd	%xmm1, 8(%rbp)
	call	_ZNSt12_Vector_baseIySaIyEED2Ev
	movq	40(%rsp), %rcx
	call	_ZNSt12_Vector_baseIySaIyEED2Ev
	nop
	movaps	2640(%rsp), %xmm6
	movq	%rbp, %rax
	addq	$2664, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	popq	%rbp
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	ret
.L57:
	movq	%r14, %rax
	andl	$1, %r14d
	pxor	%xmm0, %xmm0
	shrq	%rax
	orq	%r14, %rax
	cvtsi2sdq	%rax, %xmm0
	addsd	%xmm0, %xmm0
	jmp	.L58
.L63:
	movq	%r13, %rcx
	movq	%rax, %rbx
	call	_ZNSt12_Vector_baseIySaIyEED2Ev
.L61:
	movq	40(%rsp), %rcx
	call	_ZNSt12_Vector_baseIySaIyEED2Ev
	movq	%rbx, %rcx
.LEHB3:
	call	_Unwind_Resume
.LEHE3:
.L62:
	movq	%rax, %rbx
	jmp	.L61
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA11788:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE11788-.LLSDACSB11788
.LLSDACSB11788:
	.uleb128 .LEHB0-.LFB11788
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB11788
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L62-.LFB11788
	.uleb128 0
	.uleb128 .LEHB2-.LFB11788
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L63-.LFB11788
	.uleb128 0
	.uleb128 .LEHB3-.LFB11788
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE11788:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC7:
	.ascii "TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\12\0"
.LC8:
	.ascii "cyc/step\0"
.LC9:
	.ascii "nodes\0"
.LC10:
	.ascii "work_set\0"
.LC11:
	.ascii "%-10s %12s %14s %14s\12\0"
.LC12:
	.ascii "ns/step\0"
.LC13:
	.ascii "16KB(L1)\0"
.LC14:
	.ascii "%-10s %12zu %14.2f %14.3f\12\0"
.LC15:
	.ascii "256KB(L2)\0"
.LC16:
	.ascii "8MB(L3)\0"
.LC17:
	.ascii "64MB(DRAM)\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB11795:
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$120, %rsp
	.seh_stackalloc	120
	.seh_endprologue
	call	__main
	leaq	88(%rsp), %rcx
	call	*__imp_QueryPerformanceFrequency(%rip)
	movq	__imp_QueryPerformanceCounter(%rip), %rsi
	leaq	96(%rsp), %rcx
	call	*%rsi
/APP
 # 20 "_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	movl	$100, %ecx
	movq	%rax, %rbx
	call	*__imp_Sleep(%rip)
	leaq	104(%rsp), %rcx
	call	*%rsi
/APP
 # 20 "_ch43_cache_perf.cpp" 1
	rdtsc
 # 0 "" 2
/NO_APP
	subq	%rbx, %rax
	js	.L83
	pxor	%xmm2, %xmm2
	cvtsi2sdq	%rax, %xmm2
.L84:
	movq	104(%rsp), %rax
	pxor	%xmm0, %xmm0
	pxor	%xmm1, %xmm1
	leaq	.LC7(%rip), %rcx
	subq	96(%rsp), %rax
	leaq	64(%rsp), %rsi
	cvtsi2sdq	88(%rsp), %xmm1
	leaq	.LC14(%rip), %rbx
	cvtsi2sdq	%rax, %xmm0
	divsd	%xmm1, %xmm0
	divsd	%xmm0, %xmm2
	divsd	.LC6(%rip), %xmm2
	movapd	%xmm2, %xmm1
	movq	%xmm2, %rdx
	movsd	%xmm2, 56(%rsp)
	call	_Z6printfPKcz
	leaq	.LC12(%rip), %rax
	leaq	.LC9(%rip), %r8
	movq	%rax, 32(%rsp)
	leaq	.LC8(%rip), %r9
	leaq	.LC10(%rip), %rdx
	leaq	.LC11(%rip), %rcx
	call	_Z6printfPKcz
	movsd	56(%rsp), %xmm2
	movq	%rsi, %rcx
	movl	$50, %r9d
	movl	$16384, %edx
	call	_ZL7measureydi
	movq	72(%rsp), %rax
	movl	$2048, %r8d
	movq	%rbx, %rcx
	movsd	64(%rsp), %xmm3
	leaq	.LC13(%rip), %rdx
	movq	%xmm3, %r9
	movq	%rax, 32(%rsp)
	call	_Z6printfPKcz
	movsd	56(%rsp), %xmm2
	movq	%rsi, %rcx
	movl	$30, %r9d
	movl	$262144, %edx
	call	_ZL7measureydi
	movq	72(%rsp), %rax
	movl	$32768, %r8d
	movq	%rbx, %rcx
	movsd	64(%rsp), %xmm3
	leaq	.LC15(%rip), %rdx
	movq	%xmm3, %r9
	movq	%rax, 32(%rsp)
	call	_Z6printfPKcz
	movsd	56(%rsp), %xmm2
	movq	%rsi, %rcx
	movl	$20, %r9d
	movl	$8388608, %edx
	call	_ZL7measureydi
	movq	72(%rsp), %rax
	movl	$1048576, %r8d
	movq	%rbx, %rcx
	movsd	64(%rsp), %xmm3
	leaq	.LC16(%rip), %rdx
	movq	%xmm3, %r9
	movq	%rax, 32(%rsp)
	call	_Z6printfPKcz
	movsd	56(%rsp), %xmm2
	movq	%rsi, %rcx
	movl	$10, %r9d
	movl	$67108864, %edx
	call	_ZL7measureydi
	movq	72(%rsp), %rax
	movq	%rbx, %rcx
	movl	$8388608, %r8d
	movsd	64(%rsp), %xmm3
	leaq	.LC17(%rip), %rdx
	movq	%xmm3, %r9
	movq	%rax, 32(%rsp)
	call	_Z6printfPKcz
	xorl	%eax, %eax
	addq	$120, %rsp
	popq	%rbx
	popq	%rsi
	ret
.L83:
	movq	%rax, %rdx
	andl	$1, %eax
	pxor	%xmm2, %xmm2
	shrq	%rdx
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm2
	addsd	%xmm2, %xmm2
	jmp	.L84
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC1:
	.quad	-2147483648
	.quad	-2147483648
	.align 16
.LC2:
	.quad	2147483647
	.quad	2147483647
	.align 16
.LC3:
	.quad	1
	.quad	1
	.align 16
.LC4:
	.quad	-5403634167711393303
	.quad	-5403634167711393303
	.align 8
.LC6:
	.long	0
	.long	1104006501
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
