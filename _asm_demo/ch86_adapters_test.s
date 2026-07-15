
ch86_adapters_test.exe:     file format pei-x86-64


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
   140001024:	e8 27 23 00 00       	call   140003350 <fflush>
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
   14000103f:	48 8b 05 ba 43 00 00 	mov    rax,QWORD PTR [rip+0x43ba]        # 140005400 <.refptr.__mingw_app_type>
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
   14000106e:	48 8b 05 8b 43 00 00 	mov    rax,QWORD PTR [rip+0x438b]        # 140005400 <.refptr.__mingw_app_type>
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
   1400010e8:	48 8b 05 b9 91 00 00 	mov    rax,QWORD PTR [rip+0x91b9]        # 14000a2a8 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 58 43 00 00 	mov    rax,QWORD PTR [rip+0x4358]        # 140005450 <.refptr.__native_startup_lock>
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
   140001128:	48 8b 05 31 43 00 00 	mov    rax,QWORD PTR [rip+0x4331]        # 140005460 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 d8 21 00 00       	call   140003318 <_amsg_exit>
   140001140:	48 8b 05 19 43 00 00 	mov    rax,QWORD PTR [rip+0x4319]        # 140005460 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 08 43 00 00 	mov    rax,QWORD PTR [rip+0x4308]        # 140005460 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 58 21 00 00       	call   1400032c0 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 ff 21 00 00       	call   140003380 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 9f 21 00 00       	call   140003338 <abort>
   140001199:	e8 12 12 00 00       	call   1400023b0 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 3b 43 00 00 	mov    rax,QWORD PTR [rip+0x433b]        # 1400054e0 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 f1 90 00 00 	mov    rax,QWORD PTR [rip+0x90f1]        # 14000a2a0 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 88 42 00 00 	mov    rdx,QWORD PTR [rip+0x4288]        # 140005440 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 96 20 00 00       	call   140003260 <_set_invalid_parameter_handler>
   1400011ca:	e8 f1 1a 00 00       	call   140002cc0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 1f 42 00 00 	mov    rax,QWORD PTR [rip+0x421f]        # 140005400 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 17 21 00 00       	call   140003308 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 0b 21 00 00       	call   140003308 <__set_app_type>
   1400011fd:	e8 2e 20 00 00       	call   140003230 <__p__fmode>
   140001202:	48 8b 15 c7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42c7]        # 1400054d0 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 2e 20 00 00       	call   140003240 <__p__commode>
   140001212:	48 8b 15 97 42 00 00 	mov    rdx,QWORD PTR [rip+0x4297]        # 1400054b0 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 6e 07 00 00       	call   140001990 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 e3 20 00 00       	call   140003318 <_amsg_exit>
   140001235:	48 8b 05 24 41 00 00 	mov    rax,QWORD PTR [rip+0x4124]        # 140005360 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 a6 42 00 00 	mov    rax,QWORD PTR [rip+0x42a6]        # 1400054f0 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 78 12 00 00       	call   1400024ca <__mingw_setusermatherr>
   140001252:	48 8b 05 67 41 00 00 	mov    rax,QWORD PTR [rip+0x4167]        # 1400053c0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 36 20 00 00       	call   1400032a0 <_configthreadlocale>
   14000126a:	48 8b 15 2f 42 00 00 	mov    rdx,QWORD PTR [rip+0x422f]        # 1400054a0 <.refptr.__xi_z>
   140001271:	48 8b 05 18 42 00 00 	mov    rax,QWORD PTR [rip+0x4218]        # 140005490 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 50 1f 00 00       	call   1400031d0 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 8a 20 00 00       	call   140003318 <_amsg_exit>
   14000128e:	48 8b 05 6b 42 00 00 	mov    rax,QWORD PTR [rip+0x426b]        # 140005500 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 1f 42 00 00 	mov    rax,QWORD PTR [rip+0x421f]        # 1400054c0 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 7d 00 00 	lea    r10,[rip+0x7d65]        # 140009010 <envp>
   1400012ab:	48 8d 15 56 7d 00 00 	lea    rdx,[rip+0x7d56]        # 140009008 <argv>
   1400012b2:	48 8d 05 4b 7d 00 00 	lea    rax,[rip+0x7d4b]        # 140009004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 28 20 00 00       	call   1400032f8 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 35 20 00 00       	call   140003318 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 0e 20 00 00       	call   140003318 <_amsg_exit>
   14000130a:	48 8b 15 6f 41 00 00 	mov    rdx,QWORD PTR [rip+0x416f]        # 140005480 <.refptr.__xc_z>
   140001311:	48 8b 05 58 41 00 00 	mov    rax,QWORD PTR [rip+0x4158]        # 140005470 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 08 20 00 00       	call   140003328 <_initterm>
   140001320:	e8 42 06 00 00       	call   140001967 <__main>
   140001325:	48 8b 05 34 41 00 00 	mov    rax,QWORD PTR [rip+0x4134]        # 140005460 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de 7c 00 00 01 	mov    DWORD PTR [rip+0x7cde],0x1        # 14000901c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 05 41 00 00 	mov    rax,QWORD PTR [rip+0x4105]        # 140005450 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 47 40 00 00 	mov    rax,QWORD PTR [rip+0x4047]        # 1400053b0 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 38 40 00 00 	mov    rax,QWORD PTR [rip+0x4038]        # 1400053b0 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 be 1e 00 00       	call   140003250 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 36 24 00 00       	call   1400037f0 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 77 1f 00 00       	call   140003348 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 40 1f 00 00       	call   140003320 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 15 40 00 00 	mov    rax,QWORD PTR [rip+0x4015]        # 140005410 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 18 40 00 00 	mov    rax,QWORD PTR [rip+0x4018]        # 140005420 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 1b 40 00 00 	mov    rax,QWORD PTR [rip+0x401b]        # 140005430 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 5e 3f 00 00 	mov    rax,QWORD PTR [rip+0x3f5e]        # 140005380 <.refptr.__ImageBase>
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
   140001511:	e8 52 1e 00 00       	call   140003368 <malloc>
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
   14000155c:	e8 2f 1e 00 00       	call   140003390 <strlen>
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
   140001585:	e8 de 1d 00 00       	call   140003368 <malloc>
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
   1400015e8:	e8 83 1d 00 00       	call   140003370 <memcpy>
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
   140001642:	e8 e9 1c 00 00       	call   140003330 <_crt_atexit>
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
   140001682:	ff 15 f0 8b 00 00    	call   QWORD PTR [rip+0x8bf0]        # 14000a278 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 fb 8b 00 00    	call   QWORD PTR [rip+0x8bfb]        # 14000a298 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d dc 8b 00 00 	mov    r9,QWORD PTR [rip+0x8bdc]        # 14000a280 <__imp_GetProcAddress>
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
   14000174e:	48 ff 25 13 8b 00 00 	rex.W jmp QWORD PTR [rip+0x8b13]        # 14000a268 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]>:
   140001760:	48 83 ec 38          	sub    rsp,0x38
   140001764:	48 8b 41 30          	mov    rax,QWORD PTR [rcx+0x30]
   140001768:	49 89 c9             	mov    r9,rcx
   14000176b:	48 8b 49 40          	mov    rcx,QWORD PTR [rcx+0x40]
   14000176f:	49 89 d2             	mov    r10,rdx
   140001772:	48 8d 51 fc          	lea    rdx,[rcx-0x4]
   140001776:	48 39 d0             	cmp    rax,rdx
   140001779:	74 13                	je     14000178e <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]+0x2e>
   14000177b:	41 8b 12             	mov    edx,DWORD PTR [r10]
   14000177e:	48 83 c0 04          	add    rax,0x4
   140001782:	89 50 fc             	mov    DWORD PTR [rax-0x4],edx
   140001785:	49 89 41 30          	mov    QWORD PTR [r9+0x30],rax
   140001789:	48 83 c4 38          	add    rsp,0x38
   14000178d:	c3                   	ret
   14000178e:	49 8b 49 48          	mov    rcx,QWORD PTR [r9+0x48]
   140001792:	48 89 ca             	mov    rdx,rcx
   140001795:	49 2b 51 28          	sub    rdx,QWORD PTR [r9+0x28]
   140001799:	48 c1 fa 03          	sar    rdx,0x3
   14000179d:	48 83 f9 01          	cmp    rcx,0x1
   1400017a1:	48 83 d2 ff          	adc    rdx,0xffffffffffffffff
   1400017a5:	49 2b 41 38          	sub    rax,QWORD PTR [r9+0x38]
   1400017a9:	48 c1 e2 07          	shl    rdx,0x7
   1400017ad:	48 c1 f8 02          	sar    rax,0x2
   1400017b1:	48 01 d0             	add    rax,rdx
   1400017b4:	49 8b 51 20          	mov    rdx,QWORD PTR [r9+0x20]
   1400017b8:	49 2b 51 10          	sub    rdx,QWORD PTR [r9+0x10]
   1400017bc:	48 c1 fa 02          	sar    rdx,0x2
   1400017c0:	48 01 d0             	add    rax,rdx
   1400017c3:	48 ba ff ff ff ff ff 	movabs rdx,0x3fffffffffffffff
   1400017ca:	ff ff 3f 
   1400017cd:	48 39 d0             	cmp    rax,rdx
   1400017d0:	0f 84 ea 1f 00 00    	je     1400037c0 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0] [clone .cold]>
   1400017d6:	49 8b 41 08          	mov    rax,QWORD PTR [r9+0x8]
   1400017da:	49 2b 09             	sub    rcx,QWORD PTR [r9]
   1400017dd:	48 c1 f9 03          	sar    rcx,0x3
   1400017e1:	48 29 c8             	sub    rax,rcx
   1400017e4:	48 83 f8 01          	cmp    rax,0x1
   1400017e8:	76 56                	jbe    140001840 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]+0xe0>
   1400017ea:	49 8b 51 48          	mov    rdx,QWORD PTR [r9+0x48]
   1400017ee:	b9 00 02 00 00       	mov    ecx,0x200
   1400017f3:	4c 89 54 24 48       	mov    QWORD PTR [rsp+0x48],r10
   1400017f8:	4c 89 4c 24 40       	mov    QWORD PTR [rsp+0x40],r9
   1400017fd:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
   140001802:	e8 89 00 00 00       	call   140001890 <operator new(unsigned long long)>
   140001807:	4c 8b 4c 24 40       	mov    r9,QWORD PTR [rsp+0x40]
   14000180c:	48 8b 54 24 28       	mov    rdx,QWORD PTR [rsp+0x28]
   140001811:	4c 8b 54 24 48       	mov    r10,QWORD PTR [rsp+0x48]
   140001816:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   14000181a:	49 8b 49 30          	mov    rcx,QWORD PTR [r9+0x30]
   14000181e:	48 83 c2 08          	add    rdx,0x8
   140001822:	45 8b 02             	mov    r8d,DWORD PTR [r10]
   140001825:	44 89 01             	mov    DWORD PTR [rcx],r8d
   140001828:	49 89 51 48          	mov    QWORD PTR [r9+0x48],rdx
   14000182c:	48 8d 90 00 02 00 00 	lea    rdx,[rax+0x200]
   140001833:	49 89 41 38          	mov    QWORD PTR [r9+0x38],rax
   140001837:	49 89 51 40          	mov    QWORD PTR [r9+0x40],rdx
   14000183b:	e9 45 ff ff ff       	jmp    140001785 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]+0x25>
   140001840:	4c 89 c9             	mov    rcx,r9
   140001843:	45 31 c0             	xor    r8d,r8d
   140001846:	ba 01 00 00 00       	mov    edx,0x1
   14000184b:	4c 89 54 24 48       	mov    QWORD PTR [rsp+0x48],r10
   140001850:	4c 89 4c 24 40       	mov    QWORD PTR [rsp+0x40],r9
   140001855:	e8 66 1d 00 00       	call   1400035c0 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)>
   14000185a:	4c 8b 54 24 48       	mov    r10,QWORD PTR [rsp+0x48]
   14000185f:	4c 8b 4c 24 40       	mov    r9,QWORD PTR [rsp+0x40]
   140001864:	eb 84                	jmp    1400017ea <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]+0x8a>
   140001866:	90                   	nop
   140001867:	90                   	nop
   140001868:	90                   	nop
   140001869:	90                   	nop
   14000186a:	90                   	nop
   14000186b:	90                   	nop
   14000186c:	90                   	nop
   14000186d:	90                   	nop
   14000186e:	90                   	nop
   14000186f:	90                   	nop

0000000140001870 <__gxx_personality_seh0>:
   140001870:	ff 25 d2 89 00 00    	jmp    QWORD PTR [rip+0x89d2]        # 14000a248 <__imp___gxx_personality_seh0>
   140001876:	90                   	nop
   140001877:	90                   	nop

0000000140001878 <__cxa_rethrow>:
   140001878:	ff 25 c2 89 00 00    	jmp    QWORD PTR [rip+0x89c2]        # 14000a240 <__imp___cxa_rethrow>
   14000187e:	90                   	nop
   14000187f:	90                   	nop

0000000140001880 <__cxa_end_catch>:
   140001880:	ff 25 b2 89 00 00    	jmp    QWORD PTR [rip+0x89b2]        # 14000a238 <__imp___cxa_end_catch>
   140001886:	90                   	nop
   140001887:	90                   	nop

0000000140001888 <__cxa_begin_catch>:
   140001888:	ff 25 a2 89 00 00    	jmp    QWORD PTR [rip+0x89a2]        # 14000a230 <__imp___cxa_begin_catch>
   14000188e:	90                   	nop
   14000188f:	90                   	nop

0000000140001890 <operator new(unsigned long long)>:
   140001890:	ff 25 92 89 00 00    	jmp    QWORD PTR [rip+0x8992]        # 14000a228 <__imp__Znwy>
   140001896:	90                   	nop
   140001897:	90                   	nop

0000000140001898 <operator delete(void*, unsigned long long)>:
   140001898:	ff 25 82 89 00 00    	jmp    QWORD PTR [rip+0x8982]        # 14000a220 <__imp__ZdlPvy>
   14000189e:	90                   	nop
   14000189f:	90                   	nop

00000001400018a0 <std::__throw_length_error(char const*)>:
   1400018a0:	ff 25 72 89 00 00    	jmp    QWORD PTR [rip+0x8972]        # 14000a218 <__imp__ZSt20__throw_length_errorPKc>
   1400018a6:	90                   	nop
   1400018a7:	90                   	nop
   1400018a8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   1400018af:	00 

00000001400018b0 <__do_global_dtors>:
   1400018b0:	55                   	push   rbp
   1400018b1:	48 89 e5             	mov    rbp,rsp
   1400018b4:	48 83 ec 20          	sub    rsp,0x20
   1400018b8:	eb 1e                	jmp    1400018d8 <__do_global_dtors+0x28>
   1400018ba:	48 8b 05 4f 27 00 00 	mov    rax,QWORD PTR [rip+0x274f]        # 140004010 <p.0>
   1400018c1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400018c4:	ff d0                	call   rax
   1400018c6:	48 8b 05 43 27 00 00 	mov    rax,QWORD PTR [rip+0x2743]        # 140004010 <p.0>
   1400018cd:	48 83 c0 08          	add    rax,0x8
   1400018d1:	48 89 05 38 27 00 00 	mov    QWORD PTR [rip+0x2738],rax        # 140004010 <p.0>
   1400018d8:	48 8b 05 31 27 00 00 	mov    rax,QWORD PTR [rip+0x2731]        # 140004010 <p.0>
   1400018df:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400018e2:	48 85 c0             	test   rax,rax
   1400018e5:	75 d3                	jne    1400018ba <__do_global_dtors+0xa>
   1400018e7:	90                   	nop
   1400018e8:	90                   	nop
   1400018e9:	48 83 c4 20          	add    rsp,0x20
   1400018ed:	5d                   	pop    rbp
   1400018ee:	c3                   	ret

00000001400018ef <__do_global_ctors>:
   1400018ef:	55                   	push   rbp
   1400018f0:	48 89 e5             	mov    rbp,rsp
   1400018f3:	48 83 ec 30          	sub    rsp,0x30
   1400018f7:	48 8b 05 72 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a72]        # 140005370 <.refptr.__CTOR_LIST__>
   1400018fe:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001901:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140001904:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   140001908:	75 25                	jne    14000192f <__do_global_ctors+0x40>
   14000190a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001911:	eb 04                	jmp    140001917 <__do_global_ctors+0x28>
   140001913:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001917:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000191a:	8d 50 01             	lea    edx,[rax+0x1]
   14000191d:	48 8b 05 4c 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a4c]        # 140005370 <.refptr.__CTOR_LIST__>
   140001924:	89 d2                	mov    edx,edx
   140001926:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000192a:	48 85 c0             	test   rax,rax
   14000192d:	75 e4                	jne    140001913 <__do_global_ctors+0x24>
   14000192f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001932:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001935:	eb 14                	jmp    14000194b <__do_global_ctors+0x5c>
   140001937:	48 8b 05 32 3a 00 00 	mov    rax,QWORD PTR [rip+0x3a32]        # 140005370 <.refptr.__CTOR_LIST__>
   14000193e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001941:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001945:	ff d0                	call   rax
   140001947:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000194b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000194f:	75 e6                	jne    140001937 <__do_global_ctors+0x48>
   140001951:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 1400018b0 <__do_global_dtors>
   140001958:	48 89 c1             	mov    rcx,rax
   14000195b:	e8 cf fc ff ff       	call   14000162f <atexit>
   140001960:	90                   	nop
   140001961:	48 83 c4 30          	add    rsp,0x30
   140001965:	5d                   	pop    rbp
   140001966:	c3                   	ret

0000000140001967 <__main>:
   140001967:	55                   	push   rbp
   140001968:	48 89 e5             	mov    rbp,rsp
   14000196b:	48 83 ec 20          	sub    rsp,0x20
   14000196f:	8b 05 0b 77 00 00    	mov    eax,DWORD PTR [rip+0x770b]        # 140009080 <initialized>
   140001975:	85 c0                	test   eax,eax
   140001977:	75 0f                	jne    140001988 <__main+0x21>
   140001979:	c7 05 fd 76 00 00 01 	mov    DWORD PTR [rip+0x76fd],0x1        # 140009080 <initialized>
   140001980:	00 00 00 
   140001983:	e8 67 ff ff ff       	call   1400018ef <__do_global_ctors>
   140001988:	90                   	nop
   140001989:	48 83 c4 20          	add    rsp,0x20
   14000198d:	5d                   	pop    rbp
   14000198e:	c3                   	ret
   14000198f:	90                   	nop

0000000140001990 <_setargv>:
   140001990:	55                   	push   rbp
   140001991:	48 89 e5             	mov    rbp,rsp
   140001994:	b8 00 00 00 00       	mov    eax,0x0
   140001999:	5d                   	pop    rbp
   14000199a:	c3                   	ret
   14000199b:	90                   	nop
   14000199c:	90                   	nop
   14000199d:	90                   	nop
   14000199e:	90                   	nop
   14000199f:	90                   	nop

