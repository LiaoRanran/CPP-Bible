	.file	"_ch133_vec.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	column_filter_sum
	.def	column_filter_sum;	.scl	2;	.type	32;	.endef
	.seh_proc	column_filter_sum
column_filter_sum:
.LFB17:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	mov	rbx, QWORD PTR 48[rsp]
	test	rdx, rdx
	je	.L5
	lea	r11, [rcx+rdx*8]
	xor	r10d, r10d
	xor	edx, edx
	.p2align 4
	.p2align 3
.L4:
	mov	rax, QWORD PTR [rcx]
	cmp	rax, r8
	jb	.L3
	cmp	rax, r9
	jnb	.L3
	mov	QWORD PTR [rbx+r10*8], rax
	add	rdx, rax
	add	r10, 1
.L3:
	add	rcx, 8
	cmp	rcx, r11
	jne	.L4
	mov	rax, QWORD PTR 56[rsp]
	mov	QWORD PTR [rax], rdx
	mov	rax, r10
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	mov	rax, QWORD PTR 56[rsp]
	xor	r10d, r10d
	mov	QWORD PTR [rax], rdx
	mov	rax, r10
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	column_transform
	.def	column_transform;	.scl	2;	.type	32;	.endef
	.seh_proc	column_transform
column_transform:
.LFB18:
	.seh_endprologue
	test	r8, r8
	je	.L14
	xor	eax, eax
	.p2align 5
	.p2align 4
	.p2align 3
.L16:
	mov	r9, QWORD PTR [rcx+rax*8]
	lea	r9, 1[r9+r9*2]
	mov	QWORD PTR [rdx+rax*8], r9
	add	rax, 1
	cmp	r8, rax
	jne	.L16
.L14:
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC4:
	.ascii "k=%zu sum=%llu\12\0"
.LC5:
	.ascii "%llu \0"
.LC6:
	.ascii "\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB38:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 256
	.seh_stackalloc	256
	.seh_endprologue
	call	__main
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	lea	rax, 56[rsp]
	lea	rsi, 128[rsp]
	mov	QWORD PTR 40[rsp], rax
	mov	edx, 8
	lea	rcx, 64[rsp]
	mov	r9d, 75
	movaps	XMMWORD PTR 64[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC1[rip]
	mov	r8d, 25
	lea	rbx, 192[rsp]
	mov	QWORD PTR 32[rsp], rsi
	movaps	XMMWORD PTR 80[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC2[rip]
	movaps	XMMWORD PTR 96[rsp], xmm0
	movdqa	xmm0, XMMWORD PTR .LC3[rip]
	movaps	XMMWORD PTR 112[rsp], xmm0
	call	column_filter_sum
	mov	r8, QWORD PTR 56[rsp]
	lea	rcx, .LC4[rip]
	mov	rdx, rax
	mov	rdi, rax
	call	__mingw_printf
	lea	rdx, 64[rsp]
	mov	rcx, rbx
	.p2align 5
	.p2align 4
	.p2align 3
.L22:
	mov	r8, QWORD PTR [rdx]
	add	rdx, 8
	add	rcx, 8
	lea	r8, 1[r8+r8*2]
	mov	QWORD PTR -8[rcx], r8
	cmp	rdx, rsi
	jne	.L22
	lea	rsi, 64[rbx]
	.p2align 4
	.p2align 3
.L23:
	mov	rdx, QWORD PTR [rbx]
	lea	rcx, .LC5[rip]
	add	rbx, 8
	call	__mingw_printf
	cmp	rsi, rbx
	jne	.L23
	lea	rcx, .LC6[rip]
	call	__mingw_printf
	mov	eax, edi
	add	rsp, 256
	pop	rbx
	pop	rsi
	pop	rdi
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.quad	10
	.quad	20
	.align 16
.LC1:
	.quad	30
	.quad	40
	.align 16
.LC2:
	.quad	50
	.quad	60
	.align 16
.LC3:
	.quad	70
	.quad	80
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
