	.file	"_asm_tpl_spec.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "full-int\0"
	.text
	.align 2
	.p2align 4
	.globl	_ZN7WrapperIiE4kindEv
	.def	_ZN7WrapperIiE4kindEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7WrapperIiE4kindEv
_ZN7WrapperIiE4kindEv:
.LFB17:
	.seh_endprologue
	lea	rax, .LC0[rip]
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "primary\0"
	.section	.text$_ZN7WrapperIdE4kindEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7WrapperIdE4kindEv
	.def	_ZN7WrapperIdE4kindEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7WrapperIdE4kindEv
_ZN7WrapperIdE4kindEv:
.LFB21:
	.seh_endprologue
	lea	rax, .LC1[rip]
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC2:
	.ascii "partial-ptr\0"
	.section	.text$_ZN7WrapperIPiE4kindEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7WrapperIPiE4kindEv
	.def	_ZN7WrapperIPiE4kindEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7WrapperIPiE4kindEv
_ZN7WrapperIPiE4kindEv:
.LFB22:
	.seh_endprologue
	lea	rax, .LC2[rip]
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC3:
	.ascii "partial-const\0"
	.section	.text$_ZN7WrapperIKdE4kindEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN7WrapperIKdE4kindEv
	.def	_ZN7WrapperIKdE4kindEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN7WrapperIKdE4kindEv
_ZN7WrapperIKdE4kindEv:
.LFB23:
	.seh_endprologue
	lea	rax, .LC3[rip]
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB20:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	call	[QWORD PTR a[rip]]
	test	rax, rax
	je	.L9
	call	[QWORD PTR b[rip]]
	test	rax, rax
	je	.L9
	call	[QWORD PTR c[rip]]
	test	rax, rax
	je	.L9
	call	[QWORD PTR d[rip]]
	test	rax, rax
	sete	al
	jmp	.L8
.L9:
	mov	eax, 1
.L8:
	movzx	eax, al
	add	rsp, 40
	ret
	.seh_endproc
	.globl	d
	.data
	.align 8
d:
	.quad	_ZN7WrapperIKdE4kindEv
	.globl	c
	.align 8
c:
	.quad	_ZN7WrapperIPiE4kindEv
	.globl	b
	.align 8
b:
	.quad	_ZN7WrapperIiE4kindEv
	.globl	a
	.align 8
a:
	.quad	_ZN7WrapperIdE4kindEv
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
