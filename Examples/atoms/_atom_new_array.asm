	.file	"_atom_new_array.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znay
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znay
_Znay:
.LFB4074:
	.seh_endprologue
	mov	eax, DWORD PTR g_a[rip]
	add	eax, 1
	mov	DWORD PTR g_a[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdaPv
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPv
_ZdaPv:
.LFB4075:
	.seh_endprologue
	mov	eax, DWORD PTR g_d[rip]
	add	eax, 1
	mov	DWORD PTR g_d[rip], eax
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "array new[] calls=\0"
.LC1:
	.ascii "\12\0"
.LC2:
	.ascii "array delete[] calls=\0"
.LC3:
	.ascii "nothrow huge returned null=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4076:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	eax, DWORD PTR g_a[rip]
	lea	rdx, .LC0[rip]
	add	eax, 1
	mov	rcx, rbx
	mov	DWORD PTR g_a[rip], eax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_a[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	eax, DWORD PTR g_d[rip]
	lea	rdx, .LC2[rip]
	mov	rcx, rbx
	add	eax, 1
	mov	DWORD PTR g_d[rip], eax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, DWORD PTR g_d[rip]
	mov	rcx, rax
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rdx, QWORD PTR .refptr._ZSt7nothrow[rip]
	movabs	rcx, 400000000000
	call	_ZnayRKSt9nothrow_t
	lea	rdx, .LC3[rip]
	mov	rcx, rbx
	mov	rsi, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	edx, edx
	test	rsi, rsi
	sete	dl
	mov	rcx, rax
	call	_ZNSo9_M_insertIbEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	test	rsi, rsi
	je	.L5
	mov	eax, DWORD PTR g_d[rip]
	mov	rcx, rsi
	add	eax, 1
	mov	DWORD PTR g_d[rip], eax
	call	free
.L5:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.globl	g_d
	.bss
	.align 4
g_d:
	.space 4
	.globl	g_a
	.align 4
g_a:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZnayRKSt9nothrow_t;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIbEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt7nothrow, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt7nothrow
	.linkonce	discard
.refptr._ZSt7nothrow:
	.quad	_ZSt7nothrow
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
