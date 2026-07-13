	.file	"_ch142_system.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z15movement_systemRSt6vectorI8PositionSaIS0_EERKS_I8VelocitySaIS4_EEf
	.def	_Z15movement_systemRSt6vectorI8PositionSaIS0_EERKS_I8VelocitySaIS4_EEf;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15movement_systemRSt6vectorI8PositionSaIS0_EERKS_I8VelocitySaIS4_EEf
_Z15movement_systemRSt6vectorI8PositionSaIS0_EERKS_I8VelocitySaIS4_EEf:
.LFB1715:
	.seh_endprologue
	mov	r8, QWORD PTR 8[rcx]
	movsldup	xmm2, xmm2
	mov	r9, rdx
	mov	rdx, QWORD PTR [rcx]
	mov	rax, QWORD PTR [r9]
	mov	rcx, QWORD PTR 8[r9]
	sub	r8, rdx
	mov	r9, r8
	sub	rcx, rax
	sar	r9, 3
	mov	r10, rcx
	sar	r10, 3
	cmp	r8, rcx
	mov	rcx, r10
	cmovb	rcx, r9
	test	rcx, rcx
	je	.L1
	lea	rcx, [rax+rcx*8]
	.p2align 4,,10
	.p2align 3
.L5:
	movq	xmm0, QWORD PTR [rax]
	add	rax, 8
	add	rdx, 8
	movq	xmm1, QWORD PTR -8[rdx]
	mulps	xmm0, xmm2
	addps	xmm0, xmm1
	movlps	QWORD PTR -8[rdx], xmm0
	cmp	rax, rcx
	jne	.L5
.L1:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1718:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	call	__main
	mov	ecx, 4096
.LEHB0:
	call	_Znwy
.LEHE0:
	lea	rdx, 4096[rax]
	mov	rbx, rax
	mov	QWORD PTR 32[rsp], rax
	mov	QWORD PTR 48[rsp], rdx
	.p2align 4,,10
	.p2align 3
.L12:
	mov	QWORD PTR [rax], 0
	add	rax, 16
	mov	QWORD PTR -8[rax], 0
	cmp	rax, rdx
	jne	.L12
	mov	ecx, 4096
	pxor	xmm0, xmm0
	mov	QWORD PTR 40[rsp], rax
	movups	XMMWORD PTR 72[rsp], xmm0
.LEHB1:
	call	_Znwy
.LEHE1:
	movaps	xmm0, XMMWORD PTR .LC0[rip]
	mov	r11, rax
	mov	QWORD PTR 64[rsp], rax
	mov	rdx, rax
	lea	rcx, 4096[rax]
	.p2align 4,,10
	.p2align 3
.L13:
	movlps	QWORD PTR [rdx], xmm0
	add	rdx, 16
	movhps	QWORD PTR -8[rdx], xmm0
	cmp	rcx, rdx
	jne	.L13
	movss	xmm2, DWORD PTR .LC1[rip]
	mov	QWORD PTR 72[rsp], rcx
	lea	rdx, 64[rsp]
	lea	rcx, 32[rsp]
	call	_Z15movement_systemRSt6vectorI8PositionSaIS0_EERKS_I8VelocitySaIS4_EEf
	movss	xmm0, DWORD PTR .LC2[rip]
	mov	rcx, r11
	mov	edx, 4096
	mulss	xmm0, DWORD PTR [rbx]
	cvttss2si	esi, xmm0
	call	_ZdlPvy
	mov	edx, 4096
	mov	rcx, rbx
	call	_ZdlPvy
	mov	eax, esi
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
.L15:
	mov	rsi, rax
	mov	rcx, rbx
	mov	edx, 4096
	call	_ZdlPvy
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1718:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1718-.LLSDACSB1718
.LLSDACSB1718:
	.uleb128 .LEHB0-.LFB1718
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1718
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L15-.LFB1718
	.uleb128 0
	.uleb128 .LEHB2-.LFB1718
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE1718:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 16
.LC0:
	.long	1065353216
	.long	1056964608
	.long	1065353216
	.long	1056964608
	.align 4
.LC1:
	.long	1015222895
	.align 4
.LC2:
	.long	1148846080
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
