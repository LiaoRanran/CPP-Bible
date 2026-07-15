
ch88_variant_visit_test.exe:     file format pei-x86-64


Disassembly of section .text:

0000000140001000 <__mingw_invalidParameterHandler>:
   140001000:	55                   	push   rbp
   140001001:	48 89 e5             	mov    rbp,rsp
   140001004:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001008:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000100c:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001010:	44 89 4d 28          	mov    DWORD PTR [rbp+0x28],r9d
   140001014:	90                   	nop
   140001015:	5d                   	pop    rbp
   140001016:	c3                   	ret

0000000140001017 <safe_flush>:
   140001017:	55                   	push   rbp
   140001018:	48 89 e5             	mov    rbp,rsp
   14000101b:	48 83 ec 20          	sub    rsp,0x20
   14000101f:	b9 00 00 00 00       	mov    ecx,0x0
   140001024:	e8 27 22 00 00       	call   140003250 <fflush>
   140001029:	90                   	nop
   14000102a:	48 83 c4 20          	add    rsp,0x20
   14000102e:	5d                   	pop    rbp
   14000102f:	c3                   	ret

0000000140001030 <WinMainCRTStartup>:
   140001030:	55                   	push   rbp
   140001031:	48 89 e5             	mov    rbp,rsp
   140001034:	48 83 ec 30          	sub    rsp,0x30
   140001038:	c7 45 fc ff 00 00 00 	mov    DWORD PTR [rbp-0x4],0xff

000000014000103f <.l_startw>:
   14000103f:	48 8b 05 9a 43 00 00 	mov    rax,QWORD PTR [rip+0x439a]        # 1400053e0 <.refptr.__mingw_app_type>
   140001046:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000104c:	e8 3d 00 00 00       	call   14000108e <__tmainCRTStartup>
   140001051:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001054:	90                   	nop

0000000140001055 <.l_endw>:
   140001055:	90                   	nop
   140001056:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001059:	48 83 c4 30          	add    rsp,0x30
   14000105d:	5d                   	pop    rbp
   14000105e:	c3                   	ret

000000014000105f <mainCRTStartup>:
   14000105f:	55                   	push   rbp
   140001060:	48 89 e5             	mov    rbp,rsp
   140001063:	48 83 ec 30          	sub    rsp,0x30
   140001067:	c7 45 fc ff 00 00 00 	mov    DWORD PTR [rbp-0x4],0xff

000000014000106e <.l_start>:
   14000106e:	48 8b 05 6b 43 00 00 	mov    rax,QWORD PTR [rip+0x436b]        # 1400053e0 <.refptr.__mingw_app_type>
   140001075:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   14000107b:	e8 0e 00 00 00       	call   14000108e <__tmainCRTStartup>
   140001080:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001083:	90                   	nop

0000000140001084 <.l_end>:
   140001084:	90                   	nop
   140001085:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001088:	48 83 c4 30          	add    rsp,0x30
   14000108c:	5d                   	pop    rbp
   14000108d:	c3                   	ret

000000014000108e <__tmainCRTStartup>:
   14000108e:	55                   	push   rbp
   14000108f:	48 89 e5             	mov    rbp,rsp
   140001092:	48 81 ec 90 00 00 00 	sub    rsp,0x90
   140001099:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
   1400010a0:	00 
   1400010a1:	c7 45 e0 30 00 00 00 	mov    DWORD PTR [rbp-0x20],0x30
   1400010a8:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   1400010ab:	65 67 48 8b 00       	mov    rax,QWORD PTR gs:[eax]
   1400010b0:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400010b4:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400010b8:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   1400010bc:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400010c0:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400010c7:	c7 45 e4 00 00 00 00 	mov    DWORD PTR [rbp-0x1c],0x0
   1400010ce:	eb 21                	jmp    1400010f1 <__tmainCRTStartup+0x63>
   1400010d0:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400010d4:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   1400010d8:	75 09                	jne    1400010e3 <__tmainCRTStartup+0x55>
   1400010da:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400010e1:	eb 45                	jmp    140001128 <__tmainCRTStartup+0x9a>
   1400010e3:	b9 e8 03 00 00       	mov    ecx,0x3e8
   1400010e8:	48 8b 05 e9 90 00 00 	mov    rax,QWORD PTR [rip+0x90e9]        # 14000a1d8 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 38 43 00 00 	mov    rax,QWORD PTR [rip+0x4338]        # 140005430 <.refptr.__native_startup_lock>
   1400010f8:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   1400010fc:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001100:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140001104:	48 c7 45 c0 00 00 00 	mov    QWORD PTR [rbp-0x40],0x0
   14000110b:	00 
   14000110c:	48 8b 4d c8          	mov    rcx,QWORD PTR [rbp-0x38]
   140001110:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001114:	48 8b 55 d0          	mov    rdx,QWORD PTR [rbp-0x30]
   140001118:	f0 48 0f b1 0a       	lock cmpxchg QWORD PTR [rdx],rcx
   14000111d:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001121:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001126:	75 a8                	jne    1400010d0 <__tmainCRTStartup+0x42>
   140001128:	48 8b 05 11 43 00 00 	mov    rax,QWORD PTR [rip+0x4311]        # 140005440 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 d8 20 00 00       	call   140003218 <_amsg_exit>
   140001140:	48 8b 05 f9 42 00 00 	mov    rax,QWORD PTR [rip+0x42f9]        # 140005440 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 e8 42 00 00 	mov    rax,QWORD PTR [rip+0x42e8]        # 140005440 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 58 20 00 00       	call   1400031c0 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 f7 20 00 00       	call   140003278 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 9f 20 00 00       	call   140003238 <abort>
   140001199:	e8 22 11 00 00       	call   1400022c0 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 1b 43 00 00 	mov    rax,QWORD PTR [rip+0x431b]        # 1400054c0 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 21 90 00 00 	mov    rax,QWORD PTR [rip+0x9021]        # 14000a1d0 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 68 42 00 00 	mov    rdx,QWORD PTR [rip+0x4268]        # 140005420 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 96 1f 00 00       	call   140003160 <_set_invalid_parameter_handler>
   1400011ca:	e8 01 1a 00 00       	call   140002bd0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 ff 41 00 00 	mov    rax,QWORD PTR [rip+0x41ff]        # 1400053e0 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 17 20 00 00       	call   140003208 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 0b 20 00 00       	call   140003208 <__set_app_type>
   1400011fd:	e8 2e 1f 00 00       	call   140003130 <__p__fmode>
   140001202:	48 8b 15 a7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42a7]        # 1400054b0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 2e 1f 00 00       	call   140003140 <__p__commode>
   140001212:	48 8b 15 77 42 00 00 	mov    rdx,QWORD PTR [rip+0x4277]        # 140005490 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 7e 06 00 00       	call   1400018a0 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 e3 1f 00 00       	call   140003218 <_amsg_exit>
   140001235:	48 8b 05 04 41 00 00 	mov    rax,QWORD PTR [rip+0x4104]        # 140005340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 86 42 00 00 	mov    rax,QWORD PTR [rip+0x4286]        # 1400054d0 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 88 11 00 00       	call   1400023da <__mingw_setusermatherr>
   140001252:	48 8b 05 47 41 00 00 	mov    rax,QWORD PTR [rip+0x4147]        # 1400053a0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 36 1f 00 00       	call   1400031a0 <_configthreadlocale>
   14000126a:	48 8b 15 0f 42 00 00 	mov    rdx,QWORD PTR [rip+0x420f]        # 140005480 <.refptr.__xi_z>
   140001271:	48 8b 05 f8 41 00 00 	mov    rax,QWORD PTR [rip+0x41f8]        # 140005470 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 50 1e 00 00       	call   1400030d0 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 8a 1f 00 00       	call   140003218 <_amsg_exit>
   14000128e:	48 8b 05 4b 42 00 00 	mov    rax,QWORD PTR [rip+0x424b]        # 1400054e0 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 ff 41 00 00 	mov    rax,QWORD PTR [rip+0x41ff]        # 1400054a0 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 7d 00 00 	lea    r10,[rip+0x7d65]        # 140009010 <envp>
   1400012ab:	48 8d 15 56 7d 00 00 	lea    rdx,[rip+0x7d56]        # 140009008 <argv>
   1400012b2:	48 8d 05 4b 7d 00 00 	lea    rax,[rip+0x7d4b]        # 140009004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 28 1f 00 00       	call   1400031f8 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 35 1f 00 00       	call   140003218 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 0e 1f 00 00       	call   140003218 <_amsg_exit>
   14000130a:	48 8b 15 4f 41 00 00 	mov    rdx,QWORD PTR [rip+0x414f]        # 140005460 <.refptr.__xc_z>
   140001311:	48 8b 05 38 41 00 00 	mov    rax,QWORD PTR [rip+0x4138]        # 140005450 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 08 1f 00 00       	call   140003228 <_initterm>
   140001320:	e8 52 05 00 00       	call   140001877 <__main>
   140001325:	48 8b 05 14 41 00 00 	mov    rax,QWORD PTR [rip+0x4114]        # 140005440 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de 7c 00 00 01 	mov    DWORD PTR [rip+0x7cde],0x1        # 14000901c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 e5 40 00 00 	mov    rax,QWORD PTR [rip+0x40e5]        # 140005430 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 27 40 00 00 	mov    rax,QWORD PTR [rip+0x4027]        # 140005390 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 18 40 00 00 	mov    rax,QWORD PTR [rip+0x4018]        # 140005390 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 be 1d 00 00       	call   140003150 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 56 1f 00 00       	call   140003310 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 77 1e 00 00       	call   140003248 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 40 1e 00 00       	call   140003220 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 f5 3f 00 00 	mov    rax,QWORD PTR [rip+0x3ff5]        # 1400053f0 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 f8 3f 00 00 	mov    rax,QWORD PTR [rip+0x3ff8]        # 140005400 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 fb 3f 00 00 	mov    rax,QWORD PTR [rip+0x3ffb]        # 140005410 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 3e 3f 00 00 	mov    rax,QWORD PTR [rip+0x3f3e]        # 140005360 <.refptr.__ImageBase>
   140001422:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001426:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000142a:	0f b7 00             	movzx  eax,WORD PTR [rax]
   14000142d:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140001431:	74 0a                	je     14000143d <check_managed_app+0x51>
   140001433:	b8 00 00 00 00       	mov    eax,0x0
   140001438:	e9 ad 00 00 00       	jmp    1400014ea <check_managed_app+0xfe>
   14000143d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001441:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140001444:	48 63 d0             	movsxd rdx,eax
   140001447:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000144b:	48 01 d0             	add    rax,rdx
   14000144e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001452:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001456:	8b 00                	mov    eax,DWORD PTR [rax]
   140001458:	3d 50 45 00 00       	cmp    eax,0x4550
   14000145d:	74 0a                	je     140001469 <check_managed_app+0x7d>
   14000145f:	b8 00 00 00 00       	mov    eax,0x0
   140001464:	e9 81 00 00 00       	jmp    1400014ea <check_managed_app+0xfe>
   140001469:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000146d:	48 83 c0 18          	add    rax,0x18
   140001471:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001475:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001479:	0f b7 00             	movzx  eax,WORD PTR [rax]
   14000147c:	0f b7 c0             	movzx  eax,ax
   14000147f:	3d 0b 01 00 00       	cmp    eax,0x10b
   140001484:	74 09                	je     14000148f <check_managed_app+0xa3>
   140001486:	3d 0b 02 00 00       	cmp    eax,0x20b
   14000148b:	74 29                	je     1400014b6 <check_managed_app+0xca>
   14000148d:	eb 56                	jmp    1400014e5 <check_managed_app+0xf9>
   14000148f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001493:	8b 40 5c             	mov    eax,DWORD PTR [rax+0x5c]
   140001496:	83 f8 0e             	cmp    eax,0xe
   140001499:	77 07                	ja     1400014a2 <check_managed_app+0xb6>
   14000149b:	b8 00 00 00 00       	mov    eax,0x0
   1400014a0:	eb 48                	jmp    1400014ea <check_managed_app+0xfe>
   1400014a2:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400014a6:	8b 80 d0 00 00 00    	mov    eax,DWORD PTR [rax+0xd0]
   1400014ac:	85 c0                	test   eax,eax
   1400014ae:	0f 95 c0             	setne  al
   1400014b1:	0f b6 c0             	movzx  eax,al
   1400014b4:	eb 34                	jmp    1400014ea <check_managed_app+0xfe>
   1400014b6:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400014ba:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400014be:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400014c2:	8b 40 6c             	mov    eax,DWORD PTR [rax+0x6c]
   1400014c5:	83 f8 0e             	cmp    eax,0xe
   1400014c8:	77 07                	ja     1400014d1 <check_managed_app+0xe5>
   1400014ca:	b8 00 00 00 00       	mov    eax,0x0
   1400014cf:	eb 19                	jmp    1400014ea <check_managed_app+0xfe>
   1400014d1:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400014d5:	8b 80 e0 00 00 00    	mov    eax,DWORD PTR [rax+0xe0]
   1400014db:	85 c0                	test   eax,eax
   1400014dd:	0f 95 c0             	setne  al
   1400014e0:	0f b6 c0             	movzx  eax,al
   1400014e3:	eb 05                	jmp    1400014ea <check_managed_app+0xfe>
   1400014e5:	b8 00 00 00 00       	mov    eax,0x0
   1400014ea:	48 83 c4 20          	add    rsp,0x20
   1400014ee:	5d                   	pop    rbp
   1400014ef:	c3                   	ret

00000001400014f0 <duplicate_ppstrings>:
   1400014f0:	55                   	push   rbp
   1400014f1:	53                   	push   rbx
   1400014f2:	48 83 ec 48          	sub    rsp,0x48
   1400014f6:	48 8d 6c 24 40       	lea    rbp,[rsp+0x40]
   1400014fb:	89 4d 20             	mov    DWORD PTR [rbp+0x20],ecx
   1400014fe:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001502:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140001505:	83 c0 01             	add    eax,0x1
   140001508:	48 98                	cdqe
   14000150a:	48 c1 e0 03          	shl    rax,0x3
   14000150e:	48 89 c1             	mov    rcx,rax
   140001511:	e8 52 1d 00 00       	call   140003268 <malloc>
   140001516:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000151a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000151f:	75 0a                	jne    14000152b <duplicate_ppstrings+0x3b>
   140001521:	b8 01 00 00 00       	mov    eax,0x1
   140001526:	e9 fd 00 00 00       	jmp    140001628 <duplicate_ppstrings+0x138>
   14000152b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000152f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001532:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001536:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000153d:	e9 af 00 00 00       	jmp    1400015f1 <duplicate_ppstrings+0x101>
   140001542:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001545:	48 98                	cdqe
   140001547:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   14000154e:	00 
   14000154f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001553:	48 01 d0             	add    rax,rdx
   140001556:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001559:	48 89 c1             	mov    rcx,rax
   14000155c:	e8 27 1d 00 00       	call   140003288 <strlen>
   140001561:	48 83 c0 01          	add    rax,0x1
   140001565:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001569:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000156c:	48 98                	cdqe
   14000156e:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140001575:	00 
   140001576:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000157a:	48 8d 1c 02          	lea    rbx,[rdx+rax*1]
   14000157e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001582:	48 89 c1             	mov    rcx,rax
   140001585:	e8 de 1c 00 00       	call   140003268 <malloc>
   14000158a:	48 89 03             	mov    QWORD PTR [rbx],rax
   14000158d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001590:	48 98                	cdqe
   140001592:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140001599:	00 
   14000159a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000159e:	48 01 d0             	add    rax,rdx
   1400015a1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400015a4:	48 85 c0             	test   rax,rax
   1400015a7:	75 07                	jne    1400015b0 <duplicate_ppstrings+0xc0>
   1400015a9:	b8 01 00 00 00       	mov    eax,0x1
   1400015ae:	eb 78                	jmp    140001628 <duplicate_ppstrings+0x138>
   1400015b0:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400015b3:	48 98                	cdqe
   1400015b5:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   1400015bc:	00 
   1400015bd:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400015c1:	48 01 d0             	add    rax,rdx
   1400015c4:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   1400015c7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400015ca:	48 98                	cdqe
   1400015cc:	48 8d 0c c5 00 00 00 	lea    rcx,[rax*8+0x0]
   1400015d3:	00 
   1400015d4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400015d8:	48 01 c8             	add    rax,rcx
   1400015db:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400015de:	48 8b 4d e0          	mov    rcx,QWORD PTR [rbp-0x20]
   1400015e2:	49 89 c8             	mov    r8,rcx
   1400015e5:	48 89 c1             	mov    rcx,rax
   1400015e8:	e8 83 1c 00 00       	call   140003270 <memcpy>
   1400015ed:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400015f1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400015f4:	3b 45 20             	cmp    eax,DWORD PTR [rbp+0x20]
   1400015f7:	0f 8c 45 ff ff ff    	jl     140001542 <duplicate_ppstrings+0x52>
   1400015fd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001600:	48 98                	cdqe
   140001602:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140001609:	00 
   14000160a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000160e:	48 01 d0             	add    rax,rdx
   140001611:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   140001618:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000161c:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140001620:	48 89 10             	mov    QWORD PTR [rax],rdx
   140001623:	b8 00 00 00 00       	mov    eax,0x0
   140001628:	48 83 c4 48          	add    rsp,0x48
   14000162c:	5b                   	pop    rbx
   14000162d:	5d                   	pop    rbp
   14000162e:	c3                   	ret

