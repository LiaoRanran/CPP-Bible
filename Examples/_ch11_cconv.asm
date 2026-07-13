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
	lea	r8d, [r8+r8*2]
	mov	eax, ecx
	mov	ecx, DWORD PTR 40[rsp]
	mov	r10d, edx
	mov	edx, DWORD PTR 48[rsp]
	lea	eax, [rax+r10*2]
	add	eax, r8d
	lea	eax, [rax+r9*4]
	lea	ecx, [rcx+rcx*4]
	lea	edx, [rdx+rdx*2]
	add	eax, ecx
	lea	eax, [rax+rdx*2]
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