00000001400019a0 <__dyn_tls_init>:
   1400019a0:	55                   	push   rbp
   1400019a1:	48 89 e5             	mov    rbp,rsp
   1400019a4:	48 83 ec 30          	sub    rsp,0x30
   1400019a8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400019ac:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   1400019af:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400019b3:	48 8b 05 96 39 00 00 	mov    rax,QWORD PTR [rip+0x3996]        # 140005350 <.refptr._CRT_MT>
   1400019ba:	8b 00                	mov    eax,DWORD PTR [rax]
   1400019bc:	83 f8 02             	cmp    eax,0x2
   1400019bf:	74 0d                	je     1400019ce <__dyn_tls_init+0x2e>
   1400019c1:	48 8b 05 88 39 00 00 	mov    rax,QWORD PTR [rip+0x3988]        # 140005350 <.refptr._CRT_MT>
   1400019c8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   1400019ce:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   1400019d2:	74 1e                	je     1400019f2 <__dyn_tls_init+0x52>
   1400019d4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   1400019d8:	75 5b                	jne    140001a35 <__dyn_tls_init+0x95>
   1400019da:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400019de:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400019e1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400019e5:	49 89 c8             	mov    r8,rcx
   1400019e8:	48 89 c1             	mov    rcx,rax
   1400019eb:	e8 d1 11 00 00       	call   140002bc1 <__mingw_TLScallback>
   1400019f0:	eb 43                	jmp    140001a35 <__dyn_tls_init+0x95>
   1400019f2:	48 8d 05 bf 3c 00 00 	lea    rax,[rip+0x3cbf]        # 1400056b8 <___crt_xd_start__>
   1400019f9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019fd:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001a02:	eb 22                	jmp    140001a26 <__dyn_tls_init+0x86>
   140001a04:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001a08:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001a0c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001a10:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001a13:	48 85 c0             	test   rax,rax
   140001a16:	74 09                	je     140001a21 <__dyn_tls_init+0x81>
   140001a18:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001a1c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001a1f:	ff d0                	call   rax
   140001a21:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001a26:	48 8d 05 93 3c 00 00 	lea    rax,[rip+0x3c93]        # 1400056c0 <__xd_z>
   140001a2d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001a31:	75 d1                	jne    140001a04 <__dyn_tls_init+0x64>
   140001a33:	eb 01                	jmp    140001a36 <__dyn_tls_init+0x96>
   140001a35:	90                   	nop
   140001a36:	48 83 c4 30          	add    rsp,0x30
   140001a3a:	5d                   	pop    rbp
   140001a3b:	c3                   	ret

0000000140001a3c <__tlregdtor>:
   140001a3c:	55                   	push   rbp
   140001a3d:	48 89 e5             	mov    rbp,rsp
   140001a40:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001a44:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001a49:	75 07                	jne    140001a52 <__tlregdtor+0x16>
   140001a4b:	b8 00 00 00 00       	mov    eax,0x0
   140001a50:	eb 05                	jmp    140001a57 <__tlregdtor+0x1b>
   140001a52:	b8 00 00 00 00       	mov    eax,0x0
   140001a57:	5d                   	pop    rbp
   140001a58:	c3                   	ret

0000000140001a59 <__dyn_tls_dtor>:
   140001a59:	55                   	push   rbp
   140001a5a:	48 89 e5             	mov    rbp,rsp
   140001a5d:	48 83 ec 20          	sub    rsp,0x20
   140001a61:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001a65:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001a68:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001a6c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001a70:	74 06                	je     140001a78 <__dyn_tls_dtor+0x1f>
   140001a72:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001a76:	75 18                	jne    140001a90 <__dyn_tls_dtor+0x37>
   140001a78:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001a7c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140001a7f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001a83:	49 89 c8             	mov    r8,rcx
   140001a86:	48 89 c1             	mov    rcx,rax
   140001a89:	e8 33 11 00 00       	call   140002bc1 <__mingw_TLScallback>
   140001a8e:	eb 01                	jmp    140001a91 <__dyn_tls_dtor+0x38>
   140001a90:	90                   	nop
   140001a91:	48 83 c4 20          	add    rsp,0x20
   140001a95:	5d                   	pop    rbp
   140001a96:	c3                   	ret
   140001a97:	90                   	nop
   140001a98:	90                   	nop
   140001a99:	90                   	nop
   140001a9a:	90                   	nop
   140001a9b:	90                   	nop
   140001a9c:	90                   	nop
   140001a9d:	90                   	nop
   140001a9e:	90                   	nop
   140001a9f:	90                   	nop

0000000140001aa0 <_matherr>:
   140001aa0:	55                   	push   rbp
   140001aa1:	53                   	push   rbx
   140001aa2:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001aa9:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140001aae:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   140001ab2:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   140001ab6:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   140001abb:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   140001abf:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001ac3:	8b 00                	mov    eax,DWORD PTR [rax]
   140001ac5:	83 f8 06             	cmp    eax,0x6
   140001ac8:	74 56                	je     140001b20 <_matherr+0x80>
   140001aca:	83 f8 06             	cmp    eax,0x6
   140001acd:	7f 78                	jg     140001b47 <_matherr+0xa7>
   140001acf:	83 f8 05             	cmp    eax,0x5
   140001ad2:	74 59                	je     140001b2d <_matherr+0x8d>
   140001ad4:	83 f8 05             	cmp    eax,0x5
   140001ad7:	7f 6e                	jg     140001b47 <_matherr+0xa7>
   140001ad9:	83 f8 04             	cmp    eax,0x4
   140001adc:	74 5c                	je     140001b3a <_matherr+0x9a>
   140001ade:	83 f8 04             	cmp    eax,0x4
   140001ae1:	7f 64                	jg     140001b47 <_matherr+0xa7>
   140001ae3:	83 f8 03             	cmp    eax,0x3
   140001ae6:	74 2b                	je     140001b13 <_matherr+0x73>
   140001ae8:	83 f8 03             	cmp    eax,0x3
   140001aeb:	7f 5a                	jg     140001b47 <_matherr+0xa7>
   140001aed:	83 f8 01             	cmp    eax,0x1
   140001af0:	74 07                	je     140001af9 <_matherr+0x59>
   140001af2:	83 f8 02             	cmp    eax,0x2
   140001af5:	74 0f                	je     140001b06 <_matherr+0x66>
   140001af7:	eb 4e                	jmp    140001b47 <_matherr+0xa7>
   140001af9:	48 8d 05 c0 35 00 00 	lea    rax,[rip+0x35c0]        # 1400050c0 <.rdata>
   140001b00:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b04:	eb 4d                	jmp    140001b53 <_matherr+0xb3>
   140001b06:	48 8d 05 d2 35 00 00 	lea    rax,[rip+0x35d2]        # 1400050df <.rdata+0x1f>
   140001b0d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b11:	eb 40                	jmp    140001b53 <_matherr+0xb3>
   140001b13:	48 8d 05 e6 35 00 00 	lea    rax,[rip+0x35e6]        # 140005100 <.rdata+0x40>
   140001b1a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b1e:	eb 33                	jmp    140001b53 <_matherr+0xb3>
   140001b20:	48 8d 05 f9 35 00 00 	lea    rax,[rip+0x35f9]        # 140005120 <.rdata+0x60>
   140001b27:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b2b:	eb 26                	jmp    140001b53 <_matherr+0xb3>
   140001b2d:	48 8d 05 14 36 00 00 	lea    rax,[rip+0x3614]        # 140005148 <.rdata+0x88>
   140001b34:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b38:	eb 19                	jmp    140001b53 <_matherr+0xb3>
   140001b3a:	48 8d 05 2f 36 00 00 	lea    rax,[rip+0x362f]        # 140005170 <.rdata+0xb0>
   140001b41:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b45:	eb 0c                	jmp    140001b53 <_matherr+0xb3>
   140001b47:	48 8d 05 58 36 00 00 	lea    rax,[rip+0x3658]        # 1400051a6 <.rdata+0xe6>
   140001b4e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001b52:	90                   	nop
   140001b53:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001b57:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001b5d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001b61:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001b66:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001b6a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001b6f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001b73:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001b77:	b9 02 00 00 00       	mov    ecx,0x2
   140001b7c:	e8 3f 17 00 00       	call   1400032c0 <__acrt_iob_func>
   140001b81:	48 89 c1             	mov    rcx,rax
   140001b84:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001b88:	48 8d 05 29 36 00 00 	lea    rax,[rip+0x3629]        # 1400051b8 <.rdata+0xf8>
   140001b8f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001b96:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001b9c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001ba2:	49 89 d9             	mov    r9,rbx
   140001ba5:	49 89 d0             	mov    r8,rdx
   140001ba8:	48 89 c2             	mov    rdx,rax
   140001bab:	e8 a8 17 00 00       	call   140003358 <fprintf>
   140001bb0:	b8 00 00 00 00       	mov    eax,0x0
   140001bb5:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001bb9:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001bbd:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001bc2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001bc9:	5b                   	pop    rbx
   140001bca:	5d                   	pop    rbp
   140001bcb:	c3                   	ret
   140001bcc:	90                   	nop
   140001bcd:	90                   	nop
   140001bce:	90                   	nop
   140001bcf:	90                   	nop

0000000140001bd0 <__report_error>:
   140001bd0:	55                   	push   rbp
   140001bd1:	53                   	push   rbx
   140001bd2:	48 83 ec 38          	sub    rsp,0x38
   140001bd6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001bdb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001bdf:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001be3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001be7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001beb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001bef:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001bf3:	b9 02 00 00 00       	mov    ecx,0x2
   140001bf8:	e8 c3 16 00 00       	call   1400032c0 <__acrt_iob_func>
   140001bfd:	48 89 c1             	mov    rcx,rax
   140001c00:	48 8d 05 e9 35 00 00 	lea    rax,[rip+0x35e9]        # 1400051f0 <.rdata>
   140001c07:	48 89 c2             	mov    rdx,rax
   140001c0a:	e8 49 17 00 00       	call   140003358 <fprintf>
   140001c0f:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001c13:	b9 02 00 00 00       	mov    ecx,0x2
   140001c18:	e8 a3 16 00 00       	call   1400032c0 <__acrt_iob_func>
   140001c1d:	48 89 c1             	mov    rcx,rax
   140001c20:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001c24:	49 89 d8             	mov    r8,rbx
   140001c27:	48 89 c2             	mov    rdx,rax
   140001c2a:	e8 71 17 00 00       	call   1400033a0 <vfprintf>
   140001c2f:	e8 04 17 00 00       	call   140003338 <abort>
   140001c34:	90                   	nop

0000000140001c35 <mark_section_writable>:
   140001c35:	55                   	push   rbp
   140001c36:	48 89 e5             	mov    rbp,rsp
   140001c39:	48 83 ec 60          	sub    rsp,0x60
   140001c3d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001c41:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001c48:	e9 82 00 00 00       	jmp    140001ccf <mark_section_writable+0x9a>
   140001c4d:	48 8b 0d 8c 74 00 00 	mov    rcx,QWORD PTR [rip+0x748c]        # 1400090e0 <the_secs>
   140001c54:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c57:	48 63 d0             	movsxd rdx,eax
   140001c5a:	48 89 d0             	mov    rax,rdx
   140001c5d:	48 c1 e0 02          	shl    rax,0x2
   140001c61:	48 01 d0             	add    rax,rdx
   140001c64:	48 c1 e0 03          	shl    rax,0x3
   140001c68:	48 01 c8             	add    rax,rcx
   140001c6b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001c6f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001c73:	72 56                	jb     140001ccb <mark_section_writable+0x96>
   140001c75:	48 8b 0d 64 74 00 00 	mov    rcx,QWORD PTR [rip+0x7464]        # 1400090e0 <the_secs>
   140001c7c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c7f:	48 63 d0             	movsxd rdx,eax
   140001c82:	48 89 d0             	mov    rax,rdx
   140001c85:	48 c1 e0 02          	shl    rax,0x2
   140001c89:	48 01 d0             	add    rax,rdx
   140001c8c:	48 c1 e0 03          	shl    rax,0x3
   140001c90:	48 01 c8             	add    rax,rcx
   140001c93:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001c97:	4c 8b 05 42 74 00 00 	mov    r8,QWORD PTR [rip+0x7442]        # 1400090e0 <the_secs>
   140001c9e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ca1:	48 63 d0             	movsxd rdx,eax
   140001ca4:	48 89 d0             	mov    rax,rdx
   140001ca7:	48 c1 e0 02          	shl    rax,0x2
   140001cab:	48 01 d0             	add    rax,rdx
   140001cae:	48 c1 e0 03          	shl    rax,0x3
   140001cb2:	4c 01 c0             	add    rax,r8
   140001cb5:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001cb9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001cbc:	89 c0                	mov    eax,eax
   140001cbe:	48 01 c8             	add    rax,rcx
   140001cc1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001cc5:	0f 82 41 02 00 00    	jb     140001f0c <mark_section_writable+0x2d7>
   140001ccb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001ccf:	8b 05 13 74 00 00    	mov    eax,DWORD PTR [rip+0x7413]        # 1400090e8 <maxSections>
   140001cd5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001cd8:	0f 8c 6f ff ff ff    	jl     140001c4d <mark_section_writable+0x18>
   140001cde:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001ce2:	48 89 c1             	mov    rcx,rax
   140001ce5:	e8 c1 11 00 00       	call   140002eab <__mingw_GetSectionForAddress>
   140001cea:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001cee:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001cf3:	75 13                	jne    140001d08 <mark_section_writable+0xd3>
   140001cf5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001cf9:	48 8d 0d 10 35 00 00 	lea    rcx,[rip+0x3510]        # 140005210 <.rdata+0x20>
   140001d00:	48 89 c2             	mov    rdx,rax
   140001d03:	e8 c8 fe ff ff       	call   140001bd0 <__report_error>
   140001d08:	48 8b 0d d1 73 00 00 	mov    rcx,QWORD PTR [rip+0x73d1]        # 1400090e0 <the_secs>
   140001d0f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d12:	48 63 d0             	movsxd rdx,eax
   140001d15:	48 89 d0             	mov    rax,rdx
   140001d18:	48 c1 e0 02          	shl    rax,0x2
   140001d1c:	48 01 d0             	add    rax,rdx
   140001d1f:	48 c1 e0 03          	shl    rax,0x3
   140001d23:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d27:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001d2b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001d2f:	48 8b 0d aa 73 00 00 	mov    rcx,QWORD PTR [rip+0x73aa]        # 1400090e0 <the_secs>
   140001d36:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d39:	48 63 d0             	movsxd rdx,eax
   140001d3c:	48 89 d0             	mov    rax,rdx
   140001d3f:	48 c1 e0 02          	shl    rax,0x2
   140001d43:	48 01 d0             	add    rax,rdx
   140001d46:	48 c1 e0 03          	shl    rax,0x3
   140001d4a:	48 01 c8             	add    rax,rcx
   140001d4d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001d53:	e8 9f 12 00 00       	call   140002ff7 <_GetPEImageBase>
   140001d58:	48 89 c1             	mov    rcx,rax
   140001d5b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001d5f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001d62:	41 89 c1             	mov    r9d,eax
   140001d65:	4c 8b 05 74 73 00 00 	mov    r8,QWORD PTR [rip+0x7374]        # 1400090e0 <the_secs>
   140001d6c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d6f:	48 63 d0             	movsxd rdx,eax
   140001d72:	48 89 d0             	mov    rax,rdx
   140001d75:	48 c1 e0 02          	shl    rax,0x2
   140001d79:	48 01 d0             	add    rax,rdx
   140001d7c:	48 c1 e0 03          	shl    rax,0x3
   140001d80:	4c 01 c0             	add    rax,r8
   140001d83:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001d87:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001d8b:	48 8b 0d 4e 73 00 00 	mov    rcx,QWORD PTR [rip+0x734e]        # 1400090e0 <the_secs>
   140001d92:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d95:	48 63 d0             	movsxd rdx,eax
   140001d98:	48 89 d0             	mov    rax,rdx
   140001d9b:	48 c1 e0 02          	shl    rax,0x2
   140001d9f:	48 01 d0             	add    rax,rdx
   140001da2:	48 c1 e0 03          	shl    rax,0x3
   140001da6:	48 01 c8             	add    rax,rcx
   140001da9:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001dad:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001db1:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001db7:	48 89 c1             	mov    rcx,rax
   140001dba:	48 8b 05 ff 84 00 00 	mov    rax,QWORD PTR [rip+0x84ff]        # 14000a2c0 <__imp_VirtualQuery>
   140001dc1:	ff d0                	call   rax
   140001dc3:	48 85 c0             	test   rax,rax
   140001dc6:	75 3f                	jne    140001e07 <mark_section_writable+0x1d2>
   140001dc8:	48 8b 0d 11 73 00 00 	mov    rcx,QWORD PTR [rip+0x7311]        # 1400090e0 <the_secs>
   140001dcf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001dd2:	48 63 d0             	movsxd rdx,eax
   140001dd5:	48 89 d0             	mov    rax,rdx
   140001dd8:	48 c1 e0 02          	shl    rax,0x2
   140001ddc:	48 01 d0             	add    rax,rdx
   140001ddf:	48 c1 e0 03          	shl    rax,0x3
   140001de3:	48 01 c8             	add    rax,rcx
   140001de6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001dea:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001dee:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001df1:	89 c1                	mov    ecx,eax
   140001df3:	48 8d 05 36 34 00 00 	lea    rax,[rip+0x3436]        # 140005230 <.rdata+0x40>
   140001dfa:	49 89 d0             	mov    r8,rdx
   140001dfd:	89 ca                	mov    edx,ecx
   140001dff:	48 89 c1             	mov    rcx,rax
   140001e02:	e8 c9 fd ff ff       	call   140001bd0 <__report_error>
   140001e07:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001e0a:	83 f8 40             	cmp    eax,0x40
   140001e0d:	0f 84 e8 00 00 00    	je     140001efb <mark_section_writable+0x2c6>
   140001e13:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001e16:	83 f8 04             	cmp    eax,0x4
   140001e19:	0f 84 dc 00 00 00    	je     140001efb <mark_section_writable+0x2c6>
   140001e1f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001e22:	3d 80 00 00 00       	cmp    eax,0x80
   140001e27:	0f 84 ce 00 00 00    	je     140001efb <mark_section_writable+0x2c6>
   140001e2d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001e30:	83 f8 08             	cmp    eax,0x8
   140001e33:	0f 84 c2 00 00 00    	je     140001efb <mark_section_writable+0x2c6>
   140001e39:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001e3c:	83 f8 02             	cmp    eax,0x2
   140001e3f:	75 09                	jne    140001e4a <mark_section_writable+0x215>
   140001e41:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001e48:	eb 07                	jmp    140001e51 <mark_section_writable+0x21c>
   140001e4a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001e51:	48 8b 0d 88 72 00 00 	mov    rcx,QWORD PTR [rip+0x7288]        # 1400090e0 <the_secs>
   140001e58:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e5b:	48 63 d0             	movsxd rdx,eax
   140001e5e:	48 89 d0             	mov    rax,rdx
   140001e61:	48 c1 e0 02          	shl    rax,0x2
   140001e65:	48 01 d0             	add    rax,rdx
   140001e68:	48 c1 e0 03          	shl    rax,0x3
   140001e6c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001e70:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001e74:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001e78:	48 8b 0d 61 72 00 00 	mov    rcx,QWORD PTR [rip+0x7261]        # 1400090e0 <the_secs>
   140001e7f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e82:	48 63 d0             	movsxd rdx,eax
   140001e85:	48 89 d0             	mov    rax,rdx
   140001e88:	48 c1 e0 02          	shl    rax,0x2
   140001e8c:	48 01 d0             	add    rax,rdx
   140001e8f:	48 c1 e0 03          	shl    rax,0x3
   140001e93:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001e97:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001e9b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001e9f:	48 8b 0d 3a 72 00 00 	mov    rcx,QWORD PTR [rip+0x723a]        # 1400090e0 <the_secs>
   140001ea6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ea9:	48 63 d0             	movsxd rdx,eax
   140001eac:	48 89 d0             	mov    rax,rdx
   140001eaf:	48 c1 e0 02          	shl    rax,0x2
   140001eb3:	48 01 d0             	add    rax,rdx
   140001eb6:	48 c1 e0 03          	shl    rax,0x3
   140001eba:	48 01 c8             	add    rax,rcx
   140001ebd:	49 89 c0             	mov    r8,rax
   140001ec0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001ec4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001ec8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001ecb:	4d 89 c1             	mov    r9,r8
   140001ece:	41 89 c8             	mov    r8d,ecx
   140001ed1:	48 89 c1             	mov    rcx,rax
   140001ed4:	48 8b 05 dd 83 00 00 	mov    rax,QWORD PTR [rip+0x83dd]        # 14000a2b8 <__imp_VirtualProtect>
   140001edb:	ff d0                	call   rax
   140001edd:	85 c0                	test   eax,eax
   140001edf:	75 1a                	jne    140001efb <mark_section_writable+0x2c6>
   140001ee1:	48 8b 05 88 83 00 00 	mov    rax,QWORD PTR [rip+0x8388]        # 14000a270 <__imp_GetLastError>
   140001ee8:	ff d0                	call   rax
   140001eea:	89 c2                	mov    edx,eax
   140001eec:	48 8d 05 75 33 00 00 	lea    rax,[rip+0x3375]        # 140005268 <.rdata+0x78>
   140001ef3:	48 89 c1             	mov    rcx,rax
   140001ef6:	e8 d5 fc ff ff       	call   140001bd0 <__report_error>
   140001efb:	8b 05 e7 71 00 00    	mov    eax,DWORD PTR [rip+0x71e7]        # 1400090e8 <maxSections>
   140001f01:	83 c0 01             	add    eax,0x1
   140001f04:	89 05 de 71 00 00    	mov    DWORD PTR [rip+0x71de],eax        # 1400090e8 <maxSections>
   140001f0a:	eb 01                	jmp    140001f0d <mark_section_writable+0x2d8>
   140001f0c:	90                   	nop
   140001f0d:	48 83 c4 60          	add    rsp,0x60
   140001f11:	5d                   	pop    rbp
   140001f12:	c3                   	ret

