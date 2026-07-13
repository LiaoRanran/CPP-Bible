
_ch156_app_nolto.exe:     file format pei-x86-64


Disassembly of section .text:

0000000140001000 <__mingw_invalidParameterHandler>:
   140001000:	c3                   	ret
   140001001:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   140001008:	00 00 00 00 
   14000100c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000140001010 <pre_c_init>:
   140001010:	48 83 ec 28          	sub    rsp,0x28
   140001014:	48 8b 05 c5 33 00 00 	mov    rax,QWORD PTR [rip+0x33c5]        # 1400043e0 <.refptr.__mingw_initltsdrot_force>
   14000101b:	31 c9                	xor    ecx,ecx
   14000101d:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001023:	48 8b 05 c6 33 00 00 	mov    rax,QWORD PTR [rip+0x33c6]        # 1400043f0 <.refptr.__mingw_initltsdyn_force>
   14000102a:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001030:	48 8b 05 c9 33 00 00 	mov    rax,QWORD PTR [rip+0x33c9]        # 140004400 <.refptr.__mingw_initltssuo_force>
   140001037:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000103d:	48 8b 05 4c 33 00 00 	mov    rax,QWORD PTR [rip+0x334c]        # 140004390 <.refptr.__image_base__>
   140001044:	66 81 38 4d 5a       	cmp    WORD PTR [rax],0x5a4d
   140001049:	75 0f                	jne    14000105a <pre_c_init+0x4a>
   14000104b:	48 63 50 3c          	movsxd rdx,DWORD PTR [rax+0x3c]
   14000104f:	48 01 d0             	add    rax,rdx
   140001052:	81 38 50 45 00 00    	cmp    DWORD PTR [rax],0x4550
   140001058:	74 66                	je     1400010c0 <pre_c_init+0xb0>
   14000105a:	48 8b 05 6f 33 00 00 	mov    rax,QWORD PTR [rip+0x336f]        # 1400043d0 <.refptr.__mingw_app_type>
   140001061:	89 0d a5 5f 00 00    	mov    DWORD PTR [rip+0x5fa5],ecx        # 14000700c <managedapp>
   140001067:	8b 00                	mov    eax,DWORD PTR [rax]
   140001069:	85 c0                	test   eax,eax
   14000106b:	74 43                	je     1400010b0 <pre_c_init+0xa0>
   14000106d:	b9 02 00 00 00       	mov    ecx,0x2
   140001072:	e8 01 15 00 00       	call   140002578 <__set_app_type>
   140001077:	e8 84 14 00 00       	call   140002500 <__p__fmode>
   14000107c:	48 8b 15 1d 34 00 00 	mov    rdx,QWORD PTR [rip+0x341d]        # 1400044a0 <.refptr._fmode>
   140001083:	8b 12                	mov    edx,DWORD PTR [rdx]
   140001085:	89 10                	mov    DWORD PTR [rax],edx
   140001087:	e8 84 14 00 00       	call   140002510 <__p__commode>
   14000108c:	48 8b 15 ed 33 00 00 	mov    rdx,QWORD PTR [rip+0x33ed]        # 140004480 <.refptr._commode>
   140001093:	8b 12                	mov    edx,DWORD PTR [rdx]
   140001095:	89 10                	mov    DWORD PTR [rax],edx
   140001097:	e8 94 04 00 00       	call   140001530 <_setargv>
   14000109c:	48 8b 05 9d 32 00 00 	mov    rax,QWORD PTR [rip+0x329d]        # 140004340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   1400010a3:	83 38 01             	cmp    DWORD PTR [rax],0x1
   1400010a6:	74 50                	je     1400010f8 <pre_c_init+0xe8>
   1400010a8:	31 c0                	xor    eax,eax
   1400010aa:	48 83 c4 28          	add    rsp,0x28
   1400010ae:	c3                   	ret
   1400010af:	90                   	nop
   1400010b0:	b9 01 00 00 00       	mov    ecx,0x1
   1400010b5:	e8 be 14 00 00       	call   140002578 <__set_app_type>
   1400010ba:	eb bb                	jmp    140001077 <pre_c_init+0x67>
   1400010bc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   1400010c0:	0f b7 50 18          	movzx  edx,WORD PTR [rax+0x18]
   1400010c4:	66 81 fa 0b 01       	cmp    dx,0x10b
   1400010c9:	74 45                	je     140001110 <pre_c_init+0x100>
   1400010cb:	66 81 fa 0b 02       	cmp    dx,0x20b
   1400010d0:	75 88                	jne    14000105a <pre_c_init+0x4a>
   1400010d2:	83 b8 84 00 00 00 0e 	cmp    DWORD PTR [rax+0x84],0xe
   1400010d9:	0f 86 7b ff ff ff    	jbe    14000105a <pre_c_init+0x4a>
   1400010df:	8b 90 f8 00 00 00    	mov    edx,DWORD PTR [rax+0xf8]
   1400010e5:	31 c9                	xor    ecx,ecx
   1400010e7:	85 d2                	test   edx,edx
   1400010e9:	0f 95 c1             	setne  cl
   1400010ec:	e9 69 ff ff ff       	jmp    14000105a <pre_c_init+0x4a>
   1400010f1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400010f8:	48 8b 0d c1 33 00 00 	mov    rcx,QWORD PTR [rip+0x33c1]        # 1400044c0 <.refptr._matherr>
   1400010ff:	e8 9c 0b 00 00       	call   140001ca0 <__mingw_setusermatherr>
   140001104:	31 c0                	xor    eax,eax
   140001106:	48 83 c4 28          	add    rsp,0x28
   14000110a:	c3                   	ret
   14000110b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001110:	83 78 74 0e          	cmp    DWORD PTR [rax+0x74],0xe
   140001114:	0f 86 40 ff ff ff    	jbe    14000105a <pre_c_init+0x4a>
   14000111a:	44 8b 80 e8 00 00 00 	mov    r8d,DWORD PTR [rax+0xe8]
   140001121:	31 c9                	xor    ecx,ecx
   140001123:	45 85 c0             	test   r8d,r8d
   140001126:	0f 95 c1             	setne  cl
   140001129:	e9 2c ff ff ff       	jmp    14000105a <pre_c_init+0x4a>
   14000112e:	66 90                	xchg   ax,ax

0000000140001130 <pre_cpp_init>:
   140001130:	48 83 ec 38          	sub    rsp,0x38
   140001134:	48 8b 05 95 33 00 00 	mov    rax,QWORD PTR [rip+0x3395]        # 1400044d0 <.refptr._newmode>
   14000113b:	4c 8d 05 d6 5e 00 00 	lea    r8,[rip+0x5ed6]        # 140007018 <envp>
   140001142:	48 8d 15 d7 5e 00 00 	lea    rdx,[rip+0x5ed7]        # 140007020 <argv>
   140001149:	48 8d 0d d8 5e 00 00 	lea    rcx,[rip+0x5ed8]        # 140007028 <argc>
   140001150:	8b 00                	mov    eax,DWORD PTR [rax]
   140001152:	89 05 ac 5e 00 00    	mov    DWORD PTR [rip+0x5eac],eax        # 140007004 <startinfo>
   140001158:	48 8b 05 31 33 00 00 	mov    rax,QWORD PTR [rip+0x3331]        # 140004490 <.refptr._dowildcard>
   14000115f:	44 8b 08             	mov    r9d,DWORD PTR [rax]
   140001162:	48 8d 05 9b 5e 00 00 	lea    rax,[rip+0x5e9b]        # 140007004 <startinfo>
   140001169:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
   14000116e:	e8 f5 13 00 00       	call   140002568 <__getmainargs>
   140001173:	90                   	nop
   140001174:	48 83 c4 38          	add    rsp,0x38
   140001178:	c3                   	ret
   140001179:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000140001180 <__tmainCRTStartup>:
   140001180:	41 54                	push   r12
   140001182:	55                   	push   rbp
   140001183:	57                   	push   rdi
   140001184:	56                   	push   rsi
   140001185:	53                   	push   rbx
   140001186:	48 83 ec 20          	sub    rsp,0x20
   14000118a:	48 8b 1d 8f 32 00 00 	mov    rbx,QWORD PTR [rip+0x328f]        # 140004420 <.refptr.__native_startup_lock>
   140001191:	31 ff                	xor    edi,edi
   140001193:	65 48 8b 04 25 30 00 	mov    rax,QWORD PTR gs:0x30
   14000119a:	00 00 
   14000119c:	48 8b 2d e9 6f 00 00 	mov    rbp,QWORD PTR [rip+0x6fe9]        # 14000818c <__imp_Sleep>
   1400011a3:	48 8b 70 08          	mov    rsi,QWORD PTR [rax+0x8]
   1400011a7:	eb 17                	jmp    1400011c0 <__tmainCRTStartup+0x40>
   1400011a9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400011b0:	48 39 c6             	cmp    rsi,rax
   1400011b3:	0f 84 67 01 00 00    	je     140001320 <__tmainCRTStartup+0x1a0>
   1400011b9:	b9 e8 03 00 00       	mov    ecx,0x3e8
   1400011be:	ff d5                	call   rbp
   1400011c0:	48 89 f8             	mov    rax,rdi
   1400011c3:	f0 48 0f b1 33       	lock cmpxchg QWORD PTR [rbx],rsi
   1400011c8:	48 85 c0             	test   rax,rax
   1400011cb:	75 e3                	jne    1400011b0 <__tmainCRTStartup+0x30>
   1400011cd:	48 8b 35 5c 32 00 00 	mov    rsi,QWORD PTR [rip+0x325c]        # 140004430 <.refptr.__native_startup_state>
   1400011d4:	31 ff                	xor    edi,edi
   1400011d6:	8b 06                	mov    eax,DWORD PTR [rsi]
   1400011d8:	83 f8 01             	cmp    eax,0x1
   1400011db:	0f 84 56 01 00 00    	je     140001337 <__tmainCRTStartup+0x1b7>
   1400011e1:	8b 06                	mov    eax,DWORD PTR [rsi]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	0f 84 b5 01 00 00    	je     1400013a0 <__tmainCRTStartup+0x220>
   1400011eb:	c7 05 13 5e 00 00 01 	mov    DWORD PTR [rip+0x5e13],0x1        # 140007008 <has_cctor>
   1400011f2:	00 00 00 
   1400011f5:	8b 06                	mov    eax,DWORD PTR [rsi]
   1400011f7:	83 f8 01             	cmp    eax,0x1
   1400011fa:	0f 84 4c 01 00 00    	je     14000134c <__tmainCRTStartup+0x1cc>
   140001200:	85 ff                	test   edi,edi
   140001202:	0f 84 65 01 00 00    	je     14000136d <__tmainCRTStartup+0x1ed>
   140001208:	48 8b 05 71 31 00 00 	mov    rax,QWORD PTR [rip+0x3171]        # 140004380 <.refptr.__dyn_tls_init_callback>
   14000120f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001212:	48 85 c0             	test   rax,rax
   140001215:	74 0c                	je     140001223 <__tmainCRTStartup+0xa3>
   140001217:	45 31 c0             	xor    r8d,r8d
   14000121a:	ba 02 00 00 00       	mov    edx,0x2
   14000121f:	31 c9                	xor    ecx,ecx
   140001221:	ff d0                	call   rax
   140001223:	e8 d8 06 00 00       	call   140001900 <_pei386_runtime_relocator>
   140001228:	48 8b 0d 81 32 00 00 	mov    rcx,QWORD PTR [rip+0x3281]        # 1400044b0 <.refptr._gnu_exception_handler>
   14000122f:	ff 15 4f 6f 00 00    	call   QWORD PTR [rip+0x6f4f]        # 140008184 <__imp_SetUnhandledExceptionFilter>
   140001235:	48 8b 15 d4 31 00 00 	mov    rdx,QWORD PTR [rip+0x31d4]        # 140004410 <.refptr.__mingw_oldexcpt_handler>
   14000123c:	48 8d 0d bd fd ff ff 	lea    rcx,[rip+0xfffffffffffffdbd]        # 140001000 <__mingw_invalidParameterHandler>
   140001243:	48 89 02             	mov    QWORD PTR [rdx],rax
   140001246:	e8 e5 12 00 00       	call   140002530 <_set_invalid_parameter_handler>
   14000124b:	e8 c0 04 00 00       	call   140001710 <_fpreset>
   140001250:	8b 1d d2 5d 00 00    	mov    ebx,DWORD PTR [rip+0x5dd2]        # 140007028 <argc>
   140001256:	8d 7b 01             	lea    edi,[rbx+0x1]
   140001259:	48 63 ff             	movsxd rdi,edi
   14000125c:	48 c1 e7 03          	shl    rdi,0x3
   140001260:	48 89 f9             	mov    rcx,rdi
   140001263:	e8 70 13 00 00       	call   1400025d8 <malloc>
   140001268:	85 db                	test   ebx,ebx
   14000126a:	48 8b 2d af 5d 00 00 	mov    rbp,QWORD PTR [rip+0x5daf]        # 140007020 <argv>
   140001271:	49 89 c4             	mov    r12,rax
   140001274:	0f 8e 46 01 00 00    	jle    1400013c0 <__tmainCRTStartup+0x240>
   14000127a:	48 83 ef 08          	sub    rdi,0x8
   14000127e:	31 db                	xor    ebx,ebx
   140001280:	48 8b 4c 1d 00       	mov    rcx,QWORD PTR [rbp+rbx*1+0x0]
   140001285:	e8 66 13 00 00       	call   1400025f0 <strlen>
   14000128a:	48 8d 70 01          	lea    rsi,[rax+0x1]
   14000128e:	48 89 f1             	mov    rcx,rsi
   140001291:	e8 42 13 00 00       	call   1400025d8 <malloc>
   140001296:	49 89 f0             	mov    r8,rsi
   140001299:	49 89 04 1c          	mov    QWORD PTR [r12+rbx*1],rax
   14000129d:	48 8b 54 1d 00       	mov    rdx,QWORD PTR [rbp+rbx*1+0x0]
   1400012a2:	48 89 c1             	mov    rcx,rax
   1400012a5:	48 83 c3 08          	add    rbx,0x8
   1400012a9:	e8 32 13 00 00       	call   1400025e0 <memcpy>
   1400012ae:	48 39 df             	cmp    rdi,rbx
   1400012b1:	75 cd                	jne    140001280 <__tmainCRTStartup+0x100>
   1400012b3:	4c 01 e7             	add    rdi,r12
   1400012b6:	48 c7 07 00 00 00 00 	mov    QWORD PTR [rdi],0x0
   1400012bd:	4c 89 25 5c 5d 00 00 	mov    QWORD PTR [rip+0x5d5c],r12        # 140007020 <argv>
   1400012c4:	e8 47 02 00 00       	call   140001510 <__main>
   1400012c9:	48 8b 05 d0 30 00 00 	mov    rax,QWORD PTR [rip+0x30d0]        # 1400043a0 <.refptr.__imp___initenv>
   1400012d0:	4c 8b 05 41 5d 00 00 	mov    r8,QWORD PTR [rip+0x5d41]        # 140007018 <envp>
   1400012d7:	8b 0d 4b 5d 00 00    	mov    ecx,DWORD PTR [rip+0x5d4b]        # 140007028 <argc>
   1400012dd:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400012e0:	4c 89 00             	mov    QWORD PTR [rax],r8
   1400012e3:	48 8b 15 36 5d 00 00 	mov    rdx,QWORD PTR [rip+0x5d36]        # 140007020 <argv>
   1400012ea:	e8 71 13 00 00       	call   140002660 <main>
   1400012ef:	8b 0d 17 5d 00 00    	mov    ecx,DWORD PTR [rip+0x5d17]        # 14000700c <managedapp>
   1400012f5:	89 05 15 5d 00 00    	mov    DWORD PTR [rip+0x5d15],eax        # 140007010 <mainret>
   1400012fb:	85 c9                	test   ecx,ecx
   1400012fd:	0f 84 c5 00 00 00    	je     1400013c8 <__tmainCRTStartup+0x248>
   140001303:	8b 15 ff 5c 00 00    	mov    edx,DWORD PTR [rip+0x5cff]        # 140007008 <has_cctor>
   140001309:	85 d2                	test   edx,edx
   14000130b:	74 73                	je     140001380 <__tmainCRTStartup+0x200>
   14000130d:	48 83 c4 20          	add    rsp,0x20
   140001311:	5b                   	pop    rbx
   140001312:	5e                   	pop    rsi
   140001313:	5f                   	pop    rdi
   140001314:	5d                   	pop    rbp
   140001315:	41 5c                	pop    r12
   140001317:	c3                   	ret
   140001318:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000131f:	00 
   140001320:	48 8b 35 09 31 00 00 	mov    rsi,QWORD PTR [rip+0x3109]        # 140004430 <.refptr.__native_startup_state>
   140001327:	bf 01 00 00 00       	mov    edi,0x1
   14000132c:	8b 06                	mov    eax,DWORD PTR [rsi]
   14000132e:	83 f8 01             	cmp    eax,0x1
   140001331:	0f 85 aa fe ff ff    	jne    1400011e1 <__tmainCRTStartup+0x61>
   140001337:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000133c:	e8 47 12 00 00       	call   140002588 <_amsg_exit>
   140001341:	8b 06                	mov    eax,DWORD PTR [rsi]
   140001343:	83 f8 01             	cmp    eax,0x1
   140001346:	0f 85 b4 fe ff ff    	jne    140001200 <__tmainCRTStartup+0x80>
   14000134c:	48 8b 15 fd 30 00 00 	mov    rdx,QWORD PTR [rip+0x30fd]        # 140004450 <.refptr.__xc_z>
   140001353:	48 8b 0d e6 30 00 00 	mov    rcx,QWORD PTR [rip+0x30e6]        # 140004440 <.refptr.__xc_a>
   14000135a:	e8 39 12 00 00       	call   140002598 <_initterm>
   14000135f:	85 ff                	test   edi,edi
   140001361:	c7 06 02 00 00 00    	mov    DWORD PTR [rsi],0x2
   140001367:	0f 85 9b fe ff ff    	jne    140001208 <__tmainCRTStartup+0x88>
   14000136d:	31 c0                	xor    eax,eax
   14000136f:	48 87 03             	xchg   QWORD PTR [rbx],rax
   140001372:	e9 91 fe ff ff       	jmp    140001208 <__tmainCRTStartup+0x88>
   140001377:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000137e:	00 00 
   140001380:	e8 0b 12 00 00       	call   140002590 <_cexit>
   140001385:	8b 05 85 5c 00 00    	mov    eax,DWORD PTR [rip+0x5c85]        # 140007010 <mainret>
   14000138b:	48 83 c4 20          	add    rsp,0x20
   14000138f:	5b                   	pop    rbx
   140001390:	5e                   	pop    rsi
   140001391:	5f                   	pop    rdi
   140001392:	5d                   	pop    rbp
   140001393:	41 5c                	pop    r12
   140001395:	c3                   	ret
   140001396:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000139d:	00 00 00 
   1400013a0:	48 8b 15 c9 30 00 00 	mov    rdx,QWORD PTR [rip+0x30c9]        # 140004470 <.refptr.__xi_z>
   1400013a7:	c7 06 01 00 00 00    	mov    DWORD PTR [rsi],0x1
   1400013ad:	48 8b 0d ac 30 00 00 	mov    rcx,QWORD PTR [rip+0x30ac]        # 140004460 <.refptr.__xi_a>
   1400013b4:	e8 df 11 00 00       	call   140002598 <_initterm>
   1400013b9:	e9 37 fe ff ff       	jmp    1400011f5 <__tmainCRTStartup+0x75>
   1400013be:	66 90                	xchg   ax,ax
   1400013c0:	48 89 c7             	mov    rdi,rax
   1400013c3:	e9 ee fe ff ff       	jmp    1400012b6 <__tmainCRTStartup+0x136>
   1400013c8:	89 c1                	mov    ecx,eax
   1400013ca:	e8 e9 11 00 00       	call   1400025b8 <exit>
   1400013cf:	90                   	nop

