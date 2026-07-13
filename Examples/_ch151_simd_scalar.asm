	.file	"_ch151_simd_scalar.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z6printfPKcz,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z6printfPKcz
	.def	_Z6printfPKcz;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6printfPKcz
_Z6printfPKcz:
.LFB11:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	lea	rsi, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	ecx, 1
	mov	QWORD PTR 96[rsp], r8
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 40[rsp], rsi
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, rsi
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC3:
	.ascii "scalar: sum_ms=%.3f s=%.1f\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5605:
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
	call	memset
	movss	xmm1, DWORD PTR .LC0[rip]
	mov	rbx, rdi
	mov	rax, rdi
	lea	rsi, 160000000[rdi]
	movaps	xmm0, xmm1
	.p2align 4,,10
	.p2align 3
.L4:
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	addss	xmm0, xmm1
	cmp	rax, rsi
	jne	.L4
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	DWORD PTR 44[rsp], 0x00000000
	mov	rbp, rax
	.p2align 4,,10
	.p2align 3
.L5:
	movss	xmm0, DWORD PTR 44[rsp]
	add	rbx, 4
	addss	xmm0, DWORD PTR -4[rbx]
	cmp	rsi, rbx
	movss	DWORD PTR 44[rsp], xmm0
	jne	.L5
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movss	xmm2, DWORD PTR 44[rsp]
	pxor	xmm3, xmm3
	pxor	xmm1, xmm1
	lea	rcx, .LC3[rip]
	sub	rax, rbp
	cvtss2sd	xmm3, xmm2
	cvtsi2sd	xmm1, rax
	movq	r8, xmm3
	divsd	xmm1, QWORD PTR .LC2[rip]
	movapd	xmm2, xmm3
	movq	rdx, xmm1
.LEHB1:
	call	_Z6printfPKcz
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
.L7:
	mov	rbx, rax
	mov	rcx, rdi
	mov	edx, 160000000
	call	_ZdlPvy
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5605:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5605-.LLSDACSB5605
.LLSDACSB5605:
	.uleb128 .LEHB0-.LFB5605
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB5605
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L7-.LFB5605
	.uleb128 0
	.uleb128 .LEHB2-.LFB5605
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE5605:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1065353216
	.align 8
.LC2:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
