	.file	"_atom_move_alloc.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Znwy
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znwy
_Znwy:
.LFB276:
	.seh_endprologue
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_Znay
	.def	_Znay;	.scl	2;	.type	32;	.endef
	.seh_proc	_Znay
_Znay:
.LFB307:
	.seh_endprologue
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	jmp	malloc
	.seh_endproc
	.p2align 4
	.globl	_ZdlPv
	.def	_ZdlPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPv
_ZdlPv:
.LFB278:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdlPvy
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdlPvy
_ZdlPvy:
.LFB279:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdaPv
	.def	_ZdaPv;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPv
_ZdaPv:
.LFB309:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.p2align 4
	.globl	_ZdaPvy
	.def	_ZdaPvy;	.scl	2;	.type	32;	.endef
	.seh_proc	_ZdaPvy
_ZdaPvy:
.LFB311:
	.seh_endprologue
	jmp	free
	.seh_endproc
	.section .rdata,"dr"
	.align 8
.LC0:
	.ascii "\350\257\201\344\274\252\345\257\271\347\205\247(\345\201\207\347\247\273\345\212\250)\345\210\206\351\205\215=%ld\12\0"
	.align 8
.LC1:
	.ascii "\346\236\204\351\200\240\345\210\206\351\205\215=%ld \346\213\267\350\264\235\345\210\206\351\205\215=%ld \347\247\273\345\212\250\345\210\206\351\205\215=%ld\12\0"
	.section	.text.unlikely,"x"
.LCOLDB2:
	.section	.text.startup,"x"
.LHOTB2:
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB303:
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
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	movsxd	rbx, ecx
	call	__main
	add	rbx, 1
	movabs	rax, 2305843009213693950
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	lea	rsi, 0[0+rbx*8]
	cmp	rax, rsi
	jb	.L9
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	sal	rbx, 5
	mov	rcx, rbx
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	call	malloc
	mov	r12d, DWORD PTR _ZL8g_allocs[rip]
	mov	rcx, rbx
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	rbp, rax
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	call	malloc
	mov	rdi, rax
	xor	eax, eax
	test	rsi, rsi
	je	.L11
	.p2align 4
	.p2align 4
	.p2align 3
.L10:
	mov	edx, DWORD PTR 0[rbp+rax*4]
	mov	DWORD PTR [rdi+rax*4], edx
	add	rax, 1
	cmp	rsi, rax
	jne	.L10
.L11:
	mov	esi, DWORD PTR _ZL8g_allocs[rip]
	mov	rcx, rbx
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	r13d, DWORD PTR _ZL8g_allocs[rip]
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	mov	DWORD PTR _ZL8g_allocs[rip], 0
	mov	eax, DWORD PTR _ZL8g_allocs[rip]
	add	eax, 1
	mov	DWORD PTR _ZL8g_allocs[rip], eax
	call	malloc
	mov	edx, DWORD PTR _ZL8g_allocs[rip]
	lea	rcx, .LC0[rip]
	mov	rbx, rax
.LEHB0:
	call	__mingw_printf
.LEHE0:
	test	rbx, rbx
	je	.L12
	mov	rcx, rbx
	call	free
.L12:
	test	rbp, rbp
	je	.L13
	mov	rcx, rbp
	call	free
.L13:
	test	rdi, rdi
	je	.L14
	mov	rcx, rdi
	call	free
.L14:
	mov	r9d, r13d
	mov	r8d, esi
	lea	rcx, .LC1[rip]
	mov	edx, r12d
.LEHB1:
	call	__mingw_printf
.LEHE1:
	xor	eax, eax
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
.L20:
	mov	rsi, rax
	jmp	.L15
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA303:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE303-.LLSDACSB303
.LLSDACSB303:
	.uleb128 .LEHB0-.LFB303
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L20-.LFB303
	.uleb128 0
	.uleb128 .LEHB1-.LFB303
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE303:
	.section	.text.startup,"x"
	.seh_endproc
	.section	.text.unlikely,"x"
	.def	main.cold;	.scl	3;	.type	32;	.endef
	.seh_proc	main.cold
	.seh_stackalloc	88
	.seh_savereg	rbx, 40
	.seh_savereg	rsi, 48
	.seh_savereg	rdi, 56
	.seh_savereg	rbp, 64
	.seh_savereg	r12, 72
	.seh_savereg	r13, 80
	.seh_endprologue
main.cold:
.L9:
.LEHB2:
	call	__cxa_throw_bad_array_new_length
.L15:
	test	rbx, rbx
	je	.L16
	mov	rcx, rbx
	call	free
.L16:
	test	rbp, rbp
	je	.L17
	mov	rcx, rbp
	call	free
.L17:
	test	rdi, rdi
	je	.L18
	mov	rcx, rdi
	call	free
.L18:
	mov	rcx, rsi
	call	_Unwind_Resume
	nop
.LEHE2:
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDAC303:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSEC303-.LLSDACSBC303
.LLSDACSBC303:
	.uleb128 .LEHB2-.LCOLDB2
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSEC303:
	.section	.text.unlikely,"x"
	.section	.text.startup,"x"
	.section	.text.unlikely,"x"
	.seh_endproc
.LCOLDE2:
	.section	.text.startup,"x"
.LHOTE2:
.lcomm _ZL8g_allocs,4,4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	malloc;	.scl	2;	.type	32;	.endef
	.def	free;	.scl	2;	.type	32;	.endef
	.def	__cxa_throw_bad_array_new_length;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
