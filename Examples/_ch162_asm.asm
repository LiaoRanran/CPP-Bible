	.file	"_ch162_asm.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE
	.def	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE
_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE:
.LFB1074:
	.seh_endprologue
	mov	rdx, QWORD PTR 8[rcx]
	mov	rax, QWORD PTR [rcx]
	add	rax, rdx
	mov	rcx, rax
	cmp	rax, rdx
	je	.L5
	mov	r8d, 8388627
	jmp	.L4
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L3:
	add	rdx, 1
	cmp	rcx, rdx
	je	.L5
.L4:
	movzx	eax, BYTE PTR [rdx]
	sub	eax, 9
	cmp	al, 23
	ja	.L3
	bt	r8, rax
	setc	al
	test	al, al
	je	.L3
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	xor	eax, eax
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii " \11\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1075:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rax, .LC0[rip]
	lea	rcx, 32[rsp]
	mov	QWORD PTR 32[rsp], 3
	mov	QWORD PTR 40[rsp], rax
	call	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE
	xor	eax, 1
	movzx	eax, al
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
