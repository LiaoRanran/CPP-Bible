	.file	"_ch133_vec.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	column_filter_sum
	.def	column_filter_sum;	.scl	2;	.type	32;	.endef
	.seh_proc	column_filter_sum
column_filter_sum:
.LFB16:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	mov	rbx, QWORD PTR 48[rsp]
	test	rdx, rdx
	je	.L5
	lea	r11, [rcx+rdx*8]
	xor	r10d, r10d
	xor	edx, edx
	.p2align 4,,10
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
	cmp	r11, rcx
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
.LFB17:
	.seh_endprologue
	test	r8, r8
	mov	r9, rdx
	je	.L34
	lea	rax, -1[r8]
	cmp	rax, 3
	jbe	.L22
	lea	rax, 8[rcx]
	sub	rdx, rax
	xor	eax, eax
	cmp	rdx, 16
	ja	.L35
	.p2align 4,,10
	.p2align 3
.L20:
	mov	rdx, QWORD PTR [rcx+rax*8]
	lea	rdx, 1[rdx+rdx*2]
	mov	QWORD PTR [r9+rax*8], rdx
	add	rax, 1
	cmp	r8, rax
	jne	.L20
.L34:
	ret
	.p2align 4,,10
	.p2align 3
.L35:
	vpbroadcastq	ymm1, QWORD PTR .LC1[rip]
	mov	rdx, r8
	shr	rdx, 2
	sal	rdx, 5
	.p2align 4,,10
	.p2align 3
.L17:
	vmovdqu	ymm2, YMMWORD PTR [rcx+rax]
	vpsllq	ymm0, ymm2, 1
	vpaddq	ymm0, ymm0, ymm2
	vpaddq	ymm0, ymm0, ymm1
	vmovdqu	YMMWORD PTR [r9+rax], ymm0
	add	rax, 32
	cmp	rax, rdx
	jne	.L17
	mov	rax, r8
	and	rax, -4
	test	r8b, 3
	je	.L33
	.p2align 4,,10
	.p2align 3
.L19:
	mov	rdx, QWORD PTR [rcx+rax*8]
	lea	rdx, 1[rdx+rdx*2]
	mov	QWORD PTR [r9+rax*8], rdx
	add	rax, 1
	cmp	rax, r8
	jb	.L19
.L33:
	vzeroupper
	ret
	.p2align 4,,10
	.p2align 3
.L22:
	xor	eax, eax
	jmp	.L20
	.seh_endproc
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB25:
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
.LC4:
	.ascii "k=%zu sum=%llu\12\0"
.LC7:
	.ascii "%llu \0"
.LC8:
	.ascii "\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB63:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 264
	.seh_stackalloc	264
	.seh_endprologue
	lea	rsi, .LC7[rip]
	call	__main
	vmovdqa	ymm0, YMMWORD PTR .LC2[rip]
	lea	rax, 56[rsp]
	mov	r9d, 75
	mov	QWORD PTR 40[rsp], rax
	lea	rcx, 64[rsp]
	mov	r8d, 25
	mov	edx, 8
	vmovdqu	YMMWORD PTR 64[rsp], ymm0
	lea	rax, 128[rsp]
	vmovdqa	ymm0, YMMWORD PTR .LC3[rip]
	mov	QWORD PTR 32[rsp], rax
	lea	rbx, 192[rsp]
	vmovdqu	YMMWORD PTR 96[rsp], ymm0
	lea	rdi, 256[rsp]
	call	column_filter_sum
	mov	r8, QWORD PTR 56[rsp]
	lea	rcx, .LC4[rip]
	mov	rdx, rax
	mov	rbp, rax
	call	_Z6printfPKcz
	vmovdqa	ymm0, YMMWORD PTR .LC5[rip]
	vmovdqu	YMMWORD PTR 192[rsp], ymm0
	vmovdqa	ymm0, YMMWORD PTR .LC6[rip]
	vmovdqu	YMMWORD PTR 224[rsp], ymm0
	vzeroupper
	.p2align 4,,10
	.p2align 3
.L38:
	mov	rdx, QWORD PTR [rbx]
	mov	rcx, rsi
	add	rbx, 8
	call	_Z6printfPKcz
	cmp	rdi, rbx
	jne	.L38
	lea	rcx, .LC8[rip]
	call	_Z6printfPKcz
	mov	eax, ebp
	add	rsp, 264
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC1:
	.quad	1
	.align 32
.LC2:
	.quad	10
	.quad	20
	.quad	30
	.quad	40
	.align 32
.LC3:
	.quad	50
	.quad	60
	.quad	70
	.quad	80
	.align 32
.LC5:
	.quad	31
	.quad	61
	.quad	91
	.quad	121
	.align 32
.LC6:
	.quad	151
	.quad	181
	.quad	211
	.quad	241
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
