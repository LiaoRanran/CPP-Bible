	.file	"_ch109_fence_perf.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z13relaxed_storeRSt6atomicIiEi
	.def	_Z13relaxed_storeRSt6atomicIiEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13relaxed_storeRSt6atomicIiEi
_Z13relaxed_storeRSt6atomicIiEi:
.LFB665:
	.seh_endprologue
	mov	DWORD PTR [rcx], edx
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12relaxed_loadRSt6atomicIiE
	.def	_Z12relaxed_loadRSt6atomicIiE;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12relaxed_loadRSt6atomicIiE
_Z12relaxed_loadRSt6atomicIiE:
.LFB666:
	.seh_endprologue
	mov	eax, DWORD PTR [rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12seqcst_storeRSt6atomicIiEi
	.def	_Z12seqcst_storeRSt6atomicIiEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12seqcst_storeRSt6atomicIiEi
_Z12seqcst_storeRSt6atomicIiEi:
.LFB667:
	.seh_endprologue
	xchg	edx, DWORD PTR [rcx]
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z12seqcst_fencev
	.def	_Z12seqcst_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z12seqcst_fencev
_Z12seqcst_fencev:
.LFB668:
	.seh_endprologue
	lock or	QWORD PTR [rsp], 0
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13acquire_fencev
	.def	_Z13acquire_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13acquire_fencev
_Z13acquire_fencev:
.LFB669:
	.seh_endprologue
	ret
	.seh_endproc
	.p2align 4
	.globl	_Z13release_fencev
	.def	_Z13release_fencev;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13release_fencev
_Z13release_fencev:
.LFB670:
	.seh_endprologue
	ret
	.seh_endproc
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB671:
	sub	rsp, 56
	.seh_stackalloc	56
	.seh_endprologue
	call	__main
	mov	DWORD PTR 44[rsp], 1
	mov	eax, DWORD PTR 44[rsp]
	mov	eax, 2
	xchg	eax, DWORD PTR 44[rsp]
	lock or	QWORD PTR [rsp], 0
	mov	eax, DWORD PTR 44[rsp]
	add	rsp, 56
	ret
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
