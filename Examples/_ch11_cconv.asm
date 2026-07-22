	.file	"_ch11_cconv.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7computellllll
	.def	_Z7computellllll;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7computellllll
_Z7computellllll:
.LFB0:
	.seh_endprologue
	lea	eax, [rcx+rdx*2]
	lea	r8d, [r8+r8*2]
	mov	ecx, DWORD PTR 40[rsp]
	mov	edx, DWORD PTR 48[rsp]
	add	eax, r8d
	lea	eax, [rax+r9*4]
	lea	ecx, [rcx+rcx*4]
	add	eax, ecx
	lea	edx, [rdx+rdx*2]
	lea	eax, [rax+rdx*2]
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
