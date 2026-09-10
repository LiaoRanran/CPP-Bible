	.file	"_atom_move_alloc.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB276:
	.seh_endprologue
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_Znay
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znay
_Znay:
.LFB297:
	.seh_endprologue
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB278:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB279:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdaPv
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPv
_ZdaPv:
.LFB299:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdaPvy
	.def	_ZdaPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPvy
_ZdaPvy:
.LFB301:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "\346\236\204\351\200\240\345\210\206\351\205\215=%ld \346\213\267\350\264\235\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\210\206\351\205\215=%ld\12\0"
	.section	.text.unlikely,"x"
.LCOLDB1:
	.section	.text.startup,"x"
.LHOTB1:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB294:
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	movsxd	rbx, ecx
	call	__main
	add	rbx, 1
	movabs	rax, 2305843009213693950
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	lea	rsi, 0[0+rbx*8]
	cmp	rax, rsi
	jb	.L9
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	sal	rbx, 5
	mov	rcx, rbx
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	call	malloc
	mov	ebp, DWORD PTR _ZL8g_allocs[rip]
	mov	rcx, rbx
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	rdi, rax
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	call	malloc
	mov	rbx, rax
	xor	eax, eax
	test	rsi, rsi
	je	.L25
	.p2align 4
	.p2align 4
	.p2align 3
.L10:
	mov	edx, DWORD PTR [rdi+rax*4]
	mov	DWORD PTR [rbx+rax*4], edx
	add	rax, 1
	cmp	rsi, rax
	jne	.L10
	mov	rcx, rdi
	mov	esi, DWORD PTR _ZL8g_allocs[rip]
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	r12d, DWORD PTR _ZL8g_allocs[rip]
	call	free
.L12:
	mov	rcx, rbx
	call	free
.L14:
	mov	r9d, r12d
	mov	r8d, esi
	lea	rcx, .LC0[rip]
	mov	edx, ebp
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L25:
	xor	eax, eax
	mov	esi, DWORD PTR _ZL8g_allocs[rip]
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	mov	r12d, DWORD PTR _ZL8g_allocs[rip]
	test	rdi, rdi
	jne	.L26
.L13:
	test	rbx, rbx
	je	.L14
	jmp	.L12
.L26:
	mov	rcx, rdi
	call	free
	jmp	.L13
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 32
	.seh_savereg	rsi, 40
	.seh_savereg	rdi, 48
	.seh_savereg	rbp, 56
	.seh_savereg	r12, 64
	.seh_endprologue
main.cold:
.L9:
	call	__cxa_throw_bad_array_new_length
	nop
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.section	.text.startup,"x"
.LHOTE1:
.lcomm _ZL8g_allocs,4,4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw_bad_array_new_length;	.scl	2;	.type	32;	.endef
