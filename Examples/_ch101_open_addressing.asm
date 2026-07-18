	.file	"_ch101_open_addressing.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC1:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB78:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	edx, 12
	mov	ecx, 65536
	call	calloc
	movzx	r11d, WORD PTR .LC0[rip]
	xor	r10d, r10d
	xor	r9d, r9d
	mov	r8, rax
	.p2align 4
	.p2align 3
.L7:
	movzx	eax, r10w
	lea	rcx, 65536[rax]
	.p2align 4
	.p2align 3
.L6:
	movzx	edx, ax
	lea	rdx, [rdx+rdx*2]
	lea	rdx, [r8+rdx*4]
	cmp	BYTE PTR 8[rdx], 0
	je	.L5
	cmp	BYTE PTR 9[rdx], 0
	je	.L4
	cmp	DWORD PTR [rdx], r9d
	je	.L5
.L4:
	add	rax, 1
	cmp	rax, rcx
	jne	.L6
.L3:
	add	r9d, 1
	sub	r10d, 1640531535
	cmp	r9d, 10000
	jne	.L7
	mov	eax, 55825
.L11:
	movzx	edx, ax
	lea	rdx, [rdx+rdx*2]
	lea	rdx, [r8+rdx*4]
	cmp	BYTE PTR 8[rdx], 0
	je	.L12
	cmp	BYTE PTR 9[rdx], 0
	jne	.L9
	cmp	DWORD PTR [rdx], 7777
	je	.L10
.L9:
	add	rax, 1
	cmp	rax, 121361
	jne	.L11
.L12:
	mov	edx, -1
.L8:
	lea	rcx, .LC1[rip]
	call	__mingw_printf
	xor	eax, eax
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	lea	eax, [r9+r9]
	mov	DWORD PTR [rdx], r9d
	mov	DWORD PTR 4[rdx], eax
	mov	WORD PTR 8[rdx], r11w
	jmp	.L3
.L10:
	mov	edx, DWORD PTR 4[rdx]
	jmp	.L8
	.seh_endproc
	.section .rdata,"dr"
	.align 2
.LC0:
	.byte	1
	.byte	0
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	calloc;	.scl	2;	.type	32;	.endef
