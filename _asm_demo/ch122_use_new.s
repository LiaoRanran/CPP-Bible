	.file	"ch122_use_new.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7use_newv
	.def	_Z7use_newv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_newv
_Z7use_newv:
.LFB0:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 40
	call	_Znay
	mov	ecx, 40
	mov	rsi, rax
	mov	QWORD PTR g_a[rip], rax
	call	_Znay
	mov	rcx, rsi
	mov	rbx, rax
	mov	QWORD PTR g_b[rip], rax
	call	_ZdaPv
	mov	rcx, rbx
	add	rsp, 40
	pop	rbx
	pop	rsi
	jmp	_ZdaPv
	.seh_endproc
	.globl	g_b
	.bss
	.align 8
g_b:
	.space 8
	.globl	g_a
	.align 8
g_a:
	.space 8
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
