
/tmp/ch88_optional.exe:     file format pei-x86-64


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
   140001024:	e8 47 22 00 00       	call   140003270 <fflush>
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
   14000113b:	e8 f8 20 00 00       	call   140003238 <_amsg_exit>
   140001140:	48 8b 05 f9 42 00 00 	mov    rax,QWORD PTR [rip+0x42f9]        # 140005440 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 e8 42 00 00 	mov    rax,QWORD PTR [rip+0x42e8]        # 140005440 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 78 20 00 00       	call   1400031e0 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 17 21 00 00       	call   140003298 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 bf 20 00 00       	call   140003258 <abort>
   140001199:	e8 42 11 00 00       	call   1400022e0 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 1b 43 00 00 	mov    rax,QWORD PTR [rip+0x431b]        # 1400054c0 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 21 90 00 00 	mov    rax,QWORD PTR [rip+0x9021]        # 14000a1d0 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 68 42 00 00 	mov    rdx,QWORD PTR [rip+0x4268]        # 140005420 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 b6 1f 00 00       	call   140003180 <_set_invalid_parameter_handler>
   1400011ca:	e8 21 1a 00 00       	call   140002bf0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 ff 41 00 00 	mov    rax,QWORD PTR [rip+0x41ff]        # 1400053e0 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 37 20 00 00       	call   140003228 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 2b 20 00 00       	call   140003228 <__set_app_type>
   1400011fd:	e8 4e 1f 00 00       	call   140003150 <__p__fmode>
   140001202:	48 8b 15 a7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42a7]        # 1400054b0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 4e 1f 00 00       	call   140003160 <__p__commode>
   140001212:	48 8b 15 77 42 00 00 	mov    rdx,QWORD PTR [rip+0x4277]        # 140005490 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 9e 06 00 00       	call   1400018c0 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 03 20 00 00       	call   140003238 <_amsg_exit>
   140001235:	48 8b 05 04 41 00 00 	mov    rax,QWORD PTR [rip+0x4104]        # 140005340 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 86 42 00 00 	mov    rax,QWORD PTR [rip+0x4286]        # 1400054d0 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 a8 11 00 00       	call   1400023fa <__mingw_setusermatherr>
   140001252:	48 8b 05 47 41 00 00 	mov    rax,QWORD PTR [rip+0x4147]        # 1400053a0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 56 1f 00 00       	call   1400031c0 <_configthreadlocale>
   14000126a:	48 8b 15 0f 42 00 00 	mov    rdx,QWORD PTR [rip+0x420f]        # 140005480 <.refptr.__xi_z>
   140001271:	48 8b 05 f8 41 00 00 	mov    rax,QWORD PTR [rip+0x41f8]        # 140005470 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 70 1e 00 00       	call   1400030f0 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 aa 1f 00 00       	call   140003238 <_amsg_exit>
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
   1400012cb:	e8 48 1f 00 00       	call   140003218 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 55 1f 00 00       	call   140003238 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 2e 1f 00 00       	call   140003238 <_amsg_exit>
   14000130a:	48 8b 15 4f 41 00 00 	mov    rdx,QWORD PTR [rip+0x414f]        # 140005460 <.refptr.__xc_z>
   140001311:	48 8b 05 38 41 00 00 	mov    rax,QWORD PTR [rip+0x4138]        # 140005450 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 28 1f 00 00       	call   140003248 <_initterm>
   140001320:	e8 72 05 00 00       	call   140001897 <__main>
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
   14000138d:	e8 de 1d 00 00       	call   140003170 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 76 1f 00 00       	call   140003330 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 97 1e 00 00       	call   140003268 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 60 1e 00 00       	call   140003240 <_cexit>
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
   140001511:	e8 72 1d 00 00       	call   140003288 <malloc>
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
   14000155c:	e8 47 1d 00 00       	call   1400032a8 <strlen>
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
   140001585:	e8 fe 1c 00 00       	call   140003288 <malloc>
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
   1400015e8:	e8 a3 1c 00 00       	call   140003290 <memcpy>
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
   140001642:	e8 09 1c 00 00       	call   140003250 <_crt_atexit>
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

0000000140001760 <get_opt(std::optional<int>)>:
   140001760:	48 89 c8             	mov    rax,rcx
   140001763:	48 89 4c 24 08       	mov    QWORD PTR [rsp+0x8],rcx
   140001768:	48 c1 e8 20          	shr    rax,0x20
   14000176c:	84 c0                	test   al,al
   14000176e:	74 08                	je     140001778 <get_opt(std::optional<int>)+0x18>
   140001770:	8b 44 24 08          	mov    eax,DWORD PTR [rsp+0x8]
   140001774:	c3                   	ret
   140001775:	0f 1f 00             	nop    DWORD PTR [rax]
   140001778:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000177d:	c3                   	ret
   14000177e:	66 90                	xchg   ax,ax

0000000140001780 <get_raw(int const*)>:
   140001780:	48 85 c9             	test   rcx,rcx
   140001783:	74 0b                	je     140001790 <get_raw(int const*)+0x10>
   140001785:	8b 01                	mov    eax,DWORD PTR [rcx]
   140001787:	c3                   	ret
   140001788:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000178f:	00 
   140001790:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140001795:	c3                   	ret
   140001796:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
   14000179d:	00 00 00 

00000001400017a0 <opt_use(std::optional<int>)>:
   1400017a0:	48 89 c8             	mov    rax,rcx
   1400017a3:	48 c1 e8 20          	shr    rax,0x20
   1400017a7:	0f b6 c0             	movzx  eax,al
   1400017aa:	01 c8                	add    eax,ecx
   1400017ac:	c3                   	ret
   1400017ad:	0f 1f 00             	nop    DWORD PTR [rax]

00000001400017b0 <emit_sizes()>:
   1400017b0:	c7 05 c6 78 00 00 08 	mov    DWORD PTR [rip+0x78c6],0x8        # 140009080 <g_obs>
   1400017b7:	00 00 00 
   1400017ba:	c7 05 bc 78 00 00 04 	mov    DWORD PTR [rip+0x78bc],0x4        # 140009080 <g_obs>
   1400017c1:	00 00 00 
   1400017c4:	c7 05 b2 78 00 00 10 	mov    DWORD PTR [rip+0x78b2],0x10        # 140009080 <g_obs>
   1400017cb:	00 00 00 
   1400017ce:	c7 05 a8 78 00 00 02 	mov    DWORD PTR [rip+0x78a8],0x2        # 140009080 <g_obs>
   1400017d5:	00 00 00 
   1400017d8:	c3                   	ret
   1400017d9:	90                   	nop
   1400017da:	90                   	nop
   1400017db:	90                   	nop
   1400017dc:	90                   	nop
   1400017dd:	90                   	nop
   1400017de:	90                   	nop
   1400017df:	90                   	nop

00000001400017e0 <__do_global_dtors>:
   1400017e0:	55                   	push   rbp
   1400017e1:	48 89 e5             	mov    rbp,rsp
   1400017e4:	48 83 ec 20          	sub    rsp,0x20
   1400017e8:	eb 1e                	jmp    140001808 <__do_global_dtors+0x28>
   1400017ea:	48 8b 05 1f 28 00 00 	mov    rax,QWORD PTR [rip+0x281f]        # 140004010 <p.0>
   1400017f1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017f4:	ff d0                	call   rax
   1400017f6:	48 8b 05 13 28 00 00 	mov    rax,QWORD PTR [rip+0x2813]        # 140004010 <p.0>
   1400017fd:	48 83 c0 08          	add    rax,0x8
   140001801:	48 89 05 08 28 00 00 	mov    QWORD PTR [rip+0x2808],rax        # 140004010 <p.0>
   140001808:	48 8b 05 01 28 00 00 	mov    rax,QWORD PTR [rip+0x2801]        # 140004010 <p.0>
   14000180f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001812:	48 85 c0             	test   rax,rax
   140001815:	75 d3                	jne    1400017ea <__do_global_dtors+0xa>
   140001817:	90                   	nop
   140001818:	90                   	nop
   140001819:	48 83 c4 20          	add    rsp,0x20
   14000181d:	5d                   	pop    rbp
   14000181e:	c3                   	ret

000000014000181f <__do_global_ctors>:
   14000181f:	55                   	push   rbp
   140001820:	48 89 e5             	mov    rbp,rsp
   140001823:	48 83 ec 30          	sub    rsp,0x30
   140001827:	48 8b 05 22 3b 00 00 	mov    rax,QWORD PTR [rip+0x3b22]        # 140005350 <.refptr.__CTOR_LIST__>
   14000182e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001831:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001834:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   140001838:	75 25                	jne    14000185f <__do_global_ctors+0x40>
   14000183a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001841:	eb 04                	jmp    140001847 <__do_global_ctors+0x28>
   140001843:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001847:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000184a:	8d 50 01             	lea    edx,[rax+0x1]
   14000184d:	48 8b 05 fc 3a 00 00 	mov    rax,QWORD PTR [rip+0x3afc]        # 140005350 <.refptr.__CTOR_LIST__>
   140001854:	89 d2                	mov    edx,edx
   140001856:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000185a:	48 85 c0             	test   rax,rax
   14000185d:	75 e4                	jne    140001843 <__do_global_ctors+0x24>
   14000185f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001862:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001865:	eb 14                	jmp    14000187b <__do_global_ctors+0x5c>
   140001867:	48 8b 05 e2 3a 00 00 	mov    rax,QWORD PTR [rip+0x3ae2]        # 140005350 <.refptr.__CTOR_LIST__>
   14000186e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001871:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001875:	ff d0                	call   rax
   140001877:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000187b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000187f:	75 e6                	jne    140001867 <__do_global_ctors+0x48>
   140001881:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 1400017e0 <__do_global_dtors>
   140001888:	48 89 c1             	mov    rcx,rax
   14000188b:	e8 9f fd ff ff       	call   14000162f <atexit>
   140001890:	90                   	nop
   140001891:	48 83 c4 30          	add    rsp,0x30
   140001895:	5d                   	pop    rbp
   140001896:	c3                   	ret

0000000140001897 <__main>:
   140001897:	55                   	push   rbp
   140001898:	48 89 e5             	mov    rbp,rsp
   14000189b:	48 83 ec 20          	sub    rsp,0x20
   14000189f:	8b 05 eb 77 00 00    	mov    eax,DWORD PTR [rip+0x77eb]        # 140009090 <initialized>
   1400018a5:	85 c0                	test   eax,eax
   1400018a7:	75 0f                	jne    1400018b8 <__main+0x21>
   1400018a9:	c7 05 dd 77 00 00 01 	mov    DWORD PTR [rip+0x77dd],0x1        # 140009090 <initialized>
   1400018b0:	00 00 00 
   1400018b3:	e8 67 ff ff ff       	call   14000181f <__do_global_ctors>
   1400018b8:	90                   	nop
   1400018b9:	48 83 c4 20          	add    rsp,0x20
   1400018bd:	5d                   	pop    rbp
   1400018be:	c3                   	ret
   1400018bf:	90                   	nop

00000001400018c0 <_setargv>:
   1400018c0:	55                   	push   rbp
   1400018c1:	48 89 e5             	mov    rbp,rsp
   1400018c4:	b8 00 00 00 00       	mov    eax,0x0
   1400018c9:	5d                   	pop    rbp
   1400018ca:	c3                   	ret
   1400018cb:	90                   	nop
   1400018cc:	90                   	nop
   1400018cd:	90                   	nop
   1400018ce:	90                   	nop
   1400018cf:	90                   	nop

00000001400018d0 <__dyn_tls_init>:
   1400018d0:	55                   	push   rbp
   1400018d1:	48 89 e5             	mov    rbp,rsp
   1400018d4:	48 83 ec 30          	sub    rsp,0x30
   1400018d8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400018dc:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   1400018df:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400018e3:	48 8b 05 46 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a46]        # 140005330 <.refptr._CRT_MT>
   1400018ea:	8b 00                	mov    eax,DWORD PTR [rax]
   1400018ec:	83 f8 02             	cmp    eax,0x2
   1400018ef:	74 0d                	je     1400018fe <__dyn_tls_init+0x2e>
   1400018f1:	48 8b 05 38 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a38]        # 140005330 <.refptr._CRT_MT>
   1400018f8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   1400018fe:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140001902:	74 1e                	je     140001922 <__dyn_tls_init+0x52>
   140001904:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140001908:	75 5b                	jne    140001965 <__dyn_tls_init+0x95>
   14000190a:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   14000190e:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140001911:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001915:	49 89 c8             	mov    r8,rcx
   140001918:	48 89 c1             	mov    rcx,rax
   14000191b:	e8 d1 11 00 00       	call   140002af1 <__mingw_TLScallback>
   140001920:	eb 43                	jmp    140001965 <__dyn_tls_init+0x95>
   140001922:	48 8d 05 6f 3d 00 00 	lea    rax,[rip+0x3d6f]        # 140005698 <___crt_xd_start__>
   140001929:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000192d:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001932:	eb 22                	jmp    140001956 <__dyn_tls_init+0x86>
   140001934:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001938:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000193c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001940:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001943:	48 85 c0             	test   rax,rax
   140001946:	74 09                	je     140001951 <__dyn_tls_init+0x81>
   140001948:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000194c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000194f:	ff d0                	call   rax
   140001951:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001956:	48 8d 05 43 3d 00 00 	lea    rax,[rip+0x3d43]        # 1400056a0 <__xd_z>
   14000195d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001961:	75 d1                	jne    140001934 <__dyn_tls_init+0x64>
   140001963:	eb 01                	jmp    140001966 <__dyn_tls_init+0x96>
   140001965:	90                   	nop
   140001966:	48 83 c4 30          	add    rsp,0x30
   14000196a:	5d                   	pop    rbp
   14000196b:	c3                   	ret

000000014000196c <__tlregdtor>:
   14000196c:	55                   	push   rbp
   14000196d:	48 89 e5             	mov    rbp,rsp
   140001970:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001974:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001979:	75 07                	jne    140001982 <__tlregdtor+0x16>
   14000197b:	b8 00 00 00 00       	mov    eax,0x0
   140001980:	eb 05                	jmp    140001987 <__tlregdtor+0x1b>
   140001982:	b8 00 00 00 00       	mov    eax,0x0
   140001987:	5d                   	pop    rbp
   140001988:	c3                   	ret

