	.file	"_ch147_refactor.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z10bad_reportRKSt6vectorIiSaIiEES3_
	.def	_Z10bad_reportRKSt6vectorIiSaIiEES3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10bad_reportRKSt6vectorIiSaIiEES3_
_Z10bad_reportRKSt6vectorIiSaIiEES3_:
.LFB2313:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r8, QWORD PTR 8[rcx]
	xor	ecx, ecx
	cmp	r8, rax
	je	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	add	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	r8, rax
	jne	.L3
.L2:
	mov	rax, QWORD PTR [rdx]
	mov	r8, QWORD PTR 8[rdx]
	cmp	r8, rax
	je	.L1
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L5:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	r8, rax
	jne	.L5
	add	ecx, edx
.L1:
	mov	eax, ecx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z6sum_ofRKSt6vectorIiSaIiEE
	.def	_Z6sum_ofRKSt6vectorIiSaIiEE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z6sum_ofRKSt6vectorIiSaIiEE
_Z6sum_ofRKSt6vectorIiSaIiEE:
.LFB2318:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rcx, QWORD PTR 8[rcx]
	cmp	rcx, rax
	je	.L10
	.p2align 4,,10
	.p2align 3
.L12:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, rcx
	jne	.L12
.L10:
	mov	eax, edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z11good_reportRKSt6vectorIiSaIiEES3_
	.def	_Z11good_reportRKSt6vectorIiSaIiEES3_;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z11good_reportRKSt6vectorIiSaIiEES3_
_Z11good_reportRKSt6vectorIiSaIiEES3_:
.LFB2319:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r8, QWORD PTR 8[rcx]
	xor	ecx, ecx
	cmp	rax, r8
	je	.L16
	.p2align 4,,10
	.p2align 3
.L17:
	add	ecx, DWORD PTR [rax]
	add	rax, 4
	cmp	rax, r8
	jne	.L17
.L16:
	mov	rax, QWORD PTR [rdx]
	mov	r8, QWORD PTR 8[rdx]
	cmp	r8, rax
	je	.L15
	xor	edx, edx
	.p2align 4,,10
	.p2align 3
.L19:
	add	edx, DWORD PTR [rax]
	add	rax, 4
	cmp	r8, rax
	jne	.L19
	add	ecx, edx
.L15:
	mov	eax, ecx
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0"
