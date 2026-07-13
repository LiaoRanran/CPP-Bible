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
	mov	rcx, QWORD PTR -32[rbp]
	mov	r8, QWORD PTR 48[rbp]
	mov	rax, QWORD PTR -8[rbp]
	lea	rdx, 1[rax]
	mov	QWORD PTR -8[rbp], rdx
	sal	rax, 3
	add	rax, r8
	mov	QWORD PTR [rax], rcx
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
