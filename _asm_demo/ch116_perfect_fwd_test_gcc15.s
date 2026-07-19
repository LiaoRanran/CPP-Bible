	.file	"ch116_perfect_fwd_test.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z6sink_lR1S
	.def	_Z6sink_lR1S;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6sink_lR1S
_Z6sink_lR1S:
.LFB204:
	.seh_endprologue
	mov	DWORD PTR g_l[rip], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6sink_rO1S
	.def	_Z6sink_rO1S;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6sink_rO1S
_Z6sink_rO1S:
.LFB205:
	.seh_endprologue
	mov	DWORD PTR g_r[rip], 1
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z10fwd_lvalueR1S
	.def	_Z10fwd_lvalueR1S;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10fwd_lvalueR1S
_Z10fwd_lvalueR1S:
.LFB206:
	.seh_endprologue
	jmp	_Z6sink_lR1S
	.seh_endproc
	.p2align 4
	.globl	_Z10fwd_rvalueO1S
	.def	_Z10fwd_rvalueO1S;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10fwd_rvalueO1S
_Z10fwd_rvalueO1S:
.LFB207:
	.seh_endprologue
	jmp	_Z6sink_rO1S
	.seh_endproc
	.section	.text$_Z8fwd_tmplIR1SEvOT_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8fwd_tmplIR1SEvOT_
	.def	_Z8fwd_tmplIR1SEvOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8fwd_tmplIR1SEvOT_
_Z8fwd_tmplIR1SEvOT_:
.LFB211:
	.seh_endprologue
	jmp	_Z6sink_lR1S
	.seh_endproc
	.section	.text$_Z8fwd_tmplI1SEvOT_,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z8fwd_tmplI1SEvOT_
	.def	_Z8fwd_tmplI1SEvOT_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8fwd_tmplI1SEvOT_
_Z8fwd_tmplI1SEvOT_:
.LFB212:
	.seh_endprologue
	jmp	_Z6sink_rO1S
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z7fwd_val1S
	.def	_Z7fwd_val1S;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7fwd_val1S
_Z7fwd_val1S:
.LFB209:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	movdqu	xmm0, XMMWORD PTR [rcx]
	lea	rcx, 32[rsp]
	movaps	XMMWORD PTR 32[rsp], xmm0
	call	_Z6sink_rO1S
	nop
	add	rsp, 56
	ret
	.seh_endproc
	.globl	g_r
	.bss
	.align 4
g_r:
	.space 4
	.globl	g_l
	.align 4
g_l:
	.space 4
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
