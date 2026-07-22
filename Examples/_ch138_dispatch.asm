	.file	"_ch138_dispatch.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z11via_virtualRK4Base
	.def	_Z11via_virtualRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK4Base
_Z11via_virtualRK4Base:
.LFB4188:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 16[rax]]
	.seh_endproc
	.p2align 4
	.globl	_Z11via_variantRKSt7variantIJ4VAdd4VSubEE
	.def	_Z11via_variantRKSt7variantIJ4VAdd4VSubEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_variantRKSt7variantIJ4VAdd4VSubEE
_Z11via_variantRKSt7variantIJ4VAdd4VSubEE:
.LFB4189:
	.seh_endprologue
	mov	eax, 1
	cmp	BYTE PTR 1[rcx], 1
	sbb	eax, -1
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB4196:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	edx, 9
	call	_ZNSolsEi
	mov	BYTE PTR 47[rsp], 10
	mov	rdx, QWORD PTR [rax]
	mov	rdx, QWORD PTR -24[rdx]
	cmp	QWORD PTR 16[rax+rdx], 0
	je	.L7
	lea	rdx, 47[rsp]
	mov	r8d, 1
	mov	rcx, rax
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L8:
	mov	eax, 9
	add	rsp, 56
	ret
.L7:
	mov	edx, 10
	mov	rcx, rax
	call	_ZNSo3putEc
	jmp	.L8
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.p2align	3, 0
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
