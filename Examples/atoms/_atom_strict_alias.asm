	.file	"_atom_strict_alias.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10alias_killPiPf
	.def	_Z10alias_killPiPf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10alias_killPiPf
_Z10alias_killPiPf:
.LFB59:
	.seh_endprologue
	mov	eax, 1
	mov	DWORD PTR [rcx], 1
	mov	DWORD PTR [rdx], 0x40000000
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z19write_via_float_ptrv
	.def	_Z19write_via_float_ptrv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z19write_via_float_ptrv
_Z19write_via_float_ptrv:
.LFB60:
	.seh_endprologue
	mov	eax, 1073741824
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z16write_via_memcpyv
	.def	_Z16write_via_memcpyv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16write_via_memcpyv
_Z16write_via_memcpyv:
.LFB61:
	.seh_endprologue
	mov	eax, 1073741824
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "\346\230\257\0"
.LC2:
	.ascii "\345\220\246\0"
	.align 8
.LC3:
	.ascii "A \345\207\275\346\225\260\350\277\224\345\233\236=%d \345\206\205\345\255\230\345\256\236\351\231\205=%d \350\207\252\346\264\275=%s\12\0"
	.align 8
.LC4:
	.ascii "B UB\350\267\257\345\276\204=%d \345\220\210\350\247\204\350\267\257\345\276\204=%d \344\270\200\350\207\264=%s\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB62:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	lea	rbx, .LC1[rip]
	call	__main
	lea	rcx, 44[rsp]
	lea	r9, .LC2[rip]
	mov	rdx, rcx
	call	_Z10alias_killPiPf
	movsxd	rax, DWORD PTR 44[rsp]
	mov	edx, 2147483648
	lea	rcx, .LC3[rip]
	mov	r8, rax
	add	rax, 1
	mov	QWORD PTR _ZL6g_sink[rip], rax
	mov	rax, QWORD PTR _ZL6g_sink[rip]
	add	rax, rdx
	cmp	r8d, 1
	mov	edx, 1
	cmove	r9, rbx
	mov	QWORD PTR _ZL6g_sink[rip], rax
	call	__mingw_printf
	mov	r9, rbx
	mov	r8d, 1073741824
	mov	edx, 1073741824
	lea	rcx, .LC4[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
.lcomm _ZL6g_sink,8,8
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