00000001400013d0 <WinMainCRTStartup>:
   1400013d0:	48 83 ec 28          	sub    rsp,0x28

00000001400013d4 <.l_startw>:
   1400013d4:	48 8b 05 f5 2f 00 00 	mov    rax,QWORD PTR [rip+0x2ff5]        # 1400043d0 <.refptr.__mingw_app_type>
   1400013db:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   1400013e1:	e8 9a fd ff ff       	call   140001180 <__tmainCRTStartup>
   1400013e6:	90                   	nop

00000001400013e7 <.l_endw>:
   1400013e7:	90                   	nop
   1400013e8:	48 83 c4 28          	add    rsp,0x28
   1400013ec:	c3                   	ret
   1400013ed:	0f 1f 00             	nop    DWORD PTR [rax]

00000001400013f0 <mainCRTStartup>:
   1400013f0:	48 83 ec 28          	sub    rsp,0x28

00000001400013f4 <.l_start>:
   1400013f4:	48 8b 05 d5 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd5]        # 1400043d0 <.refptr.__mingw_app_type>
   1400013fb:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001401:	e8 7a fd ff ff       	call   140001180 <__tmainCRTStartup>
   140001406:	90                   	nop

0000000140001407 <.l_end>:
   140001407:	90                   	nop
   140001408:	48 83 c4 28          	add    rsp,0x28
   14000140c:	c3                   	ret
   14000140d:	0f 1f 00             	nop    DWORD PTR [rax]

0000000140001410 <atexit>:
   140001410:	48 83 ec 28          	sub    rsp,0x28
   140001414:	e8 87 11 00 00       	call   1400025a0 <_onexit>
   140001419:	48 83 f8 01          	cmp    rax,0x1
   14000141d:	19 c0                	sbb    eax,eax
   14000141f:	48 83 c4 28          	add    rsp,0x28
   140001423:	c3                   	ret
   140001424:	90                   	nop
   140001425:	90                   	nop
   140001426:	90                   	nop
   140001427:	90                   	nop
   140001428:	90                   	nop
   140001429:	90                   	nop
   14000142a:	90                   	nop
   14000142b:	90                   	nop
   14000142c:	90                   	nop
   14000142d:	90                   	nop
   14000142e:	90                   	nop
   14000142f:	90                   	nop

0000000140001430 <__gcc_register_frame>:
   140001430:	48 8d 0d 09 00 00 00 	lea    rcx,[rip+0x9]        # 140001440 <__gcc_deregister_frame>
   140001437:	e9 d4 ff ff ff       	jmp    140001410 <atexit>
   14000143c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000140001440 <__gcc_deregister_frame>:
   140001440:	c3                   	ret
   140001441:	90                   	nop
   140001442:	90                   	nop
   140001443:	90                   	nop
   140001444:	90                   	nop
   140001445:	90                   	nop
   140001446:	90                   	nop
   140001447:	90                   	nop
   140001448:	90                   	nop
   140001449:	90                   	nop
   14000144a:	90                   	nop
   14000144b:	90                   	nop
   14000144c:	90                   	nop
   14000144d:	90                   	nop
   14000144e:	90                   	nop
   14000144f:	90                   	nop

0000000140001450 <_Z7computei>:
   140001450:	0f af c9             	imul   ecx,ecx
   140001453:	8d 41 01             	lea    eax,[rcx+0x1]
   140001456:	c3                   	ret
   140001457:	90                   	nop
   140001458:	90                   	nop
   140001459:	90                   	nop
   14000145a:	90                   	nop
   14000145b:	90                   	nop
   14000145c:	90                   	nop
   14000145d:	90                   	nop
   14000145e:	90                   	nop
   14000145f:	90                   	nop

0000000140001460 <__do_global_dtors>:
   140001460:	48 83 ec 28          	sub    rsp,0x28
   140001464:	48 8b 05 95 1b 00 00 	mov    rax,QWORD PTR [rip+0x1b95]        # 140003000 <__data_start__>
   14000146b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000146e:	48 85 c0             	test   rax,rax
   140001471:	74 22                	je     140001495 <__do_global_dtors+0x35>
   140001473:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001478:	ff d0                	call   rax
   14000147a:	48 8b 05 7f 1b 00 00 	mov    rax,QWORD PTR [rip+0x1b7f]        # 140003000 <__data_start__>
   140001481:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140001485:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001489:	48 89 15 70 1b 00 00 	mov    QWORD PTR [rip+0x1b70],rdx        # 140003000 <__data_start__>
   140001490:	48 85 c0             	test   rax,rax
   140001493:	75 e3                	jne    140001478 <__do_global_dtors+0x18>
   140001495:	48 83 c4 28          	add    rsp,0x28
   140001499:	c3                   	ret
   14000149a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

00000001400014a0 <__do_global_ctors>:
   1400014a0:	56                   	push   rsi
   1400014a1:	53                   	push   rbx
   1400014a2:	48 83 ec 28          	sub    rsp,0x28
   1400014a6:	48 8b 15 a3 2e 00 00 	mov    rdx,QWORD PTR [rip+0x2ea3]        # 140004350 <.refptr.__CTOR_LIST__>
   1400014ad:	48 8b 02             	mov    rax,QWORD PTR [rdx]
   1400014b0:	83 f8 ff             	cmp    eax,0xffffffff
   1400014b3:	89 c1                	mov    ecx,eax
   1400014b5:	74 39                	je     1400014f0 <__do_global_ctors+0x50>
   1400014b7:	85 c9                	test   ecx,ecx
   1400014b9:	74 20                	je     1400014db <__do_global_ctors+0x3b>
   1400014bb:	89 c8                	mov    eax,ecx
   1400014bd:	83 e9 01             	sub    ecx,0x1
   1400014c0:	48 8d 1c c2          	lea    rbx,[rdx+rax*8]
   1400014c4:	48 29 c8             	sub    rax,rcx
   1400014c7:	48 8d 74 c2 f8       	lea    rsi,[rdx+rax*8-0x8]
   1400014cc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   1400014d0:	ff 13                	call   QWORD PTR [rbx]
   1400014d2:	48 83 eb 08          	sub    rbx,0x8
   1400014d6:	48 39 f3             	cmp    rbx,rsi
   1400014d9:	75 f5                	jne    1400014d0 <__do_global_ctors+0x30>
   1400014db:	48 8d 0d 7e ff ff ff 	lea    rcx,[rip+0xffffffffffffff7e]        # 140001460 <__do_global_dtors>
   1400014e2:	48 83 c4 28          	add    rsp,0x28
   1400014e6:	5b                   	pop    rbx
   1400014e7:	5e                   	pop    rsi
   1400014e8:	e9 23 ff ff ff       	jmp    140001410 <atexit>
   1400014ed:	0f 1f 00             	nop    DWORD PTR [rax]
   1400014f0:	31 c0                	xor    eax,eax
   1400014f2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
   1400014f8:	44 8d 40 01          	lea    r8d,[rax+0x1]
   1400014fc:	89 c1                	mov    ecx,eax
   1400014fe:	4a 83 3c c2 00       	cmp    QWORD PTR [rdx+r8*8],0x0
   140001503:	4c 89 c0             	mov    rax,r8
   140001506:	75 f0                	jne    1400014f8 <__do_global_ctors+0x58>
   140001508:	eb ad                	jmp    1400014b7 <__do_global_ctors+0x17>
   14000150a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000140001510 <__main>:
   140001510:	8b 05 1a 5b 00 00    	mov    eax,DWORD PTR [rip+0x5b1a]        # 140007030 <initialized>
   140001516:	85 c0                	test   eax,eax
   140001518:	74 06                	je     140001520 <__main+0x10>
   14000151a:	c3                   	ret
   14000151b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001520:	c7 05 06 5b 00 00 01 	mov    DWORD PTR [rip+0x5b06],0x1        # 140007030 <initialized>
   140001527:	00 00 00 
   14000152a:	e9 71 ff ff ff       	jmp    1400014a0 <__do_global_ctors>
   14000152f:	90                   	nop

0000000140001530 <_setargv>:
   140001530:	31 c0                	xor    eax,eax
   140001532:	c3                   	ret
   140001533:	90                   	nop
   140001534:	90                   	nop
   140001535:	90                   	nop
   140001536:	90                   	nop
   140001537:	90                   	nop
   140001538:	90                   	nop
   140001539:	90                   	nop
   14000153a:	90                   	nop
   14000153b:	90                   	nop
   14000153c:	90                   	nop
   14000153d:	90                   	nop
   14000153e:	90                   	nop
   14000153f:	90                   	nop

0000000140001540 <__dyn_tls_dtor>:
   140001540:	48 83 ec 28          	sub    rsp,0x28
   140001544:	83 fa 03             	cmp    edx,0x3
   140001547:	74 17                	je     140001560 <__dyn_tls_dtor+0x20>
   140001549:	85 d2                	test   edx,edx
   14000154b:	74 13                	je     140001560 <__dyn_tls_dtor+0x20>
   14000154d:	b8 01 00 00 00       	mov    eax,0x1
   140001552:	48 83 c4 28          	add    rsp,0x28
   140001556:	c3                   	ret
   140001557:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000155e:	00 00 
   140001560:	e8 5b 0a 00 00       	call   140001fc0 <__mingw_TLScallback>
   140001565:	b8 01 00 00 00       	mov    eax,0x1
   14000156a:	48 83 c4 28          	add    rsp,0x28
   14000156e:	c3                   	ret
   14000156f:	90                   	nop

0000000140001570 <__dyn_tls_init>:
   140001570:	56                   	push   rsi
   140001571:	53                   	push   rbx
   140001572:	48 83 ec 28          	sub    rsp,0x28
   140001576:	48 8b 05 b3 2d 00 00 	mov    rax,QWORD PTR [rip+0x2db3]        # 140004330 <.refptr._CRT_MT>
   14000157d:	83 38 02             	cmp    DWORD PTR [rax],0x2
   140001580:	74 06                	je     140001588 <__dyn_tls_init+0x18>
   140001582:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001588:	83 fa 02             	cmp    edx,0x2
   14000158b:	74 13                	je     1400015a0 <__dyn_tls_init+0x30>
   14000158d:	83 fa 01             	cmp    edx,0x1
   140001590:	74 4e                	je     1400015e0 <__dyn_tls_init+0x70>
   140001592:	b8 01 00 00 00       	mov    eax,0x1
   140001597:	48 83 c4 28          	add    rsp,0x28
   14000159b:	5b                   	pop    rbx
   14000159c:	5e                   	pop    rsi
   14000159d:	c3                   	ret
   14000159e:	66 90                	xchg   ax,ax
   1400015a0:	48 8d 1d b1 7a 00 00 	lea    rbx,[rip+0x7ab1]        # 140009058 <__xd_z>
   1400015a7:	48 8d 35 aa 7a 00 00 	lea    rsi,[rip+0x7aaa]        # 140009058 <__xd_z>
   1400015ae:	48 39 de             	cmp    rsi,rbx
   1400015b1:	74 df                	je     140001592 <__dyn_tls_init+0x22>
   1400015b3:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   1400015b8:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   1400015bb:	48 85 c0             	test   rax,rax
   1400015be:	74 02                	je     1400015c2 <__dyn_tls_init+0x52>
   1400015c0:	ff d0                	call   rax
   1400015c2:	48 83 c3 08          	add    rbx,0x8
   1400015c6:	48 39 de             	cmp    rsi,rbx
   1400015c9:	75 ed                	jne    1400015b8 <__dyn_tls_init+0x48>
   1400015cb:	b8 01 00 00 00       	mov    eax,0x1
   1400015d0:	48 83 c4 28          	add    rsp,0x28
   1400015d4:	5b                   	pop    rbx
   1400015d5:	5e                   	pop    rsi
   1400015d6:	c3                   	ret
   1400015d7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   1400015de:	00 00 
   1400015e0:	e8 db 09 00 00       	call   140001fc0 <__mingw_TLScallback>
   1400015e5:	b8 01 00 00 00       	mov    eax,0x1
   1400015ea:	48 83 c4 28          	add    rsp,0x28
   1400015ee:	5b                   	pop    rbx
   1400015ef:	5e                   	pop    rsi
   1400015f0:	c3                   	ret
   1400015f1:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   1400015f8:	00 00 00 00 
   1400015fc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000140001600 <__tlregdtor>:
   140001600:	31 c0                	xor    eax,eax
   140001602:	c3                   	ret
   140001603:	90                   	nop
   140001604:	90                   	nop
   140001605:	90                   	nop
   140001606:	90                   	nop
   140001607:	90                   	nop
   140001608:	90                   	nop
   140001609:	90                   	nop
   14000160a:	90                   	nop
   14000160b:	90                   	nop
   14000160c:	90                   	nop
   14000160d:	90                   	nop
   14000160e:	90                   	nop
   14000160f:	90                   	nop

