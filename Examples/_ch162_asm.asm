	.file	"_ch162_asm.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE
	.def	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE
_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE:
.LFB695:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rdx, QWORD PTR [rcx]
	add	rdx, rax
	cmp	rdx, rax
	mov	rcx, rdx
	je	.L5
	movabs	r8, 4294977024
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L3:
	add	rax, 1
	cmp	rcx, rax
	je	.L5
.L4:
	movzx	edx, BYTE PTR [rax]
	cmp	dl, 32
	ja	.L3
	bt	r8, rdx
	setc	dl
	test	dl, dl
	je	.L3
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	xor	edx, edx
	mov	eax, edx
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC0:
	.ascii " \11\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB696:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rax, .LC0[rip]
	mov	QWORD PTR 32[rsp], 3
	lea	rcx, 32[rsp]
	mov	QWORD PTR 40[rsp], rax
	call	_Z6any_wsSt17basic_string_viewIcSt11char_traitsIcEE
	xor	eax, 1
	movzx	eax, al
	add	rsp, 56
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
