	.file	"_atom_false_sharing.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "cache_line_size=%zu\12\0"
.LC1:
	.ascii "atomic_ll_size=%zu\12\0"
.LC2:
	.ascii "tight_offset_bytes=%zu\12\0"
.LC3:
	.ascii "tight_same_line=%d\12\0"
.LC4:
	.ascii "padded_offset_bytes=%zu\12\0"
.LC5:
	.ascii "padded_same_line=%d\12\0"
.LC6:
	.ascii "padded_sizeof=%zu\12\0"
.LC7:
	.ascii "pod_offset_bytes=%zu\12\0"
.LC8:
	.ascii "pod_same_line=%d\12\0"
	.align 8
.LC9:
	.ascii "same_object_members_same_line=%d\12\0"
.LC10:
	.ascii "cross_object_same_line=%d\12\0"
.LC11:
	.ascii "std\0"
.LC12:
	.ascii "kline_source=%s\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB697:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 240
	.seh_stackalloc	240
	.seh_endprologue
	xor	edi, edi
	call	__main
	mov	edx, 64
	lea	rsi, 32[rsp]
	lea	rcx, .LC0[rip]
	call	__mingw_printf
	mov	edx, 8
	shr	rsi, 6
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	mov	edx, 8
	lea	rbx, 127[rsp]
	lea	rcx, .LC2[rip]
	call	__mingw_printf
	lea	rax, 40[rsp]
	and	rbx, -64
	lea	rcx, .LC3[rip]
	shr	rax, 6
	cmp	rax, rsi
	sete	dil
	shr	rbx, 6
	mov	edx, edi
	call	__mingw_printf
	mov	edx, 64
	lea	rcx, .LC4[rip]
	call	__mingw_printf
	xor	edx, edx
	lea	rcx, .LC5[rip]
	call	__mingw_printf
	mov	edx, 128
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	mov	edx, 8
	lea	rcx, .LC7[rip]
	call	__mingw_printf
	lea	rdx, 48[rsp]
	lea	rax, 56[rsp]
	shr	rdx, 6
	shr	rax, 6
	lea	rcx, .LC8[rip]
	cmp	rdx, rax
	sete	dl
	movzx	edx, dl
	call	__mingw_printf
	mov	edx, edi
	lea	rcx, .LC9[rip]
	call	__mingw_printf
	xor	edx, edx
	cmp	rsi, rbx
	lea	rcx, .LC10[rip]
	sete	dl
	call	__mingw_printf
	lea	rdx, .LC11[rip]
	lea	rcx, .LC12[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 240
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
