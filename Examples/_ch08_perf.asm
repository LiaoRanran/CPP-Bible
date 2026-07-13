; Examples/_ch08_perf.asm  —— 真实汇编证据（GCC 13.1.0 -O2 -m64 -masm=intel）
; 由 Examples/_ch08_perf.cpp 经 `g++ -O2 -std=c++23 -m64 -masm=intel -S` 生成。
; 用途：为 ch08_cpp23.md 附录 D(expected vs exception) 提供机器可校验的真实 asm，
;        替换原先"注释式假 asm"（~100ns / ~1ns / 100x 无真实产物）。
;
; 关键观察（结合 ch08 正文实测延迟，来源 Examples/_ch08_perf.out）：
;   - throw_path : call __cxa_allocate_exception + call __cxa_throw + __cxa_begin_catch/
;     __cxa_end_catch + _Unwind_Resume 栈展开 → 实测 2192ns(2.19µs)
;   - expected_path : 编译器直接优化为 `mov eax,1; ret`（零异常机制）→ 实测 0.43ns
;   - 失败路径 expected 比 exception 快 ~5085x（旧估 100x 严重偏低）

	.globl	_Z10throw_pathv
	.def	_Z10throw_pathv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z10throw_pathv
_Z10throw_pathv:
	mov	eax, DWORD PTR _ZL9g_trigger[rip]
	test	eax, eax
	jne	.L17
	add	rsp, 56
	ret
.L17:
	mov	ecx, 4
	call	__cxa_allocate_exception      ; 分配异常对象
	mov	rdx, QWORD PTR .refptr._ZTIi[rip]
	xor	r8d, r8d
	mov	rcx, rax
	mov	DWORD PTR [rax], 1
	call	__cxa_throw                   ; 抛异常（触发栈展开）
.L13:
	sub	rdx, 1
	mov	rcx, rax
	jne	.L18
	call	__cxa_begin_catch             ; 进入 catch
	mov	eax, DWORD PTR [rax]
	mov	DWORD PTR 44[rsp], eax
	call	__cxa_end_catch               ; 离开 catch
	mov	eax, DWORD PTR 44[rsp]
	jmp	.L9
.L18:
	call	_Unwind_Resume                 ; 栈展开（失败路径核心成本）
	.seh_endproc

	.globl	_Z13expected_pathv
	.def	_Z13expected_pathv;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z13expected_pathv
_Z13expected_pathv:
	mov	eax, 1                          ; 直接返回错误值，无异常机制
	ret
	.seh_endproc