000000014000162f <atexit>:
   14000162f:	55                   	push   rbp
   140001630:	48 89 e5             	mov    rbp,rsp
   140001633:	48 83 ec 20          	sub    rsp,0x20
   140001637:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000163b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000163f:	48 89 c1             	mov    rcx,rax
   140001642:	e8 e9 1b 00 00       	call   140003230 <_crt_atexit>
   140001647:	48 83 c4 20          	add    rsp,0x20
   14000164b:	5d                   	pop    rbp
   14000164c:	c3                   	ret
   14000164d:	90                   	nop
   14000164e:	90                   	nop
   14000164f:	90                   	nop

0000000140001650 <.weak.__register_frame_info.hmod_libgcc>:
   140001650:	c3                   	ret
   140001651:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140001655:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000165c:	00 00 00 00 

0000000140001660 <.weak.__deregister_frame_info.hmod_libgcc>:
   140001660:	31 c0                	xor    eax,eax
   140001662:	c3                   	ret
   140001663:	66 90                	xchg   ax,ax
   140001665:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000166c:	00 00 00 00 

0000000140001670 <__gcc_register_frame>:
   140001670:	55                   	push   rbp
   140001671:	53                   	push   rbx
   140001672:	48 83 ec 38          	sub    rsp,0x38
   140001676:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   14000167b:	48 8d 0d 7e 39 00 00 	lea    rcx,[rip+0x397e]        # 140005000 <.rdata>
   140001682:	ff 15 20 8b 00 00    	call   QWORD PTR [rip+0x8b20]        # 14000a1a8 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 2b 8b 00 00    	call   QWORD PTR [rip+0x8b2b]        # 14000a1c8 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d 0c 8b 00 00 	mov    r9,QWORD PTR [rip+0x8b0c]        # 14000a1b0 <__imp_GetProcAddress>
   1400016a4:	48 8d 15 68 39 00 00 	lea    rdx,[rip+0x3968]        # 140005013 <.rdata+0x13>
   1400016ab:	48 89 d9             	mov    rcx,rbx
   1400016ae:	48 89 05 6b 79 00 00 	mov    QWORD PTR [rip+0x796b],rax        # 140009020 <hmod_libgcc>
   1400016b5:	4c 89 4d f0          	mov    QWORD PTR [rbp-0x10],r9
   1400016b9:	41 ff d1             	call   r9
   1400016bc:	48 8d 15 66 39 00 00 	lea    rdx,[rip+0x3966]        # 140005029 <.rdata+0x29>
   1400016c3:	48 89 d9             	mov    rcx,rbx
   1400016c6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400016ca:	ff 55 f0             	call   QWORD PTR [rbp-0x10]
   1400016cd:	4c 8b 45 f8          	mov    r8,QWORD PTR [rbp-0x8]
   1400016d1:	48 89 05 28 29 00 00 	mov    QWORD PTR [rip+0x2928],rax        # 140004000 <__data_start__>
   1400016d8:	4d 85 c0             	test   r8,r8
   1400016db:	74 11                	je     1400016ee <__gcc_register_frame+0x7e>
   1400016dd:	48 8d 15 5c 79 00 00 	lea    rdx,[rip+0x795c]        # 140009040 <obj>
   1400016e4:	48 8d 0d 15 49 00 00 	lea    rcx,[rip+0x4915]        # 140006000 <__EH_FRAME_BEGIN__>
   1400016eb:	41 ff d0             	call   r8
   1400016ee:	48 8d 0d 2b 00 00 00 	lea    rcx,[rip+0x2b]        # 140001720 <__gcc_deregister_frame>
   1400016f5:	48 83 c4 38          	add    rsp,0x38
   1400016f9:	5b                   	pop    rbx
   1400016fa:	5d                   	pop    rbp
   1400016fb:	e9 2f ff ff ff       	jmp    14000162f <atexit>
   140001700:	48 8d 05 59 ff ff ff 	lea    rax,[rip+0xffffffffffffff59]        # 140001660 <.weak.__deregister_frame_info.hmod_libgcc>
   140001707:	4c 8d 05 42 ff ff ff 	lea    r8,[rip+0xffffffffffffff42]        # 140001650 <.weak.__register_frame_info.hmod_libgcc>
   14000170e:	48 89 05 eb 28 00 00 	mov    QWORD PTR [rip+0x28eb],rax        # 140004000 <__data_start__>
   140001715:	eb c6                	jmp    1400016dd <__gcc_register_frame+0x6d>
   140001717:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000171e:	00 00 

0000000140001720 <__gcc_deregister_frame>:
   140001720:	55                   	push   rbp
   140001721:	48 89 e5             	mov    rbp,rsp
   140001724:	48 83 ec 20          	sub    rsp,0x20
   140001728:	48 8b 05 d1 28 00 00 	mov    rax,QWORD PTR [rip+0x28d1]        # 140004000 <__data_start__>
   14000172f:	48 85 c0             	test   rax,rax
   140001732:	74 09                	je     14000173d <__gcc_deregister_frame+0x1d>
   140001734:	48 8d 0d c5 48 00 00 	lea    rcx,[rip+0x48c5]        # 140006000 <__EH_FRAME_BEGIN__>
   14000173b:	ff d0                	call   rax
   14000173d:	48 8b 0d dc 78 00 00 	mov    rcx,QWORD PTR [rip+0x78dc]        # 140009020 <hmod_libgcc>
   140001744:	48 85 c9             	test   rcx,rcx
   140001747:	74 0f                	je     140001758 <__gcc_deregister_frame+0x38>
   140001749:	48 83 c4 20          	add    rsp,0x20
   14000174d:	5d                   	pop    rbp
   14000174e:	48 ff 25 43 8a 00 00 	rex.W jmp QWORD PTR [rip+0x8a43]        # 14000a198 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <dispatch_visit(std::variant<A, B, C> const&)>:
   140001760:	0f b6 41 04          	movzx  eax,BYTE PTR [rcx+0x4]
   140001764:	3c 01                	cmp    al,0x1
   140001766:	74 10                	je     140001778 <dispatch_visit(std::variant<A, B, C> const&)+0x18>
   140001768:	3c 02                	cmp    al,0x2
   14000176a:	8b 01                	mov    eax,DWORD PTR [rcx]
   14000176c:	75 03                	jne    140001771 <dispatch_visit(std::variant<A, B, C> const&)+0x11>
   14000176e:	8d 04 40             	lea    eax,[rax+rax*2]
   140001771:	c3                   	ret
   140001772:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
   140001778:	8b 01                	mov    eax,DWORD PTR [rcx]
   14000177a:	01 c0                	add    eax,eax
   14000177c:	c3                   	ret
   14000177d:	0f 1f 00             	nop    DWORD PTR [rax]

0000000140001780 <dispatch_manual(std::variant<A, B, C> const&)>:
   140001780:	0f b6 41 04          	movzx  eax,BYTE PTR [rcx+0x4]
   140001784:	3c 01                	cmp    al,0x1
   140001786:	74 28                	je     1400017b0 <dispatch_manual(std::variant<A, B, C> const&)+0x30>
   140001788:	3c 02                	cmp    al,0x2
   14000178a:	74 14                	je     1400017a0 <dispatch_manual(std::variant<A, B, C> const&)+0x20>
   14000178c:	31 d2                	xor    edx,edx
   14000178e:	84 c0                	test   al,al
   140001790:	75 02                	jne    140001794 <dispatch_manual(std::variant<A, B, C> const&)+0x14>
   140001792:	8b 11                	mov    edx,DWORD PTR [rcx]
   140001794:	89 d0                	mov    eax,edx
   140001796:	c3                   	ret
   140001797:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000179e:	00 00 
   1400017a0:	8b 01                	mov    eax,DWORD PTR [rcx]
   1400017a2:	8d 14 40             	lea    edx,[rax+rax*2]
   1400017a5:	89 d0                	mov    eax,edx
   1400017a7:	c3                   	ret
   1400017a8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   1400017af:	00 
   1400017b0:	8b 11                	mov    edx,DWORD PTR [rcx]
   1400017b2:	01 d2                	add    edx,edx
   1400017b4:	89 d0                	mov    eax,edx
   1400017b6:	c3                   	ret
   1400017b7:	90                   	nop
   1400017b8:	90                   	nop
   1400017b9:	90                   	nop
   1400017ba:	90                   	nop
   1400017bb:	90                   	nop
   1400017bc:	90                   	nop
   1400017bd:	90                   	nop
   1400017be:	90                   	nop
   1400017bf:	90                   	nop

00000001400017c0 <__do_global_dtors>:
   1400017c0:	55                   	push   rbp
   1400017c1:	48 89 e5             	mov    rbp,rsp
   1400017c4:	48 83 ec 20          	sub    rsp,0x20
   1400017c8:	eb 1e                	jmp    1400017e8 <__do_global_dtors+0x28>
   1400017ca:	48 8b 05 3f 28 00 00 	mov    rax,QWORD PTR [rip+0x283f]        # 140004010 <p.0>
   1400017d1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017d4:	ff d0                	call   rax
   1400017d6:	48 8b 05 33 28 00 00 	mov    rax,QWORD PTR [rip+0x2833]        # 140004010 <p.0>
   1400017dd:	48 83 c0 08          	add    rax,0x8
   1400017e1:	48 89 05 28 28 00 00 	mov    QWORD PTR [rip+0x2828],rax        # 140004010 <p.0>
   1400017e8:	48 8b 05 21 28 00 00 	mov    rax,QWORD PTR [rip+0x2821]        # 140004010 <p.0>
   1400017ef:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017f2:	48 85 c0             	test   rax,rax
   1400017f5:	75 d3                	jne    1400017ca <__do_global_dtors+0xa>
   1400017f7:	90                   	nop
   1400017f8:	90                   	nop
   1400017f9:	48 83 c4 20          	add    rsp,0x20
   1400017fd:	5d                   	pop    rbp
   1400017fe:	c3                   	ret

00000001400017ff <__do_global_ctors>:
   1400017ff:	55                   	push   rbp
   140001800:	48 89 e5             	mov    rbp,rsp
   140001803:	48 83 ec 30          	sub    rsp,0x30
   140001807:	48 8b 05 42 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b42]        # 140005350 <.refptr.__CTOR_LIST__>
   14000180e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001811:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001814:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   140001818:	75 25                	jne    14000183f <__do_global_ctors+0x40>
   14000181a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001821:	eb 04                	jmp    140001827 <__do_global_ctors+0x28>
   140001823:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001827:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000182a:	8d 50 01             	lea    edx,[rax+0x1]
   14000182d:	48 8b 05 1c 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b1c]        # 140005350 <.refptr.__CTOR_LIST__>
   140001834:	89 d2                	mov    edx,edx
   140001836:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000183a:	48 85 c0             	test   rax,rax
   14000183d:	75 e4                	jne    140001823 <__do_global_ctors+0x24>
   14000183f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001842:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001845:	eb 14                	jmp    14000185b <__do_global_ctors+0x5c>
   140001847:	48 8b 05 02 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b02]        # 140005350 <.refptr.__CTOR_LIST__>
   14000184e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001851:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001855:	ff d0                	call   rax
   140001857:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000185b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000185f:	75 e6                	jne    140001847 <__do_global_ctors+0x48>
   140001861:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 1400017c0 <__do_global_dtors>
   140001868:	48 89 c1             	mov    rcx,rax
   14000186b:	e8 bf fd ff ff       	call   14000162f <atexit>
   140001870:	90                   	nop
   140001871:	48 83 c4 30          	add    rsp,0x30
   140001875:	5d                   	pop    rbp
   140001876:	c3                   	ret

0000000140001877 <__main>:
   140001877:	55                   	push   rbp
   140001878:	48 89 e5             	mov    rbp,rsp
   14000187b:	48 83 ec 20          	sub    rsp,0x20
   14000187f:	8b 05 fb 77 00 00    	mov    eax,DWORD PTR [rip+0x77fb]        # 140009080 <initialized>
   140001885:	85 c0                	test   eax,eax
   140001887:	75 0f                	jne    140001898 <__main+0x21>
   140001889:	c7 05 ed 77 00 00 01 	mov    DWORD PTR [rip+0x77ed],0x1        # 140009080 <initialized>
   140001890:	00 00 00 
   140001893:	e8 67 ff ff ff       	call   1400017ff <__do_global_ctors>
   140001898:	90                   	nop
   140001899:	48 83 c4 20          	add    rsp,0x20
   14000189d:	5d                   	pop    rbp
   14000189e:	c3                   	ret
   14000189f:	90                   	nop

00000001400018a0 <_setargv>:
   1400018a0:	55                   	push   rbp
   1400018a1:	48 89 e5             	mov    rbp,rsp
   1400018a4:	b8 00 00 00 00       	mov    eax,0x0
   1400018a9:	5d                   	pop    rbp
   1400018aa:	c3                   	ret
   1400018ab:	90                   	nop
   1400018ac:	90                   	nop
   1400018ad:	90                   	nop
   1400018ae:	90                   	nop
   1400018af:	90                   	nop

00000001400018b0 <__dyn_tls_init>:
   1400018b0:	55                   	push   rbp
   1400018b1:	48 89 e5             	mov    rbp,rsp
   1400018b4:	48 83 ec 30          	sub    rsp,0x30
   1400018b8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400018bc:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   1400018bf:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400018c3:	48 8b 05 66 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a66]        # 140005330 <.refptr._CRT_MT>
   1400018ca:	8b 00                	mov    eax,DWORD PTR [rax]
   1400018cc:	83 f8 02             	cmp    eax,0x2
   1400018cf:	74 0d                	je     1400018de <__dyn_tls_init+0x2e>
   1400018d1:	48 8b 05 58 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a58]        # 140005330 <.refptr._CRT_MT>
   1400018d8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   1400018de:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   1400018e2:	74 1e                	je     140001902 <__dyn_tls_init+0x52>
   1400018e4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   1400018e8:	75 5b                	jne    140001945 <__dyn_tls_init+0x95>
   1400018ea:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400018ee:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400018f1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400018f5:	49 89 c8             	mov    r8,rcx
   1400018f8:	48 89 c1             	mov    rcx,rax
   1400018fb:	e8 d1 11 00 00       	call   140002ad1 <__mingw_TLScallback>
   140001900:	eb 43                	jmp    140001945 <__dyn_tls_init+0x95>
   140001902:	48 8d 05 8f 3d 00 00 	lea    rax,[rip+0x3d8f]        # 140005698 <___crt_xd_start__>
   140001909:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000190d:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001912:	eb 22                	jmp    140001936 <__dyn_tls_init+0x86>
   140001914:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001918:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000191c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001920:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001923:	48 85 c0             	test   rax,rax
   140001926:	74 09                	je     140001931 <__dyn_tls_init+0x81>
   140001928:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000192c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000192f:	ff d0                	call   rax
   140001931:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001936:	48 8d 05 63 3d 00 00 	lea    rax,[rip+0x3d63]        # 1400056a0 <__xd_z>
   14000193d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001941:	75 d1                	jne    140001914 <__dyn_tls_init+0x64>
   140001943:	eb 01                	jmp    140001946 <__dyn_tls_init+0x96>
   140001945:	90                   	nop
   140001946:	48 83 c4 30          	add    rsp,0x30
   14000194a:	5d                   	pop    rbp
   14000194b:	c3                   	ret

000000014000194c <__tlregdtor>:
   14000194c:	55                   	push   rbp
   14000194d:	48 89 e5             	mov    rbp,rsp
   140001950:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001954:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001959:	75 07                	jne    140001962 <__tlregdtor+0x16>
   14000195b:	b8 00 00 00 00       	mov    eax,0x0
   140001960:	eb 05                	jmp    140001967 <__tlregdtor+0x1b>
   140001962:	b8 00 00 00 00       	mov    eax,0x0
   140001967:	5d                   	pop    rbp
   140001968:	c3                   	ret

0000000140001969 <__dyn_tls_dtor>:
   140001969:	55                   	push   rbp
   14000196a:	48 89 e5             	mov    rbp,rsp
   14000196d:	48 83 ec 20          	sub    rsp,0x20
   140001971:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001975:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001978:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000197c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001980:	74 06                	je     140001988 <__dyn_tls_dtor+0x1f>
   140001982:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001986:	75 18                	jne    1400019a0 <__dyn_tls_dtor+0x37>
   140001988:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   14000198c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   14000198f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001993:	49 89 c8             	mov    r8,rcx
   140001996:	48 89 c1             	mov    rcx,rax
   140001999:	e8 33 11 00 00       	call   140002ad1 <__mingw_TLScallback>
   14000199e:	eb 01                	jmp    1400019a1 <__dyn_tls_dtor+0x38>
   1400019a0:	90                   	nop
   1400019a1:	48 83 c4 20          	add    rsp,0x20
   1400019a5:	5d                   	pop    rbp
   1400019a6:	c3                   	ret
   1400019a7:	90                   	nop
   1400019a8:	90                   	nop
   1400019a9:	90                   	nop
   1400019aa:	90                   	nop
   1400019ab:	90                   	nop
   1400019ac:	90                   	nop
   1400019ad:	90                   	nop
   1400019ae:	90                   	nop
   1400019af:	90                   	nop