0000000140001f13 <restore_modified_sections>:
   140001f13:	55                   	push   rbp
   140001f14:	48 89 e5             	mov    rbp,rsp
   140001f17:	48 83 ec 30          	sub    rsp,0x30
   140001f1b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001f22:	e9 ad 00 00 00       	jmp    140001fd4 <restore_modified_sections+0xc1>
   140001f27:	48 8b 0d b2 71 00 00 	mov    rcx,QWORD PTR [rip+0x71b2]        # 1400090e0 <the_secs>
   140001f2e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f31:	48 63 d0             	movsxd rdx,eax
   140001f34:	48 89 d0             	mov    rax,rdx
   140001f37:	48 c1 e0 02          	shl    rax,0x2
   140001f3b:	48 01 d0             	add    rax,rdx
   140001f3e:	48 c1 e0 03          	shl    rax,0x3
   140001f42:	48 01 c8             	add    rax,rcx
   140001f45:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f47:	85 c0                	test   eax,eax
   140001f49:	0f 84 80 00 00 00    	je     140001fcf <restore_modified_sections+0xbc>
   140001f4f:	48 8b 0d 8a 71 00 00 	mov    rcx,QWORD PTR [rip+0x718a]        # 1400090e0 <the_secs>
   140001f56:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f59:	48 63 d0             	movsxd rdx,eax
   140001f5c:	48 89 d0             	mov    rax,rdx
   140001f5f:	48 c1 e0 02          	shl    rax,0x2
   140001f63:	48 01 d0             	add    rax,rdx
   140001f66:	48 c1 e0 03          	shl    rax,0x3
   140001f6a:	48 01 c8             	add    rax,rcx
   140001f6d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001f70:	48 8b 0d 69 71 00 00 	mov    rcx,QWORD PTR [rip+0x7169]        # 1400090e0 <the_secs>
   140001f77:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f7a:	48 63 d0             	movsxd rdx,eax
   140001f7d:	48 89 d0             	mov    rax,rdx
   140001f80:	48 c1 e0 02          	shl    rax,0x2
   140001f84:	48 01 d0             	add    rax,rdx
   140001f87:	48 c1 e0 03          	shl    rax,0x3
   140001f8b:	48 01 c8             	add    rax,rcx
   140001f8e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001f92:	4c 8b 05 47 71 00 00 	mov    r8,QWORD PTR [rip+0x7147]        # 1400090e0 <the_secs>
   140001f99:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001f9c:	48 63 d0             	movsxd rdx,eax
   140001f9f:	48 89 d0             	mov    rax,rdx
   140001fa2:	48 c1 e0 02          	shl    rax,0x2
   140001fa6:	48 01 d0             	add    rax,rdx
   140001fa9:	48 c1 e0 03          	shl    rax,0x3
   140001fad:	4c 01 c0             	add    rax,r8
   140001fb0:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001fb4:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001fb8:	49 89 d1             	mov    r9,rdx
   140001fbb:	45 89 d0             	mov    r8d,r10d
   140001fbe:	48 89 ca             	mov    rdx,rcx
   140001fc1:	48 89 c1             	mov    rcx,rax
   140001fc4:	48 8b 05 ed 82 00 00 	mov    rax,QWORD PTR [rip+0x82ed]        # 14000a2b8 <__imp_VirtualProtect>
   140001fcb:	ff d0                	call   rax
   140001fcd:	eb 01                	jmp    140001fd0 <restore_modified_sections+0xbd>
   140001fcf:	90                   	nop
   140001fd0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001fd4:	8b 05 0e 71 00 00    	mov    eax,DWORD PTR [rip+0x710e]        # 1400090e8 <maxSections>
   140001fda:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001fdd:	0f 8c 44 ff ff ff    	jl     140001f27 <restore_modified_sections+0x14>
   140001fe3:	90                   	nop
   140001fe4:	90                   	nop
   140001fe5:	48 83 c4 30          	add    rsp,0x30
   140001fe9:	5d                   	pop    rbp
   140001fea:	c3                   	ret

0000000140001feb <__write_memory>:
   140001feb:	55                   	push   rbp
   140001fec:	48 89 e5             	mov    rbp,rsp
   140001fef:	48 83 ec 20          	sub    rsp,0x20
   140001ff3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001ff7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001ffb:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001fff:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140002004:	74 25                	je     14000202b <__write_memory+0x40>
   140002006:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000200a:	48 89 c1             	mov    rcx,rax
   14000200d:	e8 23 fc ff ff       	call   140001c35 <mark_section_writable>
   140002012:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140002016:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   14000201a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000201e:	49 89 c8             	mov    r8,rcx
   140002021:	48 89 c1             	mov    rcx,rax
   140002024:	e8 47 13 00 00       	call   140003370 <memcpy>
   140002029:	eb 01                	jmp    14000202c <__write_memory+0x41>
   14000202b:	90                   	nop
   14000202c:	48 83 c4 20          	add    rsp,0x20
   140002030:	5d                   	pop    rbp
   140002031:	c3                   	ret

0000000140002032 <do_pseudo_reloc>:
   140002032:	55                   	push   rbp
   140002033:	48 89 e5             	mov    rbp,rsp
   140002036:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   14000203a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000203e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002042:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002046:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000204a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   14000204e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002052:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002056:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000205a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   14000205f:	0f 8e 44 03 00 00    	jle    1400023a9 <do_pseudo_reloc+0x377>
   140002065:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   14000206a:	7e 25                	jle    140002091 <do_pseudo_reloc+0x5f>
   14000206c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002070:	8b 00                	mov    eax,DWORD PTR [rax]
   140002072:	85 c0                	test   eax,eax
   140002074:	75 1b                	jne    140002091 <do_pseudo_reloc+0x5f>
   140002076:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000207a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000207d:	85 c0                	test   eax,eax
   14000207f:	75 10                	jne    140002091 <do_pseudo_reloc+0x5f>
   140002081:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002085:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002088:	85 c0                	test   eax,eax
   14000208a:	75 05                	jne    140002091 <do_pseudo_reloc+0x5f>
   14000208c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140002091:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002095:	8b 00                	mov    eax,DWORD PTR [rax]
   140002097:	85 c0                	test   eax,eax
   140002099:	75 0b                	jne    1400020a6 <do_pseudo_reloc+0x74>
   14000209b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000209f:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400020a2:	85 c0                	test   eax,eax
   1400020a4:	74 59                	je     1400020ff <do_pseudo_reloc+0xcd>
   1400020a6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400020aa:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400020ae:	eb 40                	jmp    1400020f0 <do_pseudo_reloc+0xbe>
   1400020b0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400020b4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400020b7:	89 c2                	mov    edx,eax
   1400020b9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400020bd:	48 01 d0             	add    rax,rdx
   1400020c0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400020c4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020c8:	8b 10                	mov    edx,DWORD PTR [rax]
   1400020ca:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400020ce:	8b 00                	mov    eax,DWORD PTR [rax]
   1400020d0:	01 d0                	add    eax,edx
   1400020d2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   1400020d5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020d9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   1400020dd:	41 b8 04 00 00 00    	mov    r8d,0x4
   1400020e3:	48 89 c1             	mov    rcx,rax
   1400020e6:	e8 00 ff ff ff       	call   140001feb <__write_memory>
   1400020eb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   1400020f0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400020f4:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400020f8:	72 b6                	jb     1400020b0 <do_pseudo_reloc+0x7e>
   1400020fa:	e9 ab 02 00 00       	jmp    1400023aa <do_pseudo_reloc+0x378>
   1400020ff:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002103:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002106:	83 f8 01             	cmp    eax,0x1
   140002109:	74 18                	je     140002123 <do_pseudo_reloc+0xf1>
   14000210b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000210f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002112:	89 c2                	mov    edx,eax
   140002114:	48 8d 05 75 31 00 00 	lea    rax,[rip+0x3175]        # 140005290 <.rdata+0xa0>
   14000211b:	48 89 c1             	mov    rcx,rax
   14000211e:	e8 ad fa ff ff       	call   140001bd0 <__report_error>
   140002123:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002127:	48 83 c0 0c          	add    rax,0xc
   14000212b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000212f:	e9 65 02 00 00       	jmp    140002399 <do_pseudo_reloc+0x367>
   140002134:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002138:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000213b:	89 c2                	mov    edx,eax
   14000213d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002141:	48 01 d0             	add    rax,rdx
   140002144:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002148:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000214c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000214e:	89 c2                	mov    edx,eax
   140002150:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002154:	48 01 d0             	add    rax,rdx
   140002157:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000215b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000215f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002162:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002166:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000216a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000216d:	0f b6 c0             	movzx  eax,al
   140002170:	83 f8 40             	cmp    eax,0x40
   140002173:	0f 84 b6 00 00 00    	je     14000222f <do_pseudo_reloc+0x1fd>
   140002179:	83 f8 40             	cmp    eax,0x40
   14000217c:	0f 87 ba 00 00 00    	ja     14000223c <do_pseudo_reloc+0x20a>
   140002182:	83 f8 20             	cmp    eax,0x20
   140002185:	74 77                	je     1400021fe <do_pseudo_reloc+0x1cc>
   140002187:	83 f8 20             	cmp    eax,0x20
   14000218a:	0f 87 ac 00 00 00    	ja     14000223c <do_pseudo_reloc+0x20a>
   140002190:	83 f8 08             	cmp    eax,0x8
   140002193:	74 0a                	je     14000219f <do_pseudo_reloc+0x16d>
   140002195:	83 f8 10             	cmp    eax,0x10
   140002198:	74 38                	je     1400021d2 <do_pseudo_reloc+0x1a0>
   14000219a:	e9 9d 00 00 00       	jmp    14000223c <do_pseudo_reloc+0x20a>
   14000219f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400021a3:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400021a6:	0f b6 c0             	movzx  eax,al
   1400021a9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400021ad:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021b1:	25 80 00 00 00       	and    eax,0x80
   1400021b6:	48 85 c0             	test   rax,rax
   1400021b9:	0f 84 9d 00 00 00    	je     14000225c <do_pseudo_reloc+0x22a>
   1400021bf:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021c3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400021c9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400021cd:	e9 8a 00 00 00       	jmp    14000225c <do_pseudo_reloc+0x22a>
   1400021d2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400021d6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400021d9:	0f b7 c0             	movzx  eax,ax
   1400021dc:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400021e0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021e4:	25 00 80 00 00       	and    eax,0x8000
   1400021e9:	48 85 c0             	test   rax,rax
   1400021ec:	74 71                	je     14000225f <do_pseudo_reloc+0x22d>
   1400021ee:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021f2:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   1400021f8:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400021fc:	eb 61                	jmp    14000225f <do_pseudo_reloc+0x22d>
   1400021fe:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002202:	8b 00                	mov    eax,DWORD PTR [rax]
   140002204:	89 c0                	mov    eax,eax
   140002206:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000220a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000220e:	25 00 00 00 80       	and    eax,0x80000000
   140002213:	48 85 c0             	test   rax,rax
   140002216:	74 4a                	je     140002262 <do_pseudo_reloc+0x230>
   140002218:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000221c:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002223:	ff ff ff 
   140002226:	48 09 d0             	or     rax,rdx
   140002229:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000222d:	eb 33                	jmp    140002262 <do_pseudo_reloc+0x230>
   14000222f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002233:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002236:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000223a:	eb 27                	jmp    140002263 <do_pseudo_reloc+0x231>
   14000223c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002243:	00 
   140002244:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002248:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000224b:	0f b6 c0             	movzx  eax,al
   14000224e:	48 8d 0d 73 30 00 00 	lea    rcx,[rip+0x3073]        # 1400052c8 <.rdata+0xd8>
   140002255:	89 c2                	mov    edx,eax
   140002257:	e8 74 f9 ff ff       	call   140001bd0 <__report_error>
   14000225c:	90                   	nop
   14000225d:	eb 04                	jmp    140002263 <do_pseudo_reloc+0x231>
   14000225f:	90                   	nop
   140002260:	eb 01                	jmp    140002263 <do_pseudo_reloc+0x231>
   140002262:	90                   	nop
   140002263:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002267:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000226b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000226d:	89 c2                	mov    edx,eax
   14000226f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002273:	48 01 c2             	add    rdx,rax
   140002276:	48 89 c8             	mov    rax,rcx
   140002279:	48 29 d0             	sub    rax,rdx
   14000227c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002280:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002284:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002288:	48 01 d0             	add    rax,rdx
   14000228b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000228f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002293:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002296:	25 ff 00 00 00       	and    eax,0xff
   14000229b:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000229e:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   1400022a2:	77 67                	ja     14000230b <do_pseudo_reloc+0x2d9>
   1400022a4:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400022a7:	ba 01 00 00 00       	mov    edx,0x1
   1400022ac:	89 c1                	mov    ecx,eax
   1400022ae:	48 d3 e2             	shl    rdx,cl
   1400022b1:	48 89 d0             	mov    rax,rdx
   1400022b4:	48 83 e8 01          	sub    rax,0x1
   1400022b8:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400022bc:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400022bf:	83 e8 01             	sub    eax,0x1
   1400022c2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400022c9:	89 c1                	mov    ecx,eax
   1400022cb:	48 d3 e2             	shl    rdx,cl
   1400022ce:	48 89 d0             	mov    rax,rdx
   1400022d1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400022d5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400022d9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400022dd:	7c 0a                	jl     1400022e9 <do_pseudo_reloc+0x2b7>
   1400022df:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400022e3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400022e7:	7e 22                	jle    14000230b <do_pseudo_reloc+0x2d9>
   1400022e9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400022ed:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   1400022f1:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   1400022f5:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400022f8:	48 8d 0d f9 2f 00 00 	lea    rcx,[rip+0x2ff9]        # 1400052f8 <.rdata+0x108>
   1400022ff:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140002304:	89 c2                	mov    edx,eax
   140002306:	e8 c5 f8 ff ff       	call   140001bd0 <__report_error>
   14000230b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000230f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002312:	0f b6 c0             	movzx  eax,al
   140002315:	83 f8 40             	cmp    eax,0x40
   140002318:	74 63                	je     14000237d <do_pseudo_reloc+0x34b>
   14000231a:	83 f8 40             	cmp    eax,0x40
   14000231d:	77 75                	ja     140002394 <do_pseudo_reloc+0x362>
   14000231f:	83 f8 20             	cmp    eax,0x20
   140002322:	74 41                	je     140002365 <do_pseudo_reloc+0x333>
   140002324:	83 f8 20             	cmp    eax,0x20
   140002327:	77 6b                	ja     140002394 <do_pseudo_reloc+0x362>
   140002329:	83 f8 08             	cmp    eax,0x8
   14000232c:	74 07                	je     140002335 <do_pseudo_reloc+0x303>
   14000232e:	83 f8 10             	cmp    eax,0x10
   140002331:	74 1a                	je     14000234d <do_pseudo_reloc+0x31b>
   140002333:	eb 5f                	jmp    140002394 <do_pseudo_reloc+0x362>
   140002335:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002339:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000233d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002343:	48 89 c1             	mov    rcx,rax
   140002346:	e8 a0 fc ff ff       	call   140001feb <__write_memory>
   14000234b:	eb 47                	jmp    140002394 <do_pseudo_reloc+0x362>
   14000234d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002351:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002355:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000235b:	48 89 c1             	mov    rcx,rax
   14000235e:	e8 88 fc ff ff       	call   140001feb <__write_memory>
   140002363:	eb 2f                	jmp    140002394 <do_pseudo_reloc+0x362>
   140002365:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002369:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000236d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002373:	48 89 c1             	mov    rcx,rax
   140002376:	e8 70 fc ff ff       	call   140001feb <__write_memory>
   14000237b:	eb 17                	jmp    140002394 <do_pseudo_reloc+0x362>
   14000237d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002381:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002385:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000238b:	48 89 c1             	mov    rcx,rax
   14000238e:	e8 58 fc ff ff       	call   140001feb <__write_memory>
   140002393:	90                   	nop
   140002394:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   140002399:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000239d:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400023a1:	0f 82 8d fd ff ff    	jb     140002134 <do_pseudo_reloc+0x102>
   1400023a7:	eb 01                	jmp    1400023aa <do_pseudo_reloc+0x378>
   1400023a9:	90                   	nop
   1400023aa:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   1400023ae:	5d                   	pop    rbp
   1400023af:	c3                   	ret

