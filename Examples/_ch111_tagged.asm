	.file	"_ch111_tagged.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z11push_taggedRSt6atomicInEPvS2_
	.def	_Z11push_taggedRSt6atomicInEPvS2_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11push_taggedRSt6atomicInEPvS2_
_Z11push_taggedRSt6atomicInEPvS2_:
.LFB697:
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	r9d, 4
	mov	QWORD PTR 64[rsp], rdx
	mov	QWORD PTR 48[rsp], r8
	lea	rdx, 64[rsp]
	lea	r8, 48[rsp]
	mov	QWORD PTR 72[rsp], 0
	mov	QWORD PTR 56[rsp], 1
	mov	DWORD PTR 32[rsp], 2
	call	__atomic_compare_exchange_16
	and	eax, 1
	add	rsp, 88
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__atomic_compare_exchange_16;	.scl	2;	.type	32;	.endef
