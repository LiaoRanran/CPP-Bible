	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z4leafii
	.def	_Z4leafii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4leafii
_Z4leafii:
.LFB49:
	.seh_endprologue
	add	ecx, edx
	lea	eax, 3[rcx+rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6calleriiii
	.def	_Z6calleriiii;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6calleriiii
_Z6calleriiii:
.LFB50:
	.seh_endprologue
	add	ecx, edx
	add	r8d, r9d
	lea	eax, 3[rcx+rcx]
	lea	eax, 3[rax+r8*2]
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