0000000140001989 <__dyn_tls_dtor>:
   140001989:	55                   	push   rbp
   14000198a:	48 89 e5             	mov    rbp,rsp
   14000198d:	48 83 ec 20          	sub    rsp,0x20
   140001991:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001995:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001998:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000199c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   1400019a0:	74 06                	je     1400019a8 <__dyn_tls_dtor+0x1f>
   1400019a2:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   1400019a6:	75 18                	jne    1400019c0 <__dyn_tls_dtor+0x37>
   1400019a8:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400019ac:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400019af:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400019b3:	49 89 c8             	mov    r8,rcx
   1400019b6:	48 89 c1             	mov    rcx,rax
   1400019b9:	e8 33 11 00 00       	call   140002af1 <__mingw_TLScallback>
   1400019be:	eb 01                	jmp    1400019c1 <__dyn_tls_dtor+0x38>
   1400019c0:	90                   	nop
   1400019c1:	48 83 c4 20          	add    rsp,0x20
   1400019c5:	5d                   	pop    rbp
   1400019c6:	c3                   	ret
   1400019c7:	90                   	nop
   1400019c8:	90                   	nop
   1400019c9:	90                   	nop
   1400019ca:	90                   	nop
   1400019cb:	90                   	nop
   1400019cc:	90                   	nop
   1400019cd:	90                   	nop
   1400019ce:	90                   	nop
   1400019cf:	90                   	nop

00000001400019d0 <_matherr>:
   1400019d0:	55                   	push   rbp
   1400019d1:	53                   	push   rbx
   1400019d2:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   1400019d9:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   1400019de:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   1400019e2:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   1400019e6:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   1400019eb:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   1400019ef:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   1400019f3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400019f5:	83 f8 06             	cmp    eax,0x6
   1400019f8:	74 56                	je     140001a50 <_matherr+0x80>
   1400019fa:	83 f8 06             	cmp    eax,0x6
   1400019fd:	7f 78                	jg     140001a77 <_matherr+0xa7>
   1400019ff:	83 f8 05             	cmp    eax,0x5
   140001a02:	74 59                	je     140001a5d <_matherr+0x8d>
   140001a04:	83 f8 05             	cmp    eax,0x5
   140001a07:	7f 6e                	jg     140001a77 <_matherr+0xa7>
   140001a09:	83 f8 04             	cmp    eax,0x4
   140001a0c:	74 5c                	je     140001a6a <_matherr+0x9a>
   140001a0e:	83 f8 04             	cmp    eax,0x4
   140001a11:	7f 64                	jg     140001a77 <_matherr+0xa7>
   140001a13:	83 f8 03             	cmp    eax,0x3
   140001a16:	74 2b                	je     140001a43 <_matherr+0x73>
   140001a18:	83 f8 03             	cmp    eax,0x3
   140001a1b:	7f 5a                	jg     140001a77 <_matherr+0xa7>
   140001a1d:	83 f8 01             	cmp    eax,0x1
   140001a20:	74 07                	je     140001a29 <_matherr+0x59>
   140001a22:	83 f8 02             	cmp    eax,0x2
   140001a25:	74 0f                	je     140001a36 <_matherr+0x66>
   140001a27:	eb 4e                	jmp    140001a77 <_matherr+0xa7>
   140001a29:	48 8d 05 70 36 00 00 	lea    rax,[rip+0x3670]        # 1400050a0 <.rdata>
   140001a30:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a34:	eb 4d                	jmp    140001a83 <_matherr+0xb3>
   140001a36:	48 8d 05 82 36 00 00 	lea    rax,[rip+0x3682]        # 1400050bf <.rdata+0x1f>
   140001a3d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a41:	eb 40                	jmp    140001a83 <_matherr+0xb3>
   140001a43:	48 8d 05 96 36 00 00 	lea    rax,[rip+0x3696]        # 1400050e0 <.rdata+0x40>
   140001a4a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a4e:	eb 33                	jmp    140001a83 <_matherr+0xb3>
   140001a50:	48 8d 05 a9 36 00 00 	lea    rax,[rip+0x36a9]        # 140005100 <.rdata+0x60>
   140001a57:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a5b:	eb 26                	jmp    140001a83 <_matherr+0xb3>
   140001a5d:	48 8d 05 c4 36 00 00 	lea    rax,[rip+0x36c4]        # 140005128 <.rdata+0x88>
   140001a64:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a68:	eb 19                	jmp    140001a83 <_matherr+0xb3>
   140001a6a:	48 8d 05 df 36 00 00 	lea    rax,[rip+0x36df]        # 140005150 <.rdata+0xb0>
   140001a71:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a75:	eb 0c                	jmp    140001a83 <_matherr+0xb3>
   140001a77:	48 8d 05 08 37 00 00 	lea    rax,[rip+0x3708]        # 140005186 <.rdata+0xe6>
   140001a7e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a82:	90                   	nop
   140001a83:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a87:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001a8d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a91:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001a96:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a9a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001a9f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001aa3:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001aa7:	b9 02 00 00 00       	mov    ecx,0x2
   140001aac:	e8 2f 17 00 00       	call   1400031e0 <__acrt_iob_func>
   140001ab1:	48 89 c1             	mov    rcx,rax
   140001ab4:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001ab8:	48 8d 05 d9 36 00 00 	lea    rax,[rip+0x36d9]        # 140005198 <.rdata+0xf8>
   140001abf:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001ac6:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001acc:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001ad2:	49 89 d9             	mov    r9,rbx
   140001ad5:	49 89 d0             	mov    r8,rdx
   140001ad8:	48 89 c2             	mov    rdx,rax
   140001adb:	e8 98 17 00 00       	call   140003278 <fprintf>
   140001ae0:	b8 00 00 00 00       	mov    eax,0x0
   140001ae5:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001ae9:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001aed:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001af2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001af9:	5b                   	pop    rbx
   140001afa:	5d                   	pop    rbp
   140001afb:	c3                   	ret
   140001afc:	90                   	nop
   140001afd:	90                   	nop
   140001afe:	90                   	nop
   140001aff:	90                   	nop

0000000140001b00 <__report_error>:
   140001b00:	55                   	push   rbp
   140001b01:	53                   	push   rbx
   140001b02:	48 83 ec 38          	sub    rsp,0x38
   140001b06:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001b0b:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001b0f:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001b13:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001b17:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001b1b:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001b1f:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b23:	b9 02 00 00 00       	mov    ecx,0x2
   140001b28:	e8 b3 16 00 00       	call   1400031e0 <__acrt_iob_func>
   140001b2d:	48 89 c1             	mov    rcx,rax
   140001b30:	48 8d 05 99 36 00 00 	lea    rax,[rip+0x3699]        # 1400051d0 <.rdata>
   140001b37:	48 89 c2             	mov    rdx,rax
   140001b3a:	e8 39 17 00 00       	call   140003278 <fprintf>
   140001b3f:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001b43:	b9 02 00 00 00       	mov    ecx,0x2
   140001b48:	e8 93 16 00 00       	call   1400031e0 <__acrt_iob_func>
   140001b4d:	48 89 c1             	mov    rcx,rax
   140001b50:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001b54:	49 89 d8             	mov    r8,rbx
   140001b57:	48 89 c2             	mov    rdx,rax
   140001b5a:	e8 59 17 00 00       	call   1400032b8 <vfprintf>
   140001b5f:	e8 f4 16 00 00       	call   140003258 <abort>
   140001b64:	90                   	nop

0000000140001b65 <mark_section_writable>:
   140001b65:	55                   	push   rbp
   140001b66:	48 89 e5             	mov    rbp,rsp
   140001b69:	48 83 ec 60          	sub    rsp,0x60
   140001b6d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b71:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b78:	e9 82 00 00 00       	jmp    140001bff <mark_section_writable+0x9a>
   140001b7d:	48 8b 0d 6c 75 00 00 	mov    rcx,QWORD PTR [rip+0x756c]        # 1400090f0 <the_secs>
   140001b84:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b87:	48 63 d0             	movsxd rdx,eax
   140001b8a:	48 89 d0             	mov    rax,rdx
   140001b8d:	48 c1 e0 02          	shl    rax,0x2
   140001b91:	48 01 d0             	add    rax,rdx
   140001b94:	48 c1 e0 03          	shl    rax,0x3
   140001b98:	48 01 c8             	add    rax,rcx
   140001b9b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001b9f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001ba3:	72 56                	jb     140001bfb <mark_section_writable+0x96>
   140001ba5:	48 8b 0d 44 75 00 00 	mov    rcx,QWORD PTR [rip+0x7544]        # 1400090f0 <the_secs>
   140001bac:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001baf:	48 63 d0             	movsxd rdx,eax
   140001bb2:	48 89 d0             	mov    rax,rdx
   140001bb5:	48 c1 e0 02          	shl    rax,0x2
   140001bb9:	48 01 d0             	add    rax,rdx
   140001bbc:	48 c1 e0 03          	shl    rax,0x3
   140001bc0:	48 01 c8             	add    rax,rcx
   140001bc3:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001bc7:	4c 8b 05 22 75 00 00 	mov    r8,QWORD PTR [rip+0x7522]        # 1400090f0 <the_secs>
   140001bce:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001bd1:	48 63 d0             	movsxd rdx,eax
   140001bd4:	48 89 d0             	mov    rax,rdx
   140001bd7:	48 c1 e0 02          	shl    rax,0x2
   140001bdb:	48 01 d0             	add    rax,rdx
   140001bde:	48 c1 e0 03          	shl    rax,0x3
   140001be2:	4c 01 c0             	add    rax,r8
   140001be5:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001be9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001bec:	89 c0                	mov    eax,eax
   140001bee:	48 01 c8             	add    rax,rcx
   140001bf1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001bf5:	0f 82 41 02 00 00    	jb     140001e3c <mark_section_writable+0x2d7>
   140001bfb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001bff:	8b 05 f3 74 00 00    	mov    eax,DWORD PTR [rip+0x74f3]        # 1400090f8 <maxSections>
   140001c05:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001c08:	0f 8c 6f ff ff ff    	jl     140001b7d <mark_section_writable+0x18>
   140001c0e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001c12:	48 89 c1             	mov    rcx,rax
   140001c15:	e8 c1 11 00 00       	call   140002ddb <__mingw_GetSectionForAddress>
   140001c1a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001c1e:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001c23:	75 13                	jne    140001c38 <mark_section_writable+0xd3>
   140001c25:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001c29:	48 8d 0d c0 35 00 00 	lea    rcx,[rip+0x35c0]        # 1400051f0 <.rdata+0x20>
   140001c30:	48 89 c2             	mov    rdx,rax
   140001c33:	e8 c8 fe ff ff       	call   140001b00 <__report_error>
   140001c38:	48 8b 0d b1 74 00 00 	mov    rcx,QWORD PTR [rip+0x74b1]        # 1400090f0 <the_secs>
   140001c3f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c42:	48 63 d0             	movsxd rdx,eax
   140001c45:	48 89 d0             	mov    rax,rdx
   140001c48:	48 c1 e0 02          	shl    rax,0x2
   140001c4c:	48 01 d0             	add    rax,rdx
   140001c4f:	48 c1 e0 03          	shl    rax,0x3
   140001c53:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001c57:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c5b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001c5f:	48 8b 0d 8a 74 00 00 	mov    rcx,QWORD PTR [rip+0x748a]        # 1400090f0 <the_secs>
   140001c66:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c69:	48 63 d0             	movsxd rdx,eax
   140001c6c:	48 89 d0             	mov    rax,rdx
   140001c6f:	48 c1 e0 02          	shl    rax,0x2
   140001c73:	48 01 d0             	add    rax,rdx
   140001c76:	48 c1 e0 03          	shl    rax,0x3
   140001c7a:	48 01 c8             	add    rax,rcx
   140001c7d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001c83:	e8 9f 12 00 00       	call   140002f27 <_GetPEImageBase>
   140001c88:	48 89 c1             	mov    rcx,rax
   140001c8b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c8f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001c92:	41 89 c1             	mov    r9d,eax
   140001c95:	4c 8b 05 54 74 00 00 	mov    r8,QWORD PTR [rip+0x7454]        # 1400090f0 <the_secs>
   140001c9c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c9f:	48 63 d0             	movsxd rdx,eax
   140001ca2:	48 89 d0             	mov    rax,rdx
   140001ca5:	48 c1 e0 02          	shl    rax,0x2
   140001ca9:	48 01 d0             	add    rax,rdx
   140001cac:	48 c1 e0 03          	shl    rax,0x3
   140001cb0:	4c 01 c0             	add    rax,r8
   140001cb3:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001cb7:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001cbb:	48 8b 0d 2e 74 00 00 	mov    rcx,QWORD PTR [rip+0x742e]        # 1400090f0 <the_secs>
   140001cc2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001cc5:	48 63 d0             	movsxd rdx,eax
   140001cc8:	48 89 d0             	mov    rax,rdx
   140001ccb:	48 c1 e0 02          	shl    rax,0x2
   140001ccf:	48 01 d0             	add    rax,rdx
   140001cd2:	48 c1 e0 03          	shl    rax,0x3
   140001cd6:	48 01 c8             	add    rax,rcx
   140001cd9:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001cdd:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001ce1:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001ce7:	48 89 c1             	mov    rcx,rax
   140001cea:	48 8b 05 ff 84 00 00 	mov    rax,QWORD PTR [rip+0x84ff]        # 14000a1f0 <__imp_VirtualQuery>
   140001cf1:	ff d0                	call   rax
   140001cf3:	48 85 c0             	test   rax,rax
   140001cf6:	75 3f                	jne    140001d37 <mark_section_writable+0x1d2>
   140001cf8:	48 8b 0d f1 73 00 00 	mov    rcx,QWORD PTR [rip+0x73f1]        # 1400090f0 <the_secs>
   140001cff:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d02:	48 63 d0             	movsxd rdx,eax
   140001d05:	48 89 d0             	mov    rax,rdx
   140001d08:	48 c1 e0 02          	shl    rax,0x2
   140001d0c:	48 01 d0             	add    rax,rdx
   140001d0f:	48 c1 e0 03          	shl    rax,0x3
   140001d13:	48 01 c8             	add    rax,rcx
   140001d16:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001d1a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001d1e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001d21:	89 c1                	mov    ecx,eax
   140001d23:	48 8d 05 e6 34 00 00 	lea    rax,[rip+0x34e6]        # 140005210 <.rdata+0x40>
   140001d2a:	49 89 d0             	mov    r8,rdx
   140001d2d:	89 ca                	mov    edx,ecx
   140001d2f:	48 89 c1             	mov    rcx,rax
   140001d32:	e8 c9 fd ff ff       	call   140001b00 <__report_error>
   140001d37:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d3a:	83 f8 40             	cmp    eax,0x40
   140001d3d:	0f 84 e8 00 00 00    	je     140001e2b <mark_section_writable+0x2c6>
   140001d43:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d46:	83 f8 04             	cmp    eax,0x4
   140001d49:	0f 84 dc 00 00 00    	je     140001e2b <mark_section_writable+0x2c6>
   140001d4f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d52:	3d 80 00 00 00       	cmp    eax,0x80
   140001d57:	0f 84 ce 00 00 00    	je     140001e2b <mark_section_writable+0x2c6>
   140001d5d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d60:	83 f8 08             	cmp    eax,0x8
   140001d63:	0f 84 c2 00 00 00    	je     140001e2b <mark_section_writable+0x2c6>
   140001d69:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d6c:	83 f8 02             	cmp    eax,0x2
   140001d6f:	75 09                	jne    140001d7a <mark_section_writable+0x215>
   140001d71:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001d78:	eb 07                	jmp    140001d81 <mark_section_writable+0x21c>
   140001d7a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001d81:	48 8b 0d 68 73 00 00 	mov    rcx,QWORD PTR [rip+0x7368]        # 1400090f0 <the_secs>
   140001d88:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d8b:	48 63 d0             	movsxd rdx,eax
   140001d8e:	48 89 d0             	mov    rax,rdx
   140001d91:	48 c1 e0 02          	shl    rax,0x2
   140001d95:	48 01 d0             	add    rax,rdx
   140001d98:	48 c1 e0 03          	shl    rax,0x3
   140001d9c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001da0:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001da4:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001da8:	48 8b 0d 41 73 00 00 	mov    rcx,QWORD PTR [rip+0x7341]        # 1400090f0 <the_secs>
   140001daf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001db2:	48 63 d0             	movsxd rdx,eax
   140001db5:	48 89 d0             	mov    rax,rdx
   140001db8:	48 c1 e0 02          	shl    rax,0x2
   140001dbc:	48 01 d0             	add    rax,rdx
   140001dbf:	48 c1 e0 03          	shl    rax,0x3
   140001dc3:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001dc7:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001dcb:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001dcf:	48 8b 0d 1a 73 00 00 	mov    rcx,QWORD PTR [rip+0x731a]        # 1400090f0 <the_secs>
   140001dd6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001dd9:	48 63 d0             	movsxd rdx,eax
   140001ddc:	48 89 d0             	mov    rax,rdx
   140001ddf:	48 c1 e0 02          	shl    rax,0x2
   140001de3:	48 01 d0             	add    rax,rdx
   140001de6:	48 c1 e0 03          	shl    rax,0x3
   140001dea:	48 01 c8             	add    rax,rcx
   140001ded:	49 89 c0             	mov    r8,rax
   140001df0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001df4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001df8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001dfb:	4d 89 c1             	mov    r9,r8
   140001dfe:	41 89 c8             	mov    r8d,ecx
   140001e01:	48 89 c1             	mov    rcx,rax
   140001e04:	48 8b 05 dd 83 00 00 	mov    rax,QWORD PTR [rip+0x83dd]        # 14000a1e8 <__imp_VirtualProtect>
   140001e0b:	ff d0                	call   rax
   140001e0d:	85 c0                	test   eax,eax
   140001e0f:	75 1a                	jne    140001e2b <mark_section_writable+0x2c6>
   140001e11:	48 8b 05 88 83 00 00 	mov    rax,QWORD PTR [rip+0x8388]        # 14000a1a0 <__imp_GetLastError>
   140001e18:	ff d0                	call   rax
   140001e1a:	89 c2                	mov    edx,eax
   140001e1c:	48 8d 05 25 34 00 00 	lea    rax,[rip+0x3425]        # 140005248 <.rdata+0x78>
   140001e23:	48 89 c1             	mov    rcx,rax
   140001e26:	e8 d5 fc ff ff       	call   140001b00 <__report_error>
   140001e2b:	8b 05 c7 72 00 00    	mov    eax,DWORD PTR [rip+0x72c7]        # 1400090f8 <maxSections>
   140001e31:	83 c0 01             	add    eax,0x1
   140001e34:	89 05 be 72 00 00    	mov    DWORD PTR [rip+0x72be],eax        # 1400090f8 <maxSections>
   140001e3a:	eb 01                	jmp    140001e3d <mark_section_writable+0x2d8>
   140001e3c:	90                   	nop
   140001e3d:	48 83 c4 60          	add    rsp,0x60
   140001e41:	5d                   	pop    rbp
   140001e42:	c3                   	ret

