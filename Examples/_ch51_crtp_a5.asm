	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13crtp_dispatchR7DogCRTP
	.def	_Z13crtp_dispatchR7DogCRTP;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13crtp_dispatchR7DogCRTP
_Z13crtp_dispatchR7DogCRTP:
.LFB4:
	.seh_endprologue
	add	DWORD PTR [rcx], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13virt_dispatchP10AnimalVirt
	.def	_Z13virt_dispatchP10AnimalVirt;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13virt_dispatchP10AnimalVirt
_Z13virt_dispatchP10AnimalVirt:
.LFB5:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	rex.W jmp	[QWORD PTR [rax]]
	.seh_endproc
	.p2align 4
	.globl	_Z10final_callP8DogFinal
	.def	_Z10final_callP8DogFinal;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10final_callP8DogFinal
_Z10final_callP8DogFinal:
.LFB6:
	.seh_endprologue
	add	DWORD PTR 8[rcx], 2
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
