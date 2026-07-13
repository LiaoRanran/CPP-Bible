	.file	"_ch145_pimpl.cpp"
	.intel_syntax noprefix
	.text
	.section .rdata,"dr"
.LC0:
	.ascii "%d\12\0"
	.text
	.p2align 4
	.def	_ZL6printfPKcz.constprop.0;	.scl	3;	.type	32;	.endef
	.seh_proc	_ZL6printfPKcz.constprop.0
_ZL6printfPKcz.constprop.0:
.LFB4200:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 48
	.seh_stackalloc	48
	.seh_endprologue
	mov	ecx, 1
	lea	rbx, 72[rsp]
	mov	QWORD PTR 72[rsp], rdx
	mov	QWORD PTR 80[rsp], r8
	mov	QWORD PTR 88[rsp], r9
	mov	QWORD PTR 40[rsp], rbx
	call	[QWORD PTR __imp___acrt_iob_func[rip]]
	lea	rdx, .LC0[rip]
	mov	r8, rbx
	mov	rcx, rax
	call	__mingw_vfprintf
	add	rsp, 48
	pop	rbx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z9draw_impli
	.def	_Z9draw_impli;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9draw_impli
_Z9draw_impli:
.LFB3493:
	.seh_endprologue
	mov	edx, ecx
	lea	rcx, .LC0[rip]
	jmp	_ZL6printfPKcz.constprop.0
	.seh_endproc
	.p2align 4
	.globl	_Z12use_indirectPFviEi
	.def	_Z12use_indirectPFviEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12use_indirectPFviEi
_Z12use_indirectPFviEi:
.LFB3494:
	.seh_endprologue
	mov	rax, rcx
	mov	ecx, edx
	rex.W jmp	rax
	.seh_endproc
	.p2align 4
	.globl	_Z10use_directi
	.def	_Z10use_directi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10use_directi
_Z10use_directi:
.LFB4199:
	.seh_endprologue
	mov	edx, ecx
	lea	rcx, .LC0[rip]
	jmp	_ZL6printfPKcz.constprop.0
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB3496:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	lea	rbx, 40[rsp]
	mov	rcx, rbx
.LEHB0:
	call	_ZN6WidgetC1Ev
.LEHE0:
	mov	rcx, rbx
.LEHB1:
	call	_ZN6Widget4drawEv
	mov	ecx, 7
	call	_Z9draw_impli
	lea	rcx, .LC0[rip]
	mov	edx, 7
	call	_ZL6printfPKcz.constprop.0
	mov	rcx, rbx
	call	_ZNK6Widget6metricEv
.LEHE1:
	mov	esi, eax
	mov	rcx, rbx
	call	_ZN6WidgetD1Ev
	mov	eax, esi
	add	rsp, 56
	pop	rbx
	pop	rsi
	ret
.L8:
	mov	rsi, rax
	mov	rcx, rbx
	call	_ZN6WidgetD1Ev
	mov	rcx, rsi
.LEHB2:
	call	_Unwind_Resume
	nop
.LEHE2:
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA3496:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3496-.LLSDACSB3496
.LLSDACSB3496:
	.uleb128 .LEHB0-.LFB3496
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB3496
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L8-.LFB3496
	.uleb128 0
	.uleb128 .LEHB2-.LFB3496
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE3496:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	_ZN6WidgetC1Ev;	.scl	2;	.type	32;	.endef
	.def	_ZN6Widget4drawEv;	.scl	2;	.type	32;	.endef
	.def	_ZNK6Widget6metricEv;	.scl	2;	.type	32;	.endef
	.def	_ZN6WidgetD1Ev;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