0000000140001e43 <restore_modified_sections>:
   140001e43:	55                   	push   rbp
   140001e44:	48 89 e5             	mov    rbp,rsp
   140001e47:	48 83 ec 30          	sub    rsp,0x30
   140001e4b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001e52:	e9 ad 00 00 00       	jmp    140001f04 <restore_modified_sections+0xc1>
   140001e57:	48 8b 0d 92 72 00 00 	mov    rcx,QWORD PTR [rip+0x7292]        # 1400090f0 <the_secs>
   140001e5e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e61:	48 63 d0             	movsxd rdx,eax
   140001e64:	48 89 d0             	mov    rax,rdx
   140001e67:	48 c1 e0 02          	shl    rax,0x2
   140001e6b:	48 01 d0             	add    rax,rdx
   140001e6e:	48 c1 e0 03          	shl    rax,0x3
   140001e72:	48 01 c8             	add    rax,rcx
   140001e75:	8b 00                	mov    eax,DWORD PTR [rax]
   140001e77:	85 c0                	test   eax,eax
   140001e79:	0f 84 80 00 00 00    	je     140001eff <restore_modified_sections+0xbc>
   140001e7f:	48 8b 0d 6a 72 00 00 	mov    rcx,QWORD PTR [rip+0x726a]        # 1400090f0 <the_secs>
   140001e86:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e89:	48 63 d0             	movsxd rdx,eax
   140001e8c:	48 89 d0             	mov    rax,rdx
   140001e8f:	48 c1 e0 02          	shl    rax,0x2
   140001e93:	48 01 d0             	add    rax,rdx
   140001e96:	48 c1 e0 03          	shl    rax,0x3
   140001e9a:	48 01 c8             	add    rax,rcx
   140001e9d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001ea0:	48 8b 0d 49 72 00 00 	mov    rcx,QWORD PTR [rip+0x7249]        # 1400090f0 <the_secs>
   140001ea7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001eaa:	48 63 d0             	movsxd rdx,eax
   140001ead:	48 89 d0             	mov    rax,rdx
   140001eb0:	48 c1 e0 02          	shl    rax,0x2
   140001eb4:	48 01 d0             	add    rax,rdx
   140001eb7:	48 c1 e0 03          	shl    rax,0x3
   140001ebb:	48 01 c8             	add    rax,rcx
   140001ebe:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001ec2:	4c 8b 05 27 72 00 00 	mov    r8,QWORD PTR [rip+0x7227]        # 1400090f0 <the_secs>
   140001ec9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ecc:	48 63 d0             	movsxd rdx,eax
   140001ecf:	48 89 d0             	mov    rax,rdx
   140001ed2:	48 c1 e0 02          	shl    rax,0x2
   140001ed6:	48 01 d0             	add    rax,rdx
   140001ed9:	48 c1 e0 03          	shl    rax,0x3
   140001edd:	4c 01 c0             	add    rax,r8
   140001ee0:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001ee4:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001ee8:	49 89 d1             	mov    r9,rdx
   140001eeb:	45 89 d0             	mov    r8d,r10d
   140001eee:	48 89 ca             	mov    rdx,rcx
   140001ef1:	48 89 c1             	mov    rcx,rax
   140001ef4:	48 8b 05 ed 82 00 00 	mov    rax,QWORD PTR [rip+0x82ed]        # 14000a1e8 <__imp_VirtualProtect>
   140001efb:	ff d0                	call   rax
   140001efd:	eb 01                	jmp    140001f00 <restore_modified_sections+0xbd>
   140001eff:	90                   	nop
   140001f00:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001f04:	8b 05 ee 71 00 00    	mov    eax,DWORD PTR [rip+0x71ee]        # 1400090f8 <maxSections>
   140001f0a:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001f0d:	0f 8c 44 ff ff ff    	jl     140001e57 <restore_modified_sections+0x14>
   140001f13:	90                   	nop
   140001f14:	90                   	nop
   140001f15:	48 83 c4 30          	add    rsp,0x30
   140001f19:	5d                   	pop    rbp
   140001f1a:	c3                   	ret

0000000140001f1b <__write_memory>:
   140001f1b:	55                   	push   rbp
   140001f1c:	48 89 e5             	mov    rbp,rsp
   140001f1f:	48 83 ec 20          	sub    rsp,0x20
   140001f23:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f27:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f2b:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f2f:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140001f34:	74 25                	je     140001f5b <__write_memory+0x40>
   140001f36:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f3a:	48 89 c1             	mov    rcx,rax
   140001f3d:	e8 23 fc ff ff       	call   140001b65 <mark_section_writable>
   140001f42:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001f46:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140001f4a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f4e:	49 89 c8             	mov    r8,rcx
   140001f51:	48 89 c1             	mov    rcx,rax
   140001f54:	e8 37 13 00 00       	call   140003290 <memcpy>
   140001f59:	eb 01                	jmp    140001f5c <__write_memory+0x41>
   140001f5b:	90                   	nop
   140001f5c:	48 83 c4 20          	add    rsp,0x20
   140001f60:	5d                   	pop    rbp
   140001f61:	c3                   	ret

0000000140001f62 <do_pseudo_reloc>:
   140001f62:	55                   	push   rbp
   140001f63:	48 89 e5             	mov    rbp,rsp
   140001f66:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   140001f6a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f6e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f72:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f76:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140001f7a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140001f7e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f82:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f86:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001f8a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   140001f8f:	0f 8e 44 03 00 00    	jle    1400022d9 <do_pseudo_reloc+0x377>
   140001f95:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   140001f9a:	7e 25                	jle    140001fc1 <do_pseudo_reloc+0x5f>
   140001f9c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fa0:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fa2:	85 c0                	test   eax,eax
   140001fa4:	75 1b                	jne    140001fc1 <do_pseudo_reloc+0x5f>
   140001fa6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001faa:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fad:	85 c0                	test   eax,eax
   140001faf:	75 10                	jne    140001fc1 <do_pseudo_reloc+0x5f>
   140001fb1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fb5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001fb8:	85 c0                	test   eax,eax
   140001fba:	75 05                	jne    140001fc1 <do_pseudo_reloc+0x5f>
   140001fbc:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140001fc1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fc5:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fc7:	85 c0                	test   eax,eax
   140001fc9:	75 0b                	jne    140001fd6 <do_pseudo_reloc+0x74>
   140001fcb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fcf:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fd2:	85 c0                	test   eax,eax
   140001fd4:	74 59                	je     14000202f <do_pseudo_reloc+0xcd>
   140001fd6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fda:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001fde:	eb 40                	jmp    140002020 <do_pseudo_reloc+0xbe>
   140001fe0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fe4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fe7:	89 c2                	mov    edx,eax
   140001fe9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001fed:	48 01 d0             	add    rax,rdx
   140001ff0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001ff4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001ff8:	8b 10                	mov    edx,DWORD PTR [rax]
   140001ffa:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001ffe:	8b 00                	mov    eax,DWORD PTR [rax]
   140002000:	01 d0                	add    eax,edx
   140002002:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140002005:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002009:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   14000200d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002013:	48 89 c1             	mov    rcx,rax
   140002016:	e8 00 ff ff ff       	call   140001f1b <__write_memory>
   14000201b:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140002020:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002024:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002028:	72 b6                	jb     140001fe0 <do_pseudo_reloc+0x7e>
   14000202a:	e9 ab 02 00 00       	jmp    1400022da <do_pseudo_reloc+0x378>
   14000202f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002033:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002036:	83 f8 01             	cmp    eax,0x1
   140002039:	74 18                	je     140002053 <do_pseudo_reloc+0xf1>
   14000203b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000203f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002042:	89 c2                	mov    edx,eax
   140002044:	48 8d 05 25 32 00 00 	lea    rax,[rip+0x3225]        # 140005270 <.rdata+0xa0>
   14000204b:	48 89 c1             	mov    rcx,rax
   14000204e:	e8 ad fa ff ff       	call   140001b00 <__report_error>
   140002053:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002057:	48 83 c0 0c          	add    rax,0xc
   14000205b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000205f:	e9 65 02 00 00       	jmp    1400022c9 <do_pseudo_reloc+0x367>
   140002064:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002068:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000206b:	89 c2                	mov    edx,eax
   14000206d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002071:	48 01 d0             	add    rax,rdx
   140002074:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002078:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000207c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000207e:	89 c2                	mov    edx,eax
   140002080:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002084:	48 01 d0             	add    rax,rdx
   140002087:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000208b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000208f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002092:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002096:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000209a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000209d:	0f b6 c0             	movzx  eax,al
   1400020a0:	83 f8 40             	cmp    eax,0x40
   1400020a3:	0f 84 b6 00 00 00    	je     14000215f <do_pseudo_reloc+0x1fd>
   1400020a9:	83 f8 40             	cmp    eax,0x40
   1400020ac:	0f 87 ba 00 00 00    	ja     14000216c <do_pseudo_reloc+0x20a>
   1400020b2:	83 f8 20             	cmp    eax,0x20
   1400020b5:	74 77                	je     14000212e <do_pseudo_reloc+0x1cc>
   1400020b7:	83 f8 20             	cmp    eax,0x20
   1400020ba:	0f 87 ac 00 00 00    	ja     14000216c <do_pseudo_reloc+0x20a>
   1400020c0:	83 f8 08             	cmp    eax,0x8
   1400020c3:	74 0a                	je     1400020cf <do_pseudo_reloc+0x16d>
   1400020c5:	83 f8 10             	cmp    eax,0x10
   1400020c8:	74 38                	je     140002102 <do_pseudo_reloc+0x1a0>
   1400020ca:	e9 9d 00 00 00       	jmp    14000216c <do_pseudo_reloc+0x20a>
   1400020cf:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020d3:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400020d6:	0f b6 c0             	movzx  eax,al
   1400020d9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020dd:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020e1:	25 80 00 00 00       	and    eax,0x80
   1400020e6:	48 85 c0             	test   rax,rax
   1400020e9:	0f 84 9d 00 00 00    	je     14000218c <do_pseudo_reloc+0x22a>
   1400020ef:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020f3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400020f9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020fd:	e9 8a 00 00 00       	jmp    14000218c <do_pseudo_reloc+0x22a>
   140002102:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002106:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002109:	0f b7 c0             	movzx  eax,ax
   14000210c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002110:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002114:	25 00 80 00 00       	and    eax,0x8000
   140002119:	48 85 c0             	test   rax,rax
   14000211c:	74 71                	je     14000218f <do_pseudo_reloc+0x22d>
   14000211e:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002122:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   140002128:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000212c:	eb 61                	jmp    14000218f <do_pseudo_reloc+0x22d>
   14000212e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002132:	8b 00                	mov    eax,DWORD PTR [rax]
   140002134:	89 c0                	mov    eax,eax
   140002136:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000213a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000213e:	25 00 00 00 80       	and    eax,0x80000000
   140002143:	48 85 c0             	test   rax,rax
   140002146:	74 4a                	je     140002192 <do_pseudo_reloc+0x230>
   140002148:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000214c:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002153:	ff ff ff 
   140002156:	48 09 d0             	or     rax,rdx
   140002159:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000215d:	eb 33                	jmp    140002192 <do_pseudo_reloc+0x230>
   14000215f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002163:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002166:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000216a:	eb 27                	jmp    140002193 <do_pseudo_reloc+0x231>
   14000216c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002173:	00 
   140002174:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002178:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000217b:	0f b6 c0             	movzx  eax,al
   14000217e:	48 8d 0d 23 31 00 00 	lea    rcx,[rip+0x3123]        # 1400052a8 <.rdata+0xd8>
   140002185:	89 c2                	mov    edx,eax
   140002187:	e8 74 f9 ff ff       	call   140001b00 <__report_error>
   14000218c:	90                   	nop
   14000218d:	eb 04                	jmp    140002193 <do_pseudo_reloc+0x231>
   14000218f:	90                   	nop
   140002190:	eb 01                	jmp    140002193 <do_pseudo_reloc+0x231>
   140002192:	90                   	nop
   140002193:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002197:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000219b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000219d:	89 c2                	mov    edx,eax
   14000219f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400021a3:	48 01 c2             	add    rdx,rax
   1400021a6:	48 89 c8             	mov    rax,rcx
   1400021a9:	48 29 d0             	sub    rax,rdx
   1400021ac:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400021b0:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400021b4:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400021b8:	48 01 d0             	add    rax,rdx
   1400021bb:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400021bf:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021c3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400021c6:	25 ff 00 00 00       	and    eax,0xff
   1400021cb:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   1400021ce:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   1400021d2:	77 67                	ja     14000223b <do_pseudo_reloc+0x2d9>
   1400021d4:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021d7:	ba 01 00 00 00       	mov    edx,0x1
   1400021dc:	89 c1                	mov    ecx,eax
   1400021de:	48 d3 e2             	shl    rdx,cl
   1400021e1:	48 89 d0             	mov    rax,rdx
   1400021e4:	48 83 e8 01          	sub    rax,0x1
   1400021e8:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400021ec:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021ef:	83 e8 01             	sub    eax,0x1
   1400021f2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400021f9:	89 c1                	mov    ecx,eax
   1400021fb:	48 d3 e2             	shl    rdx,cl
   1400021fe:	48 89 d0             	mov    rax,rdx
   140002201:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140002205:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002209:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   14000220d:	7c 0a                	jl     140002219 <do_pseudo_reloc+0x2b7>
   14000220f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002213:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   140002217:	7e 22                	jle    14000223b <do_pseudo_reloc+0x2d9>
   140002219:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   14000221d:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   140002221:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   140002225:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002228:	48 8d 0d a9 30 00 00 	lea    rcx,[rip+0x30a9]        # 1400052d8 <.rdata+0x108>
   14000222f:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140002234:	89 c2                	mov    edx,eax
   140002236:	e8 c5 f8 ff ff       	call   140001b00 <__report_error>
   14000223b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000223f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002242:	0f b6 c0             	movzx  eax,al
   140002245:	83 f8 40             	cmp    eax,0x40
   140002248:	74 63                	je     1400022ad <do_pseudo_reloc+0x34b>
   14000224a:	83 f8 40             	cmp    eax,0x40
   14000224d:	77 75                	ja     1400022c4 <do_pseudo_reloc+0x362>
   14000224f:	83 f8 20             	cmp    eax,0x20
   140002252:	74 41                	je     140002295 <do_pseudo_reloc+0x333>
   140002254:	83 f8 20             	cmp    eax,0x20
   140002257:	77 6b                	ja     1400022c4 <do_pseudo_reloc+0x362>
   140002259:	83 f8 08             	cmp    eax,0x8
   14000225c:	74 07                	je     140002265 <do_pseudo_reloc+0x303>
   14000225e:	83 f8 10             	cmp    eax,0x10
   140002261:	74 1a                	je     14000227d <do_pseudo_reloc+0x31b>
   140002263:	eb 5f                	jmp    1400022c4 <do_pseudo_reloc+0x362>
   140002265:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002269:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000226d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002273:	48 89 c1             	mov    rcx,rax
   140002276:	e8 a0 fc ff ff       	call   140001f1b <__write_memory>
   14000227b:	eb 47                	jmp    1400022c4 <do_pseudo_reloc+0x362>
   14000227d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002281:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002285:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000228b:	48 89 c1             	mov    rcx,rax
   14000228e:	e8 88 fc ff ff       	call   140001f1b <__write_memory>
   140002293:	eb 2f                	jmp    1400022c4 <do_pseudo_reloc+0x362>
   140002295:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002299:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000229d:	41 b8 04 00 00 00    	mov    r8d,0x4
   1400022a3:	48 89 c1             	mov    rcx,rax
   1400022a6:	e8 70 fc ff ff       	call   140001f1b <__write_memory>
   1400022ab:	eb 17                	jmp    1400022c4 <do_pseudo_reloc+0x362>
   1400022ad:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400022b1:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   1400022b5:	41 b8 08 00 00 00    	mov    r8d,0x8
   1400022bb:	48 89 c1             	mov    rcx,rax
   1400022be:	e8 58 fc ff ff       	call   140001f1b <__write_memory>
   1400022c3:	90                   	nop
   1400022c4:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   1400022c9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400022cd:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400022d1:	0f 82 8d fd ff ff    	jb     140002064 <do_pseudo_reloc+0x102>
   1400022d7:	eb 01                	jmp    1400022da <do_pseudo_reloc+0x378>
   1400022d9:	90                   	nop
   1400022da:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   1400022de:	5d                   	pop    rbp
   1400022df:	c3                   	ret

