	.file	"_ch133_vec.cpp"
	.intel_syntax noprefix
	.text
	.globl	column_filter_sum
	.def	column_filter_sum;	.scl	2;	.type	32;	.endef
	.seh_proc	column_filter_sum
column_filter_sum:
.LFB16:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	QWORD PTR 40[rbp], r9
	mov	QWORD PTR -8[rbp], 0
	mov	QWORD PTR -16[rbp], 0
	mov	QWORD PTR -24[rbp], 0
	jmp	.L2
.L4:
	mov	rax, QWORD PTR -24[rbp]
	lea	rdx, 0[0+rax*8]
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	mov	rax, QWORD PTR [rax]
	mov	QWORD PTR -32[rbp], rax
	mov	rax, QWORD PTR -32[rbp]
	cmp	rax, QWORD PTR 32[rbp]
	jb	.L3
	mov	rax, QWORD PTR -32[rbp]
	cmp	rax, QWORD PTR 40[rbp]
	jnb	.L3
	mov	rdx, QWORD PTR -32[rbp]
	mov	r8, QWORD PTR 48[rbp]
	mov	rax, QWORD PTR -8[rbp]
	lea	rcx, 1[rax]
	mov	QWORD PTR -8[rbp], rcx
	sal	rax, 3
	add	rax, r8
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -32[rbp]
	add	QWORD PTR -16[rbp], rax
.L3:
	add	QWORD PTR -24[rbp], 1
.L2:
	mov	rax, QWORD PTR -24[rbp]
	cmp	rax, QWORD PTR 24[rbp]
	jb	.L4
	mov	rax, QWORD PTR 56[rbp]
	mov	rdx, QWORD PTR -16[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.globl	column_transform
	.def	column_transform;	.scl	2;	.type	32;	.endef
	.seh_proc	column_transform
column_transform:
.LFB17:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	QWORD PTR 24[rbp], rdx
	mov	QWORD PTR 32[rbp], r8
	mov	QWORD PTR -8[rbp], 0
	jmp	.L7
.L8:
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, 0[0+rax*8]
	mov	rax, QWORD PTR 16[rbp]
	add	rax, rdx
	mov	rdx, QWORD PTR [rax]
	mov	rax, rdx
	add	rax, rax
	add	rdx, rax
	mov	rax, QWORD PTR -8[rbp]
	lea	rcx, 0[0+rax*8]
	mov	rax, QWORD PTR 24[rbp]
	add	rax, rcx
	add	rdx, 1
	mov	QWORD PTR [rax], rdx
	add	QWORD PTR -8[rbp], 1
.L7:
	mov	rax, QWORD PTR -8[rbp]
	cmp	rax, QWORD PTR 32[rbp]
	jb	.L8
	nop
	nop
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "k=%zu sum=%llu\12\0"
.LC1:
	.ascii "%llu \0"
.LC2:
	.ascii "\12\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB35:
	push	rbp
	.seh_pushreg	rbp
	sub	rsp, 272
	.seh_stackalloc	272
	lea	rbp, 128[rsp]
	.seh_setframe	rbp, 128
	.seh_endprologue
	call	__main
	mov	QWORD PTR 64[rbp], 10
	mov	QWORD PTR 72[rbp], 20
	mov	QWORD PTR 80[rbp], 30
	mov	QWORD PTR 88[rbp], 40
	mov	QWORD PTR 96[rbp], 50
	mov	QWORD PTR 104[rbp], 60
	mov	QWORD PTR 112[rbp], 70
	mov	QWORD PTR 120[rbp], 80
	mov	QWORD PTR -8[rbp], 0
	lea	rax, 64[rbp]
	lea	rdx, -8[rbp]
	mov	QWORD PTR 40[rsp], rdx
	mov	rdx, rbp
	mov	QWORD PTR 32[rsp], rdx
	mov	r9d, 75
	mov	r8d, 25
	mov	edx, 8
	mov	rcx, rax
	call	column_filter_sum
	mov	QWORD PTR 128[rbp], rax
	mov	rdx, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR 128[rbp]
	lea	rcx, .LC0[rip]
	mov	r8, rdx
	mov	rdx, rax
	call	__mingw_printf
	lea	rdx, -80[rbp]
	lea	rax, 64[rbp]
	mov	r8d, 8
	mov	rcx, rax
	call	column_transform
	mov	DWORD PTR 140[rbp], 0
	jmp	.L10
.L11:
	mov	eax, DWORD PTR 140[rbp]
	cdqe
	mov	rax, QWORD PTR -80[rbp+rax*8]
	lea	rcx, .LC1[rip]
	mov	rdx, rax
	call	__mingw_printf
	add	DWORD PTR 140[rbp], 1
.L10:
	cmp	DWORD PTR 140[rbp], 7
	jle	.L11
	lea	rax, .LC2[rip]
	mov	rcx, rax
	call	__mingw_printf
	mov	rax, QWORD PTR 128[rbp]
	add	rsp, 272
	pop	rbp
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
