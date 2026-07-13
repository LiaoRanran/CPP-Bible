	.file	"_ch147_asm.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.def	__tcf_0;	.scl	3;	.type	32;	.endef
	.seh_proc	__tcf_0
__tcf_0:
.LFB1485:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, g_mtx[rip]
	call	pthread_mutex_destroy
	nop
	add	rsp, 40
	ret
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1485:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1485-.LLSDACSB1485
.LLSDACSB1485:
.LLSDACSE1485:
	.text
	.seh_endproc
	.p2align 4
	.globl	_Z16critical_sectionv
	.def	_Z16critical_sectionv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z16critical_sectionv
_Z16critical_sectionv:
.LFB1428:
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 32
	.seh_stackalloc	32
	.seh_endprologue
	lea	rbx, g_mtx[rip]
	mov	rcx, rbx
.LEHB0:
	call	pthread_mutex_lock
.LEHE0:
	test	eax, eax
	jne	.L5
	mov	rcx, rbx
	call	pthread_mutex_unlock
	nop
	add	rsp, 32
	pop	rbx
	ret
.L5:
	mov	ecx, eax
.LEHB1:
	call	_ZSt20__throw_system_errori
	nop
.LEHE1:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1428:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1428-.LLSDACSB1428
.LLSDACSB1428:
	.uleb128 .LEHB0-.LFB1428
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB1428
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1428:
	.text
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.def	_GLOBAL__sub_I_g_mtx;	.scl	3;	.type	32;	.endef
	.seh_proc	_GLOBAL__sub_I_g_mtx
_GLOBAL__sub_I_g_mtx:
.LFB1486:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, g_mtx[rip]
	xor	edx, edx
	call	pthread_mutex_init
	lea	rcx, __tcf_0[rip]
	add	rsp, 40
	jmp	atexit
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1486:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1486-.LLSDACSB1486
.LLSDACSB1486:
.LLSDACSE1486:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.ctors,"w"
	.align 8
	.quad	_GLOBAL__sub_I_g_mtx
	.globl	g_mtx
	.bss
	.align 8
g_mtx:
	.space 8
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	pthread_mutex_destroy;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_lock;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_unlock;	.scl	2;	.type	32;	.endef
	.def	_ZSt20__throw_system_errori;	.scl	2;	.type	32;	.endef
	.def	pthread_mutex_init;	.scl	2;	.type	32;	.endef
	.def	atexit;	.scl	2;	.type	32;	.endef