00000001400022e0 <_pei386_runtime_relocator>:
   1400022e0:	55                   	push   rbp
   1400022e1:	48 89 e5             	mov    rbp,rsp
   1400022e4:	48 83 ec 30          	sub    rsp,0x30
   1400022e8:	8b 05 0e 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e0e]        # 1400090fc <was_init.0>
   1400022ee:	85 c0                	test   eax,eax
   1400022f0:	0f 85 88 00 00 00    	jne    14000237e <_pei386_runtime_relocator+0x9e>
   1400022f6:	8b 05 00 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e00]        # 1400090fc <was_init.0>
   1400022fc:	83 c0 01             	add    eax,0x1
   1400022ff:	89 05 f7 6d 00 00    	mov    DWORD PTR [rip+0x6df7],eax        # 1400090fc <was_init.0>
   140002305:	e8 21 0b 00 00       	call   140002e2b <__mingw_GetSectionCount>
   14000230a:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000230d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002310:	48 63 d0             	movsxd rdx,eax
   140002313:	48 89 d0             	mov    rax,rdx
   140002316:	48 c1 e0 02          	shl    rax,0x2
   14000231a:	48 01 d0             	add    rax,rdx
   14000231d:	48 c1 e0 03          	shl    rax,0x3
   140002321:	48 83 c0 0f          	add    rax,0xf
   140002325:	48 c1 e8 04          	shr    rax,0x4
   140002329:	48 c1 e0 04          	shl    rax,0x4
   14000232d:	e8 7e 0d 00 00       	call   1400030b0 <___chkstk_ms>
   140002332:	48 29 c4             	sub    rsp,rax
   140002335:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   14000233a:	48 83 c0 0f          	add    rax,0xf
   14000233e:	48 c1 e8 04          	shr    rax,0x4
   140002342:	48 c1 e0 04          	shl    rax,0x4
   140002346:	48 89 05 a3 6d 00 00 	mov    QWORD PTR [rip+0x6da3],rax        # 1400090f0 <the_secs>
   14000234d:	c7 05 a1 6d 00 00 00 	mov    DWORD PTR [rip+0x6da1],0x0        # 1400090f8 <maxSections>
   140002354:	00 00 00 
   140002357:	48 8b 0d 02 30 00 00 	mov    rcx,QWORD PTR [rip+0x3002]        # 140005360 <.refptr.__ImageBase>
   14000235e:	48 8b 15 0b 30 00 00 	mov    rdx,QWORD PTR [rip+0x300b]        # 140005370 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002365:	48 8b 05 14 30 00 00 	mov    rax,QWORD PTR [rip+0x3014]        # 140005380 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000236c:	49 89 c8             	mov    r8,rcx
   14000236f:	48 89 c1             	mov    rcx,rax
   140002372:	e8 eb fb ff ff       	call   140001f62 <do_pseudo_reloc>
   140002377:	e8 c7 fa ff ff       	call   140001e43 <restore_modified_sections>
   14000237c:	eb 01                	jmp    14000237f <_pei386_runtime_relocator+0x9f>
   14000237e:	90                   	nop
   14000237f:	48 89 ec             	mov    rsp,rbp
   140002382:	5d                   	pop    rbp
   140002383:	c3                   	ret
   140002384:	90                   	nop
   140002385:	90                   	nop
   140002386:	90                   	nop
   140002387:	90                   	nop
   140002388:	90                   	nop
   140002389:	90                   	nop
   14000238a:	90                   	nop
   14000238b:	90                   	nop
   14000238c:	90                   	nop
   14000238d:	90                   	nop
   14000238e:	90                   	nop
   14000238f:	90                   	nop

0000000140002390 <__mingw_raise_matherr>:
   140002390:	55                   	push   rbp
   140002391:	48 89 e5             	mov    rbp,rsp
   140002394:	48 83 ec 50          	sub    rsp,0x50
   140002398:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000239b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000239f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   1400023a4:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   1400023a9:	48 8b 05 50 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d50]        # 140009100 <stUserMathErr>
   1400023b0:	48 85 c0             	test   rax,rax
   1400023b3:	74 3e                	je     1400023f3 <__mingw_raise_matherr+0x63>
   1400023b5:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   1400023b8:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   1400023bb:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400023bf:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   1400023c3:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   1400023c8:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   1400023cd:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   1400023d2:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   1400023d7:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   1400023dc:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   1400023e1:	48 8b 15 18 6d 00 00 	mov    rdx,QWORD PTR [rip+0x6d18]        # 140009100 <stUserMathErr>
   1400023e8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   1400023ec:	48 89 c1             	mov    rcx,rax
   1400023ef:	ff d2                	call   rdx
   1400023f1:	eb 01                	jmp    1400023f4 <__mingw_raise_matherr+0x64>
   1400023f3:	90                   	nop
   1400023f4:	48 83 c4 50          	add    rsp,0x50
   1400023f8:	5d                   	pop    rbp
   1400023f9:	c3                   	ret

00000001400023fa <__mingw_setusermatherr>:
   1400023fa:	55                   	push   rbp
   1400023fb:	48 89 e5             	mov    rbp,rsp
   1400023fe:	48 83 ec 20          	sub    rsp,0x20
   140002402:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002406:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000240a:	48 89 05 ef 6c 00 00 	mov    QWORD PTR [rip+0x6cef],rax        # 140009100 <stUserMathErr>
   140002411:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002415:	48 89 c1             	mov    rcx,rax
   140002418:	e8 13 0e 00 00       	call   140003230 <__setusermatherr>
   14000241d:	90                   	nop
   14000241e:	48 83 c4 20          	add    rsp,0x20
   140002422:	5d                   	pop    rbp
   140002423:	c3                   	ret
   140002424:	90                   	nop
   140002425:	90                   	nop
   140002426:	90                   	nop
   140002427:	90                   	nop
   140002428:	90                   	nop
   140002429:	90                   	nop
   14000242a:	90                   	nop
   14000242b:	90                   	nop
   14000242c:	90                   	nop
   14000242d:	90                   	nop
   14000242e:	90                   	nop
   14000242f:	90                   	nop

