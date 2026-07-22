	.file	"_ch138_variant_opaque.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z18via_variant_opaqueRKSt7variantIJ4VAdd4VSubEE
	.def	_Z18via_variant_opaqueRKSt7variantIJ4VAdd4VSubEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z18via_variant_opaqueRKSt7variantIJ4VAdd4VSubEE
_Z18via_variant_opaqueRKSt7variantIJ4VAdd4VSubEE:
.LFB336:
	.seh_endprologue
	mov	eax, 1
	cmp	BYTE PTR 1[rcx], 1
	sbb	eax, -1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z3usei
	.def	_Z3usei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3usei
_Z3usei:
.LFB343:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	_Z11make_opaquei
	shr	ax, 8
	setne	al
	movzx	eax, al
	add	eax, 1
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Z11make_opaquei;	.scl	2;	.type	32;	.endef