00000001400023b0 <_pei386_runtime_relocator>:
   1400023b0:	55                   	push   rbp
   1400023b1:	48 89 e5             	mov    rbp,rsp
   1400023b4:	48 83 ec 30          	sub    rsp,0x30
   1400023b8:	8b 05 2e 6d 00 00    	mov    eax,DWORD PTR [rip+0x6d2e]        # 1400090ec <was_init.0>
   1400023be:	85 c0                	test   eax,eax
   1400023c0:	0f 85 88 00 00 00    	jne    14000244e <_pei386_runtime_relocator+0x9e>
   1400023c6:	8b 05 20 6d 00 00    	mov    eax,DWORD PTR [rip+0x6d20]        # 1400090ec <was_init.0>
   1400023cc:	83 c0 01             	add    eax,0x1
   1400023cf:	89 05 17 6d 00 00    	mov    DWORD PTR [rip+0x6d17],eax        # 1400090ec <was_init.0>
   1400023d5:	e8 21 0b 00 00       	call   140002efb <__mingw_GetSectionCount>
   1400023da:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400023dd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400023e0:	48 63 d0             	movsxd rdx,eax
   1400023e3:	48 89 d0             	mov    rax,rdx
   1400023e6:	48 c1 e0 02          	shl    rax,0x2
   1400023ea:	48 01 d0             	add    rax,rdx
   1400023ed:	48 c1 e0 03          	shl    rax,0x3
   1400023f1:	48 83 c0 0f          	add    rax,0xf
   1400023f5:	48 c1 e8 04          	shr    rax,0x4
   1400023f9:	48 c1 e0 04          	shl    rax,0x4
   1400023fd:	e8 8e 0d 00 00       	call   140003190 <___chkstk_ms>
   140002402:	48 29 c4             	sub    rsp,rax
   140002405:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   14000240a:	48 83 c0 0f          	add    rax,0xf
   14000240e:	48 c1 e8 04          	shr    rax,0x4
   140002412:	48 c1 e0 04          	shl    rax,0x4
   140002416:	48 89 05 c3 6c 00 00 	mov    QWORD PTR [rip+0x6cc3],rax        # 1400090e0 <the_secs>
   14000241d:	c7 05 c1 6c 00 00 00 	mov    DWORD PTR [rip+0x6cc1],0x0        # 1400090e8 <maxSections>
   140002424:	00 00 00 
   140002427:	48 8b 0d 52 2f 00 00 	mov    rcx,QWORD PTR [rip+0x2f52]        # 140005380 <.refptr.__ImageBase>
   14000242e:	48 8b 15 5b 2f 00 00 	mov    rdx,QWORD PTR [rip+0x2f5b]        # 140005390 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002435:	48 8b 05 64 2f 00 00 	mov    rax,QWORD PTR [rip+0x2f64]        # 1400053a0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000243c:	49 89 c8             	mov    r8,rcx
   14000243f:	48 89 c1             	mov    rcx,rax
   140002442:	e8 eb fb ff ff       	call   140002032 <do_pseudo_reloc>
   140002447:	e8 c7 fa ff ff       	call   140001f13 <restore_modified_sections>
   14000244c:	eb 01                	jmp    14000244f <_pei386_runtime_relocator+0x9f>
   14000244e:	90                   	nop
   14000244f:	48 89 ec             	mov    rsp,rbp
   140002452:	5d                   	pop    rbp
   140002453:	c3                   	ret
   140002454:	90                   	nop
   140002455:	90                   	nop
   140002456:	90                   	nop
   140002457:	90                   	nop
   140002458:	90                   	nop
   140002459:	90                   	nop
   14000245a:	90                   	nop
   14000245b:	90                   	nop
   14000245c:	90                   	nop
   14000245d:	90                   	nop
   14000245e:	90                   	nop
   14000245f:	90                   	nop

0000000140002460 <__mingw_raise_matherr>:
   140002460:	55                   	push   rbp
   140002461:	48 89 e5             	mov    rbp,rsp
   140002464:	48 83 ec 50          	sub    rsp,0x50
   140002468:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000246b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000246f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002474:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002479:	48 8b 05 70 6c 00 00 	mov    rax,QWORD PTR [rip+0x6c70]        # 1400090f0 <stUserMathErr>
   140002480:	48 85 c0             	test   rax,rax
   140002483:	74 3e                	je     1400024c3 <__mingw_raise_matherr+0x63>
   140002485:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002488:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000248b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000248f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002493:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140002498:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   14000249d:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   1400024a2:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   1400024a7:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   1400024ac:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   1400024b1:	48 8b 15 38 6c 00 00 	mov    rdx,QWORD PTR [rip+0x6c38]        # 1400090f0 <stUserMathErr>
   1400024b8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   1400024bc:	48 89 c1             	mov    rcx,rax
   1400024bf:	ff d2                	call   rdx
   1400024c1:	eb 01                	jmp    1400024c4 <__mingw_raise_matherr+0x64>
   1400024c3:	90                   	nop
   1400024c4:	48 83 c4 50          	add    rsp,0x50
   1400024c8:	5d                   	pop    rbp
   1400024c9:	c3                   	ret

00000001400024ca <__mingw_setusermatherr>:
   1400024ca:	55                   	push   rbp
   1400024cb:	48 89 e5             	mov    rbp,rsp
   1400024ce:	48 83 ec 20          	sub    rsp,0x20
   1400024d2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400024d6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400024da:	48 89 05 0f 6c 00 00 	mov    QWORD PTR [rip+0x6c0f],rax        # 1400090f0 <stUserMathErr>
   1400024e1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400024e5:	48 89 c1             	mov    rcx,rax
   1400024e8:	e8 23 0e 00 00       	call   140003310 <__setusermatherr>
   1400024ed:	90                   	nop
   1400024ee:	48 83 c4 20          	add    rsp,0x20
   1400024f2:	5d                   	pop    rbp
   1400024f3:	c3                   	ret
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

0000000140002500 <__mingw_SEH_error_handler>:
   140002500:	55                   	push   rbp
   140002501:	48 89 e5             	mov    rbp,rsp
   140002504:	48 83 ec 30          	sub    rsp,0x30
   140002508:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000250c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002510:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002514:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140002518:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   14000251f:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002526:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000252a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000252d:	83 e0 02             	and    eax,0x2
   140002530:	85 c0                	test   eax,eax
   140002532:	74 0a                	je     14000253e <__mingw_SEH_error_handler+0x3e>
   140002534:	b8 01 00 00 00       	mov    eax,0x1
   140002539:	e9 16 02 00 00       	jmp    140002754 <__mingw_SEH_error_handler+0x254>
   14000253e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002542:	8b 00                	mov    eax,DWORD PTR [rax]
   140002544:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002549:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000254e:	75 18                	jne    140002568 <__mingw_SEH_error_handler+0x68>
   140002550:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002554:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002557:	83 e0 01             	and    eax,0x1
   14000255a:	85 c0                	test   eax,eax
   14000255c:	75 0a                	jne    140002568 <__mingw_SEH_error_handler+0x68>
   14000255e:	b8 00 00 00 00       	mov    eax,0x0
   140002563:	e9 ec 01 00 00       	jmp    140002754 <__mingw_SEH_error_handler+0x254>
   140002568:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000256c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000256e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002573:	0f 84 12 01 00 00    	je     14000268b <__mingw_SEH_error_handler+0x18b>
   140002579:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000257e:	0f 87 c3 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   140002584:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002589:	0f 87 b8 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   14000258f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002594:	0f 83 4c 01 00 00    	jae    1400026e6 <__mingw_SEH_error_handler+0x1e6>
   14000259a:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000259f:	0f 84 3a 01 00 00    	je     1400026df <__mingw_SEH_error_handler+0x1df>
   1400025a5:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400025aa:	0f 87 97 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   1400025b0:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400025b5:	0f 84 83 01 00 00    	je     14000273e <__mingw_SEH_error_handler+0x23e>
   1400025bb:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400025c0:	0f 87 81 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   1400025c6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400025cb:	0f 87 76 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   1400025d1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400025d6:	0f 83 03 01 00 00    	jae    1400026df <__mingw_SEH_error_handler+0x1df>
   1400025dc:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400025e1:	0f 84 57 01 00 00    	je     14000273e <__mingw_SEH_error_handler+0x23e>
   1400025e7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400025ec:	0f 87 55 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   1400025f2:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400025f7:	0f 84 8e 00 00 00    	je     14000268b <__mingw_SEH_error_handler+0x18b>
   1400025fd:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002602:	0f 87 3f 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   140002608:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000260d:	0f 84 2b 01 00 00    	je     14000273e <__mingw_SEH_error_handler+0x23e>
   140002613:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002618:	0f 87 29 01 00 00    	ja     140002747 <__mingw_SEH_error_handler+0x247>
   14000261e:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002623:	0f 84 15 01 00 00    	je     14000273e <__mingw_SEH_error_handler+0x23e>
   140002629:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000262e:	0f 85 13 01 00 00    	jne    140002747 <__mingw_SEH_error_handler+0x247>
   140002634:	ba 00 00 00 00       	mov    edx,0x0
   140002639:	b9 0b 00 00 00       	mov    ecx,0xb
   14000263e:	e8 45 0d 00 00       	call   140003388 <signal>
   140002643:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002647:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000264c:	75 1b                	jne    140002669 <__mingw_SEH_error_handler+0x169>
   14000264e:	ba 01 00 00 00       	mov    edx,0x1
   140002653:	b9 0b 00 00 00       	mov    ecx,0xb
   140002658:	e8 2b 0d 00 00       	call   140003388 <signal>
   14000265d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002664:	e9 e1 00 00 00       	jmp    14000274a <__mingw_SEH_error_handler+0x24a>
   140002669:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000266e:	0f 84 d6 00 00 00    	je     14000274a <__mingw_SEH_error_handler+0x24a>
   140002674:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002678:	b9 0b 00 00 00       	mov    ecx,0xb
   14000267d:	ff d0                	call   rax
   14000267f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002686:	e9 bf 00 00 00       	jmp    14000274a <__mingw_SEH_error_handler+0x24a>
   14000268b:	ba 00 00 00 00       	mov    edx,0x0
   140002690:	b9 04 00 00 00       	mov    ecx,0x4
   140002695:	e8 ee 0c 00 00       	call   140003388 <signal>
   14000269a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000269e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400026a3:	75 1b                	jne    1400026c0 <__mingw_SEH_error_handler+0x1c0>
   1400026a5:	ba 01 00 00 00       	mov    edx,0x1
   1400026aa:	b9 04 00 00 00       	mov    ecx,0x4
   1400026af:	e8 d4 0c 00 00       	call   140003388 <signal>
   1400026b4:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400026bb:	e9 8d 00 00 00       	jmp    14000274d <__mingw_SEH_error_handler+0x24d>
   1400026c0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400026c5:	0f 84 82 00 00 00    	je     14000274d <__mingw_SEH_error_handler+0x24d>
   1400026cb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400026cf:	b9 04 00 00 00       	mov    ecx,0x4
   1400026d4:	ff d0                	call   rax
   1400026d6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400026dd:	eb 6e                	jmp    14000274d <__mingw_SEH_error_handler+0x24d>
   1400026df:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400026e6:	ba 00 00 00 00       	mov    edx,0x0
   1400026eb:	b9 08 00 00 00       	mov    ecx,0x8
   1400026f0:	e8 93 0c 00 00       	call   140003388 <signal>
   1400026f5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400026f9:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400026fe:	75 23                	jne    140002723 <__mingw_SEH_error_handler+0x223>
   140002700:	ba 01 00 00 00       	mov    edx,0x1
   140002705:	b9 08 00 00 00       	mov    ecx,0x8
   14000270a:	e8 79 0c 00 00       	call   140003388 <signal>
   14000270f:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002713:	74 05                	je     14000271a <__mingw_SEH_error_handler+0x21a>
   140002715:	e8 a6 05 00 00       	call   140002cc0 <_fpreset>
   14000271a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002721:	eb 2d                	jmp    140002750 <__mingw_SEH_error_handler+0x250>
   140002723:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002728:	74 26                	je     140002750 <__mingw_SEH_error_handler+0x250>
   14000272a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000272e:	b9 08 00 00 00       	mov    ecx,0x8
   140002733:	ff d0                	call   rax
   140002735:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000273c:	eb 12                	jmp    140002750 <__mingw_SEH_error_handler+0x250>
   14000273e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002745:	eb 0a                	jmp    140002751 <__mingw_SEH_error_handler+0x251>
   140002747:	90                   	nop
   140002748:	eb 07                	jmp    140002751 <__mingw_SEH_error_handler+0x251>
   14000274a:	90                   	nop
   14000274b:	eb 04                	jmp    140002751 <__mingw_SEH_error_handler+0x251>
   14000274d:	90                   	nop
   14000274e:	eb 01                	jmp    140002751 <__mingw_SEH_error_handler+0x251>
   140002750:	90                   	nop
   140002751:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002754:	48 83 c4 30          	add    rsp,0x30
   140002758:	5d                   	pop    rbp
   140002759:	c3                   	ret

000000014000275a <_gnu_exception_handler>:
   14000275a:	55                   	push   rbp
   14000275b:	48 89 e5             	mov    rbp,rsp
   14000275e:	48 83 ec 30          	sub    rsp,0x30
   140002762:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002766:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000276d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002774:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002778:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000277b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000277d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002782:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002787:	75 1b                	jne    1400027a4 <_gnu_exception_handler+0x4a>
   140002789:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000278d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002790:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002793:	83 e0 01             	and    eax,0x1
   140002796:	85 c0                	test   eax,eax
   140002798:	75 0a                	jne    1400027a4 <_gnu_exception_handler+0x4a>
   14000279a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000279f:	e9 14 02 00 00       	jmp    1400029b8 <_gnu_exception_handler+0x25e>
   1400027a4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400027a8:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400027ab:	8b 00                	mov    eax,DWORD PTR [rax]
   1400027ad:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400027b2:	0f 84 12 01 00 00    	je     1400028ca <_gnu_exception_handler+0x170>
   1400027b8:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400027bd:	0f 87 c3 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   1400027c3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400027c8:	0f 87 b8 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   1400027ce:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400027d3:	0f 83 4c 01 00 00    	jae    140002925 <_gnu_exception_handler+0x1cb>
   1400027d9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400027de:	0f 84 3a 01 00 00    	je     14000291e <_gnu_exception_handler+0x1c4>
   1400027e4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400027e9:	0f 87 97 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   1400027ef:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400027f4:	0f 84 83 01 00 00    	je     14000297d <_gnu_exception_handler+0x223>
   1400027fa:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400027ff:	0f 87 81 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   140002805:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   14000280a:	0f 87 76 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   140002810:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002815:	0f 83 03 01 00 00    	jae    14000291e <_gnu_exception_handler+0x1c4>
   14000281b:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002820:	0f 84 57 01 00 00    	je     14000297d <_gnu_exception_handler+0x223>
   140002826:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000282b:	0f 87 55 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   140002831:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002836:	0f 84 8e 00 00 00    	je     1400028ca <_gnu_exception_handler+0x170>
   14000283c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002841:	0f 87 3f 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   140002847:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000284c:	0f 84 2b 01 00 00    	je     14000297d <_gnu_exception_handler+0x223>
   140002852:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002857:	0f 87 29 01 00 00    	ja     140002986 <_gnu_exception_handler+0x22c>
   14000285d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002862:	0f 84 15 01 00 00    	je     14000297d <_gnu_exception_handler+0x223>
   140002868:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000286d:	0f 85 13 01 00 00    	jne    140002986 <_gnu_exception_handler+0x22c>
   140002873:	ba 00 00 00 00       	mov    edx,0x0
   140002878:	b9 0b 00 00 00       	mov    ecx,0xb
   14000287d:	e8 06 0b 00 00       	call   140003388 <signal>
   140002882:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002886:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000288b:	75 1b                	jne    1400028a8 <_gnu_exception_handler+0x14e>
   14000288d:	ba 01 00 00 00       	mov    edx,0x1
   140002892:	b9 0b 00 00 00       	mov    ecx,0xb
   140002897:	e8 ec 0a 00 00       	call   140003388 <signal>
   14000289c:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400028a3:	e9 e1 00 00 00       	jmp    140002989 <_gnu_exception_handler+0x22f>
   1400028a8:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400028ad:	0f 84 d6 00 00 00    	je     140002989 <_gnu_exception_handler+0x22f>
   1400028b3:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400028b7:	b9 0b 00 00 00       	mov    ecx,0xb
   1400028bc:	ff d0                	call   rax
   1400028be:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400028c5:	e9 bf 00 00 00       	jmp    140002989 <_gnu_exception_handler+0x22f>
   1400028ca:	ba 00 00 00 00       	mov    edx,0x0
   1400028cf:	b9 04 00 00 00       	mov    ecx,0x4
   1400028d4:	e8 af 0a 00 00       	call   140003388 <signal>
   1400028d9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400028dd:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400028e2:	75 1b                	jne    1400028ff <_gnu_exception_handler+0x1a5>
   1400028e4:	ba 01 00 00 00       	mov    edx,0x1
   1400028e9:	b9 04 00 00 00       	mov    ecx,0x4
   1400028ee:	e8 95 0a 00 00       	call   140003388 <signal>
   1400028f3:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400028fa:	e9 8d 00 00 00       	jmp    14000298c <_gnu_exception_handler+0x232>
   1400028ff:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002904:	0f 84 82 00 00 00    	je     14000298c <_gnu_exception_handler+0x232>
   14000290a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000290e:	b9 04 00 00 00       	mov    ecx,0x4
   140002913:	ff d0                	call   rax
   140002915:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000291c:	eb 6e                	jmp    14000298c <_gnu_exception_handler+0x232>
   14000291e:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002925:	ba 00 00 00 00       	mov    edx,0x0
   14000292a:	b9 08 00 00 00       	mov    ecx,0x8
   14000292f:	e8 54 0a 00 00       	call   140003388 <signal>
   140002934:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002938:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000293d:	75 23                	jne    140002962 <_gnu_exception_handler+0x208>
   14000293f:	ba 01 00 00 00       	mov    edx,0x1
   140002944:	b9 08 00 00 00       	mov    ecx,0x8
   140002949:	e8 3a 0a 00 00       	call   140003388 <signal>
   14000294e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002952:	74 05                	je     140002959 <_gnu_exception_handler+0x1ff>
   140002954:	e8 67 03 00 00       	call   140002cc0 <_fpreset>
   140002959:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002960:	eb 2d                	jmp    14000298f <_gnu_exception_handler+0x235>
   140002962:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002967:	74 26                	je     14000298f <_gnu_exception_handler+0x235>
   140002969:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000296d:	b9 08 00 00 00       	mov    ecx,0x8
   140002972:	ff d0                	call   rax
   140002974:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000297b:	eb 12                	jmp    14000298f <_gnu_exception_handler+0x235>
   14000297d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002984:	eb 0a                	jmp    140002990 <_gnu_exception_handler+0x236>
   140002986:	90                   	nop
   140002987:	eb 07                	jmp    140002990 <_gnu_exception_handler+0x236>
   140002989:	90                   	nop
   14000298a:	eb 04                	jmp    140002990 <_gnu_exception_handler+0x236>
   14000298c:	90                   	nop
   14000298d:	eb 01                	jmp    140002990 <_gnu_exception_handler+0x236>
   14000298f:	90                   	nop
   140002990:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002994:	75 1f                	jne    1400029b5 <_gnu_exception_handler+0x25b>
   140002996:	48 8b 05 73 67 00 00 	mov    rax,QWORD PTR [rip+0x6773]        # 140009110 <__mingw_oldexcpt_handler>
   14000299d:	48 85 c0             	test   rax,rax
   1400029a0:	74 13                	je     1400029b5 <_gnu_exception_handler+0x25b>
   1400029a2:	48 8b 15 67 67 00 00 	mov    rdx,QWORD PTR [rip+0x6767]        # 140009110 <__mingw_oldexcpt_handler>
   1400029a9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400029ad:	48 89 c1             	mov    rcx,rax
   1400029b0:	ff d2                	call   rdx
   1400029b2:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400029b5:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400029b8:	48 83 c4 30          	add    rsp,0x30
   1400029bc:	5d                   	pop    rbp
   1400029bd:	c3                   	ret
   1400029be:	90                   	nop
   1400029bf:	90                   	nop

