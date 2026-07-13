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
	test	ecx, ecx
	jle	.L4
	lea	r8d, 1[rcx]
	xor	edx, edx
	and	ecx, 1
	mov	eax, 1
	je	.L3
	mov	eax, 2
	mov	edx, 1
	cmp	eax, r8d
	je	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	lea	edx, 1[rdx+rax*2]
	add	eax, 2
	cmp	eax, r8d
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
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.section	.rdata$.refptr.sink, "dr"
	.globl	.refptr.sink
	.linkonce	discard
.refptr.sink:
	.quad	sink