0000000140001610 <_matherr>:
   140001610:	56                   	push   rsi
   140001611:	53                   	push   rbx
   140001612:	48 83 ec 78          	sub    rsp,0x78
   140001616:	0f 29 74 24 40       	movaps XMMWORD PTR [rsp+0x40],xmm6
   14000161b:	0f 29 7c 24 50       	movaps XMMWORD PTR [rsp+0x50],xmm7
   140001620:	44 0f 29 44 24 60    	movaps XMMWORD PTR [rsp+0x60],xmm8
   140001626:	83 39 06             	cmp    DWORD PTR [rcx],0x6
   140001629:	0f 87 cd 00 00 00    	ja     1400016fc <_matherr+0xec>
   14000162f:	8b 01                	mov    eax,DWORD PTR [rcx]
   140001631:	48 8d 15 4c 2b 00 00 	lea    rdx,[rip+0x2b4c]        # 140004184 <.rdata+0x124>
   140001638:	48 63 04 82          	movsxd rax,DWORD PTR [rdx+rax*4]
   14000163c:	48 01 d0             	add    rax,rdx
   14000163f:	ff e0                	jmp    rax
   140001641:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140001648:	48 8d 1d 30 2a 00 00 	lea    rbx,[rip+0x2a30]        # 14000407f <.rdata+0x1f>
   14000164f:	48 8b 71 08          	mov    rsi,QWORD PTR [rcx+0x8]
   140001653:	f2 44 0f 10 41 20    	movsd  xmm8,QWORD PTR [rcx+0x20]
   140001659:	f2 0f 10 79 18       	movsd  xmm7,QWORD PTR [rcx+0x18]
   14000165e:	f2 0f 10 71 10       	movsd  xmm6,QWORD PTR [rcx+0x10]
   140001663:	b9 02 00 00 00       	mov    ecx,0x2
   140001668:	e8 d3 0e 00 00       	call   140002540 <__acrt_iob_func>
   14000166d:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001674:	49 89 f1             	mov    r9,rsi
   140001677:	49 89 d8             	mov    r8,rbx
   14000167a:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001680:	48 89 c1             	mov    rcx,rax
   140001683:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001689:	48 8d 15 c8 2a 00 00 	lea    rdx,[rip+0x2ac8]        # 140004158 <.rdata+0xf8>
   140001690:	e8 2b 0f 00 00       	call   1400025c0 <fprintf>
   140001695:	90                   	nop
   140001696:	0f 28 74 24 40       	movaps xmm6,XMMWORD PTR [rsp+0x40]
   14000169b:	31 c0                	xor    eax,eax
   14000169d:	0f 28 7c 24 50       	movaps xmm7,XMMWORD PTR [rsp+0x50]
   1400016a2:	44 0f 28 44 24 60    	movaps xmm8,XMMWORD PTR [rsp+0x60]
   1400016a8:	48 83 c4 78          	add    rsp,0x78
   1400016ac:	5b                   	pop    rbx
   1400016ad:	5e                   	pop    rsi
   1400016ae:	c3                   	ret
   1400016af:	90                   	nop
   1400016b0:	48 8d 1d a9 29 00 00 	lea    rbx,[rip+0x29a9]        # 140004060 <.rdata>
   1400016b7:	eb 96                	jmp    14000164f <_matherr+0x3f>
   1400016b9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400016c0:	48 8d 1d f9 29 00 00 	lea    rbx,[rip+0x29f9]        # 1400040c0 <.rdata+0x60>
   1400016c7:	eb 86                	jmp    14000164f <_matherr+0x3f>
   1400016c9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400016d0:	48 8d 1d c9 29 00 00 	lea    rbx,[rip+0x29c9]        # 1400040a0 <.rdata+0x40>
   1400016d7:	e9 73 ff ff ff       	jmp    14000164f <_matherr+0x3f>
   1400016dc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   1400016e0:	48 8d 1d 29 2a 00 00 	lea    rbx,[rip+0x2a29]        # 140004110 <.rdata+0xb0>
   1400016e7:	e9 63 ff ff ff       	jmp    14000164f <_matherr+0x3f>
   1400016ec:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   1400016f0:	48 8d 1d f1 29 00 00 	lea    rbx,[rip+0x29f1]        # 1400040e8 <.rdata+0x88>
   1400016f7:	e9 53 ff ff ff       	jmp    14000164f <_matherr+0x3f>
   1400016fc:	48 8d 1d 43 2a 00 00 	lea    rbx,[rip+0x2a43]        # 140004146 <.rdata+0xe6>
   140001703:	e9 47 ff ff ff       	jmp    14000164f <_matherr+0x3f>
   140001708:	90                   	nop
   140001709:	90                   	nop
   14000170a:	90                   	nop
   14000170b:	90                   	nop
   14000170c:	90                   	nop
   14000170d:	90                   	nop
   14000170e:	90                   	nop
   14000170f:	90                   	nop

0000000140001710 <_fpreset>:
   140001710:	db e3                	fninit
   140001712:	c3                   	ret
   140001713:	90                   	nop
   140001714:	90                   	nop
   140001715:	90                   	nop
   140001716:	90                   	nop
   140001717:	90                   	nop
   140001718:	90                   	nop
   140001719:	90                   	nop
   14000171a:	90                   	nop
   14000171b:	90                   	nop
   14000171c:	90                   	nop
   14000171d:	90                   	nop
   14000171e:	90                   	nop
   14000171f:	90                   	nop

0000000140001720 <__report_error>:
   140001720:	56                   	push   rsi
   140001721:	53                   	push   rbx
   140001722:	48 83 ec 38          	sub    rsp,0x38
   140001726:	48 8d 44 24 58       	lea    rax,[rsp+0x58]
   14000172b:	48 89 cb             	mov    rbx,rcx
   14000172e:	b9 02 00 00 00       	mov    ecx,0x2
   140001733:	48 89 54 24 58       	mov    QWORD PTR [rsp+0x58],rdx
   140001738:	4c 89 44 24 60       	mov    QWORD PTR [rsp+0x60],r8
   14000173d:	4c 89 4c 24 68       	mov    QWORD PTR [rsp+0x68],r9
   140001742:	48 89 44 24 28       	mov    QWORD PTR [rsp+0x28],rax
   140001747:	e8 f4 0d 00 00       	call   140002540 <__acrt_iob_func>
   14000174c:	41 b8 1b 00 00 00    	mov    r8d,0x1b
   140001752:	ba 01 00 00 00       	mov    edx,0x1
   140001757:	48 8d 0d 42 2a 00 00 	lea    rcx,[rip+0x2a42]        # 1400041a0 <.rdata>
   14000175e:	49 89 c1             	mov    r9,rax
   140001761:	e8 6a 0e 00 00       	call   1400025d0 <fwrite>
   140001766:	48 8b 74 24 28       	mov    rsi,QWORD PTR [rsp+0x28]
   14000176b:	b9 02 00 00 00       	mov    ecx,0x2
   140001770:	e8 cb 0d 00 00       	call   140002540 <__acrt_iob_func>
   140001775:	48 89 da             	mov    rdx,rbx
   140001778:	48 89 c1             	mov    rcx,rax
   14000177b:	49 89 f0             	mov    r8,rsi
   14000177e:	e8 7d 0e 00 00       	call   140002600 <vfprintf>
   140001783:	e8 20 0e 00 00       	call   1400025a8 <abort>
   140001788:	90                   	nop
   140001789:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000140001790 <mark_section_writable>:
   140001790:	57                   	push   rdi
   140001791:	56                   	push   rsi
   140001792:	53                   	push   rbx
   140001793:	48 83 ec 50          	sub    rsp,0x50
   140001797:	48 63 35 f6 58 00 00 	movsxd rsi,DWORD PTR [rip+0x58f6]        # 140007094 <maxSections>
   14000179e:	85 f6                	test   esi,esi
   1400017a0:	48 89 cb             	mov    rbx,rcx
   1400017a3:	0f 8e 17 01 00 00    	jle    1400018c0 <mark_section_writable+0x130>
   1400017a9:	48 8b 05 e8 58 00 00 	mov    rax,QWORD PTR [rip+0x58e8]        # 140007098 <the_secs>
   1400017b0:	45 31 c9             	xor    r9d,r9d
   1400017b3:	48 83 c0 18          	add    rax,0x18
   1400017b7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   1400017be:	00 00 
   1400017c0:	4c 8b 00             	mov    r8,QWORD PTR [rax]
   1400017c3:	4c 39 c3             	cmp    rbx,r8
   1400017c6:	72 13                	jb     1400017db <mark_section_writable+0x4b>
   1400017c8:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   1400017cc:	8b 52 08             	mov    edx,DWORD PTR [rdx+0x8]
   1400017cf:	49 01 d0             	add    r8,rdx
   1400017d2:	4c 39 c3             	cmp    rbx,r8
   1400017d5:	0f 82 8a 00 00 00    	jb     140001865 <mark_section_writable+0xd5>
   1400017db:	41 83 c1 01          	add    r9d,0x1
   1400017df:	48 83 c0 28          	add    rax,0x28
   1400017e3:	41 39 f1             	cmp    r9d,esi
   1400017e6:	75 d8                	jne    1400017c0 <mark_section_writable+0x30>
   1400017e8:	48 89 d9             	mov    rcx,rbx
   1400017eb:	e8 f0 09 00 00       	call   1400021e0 <__mingw_GetSectionForAddress>
   1400017f0:	48 85 c0             	test   rax,rax
   1400017f3:	48 89 c7             	mov    rdi,rax
   1400017f6:	0f 84 e6 00 00 00    	je     1400018e2 <mark_section_writable+0x152>
   1400017fc:	48 8b 05 95 58 00 00 	mov    rax,QWORD PTR [rip+0x5895]        # 140007098 <the_secs>
   140001803:	48 8d 1c b6          	lea    rbx,[rsi+rsi*4]
   140001807:	48 c1 e3 03          	shl    rbx,0x3
   14000180b:	48 01 d8             	add    rax,rbx
   14000180e:	48 89 78 20          	mov    QWORD PTR [rax+0x20],rdi
   140001812:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001818:	e8 03 0b 00 00       	call   140002320 <_GetPEImageBase>
   14000181d:	8b 57 0c             	mov    edx,DWORD PTR [rdi+0xc]
   140001820:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001826:	48 8d 0c 10          	lea    rcx,[rax+rdx*1]
   14000182a:	48 8b 05 67 58 00 00 	mov    rax,QWORD PTR [rip+0x5867]        # 140007098 <the_secs>
   140001831:	48 8d 54 24 20       	lea    rdx,[rsp+0x20]
   140001836:	48 89 4c 18 18       	mov    QWORD PTR [rax+rbx*1+0x18],rcx
   14000183b:	ff 15 63 69 00 00    	call   QWORD PTR [rip+0x6963]        # 1400081a4 <__imp_VirtualQuery>
   140001841:	48 85 c0             	test   rax,rax
   140001844:	0f 84 7d 00 00 00    	je     1400018c7 <mark_section_writable+0x137>
   14000184a:	8b 44 24 44          	mov    eax,DWORD PTR [rsp+0x44]
   14000184e:	8d 50 c0             	lea    edx,[rax-0x40]
   140001851:	83 e2 bf             	and    edx,0xffffffbf
   140001854:	74 08                	je     14000185e <mark_section_writable+0xce>
   140001856:	8d 50 fc             	lea    edx,[rax-0x4]
   140001859:	83 e2 fb             	and    edx,0xfffffffb
   14000185c:	75 12                	jne    140001870 <mark_section_writable+0xe0>
   14000185e:	83 05 2f 58 00 00 01 	add    DWORD PTR [rip+0x582f],0x1        # 140007094 <maxSections>
   140001865:	48 83 c4 50          	add    rsp,0x50
   140001869:	5b                   	pop    rbx
   14000186a:	5e                   	pop    rsi
   14000186b:	5f                   	pop    rdi
   14000186c:	c3                   	ret
   14000186d:	0f 1f 00             	nop    DWORD PTR [rax]
   140001870:	83 f8 02             	cmp    eax,0x2
   140001873:	41 b8 40 00 00 00    	mov    r8d,0x40
   140001879:	b8 04 00 00 00       	mov    eax,0x4
   14000187e:	48 8b 4c 24 20       	mov    rcx,QWORD PTR [rsp+0x20]
   140001883:	44 0f 44 c0          	cmove  r8d,eax
   140001887:	48 8b 54 24 38       	mov    rdx,QWORD PTR [rsp+0x38]
   14000188c:	48 03 1d 05 58 00 00 	add    rbx,QWORD PTR [rip+0x5805]        # 140007098 <the_secs>
   140001893:	49 89 d9             	mov    r9,rbx
   140001896:	48 89 4b 08          	mov    QWORD PTR [rbx+0x8],rcx
   14000189a:	48 89 53 10          	mov    QWORD PTR [rbx+0x10],rdx
   14000189e:	ff 15 f8 68 00 00    	call   QWORD PTR [rip+0x68f8]        # 14000819c <__imp_VirtualProtect>
   1400018a4:	85 c0                	test   eax,eax
   1400018a6:	75 b6                	jne    14000185e <mark_section_writable+0xce>
   1400018a8:	ff 15 be 68 00 00    	call   QWORD PTR [rip+0x68be]        # 14000816c <__imp_GetLastError>
   1400018ae:	48 8d 0d 63 29 00 00 	lea    rcx,[rip+0x2963]        # 140004218 <.rdata+0x78>
   1400018b5:	89 c2                	mov    edx,eax
   1400018b7:	e8 64 fe ff ff       	call   140001720 <__report_error>
   1400018bc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   1400018c0:	31 f6                	xor    esi,esi
   1400018c2:	e9 21 ff ff ff       	jmp    1400017e8 <mark_section_writable+0x58>
   1400018c7:	48 8b 05 ca 57 00 00 	mov    rax,QWORD PTR [rip+0x57ca]        # 140007098 <the_secs>
   1400018ce:	48 8d 0d 0b 29 00 00 	lea    rcx,[rip+0x290b]        # 1400041e0 <.rdata+0x40>
   1400018d5:	8b 57 08             	mov    edx,DWORD PTR [rdi+0x8]
   1400018d8:	4c 8b 44 18 18       	mov    r8,QWORD PTR [rax+rbx*1+0x18]
   1400018dd:	e8 3e fe ff ff       	call   140001720 <__report_error>
   1400018e2:	48 8d 0d d7 28 00 00 	lea    rcx,[rip+0x28d7]        # 1400041c0 <.rdata+0x20>
   1400018e9:	48 89 da             	mov    rdx,rbx
   1400018ec:	e8 2f fe ff ff       	call   140001720 <__report_error>
   1400018f1:	90                   	nop
   1400018f2:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   1400018f9:	00 00 00 00 
   1400018fd:	0f 1f 00             	nop    DWORD PTR [rax]

