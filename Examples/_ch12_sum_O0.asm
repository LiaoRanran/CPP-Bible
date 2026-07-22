	.file	"_ch12_sum.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z6sum_toi
	.def	_Z6sum_toi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6sum_toi
_Z6sum_toi:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 16
	.seh_stackalloc	16
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	DWORD PTR -4[rbp], 0
	mov	DWORD PTR -8[rbp], 1
	jmp	.L2
.L3:
	mov	eax, DWORD PTR -8[rbp]
	add	DWORD PTR -4[rbp], eax
	add	DWORD PTR -8[rbp], 1
.L2:
	mov	eax, DWORD PTR -8[rbp]
	cmp	eax, DWORD PTR 16[rbp]
	jle	.L3
	mov	rax, QWORD PTR .refptr.sink[rip]
	mov	edx, DWORD PTR -4[rbp]
	mov	DWORD PTR [rax], edx
	mov	eax, DWORD PTR -4[rbp]
	add	rsp, 16
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.section	.rdata$.refptr.sink, "dr"
	.p2align	3, 0
	.globl	.refptr.sink
	.linkonce	discard
.refptr.sink:
	.quad	sink