00000001400019b0 <_matherr>:
   1400019b0:	55                   	push   rbp
   1400019b1:	53                   	push   rbx
   1400019b2:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   1400019b9:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   1400019be:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   1400019c2:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   1400019c6:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   1400019cb:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   1400019cf:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   1400019d3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400019d5:	83 f8 06             	cmp    eax,0x6
   1400019d8:	74 56                	je     140001a30 <_matherr+0x80>
   1400019da:	83 f8 06             	cmp    eax,0x6
   1400019dd:	7f 78                	jg     140001a57 <_matherr+0xa7>
   1400019df:	83 f8 05             	cmp    eax,0x5
   1400019e2:	74 59                	je     140001a3d <_matherr+0x8d>
   1400019e4:	83 f8 05             	cmp    eax,0x5
   1400019e7:	7f 6e                	jg     140001a57 <_matherr+0xa7>
   1400019e9:	83 f8 04             	cmp    eax,0x4
   1400019ec:	74 5c                	je     140001a4a <_matherr+0x9a>
   1400019ee:	83 f8 04             	cmp    eax,0x4
   1400019f1:	7f 64                	jg     140001a57 <_matherr+0xa7>
   1400019f3:	83 f8 03             	cmp    eax,0x3
   1400019f6:	74 2b                	je     140001a23 <_matherr+0x73>
   1400019f8:	83 f8 03             	cmp    eax,0x3
   1400019fb:	7f 5a                	jg     140001a57 <_matherr+0xa7>
   1400019fd:	83 f8 01             	cmp    eax,0x1
   140001a00:	74 07                	je     140001a09 <_matherr+0x59>
   140001a02:	83 f8 02             	cmp    eax,0x2
   140001a05:	74 0f                	je     140001a16 <_matherr+0x66>
   140001a07:	eb 4e                	jmp    140001a57 <_matherr+0xa7>
   140001a09:	48 8d 05 90 36 00 00 	lea    rax,[rip+0x3690]        # 1400050a0 <.rdata>
   140001a10:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a14:	eb 4d                	jmp    140001a63 <_matherr+0xb3>
   140001a16:	48 8d 05 a2 36 00 00 	lea    rax,[rip+0x36a2]        # 1400050bf <.rdata+0x1f>
   140001a1d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a21:	eb 40                	jmp    140001a63 <_matherr+0xb3>
   140001a23:	48 8d 05 b6 36 00 00 	lea    rax,[rip+0x36b6]        # 1400050e0 <.rdata+0x40>
   140001a2a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a2e:	eb 33                	jmp    140001a63 <_matherr+0xb3>
   140001a30:	48 8d 05 c9 36 00 00 	lea    rax,[rip+0x36c9]        # 140005100 <.rdata+0x60>
   140001a37:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a3b:	eb 26                	jmp    140001a63 <_matherr+0xb3>
   140001a3d:	48 8d 05 e4 36 00 00 	lea    rax,[rip+0x36e4]        # 140005128 <.rdata+0x88>
   140001a44:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a48:	eb 19                	jmp    140001a63 <_matherr+0xb3>
   140001a4a:	48 8d 05 ff 36 00 00 	lea    rax,[rip+0x36ff]        # 140005150 <.rdata+0xb0>
   140001a51:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a55:	eb 0c                	jmp    140001a63 <_matherr+0xb3>
   140001a57:	48 8d 05 28 37 00 00 	lea    rax,[rip+0x3728]        # 140005186 <.rdata+0xe6>
   140001a5e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a62:	90                   	nop
   140001a63:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a67:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001a6d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a71:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001a76:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a7a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001a7f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a83:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001a87:	b9 02 00 00 00       	mov    ecx,0x2
   140001a8c:	e8 2f 17 00 00       	call   1400031c0 <__acrt_iob_func>
   140001a91:	48 89 c1             	mov    rcx,rax
   140001a94:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001a98:	48 8d 05 f9 36 00 00 	lea    rax,[rip+0x36f9]        # 140005198 <.rdata+0xf8>
   140001a9f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001aa6:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001aac:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001ab2:	49 89 d9             	mov    r9,rbx
   140001ab5:	49 89 d0             	mov    r8,rdx
   140001ab8:	48 89 c2             	mov    rdx,rax
   140001abb:	e8 98 17 00 00       	call   140003258 <fprintf>
   140001ac0:	b8 00 00 00 00       	mov    eax,0x0
   140001ac5:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001ac9:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001acd:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001ad2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001ad9:	5b                   	pop    rbx
   140001ada:	5d                   	pop    rbp
   140001adb:	c3                   	ret
   140001adc:	90                   	nop
   140001add:	90                   	nop
   140001ade:	90                   	nop
   140001adf:	90                   	nop

0000000140001ae0 <__report_error>:
   140001ae0:	55                   	push   rbp
   140001ae1:	53                   	push   rbx
   140001ae2:	48 83 ec 38          	sub    rsp,0x38
   140001ae6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001aeb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001aef:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001af3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001af7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001afb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001aff:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b03:	b9 02 00 00 00       	mov    ecx,0x2
   140001b08:	e8 b3 16 00 00       	call   1400031c0 <__acrt_iob_func>
   140001b0d:	48 89 c1             	mov    rcx,rax
   140001b10:	48 8d 05 b9 36 00 00 	lea    rax,[rip+0x36b9]        # 1400051d0 <.rdata>
   140001b17:	48 89 c2             	mov    rdx,rax
   140001b1a:	e8 39 17 00 00       	call   140003258 <fprintf>
   140001b1f:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001b23:	b9 02 00 00 00       	mov    ecx,0x2
   140001b28:	e8 93 16 00 00       	call   1400031c0 <__acrt_iob_func>
   140001b2d:	48 89 c1             	mov    rcx,rax
   140001b30:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001b34:	49 89 d8             	mov    r8,rbx
   140001b37:	48 89 c2             	mov    rdx,rax
   140001b3a:	e8 59 17 00 00       	call   140003298 <vfprintf>
   140001b3f:	e8 f4 16 00 00       	call   140003238 <abort>
   140001b44:	90                   	nop

0000000140001b45 <mark_section_writable>:
   140001b45:	55                   	push   rbp
   140001b46:	48 89 e5             	mov    rbp,rsp
   140001b49:	48 83 ec 60          	sub    rsp,0x60
   140001b4d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b51:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b58:	e9 82 00 00 00       	jmp    140001bdf <mark_section_writable+0x9a>
   140001b5d:	48 8b 0d 7c 75 00 00 	mov    rcx,QWORD PTR [rip+0x757c]        # 1400090e0 <the_secs>
   140001b64:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b67:	48 63 d0             	movsxd rdx,eax
   140001b6a:	48 89 d0             	mov    rax,rdx
   140001b6d:	48 c1 e0 02          	shl    rax,0x2
   140001b71:	48 01 d0             	add    rax,rdx
   140001b74:	48 c1 e0 03          	shl    rax,0x3
   140001b78:	48 01 c8             	add    rax,rcx
   140001b7b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001b7f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001b83:	72 56                	jb     140001bdb <mark_section_writable+0x96>
   140001b85:	48 8b 0d 54 75 00 00 	mov    rcx,QWORD PTR [rip+0x7554]        # 1400090e0 <the_secs>
   140001b8c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b8f:	48 63 d0             	movsxd rdx,eax
   140001b92:	48 89 d0             	mov    rax,rdx
   140001b95:	48 c1 e0 02          	shl    rax,0x2
   140001b99:	48 01 d0             	add    rax,rdx
   140001b9c:	48 c1 e0 03          	shl    rax,0x3
   140001ba0:	48 01 c8             	add    rax,rcx
   140001ba3:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001ba7:	4c 8b 05 32 75 00 00 	mov    r8,QWORD PTR [rip+0x7532]        # 1400090e0 <the_secs>
   140001bae:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001bb1:	48 63 d0             	movsxd rdx,eax
   140001bb4:	48 89 d0             	mov    rax,rdx
   140001bb7:	48 c1 e0 02          	shl    rax,0x2
   140001bbb:	48 01 d0             	add    rax,rdx
   140001bbe:	48 c1 e0 03          	shl    rax,0x3
   140001bc2:	4c 01 c0             	add    rax,r8
   140001bc5:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001bc9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001bcc:	89 c0                	mov    eax,eax
   140001bce:	48 01 c8             	add    rax,rcx
   140001bd1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001bd5:	0f 82 41 02 00 00    	jb     140001e1c <mark_section_writable+0x2d7>
   140001bdb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001bdf:	8b 05 03 75 00 00    	mov    eax,DWORD PTR [rip+0x7503]        # 1400090e8 <maxSections>
   140001be5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001be8:	0f 8c 6f ff ff ff    	jl     140001b5d <mark_section_writable+0x18>
   140001bee:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bf2:	48 89 c1             	mov    rcx,rax
   140001bf5:	e8 c1 11 00 00       	call   140002dbb <__mingw_GetSectionForAddress>
   140001bfa:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001bfe:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001c03:	75 13                	jne    140001c18 <mark_section_writable+0xd3>
   140001c05:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001c09:	48 8d 0d e0 35 00 00 	lea    rcx,[rip+0x35e0]        # 1400051f0 <.rdata+0x20>
   140001c10:	48 89 c2             	mov    rdx,rax
   140001c13:	e8 c8 fe ff ff       	call   140001ae0 <__report_error>
   140001c18:	48 8b 0d c1 74 00 00 	mov    rcx,QWORD PTR [rip+0x74c1]        # 1400090e0 <the_secs>
   140001c1f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c22:	48 63 d0             	movsxd rdx,eax
   140001c25:	48 89 d0             	mov    rax,rdx
   140001c28:	48 c1 e0 02          	shl    rax,0x2
   140001c2c:	48 01 d0             	add    rax,rdx
   140001c2f:	48 c1 e0 03          	shl    rax,0x3
   140001c33:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001c37:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c3b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001c3f:	48 8b 0d 9a 74 00 00 	mov    rcx,QWORD PTR [rip+0x749a]        # 1400090e0 <the_secs>
   140001c46:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c49:	48 63 d0             	movsxd rdx,eax
   140001c4c:	48 89 d0             	mov    rax,rdx
   140001c4f:	48 c1 e0 02          	shl    rax,0x2
   140001c53:	48 01 d0             	add    rax,rdx
   140001c56:	48 c1 e0 03          	shl    rax,0x3
   140001c5a:	48 01 c8             	add    rax,rcx
   140001c5d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001c63:	e8 9f 12 00 00       	call   140002f07 <_GetPEImageBase>
   140001c68:	48 89 c1             	mov    rcx,rax
   140001c6b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c6f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001c72:	41 89 c1             	mov    r9d,eax
   140001c75:	4c 8b 05 64 74 00 00 	mov    r8,QWORD PTR [rip+0x7464]        # 1400090e0 <the_secs>
   140001c7c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c7f:	48 63 d0             	movsxd rdx,eax
   140001c82:	48 89 d0             	mov    rax,rdx
   140001c85:	48 c1 e0 02          	shl    rax,0x2
   140001c89:	48 01 d0             	add    rax,rdx
   140001c8c:	48 c1 e0 03          	shl    rax,0x3
   140001c90:	4c 01 c0             	add    rax,r8
   140001c93:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001c97:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001c9b:	48 8b 0d 3e 74 00 00 	mov    rcx,QWORD PTR [rip+0x743e]        # 1400090e0 <the_secs>
   140001ca2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ca5:	48 63 d0             	movsxd rdx,eax
   140001ca8:	48 89 d0             	mov    rax,rdx
   140001cab:	48 c1 e0 02          	shl    rax,0x2
   140001caf:	48 01 d0             	add    rax,rdx
   140001cb2:	48 c1 e0 03          	shl    rax,0x3
   140001cb6:	48 01 c8             	add    rax,rcx
   140001cb9:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001cbd:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001cc1:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001cc7:	48 89 c1             	mov    rcx,rax
   140001cca:	48 8b 05 1f 85 00 00 	mov    rax,QWORD PTR [rip+0x851f]        # 14000a1f0 <__imp_VirtualQuery>
   140001cd1:	ff d0                	call   rax
   140001cd3:	48 85 c0             	test   rax,rax
   140001cd6:	75 3f                	jne    140001d17 <mark_section_writable+0x1d2>
   140001cd8:	48 8b 0d 01 74 00 00 	mov    rcx,QWORD PTR [rip+0x7401]        # 1400090e0 <the_secs>
   140001cdf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ce2:	48 63 d0             	movsxd rdx,eax
   140001ce5:	48 89 d0             	mov    rax,rdx
   140001ce8:	48 c1 e0 02          	shl    rax,0x2
   140001cec:	48 01 d0             	add    rax,rdx
   140001cef:	48 c1 e0 03          	shl    rax,0x3
   140001cf3:	48 01 c8             	add    rax,rcx
   140001cf6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001cfa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001cfe:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001d01:	89 c1                	mov    ecx,eax
   140001d03:	48 8d 05 06 35 00 00 	lea    rax,[rip+0x3506]        # 140005210 <.rdata+0x40>
   140001d0a:	49 89 d0             	mov    r8,rdx
   140001d0d:	89 ca                	mov    edx,ecx
   140001d0f:	48 89 c1             	mov    rcx,rax
   140001d12:	e8 c9 fd ff ff       	call   140001ae0 <__report_error>
   140001d17:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d1a:	83 f8 40             	cmp    eax,0x40
   140001d1d:	0f 84 e8 00 00 00    	je     140001e0b <mark_section_writable+0x2c6>
   140001d23:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d26:	83 f8 04             	cmp    eax,0x4
   140001d29:	0f 84 dc 00 00 00    	je     140001e0b <mark_section_writable+0x2c6>
   140001d2f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d32:	3d 80 00 00 00       	cmp    eax,0x80
   140001d37:	0f 84 ce 00 00 00    	je     140001e0b <mark_section_writable+0x2c6>
   140001d3d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d40:	83 f8 08             	cmp    eax,0x8
   140001d43:	0f 84 c2 00 00 00    	je     140001e0b <mark_section_writable+0x2c6>
   140001d49:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d4c:	83 f8 02             	cmp    eax,0x2
   140001d4f:	75 09                	jne    140001d5a <mark_section_writable+0x215>
   140001d51:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001d58:	eb 07                	jmp    140001d61 <mark_section_writable+0x21c>
   140001d5a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001d61:	48 8b 0d 78 73 00 00 	mov    rcx,QWORD PTR [rip+0x7378]        # 1400090e0 <the_secs>
   140001d68:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d6b:	48 63 d0             	movsxd rdx,eax
   140001d6e:	48 89 d0             	mov    rax,rdx
   140001d71:	48 c1 e0 02          	shl    rax,0x2
   140001d75:	48 01 d0             	add    rax,rdx
   140001d78:	48 c1 e0 03          	shl    rax,0x3
   140001d7c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d80:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d84:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001d88:	48 8b 0d 51 73 00 00 	mov    rcx,QWORD PTR [rip+0x7351]        # 1400090e0 <the_secs>
   140001d8f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d92:	48 63 d0             	movsxd rdx,eax
   140001d95:	48 89 d0             	mov    rax,rdx
   140001d98:	48 c1 e0 02          	shl    rax,0x2
   140001d9c:	48 01 d0             	add    rax,rdx
   140001d9f:	48 c1 e0 03          	shl    rax,0x3
   140001da3:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001da7:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001dab:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001daf:	48 8b 0d 2a 73 00 00 	mov    rcx,QWORD PTR [rip+0x732a]        # 1400090e0 <the_secs>
   140001db6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001db9:	48 63 d0             	movsxd rdx,eax
   140001dbc:	48 89 d0             	mov    rax,rdx
   140001dbf:	48 c1 e0 02          	shl    rax,0x2
   140001dc3:	48 01 d0             	add    rax,rdx
   140001dc6:	48 c1 e0 03          	shl    rax,0x3
   140001dca:	48 01 c8             	add    rax,rcx
   140001dcd:	49 89 c0             	mov    r8,rax
   140001dd0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001dd4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001dd8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001ddb:	4d 89 c1             	mov    r9,r8
   140001dde:	41 89 c8             	mov    r8d,ecx
   140001de1:	48 89 c1             	mov    rcx,rax
   140001de4:	48 8b 05 fd 83 00 00 	mov    rax,QWORD PTR [rip+0x83fd]        # 14000a1e8 <__imp_VirtualProtect>
   140001deb:	ff d0                	call   rax
   140001ded:	85 c0                	test   eax,eax
   140001def:	75 1a                	jne    140001e0b <mark_section_writable+0x2c6>
   140001df1:	48 8b 05 a8 83 00 00 	mov    rax,QWORD PTR [rip+0x83a8]        # 14000a1a0 <__imp_GetLastError>
   140001df8:	ff d0                	call   rax
   140001dfa:	89 c2                	mov    edx,eax
   140001dfc:	48 8d 05 45 34 00 00 	lea    rax,[rip+0x3445]        # 140005248 <.rdata+0x78>
   140001e03:	48 89 c1             	mov    rcx,rax
   140001e06:	e8 d5 fc ff ff       	call   140001ae0 <__report_error>
   140001e0b:	8b 05 d7 72 00 00    	mov    eax,DWORD PTR [rip+0x72d7]        # 1400090e8 <maxSections>
   140001e11:	83 c0 01             	add    eax,0x1
   140001e14:	89 05 ce 72 00 00    	mov    DWORD PTR [rip+0x72ce],eax        # 1400090e8 <maxSections>
   140001e1a:	eb 01                	jmp    140001e1d <mark_section_writable+0x2d8>
   140001e1c:	90                   	nop
   140001e1d:	48 83 c4 60          	add    rsp,0x60
   140001e21:	5d                   	pop    rbp
   140001e22:	c3                   	ret

