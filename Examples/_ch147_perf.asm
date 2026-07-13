	.file	"_ch147_perf.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10bad_lookupSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_Z10bad_lookupSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10bad_lookupSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z10bad_lookupSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB2313:
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
	mov	rbx, QWORD PTR [rcx]
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, rdx
	cmp	rdi, rbx
	je	.L7
	mov	rsi, QWORD PTR 8[rdx]
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L3:
	add	rbx, 40
	cmp	rdi, rbx
	je	.L7
.L6:
	cmp	QWORD PTR 8[rbx], rsi
	jne	.L3
	test	rsi, rsi
	je	.L5
	mov	rdx, QWORD PTR 0[rbp]
	mov	r8, rsi
	mov	rcx, QWORD PTR [rbx]
	call	memcmp
	test	eax, eax
	jne	.L3
.L5:
	mov	eax, DWORD PTR 32[rbx]
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	mov	eax, -1
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11good_lookupRKSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
	.def	_Z11good_lookupRKSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11good_lookupRKSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z11good_lookupRKSt6vectorI6RecordSaIS0_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE:
.LFB2318:
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
	mov	rbx, QWORD PTR [rcx]
	mov	rdi, QWORD PTR 8[rcx]
	mov	rbp, rdx
	cmp	rdi, rbx
	je	.L19
	mov	rsi, QWORD PTR 8[rdx]
	jmp	.L18
	.p2align 4,,10
	.p2align 3
.L15:
	add	rbx, 40
	cmp	rdi, rbx
	je	.L19
.L18:
	cmp	QWORD PTR 8[rbx], rsi
	jne	.L15
	test	rsi, rsi
	je	.L17
	mov	rdx, QWORD PTR 0[rbp]
	mov	r8, rsi
	mov	rcx, QWORD PTR [rbx]
	call	memcmp
	test	eax, eax
	jne	.L15
.L17:
	mov	eax, DWORD PTR 32[rbx]
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.p2align 4,,10
	.p2align 3
.L19:
	mov	eax, -1
	add	rsp, 40
	pop	rbx
	pop	rsi
	pop	rdi
	pop	rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
	.def	memcmp;	.scl	2;	.type	32;	.endef