0000000140001900 <_pei386_runtime_relocator>:
   140001900:	55                   	push   rbp
   140001901:	41 57                	push   r15
   140001903:	41 56                	push   r14
   140001905:	41 55                	push   r13
   140001907:	41 54                	push   r12
   140001909:	57                   	push   rdi
   14000190a:	56                   	push   rsi
   14000190b:	53                   	push   rbx
   14000190c:	48 83 ec 48          	sub    rsp,0x48
   140001910:	48 8d 6c 24 40       	lea    rbp,[rsp+0x40]
   140001915:	8b 3d 75 57 00 00    	mov    edi,DWORD PTR [rip+0x5775]        # 140007090 <was_init.0>
   14000191b:	85 ff                	test   edi,edi
   14000191d:	74 11                	je     140001930 <_pei386_runtime_relocator+0x30>
   14000191f:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   140001923:	5b                   	pop    rbx
   140001924:	5e                   	pop    rsi
   140001925:	5f                   	pop    rdi
   140001926:	41 5c                	pop    r12
   140001928:	41 5d                	pop    r13
   14000192a:	41 5e                	pop    r14
   14000192c:	41 5f                	pop    r15
   14000192e:	5d                   	pop    rbp
   14000192f:	c3                   	ret
   140001930:	c7 05 56 57 00 00 01 	mov    DWORD PTR [rip+0x5756],0x1        # 140007090 <was_init.0>
   140001937:	00 00 00 
   14000193a:	e8 21 09 00 00       	call   140002260 <__mingw_GetSectionCount>
   14000193f:	48 98                	cdqe
   140001941:	48 8d 04 80          	lea    rax,[rax+rax*4]
   140001945:	48 8d 04 c5 0f 00 00 	lea    rax,[rax*8+0xf]
   14000194c:	00 
   14000194d:	48 83 e0 f0          	and    rax,0xfffffffffffffff0
   140001951:	e8 6a 0b 00 00       	call   1400024c0 <___chkstk_ms>
   140001956:	4c 8b 2d 03 2a 00 00 	mov    r13,QWORD PTR [rip+0x2a03]        # 140004360 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   14000195d:	c7 05 2d 57 00 00 00 	mov    DWORD PTR [rip+0x572d],0x0        # 140007094 <maxSections>
   140001964:	00 00 00 
   140001967:	48 8b 1d 02 2a 00 00 	mov    rbx,QWORD PTR [rip+0x2a02]        # 140004370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000196e:	48 29 c4             	sub    rsp,rax
   140001971:	48 8d 44 24 30       	lea    rax,[rsp+0x30]
   140001976:	48 89 05 1b 57 00 00 	mov    QWORD PTR [rip+0x571b],rax        # 140007098 <the_secs>
   14000197d:	4c 89 e8             	mov    rax,r13
   140001980:	48 29 d8             	sub    rax,rbx
   140001983:	48 83 f8 07          	cmp    rax,0x7
   140001987:	7e 96                	jle    14000191f <_pei386_runtime_relocator+0x1f>
   140001989:	48 83 f8 0b          	cmp    rax,0xb
   14000198d:	8b 13                	mov    edx,DWORD PTR [rbx]
   14000198f:	0f 8f 83 01 00 00    	jg     140001b18 <_pei386_runtime_relocator+0x218>
   140001995:	8b 03                	mov    eax,DWORD PTR [rbx]
   140001997:	85 c0                	test   eax,eax
   140001999:	0f 85 71 02 00 00    	jne    140001c10 <_pei386_runtime_relocator+0x310>
   14000199f:	8b 43 04             	mov    eax,DWORD PTR [rbx+0x4]
   1400019a2:	85 c0                	test   eax,eax
   1400019a4:	0f 85 66 02 00 00    	jne    140001c10 <_pei386_runtime_relocator+0x310>
   1400019aa:	8b 53 08             	mov    edx,DWORD PTR [rbx+0x8]
   1400019ad:	83 fa 01             	cmp    edx,0x1
   1400019b0:	0f 85 9c 02 00 00    	jne    140001c52 <_pei386_runtime_relocator+0x352>
   1400019b6:	48 83 c3 0c          	add    rbx,0xc
   1400019ba:	4c 39 eb             	cmp    rbx,r13
   1400019bd:	0f 83 5c ff ff ff    	jae    14000191f <_pei386_runtime_relocator+0x1f>
   1400019c3:	4c 8b 25 c6 29 00 00 	mov    r12,QWORD PTR [rip+0x29c6]        # 140004390 <.refptr.__image_base__>
   1400019ca:	49 bf ff ff ff 7f ff 	movabs r15,0xffffffff7fffffff
   1400019d1:	ff ff ff 
   1400019d4:	eb 5d                	jmp    140001a33 <_pei386_runtime_relocator+0x133>
   1400019d6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   1400019dd:	00 00 00 
   1400019e0:	41 0f b6 36          	movzx  esi,BYTE PTR [r14]
   1400019e4:	81 e1 c0 00 00 00    	and    ecx,0xc0
   1400019ea:	40 84 f6             	test   sil,sil
   1400019ed:	0f 89 05 02 00 00    	jns    140001bf8 <_pei386_runtime_relocator+0x2f8>
   1400019f3:	48 81 ce 00 ff ff ff 	or     rsi,0xffffffffffffff00
   1400019fa:	48 29 c6             	sub    rsi,rax
   1400019fd:	4c 01 ce             	add    rsi,r9
   140001a00:	85 c9                	test   ecx,ecx
   140001a02:	75 17                	jne    140001a1b <_pei386_runtime_relocator+0x11b>
   140001a04:	48 81 fe ff 00 00 00 	cmp    rsi,0xff
   140001a0b:	0f 8f 4e 01 00 00    	jg     140001b5f <_pei386_runtime_relocator+0x25f>
   140001a11:	48 83 fe 80          	cmp    rsi,0xffffffffffffff80
   140001a15:	0f 8c 44 01 00 00    	jl     140001b5f <_pei386_runtime_relocator+0x25f>
   140001a1b:	4c 89 f1             	mov    rcx,r14
   140001a1e:	e8 6d fd ff ff       	call   140001790 <mark_section_writable>
   140001a23:	41 88 36             	mov    BYTE PTR [r14],sil
   140001a26:	48 83 c3 0c          	add    rbx,0xc
   140001a2a:	4c 39 eb             	cmp    rbx,r13
   140001a2d:	0f 83 8d 00 00 00    	jae    140001ac0 <_pei386_runtime_relocator+0x1c0>
   140001a33:	8b 4b 08             	mov    ecx,DWORD PTR [rbx+0x8]
   140001a36:	8b 03                	mov    eax,DWORD PTR [rbx]
   140001a38:	44 8b 43 04          	mov    r8d,DWORD PTR [rbx+0x4]
   140001a3c:	0f b6 d1             	movzx  edx,cl
   140001a3f:	4c 01 e0             	add    rax,r12
   140001a42:	83 fa 20             	cmp    edx,0x20
   140001a45:	4c 8b 08             	mov    r9,QWORD PTR [rax]
   140001a48:	4f 8d 34 20          	lea    r14,[r8+r12*1]
   140001a4c:	0f 84 26 01 00 00    	je     140001b78 <_pei386_runtime_relocator+0x278>
   140001a52:	0f 87 e8 00 00 00    	ja     140001b40 <_pei386_runtime_relocator+0x240>
   140001a58:	83 fa 08             	cmp    edx,0x8
   140001a5b:	74 83                	je     1400019e0 <_pei386_runtime_relocator+0xe0>
   140001a5d:	83 fa 10             	cmp    edx,0x10
   140001a60:	0f 85 e0 01 00 00    	jne    140001c46 <_pei386_runtime_relocator+0x346>
   140001a66:	41 0f b7 36          	movzx  esi,WORD PTR [r14]
   140001a6a:	81 e1 c0 00 00 00    	and    ecx,0xc0
   140001a70:	66 85 f6             	test   si,si
   140001a73:	0f 89 67 01 00 00    	jns    140001be0 <_pei386_runtime_relocator+0x2e0>
   140001a79:	48 81 ce 00 00 ff ff 	or     rsi,0xffffffffffff0000
   140001a80:	48 29 c6             	sub    rsi,rax
   140001a83:	4c 01 ce             	add    rsi,r9
   140001a86:	85 c9                	test   ecx,ecx
   140001a88:	75 1a                	jne    140001aa4 <_pei386_runtime_relocator+0x1a4>
   140001a8a:	48 81 fe 00 80 ff ff 	cmp    rsi,0xffffffffffff8000
   140001a91:	0f 8c c8 00 00 00    	jl     140001b5f <_pei386_runtime_relocator+0x25f>
   140001a97:	48 81 fe ff ff 00 00 	cmp    rsi,0xffff
   140001a9e:	0f 8f bb 00 00 00    	jg     140001b5f <_pei386_runtime_relocator+0x25f>
   140001aa4:	4c 89 f1             	mov    rcx,r14
   140001aa7:	48 83 c3 0c          	add    rbx,0xc
   140001aab:	e8 e0 fc ff ff       	call   140001790 <mark_section_writable>
   140001ab0:	4c 39 eb             	cmp    rbx,r13
   140001ab3:	66 41 89 36          	mov    WORD PTR [r14],si
   140001ab7:	0f 82 76 ff ff ff    	jb     140001a33 <_pei386_runtime_relocator+0x133>
   140001abd:	0f 1f 00             	nop    DWORD PTR [rax]
   140001ac0:	8b 15 ce 55 00 00    	mov    edx,DWORD PTR [rip+0x55ce]        # 140007094 <maxSections>
   140001ac6:	85 d2                	test   edx,edx
   140001ac8:	0f 8e 51 fe ff ff    	jle    14000191f <_pei386_runtime_relocator+0x1f>
   140001ace:	48 8b 35 c7 66 00 00 	mov    rsi,QWORD PTR [rip+0x66c7]        # 14000819c <__imp_VirtualProtect>
   140001ad5:	4c 8d 65 fc          	lea    r12,[rbp-0x4]
   140001ad9:	31 db                	xor    ebx,ebx
   140001adb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001ae0:	48 8b 05 b1 55 00 00 	mov    rax,QWORD PTR [rip+0x55b1]        # 140007098 <the_secs>
   140001ae7:	48 01 d8             	add    rax,rbx
   140001aea:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   140001aed:	45 85 c0             	test   r8d,r8d
   140001af0:	74 0d                	je     140001aff <_pei386_runtime_relocator+0x1ff>
   140001af2:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   140001af6:	4d 89 e1             	mov    r9,r12
   140001af9:	48 8b 48 08          	mov    rcx,QWORD PTR [rax+0x8]
   140001afd:	ff d6                	call   rsi
   140001aff:	83 c7 01             	add    edi,0x1
   140001b02:	48 83 c3 28          	add    rbx,0x28
   140001b06:	3b 3d 88 55 00 00    	cmp    edi,DWORD PTR [rip+0x5588]        # 140007094 <maxSections>
   140001b0c:	7c d2                	jl     140001ae0 <_pei386_runtime_relocator+0x1e0>
   140001b0e:	e9 0c fe ff ff       	jmp    14000191f <_pei386_runtime_relocator+0x1f>
   140001b13:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001b18:	85 d2                	test   edx,edx
   140001b1a:	0f 85 f0 00 00 00    	jne    140001c10 <_pei386_runtime_relocator+0x310>
   140001b20:	8b 43 04             	mov    eax,DWORD PTR [rbx+0x4]
   140001b23:	89 c2                	mov    edx,eax
   140001b25:	0b 53 08             	or     edx,DWORD PTR [rbx+0x8]
   140001b28:	0f 85 74 fe ff ff    	jne    1400019a2 <_pei386_runtime_relocator+0xa2>
   140001b2e:	48 83 c3 0c          	add    rbx,0xc
   140001b32:	e9 5e fe ff ff       	jmp    140001995 <_pei386_runtime_relocator+0x95>
   140001b37:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   140001b3e:	00 00 
   140001b40:	83 fa 40             	cmp    edx,0x40
   140001b43:	0f 85 fd 00 00 00    	jne    140001c46 <_pei386_runtime_relocator+0x346>
   140001b49:	49 8b 36             	mov    rsi,QWORD PTR [r14]
   140001b4c:	48 29 c6             	sub    rsi,rax
   140001b4f:	4c 01 ce             	add    rsi,r9
   140001b52:	81 e1 c0 00 00 00    	and    ecx,0xc0
   140001b58:	75 66                	jne    140001bc0 <_pei386_runtime_relocator+0x2c0>
   140001b5a:	48 85 f6             	test   rsi,rsi
   140001b5d:	78 61                	js     140001bc0 <_pei386_runtime_relocator+0x2c0>
   140001b5f:	48 89 74 24 20       	mov    QWORD PTR [rsp+0x20],rsi
   140001b64:	48 8d 0d 3d 27 00 00 	lea    rcx,[rip+0x273d]        # 1400042a8 <.rdata+0x108>
   140001b6b:	4d 89 f0             	mov    r8,r14
   140001b6e:	e8 ad fb ff ff       	call   140001720 <__report_error>
   140001b73:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001b78:	41 8b 36             	mov    esi,DWORD PTR [r14]
   140001b7b:	81 e1 c0 00 00 00    	and    ecx,0xc0
   140001b81:	85 f6                	test   esi,esi
   140001b83:	79 4b                	jns    140001bd0 <_pei386_runtime_relocator+0x2d0>
   140001b85:	49 bb 00 00 00 00 ff 	movabs r11,0xffffffff00000000
   140001b8c:	ff ff ff 
   140001b8f:	4c 09 de             	or     rsi,r11
   140001b92:	48 29 c6             	sub    rsi,rax
   140001b95:	4c 01 ce             	add    rsi,r9
   140001b98:	85 c9                	test   ecx,ecx
   140001b9a:	75 0f                	jne    140001bab <_pei386_runtime_relocator+0x2ab>
   140001b9c:	4c 39 fe             	cmp    rsi,r15
   140001b9f:	7e be                	jle    140001b5f <_pei386_runtime_relocator+0x25f>
   140001ba1:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140001ba6:	48 39 c6             	cmp    rsi,rax
   140001ba9:	7f b4                	jg     140001b5f <_pei386_runtime_relocator+0x25f>
   140001bab:	4c 89 f1             	mov    rcx,r14
   140001bae:	e8 dd fb ff ff       	call   140001790 <mark_section_writable>
   140001bb3:	41 89 36             	mov    DWORD PTR [r14],esi
   140001bb6:	e9 6b fe ff ff       	jmp    140001a26 <_pei386_runtime_relocator+0x126>
   140001bbb:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001bc0:	4c 89 f1             	mov    rcx,r14
   140001bc3:	e8 c8 fb ff ff       	call   140001790 <mark_section_writable>
   140001bc8:	49 89 36             	mov    QWORD PTR [r14],rsi
   140001bcb:	e9 56 fe ff ff       	jmp    140001a26 <_pei386_runtime_relocator+0x126>
   140001bd0:	48 29 c6             	sub    rsi,rax
   140001bd3:	4c 01 ce             	add    rsi,r9
   140001bd6:	85 c9                	test   ecx,ecx
   140001bd8:	74 c2                	je     140001b9c <_pei386_runtime_relocator+0x29c>
   140001bda:	eb cf                	jmp    140001bab <_pei386_runtime_relocator+0x2ab>
   140001bdc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001be0:	48 29 c6             	sub    rsi,rax
   140001be3:	4c 01 ce             	add    rsi,r9
   140001be6:	85 c9                	test   ecx,ecx
   140001be8:	0f 84 9c fe ff ff    	je     140001a8a <_pei386_runtime_relocator+0x18a>
   140001bee:	e9 b1 fe ff ff       	jmp    140001aa4 <_pei386_runtime_relocator+0x1a4>
   140001bf3:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001bf8:	48 29 c6             	sub    rsi,rax
   140001bfb:	4c 01 ce             	add    rsi,r9
   140001bfe:	85 c9                	test   ecx,ecx
   140001c00:	0f 84 fe fd ff ff    	je     140001a04 <_pei386_runtime_relocator+0x104>
   140001c06:	e9 10 fe ff ff       	jmp    140001a1b <_pei386_runtime_relocator+0x11b>
   140001c0b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001c10:	4c 39 eb             	cmp    rbx,r13
   140001c13:	0f 83 06 fd ff ff    	jae    14000191f <_pei386_runtime_relocator+0x1f>
   140001c19:	4c 8b 35 70 27 00 00 	mov    r14,QWORD PTR [rip+0x2770]        # 140004390 <.refptr.__image_base__>
   140001c20:	8b 73 04             	mov    esi,DWORD PTR [rbx+0x4]
   140001c23:	48 83 c3 08          	add    rbx,0x8
   140001c27:	44 8b 63 f8          	mov    r12d,DWORD PTR [rbx-0x8]
   140001c2b:	4c 01 f6             	add    rsi,r14
   140001c2e:	44 03 26             	add    r12d,DWORD PTR [rsi]
   140001c31:	48 89 f1             	mov    rcx,rsi
   140001c34:	e8 57 fb ff ff       	call   140001790 <mark_section_writable>
   140001c39:	4c 39 eb             	cmp    rbx,r13
   140001c3c:	44 89 26             	mov    DWORD PTR [rsi],r12d
   140001c3f:	72 df                	jb     140001c20 <_pei386_runtime_relocator+0x320>
   140001c41:	e9 7a fe ff ff       	jmp    140001ac0 <_pei386_runtime_relocator+0x1c0>
   140001c46:	48 8d 0d 2b 26 00 00 	lea    rcx,[rip+0x262b]        # 140004278 <.rdata+0xd8>
   140001c4d:	e8 ce fa ff ff       	call   140001720 <__report_error>
   140001c52:	48 8d 0d e7 25 00 00 	lea    rcx,[rip+0x25e7]        # 140004240 <.rdata+0xa0>
   140001c59:	e8 c2 fa ff ff       	call   140001720 <__report_error>
   140001c5e:	90                   	nop
   140001c5f:	90                   	nop