0000000140001e23 <restore_modified_sections>:
   140001e23:	55                   	push   rbp
   140001e24:	48 89 e5             	mov    rbp,rsp
   140001e27:	48 83 ec 30          	sub    rsp,0x30
   140001e2b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001e32:	e9 ad 00 00 00       	jmp    140001ee4 <restore_modified_sections+0xc1>
   140001e37:	48 8b 0d a2 72 00 00 	mov    rcx,QWORD PTR [rip+0x72a2]        # 1400090e0 <the_secs>
   140001e3e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e41:	48 63 d0             	movsxd rdx,eax
   140001e44:	48 89 d0             	mov    rax,rdx
   140001e47:	48 c1 e0 02          	shl    rax,0x2
   140001e4b:	48 01 d0             	add    rax,rdx
   140001e4e:	48 c1 e0 03          	shl    rax,0x3
   140001e52:	48 01 c8             	add    rax,rcx
   140001e55:	8b 00                	mov    eax,DWORD PTR [rax]
   140001e57:	85 c0                	test   eax,eax
   140001e59:	0f 84 80 00 00 00    	je     140001edf <restore_modified_sections+0xbc>
   140001e5f:	48 8b 0d 7a 72 00 00 	mov    rcx,QWORD PTR [rip+0x727a]        # 1400090e0 <the_secs>
   140001e66:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e69:	48 63 d0             	movsxd rdx,eax
   140001e6c:	48 89 d0             	mov    rax,rdx
   140001e6f:	48 c1 e0 02          	shl    rax,0x2
   140001e73:	48 01 d0             	add    rax,rdx
   140001e76:	48 c1 e0 03          	shl    rax,0x3
   140001e7a:	48 01 c8             	add    rax,rcx
   140001e7d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001e80:	48 8b 0d 59 72 00 00 	mov    rcx,QWORD PTR [rip+0x7259]        # 1400090e0 <the_secs>
   140001e87:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e8a:	48 63 d0             	movsxd rdx,eax
   140001e8d:	48 89 d0             	mov    rax,rdx
   140001e90:	48 c1 e0 02          	shl    rax,0x2
   140001e94:	48 01 d0             	add    rax,rdx
   140001e97:	48 c1 e0 03          	shl    rax,0x3
   140001e9b:	48 01 c8             	add    rax,rcx
   140001e9e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001ea2:	4c 8b 05 37 72 00 00 	mov    r8,QWORD PTR [rip+0x7237]        # 1400090e0 <the_secs>
   140001ea9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001eac:	48 63 d0             	movsxd rdx,eax
   140001eaf:	48 89 d0             	mov    rax,rdx
   140001eb2:	48 c1 e0 02          	shl    rax,0x2
   140001eb6:	48 01 d0             	add    rax,rdx
   140001eb9:	48 c1 e0 03          	shl    rax,0x3
   140001ebd:	4c 01 c0             	add    rax,r8
   140001ec0:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001ec4:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001ec8:	49 89 d1             	mov    r9,rdx
   140001ecb:	45 89 d0             	mov    r8d,r10d
   140001ece:	48 89 ca             	mov    rdx,rcx
   140001ed1:	48 89 c1             	mov    rcx,rax
   140001ed4:	48 8b 05 0d 83 00 00 	mov    rax,QWORD PTR [rip+0x830d]        # 14000a1e8 <__imp_VirtualProtect>
   140001edb:	ff d0                	call   rax
   140001edd:	eb 01                	jmp    140001ee0 <restore_modified_sections+0xbd>
   140001edf:	90                   	nop
   140001ee0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001ee4:	8b 05 fe 71 00 00    	mov    eax,DWORD PTR [rip+0x71fe]        # 1400090e8 <maxSections>
   140001eea:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001eed:	0f 8c 44 ff ff ff    	jl     140001e37 <restore_modified_sections+0x14>
   140001ef3:	90                   	nop
   140001ef4:	90                   	nop
   140001ef5:	48 83 c4 30          	add    rsp,0x30
   140001ef9:	5d                   	pop    rbp
   140001efa:	c3                   	ret

0000000140001efb <__write_memory>:
   140001efb:	55                   	push   rbp
   140001efc:	48 89 e5             	mov    rbp,rsp
   140001eff:	48 83 ec 20          	sub    rsp,0x20
   140001f03:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f07:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f0b:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f0f:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140001f14:	74 25                	je     140001f3b <__write_memory+0x40>
   140001f16:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f1a:	48 89 c1             	mov    rcx,rax
   140001f1d:	e8 23 fc ff ff       	call   140001b45 <mark_section_writable>
   140001f22:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001f26:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140001f2a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f2e:	49 89 c8             	mov    r8,rcx
   140001f31:	48 89 c1             	mov    rcx,rax
   140001f34:	e8 37 13 00 00       	call   140003270 <memcpy>
   140001f39:	eb 01                	jmp    140001f3c <__write_memory+0x41>
   140001f3b:	90                   	nop
   140001f3c:	48 83 c4 20          	add    rsp,0x20
   140001f40:	5d                   	pop    rbp
   140001f41:	c3                   	ret

0000000140001f42 <do_pseudo_reloc>:
   140001f42:	55                   	push   rbp
   140001f43:	48 89 e5             	mov    rbp,rsp
   140001f46:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   140001f4a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f4e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f52:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f56:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140001f5a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140001f5e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f62:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f66:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001f6a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   140001f6f:	0f 8e 44 03 00 00    	jle    1400022b9 <do_pseudo_reloc+0x377>
   140001f75:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   140001f7a:	7e 25                	jle    140001fa1 <do_pseudo_reloc+0x5f>
   140001f7c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f80:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f82:	85 c0                	test   eax,eax
   140001f84:	75 1b                	jne    140001fa1 <do_pseudo_reloc+0x5f>
   140001f86:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f8a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f8d:	85 c0                	test   eax,eax
   140001f8f:	75 10                	jne    140001fa1 <do_pseudo_reloc+0x5f>
   140001f91:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f95:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001f98:	85 c0                	test   eax,eax
   140001f9a:	75 05                	jne    140001fa1 <do_pseudo_reloc+0x5f>
   140001f9c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140001fa1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fa5:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fa7:	85 c0                	test   eax,eax
   140001fa9:	75 0b                	jne    140001fb6 <do_pseudo_reloc+0x74>
   140001fab:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001faf:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fb2:	85 c0                	test   eax,eax
   140001fb4:	74 59                	je     14000200f <do_pseudo_reloc+0xcd>
   140001fb6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fba:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001fbe:	eb 40                	jmp    140002000 <do_pseudo_reloc+0xbe>
   140001fc0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fc4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fc7:	89 c2                	mov    edx,eax
   140001fc9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001fcd:	48 01 d0             	add    rax,rdx
   140001fd0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001fd4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fd8:	8b 10                	mov    edx,DWORD PTR [rax]
   140001fda:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fde:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fe0:	01 d0                	add    eax,edx
   140001fe2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140001fe5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fe9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   140001fed:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001ff3:	48 89 c1             	mov    rcx,rax
   140001ff6:	e8 00 ff ff ff       	call   140001efb <__write_memory>
   140001ffb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140002000:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002004:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002008:	72 b6                	jb     140001fc0 <do_pseudo_reloc+0x7e>
   14000200a:	e9 ab 02 00 00       	jmp    1400022ba <do_pseudo_reloc+0x378>
   14000200f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002013:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002016:	83 f8 01             	cmp    eax,0x1
   140002019:	74 18                	je     140002033 <do_pseudo_reloc+0xf1>
   14000201b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000201f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002022:	89 c2                	mov    edx,eax
   140002024:	48 8d 05 45 32 00 00 	lea    rax,[rip+0x3245]        # 140005270 <.rdata+0xa0>
   14000202b:	48 89 c1             	mov    rcx,rax
   14000202e:	e8 ad fa ff ff       	call   140001ae0 <__report_error>
   140002033:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002037:	48 83 c0 0c          	add    rax,0xc
   14000203b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000203f:	e9 65 02 00 00       	jmp    1400022a9 <do_pseudo_reloc+0x367>
   140002044:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002048:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000204b:	89 c2                	mov    edx,eax
   14000204d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002051:	48 01 d0             	add    rax,rdx
   140002054:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002058:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000205c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000205e:	89 c2                	mov    edx,eax
   140002060:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002064:	48 01 d0             	add    rax,rdx
   140002067:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000206b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000206f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002072:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002076:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000207a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000207d:	0f b6 c0             	movzx  eax,al
   140002080:	83 f8 40             	cmp    eax,0x40
   140002083:	0f 84 b6 00 00 00    	je     14000213f <do_pseudo_reloc+0x1fd>
   140002089:	83 f8 40             	cmp    eax,0x40
   14000208c:	0f 87 ba 00 00 00    	ja     14000214c <do_pseudo_reloc+0x20a>
   140002092:	83 f8 20             	cmp    eax,0x20
   140002095:	74 77                	je     14000210e <do_pseudo_reloc+0x1cc>
   140002097:	83 f8 20             	cmp    eax,0x20
   14000209a:	0f 87 ac 00 00 00    	ja     14000214c <do_pseudo_reloc+0x20a>
   1400020a0:	83 f8 08             	cmp    eax,0x8
   1400020a3:	74 0a                	je     1400020af <do_pseudo_reloc+0x16d>
   1400020a5:	83 f8 10             	cmp    eax,0x10
   1400020a8:	74 38                	je     1400020e2 <do_pseudo_reloc+0x1a0>
   1400020aa:	e9 9d 00 00 00       	jmp    14000214c <do_pseudo_reloc+0x20a>
   1400020af:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020b3:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400020b6:	0f b6 c0             	movzx  eax,al
   1400020b9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020bd:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020c1:	25 80 00 00 00       	and    eax,0x80
   1400020c6:	48 85 c0             	test   rax,rax
   1400020c9:	0f 84 9d 00 00 00    	je     14000216c <do_pseudo_reloc+0x22a>
   1400020cf:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020d3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400020d9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020dd:	e9 8a 00 00 00       	jmp    14000216c <do_pseudo_reloc+0x22a>
   1400020e2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020e6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400020e9:	0f b7 c0             	movzx  eax,ax
   1400020ec:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020f0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020f4:	25 00 80 00 00       	and    eax,0x8000
   1400020f9:	48 85 c0             	test   rax,rax
   1400020fc:	74 71                	je     14000216f <do_pseudo_reloc+0x22d>
   1400020fe:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002102:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   140002108:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000210c:	eb 61                	jmp    14000216f <do_pseudo_reloc+0x22d>
   14000210e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002112:	8b 00                	mov    eax,DWORD PTR [rax]
   140002114:	89 c0                	mov    eax,eax
   140002116:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000211a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000211e:	25 00 00 00 80       	and    eax,0x80000000
   140002123:	48 85 c0             	test   rax,rax
   140002126:	74 4a                	je     140002172 <do_pseudo_reloc+0x230>
   140002128:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000212c:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002133:	ff ff ff 
   140002136:	48 09 d0             	or     rax,rdx
   140002139:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000213d:	eb 33                	jmp    140002172 <do_pseudo_reloc+0x230>
   14000213f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002143:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002146:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000214a:	eb 27                	jmp    140002173 <do_pseudo_reloc+0x231>
   14000214c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002153:	00 
   140002154:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002158:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000215b:	0f b6 c0             	movzx  eax,al
   14000215e:	48 8d 0d 43 31 00 00 	lea    rcx,[rip+0x3143]        # 1400052a8 <.rdata+0xd8>
   140002165:	89 c2                	mov    edx,eax
   140002167:	e8 74 f9 ff ff       	call   140001ae0 <__report_error>
   14000216c:	90                   	nop
   14000216d:	eb 04                	jmp    140002173 <do_pseudo_reloc+0x231>
   14000216f:	90                   	nop
   140002170:	eb 01                	jmp    140002173 <do_pseudo_reloc+0x231>
   140002172:	90                   	nop
   140002173:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002177:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000217b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000217d:	89 c2                	mov    edx,eax
   14000217f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002183:	48 01 c2             	add    rdx,rax
   140002186:	48 89 c8             	mov    rax,rcx
   140002189:	48 29 d0             	sub    rax,rdx
   14000218c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002190:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002194:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002198:	48 01 d0             	add    rax,rdx
   14000219b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000219f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021a3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400021a6:	25 ff 00 00 00       	and    eax,0xff
   1400021ab:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   1400021ae:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   1400021b2:	77 67                	ja     14000221b <do_pseudo_reloc+0x2d9>
   1400021b4:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021b7:	ba 01 00 00 00       	mov    edx,0x1
   1400021bc:	89 c1                	mov    ecx,eax
   1400021be:	48 d3 e2             	shl    rdx,cl
   1400021c1:	48 89 d0             	mov    rax,rdx
   1400021c4:	48 83 e8 01          	sub    rax,0x1
   1400021c8:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400021cc:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021cf:	83 e8 01             	sub    eax,0x1
   1400021d2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400021d9:	89 c1                	mov    ecx,eax
   1400021db:	48 d3 e2             	shl    rdx,cl
   1400021de:	48 89 d0             	mov    rax,rdx
   1400021e1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400021e5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021e9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400021ed:	7c 0a                	jl     1400021f9 <do_pseudo_reloc+0x2b7>
   1400021ef:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021f3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400021f7:	7e 22                	jle    14000221b <do_pseudo_reloc+0x2d9>
   1400021f9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400021fd:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   140002201:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   140002205:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002208:	48 8d 0d c9 30 00 00 	lea    rcx,[rip+0x30c9]        # 1400052d8 <.rdata+0x108>
   14000220f:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140002214:	89 c2                	mov    edx,eax
   140002216:	e8 c5 f8 ff ff       	call   140001ae0 <__report_error>
   14000221b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000221f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002222:	0f b6 c0             	movzx  eax,al
   140002225:	83 f8 40             	cmp    eax,0x40
   140002228:	74 63                	je     14000228d <do_pseudo_reloc+0x34b>
   14000222a:	83 f8 40             	cmp    eax,0x40
   14000222d:	77 75                	ja     1400022a4 <do_pseudo_reloc+0x362>
   14000222f:	83 f8 20             	cmp    eax,0x20
   140002232:	74 41                	je     140002275 <do_pseudo_reloc+0x333>
   140002234:	83 f8 20             	cmp    eax,0x20
   140002237:	77 6b                	ja     1400022a4 <do_pseudo_reloc+0x362>
   140002239:	83 f8 08             	cmp    eax,0x8
   14000223c:	74 07                	je     140002245 <do_pseudo_reloc+0x303>
   14000223e:	83 f8 10             	cmp    eax,0x10
   140002241:	74 1a                	je     14000225d <do_pseudo_reloc+0x31b>
   140002243:	eb 5f                	jmp    1400022a4 <do_pseudo_reloc+0x362>
   140002245:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002249:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000224d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002253:	48 89 c1             	mov    rcx,rax
   140002256:	e8 a0 fc ff ff       	call   140001efb <__write_memory>
   14000225b:	eb 47                	jmp    1400022a4 <do_pseudo_reloc+0x362>
   14000225d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002261:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002265:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000226b:	48 89 c1             	mov    rcx,rax
   14000226e:	e8 88 fc ff ff       	call   140001efb <__write_memory>
   140002273:	eb 2f                	jmp    1400022a4 <do_pseudo_reloc+0x362>
   140002275:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002279:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000227d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002283:	48 89 c1             	mov    rcx,rax
   140002286:	e8 70 fc ff ff       	call   140001efb <__write_memory>
   14000228b:	eb 17                	jmp    1400022a4 <do_pseudo_reloc+0x362>
   14000228d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002291:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002295:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000229b:	48 89 c1             	mov    rcx,rax
   14000229e:	e8 58 fc ff ff       	call   140001efb <__write_memory>
   1400022a3:	90                   	nop
   1400022a4:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   1400022a9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400022ad:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400022b1:	0f 82 8d fd ff ff    	jb     140002044 <do_pseudo_reloc+0x102>
   1400022b7:	eb 01                	jmp    1400022ba <do_pseudo_reloc+0x378>
   1400022b9:	90                   	nop
   1400022ba:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   1400022be:	5d                   	pop    rbp
   1400022bf:	c3                   	ret

