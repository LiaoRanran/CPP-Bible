	.file	"_ch101_open_addressing.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB61:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB102:
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
	.p2align 4,,10
	.p2align 3
.L9:
	movzx	eax, r10w
	lea	rcx, 65536[rax]
	jmp	.L8
	.p2align 4,,10
	.p2align 3
.L4:
	cmp	BYTE PTR 9[rdx], 0
	je	.L6
	cmp	r9d, DWORD PTR [rdx]
	je	.L7
.L6:
	add	rax, 1
	cmp	rcx, rax
	je	.L5
.L8:
	movzx	edx, ax
	lea	rdx, [rdx+rdx*2]
	lea	rdx, [r8+rdx*4]
	cmp	BYTE PTR 8[rdx], 0
	jne	.L4
.L7:
	lea	eax, [r9+r9]
	movd	xmm0, r9d
	mov	WORD PTR 8[rdx], r11w
	movd	xmm1, eax
	punpckldq	xmm0, xmm1
	movq	QWORD PTR [rdx], xmm0
.L5:
	add	r9d, 1
	sub	r10d, 1640531535
	cmp	r9d, 10000
	jne	.L9
	mov	eax, 55825
	jmp	.L13
.L19:
	cmp	BYTE PTR 9[rdx], 0
	jne	.L11
	cmp	DWORD PTR [rdx], 7777
	je	.L12
.L11:
	add	rax, 1
	cmp	rax, 121361
	je	.L14
.L13:
	movzx	edx, ax
	lea	rdx, [rdx+rdx*2]
	lea	rdx, [r8+rdx*4]
	cmp	BYTE PTR 8[rdx], 0
	jne	.L19
.L14:
	mov	edx, -1
.L10:
	lea	rcx, .LC1[rip]
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 40
	ret
.L12:
	mov	edx, DWORD PTR 4[rdx]
	jmp	.L10
	.seh_endproc
	.section .rdata,"dr"
	.align 2
.LC0:
	.byte	1
	.byte	0
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	calloc;	.scl	2;	.type	32;	.endef
