	.file	"_atom_align_pad.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "sizeof(Padded)=\0"
.LC1:
	.ascii "\12\0"
.LC2:
	.ascii "offsetof a=\0"
.LC3:
	.ascii "offsetof b=\0"
.LC4:
	.ascii "padding bytes=\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4074:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	__main
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC0[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 8
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC2[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	edx, edx
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC3[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 4
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC4[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 3
	mov	rcx, rax
	call	_ZNSo9_M_insertIyEERSoT_
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIyEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
