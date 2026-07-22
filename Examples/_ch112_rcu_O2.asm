	.file	"_ch112_rcu.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	rcu_update
	.def	rcu_update;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_update
rcu_update:
.LFB671:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, QWORD PTR g_config[rip]
	mov	edi, ecx
	mov	ecx, 8
	mov	esi, edx
	call	_Znwy
	mov	DWORD PTR [rax], edi
	mov	DWORD PTR 4[rax], esi
	mov	QWORD PTR g_config[rip], rax
	test	rbx, rbx
	jne	.L4
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	mov	edx, 8
	mov	rcx, rbx
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	jmp	_ZdlPvy
	.seh_endproc
	.p2align 4
	.globl	rcu_read
	.def	rcu_read;	.scl	2;	.type	32;	.endef
	.seh_proc	rcu_read
rcu_read:
.LFB672:
	.seh_endprologue
	mov	rax, QWORD PTR g_config[rip]
	ret
	.seh_endproc
	.globl	g_config
	.bss
	.align 8
g_config:
	.space 8
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
