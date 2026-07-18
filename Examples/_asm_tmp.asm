	.file	"_asm_tmp.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7use_tmpv
	.def	_Z7use_tmpv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_tmpv
_Z7use_tmpv:
.LFB205:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	DWORD PTR 8[rsp], 120
	mov	DWORD PTR 12[rsp], 12
	mov	DWORD PTR 16[rsp], 1
	mov	DWORD PTR 20[rsp], 0
	mov	DWORD PTR 24[rsp], 1
	mov	DWORD PTR 28[rsp], 15
	mov	eax, DWORD PTR 8[rsp]
	mov	r10d, DWORD PTR 12[rsp]
	mov	r9d, DWORD PTR 16[rsp]
	mov	r8d, DWORD PTR 20[rsp]
	mov	ecx, DWORD PTR 24[rsp]
	add	eax, r10d
	mov	edx, DWORD PTR 28[rsp]
	add	eax, r9d
	sub	eax, r8d
	add	eax, ecx
	add	eax, edx
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
