	.file	"_asm_sso.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z7use_ssov
	.def	_Z7use_ssov;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z7use_ssov
_Z7use_ssov:
.LFB1951:
	push	rsi
	.seh_pushreg	rsi
	push	rbx
	.seh_pushreg	rbx
	sub	rsp, 104
	.seh_stackalloc	104
	.seh_endprologue
	mov	eax, 26984
	mov	ecx, 52
	lea	rsi, 48[rsp]
	mov	WORD PTR 48[rsp], ax
	lea	rax, 80[rsp]
	mov	QWORD PTR 32[rsp], rsi
	mov	QWORD PTR 40[rsp], 2
	mov	BYTE PTR 50[rsp], 0
	mov	QWORD PTR 64[rsp], rax
.LEHB0:
	call	_Znwy
.LEHE0:
	mov	rcx, rax
	mov	edx, 52
	movabs	rax, 2338328219631577204
	mov	QWORD PTR [rcx], rax
	movabs	rax, 8295744237629874273
	mov	QWORD PTR 8[rcx], rax
	movabs	rax, 7526676505849066100
	mov	QWORD PTR 16[rcx], rax
	movabs	rax, 7306355339222348897
	mov	QWORD PTR 24[rcx], rax
	movabs	rax, 8295742012915741540
	mov	QWORD PTR 32[rcx], rax
	movabs	rax, 7382915055541313901
	mov	QWORD PTR 40[rcx], rax
	mov	eax, DWORD PTR 40[rsp]
	mov	DWORD PTR 47[rcx], 1919247974
	mov	BYTE PTR 51[rcx], 0
	lea	ebx, 51[rax]
	call	_ZdlPvy
	mov	rcx, QWORD PTR 32[rsp]
	cmp	rcx, rsi
	je	.L1
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
.L1:
	mov	eax, ebx
	add	rsp, 104
	pop	rbx
	pop	rsi
	ret
.L5:
	mov	rcx, QWORD PTR 32[rsp]
	mov	rbx, rax
	cmp	rcx, rsi
	jne	.L7
.L4:
	mov	rcx, rbx
.LEHB1:
	call	_Unwind_Resume
.LEHE1:
.L7:
	mov	rax, QWORD PTR 48[rsp]
	lea	rdx, 1[rax]
	call	_ZdlPvy
	jmp	.L4
	.def	__gxx_personality_seh0;	.scl	2;	.type	32;	.endef
	.seh_handler	__gxx_personality_seh0, @unwind, @except
	.seh_handlerdata
.LLSDA1951:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1951-.LLSDACSB1951
.LLSDACSB1951:
	.uleb128 .LEHB0-.LFB1951
	.uleb128 .LEHE0-.LEHB0
	.uleb128 .L5-.LFB1951
	.uleb128 0
	.uleb128 .LEHB1-.LFB1951
	.uleb128 .LEHE1-.LEHB1
	.uleb128 0
	.uleb128 0
.LLSDACSE1951:
	.text
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	_Znwy;	.scl	2;	.type	32;	.endef
	.def	_ZdlPvy;	.scl	2;	.type	32;	.endef
	.def	_Unwind_Resume;	.scl	2;	.type	32;	.endef