0000000140002430 <__mingw_SEH_error_handler>:
   140002430:	55                   	push   rbp
   140002431:	48 89 e5             	mov    rbp,rsp
   140002434:	48 83 ec 30          	sub    rsp,0x30
   140002438:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000243c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002440:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002444:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140002448:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   14000244f:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002456:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000245a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000245d:	83 e0 02             	and    eax,0x2
   140002460:	85 c0                	test   eax,eax
   140002462:	74 0a                	je     14000246e <__mingw_SEH_error_handler+0x3e>
   140002464:	b8 01 00 00 00       	mov    eax,0x1
   140002469:	e9 16 02 00 00       	jmp    140002684 <__mingw_SEH_error_handler+0x254>
   14000246e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002472:	8b 00                	mov    eax,DWORD PTR [rax]
   140002474:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002479:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000247e:	75 18                	jne    140002498 <__mingw_SEH_error_handler+0x68>
   140002480:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002484:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002487:	83 e0 01             	and    eax,0x1
   14000248a:	85 c0                	test   eax,eax
   14000248c:	75 0a                	jne    140002498 <__mingw_SEH_error_handler+0x68>
   14000248e:	b8 00 00 00 00       	mov    eax,0x0
   140002493:	e9 ec 01 00 00       	jmp    140002684 <__mingw_SEH_error_handler+0x254>
   140002498:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000249c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000249e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400024a3:	0f 84 12 01 00 00    	je     1400025bb <__mingw_SEH_error_handler+0x18b>
   1400024a9:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400024ae:	0f 87 c3 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   1400024b4:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400024b9:	0f 87 b8 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   1400024bf:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400024c4:	0f 83 4c 01 00 00    	jae    140002616 <__mingw_SEH_error_handler+0x1e6>
   1400024ca:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400024cf:	0f 84 3a 01 00 00    	je     14000260f <__mingw_SEH_error_handler+0x1df>
   1400024d5:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400024da:	0f 87 97 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   1400024e0:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024e5:	0f 84 83 01 00 00    	je     14000266e <__mingw_SEH_error_handler+0x23e>
   1400024eb:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024f0:	0f 87 81 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   1400024f6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400024fb:	0f 87 76 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   140002501:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002506:	0f 83 03 01 00 00    	jae    14000260f <__mingw_SEH_error_handler+0x1df>
   14000250c:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002511:	0f 84 57 01 00 00    	je     14000266e <__mingw_SEH_error_handler+0x23e>
   140002517:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000251c:	0f 87 55 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   140002522:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002527:	0f 84 8e 00 00 00    	je     1400025bb <__mingw_SEH_error_handler+0x18b>
   14000252d:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002532:	0f 87 3f 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   140002538:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000253d:	0f 84 2b 01 00 00    	je     14000266e <__mingw_SEH_error_handler+0x23e>
   140002543:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002548:	0f 87 29 01 00 00    	ja     140002677 <__mingw_SEH_error_handler+0x247>
   14000254e:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002553:	0f 84 15 01 00 00    	je     14000266e <__mingw_SEH_error_handler+0x23e>
   140002559:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000255e:	0f 85 13 01 00 00    	jne    140002677 <__mingw_SEH_error_handler+0x247>
   140002564:	ba 00 00 00 00       	mov    edx,0x0
   140002569:	b9 0b 00 00 00       	mov    ecx,0xb
   14000256e:	e8 2d 0d 00 00       	call   1400032a0 <signal>
   140002573:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002577:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000257c:	75 1b                	jne    140002599 <__mingw_SEH_error_handler+0x169>
   14000257e:	ba 01 00 00 00       	mov    edx,0x1
   140002583:	b9 0b 00 00 00       	mov    ecx,0xb
   140002588:	e8 13 0d 00 00       	call   1400032a0 <signal>
   14000258d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002594:	e9 e1 00 00 00       	jmp    14000267a <__mingw_SEH_error_handler+0x24a>
   140002599:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000259e:	0f 84 d6 00 00 00    	je     14000267a <__mingw_SEH_error_handler+0x24a>
   1400025a4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025a8:	b9 0b 00 00 00       	mov    ecx,0xb
   1400025ad:	ff d0                	call   rax
   1400025af:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025b6:	e9 bf 00 00 00       	jmp    14000267a <__mingw_SEH_error_handler+0x24a>
   1400025bb:	ba 00 00 00 00       	mov    edx,0x0
   1400025c0:	b9 04 00 00 00       	mov    ecx,0x4
   1400025c5:	e8 d6 0c 00 00       	call   1400032a0 <signal>
   1400025ca:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025ce:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025d3:	75 1b                	jne    1400025f0 <__mingw_SEH_error_handler+0x1c0>
   1400025d5:	ba 01 00 00 00       	mov    edx,0x1
   1400025da:	b9 04 00 00 00       	mov    ecx,0x4
   1400025df:	e8 bc 0c 00 00       	call   1400032a0 <signal>
   1400025e4:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025eb:	e9 8d 00 00 00       	jmp    14000267d <__mingw_SEH_error_handler+0x24d>
   1400025f0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400025f5:	0f 84 82 00 00 00    	je     14000267d <__mingw_SEH_error_handler+0x24d>
   1400025fb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025ff:	b9 04 00 00 00       	mov    ecx,0x4
   140002604:	ff d0                	call   rax
   140002606:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000260d:	eb 6e                	jmp    14000267d <__mingw_SEH_error_handler+0x24d>
   14000260f:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002616:	ba 00 00 00 00       	mov    edx,0x0
   14000261b:	b9 08 00 00 00       	mov    ecx,0x8
   140002620:	e8 7b 0c 00 00       	call   1400032a0 <signal>
   140002625:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002629:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000262e:	75 23                	jne    140002653 <__mingw_SEH_error_handler+0x223>
   140002630:	ba 01 00 00 00       	mov    edx,0x1
   140002635:	b9 08 00 00 00       	mov    ecx,0x8
   14000263a:	e8 61 0c 00 00       	call   1400032a0 <signal>
   14000263f:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002643:	74 05                	je     14000264a <__mingw_SEH_error_handler+0x21a>
   140002645:	e8 a6 05 00 00       	call   140002bf0 <_fpreset>
   14000264a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002651:	eb 2d                	jmp    140002680 <__mingw_SEH_error_handler+0x250>
   140002653:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002658:	74 26                	je     140002680 <__mingw_SEH_error_handler+0x250>
   14000265a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000265e:	b9 08 00 00 00       	mov    ecx,0x8
   140002663:	ff d0                	call   rax
   140002665:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000266c:	eb 12                	jmp    140002680 <__mingw_SEH_error_handler+0x250>
   14000266e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002675:	eb 0a                	jmp    140002681 <__mingw_SEH_error_handler+0x251>
   140002677:	90                   	nop
   140002678:	eb 07                	jmp    140002681 <__mingw_SEH_error_handler+0x251>
   14000267a:	90                   	nop
   14000267b:	eb 04                	jmp    140002681 <__mingw_SEH_error_handler+0x251>
   14000267d:	90                   	nop
   14000267e:	eb 01                	jmp    140002681 <__mingw_SEH_error_handler+0x251>
   140002680:	90                   	nop
   140002681:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002684:	48 83 c4 30          	add    rsp,0x30
   140002688:	5d                   	pop    rbp
   140002689:	c3                   	ret

000000014000268a <_gnu_exception_handler>:
   14000268a:	55                   	push   rbp
   14000268b:	48 89 e5             	mov    rbp,rsp
   14000268e:	48 83 ec 30          	sub    rsp,0x30
   140002692:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002696:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000269d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   1400026a4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400026a8:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400026ab:	8b 00                	mov    eax,DWORD PTR [rax]
   1400026ad:	25 ff ff ff 20       	and    eax,0x20ffffff
   1400026b2:	3d 43 43 47 20       	cmp    eax,0x20474343
   1400026b7:	75 1b                	jne    1400026d4 <_gnu_exception_handler+0x4a>
   1400026b9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400026bd:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400026c0:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400026c3:	83 e0 01             	and    eax,0x1
   1400026c6:	85 c0                	test   eax,eax
   1400026c8:	75 0a                	jne    1400026d4 <_gnu_exception_handler+0x4a>
   1400026ca:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400026cf:	e9 14 02 00 00       	jmp    1400028e8 <_gnu_exception_handler+0x25e>
   1400026d4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400026d8:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400026db:	8b 00                	mov    eax,DWORD PTR [rax]
   1400026dd:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026e2:	0f 84 12 01 00 00    	je     1400027fa <_gnu_exception_handler+0x170>
   1400026e8:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026ed:	0f 87 c3 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   1400026f3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400026f8:	0f 87 b8 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   1400026fe:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002703:	0f 83 4c 01 00 00    	jae    140002855 <_gnu_exception_handler+0x1cb>
   140002709:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000270e:	0f 84 3a 01 00 00    	je     14000284e <_gnu_exception_handler+0x1c4>
   140002714:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   140002719:	0f 87 97 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   14000271f:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002724:	0f 84 83 01 00 00    	je     1400028ad <_gnu_exception_handler+0x223>
   14000272a:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   14000272f:	0f 87 81 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   140002735:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   14000273a:	0f 87 76 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   140002740:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002745:	0f 83 03 01 00 00    	jae    14000284e <_gnu_exception_handler+0x1c4>
   14000274b:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002750:	0f 84 57 01 00 00    	je     1400028ad <_gnu_exception_handler+0x223>
   140002756:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000275b:	0f 87 55 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   140002761:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002766:	0f 84 8e 00 00 00    	je     1400027fa <_gnu_exception_handler+0x170>
   14000276c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002771:	0f 87 3f 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   140002777:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000277c:	0f 84 2b 01 00 00    	je     1400028ad <_gnu_exception_handler+0x223>
   140002782:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002787:	0f 87 29 01 00 00    	ja     1400028b6 <_gnu_exception_handler+0x22c>
   14000278d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002792:	0f 84 15 01 00 00    	je     1400028ad <_gnu_exception_handler+0x223>
   140002798:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000279d:	0f 85 13 01 00 00    	jne    1400028b6 <_gnu_exception_handler+0x22c>
   1400027a3:	ba 00 00 00 00       	mov    edx,0x0
   1400027a8:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027ad:	e8 ee 0a 00 00       	call   1400032a0 <signal>
   1400027b2:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027b6:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027bb:	75 1b                	jne    1400027d8 <_gnu_exception_handler+0x14e>
   1400027bd:	ba 01 00 00 00       	mov    edx,0x1
   1400027c2:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027c7:	e8 d4 0a 00 00       	call   1400032a0 <signal>
   1400027cc:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027d3:	e9 e1 00 00 00       	jmp    1400028b9 <_gnu_exception_handler+0x22f>
   1400027d8:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027dd:	0f 84 d6 00 00 00    	je     1400028b9 <_gnu_exception_handler+0x22f>
   1400027e3:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027e7:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027ec:	ff d0                	call   rax
   1400027ee:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027f5:	e9 bf 00 00 00       	jmp    1400028b9 <_gnu_exception_handler+0x22f>
   1400027fa:	ba 00 00 00 00       	mov    edx,0x0
   1400027ff:	b9 04 00 00 00       	mov    ecx,0x4
   140002804:	e8 97 0a 00 00       	call   1400032a0 <signal>
   140002809:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000280d:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002812:	75 1b                	jne    14000282f <_gnu_exception_handler+0x1a5>
   140002814:	ba 01 00 00 00       	mov    edx,0x1
   140002819:	b9 04 00 00 00       	mov    ecx,0x4
   14000281e:	e8 7d 0a 00 00       	call   1400032a0 <signal>
   140002823:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000282a:	e9 8d 00 00 00       	jmp    1400028bc <_gnu_exception_handler+0x232>
   14000282f:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002834:	0f 84 82 00 00 00    	je     1400028bc <_gnu_exception_handler+0x232>
   14000283a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000283e:	b9 04 00 00 00       	mov    ecx,0x4
   140002843:	ff d0                	call   rax
   140002845:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000284c:	eb 6e                	jmp    1400028bc <_gnu_exception_handler+0x232>
   14000284e:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002855:	ba 00 00 00 00       	mov    edx,0x0
   14000285a:	b9 08 00 00 00       	mov    ecx,0x8
   14000285f:	e8 3c 0a 00 00       	call   1400032a0 <signal>
   140002864:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002868:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000286d:	75 23                	jne    140002892 <_gnu_exception_handler+0x208>
   14000286f:	ba 01 00 00 00       	mov    edx,0x1
   140002874:	b9 08 00 00 00       	mov    ecx,0x8
   140002879:	e8 22 0a 00 00       	call   1400032a0 <signal>
   14000287e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002882:	74 05                	je     140002889 <_gnu_exception_handler+0x1ff>
   140002884:	e8 67 03 00 00       	call   140002bf0 <_fpreset>
   140002889:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002890:	eb 2d                	jmp    1400028bf <_gnu_exception_handler+0x235>
   140002892:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002897:	74 26                	je     1400028bf <_gnu_exception_handler+0x235>
   140002899:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000289d:	b9 08 00 00 00       	mov    ecx,0x8
   1400028a2:	ff d0                	call   rax
   1400028a4:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400028ab:	eb 12                	jmp    1400028bf <_gnu_exception_handler+0x235>
   1400028ad:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400028b4:	eb 0a                	jmp    1400028c0 <_gnu_exception_handler+0x236>
   1400028b6:	90                   	nop
   1400028b7:	eb 07                	jmp    1400028c0 <_gnu_exception_handler+0x236>
   1400028b9:	90                   	nop
   1400028ba:	eb 04                	jmp    1400028c0 <_gnu_exception_handler+0x236>
   1400028bc:	90                   	nop
   1400028bd:	eb 01                	jmp    1400028c0 <_gnu_exception_handler+0x236>
   1400028bf:	90                   	nop
   1400028c0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400028c4:	75 1f                	jne    1400028e5 <_gnu_exception_handler+0x25b>
   1400028c6:	48 8b 05 53 68 00 00 	mov    rax,QWORD PTR [rip+0x6853]        # 140009120 <__mingw_oldexcpt_handler>
   1400028cd:	48 85 c0             	test   rax,rax
   1400028d0:	74 13                	je     1400028e5 <_gnu_exception_handler+0x25b>
   1400028d2:	48 8b 15 47 68 00 00 	mov    rdx,QWORD PTR [rip+0x6847]        # 140009120 <__mingw_oldexcpt_handler>
   1400028d9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400028dd:	48 89 c1             	mov    rcx,rax
   1400028e0:	ff d2                	call   rdx
   1400028e2:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400028e5:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400028e8:	48 83 c4 30          	add    rsp,0x30
   1400028ec:	5d                   	pop    rbp
   1400028ed:	c3                   	ret
   1400028ee:	90                   	nop
   1400028ef:	90                   	nop

00000001400028f0 <___w64_mingwthr_add_key_dtor>:
   1400028f0:	55                   	push   rbp
   1400028f1:	48 89 e5             	mov    rbp,rsp
   1400028f4:	48 83 ec 30          	sub    rsp,0x30
   1400028f8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400028fb:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400028ff:	8b 05 63 68 00 00    	mov    eax,DWORD PTR [rip+0x6863]        # 140009168 <__mingwthr_cs_init>
   140002905:	85 c0                	test   eax,eax
   140002907:	75 07                	jne    140002910 <___w64_mingwthr_add_key_dtor+0x20>
   140002909:	b8 00 00 00 00       	mov    eax,0x0
   14000290e:	eb 7b                	jmp    14000298b <___w64_mingwthr_add_key_dtor+0x9b>
   140002910:	ba 18 00 00 00       	mov    edx,0x18
   140002915:	b9 01 00 00 00       	mov    ecx,0x1
   14000291a:	e8 41 09 00 00       	call   140003260 <calloc>
   14000291f:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002923:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002928:	75 07                	jne    140002931 <___w64_mingwthr_add_key_dtor+0x41>
   14000292a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000292f:	eb 5a                	jmp    14000298b <___w64_mingwthr_add_key_dtor+0x9b>
   140002931:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002935:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140002938:	89 10                	mov    DWORD PTR [rax],edx
   14000293a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000293e:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002942:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002946:	48 8d 05 f3 67 00 00 	lea    rax,[rip+0x67f3]        # 140009140 <__mingwthr_cs>
   14000294d:	48 89 c1             	mov    rcx,rax
   140002950:	48 8b 05 39 78 00 00 	mov    rax,QWORD PTR [rip+0x7839]        # 14000a190 <__imp_EnterCriticalSection>
   140002957:	ff d0                	call   rax
   140002959:	48 8b 15 10 68 00 00 	mov    rdx,QWORD PTR [rip+0x6810]        # 140009170 <key_dtor_list>
   140002960:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002964:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002968:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000296c:	48 89 05 fd 67 00 00 	mov    QWORD PTR [rip+0x67fd],rax        # 140009170 <key_dtor_list>
   140002973:	48 8d 05 c6 67 00 00 	lea    rax,[rip+0x67c6]        # 140009140 <__mingwthr_cs>
   14000297a:	48 89 c1             	mov    rcx,rax
   14000297d:	48 8b 05 3c 78 00 00 	mov    rax,QWORD PTR [rip+0x783c]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002984:	ff d0                	call   rax
   140002986:	b8 00 00 00 00       	mov    eax,0x0
   14000298b:	48 83 c4 30          	add    rsp,0x30
   14000298f:	5d                   	pop    rbp
   140002990:	c3                   	ret

