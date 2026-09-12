	.file	"_atom_inline_odr_main.cpp"
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "\0"
.LC1:
	.ascii "%stu_a=%d\12\0"
.LC2:
	.ascii "%stu_b=%d\12\0"
.LC3:
	.ascii "%sstable_a=%d\12\0"
.LC4:
	.ascii "%sstable_b=%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB24:
	pushq	%rdi
	.seh_pushreg	%rdi
	pushq	%rsi
	.seh_pushreg	%rsi
	pushq	%rbx
	.seh_pushreg	%rbx
	subq	$32, %rsp
	.seh_stackalloc	32
	.seh_endprologue
	leaq	.LC0(%rip), %rbx
	movl	%ecx, %esi
	movq	%rdx, %rdi
	call	__main
	cmpl	$1, %esi
	jle	.L2
	movq	8(%rdi), %rbx
.L2:
	call	_Z10tu_a_valuev
	movq	%rbx, %rdx
	leaq	.LC1(%rip), %rcx
	movl	%eax, %r8d
	call	__mingw_printf
	call	_Z10tu_b_valuev
	movq	%rbx, %rdx
	leaq	.LC2(%rip), %rcx
	movl	%eax, %r8d
	call	__mingw_printf
	call	_Z11tu_a_stablev
	movq	%rbx, %rdx
	leaq	.LC3(%rip), %rcx
	movl	%eax, %r8d
	call	__mingw_printf
	call	_Z11tu_b_stablev
	movq	%rbx, %rdx
	leaq	.LC4(%rip), %rcx
	movl	%eax, %r8d
	call	__mingw_printf
	xorl	%eax, %eax
	addq	$32, %rsp
	popq	%rbx
	popq	%rsi
	popq	%rdi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Z10tu_a_valuev;	.scl	2;	.type	32;	.endef
	.def	_Z10tu_b_valuev;	.scl	2;	.type	32;	.endef
	.def	_Z11tu_a_stablev;	.scl	2;	.type	32;	.endef
	.def	_Z11tu_b_stablev;	.scl	2;	.type	32;	.endef
