	.file	"_ch143_constexpr.cpp"
	.intel_syntax noprefix
	.text
	.section	.text$_Z3fibi,"x"
	.linkonce discard
	.p2align 4
	.globl	_Z3fibi
	.def	_Z3fibi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z3fibi
_Z3fibi:
.LFB0:
	push	r15
	.seh_pushreg	r15
	push	r14
	.seh_pushreg	r14
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
	sub	rsp, 136
	.seh_stackalloc	136
	.seh_endprologue
	cmp	ecx, 1
	mov	r12d, ecx
	jle	.L2
	lea	eax, -1[rcx]
	mov	ebp, ecx
	mov	esi, ecx
	mov	edx, eax
	xor	ebx, ebx
	mov	edi, eax
	and	edx, -2
	sub	ebp, edx
	cmp	esi, ebp
	je	.L3
.L64:
	sub	esi, 2
	mov	edx, edi
	xor	r13d, r13d
	mov	eax, esi
	and	eax, -2
	sub	edx, eax
	mov	DWORD PTR 104[rsp], edx
.L32:
	mov	edx, DWORD PTR 104[rsp]
	lea	eax, -1[rdi]
	mov	r15d, eax
	cmp	edi, edx
	je	.L4
.L63:
	sub	edi, 2
	mov	edx, r15d
	mov	DWORD PTR 76[rsp], r13d
	xor	r12d, r12d
	mov	eax, edi
	mov	r13d, esi
	and	eax, -2
	sub	edx, eax
	mov	eax, r15d
	mov	DWORD PTR 100[rsp], edx
.L29:
	cmp	DWORD PTR 100[rsp], eax
	lea	edx, -1[rax]
	mov	r8d, edx
	je	.L5
	lea	r14d, -2[rax]
	mov	eax, r8d
	xor	esi, esi
	mov	DWORD PTR 80[rsp], ebx
	mov	edx, r14d
	mov	DWORD PTR 88[rsp], r14d
	mov	r14d, esi
	and	edx, -2
	mov	DWORD PTR 84[rsp], r12d
	sub	eax, edx
	mov	DWORD PTR 96[rsp], eax
.L26:
	cmp	DWORD PTR 96[rsp], r8d
	lea	edx, -1[r8]
	mov	r10d, edx
	je	.L6
	lea	esi, -2[r8]
	mov	r9d, r10d
	mov	DWORD PTR 92[rsp], r14d
	mov	r11d, ebp
	mov	edx, esi
	mov	ebp, esi
	mov	r14d, r13d
	and	edx, -2
	xor	r12d, r12d
	mov	r13d, r10d
	sub	r9d, edx
	mov	esi, r9d
	mov	r9d, edi
.L23:
	lea	r8d, -1[r13]
	cmp	esi, r13d
	je	.L7
	sub	r13d, 2
	mov	r15d, r8d
	xor	edi, edi
	mov	eax, r13d
	and	eax, -2
	sub	r15d, eax
.L20:
	lea	eax, -1[r8]
	cmp	r8d, r15d
	mov	ebx, eax
	je	.L8
	lea	edx, -3[r8]
	sub	r8d, 2
	mov	ecx, ebx
	mov	eax, r8d
	mov	DWORD PTR 52[rsp], edx
	xor	r10d, r10d
	mov	edx, ebx
	and	eax, -2
	mov	ebx, r9d
	sub	ecx, eax
	mov	DWORD PTR 68[rsp], ecx
.L17:
	mov	r9d, DWORD PTR 68[rsp]
	lea	ecx, -1[rdx]
	mov	eax, ecx
	cmp	edx, r9d
	je	.L9
	lea	ecx, -4[rdx]
	mov	r9d, eax
	mov	DWORD PTR 60[rsp], edx
	mov	DWORD PTR 44[rsp], ecx
	mov	ecx, DWORD PTR 52[rsp]
	mov	DWORD PTR 48[rsp], 0
	mov	DWORD PTR 64[rsp], r8d
	and	ecx, -2
	sub	r9d, ecx
	mov	DWORD PTR 56[rsp], r9d
.L14:
	mov	ecx, DWORD PTR 56[rsp]
	cmp	eax, ecx
	je	.L10
	mov	ecx, DWORD PTR 44[rsp]
	lea	r8d, -2[rax]
	sub	eax, 4
	xor	edx, edx
	mov	r9d, r8d
	and	ecx, -2
	sub	eax, ecx
	mov	DWORD PTR 72[rsp], eax
.L11:
	mov	ecx, r9d
	mov	DWORD PTR 124[rsp], r8d
	mov	DWORD PTR 120[rsp], r11d
	mov	DWORD PTR 116[rsp], edx
	mov	DWORD PTR 112[rsp], r10d
	mov	DWORD PTR 108[rsp], r9d
	call	_Z3fibi
	mov	edx, DWORD PTR 116[rsp]
	mov	r9d, DWORD PTR 108[rsp]
	mov	r10d, DWORD PTR 112[rsp]
	mov	r11d, DWORD PTR 120[rsp]
	add	edx, eax
	mov	r8d, DWORD PTR 124[rsp]
	sub	r9d, 2
	cmp	DWORD PTR 72[rsp], r9d
	jne	.L11
	mov	r9d, DWORD PTR 44[rsp]
	mov	eax, r8d
	mov	ecx, r9d
	sub	r9d, 2
	and	ecx, 1
	mov	DWORD PTR 44[rsp], r9d
	add	ecx, edx
	add	DWORD PTR 48[rsp], ecx
	cmp	r8d, 1
	jne	.L14
	mov	eax, DWORD PTR 48[rsp]
	mov	edx, DWORD PTR 60[rsp]
	mov	r8d, DWORD PTR 64[rsp]
	add	eax, 1
