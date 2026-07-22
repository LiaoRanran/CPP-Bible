	.file	"_ch151_simd_scalar.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC3:
	.ascii "scalar: sum_ms=%.3f s=%.1f\12\0"
	.section	.text.unlikely,"x"
.LCOLDB4:
	.section	.text.startup,"x"
.LHOTB4:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5862:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	ecx, 160000000
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 159999996
	xor	edx, edx
	mov	DWORD PTR [rax], 0x00000000
	lea	rcx, 4[rax]
	mov	rdi, rax
	mov	rbx, rdi
	lea	rsi, 160000000[rdi]
	call	memset
	movss	xmm1, DWORD PTR .LC0[rip]
	mov	rax, rdi
	movaps	xmm0, xmm1
	.p2align 5
	.p2align 4
	.p2align 3
.L2:
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	addss	xmm0, xmm1
	cmp	rax, rsi
	jne	.L2
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	DWORD PTR 44[rsp], 0x00000000
	mov	rbp, rax
	.p2align 5
	.p2align 4
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR 44[rsp]
	addss	xmm0, DWORD PTR [rbx]
	add	rbx, 4
	movss	DWORD PTR 44[rsp], xmm0
	cmp	rbx, rsi
	jne	.L3
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movss	xmm2, DWORD PTR 44[rsp]
	pxor	xmm3, xmm3
	pxor	xmm1, xmm1
	sub	rax, rbp
	lea	rcx, .LC3[rip]
	cvtss2sd	xmm3, xmm2
	cvtsi2sd	xmm1, rax
	movq	r8, xmm3
	divsd	xmm1, QWORD PTR .LC2[rip]
	movapd	xmm2, xmm3
	movq	rdx, xmm1
.LEHB1:
	call	__mingw_printf
.LEHE1:
	mov	edx, 160000000
	mov	rcx, rdi
	call	_ZdlPvy
	xor	eax, eax
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L5:
	mov	rbx, rax
	jmp	.L4
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5862:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5862-.LLSDACSB5862
.LLSDACSB5862:
	.uleb128 .LEHB0-.LFB5862
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5862
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L5-.LFB5862
	.uleb128 0
.LLSDACSE5862:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 56
	.seh_savereg	rsi, 64
	.seh_savereg	rdi, 72
	.seh_savereg	rbp, 80
	.seh_endprologue
main.cold:
.L4:
	mov	rcx, rdi
	mov	edx, 160000000
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC5862:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC5862-.LLSDACSBC5862
.LLSDACSBC5862:
	.uleb128 .LEHB2-.LCOLDB4
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC5862:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE4:
	.section	.text.startup,"x"
.LHOTE4:
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1065353216
	.align 8
.LC2:
	.long	0
	.long	1093567616
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
