	.file	"_asm_ebo.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z12read_derivedP7Derived
	.def	_Z12read_derivedP7Derived;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12read_derivedP7Derived
_Z12read_derivedP7Derived:
.LFB17:
	.seh_endprologue
	mov	eax, DWORD PTR [rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11read_memberP8AsMember
	.def	_Z11read_memberP8AsMember;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11read_memberP8AsMember
_Z11read_memberP8AsMember:
.LFB18:
	.seh_endprologue
	mov	eax, DWORD PTR 4[rcx]
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