0000000140002991 <___w64_mingwthr_remove_key_dtor>:
   140002991:	55                   	push   rbp
   140002992:	48 89 e5             	mov    rbp,rsp
   140002995:	48 83 ec 30          	sub    rsp,0x30
   140002999:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000299c:	8b 05 c6 67 00 00    	mov    eax,DWORD PTR [rip+0x67c6]        # 140009168 <__mingwthr_cs_init>
   1400029a2:	85 c0                	test   eax,eax
   1400029a4:	75 0a                	jne    1400029b0 <___w64_mingwthr_remove_key_dtor+0x1f>
   1400029a6:	b8 00 00 00 00       	mov    eax,0x0
   1400029ab:	e9 9c 00 00 00       	jmp    140002a4c <___w64_mingwthr_remove_key_dtor+0xbb>
   1400029b0:	48 8d 05 89 67 00 00 	lea    rax,[rip+0x6789]        # 140009140 <__mingwthr_cs>
   1400029b7:	48 89 c1             	mov    rcx,rax
   1400029ba:	48 8b 05 cf 77 00 00 	mov    rax,QWORD PTR [rip+0x77cf]        # 14000a190 <__imp_EnterCriticalSection>
   1400029c1:	ff d0                	call   rax
   1400029c3:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   1400029ca:	00 
   1400029cb:	48 8b 05 9e 67 00 00 	mov    rax,QWORD PTR [rip+0x679e]        # 140009170 <key_dtor_list>
   1400029d2:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029d6:	eb 55                	jmp    140002a2d <___w64_mingwthr_remove_key_dtor+0x9c>
   1400029d8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029dc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400029de:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   1400029e1:	75 36                	jne    140002a19 <___w64_mingwthr_remove_key_dtor+0x88>
   1400029e3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400029e8:	75 11                	jne    1400029fb <___w64_mingwthr_remove_key_dtor+0x6a>
   1400029ea:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029ee:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029f2:	48 89 05 77 67 00 00 	mov    QWORD PTR [rip+0x6777],rax        # 140009170 <key_dtor_list>
   1400029f9:	eb 10                	jmp    140002a0b <___w64_mingwthr_remove_key_dtor+0x7a>
   1400029fb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029ff:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   140002a03:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a07:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002a0b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a0f:	48 89 c1             	mov    rcx,rax
   140002a12:	e8 69 08 00 00       	call   140003280 <free>
   140002a17:	eb 1b                	jmp    140002a34 <___w64_mingwthr_remove_key_dtor+0xa3>
   140002a19:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a1d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a21:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a25:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002a29:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a2d:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a32:	75 a4                	jne    1400029d8 <___w64_mingwthr_remove_key_dtor+0x47>
   140002a34:	48 8d 05 05 67 00 00 	lea    rax,[rip+0x6705]        # 140009140 <__mingwthr_cs>
   140002a3b:	48 89 c1             	mov    rcx,rax
   140002a3e:	48 8b 05 7b 77 00 00 	mov    rax,QWORD PTR [rip+0x777b]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002a45:	ff d0                	call   rax
   140002a47:	b8 00 00 00 00       	mov    eax,0x0
   140002a4c:	48 83 c4 30          	add    rsp,0x30
   140002a50:	5d                   	pop    rbp
   140002a51:	c3                   	ret

0000000140002a52 <__mingwthr_run_key_dtors>:
   140002a52:	55                   	push   rbp
   140002a53:	48 89 e5             	mov    rbp,rsp
   140002a56:	48 83 ec 30          	sub    rsp,0x30
   140002a5a:	8b 05 08 67 00 00    	mov    eax,DWORD PTR [rip+0x6708]        # 140009168 <__mingwthr_cs_init>
   140002a60:	85 c0                	test   eax,eax
   140002a62:	0f 84 82 00 00 00    	je     140002aea <__mingwthr_run_key_dtors+0x98>
   140002a68:	48 8d 05 d1 66 00 00 	lea    rax,[rip+0x66d1]        # 140009140 <__mingwthr_cs>
   140002a6f:	48 89 c1             	mov    rcx,rax
   140002a72:	48 8b 05 17 77 00 00 	mov    rax,QWORD PTR [rip+0x7717]        # 14000a190 <__imp_EnterCriticalSection>
   140002a79:	ff d0                	call   rax
   140002a7b:	48 8b 05 ee 66 00 00 	mov    rax,QWORD PTR [rip+0x66ee]        # 140009170 <key_dtor_list>
   140002a82:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a86:	eb 46                	jmp    140002ace <__mingwthr_run_key_dtors+0x7c>
   140002a88:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a8c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a8e:	89 c1                	mov    ecx,eax
   140002a90:	48 8b 05 49 77 00 00 	mov    rax,QWORD PTR [rip+0x7749]        # 14000a1e0 <__imp_TlsGetValue>
   140002a97:	ff d0                	call   rax
   140002a99:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a9d:	48 8b 05 fc 76 00 00 	mov    rax,QWORD PTR [rip+0x76fc]        # 14000a1a0 <__imp_GetLastError>
   140002aa4:	ff d0                	call   rax
   140002aa6:	85 c0                	test   eax,eax
   140002aa8:	75 18                	jne    140002ac2 <__mingwthr_run_key_dtors+0x70>
   140002aaa:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002aaf:	74 11                	je     140002ac2 <__mingwthr_run_key_dtors+0x70>
   140002ab1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ab5:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002ab9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002abd:	48 89 c1             	mov    rcx,rax
   140002ac0:	ff d2                	call   rdx
   140002ac2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ac6:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002aca:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ace:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002ad3:	75 b3                	jne    140002a88 <__mingwthr_run_key_dtors+0x36>
   140002ad5:	48 8d 05 64 66 00 00 	lea    rax,[rip+0x6664]        # 140009140 <__mingwthr_cs>
   140002adc:	48 89 c1             	mov    rcx,rax
   140002adf:	48 8b 05 da 76 00 00 	mov    rax,QWORD PTR [rip+0x76da]        # 14000a1c0 <__imp_LeaveCriticalSection>
   140002ae6:	ff d0                	call   rax
   140002ae8:	eb 01                	jmp    140002aeb <__mingwthr_run_key_dtors+0x99>
   140002aea:	90                   	nop
   140002aeb:	48 83 c4 30          	add    rsp,0x30
   140002aef:	5d                   	pop    rbp
   140002af0:	c3                   	ret

0000000140002af1 <__mingw_TLScallback>:
   140002af1:	55                   	push   rbp
   140002af2:	48 89 e5             	mov    rbp,rsp
   140002af5:	48 83 ec 30          	sub    rsp,0x30
   140002af9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002afd:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002b00:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002b04:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002b08:	0f 84 cc 00 00 00    	je     140002bda <__mingw_TLScallback+0xe9>
   140002b0e:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002b12:	0f 87 ca 00 00 00    	ja     140002be2 <__mingw_TLScallback+0xf1>
   140002b18:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002b1c:	0f 84 b1 00 00 00    	je     140002bd3 <__mingw_TLScallback+0xe2>
   140002b22:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002b26:	0f 87 b6 00 00 00    	ja     140002be2 <__mingw_TLScallback+0xf1>
   140002b2c:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002b30:	74 33                	je     140002b65 <__mingw_TLScallback+0x74>
   140002b32:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002b36:	0f 85 a6 00 00 00    	jne    140002be2 <__mingw_TLScallback+0xf1>
   140002b3c:	8b 05 26 66 00 00    	mov    eax,DWORD PTR [rip+0x6626]        # 140009168 <__mingwthr_cs_init>
   140002b42:	85 c0                	test   eax,eax
   140002b44:	75 13                	jne    140002b59 <__mingw_TLScallback+0x68>
   140002b46:	48 8d 05 f3 65 00 00 	lea    rax,[rip+0x65f3]        # 140009140 <__mingwthr_cs>
   140002b4d:	48 89 c1             	mov    rcx,rax
   140002b50:	48 8b 05 61 76 00 00 	mov    rax,QWORD PTR [rip+0x7661]        # 14000a1b8 <__imp_InitializeCriticalSection>
   140002b57:	ff d0                	call   rax
   140002b59:	c7 05 05 66 00 00 01 	mov    DWORD PTR [rip+0x6605],0x1        # 140009168 <__mingwthr_cs_init>
   140002b60:	00 00 00 
   140002b63:	eb 7d                	jmp    140002be2 <__mingw_TLScallback+0xf1>
   140002b65:	e8 e8 fe ff ff       	call   140002a52 <__mingwthr_run_key_dtors>
   140002b6a:	8b 05 f8 65 00 00    	mov    eax,DWORD PTR [rip+0x65f8]        # 140009168 <__mingwthr_cs_init>
   140002b70:	83 f8 01             	cmp    eax,0x1
   140002b73:	75 6c                	jne    140002be1 <__mingw_TLScallback+0xf0>
   140002b75:	48 8b 05 f4 65 00 00 	mov    rax,QWORD PTR [rip+0x65f4]        # 140009170 <key_dtor_list>
   140002b7c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b80:	eb 20                	jmp    140002ba2 <__mingw_TLScallback+0xb1>
   140002b82:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b86:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b8a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b8e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b92:	48 89 c1             	mov    rcx,rax
   140002b95:	e8 e6 06 00 00       	call   140003280 <free>
   140002b9a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b9e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ba2:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002ba7:	75 d9                	jne    140002b82 <__mingw_TLScallback+0x91>
   140002ba9:	48 c7 05 bc 65 00 00 	mov    QWORD PTR [rip+0x65bc],0x0        # 140009170 <key_dtor_list>
   140002bb0:	00 00 00 00 
   140002bb4:	c7 05 aa 65 00 00 00 	mov    DWORD PTR [rip+0x65aa],0x0        # 140009168 <__mingwthr_cs_init>
   140002bbb:	00 00 00 
   140002bbe:	48 8d 05 7b 65 00 00 	lea    rax,[rip+0x657b]        # 140009140 <__mingwthr_cs>
   140002bc5:	48 89 c1             	mov    rcx,rax
   140002bc8:	48 8b 05 b9 75 00 00 	mov    rax,QWORD PTR [rip+0x75b9]        # 14000a188 <__IAT_start__>
   140002bcf:	ff d0                	call   rax
   140002bd1:	eb 0e                	jmp    140002be1 <__mingw_TLScallback+0xf0>
   140002bd3:	e8 18 00 00 00       	call   140002bf0 <_fpreset>
   140002bd8:	eb 08                	jmp    140002be2 <__mingw_TLScallback+0xf1>
   140002bda:	e8 73 fe ff ff       	call   140002a52 <__mingwthr_run_key_dtors>
   140002bdf:	eb 01                	jmp    140002be2 <__mingw_TLScallback+0xf1>
   140002be1:	90                   	nop
   140002be2:	b8 01 00 00 00       	mov    eax,0x1
   140002be7:	48 83 c4 30          	add    rsp,0x30
   140002beb:	5d                   	pop    rbp
   140002bec:	c3                   	ret
   140002bed:	90                   	nop
   140002bee:	90                   	nop
   140002bef:	90                   	nop

0000000140002bf0 <_fpreset>:
   140002bf0:	55                   	push   rbp
   140002bf1:	48 89 e5             	mov    rbp,rsp
   140002bf4:	db e3                	fninit
   140002bf6:	90                   	nop
   140002bf7:	5d                   	pop    rbp
   140002bf8:	c3                   	ret
   140002bf9:	90                   	nop
   140002bfa:	90                   	nop
   140002bfb:	90                   	nop
   140002bfc:	90                   	nop
   140002bfd:	90                   	nop
   140002bfe:	90                   	nop
   140002bff:	90                   	nop

0000000140002c00 <_ValidateImageBase>:
   140002c00:	55                   	push   rbp
   140002c01:	48 89 e5             	mov    rbp,rsp
   140002c04:	48 83 ec 20          	sub    rsp,0x20
   140002c08:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c0c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c10:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c14:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c18:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c1b:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002c1f:	74 07                	je     140002c28 <_ValidateImageBase+0x28>
   140002c21:	b8 00 00 00 00       	mov    eax,0x0
   140002c26:	eb 4e                	jmp    140002c76 <_ValidateImageBase+0x76>
   140002c28:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c2c:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c2f:	48 63 d0             	movsxd rdx,eax
   140002c32:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c36:	48 01 d0             	add    rax,rdx
   140002c39:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002c3d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c41:	8b 00                	mov    eax,DWORD PTR [rax]
   140002c43:	3d 50 45 00 00       	cmp    eax,0x4550
   140002c48:	74 07                	je     140002c51 <_ValidateImageBase+0x51>
   140002c4a:	b8 00 00 00 00       	mov    eax,0x0
   140002c4f:	eb 25                	jmp    140002c76 <_ValidateImageBase+0x76>
   140002c51:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c55:	48 83 c0 18          	add    rax,0x18
   140002c59:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c5d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c61:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c64:	66 3d 0b 02          	cmp    ax,0x20b
   140002c68:	74 07                	je     140002c71 <_ValidateImageBase+0x71>
   140002c6a:	b8 00 00 00 00       	mov    eax,0x0
   140002c6f:	eb 05                	jmp    140002c76 <_ValidateImageBase+0x76>
   140002c71:	b8 01 00 00 00       	mov    eax,0x1
   140002c76:	48 83 c4 20          	add    rsp,0x20
   140002c7a:	5d                   	pop    rbp
   140002c7b:	c3                   	ret

0000000140002c7c <_FindPESection>:
   140002c7c:	55                   	push   rbp
   140002c7d:	48 89 e5             	mov    rbp,rsp
   140002c80:	48 83 ec 20          	sub    rsp,0x20
   140002c84:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c88:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002c8c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c90:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c93:	48 63 d0             	movsxd rdx,eax
   140002c96:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c9a:	48 01 d0             	add    rax,rdx
   140002c9d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002ca1:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002ca8:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cac:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002cb0:	0f b7 d0             	movzx  edx,ax
   140002cb3:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cb7:	48 01 d0             	add    rax,rdx
   140002cba:	48 83 c0 18          	add    rax,0x18
   140002cbe:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002cc2:	eb 36                	jmp    140002cfa <_FindPESection+0x7e>
   140002cc4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cc8:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002ccb:	89 c0                	mov    eax,eax
   140002ccd:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002cd1:	72 1e                	jb     140002cf1 <_FindPESection+0x75>
   140002cd3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cd7:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002cda:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cde:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002ce1:	01 d0                	add    eax,edx
   140002ce3:	89 c0                	mov    eax,eax
   140002ce5:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002ce9:	73 06                	jae    140002cf1 <_FindPESection+0x75>
   140002ceb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cef:	eb 1e                	jmp    140002d0f <_FindPESection+0x93>
   140002cf1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002cf5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002cfa:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cfe:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002d02:	0f b7 c0             	movzx  eax,ax
   140002d05:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002d08:	72 ba                	jb     140002cc4 <_FindPESection+0x48>
   140002d0a:	b8 00 00 00 00       	mov    eax,0x0
   140002d0f:	48 83 c4 20          	add    rsp,0x20
   140002d13:	5d                   	pop    rbp
   140002d14:	c3                   	ret

