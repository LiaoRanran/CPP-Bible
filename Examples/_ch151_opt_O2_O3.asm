	.file	"_ch151_opt_O2.cpp"
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
	.section	.text$_ZNSt6vectorIdSaIdEED1Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt6vectorIdSaIdEED1Ev
	.def	_ZNSt6vectorIdSaIdEED1Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt6vectorIdSaIdEED1Ev
_ZNSt6vectorIdSaIdEED1Ev:
.LFB6114:
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
.LC4:
	.ascii "opt_O2: axpy_ms=%.3f chk=%.1f\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5605:
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
	sub	rsp, 152
	.seh_stackalloc	152
	.seh_endprologue
	call	__main
	mov	ecx, 400000000
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	r8d, 399999992
	xor	edx, edx
	lea	r12, 400000000[rax]
	lea	rcx, 8[rax]
	mov	rbx, rax
	mov	QWORD PTR 48[rsp], rax
	mov	QWORD PTR 64[rsp], r12
	mov	QWORD PTR [rax], 0x000000000
	call	memset
	mov	ecx, 400000000
	mov	QWORD PTR 56[rsp], r12
	mov	QWORD PTR 88[rsp], 0
	mov	QWORD PTR 96[rsp], 0
.LEHB1:
	call	_Znwy
.LEHE1:
	lea	rbp, 400000000[rax]
	lea	rcx, 8[rax]
	mov	r8d, 399999992
	xor	edx, edx
	mov	rsi, rax
	mov	QWORD PTR 80[rsp], rax
	mov	QWORD PTR 96[rsp], rbp
	mov	QWORD PTR [rax], 0x000000000
	call	memset
	mov	ecx, 400000000
	mov	QWORD PTR 88[rsp], rbp
	mov	QWORD PTR 120[rsp], 0
	mov	QWORD PTR 128[rsp], 0
.LEHB2:
	call	_Znwy
.LEHE2:
	lea	r13, 400000000[rax]
	lea	rcx, 8[rax]
	mov	r8d, 399999992
	xor	edx, edx
	mov	rdi, rax
	mov	QWORD PTR 112[rsp], rax
	mov	QWORD PTR 128[rsp], r13
	mov	QWORD PTR [rax], 0x000000000
	call	memset
	mov	rax, rbx
	vmovsd	xmm1, QWORD PTR .LC0[rip]
	mov	QWORD PTR 120[rsp], r13
	vmovsd	xmm0, xmm1, xmm1
	.p2align 4
	.p2align 3
.L7:
	vmovsd	QWORD PTR [rax], xmm0
	add	rax, 8
	vaddsd	xmm0, xmm0, xmm1
	cmp	rax, r12
	jne	.L7
	mov	rax, rsi
	vmovsd	xmm0, QWORD PTR .LC1[rip]
	.p2align 4
	.p2align 3
.L8:
	vmovsd	QWORD PTR [rax], xmm0
	add	rax, 8
	vaddsd	xmm0, xmm0, xmm1
	cmp	rbp, rax
	jne	.L8
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rbp, rax
	xor	eax, eax
	.p2align 4
	.p2align 3
.L9:
	vmovupd	zmm0, ZMMWORD PTR [rsi+rax]
	vmovupd	zmm3, ZMMWORD PTR [rbx+rax]
	vfmadd132pd	zmm0, zmm3, zmm3
	vmovupd	ZMMWORD PTR [rdi+rax], zmm0
	add	rax, 64
	cmp	rax, 400000000
	jne	.L9
	vzeroupper
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	vmovsd	xmm0, QWORD PTR 399999992[rdi]
	vmovsd	QWORD PTR 40[rsp], xmm0
	mov	r8, QWORD PTR 40[rsp]
	sub	rax, rbp
	vxorps	xmm1, xmm1, xmm1
	lea	rcx, .LC4[rip]
	vcvtsi2sd	xmm1, xmm1, rax
	vdivsd	xmm1, xmm1, QWORD PTR .LC3[rip]
	vmovq	rdx, xmm1
	vmovq	xmm2, r8
.LEHB3:
	call	_Z6printfPKcz
.LEHE3:
	lea	rcx, 112[rsp]
	call	_ZNSt6vectorIdSaIdEED1Ev
	lea	rcx, 80[rsp]
	call	_ZNSt6vectorIdSaIdEED1Ev
	lea	rcx, 48[rsp]
	call	_ZNSt6vectorIdSaIdEED1Ev
	xor	eax, eax
	add	rsp, 152
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L13:
	mov	rbx, rax
	vzeroupper
.L12:
	lea	rcx, 48[rsp]
	call	_ZNSt6vectorIdSaIdEED1Ev
	mov	rcx, rbx
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L15:
	lea	rcx, 112[rsp]
	mov	rbx, rax
	vzeroupper
	call	_ZNSt6vectorIdSaIdEED1Ev
.L11:
	lea	rcx, 80[rsp]
	call	_ZNSt6vectorIdSaIdEED1Ev
	jmp	.L12
.L14:
	mov	rbx, rax
	vzeroupper
	jmp	.L11
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
	.uleb128 .L13-.LFB5605
	.uleb128 0
	.uleb128 .LEHB2-.LFB5605
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L14-.LFB5605
	.uleb128 0
	.uleb128 .LEHB3-.LFB5605
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L15-.LFB5605
	.uleb128 0
	.uleb128 .LEHB4-.LFB5605
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0
	.uleb128 0
.LLSDACSE5605:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	0
	.long	1072693248
	.align 8
.LC1:
	.long	0
	.long	1073741824
	.align 8
.LC3:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	memset;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
