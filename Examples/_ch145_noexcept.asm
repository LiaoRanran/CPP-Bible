	.file	"_ch145_noexcept.cpp"
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
	.section	.text.unlikely,"x"
	.globl	_Z7fragilev
	.def	_Z7fragilev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7fragilev
_Z7fragilev:
.LFB49:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	mov	ecx, 4
	call	__cxa_allocate_exception
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	xor	r8d, r8d
	mov	rcx, rax
	mov	DWORD PTR [rax], 1
	call	__cxa_throw
	nop
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "ok\12\0"
	.text
	.p2align 4
	.globl	_Z5solidv
	.def	_Z5solidv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z5solidv
_Z5solidv:
.LFB50:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC0[rip]
	call	_Z6printfPKcz
	nop
	add	rsp, 40
	ret
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA50:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE50-.LLSDACSB50
.LLSDACSB50:
.LLSDACSE50:
	.text
	.seh_endproc
	.section	.text.unlikely,"x"
	.globl	_Z12call_fragilev
	.def	_Z12call_fragilev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12call_fragilev
_Z12call_fragilev:
.LFB51:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	_Z7fragilev
	nop
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z10call_solidv
	.def	_Z10call_solidv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10call_solidv
_Z10call_solidv:
.LFB55:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	lea	rcx, .LC0[rip]
	call	_Z6printfPKcz
	nop
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA55:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE55-.LLSDACSB55
.LLSDACSB55:
.LLSDACSE55:
	.text
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB53:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	lea	rcx, .LC0[rip]
	call	_Z6printfPKcz
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA53:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE53-.LLSDACSB53
.LLSDACSB53:
.LLSDACSE53:
	.section	.text.startup,"x"
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	__mingw_vfprintf;	.scl	2;	.type	32;	.endef
	.def	__cxa_allocate_exception;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw;	.scl	2;	.type	32;	.endef
	.section	.rdata$.refptr._ZTIi, "dr"
	.globl	.refptr._ZTIi
	.linkonce	discard
.refptr._ZTIi:
	.quad	_ZTIi
