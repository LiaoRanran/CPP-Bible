	.file	"_atom_value_cat.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "lvalue  decltype((x))            => \0"
.LC1:
	.ascii "lvalue\0"
.LC2:
	.ascii "   glvalue / not-rvalue\12\0"
	.align 8
.LC3:
	.ascii "xvalue  decltype(std::move(x))    => \0"
.LC4:
	.ascii "xvalue\0"
.LC5:
	.ascii "   glvalue / rvalue\12\0"
	.align 8
.LC6:
	.ascii "prvalue decltype(42)             => \0"
.LC7:
	.ascii "prvalue\0"
.LC8:
	.ascii "   not-glvalue / rvalue\12\0"
	.align 8
.LC9:
	.ascii "lvalue  named rvalue ref int&& r  => \0"
.LC10:
	.ascii "   (int&)\12\0"
	.align 8
.LC11:
	.ascii "prvalue std::string() temporary   => \0"
.LC12:
	.ascii "   (std::string)\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4092:
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
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC2[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC3[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC4[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC5[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC6[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC7[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC8[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC9[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC1[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC10[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, rbx
	lea	rdx, .LC11[rip]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC7[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC12[rip]
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
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
