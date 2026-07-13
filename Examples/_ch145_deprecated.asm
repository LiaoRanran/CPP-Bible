	.file	"_ch145_deprecated.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7old_apiv
	.def	_Z7old_apiv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7old_apiv
_Z7old_apiv:
.LFB0:
	.seh_endprologue
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z7new_apiv
	.def	_Z7new_apiv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7new_apiv
_Z7new_apiv:
.LFB1:
	.seh_endprologue
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB2:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
