; Examples/_ch83_map_perf.asm  —— 真实汇编证据（GCC 13.1.0 -O2 -m64 -masm=intel）
; 由 Examples/_ch83_map_asm.cpp 经 `g++ -O2 -std=c++23 -m64 -masm=intel -S` 生成。
; 用途：为 ch83_map.md 附录 E(红黑树 vs flat_map) / H(map vs unordered_map) 提供
;        机器可校验的真实 asm，替换原先"注释式假 asm"。
;
; 关键观察（结合 ch83_map.md 正文实测延迟）：
;   - probe_map_find : 红黑树下降循环 .L60，每轮 2 次指针间接寻址
;                      (QWORD PTR 16[rax]=_M_left, QWORD PTR 24[rax]=_M_right) + 1 次 key 比较
;                      → 随机 key 命中率低，实测 ~670ns/find（L2 miss 主导）
;   - probe_flat_find: std::lower_bound 连续内存二分，循环 .L73 仅 1 次 key 比较/轮
;                      → 缓存友好，实测 ~213ns/find
;   - probe_umap_find: 哈希取模 (div r10) + 桶数组一次访存 + 冲突链遍历
;                      → 通常 1 次访存命中，实测 ~51.6ns/find

	.globl	_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi
	.def	_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi
_Z14probe_map_findRKSt3mapIiiSt4lessIiESaISt4pairIKiiEEEi:
.LFB3277:
	.seh_endprologue
	mov	rax, QWORD PTR 16[rcx]
	lea	r10, 8[rcx]
	test	rax, rax
	je	.L62
	mov	r9, r10
	jmp	.L60
	.p2align 4,,10
	.p2align 3
.L67:
	mov	r9, rax
	mov	rax, r8
	test	rax, rax
	je	.L66
.L60:
	cmp	DWORD PTR 32[rax], edx
	mov	r8, QWORD PTR 16[rax]
	mov	rcx, QWORD PTR 24[rax]
	jge	.L67
	mov	rax, rcx
	test	rax, rax
	jne	.L60
.L66:
	cmp	r10, r9
	je	.L57
	cmp	DWORD PTR 32[r9], edx
	jle	.L61
.L57:
	ret
	.p2align 4,,10
	.p2align 3
.L61:
	mov	eax, DWORD PTR 36[r9]
	ret
	.p2align 4,,10
	.p2align 3
.L62:
	xor	eax, eax
	ret
	.seh_endproc

	.globl	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi
	.def	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi
_Z15probe_flat_findRKSt6vectorISt4pairIiiESaIS1_EEi:
.LFB3281:
	.seh_endprologue
	mov	r10, QWORD PTR 8[rcx]
	mov	r9, QWORD PTR [rcx]
	mov	rcx, r10
	sub	rcx, r9
	mov	rax, rcx
	sar	rax, 3
	test	rcx, rcx
	jg	.L73
	jmp	.L69
	.p2align 4,,10
	.p2align 3
.L70:
	jle	.L75
.L71:
	lea	r9, 8[rcx]
	sub	rax, r8
	sub	rax, 1
	test	rax, rax
	jle	.L69
.L73:
	mov	r8, rax
	sar	r8
	lea	rcx, [r9+r8*8]
	cmp	edx, DWORD PTR [rcx]
	jne	.L70
	mov	r11d, DWORD PTR 4[rcx]
	test	r11d, r11d
	js	.L71
.L75:
	mov	rax, r8
	test	rax, rax
	jg	.L73
.L69:
	xor	eax, eax
	cmp	r10, r9
	je	.L68
	cmp	DWORD PTR [r9], edx
	je	.L79
.L68:
	ret
	.p2align 4,,10
	.p2align 3
.L79:
	mov	eax, DWORD PTR 4[r9]
	ret
	.seh_endproc

	.globl	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi
	.def	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi;	.scl	2;	.type	32;	.endef
	.seh_proc	_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi
_Z15probe_umap_findRKSt13unordered_mapIiiSt4hashIiESt8equal_toIiESaISt4pairIKiiEEEi:
.LFB3291:
	push	rbx
	.seh_pushreg	rbx
	.seh_endprologue
	cmp	QWORD PTR 24[rcx], 0
	mov	r8d, edx
	jne	.L81
	mov	rax, QWORD PTR 16[rcx]
	test	rax, rax
	jne	.L84
.L91:
	xor	eax, eax
.L80:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L94:
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	je	.L80
.L84:
	cmp	DWORD PTR 8[rax], r8d
	jne	.L94
	mov	eax, DWORD PTR 12[rax]
.L96:
	pop	rbx
	ret
	.p2align 4,,10
	.p2align 3
.L81:
	mov	r10, QWORD PTR 8[rcx]
	movsx	rax, edx
	xor	edx, edx
	div	r10
	mov	rax, QWORD PTR [rcx]
	mov	rbx, rdx
	mov	r11, QWORD PTR [rax+rdx*8]
	test	r11, r11
	je	.L91
	mov	rax, QWORD PTR [r11]
	mov	ecx, DWORD PTR 8[rax]
	cmp	r8d, ecx
	je	.L85
.L95:
	mov	r9, QWORD PTR [rax]
	test	r9, r9
	je	.L91
	mov	ecx, DWORD PTR 8[r9]
	xor	edx, edx
	mov	r11, rax
	movsx	rax, ecx
	div	r10
	cmp	rbx, rdx
	jne	.L91
	cmp	r8d, ecx
	mov	rax, r9
	jne	.L95
.L85:
	mov	rax, QWORD PTR [r11]
	test	rax, rax
	je	.L91
	mov	eax, DWORD PTR 12[rax]
	jmp	.L96
	.seh_endproc