0000000140002d15 <_FindPESectionByName>:
   140002d15:	55                   	push   rbp
   140002d16:	48 89 e5             	mov    rbp,rsp
   140002d19:	48 83 ec 40          	sub    rsp,0x40
   140002d1d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002d21:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002d25:	48 89 c1             	mov    rcx,rax
   140002d28:	e8 7b 05 00 00       	call   1400032a8 <strlen>
   140002d2d:	48 83 f8 08          	cmp    rax,0x8
   140002d31:	76 0a                	jbe    140002d3d <_FindPESectionByName+0x28>
   140002d33:	b8 00 00 00 00       	mov    eax,0x0
   140002d38:	e9 98 00 00 00       	jmp    140002dd5 <_FindPESectionByName+0xc0>
   140002d3d:	48 8b 05 1c 26 00 00 	mov    rax,QWORD PTR [rip+0x261c]        # 140005360 <.refptr.__ImageBase>
   140002d44:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002d48:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d4c:	48 89 c1             	mov    rcx,rax
   140002d4f:	e8 ac fe ff ff       	call   140002c00 <_ValidateImageBase>
   140002d54:	85 c0                	test   eax,eax
   140002d56:	75 07                	jne    140002d5f <_FindPESectionByName+0x4a>
   140002d58:	b8 00 00 00 00       	mov    eax,0x0
   140002d5d:	eb 76                	jmp    140002dd5 <_FindPESectionByName+0xc0>
   140002d5f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d63:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d66:	48 63 d0             	movsxd rdx,eax
   140002d69:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d6d:	48 01 d0             	add    rax,rdx
   140002d70:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002d74:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d7b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d7f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d83:	0f b7 d0             	movzx  edx,ax
   140002d86:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d8a:	48 01 d0             	add    rax,rdx
   140002d8d:	48 83 c0 18          	add    rax,0x18
   140002d91:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d95:	eb 29                	jmp    140002dc0 <_FindPESectionByName+0xab>
   140002d97:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d9b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002d9f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002da5:	48 89 c1             	mov    rcx,rax
   140002da8:	e8 03 05 00 00       	call   1400032b0 <strncmp>
   140002dad:	85 c0                	test   eax,eax
   140002daf:	75 06                	jne    140002db7 <_FindPESectionByName+0xa2>
   140002db1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002db5:	eb 1e                	jmp    140002dd5 <_FindPESectionByName+0xc0>
   140002db7:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002dbb:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002dc0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002dc4:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002dc8:	0f b7 c0             	movzx  eax,ax
   140002dcb:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002dce:	72 c7                	jb     140002d97 <_FindPESectionByName+0x82>
   140002dd0:	b8 00 00 00 00       	mov    eax,0x0
   140002dd5:	48 83 c4 40          	add    rsp,0x40
   140002dd9:	5d                   	pop    rbp
   140002dda:	c3                   	ret

0000000140002ddb <__mingw_GetSectionForAddress>:
   140002ddb:	55                   	push   rbp
   140002ddc:	48 89 e5             	mov    rbp,rsp
   140002ddf:	48 83 ec 30          	sub    rsp,0x30
   140002de3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002de7:	48 8b 05 72 25 00 00 	mov    rax,QWORD PTR [rip+0x2572]        # 140005360 <.refptr.__ImageBase>
   140002dee:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002df2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002df6:	48 89 c1             	mov    rcx,rax
   140002df9:	e8 02 fe ff ff       	call   140002c00 <_ValidateImageBase>
   140002dfe:	85 c0                	test   eax,eax
   140002e00:	75 07                	jne    140002e09 <__mingw_GetSectionForAddress+0x2e>
   140002e02:	b8 00 00 00 00       	mov    eax,0x0
   140002e07:	eb 1c                	jmp    140002e25 <__mingw_GetSectionForAddress+0x4a>
   140002e09:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002e0d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002e11:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e15:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002e19:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e1d:	48 89 c1             	mov    rcx,rax
   140002e20:	e8 57 fe ff ff       	call   140002c7c <_FindPESection>
   140002e25:	48 83 c4 30          	add    rsp,0x30
   140002e29:	5d                   	pop    rbp
   140002e2a:	c3                   	ret

0000000140002e2b <__mingw_GetSectionCount>:
   140002e2b:	55                   	push   rbp
   140002e2c:	48 89 e5             	mov    rbp,rsp
   140002e2f:	48 83 ec 30          	sub    rsp,0x30
   140002e33:	48 8b 05 26 25 00 00 	mov    rax,QWORD PTR [rip+0x2526]        # 140005360 <.refptr.__ImageBase>
   140002e3a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e3e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e42:	48 89 c1             	mov    rcx,rax
   140002e45:	e8 b6 fd ff ff       	call   140002c00 <_ValidateImageBase>
   140002e4a:	85 c0                	test   eax,eax
   140002e4c:	75 07                	jne    140002e55 <__mingw_GetSectionCount+0x2a>
   140002e4e:	b8 00 00 00 00       	mov    eax,0x0
   140002e53:	eb 20                	jmp    140002e75 <__mingw_GetSectionCount+0x4a>
   140002e55:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e59:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e5c:	48 63 d0             	movsxd rdx,eax
   140002e5f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e63:	48 01 d0             	add    rax,rdx
   140002e66:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e6a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e6e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e72:	0f b7 c0             	movzx  eax,ax
   140002e75:	48 83 c4 30          	add    rsp,0x30
   140002e79:	5d                   	pop    rbp
   140002e7a:	c3                   	ret

0000000140002e7b <_FindPESectionExec>:
   140002e7b:	55                   	push   rbp
   140002e7c:	48 89 e5             	mov    rbp,rsp
   140002e7f:	48 83 ec 40          	sub    rsp,0x40
   140002e83:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e87:	48 8b 05 d2 24 00 00 	mov    rax,QWORD PTR [rip+0x24d2]        # 140005360 <.refptr.__ImageBase>
   140002e8e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e92:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e96:	48 89 c1             	mov    rcx,rax
   140002e99:	e8 62 fd ff ff       	call   140002c00 <_ValidateImageBase>
   140002e9e:	85 c0                	test   eax,eax
   140002ea0:	75 07                	jne    140002ea9 <_FindPESectionExec+0x2e>
   140002ea2:	b8 00 00 00 00       	mov    eax,0x0
   140002ea7:	eb 78                	jmp    140002f21 <_FindPESectionExec+0xa6>
   140002ea9:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002ead:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002eb0:	48 63 d0             	movsxd rdx,eax
   140002eb3:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002eb7:	48 01 d0             	add    rax,rdx
   140002eba:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002ebe:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002ec5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ec9:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002ecd:	0f b7 d0             	movzx  edx,ax
   140002ed0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ed4:	48 01 d0             	add    rax,rdx
   140002ed7:	48 83 c0 18          	add    rax,0x18
   140002edb:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002edf:	eb 2b                	jmp    140002f0c <_FindPESectionExec+0x91>
   140002ee1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ee5:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002ee8:	25 00 00 00 20       	and    eax,0x20000000
   140002eed:	85 c0                	test   eax,eax
   140002eef:	74 12                	je     140002f03 <_FindPESectionExec+0x88>
   140002ef1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002ef6:	75 06                	jne    140002efe <_FindPESectionExec+0x83>
   140002ef8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002efc:	eb 23                	jmp    140002f21 <_FindPESectionExec+0xa6>
   140002efe:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002f03:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002f07:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002f0c:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002f10:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002f14:	0f b7 c0             	movzx  eax,ax
   140002f17:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002f1a:	72 c5                	jb     140002ee1 <_FindPESectionExec+0x66>
   140002f1c:	b8 00 00 00 00       	mov    eax,0x0
   140002f21:	48 83 c4 40          	add    rsp,0x40
   140002f25:	5d                   	pop    rbp
   140002f26:	c3                   	ret

0000000140002f27 <_GetPEImageBase>:
   140002f27:	55                   	push   rbp
   140002f28:	48 89 e5             	mov    rbp,rsp
   140002f2b:	48 83 ec 30          	sub    rsp,0x30
   140002f2f:	48 8b 05 2a 24 00 00 	mov    rax,QWORD PTR [rip+0x242a]        # 140005360 <.refptr.__ImageBase>
   140002f36:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f3a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f3e:	48 89 c1             	mov    rcx,rax
   140002f41:	e8 ba fc ff ff       	call   140002c00 <_ValidateImageBase>
   140002f46:	85 c0                	test   eax,eax
   140002f48:	75 07                	jne    140002f51 <_GetPEImageBase+0x2a>
   140002f4a:	b8 00 00 00 00       	mov    eax,0x0
   140002f4f:	eb 04                	jmp    140002f55 <_GetPEImageBase+0x2e>
   140002f51:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f55:	48 83 c4 30          	add    rsp,0x30
   140002f59:	5d                   	pop    rbp
   140002f5a:	c3                   	ret

0000000140002f5b <_IsNonwritableInCurrentImage>:
   140002f5b:	55                   	push   rbp
   140002f5c:	48 89 e5             	mov    rbp,rsp
   140002f5f:	48 83 ec 40          	sub    rsp,0x40
   140002f63:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f67:	48 8b 05 f2 23 00 00 	mov    rax,QWORD PTR [rip+0x23f2]        # 140005360 <.refptr.__ImageBase>
   140002f6e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f72:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f76:	48 89 c1             	mov    rcx,rax
   140002f79:	e8 82 fc ff ff       	call   140002c00 <_ValidateImageBase>
   140002f7e:	85 c0                	test   eax,eax
   140002f80:	75 07                	jne    140002f89 <_IsNonwritableInCurrentImage+0x2e>
   140002f82:	b8 00 00 00 00       	mov    eax,0x0
   140002f87:	eb 3d                	jmp    140002fc6 <_IsNonwritableInCurrentImage+0x6b>
   140002f89:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f8d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f91:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f95:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f99:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f9d:	48 89 c1             	mov    rcx,rax
   140002fa0:	e8 d7 fc ff ff       	call   140002c7c <_FindPESection>
   140002fa5:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002fa9:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140002fae:	75 07                	jne    140002fb7 <_IsNonwritableInCurrentImage+0x5c>
   140002fb0:	b8 00 00 00 00       	mov    eax,0x0
   140002fb5:	eb 0f                	jmp    140002fc6 <_IsNonwritableInCurrentImage+0x6b>
   140002fb7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002fbb:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002fbe:	f7 d0                	not    eax
   140002fc0:	c1 e8 1f             	shr    eax,0x1f
   140002fc3:	0f b6 c0             	movzx  eax,al
   140002fc6:	48 83 c4 40          	add    rsp,0x40
   140002fca:	5d                   	pop    rbp
   140002fcb:	c3                   	ret

0000000140002fcc <__mingw_enum_import_library_names>:
   140002fcc:	55                   	push   rbp
   140002fcd:	48 89 e5             	mov    rbp,rsp
   140002fd0:	48 83 ec 50          	sub    rsp,0x50
   140002fd4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002fd7:	48 8b 05 82 23 00 00 	mov    rax,QWORD PTR [rip+0x2382]        # 140005360 <.refptr.__ImageBase>
   140002fde:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002fe2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fe6:	48 89 c1             	mov    rcx,rax
   140002fe9:	e8 12 fc ff ff       	call   140002c00 <_ValidateImageBase>
   140002fee:	85 c0                	test   eax,eax
   140002ff0:	75 0a                	jne    140002ffc <__mingw_enum_import_library_names+0x30>
   140002ff2:	b8 00 00 00 00       	mov    eax,0x0
   140002ff7:	e9 ab 00 00 00       	jmp    1400030a7 <__mingw_enum_import_library_names+0xdb>
   140002ffc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003000:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140003003:	48 63 d0             	movsxd rdx,eax
   140003006:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000300a:	48 01 d0             	add    rax,rdx
   14000300d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003011:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140003015:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   14000301b:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   14000301e:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140003022:	75 07                	jne    14000302b <__mingw_enum_import_library_names+0x5f>
   140003024:	b8 00 00 00 00       	mov    eax,0x0
   140003029:	eb 7c                	jmp    1400030a7 <__mingw_enum_import_library_names+0xdb>
   14000302b:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000302e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003032:	48 89 c1             	mov    rcx,rax
   140003035:	e8 42 fc ff ff       	call   140002c7c <_FindPESection>
   14000303a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000303e:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140003043:	75 07                	jne    14000304c <__mingw_enum_import_library_names+0x80>
   140003045:	b8 00 00 00 00       	mov    eax,0x0
   14000304a:	eb 5b                	jmp    1400030a7 <__mingw_enum_import_library_names+0xdb>
   14000304c:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000304f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003053:	48 01 d0             	add    rax,rdx
   140003056:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000305a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000305f:	75 07                	jne    140003068 <__mingw_enum_import_library_names+0x9c>
   140003061:	b8 00 00 00 00       	mov    eax,0x0
   140003066:	eb 3f                	jmp    1400030a7 <__mingw_enum_import_library_names+0xdb>
   140003068:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000306c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000306f:	85 c0                	test   eax,eax
   140003071:	75 0b                	jne    14000307e <__mingw_enum_import_library_names+0xb2>
   140003073:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003077:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000307a:	85 c0                	test   eax,eax
   14000307c:	74 23                	je     1400030a1 <__mingw_enum_import_library_names+0xd5>
   14000307e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003082:	7f 12                	jg     140003096 <__mingw_enum_import_library_names+0xca>
   140003084:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003088:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000308b:	89 c2                	mov    edx,eax
   14000308d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003091:	48 01 d0             	add    rax,rdx
   140003094:	eb 11                	jmp    1400030a7 <__mingw_enum_import_library_names+0xdb>
   140003096:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000309a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000309f:	eb c7                	jmp    140003068 <__mingw_enum_import_library_names+0x9c>
   1400030a1:	90                   	nop
   1400030a2:	b8 00 00 00 00       	mov    eax,0x0
   1400030a7:	48 83 c4 50          	add    rsp,0x50
   1400030ab:	5d                   	pop    rbp
   1400030ac:	c3                   	ret
   1400030ad:	90                   	nop
   1400030ae:	90                   	nop
   1400030af:	90                   	nop

00000001400030b0 <___chkstk_ms>:
   1400030b0:	51                   	push   rcx
   1400030b1:	50                   	push   rax
   1400030b2:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400030b8:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   1400030bd:	72 19                	jb     1400030d8 <___chkstk_ms+0x28>
   1400030bf:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   1400030c6:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400030ca:	48 2d 00 10 00 00    	sub    rax,0x1000
   1400030d0:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400030d6:	77 e7                	ja     1400030bf <___chkstk_ms+0xf>
   1400030d8:	48 29 c1             	sub    rcx,rax
   1400030db:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400030df:	58                   	pop    rax
   1400030e0:	59                   	pop    rcx
   1400030e1:	c3                   	ret
   1400030e2:	90                   	nop
   1400030e3:	90                   	nop
   1400030e4:	90                   	nop
   1400030e5:	90                   	nop
   1400030e6:	90                   	nop
   1400030e7:	90                   	nop
   1400030e8:	90                   	nop
   1400030e9:	90                   	nop
   1400030ea:	90                   	nop
   1400030eb:	90                   	nop
   1400030ec:	90                   	nop
   1400030ed:	90                   	nop
   1400030ee:	90                   	nop
   1400030ef:	90                   	nop

