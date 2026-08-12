	.file	"_ch38_bump_allocate.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13bump_allocateRPcS_y
	.def	_Z13bump_allocateRPcS_y;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13bump_allocateRPcS_y
_Z13bump_allocateRPcS_y:
.LFB17:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	add	r8, rax
	cmp	rdx, r8
	jb	.L3
	mov	QWORD PTR [rcx], r8
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	xor	eax, eax
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