00000001400029c0 <___w64_mingwthr_add_key_dtor>:
   1400029c0:	55                   	push   rbp
   1400029c1:	48 89 e5             	mov    rbp,rsp
   1400029c4:	48 83 ec 30          	sub    rsp,0x30
   1400029c8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400029cb:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400029cf:	8b 05 73 67 00 00    	mov    eax,DWORD PTR [rip+0x6773]        # 140009148 <__mingwthr_cs_init>
   1400029d5:	85 c0                	test   eax,eax
   1400029d7:	75 07                	jne    1400029e0 <___w64_mingwthr_add_key_dtor+0x20>
   1400029d9:	b8 00 00 00 00       	mov    eax,0x0
   1400029de:	eb 7b                	jmp    140002a5b <___w64_mingwthr_add_key_dtor+0x9b>
   1400029e0:	ba 18 00 00 00       	mov    edx,0x18
   1400029e5:	b9 01 00 00 00       	mov    ecx,0x1
   1400029ea:	e8 51 09 00 00       	call   140003340 <calloc>
   1400029ef:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400029f3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400029f8:	75 07                	jne    140002a01 <___w64_mingwthr_add_key_dtor+0x41>
   1400029fa:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400029ff:	eb 5a                	jmp    140002a5b <___w64_mingwthr_add_key_dtor+0x9b>
   140002a01:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a05:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140002a08:	89 10                	mov    DWORD PTR [rax],edx
   140002a0a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a0e:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002a12:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002a16:	48 8d 05 03 67 00 00 	lea    rax,[rip+0x6703]        # 140009120 <__mingwthr_cs>
   140002a1d:	48 89 c1             	mov    rcx,rax
   140002a20:	48 8b 05 39 78 00 00 	mov    rax,QWORD PTR [rip+0x7839]        # 14000a260 <__imp_EnterCriticalSection>
   140002a27:	ff d0                	call   rax
   140002a29:	48 8b 15 20 67 00 00 	mov    rdx,QWORD PTR [rip+0x6720]        # 140009150 <key_dtor_list>
   140002a30:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a34:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002a38:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a3c:	48 89 05 0d 67 00 00 	mov    QWORD PTR [rip+0x670d],rax        # 140009150 <key_dtor_list>
   140002a43:	48 8d 05 d6 66 00 00 	lea    rax,[rip+0x66d6]        # 140009120 <__mingwthr_cs>
   140002a4a:	48 89 c1             	mov    rcx,rax
   140002a4d:	48 8b 05 3c 78 00 00 	mov    rax,QWORD PTR [rip+0x783c]        # 14000a290 <__imp_LeaveCriticalSection>
   140002a54:	ff d0                	call   rax
   140002a56:	b8 00 00 00 00       	mov    eax,0x0
   140002a5b:	48 83 c4 30          	add    rsp,0x30
   140002a5f:	5d                   	pop    rbp
   140002a60:	c3                   	ret

0000000140002a61 <___w64_mingwthr_remove_key_dtor>:
   140002a61:	55                   	push   rbp
   140002a62:	48 89 e5             	mov    rbp,rsp
   140002a65:	48 83 ec 30          	sub    rsp,0x30
   140002a69:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002a6c:	8b 05 d6 66 00 00    	mov    eax,DWORD PTR [rip+0x66d6]        # 140009148 <__mingwthr_cs_init>
   140002a72:	85 c0                	test   eax,eax
   140002a74:	75 0a                	jne    140002a80 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002a76:	b8 00 00 00 00       	mov    eax,0x0
   140002a7b:	e9 9c 00 00 00       	jmp    140002b1c <___w64_mingwthr_remove_key_dtor+0xbb>
   140002a80:	48 8d 05 99 66 00 00 	lea    rax,[rip+0x6699]        # 140009120 <__mingwthr_cs>
   140002a87:	48 89 c1             	mov    rcx,rax
   140002a8a:	48 8b 05 cf 77 00 00 	mov    rax,QWORD PTR [rip+0x77cf]        # 14000a260 <__imp_EnterCriticalSection>
   140002a91:	ff d0                	call   rax
   140002a93:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   140002a9a:	00 
   140002a9b:	48 8b 05 ae 66 00 00 	mov    rax,QWORD PTR [rip+0x66ae]        # 140009150 <key_dtor_list>
   140002aa2:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002aa6:	eb 55                	jmp    140002afd <___w64_mingwthr_remove_key_dtor+0x9c>
   140002aa8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002aac:	8b 00                	mov    eax,DWORD PTR [rax]
   140002aae:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140002ab1:	75 36                	jne    140002ae9 <___w64_mingwthr_remove_key_dtor+0x88>
   140002ab3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002ab8:	75 11                	jne    140002acb <___w64_mingwthr_remove_key_dtor+0x6a>
   140002aba:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002abe:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002ac2:	48 89 05 87 66 00 00 	mov    QWORD PTR [rip+0x6687],rax        # 140009150 <key_dtor_list>
   140002ac9:	eb 10                	jmp    140002adb <___w64_mingwthr_remove_key_dtor+0x7a>
   140002acb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002acf:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   140002ad3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ad7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002adb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002adf:	48 89 c1             	mov    rcx,rax
   140002ae2:	e8 79 08 00 00       	call   140003360 <free>
   140002ae7:	eb 1b                	jmp    140002b04 <___w64_mingwthr_remove_key_dtor+0xa3>
   140002ae9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002aed:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002af1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002af5:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002af9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002afd:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002b02:	75 a4                	jne    140002aa8 <___w64_mingwthr_remove_key_dtor+0x47>
   140002b04:	48 8d 05 15 66 00 00 	lea    rax,[rip+0x6615]        # 140009120 <__mingwthr_cs>
   140002b0b:	48 89 c1             	mov    rcx,rax
   140002b0e:	48 8b 05 7b 77 00 00 	mov    rax,QWORD PTR [rip+0x777b]        # 14000a290 <__imp_LeaveCriticalSection>
   140002b15:	ff d0                	call   rax
   140002b17:	b8 00 00 00 00       	mov    eax,0x0
   140002b1c:	48 83 c4 30          	add    rsp,0x30
   140002b20:	5d                   	pop    rbp
   140002b21:	c3                   	ret

0000000140002b22 <__mingwthr_run_key_dtors>:
   140002b22:	55                   	push   rbp
   140002b23:	48 89 e5             	mov    rbp,rsp
   140002b26:	48 83 ec 30          	sub    rsp,0x30
   140002b2a:	8b 05 18 66 00 00    	mov    eax,DWORD PTR [rip+0x6618]        # 140009148 <__mingwthr_cs_init>
   140002b30:	85 c0                	test   eax,eax
   140002b32:	0f 84 82 00 00 00    	je     140002bba <__mingwthr_run_key_dtors+0x98>
   140002b38:	48 8d 05 e1 65 00 00 	lea    rax,[rip+0x65e1]        # 140009120 <__mingwthr_cs>
   140002b3f:	48 89 c1             	mov    rcx,rax
   140002b42:	48 8b 05 17 77 00 00 	mov    rax,QWORD PTR [rip+0x7717]        # 14000a260 <__imp_EnterCriticalSection>
   140002b49:	ff d0                	call   rax
   140002b4b:	48 8b 05 fe 65 00 00 	mov    rax,QWORD PTR [rip+0x65fe]        # 140009150 <key_dtor_list>
   140002b52:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b56:	eb 46                	jmp    140002b9e <__mingwthr_run_key_dtors+0x7c>
   140002b58:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b5c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002b5e:	89 c1                	mov    ecx,eax
   140002b60:	48 8b 05 49 77 00 00 	mov    rax,QWORD PTR [rip+0x7749]        # 14000a2b0 <__imp_TlsGetValue>
   140002b67:	ff d0                	call   rax
   140002b69:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b6d:	48 8b 05 fc 76 00 00 	mov    rax,QWORD PTR [rip+0x76fc]        # 14000a270 <__imp_GetLastError>
   140002b74:	ff d0                	call   rax
   140002b76:	85 c0                	test   eax,eax
   140002b78:	75 18                	jne    140002b92 <__mingwthr_run_key_dtors+0x70>
   140002b7a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002b7f:	74 11                	je     140002b92 <__mingwthr_run_key_dtors+0x70>
   140002b81:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b85:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002b89:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b8d:	48 89 c1             	mov    rcx,rax
   140002b90:	ff d2                	call   rdx
   140002b92:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b96:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b9a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b9e:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002ba3:	75 b3                	jne    140002b58 <__mingwthr_run_key_dtors+0x36>
   140002ba5:	48 8d 05 74 65 00 00 	lea    rax,[rip+0x6574]        # 140009120 <__mingwthr_cs>
   140002bac:	48 89 c1             	mov    rcx,rax
   140002baf:	48 8b 05 da 76 00 00 	mov    rax,QWORD PTR [rip+0x76da]        # 14000a290 <__imp_LeaveCriticalSection>
   140002bb6:	ff d0                	call   rax
   140002bb8:	eb 01                	jmp    140002bbb <__mingwthr_run_key_dtors+0x99>
   140002bba:	90                   	nop
   140002bbb:	48 83 c4 30          	add    rsp,0x30
   140002bbf:	5d                   	pop    rbp
   140002bc0:	c3                   	ret

0000000140002bc1 <__mingw_TLScallback>:
   140002bc1:	55                   	push   rbp
   140002bc2:	48 89 e5             	mov    rbp,rsp
   140002bc5:	48 83 ec 30          	sub    rsp,0x30
   140002bc9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002bcd:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002bd0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002bd4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002bd8:	0f 84 cc 00 00 00    	je     140002caa <__mingw_TLScallback+0xe9>
   140002bde:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002be2:	0f 87 ca 00 00 00    	ja     140002cb2 <__mingw_TLScallback+0xf1>
   140002be8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002bec:	0f 84 b1 00 00 00    	je     140002ca3 <__mingw_TLScallback+0xe2>
   140002bf2:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002bf6:	0f 87 b6 00 00 00    	ja     140002cb2 <__mingw_TLScallback+0xf1>
   140002bfc:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002c00:	74 33                	je     140002c35 <__mingw_TLScallback+0x74>
   140002c02:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002c06:	0f 85 a6 00 00 00    	jne    140002cb2 <__mingw_TLScallback+0xf1>
   140002c0c:	8b 05 36 65 00 00    	mov    eax,DWORD PTR [rip+0x6536]        # 140009148 <__mingwthr_cs_init>
   140002c12:	85 c0                	test   eax,eax
   140002c14:	75 13                	jne    140002c29 <__mingw_TLScallback+0x68>
   140002c16:	48 8d 05 03 65 00 00 	lea    rax,[rip+0x6503]        # 140009120 <__mingwthr_cs>
   140002c1d:	48 89 c1             	mov    rcx,rax
   140002c20:	48 8b 05 61 76 00 00 	mov    rax,QWORD PTR [rip+0x7661]        # 14000a288 <__imp_InitializeCriticalSection>
   140002c27:	ff d0                	call   rax
   140002c29:	c7 05 15 65 00 00 01 	mov    DWORD PTR [rip+0x6515],0x1        # 140009148 <__mingwthr_cs_init>
   140002c30:	00 00 00 
   140002c33:	eb 7d                	jmp    140002cb2 <__mingw_TLScallback+0xf1>
   140002c35:	e8 e8 fe ff ff       	call   140002b22 <__mingwthr_run_key_dtors>
   140002c3a:	8b 05 08 65 00 00    	mov    eax,DWORD PTR [rip+0x6508]        # 140009148 <__mingwthr_cs_init>
   140002c40:	83 f8 01             	cmp    eax,0x1
   140002c43:	75 6c                	jne    140002cb1 <__mingw_TLScallback+0xf0>
   140002c45:	48 8b 05 04 65 00 00 	mov    rax,QWORD PTR [rip+0x6504]        # 140009150 <key_dtor_list>
   140002c4c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c50:	eb 20                	jmp    140002c72 <__mingw_TLScallback+0xb1>
   140002c52:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c56:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002c5a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002c5e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c62:	48 89 c1             	mov    rcx,rax
   140002c65:	e8 f6 06 00 00       	call   140003360 <free>
   140002c6a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c6e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c72:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002c77:	75 d9                	jne    140002c52 <__mingw_TLScallback+0x91>
   140002c79:	48 c7 05 cc 64 00 00 	mov    QWORD PTR [rip+0x64cc],0x0        # 140009150 <key_dtor_list>
   140002c80:	00 00 00 00 
   140002c84:	c7 05 ba 64 00 00 00 	mov    DWORD PTR [rip+0x64ba],0x0        # 140009148 <__mingwthr_cs_init>
   140002c8b:	00 00 00 
   140002c8e:	48 8d 05 8b 64 00 00 	lea    rax,[rip+0x648b]        # 140009120 <__mingwthr_cs>
   140002c95:	48 89 c1             	mov    rcx,rax
   140002c98:	48 8b 05 b9 75 00 00 	mov    rax,QWORD PTR [rip+0x75b9]        # 14000a258 <__imp_DeleteCriticalSection>
   140002c9f:	ff d0                	call   rax
   140002ca1:	eb 0e                	jmp    140002cb1 <__mingw_TLScallback+0xf0>
   140002ca3:	e8 18 00 00 00       	call   140002cc0 <_fpreset>
   140002ca8:	eb 08                	jmp    140002cb2 <__mingw_TLScallback+0xf1>
   140002caa:	e8 73 fe ff ff       	call   140002b22 <__mingwthr_run_key_dtors>
   140002caf:	eb 01                	jmp    140002cb2 <__mingw_TLScallback+0xf1>
   140002cb1:	90                   	nop
   140002cb2:	b8 01 00 00 00       	mov    eax,0x1
   140002cb7:	48 83 c4 30          	add    rsp,0x30
   140002cbb:	5d                   	pop    rbp
   140002cbc:	c3                   	ret
   140002cbd:	90                   	nop
   140002cbe:	90                   	nop
   140002cbf:	90                   	nop

0000000140002cc0 <_fpreset>:
   140002cc0:	55                   	push   rbp
   140002cc1:	48 89 e5             	mov    rbp,rsp
   140002cc4:	db e3                	fninit
   140002cc6:	90                   	nop
   140002cc7:	5d                   	pop    rbp
   140002cc8:	c3                   	ret
   140002cc9:	90                   	nop
   140002cca:	90                   	nop
   140002ccb:	90                   	nop
   140002ccc:	90                   	nop
   140002ccd:	90                   	nop
   140002cce:	90                   	nop
   140002ccf:	90                   	nop

0000000140002cd0 <_ValidateImageBase>:
   140002cd0:	55                   	push   rbp
   140002cd1:	48 89 e5             	mov    rbp,rsp
   140002cd4:	48 83 ec 20          	sub    rsp,0x20
   140002cd8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002cdc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002ce0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ce4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ce8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002ceb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002cef:	74 07                	je     140002cf8 <_ValidateImageBase+0x28>
   140002cf1:	b8 00 00 00 00       	mov    eax,0x0
   140002cf6:	eb 4e                	jmp    140002d46 <_ValidateImageBase+0x76>
   140002cf8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002cfc:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002cff:	48 63 d0             	movsxd rdx,eax
   140002d02:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d06:	48 01 d0             	add    rax,rdx
   140002d09:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002d0d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002d11:	8b 00                	mov    eax,DWORD PTR [rax]
   140002d13:	3d 50 45 00 00       	cmp    eax,0x4550
   140002d18:	74 07                	je     140002d21 <_ValidateImageBase+0x51>
   140002d1a:	b8 00 00 00 00       	mov    eax,0x0
   140002d1f:	eb 25                	jmp    140002d46 <_ValidateImageBase+0x76>
   140002d21:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002d25:	48 83 c0 18          	add    rax,0x18
   140002d29:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002d2d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d31:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002d34:	66 3d 0b 02          	cmp    ax,0x20b
   140002d38:	74 07                	je     140002d41 <_ValidateImageBase+0x71>
   140002d3a:	b8 00 00 00 00       	mov    eax,0x0
   140002d3f:	eb 05                	jmp    140002d46 <_ValidateImageBase+0x76>
   140002d41:	b8 01 00 00 00       	mov    eax,0x1
   140002d46:	48 83 c4 20          	add    rsp,0x20
   140002d4a:	5d                   	pop    rbp
   140002d4b:	c3                   	ret

0000000140002d4c <_FindPESection>:
   140002d4c:	55                   	push   rbp
   140002d4d:	48 89 e5             	mov    rbp,rsp
   140002d50:	48 83 ec 20          	sub    rsp,0x20
   140002d54:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002d58:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002d5c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002d60:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d63:	48 63 d0             	movsxd rdx,eax
   140002d66:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002d6a:	48 01 d0             	add    rax,rdx
   140002d6d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002d71:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d78:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d7c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d80:	0f b7 d0             	movzx  edx,ax
   140002d83:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d87:	48 01 d0             	add    rax,rdx
   140002d8a:	48 83 c0 18          	add    rax,0x18
   140002d8e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d92:	eb 36                	jmp    140002dca <_FindPESection+0x7e>
   140002d94:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d98:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002d9b:	89 c0                	mov    eax,eax
   140002d9d:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002da1:	72 1e                	jb     140002dc1 <_FindPESection+0x75>
   140002da3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002da7:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002daa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002dae:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002db1:	01 d0                	add    eax,edx
   140002db3:	89 c0                	mov    eax,eax
   140002db5:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002db9:	73 06                	jae    140002dc1 <_FindPESection+0x75>
   140002dbb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002dbf:	eb 1e                	jmp    140002ddf <_FindPESection+0x93>
   140002dc1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002dc5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002dca:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002dce:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002dd2:	0f b7 c0             	movzx  eax,ax
   140002dd5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002dd8:	72 ba                	jb     140002d94 <_FindPESection+0x48>
   140002dda:	b8 00 00 00 00       	mov    eax,0x0
   140002ddf:	48 83 c4 20          	add    rsp,0x20
   140002de3:	5d                   	pop    rbp
   140002de4:	c3                   	ret

