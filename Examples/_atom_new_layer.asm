	.file	"_atom_new_layer.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB4074:
	.seh_endprologue
	mov	eax, DWORD PTR g_alloc[rip]
	add	eax, 1
	mov	DWORD PTR g_alloc[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB4075:
	.seh_endprologue
	mov	eax, DWORD PTR g_dealloc[rip]
	add	eax, 1
	mov	DWORD PTR g_dealloc[rip], eax
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB4076:
	.seh_endprologue
	mov	eax, DWORD PTR g_dealloc[rip]
	add	eax, 1
	mov	DWORD PTR g_dealloc[rip], eax
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "after new: alloc=\0"
.LC1:
	.ascii " ctor=\0"
.LC2:
	.ascii "\12\0"
.LC3:
	.ascii "after delete: dealloc=\0"
.LC4:
	.ascii " dtor=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4083:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	eax, DWORD PTR g_alloc[rip]
	mov	ecx, 1
	add	eax, 1
	mov	DWORD PTR g_alloc[rip], eax
	call	malloc
	mov	rbx, rax
	mov	eax, DWORD PTR g_ctor[rip]
	add	eax, 1
	mov	DWORD PTR g_ctor[rip], eax
	mov	rax, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC0[rip]
	mov	rcx, rax
	mov	rsi, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_alloc[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_ctor[rip]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	test	rbx, rbx
	je	.L6
	mov	eax, DWORD PTR g_dtor[rip]
	mov	rcx, rbx
	add	eax, 1
	mov	DWORD PTR g_dtor[rip], eax
	mov	eax, DWORD PTR g_dealloc[rip]
	add	eax, 1
	mov	DWORD PTR g_dealloc[rip], eax
	call	free
.L6:
	lea	rdx, .LC3[rip]
	mov	rcx, rsi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_dealloc[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_dtor[rip]
	mov	rcx, rax
	call	_ZNSolsEi
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.globl	g_dtor
	.bss
	.align 4
g_dtor:
	.space 4
	.globl	g_ctor
	.align 4
g_ctor:
	.space 4
	.globl	g_dealloc
	.align 4
g_dealloc:
	.space 4
	.globl	g_alloc
	.align 4
g_alloc:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
