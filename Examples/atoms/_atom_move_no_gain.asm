	.file	"_atom_move_no_gain.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB779:
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
.LFB810:
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
.LFB781:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB782:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdaPv
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPv
_ZdaPv:
.LFB812:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdaPvy
	.def	_ZdaPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPvy
_ZdaPvy:
.LFB814:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "\346\230\257\0"
.LC1:
	.ascii "\345\220\246\0"
	.align 8
.LC2:
	.ascii "HeapBuf  \346\213\267\350\264\235\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\220\216\346\272\220\350\242\253\346\216\217\347\251\272=%s\12\0"
	.align 8
.LC3:
	.ascii "FixedBuf \346\213\267\350\264\235\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\220\216\346\272\220\345\256\214\345\245\275=%s\12\0"
	.align 8
.LC4:
	.ascii "array    \346\213\267\350\264\235\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\220\216\346\272\220\345\256\214\345\245\275=%s\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB800:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
	push	r13
	.seh_pushreg	r13
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
	sub	rsp, 120
	.seh_stackalloc	120
	.seh_endprologue
	mov	ebx, ecx
	call	__main
	lea	eax, 0[0+rbx*8]
	mov	ecx, 32
	sub	eax, ebx
	lea	ebx, 1[rax]
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	call	malloc
	mov	edx, DWORD PTR _ZL8g_allocs[rip]
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	r8d, DWORD PTR _ZL8g_allocs[rip]
	mov	rcx, rax
	mov	QWORD PTR 56[rsp], 0
	mov	DWORD PTR 44[rsp], edx
	mov	rdi, QWORD PTR 56[rsp]
	mov	DWORD PTR 40[rsp], r8d
	call	free
	movd	xmm1, ebx
	test	rdi, rdi
	mov	edx, DWORD PTR 44[rsp]
	lea	rax, 80[rsp]
	pshufd	xmm0, xmm1, 0
	mov	r8d, DWORD PTR 40[rsp]
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	r13d, DWORD PTR _ZL8g_allocs[rip]
	lea	r9, .LC1[rip]
	movaps	XMMWORD PTR 80[rsp], xmm0
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	r14d, DWORD PTR _ZL8g_allocs[rip]
	mov	QWORD PTR 64[rsp], rax
	mov	rcx, QWORD PTR 64[rsp]
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	esi, DWORD PTR _ZL8g_allocs[rip]
	movaps	XMMWORD PTR 96[rsp], xmm0
	mov	r15d, DWORD PTR [rcx]
	lea	rcx, .LC2[rip]
	mov	DWORD PTR 36[rsp], esi
	lea	rsi, .LC0[rip]
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	cmove	r9, rsi
	mov	ebp, DWORD PTR _ZL8g_allocs[rip]
	mov	QWORD PTR 72[rsp], rax
	mov	rax, QWORD PTR 72[rsp]
	mov	r12d, DWORD PTR [rax]
	call	__mingw_printf
	cmp	r15d, ebx
	mov	r8d, r14d
	mov	edx, r13d
	lea	r9, .LC1[rip]
	lea	rcx, .LC3[rip]
	cmove	r9, rsi
	call	__mingw_printf
	cmp	r12d, ebx
	mov	edx, DWORD PTR 36[rsp]
	mov	r8d, ebp
	lea	r9, .LC1[rip]
	lea	rcx, .LC4[rip]
	cmove	r9, rsi
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 120
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.seh_endproc
.lcomm _ZL8g_allocs,4,4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