0000000140002de5 <_FindPESectionByName>:
   140002de5:	55                   	push   rbp
   140002de6:	48 89 e5             	mov    rbp,rsp
   140002de9:	48 83 ec 40          	sub    rsp,0x40
   140002ded:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002df1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002df5:	48 89 c1             	mov    rcx,rax
   140002df8:	e8 93 05 00 00       	call   140003390 <strlen>
   140002dfd:	48 83 f8 08          	cmp    rax,0x8
   140002e01:	76 0a                	jbe    140002e0d <_FindPESectionByName+0x28>
   140002e03:	b8 00 00 00 00       	mov    eax,0x0
   140002e08:	e9 98 00 00 00       	jmp    140002ea5 <_FindPESectionByName+0xc0>
   140002e0d:	48 8b 05 6c 25 00 00 	mov    rax,QWORD PTR [rip+0x256c]        # 140005380 <.refptr.__ImageBase>
   140002e14:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e18:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e1c:	48 89 c1             	mov    rcx,rax
   140002e1f:	e8 ac fe ff ff       	call   140002cd0 <_ValidateImageBase>
   140002e24:	85 c0                	test   eax,eax
   140002e26:	75 07                	jne    140002e2f <_FindPESectionByName+0x4a>
   140002e28:	b8 00 00 00 00       	mov    eax,0x0
   140002e2d:	eb 76                	jmp    140002ea5 <_FindPESectionByName+0xc0>
   140002e2f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e33:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e36:	48 63 d0             	movsxd rdx,eax
   140002e39:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e3d:	48 01 d0             	add    rax,rdx
   140002e40:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002e44:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002e4b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e4f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002e53:	0f b7 d0             	movzx  edx,ax
   140002e56:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e5a:	48 01 d0             	add    rax,rdx
   140002e5d:	48 83 c0 18          	add    rax,0x18
   140002e61:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e65:	eb 29                	jmp    140002e90 <_FindPESectionByName+0xab>
   140002e67:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e6b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002e6f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002e75:	48 89 c1             	mov    rcx,rax
   140002e78:	e8 1b 05 00 00       	call   140003398 <strncmp>
   140002e7d:	85 c0                	test   eax,eax
   140002e7f:	75 06                	jne    140002e87 <_FindPESectionByName+0xa2>
   140002e81:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e85:	eb 1e                	jmp    140002ea5 <_FindPESectionByName+0xc0>
   140002e87:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002e8b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002e90:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e94:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e98:	0f b7 c0             	movzx  eax,ax
   140002e9b:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002e9e:	72 c7                	jb     140002e67 <_FindPESectionByName+0x82>
   140002ea0:	b8 00 00 00 00       	mov    eax,0x0
   140002ea5:	48 83 c4 40          	add    rsp,0x40
   140002ea9:	5d                   	pop    rbp
   140002eaa:	c3                   	ret

0000000140002eab <__mingw_GetSectionForAddress>:
   140002eab:	55                   	push   rbp
   140002eac:	48 89 e5             	mov    rbp,rsp
   140002eaf:	48 83 ec 30          	sub    rsp,0x30
   140002eb3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002eb7:	48 8b 05 c2 24 00 00 	mov    rax,QWORD PTR [rip+0x24c2]        # 140005380 <.refptr.__ImageBase>
   140002ebe:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ec2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ec6:	48 89 c1             	mov    rcx,rax
   140002ec9:	e8 02 fe ff ff       	call   140002cd0 <_ValidateImageBase>
   140002ece:	85 c0                	test   eax,eax
   140002ed0:	75 07                	jne    140002ed9 <__mingw_GetSectionForAddress+0x2e>
   140002ed2:	b8 00 00 00 00       	mov    eax,0x0
   140002ed7:	eb 1c                	jmp    140002ef5 <__mingw_GetSectionForAddress+0x4a>
   140002ed9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002edd:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002ee1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002ee5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002ee9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002eed:	48 89 c1             	mov    rcx,rax
   140002ef0:	e8 57 fe ff ff       	call   140002d4c <_FindPESection>
   140002ef5:	48 83 c4 30          	add    rsp,0x30
   140002ef9:	5d                   	pop    rbp
   140002efa:	c3                   	ret

0000000140002efb <__mingw_GetSectionCount>:
   140002efb:	55                   	push   rbp
   140002efc:	48 89 e5             	mov    rbp,rsp
   140002eff:	48 83 ec 30          	sub    rsp,0x30
   140002f03:	48 8b 05 76 24 00 00 	mov    rax,QWORD PTR [rip+0x2476]        # 140005380 <.refptr.__ImageBase>
   140002f0a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f0e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f12:	48 89 c1             	mov    rcx,rax
   140002f15:	e8 b6 fd ff ff       	call   140002cd0 <_ValidateImageBase>
   140002f1a:	85 c0                	test   eax,eax
   140002f1c:	75 07                	jne    140002f25 <__mingw_GetSectionCount+0x2a>
   140002f1e:	b8 00 00 00 00       	mov    eax,0x0
   140002f23:	eb 20                	jmp    140002f45 <__mingw_GetSectionCount+0x4a>
   140002f25:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f29:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002f2c:	48 63 d0             	movsxd rdx,eax
   140002f2f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f33:	48 01 d0             	add    rax,rdx
   140002f36:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f3a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002f3e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002f42:	0f b7 c0             	movzx  eax,ax
   140002f45:	48 83 c4 30          	add    rsp,0x30
   140002f49:	5d                   	pop    rbp
   140002f4a:	c3                   	ret

0000000140002f4b <_FindPESectionExec>:
   140002f4b:	55                   	push   rbp
   140002f4c:	48 89 e5             	mov    rbp,rsp
   140002f4f:	48 83 ec 40          	sub    rsp,0x40
   140002f53:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f57:	48 8b 05 22 24 00 00 	mov    rax,QWORD PTR [rip+0x2422]        # 140005380 <.refptr.__ImageBase>
   140002f5e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f62:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f66:	48 89 c1             	mov    rcx,rax
   140002f69:	e8 62 fd ff ff       	call   140002cd0 <_ValidateImageBase>
   140002f6e:	85 c0                	test   eax,eax
   140002f70:	75 07                	jne    140002f79 <_FindPESectionExec+0x2e>
   140002f72:	b8 00 00 00 00       	mov    eax,0x0
   140002f77:	eb 78                	jmp    140002ff1 <_FindPESectionExec+0xa6>
   140002f79:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f7d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002f80:	48 63 d0             	movsxd rdx,eax
   140002f83:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f87:	48 01 d0             	add    rax,rdx
   140002f8a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002f8e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002f95:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002f99:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002f9d:	0f b7 d0             	movzx  edx,ax
   140002fa0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002fa4:	48 01 d0             	add    rax,rdx
   140002fa7:	48 83 c0 18          	add    rax,0x18
   140002fab:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002faf:	eb 2b                	jmp    140002fdc <_FindPESectionExec+0x91>
   140002fb1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fb5:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002fb8:	25 00 00 00 20       	and    eax,0x20000000
   140002fbd:	85 c0                	test   eax,eax
   140002fbf:	74 12                	je     140002fd3 <_FindPESectionExec+0x88>
   140002fc1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002fc6:	75 06                	jne    140002fce <_FindPESectionExec+0x83>
   140002fc8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002fcc:	eb 23                	jmp    140002ff1 <_FindPESectionExec+0xa6>
   140002fce:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002fd3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002fd7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002fdc:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002fe0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002fe4:	0f b7 c0             	movzx  eax,ax
   140002fe7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002fea:	72 c5                	jb     140002fb1 <_FindPESectionExec+0x66>
   140002fec:	b8 00 00 00 00       	mov    eax,0x0
   140002ff1:	48 83 c4 40          	add    rsp,0x40
   140002ff5:	5d                   	pop    rbp
   140002ff6:	c3                   	ret

0000000140002ff7 <_GetPEImageBase>:
   140002ff7:	55                   	push   rbp
   140002ff8:	48 89 e5             	mov    rbp,rsp
   140002ffb:	48 83 ec 30          	sub    rsp,0x30
   140002fff:	48 8b 05 7a 23 00 00 	mov    rax,QWORD PTR [rip+0x237a]        # 140005380 <.refptr.__ImageBase>
   140003006:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000300a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000300e:	48 89 c1             	mov    rcx,rax
   140003011:	e8 ba fc ff ff       	call   140002cd0 <_ValidateImageBase>
   140003016:	85 c0                	test   eax,eax
   140003018:	75 07                	jne    140003021 <_GetPEImageBase+0x2a>
   14000301a:	b8 00 00 00 00       	mov    eax,0x0
   14000301f:	eb 04                	jmp    140003025 <_GetPEImageBase+0x2e>
   140003021:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003025:	48 83 c4 30          	add    rsp,0x30
   140003029:	5d                   	pop    rbp
   14000302a:	c3                   	ret

000000014000302b <_IsNonwritableInCurrentImage>:
   14000302b:	55                   	push   rbp
   14000302c:	48 89 e5             	mov    rbp,rsp
   14000302f:	48 83 ec 40          	sub    rsp,0x40
   140003033:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003037:	48 8b 05 42 23 00 00 	mov    rax,QWORD PTR [rip+0x2342]        # 140005380 <.refptr.__ImageBase>
   14000303e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003042:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003046:	48 89 c1             	mov    rcx,rax
   140003049:	e8 82 fc ff ff       	call   140002cd0 <_ValidateImageBase>
   14000304e:	85 c0                	test   eax,eax
   140003050:	75 07                	jne    140003059 <_IsNonwritableInCurrentImage+0x2e>
   140003052:	b8 00 00 00 00       	mov    eax,0x0
   140003057:	eb 3d                	jmp    140003096 <_IsNonwritableInCurrentImage+0x6b>
   140003059:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000305d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140003061:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140003065:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003069:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000306d:	48 89 c1             	mov    rcx,rax
   140003070:	e8 d7 fc ff ff       	call   140002d4c <_FindPESection>
   140003075:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140003079:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   14000307e:	75 07                	jne    140003087 <_IsNonwritableInCurrentImage+0x5c>
   140003080:	b8 00 00 00 00       	mov    eax,0x0
   140003085:	eb 0f                	jmp    140003096 <_IsNonwritableInCurrentImage+0x6b>
   140003087:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000308b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   14000308e:	f7 d0                	not    eax
   140003090:	c1 e8 1f             	shr    eax,0x1f
   140003093:	0f b6 c0             	movzx  eax,al
   140003096:	48 83 c4 40          	add    rsp,0x40
   14000309a:	5d                   	pop    rbp
   14000309b:	c3                   	ret

000000014000309c <__mingw_enum_import_library_names>:
   14000309c:	55                   	push   rbp
   14000309d:	48 89 e5             	mov    rbp,rsp
   1400030a0:	48 83 ec 50          	sub    rsp,0x50
   1400030a4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400030a7:	48 8b 05 d2 22 00 00 	mov    rax,QWORD PTR [rip+0x22d2]        # 140005380 <.refptr.__ImageBase>
   1400030ae:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400030b2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400030b6:	48 89 c1             	mov    rcx,rax
   1400030b9:	e8 12 fc ff ff       	call   140002cd0 <_ValidateImageBase>
   1400030be:	85 c0                	test   eax,eax
   1400030c0:	75 0a                	jne    1400030cc <__mingw_enum_import_library_names+0x30>
   1400030c2:	b8 00 00 00 00       	mov    eax,0x0
   1400030c7:	e9 ab 00 00 00       	jmp    140003177 <__mingw_enum_import_library_names+0xdb>
   1400030cc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400030d0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   1400030d3:	48 63 d0             	movsxd rdx,eax
   1400030d6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400030da:	48 01 d0             	add    rax,rdx
   1400030dd:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400030e1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400030e5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   1400030eb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400030ee:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400030f2:	75 07                	jne    1400030fb <__mingw_enum_import_library_names+0x5f>
   1400030f4:	b8 00 00 00 00       	mov    eax,0x0
   1400030f9:	eb 7c                	jmp    140003177 <__mingw_enum_import_library_names+0xdb>
   1400030fb:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   1400030fe:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003102:	48 89 c1             	mov    rcx,rax
   140003105:	e8 42 fc ff ff       	call   140002d4c <_FindPESection>
   14000310a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000310e:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140003113:	75 07                	jne    14000311c <__mingw_enum_import_library_names+0x80>
   140003115:	b8 00 00 00 00       	mov    eax,0x0
   14000311a:	eb 5b                	jmp    140003177 <__mingw_enum_import_library_names+0xdb>
   14000311c:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000311f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003123:	48 01 d0             	add    rax,rdx
   140003126:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000312a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000312f:	75 07                	jne    140003138 <__mingw_enum_import_library_names+0x9c>
   140003131:	b8 00 00 00 00       	mov    eax,0x0
   140003136:	eb 3f                	jmp    140003177 <__mingw_enum_import_library_names+0xdb>
   140003138:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000313c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000313f:	85 c0                	test   eax,eax
   140003141:	75 0b                	jne    14000314e <__mingw_enum_import_library_names+0xb2>
   140003143:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003147:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000314a:	85 c0                	test   eax,eax
   14000314c:	74 23                	je     140003171 <__mingw_enum_import_library_names+0xd5>
   14000314e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003152:	7f 12                	jg     140003166 <__mingw_enum_import_library_names+0xca>
   140003154:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003158:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000315b:	89 c2                	mov    edx,eax
   14000315d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003161:	48 01 d0             	add    rax,rdx
   140003164:	eb 11                	jmp    140003177 <__mingw_enum_import_library_names+0xdb>
   140003166:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000316a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000316f:	eb c7                	jmp    140003138 <__mingw_enum_import_library_names+0x9c>
   140003171:	90                   	nop
   140003172:	b8 00 00 00 00       	mov    eax,0x0
   140003177:	48 83 c4 50          	add    rsp,0x50
   14000317b:	5d                   	pop    rbp
   14000317c:	c3                   	ret
   14000317d:	90                   	nop
   14000317e:	90                   	nop
   14000317f:	90                   	nop

0000000140003180 <_Unwind_Resume>:
   140003180:	ff 25 82 70 00 00    	jmp    QWORD PTR [rip+0x7082]        # 14000a208 <__IAT_start__>
   140003186:	90                   	nop
   140003187:	90                   	nop
   140003188:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000318f:	00 

0000000140003190 <___chkstk_ms>:
   140003190:	51                   	push   rcx
   140003191:	50                   	push   rax
   140003192:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003198:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000319d:	72 19                	jb     1400031b8 <___chkstk_ms+0x28>
   14000319f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   1400031a6:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400031aa:	48 2d 00 10 00 00    	sub    rax,0x1000
   1400031b0:	48 3d 00 10 00 00    	cmp    rax,0x1000
   1400031b6:	77 e7                	ja     14000319f <___chkstk_ms+0xf>
   1400031b8:	48 29 c1             	sub    rcx,rax
   1400031bb:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   1400031bf:	58                   	pop    rax
   1400031c0:	59                   	pop    rcx
   1400031c1:	c3                   	ret
   1400031c2:	90                   	nop
   1400031c3:	90                   	nop
   1400031c4:	90                   	nop
   1400031c5:	90                   	nop
   1400031c6:	90                   	nop
   1400031c7:	90                   	nop
   1400031c8:	90                   	nop
   1400031c9:	90                   	nop
   1400031ca:	90                   	nop
   1400031cb:	90                   	nop
   1400031cc:	90                   	nop
   1400031cd:	90                   	nop
   1400031ce:	90                   	nop
   1400031cf:	90                   	nop

00000001400031d0 <_initterm_e>:
   1400031d0:	55                   	push   rbp
   1400031d1:	48 89 e5             	mov    rbp,rsp
   1400031d4:	48 83 ec 30          	sub    rsp,0x30
   1400031d8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400031dc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400031e0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400031e4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400031e8:	eb 29                	jmp    140003213 <_initterm_e+0x43>
   1400031ea:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031ee:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400031f1:	48 85 c0             	test   rax,rax
   1400031f4:	74 17                	je     14000320d <_initterm_e+0x3d>
   1400031f6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400031fa:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400031fd:	ff d0                	call   rax
   1400031ff:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003202:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003206:	74 06                	je     14000320e <_initterm_e+0x3e>
   140003208:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000320b:	eb 15                	jmp    140003222 <_initterm_e+0x52>
   14000320d:	90                   	nop
   14000320e:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140003213:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003217:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   14000321b:	72 cd                	jb     1400031ea <_initterm_e+0x1a>
   14000321d:	b8 00 00 00 00       	mov    eax,0x0
   140003222:	48 83 c4 30          	add    rsp,0x30
   140003226:	5d                   	pop    rbp
   140003227:	c3                   	ret
   140003228:	90                   	nop
   140003229:	90                   	nop
   14000322a:	90                   	nop
   14000322b:	90                   	nop
   14000322c:	90                   	nop
   14000322d:	90                   	nop
   14000322e:	90                   	nop
   14000322f:	90                   	nop

0000000140003230 <__p__fmode>:
   140003230:	55                   	push   rbp
   140003231:	48 89 e5             	mov    rbp,rsp
   140003234:	48 8b 05 b5 21 00 00 	mov    rax,QWORD PTR [rip+0x21b5]        # 1400053f0 <.refptr.__imp__fmode>
   14000323b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000323e:	5d                   	pop    rbp
   14000323f:	c3                   	ret

0000000140003240 <__p__commode>:
   140003240:	55                   	push   rbp
   140003241:	48 89 e5             	mov    rbp,rsp
   140003244:	48 8b 05 95 21 00 00 	mov    rax,QWORD PTR [rip+0x2195]        # 1400053e0 <.refptr.__imp__commode>
   14000324b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000324e:	5d                   	pop    rbp
   14000324f:	c3                   	ret

0000000140003250 <__p___initenv>:
   140003250:	55                   	push   rbp
   140003251:	48 89 e5             	mov    rbp,rsp
   140003254:	48 8b 05 75 21 00 00 	mov    rax,QWORD PTR [rip+0x2175]        # 1400053d0 <.refptr.__imp___initenv>
   14000325b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000325e:	5d                   	pop    rbp
   14000325f:	c3                   	ret

0000000140003260 <_set_invalid_parameter_handler>:
   140003260:	55                   	push   rbp
   140003261:	48 89 e5             	mov    rbp,rsp
   140003264:	48 83 ec 10          	sub    rsp,0x10
   140003268:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000326c:	48 8d 05 1d 5f 00 00 	lea    rax,[rip+0x5f1d]        # 140009190 <handler>
   140003273:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003277:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000327b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000327f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003283:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003287:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000328a:	48 89 d0             	mov    rax,rdx
   14000328d:	48 83 c4 10          	add    rsp,0x10
   140003291:	5d                   	pop    rbp
   140003292:	c3                   	ret

