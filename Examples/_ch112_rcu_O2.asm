	.file	"_ch112_rcu.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	rcu_update
	.def	rcu_update;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_update
rcu_update:
.LFB668:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	mov	rbx, QWORD PTR g_config[rip]
	movd	xmm6, ecx
	movd	xmm0, edx
	mov	ecx, 8
	punpckldq	xmm6, xmm0
	call	_Znwy
	test	rbx, rbx
	movq	QWORD PTR [rax], xmm6
	mov	QWORD PTR g_config[rip], rax
	jne	.L4
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 48
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	edx, 8
	mov	rcx, rbx
	add	rsp, 48
	pop	rbx
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.globl	rcu_read
	.def	rcu_read;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_read
rcu_read:
.LFB669:
	.seh_endprologue
	mov	rax, QWORD PTR g_config[rip]
	ret
	.seh_endproc
	.globl	g_config
	.bss
	.align 8
g_config:
	.space 8
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
