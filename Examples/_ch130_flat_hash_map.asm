	.file	"_ch130_flat_hash_map.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8sum_evenRK7FlatMapIiiLy1024EEi
	.def	_Z8sum_evenRK7FlatMapIiiLy1024EEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sum_evenRK7FlatMapIiiLy1024EEi
_Z8sum_evenRK7FlatMapIiiLy1024EEi:
.LFB19:
	.seh_endprologue
	test	edx, edx
	jle	.L7
	lea	r8d, [rdx+rdx]
	xor	r9d, r9d
	xor	edx, edx
	.p2align 4
	.p2align 3
.L6:
	mov	eax, edx
	and	eax, 1023
	cmp	BYTE PTR 8192[rcx+rax], 0
	jne	.L5
	jmp	.L3
	.p2align 5
	.p2align 4,,10
	.p2align 3
.L4:
	add	rax, 1
	and	eax, 1023
	cmp	BYTE PTR 8192[rcx+rax], 0
	je	.L3
.L5:
	cmp	edx, DWORD PTR [rcx+rax*4]
	jne	.L4
	add	r9d, DWORD PTR 4096[rcx+rax*4]
.L3:
	add	edx, 2
	cmp	r8d, edx
	jne	.L6
	mov	eax, r9d
	ret
.L7:
	xor	r9d, r9d
	mov	eax, r9d
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB20:
	push	rdi
	.seh_pushreg	rdi
	mov	eax, 9304
	push	rbx
	.seh_pushreg	rbx
	call	___chkstk_ms
	sub	rsp, rax
	.seh_stackalloc	9304
	.seh_endprologue
	call	__main
	lea	rbx, 95[rsp]
	xor	eax, eax
	xor	edx, edx
	and	rbx, -64
	mov	ecx, 128
	lea	rdi, 8192[rbx]
	lea	r8, 8192[rbx]
	rep stosq
	.p2align 4
	.p2align 3
.L14:
	mov	r9d, ecx
	mov	rax, rcx
	cmp	BYTE PTR [r8], 0
	je	.L12
	.p2align 5
	.p2align 4
	.p2align 3
.L13:
	add	rax, 1
	and	eax, 1023
	cmp	BYTE PTR 8192[rbx+rax], 0
	jne	.L13
.L12:
	mov	DWORD PTR 4096[rbx+rax*4], edx
	add	edx, 1
	add	r8, 2
	add	rcx, 2
	mov	DWORD PTR [rbx+rax*4], r9d
	mov	BYTE PTR 8192[rbx+rax], 1
	cmp	edx, 512
	jne	.L14
	mov	rcx, rbx
	call	_Z8sum_evenRK7FlatMapIiiLy1024EEi
	add	rsp, 9304
	pop	rbx
	pop	rdi
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