00000001400022c0 <_pei386_runtime_relocator>:
   1400022c0:	55                   	push   rbp
   1400022c1:	48 89 e5             	mov    rbp,rsp
   1400022c4:	48 83 ec 30          	sub    rsp,0x30
   1400022c8:	8b 05 1e 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e1e]        # 1400090ec <was_init.0>
   1400022ce:	85 c0                	test   eax,eax
   1400022d0:	0f 85 88 00 00 00    	jne    14000235e <_pei386_runtime_relocator+0x9e>
   1400022d6:	8b 05 10 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e10]        # 1400090ec <was_init.0>
   1400022dc:	83 c0 01             	add    eax,0x1
   1400022df:	89 05 07 6e 00 00    	mov    DWORD PTR [rip+0x6e07],eax        # 1400090ec <was_init.0>
   1400022e5:	e8 21 0b 00 00       	call   140002e0b <__mingw_GetSectionCount>
   1400022ea:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400022ed:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400022f0:	48 63 d0             	movsxd rdx,eax
   1400022f3:	48 89 d0             	mov    rax,rdx
   1400022f6:	48 c1 e0 02          	shl    rax,0x2
   1400022fa:	48 01 d0             	add    rax,rdx
   1400022fd:	48 c1 e0 03          	shl    rax,0x3
   140002301:	48 83 c0 0f          	add    rax,0xf
   140002305:	48 c1 e8 04          	shr    rax,0x4
   140002309:	48 c1 e0 04          	shl    rax,0x4
   14000230d:	e8 7e 0d 00 00       	call   140003090 <___chkstk_ms>
   140002312:	48 29 c4             	sub    rsp,rax
   140002315:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   14000231a:	48 83 c0 0f          	add    rax,0xf
   14000231e:	48 c1 e8 04          	shr    rax,0x4
   140002322:	48 c1 e0 04          	shl    rax,0x4
   140002326:	48 89 05 b3 6d 00 00 	mov    QWORD PTR [rip+0x6db3],rax        # 1400090e0 <the_secs>
   14000232d:	c7 05 b1 6d 00 00 00 	mov    DWORD PTR [rip+0x6db1],0x0        # 1400090e8 <maxSections>
   140002334:	00 00 00 
   140002337:	48 8b 0d 22 30 00 00 	mov    rcx,QWORD PTR [rip+0x3022]        # 140005360 <.refptr.__ImageBase>
   14000233e:	48 8b 15 2b 30 00 00 	mov    rdx,QWORD PTR [rip+0x302b]        # 140005370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002345:	48 8b 05 34 30 00 00 	mov    rax,QWORD PTR [rip+0x3034]        # 140005380 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000234c:	49 89 c8             	mov    r8,rcx
   14000234f:	48 89 c1             	mov    rcx,rax
   140002352:	e8 eb fb ff ff       	call   140001f42 <do_pseudo_reloc>
   140002357:	e8 c7 fa ff ff       	call   140001e23 <restore_modified_sections>
   14000235c:	eb 01                	jmp    14000235f <_pei386_runtime_relocator+0x9f>
   14000235e:	90                   	nop
   14000235f:	48 89 ec             	mov    rsp,rbp
   140002362:	5d                   	pop    rbp
   140002363:	c3                   	ret
   140002364:	90                   	nop
   140002365:	90                   	nop
   140002366:	90                   	nop
   140002367:	90                   	nop
   140002368:	90                   	nop
   140002369:	90                   	nop
   14000236a:	90                   	nop
   14000236b:	90                   	nop
   14000236c:	90                   	nop
   14000236d:	90                   	nop
   14000236e:	90                   	nop
   14000236f:	90                   	nop

0000000140002370 <__mingw_raise_matherr>:
   140002370:	55                   	push   rbp
   140002371:	48 89 e5             	mov    rbp,rsp
   140002374:	48 83 ec 50          	sub    rsp,0x50
   140002378:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000237b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000237f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002384:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002389:	48 8b 05 60 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d60]        # 1400090f0 <stUserMathErr>
   140002390:	48 85 c0             	test   rax,rax
   140002393:	74 3e                	je     1400023d3 <__mingw_raise_matherr+0x63>
   140002395:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002398:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000239b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000239f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400023a3:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   1400023a8:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   1400023ad:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   1400023b2:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   1400023b7:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   1400023bc:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   1400023c1:	48 8b 15 28 6d 00 00 	mov    rdx,QWORD PTR [rip+0x6d28]        # 1400090f0 <stUserMathErr>
   1400023c8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   1400023cc:	48 89 c1             	mov    rcx,rax
   1400023cf:	ff d2                	call   rdx
   1400023d1:	eb 01                	jmp    1400023d4 <__mingw_raise_matherr+0x64>
   1400023d3:	90                   	nop
   1400023d4:	48 83 c4 50          	add    rsp,0x50
   1400023d8:	5d                   	pop    rbp
   1400023d9:	c3                   	ret

00000001400023da <__mingw_setusermatherr>:
   1400023da:	55                   	push   rbp
   1400023db:	48 89 e5             	mov    rbp,rsp
   1400023de:	48 83 ec 20          	sub    rsp,0x20
   1400023e2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023e6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023ea:	48 89 05 ff 6c 00 00 	mov    QWORD PTR [rip+0x6cff],rax        # 1400090f0 <stUserMathErr>
   1400023f1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023f5:	48 89 c1             	mov    rcx,rax
   1400023f8:	e8 13 0e 00 00       	call   140003210 <__setusermatherr>
   1400023fd:	90                   	nop
   1400023fe:	48 83 c4 20          	add    rsp,0x20
   140002402:	5d                   	pop    rbp
   140002403:	c3                   	ret
   140002404:	90                   	nop
   140002405:	90                   	nop
   140002406:	90                   	nop
   140002407:	90                   	nop
   140002408:	90                   	nop
   140002409:	90                   	nop
   14000240a:	90                   	nop
   14000240b:	90                   	nop
   14000240c:	90                   	nop
   14000240d:	90                   	nop
   14000240e:	90                   	nop
   14000240f:	90                   	nop

0000000140002410 <__mingw_SEH_error_handler>:
   140002410:	55                   	push   rbp
   140002411:	48 89 e5             	mov    rbp,rsp
   140002414:	48 83 ec 30          	sub    rsp,0x30
   140002418:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000241c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002420:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002424:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140002428:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   14000242f:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002436:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000243a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000243d:	83 e0 02             	and    eax,0x2
   140002440:	85 c0                	test   eax,eax
   140002442:	74 0a                	je     14000244e <__mingw_SEH_error_handler+0x3e>
   140002444:	b8 01 00 00 00       	mov    eax,0x1
   140002449:	e9 16 02 00 00       	jmp    140002664 <__mingw_SEH_error_handler+0x254>
   14000244e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002452:	8b 00                	mov    eax,DWORD PTR [rax]
   140002454:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002459:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000245e:	75 18                	jne    140002478 <__mingw_SEH_error_handler+0x68>
   140002460:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002464:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002467:	83 e0 01             	and    eax,0x1
   14000246a:	85 c0                	test   eax,eax
   14000246c:	75 0a                	jne    140002478 <__mingw_SEH_error_handler+0x68>
   14000246e:	b8 00 00 00 00       	mov    eax,0x0
   140002473:	e9 ec 01 00 00       	jmp    140002664 <__mingw_SEH_error_handler+0x254>
   140002478:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000247c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000247e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002483:	0f 84 12 01 00 00    	je     14000259b <__mingw_SEH_error_handler+0x18b>
   140002489:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000248e:	0f 87 c3 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   140002494:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002499:	0f 87 b8 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   14000249f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400024a4:	0f 83 4c 01 00 00    	jae    1400025f6 <__mingw_SEH_error_handler+0x1e6>
   1400024aa:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400024af:	0f 84 3a 01 00 00    	je     1400025ef <__mingw_SEH_error_handler+0x1df>
   1400024b5:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400024ba:	0f 87 97 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   1400024c0:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024c5:	0f 84 83 01 00 00    	je     14000264e <__mingw_SEH_error_handler+0x23e>
   1400024cb:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024d0:	0f 87 81 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   1400024d6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400024db:	0f 87 76 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   1400024e1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400024e6:	0f 83 03 01 00 00    	jae    1400025ef <__mingw_SEH_error_handler+0x1df>
   1400024ec:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024f1:	0f 84 57 01 00 00    	je     14000264e <__mingw_SEH_error_handler+0x23e>
   1400024f7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024fc:	0f 87 55 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   140002502:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002507:	0f 84 8e 00 00 00    	je     14000259b <__mingw_SEH_error_handler+0x18b>
   14000250d:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002512:	0f 87 3f 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   140002518:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000251d:	0f 84 2b 01 00 00    	je     14000264e <__mingw_SEH_error_handler+0x23e>
   140002523:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002528:	0f 87 29 01 00 00    	ja     140002657 <__mingw_SEH_error_handler+0x247>
   14000252e:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002533:	0f 84 15 01 00 00    	je     14000264e <__mingw_SEH_error_handler+0x23e>
   140002539:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000253e:	0f 85 13 01 00 00    	jne    140002657 <__mingw_SEH_error_handler+0x247>
   140002544:	ba 00 00 00 00       	mov    edx,0x0
   140002549:	b9 0b 00 00 00       	mov    ecx,0xb
   14000254e:	e8 2d 0d 00 00       	call   140003280 <signal>
   140002553:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002557:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000255c:	75 1b                	jne    140002579 <__mingw_SEH_error_handler+0x169>
   14000255e:	ba 01 00 00 00       	mov    edx,0x1
   140002563:	b9 0b 00 00 00       	mov    ecx,0xb
   140002568:	e8 13 0d 00 00       	call   140003280 <signal>
   14000256d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002574:	e9 e1 00 00 00       	jmp    14000265a <__mingw_SEH_error_handler+0x24a>
   140002579:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000257e:	0f 84 d6 00 00 00    	je     14000265a <__mingw_SEH_error_handler+0x24a>
   140002584:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002588:	b9 0b 00 00 00       	mov    ecx,0xb
   14000258d:	ff d0                	call   rax
   14000258f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002596:	e9 bf 00 00 00       	jmp    14000265a <__mingw_SEH_error_handler+0x24a>
   14000259b:	ba 00 00 00 00       	mov    edx,0x0
   1400025a0:	b9 04 00 00 00       	mov    ecx,0x4
   1400025a5:	e8 d6 0c 00 00       	call   140003280 <signal>
   1400025aa:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025ae:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025b3:	75 1b                	jne    1400025d0 <__mingw_SEH_error_handler+0x1c0>
   1400025b5:	ba 01 00 00 00       	mov    edx,0x1
   1400025ba:	b9 04 00 00 00       	mov    ecx,0x4
   1400025bf:	e8 bc 0c 00 00       	call   140003280 <signal>
   1400025c4:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025cb:	e9 8d 00 00 00       	jmp    14000265d <__mingw_SEH_error_handler+0x24d>
   1400025d0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400025d5:	0f 84 82 00 00 00    	je     14000265d <__mingw_SEH_error_handler+0x24d>
   1400025db:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025df:	b9 04 00 00 00       	mov    ecx,0x4
   1400025e4:	ff d0                	call   rax
   1400025e6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025ed:	eb 6e                	jmp    14000265d <__mingw_SEH_error_handler+0x24d>
   1400025ef:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400025f6:	ba 00 00 00 00       	mov    edx,0x0
   1400025fb:	b9 08 00 00 00       	mov    ecx,0x8
   140002600:	e8 7b 0c 00 00       	call   140003280 <signal>
   140002605:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002609:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000260e:	75 23                	jne    140002633 <__mingw_SEH_error_handler+0x223>
   140002610:	ba 01 00 00 00       	mov    edx,0x1
   140002615:	b9 08 00 00 00       	mov    ecx,0x8
   14000261a:	e8 61 0c 00 00       	call   140003280 <signal>
   14000261f:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002623:	74 05                	je     14000262a <__mingw_SEH_error_handler+0x21a>
   140002625:	e8 a6 05 00 00       	call   140002bd0 <_fpreset>
   14000262a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002631:	eb 2d                	jmp    140002660 <__mingw_SEH_error_handler+0x250>
   140002633:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002638:	74 26                	je     140002660 <__mingw_SEH_error_handler+0x250>
   14000263a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000263e:	b9 08 00 00 00       	mov    ecx,0x8
   140002643:	ff d0                	call   rax
   140002645:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000264c:	eb 12                	jmp    140002660 <__mingw_SEH_error_handler+0x250>
   14000264e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002655:	eb 0a                	jmp    140002661 <__mingw_SEH_error_handler+0x251>
   140002657:	90                   	nop
   140002658:	eb 07                	jmp    140002661 <__mingw_SEH_error_handler+0x251>
   14000265a:	90                   	nop
   14000265b:	eb 04                	jmp    140002661 <__mingw_SEH_error_handler+0x251>
   14000265d:	90                   	nop
   14000265e:	eb 01                	jmp    140002661 <__mingw_SEH_error_handler+0x251>
   140002660:	90                   	nop
   140002661:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002664:	48 83 c4 30          	add    rsp,0x30
   140002668:	5d                   	pop    rbp
   140002669:	c3                   	ret

000000014000266a <_gnu_exception_handler>:
   14000266a:	55                   	push   rbp
   14000266b:	48 89 e5             	mov    rbp,rsp
   14000266e:	48 83 ec 30          	sub    rsp,0x30
   140002672:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002676:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000267d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002684:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002688:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000268b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000268d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002692:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002697:	75 1b                	jne    1400026b4 <_gnu_exception_handler+0x4a>
   140002699:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000269d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400026a0:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400026a3:	83 e0 01             	and    eax,0x1
   1400026a6:	85 c0                	test   eax,eax
   1400026a8:	75 0a                	jne    1400026b4 <_gnu_exception_handler+0x4a>
   1400026aa:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400026af:	e9 14 02 00 00       	jmp    1400028c8 <_gnu_exception_handler+0x25e>
   1400026b4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400026b8:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400026bb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400026bd:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026c2:	0f 84 12 01 00 00    	je     1400027da <_gnu_exception_handler+0x170>
   1400026c8:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026cd:	0f 87 c3 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   1400026d3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400026d8:	0f 87 b8 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   1400026de:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400026e3:	0f 83 4c 01 00 00    	jae    140002835 <_gnu_exception_handler+0x1cb>
   1400026e9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026ee:	0f 84 3a 01 00 00    	je     14000282e <_gnu_exception_handler+0x1c4>
   1400026f4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026f9:	0f 87 97 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   1400026ff:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002704:	0f 84 83 01 00 00    	je     14000288d <_gnu_exception_handler+0x223>
   14000270a:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   14000270f:	0f 87 81 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   140002715:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   14000271a:	0f 87 76 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   140002720:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002725:	0f 83 03 01 00 00    	jae    14000282e <_gnu_exception_handler+0x1c4>
   14000272b:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002730:	0f 84 57 01 00 00    	je     14000288d <_gnu_exception_handler+0x223>
   140002736:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000273b:	0f 87 55 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   140002741:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002746:	0f 84 8e 00 00 00    	je     1400027da <_gnu_exception_handler+0x170>
   14000274c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002751:	0f 87 3f 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   140002757:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000275c:	0f 84 2b 01 00 00    	je     14000288d <_gnu_exception_handler+0x223>
   140002762:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002767:	0f 87 29 01 00 00    	ja     140002896 <_gnu_exception_handler+0x22c>
   14000276d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002772:	0f 84 15 01 00 00    	je     14000288d <_gnu_exception_handler+0x223>
   140002778:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000277d:	0f 85 13 01 00 00    	jne    140002896 <_gnu_exception_handler+0x22c>
   140002783:	ba 00 00 00 00       	mov    edx,0x0
   140002788:	b9 0b 00 00 00       	mov    ecx,0xb
   14000278d:	e8 ee 0a 00 00       	call   140003280 <signal>
   140002792:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002796:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000279b:	75 1b                	jne    1400027b8 <_gnu_exception_handler+0x14e>
   14000279d:	ba 01 00 00 00       	mov    edx,0x1
   1400027a2:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027a7:	e8 d4 0a 00 00       	call   140003280 <signal>
   1400027ac:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027b3:	e9 e1 00 00 00       	jmp    140002899 <_gnu_exception_handler+0x22f>
   1400027b8:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027bd:	0f 84 d6 00 00 00    	je     140002899 <_gnu_exception_handler+0x22f>
   1400027c3:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027c7:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027cc:	ff d0                	call   rax
   1400027ce:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027d5:	e9 bf 00 00 00       	jmp    140002899 <_gnu_exception_handler+0x22f>
   1400027da:	ba 00 00 00 00       	mov    edx,0x0
   1400027df:	b9 04 00 00 00       	mov    ecx,0x4
   1400027e4:	e8 97 0a 00 00       	call   140003280 <signal>
   1400027e9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027ed:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027f2:	75 1b                	jne    14000280f <_gnu_exception_handler+0x1a5>
   1400027f4:	ba 01 00 00 00       	mov    edx,0x1
   1400027f9:	b9 04 00 00 00       	mov    ecx,0x4
   1400027fe:	e8 7d 0a 00 00       	call   140003280 <signal>
   140002803:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000280a:	e9 8d 00 00 00       	jmp    14000289c <_gnu_exception_handler+0x232>
   14000280f:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002814:	0f 84 82 00 00 00    	je     14000289c <_gnu_exception_handler+0x232>
   14000281a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000281e:	b9 04 00 00 00       	mov    ecx,0x4
   140002823:	ff d0                	call   rax
   140002825:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000282c:	eb 6e                	jmp    14000289c <_gnu_exception_handler+0x232>
   14000282e:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002835:	ba 00 00 00 00       	mov    edx,0x0
   14000283a:	b9 08 00 00 00       	mov    ecx,0x8
   14000283f:	e8 3c 0a 00 00       	call   140003280 <signal>
   140002844:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002848:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000284d:	75 23                	jne    140002872 <_gnu_exception_handler+0x208>
   14000284f:	ba 01 00 00 00       	mov    edx,0x1
   140002854:	b9 08 00 00 00       	mov    ecx,0x8
   140002859:	e8 22 0a 00 00       	call   140003280 <signal>
   14000285e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002862:	74 05                	je     140002869 <_gnu_exception_handler+0x1ff>
   140002864:	e8 67 03 00 00       	call   140002bd0 <_fpreset>
   140002869:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002870:	eb 2d                	jmp    14000289f <_gnu_exception_handler+0x235>
   140002872:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002877:	74 26                	je     14000289f <_gnu_exception_handler+0x235>
   140002879:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000287d:	b9 08 00 00 00       	mov    ecx,0x8
   140002882:	ff d0                	call   rax
   140002884:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000288b:	eb 12                	jmp    14000289f <_gnu_exception_handler+0x235>
   14000288d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002894:	eb 0a                	jmp    1400028a0 <_gnu_exception_handler+0x236>
   140002896:	90                   	nop
   140002897:	eb 07                	jmp    1400028a0 <_gnu_exception_handler+0x236>
   140002899:	90                   	nop
   14000289a:	eb 04                	jmp    1400028a0 <_gnu_exception_handler+0x236>
   14000289c:	90                   	nop
   14000289d:	eb 01                	jmp    1400028a0 <_gnu_exception_handler+0x236>
   14000289f:	90                   	nop
   1400028a0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400028a4:	75 1f                	jne    1400028c5 <_gnu_exception_handler+0x25b>
   1400028a6:	48 8b 05 63 68 00 00 	mov    rax,QWORD PTR [rip+0x6863]        # 140009110 <__mingw_oldexcpt_handler>
   1400028ad:	48 85 c0             	test   rax,rax
   1400028b0:	74 13                	je     1400028c5 <_gnu_exception_handler+0x25b>
   1400028b2:	48 8b 15 57 68 00 00 	mov    rdx,QWORD PTR [rip+0x6857]        # 140009110 <__mingw_oldexcpt_handler>
   1400028b9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400028bd:	48 89 c1             	mov    rcx,rax
   1400028c0:	ff d2                	call   rdx
   1400028c2:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400028c5:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400028c8:	48 83 c4 30          	add    rsp,0x30
   1400028cc:	5d                   	pop    rbp
   1400028cd:	c3                   	ret
   1400028ce:	90                   	nop
   1400028cf:	90                   	nop

