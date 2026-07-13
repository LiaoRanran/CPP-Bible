	.file	"_ch130_flat_hash_map.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z8sum_evenRK7FlatMapIiiLy1024EEi
	.def	_Z8sum_evenRK7FlatMapIiiLy1024EEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8sum_evenRK7FlatMapIiiLy1024EEi
_Z8sum_evenRK7FlatMapIiiLy1024EEi:
.LFB18:
	.seh_endprologue
	test	edx, edx
	jle	.L7
	lea	r8d, [rdx+rdx]
	xor	r9d, r9d
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L6:
	mov	eax, edx
	and	eax, 1023
	cmp	BYTE PTR 8192[rcx+rax], 0
	jne	.L5
	jmp	.L3
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
	cmp	edx, r8d
	jne	.L6
	mov	eax, r9d
	ret
.L7:
	xor	r9d, r9d
	mov	eax, r9d
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB19:
	push	rbx
	.seh_pushreg	rbx
	mov	eax, 9296
	call	___chkstk_ms
	sub	rsp, rax
	.seh_stackalloc	9296
	.seh_endprologue
	call	__main
	lea	rbx, 95[rsp]
	xor	edx, edx
	mov	r8d, 1024
	and	rbx, -64
	lea	r9, 8192[rbx]
	mov	rcx, r9
	call	memset
	xor	edx, edx
	xor	ecx, ecx
	mov	r9, rax
	.p2align 4,,10
	.p2align 3
.L14:
	cmp	BYTE PTR [r9+rdx], 0
	mov	r8d, edx
	mov	rax, rdx
	je	.L12
	.p2align 4,,10
	.p2align 3
.L13:
	add	rax, 1
	and	eax, 1023
	cmp	BYTE PTR 8192[rbx+rax], 0
	jne	.L13
.L12:
	mov	DWORD PTR 4096[rbx+rax*4], ecx
	add	ecx, 1
	add	rdx, 2
	cmp	ecx, 512
	mov	DWORD PTR [rbx+rax*4], r8d
	mov	BYTE PTR 8192[rbx+rax], 1
	jne	.L14
	mov	edx, 512
	mov	rcx, rbx
	call	_Z8sum_evenRK7FlatMapIiiLy1024EEi
	add	rsp, 9296
	pop	rbx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memset;	.scl	2;	.type	32;	.endef