00000001400030f0 <_initterm_e>:
   1400030f0:	55                   	push   rbp
   1400030f1:	48 89 e5             	mov    rbp,rsp
   1400030f4:	48 83 ec 30          	sub    rsp,0x30
   1400030f8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400030fc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140003100:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003104:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003108:	eb 29                	jmp    140003133 <_initterm_e+0x43>
   14000310a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000310e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140003111:	48 85 c0             	test   rax,rax
   140003114:	74 17                	je     14000312d <_initterm_e+0x3d>
   140003116:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000311a:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000311d:	ff d0                	call   rax
   14000311f:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003122:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003126:	74 06                	je     14000312e <_initterm_e+0x3e>
   140003128:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000312b:	eb 15                	jmp    140003142 <_initterm_e+0x52>
   14000312d:	90                   	nop
   14000312e:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140003133:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003137:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   14000313b:	72 cd                	jb     14000310a <_initterm_e+0x1a>
   14000313d:	b8 00 00 00 00       	mov    eax,0x0
   140003142:	48 83 c4 30          	add    rsp,0x30
   140003146:	5d                   	pop    rbp
   140003147:	c3                   	ret
   140003148:	90                   	nop
   140003149:	90                   	nop
   14000314a:	90                   	nop
   14000314b:	90                   	nop
   14000314c:	90                   	nop
   14000314d:	90                   	nop
   14000314e:	90                   	nop
   14000314f:	90                   	nop

0000000140003150 <__p__fmode>:
   140003150:	55                   	push   rbp
   140003151:	48 89 e5             	mov    rbp,rsp
   140003154:	48 8b 05 75 22 00 00 	mov    rax,QWORD PTR [rip+0x2275]        # 1400053d0 <.refptr.__imp__fmode>
   14000315b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000315e:	5d                   	pop    rbp
   14000315f:	c3                   	ret

0000000140003160 <__p__commode>:
   140003160:	55                   	push   rbp
   140003161:	48 89 e5             	mov    rbp,rsp
   140003164:	48 8b 05 55 22 00 00 	mov    rax,QWORD PTR [rip+0x2255]        # 1400053c0 <.refptr.__imp__commode>
   14000316b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000316e:	5d                   	pop    rbp
   14000316f:	c3                   	ret

0000000140003170 <__p___initenv>:
   140003170:	55                   	push   rbp
   140003171:	48 89 e5             	mov    rbp,rsp
   140003174:	48 8b 05 35 22 00 00 	mov    rax,QWORD PTR [rip+0x2235]        # 1400053b0 <.refptr.__imp___initenv>
   14000317b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000317e:	5d                   	pop    rbp
   14000317f:	c3                   	ret

0000000140003180 <_set_invalid_parameter_handler>:
   140003180:	55                   	push   rbp
   140003181:	48 89 e5             	mov    rbp,rsp
   140003184:	48 83 ec 10          	sub    rsp,0x10
   140003188:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000318c:	48 8d 05 1d 60 00 00 	lea    rax,[rip+0x601d]        # 1400091b0 <handler>
   140003193:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003197:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000319b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000319f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   1400031a3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031a7:	48 87 10             	xchg   QWORD PTR [rax],rdx
   1400031aa:	48 89 d0             	mov    rax,rdx
   1400031ad:	48 83 c4 10          	add    rsp,0x10
   1400031b1:	5d                   	pop    rbp
   1400031b2:	c3                   	ret

00000001400031b3 <_get_invalid_parameter_handler>:
   1400031b3:	55                   	push   rbp
   1400031b4:	48 89 e5             	mov    rbp,rsp
   1400031b7:	48 8b 05 f2 5f 00 00 	mov    rax,QWORD PTR [rip+0x5ff2]        # 1400091b0 <handler>
   1400031be:	5d                   	pop    rbp
   1400031bf:	c3                   	ret

00000001400031c0 <_configthreadlocale>:
   1400031c0:	55                   	push   rbp
   1400031c1:	48 89 e5             	mov    rbp,rsp
   1400031c4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400031c7:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   1400031cb:	75 07                	jne    1400031d4 <_configthreadlocale+0x14>
   1400031cd:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400031d2:	eb 05                	jmp    1400031d9 <_configthreadlocale+0x19>
   1400031d4:	b8 02 00 00 00       	mov    eax,0x2
   1400031d9:	5d                   	pop    rbp
   1400031da:	c3                   	ret
   1400031db:	90                   	nop
   1400031dc:	90                   	nop
   1400031dd:	90                   	nop
   1400031de:	90                   	nop
   1400031df:	90                   	nop

00000001400031e0 <__acrt_iob_func>:
   1400031e0:	55                   	push   rbp
   1400031e1:	48 89 e5             	mov    rbp,rsp
   1400031e4:	48 83 ec 20          	sub    rsp,0x20
   1400031e8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400031eb:	e8 30 00 00 00       	call   140003220 <__iob_func>
   1400031f0:	48 89 c1             	mov    rcx,rax
   1400031f3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400031f6:	48 89 d0             	mov    rax,rdx
   1400031f9:	48 01 c0             	add    rax,rax
   1400031fc:	48 01 d0             	add    rax,rdx
   1400031ff:	48 c1 e0 04          	shl    rax,0x4
   140003203:	48 01 c8             	add    rax,rcx
   140003206:	48 83 c4 20          	add    rsp,0x20
   14000320a:	5d                   	pop    rbp
   14000320b:	c3                   	ret
   14000320c:	90                   	nop
   14000320d:	90                   	nop
   14000320e:	90                   	nop
   14000320f:	90                   	nop

0000000140003210 <__C_specific_handler>:
   140003210:	ff 25 ea 6f 00 00    	jmp    QWORD PTR [rip+0x6fea]        # 14000a200 <__imp___C_specific_handler>
   140003216:	90                   	nop
   140003217:	90                   	nop

0000000140003218 <__getmainargs>:
   140003218:	ff 25 ea 6f 00 00    	jmp    QWORD PTR [rip+0x6fea]        # 14000a208 <__imp___getmainargs>
   14000321e:	90                   	nop
   14000321f:	90                   	nop

0000000140003220 <__iob_func>:
   140003220:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a218 <__imp___iob_func>
   140003226:	90                   	nop
   140003227:	90                   	nop

0000000140003228 <__set_app_type>:
   140003228:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a220 <__imp___set_app_type>
   14000322e:	90                   	nop
   14000322f:	90                   	nop

0000000140003230 <__setusermatherr>:
   140003230:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a228 <__imp___setusermatherr>
   140003236:	90                   	nop
   140003237:	90                   	nop

0000000140003238 <_amsg_exit>:
   140003238:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a230 <__imp__amsg_exit>
   14000323e:	90                   	nop
   14000323f:	90                   	nop

0000000140003240 <_cexit>:
   140003240:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a238 <__imp__cexit>
   140003246:	90                   	nop
   140003247:	90                   	nop

0000000140003248 <_initterm>:
   140003248:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a250 <__imp__initterm>
   14000324e:	90                   	nop
   14000324f:	90                   	nop

0000000140003250 <_crt_atexit>:
   140003250:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a258 <__imp__crt_atexit>
   140003256:	90                   	nop
   140003257:	90                   	nop

0000000140003258 <abort>:
   140003258:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a260 <__imp_abort>
   14000325e:	90                   	nop
   14000325f:	90                   	nop

0000000140003260 <calloc>:
   140003260:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a268 <__imp_calloc>
   140003266:	90                   	nop
   140003267:	90                   	nop

0000000140003268 <exit>:
   140003268:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a270 <__imp_exit>
   14000326e:	90                   	nop
   14000326f:	90                   	nop

0000000140003270 <fflush>:
   140003270:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a278 <__imp_fflush>
   140003276:	90                   	nop
   140003277:	90                   	nop

0000000140003278 <fprintf>:
   140003278:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a280 <__imp_fprintf>
   14000327e:	90                   	nop
   14000327f:	90                   	nop

0000000140003280 <free>:
   140003280:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a288 <__imp_free>
   140003286:	90                   	nop
   140003287:	90                   	nop

0000000140003288 <malloc>:
   140003288:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a290 <__imp_malloc>
   14000328e:	90                   	nop
   14000328f:	90                   	nop

0000000140003290 <memcpy>:
   140003290:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a298 <__imp_memcpy>
   140003296:	90                   	nop
   140003297:	90                   	nop

0000000140003298 <setvbuf>:
   140003298:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a2a0 <__imp_setvbuf>
   14000329e:	90                   	nop
   14000329f:	90                   	nop

00000001400032a0 <signal>:
   1400032a0:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a2a8 <__imp_signal>
   1400032a6:	90                   	nop
   1400032a7:	90                   	nop

00000001400032a8 <strlen>:
   1400032a8:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a2b0 <__imp_strlen>
   1400032ae:	90                   	nop
   1400032af:	90                   	nop

00000001400032b0 <strncmp>:
   1400032b0:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a2b8 <__imp_strncmp>
   1400032b6:	90                   	nop
   1400032b7:	90                   	nop

00000001400032b8 <vfprintf>:
   1400032b8:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a2c0 <__imp_vfprintf>
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <VirtualQuery>:
   1400032c0:	ff 25 2a 6f 00 00    	jmp    QWORD PTR [rip+0x6f2a]        # 14000a1f0 <__imp_VirtualQuery>
   1400032c6:	90                   	nop
   1400032c7:	90                   	nop

00000001400032c8 <VirtualProtect>:
   1400032c8:	ff 25 1a 6f 00 00    	jmp    QWORD PTR [rip+0x6f1a]        # 14000a1e8 <__imp_VirtualProtect>
   1400032ce:	90                   	nop
   1400032cf:	90                   	nop

00000001400032d0 <TlsGetValue>:
   1400032d0:	ff 25 0a 6f 00 00    	jmp    QWORD PTR [rip+0x6f0a]        # 14000a1e0 <__imp_TlsGetValue>
   1400032d6:	90                   	nop
   1400032d7:	90                   	nop

00000001400032d8 <Sleep>:
   1400032d8:	ff 25 fa 6e 00 00    	jmp    QWORD PTR [rip+0x6efa]        # 14000a1d8 <__imp_Sleep>
   1400032de:	90                   	nop
   1400032df:	90                   	nop

00000001400032e0 <SetUnhandledExceptionFilter>:
   1400032e0:	ff 25 ea 6e 00 00    	jmp    QWORD PTR [rip+0x6eea]        # 14000a1d0 <__imp_SetUnhandledExceptionFilter>
   1400032e6:	90                   	nop
   1400032e7:	90                   	nop

00000001400032e8 <LoadLibraryA>:
   1400032e8:	ff 25 da 6e 00 00    	jmp    QWORD PTR [rip+0x6eda]        # 14000a1c8 <__imp_LoadLibraryA>
   1400032ee:	90                   	nop
   1400032ef:	90                   	nop

00000001400032f0 <LeaveCriticalSection>:
   1400032f0:	ff 25 ca 6e 00 00    	jmp    QWORD PTR [rip+0x6eca]        # 14000a1c0 <__imp_LeaveCriticalSection>
   1400032f6:	90                   	nop
   1400032f7:	90                   	nop

00000001400032f8 <InitializeCriticalSection>:
   1400032f8:	ff 25 ba 6e 00 00    	jmp    QWORD PTR [rip+0x6eba]        # 14000a1b8 <__imp_InitializeCriticalSection>
   1400032fe:	90                   	nop
   1400032ff:	90                   	nop

0000000140003300 <GetProcAddress>:
   140003300:	ff 25 aa 6e 00 00    	jmp    QWORD PTR [rip+0x6eaa]        # 14000a1b0 <__imp_GetProcAddress>
   140003306:	90                   	nop
   140003307:	90                   	nop

0000000140003308 <GetModuleHandleA>:
   140003308:	ff 25 9a 6e 00 00    	jmp    QWORD PTR [rip+0x6e9a]        # 14000a1a8 <__imp_GetModuleHandleA>
   14000330e:	90                   	nop
   14000330f:	90                   	nop

0000000140003310 <GetLastError>:
   140003310:	ff 25 8a 6e 00 00    	jmp    QWORD PTR [rip+0x6e8a]        # 14000a1a0 <__imp_GetLastError>
   140003316:	90                   	nop
   140003317:	90                   	nop

0000000140003318 <FreeLibrary>:
   140003318:	ff 25 7a 6e 00 00    	jmp    QWORD PTR [rip+0x6e7a]        # 14000a198 <__imp_FreeLibrary>
   14000331e:	90                   	nop
   14000331f:	90                   	nop

0000000140003320 <EnterCriticalSection>:
   140003320:	ff 25 6a 6e 00 00    	jmp    QWORD PTR [rip+0x6e6a]        # 14000a190 <__imp_EnterCriticalSection>
   140003326:	90                   	nop
   140003327:	90                   	nop

0000000140003328 <DeleteCriticalSection>:
   140003328:	ff 25 5a 6e 00 00    	jmp    QWORD PTR [rip+0x6e5a]        # 14000a188 <__IAT_start__>
   14000332e:	90                   	nop
   14000332f:	90                   	nop

0000000140003330 <main>:
   140003330:	48 83 ec 28          	sub    rsp,0x28
   140003334:	e8 5e e5 ff ff       	call   140001897 <__main>
   140003339:	b8 2a 00 00 00       	mov    eax,0x2a
   14000333e:	c7 05 38 5d 00 00 08 	mov    DWORD PTR [rip+0x5d38],0x8        # 140009080 <g_obs>
   140003345:	00 00 00 
   140003348:	c7 05 2e 5d 00 00 04 	mov    DWORD PTR [rip+0x5d2e],0x4        # 140009080 <g_obs>
   14000334f:	00 00 00 
   140003352:	c7 05 24 5d 00 00 10 	mov    DWORD PTR [rip+0x5d24],0x10        # 140009080 <g_obs>
   140003359:	00 00 00 
   14000335c:	c7 05 1a 5d 00 00 02 	mov    DWORD PTR [rip+0x5d1a],0x2        # 140009080 <g_obs>
   140003363:	00 00 00 
   140003366:	48 83 c4 28          	add    rsp,0x28
   14000336a:	c3                   	ret
   14000336b:	90                   	nop
   14000336c:	90                   	nop
   14000336d:	90                   	nop
   14000336e:	90                   	nop
   14000336f:	90                   	nop

0000000140003370 <register_frame_ctor>:
   140003370:	e9 fb e2 ff ff       	jmp    140001670 <__gcc_register_frame>
   140003375:	90                   	nop
   140003376:	90                   	nop
   140003377:	90                   	nop
   140003378:	90                   	nop
   140003379:	90                   	nop
   14000337a:	90                   	nop
   14000337b:	90                   	nop
   14000337c:	90                   	nop
   14000337d:	90                   	nop
   14000337e:	90                   	nop
   14000337f:	90                   	nop
