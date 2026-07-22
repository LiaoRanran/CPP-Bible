	.file	"_ch130_allocator.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10make_threeR5Arena
	.def	_Z10make_threeR5Arena;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10make_threeR5Arena
_Z10make_threeR5Arena:
.LFB19:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	lea	rax, 16[rdx]
	cmp	QWORD PTR 16[rcx], rax
	mov	eax, 0
	cmovnb	rax, rdx
	add	rdx, 64
	mov	QWORD PTR 8[rcx], rdx
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB20:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