0000000140001c60 <__mingw_raise_matherr>:
   140001c60:	48 83 ec 58          	sub    rsp,0x58
   140001c64:	48 8b 05 35 54 00 00 	mov    rax,QWORD PTR [rip+0x5435]        # 1400070a0 <stUserMathErr>
   140001c6b:	48 85 c0             	test   rax,rax
   140001c6e:	66 0f 14 d3          	unpcklpd xmm2,xmm3
   140001c72:	74 25                	je     140001c99 <__mingw_raise_matherr+0x39>
   140001c74:	f2 0f 10 84 24 80 00 	movsd  xmm0,QWORD PTR [rsp+0x80]
   140001c7b:	00 00 
   140001c7d:	89 4c 24 20          	mov    DWORD PTR [rsp+0x20],ecx
   140001c81:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
   140001c86:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
   140001c8b:	0f 29 54 24 30       	movaps XMMWORD PTR [rsp+0x30],xmm2
   140001c90:	f2 0f 11 44 24 40    	movsd  QWORD PTR [rsp+0x40],xmm0
   140001c96:	ff d0                	call   rax
   140001c98:	90                   	nop
   140001c99:	48 83 c4 58          	add    rsp,0x58
   140001c9d:	c3                   	ret
   140001c9e:	66 90                	xchg   ax,ax

0000000140001ca0 <__mingw_setusermatherr>:
   140001ca0:	48 89 0d f9 53 00 00 	mov    QWORD PTR [rip+0x53f9],rcx        # 1400070a0 <stUserMathErr>
   140001ca7:	e9 d4 08 00 00       	jmp    140002580 <__setusermatherr>
   140001cac:	90                   	nop
   140001cad:	90                   	nop
   140001cae:	90                   	nop
   140001caf:	90                   	nop

0000000140001cb0 <_gnu_exception_handler>:
   140001cb0:	53                   	push   rbx
   140001cb1:	48 83 ec 20          	sub    rsp,0x20
   140001cb5:	48 8b 11             	mov    rdx,QWORD PTR [rcx]
   140001cb8:	8b 02                	mov    eax,DWORD PTR [rdx]
   140001cba:	48 89 cb             	mov    rbx,rcx
   140001cbd:	89 c1                	mov    ecx,eax
   140001cbf:	81 e1 ff ff ff 20    	and    ecx,0x20ffffff
   140001cc5:	81 f9 43 43 47 20    	cmp    ecx,0x20474343
   140001ccb:	0f 84 9f 00 00 00    	je     140001d70 <_gnu_exception_handler+0xc0>
   140001cd1:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140001cd6:	77 77                	ja     140001d4f <_gnu_exception_handler+0x9f>
   140001cd8:	3d 8b 00 00 c0       	cmp    eax,0xc000008b
   140001cdd:	76 21                	jbe    140001d00 <_gnu_exception_handler+0x50>
   140001cdf:	05 73 ff ff 3f       	add    eax,0x3fffff73
   140001ce4:	83 f8 09             	cmp    eax,0x9
   140001ce7:	77 54                	ja     140001d3d <_gnu_exception_handler+0x8d>
   140001ce9:	48 8d 15 10 26 00 00 	lea    rdx,[rip+0x2610]        # 140004300 <.rdata>
   140001cf0:	48 63 04 82          	movsxd rax,DWORD PTR [rdx+rax*4]
   140001cf4:	48 01 d0             	add    rax,rdx
   140001cf7:	ff e0                	jmp    rax
   140001cf9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140001d00:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   140001d05:	0f 84 d5 00 00 00    	je     140001de0 <_gnu_exception_handler+0x130>
   140001d0b:	76 3b                	jbe    140001d48 <_gnu_exception_handler+0x98>
   140001d0d:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140001d12:	74 29                	je     140001d3d <_gnu_exception_handler+0x8d>
   140001d14:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140001d19:	75 34                	jne    140001d4f <_gnu_exception_handler+0x9f>
   140001d1b:	31 d2                	xor    edx,edx
   140001d1d:	b9 04 00 00 00       	mov    ecx,0x4
   140001d22:	e8 c1 08 00 00       	call   1400025e8 <signal>
   140001d27:	48 83 f8 01          	cmp    rax,0x1
   140001d2b:	0f 84 d6 00 00 00    	je     140001e07 <_gnu_exception_handler+0x157>
   140001d31:	48 85 c0             	test   rax,rax
   140001d34:	74 19                	je     140001d4f <_gnu_exception_handler+0x9f>
   140001d36:	b9 04 00 00 00       	mov    ecx,0x4
   140001d3b:	ff d0                	call   rax
   140001d3d:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140001d42:	48 83 c4 20          	add    rsp,0x20
   140001d46:	5b                   	pop    rbx
   140001d47:	c3                   	ret
   140001d48:	3d 02 00 00 80       	cmp    eax,0x80000002
   140001d4d:	74 ee                	je     140001d3d <_gnu_exception_handler+0x8d>
   140001d4f:	48 8b 05 6a 53 00 00 	mov    rax,QWORD PTR [rip+0x536a]        # 1400070c0 <__mingw_oldexcpt_handler>
   140001d56:	48 85 c0             	test   rax,rax
   140001d59:	74 25                	je     140001d80 <_gnu_exception_handler+0xd0>
   140001d5b:	48 89 d9             	mov    rcx,rbx
   140001d5e:	48 83 c4 20          	add    rsp,0x20
   140001d62:	5b                   	pop    rbx
   140001d63:	48 ff e0             	rex.W jmp rax
   140001d66:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   140001d6d:	00 00 00 
   140001d70:	f6 42 04 01          	test   BYTE PTR [rdx+0x4],0x1
   140001d74:	0f 85 57 ff ff ff    	jne    140001cd1 <_gnu_exception_handler+0x21>
   140001d7a:	eb c1                	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001d7c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001d80:	31 c0                	xor    eax,eax
   140001d82:	48 83 c4 20          	add    rsp,0x20
   140001d86:	5b                   	pop    rbx
   140001d87:	c3                   	ret
   140001d88:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   140001d8f:	00 
   140001d90:	31 d2                	xor    edx,edx
   140001d92:	b9 08 00 00 00       	mov    ecx,0x8
   140001d97:	e8 4c 08 00 00       	call   1400025e8 <signal>
   140001d9c:	48 83 f8 01          	cmp    rax,0x1
   140001da0:	0f 84 89 00 00 00    	je     140001e2f <_gnu_exception_handler+0x17f>
   140001da6:	48 85 c0             	test   rax,rax
   140001da9:	74 a4                	je     140001d4f <_gnu_exception_handler+0x9f>
   140001dab:	b9 08 00 00 00       	mov    ecx,0x8
   140001db0:	ff d0                	call   rax
   140001db2:	eb 89                	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001db4:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001db8:	31 d2                	xor    edx,edx
   140001dba:	b9 08 00 00 00       	mov    ecx,0x8
   140001dbf:	e8 24 08 00 00       	call   1400025e8 <signal>
   140001dc4:	48 83 f8 01          	cmp    rax,0x1
   140001dc8:	75 dc                	jne    140001da6 <_gnu_exception_handler+0xf6>
   140001dca:	ba 01 00 00 00       	mov    edx,0x1
   140001dcf:	b9 08 00 00 00       	mov    ecx,0x8
   140001dd4:	e8 0f 08 00 00       	call   1400025e8 <signal>
   140001dd9:	e9 5f ff ff ff       	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001dde:	66 90                	xchg   ax,ax
   140001de0:	31 d2                	xor    edx,edx
   140001de2:	b9 0b 00 00 00       	mov    ecx,0xb
   140001de7:	e8 fc 07 00 00       	call   1400025e8 <signal>
   140001dec:	48 83 f8 01          	cmp    rax,0x1
   140001df0:	74 29                	je     140001e1b <_gnu_exception_handler+0x16b>
   140001df2:	48 85 c0             	test   rax,rax
   140001df5:	0f 84 54 ff ff ff    	je     140001d4f <_gnu_exception_handler+0x9f>
   140001dfb:	b9 0b 00 00 00       	mov    ecx,0xb
   140001e00:	ff d0                	call   rax
   140001e02:	e9 36 ff ff ff       	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001e07:	ba 01 00 00 00       	mov    edx,0x1
   140001e0c:	b9 04 00 00 00       	mov    ecx,0x4
   140001e11:	e8 d2 07 00 00       	call   1400025e8 <signal>
   140001e16:	e9 22 ff ff ff       	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001e1b:	ba 01 00 00 00       	mov    edx,0x1
   140001e20:	b9 0b 00 00 00       	mov    ecx,0xb
   140001e25:	e8 be 07 00 00       	call   1400025e8 <signal>
   140001e2a:	e9 0e ff ff ff       	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001e2f:	ba 01 00 00 00       	mov    edx,0x1
   140001e34:	b9 08 00 00 00       	mov    ecx,0x8
   140001e39:	e8 aa 07 00 00       	call   1400025e8 <signal>
   140001e3e:	e8 cd f8 ff ff       	call   140001710 <_fpreset>
   140001e43:	e9 f5 fe ff ff       	jmp    140001d3d <_gnu_exception_handler+0x8d>
   140001e48:	90                   	nop
   140001e49:	90                   	nop
   140001e4a:	90                   	nop
   140001e4b:	90                   	nop
   140001e4c:	90                   	nop
   140001e4d:	90                   	nop
   140001e4e:	90                   	nop
   140001e4f:	90                   	nop

0000000140001e50 <__mingwthr_run_key_dtors.part.0>:
   140001e50:	41 54                	push   r12
   140001e52:	55                   	push   rbp
   140001e53:	57                   	push   rdi
   140001e54:	56                   	push   rsi
   140001e55:	53                   	push   rbx
   140001e56:	48 83 ec 20          	sub    rsp,0x20
   140001e5a:	4c 8d 25 9f 52 00 00 	lea    r12,[rip+0x529f]        # 140007100 <__mingwthr_cs>
   140001e61:	4c 89 e1             	mov    rcx,r12
   140001e64:	ff 15 fa 62 00 00    	call   QWORD PTR [rip+0x62fa]        # 140008164 <__imp_EnterCriticalSection>
   140001e6a:	48 8b 1d 6f 52 00 00 	mov    rbx,QWORD PTR [rip+0x526f]        # 1400070e0 <key_dtor_list>
   140001e71:	48 85 db             	test   rbx,rbx
   140001e74:	74 36                	je     140001eac <__mingwthr_run_key_dtors.part.0+0x5c>
   140001e76:	48 8b 2d 17 63 00 00 	mov    rbp,QWORD PTR [rip+0x6317]        # 140008194 <__imp_TlsGetValue>
   140001e7d:	48 8b 3d e8 62 00 00 	mov    rdi,QWORD PTR [rip+0x62e8]        # 14000816c <__imp_GetLastError>
   140001e84:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001e88:	8b 0b                	mov    ecx,DWORD PTR [rbx]
   140001e8a:	ff d5                	call   rbp
   140001e8c:	48 89 c6             	mov    rsi,rax
   140001e8f:	ff d7                	call   rdi
   140001e91:	85 c0                	test   eax,eax
   140001e93:	75 0e                	jne    140001ea3 <__mingwthr_run_key_dtors.part.0+0x53>
   140001e95:	48 85 f6             	test   rsi,rsi
   140001e98:	74 09                	je     140001ea3 <__mingwthr_run_key_dtors.part.0+0x53>
   140001e9a:	48 8b 43 08          	mov    rax,QWORD PTR [rbx+0x8]
   140001e9e:	48 89 f1             	mov    rcx,rsi
   140001ea1:	ff d0                	call   rax
   140001ea3:	48 8b 5b 10          	mov    rbx,QWORD PTR [rbx+0x10]
   140001ea7:	48 85 db             	test   rbx,rbx
   140001eaa:	75 dc                	jne    140001e88 <__mingwthr_run_key_dtors.part.0+0x38>
   140001eac:	4c 89 e1             	mov    rcx,r12
   140001eaf:	48 83 c4 20          	add    rsp,0x20
   140001eb3:	5b                   	pop    rbx
   140001eb4:	5e                   	pop    rsi
   140001eb5:	5f                   	pop    rdi
   140001eb6:	5d                   	pop    rbp
   140001eb7:	41 5c                	pop    r12
   140001eb9:	48 ff 25 bc 62 00 00 	rex.W jmp QWORD PTR [rip+0x62bc]        # 14000817c <__imp_LeaveCriticalSection>