00000001400028d0 <___w64_mingwthr_add_key_dtor>:
   1400028d0:	55                   	push   rbp
   1400028d1:	48 89 e5             	mov    rbp,rsp
   1400028d4:	48 83 ec 30          	sub    rsp,0x30
   1400028d8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400028db:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400028df:	8b 05 63 68 00 00    	mov    eax,DWORD PTR [rip+0x6863]        # 140009148 <__mingwthr_cs_init>
   1400028e5:	85 c0                	test   eax,eax
   1400028e7:	75 07                	jne    1400028f0 <___w64_mingwthr_add_key_dtor+0x20>
   1400028e9:	b8 00 00 00 00       	mov    eax,0x0
   1400028ee:	eb 7b                	jmp    14000296b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028f0:	ba 18 00 00 00       	mov    edx,0x18
   1400028f5:	b9 01 00 00 00       	mov    ecx,0x1
   1400028fa:	e8 41 09 00 00       	call   140003240 <calloc>
   1400028ff:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002903:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002908:	75 07                	jne    140002911 <___w64_mingwthr_add_key_dtor+0x41>
   14000290a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000290f:	eb 5a                	jmp    14000296b <___w64_mingwthr_add_key_dtor+0x9b>
   140002911:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002915:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140002918:	89 10                	mov    DWORD PTR [rax],edx
   14000291a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000291e:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002922:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002926:	48 8d 05 f3 67 00 00 	lea    rax,[rip+0x67f3]        # 140009120 <__mingwthr_cs>
   14000292d:	48 89 c1             	mov    rcx,rax
   140002930:	48 8b 05 59 78 00 00 	mov    rax,QWORD PTR [rip+0x7859]        # 14000a190 <__imp_EnterCriticalSection>
   140002937:	ff d0                	call   rax
   140002939:	48 8b 15 10 68 00 00 	mov    rdx,QWORD PTR [rip+0x6810]        # 140009150 <key_dtor_list>
   140002940:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002944:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002948:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000294c:	48 89 05 fd 67 00 00 	mov    QWORD PTR [rip+0x67fd],rax        # 140009150 <key_dtor_list>
   140002953:	48 8d 05 c6 67 00 00 	lea    rax,[rip+0x67c6]        # 140009120 <__mingwthr_cs>
   14000295a:	48 89 c1             	mov    rcx,rax
   14000295d:	48 8b 05 5c 78 00 00 	mov    rax,QWORD PTR [rip+0x785c]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002964:	ff d0                	call   rax
   140002966:	b8 00 00 00 00       	mov    eax,0x0
   14000296b:	48 83 c4 30          	add    rsp,0x30
   14000296f:	5d                   	pop    rbp
   140002970:	c3                   	ret

0000000140002971 <___w64_mingwthr_remove_key_dtor>:
   140002971:	55                   	push   rbp
   140002972:	48 89 e5             	mov    rbp,rsp
   140002975:	48 83 ec 30          	sub    rsp,0x30
   140002979:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000297c:	8b 05 c6 67 00 00    	mov    eax,DWORD PTR [rip+0x67c6]        # 140009148 <__mingwthr_cs_init>
   140002982:	85 c0                	test   eax,eax
   140002984:	75 0a                	jne    140002990 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002986:	b8 00 00 00 00       	mov    eax,0x0
   14000298b:	e9 9c 00 00 00       	jmp    140002a2c <___w64_mingwthr_remove_key_dtor+0xbb>
   140002990:	48 8d 05 89 67 00 00 	lea    rax,[rip+0x6789]        # 140009120 <__mingwthr_cs>
   140002997:	48 89 c1             	mov    rcx,rax
   14000299a:	48 8b 05 ef 77 00 00 	mov    rax,QWORD PTR [rip+0x77ef]        # 14000a190 <__imp_EnterCriticalSection>
   1400029a1:	ff d0                	call   rax
   1400029a3:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   1400029aa:	00 
   1400029ab:	48 8b 05 9e 67 00 00 	mov    rax,QWORD PTR [rip+0x679e]        # 140009150 <key_dtor_list>
   1400029b2:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029b6:	eb 55                	jmp    140002a0d <___w64_mingwthr_remove_key_dtor+0x9c>
   1400029b8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029bc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400029be:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   1400029c1:	75 36                	jne    1400029f9 <___w64_mingwthr_remove_key_dtor+0x88>
   1400029c3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400029c8:	75 11                	jne    1400029db <___w64_mingwthr_remove_key_dtor+0x6a>
   1400029ca:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029ce:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029d2:	48 89 05 77 67 00 00 	mov    QWORD PTR [rip+0x6777],rax        # 140009150 <key_dtor_list>
   1400029d9:	eb 10                	jmp    1400029eb <___w64_mingwthr_remove_key_dtor+0x7a>
   1400029db:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029df:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   1400029e3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400029e7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   1400029eb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029ef:	48 89 c1             	mov    rcx,rax
   1400029f2:	e8 69 08 00 00       	call   140003260 <free>
   1400029f7:	eb 1b                	jmp    140002a14 <___w64_mingwthr_remove_key_dtor+0xa3>
   1400029f9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029fd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a01:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a05:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002a09:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a0d:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a12:	75 a4                	jne    1400029b8 <___w64_mingwthr_remove_key_dtor+0x47>
   140002a14:	48 8d 05 05 67 00 00 	lea    rax,[rip+0x6705]        # 140009120 <__mingwthr_cs>
   140002a1b:	48 89 c1             	mov    rcx,rax
   140002a1e:	48 8b 05 9b 77 00 00 	mov    rax,QWORD PTR [rip+0x779b]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002a25:	ff d0                	call   rax
   140002a27:	b8 00 00 00 00       	mov    eax,0x0
   140002a2c:	48 83 c4 30          	add    rsp,0x30
   140002a30:	5d                   	pop    rbp
   140002a31:	c3                   	ret

0000000140002a32 <__mingwthr_run_key_dtors>:
   140002a32:	55                   	push   rbp
   140002a33:	48 89 e5             	mov    rbp,rsp
   140002a36:	48 83 ec 30          	sub    rsp,0x30
   140002a3a:	8b 05 08 67 00 00    	mov    eax,DWORD PTR [rip+0x6708]        # 140009148 <__mingwthr_cs_init>
   140002a40:	85 c0                	test   eax,eax
   140002a42:	0f 84 82 00 00 00    	je     140002aca <__mingwthr_run_key_dtors+0x98>
   140002a48:	48 8d 05 d1 66 00 00 	lea    rax,[rip+0x66d1]        # 140009120 <__mingwthr_cs>
   140002a4f:	48 89 c1             	mov    rcx,rax
   140002a52:	48 8b 05 37 77 00 00 	mov    rax,QWORD PTR [rip+0x7737]        # 14000a190 <__imp_EnterCriticalSection>
   140002a59:	ff d0                	call   rax
   140002a5b:	48 8b 05 ee 66 00 00 	mov    rax,QWORD PTR [rip+0x66ee]        # 140009150 <key_dtor_list>
   140002a62:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a66:	eb 46                	jmp    140002aae <__mingwthr_run_key_dtors+0x7c>
   140002a68:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a6c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a6e:	89 c1                	mov    ecx,eax
   140002a70:	48 8b 05 69 77 00 00 	mov    rax,QWORD PTR [rip+0x7769]        # 14000a1e0 <__imp_TlsGetValue>
   140002a77:	ff d0                	call   rax
   140002a79:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a7d:	48 8b 05 1c 77 00 00 	mov    rax,QWORD PTR [rip+0x771c]        # 14000a1a0 <__imp_GetLastError>
   140002a84:	ff d0                	call   rax
   140002a86:	85 c0                	test   eax,eax
   140002a88:	75 18                	jne    140002aa2 <__mingwthr_run_key_dtors+0x70>
   140002a8a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a8f:	74 11                	je     140002aa2 <__mingwthr_run_key_dtors+0x70>
   140002a91:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a95:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002a99:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a9d:	48 89 c1             	mov    rcx,rax
   140002aa0:	ff d2                	call   rdx
   140002aa2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002aa6:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002aaa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002aae:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002ab3:	75 b3                	jne    140002a68 <__mingwthr_run_key_dtors+0x36>
   140002ab5:	48 8d 05 64 66 00 00 	lea    rax,[rip+0x6664]        # 140009120 <__mingwthr_cs>
   140002abc:	48 89 c1             	mov    rcx,rax
   140002abf:	48 8b 05 fa 76 00 00 	mov    rax,QWORD PTR [rip+0x76fa]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002ac6:	ff d0                	call   rax
   140002ac8:	eb 01                	jmp    140002acb <__mingwthr_run_key_dtors+0x99>
   140002aca:	90                   	nop
   140002acb:	48 83 c4 30          	add    rsp,0x30
   140002acf:	5d                   	pop    rbp
   140002ad0:	c3                   	ret

0000000140002ad1 <__mingw_TLScallback>:
   140002ad1:	55                   	push   rbp
   140002ad2:	48 89 e5             	mov    rbp,rsp
   140002ad5:	48 83 ec 30          	sub    rsp,0x30
   140002ad9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002add:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002ae0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002ae4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ae8:	0f 84 cc 00 00 00    	je     140002bba <__mingw_TLScallback+0xe9>
   140002aee:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002af2:	0f 87 ca 00 00 00    	ja     140002bc2 <__mingw_TLScallback+0xf1>
   140002af8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002afc:	0f 84 b1 00 00 00    	je     140002bb3 <__mingw_TLScallback+0xe2>
   140002b02:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002b06:	0f 87 b6 00 00 00    	ja     140002bc2 <__mingw_TLScallback+0xf1>
   140002b0c:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002b10:	74 33                	je     140002b45 <__mingw_TLScallback+0x74>
   140002b12:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002b16:	0f 85 a6 00 00 00    	jne    140002bc2 <__mingw_TLScallback+0xf1>
   140002b1c:	8b 05 26 66 00 00    	mov    eax,DWORD PTR [rip+0x6626]        # 140009148 <__mingwthr_cs_init>
   140002b22:	85 c0                	test   eax,eax
   140002b24:	75 13                	jne    140002b39 <__mingw_TLScallback+0x68>
   140002b26:	48 8d 05 f3 65 00 00 	lea    rax,[rip+0x65f3]        # 140009120 <__mingwthr_cs>
   140002b2d:	48 89 c1             	mov    rcx,rax
   140002b30:	48 8b 05 81 76 00 00 	mov    rax,QWORD PTR [rip+0x7681]        # 14000a1b8 <__imp_InitializeCriticalSection>
   140002b37:	ff d0                	call   rax
   140002b39:	c7 05 05 66 00 00 01 	mov    DWORD PTR [rip+0x6605],0x1        # 140009148 <__mingwthr_cs_init>
   140002b40:	00 00 00 
   140002b43:	eb 7d                	jmp    140002bc2 <__mingw_TLScallback+0xf1>
   140002b45:	e8 e8 fe ff ff       	call   140002a32 <__mingwthr_run_key_dtors>
   140002b4a:	8b 05 f8 65 00 00    	mov    eax,DWORD PTR [rip+0x65f8]        # 140009148 <__mingwthr_cs_init>
   140002b50:	83 f8 01             	cmp    eax,0x1
   140002b53:	75 6c                	jne    140002bc1 <__mingw_TLScallback+0xf0>
   140002b55:	48 8b 05 f4 65 00 00 	mov    rax,QWORD PTR [rip+0x65f4]        # 140009150 <key_dtor_list>
   140002b5c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b60:	eb 20                	jmp    140002b82 <__mingw_TLScallback+0xb1>
   140002b62:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b66:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b6a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b6e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b72:	48 89 c1             	mov    rcx,rax
   140002b75:	e8 e6 06 00 00       	call   140003260 <free>
   140002b7a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b7e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b82:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b87:	75 d9                	jne    140002b62 <__mingw_TLScallback+0x91>
   140002b89:	48 c7 05 bc 65 00 00 	mov    QWORD PTR [rip+0x65bc],0x0        # 140009150 <key_dtor_list>
   140002b90:	00 00 00 00 
   140002b94:	c7 05 aa 65 00 00 00 	mov    DWORD PTR [rip+0x65aa],0x0        # 140009148 <__mingwthr_cs_init>
   140002b9b:	00 00 00 
   140002b9e:	48 8d 05 7b 65 00 00 	lea    rax,[rip+0x657b]        # 140009120 <__mingwthr_cs>
   140002ba5:	48 89 c1             	mov    rcx,rax
   140002ba8:	48 8b 05 d9 75 00 00 	mov    rax,QWORD PTR [rip+0x75d9]        # 14000a188 <__IAT_start__>
   140002baf:	ff d0                	call   rax
   140002bb1:	eb 0e                	jmp    140002bc1 <__mingw_TLScallback+0xf0>
   140002bb3:	e8 18 00 00 00       	call   140002bd0 <_fpreset>
   140002bb8:	eb 08                	jmp    140002bc2 <__mingw_TLScallback+0xf1>
   140002bba:	e8 73 fe ff ff       	call   140002a32 <__mingwthr_run_key_dtors>
   140002bbf:	eb 01                	jmp    140002bc2 <__mingw_TLScallback+0xf1>
   140002bc1:	90                   	nop
   140002bc2:	b8 01 00 00 00       	mov    eax,0x1
   140002bc7:	48 83 c4 30          	add    rsp,0x30
   140002bcb:	5d                   	pop    rbp
   140002bcc:	c3                   	ret
   140002bcd:	90                   	nop
   140002bce:	90                   	nop
   140002bcf:	90                   	nop

