	.file	"_ch15_profiling.cpp"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	_Z1fv
	.def	_Z1fv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z1fv
_Z1fv:
.LFB5829:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	_ZNSt6chrono3_V212steady_clock3nowEv
	add	rsp, 40
	ret
	.seh_endproc
	.ident	"GCC: (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0"
	.def	_ZNSt6chrono3_V212steady_clock3nowEv;	.scl	2;	.type	32;	.endef