0000000140001ec0 <___w64_mingwthr_add_key_dtor>:
   140001ec0:	57                   	push   rdi
   140001ec1:	56                   	push   rsi
   140001ec2:	53                   	push   rbx
   140001ec3:	48 83 ec 20          	sub    rsp,0x20
   140001ec7:	8b 05 1b 52 00 00    	mov    eax,DWORD PTR [rip+0x521b]        # 1400070e8 <__mingwthr_cs_init>
   140001ecd:	85 c0                	test   eax,eax
   140001ecf:	89 cf                	mov    edi,ecx
   140001ed1:	48 89 d6             	mov    rsi,rdx
   140001ed4:	75 0a                	jne    140001ee0 <___w64_mingwthr_add_key_dtor+0x20>
   140001ed6:	31 c0                	xor    eax,eax
   140001ed8:	48 83 c4 20          	add    rsp,0x20
   140001edc:	5b                   	pop    rbx
   140001edd:	5e                   	pop    rsi
   140001ede:	5f                   	pop    rdi
   140001edf:	c3                   	ret
   140001ee0:	ba 18 00 00 00       	mov    edx,0x18
   140001ee5:	b9 01 00 00 00       	mov    ecx,0x1
   140001eea:	e8 c1 06 00 00       	call   1400025b0 <calloc>
   140001eef:	48 85 c0             	test   rax,rax
   140001ef2:	48 89 c3             	mov    rbx,rax
   140001ef5:	74 33                	je     140001f2a <___w64_mingwthr_add_key_dtor+0x6a>
   140001ef7:	48 89 70 08          	mov    QWORD PTR [rax+0x8],rsi
   140001efb:	48 8d 35 fe 51 00 00 	lea    rsi,[rip+0x51fe]        # 140007100 <__mingwthr_cs>
   140001f02:	89 38                	mov    DWORD PTR [rax],edi
   140001f04:	48 89 f1             	mov    rcx,rsi
   140001f07:	ff 15 57 62 00 00    	call   QWORD PTR [rip+0x6257]        # 140008164 <__imp_EnterCriticalSection>
   140001f0d:	48 8b 05 cc 51 00 00 	mov    rax,QWORD PTR [rip+0x51cc]        # 1400070e0 <key_dtor_list>
   140001f14:	48 89 f1             	mov    rcx,rsi
   140001f17:	48 89 1d c2 51 00 00 	mov    QWORD PTR [rip+0x51c2],rbx        # 1400070e0 <key_dtor_list>
   140001f1e:	48 89 43 10          	mov    QWORD PTR [rbx+0x10],rax
   140001f22:	ff 15 54 62 00 00    	call   QWORD PTR [rip+0x6254]        # 14000817c <__imp_LeaveCriticalSection>
   140001f28:	eb ac                	jmp    140001ed6 <___w64_mingwthr_add_key_dtor+0x16>
   140001f2a:	83 c8 ff             	or     eax,0xffffffff
   140001f2d:	eb a9                	jmp    140001ed8 <___w64_mingwthr_add_key_dtor+0x18>
   140001f2f:	90                   	nop

0000000140001f30 <___w64_mingwthr_remove_key_dtor>:
   140001f30:	56                   	push   rsi
   140001f31:	53                   	push   rbx
   140001f32:	48 83 ec 28          	sub    rsp,0x28
   140001f36:	8b 05 ac 51 00 00    	mov    eax,DWORD PTR [rip+0x51ac]        # 1400070e8 <__mingwthr_cs_init>
   140001f3c:	85 c0                	test   eax,eax
   140001f3e:	89 cb                	mov    ebx,ecx
   140001f40:	75 0e                	jne    140001f50 <___w64_mingwthr_remove_key_dtor+0x20>
   140001f42:	31 c0                	xor    eax,eax
   140001f44:	48 83 c4 28          	add    rsp,0x28
   140001f48:	5b                   	pop    rbx
   140001f49:	5e                   	pop    rsi
   140001f4a:	c3                   	ret
   140001f4b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140001f50:	48 8d 35 a9 51 00 00 	lea    rsi,[rip+0x51a9]        # 140007100 <__mingwthr_cs>
   140001f57:	48 89 f1             	mov    rcx,rsi
   140001f5a:	ff 15 04 62 00 00    	call   QWORD PTR [rip+0x6204]        # 140008164 <__imp_EnterCriticalSection>
   140001f60:	48 8b 0d 79 51 00 00 	mov    rcx,QWORD PTR [rip+0x5179]        # 1400070e0 <key_dtor_list>
   140001f67:	48 85 c9             	test   rcx,rcx
   140001f6a:	74 27                	je     140001f93 <___w64_mingwthr_remove_key_dtor+0x63>
   140001f6c:	31 d2                	xor    edx,edx
   140001f6e:	eb 0b                	jmp    140001f7b <___w64_mingwthr_remove_key_dtor+0x4b>
   140001f70:	48 85 c0             	test   rax,rax
   140001f73:	48 89 ca             	mov    rdx,rcx
   140001f76:	74 1b                	je     140001f93 <___w64_mingwthr_remove_key_dtor+0x63>
   140001f78:	48 89 c1             	mov    rcx,rax
   140001f7b:	8b 01                	mov    eax,DWORD PTR [rcx]
   140001f7d:	39 d8                	cmp    eax,ebx
   140001f7f:	48 8b 41 10          	mov    rax,QWORD PTR [rcx+0x10]
   140001f83:	75 eb                	jne    140001f70 <___w64_mingwthr_remove_key_dtor+0x40>
   140001f85:	48 85 d2             	test   rdx,rdx
   140001f88:	74 1e                	je     140001fa8 <___w64_mingwthr_remove_key_dtor+0x78>
   140001f8a:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001f8e:	e8 35 06 00 00       	call   1400025c8 <free>
   140001f93:	48 89 f1             	mov    rcx,rsi
   140001f96:	ff 15 e0 61 00 00    	call   QWORD PTR [rip+0x61e0]        # 14000817c <__imp_LeaveCriticalSection>
   140001f9c:	31 c0                	xor    eax,eax
   140001f9e:	48 83 c4 28          	add    rsp,0x28
   140001fa2:	5b                   	pop    rbx
   140001fa3:	5e                   	pop    rsi
   140001fa4:	c3                   	ret
   140001fa5:	0f 1f 00             	nop    DWORD PTR [rax]
   140001fa8:	48 89 05 31 51 00 00 	mov    QWORD PTR [rip+0x5131],rax        # 1400070e0 <key_dtor_list>
   140001faf:	eb dd                	jmp    140001f8e <___w64_mingwthr_remove_key_dtor+0x5e>
   140001fb1:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   140001fb8:	00 00 00 00 
   140001fbc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000140001fc0 <__mingw_TLScallback>:
   140001fc0:	53                   	push   rbx
   140001fc1:	48 83 ec 20          	sub    rsp,0x20
   140001fc5:	83 fa 02             	cmp    edx,0x2
   140001fc8:	0f 84 b2 00 00 00    	je     140002080 <__mingw_TLScallback+0xc0>
   140001fce:	77 30                	ja     140002000 <__mingw_TLScallback+0x40>
   140001fd0:	85 d2                	test   edx,edx
   140001fd2:	74 4c                	je     140002020 <__mingw_TLScallback+0x60>
   140001fd4:	8b 05 0e 51 00 00    	mov    eax,DWORD PTR [rip+0x510e]        # 1400070e8 <__mingwthr_cs_init>
   140001fda:	85 c0                	test   eax,eax
   140001fdc:	0f 84 be 00 00 00    	je     1400020a0 <__mingw_TLScallback+0xe0>
   140001fe2:	c7 05 fc 50 00 00 01 	mov    DWORD PTR [rip+0x50fc],0x1        # 1400070e8 <__mingwthr_cs_init>
   140001fe9:	00 00 00 
   140001fec:	b8 01 00 00 00       	mov    eax,0x1
   140001ff1:	48 83 c4 20          	add    rsp,0x20
   140001ff5:	5b                   	pop    rbx
   140001ff6:	c3                   	ret
   140001ff7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   140001ffe:	00 00 
   140002000:	83 fa 03             	cmp    edx,0x3
   140002003:	75 e7                	jne    140001fec <__mingw_TLScallback+0x2c>
   140002005:	8b 05 dd 50 00 00    	mov    eax,DWORD PTR [rip+0x50dd]        # 1400070e8 <__mingwthr_cs_init>
   14000200b:	85 c0                	test   eax,eax
   14000200d:	74 dd                	je     140001fec <__mingw_TLScallback+0x2c>
   14000200f:	e8 3c fe ff ff       	call   140001e50 <__mingwthr_run_key_dtors.part.0>
   140002014:	eb d6                	jmp    140001fec <__mingw_TLScallback+0x2c>
   140002016:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000201d:	00 00 00 
   140002020:	8b 05 c2 50 00 00    	mov    eax,DWORD PTR [rip+0x50c2]        # 1400070e8 <__mingwthr_cs_init>
   140002026:	85 c0                	test   eax,eax
   140002028:	75 66                	jne    140002090 <__mingw_TLScallback+0xd0>
   14000202a:	8b 05 b8 50 00 00    	mov    eax,DWORD PTR [rip+0x50b8]        # 1400070e8 <__mingwthr_cs_init>
   140002030:	83 f8 01             	cmp    eax,0x1
   140002033:	75 b7                	jne    140001fec <__mingw_TLScallback+0x2c>
   140002035:	48 8b 1d a4 50 00 00 	mov    rbx,QWORD PTR [rip+0x50a4]        # 1400070e0 <key_dtor_list>
   14000203c:	48 85 db             	test   rbx,rbx
   14000203f:	74 18                	je     140002059 <__mingw_TLScallback+0x99>
   140002041:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140002048:	48 89 d9             	mov    rcx,rbx
   14000204b:	48 8b 5b 10          	mov    rbx,QWORD PTR [rbx+0x10]
   14000204f:	e8 74 05 00 00       	call   1400025c8 <free>
   140002054:	48 85 db             	test   rbx,rbx
   140002057:	75 ef                	jne    140002048 <__mingw_TLScallback+0x88>
   140002059:	48 8d 0d a0 50 00 00 	lea    rcx,[rip+0x50a0]        # 140007100 <__mingwthr_cs>
   140002060:	48 c7 05 75 50 00 00 	mov    QWORD PTR [rip+0x5075],0x0        # 1400070e0 <key_dtor_list>
   140002067:	00 00 00 00 
   14000206b:	c7 05 73 50 00 00 00 	mov    DWORD PTR [rip+0x5073],0x0        # 1400070e8 <__mingwthr_cs_init>
   140002072:	00 00 00 
   140002075:	ff 15 e1 60 00 00    	call   QWORD PTR [rip+0x60e1]        # 14000815c <__IAT_start__>
   14000207b:	e9 6c ff ff ff       	jmp    140001fec <__mingw_TLScallback+0x2c>
   140002080:	e8 8b f6 ff ff       	call   140001710 <_fpreset>
   140002085:	b8 01 00 00 00       	mov    eax,0x1
   14000208a:	48 83 c4 20          	add    rsp,0x20
   14000208e:	5b                   	pop    rbx
   14000208f:	c3                   	ret
   140002090:	e8 bb fd ff ff       	call   140001e50 <__mingwthr_run_key_dtors.part.0>
   140002095:	eb 93                	jmp    14000202a <__mingw_TLScallback+0x6a>
   140002097:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000209e:	00 00 
   1400020a0:	48 8d 0d 59 50 00 00 	lea    rcx,[rip+0x5059]        # 140007100 <__mingwthr_cs>
   1400020a7:	ff 15 c7 60 00 00    	call   QWORD PTR [rip+0x60c7]        # 140008174 <__imp_InitializeCriticalSection>
   1400020ad:	e9 30 ff ff ff       	jmp    140001fe2 <__mingw_TLScallback+0x22>
   1400020b2:	90                   	nop
   1400020b3:	90                   	nop
   1400020b4:	90                   	nop
   1400020b5:	90                   	nop
   1400020b6:	90                   	nop
   1400020b7:	90                   	nop
   1400020b8:	90                   	nop
   1400020b9:	90                   	nop
   1400020ba:	90                   	nop
   1400020bb:	90                   	nop
   1400020bc:	90                   	nop
   1400020bd:	90                   	nop
   1400020be:	90                   	nop
   1400020bf:	90                   	nop

00000001400020c0 <_ValidateImageBase>:
   1400020c0:	31 c0                	xor    eax,eax
   1400020c2:	66 81 39 4d 5a       	cmp    WORD PTR [rcx],0x5a4d
   1400020c7:	75 0f                	jne    1400020d8 <_ValidateImageBase+0x18>
   1400020c9:	48 63 51 3c          	movsxd rdx,DWORD PTR [rcx+0x3c]
   1400020cd:	48 01 d1             	add    rcx,rdx
   1400020d0:	81 39 50 45 00 00    	cmp    DWORD PTR [rcx],0x4550
   1400020d6:	74 08                	je     1400020e0 <_ValidateImageBase+0x20>
   1400020d8:	c3                   	ret
   1400020d9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400020e0:	31 c0                	xor    eax,eax
   1400020e2:	66 81 79 18 0b 02    	cmp    WORD PTR [rcx+0x18],0x20b
   1400020e8:	0f 94 c0             	sete   al
   1400020eb:	c3                   	ret
   1400020ec:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

00000001400020f0 <_FindPESection>:
   1400020f0:	48 63 41 3c          	movsxd rax,DWORD PTR [rcx+0x3c]
   1400020f4:	48 01 c1             	add    rcx,rax
   1400020f7:	44 0f b7 41 06       	movzx  r8d,WORD PTR [rcx+0x6]
   1400020fc:	0f b7 41 14          	movzx  eax,WORD PTR [rcx+0x14]
   140002100:	66 45 85 c0          	test   r8w,r8w
   140002104:	48 8d 44 01 18       	lea    rax,[rcx+rax*1+0x18]
   140002109:	74 32                	je     14000213d <_FindPESection+0x4d>
   14000210b:	41 8d 48 ff          	lea    ecx,[r8-0x1]
   14000210f:	48 8d 0c 89          	lea    rcx,[rcx+rcx*4]
   140002113:	4c 8d 4c c8 28       	lea    r9,[rax+rcx*8+0x28]
   140002118:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000211f:	00 
   140002120:	44 8b 40 0c          	mov    r8d,DWORD PTR [rax+0xc]
   140002124:	4c 39 c2             	cmp    rdx,r8
   140002127:	4c 89 c1             	mov    rcx,r8
   14000212a:	72 08                	jb     140002134 <_FindPESection+0x44>
   14000212c:	03 48 08             	add    ecx,DWORD PTR [rax+0x8]
   14000212f:	48 39 ca             	cmp    rdx,rcx
   140002132:	72 0b                	jb     14000213f <_FindPESection+0x4f>
   140002134:	48 83 c0 28          	add    rax,0x28
   140002138:	4c 39 c8             	cmp    rax,r9
   14000213b:	75 e3                	jne    140002120 <_FindPESection+0x30>
   14000213d:	31 c0                	xor    eax,eax
   14000213f:	c3                   	ret