.L13:
	sub	DWORD PTR 52[rsp], 2
	sub	edx, 2
	add	r10d, eax
	cmp	edx, 1
	jne	.L17
	mov	r9d, ebx
	add	r10d, 1
.L16:
	add	edi, r10d
	cmp	r8d, 1
	jne	.L20
	add	edi, 1
.L19:
	add	r12d, edi
	cmp	r13d, 1
	jne	.L23
	mov	r13d, r14d
	mov	r14d, DWORD PTR 92[rsp]
	mov	esi, ebp
	mov	edi, r9d
	mov	ebp, r11d
	add	r12d, 1
.L22:
	add	r14d, r12d
	cmp	esi, 1
	mov	r8d, esi
	jne	.L26
	mov	esi, r14d
	mov	ebx, DWORD PTR 80[rsp]
	mov	r12d, DWORD PTR 84[rsp]
	add	esi, 1
	mov	r14d, DWORD PTR 88[rsp]
.L25:
	add	r12d, esi
	cmp	r14d, 1
	mov	eax, r14d
	jne	.L29
	mov	esi, r13d
	mov	r13d, DWORD PTR 76[rsp]
	add	r12d, 1
	add	r13d, r12d
	cmp	edi, 1
	jne	.L32
.L62:
	mov	r14d, r13d
	add	r14d, 1
	add	ebx, r14d
	cmp	esi, 1
	jne	.L61
.L52:
	lea	r12d, 1[rbx]
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L8:
	add	edi, eax
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L9:
	mov	r9d, ebx
	add	r10d, ecx
	jmp	.L16
	.p2align 4,,10
	.p2align 3
.L10:
	mov	ecx, DWORD PTR 48[rsp]
	mov	edx, DWORD PTR 60[rsp]
	mov	r8d, DWORD PTR 64[rsp]
	lea	eax, -1[rax+rcx]
	jmp	.L13
.L7:
	mov	esi, ebp
	mov	r13d, r14d
	mov	edi, r9d
	mov	r14d, DWORD PTR 92[rsp]
	mov	ebp, r11d
	add	r12d, r8d
	jmp	.L22
.L6:
	mov	esi, r14d
	mov	ebx, DWORD PTR 80[rsp]
	mov	r12d, DWORD PTR 84[rsp]
	add	esi, edx
	mov	r14d, DWORD PTR 88[rsp]
	jmp	.L25
.L5:
	mov	esi, r13d
	mov	r13d, DWORD PTR 76[rsp]
	add	r12d, edx
	add	r13d, r12d
	cmp	edi, 1
	je	.L62
	mov	edx, DWORD PTR 104[rsp]
	lea	eax, -1[rdi]
	mov	r15d, eax
	cmp	edi, edx
	jne	.L63
.L4:
	mov	r14d, r13d
	add	r14d, eax
	add	ebx, r14d
	cmp	esi, 1
	je	.L52
.L61:
	lea	eax, -1[rsi]
	cmp	esi, ebp
	mov	edi, eax
	jne	.L64
.L3:
	lea	r12d, [rax+rbx]
.L2:
	mov	eax, r12d
	add	rsp, 136
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	pop	r14
	pop	r15
	ret
	.seh_endproc
	.text
	.p2align 4
	.globl	_Z9use_tablev
	.def	_Z9use_tablev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9use_tablev
_Z9use_tablev:
.LFB2:
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
	sub	rsp, 264
	.seh_stackalloc	264
	.seh_endprologue
	mov	r13d, -2
	xor	edi, edi
	lea	r12, 32[rsp]
	.p2align 4,,10
	.p2align 3
.L66:
	cmp	rdi, 1
	jbe	.L74
	lea	ebp, -3[rdi]
	mov	eax, r13d
	xor	esi, esi
	lea	ebx, -1[rdi]
	and	eax, -2
	sub	ebp, eax
.L67:
	mov	ecx, ebx
	sub	ebx, 2
	call	_Z3fibi
	add	esi, eax
	cmp	ebx, ebp
	jne	.L67
	mov	eax, r13d
	add	r13d, 1
	and	eax, 1
	add	eax, esi
	mov	DWORD PTR [r12+rdi*4], eax
	add	rdi, 1
	cmp	rdi, 55
	jne	.L66
	lea	rcx, 252[rsp]
	mov	rax, r12
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L71:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L71
	mov	eax, edx
	add	rsp, 264
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	pop	r12
	pop	r13
	ret
	.p2align 4,,10
	.p2align 3
.L74:
	mov	DWORD PTR [r12+rdi*4], edi
	add	r13d, 1
	add	rdi, 1
	jmp	.L66
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
