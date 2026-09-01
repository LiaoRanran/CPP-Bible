	.file	"ch122_use_monotonic.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.unlikely,"x"
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	_Z13use_monotonicv
	.def	_Z13use_monotonicv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13use_monotonicv
_Z13use_monotonicv:
.LFB2288:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 1144
	.seh_stackalloc	1144
	movaps	XMMWORD PTR 1120[rsp], xmm6
	.seh_savexmm	xmm6, 1120
	.seh_endprologue
	mov	rax, QWORD PTR .refptr._ZTVNSt3pmr25monotonic_buffer_resourceE[rip]
	add	rax, 16
	movq	xmm6, rax
	lea	rbx, 96[rsp]
	movq	xmm1, rbx
	punpcklqdq	xmm6, xmm1
	call	_ZNSt3pmr20get_default_resourceEv
	movdqa	xmm0, XMMWORD PTR .LC0[rip]
	mov	rdx, rbx
	mov	QWORD PTR 72[rsp], rbx
	sub	rdx, rbx
	mov	QWORD PTR 64[rsp], rax
	mov	rax, rbx
	mov	QWORD PTR 80[rsp], 1024
	mov	QWORD PTR 88[rsp], 0
	movaps	XMMWORD PTR 32[rsp], xmm6
	movaps	XMMWORD PTR 48[rsp], xmm0
	cmp	rdx, 960
	ja	.L10
	lea	rdx, 1120[rsp]
	sub	rdx, rbx
	lea	rbx, 32[rsp]
.L4:
	add	rax, 64
	mov	rcx, rbx
	mov	QWORD PTR 40[rsp], rax
	lea	rax, -64[rdx]
	mov	QWORD PTR 48[rsp], rax
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	nop
	movaps	xmm6, XMMWORD PTR 1120[rsp]
	add	rsp, 1144
	pop	rbx
	pop	rsi
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	lea	rbx, 32[rsp]
	mov	r8d, 16
	mov	edx, 64
	mov	rcx, rbx
.LEHB0:
	call	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy
.LEHE0:
	mov	rax, QWORD PTR 40[rsp]
	mov	rdx, QWORD PTR 48[rsp]
	jmp	.L4
.L6:
	mov	rsi, rax
	jmp	.L5
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA2288:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2288-.LLSDACSB2288
.LLSDACSB2288:
	.uleb128 .LEHB0-.LFB2288
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L6-.LFB2288
	.uleb128 0
.LLSDACSE2288:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	_Z13use_monotonicv.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	_Z13use_monotonicv.cold
	.seh_stackalloc	1160
	.seh_savereg	rbx, 1144
	.seh_savereg	rsi, 1152
	.seh_savexmm	xmm6, 1120
	.seh_endprologue
_Z13use_monotonicv.cold:
.L5:
	mov	rcx, rbx
	call	_ZNSt3pmr25monotonic_buffer_resourceD1Ev
	mov	rcx, rsi
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC2288:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC2288-.LLSDACSBC2288
.LLSDACSBC2288:
	.uleb128 .LEHB1-.LCOLDB1
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSEC2288:
	.section	.text.unlikely,"x"
	.text
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE1:
	.text
.LHOTE1:
	.section .rdata,"dr"
	.align 16
.LC0:
	.quad	1024
	.quad	1536
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt3pmr20get_default_resourceEv;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr25monotonic_buffer_resourceD1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZNSt3pmr25monotonic_buffer_resource13_M_new_bufferEyy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE, "dr"
	.p2align	3, 0
	.globl	.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE
	.linkonce	discard
.refptr._ZTVNSt3pmr25monotonic_buffer_resourceE:
	.quad	_ZTVNSt3pmr25monotonic_buffer_resourceE