0000000140002bd0 <_fpreset>:
   140002bd0:	55                   	push   rbp
   140002bd1:	48 89 e5             	mov    rbp,rsp
   140002bd4:	db e3                	fninit
   140002bd6:	90                   	nop
   140002bd7:	5d                   	pop    rbp
   140002bd8:	c3                   	ret
   140002bd9:	90                   	nop
   140002bda:	90                   	nop
   140002bdb:	90                   	nop
   140002bdc:	90                   	nop
   140002bdd:	90                   	nop
   140002bde:	90                   	nop
   140002bdf:	90                   	nop

0000000140002be0 <_ValidateImageBase>:
   140002be0:	55                   	push   rbp
   140002be1:	48 89 e5             	mov    rbp,rsp
   140002be4:	48 83 ec 20          	sub    rsp,0x20
   140002be8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002bec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002bf0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002bf4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bf8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002bfb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002bff:	74 07                	je     140002c08 <_ValidateImageBase+0x28>
   140002c01:	b8 00 00 00 00       	mov    eax,0x0
   140002c06:	eb 4e                	jmp    140002c56 <_ValidateImageBase+0x76>
   140002c08:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c0c:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c0f:	48 63 d0             	movsxd rdx,eax
   140002c12:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c16:	48 01 d0             	add    rax,rdx
   140002c19:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002c1d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c21:	8b 00                	mov    eax,DWORD PTR [rax]
   140002c23:	3d 50 45 00 00       	cmp    eax,0x4550
   140002c28:	74 07                	je     140002c31 <_ValidateImageBase+0x51>
   140002c2a:	b8 00 00 00 00       	mov    eax,0x0
   140002c2f:	eb 25                	jmp    140002c56 <_ValidateImageBase+0x76>
   140002c31:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c35:	48 83 c0 18          	add    rax,0x18
   140002c39:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c3d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c41:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c44:	66 3d 0b 02          	cmp    ax,0x20b
   140002c48:	74 07                	je     140002c51 <_ValidateImageBase+0x71>
   140002c4a:	b8 00 00 00 00       	mov    eax,0x0
   140002c4f:	eb 05                	jmp    140002c56 <_ValidateImageBase+0x76>
   140002c51:	b8 01 00 00 00       	mov    eax,0x1
   140002c56:	48 83 c4 20          	add    rsp,0x20
   140002c5a:	5d                   	pop    rbp
   140002c5b:	c3                   	ret

0000000140002c5c <_FindPESection>:
   140002c5c:	55                   	push   rbp
   140002c5d:	48 89 e5             	mov    rbp,rsp
   140002c60:	48 83 ec 20          	sub    rsp,0x20
   140002c64:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c68:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002c6c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c70:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c73:	48 63 d0             	movsxd rdx,eax
   140002c76:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c7a:	48 01 d0             	add    rax,rdx
   140002c7d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c81:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002c88:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c8c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002c90:	0f b7 d0             	movzx  edx,ax
   140002c93:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c97:	48 01 d0             	add    rax,rdx
   140002c9a:	48 83 c0 18          	add    rax,0x18
   140002c9e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ca2:	eb 36                	jmp    140002cda <_FindPESection+0x7e>
   140002ca4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ca8:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002cab:	89 c0                	mov    eax,eax
   140002cad:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002cb1:	72 1e                	jb     140002cd1 <_FindPESection+0x75>
   140002cb3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cb7:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002cba:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cbe:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002cc1:	01 d0                	add    eax,edx
   140002cc3:	89 c0                	mov    eax,eax
   140002cc5:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002cc9:	73 06                	jae    140002cd1 <_FindPESection+0x75>
   140002ccb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ccf:	eb 1e                	jmp    140002cef <_FindPESection+0x93>
   140002cd1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002cd5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002cda:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cde:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002ce2:	0f b7 c0             	movzx  eax,ax
   140002ce5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002ce8:	72 ba                	jb     140002ca4 <_FindPESection+0x48>
   140002cea:	b8 00 00 00 00       	mov    eax,0x0
   140002cef:	48 83 c4 20          	add    rsp,0x20
   140002cf3:	5d                   	pop    rbp
   140002cf4:	c3                   	ret

0000000140002cf5 <_FindPESectionByName>:
   140002cf5:	55                   	push   rbp
   140002cf6:	48 89 e5             	mov    rbp,rsp
   140002cf9:	48 83 ec 40          	sub    rsp,0x40
   140002cfd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002d01:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002d05:	48 89 c1             	mov    rcx,rax
   140002d08:	e8 7b 05 00 00       	call   140003288 <strlen>
   140002d0d:	48 83 f8 08          	cmp    rax,0x8
   140002d11:	76 0a                	jbe    140002d1d <_FindPESectionByName+0x28>
   140002d13:	b8 00 00 00 00       	mov    eax,0x0
   140002d18:	e9 98 00 00 00       	jmp    140002db5 <_FindPESectionByName+0xc0>
   140002d1d:	48 8b 05 3c 26 00 00 	mov    rax,QWORD PTR [rip+0x263c]        # 140005360 <.refptr.__ImageBase>
   140002d24:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002d28:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d2c:	48 89 c1             	mov    rcx,rax
   140002d2f:	e8 ac fe ff ff       	call   140002be0 <_ValidateImageBase>
   140002d34:	85 c0                	test   eax,eax
   140002d36:	75 07                	jne    140002d3f <_FindPESectionByName+0x4a>
   140002d38:	b8 00 00 00 00       	mov    eax,0x0
   140002d3d:	eb 76                	jmp    140002db5 <_FindPESectionByName+0xc0>
   140002d3f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d43:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d46:	48 63 d0             	movsxd rdx,eax
   140002d49:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d4d:	48 01 d0             	add    rax,rdx
   140002d50:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002d54:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d5b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d5f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d63:	0f b7 d0             	movzx  edx,ax
   140002d66:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d6a:	48 01 d0             	add    rax,rdx
   140002d6d:	48 83 c0 18          	add    rax,0x18
   140002d71:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d75:	eb 29                	jmp    140002da0 <_FindPESectionByName+0xab>
   140002d77:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d7b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002d7f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002d85:	48 89 c1             	mov    rcx,rax
   140002d88:	e8 03 05 00 00       	call   140003290 <strncmp>
   140002d8d:	85 c0                	test   eax,eax
   140002d8f:	75 06                	jne    140002d97 <_FindPESectionByName+0xa2>
   140002d91:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d95:	eb 1e                	jmp    140002db5 <_FindPESectionByName+0xc0>
   140002d97:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002d9b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002da0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002da4:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002da8:	0f b7 c0             	movzx  eax,ax
   140002dab:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002dae:	72 c7                	jb     140002d77 <_FindPESectionByName+0x82>
   140002db0:	b8 00 00 00 00       	mov    eax,0x0
   140002db5:	48 83 c4 40          	add    rsp,0x40
   140002db9:	5d                   	pop    rbp
   140002dba:	c3                   	ret

0000000140002dbb <__mingw_GetSectionForAddress>:
   140002dbb:	55                   	push   rbp
   140002dbc:	48 89 e5             	mov    rbp,rsp
   140002dbf:	48 83 ec 30          	sub    rsp,0x30
   140002dc3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002dc7:	48 8b 05 92 25 00 00 	mov    rax,QWORD PTR [rip+0x2592]        # 140005360 <.refptr.__ImageBase>
   140002dce:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002dd2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002dd6:	48 89 c1             	mov    rcx,rax
   140002dd9:	e8 02 fe ff ff       	call   140002be0 <_ValidateImageBase>
   140002dde:	85 c0                	test   eax,eax
   140002de0:	75 07                	jne    140002de9 <__mingw_GetSectionForAddress+0x2e>
   140002de2:	b8 00 00 00 00       	mov    eax,0x0
   140002de7:	eb 1c                	jmp    140002e05 <__mingw_GetSectionForAddress+0x4a>
   140002de9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002ded:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002df1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002df5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002df9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002dfd:	48 89 c1             	mov    rcx,rax
   140002e00:	e8 57 fe ff ff       	call   140002c5c <_FindPESection>
   140002e05:	48 83 c4 30          	add    rsp,0x30
   140002e09:	5d                   	pop    rbp
   140002e0a:	c3                   	ret

0000000140002e0b <__mingw_GetSectionCount>:
   140002e0b:	55                   	push   rbp
   140002e0c:	48 89 e5             	mov    rbp,rsp
   140002e0f:	48 83 ec 30          	sub    rsp,0x30
   140002e13:	48 8b 05 46 25 00 00 	mov    rax,QWORD PTR [rip+0x2546]        # 140005360 <.refptr.__ImageBase>
   140002e1a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e1e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e22:	48 89 c1             	mov    rcx,rax
   140002e25:	e8 b6 fd ff ff       	call   140002be0 <_ValidateImageBase>
   140002e2a:	85 c0                	test   eax,eax
   140002e2c:	75 07                	jne    140002e35 <__mingw_GetSectionCount+0x2a>
   140002e2e:	b8 00 00 00 00       	mov    eax,0x0
   140002e33:	eb 20                	jmp    140002e55 <__mingw_GetSectionCount+0x4a>
   140002e35:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e39:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e3c:	48 63 d0             	movsxd rdx,eax
   140002e3f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e43:	48 01 d0             	add    rax,rdx
   140002e46:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e4a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e4e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e52:	0f b7 c0             	movzx  eax,ax
   140002e55:	48 83 c4 30          	add    rsp,0x30
   140002e59:	5d                   	pop    rbp
   140002e5a:	c3                   	ret

0000000140002e5b <_FindPESectionExec>:
   140002e5b:	55                   	push   rbp
   140002e5c:	48 89 e5             	mov    rbp,rsp
   140002e5f:	48 83 ec 40          	sub    rsp,0x40
   140002e63:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e67:	48 8b 05 f2 24 00 00 	mov    rax,QWORD PTR [rip+0x24f2]        # 140005360 <.refptr.__ImageBase>
   140002e6e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e72:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e76:	48 89 c1             	mov    rcx,rax
   140002e79:	e8 62 fd ff ff       	call   140002be0 <_ValidateImageBase>
   140002e7e:	85 c0                	test   eax,eax
   140002e80:	75 07                	jne    140002e89 <_FindPESectionExec+0x2e>
   140002e82:	b8 00 00 00 00       	mov    eax,0x0
   140002e87:	eb 78                	jmp    140002f01 <_FindPESectionExec+0xa6>
   140002e89:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e8d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e90:	48 63 d0             	movsxd rdx,eax
   140002e93:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e97:	48 01 d0             	add    rax,rdx
   140002e9a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002e9e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002ea5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ea9:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002ead:	0f b7 d0             	movzx  edx,ax
   140002eb0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002eb4:	48 01 d0             	add    rax,rdx
   140002eb7:	48 83 c0 18          	add    rax,0x18
   140002ebb:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ebf:	eb 2b                	jmp    140002eec <_FindPESectionExec+0x91>
   140002ec1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ec5:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002ec8:	25 00 00 00 20       	and    eax,0x20000000
   140002ecd:	85 c0                	test   eax,eax
   140002ecf:	74 12                	je     140002ee3 <_FindPESectionExec+0x88>
   140002ed1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002ed6:	75 06                	jne    140002ede <_FindPESectionExec+0x83>
   140002ed8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002edc:	eb 23                	jmp    140002f01 <_FindPESectionExec+0xa6>
   140002ede:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002ee3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002ee7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002eec:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ef0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002ef4:	0f b7 c0             	movzx  eax,ax
   140002ef7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002efa:	72 c5                	jb     140002ec1 <_FindPESectionExec+0x66>
   140002efc:	b8 00 00 00 00       	mov    eax,0x0
   140002f01:	48 83 c4 40          	add    rsp,0x40
   140002f05:	5d                   	pop    rbp
   140002f06:	c3                   	ret

0000000140002f07 <_GetPEImageBase>:
   140002f07:	55                   	push   rbp
   140002f08:	48 89 e5             	mov    rbp,rsp
   140002f0b:	48 83 ec 30          	sub    rsp,0x30
   140002f0f:	48 8b 05 4a 24 00 00 	mov    rax,QWORD PTR [rip+0x244a]        # 140005360 <.refptr.__ImageBase>
   140002f16:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f1a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f1e:	48 89 c1             	mov    rcx,rax
   140002f21:	e8 ba fc ff ff       	call   140002be0 <_ValidateImageBase>
   140002f26:	85 c0                	test   eax,eax
   140002f28:	75 07                	jne    140002f31 <_GetPEImageBase+0x2a>
   140002f2a:	b8 00 00 00 00       	mov    eax,0x0
   140002f2f:	eb 04                	jmp    140002f35 <_GetPEImageBase+0x2e>
   140002f31:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f35:	48 83 c4 30          	add    rsp,0x30
   140002f39:	5d                   	pop    rbp
   140002f3a:	c3                   	ret

0000000140002f3b <_IsNonwritableInCurrentImage>:
   140002f3b:	55                   	push   rbp
   140002f3c:	48 89 e5             	mov    rbp,rsp
   140002f3f:	48 83 ec 40          	sub    rsp,0x40
   140002f43:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f47:	48 8b 05 12 24 00 00 	mov    rax,QWORD PTR [rip+0x2412]        # 140005360 <.refptr.__ImageBase>
   140002f4e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f52:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f56:	48 89 c1             	mov    rcx,rax
   140002f59:	e8 82 fc ff ff       	call   140002be0 <_ValidateImageBase>
   140002f5e:	85 c0                	test   eax,eax
   140002f60:	75 07                	jne    140002f69 <_IsNonwritableInCurrentImage+0x2e>
   140002f62:	b8 00 00 00 00       	mov    eax,0x0
   140002f67:	eb 3d                	jmp    140002fa6 <_IsNonwritableInCurrentImage+0x6b>
   140002f69:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f6d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f71:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f75:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f79:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f7d:	48 89 c1             	mov    rcx,rax
   140002f80:	e8 d7 fc ff ff       	call   140002c5c <_FindPESection>
   140002f85:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f89:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140002f8e:	75 07                	jne    140002f97 <_IsNonwritableInCurrentImage+0x5c>
   140002f90:	b8 00 00 00 00       	mov    eax,0x0
   140002f95:	eb 0f                	jmp    140002fa6 <_IsNonwritableInCurrentImage+0x6b>
   140002f97:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f9b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002f9e:	f7 d0                	not    eax
   140002fa0:	c1 e8 1f             	shr    eax,0x1f
   140002fa3:	0f b6 c0             	movzx  eax,al
   140002fa6:	48 83 c4 40          	add    rsp,0x40
   140002faa:	5d                   	pop    rbp
   140002fab:	c3                   	ret

0000000140002fac <__mingw_enum_import_library_names>:
   140002fac:	55                   	push   rbp
   140002fad:	48 89 e5             	mov    rbp,rsp
   140002fb0:	48 83 ec 50          	sub    rsp,0x50
   140002fb4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002fb7:	48 8b 05 a2 23 00 00 	mov    rax,QWORD PTR [rip+0x23a2]        # 140005360 <.refptr.__ImageBase>
   140002fbe:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002fc2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fc6:	48 89 c1             	mov    rcx,rax
   140002fc9:	e8 12 fc ff ff       	call   140002be0 <_ValidateImageBase>
   140002fce:	85 c0                	test   eax,eax
   140002fd0:	75 0a                	jne    140002fdc <__mingw_enum_import_library_names+0x30>
   140002fd2:	b8 00 00 00 00       	mov    eax,0x0
   140002fd7:	e9 ab 00 00 00       	jmp    140003087 <__mingw_enum_import_library_names+0xdb>
   140002fdc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fe0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002fe3:	48 63 d0             	movsxd rdx,eax
   140002fe6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fea:	48 01 d0             	add    rax,rdx
   140002fed:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002ff1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002ff5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   140002ffb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140002ffe:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140003002:	75 07                	jne    14000300b <__mingw_enum_import_library_names+0x5f>
   140003004:	b8 00 00 00 00       	mov    eax,0x0
   140003009:	eb 7c                	jmp    140003087 <__mingw_enum_import_library_names+0xdb>
   14000300b:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000300e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003012:	48 89 c1             	mov    rcx,rax
   140003015:	e8 42 fc ff ff       	call   140002c5c <_FindPESection>
   14000301a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000301e:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140003023:	75 07                	jne    14000302c <__mingw_enum_import_library_names+0x80>
   140003025:	b8 00 00 00 00       	mov    eax,0x0
   14000302a:	eb 5b                	jmp    140003087 <__mingw_enum_import_library_names+0xdb>
   14000302c:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000302f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003033:	48 01 d0             	add    rax,rdx
   140003036:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000303a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000303f:	75 07                	jne    140003048 <__mingw_enum_import_library_names+0x9c>
   140003041:	b8 00 00 00 00       	mov    eax,0x0
   140003046:	eb 3f                	jmp    140003087 <__mingw_enum_import_library_names+0xdb>
   140003048:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000304c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000304f:	85 c0                	test   eax,eax
   140003051:	75 0b                	jne    14000305e <__mingw_enum_import_library_names+0xb2>
   140003053:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003057:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000305a:	85 c0                	test   eax,eax
   14000305c:	74 23                	je     140003081 <__mingw_enum_import_library_names+0xd5>
   14000305e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003062:	7f 12                	jg     140003076 <__mingw_enum_import_library_names+0xca>
   140003064:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003068:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000306b:	89 c2                	mov    edx,eax
   14000306d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003071:	48 01 d0             	add    rax,rdx
   140003074:	eb 11                	jmp    140003087 <__mingw_enum_import_library_names+0xdb>
   140003076:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000307a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000307f:	eb c7                	jmp    140003048 <__mingw_enum_import_library_names+0x9c>
   140003081:	90                   	nop
   140003082:	b8 00 00 00 00       	mov    eax,0x0
   140003087:	48 83 c4 50          	add    rsp,0x50
   14000308b:	5d                   	pop    rbp
   14000308c:	c3                   	ret
   14000308d:	90                   	nop
   14000308e:	90                   	nop
   14000308f:	90                   	nop