0000000140003293 <_get_invalid_parameter_handler>:
   140003293:	55                   	push   rbp
   140003294:	48 89 e5             	mov    rbp,rsp
   140003297:	48 8b 05 f2 5e 00 00 	mov    rax,QWORD PTR [rip+0x5ef2]        # 140009190 <handler>
   14000329e:	5d                   	pop    rbp
   14000329f:	c3                   	ret

00000001400032a0 <_configthreadlocale>:
   1400032a0:	55                   	push   rbp
   1400032a1:	48 89 e5             	mov    rbp,rsp
   1400032a4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400032a7:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   1400032ab:	75 07                	jne    1400032b4 <_configthreadlocale+0x14>
   1400032ad:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400032b2:	eb 05                	jmp    1400032b9 <_configthreadlocale+0x19>
   1400032b4:	b8 02 00 00 00       	mov    eax,0x2
   1400032b9:	5d                   	pop    rbp
   1400032ba:	c3                   	ret
   1400032bb:	90                   	nop
   1400032bc:	90                   	nop
   1400032bd:	90                   	nop
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <__acrt_iob_func>:
   1400032c0:	55                   	push   rbp
   1400032c1:	48 89 e5             	mov    rbp,rsp
   1400032c4:	48 83 ec 20          	sub    rsp,0x20
   1400032c8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400032cb:	e8 30 00 00 00       	call   140003300 <__iob_func>
   1400032d0:	48 89 c1             	mov    rcx,rax
   1400032d3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400032d6:	48 89 d0             	mov    rax,rdx
   1400032d9:	48 01 c0             	add    rax,rax
   1400032dc:	48 01 d0             	add    rax,rdx
   1400032df:	48 c1 e0 04          	shl    rax,0x4
   1400032e3:	48 01 c8             	add    rax,rcx
   1400032e6:	48 83 c4 20          	add    rsp,0x20
   1400032ea:	5d                   	pop    rbp
   1400032eb:	c3                   	ret
   1400032ec:	90                   	nop
   1400032ed:	90                   	nop
   1400032ee:	90                   	nop
   1400032ef:	90                   	nop

00000001400032f0 <__C_specific_handler>:
   1400032f0:	ff 25 da 6f 00 00    	jmp    QWORD PTR [rip+0x6fda]        # 14000a2d0 <__imp___C_specific_handler>
   1400032f6:	90                   	nop
   1400032f7:	90                   	nop

00000001400032f8 <__getmainargs>:
   1400032f8:	ff 25 da 6f 00 00    	jmp    QWORD PTR [rip+0x6fda]        # 14000a2d8 <__imp___getmainargs>
   1400032fe:	90                   	nop
   1400032ff:	90                   	nop

0000000140003300 <__iob_func>:
   140003300:	ff 25 e2 6f 00 00    	jmp    QWORD PTR [rip+0x6fe2]        # 14000a2e8 <__imp___iob_func>
   140003306:	90                   	nop
   140003307:	90                   	nop

0000000140003308 <__set_app_type>:
   140003308:	ff 25 e2 6f 00 00    	jmp    QWORD PTR [rip+0x6fe2]        # 14000a2f0 <__imp___set_app_type>
   14000330e:	90                   	nop
   14000330f:	90                   	nop

0000000140003310 <__setusermatherr>:
   140003310:	ff 25 e2 6f 00 00    	jmp    QWORD PTR [rip+0x6fe2]        # 14000a2f8 <__imp___setusermatherr>
   140003316:	90                   	nop
   140003317:	90                   	nop

0000000140003318 <_amsg_exit>:
   140003318:	ff 25 e2 6f 00 00    	jmp    QWORD PTR [rip+0x6fe2]        # 14000a300 <__imp__amsg_exit>
   14000331e:	90                   	nop
   14000331f:	90                   	nop

0000000140003320 <_cexit>:
   140003320:	ff 25 e2 6f 00 00    	jmp    QWORD PTR [rip+0x6fe2]        # 14000a308 <__imp__cexit>
   140003326:	90                   	nop
   140003327:	90                   	nop

0000000140003328 <_initterm>:
   140003328:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a320 <__imp__initterm>
   14000332e:	90                   	nop
   14000332f:	90                   	nop

0000000140003330 <_crt_atexit>:
   140003330:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a328 <__imp__crt_atexit>
   140003336:	90                   	nop
   140003337:	90                   	nop

0000000140003338 <abort>:
   140003338:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a330 <__imp_abort>
   14000333e:	90                   	nop
   14000333f:	90                   	nop

0000000140003340 <calloc>:
   140003340:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a338 <__imp_calloc>
   140003346:	90                   	nop
   140003347:	90                   	nop

0000000140003348 <exit>:
   140003348:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a340 <__imp_exit>
   14000334e:	90                   	nop
   14000334f:	90                   	nop

0000000140003350 <fflush>:
   140003350:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a348 <__imp_fflush>
   140003356:	90                   	nop
   140003357:	90                   	nop

0000000140003358 <fprintf>:
   140003358:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a350 <__imp_fprintf>
   14000335e:	90                   	nop
   14000335f:	90                   	nop

0000000140003360 <free>:
   140003360:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a358 <__imp_free>
   140003366:	90                   	nop
   140003367:	90                   	nop

0000000140003368 <malloc>:
   140003368:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a360 <__imp_malloc>
   14000336e:	90                   	nop
   14000336f:	90                   	nop

0000000140003370 <memcpy>:
   140003370:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a368 <__imp_memcpy>
   140003376:	90                   	nop
   140003377:	90                   	nop

0000000140003378 <memmove>:
   140003378:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a370 <__imp_memmove>
   14000337e:	90                   	nop
   14000337f:	90                   	nop

0000000140003380 <setvbuf>:
   140003380:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a378 <__imp_setvbuf>
   140003386:	90                   	nop
   140003387:	90                   	nop

0000000140003388 <signal>:
   140003388:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a380 <__imp_signal>
   14000338e:	90                   	nop
   14000338f:	90                   	nop

0000000140003390 <strlen>:
   140003390:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a388 <__imp_strlen>
   140003396:	90                   	nop
   140003397:	90                   	nop

0000000140003398 <strncmp>:
   140003398:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a390 <__imp_strncmp>
   14000339e:	90                   	nop
   14000339f:	90                   	nop

00000001400033a0 <vfprintf>:
   1400033a0:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a398 <__imp_vfprintf>
   1400033a6:	90                   	nop
   1400033a7:	90                   	nop
   1400033a8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   1400033af:	00 

00000001400033b0 <VirtualQuery>:
   1400033b0:	ff 25 0a 6f 00 00    	jmp    QWORD PTR [rip+0x6f0a]        # 14000a2c0 <__imp_VirtualQuery>
   1400033b6:	90                   	nop
   1400033b7:	90                   	nop

00000001400033b8 <VirtualProtect>:
   1400033b8:	ff 25 fa 6e 00 00    	jmp    QWORD PTR [rip+0x6efa]        # 14000a2b8 <__imp_VirtualProtect>
   1400033be:	90                   	nop
   1400033bf:	90                   	nop

00000001400033c0 <TlsGetValue>:
   1400033c0:	ff 25 ea 6e 00 00    	jmp    QWORD PTR [rip+0x6eea]        # 14000a2b0 <__imp_TlsGetValue>
   1400033c6:	90                   	nop
   1400033c7:	90                   	nop

00000001400033c8 <Sleep>:
   1400033c8:	ff 25 da 6e 00 00    	jmp    QWORD PTR [rip+0x6eda]        # 14000a2a8 <__imp_Sleep>
   1400033ce:	90                   	nop
   1400033cf:	90                   	nop

00000001400033d0 <SetUnhandledExceptionFilter>:
   1400033d0:	ff 25 ca 6e 00 00    	jmp    QWORD PTR [rip+0x6eca]        # 14000a2a0 <__imp_SetUnhandledExceptionFilter>
   1400033d6:	90                   	nop
   1400033d7:	90                   	nop

00000001400033d8 <LoadLibraryA>:
   1400033d8:	ff 25 ba 6e 00 00    	jmp    QWORD PTR [rip+0x6eba]        # 14000a298 <__imp_LoadLibraryA>
   1400033de:	90                   	nop
   1400033df:	90                   	nop

00000001400033e0 <LeaveCriticalSection>:
   1400033e0:	ff 25 aa 6e 00 00    	jmp    QWORD PTR [rip+0x6eaa]        # 14000a290 <__imp_LeaveCriticalSection>
   1400033e6:	90                   	nop
   1400033e7:	90                   	nop

00000001400033e8 <InitializeCriticalSection>:
   1400033e8:	ff 25 9a 6e 00 00    	jmp    QWORD PTR [rip+0x6e9a]        # 14000a288 <__imp_InitializeCriticalSection>
   1400033ee:	90                   	nop
   1400033ef:	90                   	nop

00000001400033f0 <GetProcAddress>:
   1400033f0:	ff 25 8a 6e 00 00    	jmp    QWORD PTR [rip+0x6e8a]        # 14000a280 <__imp_GetProcAddress>
   1400033f6:	90                   	nop
   1400033f7:	90                   	nop

00000001400033f8 <GetModuleHandleA>:
   1400033f8:	ff 25 7a 6e 00 00    	jmp    QWORD PTR [rip+0x6e7a]        # 14000a278 <__imp_GetModuleHandleA>
   1400033fe:	90                   	nop
   1400033ff:	90                   	nop

0000000140003400 <GetLastError>:
   140003400:	ff 25 6a 6e 00 00    	jmp    QWORD PTR [rip+0x6e6a]        # 14000a270 <__imp_GetLastError>
   140003406:	90                   	nop
   140003407:	90                   	nop

0000000140003408 <FreeLibrary>:
   140003408:	ff 25 5a 6e 00 00    	jmp    QWORD PTR [rip+0x6e5a]        # 14000a268 <__imp_FreeLibrary>
   14000340e:	90                   	nop
   14000340f:	90                   	nop

0000000140003410 <EnterCriticalSection>:
   140003410:	ff 25 4a 6e 00 00    	jmp    QWORD PTR [rip+0x6e4a]        # 14000a260 <__imp_EnterCriticalSection>
   140003416:	90                   	nop
   140003417:	90                   	nop

0000000140003418 <DeleteCriticalSection>:
   140003418:	ff 25 3a 6e 00 00    	jmp    QWORD PTR [rip+0x6e3a]        # 14000a258 <__imp_DeleteCriticalSection>
   14000341e:	90                   	nop
   14000341f:	90                   	nop

0000000140003420 <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)>:
   140003420:	41 54                	push   r12
   140003422:	55                   	push   rbp
   140003423:	57                   	push   rdi
   140003424:	56                   	push   rsi
   140003425:	53                   	push   rbx
   140003426:	48 83 ec 20          	sub    rsp,0x20
   14000342a:	b8 08 00 00 00       	mov    eax,0x8
   14000342f:	48 89 d3             	mov    rbx,rdx
   140003432:	48 89 ce             	mov    rsi,rcx
   140003435:	48 89 d7             	mov    rdi,rdx
   140003438:	48 c1 eb 07          	shr    rbx,0x7
   14000343c:	48 8d 6b 01          	lea    rbp,[rbx+0x1]
   140003440:	48 83 c3 03          	add    rbx,0x3
   140003444:	48 39 c3             	cmp    rbx,rax
   140003447:	48 0f 42 d8          	cmovb  rbx,rax
   14000344b:	48 89 59 08          	mov    QWORD PTR [rcx+0x8],rbx
   14000344f:	48 8d 0c dd 00 00 00 	lea    rcx,[rbx*8+0x0]
   140003456:	00 
   140003457:	48 29 eb             	sub    rbx,rbp
   14000345a:	48 d1 eb             	shr    rbx,1
   14000345d:	e8 2e e4 ff ff       	call   140001890 <operator new(unsigned long long)>
   140003462:	4c 8d 24 d8          	lea    r12,[rax+rbx*8]
   140003466:	48 89 06             	mov    QWORD PTR [rsi],rax
   140003469:	49 8d 2c ec          	lea    rbp,[r12+rbp*8]
   14000346d:	49 39 ec             	cmp    r12,rbp
   140003470:	73 24                	jae    140003496 <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)+0x76>
   140003472:	4c 89 e3             	mov    rbx,r12
   140003475:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000347c:	00 00 00 00 
   140003480:	b9 00 02 00 00       	mov    ecx,0x200
   140003485:	e8 06 e4 ff ff       	call   140001890 <operator new(unsigned long long)>
   14000348a:	48 89 03             	mov    QWORD PTR [rbx],rax
   14000348d:	48 83 c3 08          	add    rbx,0x8
   140003491:	48 39 eb             	cmp    rbx,rbp
   140003494:	72 ea                	jb     140003480 <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)+0x60>
   140003496:	49 8b 04 24          	mov    rax,QWORD PTR [r12]
   14000349a:	83 e7 7f             	and    edi,0x7f
   14000349d:	4c 89 66 28          	mov    QWORD PTR [rsi+0x28],r12
   1400034a1:	48 8d 90 00 02 00 00 	lea    rdx,[rax+0x200]
   1400034a8:	66 48 0f 6e c0       	movq   xmm0,rax
   1400034ad:	48 89 56 20          	mov    QWORD PTR [rsi+0x20],rdx
   1400034b1:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   1400034b5:	66 0f 6c c0          	punpcklqdq xmm0,xmm0
   1400034b9:	48 89 56 48          	mov    QWORD PTR [rsi+0x48],rdx
   1400034bd:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400034c1:	0f 11 46 10          	movups XMMWORD PTR [rsi+0x10],xmm0
   1400034c5:	48 8d 8a 00 02 00 00 	lea    rcx,[rdx+0x200]
   1400034cc:	48 8d 04 ba          	lea    rax,[rdx+rdi*4]
   1400034d0:	48 89 56 38          	mov    QWORD PTR [rsi+0x38],rdx
   1400034d4:	48 89 4e 40          	mov    QWORD PTR [rsi+0x40],rcx
   1400034d8:	48 89 46 30          	mov    QWORD PTR [rsi+0x30],rax
   1400034dc:	48 83 c4 20          	add    rsp,0x20
   1400034e0:	5b                   	pop    rbx
   1400034e1:	5e                   	pop    rsi
   1400034e2:	5f                   	pop    rdi
   1400034e3:	5d                   	pop    rbp
   1400034e4:	41 5c                	pop    r12
   1400034e6:	c3                   	ret
   1400034e7:	48 89 c1             	mov    rcx,rax
   1400034ea:	e8 99 e3 ff ff       	call   140001888 <__cxa_begin_catch>
   1400034ef:	49 39 dc             	cmp    r12,rbx
   1400034f2:	73 14                	jae    140003508 <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)+0xe8>
   1400034f4:	49 8b 0c 24          	mov    rcx,QWORD PTR [r12]
   1400034f8:	ba 00 02 00 00       	mov    edx,0x200
   1400034fd:	49 83 c4 08          	add    r12,0x8
   140003501:	e8 92 e3 ff ff       	call   140001898 <operator delete(void*, unsigned long long)>
   140003506:	eb e7                	jmp    1400034ef <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)+0xcf>
   140003508:	e8 6b e3 ff ff       	call   140001878 <__cxa_rethrow>
   14000350d:	48 89 c3             	mov    rbx,rax
   140003510:	e8 6b e3 ff ff       	call   140001880 <__cxa_end_catch>
   140003515:	48 89 d9             	mov    rcx,rbx
   140003518:	e8 6b e3 ff ff       	call   140001888 <__cxa_begin_catch>
   14000351d:	48 8b 46 08          	mov    rax,QWORD PTR [rsi+0x8]
   140003521:	48 8b 0e             	mov    rcx,QWORD PTR [rsi]
   140003524:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   14000352b:	00 
   14000352c:	e8 67 e3 ff ff       	call   140001898 <operator delete(void*, unsigned long long)>
   140003531:	31 c0                	xor    eax,eax
   140003533:	48 89 06             	mov    QWORD PTR [rsi],rax
   140003536:	48 89 46 08          	mov    QWORD PTR [rsi+0x8],rax
   14000353a:	e8 39 e3 ff ff       	call   140001878 <__cxa_rethrow>
   14000353f:	48 89 c3             	mov    rbx,rax
   140003542:	e8 39 e3 ff ff       	call   140001880 <__cxa_end_catch>
   140003547:	48 89 d9             	mov    rcx,rbx
   14000354a:	e8 31 fc ff ff       	call   140003180 <_Unwind_Resume>
   14000354f:	90                   	nop

0000000140003550 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()>:
   140003550:	57                   	push   rdi
   140003551:	56                   	push   rsi
   140003552:	53                   	push   rbx
   140003553:	48 83 ec 20          	sub    rsp,0x20
   140003557:	48 89 cf             	mov    rdi,rcx
   14000355a:	48 8b 09             	mov    rcx,QWORD PTR [rcx]
   14000355d:	48 85 c9             	test   rcx,rcx
   140003560:	74 4e                	je     1400035b0 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()+0x60>
   140003562:	48 8b 47 48          	mov    rax,QWORD PTR [rdi+0x48]
   140003566:	48 8b 5f 28          	mov    rbx,QWORD PTR [rdi+0x28]
   14000356a:	48 8d 70 08          	lea    rsi,[rax+0x8]
   14000356e:	48 39 f3             	cmp    rbx,rsi
   140003571:	73 26                	jae    140003599 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()+0x49>
   140003573:	66 90                	xchg   ax,ax
   140003575:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000357c:	00 00 00 00 
   140003580:	48 8b 0b             	mov    rcx,QWORD PTR [rbx]
   140003583:	ba 00 02 00 00       	mov    edx,0x200
   140003588:	48 83 c3 08          	add    rbx,0x8
   14000358c:	e8 07 e3 ff ff       	call   140001898 <operator delete(void*, unsigned long long)>
   140003591:	48 39 f3             	cmp    rbx,rsi
   140003594:	72 ea                	jb     140003580 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()+0x30>
   140003596:	48 8b 0f             	mov    rcx,QWORD PTR [rdi]
   140003599:	48 8b 57 08          	mov    rdx,QWORD PTR [rdi+0x8]
   14000359d:	48 c1 e2 03          	shl    rdx,0x3
   1400035a1:	48 83 c4 20          	add    rsp,0x20
   1400035a5:	5b                   	pop    rbx
   1400035a6:	5e                   	pop    rsi
   1400035a7:	5f                   	pop    rdi
   1400035a8:	e9 eb e2 ff ff       	jmp    140001898 <operator delete(void*, unsigned long long)>
   1400035ad:	0f 1f 00             	nop    DWORD PTR [rax]
   1400035b0:	48 83 c4 20          	add    rsp,0x20
   1400035b4:	5b                   	pop    rbx
   1400035b5:	5e                   	pop    rsi
   1400035b6:	5f                   	pop    rdi
   1400035b7:	c3                   	ret
   1400035b8:	90                   	nop
   1400035b9:	90                   	nop
   1400035ba:	90                   	nop
   1400035bb:	90                   	nop
   1400035bc:	90                   	nop
   1400035bd:	90                   	nop
   1400035be:	90                   	nop
   1400035bf:	90                   	nop

