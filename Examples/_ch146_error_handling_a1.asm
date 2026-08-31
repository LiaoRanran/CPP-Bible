	.file	"s.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_ZNKSt5ctypeIcE8do_widenEc,"x"
	.linkonce discard
	.align 2
	.p2align 4
	.globl	_ZNKSt5ctypeIcE8do_widenEc
	.def	_ZNKSt5ctypeIcE8do_widenEc;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZNKSt5ctypeIcE8do_widenEc
_ZNKSt5ctypeIcE8do_widenEc:
.LFB2659:
	.seh_endprologue
	mov	eax, edx
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z10compute_eciRi
	.def	_Z10compute_eciRi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10compute_eciRi
_Z10compute_eciRi:
.LFB5564:
	.seh_endprologue
	test	ecx, ecx
	je	.L5
	add	ecx, ecx
	xor	eax, eax
	mov	DWORD PTR [rdx], ecx
	ret
	.p2align 4,,10
	.p2align 3
.L5:
	mov	eax, -1
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "zero\0"
	.text
	.p2align 4
	.globl	_Z10compute_exi
	.def	_Z10compute_exi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10compute_exi
_Z10compute_exi:
.LFB5565:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	test	ecx, ecx
	je	.L11
	lea	eax, [rcx+rcx]
	add	rsp, 40
	pop	rbx
	pop	rsi
	ret
.L11:
	mov	ecx, 16
	call	__cxa_allocate_exception
	lea	rdx, .LC0[rip]
	mov	rcx, rax
	mov	rbx, rax
.LEHB0:
	call	_ZNSt13runtime_errorC1EPKc
.LEHE0:
	lea	r8, _ZNSt13runtime_errorD1Ev[rip]
	mov	rcx, rbx
	lea	rdx, _ZTISt13runtime_error[rip]
.LEHB1:
	call	__cxa_throw
.L9:
	mov	rsi, rax
	mov	rcx, rbx
	call	__cxa_free_exception
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE1:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA5565:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE5565-.LLSDACSB5565
.LLSDACSB5565:
	.uleb128 .LEHB0-.LFB5565
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L9-.LFB5565
	.uleb128 0
	.uleb128 .LEHB1-.LFB5565
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE5565:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section .rdata,"dr"
.LC1:
	.ascii "error-code success: \0"
.LC3:
	.ascii " ms\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB5566:
	push	rdi
	.seh_pushreg	rdi
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	xor	ebx, ebx
	call	__main
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rdi, rax
	mov	eax, 2
	.p2align 4,,10
	.p2align 3
.L13:
	add	rbx, rax
	add	rax, 2
	cmp	rax, 20000002
	jne	.L13
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	mov	rcx, QWORD PTR .refptr._ZSt4cout[rip]
	lea	rdx, .LC1[rip]
	add	QWORD PTR _ZL4sink[rip], rbx
	mov	rsi, rax
	sub	rsi, rdi
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	pxor	xmm1, xmm1
	cvtsi2sd	xmm1, rsi
	mov	rcx, rax
	divsd	xmm1, QWORD PTR .LC2[rip]
	call	_ZNSo9_M_insertIdEERSoT_
	lea	rdx, .LC3[rip]
	mov	rcx, rax
	call	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
	mov	rbx, rax
	mov	rax, QWORD PTR [rax]
	mov	rax, QWORD PTR -24[rax]
	mov	rsi, QWORD PTR 240[rbx+rax]
	test	rsi, rsi
	je	.L19
	cmp	BYTE PTR 56[rsi], 0
	je	.L15
	movzx	eax, BYTE PTR 67[rsi]
.L16:
	movsx	edx, al
	mov	rcx, rbx
	call	_ZNSo3putEc
	mov	rcx, rax
	call	_ZNSo5flushEv
	xor	eax, eax
	add	rsp, 32
	pop	rbx
	pop	rsi
	pop	rdi
	ret
.L15:
	mov	rcx, rsi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv
	mov	rax, QWORD PTR [rsi]
	lea	rdx, _ZNKSt5ctypeIcE8do_widenEc[rip]
	mov	r8, QWORD PTR 48[rax]
	mov	eax, 10
	cmp	r8, rdx
	je	.L16
	mov	edx, 10
	mov	rcx, rsi
	call	r8
	jmp	.L16
.L19:
	call	_ZSt16__throw_bad_castv
	nop
	.seh_endproc
	.globl	_ZTSSt9exception
	.section	.rdata$_ZTSSt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTSSt9exception:
	.ascii "St9exception\0"
	.globl	_ZTISt9exception
	.section	.rdata$_ZTISt9exception,"dr"
	.linkonce same_size
	.align 8
_ZTISt9exception:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSt9exception
	.globl	_ZTSSt13runtime_error
	.section	.rdata$_ZTSSt13runtime_error,"dr"
	.linkonce same_size
	.align 16
_ZTSSt13runtime_error:
	.ascii "St13runtime_error\0"
	.globl	_ZTISt13runtime_error
	.section	.rdata$_ZTISt13runtime_error,"dr"
	.linkonce same_size
	.align 8
_ZTISt13runtime_error:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSSt13runtime_error
	.quad	_ZTISt9exception
.lcomm _ZL4sink,8,8
	.section .rdata,"dr"
	.align 8
.LC2:
	.long	0
	.long	1093567616
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorC1EPKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSt13runtime_errorD1Ev;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.def	__cxa_free_exception;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
	.def	_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo9_M_insertIdEERSoT_;	.scl	2;	.type	32;	.endef
	.def	_ZNSo3putEc;	.scl	2;	.type	32;	.endef
	.def	_ZNSo5flushEv;	.scl	2;	.type	32;	.endef
	.def	_ZNKSt5ctypeIcE13_M_widen_initEv;	.scl	2;	.type	32;	.endef
	.def	_ZSt16__throw_bad_castv;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZSt4cout, "dr"
	.globl	.refptr._ZSt4cout
	.linkonce	discard
.refptr._ZSt4cout:
	.quad	_ZSt4cout
	.section	.rdata$.refptr._ZNSt13runtime_errorD1Ev, "dr"
	.globl	.refptr._ZNSt13runtime_errorD1Ev
	.linkonce	discard
.refptr._ZNSt13runtime_errorD1Ev:
	.quad	_ZNSt13runtime_errorD1Ev
