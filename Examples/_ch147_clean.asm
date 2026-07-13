	.file	"_ch147_clean.cpp"
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
	.text
	.p2align 4
	.globl	_Z3sumRKSt6vectorIiSaIiEE
	.def	_Z3sumRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3sumRKSt6vectorIiSaIiEE
_Z3sumRKSt6vectorIiSaIiEE:
.LFB1760:
	.seh_endprologue
	mov	rax, QWORD PTR 8[rcx]
	mov	rcx, QWORD PTR [rcx]
	mov	r8, rax
	sub	r8, rcx
	sar	r8, 2
	cmp	rax, rcx
	je	.L6
	xor	eax, eax
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L5:
	add	edx, DWORD PTR [rcx+rax*4]
	add	rax, 1
	cmp	rax, r8
	jb	.L5
	mov	eax, edx
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	xor	edx, edx
	mov	eax, edx
	ret
	.seh_endproc
	.section	.text$_ZNSt12_Vector_baseIiSaIiEED2Ev,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNSt12_Vector_baseIiSaIiEED2Ev
	.def	_ZNSt12_Vector_baseIiSaIiEED2Ev;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNSt12_Vector_baseIiSaIiEED2Ev
_ZNSt12_Vector_baseIiSaIiEED2Ev:
.LFB1815:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L8
	mov	rdx, QWORD PTR 16[rcx]
	mov	rcx, rax
	sub	rdx, rax
	jmp	_ZdlPvy
	.p2align 4,,10
	.p2align 3
.L8:
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "%d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB1761:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	call	__main
	mov	rax, QWORD PTR .LC0[rip]
	mov	ecx, 12
	pxor	xmm0, xmm0
	mov	DWORD PTR 40[rsp], 3
	movaps	XMMWORD PTR 48[rsp], xmm0
	mov	QWORD PTR 64[rsp], 0
	mov	QWORD PTR 32[rsp], rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rdx, QWORD PTR 32[rsp]
	mov	rbx, rax
	mov	QWORD PTR 48[rsp], rax
	lea	rsi, 48[rsp]
	lea	rax, 12[rax]
	mov	rcx, rsi
	mov	QWORD PTR 64[rsp], rax
	mov	QWORD PTR [rbx], rdx
	mov	edx, DWORD PTR 40[rsp]
	mov	QWORD PTR 56[rsp], rax
	mov	DWORD PTR 8[rbx], edx
	call	_Z3sumRKSt6vectorIiSaIiEE
	lea	rcx, .LC1[rip]
	mov	edx, eax
.LEHB1:
	call	_Z6printfPKcz
.LEHE1:
	mov	rcx, rsi
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	xor	eax, eax
	add	rsp, 88
	pop	rbx
	pop	rsi
	ret
.L15:
	lea	rcx, 48[rsp]
	mov	rbx, rax
	call	_ZNSt12_Vector_baseIiSaIiEED2Ev
	mov	rcx, rbx
.LEHB2:
	call	_Unwind_Resume
.L14:
	mov	rsi, rax
	mov	rcx, rbx
	mov	edx, 12
	call	_ZdlPvy
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1761:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1761-.LLSDACSB1761
.LLSDACSB1761:
	.uleb128 .LEHB0-.LFB1761
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L15-.LFB1761
	.uleb128 0
	.uleb128 .LEHB1-.LFB1761
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L14-.LFB1761
	.uleb128 0
	.uleb128 .LEHB2-.LFB1761
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE1761:
	.section	.text.startup,"x"
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.long	1
	.long	2
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
