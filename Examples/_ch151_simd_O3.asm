	.file	"_ch151_simd.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
	.align 8
.LC3:
	.ascii "simd(reduce): sum_ms=%.3f s=%.1f\12\0"
	.section	.text.unlikely,"x"
.LCOLDB4:
	.section	.text.startup,"x"
.LHOTB4:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB8192:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
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
	mov	rsi, rax
	lea	rbx, 160000000[rax]
	call	memset
	movss	xmm1, DWORD PTR .LC0[rip]
	mov	rax, rsi
	movaps	xmm0, xmm1
	.p2align 5
	.p2align 4
	.p2align 3
.L2:
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	addss	xmm0, xmm1
	cmp	rbx, rax
	jne	.L2
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm1, xmm1
	mov	rdi, rax
	mov	rax, rsi
	.p2align 6
	.p2align 4
	.p2align 3
.L3:
	movss	xmm0, DWORD PTR [rax]
	movss	xmm2, DWORD PTR 8[rax]
	mov	rdx, rbx
	add	rax, 16
	addss	xmm0, DWORD PTR -12[rax]
	addss	xmm2, DWORD PTR -4[rax]
	sub	rdx, rax
	addss	xmm0, xmm2
	addss	xmm1, xmm0
	cmp	rdx, 12
	jg	.L3
	cmp	rbx, rax
	je	.L4
	and	edx, 4
	je	.L5
	addss	xmm1, DWORD PTR [rax]
	add	rax, 4
	cmp	rbx, rax
	je	.L4
	.p2align 5
	.p2align 4
	.p2align 3
.L5:
	addss	xmm1, DWORD PTR [rax]
	add	rax, 8
	addss	xmm1, DWORD PTR -4[rax]
	cmp	rbx, rax
	jne	.L5
.L4:
	movss	DWORD PTR 44[rsp], xmm1
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movss	xmm2, DWORD PTR 44[rsp]
	pxor	xmm3, xmm3
	pxor	xmm1, xmm1
	sub	rax, rdi
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
	mov	rcx, rsi
	call	_ZdlPvy
	xor	eax, eax
	add	rsp, 48
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L7:
	mov	rbx, rax
	jmp	.L6
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA8192:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE8192-.LLSDACSB8192
.LLSDACSB8192:
	.uleb128 .LEHB0-.LFB8192
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB8192
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L7-.LFB8192
	.uleb128 0
.LLSDACSE8192:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	72
	.seh_savereg	rbx, 48
	.seh_savereg	rsi, 56
	.seh_savereg	rdi, 64
	.seh_endprologue
main.cold:
.L6:
	mov	rcx, rsi
	mov	edx, 160000000
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC8192:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC8192-.LLSDACSBC8192
.LLSDACSBC8192:
	.uleb128 .LEHB2-.LCOLDB4
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC8192:
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
