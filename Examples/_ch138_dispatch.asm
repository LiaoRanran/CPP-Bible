	.file	"_ch138_dispatch.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNK3Add4evalEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK3Add4evalEv
	.def	_ZNK3Add4evalEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3Add4evalEv
_ZNK3Add4evalEv:
.LFB2696:
	.seh_endprologue
	mov	eax, 1
	ret
	.seh_endproc
	.section	.text$_ZNK3Sub4evalEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNK3Sub4evalEv
	.def	_ZNK3Sub4evalEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNK3Sub4evalEv
_ZNK3Sub4evalEv:
.LFB2697:
	.seh_endprologue
	mov	eax, 2
	ret
	.seh_endproc
	.section	.text$_ZN3AddD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3AddD1Ev
	.def	_ZN3AddD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3AddD1Ev
_ZN3AddD1Ev:
.LFB2722:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN3SubD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3SubD1Ev
	.def	_ZN3SubD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3SubD1Ev
_ZN3SubD1Ev:
.LFB2729:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text$_ZN3SubD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3SubD0Ev
	.def	_ZN3SubD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3SubD0Ev
_ZN3SubD0Ev:
.LFB2730:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.section	.text$_ZN3AddD0Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3AddD0Ev
	.def	_ZN3AddD0Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3AddD0Ev
_ZN3AddD0Ev:
.LFB2723:
	.seh_endprologue
	mov	edx, 8
	jmp	_ZdlPvy
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z11via_virtualRK4Base
	.def	_Z11via_virtualRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_virtualRK4Base
_Z11via_virtualRK4Base:
.LFB2701:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR 16[rax]]
	.seh_endproc
	.p2align 4
	.globl	_Z11via_variantRKSt7variantIJ4VAdd4VSubEE
	.def	_Z11via_variantRKSt7variantIJ4VAdd4VSubEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11via_variantRKSt7variantIJ4VAdd4VSubEE
_Z11via_variantRKSt7variantIJ4VAdd4VSubEE:
.LFB2702:
	.seh_endprologue
	cmp	BYTE PTR 1[rcx], 1
	sbb	eax, eax
	add	eax, 2
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2709:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	mov	edx, 9
	call	_ZNSolsEi
	mov	BYTE PTR 47[rsp], 10
	mov	rcx, rax
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR -24[rax]
	cmp	QWORD PTR 16[rcx+rax], 0
	je	.L13
	lea	rdx, 47[rsp]
	mov	r8d, 1
	call	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x
.L14:
	mov	eax, 9
	add	rsp, 56
	ret
.L13:
	mov	edx, 10
	call	_ZNSo3putEc
	jmp	.L14
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZNSolsEi;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_x;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
