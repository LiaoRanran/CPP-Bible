	.file	"_ch14_opt.cpp"
	.text
	.p2align 4
	.globl	_Z6sum_toi
	.def	_Z6sum_toi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6sum_toi
_Z6sum_toi:
.LFB0:
	.seh_endprologue
	testl	%ecx, %ecx
	jle	.L4
	leal	1(%rcx), %r8d
	xorl	%edx, %edx
	andl	$1, %ecx
	movl	$1, %eax
	je	.L3
	movl	$2, %eax
	movl	$1, %edx
	cmpl	%r8d, %eax
	je	.L1
	.p2align 4,,10
	.p2align 3
.L3:
	leal	1(%rdx,%rax,2), %edx
	addl	$2, %eax
	cmpl	%r8d, %eax
	jne	.L3
.L1:
	movl	%edx, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	xorl	%edx, %edx
	movl	%edx, %eax
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
