	.file	"_asm_crtp.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN5VVec34implEv,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN5VVec34implEv
	.def	_ZN5VVec34implEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN5VVec34implEv
_ZN5VVec34implEv:
.LFB3:
	.seh_endprologue
	mov	eax, DWORD PTR 8[rcx]
	lea	eax, [rax+rax*2]
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z8use_crtpR4Vec3
	.def	_Z8use_crtpR4Vec3;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8use_crtpR4Vec3
_Z8use_crtpR4Vec3:
.LFB2:
	.seh_endprologue
	mov	eax, DWORD PTR [rcx]
	lea	eax, 1[rax+rax*2]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11use_virtualR5VBase
	.def	_Z11use_virtualR5VBase;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11use_virtualR5VBase
_Z11use_virtualR5VBase:
.LFB4:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rdx, _ZN5VVec34implEv[rip]
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR [rax]
	cmp	rax, rdx
	jne	.L5
	mov	eax, DWORD PTR 8[rcx]
	lea	eax, [rax+rax*2]
	add	eax, 1
	add	rsp, 40
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	call	rax
	add	eax, 1
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
