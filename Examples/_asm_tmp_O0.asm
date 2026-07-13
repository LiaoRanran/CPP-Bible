	.file	"_asm_tmp.cpp"
	.intel_syntax noprefix
	.text
	.globl	_Z7use_tmpv
	.def	_Z7use_tmpv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_tmpv
_Z7use_tmpv:
.LFB192:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	DWORD PTR -4[rbp], 120
	mov	DWORD PTR -8[rbp], 12
	mov	DWORD PTR -12[rbp], 1
	mov	DWORD PTR -16[rbp], 0
	mov	DWORD PTR -20[rbp], 1
	mov	ecx, eax
	call	_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE
	mov	DWORD PTR -24[rbp], eax
	mov	edx, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR -8[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -12[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -16[rbp]
	sub	edx, eax
	mov	eax, DWORD PTR -20[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -24[rbp]
	add	eax, edx
	add	rsp, 64
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE,"x"
	.linkonce discard
	.globl	_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE
	.def	_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE
_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE:
.LFB193:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	eax, 15
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
