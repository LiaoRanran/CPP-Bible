	.file	"_asm_tmp_recur.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZN3FibILi0EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi0EE7computeEv
	.def	_ZN3FibILi0EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi0EE7computeEv
_ZN3FibILi0EE7computeEv:
.LFB1:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	eax, 0
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi1EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi1EE7computeEv
	.def	_ZN3FibILi1EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi1EE7computeEv
_ZN3FibILi1EE7computeEv:
.LFB2:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	.seh_endprologue
	mov	eax, 1
	pop	rbp
	ret
	.seh_endproc
	.text
	.globl	_Z7use_fibv
	.def	_Z7use_fibv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_fibv
_Z7use_fibv:
.LFB3:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	call	_ZN3FibILi10EE7computeEv
	add	rsp, 32
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi10EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi10EE7computeEv
	.def	_ZN3FibILi10EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi10EE7computeEv
_ZN3FibILi10EE7computeEv:
.LFB4:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi9EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi8EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi9EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi9EE7computeEv
	.def	_ZN3FibILi9EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi9EE7computeEv
_ZN3FibILi9EE7computeEv:
.LFB5:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi8EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi7EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi8EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi8EE7computeEv
	.def	_ZN3FibILi8EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi8EE7computeEv
_ZN3FibILi8EE7computeEv:
.LFB6:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi7EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi6EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi7EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi7EE7computeEv
	.def	_ZN3FibILi7EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi7EE7computeEv
_ZN3FibILi7EE7computeEv:
.LFB7:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi6EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi5EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi6EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi6EE7computeEv
	.def	_ZN3FibILi6EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi6EE7computeEv
_ZN3FibILi6EE7computeEv:
.LFB8:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi5EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi4EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi5EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi5EE7computeEv
	.def	_ZN3FibILi5EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi5EE7computeEv
_ZN3FibILi5EE7computeEv:
.LFB9:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi4EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi3EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi4EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi4EE7computeEv
	.def	_ZN3FibILi4EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi4EE7computeEv
_ZN3FibILi4EE7computeEv:
.LFB10:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi3EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi2EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi3EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi3EE7computeEv
	.def	_ZN3FibILi3EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi3EE7computeEv
_ZN3FibILi3EE7computeEv:
.LFB11:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi2EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi1EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.section	.text$_ZN3FibILi2EE7computeEv,"x"
	.linkonce discard
	.globl	_ZN3FibILi2EE7computeEv
	.def	_ZN3FibILi2EE7computeEv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3FibILi2EE7computeEv
_ZN3FibILi2EE7computeEv:
.LFB12:
	push	rbp
	.seh_pushreg	rbp
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	lea	rbp, 32[rsp]
	.seh_setframe	rbp, 32
	.seh_endprologue
	call	_ZN3FibILi1EE7computeEv
	mov	ebx, eax
	call	_ZN3FibILi0EE7computeEv
	add	eax, ebx
	add	rsp, 40
	pop	rbx
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
