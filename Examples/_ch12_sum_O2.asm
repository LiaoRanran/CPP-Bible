	.file	"_ch12_sum.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6sum_toi
	.def	_Z6sum_toi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6sum_toi
_Z6sum_toi:
.LFB0:
	.seh_endprologue
	mov	r8d, ecx
	test	ecx, ecx
	jle	.L4
	xor	edx, edx
	and	r8d, 1
	lea	ecx, 1[rcx]
	mov	eax, 1
	je	.L3
	mov	eax, 2
	mov	edx, 1
	cmp	eax, ecx
	je	.L2
	.p2align 4
	.p2align 4
	.p2align 3
.L3:
	lea	edx, 1[rdx+rax*2]
	add	eax, 2
	cmp	eax, ecx
	jne	.L3
.L2:
	mov	rax, QWORD PTR .refptr.sink[rip]
	mov	DWORD PTR [rax], edx
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	mov	rax, QWORD PTR .refptr.sink[rip]
	xor	edx, edx
	mov	DWORD PTR [rax], edx
	mov	eax, edx
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.section	.rdata$.refptr.sink, "dr"
	.p2align	3, 0
	.globl	.refptr.sink
	.linkonce	discard
.refptr.sink:
	.quad	sink
