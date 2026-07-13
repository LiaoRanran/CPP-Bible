	.file	"_asm_tag.cpp"
	.intel_syntax noprefix
	.text
	.globl	g_count
	.bss
	.align 4
g_count:
	.space 4
	.globl	g_step
	.align 4
g_step:
	.space 4
	.text
	.globl	_Z7use_tagv
	.def	_Z7use_tagv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_tagv
_Z7use_tagv:
.LFB2292:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	ecx, 42
	call	_Z8dispatchIiEvT_
	mov	rax, QWORD PTR .LC0[rip]
	movq	xmm0, rax
	call	_Z8dispatchIdEvT_
	mov	QWORD PTR -12[rbp], 0
	mov	DWORD PTR -4[rbp], 0
	lea	rax, -12[rbp]
	mov	rcx, rax
	call	_Z12adv_dispatchIPiEvT_
	mov	edx, DWORD PTR g_count[rip]
	mov	eax, DWORD PTR g_step[rip]
	add	eax, edx
	add	rsp, 48
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z8dispatchIiEvT_,"x"
	.linkonce discard
	.globl	_Z8dispatchIiEvT_
	.def	_Z8dispatchIiEvT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8dispatchIiEvT_
_Z8dispatchIiEvT_:
.LFB2593:
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
	call	_Z4implIiEvT_St17integral_constantIbLb1EE
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z8dispatchIdEvT_,"x"
	.linkonce discard
	.globl	_Z8dispatchIdEvT_
	.def	_Z8dispatchIdEvT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8dispatchIdEvT_
_Z8dispatchIdEvT_:
.LFB2594:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	movsd	QWORD PTR 16[rbp], xmm0
	mov	rax, QWORD PTR 16[rbp]
	movq	xmm0, rax
	call	_Z4implIdEvT_St17integral_constantIbLb0EE
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z12adv_dispatchIPiEvT_,"x"
	.linkonce discard
	.globl	_Z12adv_dispatchIPiEvT_
	.def	_Z12adv_dispatchIPiEvT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12adv_dispatchIPiEvT_
_Z12adv_dispatchIPiEvT_:
.LFB2595:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	rax, QWORD PTR 16[rbp]
	mov	rcx, rax
	call	_Z3advIPiEvT_St26random_access_iterator_tag
	nop
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z4implIiEvT_St17integral_constantIbLb1EE,"x"
	.linkonce discard
	.globl	_Z4implIiEvT_St17integral_constantIbLb1EE
	.def	_Z4implIiEvT_St17integral_constantIbLb1EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4implIiEvT_St17integral_constantIbLb1EE
_Z4implIiEvT_St17integral_constantIbLb1EE:
.LFB2716:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx
	mov	eax, DWORD PTR g_count[rip]
	add	eax, 1
	mov	DWORD PTR g_count[rip], eax
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z4implIdEvT_St17integral_constantIbLb0EE,"x"
	.linkonce discard
	.globl	_Z4implIdEvT_St17integral_constantIbLb0EE
	.def	_Z4implIdEvT_St17integral_constantIbLb0EE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z4implIdEvT_St17integral_constantIbLb0EE
_Z4implIdEvT_St17integral_constantIbLb0EE:
.LFB2717:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	movsd	QWORD PTR 16[rbp], xmm0
	mov	eax, DWORD PTR g_count[rip]
	add	eax, 100
	mov	DWORD PTR g_count[rip], eax
	nop
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_Z3advIPiEvT_St26random_access_iterator_tag,"x"
	.linkonce discard
	.globl	_Z3advIPiEvT_St26random_access_iterator_tag
	.def	_Z3advIPiEvT_St26random_access_iterator_tag;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3advIPiEvT_St26random_access_iterator_tag
_Z3advIPiEvT_St26random_access_iterator_tag:
.LFB2718:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	QWORD PTR 16[rbp], rcx
	mov	eax, DWORD PTR g_step[rip]
	add	eax, 1
	mov	DWORD PTR g_step[rip], eax
	nop
	pop	rbp
	ret
	.seh_endproc
	.section .rdata,"dr"
_ZNSt8__detail30__integer_to_chars_is_unsignedIjEE:
	.byte	1
_ZNSt8__detail30__integer_to_chars_is_unsignedImEE:
	.byte	1
_ZNSt8__detail30__integer_to_chars_is_unsignedIyEE:
	.byte	1
	.align 8
.LC0:
	.long	0
	.long	1074003968
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