00000001400035c0 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)>:
   1400035c0:	41 55                	push   r13
   1400035c2:	41 54                	push   r12
   1400035c4:	55                   	push   rbp
   1400035c5:	57                   	push   rdi
   1400035c6:	56                   	push   rsi
   1400035c7:	53                   	push   rbx
   1400035c8:	48 83 ec 48          	sub    rsp,0x48
   1400035cc:	4c 8b 49 48          	mov    r9,QWORD PTR [rcx+0x48]
   1400035d0:	48 8b 79 08          	mov    rdi,QWORD PTR [rcx+0x8]
   1400035d4:	4c 89 cd             	mov    rbp,r9
   1400035d7:	48 89 d6             	mov    rsi,rdx
   1400035da:	48 8b 51 28          	mov    rdx,QWORD PTR [rcx+0x28]
   1400035de:	48 89 cb             	mov    rbx,rcx
   1400035e1:	48 29 d5             	sub    rbp,rdx
   1400035e4:	48 89 e8             	mov    rax,rbp
   1400035e7:	48 c1 f8 03          	sar    rax,0x3
   1400035eb:	4c 8d 54 06 01       	lea    r10,[rsi+rax*1+0x1]
   1400035f0:	4b 8d 04 12          	lea    rax,[r10+r10*1]
   1400035f4:	48 39 f8             	cmp    rax,rdi
   1400035f7:	73 47                	jae    140003640 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x80>
   1400035f9:	4c 29 d7             	sub    rdi,r10
   1400035fc:	48 d1 ef             	shr    rdi,1
   1400035ff:	48 c1 e7 03          	shl    rdi,0x3
   140003603:	45 84 c0             	test   r8b,r8b
   140003606:	4d 8d 41 08          	lea    r8,[r9+0x8]
   14000360a:	48 8d 04 f7          	lea    rax,[rdi+rsi*8]
   14000360e:	48 0f 45 f8          	cmovne rdi,rax
   140003612:	48 03 39             	add    rdi,QWORD PTR [rcx]
   140003615:	49 29 d0             	sub    r8,rdx
   140003618:	48 89 fe             	mov    rsi,rdi
   14000361b:	48 39 d7             	cmp    rdi,rdx
   14000361e:	0f 83 f4 00 00 00    	jae    140003718 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x158>
   140003624:	49 83 f8 08          	cmp    r8,0x8
   140003628:	0f 8e 42 01 00 00    	jle    140003770 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x1b0>
   14000362e:	48 89 f9             	mov    rcx,rdi
   140003631:	e8 42 fd ff ff       	call   140003378 <memmove>
   140003636:	48 8b 07             	mov    rax,QWORD PTR [rdi]
   140003639:	e9 93 00 00 00       	jmp    1400036d1 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x111>
   14000363e:	66 90                	xchg   ax,ax
   140003640:	48 39 f7             	cmp    rdi,rsi
   140003643:	48 89 f0             	mov    rax,rsi
   140003646:	44 89 44 24 3c       	mov    DWORD PTR [rsp+0x3c],r8d
   14000364b:	48 0f 43 c7          	cmovae rax,rdi
   14000364f:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx
   140003654:	4c 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],r9
   140003659:	4c 8d 64 07 02       	lea    r12,[rdi+rax*1+0x2]
   14000365e:	4c 89 54 24 30       	mov    QWORD PTR [rsp+0x30],r10
   140003663:	4a 8d 0c e5 00 00 00 	lea    rcx,[r12*8+0x0]
   14000366a:	00 
   14000366b:	e8 20 e2 ff ff       	call   140001890 <operator new(unsigned long long)>
   140003670:	4c 8b 4c 24 20       	mov    r9,QWORD PTR [rsp+0x20]
   140003675:	48 8b 54 24 28       	mov    rdx,QWORD PTR [rsp+0x28]
   14000367a:	49 89 c5             	mov    r13,rax
   14000367d:	4c 89 e0             	mov    rax,r12
   140003680:	48 2b 44 24 30       	sub    rax,QWORD PTR [rsp+0x30]
   140003685:	48 d1 e8             	shr    rax,1
   140003688:	4d 8d 41 08          	lea    r8,[r9+0x8]
   14000368c:	48 c1 e0 03          	shl    rax,0x3
   140003690:	80 7c 24 3c 00       	cmp    BYTE PTR [rsp+0x3c],0x0
   140003695:	48 8d 0c f0          	lea    rcx,[rax+rsi*8]
   140003699:	48 0f 45 c1          	cmovne rax,rcx
   14000369d:	49 29 d0             	sub    r8,rdx
   1400036a0:	49 8d 74 05 00       	lea    rsi,[r13+rax*1+0x0]
   1400036a5:	49 83 f8 08          	cmp    r8,0x8
   1400036a9:	0f 8e 91 00 00 00    	jle    140003740 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x180>
   1400036af:	48 89 f1             	mov    rcx,rsi
   1400036b2:	e8 c1 fc ff ff       	call   140003378 <memmove>
   1400036b7:	48 8b 0b             	mov    rcx,QWORD PTR [rbx]
   1400036ba:	48 8d 14 fd 00 00 00 	lea    rdx,[rdi*8+0x0]
   1400036c1:	00 
   1400036c2:	e8 d1 e1 ff ff       	call   140001898 <operator delete(void*, unsigned long long)>
   1400036c7:	4c 89 2b             	mov    QWORD PTR [rbx],r13
   1400036ca:	4c 89 63 08          	mov    QWORD PTR [rbx+0x8],r12
   1400036ce:	48 8b 06             	mov    rax,QWORD PTR [rsi]
   1400036d1:	48 89 43 18          	mov    QWORD PTR [rbx+0x18],rax
   1400036d5:	48 05 00 02 00 00    	add    rax,0x200
   1400036db:	48 89 73 28          	mov    QWORD PTR [rbx+0x28],rsi
   1400036df:	48 01 ee             	add    rsi,rbp
   1400036e2:	48 89 43 20          	mov    QWORD PTR [rbx+0x20],rax
   1400036e6:	48 8b 06             	mov    rax,QWORD PTR [rsi]
   1400036e9:	48 89 73 48          	mov    QWORD PTR [rbx+0x48],rsi
   1400036ed:	48 8d 90 00 02 00 00 	lea    rdx,[rax+0x200]
   1400036f4:	66 48 0f 6e c0       	movq   xmm0,rax
   1400036f9:	66 48 0f 6e ca       	movq   xmm1,rdx
   1400036fe:	66 0f 6c c1          	punpcklqdq xmm0,xmm1
   140003702:	0f 11 43 38          	movups XMMWORD PTR [rbx+0x38],xmm0
   140003706:	48 83 c4 48          	add    rsp,0x48
   14000370a:	5b                   	pop    rbx
   14000370b:	5e                   	pop    rsi
   14000370c:	5f                   	pop    rdi
   14000370d:	5d                   	pop    rbp
   14000370e:	41 5c                	pop    r12
   140003710:	41 5d                	pop    r13
   140003712:	c3                   	ret
   140003713:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   140003718:	4c 89 c0             	mov    rax,r8
   14000371b:	48 c1 e0 3d          	shl    rax,0x3d
   14000371f:	4c 29 c0             	sub    rax,r8
   140003722:	48 8d 4c 05 08       	lea    rcx,[rbp+rax*1+0x8]
   140003727:	48 01 f9             	add    rcx,rdi
   14000372a:	49 83 f8 08          	cmp    r8,0x8
   14000372e:	7e 28                	jle    140003758 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x198>
   140003730:	e8 43 fc ff ff       	call   140003378 <memmove>
   140003735:	48 8b 07             	mov    rax,QWORD PTR [rdi]
   140003738:	eb 97                	jmp    1400036d1 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x111>
   14000373a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
   140003740:	0f 85 71 ff ff ff    	jne    1400036b7 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0xf7>
   140003746:	48 8b 02             	mov    rax,QWORD PTR [rdx]
   140003749:	48 89 06             	mov    QWORD PTR [rsi],rax
   14000374c:	e9 66 ff ff ff       	jmp    1400036b7 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0xf7>
   140003751:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140003758:	0f 85 70 ff ff ff    	jne    1400036ce <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x10e>
   14000375e:	48 8b 02             	mov    rax,QWORD PTR [rdx]
   140003761:	48 89 01             	mov    QWORD PTR [rcx],rax
   140003764:	48 8b 07             	mov    rax,QWORD PTR [rdi]
   140003767:	e9 65 ff ff ff       	jmp    1400036d1 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x111>
   14000376c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
   140003770:	0f 85 58 ff ff ff    	jne    1400036ce <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x10e>
   140003776:	48 8b 02             	mov    rax,QWORD PTR [rdx]
   140003779:	48 89 07             	mov    QWORD PTR [rdi],rax
   14000377c:	e9 50 ff ff ff       	jmp    1400036d1 <std::deque<int, std::allocator<int> >::_M_reallocate_map(unsigned long long, bool)+0x111>
   140003781:	90                   	nop
   140003782:	90                   	nop
   140003783:	90                   	nop
   140003784:	90                   	nop
   140003785:	90                   	nop
   140003786:	90                   	nop
   140003787:	90                   	nop
   140003788:	90                   	nop
   140003789:	90                   	nop
   14000378a:	90                   	nop
   14000378b:	90                   	nop
   14000378c:	90                   	nop
   14000378d:	90                   	nop
   14000378e:	90                   	nop
   14000378f:	90                   	nop

0000000140003790 <std::deque<int, std::allocator<int> >::back()>:
   140003790:	48 8b 41 30          	mov    rax,QWORD PTR [rcx+0x30]
   140003794:	48 3b 41 38          	cmp    rax,QWORD PTR [rcx+0x38]
   140003798:	74 06                	je     1400037a0 <std::deque<int, std::allocator<int> >::back()+0x10>
   14000379a:	48 83 e8 04          	sub    rax,0x4
   14000379e:	c3                   	ret
   14000379f:	90                   	nop
   1400037a0:	48 8b 41 48          	mov    rax,QWORD PTR [rcx+0x48]
   1400037a4:	48 8b 40 f8          	mov    rax,QWORD PTR [rax-0x8]
   1400037a8:	48 05 00 02 00 00    	add    rax,0x200
   1400037ae:	48 83 e8 04          	sub    rax,0x4
   1400037b2:	c3                   	ret
   1400037b3:	90                   	nop
   1400037b4:	90                   	nop
   1400037b5:	90                   	nop
   1400037b6:	90                   	nop
   1400037b7:	90                   	nop
   1400037b8:	90                   	nop
   1400037b9:	90                   	nop
   1400037ba:	90                   	nop
   1400037bb:	90                   	nop
   1400037bc:	90                   	nop
   1400037bd:	90                   	nop
   1400037be:	90                   	nop
   1400037bf:	90                   	nop

00000001400037c0 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0] [clone .cold]>:
   1400037c0:	48 8d 0d 89 18 00 00 	lea    rcx,[rip+0x1889]        # 140005050 <.rdata>
   1400037c7:	e8 d4 e0 ff ff       	call   1400018a0 <std::__throw_length_error(char const*)>
   1400037cc:	90                   	nop

00000001400037cd <main.cold>:
   1400037cd:	48 8d 8c 24 80 00 00 	lea    rcx,[rsp+0x80]
   1400037d4:	00 
   1400037d5:	e8 76 fd ff ff       	call   140003550 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()>
   1400037da:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   1400037df:	e8 6c fd ff ff       	call   140003550 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()>
   1400037e4:	48 89 f9             	mov    rcx,rdi
   1400037e7:	e8 94 f9 ff ff       	call   140003180 <_Unwind_Resume>
   1400037ec:	90                   	nop
   1400037ed:	90                   	nop
   1400037ee:	90                   	nop
   1400037ef:	90                   	nop

00000001400037f0 <main>:
   1400037f0:	57                   	push   rdi
   1400037f1:	56                   	push   rsi
   1400037f2:	53                   	push   rbx
   1400037f3:	48 81 ec d0 00 00 00 	sub    rsp,0xd0
   1400037fa:	e8 68 e1 ff ff       	call   140001967 <__main>
   1400037ff:	66 0f ef c0          	pxor   xmm0,xmm0
   140003803:	31 d2                	xor    edx,edx
   140003805:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   14000380a:	48 c7 44 24 30 00 00 	mov    QWORD PTR [rsp+0x30],0x0
   140003811:	00 00 
   140003813:	48 c7 44 24 38 00 00 	mov    QWORD PTR [rsp+0x38],0x0
   14000381a:	00 00 
   14000381c:	0f 29 44 24 40       	movaps XMMWORD PTR [rsp+0x40],xmm0
   140003821:	0f 29 44 24 50       	movaps XMMWORD PTR [rsp+0x50],xmm0
   140003826:	0f 29 44 24 60       	movaps XMMWORD PTR [rsp+0x60],xmm0
   14000382b:	0f 29 44 24 70       	movaps XMMWORD PTR [rsp+0x70],xmm0
   140003830:	e8 eb fb ff ff       	call   140003420 <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)>
   140003835:	48 8d 94 24 80 00 00 	lea    rdx,[rsp+0x80]
   14000383c:	00 
   14000383d:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   140003842:	c7 84 24 80 00 00 00 	mov    DWORD PTR [rsp+0x80],0x1
   140003849:	01 00 00 00 
   14000384d:	e8 0e df ff ff       	call   140001760 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]>
   140003852:	48 8d 94 24 80 00 00 	lea    rdx,[rsp+0x80]
   140003859:	00 
   14000385a:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   14000385f:	c7 84 24 80 00 00 00 	mov    DWORD PTR [rsp+0x80],0x2
   140003866:	02 00 00 00 
   14000386a:	e8 f1 de ff ff       	call   140001760 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]>
   14000386f:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   140003874:	e8 17 ff ff ff       	call   140003790 <std::deque<int, std::allocator<int> >::back()>
   140003879:	66 0f ef c0          	pxor   xmm0,xmm0
   14000387d:	31 d2                	xor    edx,edx
   14000387f:	48 8d 8c 24 80 00 00 	lea    rcx,[rsp+0x80]
   140003886:	00 
   140003887:	8b 00                	mov    eax,DWORD PTR [rax]
   140003889:	0f 29 84 24 90 00 00 	movaps XMMWORD PTR [rsp+0x90],xmm0
   140003890:	00 
   140003891:	48 c7 84 24 80 00 00 	mov    QWORD PTR [rsp+0x80],0x0
   140003898:	00 00 00 00 00 
   14000389d:	89 44 24 24          	mov    DWORD PTR [rsp+0x24],eax
   1400038a1:	8b 44 24 24          	mov    eax,DWORD PTR [rsp+0x24]
   1400038a5:	48 c7 84 24 88 00 00 	mov    QWORD PTR [rsp+0x88],0x0
   1400038ac:	00 00 00 00 00 
   1400038b1:	0f 29 84 24 a0 00 00 	movaps XMMWORD PTR [rsp+0xa0],xmm0
   1400038b8:	00 
   1400038b9:	0f 29 84 24 b0 00 00 	movaps XMMWORD PTR [rsp+0xb0],xmm0
   1400038c0:	00 
   1400038c1:	0f 29 84 24 c0 00 00 	movaps XMMWORD PTR [rsp+0xc0],xmm0
   1400038c8:	00 
   1400038c9:	e8 52 fb ff ff       	call   140003420 <std::_Deque_base<int, std::allocator<int> >::_M_initialize_map(unsigned long long)>
   1400038ce:	48 8d 54 24 2c       	lea    rdx,[rsp+0x2c]
   1400038d3:	48 8d 8c 24 80 00 00 	lea    rcx,[rsp+0x80]
   1400038da:	00 
   1400038db:	c7 44 24 2c 01 00 00 	mov    DWORD PTR [rsp+0x2c],0x1
   1400038e2:	00 
   1400038e3:	e8 78 de ff ff       	call   140001760 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]>
   1400038e8:	48 8d 54 24 2c       	lea    rdx,[rsp+0x2c]
   1400038ed:	48 8d 8c 24 80 00 00 	lea    rcx,[rsp+0x80]
   1400038f4:	00 
   1400038f5:	c7 44 24 2c 02 00 00 	mov    DWORD PTR [rsp+0x2c],0x2
   1400038fc:	00 
   1400038fd:	e8 5e de ff ff       	call   140001760 <int& std::deque<int, std::allocator<int> >::emplace_back<int>(int&&) [clone .isra.0]>
   140003902:	48 8b 84 24 90 00 00 	mov    rax,QWORD PTR [rsp+0x90]
   140003909:	00 
   14000390a:	48 8d 8c 24 80 00 00 	lea    rcx,[rsp+0x80]
   140003911:	00 
   140003912:	8b 00                	mov    eax,DWORD PTR [rax]
   140003914:	89 44 24 28          	mov    DWORD PTR [rsp+0x28],eax
   140003918:	8b 44 24 28          	mov    eax,DWORD PTR [rsp+0x28]
   14000391c:	e8 6f fe ff ff       	call   140003790 <std::deque<int, std::allocator<int> >::back()>
   140003921:	48 8d 8c 24 80 00 00 	lea    rcx,[rsp+0x80]
   140003928:	00 
   140003929:	8b 00                	mov    eax,DWORD PTR [rax]
   14000392b:	89 44 24 2c          	mov    DWORD PTR [rsp+0x2c],eax
   14000392f:	8b 44 24 2c          	mov    eax,DWORD PTR [rsp+0x2c]
   140003933:	e8 18 fc ff ff       	call   140003550 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()>
   140003938:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   14000393d:	e8 0e fc ff ff       	call   140003550 <std::_Deque_base<int, std::allocator<int> >::~_Deque_base()>
   140003942:	31 c0                	xor    eax,eax
   140003944:	48 81 c4 d0 00 00 00 	add    rsp,0xd0
   14000394b:	5b                   	pop    rbx
   14000394c:	5e                   	pop    rsi
   14000394d:	5f                   	pop    rdi
   14000394e:	c3                   	ret
   14000394f:	48 89 c7             	mov    rdi,rax
   140003952:	e9 83 fe ff ff       	jmp    1400037da <main.cold+0xd>
   140003957:	48 89 c7             	mov    rdi,rax
   14000395a:	e9 6e fe ff ff       	jmp    1400037cd <main.cold>
   14000395f:	48 89 c7             	mov    rdi,rax
   140003962:	e9 66 fe ff ff       	jmp    1400037cd <main.cold>
   140003967:	90                   	nop
   140003968:	90                   	nop
   140003969:	90                   	nop
   14000396a:	90                   	nop
   14000396b:	90                   	nop
   14000396c:	90                   	nop
   14000396d:	90                   	nop
   14000396e:	90                   	nop
   14000396f:	90                   	nop

0000000140003970 <register_frame_ctor>:
   140003970:	e9 fb dc ff ff       	jmp    140001670 <__gcc_register_frame>
   140003975:	90                   	nop
   140003976:	90                   	nop
   140003977:	90                   	nop
   140003978:	90                   	nop
   140003979:	90                   	nop
   14000397a:	90                   	nop
   14000397b:	90                   	nop
   14000397c:	90                   	nop
   14000397d:	90                   	nop
   14000397e:	90                   	nop
   14000397f:	90                   	nop
