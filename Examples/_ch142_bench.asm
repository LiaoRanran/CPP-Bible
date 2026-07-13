	.file	"_ch142_bench.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "cannot create std::vector larger than max_size()\0"
	.text
	.p2align 4
	.globl	_Z14bench_aos_fullyy
	.def	_Z14bench_aos_fullyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14bench_aos_fullyy
_Z14bench_aos_fullyy:
.LFB5564:
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
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
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	movabs	rax, 72057594037927935
	cmp	rax, rcx
	mov	r13, rcx
	mov	r12, rdx
	jb	.L31
	test	rcx, rcx
	je	.L3
	mov	rbx, rcx
	sal	rbx, 7
	mov	rcx, rbx
	call	_Znwy
	mov	ecx, 16
	mov	rbp, rax
	xor	eax, eax
	cmp	r13, 1
	mov	rdi, rbp
	rep stosq
	jne	.L32
	mov	ebx, 128
.L4:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	test	r12, r12
	mov	rsi, rax
	je	.L33
.L13:
	mov	rdx, r13
	xor	ecx, ecx
	sal	rdx, 7
	add	rdx, rbp
	test	r13, r13
	je	.L26
	movq	xmm3, QWORD PTR .LC1[rip]
	movss	xmm2, DWORD PTR .LC2[rip]
	.p2align 4,,10
	.p2align 3
.L9:
	mov	rax, rbp
	.p2align 4,,10
	.p2align 3
.L8:
	movq	xmm0, QWORD PTR 12[rax]
	sub	rax, -128
	movq	xmm1, QWORD PTR -128[rax]
	mulps	xmm0, xmm3
	addps	xmm0, xmm1
	movlps	QWORD PTR -128[rax], xmm0
	movss	xmm0, DWORD PTR -108[rax]
	mulss	xmm0, xmm2
	addss	xmm0, DWORD PTR -120[rax]
	movss	DWORD PTR -120[rax], xmm0
	cmp	rdx, rax
	jne	.L8
	add	rcx, 1
	cmp	rcx, r12
	jb	.L9
.L10:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm6, xmm6
	sub	rax, rsi
	test	rbp, rbp
	cvtsi2sd	xmm6, rax
	divsd	xmm6, QWORD PTR .LC3[rip]
	je	.L1
.L15:
	mov	rdx, rbx
	mov	rcx, rbp
	call	_ZdlPvy
.L1:
	movapd	xmm0, xmm6
	movaps	xmm6, XMMWORD PTR 32[rsp]
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L26:
	add	rcx, 1
	cmp	rcx, r12
	jnb	.L10
	add	rcx, 1
	cmp	rcx, r12
	jb	.L26
	jmp	.L10
.L32:
	lea	rcx, 0[rbp+rbx]
	lea	rax, 128[rbp]
	cmp	rax, rcx
	je	.L4
	.p2align 4,,10
	.p2align 3
.L5:
	mov	rdx, QWORD PTR 0[rbp]
	sub	rax, -128
	mov	QWORD PTR -128[rax], rdx
	mov	rdx, QWORD PTR 8[rbp]
	mov	QWORD PTR -120[rax], rdx
	mov	rdx, QWORD PTR 16[rbp]
	mov	QWORD PTR -112[rax], rdx
	mov	rdx, QWORD PTR 24[rbp]
	mov	QWORD PTR -104[rax], rdx
	mov	rdx, QWORD PTR 32[rbp]
	mov	QWORD PTR -96[rax], rdx
	mov	rdx, QWORD PTR 40[rbp]
	mov	QWORD PTR -88[rax], rdx
	mov	rdx, QWORD PTR 48[rbp]
	mov	QWORD PTR -80[rax], rdx
	mov	rdx, QWORD PTR 56[rbp]
	mov	QWORD PTR -72[rax], rdx
	mov	rdx, QWORD PTR 64[rbp]
	mov	QWORD PTR -64[rax], rdx
	mov	rdx, QWORD PTR 72[rbp]
	mov	QWORD PTR -56[rax], rdx
	mov	rdx, QWORD PTR 80[rbp]
	mov	QWORD PTR -48[rax], rdx
	mov	rdx, QWORD PTR 88[rbp]
	mov	QWORD PTR -40[rax], rdx
	mov	rdx, QWORD PTR 96[rbp]
	mov	QWORD PTR -32[rax], rdx
	mov	rdx, QWORD PTR 104[rbp]
	mov	QWORD PTR -24[rax], rdx
	mov	rdx, QWORD PTR 112[rbp]
	mov	QWORD PTR -16[rax], rdx
	mov	rdx, QWORD PTR 120[rbp]
	mov	QWORD PTR -8[rax], rdx
	cmp	rax, rcx
	jne	.L5
	jmp	.L4
