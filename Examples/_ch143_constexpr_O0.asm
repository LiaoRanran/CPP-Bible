	.file	"_ch143_constexpr.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z3fibi,"x"
	.linkonce discard
	.globl	_Z3fibi
	.def	_Z3fibi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3fibi
_Z3fibi:
.LFB0:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	mov	DWORD PTR 32[rbp], ecx
	cmp	DWORD PTR 32[rbp], 1
	jle	.L2
	mov	eax, DWORD PTR 32[rbp]
	sub	eax, 1
	mov	ecx, eax
	call	_Z3fibi
	mov	ebx, eax
	mov	eax, DWORD PTR 32[rbp]
	sub	eax, 2
	mov	ecx, eax
	call	_Z3fibi
	add	eax, ebx
	jmp	.L4
.L2:
	mov	eax, DWORD PTR 32[rbp]
.L4:
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
	.align 4
_ZL10kTableSize:
	.long	55
	.section	.text$_Z10make_tablei,"x"
	.linkonce discard
	.globl	_Z10make_tablei
	.def	_Z10make_tablei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10make_tablei
_Z10make_tablei:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	eax, DWORD PTR 16[rbp]
	mov	ecx, eax
	call	_Z3fibi
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z9use_tablev
	.def	_Z9use_tablev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_tablev
_Z9use_tablev:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	sub	rsp, 272
	.seh_stackalloc	272
	lea	rbp, 128[rsp]
	.seh_setframe	rbp, 128
	.seh_endprologue
	mov	DWORD PTR 140[rbp], 0
	jmp	.L8
.L9:
	mov	eax, DWORD PTR 140[rbp]
	mov	ecx, eax
	call	_Z10make_tablei
	mov	edx, DWORD PTR 140[rbp]
	movsx	rdx, edx
	mov	DWORD PTR -96[rbp+rdx*4], eax
	add	DWORD PTR 140[rbp], 1
.L8:
	cmp	DWORD PTR 140[rbp], 54
	jle	.L9
	mov	DWORD PTR 136[rbp], 0
	mov	DWORD PTR 132[rbp], 0
	jmp	.L10
.L11:
	mov	eax, DWORD PTR 132[rbp]
	cdqe
	mov	eax, DWORD PTR -96[rbp+rax*4]
	add	DWORD PTR 136[rbp], eax
	add	DWORD PTR 132[rbp], 1
.L10:
	cmp	DWORD PTR 132[rbp], 54
	jle	.L11
	mov	eax, DWORD PTR 136[rbp]
	add	rsp, 272
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