0000000140002140 <_FindPESectionByName>:
   140002140:	57                   	push   rdi
   140002141:	56                   	push   rsi
   140002142:	53                   	push   rbx
   140002143:	48 83 ec 20          	sub    rsp,0x20
   140002147:	48 89 ce             	mov    rsi,rcx
   14000214a:	e8 a1 04 00 00       	call   1400025f0 <strlen>
   14000214f:	48 83 f8 08          	cmp    rax,0x8
   140002153:	77 7b                	ja     1400021d0 <_FindPESectionByName+0x90>
   140002155:	48 8b 15 34 22 00 00 	mov    rdx,QWORD PTR [rip+0x2234]        # 140004390 <.refptr.__image_base__>
   14000215c:	31 db                	xor    ebx,ebx
   14000215e:	66 81 3a 4d 5a       	cmp    WORD PTR [rdx],0x5a4d
   140002163:	75 59                	jne    1400021be <_FindPESectionByName+0x7e>
   140002165:	48 63 42 3c          	movsxd rax,DWORD PTR [rdx+0x3c]
   140002169:	48 01 d0             	add    rax,rdx
   14000216c:	81 38 50 45 00 00    	cmp    DWORD PTR [rax],0x4550
   140002172:	75 4a                	jne    1400021be <_FindPESectionByName+0x7e>
   140002174:	66 81 78 18 0b 02    	cmp    WORD PTR [rax+0x18],0x20b
   14000217a:	75 42                	jne    1400021be <_FindPESectionByName+0x7e>
   14000217c:	0f b7 50 14          	movzx  edx,WORD PTR [rax+0x14]
   140002180:	48 8d 5c 10 18       	lea    rbx,[rax+rdx*1+0x18]
   140002185:	0f b7 50 06          	movzx  edx,WORD PTR [rax+0x6]
   140002189:	66 85 d2             	test   dx,dx
   14000218c:	74 42                	je     1400021d0 <_FindPESectionByName+0x90>
   14000218e:	8d 42 ff             	lea    eax,[rdx-0x1]
   140002191:	48 8d 04 80          	lea    rax,[rax+rax*4]
   140002195:	48 8d 7c c3 28       	lea    rdi,[rbx+rax*8+0x28]
   14000219a:	eb 0d                	jmp    1400021a9 <_FindPESectionByName+0x69>
   14000219c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   1400021a0:	48 83 c3 28          	add    rbx,0x28
   1400021a4:	48 39 fb             	cmp    rbx,rdi
   1400021a7:	74 27                	je     1400021d0 <_FindPESectionByName+0x90>
   1400021a9:	41 b8 08 00 00 00    	mov    r8d,0x8
   1400021af:	48 89 f2             	mov    rdx,rsi
   1400021b2:	48 89 d9             	mov    rcx,rbx
   1400021b5:	e8 3e 04 00 00       	call   1400025f8 <strncmp>
   1400021ba:	85 c0                	test   eax,eax
   1400021bc:	75 e2                	jne    1400021a0 <_FindPESectionByName+0x60>
   1400021be:	48 89 d8             	mov    rax,rbx
   1400021c1:	48 83 c4 20          	add    rsp,0x20
   1400021c5:	5b                   	pop    rbx
   1400021c6:	5e                   	pop    rsi
   1400021c7:	5f                   	pop    rdi
   1400021c8:	c3                   	ret
   1400021c9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400021d0:	31 db                	xor    ebx,ebx
   1400021d2:	48 89 d8             	mov    rax,rbx
   1400021d5:	48 83 c4 20          	add    rsp,0x20
   1400021d9:	5b                   	pop    rbx
   1400021da:	5e                   	pop    rsi
   1400021db:	5f                   	pop    rdi
   1400021dc:	c3                   	ret
   1400021dd:	0f 1f 00             	nop    DWORD PTR [rax]

00000001400021e0 <__mingw_GetSectionForAddress>:
   1400021e0:	48 8b 15 a9 21 00 00 	mov    rdx,QWORD PTR [rip+0x21a9]        # 140004390 <.refptr.__image_base__>
   1400021e7:	31 c0                	xor    eax,eax
   1400021e9:	66 81 3a 4d 5a       	cmp    WORD PTR [rdx],0x5a4d
   1400021ee:	75 10                	jne    140002200 <__mingw_GetSectionForAddress+0x20>
   1400021f0:	4c 63 42 3c          	movsxd r8,DWORD PTR [rdx+0x3c]
   1400021f4:	49 01 d0             	add    r8,rdx
   1400021f7:	41 81 38 50 45 00 00 	cmp    DWORD PTR [r8],0x4550
   1400021fe:	74 08                	je     140002208 <__mingw_GetSectionForAddress+0x28>
   140002200:	c3                   	ret
   140002201:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140002208:	66 41 81 78 18 0b 02 	cmp    WORD PTR [r8+0x18],0x20b
   14000220f:	75 ef                	jne    140002200 <__mingw_GetSectionForAddress+0x20>
   140002211:	41 0f b7 40 14       	movzx  eax,WORD PTR [r8+0x14]
   140002216:	48 29 d1             	sub    rcx,rdx
   140002219:	49 8d 44 00 18       	lea    rax,[r8+rax*1+0x18]
   14000221e:	45 0f b7 40 06       	movzx  r8d,WORD PTR [r8+0x6]
   140002223:	66 45 85 c0          	test   r8w,r8w
   140002227:	74 34                	je     14000225d <__mingw_GetSectionForAddress+0x7d>
   140002229:	41 8d 50 ff          	lea    edx,[r8-0x1]
   14000222d:	48 8d 14 92          	lea    rdx,[rdx+rdx*4]
   140002231:	4c 8d 4c d0 28       	lea    r9,[rax+rdx*8+0x28]
   140002236:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000223d:	00 00 00 
   140002240:	44 8b 40 0c          	mov    r8d,DWORD PTR [rax+0xc]
   140002244:	4c 39 c1             	cmp    rcx,r8
   140002247:	4c 89 c2             	mov    rdx,r8
   14000224a:	72 08                	jb     140002254 <__mingw_GetSectionForAddress+0x74>
   14000224c:	03 50 08             	add    edx,DWORD PTR [rax+0x8]
   14000224f:	48 39 d1             	cmp    rcx,rdx
   140002252:	72 ac                	jb     140002200 <__mingw_GetSectionForAddress+0x20>
   140002254:	48 83 c0 28          	add    rax,0x28
   140002258:	4c 39 c8             	cmp    rax,r9
   14000225b:	75 e3                	jne    140002240 <__mingw_GetSectionForAddress+0x60>
   14000225d:	31 c0                	xor    eax,eax
   14000225f:	c3                   	ret

0000000140002260 <__mingw_GetSectionCount>:
   140002260:	48 8b 05 29 21 00 00 	mov    rax,QWORD PTR [rip+0x2129]        # 140004390 <.refptr.__image_base__>
   140002267:	31 c9                	xor    ecx,ecx
   140002269:	66 81 38 4d 5a       	cmp    WORD PTR [rax],0x5a4d
   14000226e:	75 0f                	jne    14000227f <__mingw_GetSectionCount+0x1f>
   140002270:	48 63 50 3c          	movsxd rdx,DWORD PTR [rax+0x3c]
   140002274:	48 01 d0             	add    rax,rdx
   140002277:	81 38 50 45 00 00    	cmp    DWORD PTR [rax],0x4550
   14000227d:	74 09                	je     140002288 <__mingw_GetSectionCount+0x28>
   14000227f:	89 c8                	mov    eax,ecx
   140002281:	c3                   	ret
   140002282:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
   140002288:	66 81 78 18 0b 02    	cmp    WORD PTR [rax+0x18],0x20b
   14000228e:	75 ef                	jne    14000227f <__mingw_GetSectionCount+0x1f>
   140002290:	0f b7 48 06          	movzx  ecx,WORD PTR [rax+0x6]
   140002294:	89 c8                	mov    eax,ecx
   140002296:	c3                   	ret
   140002297:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000229e:	00 00 

00000001400022a0 <_FindPESectionExec>:
   1400022a0:	4c 8b 05 e9 20 00 00 	mov    r8,QWORD PTR [rip+0x20e9]        # 140004390 <.refptr.__image_base__>
   1400022a7:	31 c0                	xor    eax,eax
   1400022a9:	66 41 81 38 4d 5a    	cmp    WORD PTR [r8],0x5a4d
   1400022af:	75 0f                	jne    1400022c0 <_FindPESectionExec+0x20>
   1400022b1:	49 63 50 3c          	movsxd rdx,DWORD PTR [r8+0x3c]
   1400022b5:	4c 01 c2             	add    rdx,r8
   1400022b8:	81 3a 50 45 00 00    	cmp    DWORD PTR [rdx],0x4550
   1400022be:	74 08                	je     1400022c8 <_FindPESectionExec+0x28>
   1400022c0:	c3                   	ret
   1400022c1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400022c8:	66 81 7a 18 0b 02    	cmp    WORD PTR [rdx+0x18],0x20b
   1400022ce:	75 f0                	jne    1400022c0 <_FindPESectionExec+0x20>
   1400022d0:	44 0f b7 42 06       	movzx  r8d,WORD PTR [rdx+0x6]
   1400022d5:	0f b7 42 14          	movzx  eax,WORD PTR [rdx+0x14]
   1400022d9:	66 45 85 c0          	test   r8w,r8w
   1400022dd:	48 8d 44 02 18       	lea    rax,[rdx+rax*1+0x18]
   1400022e2:	74 2c                	je     140002310 <_FindPESectionExec+0x70>
   1400022e4:	41 8d 50 ff          	lea    edx,[r8-0x1]
   1400022e8:	48 8d 14 92          	lea    rdx,[rdx+rdx*4]
   1400022ec:	48 8d 54 d0 28       	lea    rdx,[rax+rdx*8+0x28]
   1400022f1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400022f8:	f6 40 27 20          	test   BYTE PTR [rax+0x27],0x20
   1400022fc:	74 09                	je     140002307 <_FindPESectionExec+0x67>
   1400022fe:	48 85 c9             	test   rcx,rcx
   140002301:	74 bd                	je     1400022c0 <_FindPESectionExec+0x20>
   140002303:	48 83 e9 01          	sub    rcx,0x1
   140002307:	48 83 c0 28          	add    rax,0x28
   14000230b:	48 39 d0             	cmp    rax,rdx
   14000230e:	75 e8                	jne    1400022f8 <_FindPESectionExec+0x58>
   140002310:	31 c0                	xor    eax,eax
   140002312:	c3                   	ret
   140002313:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000231a:	00 00 00 00 
   14000231e:	66 90                	xchg   ax,ax

0000000140002320 <_GetPEImageBase>:
   140002320:	48 8b 05 69 20 00 00 	mov    rax,QWORD PTR [rip+0x2069]        # 140004390 <.refptr.__image_base__>
   140002327:	31 d2                	xor    edx,edx
   140002329:	66 81 38 4d 5a       	cmp    WORD PTR [rax],0x5a4d
   14000232e:	75 0f                	jne    14000233f <_GetPEImageBase+0x1f>
   140002330:	48 63 48 3c          	movsxd rcx,DWORD PTR [rax+0x3c]
   140002334:	48 01 c1             	add    rcx,rax
   140002337:	81 39 50 45 00 00    	cmp    DWORD PTR [rcx],0x4550
   14000233d:	74 09                	je     140002348 <_GetPEImageBase+0x28>
   14000233f:	48 89 d0             	mov    rax,rdx
   140002342:	c3                   	ret
   140002343:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140002348:	66 81 79 18 0b 02    	cmp    WORD PTR [rcx+0x18],0x20b
   14000234e:	48 0f 44 d0          	cmove  rdx,rax
   140002352:	48 89 d0             	mov    rax,rdx
   140002355:	c3                   	ret
   140002356:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000235d:	00 00 00 

0000000140002360 <_IsNonwritableInCurrentImage>:
   140002360:	48 8b 15 29 20 00 00 	mov    rdx,QWORD PTR [rip+0x2029]        # 140004390 <.refptr.__image_base__>
   140002367:	31 c0                	xor    eax,eax
   140002369:	66 81 3a 4d 5a       	cmp    WORD PTR [rdx],0x5a4d
   14000236e:	75 10                	jne    140002380 <_IsNonwritableInCurrentImage+0x20>
   140002370:	4c 63 42 3c          	movsxd r8,DWORD PTR [rdx+0x3c]
   140002374:	49 01 d0             	add    r8,rdx
   140002377:	41 81 38 50 45 00 00 	cmp    DWORD PTR [r8],0x4550
   14000237e:	74 08                	je     140002388 <_IsNonwritableInCurrentImage+0x28>
   140002380:	c3                   	ret
   140002381:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140002388:	66 41 81 78 18 0b 02 	cmp    WORD PTR [r8+0x18],0x20b
   14000238f:	75 ef                	jne    140002380 <_IsNonwritableInCurrentImage+0x20>
   140002391:	45 0f b7 48 06       	movzx  r9d,WORD PTR [r8+0x6]
   140002396:	48 29 d1             	sub    rcx,rdx
   140002399:	41 0f b7 50 14       	movzx  edx,WORD PTR [r8+0x14]
   14000239e:	66 45 85 c9          	test   r9w,r9w
   1400023a2:	49 8d 54 10 18       	lea    rdx,[r8+rdx*1+0x18]
   1400023a7:	74 d7                	je     140002380 <_IsNonwritableInCurrentImage+0x20>
   1400023a9:	41 8d 41 ff          	lea    eax,[r9-0x1]
   1400023ad:	48 8d 04 80          	lea    rax,[rax+rax*4]
   1400023b1:	4c 8d 4c c2 28       	lea    r9,[rdx+rax*8+0x28]
   1400023b6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   1400023bd:	00 00 00 
   1400023c0:	44 8b 42 0c          	mov    r8d,DWORD PTR [rdx+0xc]
   1400023c4:	4c 39 c1             	cmp    rcx,r8
   1400023c7:	4c 89 c0             	mov    rax,r8
   1400023ca:	72 08                	jb     1400023d4 <_IsNonwritableInCurrentImage+0x74>
   1400023cc:	03 42 08             	add    eax,DWORD PTR [rdx+0x8]
   1400023cf:	48 39 c1             	cmp    rcx,rax
   1400023d2:	72 0c                	jb     1400023e0 <_IsNonwritableInCurrentImage+0x80>
   1400023d4:	48 83 c2 28          	add    rdx,0x28
   1400023d8:	49 39 d1             	cmp    r9,rdx
   1400023db:	75 e3                	jne    1400023c0 <_IsNonwritableInCurrentImage+0x60>
   1400023dd:	31 c0                	xor    eax,eax
   1400023df:	c3                   	ret
   1400023e0:	8b 42 24             	mov    eax,DWORD PTR [rdx+0x24]
   1400023e3:	f7 d0                	not    eax
   1400023e5:	c1 e8 1f             	shr    eax,0x1f
   1400023e8:	c3                   	ret
   1400023e9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000001400023f0 <__mingw_enum_import_library_names>:
   1400023f0:	4c 8b 1d 99 1f 00 00 	mov    r11,QWORD PTR [rip+0x1f99]        # 140004390 <.refptr.__image_base__>
   1400023f7:	45 31 c9             	xor    r9d,r9d
   1400023fa:	66 41 81 3b 4d 5a    	cmp    WORD PTR [r11],0x5a4d
   140002400:	75 10                	jne    140002412 <__mingw_enum_import_library_names+0x22>
   140002402:	4d 63 43 3c          	movsxd r8,DWORD PTR [r11+0x3c]
   140002406:	4d 01 d8             	add    r8,r11
   140002409:	41 81 38 50 45 00 00 	cmp    DWORD PTR [r8],0x4550
   140002410:	74 0e                	je     140002420 <__mingw_enum_import_library_names+0x30>
   140002412:	4c 89 c8             	mov    rax,r9
   140002415:	c3                   	ret
   140002416:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000241d:	00 00 00 
   140002420:	66 41 81 78 18 0b 02 	cmp    WORD PTR [r8+0x18],0x20b
   140002427:	75 e9                	jne    140002412 <__mingw_enum_import_library_names+0x22>
   140002429:	41 8b 80 90 00 00 00 	mov    eax,DWORD PTR [r8+0x90]
   140002430:	85 c0                	test   eax,eax
   140002432:	74 de                	je     140002412 <__mingw_enum_import_library_names+0x22>
   140002434:	45 0f b7 50 06       	movzx  r10d,WORD PTR [r8+0x6]
   140002439:	41 0f b7 50 14       	movzx  edx,WORD PTR [r8+0x14]
   14000243e:	66 45 85 d2          	test   r10w,r10w
   140002442:	49 8d 54 10 18       	lea    rdx,[r8+rdx*1+0x18]
   140002447:	74 c9                	je     140002412 <__mingw_enum_import_library_names+0x22>
   140002449:	45 8d 42 ff          	lea    r8d,[r10-0x1]
   14000244d:	4f 8d 04 80          	lea    r8,[r8+r8*4]
   140002451:	4e 8d 54 c2 28       	lea    r10,[rdx+r8*8+0x28]
   140002456:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000245d:	00 00 00 
   140002460:	44 8b 4a 0c          	mov    r9d,DWORD PTR [rdx+0xc]
   140002464:	4c 39 c8             	cmp    rax,r9
   140002467:	4d 89 c8             	mov    r8,r9
   14000246a:	72 09                	jb     140002475 <__mingw_enum_import_library_names+0x85>
   14000246c:	44 03 42 08          	add    r8d,DWORD PTR [rdx+0x8]
   140002470:	4c 39 c0             	cmp    rax,r8
   140002473:	72 13                	jb     140002488 <__mingw_enum_import_library_names+0x98>
   140002475:	48 83 c2 28          	add    rdx,0x28
   140002479:	4c 39 d2             	cmp    rdx,r10
   14000247c:	75 e2                	jne    140002460 <__mingw_enum_import_library_names+0x70>
   14000247e:	45 31 c9             	xor    r9d,r9d
   140002481:	4c 89 c8             	mov    rax,r9
   140002484:	c3                   	ret
   140002485:	0f 1f 00             	nop    DWORD PTR [rax]
   140002488:	4c 01 d8             	add    rax,r11
   14000248b:	eb 0a                	jmp    140002497 <__mingw_enum_import_library_names+0xa7>
   14000248d:	0f 1f 00             	nop    DWORD PTR [rax]
   140002490:	83 e9 01             	sub    ecx,0x1
   140002493:	48 83 c0 14          	add    rax,0x14
   140002497:	44 8b 40 04          	mov    r8d,DWORD PTR [rax+0x4]
   14000249b:	45 85 c0             	test   r8d,r8d
   14000249e:	75 07                	jne    1400024a7 <__mingw_enum_import_library_names+0xb7>
   1400024a0:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   1400024a3:	85 d2                	test   edx,edx
   1400024a5:	74 d7                	je     14000247e <__mingw_enum_import_library_names+0x8e>
   1400024a7:	85 c9                	test   ecx,ecx
   1400024a9:	7f e5                	jg     140002490 <__mingw_enum_import_library_names+0xa0>
   1400024ab:	44 8b 48 0c          	mov    r9d,DWORD PTR [rax+0xc]
   1400024af:	4d 01 d9             	add    r9,r11
   1400024b2:	4c 89 c8             	mov    rax,r9
   1400024b5:	c3                   	ret
   1400024b6:	90                   	nop
   1400024b7:	90                   	nop
   1400024b8:	90                   	nop
   1400024b9:	90                   	nop
   1400024ba:	90                   	nop
   1400024bb:	90                   	nop
   1400024bc:	90                   	nop
   1400024bd:	90                   	nop
   1400024be:	90                   	nop
   1400024bf:	90                   	nop

