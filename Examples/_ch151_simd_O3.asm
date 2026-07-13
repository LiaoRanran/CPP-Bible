	.file	"_ch151_simd.cpp"
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
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	QWORD PTR 96[rsp], r8
	lea	r8, 88[rsp]
	mov	rbx, rcx
	mov	QWORD PTR 88[rsp], rdx
	mov	QWORD PTR 104[rsp], r9
	mov	QWORD PTR 56[rsp], r8
	mov	QWORD PTR 40[rsp], r8
	mov	ecx, 1
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	mov	r8, QWORD PTR 40[rsp]
	mov	rdx, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 64
	pop	rbx
	ret
	.seh_endproc
	.section	.text$_ZNSt6vectorIfSaIfEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIfSaIfEED1Ev
	.def	_ZNSt6vectorIfSaIfEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIfSaIfEED1Ev
_ZNSt6vectorIfSaIfEED1Ev:
.LFB8557:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L5
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4
	.p2align 3
.L5:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC3:
	.ascii "simd(reduce): sum_ms=%.3f s=%.1f\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB7932:
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	call	__main
	mov	ecx, 160000000
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 159999996
	xor	edx, edx
	lea	rdi, 160000000[rax]
	lea	rcx, 4[rax]
	mov	rsi, rax
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 64[rsp], rdi
	mov	DWORD PTR [rax], 0x00000000
	call	memset
	vmovss	xmm1, DWORD PTR .LC0[rip]
	mov	rbp, rsi
	mov	rax, rsi
	mov	QWORD PTR 56[rsp], rdi
	vmovaps	xmm0, xmm1
	.p2align 4
	.p2align 3
.L7:
	vmovss	DWORD PTR [rax], xmm0
	add	rax, 4
	vaddss	xmm0, xmm0, xmm1
	cmp	rax, rdi
	jne	.L7
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	vxorps	xmm0, xmm0, xmm0
	mov	rbx, rax
	.p2align 4
	.p2align 3
.L8:
	vmovss	xmm1, DWORD PTR [rsi]
	vmovss	xmm2, DWORD PTR 8[rsi]
	vaddss	xmm1, xmm1, DWORD PTR 4[rsi]
	mov	rax, rdi
	vaddss	xmm2, xmm2, DWORD PTR 12[rsi]
	add	rsi, 16
	sub	rax, rsi
	vaddss	xmm1, xmm1, xmm2
	vaddss	xmm0, xmm0, xmm1
	cmp	rax, 12
	jg	.L8
	cmp	rsi, rdi
	je	.L9
	lea	rdx, 159999996[rbp]
	mov	rax, rsi
	sub	rdx, rsi
	mov	rcx, rdx
	shr	rcx, 2
	lea	r8, 1[rcx]
	cmp	rdx, 56
	jbe	.L16
	mov	rdx, r8
	shr	rdx, 4
	sal	rdx, 6
	add	rdx, rsi
	.p2align 4
	.p2align 3
.L11:
	vaddss	xmm0, xmm0, DWORD PTR [rax]
	add	rax, 64
	vaddss	xmm0, xmm0, DWORD PTR -60[rax]
	vaddss	xmm0, xmm0, DWORD PTR -56[rax]
	vaddss	xmm0, xmm0, DWORD PTR -52[rax]
	vaddss	xmm0, xmm0, DWORD PTR -48[rax]
	vaddss	xmm0, xmm0, DWORD PTR -44[rax]
	vaddss	xmm0, xmm0, DWORD PTR -40[rax]
	vaddss	xmm0, xmm0, DWORD PTR -36[rax]
	vaddss	xmm0, xmm0, DWORD PTR -32[rax]
	vaddss	xmm0, xmm0, DWORD PTR -28[rax]
	vaddss	xmm0, xmm0, DWORD PTR -24[rax]
	vaddss	xmm0, xmm0, DWORD PTR -20[rax]
	vaddss	xmm0, xmm0, DWORD PTR -16[rax]
	vaddss	xmm0, xmm0, DWORD PTR -12[rax]
	vaddss	xmm0, xmm0, DWORD PTR -8[rax]
	vaddss	xmm0, xmm0, DWORD PTR -4[rax]
	cmp	rdx, rax
	jne	.L11
	mov	rax, r8
	and	rax, -16
	and	r8d, 15
	lea	rdx, [rsi+rax*4]
	je	.L9
.L10:
	sub	rcx, rax
	lea	r8, 1[rcx]
	cmp	rcx, 6
	jbe	.L13
	lea	rax, [rsi+rax*4]
	vaddss	xmm0, xmm0, DWORD PTR [rax]
	vaddss	xmm0, xmm0, DWORD PTR 4[rax]
	vaddss	xmm0, xmm0, DWORD PTR 8[rax]
	vaddss	xmm0, xmm0, DWORD PTR 12[rax]
	vaddss	xmm0, xmm0, DWORD PTR 16[rax]
	vaddss	xmm0, xmm0, DWORD PTR 20[rax]
	vaddss	xmm0, xmm0, DWORD PTR 24[rax]
	vaddss	xmm0, xmm0, DWORD PTR 28[rax]
	mov	rax, r8
	and	rax, -8
	and	r8d, 7
	lea	rdx, [rdx+rax*4]
	je	.L9
.L13:
	lea	rax, 4[rdx]
	vaddss	xmm0, xmm0, DWORD PTR [rdx]
	cmp	rdi, rax
	je	.L9
	lea	rax, 8[rdx]
	vaddss	xmm0, xmm0, DWORD PTR 4[rdx]
	cmp	rdi, rax
	je	.L9
	lea	rax, 12[rdx]
	vaddss	xmm0, xmm0, DWORD PTR 8[rdx]
	cmp	rdi, rax
	je	.L9
	lea	rax, 16[rdx]
	vaddss	xmm0, xmm0, DWORD PTR 12[rdx]
	cmp	rdi, rax
	je	.L9
	lea	rax, 20[rdx]
	vaddss	xmm0, xmm0, DWORD PTR 16[rdx]
	cmp	rdi, rax
	je	.L9
	lea	rax, 24[rdx]
	vaddss	xmm0, xmm0, DWORD PTR 20[rdx]
	cmp	rdi, rax
	je	.L9
	vaddss	xmm0, xmm0, DWORD PTR 24[rdx]
.L9:
	vmovss	DWORD PTR 44[rsp], xmm0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	vmovss	xmm2, DWORD PTR 44[rsp]
	vxorps	xmm1, xmm1, xmm1
	sub	rax, rbx
	lea	rcx, .LC3[rip]
	vcvtsi2sd	xmm1, xmm1, rax
	vdivsd	xmm1, xmm1, QWORD PTR .LC2[rip]
	vmovq	rdx, xmm1
	vcvtss2sd	xmm3, xmm2, xmm2
	vmovq	r8, xmm3
	vmovsd	xmm2, xmm3, xmm3
.LEHB1:
	call	_Z6printfPKcz
.LEHE1:
	lea	rcx, 48[rsp]
	call	_ZNSt6vectorIfSaIfEED1Ev
	xor	eax, eax
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
.L16:
	mov	rdx, rsi
	xor	eax, eax
	jmp	.L10
.L17:
	mov	rbx, rax
	lea	rcx, 48[rsp]
	vzeroupper
	call	_ZNSt6vectorIfSaIfEED1Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA7932:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE7932-.LLSDACSB7932
.LLSDACSB7932:
	.uleb128 .LEHB0-.LFB7932
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB7932
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L17-.LFB7932
	.uleb128 0
	.uleb128 .LEHB2-.LFB7932
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE7932:
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
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
