; Examples/_ch03_perf.asm  —— 真实汇编证据（GCC 13.1.0 -O2 -m64 -masm=intel）
; 由 Examples/_ch03_perf.cpp 经 `g++ -O2 -std=c++23 -m64 -masm=intel -S` 生成。
; 用途：为 ch03_cpp98_03.md 附录⑫(虚函数) / ⑲(RTTI) 提供机器可校验的真实 asm，
;        替换原先"注释式假 asm"。
;
; 关键观察（结合 ch03 正文实测延迟，来源 Examples/_ch03_perf.out）：
;   - virt_call : vtable 取址 + 1 次间接跳转，2 条指令 → 实测 ~2.6ns/find
;   - get_tname : 经 vtable 前 8 字节取 type_info 指针 → 实测 ~1.8ns
;   - dyn_down  : 直接 jmp __dynamic_cast 运行时（类型匹配时极廉价）→ 实测 ~6.2ns，
;                 绝非旧说 ~50-200ns

	.globl	_Z9virt_callR4Basei
	.def	_Z9virt_callR4Basei;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9virt_callR4Basei
_Z9virt_callR4Basei:
.LFB13716:
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]          ; 取 vtable 指针
	rex.W jmp	[QWORD PTR [rax]]        ; 经 vtable[0] 间接调用（虚分发）
	.seh_endproc

	.globl	_Z9get_tnameRK4Base
	.def	_Z9get_tnameRK4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z9get_tnameRK4Base
_Z9get_tnameRK4Base:
.LFB13717:
	.seh_endprologue
	xor	edx, edx
	mov	rax, QWORD PTR [rcx]
	mov	rax, QWORD PTR -8[rax]        ; vtable 前 8 字节 = type_info 指针
	mov	rax, QWORD PTR 8[rax]
	cmp	BYTE PTR [rax], 42
	sete	dl
	add	rax, rdx
	ret
	.seh_endproc

	.globl	_Z8dyn_downR4Base
	.def	_Z8dyn_downR4Base;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z8dyn_downR4Base
_Z8dyn_downR4Base:
.LFB13718:
	.seh_endprologue
	lea	r8, _ZTI3Der[rip]             ; 目标类型信息 Der
	xor	r9d, r9d
	lea	rdx, _ZTI4Base[rip]           ; 源类型信息 Base
	jmp	__dynamic_cast                ; 运行时类型检查（匹配时极廉价）
	.seh_endproc