.L3:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	xor	ebx, ebx
	xor	ebp, ebp
	test	r12, r12
	mov	rsi, rax
	jne	.L13
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm6, xmm6
	sub	rax, rsi
	cvtsi2sd	xmm6, rax
	divsd	xmm6, QWORD PTR .LC3[rip]
	jmp	.L1
.L33:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	pxor	xmm6, xmm6
	sub	rax, rsi
	cvtsi2sd	xmm6, rax
	divsd	xmm6, QWORD PTR .LC3[rip]
	jmp	.L15
.L31:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.section	.text$_ZN3SoAD1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZN3SoAD1Ev
	.def	_ZN3SoAD1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZN3SoAD1Ev
_ZN3SoAD1Ev:
.LFB5596:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	mov	rbx, rcx
	mov	rcx, QWORD PTR 744[rcx]
	test	rcx, rcx
	je	.L35
	mov	rdx, QWORD PTR 760[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L35:
	mov	rcx, QWORD PTR 720[rbx]
	test	rcx, rcx
	je	.L36
	mov	rdx, QWORD PTR 736[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L36:
	mov	rcx, QWORD PTR 696[rbx]
	test	rcx, rcx
	je	.L37
	mov	rdx, QWORD PTR 712[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L37:
	mov	rcx, QWORD PTR 672[rbx]
	test	rcx, rcx
	je	.L38
	mov	rdx, QWORD PTR 688[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L38:
	mov	rcx, QWORD PTR 648[rbx]
	test	rcx, rcx
	je	.L39
	mov	rdx, QWORD PTR 664[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L39:
	mov	rcx, QWORD PTR 624[rbx]
	test	rcx, rcx
	je	.L40
	mov	rdx, QWORD PTR 640[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L40:
	mov	rcx, QWORD PTR 600[rbx]
	test	rcx, rcx
	je	.L41
	mov	rdx, QWORD PTR 616[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L41:
	mov	rcx, QWORD PTR 576[rbx]
	test	rcx, rcx
	je	.L42
	mov	rdx, QWORD PTR 592[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L42:
	mov	rcx, QWORD PTR 552[rbx]
	test	rcx, rcx
	je	.L43
	mov	rdx, QWORD PTR 568[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L43:
	mov	rcx, QWORD PTR 528[rbx]
	test	rcx, rcx
	je	.L44
	mov	rdx, QWORD PTR 544[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L44:
	mov	rcx, QWORD PTR 504[rbx]
	test	rcx, rcx
	je	.L45
	mov	rdx, QWORD PTR 520[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L45:
	mov	rcx, QWORD PTR 480[rbx]
	test	rcx, rcx
	je	.L46
	mov	rdx, QWORD PTR 496[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L46:
	mov	rcx, QWORD PTR 456[rbx]
	test	rcx, rcx
	je	.L47
	mov	rdx, QWORD PTR 472[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L47:
	mov	rcx, QWORD PTR 432[rbx]
	test	rcx, rcx
	je	.L48
	mov	rdx, QWORD PTR 448[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L48:
	mov	rcx, QWORD PTR 408[rbx]
	test	rcx, rcx
	je	.L49
	mov	rdx, QWORD PTR 424[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L49:
	mov	rcx, QWORD PTR 384[rbx]
	test	rcx, rcx
	je	.L50
	mov	rdx, QWORD PTR 400[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L50:
	mov	rcx, QWORD PTR 360[rbx]
	test	rcx, rcx
	je	.L51
	mov	rdx, QWORD PTR 376[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L51:
	mov	rcx, QWORD PTR 336[rbx]
	test	rcx, rcx
	je	.L52
	mov	rdx, QWORD PTR 352[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L52:
	mov	rcx, QWORD PTR 312[rbx]
	test	rcx, rcx
	je	.L53
	mov	rdx, QWORD PTR 328[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L53:
	mov	rcx, QWORD PTR 288[rbx]
	test	rcx, rcx
	je	.L54
	mov	rdx, QWORD PTR 304[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L54:
	mov	rcx, QWORD PTR 264[rbx]
	test	rcx, rcx
	je	.L55
	mov	rdx, QWORD PTR 280[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L55:
	mov	rcx, QWORD PTR 240[rbx]
	test	rcx, rcx
	je	.L56
	mov	rdx, QWORD PTR 256[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L56:
	mov	rcx, QWORD PTR 216[rbx]
	test	rcx, rcx
	je	.L57
	mov	rdx, QWORD PTR 232[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L57:
	mov	rcx, QWORD PTR 192[rbx]
	test	rcx, rcx
	je	.L58
	mov	rdx, QWORD PTR 208[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L58:
	mov	rcx, QWORD PTR 168[rbx]
	test	rcx, rcx
	je	.L59
	mov	rdx, QWORD PTR 184[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L59:
	mov	rcx, QWORD PTR 144[rbx]
	test	rcx, rcx
	je	.L60
	mov	rdx, QWORD PTR 160[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L60:
	mov	rcx, QWORD PTR 120[rbx]
	test	rcx, rcx
	je	.L61
	mov	rdx, QWORD PTR 136[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L61:
	mov	rcx, QWORD PTR 96[rbx]
	test	rcx, rcx
	je	.L62
	mov	rdx, QWORD PTR 112[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L62:
	mov	rcx, QWORD PTR 72[rbx]
	test	rcx, rcx
	je	.L63
	mov	rdx, QWORD PTR 88[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L63:
	mov	rcx, QWORD PTR 48[rbx]
	test	rcx, rcx
	je	.L64
	mov	rdx, QWORD PTR 64[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L64:
	mov	rcx, QWORD PTR 24[rbx]
	test	rcx, rcx
	je	.L65
	mov	rdx, QWORD PTR 40[rbx]
	sub	rdx, rcx
	call	_ZdlPvy
.L65:
	mov	rcx, QWORD PTR [rbx]
	test	rcx, rcx
	je	.L34
	mov	rdx, QWORD PTR 16[rbx]
	sub	rdx, rcx
	add	rsp, 32
	pop	rbx
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L34:
	add	rsp, 32
	pop	rbx
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z14bench_soa_fullyy
	.def	_Z14bench_soa_fullyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14bench_soa_fullyy
_Z14bench_soa_fullyy:
.LFB5568:
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 816
	.seh_stackalloc	816
	movaps	XMMWORD PTR 800[rsp], xmm6
	.seh_savexmm	xmm6, 800
	.seh_endprologue
	mov	r8d, 768
	lea	rbp, 32[rsp]
	mov	rbx, rcx
	mov	rsi, rdx
	mov	rcx, rbp
	xor	edx, edx
	call	memset
	test	rbx, rbx
	jne	.L205
.L161:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	test	rsi, rsi
	mov	rdi, rax
	je	.L166
	test	rbx, rbx
	mov	r11, QWORD PTR 104[rsp]
	mov	r8, QWORD PTR 32[rsp]
	mov	r10, QWORD PTR 128[rsp]
	mov	rcx, QWORD PTR 56[rsp]
	mov	r9, QWORD PTR 152[rsp]
	mov	rdx, QWORD PTR 80[rsp]
	je	.L166
	movss	xmm1, DWORD PTR .LC2[rip]
	xor	r12d, r12d
	.p2align 4,,10
	.p2align 3
.L169:
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L168:
	movss	xmm0, DWORD PTR [r11+rax*4]
	mulss	xmm0, xmm1
	addss	xmm0, DWORD PTR [r8+rax*4]
	movss	DWORD PTR [r8+rax*4], xmm0
	movss	xmm0, DWORD PTR [r10+rax*4]
	mulss	xmm0, xmm1
	addss	xmm0, DWORD PTR [rcx+rax*4]
	movss	DWORD PTR [rcx+rax*4], xmm0
	movss	xmm0, DWORD PTR [r9+rax*4]
	mulss	xmm0, xmm1
	addss	xmm0, DWORD PTR [rdx+rax*4]
	movss	DWORD PTR [rdx+rax*4], xmm0
	add	rax, 1
	cmp	rbx, rax
	jne	.L168
	add	r12, 1
	cmp	rsi, r12
	jne	.L169
.L166:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rcx, rbp
	pxor	xmm6, xmm6
	sub	rax, rdi
	cvtsi2sd	xmm6, rax
	divsd	xmm6, QWORD PTR .LC3[rip]
	call	_ZN3SoAD1Ev
	movapd	xmm0, xmm6
	movaps	xmm6, XMMWORD PTR 800[rsp]
	add	rsp, 816
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	ret
.L205:
	movabs	rax, 2305843009213693951
	cmp	rax, rbx
	jb	.L206
	lea	rdi, 0[0+rbx*4]
	mov	rcx, rdi
.LEHB0:
	call	_Znwy
	mov	rcx, rax
	mov	r8, rdi
	xor	edx, edx
	lea	r12, [rax+rdi]
	call	memset
	movq	xmm2, r12
	mov	rcx, rdi
	mov	QWORD PTR 48[rsp], r12
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm2
	movaps	XMMWORD PTR 32[rsp], xmm0
	call	_Znwy
	mov	rcx, rax
	mov	r8, rdi
	xor	edx, edx
	lea	r12, [rax+rdi]
	call	memset
	movq	xmm3, r12
	mov	rcx, rdi
	mov	QWORD PTR 72[rsp], r12
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm3
	movups	XMMWORD PTR 56[rsp], xmm0
	call	_Znwy
	mov	rcx, rax
	mov	r8, rdi
	xor	edx, edx
	lea	r12, [rax+rdi]
	call	memset
	movq	xmm4, r12
	mov	rcx, rdi
	mov	QWORD PTR 96[rsp], r12
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm4
	movaps	XMMWORD PTR 80[rsp], xmm0
	call	_Znwy
	lea	rdx, [rax+rdi]
	movq	xmm0, rax
	movss	xmm6, DWORD PTR .LC4[rip]
	mov	rcx, rdx
	movq	xmm5, rdx
	sub	rcx, rax
	punpcklqdq	xmm0, xmm5
	and	ecx, 4
	je	.L163
	movss	DWORD PTR [rax], xmm6
	add	rax, 4
	cmp	rdx, rax
	je	.L204
	.p2align 4,,10
	.p2align 3
.L163:
	movss	DWORD PTR [rax], xmm6
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm6
	cmp	rdx, rax
	jne	.L163
.L204:
	mov	rcx, rdi
	movups	XMMWORD PTR 104[rsp], xmm0
	mov	QWORD PTR 120[rsp], rdx
	call	_Znwy
	lea	rdx, [rax+rdi]
	movq	xmm0, rax
	mov	rcx, rdx
	movq	xmm3, rdx
	sub	rcx, rax
	punpcklqdq	xmm0, xmm3
	and	ecx, 4
	je	.L164
	movss	DWORD PTR [rax], xmm6
	add	rax, 4
	cmp	rdx, rax
	je	.L203
	.p2align 4,,10
	.p2align 3
.L164:
	movss	DWORD PTR [rax], xmm6
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm6
	cmp	rdx, rax
	jne	.L164
.L203:
	mov	rcx, rdi
	movaps	XMMWORD PTR 128[rsp], xmm0
	mov	QWORD PTR 144[rsp], rdx
	call	_Znwy
	add	rdi, rax
	movq	xmm0, rax
	mov	rdx, rdi
	movq	xmm4, rdi
	sub	rdx, rax
	punpcklqdq	xmm0, xmm4
	and	edx, 4
	je	.L165
	movss	DWORD PTR [rax], xmm6
	add	rax, 4
	cmp	rdi, rax
	je	.L202
	.p2align 4,,10
	.p2align 3
.L165:
	movss	DWORD PTR [rax], xmm6
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm6
	cmp	rdi, rax
	jne	.L165
.L202:
	movups	XMMWORD PTR 152[rsp], xmm0
	mov	QWORD PTR 168[rsp], rdi
	jmp	.L161
.L206:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE0:
.L171:
	mov	rbx, rax
	mov	rcx, rbp
	call	_ZN3SoAD1Ev
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5568:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5568-.LLSDACSB5568
.LLSDACSB5568:
	.uleb128 .LEHB0-.LFB5568
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L171-.LFB5568
	.uleb128 0
	.uleb128 .LEHB1-.LFB5568
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE5568:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z17bench_aos_partialyy
	.def	_Z17bench_aos_partialyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17bench_aos_partialyy
_Z17bench_aos_partialyy:
.LFB5597:
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
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
	movaps	XMMWORD PTR 32[rsp], xmm6
	.seh_savexmm	xmm6, 32
	.seh_endprologue
	movabs	rax, 72057594037927935
	cmp	rax, rdx
	mov	rbx, rcx
	mov	r13, rdx
	mov	rbp, r8
	jb	.L228
	test	rdx, rdx
	je	.L217
	mov	rsi, rdx
	sal	rsi, 7
	mov	rcx, rsi
	call	_Znwy
	lea	rcx, -128[rsi]
	xor	edx, edx
	shr	rcx, 7
	mov	r12, rax
	add	rcx, 1
	.p2align 4,,10
	.p2align 3
.L210:
	add	rdx, 1
	mov	QWORD PTR [rax], 0
	sub	rax, -128
	mov	QWORD PTR -120[rax], 0
	mov	QWORD PTR -112[rax], 0
	mov	QWORD PTR -104[rax], 0
	mov	QWORD PTR -96[rax], 0
	mov	QWORD PTR -88[rax], 0
	mov	QWORD PTR -80[rax], 0
	mov	QWORD PTR -72[rax], 0
	mov	QWORD PTR -64[rax], 0
	mov	QWORD PTR -56[rax], 0
	mov	QWORD PTR -48[rax], 0
	mov	QWORD PTR -40[rax], 0
	mov	QWORD PTR -32[rax], 0
	mov	QWORD PTR -24[rax], 0
	mov	QWORD PTR -16[rax], 0
	mov	QWORD PTR -8[rax], 0
	cmp	rdx, rcx
	jb	.L210
.L209:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	test	rbp, rbp
	mov	rdi, rax
	je	.L219
	mov	rdx, r13
	xor	ecx, ecx
	pxor	xmm6, xmm6
	sal	rdx, 7
	add	rdx, r12
	test	r13, r13
	je	.L227
	.p2align 4,,10
	.p2align 3
.L214:
	mov	rax, r12
	.p2align 4,,10
	.p2align 3
.L213:
	movss	xmm0, DWORD PTR [rax]
	sub	rax, -128
	movss	xmm1, DWORD PTR -124[rax]
	cmp	rax, rdx
	mulss	xmm0, xmm0
	mulss	xmm1, xmm1
	addss	xmm0, xmm1
	cvtss2sd	xmm0, xmm0
	addsd	xmm6, xmm0
	jne	.L213
	add	rcx, 1
	cmp	rbp, rcx
	jne	.L214
.L211:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movsd	xmm0, QWORD PTR g_sink[rip]
	movsd	QWORD PTR 8[rbx], xmm6
	sub	rax, rdi
	test	r12, r12
	addsd	xmm0, xmm6
	movsd	QWORD PTR g_sink[rip], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
	divsd	xmm0, QWORD PTR .LC3[rip]
	movsd	QWORD PTR [rbx], xmm0
	je	.L207
	mov	rdx, rsi
	mov	rcx, r12
	call	_ZdlPvy
	nop
.L207:
	movaps	xmm6, XMMWORD PTR 32[rsp]
	mov	rax, rbx
	add	rsp, 56
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L227:
	add	rcx, 1
	cmp	rbp, rcx
	jne	.L227
.L219:
	pxor	xmm6, xmm6
	jmp	.L211
.L217:
	xor	esi, esi
	xor	r12d, r12d
	jmp	.L209
.L228:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
	nop
	.seh_endproc
	.p2align 4
	.globl	_Z17bench_soa_partialyy
	.def	_Z17bench_soa_partialyy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z17bench_soa_partialyy
_Z17bench_soa_partialyy:
.LFB5598:
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
	push	rbp
	.seh_pushreg	rbp
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 824
	.seh_stackalloc	824
	movaps	XMMWORD PTR 800[rsp], xmm6
	.seh_savexmm	xmm6, 800
	.seh_endprologue
	lea	r12, 32[rsp]
	mov	rbx, rdx
	mov	rdi, rcx
	xor	edx, edx
	mov	rsi, r8
	mov	rcx, r12
	mov	r8d, 768
	call	memset
	test	rbx, rbx
	jne	.L261
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	test	rsi, rsi
	mov	rbp, rax
	je	.L239
.L263:
	test	rbx, rbx
	mov	rcx, QWORD PTR 32[rsp]
	mov	rdx, QWORD PTR 56[rsp]
	je	.L239
	xor	r8d, r8d
	pxor	xmm6, xmm6
	.p2align 4,,10
	.p2align 3
.L236:
	xor	eax, eax
	.p2align 4,,10
	.p2align 3
.L235:
	movss	xmm0, DWORD PTR [rcx+rax*4]
	movss	xmm1, DWORD PTR [rdx+rax*4]
	add	rax, 1
	mulss	xmm0, xmm0
	cmp	rbx, rax
	mulss	xmm1, xmm1
	addss	xmm0, xmm1
	cvtss2sd	xmm0, xmm0
	addsd	xmm6, xmm0
	jne	.L235
	add	r8, 1
	cmp	rsi, r8
	jne	.L236
.L234:
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	movsd	xmm0, QWORD PTR g_sink[rip]
	mov	rcx, r12
	movsd	QWORD PTR 8[rdi], xmm6
	sub	rax, rbp
	addsd	xmm0, xmm6
	movsd	QWORD PTR g_sink[rip], xmm0
	pxor	xmm0, xmm0
	cvtsi2sd	xmm0, rax
	divsd	xmm0, QWORD PTR .LC3[rip]
	movsd	QWORD PTR [rdi], xmm0
	call	_ZN3SoAD1Ev
	nop
	movaps	xmm6, XMMWORD PTR 800[rsp]
	mov	rax, rdi
	add	rsp, 824
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L261:
	movabs	rax, 2305843009213693951
	cmp	rax, rbx
	jb	.L262
	lea	rbp, 0[0+rbx*4]
	mov	rcx, rbp
.LEHB2:
	call	_Znwy
	lea	rdx, [rax+rbp]
	movq	xmm1, rax
	movss	xmm0, DWORD PTR .LC6[rip]
	mov	rcx, rdx
	movq	xmm2, rdx
	sub	rcx, rax
	punpcklqdq	xmm1, xmm2
	and	ecx, 4
	je	.L232
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	cmp	rdx, rax
	je	.L260
	.p2align 4,,10
	.p2align 3
.L232:
	movss	DWORD PTR [rax], xmm0
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm0
	cmp	rdx, rax
	jne	.L232
.L260:
	mov	rcx, rbp
	movaps	XMMWORD PTR 32[rsp], xmm1
	mov	QWORD PTR 48[rsp], rdx
	call	_Znwy
	lea	rdx, [rax+rbp]
	movq	xmm1, rax
	movss	xmm0, DWORD PTR .LC7[rip]
	mov	rcx, rdx
	movq	xmm3, rdx
	sub	rcx, rax
	punpcklqdq	xmm1, xmm3
	and	ecx, 4
	je	.L233
	movss	DWORD PTR [rax], xmm0
	add	rax, 4
	cmp	rdx, rax
	je	.L259
	.p2align 4,,10
	.p2align 3
.L233:
	movss	DWORD PTR [rax], xmm0
	add	rax, 8
	movss	DWORD PTR -4[rax], xmm0
	cmp	rdx, rax
	jne	.L233
.L259:
	mov	rcx, rbp
	movups	XMMWORD PTR 56[rsp], xmm1
	mov	QWORD PTR 72[rsp], rdx
	call	_Znwy
	mov	r8, rbp
	xor	edx, edx
	mov	rcx, rax
	lea	r13, [rax+rbp]
	call	memset
	movq	xmm4, r13
	mov	QWORD PTR 96[rsp], r13
	movq	xmm0, rax
	punpcklqdq	xmm0, xmm4
	movaps	XMMWORD PTR 80[rsp], xmm0
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	test	rsi, rsi
	mov	rbp, rax
	jne	.L263
.L239:
	pxor	xmm6, xmm6
	jmp	.L234
.L262:
	lea	rcx, .LC0[rip]
	call	_ZSt20__throw_length_errorPKc
.LEHE2:
.L240:
	mov	rbx, rax
	mov	rcx, r12
	call	_ZN3SoAD1Ev
	mov	rcx, rbx
.LEHB3:
	call	_Unwind_Resume
	nop
.LEHE3:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5598:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5598-.LLSDACSB5598
.LLSDACSB5598:
	.uleb128 .LEHB2-.LFB5598
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L240-.LFB5598
	.uleb128 0
	.uleb128 .LEHB3-.LFB5598
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0
	.uleb128 0
.LLSDACSE5598:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
	.align 8
.LC8:
	.ascii "[\345\234\272\346\231\257"
	.ascii "1] \347\247\273\345\212\250\347\263\273\347\273\237\350\256\277\351\227\256\345\205\250\351\203\250\347\273\204\344\273\266\12\0"
.LC9:
	.ascii "  AoS: \0"
.LC10:
	.ascii " ms   SoA: \0"
.LC11:
	.ascii " ms\0"
.LC12:
	.ascii "   AoS/SoA=\0"
.LC13:
	.ascii "x\12\0"
	.align 8
.LC14:
	.ascii "[\345\234\272\346\231\257"
	.ascii "2] \345\211\224\351\231\244\347\263\273\347\273\237\345\217\252\350\256\277\351\227\256 Position(px,py)\12\0"
.LC15:
	.ascii "   SoA/AoS=\0"
.LC16:
	.ascii "  (sink \346\240\241\351\252\214\357\274\214\351\230\262\346\255\242 DCE: \0"
.LC17:
	.ascii ")\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5599:
	push	r13
	.seh_pushreg	r13
	push	r12
	.seh_pushreg	r12
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
	movaps	XMMWORD PTR 48[rsp], xmm6
	.seh_savexmm	xmm6, 48
	movaps	XMMWORD PTR 64[rsp], xmm7
	.seh_savexmm	xmm7, 64
	.seh_endprologue
	lea	r12, .LC9[rip]
	lea	rbp, .LC10[rip]
	lea	rdi, .LC11[rip]
	lea	rsi, .LC13[rip]
	call	__main
	mov	rbx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	r13, 32[rsp]
	lea	rdx, .LC8[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	edx, 60
	mov	ecx, 262144
	call	_Z14bench_aos_fullyy
	mov	edx, 60
	mov	ecx, 262144
	movapd	xmm7, xmm0
	call	_Z14bench_soa_fullyy
	mov	rdx, r12
	mov	rcx, rbx
	movapd	xmm6, xmm0
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rbp
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rdi
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC12[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	divsd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rsi
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC14[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rcx, r13
	mov	r8d, 60
	mov	edx, 262144
	call	_Z17bench_aos_partialyy
	mov	r8d, 60
	mov	rcx, r13
	mov	edx, 262144
	movsd	xmm7, QWORD PTR 32[rsp]
	call	_Z17bench_soa_partialyy
	mov	rdx, r12
	mov	rcx, rbx
	movsd	xmm6, QWORD PTR 32[rsp]
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm7
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rbp
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movapd	xmm1, xmm6
	mov	rcx, rax
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rdi
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC15[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	divsd	xmm7, xmm6
	mov	rcx, rax
	movapd	xmm1, xmm7
	call	_ZNSo9_M_insertIdEERSoT_
	mov	rdx, rsi
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	lea	rdx, .LC16[rip]
	mov	rcx, rbx
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	movsd	xmm0, QWORD PTR g_sink[rip]
	mov	rcx, rax
	cvttsd2si	edx, xmm0
	call	_ZNSo9_M_insertIlEERSoT_
	lea	rdx, .LC17[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	nop
	movaps	xmm6, XMMWORD PTR 48[rsp]
	xor	eax, eax
	movaps	xmm7, XMMWORD PTR 64[rsp]
	add	rsp, 88
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.seh_endproc
	.globl	g_sink
	.bss
	.align 8
g_sink:
	.space 8
	.section .rdata,"dr"
	.align 8
.LC1:
	.long	1015222895
	.long	1015222895
	.set	.LC2,.LC1
	.align 8
.LC3:
	.long	0
	.long	1093567616
	.align 4
.LC4:
	.long	1065353216
	.align 4
.LC6:
	.long	1073741824
	.align 4
.LC7:
	.long	1077936128
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_length_errorPKc;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIlEERSoT_;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