00000001400024c0 <___chkstk_ms>:
   1400024c0:	51                   	push   rcx
   1400024c1:	50                   	push   rax
   1400024c2:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400024c8:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   1400024cd:	72 19                	jb     1400024e8 <___chkstk_ms+0x28>
   1400024cf:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   1400024d6:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400024da:	48 2d 00 10 00 00    	sub    rax,0x1000
   1400024e0:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400024e6:	77 e7                	ja     1400024cf <___chkstk_ms+0xf>
   1400024e8:	48 29 c1             	sub    rcx,rax
   1400024eb:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400024ef:	58                   	pop    rax
   1400024f0:	59                   	pop    rcx
   1400024f1:	c3                   	ret
   1400024f2:	90                   	nop
   1400024f3:	90                   	nop
   1400024f4:	90                   	nop
   1400024f5:	90                   	nop
   1400024f6:	90                   	nop
   1400024f7:	90                   	nop
   1400024f8:	90                   	nop
   1400024f9:	90                   	nop
   1400024fa:	90                   	nop
   1400024fb:	90                   	nop
   1400024fc:	90                   	nop
   1400024fd:	90                   	nop
   1400024fe:	90                   	nop
   1400024ff:	90                   	nop

0000000140002500 <__p__fmode>:
   140002500:	48 8b 05 b9 1e 00 00 	mov    rax,QWORD PTR [rip+0x1eb9]        # 1400043c0 <.refptr.__imp__fmode>
   140002507:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000250a:	c3                   	ret
   14000250b:	90                   	nop
   14000250c:	90                   	nop
   14000250d:	90                   	nop
   14000250e:	90                   	nop
   14000250f:	90                   	nop

0000000140002510 <__p__commode>:
   140002510:	48 8b 05 99 1e 00 00 	mov    rax,QWORD PTR [rip+0x1e99]        # 1400043b0 <.refptr.__imp__commode>
   140002517:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000251a:	c3                   	ret
   14000251b:	90                   	nop
   14000251c:	90                   	nop
   14000251d:	90                   	nop
   14000251e:	90                   	nop
   14000251f:	90                   	nop

0000000140002520 <_get_invalid_parameter_handler>:
   140002520:	48 8b 05 49 4c 00 00 	mov    rax,QWORD PTR [rip+0x4c49]        # 140007170 <handler>
   140002527:	c3                   	ret
   140002528:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000252f:	00 

0000000140002530 <_set_invalid_parameter_handler>:
   140002530:	48 89 c8             	mov    rax,rcx
   140002533:	48 87 05 36 4c 00 00 	xchg   QWORD PTR [rip+0x4c36],rax        # 140007170 <handler>
   14000253a:	c3                   	ret
   14000253b:	90                   	nop
   14000253c:	90                   	nop
   14000253d:	90                   	nop
   14000253e:	90                   	nop
   14000253f:	90                   	nop

0000000140002540 <__acrt_iob_func>:
   140002540:	53                   	push   rbx
   140002541:	48 83 ec 20          	sub    rsp,0x20
   140002545:	89 cb                	mov    ebx,ecx
   140002547:	e8 24 00 00 00       	call   140002570 <__iob_func>
   14000254c:	89 d9                	mov    ecx,ebx
   14000254e:	48 8d 14 49          	lea    rdx,[rcx+rcx*2]
   140002552:	48 c1 e2 04          	shl    rdx,0x4
   140002556:	48 01 d0             	add    rax,rdx
   140002559:	48 83 c4 20          	add    rsp,0x20
   14000255d:	5b                   	pop    rbx
   14000255e:	c3                   	ret
   14000255f:	90                   	nop

0000000140002560 <__C_specific_handler>:
   140002560:	ff 25 4e 5c 00 00    	jmp    QWORD PTR [rip+0x5c4e]        # 1400081b4 <__imp___C_specific_handler>
   140002566:	90                   	nop
   140002567:	90                   	nop

0000000140002568 <__getmainargs>:
   140002568:	ff 25 4e 5c 00 00    	jmp    QWORD PTR [rip+0x5c4e]        # 1400081bc <__imp___getmainargs>
   14000256e:	90                   	nop
   14000256f:	90                   	nop

0000000140002570 <__iob_func>:
   140002570:	ff 25 56 5c 00 00    	jmp    QWORD PTR [rip+0x5c56]        # 1400081cc <__imp___iob_func>
   140002576:	90                   	nop
   140002577:	90                   	nop

0000000140002578 <__set_app_type>:
   140002578:	ff 25 56 5c 00 00    	jmp    QWORD PTR [rip+0x5c56]        # 1400081d4 <__imp___set_app_type>
   14000257e:	90                   	nop
   14000257f:	90                   	nop

0000000140002580 <__setusermatherr>:
   140002580:	ff 25 56 5c 00 00    	jmp    QWORD PTR [rip+0x5c56]        # 1400081dc <__imp___setusermatherr>
   140002586:	90                   	nop
   140002587:	90                   	nop

0000000140002588 <_amsg_exit>:
   140002588:	ff 25 56 5c 00 00    	jmp    QWORD PTR [rip+0x5c56]        # 1400081e4 <__imp__amsg_exit>
   14000258e:	90                   	nop
   14000258f:	90                   	nop

0000000140002590 <_cexit>:
   140002590:	ff 25 56 5c 00 00    	jmp    QWORD PTR [rip+0x5c56]        # 1400081ec <__imp__cexit>
   140002596:	90                   	nop
   140002597:	90                   	nop

0000000140002598 <_initterm>:
   140002598:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008204 <__imp__initterm>
   14000259e:	90                   	nop
   14000259f:	90                   	nop

00000001400025a0 <_onexit>:
   1400025a0:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000820c <__imp__onexit>
   1400025a6:	90                   	nop
   1400025a7:	90                   	nop

00000001400025a8 <abort>:
   1400025a8:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008214 <__imp_abort>
   1400025ae:	90                   	nop
   1400025af:	90                   	nop

00000001400025b0 <calloc>:
   1400025b0:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000821c <__imp_calloc>
   1400025b6:	90                   	nop
   1400025b7:	90                   	nop

00000001400025b8 <exit>:
   1400025b8:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008224 <__imp_exit>
   1400025be:	90                   	nop
   1400025bf:	90                   	nop

00000001400025c0 <fprintf>:
   1400025c0:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000822c <__imp_fprintf>
   1400025c6:	90                   	nop
   1400025c7:	90                   	nop

00000001400025c8 <free>:
   1400025c8:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008234 <__imp_free>
   1400025ce:	90                   	nop
   1400025cf:	90                   	nop

00000001400025d0 <fwrite>:
   1400025d0:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000823c <__imp_fwrite>
   1400025d6:	90                   	nop
   1400025d7:	90                   	nop

00000001400025d8 <malloc>:
   1400025d8:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008244 <__imp_malloc>
   1400025de:	90                   	nop
   1400025df:	90                   	nop

00000001400025e0 <memcpy>:
   1400025e0:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000824c <__imp_memcpy>
   1400025e6:	90                   	nop
   1400025e7:	90                   	nop

00000001400025e8 <signal>:
   1400025e8:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008254 <__imp_signal>
   1400025ee:	90                   	nop
   1400025ef:	90                   	nop

00000001400025f0 <strlen>:
   1400025f0:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000825c <__imp_strlen>
   1400025f6:	90                   	nop
   1400025f7:	90                   	nop

00000001400025f8 <strncmp>:
   1400025f8:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 140008264 <__imp_strncmp>
   1400025fe:	90                   	nop
   1400025ff:	90                   	nop

0000000140002600 <vfprintf>:
   140002600:	ff 25 66 5c 00 00    	jmp    QWORD PTR [rip+0x5c66]        # 14000826c <__imp_vfprintf>
   140002606:	90                   	nop
   140002607:	90                   	nop
   140002608:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000260f:	00 

0000000140002610 <VirtualQuery>:
   140002610:	ff 25 8e 5b 00 00    	jmp    QWORD PTR [rip+0x5b8e]        # 1400081a4 <__imp_VirtualQuery>
   140002616:	90                   	nop
   140002617:	90                   	nop

0000000140002618 <VirtualProtect>:
   140002618:	ff 25 7e 5b 00 00    	jmp    QWORD PTR [rip+0x5b7e]        # 14000819c <__imp_VirtualProtect>
   14000261e:	90                   	nop
   14000261f:	90                   	nop

0000000140002620 <TlsGetValue>:
   140002620:	ff 25 6e 5b 00 00    	jmp    QWORD PTR [rip+0x5b6e]        # 140008194 <__imp_TlsGetValue>
   140002626:	90                   	nop
   140002627:	90                   	nop

0000000140002628 <Sleep>:
   140002628:	ff 25 5e 5b 00 00    	jmp    QWORD PTR [rip+0x5b5e]        # 14000818c <__imp_Sleep>
   14000262e:	90                   	nop
   14000262f:	90                   	nop

0000000140002630 <SetUnhandledExceptionFilter>:
   140002630:	ff 25 4e 5b 00 00    	jmp    QWORD PTR [rip+0x5b4e]        # 140008184 <__imp_SetUnhandledExceptionFilter>
   140002636:	90                   	nop
   140002637:	90                   	nop

0000000140002638 <LeaveCriticalSection>:
   140002638:	ff 25 3e 5b 00 00    	jmp    QWORD PTR [rip+0x5b3e]        # 14000817c <__imp_LeaveCriticalSection>
   14000263e:	90                   	nop
   14000263f:	90                   	nop

0000000140002640 <InitializeCriticalSection>:
   140002640:	ff 25 2e 5b 00 00    	jmp    QWORD PTR [rip+0x5b2e]        # 140008174 <__imp_InitializeCriticalSection>
   140002646:	90                   	nop
   140002647:	90                   	nop

0000000140002648 <GetLastError>:
   140002648:	ff 25 1e 5b 00 00    	jmp    QWORD PTR [rip+0x5b1e]        # 14000816c <__imp_GetLastError>
   14000264e:	90                   	nop
   14000264f:	90                   	nop

0000000140002650 <EnterCriticalSection>:
   140002650:	ff 25 0e 5b 00 00    	jmp    QWORD PTR [rip+0x5b0e]        # 140008164 <__imp_EnterCriticalSection>
   140002656:	90                   	nop
   140002657:	90                   	nop

0000000140002658 <DeleteCriticalSection>:
   140002658:	ff 25 fe 5a 00 00    	jmp    QWORD PTR [rip+0x5afe]        # 14000815c <__IAT_start__>
   14000265e:	90                   	nop
   14000265f:	90                   	nop

0000000140002660 <main>:
   140002660:	53                   	push   rbx
   140002661:	48 83 ec 20          	sub    rsp,0x20
   140002665:	89 cb                	mov    ebx,ecx
   140002667:	e8 a4 ee ff ff       	call   140001510 <__main>
   14000266c:	89 d9                	mov    ecx,ebx
   14000266e:	48 83 c4 20          	add    rsp,0x20
   140002672:	5b                   	pop    rbx
   140002673:	e9 d8 ed ff ff       	jmp    140001450 <_Z7computei>
   140002678:	90                   	nop
   140002679:	90                   	nop
   14000267a:	90                   	nop
   14000267b:	90                   	nop
   14000267c:	90                   	nop
   14000267d:	90                   	nop
   14000267e:	90                   	nop
   14000267f:	90                   	nop

0000000140002680 <register_frame_ctor>:
   140002680:	e9 ab ed ff ff       	jmp    140001430 <__gcc_register_frame>
   140002685:	90                   	nop
   140002686:	90                   	nop
   140002687:	90                   	nop
   140002688:	90                   	nop
   140002689:	90                   	nop
   14000268a:	90                   	nop
   14000268b:	90                   	nop
   14000268c:	90                   	nop
   14000268d:	90                   	nop
   14000268e:	90                   	nop
   14000268f:	90                   	nop

0000000140002690 <__CTOR_LIST__>:
   140002690:	ff                   	(bad)
   140002691:	ff                   	(bad)
   140002692:	ff                   	(bad)
   140002693:	ff                   	(bad)
   140002694:	ff                   	(bad)
   140002695:	ff                   	(bad)
   140002696:	ff                   	(bad)
   140002697:	ff                   	.byte 0xff

0000000140002698 <.ctors.65535>:
   140002698:	80 26 00             	and    BYTE PTR [rsi],0x0
   14000269b:	40 01 00             	rex add DWORD PTR [rax],eax
	...

00000001400026a8 <__DTOR_LIST__>:
   1400026a8:	ff                   	(bad)
   1400026a9:	ff                   	(bad)
   1400026aa:	ff                   	(bad)
   1400026ab:	ff                   	(bad)
   1400026ac:	ff                   	(bad)
   1400026ad:	ff                   	(bad)
   1400026ae:	ff                   	(bad)
   1400026af:	ff 00                	inc    DWORD PTR [rax]
   1400026b1:	00 00                	add    BYTE PTR [rax],al
   1400026b3:	00 00                	add    BYTE PTR [rax],al
   1400026b5:	00 00                	add    BYTE PTR [rax],al
	...