0000000140003090 <___chkstk_ms>:
   140003090:	51                   	push   rcx
   140003091:	50                   	push   rax
   140003092:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003098:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000309d:	72 19                	jb     1400030b8 <___chkstk_ms+0x28>
   14000309f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   1400030a6:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400030aa:	48 2d 00 10 00 00    	sub    rax,0x1000
   1400030b0:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400030b6:	77 e7                	ja     14000309f <___chkstk_ms+0xf>
   1400030b8:	48 29 c1             	sub    rcx,rax
   1400030bb:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400030bf:	58                   	pop    rax
   1400030c0:	59                   	pop    rcx
   1400030c1:	c3                   	ret
   1400030c2:	90                   	nop
   1400030c3:	90                   	nop
   1400030c4:	90                   	nop
   1400030c5:	90                   	nop
   1400030c6:	90                   	nop
   1400030c7:	90                   	nop
   1400030c8:	90                   	nop
   1400030c9:	90                   	nop
   1400030ca:	90                   	nop
   1400030cb:	90                   	nop
   1400030cc:	90                   	nop
   1400030cd:	90                   	nop
   1400030ce:	90                   	nop
   1400030cf:	90                   	nop

00000001400030d0 <_initterm_e>:
   1400030d0:	55                   	push   rbp
   1400030d1:	48 89 e5             	mov    rbp,rsp
   1400030d4:	48 83 ec 30          	sub    rsp,0x30
   1400030d8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400030dc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400030e0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400030e4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030e8:	eb 29                	jmp    140003113 <_initterm_e+0x43>
   1400030ea:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030ee:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400030f1:	48 85 c0             	test   rax,rax
   1400030f4:	74 17                	je     14000310d <_initterm_e+0x3d>
   1400030f6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030fa:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400030fd:	ff d0                	call   rax
   1400030ff:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003102:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003106:	74 06                	je     14000310e <_initterm_e+0x3e>
   140003108:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000310b:	eb 15                	jmp    140003122 <_initterm_e+0x52>
   14000310d:	90                   	nop
   14000310e:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140003113:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003117:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   14000311b:	72 cd                	jb     1400030ea <_initterm_e+0x1a>
   14000311d:	b8 00 00 00 00       	mov    eax,0x0
   140003122:	48 83 c4 30          	add    rsp,0x30
   140003126:	5d                   	pop    rbp
   140003127:	c3                   	ret
   140003128:	90                   	nop
   140003129:	90                   	nop
   14000312a:	90                   	nop
   14000312b:	90                   	nop
   14000312c:	90                   	nop
   14000312d:	90                   	nop
   14000312e:	90                   	nop
   14000312f:	90                   	nop

0000000140003130 <__p__fmode>:
   140003130:	55                   	push   rbp
   140003131:	48 89 e5             	mov    rbp,rsp
   140003134:	48 8b 05 95 22 00 00 	mov    rax,QWORD PTR [rip+0x2295]        # 1400053d0 <.refptr.__imp__fmode>
   14000313b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000313e:	5d                   	pop    rbp
   14000313f:	c3                   	ret

0000000140003140 <__p__commode>:
   140003140:	55                   	push   rbp
   140003141:	48 89 e5             	mov    rbp,rsp
   140003144:	48 8b 05 75 22 00 00 	mov    rax,QWORD PTR [rip+0x2275]        # 1400053c0 <.refptr.__imp__commode>
   14000314b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000314e:	5d                   	pop    rbp
   14000314f:	c3                   	ret

0000000140003150 <__p___initenv>:
   140003150:	55                   	push   rbp
   140003151:	48 89 e5             	mov    rbp,rsp
   140003154:	48 8b 05 55 22 00 00 	mov    rax,QWORD PTR [rip+0x2255]        # 1400053b0 <.refptr.__imp___initenv>
   14000315b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000315e:	5d                   	pop    rbp
   14000315f:	c3                   	ret

0000000140003160 <_set_invalid_parameter_handler>:
   140003160:	55                   	push   rbp
   140003161:	48 89 e5             	mov    rbp,rsp
   140003164:	48 83 ec 10          	sub    rsp,0x10
   140003168:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000316c:	48 8d 05 1d 60 00 00 	lea    rax,[rip+0x601d]        # 140009190 <handler>
   140003173:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003177:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000317b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000317f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003183:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003187:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000318a:	48 89 d0             	mov    rax,rdx
   14000318d:	48 83 c4 10          	add    rsp,0x10
   140003191:	5d                   	pop    rbp
   140003192:	c3                   	ret

0000000140003193 <_get_invalid_parameter_handler>:
   140003193:	55                   	push   rbp
   140003194:	48 89 e5             	mov    rbp,rsp
   140003197:	48 8b 05 f2 5f 00 00 	mov    rax,QWORD PTR [rip+0x5ff2]        # 140009190 <handler>
   14000319e:	5d                   	pop    rbp
   14000319f:	c3                   	ret

00000001400031a0 <_configthreadlocale>:
   1400031a0:	55                   	push   rbp
   1400031a1:	48 89 e5             	mov    rbp,rsp
   1400031a4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400031a7:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   1400031ab:	75 07                	jne    1400031b4 <_configthreadlocale+0x14>
   1400031ad:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400031b2:	eb 05                	jmp    1400031b9 <_configthreadlocale+0x19>
   1400031b4:	b8 02 00 00 00       	mov    eax,0x2
   1400031b9:	5d                   	pop    rbp
   1400031ba:	c3                   	ret
   1400031bb:	90                   	nop
   1400031bc:	90                   	nop
   1400031bd:	90                   	nop
   1400031be:	90                   	nop
   1400031bf:	90                   	nop

00000001400031c0 <__acrt_iob_func>:
   1400031c0:	55                   	push   rbp
   1400031c1:	48 89 e5             	mov    rbp,rsp
   1400031c4:	48 83 ec 20          	sub    rsp,0x20
   1400031c8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400031cb:	e8 30 00 00 00       	call   140003200 <__iob_func>
   1400031d0:	48 89 c1             	mov    rcx,rax
   1400031d3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400031d6:	48 89 d0             	mov    rax,rdx
   1400031d9:	48 01 c0             	add    rax,rax
   1400031dc:	48 01 d0             	add    rax,rdx
   1400031df:	48 c1 e0 04          	shl    rax,0x4
   1400031e3:	48 01 c8             	add    rax,rcx
   1400031e6:	48 83 c4 20          	add    rsp,0x20
   1400031ea:	5d                   	pop    rbp
   1400031eb:	c3                   	ret
   1400031ec:	90                   	nop
   1400031ed:	90                   	nop
   1400031ee:	90                   	nop
   1400031ef:	90                   	nop

00000001400031f0 <__C_specific_handler>:
   1400031f0:	ff 25 0a 70 00 00    	jmp    QWORD PTR [rip+0x700a]        # 14000a200 <__imp___C_specific_handler>
   1400031f6:	90                   	nop
   1400031f7:	90                   	nop

00000001400031f8 <__getmainargs>:
   1400031f8:	ff 25 0a 70 00 00    	jmp    QWORD PTR [rip+0x700a]        # 14000a208 <__imp___getmainargs>
   1400031fe:	90                   	nop
   1400031ff:	90                   	nop

0000000140003200 <__iob_func>:
   140003200:	ff 25 12 70 00 00    	jmp    QWORD PTR [rip+0x7012]        # 14000a218 <__imp___iob_func>
   140003206:	90                   	nop
   140003207:	90                   	nop

0000000140003208 <__set_app_type>:
   140003208:	ff 25 12 70 00 00    	jmp    QWORD PTR [rip+0x7012]        # 14000a220 <__imp___set_app_type>
   14000320e:	90                   	nop
   14000320f:	90                   	nop

0000000140003210 <__setusermatherr>:
   140003210:	ff 25 12 70 00 00    	jmp    QWORD PTR [rip+0x7012]        # 14000a228 <__imp___setusermatherr>
   140003216:	90                   	nop
   140003217:	90                   	nop

0000000140003218 <_amsg_exit>:
   140003218:	ff 25 12 70 00 00    	jmp    QWORD PTR [rip+0x7012]        # 14000a230 <__imp__amsg_exit>
   14000321e:	90                   	nop
   14000321f:	90                   	nop

0000000140003220 <_cexit>:
   140003220:	ff 25 12 70 00 00    	jmp    QWORD PTR [rip+0x7012]        # 14000a238 <__imp__cexit>
   140003226:	90                   	nop
   140003227:	90                   	nop

0000000140003228 <_initterm>:
   140003228:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a250 <__imp__initterm>
   14000322e:	90                   	nop
   14000322f:	90                   	nop

0000000140003230 <_crt_atexit>:
   140003230:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a258 <__imp__crt_atexit>
   140003236:	90                   	nop
   140003237:	90                   	nop

0000000140003238 <abort>:
   140003238:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a260 <__imp_abort>
   14000323e:	90                   	nop
   14000323f:	90                   	nop

0000000140003240 <calloc>:
   140003240:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a268 <__imp_calloc>
   140003246:	90                   	nop
   140003247:	90                   	nop

0000000140003248 <exit>:
   140003248:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a270 <__imp_exit>
   14000324e:	90                   	nop
   14000324f:	90                   	nop

0000000140003250 <fflush>:
   140003250:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a278 <__imp_fflush>
   140003256:	90                   	nop
   140003257:	90                   	nop

0000000140003258 <fprintf>:
   140003258:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a280 <__imp_fprintf>
   14000325e:	90                   	nop
   14000325f:	90                   	nop

0000000140003260 <free>:
   140003260:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a288 <__imp_free>
   140003266:	90                   	nop
   140003267:	90                   	nop

0000000140003268 <malloc>:
   140003268:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a290 <__imp_malloc>
   14000326e:	90                   	nop
   14000326f:	90                   	nop

0000000140003270 <memcpy>:
   140003270:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a298 <__imp_memcpy>
   140003276:	90                   	nop
   140003277:	90                   	nop

0000000140003278 <setvbuf>:
   140003278:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a2a0 <__imp_setvbuf>
   14000327e:	90                   	nop
   14000327f:	90                   	nop

0000000140003280 <signal>:
   140003280:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a2a8 <__imp_signal>
   140003286:	90                   	nop
   140003287:	90                   	nop

0000000140003288 <strlen>:
   140003288:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a2b0 <__imp_strlen>
   14000328e:	90                   	nop
   14000328f:	90                   	nop

0000000140003290 <strncmp>:
   140003290:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a2b8 <__imp_strncmp>
   140003296:	90                   	nop
   140003297:	90                   	nop

0000000140003298 <vfprintf>:
   140003298:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a2c0 <__imp_vfprintf>
   14000329e:	90                   	nop
   14000329f:	90                   	nop

00000001400032a0 <VirtualQuery>:
   1400032a0:	ff 25 4a 6f 00 00    	jmp    QWORD PTR [rip+0x6f4a]        # 14000a1f0 <__imp_VirtualQuery>
   1400032a6:	90                   	nop
   1400032a7:	90                   	nop

00000001400032a8 <VirtualProtect>:
   1400032a8:	ff 25 3a 6f 00 00    	jmp    QWORD PTR [rip+0x6f3a]        # 14000a1e8 <__imp_VirtualProtect>
   1400032ae:	90                   	nop
   1400032af:	90                   	nop

00000001400032b0 <TlsGetValue>:
   1400032b0:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a1e0 <__imp_TlsGetValue>
   1400032b6:	90                   	nop
   1400032b7:	90                   	nop

00000001400032b8 <Sleep>:
   1400032b8:	ff 25 1a 6f 00 00    	jmp    QWORD PTR [rip+0x6f1a]        # 14000a1d8 <__imp_Sleep>
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <SetUnhandledExceptionFilter>:
   1400032c0:	ff 25 0a 6f 00 00    	jmp    QWORD PTR [rip+0x6f0a]        # 14000a1d0 <__imp_SetUnhandledExceptionFilter>
   1400032c6:	90                   	nop
   1400032c7:	90                   	nop

00000001400032c8 <LoadLibraryA>:
   1400032c8:	ff 25 fa 6e 00 00    	jmp    QWORD PTR [rip+0x6efa]        # 14000a1c8 <__imp_LoadLibraryA>
   1400032ce:	90                   	nop
   1400032cf:	90                   	nop

00000001400032d0 <LeaveCriticalSection>:
   1400032d0:	ff 25 ea 6e 00 00    	jmp    QWORD PTR [rip+0x6eea]        # 14000a1c0 <__imp_LeaveCriticalSection>
   1400032d6:	90                   	nop
   1400032d7:	90                   	nop

00000001400032d8 <InitializeCriticalSection>:
   1400032d8:	ff 25 da 6e 00 00    	jmp    QWORD PTR [rip+0x6eda]        # 14000a1b8 <__imp_InitializeCriticalSection>
   1400032de:	90                   	nop
   1400032df:	90                   	nop

00000001400032e0 <GetProcAddress>:
   1400032e0:	ff 25 ca 6e 00 00    	jmp    QWORD PTR [rip+0x6eca]        # 14000a1b0 <__imp_GetProcAddress>
   1400032e6:	90                   	nop
   1400032e7:	90                   	nop

00000001400032e8 <GetModuleHandleA>:
   1400032e8:	ff 25 ba 6e 00 00    	jmp    QWORD PTR [rip+0x6eba]        # 14000a1a8 <__imp_GetModuleHandleA>
   1400032ee:	90                   	nop
   1400032ef:	90                   	nop

00000001400032f0 <GetLastError>:
   1400032f0:	ff 25 aa 6e 00 00    	jmp    QWORD PTR [rip+0x6eaa]        # 14000a1a0 <__imp_GetLastError>
   1400032f6:	90                   	nop
   1400032f7:	90                   	nop

00000001400032f8 <FreeLibrary>:
   1400032f8:	ff 25 9a 6e 00 00    	jmp    QWORD PTR [rip+0x6e9a]        # 14000a198 <__imp_FreeLibrary>
   1400032fe:	90                   	nop
   1400032ff:	90                   	nop

0000000140003300 <EnterCriticalSection>:
   140003300:	ff 25 8a 6e 00 00    	jmp    QWORD PTR [rip+0x6e8a]        # 14000a190 <__imp_EnterCriticalSection>
   140003306:	90                   	nop
   140003307:	90                   	nop

0000000140003308 <DeleteCriticalSection>:
   140003308:	ff 25 7a 6e 00 00    	jmp    QWORD PTR [rip+0x6e7a]        # 14000a188 <__IAT_start__>
   14000330e:	90                   	nop
   14000330f:	90                   	nop

0000000140003310 <main>:
   140003310:	48 83 ec 38          	sub    rsp,0x38
   140003314:	e8 5e e5 ff ff       	call   140001877 <__main>
   140003319:	48 8d 4c 24 28       	lea    rcx,[rsp+0x28]
   14000331e:	48 c7 44 24 28 07 00 	mov    QWORD PTR [rsp+0x28],0x7
   140003325:	00 00 
   140003327:	c7 44 24 24 00 00 00 	mov    DWORD PTR [rsp+0x24],0x0
   14000332e:	00 
   14000332f:	e8 2c e4 ff ff       	call   140001760 <dispatch_visit(std::variant<A, B, C> const&)>
   140003334:	89 44 24 24          	mov    DWORD PTR [rsp+0x24],eax
   140003338:	e8 43 e4 ff ff       	call   140001780 <dispatch_manual(std::variant<A, B, C> const&)>
   14000333d:	89 44 24 24          	mov    DWORD PTR [rsp+0x24],eax
   140003341:	8b 44 24 24          	mov    eax,DWORD PTR [rsp+0x24]
   140003345:	48 83 c4 38          	add    rsp,0x38
   140003349:	c3                   	ret
   14000334a:	90                   	nop
   14000334b:	90                   	nop
   14000334c:	90                   	nop
   14000334d:	90                   	nop
   14000334e:	90                   	nop
   14000334f:	90                   	nop

0000000140003350 <register_frame_ctor>:
   140003350:	e9 1b e3 ff ff       	jmp    140001670 <__gcc_register_frame>
   140003355:	90                   	nop
   140003356:	90                   	nop
   140003357:	90                   	nop
   140003358:	90                   	nop
   140003359:	90                   	nop
   14000335a:	90                   	nop
   14000335b:	90                   	nop
   14000335c:	90                   	nop
   14000335d:	90                   	nop
   14000335e:	90                   	nop
   14000335f:	90                   	nop
