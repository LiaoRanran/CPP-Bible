
ch89_any_test.exe:     file format pei-x86-64


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
   140001024:	e8 f7 21 00 00       	call   140003220 <fflush>
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
   14000103f:	48 8b 05 fa 43 00 00 	mov    rax,QWORD PTR [rip+0x43fa]        # 140005440 <.refptr.__mingw_app_type>
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
   14000106e:	48 8b 05 cb 43 00 00 	mov    rax,QWORD PTR [rip+0x43cb]        # 140005440 <.refptr.__mingw_app_type>
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
   1400010e8:	48 8b 05 b1 91 00 00 	mov    rax,QWORD PTR [rip+0x91b1]        # 14000a2a0 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 98 43 00 00 	mov    rax,QWORD PTR [rip+0x4398]        # 140005490 <.refptr.__native_startup_lock>
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
   140001128:	48 8b 05 71 43 00 00 	mov    rax,QWORD PTR [rip+0x4371]        # 1400054a0 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 a8 20 00 00       	call   1400031e8 <_amsg_exit>
   140001140:	48 8b 05 59 43 00 00 	mov    rax,QWORD PTR [rip+0x4359]        # 1400054a0 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 48 43 00 00 	mov    rax,QWORD PTR [rip+0x4348]        # 1400054a0 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 28 20 00 00       	call   140003190 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 c7 20 00 00       	call   140003248 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 6f 20 00 00       	call   140003208 <abort>
   140001199:	e8 e2 10 00 00       	call   140002280 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 7b 43 00 00 	mov    rax,QWORD PTR [rip+0x437b]        # 140005520 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 e9 90 00 00 	mov    rax,QWORD PTR [rip+0x90e9]        # 14000a298 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 c8 42 00 00 	mov    rdx,QWORD PTR [rip+0x42c8]        # 140005480 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 66 1f 00 00       	call   140003130 <_set_invalid_parameter_handler>
   1400011ca:	e8 c1 19 00 00       	call   140002b90 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e 7e 00 00    	mov    DWORD PTR [rip+0x7e3e],eax        # 140009018 <managedapp>
   1400011da:	48 8b 05 5f 42 00 00 	mov    rax,QWORD PTR [rip+0x425f]        # 140005440 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 e7 1f 00 00       	call   1400031d8 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 db 1f 00 00       	call   1400031d8 <__set_app_type>
   1400011fd:	e8 fe 1e 00 00       	call   140003100 <__p__fmode>
   140001202:	48 8b 15 07 43 00 00 	mov    rdx,QWORD PTR [rip+0x4307]        # 140005510 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 fe 1e 00 00       	call   140003110 <__p__commode>
   140001212:	48 8b 15 d7 42 00 00 	mov    rdx,QWORD PTR [rip+0x42d7]        # 1400054f0 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 3e 06 00 00       	call   140001860 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 b3 1f 00 00       	call   1400031e8 <_amsg_exit>
   140001235:	48 8b 05 54 41 00 00 	mov    rax,QWORD PTR [rip+0x4154]        # 140005390 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 e6 42 00 00 	mov    rax,QWORD PTR [rip+0x42e6]        # 140005530 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 48 11 00 00       	call   14000239a <__mingw_setusermatherr>
   140001252:	48 8b 05 a7 41 00 00 	mov    rax,QWORD PTR [rip+0x41a7]        # 140005400 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 06 1f 00 00       	call   140003170 <_configthreadlocale>
   14000126a:	48 8b 15 6f 42 00 00 	mov    rdx,QWORD PTR [rip+0x426f]        # 1400054e0 <.refptr.__xi_z>
   140001271:	48 8b 05 58 42 00 00 	mov    rax,QWORD PTR [rip+0x4258]        # 1400054d0 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 20 1e 00 00       	call   1400030a0 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 5a 1f 00 00       	call   1400031e8 <_amsg_exit>
   14000128e:	48 8b 05 ab 42 00 00 	mov    rax,QWORD PTR [rip+0x42ab]        # 140005540 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 5f 42 00 00 	mov    rax,QWORD PTR [rip+0x425f]        # 140005500 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 7d 00 00 	lea    r10,[rip+0x7d65]        # 140009010 <envp>
   1400012ab:	48 8d 15 56 7d 00 00 	lea    rdx,[rip+0x7d56]        # 140009008 <argv>
   1400012b2:	48 8d 05 4b 7d 00 00 	lea    rax,[rip+0x7d4b]        # 140009004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 f8 1e 00 00       	call   1400031c8 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 05 1f 00 00       	call   1400031e8 <_amsg_exit>
   1400012e3:	8b 05 1b 7d 00 00    	mov    eax,DWORD PTR [rip+0x7d1b]        # 140009004 <argc>
   1400012e9:	48 8d 15 18 7d 00 00 	lea    rdx,[rip+0x7d18]        # 140009008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 de 1e 00 00       	call   1400031e8 <_amsg_exit>
   14000130a:	48 8b 15 af 41 00 00 	mov    rdx,QWORD PTR [rip+0x41af]        # 1400054c0 <.refptr.__xc_z>
   140001311:	48 8b 05 98 41 00 00 	mov    rax,QWORD PTR [rip+0x4198]        # 1400054b0 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 d8 1e 00 00       	call   1400031f8 <_initterm>
   140001320:	e8 12 05 00 00       	call   140001837 <__main>
   140001325:	48 8b 05 74 41 00 00 	mov    rax,QWORD PTR [rip+0x4174]        # 1400054a0 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de 7c 00 00 01 	mov    DWORD PTR [rip+0x7cde],0x1        # 14000901c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 45 41 00 00 	mov    rax,QWORD PTR [rip+0x4145]        # 140005490 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 87 40 00 00 	mov    rax,QWORD PTR [rip+0x4087]        # 1400053f0 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 78 40 00 00 	mov    rax,QWORD PTR [rip+0x4078]        # 1400053f0 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 8e 1d 00 00       	call   140003120 <__p___initenv>
   140001392:	48 8b 15 77 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c77]        # 140009010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d 7c 00 00 	mov    rcx,QWORD PTR [rip+0x7c6d]        # 140009010 <envp>
   1400013a3:	48 8b 15 5e 7c 00 00 	mov    rdx,QWORD PTR [rip+0x7c5e]        # 140009008 <argv>
   1400013aa:	8b 05 54 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c54]        # 140009004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 f6 21 00 00       	call   1400035b0 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c55]        # 140009018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 47 1e 00 00       	call   140003218 <exit>
   1400013d1:	8b 05 45 7c 00 00    	mov    eax,DWORD PTR [rip+0x7c45]        # 14000901c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 10 1e 00 00       	call   1400031f0 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 55 40 00 00 	mov    rax,QWORD PTR [rip+0x4055]        # 140005450 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 58 40 00 00 	mov    rax,QWORD PTR [rip+0x4058]        # 140005460 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 5b 40 00 00 	mov    rax,QWORD PTR [rip+0x405b]        # 140005470 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 9e 3f 00 00 	mov    rax,QWORD PTR [rip+0x3f9e]        # 1400053c0 <.refptr.__ImageBase>
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
   140001511:	e8 22 1d 00 00       	call   140003238 <malloc>
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
   14000155c:	e8 f7 1c 00 00       	call   140003258 <strlen>
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
   140001585:	e8 ae 1c 00 00       	call   140003238 <malloc>
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
   1400015e8:	e8 53 1c 00 00       	call   140003240 <memcpy>
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
   140001642:	e8 b9 1b 00 00       	call   140003200 <_crt_atexit>
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
   140001682:	ff 15 e8 8b 00 00    	call   QWORD PTR [rip+0x8be8]        # 14000a270 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 39 00 00 	lea    rcx,[rip+0x3969]        # 140005000 <.rdata>
   140001697:	ff 15 f3 8b 00 00    	call   QWORD PTR [rip+0x8bf3]        # 14000a290 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d d4 8b 00 00 	mov    r9,QWORD PTR [rip+0x8bd4]        # 14000a278 <__imp_GetProcAddress>
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
   14000174e:	48 ff 25 0b 8b 00 00 	rex.W jmp QWORD PTR [rip+0x8b0b]        # 14000a260 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <__gxx_personality_seh0>:
   140001760:	ff 25 da 8a 00 00    	jmp    QWORD PTR [rip+0x8ada]        # 14000a240 <__imp___gxx_personality_seh0>
   140001766:	90                   	nop
   140001767:	90                   	nop

0000000140001768 <operator new(unsigned long long)>:
   140001768:	ff 25 ca 8a 00 00    	jmp    QWORD PTR [rip+0x8aca]        # 14000a238 <__imp__Znwy>
   14000176e:	90                   	nop
   14000176f:	90                   	nop

0000000140001770 <operator delete(void*, unsigned long long)>:
   140001770:	ff 25 ba 8a 00 00    	jmp    QWORD PTR [rip+0x8aba]        # 14000a230 <__imp__ZdlPvy>
   140001776:	90                   	nop
   140001777:	90                   	nop

0000000140001778 <std::bad_cast::~bad_cast()>:
   140001778:	ff 25 92 8a 00 00    	jmp    QWORD PTR [rip+0x8a92]        # 14000a210 <__imp__ZNSt8bad_castD2Ev>
   14000177e:	90                   	nop
   14000177f:	90                   	nop

0000000140001780 <__do_global_dtors>:
   140001780:	55                   	push   rbp
   140001781:	48 89 e5             	mov    rbp,rsp
   140001784:	48 83 ec 20          	sub    rsp,0x20
   140001788:	eb 1e                	jmp    1400017a8 <__do_global_dtors+0x28>
   14000178a:	48 8b 05 7f 28 00 00 	mov    rax,QWORD PTR [rip+0x287f]        # 140004010 <p.0>
   140001791:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001794:	ff d0                	call   rax
   140001796:	48 8b 05 73 28 00 00 	mov    rax,QWORD PTR [rip+0x2873]        # 140004010 <p.0>
   14000179d:	48 83 c0 08          	add    rax,0x8
   1400017a1:	48 89 05 68 28 00 00 	mov    QWORD PTR [rip+0x2868],rax        # 140004010 <p.0>
   1400017a8:	48 8b 05 61 28 00 00 	mov    rax,QWORD PTR [rip+0x2861]        # 140004010 <p.0>
   1400017af:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017b2:	48 85 c0             	test   rax,rax
   1400017b5:	75 d3                	jne    14000178a <__do_global_dtors+0xa>
   1400017b7:	90                   	nop
   1400017b8:	90                   	nop
   1400017b9:	48 83 c4 20          	add    rsp,0x20
   1400017bd:	5d                   	pop    rbp
   1400017be:	c3                   	ret

00000001400017bf <__do_global_ctors>:
   1400017bf:	55                   	push   rbp
   1400017c0:	48 89 e5             	mov    rbp,rsp
   1400017c3:	48 83 ec 30          	sub    rsp,0x30
   1400017c7:	48 8b 05 e2 3b 00 00 	mov    rax,QWORD PTR [rip+0x3be2]        # 1400053b0 <.refptr.__CTOR_LIST__>
   1400017ce:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017d1:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400017d4:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   1400017d8:	75 25                	jne    1400017ff <__do_global_ctors+0x40>
   1400017da:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400017e1:	eb 04                	jmp    1400017e7 <__do_global_ctors+0x28>
   1400017e3:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400017e7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400017ea:	8d 50 01             	lea    edx,[rax+0x1]
   1400017ed:	48 8b 05 bc 3b 00 00 	mov    rax,QWORD PTR [rip+0x3bbc]        # 1400053b0 <.refptr.__CTOR_LIST__>
   1400017f4:	89 d2                	mov    edx,edx
   1400017f6:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   1400017fa:	48 85 c0             	test   rax,rax
   1400017fd:	75 e4                	jne    1400017e3 <__do_global_ctors+0x24>
   1400017ff:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001802:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001805:	eb 14                	jmp    14000181b <__do_global_ctors+0x5c>
   140001807:	48 8b 05 a2 3b 00 00 	mov    rax,QWORD PTR [rip+0x3ba2]        # 1400053b0 <.refptr.__CTOR_LIST__>
   14000180e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001811:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001815:	ff d0                	call   rax
   140001817:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000181b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000181f:	75 e6                	jne    140001807 <__do_global_ctors+0x48>
   140001821:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 140001780 <__do_global_dtors>
   140001828:	48 89 c1             	mov    rcx,rax
   14000182b:	e8 ff fd ff ff       	call   14000162f <atexit>
   140001830:	90                   	nop
   140001831:	48 83 c4 30          	add    rsp,0x30
   140001835:	5d                   	pop    rbp
   140001836:	c3                   	ret

0000000140001837 <__main>:
   140001837:	55                   	push   rbp
   140001838:	48 89 e5             	mov    rbp,rsp
   14000183b:	48 83 ec 20          	sub    rsp,0x20
   14000183f:	8b 05 3b 78 00 00    	mov    eax,DWORD PTR [rip+0x783b]        # 140009080 <initialized>
   140001845:	85 c0                	test   eax,eax
   140001847:	75 0f                	jne    140001858 <__main+0x21>
   140001849:	c7 05 2d 78 00 00 01 	mov    DWORD PTR [rip+0x782d],0x1        # 140009080 <initialized>
   140001850:	00 00 00 
   140001853:	e8 67 ff ff ff       	call   1400017bf <__do_global_ctors>
   140001858:	90                   	nop
   140001859:	48 83 c4 20          	add    rsp,0x20
   14000185d:	5d                   	pop    rbp
   14000185e:	c3                   	ret
   14000185f:	90                   	nop

0000000140001860 <_setargv>:
   140001860:	55                   	push   rbp
   140001861:	48 89 e5             	mov    rbp,rsp
   140001864:	b8 00 00 00 00       	mov    eax,0x0
   140001869:	5d                   	pop    rbp
   14000186a:	c3                   	ret
   14000186b:	90                   	nop
   14000186c:	90                   	nop
   14000186d:	90                   	nop
   14000186e:	90                   	nop
   14000186f:	90                   	nop

0000000140001870 <__dyn_tls_init>:
   140001870:	55                   	push   rbp
   140001871:	48 89 e5             	mov    rbp,rsp
   140001874:	48 83 ec 30          	sub    rsp,0x30
   140001878:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000187c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000187f:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001883:	48 8b 05 f6 3a 00 00 	mov    rax,QWORD PTR [rip+0x3af6]        # 140005380 <.refptr._CRT_MT>
   14000188a:	8b 00                	mov    eax,DWORD PTR [rax]
   14000188c:	83 f8 02             	cmp    eax,0x2
   14000188f:	74 0d                	je     14000189e <__dyn_tls_init+0x2e>
   140001891:	48 8b 05 e8 3a 00 00 	mov    rax,QWORD PTR [rip+0x3ae8]        # 140005380 <.refptr._CRT_MT>
   140001898:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   14000189e:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   1400018a2:	74 1e                	je     1400018c2 <__dyn_tls_init+0x52>
   1400018a4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   1400018a8:	75 5b                	jne    140001905 <__dyn_tls_init+0x95>
   1400018aa:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400018ae:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400018b1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400018b5:	49 89 c8             	mov    r8,rcx
   1400018b8:	48 89 c1             	mov    rcx,rax
   1400018bb:	e8 d1 11 00 00       	call   140002a91 <__mingw_TLScallback>
   1400018c0:	eb 43                	jmp    140001905 <__dyn_tls_init+0x95>
   1400018c2:	48 8d 05 97 3f 00 00 	lea    rax,[rip+0x3f97]        # 140005860 <___crt_xd_start__>
   1400018c9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400018cd:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400018d2:	eb 22                	jmp    1400018f6 <__dyn_tls_init+0x86>
   1400018d4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400018d8:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400018dc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400018e0:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400018e3:	48 85 c0             	test   rax,rax
   1400018e6:	74 09                	je     1400018f1 <__dyn_tls_init+0x81>
   1400018e8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400018ec:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400018ef:	ff d0                	call   rax
   1400018f1:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400018f6:	48 8d 05 6b 3f 00 00 	lea    rax,[rip+0x3f6b]        # 140005868 <__xd_z>
   1400018fd:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001901:	75 d1                	jne    1400018d4 <__dyn_tls_init+0x64>
   140001903:	eb 01                	jmp    140001906 <__dyn_tls_init+0x96>
   140001905:	90                   	nop
   140001906:	48 83 c4 30          	add    rsp,0x30
   14000190a:	5d                   	pop    rbp
   14000190b:	c3                   	ret

000000014000190c <__tlregdtor>:
   14000190c:	55                   	push   rbp
   14000190d:	48 89 e5             	mov    rbp,rsp
   140001910:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001914:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001919:	75 07                	jne    140001922 <__tlregdtor+0x16>
   14000191b:	b8 00 00 00 00       	mov    eax,0x0
   140001920:	eb 05                	jmp    140001927 <__tlregdtor+0x1b>
   140001922:	b8 00 00 00 00       	mov    eax,0x0
   140001927:	5d                   	pop    rbp
   140001928:	c3                   	ret

0000000140001929 <__dyn_tls_dtor>:
   140001929:	55                   	push   rbp
   14000192a:	48 89 e5             	mov    rbp,rsp
   14000192d:	48 83 ec 20          	sub    rsp,0x20
   140001931:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001935:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001938:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000193c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001940:	74 06                	je     140001948 <__dyn_tls_dtor+0x1f>
   140001942:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001946:	75 18                	jne    140001960 <__dyn_tls_dtor+0x37>
   140001948:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   14000194c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   14000194f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001953:	49 89 c8             	mov    r8,rcx
   140001956:	48 89 c1             	mov    rcx,rax
   140001959:	e8 33 11 00 00       	call   140002a91 <__mingw_TLScallback>
   14000195e:	eb 01                	jmp    140001961 <__dyn_tls_dtor+0x38>
   140001960:	90                   	nop
   140001961:	48 83 c4 20          	add    rsp,0x20
   140001965:	5d                   	pop    rbp
   140001966:	c3                   	ret
   140001967:	90                   	nop
   140001968:	90                   	nop
   140001969:	90                   	nop
   14000196a:	90                   	nop
   14000196b:	90                   	nop
   14000196c:	90                   	nop
   14000196d:	90                   	nop
   14000196e:	90                   	nop
   14000196f:	90                   	nop

0000000140001970 <_matherr>:
   140001970:	55                   	push   rbp
   140001971:	53                   	push   rbx
   140001972:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001979:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   14000197e:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   140001982:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   140001986:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   14000198b:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   14000198f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001993:	8b 00                	mov    eax,DWORD PTR [rax]
   140001995:	83 f8 06             	cmp    eax,0x6
   140001998:	74 56                	je     1400019f0 <_matherr+0x80>
   14000199a:	83 f8 06             	cmp    eax,0x6
   14000199d:	7f 78                	jg     140001a17 <_matherr+0xa7>
   14000199f:	83 f8 05             	cmp    eax,0x5
   1400019a2:	74 59                	je     1400019fd <_matherr+0x8d>
   1400019a4:	83 f8 05             	cmp    eax,0x5
   1400019a7:	7f 6e                	jg     140001a17 <_matherr+0xa7>
   1400019a9:	83 f8 04             	cmp    eax,0x4
   1400019ac:	74 5c                	je     140001a0a <_matherr+0x9a>
   1400019ae:	83 f8 04             	cmp    eax,0x4
   1400019b1:	7f 64                	jg     140001a17 <_matherr+0xa7>
   1400019b3:	83 f8 03             	cmp    eax,0x3
   1400019b6:	74 2b                	je     1400019e3 <_matherr+0x73>
   1400019b8:	83 f8 03             	cmp    eax,0x3
   1400019bb:	7f 5a                	jg     140001a17 <_matherr+0xa7>
   1400019bd:	83 f8 01             	cmp    eax,0x1
   1400019c0:	74 07                	je     1400019c9 <_matherr+0x59>
   1400019c2:	83 f8 02             	cmp    eax,0x2
   1400019c5:	74 0f                	je     1400019d6 <_matherr+0x66>
   1400019c7:	eb 4e                	jmp    140001a17 <_matherr+0xa7>
   1400019c9:	48 8d 05 10 37 00 00 	lea    rax,[rip+0x3710]        # 1400050e0 <.rdata>
   1400019d0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019d4:	eb 4d                	jmp    140001a23 <_matherr+0xb3>
   1400019d6:	48 8d 05 22 37 00 00 	lea    rax,[rip+0x3722]        # 1400050ff <.rdata+0x1f>
   1400019dd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019e1:	eb 40                	jmp    140001a23 <_matherr+0xb3>
   1400019e3:	48 8d 05 36 37 00 00 	lea    rax,[rip+0x3736]        # 140005120 <.rdata+0x40>
   1400019ea:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019ee:	eb 33                	jmp    140001a23 <_matherr+0xb3>
   1400019f0:	48 8d 05 49 37 00 00 	lea    rax,[rip+0x3749]        # 140005140 <.rdata+0x60>
   1400019f7:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019fb:	eb 26                	jmp    140001a23 <_matherr+0xb3>
   1400019fd:	48 8d 05 64 37 00 00 	lea    rax,[rip+0x3764]        # 140005168 <.rdata+0x88>
   140001a04:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a08:	eb 19                	jmp    140001a23 <_matherr+0xb3>
   140001a0a:	48 8d 05 7f 37 00 00 	lea    rax,[rip+0x377f]        # 140005190 <.rdata+0xb0>
   140001a11:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a15:	eb 0c                	jmp    140001a23 <_matherr+0xb3>
   140001a17:	48 8d 05 a8 37 00 00 	lea    rax,[rip+0x37a8]        # 1400051c6 <.rdata+0xe6>
   140001a1e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a22:	90                   	nop
   140001a23:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a27:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001a2d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a31:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001a36:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a3a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001a3f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a43:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001a47:	b9 02 00 00 00       	mov    ecx,0x2
   140001a4c:	e8 3f 17 00 00       	call   140003190 <__acrt_iob_func>
   140001a51:	48 89 c1             	mov    rcx,rax
   140001a54:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001a58:	48 8d 05 79 37 00 00 	lea    rax,[rip+0x3779]        # 1400051d8 <.rdata+0xf8>
   140001a5f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001a66:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001a6c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001a72:	49 89 d9             	mov    r9,rbx
   140001a75:	49 89 d0             	mov    r8,rdx
   140001a78:	48 89 c2             	mov    rdx,rax
   140001a7b:	e8 a8 17 00 00       	call   140003228 <fprintf>
   140001a80:	b8 00 00 00 00       	mov    eax,0x0
   140001a85:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001a89:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001a8d:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001a92:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001a99:	5b                   	pop    rbx
   140001a9a:	5d                   	pop    rbp
   140001a9b:	c3                   	ret
   140001a9c:	90                   	nop
   140001a9d:	90                   	nop
   140001a9e:	90                   	nop
   140001a9f:	90                   	nop

0000000140001aa0 <__report_error>:
   140001aa0:	55                   	push   rbp
   140001aa1:	53                   	push   rbx
   140001aa2:	48 83 ec 38          	sub    rsp,0x38
   140001aa6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001aab:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001aaf:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001ab3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001ab7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001abb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001abf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001ac3:	b9 02 00 00 00       	mov    ecx,0x2
   140001ac8:	e8 c3 16 00 00       	call   140003190 <__acrt_iob_func>
   140001acd:	48 89 c1             	mov    rcx,rax
   140001ad0:	48 8d 05 39 37 00 00 	lea    rax,[rip+0x3739]        # 140005210 <.rdata>
   140001ad7:	48 89 c2             	mov    rdx,rax
   140001ada:	e8 49 17 00 00       	call   140003228 <fprintf>
   140001adf:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001ae3:	b9 02 00 00 00       	mov    ecx,0x2
   140001ae8:	e8 a3 16 00 00       	call   140003190 <__acrt_iob_func>
   140001aed:	48 89 c1             	mov    rcx,rax
   140001af0:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001af4:	49 89 d8             	mov    r8,rbx
   140001af7:	48 89 c2             	mov    rdx,rax
   140001afa:	e8 69 17 00 00       	call   140003268 <vfprintf>
   140001aff:	e8 04 17 00 00       	call   140003208 <abort>
   140001b04:	90                   	nop

0000000140001b05 <mark_section_writable>:
   140001b05:	55                   	push   rbp
   140001b06:	48 89 e5             	mov    rbp,rsp
   140001b09:	48 83 ec 60          	sub    rsp,0x60
   140001b0d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b11:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b18:	e9 82 00 00 00       	jmp    140001b9f <mark_section_writable+0x9a>
   140001b1d:	48 8b 0d bc 75 00 00 	mov    rcx,QWORD PTR [rip+0x75bc]        # 1400090e0 <the_secs>
   140001b24:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b27:	48 63 d0             	movsxd rdx,eax
   140001b2a:	48 89 d0             	mov    rax,rdx
   140001b2d:	48 c1 e0 02          	shl    rax,0x2
   140001b31:	48 01 d0             	add    rax,rdx
   140001b34:	48 c1 e0 03          	shl    rax,0x3
   140001b38:	48 01 c8             	add    rax,rcx
   140001b3b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001b3f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001b43:	72 56                	jb     140001b9b <mark_section_writable+0x96>
   140001b45:	48 8b 0d 94 75 00 00 	mov    rcx,QWORD PTR [rip+0x7594]        # 1400090e0 <the_secs>
   140001b4c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b4f:	48 63 d0             	movsxd rdx,eax
   140001b52:	48 89 d0             	mov    rax,rdx
   140001b55:	48 c1 e0 02          	shl    rax,0x2
   140001b59:	48 01 d0             	add    rax,rdx
   140001b5c:	48 c1 e0 03          	shl    rax,0x3
   140001b60:	48 01 c8             	add    rax,rcx
   140001b63:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001b67:	4c 8b 05 72 75 00 00 	mov    r8,QWORD PTR [rip+0x7572]        # 1400090e0 <the_secs>
   140001b6e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b71:	48 63 d0             	movsxd rdx,eax
   140001b74:	48 89 d0             	mov    rax,rdx
   140001b77:	48 c1 e0 02          	shl    rax,0x2
   140001b7b:	48 01 d0             	add    rax,rdx
   140001b7e:	48 c1 e0 03          	shl    rax,0x3
   140001b82:	4c 01 c0             	add    rax,r8
   140001b85:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001b89:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001b8c:	89 c0                	mov    eax,eax
   140001b8e:	48 01 c8             	add    rax,rcx
   140001b91:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001b95:	0f 82 41 02 00 00    	jb     140001ddc <mark_section_writable+0x2d7>
   140001b9b:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001b9f:	8b 05 43 75 00 00    	mov    eax,DWORD PTR [rip+0x7543]        # 1400090e8 <maxSections>
   140001ba5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001ba8:	0f 8c 6f ff ff ff    	jl     140001b1d <mark_section_writable+0x18>
   140001bae:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bb2:	48 89 c1             	mov    rcx,rax
   140001bb5:	e8 c1 11 00 00       	call   140002d7b <__mingw_GetSectionForAddress>
   140001bba:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001bbe:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001bc3:	75 13                	jne    140001bd8 <mark_section_writable+0xd3>
   140001bc5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bc9:	48 8d 0d 60 36 00 00 	lea    rcx,[rip+0x3660]        # 140005230 <.rdata+0x20>
   140001bd0:	48 89 c2             	mov    rdx,rax
   140001bd3:	e8 c8 fe ff ff       	call   140001aa0 <__report_error>
   140001bd8:	48 8b 0d 01 75 00 00 	mov    rcx,QWORD PTR [rip+0x7501]        # 1400090e0 <the_secs>
   140001bdf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001be2:	48 63 d0             	movsxd rdx,eax
   140001be5:	48 89 d0             	mov    rax,rdx
   140001be8:	48 c1 e0 02          	shl    rax,0x2
   140001bec:	48 01 d0             	add    rax,rdx
   140001bef:	48 c1 e0 03          	shl    rax,0x3
   140001bf3:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001bf7:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001bfb:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001bff:	48 8b 0d da 74 00 00 	mov    rcx,QWORD PTR [rip+0x74da]        # 1400090e0 <the_secs>
   140001c06:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c09:	48 63 d0             	movsxd rdx,eax
   140001c0c:	48 89 d0             	mov    rax,rdx
   140001c0f:	48 c1 e0 02          	shl    rax,0x2
   140001c13:	48 01 d0             	add    rax,rdx
   140001c16:	48 c1 e0 03          	shl    rax,0x3
   140001c1a:	48 01 c8             	add    rax,rcx
   140001c1d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001c23:	e8 9f 12 00 00       	call   140002ec7 <_GetPEImageBase>
   140001c28:	48 89 c1             	mov    rcx,rax
   140001c2b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c2f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001c32:	41 89 c1             	mov    r9d,eax
   140001c35:	4c 8b 05 a4 74 00 00 	mov    r8,QWORD PTR [rip+0x74a4]        # 1400090e0 <the_secs>
   140001c3c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c3f:	48 63 d0             	movsxd rdx,eax
   140001c42:	48 89 d0             	mov    rax,rdx
   140001c45:	48 c1 e0 02          	shl    rax,0x2
   140001c49:	48 01 d0             	add    rax,rdx
   140001c4c:	48 c1 e0 03          	shl    rax,0x3
   140001c50:	4c 01 c0             	add    rax,r8
   140001c53:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001c57:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001c5b:	48 8b 0d 7e 74 00 00 	mov    rcx,QWORD PTR [rip+0x747e]        # 1400090e0 <the_secs>
   140001c62:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c65:	48 63 d0             	movsxd rdx,eax
   140001c68:	48 89 d0             	mov    rax,rdx
   140001c6b:	48 c1 e0 02          	shl    rax,0x2
   140001c6f:	48 01 d0             	add    rax,rdx
   140001c72:	48 c1 e0 03          	shl    rax,0x3
   140001c76:	48 01 c8             	add    rax,rcx
   140001c79:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001c7d:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001c81:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001c87:	48 89 c1             	mov    rcx,rax
   140001c8a:	48 8b 05 27 86 00 00 	mov    rax,QWORD PTR [rip+0x8627]        # 14000a2b8 <__imp_VirtualQuery>
   140001c91:	ff d0                	call   rax
   140001c93:	48 85 c0             	test   rax,rax
   140001c96:	75 3f                	jne    140001cd7 <mark_section_writable+0x1d2>
   140001c98:	48 8b 0d 41 74 00 00 	mov    rcx,QWORD PTR [rip+0x7441]        # 1400090e0 <the_secs>
   140001c9f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001ca2:	48 63 d0             	movsxd rdx,eax
   140001ca5:	48 89 d0             	mov    rax,rdx
   140001ca8:	48 c1 e0 02          	shl    rax,0x2
   140001cac:	48 01 d0             	add    rax,rdx
   140001caf:	48 c1 e0 03          	shl    rax,0x3
   140001cb3:	48 01 c8             	add    rax,rcx
   140001cb6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001cba:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001cbe:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001cc1:	89 c1                	mov    ecx,eax
   140001cc3:	48 8d 05 86 35 00 00 	lea    rax,[rip+0x3586]        # 140005250 <.rdata+0x40>
   140001cca:	49 89 d0             	mov    r8,rdx
   140001ccd:	89 ca                	mov    edx,ecx
   140001ccf:	48 89 c1             	mov    rcx,rax
   140001cd2:	e8 c9 fd ff ff       	call   140001aa0 <__report_error>
   140001cd7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001cda:	83 f8 40             	cmp    eax,0x40
   140001cdd:	0f 84 e8 00 00 00    	je     140001dcb <mark_section_writable+0x2c6>
   140001ce3:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001ce6:	83 f8 04             	cmp    eax,0x4
   140001ce9:	0f 84 dc 00 00 00    	je     140001dcb <mark_section_writable+0x2c6>
   140001cef:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001cf2:	3d 80 00 00 00       	cmp    eax,0x80
   140001cf7:	0f 84 ce 00 00 00    	je     140001dcb <mark_section_writable+0x2c6>
   140001cfd:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d00:	83 f8 08             	cmp    eax,0x8
   140001d03:	0f 84 c2 00 00 00    	je     140001dcb <mark_section_writable+0x2c6>
   140001d09:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d0c:	83 f8 02             	cmp    eax,0x2
   140001d0f:	75 09                	jne    140001d1a <mark_section_writable+0x215>
   140001d11:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001d18:	eb 07                	jmp    140001d21 <mark_section_writable+0x21c>
   140001d1a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001d21:	48 8b 0d b8 73 00 00 	mov    rcx,QWORD PTR [rip+0x73b8]        # 1400090e0 <the_secs>
   140001d28:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d2b:	48 63 d0             	movsxd rdx,eax
   140001d2e:	48 89 d0             	mov    rax,rdx
   140001d31:	48 c1 e0 02          	shl    rax,0x2
   140001d35:	48 01 d0             	add    rax,rdx
   140001d38:	48 c1 e0 03          	shl    rax,0x3
   140001d3c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d40:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d44:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001d48:	48 8b 0d 91 73 00 00 	mov    rcx,QWORD PTR [rip+0x7391]        # 1400090e0 <the_secs>
   140001d4f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d52:	48 63 d0             	movsxd rdx,eax
   140001d55:	48 89 d0             	mov    rax,rdx
   140001d58:	48 c1 e0 02          	shl    rax,0x2
   140001d5c:	48 01 d0             	add    rax,rdx
   140001d5f:	48 c1 e0 03          	shl    rax,0x3
   140001d63:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d67:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001d6b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001d6f:	48 8b 0d 6a 73 00 00 	mov    rcx,QWORD PTR [rip+0x736a]        # 1400090e0 <the_secs>
   140001d76:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d79:	48 63 d0             	movsxd rdx,eax
   140001d7c:	48 89 d0             	mov    rax,rdx
   140001d7f:	48 c1 e0 02          	shl    rax,0x2
   140001d83:	48 01 d0             	add    rax,rdx
   140001d86:	48 c1 e0 03          	shl    rax,0x3
   140001d8a:	48 01 c8             	add    rax,rcx
   140001d8d:	49 89 c0             	mov    r8,rax
   140001d90:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001d94:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d98:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001d9b:	4d 89 c1             	mov    r9,r8
   140001d9e:	41 89 c8             	mov    r8d,ecx
   140001da1:	48 89 c1             	mov    rcx,rax
   140001da4:	48 8b 05 05 85 00 00 	mov    rax,QWORD PTR [rip+0x8505]        # 14000a2b0 <__imp_VirtualProtect>
   140001dab:	ff d0                	call   rax
   140001dad:	85 c0                	test   eax,eax
   140001daf:	75 1a                	jne    140001dcb <mark_section_writable+0x2c6>
   140001db1:	48 8b 05 b0 84 00 00 	mov    rax,QWORD PTR [rip+0x84b0]        # 14000a268 <__imp_GetLastError>
   140001db8:	ff d0                	call   rax
   140001dba:	89 c2                	mov    edx,eax
   140001dbc:	48 8d 05 c5 34 00 00 	lea    rax,[rip+0x34c5]        # 140005288 <.rdata+0x78>
   140001dc3:	48 89 c1             	mov    rcx,rax
   140001dc6:	e8 d5 fc ff ff       	call   140001aa0 <__report_error>
   140001dcb:	8b 05 17 73 00 00    	mov    eax,DWORD PTR [rip+0x7317]        # 1400090e8 <maxSections>
   140001dd1:	83 c0 01             	add    eax,0x1
   140001dd4:	89 05 0e 73 00 00    	mov    DWORD PTR [rip+0x730e],eax        # 1400090e8 <maxSections>
   140001dda:	eb 01                	jmp    140001ddd <mark_section_writable+0x2d8>
   140001ddc:	90                   	nop
   140001ddd:	48 83 c4 60          	add    rsp,0x60
   140001de1:	5d                   	pop    rbp
   140001de2:	c3                   	ret

0000000140001de3 <restore_modified_sections>:
   140001de3:	55                   	push   rbp
   140001de4:	48 89 e5             	mov    rbp,rsp
   140001de7:	48 83 ec 30          	sub    rsp,0x30
   140001deb:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001df2:	e9 ad 00 00 00       	jmp    140001ea4 <restore_modified_sections+0xc1>
   140001df7:	48 8b 0d e2 72 00 00 	mov    rcx,QWORD PTR [rip+0x72e2]        # 1400090e0 <the_secs>
   140001dfe:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e01:	48 63 d0             	movsxd rdx,eax
   140001e04:	48 89 d0             	mov    rax,rdx
   140001e07:	48 c1 e0 02          	shl    rax,0x2
   140001e0b:	48 01 d0             	add    rax,rdx
   140001e0e:	48 c1 e0 03          	shl    rax,0x3
   140001e12:	48 01 c8             	add    rax,rcx
   140001e15:	8b 00                	mov    eax,DWORD PTR [rax]
   140001e17:	85 c0                	test   eax,eax
   140001e19:	0f 84 80 00 00 00    	je     140001e9f <restore_modified_sections+0xbc>
   140001e1f:	48 8b 0d ba 72 00 00 	mov    rcx,QWORD PTR [rip+0x72ba]        # 1400090e0 <the_secs>
   140001e26:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e29:	48 63 d0             	movsxd rdx,eax
   140001e2c:	48 89 d0             	mov    rax,rdx
   140001e2f:	48 c1 e0 02          	shl    rax,0x2
   140001e33:	48 01 d0             	add    rax,rdx
   140001e36:	48 c1 e0 03          	shl    rax,0x3
   140001e3a:	48 01 c8             	add    rax,rcx
   140001e3d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001e40:	48 8b 0d 99 72 00 00 	mov    rcx,QWORD PTR [rip+0x7299]        # 1400090e0 <the_secs>
   140001e47:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e4a:	48 63 d0             	movsxd rdx,eax
   140001e4d:	48 89 d0             	mov    rax,rdx
   140001e50:	48 c1 e0 02          	shl    rax,0x2
   140001e54:	48 01 d0             	add    rax,rdx
   140001e57:	48 c1 e0 03          	shl    rax,0x3
   140001e5b:	48 01 c8             	add    rax,rcx
   140001e5e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001e62:	4c 8b 05 77 72 00 00 	mov    r8,QWORD PTR [rip+0x7277]        # 1400090e0 <the_secs>
   140001e69:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e6c:	48 63 d0             	movsxd rdx,eax
   140001e6f:	48 89 d0             	mov    rax,rdx
   140001e72:	48 c1 e0 02          	shl    rax,0x2
   140001e76:	48 01 d0             	add    rax,rdx
   140001e79:	48 c1 e0 03          	shl    rax,0x3
   140001e7d:	4c 01 c0             	add    rax,r8
   140001e80:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001e84:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001e88:	49 89 d1             	mov    r9,rdx
   140001e8b:	45 89 d0             	mov    r8d,r10d
   140001e8e:	48 89 ca             	mov    rdx,rcx
   140001e91:	48 89 c1             	mov    rcx,rax
   140001e94:	48 8b 05 15 84 00 00 	mov    rax,QWORD PTR [rip+0x8415]        # 14000a2b0 <__imp_VirtualProtect>
   140001e9b:	ff d0                	call   rax
   140001e9d:	eb 01                	jmp    140001ea0 <restore_modified_sections+0xbd>
   140001e9f:	90                   	nop
   140001ea0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001ea4:	8b 05 3e 72 00 00    	mov    eax,DWORD PTR [rip+0x723e]        # 1400090e8 <maxSections>
   140001eaa:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001ead:	0f 8c 44 ff ff ff    	jl     140001df7 <restore_modified_sections+0x14>
   140001eb3:	90                   	nop
   140001eb4:	90                   	nop
   140001eb5:	48 83 c4 30          	add    rsp,0x30
   140001eb9:	5d                   	pop    rbp
   140001eba:	c3                   	ret

0000000140001ebb <__write_memory>:
   140001ebb:	55                   	push   rbp
   140001ebc:	48 89 e5             	mov    rbp,rsp
   140001ebf:	48 83 ec 20          	sub    rsp,0x20
   140001ec3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001ec7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001ecb:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001ecf:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140001ed4:	74 25                	je     140001efb <__write_memory+0x40>
   140001ed6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001eda:	48 89 c1             	mov    rcx,rax
   140001edd:	e8 23 fc ff ff       	call   140001b05 <mark_section_writable>
   140001ee2:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001ee6:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140001eea:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001eee:	49 89 c8             	mov    r8,rcx
   140001ef1:	48 89 c1             	mov    rcx,rax
   140001ef4:	e8 47 13 00 00       	call   140003240 <memcpy>
   140001ef9:	eb 01                	jmp    140001efc <__write_memory+0x41>
   140001efb:	90                   	nop
   140001efc:	48 83 c4 20          	add    rsp,0x20
   140001f00:	5d                   	pop    rbp
   140001f01:	c3                   	ret

0000000140001f02 <do_pseudo_reloc>:
   140001f02:	55                   	push   rbp
   140001f03:	48 89 e5             	mov    rbp,rsp
   140001f06:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   140001f0a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f0e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f12:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f16:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140001f1a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140001f1e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f22:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f26:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001f2a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   140001f2f:	0f 8e 44 03 00 00    	jle    140002279 <do_pseudo_reloc+0x377>
   140001f35:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   140001f3a:	7e 25                	jle    140001f61 <do_pseudo_reloc+0x5f>
   140001f3c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f40:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f42:	85 c0                	test   eax,eax
   140001f44:	75 1b                	jne    140001f61 <do_pseudo_reloc+0x5f>
   140001f46:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f4a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f4d:	85 c0                	test   eax,eax
   140001f4f:	75 10                	jne    140001f61 <do_pseudo_reloc+0x5f>
   140001f51:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f55:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001f58:	85 c0                	test   eax,eax
   140001f5a:	75 05                	jne    140001f61 <do_pseudo_reloc+0x5f>
   140001f5c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140001f61:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f65:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f67:	85 c0                	test   eax,eax
   140001f69:	75 0b                	jne    140001f76 <do_pseudo_reloc+0x74>
   140001f6b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f6f:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f72:	85 c0                	test   eax,eax
   140001f74:	74 59                	je     140001fcf <do_pseudo_reloc+0xcd>
   140001f76:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f7a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001f7e:	eb 40                	jmp    140001fc0 <do_pseudo_reloc+0xbe>
   140001f80:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001f84:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f87:	89 c2                	mov    edx,eax
   140001f89:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001f8d:	48 01 d0             	add    rax,rdx
   140001f90:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f94:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001f98:	8b 10                	mov    edx,DWORD PTR [rax]
   140001f9a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001f9e:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fa0:	01 d0                	add    eax,edx
   140001fa2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140001fa5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fa9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   140001fad:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001fb3:	48 89 c1             	mov    rcx,rax
   140001fb6:	e8 00 ff ff ff       	call   140001ebb <__write_memory>
   140001fbb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140001fc0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fc4:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140001fc8:	72 b6                	jb     140001f80 <do_pseudo_reloc+0x7e>
   140001fca:	e9 ab 02 00 00       	jmp    14000227a <do_pseudo_reloc+0x378>
   140001fcf:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fd3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001fd6:	83 f8 01             	cmp    eax,0x1
   140001fd9:	74 18                	je     140001ff3 <do_pseudo_reloc+0xf1>
   140001fdb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fdf:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001fe2:	89 c2                	mov    edx,eax
   140001fe4:	48 8d 05 c5 32 00 00 	lea    rax,[rip+0x32c5]        # 1400052b0 <.rdata+0xa0>
   140001feb:	48 89 c1             	mov    rcx,rax
   140001fee:	e8 ad fa ff ff       	call   140001aa0 <__report_error>
   140001ff3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001ff7:	48 83 c0 0c          	add    rax,0xc
   140001ffb:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001fff:	e9 65 02 00 00       	jmp    140002269 <do_pseudo_reloc+0x367>
   140002004:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002008:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000200b:	89 c2                	mov    edx,eax
   14000200d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002011:	48 01 d0             	add    rax,rdx
   140002014:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002018:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000201c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000201e:	89 c2                	mov    edx,eax
   140002020:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002024:	48 01 d0             	add    rax,rdx
   140002027:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000202b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000202f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002032:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002036:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000203a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000203d:	0f b6 c0             	movzx  eax,al
   140002040:	83 f8 40             	cmp    eax,0x40
   140002043:	0f 84 b6 00 00 00    	je     1400020ff <do_pseudo_reloc+0x1fd>
   140002049:	83 f8 40             	cmp    eax,0x40
   14000204c:	0f 87 ba 00 00 00    	ja     14000210c <do_pseudo_reloc+0x20a>
   140002052:	83 f8 20             	cmp    eax,0x20
   140002055:	74 77                	je     1400020ce <do_pseudo_reloc+0x1cc>
   140002057:	83 f8 20             	cmp    eax,0x20
   14000205a:	0f 87 ac 00 00 00    	ja     14000210c <do_pseudo_reloc+0x20a>
   140002060:	83 f8 08             	cmp    eax,0x8
   140002063:	74 0a                	je     14000206f <do_pseudo_reloc+0x16d>
   140002065:	83 f8 10             	cmp    eax,0x10
   140002068:	74 38                	je     1400020a2 <do_pseudo_reloc+0x1a0>
   14000206a:	e9 9d 00 00 00       	jmp    14000210c <do_pseudo_reloc+0x20a>
   14000206f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002073:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140002076:	0f b6 c0             	movzx  eax,al
   140002079:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000207d:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002081:	25 80 00 00 00       	and    eax,0x80
   140002086:	48 85 c0             	test   rax,rax
   140002089:	0f 84 9d 00 00 00    	je     14000212c <do_pseudo_reloc+0x22a>
   14000208f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140002093:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   140002099:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000209d:	e9 8a 00 00 00       	jmp    14000212c <do_pseudo_reloc+0x22a>
   1400020a2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020a6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400020a9:	0f b7 c0             	movzx  eax,ax
   1400020ac:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020b0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020b4:	25 00 80 00 00       	and    eax,0x8000
   1400020b9:	48 85 c0             	test   rax,rax
   1400020bc:	74 71                	je     14000212f <do_pseudo_reloc+0x22d>
   1400020be:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020c2:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   1400020c8:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020cc:	eb 61                	jmp    14000212f <do_pseudo_reloc+0x22d>
   1400020ce:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020d2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400020d4:	89 c0                	mov    eax,eax
   1400020d6:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020da:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020de:	25 00 00 00 80       	and    eax,0x80000000
   1400020e3:	48 85 c0             	test   rax,rax
   1400020e6:	74 4a                	je     140002132 <do_pseudo_reloc+0x230>
   1400020e8:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020ec:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   1400020f3:	ff ff ff 
   1400020f6:	48 09 d0             	or     rax,rdx
   1400020f9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020fd:	eb 33                	jmp    140002132 <do_pseudo_reloc+0x230>
   1400020ff:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002103:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002106:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000210a:	eb 27                	jmp    140002133 <do_pseudo_reloc+0x231>
   14000210c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002113:	00 
   140002114:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002118:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000211b:	0f b6 c0             	movzx  eax,al
   14000211e:	48 8d 0d c3 31 00 00 	lea    rcx,[rip+0x31c3]        # 1400052e8 <.rdata+0xd8>
   140002125:	89 c2                	mov    edx,eax
   140002127:	e8 74 f9 ff ff       	call   140001aa0 <__report_error>
   14000212c:	90                   	nop
   14000212d:	eb 04                	jmp    140002133 <do_pseudo_reloc+0x231>
   14000212f:	90                   	nop
   140002130:	eb 01                	jmp    140002133 <do_pseudo_reloc+0x231>
   140002132:	90                   	nop
   140002133:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002137:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000213b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000213d:	89 c2                	mov    edx,eax
   14000213f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002143:	48 01 c2             	add    rdx,rax
   140002146:	48 89 c8             	mov    rax,rcx
   140002149:	48 29 d0             	sub    rax,rdx
   14000214c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002150:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002154:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002158:	48 01 d0             	add    rax,rdx
   14000215b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000215f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002163:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002166:	25 ff 00 00 00       	and    eax,0xff
   14000216b:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000216e:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   140002172:	77 67                	ja     1400021db <do_pseudo_reloc+0x2d9>
   140002174:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002177:	ba 01 00 00 00       	mov    edx,0x1
   14000217c:	89 c1                	mov    ecx,eax
   14000217e:	48 d3 e2             	shl    rdx,cl
   140002181:	48 89 d0             	mov    rax,rdx
   140002184:	48 83 e8 01          	sub    rax,0x1
   140002188:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000218c:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   14000218f:	83 e8 01             	sub    eax,0x1
   140002192:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   140002199:	89 c1                	mov    ecx,eax
   14000219b:	48 d3 e2             	shl    rdx,cl
   14000219e:	48 89 d0             	mov    rax,rdx
   1400021a1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400021a5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021a9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400021ad:	7c 0a                	jl     1400021b9 <do_pseudo_reloc+0x2b7>
   1400021af:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021b3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400021b7:	7e 22                	jle    1400021db <do_pseudo_reloc+0x2d9>
   1400021b9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400021bd:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   1400021c1:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   1400021c5:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021c8:	48 8d 0d 49 31 00 00 	lea    rcx,[rip+0x3149]        # 140005318 <.rdata+0x108>
   1400021cf:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   1400021d4:	89 c2                	mov    edx,eax
   1400021d6:	e8 c5 f8 ff ff       	call   140001aa0 <__report_error>
   1400021db:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021df:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400021e2:	0f b6 c0             	movzx  eax,al
   1400021e5:	83 f8 40             	cmp    eax,0x40
   1400021e8:	74 63                	je     14000224d <do_pseudo_reloc+0x34b>
   1400021ea:	83 f8 40             	cmp    eax,0x40
   1400021ed:	77 75                	ja     140002264 <do_pseudo_reloc+0x362>
   1400021ef:	83 f8 20             	cmp    eax,0x20
   1400021f2:	74 41                	je     140002235 <do_pseudo_reloc+0x333>
   1400021f4:	83 f8 20             	cmp    eax,0x20
   1400021f7:	77 6b                	ja     140002264 <do_pseudo_reloc+0x362>
   1400021f9:	83 f8 08             	cmp    eax,0x8
   1400021fc:	74 07                	je     140002205 <do_pseudo_reloc+0x303>
   1400021fe:	83 f8 10             	cmp    eax,0x10
   140002201:	74 1a                	je     14000221d <do_pseudo_reloc+0x31b>
   140002203:	eb 5f                	jmp    140002264 <do_pseudo_reloc+0x362>
   140002205:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002209:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000220d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002213:	48 89 c1             	mov    rcx,rax
   140002216:	e8 a0 fc ff ff       	call   140001ebb <__write_memory>
   14000221b:	eb 47                	jmp    140002264 <do_pseudo_reloc+0x362>
   14000221d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002221:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002225:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000222b:	48 89 c1             	mov    rcx,rax
   14000222e:	e8 88 fc ff ff       	call   140001ebb <__write_memory>
   140002233:	eb 2f                	jmp    140002264 <do_pseudo_reloc+0x362>
   140002235:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002239:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000223d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002243:	48 89 c1             	mov    rcx,rax
   140002246:	e8 70 fc ff ff       	call   140001ebb <__write_memory>
   14000224b:	eb 17                	jmp    140002264 <do_pseudo_reloc+0x362>
   14000224d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002251:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002255:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000225b:	48 89 c1             	mov    rcx,rax
   14000225e:	e8 58 fc ff ff       	call   140001ebb <__write_memory>
   140002263:	90                   	nop
   140002264:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   140002269:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000226d:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002271:	0f 82 8d fd ff ff    	jb     140002004 <do_pseudo_reloc+0x102>
   140002277:	eb 01                	jmp    14000227a <do_pseudo_reloc+0x378>
   140002279:	90                   	nop
   14000227a:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   14000227e:	5d                   	pop    rbp
   14000227f:	c3                   	ret

0000000140002280 <_pei386_runtime_relocator>:
   140002280:	55                   	push   rbp
   140002281:	48 89 e5             	mov    rbp,rsp
   140002284:	48 83 ec 30          	sub    rsp,0x30
   140002288:	8b 05 5e 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e5e]        # 1400090ec <was_init.0>
   14000228e:	85 c0                	test   eax,eax
   140002290:	0f 85 88 00 00 00    	jne    14000231e <_pei386_runtime_relocator+0x9e>
   140002296:	8b 05 50 6e 00 00    	mov    eax,DWORD PTR [rip+0x6e50]        # 1400090ec <was_init.0>
   14000229c:	83 c0 01             	add    eax,0x1
   14000229f:	89 05 47 6e 00 00    	mov    DWORD PTR [rip+0x6e47],eax        # 1400090ec <was_init.0>
   1400022a5:	e8 21 0b 00 00       	call   140002dcb <__mingw_GetSectionCount>
   1400022aa:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400022ad:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400022b0:	48 63 d0             	movsxd rdx,eax
   1400022b3:	48 89 d0             	mov    rax,rdx
   1400022b6:	48 c1 e0 02          	shl    rax,0x2
   1400022ba:	48 01 d0             	add    rax,rdx
   1400022bd:	48 c1 e0 03          	shl    rax,0x3
   1400022c1:	48 83 c0 0f          	add    rax,0xf
   1400022c5:	48 c1 e8 04          	shr    rax,0x4
   1400022c9:	48 c1 e0 04          	shl    rax,0x4
   1400022cd:	e8 8e 0d 00 00       	call   140003060 <___chkstk_ms>
   1400022d2:	48 29 c4             	sub    rsp,rax
   1400022d5:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400022da:	48 83 c0 0f          	add    rax,0xf
   1400022de:	48 c1 e8 04          	shr    rax,0x4
   1400022e2:	48 c1 e0 04          	shl    rax,0x4
   1400022e6:	48 89 05 f3 6d 00 00 	mov    QWORD PTR [rip+0x6df3],rax        # 1400090e0 <the_secs>
   1400022ed:	c7 05 f1 6d 00 00 00 	mov    DWORD PTR [rip+0x6df1],0x0        # 1400090e8 <maxSections>
   1400022f4:	00 00 00 
   1400022f7:	48 8b 0d c2 30 00 00 	mov    rcx,QWORD PTR [rip+0x30c2]        # 1400053c0 <.refptr.__ImageBase>
   1400022fe:	48 8b 15 cb 30 00 00 	mov    rdx,QWORD PTR [rip+0x30cb]        # 1400053d0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002305:	48 8b 05 d4 30 00 00 	mov    rax,QWORD PTR [rip+0x30d4]        # 1400053e0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000230c:	49 89 c8             	mov    r8,rcx
   14000230f:	48 89 c1             	mov    rcx,rax
   140002312:	e8 eb fb ff ff       	call   140001f02 <do_pseudo_reloc>
   140002317:	e8 c7 fa ff ff       	call   140001de3 <restore_modified_sections>
   14000231c:	eb 01                	jmp    14000231f <_pei386_runtime_relocator+0x9f>
   14000231e:	90                   	nop
   14000231f:	48 89 ec             	mov    rsp,rbp
   140002322:	5d                   	pop    rbp
   140002323:	c3                   	ret
   140002324:	90                   	nop
   140002325:	90                   	nop
   140002326:	90                   	nop
   140002327:	90                   	nop
   140002328:	90                   	nop
   140002329:	90                   	nop
   14000232a:	90                   	nop
   14000232b:	90                   	nop
   14000232c:	90                   	nop
   14000232d:	90                   	nop
   14000232e:	90                   	nop
   14000232f:	90                   	nop

0000000140002330 <__mingw_raise_matherr>:
   140002330:	55                   	push   rbp
   140002331:	48 89 e5             	mov    rbp,rsp
   140002334:	48 83 ec 50          	sub    rsp,0x50
   140002338:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000233b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000233f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002344:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002349:	48 8b 05 a0 6d 00 00 	mov    rax,QWORD PTR [rip+0x6da0]        # 1400090f0 <stUserMathErr>
   140002350:	48 85 c0             	test   rax,rax
   140002353:	74 3e                	je     140002393 <__mingw_raise_matherr+0x63>
   140002355:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002358:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000235b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000235f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002363:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140002368:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   14000236d:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   140002372:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   140002377:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   14000237c:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140002381:	48 8b 15 68 6d 00 00 	mov    rdx,QWORD PTR [rip+0x6d68]        # 1400090f0 <stUserMathErr>
   140002388:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000238c:	48 89 c1             	mov    rcx,rax
   14000238f:	ff d2                	call   rdx
   140002391:	eb 01                	jmp    140002394 <__mingw_raise_matherr+0x64>
   140002393:	90                   	nop
   140002394:	48 83 c4 50          	add    rsp,0x50
   140002398:	5d                   	pop    rbp
   140002399:	c3                   	ret

000000014000239a <__mingw_setusermatherr>:
   14000239a:	55                   	push   rbp
   14000239b:	48 89 e5             	mov    rbp,rsp
   14000239e:	48 83 ec 20          	sub    rsp,0x20
   1400023a2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023a6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023aa:	48 89 05 3f 6d 00 00 	mov    QWORD PTR [rip+0x6d3f],rax        # 1400090f0 <stUserMathErr>
   1400023b1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023b5:	48 89 c1             	mov    rcx,rax
   1400023b8:	e8 23 0e 00 00       	call   1400031e0 <__setusermatherr>
   1400023bd:	90                   	nop
   1400023be:	48 83 c4 20          	add    rsp,0x20
   1400023c2:	5d                   	pop    rbp
   1400023c3:	c3                   	ret
   1400023c4:	90                   	nop
   1400023c5:	90                   	nop
   1400023c6:	90                   	nop
   1400023c7:	90                   	nop
   1400023c8:	90                   	nop
   1400023c9:	90                   	nop
   1400023ca:	90                   	nop
   1400023cb:	90                   	nop
   1400023cc:	90                   	nop
   1400023cd:	90                   	nop
   1400023ce:	90                   	nop
   1400023cf:	90                   	nop

00000001400023d0 <__mingw_SEH_error_handler>:
   1400023d0:	55                   	push   rbp
   1400023d1:	48 89 e5             	mov    rbp,rsp
   1400023d4:	48 83 ec 30          	sub    rsp,0x30
   1400023d8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023dc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400023e0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400023e4:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400023e8:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400023ef:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   1400023f6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023fa:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   1400023fd:	83 e0 02             	and    eax,0x2
   140002400:	85 c0                	test   eax,eax
   140002402:	74 0a                	je     14000240e <__mingw_SEH_error_handler+0x3e>
   140002404:	b8 01 00 00 00       	mov    eax,0x1
   140002409:	e9 16 02 00 00       	jmp    140002624 <__mingw_SEH_error_handler+0x254>
   14000240e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002412:	8b 00                	mov    eax,DWORD PTR [rax]
   140002414:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002419:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000241e:	75 18                	jne    140002438 <__mingw_SEH_error_handler+0x68>
   140002420:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002424:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002427:	83 e0 01             	and    eax,0x1
   14000242a:	85 c0                	test   eax,eax
   14000242c:	75 0a                	jne    140002438 <__mingw_SEH_error_handler+0x68>
   14000242e:	b8 00 00 00 00       	mov    eax,0x0
   140002433:	e9 ec 01 00 00       	jmp    140002624 <__mingw_SEH_error_handler+0x254>
   140002438:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000243c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000243e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002443:	0f 84 12 01 00 00    	je     14000255b <__mingw_SEH_error_handler+0x18b>
   140002449:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000244e:	0f 87 c3 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   140002454:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002459:	0f 87 b8 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   14000245f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002464:	0f 83 4c 01 00 00    	jae    1400025b6 <__mingw_SEH_error_handler+0x1e6>
   14000246a:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000246f:	0f 84 3a 01 00 00    	je     1400025af <__mingw_SEH_error_handler+0x1df>
   140002475:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000247a:	0f 87 97 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   140002480:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002485:	0f 84 83 01 00 00    	je     14000260e <__mingw_SEH_error_handler+0x23e>
   14000248b:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   140002490:	0f 87 81 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   140002496:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   14000249b:	0f 87 76 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   1400024a1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400024a6:	0f 83 03 01 00 00    	jae    1400025af <__mingw_SEH_error_handler+0x1df>
   1400024ac:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024b1:	0f 84 57 01 00 00    	je     14000260e <__mingw_SEH_error_handler+0x23e>
   1400024b7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024bc:	0f 87 55 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   1400024c2:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024c7:	0f 84 8e 00 00 00    	je     14000255b <__mingw_SEH_error_handler+0x18b>
   1400024cd:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024d2:	0f 87 3f 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   1400024d8:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400024dd:	0f 84 2b 01 00 00    	je     14000260e <__mingw_SEH_error_handler+0x23e>
   1400024e3:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400024e8:	0f 87 29 01 00 00    	ja     140002617 <__mingw_SEH_error_handler+0x247>
   1400024ee:	3d 02 00 00 80       	cmp    eax,0x80000002
   1400024f3:	0f 84 15 01 00 00    	je     14000260e <__mingw_SEH_error_handler+0x23e>
   1400024f9:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   1400024fe:	0f 85 13 01 00 00    	jne    140002617 <__mingw_SEH_error_handler+0x247>
   140002504:	ba 00 00 00 00       	mov    edx,0x0
   140002509:	b9 0b 00 00 00       	mov    ecx,0xb
   14000250e:	e8 3d 0d 00 00       	call   140003250 <signal>
   140002513:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002517:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000251c:	75 1b                	jne    140002539 <__mingw_SEH_error_handler+0x169>
   14000251e:	ba 01 00 00 00       	mov    edx,0x1
   140002523:	b9 0b 00 00 00       	mov    ecx,0xb
   140002528:	e8 23 0d 00 00       	call   140003250 <signal>
   14000252d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002534:	e9 e1 00 00 00       	jmp    14000261a <__mingw_SEH_error_handler+0x24a>
   140002539:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000253e:	0f 84 d6 00 00 00    	je     14000261a <__mingw_SEH_error_handler+0x24a>
   140002544:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002548:	b9 0b 00 00 00       	mov    ecx,0xb
   14000254d:	ff d0                	call   rax
   14000254f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002556:	e9 bf 00 00 00       	jmp    14000261a <__mingw_SEH_error_handler+0x24a>
   14000255b:	ba 00 00 00 00       	mov    edx,0x0
   140002560:	b9 04 00 00 00       	mov    ecx,0x4
   140002565:	e8 e6 0c 00 00       	call   140003250 <signal>
   14000256a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000256e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002573:	75 1b                	jne    140002590 <__mingw_SEH_error_handler+0x1c0>
   140002575:	ba 01 00 00 00       	mov    edx,0x1
   14000257a:	b9 04 00 00 00       	mov    ecx,0x4
   14000257f:	e8 cc 0c 00 00       	call   140003250 <signal>
   140002584:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000258b:	e9 8d 00 00 00       	jmp    14000261d <__mingw_SEH_error_handler+0x24d>
   140002590:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002595:	0f 84 82 00 00 00    	je     14000261d <__mingw_SEH_error_handler+0x24d>
   14000259b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000259f:	b9 04 00 00 00       	mov    ecx,0x4
   1400025a4:	ff d0                	call   rax
   1400025a6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025ad:	eb 6e                	jmp    14000261d <__mingw_SEH_error_handler+0x24d>
   1400025af:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400025b6:	ba 00 00 00 00       	mov    edx,0x0
   1400025bb:	b9 08 00 00 00       	mov    ecx,0x8
   1400025c0:	e8 8b 0c 00 00       	call   140003250 <signal>
   1400025c5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025c9:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025ce:	75 23                	jne    1400025f3 <__mingw_SEH_error_handler+0x223>
   1400025d0:	ba 01 00 00 00       	mov    edx,0x1
   1400025d5:	b9 08 00 00 00       	mov    ecx,0x8
   1400025da:	e8 71 0c 00 00       	call   140003250 <signal>
   1400025df:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400025e3:	74 05                	je     1400025ea <__mingw_SEH_error_handler+0x21a>
   1400025e5:	e8 a6 05 00 00       	call   140002b90 <_fpreset>
   1400025ea:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025f1:	eb 2d                	jmp    140002620 <__mingw_SEH_error_handler+0x250>
   1400025f3:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400025f8:	74 26                	je     140002620 <__mingw_SEH_error_handler+0x250>
   1400025fa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025fe:	b9 08 00 00 00       	mov    ecx,0x8
   140002603:	ff d0                	call   rax
   140002605:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000260c:	eb 12                	jmp    140002620 <__mingw_SEH_error_handler+0x250>
   14000260e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002615:	eb 0a                	jmp    140002621 <__mingw_SEH_error_handler+0x251>
   140002617:	90                   	nop
   140002618:	eb 07                	jmp    140002621 <__mingw_SEH_error_handler+0x251>
   14000261a:	90                   	nop
   14000261b:	eb 04                	jmp    140002621 <__mingw_SEH_error_handler+0x251>
   14000261d:	90                   	nop
   14000261e:	eb 01                	jmp    140002621 <__mingw_SEH_error_handler+0x251>
   140002620:	90                   	nop
   140002621:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002624:	48 83 c4 30          	add    rsp,0x30
   140002628:	5d                   	pop    rbp
   140002629:	c3                   	ret

000000014000262a <_gnu_exception_handler>:
   14000262a:	55                   	push   rbp
   14000262b:	48 89 e5             	mov    rbp,rsp
   14000262e:	48 83 ec 30          	sub    rsp,0x30
   140002632:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002636:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000263d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002644:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002648:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000264b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000264d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002652:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002657:	75 1b                	jne    140002674 <_gnu_exception_handler+0x4a>
   140002659:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000265d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002660:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002663:	83 e0 01             	and    eax,0x1
   140002666:	85 c0                	test   eax,eax
   140002668:	75 0a                	jne    140002674 <_gnu_exception_handler+0x4a>
   14000266a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000266f:	e9 14 02 00 00       	jmp    140002888 <_gnu_exception_handler+0x25e>
   140002674:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002678:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000267b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000267d:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002682:	0f 84 12 01 00 00    	je     14000279a <_gnu_exception_handler+0x170>
   140002688:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000268d:	0f 87 c3 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   140002693:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002698:	0f 87 b8 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   14000269e:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400026a3:	0f 83 4c 01 00 00    	jae    1400027f5 <_gnu_exception_handler+0x1cb>
   1400026a9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026ae:	0f 84 3a 01 00 00    	je     1400027ee <_gnu_exception_handler+0x1c4>
   1400026b4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026b9:	0f 87 97 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   1400026bf:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026c4:	0f 84 83 01 00 00    	je     14000284d <_gnu_exception_handler+0x223>
   1400026ca:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026cf:	0f 87 81 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   1400026d5:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400026da:	0f 87 76 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   1400026e0:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400026e5:	0f 83 03 01 00 00    	jae    1400027ee <_gnu_exception_handler+0x1c4>
   1400026eb:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400026f0:	0f 84 57 01 00 00    	je     14000284d <_gnu_exception_handler+0x223>
   1400026f6:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400026fb:	0f 87 55 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   140002701:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002706:	0f 84 8e 00 00 00    	je     14000279a <_gnu_exception_handler+0x170>
   14000270c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002711:	0f 87 3f 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   140002717:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000271c:	0f 84 2b 01 00 00    	je     14000284d <_gnu_exception_handler+0x223>
   140002722:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002727:	0f 87 29 01 00 00    	ja     140002856 <_gnu_exception_handler+0x22c>
   14000272d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002732:	0f 84 15 01 00 00    	je     14000284d <_gnu_exception_handler+0x223>
   140002738:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000273d:	0f 85 13 01 00 00    	jne    140002856 <_gnu_exception_handler+0x22c>
   140002743:	ba 00 00 00 00       	mov    edx,0x0
   140002748:	b9 0b 00 00 00       	mov    ecx,0xb
   14000274d:	e8 fe 0a 00 00       	call   140003250 <signal>
   140002752:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002756:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000275b:	75 1b                	jne    140002778 <_gnu_exception_handler+0x14e>
   14000275d:	ba 01 00 00 00       	mov    edx,0x1
   140002762:	b9 0b 00 00 00       	mov    ecx,0xb
   140002767:	e8 e4 0a 00 00       	call   140003250 <signal>
   14000276c:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002773:	e9 e1 00 00 00       	jmp    140002859 <_gnu_exception_handler+0x22f>
   140002778:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000277d:	0f 84 d6 00 00 00    	je     140002859 <_gnu_exception_handler+0x22f>
   140002783:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002787:	b9 0b 00 00 00       	mov    ecx,0xb
   14000278c:	ff d0                	call   rax
   14000278e:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002795:	e9 bf 00 00 00       	jmp    140002859 <_gnu_exception_handler+0x22f>
   14000279a:	ba 00 00 00 00       	mov    edx,0x0
   14000279f:	b9 04 00 00 00       	mov    ecx,0x4
   1400027a4:	e8 a7 0a 00 00       	call   140003250 <signal>
   1400027a9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027ad:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027b2:	75 1b                	jne    1400027cf <_gnu_exception_handler+0x1a5>
   1400027b4:	ba 01 00 00 00       	mov    edx,0x1
   1400027b9:	b9 04 00 00 00       	mov    ecx,0x4
   1400027be:	e8 8d 0a 00 00       	call   140003250 <signal>
   1400027c3:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027ca:	e9 8d 00 00 00       	jmp    14000285c <_gnu_exception_handler+0x232>
   1400027cf:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027d4:	0f 84 82 00 00 00    	je     14000285c <_gnu_exception_handler+0x232>
   1400027da:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027de:	b9 04 00 00 00       	mov    ecx,0x4
   1400027e3:	ff d0                	call   rax
   1400027e5:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027ec:	eb 6e                	jmp    14000285c <_gnu_exception_handler+0x232>
   1400027ee:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400027f5:	ba 00 00 00 00       	mov    edx,0x0
   1400027fa:	b9 08 00 00 00       	mov    ecx,0x8
   1400027ff:	e8 4c 0a 00 00       	call   140003250 <signal>
   140002804:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002808:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000280d:	75 23                	jne    140002832 <_gnu_exception_handler+0x208>
   14000280f:	ba 01 00 00 00       	mov    edx,0x1
   140002814:	b9 08 00 00 00       	mov    ecx,0x8
   140002819:	e8 32 0a 00 00       	call   140003250 <signal>
   14000281e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002822:	74 05                	je     140002829 <_gnu_exception_handler+0x1ff>
   140002824:	e8 67 03 00 00       	call   140002b90 <_fpreset>
   140002829:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002830:	eb 2d                	jmp    14000285f <_gnu_exception_handler+0x235>
   140002832:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002837:	74 26                	je     14000285f <_gnu_exception_handler+0x235>
   140002839:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000283d:	b9 08 00 00 00       	mov    ecx,0x8
   140002842:	ff d0                	call   rax
   140002844:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000284b:	eb 12                	jmp    14000285f <_gnu_exception_handler+0x235>
   14000284d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002854:	eb 0a                	jmp    140002860 <_gnu_exception_handler+0x236>
   140002856:	90                   	nop
   140002857:	eb 07                	jmp    140002860 <_gnu_exception_handler+0x236>
   140002859:	90                   	nop
   14000285a:	eb 04                	jmp    140002860 <_gnu_exception_handler+0x236>
   14000285c:	90                   	nop
   14000285d:	eb 01                	jmp    140002860 <_gnu_exception_handler+0x236>
   14000285f:	90                   	nop
   140002860:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002864:	75 1f                	jne    140002885 <_gnu_exception_handler+0x25b>
   140002866:	48 8b 05 a3 68 00 00 	mov    rax,QWORD PTR [rip+0x68a3]        # 140009110 <__mingw_oldexcpt_handler>
   14000286d:	48 85 c0             	test   rax,rax
   140002870:	74 13                	je     140002885 <_gnu_exception_handler+0x25b>
   140002872:	48 8b 15 97 68 00 00 	mov    rdx,QWORD PTR [rip+0x6897]        # 140009110 <__mingw_oldexcpt_handler>
   140002879:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000287d:	48 89 c1             	mov    rcx,rax
   140002880:	ff d2                	call   rdx
   140002882:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140002885:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002888:	48 83 c4 30          	add    rsp,0x30
   14000288c:	5d                   	pop    rbp
   14000288d:	c3                   	ret
   14000288e:	90                   	nop
   14000288f:	90                   	nop

0000000140002890 <___w64_mingwthr_add_key_dtor>:
   140002890:	55                   	push   rbp
   140002891:	48 89 e5             	mov    rbp,rsp
   140002894:	48 83 ec 30          	sub    rsp,0x30
   140002898:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000289b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000289f:	8b 05 a3 68 00 00    	mov    eax,DWORD PTR [rip+0x68a3]        # 140009148 <__mingwthr_cs_init>
   1400028a5:	85 c0                	test   eax,eax
   1400028a7:	75 07                	jne    1400028b0 <___w64_mingwthr_add_key_dtor+0x20>
   1400028a9:	b8 00 00 00 00       	mov    eax,0x0
   1400028ae:	eb 7b                	jmp    14000292b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028b0:	ba 18 00 00 00       	mov    edx,0x18
   1400028b5:	b9 01 00 00 00       	mov    ecx,0x1
   1400028ba:	e8 51 09 00 00       	call   140003210 <calloc>
   1400028bf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400028c3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400028c8:	75 07                	jne    1400028d1 <___w64_mingwthr_add_key_dtor+0x41>
   1400028ca:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400028cf:	eb 5a                	jmp    14000292b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028d1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028d5:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400028d8:	89 10                	mov    DWORD PTR [rax],edx
   1400028da:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028de:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400028e2:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   1400028e6:	48 8d 05 33 68 00 00 	lea    rax,[rip+0x6833]        # 140009120 <__mingwthr_cs>
   1400028ed:	48 89 c1             	mov    rcx,rax
   1400028f0:	48 8b 05 61 79 00 00 	mov    rax,QWORD PTR [rip+0x7961]        # 14000a258 <__imp_EnterCriticalSection>
   1400028f7:	ff d0                	call   rax
   1400028f9:	48 8b 15 50 68 00 00 	mov    rdx,QWORD PTR [rip+0x6850]        # 140009150 <key_dtor_list>
   140002900:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002904:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002908:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000290c:	48 89 05 3d 68 00 00 	mov    QWORD PTR [rip+0x683d],rax        # 140009150 <key_dtor_list>
   140002913:	48 8d 05 06 68 00 00 	lea    rax,[rip+0x6806]        # 140009120 <__mingwthr_cs>
   14000291a:	48 89 c1             	mov    rcx,rax
   14000291d:	48 8b 05 64 79 00 00 	mov    rax,QWORD PTR [rip+0x7964]        # 14000a288 <__imp_LeaveCriticalSection>
   140002924:	ff d0                	call   rax
   140002926:	b8 00 00 00 00       	mov    eax,0x0
   14000292b:	48 83 c4 30          	add    rsp,0x30
   14000292f:	5d                   	pop    rbp
   140002930:	c3                   	ret

0000000140002931 <___w64_mingwthr_remove_key_dtor>:
   140002931:	55                   	push   rbp
   140002932:	48 89 e5             	mov    rbp,rsp
   140002935:	48 83 ec 30          	sub    rsp,0x30
   140002939:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000293c:	8b 05 06 68 00 00    	mov    eax,DWORD PTR [rip+0x6806]        # 140009148 <__mingwthr_cs_init>
   140002942:	85 c0                	test   eax,eax
   140002944:	75 0a                	jne    140002950 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002946:	b8 00 00 00 00       	mov    eax,0x0
   14000294b:	e9 9c 00 00 00       	jmp    1400029ec <___w64_mingwthr_remove_key_dtor+0xbb>
   140002950:	48 8d 05 c9 67 00 00 	lea    rax,[rip+0x67c9]        # 140009120 <__mingwthr_cs>
   140002957:	48 89 c1             	mov    rcx,rax
   14000295a:	48 8b 05 f7 78 00 00 	mov    rax,QWORD PTR [rip+0x78f7]        # 14000a258 <__imp_EnterCriticalSection>
   140002961:	ff d0                	call   rax
   140002963:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   14000296a:	00 
   14000296b:	48 8b 05 de 67 00 00 	mov    rax,QWORD PTR [rip+0x67de]        # 140009150 <key_dtor_list>
   140002972:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002976:	eb 55                	jmp    1400029cd <___w64_mingwthr_remove_key_dtor+0x9c>
   140002978:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000297c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000297e:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140002981:	75 36                	jne    1400029b9 <___w64_mingwthr_remove_key_dtor+0x88>
   140002983:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002988:	75 11                	jne    14000299b <___w64_mingwthr_remove_key_dtor+0x6a>
   14000298a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000298e:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002992:	48 89 05 b7 67 00 00 	mov    QWORD PTR [rip+0x67b7],rax        # 140009150 <key_dtor_list>
   140002999:	eb 10                	jmp    1400029ab <___w64_mingwthr_remove_key_dtor+0x7a>
   14000299b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000299f:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   1400029a3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400029a7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   1400029ab:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029af:	48 89 c1             	mov    rcx,rax
   1400029b2:	e8 79 08 00 00       	call   140003230 <free>
   1400029b7:	eb 1b                	jmp    1400029d4 <___w64_mingwthr_remove_key_dtor+0xa3>
   1400029b9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029bd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400029c1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029c5:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029c9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029cd:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400029d2:	75 a4                	jne    140002978 <___w64_mingwthr_remove_key_dtor+0x47>
   1400029d4:	48 8d 05 45 67 00 00 	lea    rax,[rip+0x6745]        # 140009120 <__mingwthr_cs>
   1400029db:	48 89 c1             	mov    rcx,rax
   1400029de:	48 8b 05 a3 78 00 00 	mov    rax,QWORD PTR [rip+0x78a3]        # 14000a288 <__imp_LeaveCriticalSection>
   1400029e5:	ff d0                	call   rax
   1400029e7:	b8 00 00 00 00       	mov    eax,0x0
   1400029ec:	48 83 c4 30          	add    rsp,0x30
   1400029f0:	5d                   	pop    rbp
   1400029f1:	c3                   	ret

00000001400029f2 <__mingwthr_run_key_dtors>:
   1400029f2:	55                   	push   rbp
   1400029f3:	48 89 e5             	mov    rbp,rsp
   1400029f6:	48 83 ec 30          	sub    rsp,0x30
   1400029fa:	8b 05 48 67 00 00    	mov    eax,DWORD PTR [rip+0x6748]        # 140009148 <__mingwthr_cs_init>
   140002a00:	85 c0                	test   eax,eax
   140002a02:	0f 84 82 00 00 00    	je     140002a8a <__mingwthr_run_key_dtors+0x98>
   140002a08:	48 8d 05 11 67 00 00 	lea    rax,[rip+0x6711]        # 140009120 <__mingwthr_cs>
   140002a0f:	48 89 c1             	mov    rcx,rax
   140002a12:	48 8b 05 3f 78 00 00 	mov    rax,QWORD PTR [rip+0x783f]        # 14000a258 <__imp_EnterCriticalSection>
   140002a19:	ff d0                	call   rax
   140002a1b:	48 8b 05 2e 67 00 00 	mov    rax,QWORD PTR [rip+0x672e]        # 140009150 <key_dtor_list>
   140002a22:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a26:	eb 46                	jmp    140002a6e <__mingwthr_run_key_dtors+0x7c>
   140002a28:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a2c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a2e:	89 c1                	mov    ecx,eax
   140002a30:	48 8b 05 71 78 00 00 	mov    rax,QWORD PTR [rip+0x7871]        # 14000a2a8 <__imp_TlsGetValue>
   140002a37:	ff d0                	call   rax
   140002a39:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a3d:	48 8b 05 24 78 00 00 	mov    rax,QWORD PTR [rip+0x7824]        # 14000a268 <__imp_GetLastError>
   140002a44:	ff d0                	call   rax
   140002a46:	85 c0                	test   eax,eax
   140002a48:	75 18                	jne    140002a62 <__mingwthr_run_key_dtors+0x70>
   140002a4a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a4f:	74 11                	je     140002a62 <__mingwthr_run_key_dtors+0x70>
   140002a51:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a55:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002a59:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a5d:	48 89 c1             	mov    rcx,rax
   140002a60:	ff d2                	call   rdx
   140002a62:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a66:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002a6a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a6e:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002a73:	75 b3                	jne    140002a28 <__mingwthr_run_key_dtors+0x36>
   140002a75:	48 8d 05 a4 66 00 00 	lea    rax,[rip+0x66a4]        # 140009120 <__mingwthr_cs>
   140002a7c:	48 89 c1             	mov    rcx,rax
   140002a7f:	48 8b 05 02 78 00 00 	mov    rax,QWORD PTR [rip+0x7802]        # 14000a288 <__imp_LeaveCriticalSection>
   140002a86:	ff d0                	call   rax
   140002a88:	eb 01                	jmp    140002a8b <__mingwthr_run_key_dtors+0x99>
   140002a8a:	90                   	nop
   140002a8b:	48 83 c4 30          	add    rsp,0x30
   140002a8f:	5d                   	pop    rbp
   140002a90:	c3                   	ret

0000000140002a91 <__mingw_TLScallback>:
   140002a91:	55                   	push   rbp
   140002a92:	48 89 e5             	mov    rbp,rsp
   140002a95:	48 83 ec 30          	sub    rsp,0x30
   140002a99:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002a9d:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002aa0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002aa4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002aa8:	0f 84 cc 00 00 00    	je     140002b7a <__mingw_TLScallback+0xe9>
   140002aae:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ab2:	0f 87 ca 00 00 00    	ja     140002b82 <__mingw_TLScallback+0xf1>
   140002ab8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002abc:	0f 84 b1 00 00 00    	je     140002b73 <__mingw_TLScallback+0xe2>
   140002ac2:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002ac6:	0f 87 b6 00 00 00    	ja     140002b82 <__mingw_TLScallback+0xf1>
   140002acc:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002ad0:	74 33                	je     140002b05 <__mingw_TLScallback+0x74>
   140002ad2:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002ad6:	0f 85 a6 00 00 00    	jne    140002b82 <__mingw_TLScallback+0xf1>
   140002adc:	8b 05 66 66 00 00    	mov    eax,DWORD PTR [rip+0x6666]        # 140009148 <__mingwthr_cs_init>
   140002ae2:	85 c0                	test   eax,eax
   140002ae4:	75 13                	jne    140002af9 <__mingw_TLScallback+0x68>
   140002ae6:	48 8d 05 33 66 00 00 	lea    rax,[rip+0x6633]        # 140009120 <__mingwthr_cs>
   140002aed:	48 89 c1             	mov    rcx,rax
   140002af0:	48 8b 05 89 77 00 00 	mov    rax,QWORD PTR [rip+0x7789]        # 14000a280 <__imp_InitializeCriticalSection>
   140002af7:	ff d0                	call   rax
   140002af9:	c7 05 45 66 00 00 01 	mov    DWORD PTR [rip+0x6645],0x1        # 140009148 <__mingwthr_cs_init>
   140002b00:	00 00 00 
   140002b03:	eb 7d                	jmp    140002b82 <__mingw_TLScallback+0xf1>
   140002b05:	e8 e8 fe ff ff       	call   1400029f2 <__mingwthr_run_key_dtors>
   140002b0a:	8b 05 38 66 00 00    	mov    eax,DWORD PTR [rip+0x6638]        # 140009148 <__mingwthr_cs_init>
   140002b10:	83 f8 01             	cmp    eax,0x1
   140002b13:	75 6c                	jne    140002b81 <__mingw_TLScallback+0xf0>
   140002b15:	48 8b 05 34 66 00 00 	mov    rax,QWORD PTR [rip+0x6634]        # 140009150 <key_dtor_list>
   140002b1c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b20:	eb 20                	jmp    140002b42 <__mingw_TLScallback+0xb1>
   140002b22:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b26:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b2a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b2e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b32:	48 89 c1             	mov    rcx,rax
   140002b35:	e8 f6 06 00 00       	call   140003230 <free>
   140002b3a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b3e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b42:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b47:	75 d9                	jne    140002b22 <__mingw_TLScallback+0x91>
   140002b49:	48 c7 05 fc 65 00 00 	mov    QWORD PTR [rip+0x65fc],0x0        # 140009150 <key_dtor_list>
   140002b50:	00 00 00 00 
   140002b54:	c7 05 ea 65 00 00 00 	mov    DWORD PTR [rip+0x65ea],0x0        # 140009148 <__mingwthr_cs_init>
   140002b5b:	00 00 00 
   140002b5e:	48 8d 05 bb 65 00 00 	lea    rax,[rip+0x65bb]        # 140009120 <__mingwthr_cs>
   140002b65:	48 89 c1             	mov    rcx,rax
   140002b68:	48 8b 05 e1 76 00 00 	mov    rax,QWORD PTR [rip+0x76e1]        # 14000a250 <__imp_DeleteCriticalSection>
   140002b6f:	ff d0                	call   rax
   140002b71:	eb 0e                	jmp    140002b81 <__mingw_TLScallback+0xf0>
   140002b73:	e8 18 00 00 00       	call   140002b90 <_fpreset>
   140002b78:	eb 08                	jmp    140002b82 <__mingw_TLScallback+0xf1>
   140002b7a:	e8 73 fe ff ff       	call   1400029f2 <__mingwthr_run_key_dtors>
   140002b7f:	eb 01                	jmp    140002b82 <__mingw_TLScallback+0xf1>
   140002b81:	90                   	nop
   140002b82:	b8 01 00 00 00       	mov    eax,0x1
   140002b87:	48 83 c4 30          	add    rsp,0x30
   140002b8b:	5d                   	pop    rbp
   140002b8c:	c3                   	ret
   140002b8d:	90                   	nop
   140002b8e:	90                   	nop
   140002b8f:	90                   	nop

0000000140002b90 <_fpreset>:
   140002b90:	55                   	push   rbp
   140002b91:	48 89 e5             	mov    rbp,rsp
   140002b94:	db e3                	fninit
   140002b96:	90                   	nop
   140002b97:	5d                   	pop    rbp
   140002b98:	c3                   	ret
   140002b99:	90                   	nop
   140002b9a:	90                   	nop
   140002b9b:	90                   	nop
   140002b9c:	90                   	nop
   140002b9d:	90                   	nop
   140002b9e:	90                   	nop
   140002b9f:	90                   	nop

0000000140002ba0 <_ValidateImageBase>:
   140002ba0:	55                   	push   rbp
   140002ba1:	48 89 e5             	mov    rbp,rsp
   140002ba4:	48 83 ec 20          	sub    rsp,0x20
   140002ba8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002bac:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002bb0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002bb4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bb8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002bbb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002bbf:	74 07                	je     140002bc8 <_ValidateImageBase+0x28>
   140002bc1:	b8 00 00 00 00       	mov    eax,0x0
   140002bc6:	eb 4e                	jmp    140002c16 <_ValidateImageBase+0x76>
   140002bc8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bcc:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002bcf:	48 63 d0             	movsxd rdx,eax
   140002bd2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bd6:	48 01 d0             	add    rax,rdx
   140002bd9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002bdd:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002be1:	8b 00                	mov    eax,DWORD PTR [rax]
   140002be3:	3d 50 45 00 00       	cmp    eax,0x4550
   140002be8:	74 07                	je     140002bf1 <_ValidateImageBase+0x51>
   140002bea:	b8 00 00 00 00       	mov    eax,0x0
   140002bef:	eb 25                	jmp    140002c16 <_ValidateImageBase+0x76>
   140002bf1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002bf5:	48 83 c0 18          	add    rax,0x18
   140002bf9:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002bfd:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c01:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c04:	66 3d 0b 02          	cmp    ax,0x20b
   140002c08:	74 07                	je     140002c11 <_ValidateImageBase+0x71>
   140002c0a:	b8 00 00 00 00       	mov    eax,0x0
   140002c0f:	eb 05                	jmp    140002c16 <_ValidateImageBase+0x76>
   140002c11:	b8 01 00 00 00       	mov    eax,0x1
   140002c16:	48 83 c4 20          	add    rsp,0x20
   140002c1a:	5d                   	pop    rbp
   140002c1b:	c3                   	ret

0000000140002c1c <_FindPESection>:
   140002c1c:	55                   	push   rbp
   140002c1d:	48 89 e5             	mov    rbp,rsp
   140002c20:	48 83 ec 20          	sub    rsp,0x20
   140002c24:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c28:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002c2c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c30:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c33:	48 63 d0             	movsxd rdx,eax
   140002c36:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c3a:	48 01 d0             	add    rax,rdx
   140002c3d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c41:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002c48:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c4c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002c50:	0f b7 d0             	movzx  edx,ax
   140002c53:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c57:	48 01 d0             	add    rax,rdx
   140002c5a:	48 83 c0 18          	add    rax,0x18
   140002c5e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c62:	eb 36                	jmp    140002c9a <_FindPESection+0x7e>
   140002c64:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c68:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002c6b:	89 c0                	mov    eax,eax
   140002c6d:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002c71:	72 1e                	jb     140002c91 <_FindPESection+0x75>
   140002c73:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c77:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002c7a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c7e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002c81:	01 d0                	add    eax,edx
   140002c83:	89 c0                	mov    eax,eax
   140002c85:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002c89:	73 06                	jae    140002c91 <_FindPESection+0x75>
   140002c8b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c8f:	eb 1e                	jmp    140002caf <_FindPESection+0x93>
   140002c91:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002c95:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002c9a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c9e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002ca2:	0f b7 c0             	movzx  eax,ax
   140002ca5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002ca8:	72 ba                	jb     140002c64 <_FindPESection+0x48>
   140002caa:	b8 00 00 00 00       	mov    eax,0x0
   140002caf:	48 83 c4 20          	add    rsp,0x20
   140002cb3:	5d                   	pop    rbp
   140002cb4:	c3                   	ret

0000000140002cb5 <_FindPESectionByName>:
   140002cb5:	55                   	push   rbp
   140002cb6:	48 89 e5             	mov    rbp,rsp
   140002cb9:	48 83 ec 40          	sub    rsp,0x40
   140002cbd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002cc1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002cc5:	48 89 c1             	mov    rcx,rax
   140002cc8:	e8 8b 05 00 00       	call   140003258 <strlen>
   140002ccd:	48 83 f8 08          	cmp    rax,0x8
   140002cd1:	76 0a                	jbe    140002cdd <_FindPESectionByName+0x28>
   140002cd3:	b8 00 00 00 00       	mov    eax,0x0
   140002cd8:	e9 98 00 00 00       	jmp    140002d75 <_FindPESectionByName+0xc0>
   140002cdd:	48 8b 05 dc 26 00 00 	mov    rax,QWORD PTR [rip+0x26dc]        # 1400053c0 <.refptr.__ImageBase>
   140002ce4:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002ce8:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cec:	48 89 c1             	mov    rcx,rax
   140002cef:	e8 ac fe ff ff       	call   140002ba0 <_ValidateImageBase>
   140002cf4:	85 c0                	test   eax,eax
   140002cf6:	75 07                	jne    140002cff <_FindPESectionByName+0x4a>
   140002cf8:	b8 00 00 00 00       	mov    eax,0x0
   140002cfd:	eb 76                	jmp    140002d75 <_FindPESectionByName+0xc0>
   140002cff:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d03:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d06:	48 63 d0             	movsxd rdx,eax
   140002d09:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d0d:	48 01 d0             	add    rax,rdx
   140002d10:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002d14:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d1b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d1f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d23:	0f b7 d0             	movzx  edx,ax
   140002d26:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d2a:	48 01 d0             	add    rax,rdx
   140002d2d:	48 83 c0 18          	add    rax,0x18
   140002d31:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d35:	eb 29                	jmp    140002d60 <_FindPESectionByName+0xab>
   140002d37:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d3b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002d3f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002d45:	48 89 c1             	mov    rcx,rax
   140002d48:	e8 13 05 00 00       	call   140003260 <strncmp>
   140002d4d:	85 c0                	test   eax,eax
   140002d4f:	75 06                	jne    140002d57 <_FindPESectionByName+0xa2>
   140002d51:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d55:	eb 1e                	jmp    140002d75 <_FindPESectionByName+0xc0>
   140002d57:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002d5b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002d60:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d64:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002d68:	0f b7 c0             	movzx  eax,ax
   140002d6b:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002d6e:	72 c7                	jb     140002d37 <_FindPESectionByName+0x82>
   140002d70:	b8 00 00 00 00       	mov    eax,0x0
   140002d75:	48 83 c4 40          	add    rsp,0x40
   140002d79:	5d                   	pop    rbp
   140002d7a:	c3                   	ret

0000000140002d7b <__mingw_GetSectionForAddress>:
   140002d7b:	55                   	push   rbp
   140002d7c:	48 89 e5             	mov    rbp,rsp
   140002d7f:	48 83 ec 30          	sub    rsp,0x30
   140002d83:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002d87:	48 8b 05 32 26 00 00 	mov    rax,QWORD PTR [rip+0x2632]        # 1400053c0 <.refptr.__ImageBase>
   140002d8e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d92:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d96:	48 89 c1             	mov    rcx,rax
   140002d99:	e8 02 fe ff ff       	call   140002ba0 <_ValidateImageBase>
   140002d9e:	85 c0                	test   eax,eax
   140002da0:	75 07                	jne    140002da9 <__mingw_GetSectionForAddress+0x2e>
   140002da2:	b8 00 00 00 00       	mov    eax,0x0
   140002da7:	eb 1c                	jmp    140002dc5 <__mingw_GetSectionForAddress+0x4a>
   140002da9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002dad:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002db1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002db5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002db9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002dbd:	48 89 c1             	mov    rcx,rax
   140002dc0:	e8 57 fe ff ff       	call   140002c1c <_FindPESection>
   140002dc5:	48 83 c4 30          	add    rsp,0x30
   140002dc9:	5d                   	pop    rbp
   140002dca:	c3                   	ret

0000000140002dcb <__mingw_GetSectionCount>:
   140002dcb:	55                   	push   rbp
   140002dcc:	48 89 e5             	mov    rbp,rsp
   140002dcf:	48 83 ec 30          	sub    rsp,0x30
   140002dd3:	48 8b 05 e6 25 00 00 	mov    rax,QWORD PTR [rip+0x25e6]        # 1400053c0 <.refptr.__ImageBase>
   140002dda:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002dde:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002de2:	48 89 c1             	mov    rcx,rax
   140002de5:	e8 b6 fd ff ff       	call   140002ba0 <_ValidateImageBase>
   140002dea:	85 c0                	test   eax,eax
   140002dec:	75 07                	jne    140002df5 <__mingw_GetSectionCount+0x2a>
   140002dee:	b8 00 00 00 00       	mov    eax,0x0
   140002df3:	eb 20                	jmp    140002e15 <__mingw_GetSectionCount+0x4a>
   140002df5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002df9:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002dfc:	48 63 d0             	movsxd rdx,eax
   140002dff:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e03:	48 01 d0             	add    rax,rdx
   140002e06:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e0a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e0e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e12:	0f b7 c0             	movzx  eax,ax
   140002e15:	48 83 c4 30          	add    rsp,0x30
   140002e19:	5d                   	pop    rbp
   140002e1a:	c3                   	ret

0000000140002e1b <_FindPESectionExec>:
   140002e1b:	55                   	push   rbp
   140002e1c:	48 89 e5             	mov    rbp,rsp
   140002e1f:	48 83 ec 40          	sub    rsp,0x40
   140002e23:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e27:	48 8b 05 92 25 00 00 	mov    rax,QWORD PTR [rip+0x2592]        # 1400053c0 <.refptr.__ImageBase>
   140002e2e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e32:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e36:	48 89 c1             	mov    rcx,rax
   140002e39:	e8 62 fd ff ff       	call   140002ba0 <_ValidateImageBase>
   140002e3e:	85 c0                	test   eax,eax
   140002e40:	75 07                	jne    140002e49 <_FindPESectionExec+0x2e>
   140002e42:	b8 00 00 00 00       	mov    eax,0x0
   140002e47:	eb 78                	jmp    140002ec1 <_FindPESectionExec+0xa6>
   140002e49:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e4d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e50:	48 63 d0             	movsxd rdx,eax
   140002e53:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e57:	48 01 d0             	add    rax,rdx
   140002e5a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002e5e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002e65:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e69:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002e6d:	0f b7 d0             	movzx  edx,ax
   140002e70:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e74:	48 01 d0             	add    rax,rdx
   140002e77:	48 83 c0 18          	add    rax,0x18
   140002e7b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e7f:	eb 2b                	jmp    140002eac <_FindPESectionExec+0x91>
   140002e81:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e85:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002e88:	25 00 00 00 20       	and    eax,0x20000000
   140002e8d:	85 c0                	test   eax,eax
   140002e8f:	74 12                	je     140002ea3 <_FindPESectionExec+0x88>
   140002e91:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002e96:	75 06                	jne    140002e9e <_FindPESectionExec+0x83>
   140002e98:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e9c:	eb 23                	jmp    140002ec1 <_FindPESectionExec+0xa6>
   140002e9e:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002ea3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002ea7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002eac:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002eb0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002eb4:	0f b7 c0             	movzx  eax,ax
   140002eb7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002eba:	72 c5                	jb     140002e81 <_FindPESectionExec+0x66>
   140002ebc:	b8 00 00 00 00       	mov    eax,0x0
   140002ec1:	48 83 c4 40          	add    rsp,0x40
   140002ec5:	5d                   	pop    rbp
   140002ec6:	c3                   	ret

0000000140002ec7 <_GetPEImageBase>:
   140002ec7:	55                   	push   rbp
   140002ec8:	48 89 e5             	mov    rbp,rsp
   140002ecb:	48 83 ec 30          	sub    rsp,0x30
   140002ecf:	48 8b 05 ea 24 00 00 	mov    rax,QWORD PTR [rip+0x24ea]        # 1400053c0 <.refptr.__ImageBase>
   140002ed6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002eda:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ede:	48 89 c1             	mov    rcx,rax
   140002ee1:	e8 ba fc ff ff       	call   140002ba0 <_ValidateImageBase>
   140002ee6:	85 c0                	test   eax,eax
   140002ee8:	75 07                	jne    140002ef1 <_GetPEImageBase+0x2a>
   140002eea:	b8 00 00 00 00       	mov    eax,0x0
   140002eef:	eb 04                	jmp    140002ef5 <_GetPEImageBase+0x2e>
   140002ef1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ef5:	48 83 c4 30          	add    rsp,0x30
   140002ef9:	5d                   	pop    rbp
   140002efa:	c3                   	ret

0000000140002efb <_IsNonwritableInCurrentImage>:
   140002efb:	55                   	push   rbp
   140002efc:	48 89 e5             	mov    rbp,rsp
   140002eff:	48 83 ec 40          	sub    rsp,0x40
   140002f03:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f07:	48 8b 05 b2 24 00 00 	mov    rax,QWORD PTR [rip+0x24b2]        # 1400053c0 <.refptr.__ImageBase>
   140002f0e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f12:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f16:	48 89 c1             	mov    rcx,rax
   140002f19:	e8 82 fc ff ff       	call   140002ba0 <_ValidateImageBase>
   140002f1e:	85 c0                	test   eax,eax
   140002f20:	75 07                	jne    140002f29 <_IsNonwritableInCurrentImage+0x2e>
   140002f22:	b8 00 00 00 00       	mov    eax,0x0
   140002f27:	eb 3d                	jmp    140002f66 <_IsNonwritableInCurrentImage+0x6b>
   140002f29:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f2d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f31:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f35:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f39:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f3d:	48 89 c1             	mov    rcx,rax
   140002f40:	e8 d7 fc ff ff       	call   140002c1c <_FindPESection>
   140002f45:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f49:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140002f4e:	75 07                	jne    140002f57 <_IsNonwritableInCurrentImage+0x5c>
   140002f50:	b8 00 00 00 00       	mov    eax,0x0
   140002f55:	eb 0f                	jmp    140002f66 <_IsNonwritableInCurrentImage+0x6b>
   140002f57:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f5b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002f5e:	f7 d0                	not    eax
   140002f60:	c1 e8 1f             	shr    eax,0x1f
   140002f63:	0f b6 c0             	movzx  eax,al
   140002f66:	48 83 c4 40          	add    rsp,0x40
   140002f6a:	5d                   	pop    rbp
   140002f6b:	c3                   	ret

0000000140002f6c <__mingw_enum_import_library_names>:
   140002f6c:	55                   	push   rbp
   140002f6d:	48 89 e5             	mov    rbp,rsp
   140002f70:	48 83 ec 50          	sub    rsp,0x50
   140002f74:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002f77:	48 8b 05 42 24 00 00 	mov    rax,QWORD PTR [rip+0x2442]        # 1400053c0 <.refptr.__ImageBase>
   140002f7e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f82:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002f86:	48 89 c1             	mov    rcx,rax
   140002f89:	e8 12 fc ff ff       	call   140002ba0 <_ValidateImageBase>
   140002f8e:	85 c0                	test   eax,eax
   140002f90:	75 0a                	jne    140002f9c <__mingw_enum_import_library_names+0x30>
   140002f92:	b8 00 00 00 00       	mov    eax,0x0
   140002f97:	e9 ab 00 00 00       	jmp    140003047 <__mingw_enum_import_library_names+0xdb>
   140002f9c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fa0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002fa3:	48 63 d0             	movsxd rdx,eax
   140002fa6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002faa:	48 01 d0             	add    rax,rdx
   140002fad:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002fb1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002fb5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   140002fbb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140002fbe:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140002fc2:	75 07                	jne    140002fcb <__mingw_enum_import_library_names+0x5f>
   140002fc4:	b8 00 00 00 00       	mov    eax,0x0
   140002fc9:	eb 7c                	jmp    140003047 <__mingw_enum_import_library_names+0xdb>
   140002fcb:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140002fce:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fd2:	48 89 c1             	mov    rcx,rax
   140002fd5:	e8 42 fc ff ff       	call   140002c1c <_FindPESection>
   140002fda:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002fde:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140002fe3:	75 07                	jne    140002fec <__mingw_enum_import_library_names+0x80>
   140002fe5:	b8 00 00 00 00       	mov    eax,0x0
   140002fea:	eb 5b                	jmp    140003047 <__mingw_enum_import_library_names+0xdb>
   140002fec:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140002fef:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002ff3:	48 01 d0             	add    rax,rdx
   140002ff6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002ffa:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002fff:	75 07                	jne    140003008 <__mingw_enum_import_library_names+0x9c>
   140003001:	b8 00 00 00 00       	mov    eax,0x0
   140003006:	eb 3f                	jmp    140003047 <__mingw_enum_import_library_names+0xdb>
   140003008:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000300c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000300f:	85 c0                	test   eax,eax
   140003011:	75 0b                	jne    14000301e <__mingw_enum_import_library_names+0xb2>
   140003013:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003017:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000301a:	85 c0                	test   eax,eax
   14000301c:	74 23                	je     140003041 <__mingw_enum_import_library_names+0xd5>
   14000301e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003022:	7f 12                	jg     140003036 <__mingw_enum_import_library_names+0xca>
   140003024:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003028:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000302b:	89 c2                	mov    edx,eax
   14000302d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003031:	48 01 d0             	add    rax,rdx
   140003034:	eb 11                	jmp    140003047 <__mingw_enum_import_library_names+0xdb>
   140003036:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000303a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000303f:	eb c7                	jmp    140003008 <__mingw_enum_import_library_names+0x9c>
   140003041:	90                   	nop
   140003042:	b8 00 00 00 00       	mov    eax,0x0
   140003047:	48 83 c4 50          	add    rsp,0x50
   14000304b:	5d                   	pop    rbp
   14000304c:	c3                   	ret
   14000304d:	90                   	nop
   14000304e:	90                   	nop
   14000304f:	90                   	nop

0000000140003050 <_Unwind_Resume>:
   140003050:	ff 25 aa 71 00 00    	jmp    QWORD PTR [rip+0x71aa]        # 14000a200 <__IAT_start__>
   140003056:	90                   	nop
   140003057:	90                   	nop
   140003058:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000305f:	00 

0000000140003060 <___chkstk_ms>:
   140003060:	51                   	push   rcx
   140003061:	50                   	push   rax
   140003062:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003068:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000306d:	72 19                	jb     140003088 <___chkstk_ms+0x28>
   14000306f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   140003076:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000307a:	48 2d 00 10 00 00    	sub    rax,0x1000
   140003080:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003086:	77 e7                	ja     14000306f <___chkstk_ms+0xf>
   140003088:	48 29 c1             	sub    rcx,rax
   14000308b:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000308f:	58                   	pop    rax
   140003090:	59                   	pop    rcx
   140003091:	c3                   	ret
   140003092:	90                   	nop
   140003093:	90                   	nop
   140003094:	90                   	nop
   140003095:	90                   	nop
   140003096:	90                   	nop
   140003097:	90                   	nop
   140003098:	90                   	nop
   140003099:	90                   	nop
   14000309a:	90                   	nop
   14000309b:	90                   	nop
   14000309c:	90                   	nop
   14000309d:	90                   	nop
   14000309e:	90                   	nop
   14000309f:	90                   	nop

00000001400030a0 <_initterm_e>:
   1400030a0:	55                   	push   rbp
   1400030a1:	48 89 e5             	mov    rbp,rsp
   1400030a4:	48 83 ec 30          	sub    rsp,0x30
   1400030a8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400030ac:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400030b0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400030b4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030b8:	eb 29                	jmp    1400030e3 <_initterm_e+0x43>
   1400030ba:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030be:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400030c1:	48 85 c0             	test   rax,rax
   1400030c4:	74 17                	je     1400030dd <_initterm_e+0x3d>
   1400030c6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030ca:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400030cd:	ff d0                	call   rax
   1400030cf:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   1400030d2:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   1400030d6:	74 06                	je     1400030de <_initterm_e+0x3e>
   1400030d8:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400030db:	eb 15                	jmp    1400030f2 <_initterm_e+0x52>
   1400030dd:	90                   	nop
   1400030de:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400030e3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400030e7:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400030eb:	72 cd                	jb     1400030ba <_initterm_e+0x1a>
   1400030ed:	b8 00 00 00 00       	mov    eax,0x0
   1400030f2:	48 83 c4 30          	add    rsp,0x30
   1400030f6:	5d                   	pop    rbp
   1400030f7:	c3                   	ret
   1400030f8:	90                   	nop
   1400030f9:	90                   	nop
   1400030fa:	90                   	nop
   1400030fb:	90                   	nop
   1400030fc:	90                   	nop
   1400030fd:	90                   	nop
   1400030fe:	90                   	nop
   1400030ff:	90                   	nop

0000000140003100 <__p__fmode>:
   140003100:	55                   	push   rbp
   140003101:	48 89 e5             	mov    rbp,rsp
   140003104:	48 8b 05 25 23 00 00 	mov    rax,QWORD PTR [rip+0x2325]        # 140005430 <.refptr.__imp__fmode>
   14000310b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000310e:	5d                   	pop    rbp
   14000310f:	c3                   	ret

0000000140003110 <__p__commode>:
   140003110:	55                   	push   rbp
   140003111:	48 89 e5             	mov    rbp,rsp
   140003114:	48 8b 05 05 23 00 00 	mov    rax,QWORD PTR [rip+0x2305]        # 140005420 <.refptr.__imp__commode>
   14000311b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000311e:	5d                   	pop    rbp
   14000311f:	c3                   	ret

0000000140003120 <__p___initenv>:
   140003120:	55                   	push   rbp
   140003121:	48 89 e5             	mov    rbp,rsp
   140003124:	48 8b 05 e5 22 00 00 	mov    rax,QWORD PTR [rip+0x22e5]        # 140005410 <.refptr.__imp___initenv>
   14000312b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000312e:	5d                   	pop    rbp
   14000312f:	c3                   	ret

0000000140003130 <_set_invalid_parameter_handler>:
   140003130:	55                   	push   rbp
   140003131:	48 89 e5             	mov    rbp,rsp
   140003134:	48 83 ec 10          	sub    rsp,0x10
   140003138:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000313c:	48 8d 05 4d 60 00 00 	lea    rax,[rip+0x604d]        # 140009190 <handler>
   140003143:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003147:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000314b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000314f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003153:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003157:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000315a:	48 89 d0             	mov    rax,rdx
   14000315d:	48 83 c4 10          	add    rsp,0x10
   140003161:	5d                   	pop    rbp
   140003162:	c3                   	ret

0000000140003163 <_get_invalid_parameter_handler>:
   140003163:	55                   	push   rbp
   140003164:	48 89 e5             	mov    rbp,rsp
   140003167:	48 8b 05 22 60 00 00 	mov    rax,QWORD PTR [rip+0x6022]        # 140009190 <handler>
   14000316e:	5d                   	pop    rbp
   14000316f:	c3                   	ret

0000000140003170 <_configthreadlocale>:
   140003170:	55                   	push   rbp
   140003171:	48 89 e5             	mov    rbp,rsp
   140003174:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003177:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   14000317b:	75 07                	jne    140003184 <_configthreadlocale+0x14>
   14000317d:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140003182:	eb 05                	jmp    140003189 <_configthreadlocale+0x19>
   140003184:	b8 02 00 00 00       	mov    eax,0x2
   140003189:	5d                   	pop    rbp
   14000318a:	c3                   	ret
   14000318b:	90                   	nop
   14000318c:	90                   	nop
   14000318d:	90                   	nop
   14000318e:	90                   	nop
   14000318f:	90                   	nop

0000000140003190 <__acrt_iob_func>:
   140003190:	55                   	push   rbp
   140003191:	48 89 e5             	mov    rbp,rsp
   140003194:	48 83 ec 20          	sub    rsp,0x20
   140003198:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000319b:	e8 30 00 00 00       	call   1400031d0 <__iob_func>
   1400031a0:	48 89 c1             	mov    rcx,rax
   1400031a3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400031a6:	48 89 d0             	mov    rax,rdx
   1400031a9:	48 01 c0             	add    rax,rax
   1400031ac:	48 01 d0             	add    rax,rdx
   1400031af:	48 c1 e0 04          	shl    rax,0x4
   1400031b3:	48 01 c8             	add    rax,rcx
   1400031b6:	48 83 c4 20          	add    rsp,0x20
   1400031ba:	5d                   	pop    rbp
   1400031bb:	c3                   	ret
   1400031bc:	90                   	nop
   1400031bd:	90                   	nop
   1400031be:	90                   	nop
   1400031bf:	90                   	nop

00000001400031c0 <__C_specific_handler>:
   1400031c0:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a2c8 <__imp___C_specific_handler>
   1400031c6:	90                   	nop
   1400031c7:	90                   	nop

00000001400031c8 <__getmainargs>:
   1400031c8:	ff 25 02 71 00 00    	jmp    QWORD PTR [rip+0x7102]        # 14000a2d0 <__imp___getmainargs>
   1400031ce:	90                   	nop
   1400031cf:	90                   	nop

00000001400031d0 <__iob_func>:
   1400031d0:	ff 25 0a 71 00 00    	jmp    QWORD PTR [rip+0x710a]        # 14000a2e0 <__imp___iob_func>
   1400031d6:	90                   	nop
   1400031d7:	90                   	nop

00000001400031d8 <__set_app_type>:
   1400031d8:	ff 25 0a 71 00 00    	jmp    QWORD PTR [rip+0x710a]        # 14000a2e8 <__imp___set_app_type>
   1400031de:	90                   	nop
   1400031df:	90                   	nop

00000001400031e0 <__setusermatherr>:
   1400031e0:	ff 25 0a 71 00 00    	jmp    QWORD PTR [rip+0x710a]        # 14000a2f0 <__imp___setusermatherr>
   1400031e6:	90                   	nop
   1400031e7:	90                   	nop

00000001400031e8 <_amsg_exit>:
   1400031e8:	ff 25 0a 71 00 00    	jmp    QWORD PTR [rip+0x710a]        # 14000a2f8 <__imp__amsg_exit>
   1400031ee:	90                   	nop
   1400031ef:	90                   	nop

00000001400031f0 <_cexit>:
   1400031f0:	ff 25 0a 71 00 00    	jmp    QWORD PTR [rip+0x710a]        # 14000a300 <__imp__cexit>
   1400031f6:	90                   	nop
   1400031f7:	90                   	nop

00000001400031f8 <_initterm>:
   1400031f8:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a318 <__imp__initterm>
   1400031fe:	90                   	nop
   1400031ff:	90                   	nop

0000000140003200 <_crt_atexit>:
   140003200:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a320 <__imp__crt_atexit>
   140003206:	90                   	nop
   140003207:	90                   	nop

0000000140003208 <abort>:
   140003208:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a328 <__imp_abort>
   14000320e:	90                   	nop
   14000320f:	90                   	nop

0000000140003210 <calloc>:
   140003210:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a330 <__imp_calloc>
   140003216:	90                   	nop
   140003217:	90                   	nop

0000000140003218 <exit>:
   140003218:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a338 <__imp_exit>
   14000321e:	90                   	nop
   14000321f:	90                   	nop

0000000140003220 <fflush>:
   140003220:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a340 <__imp_fflush>
   140003226:	90                   	nop
   140003227:	90                   	nop

0000000140003228 <fprintf>:
   140003228:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a348 <__imp_fprintf>
   14000322e:	90                   	nop
   14000322f:	90                   	nop

0000000140003230 <free>:
   140003230:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a350 <__imp_free>
   140003236:	90                   	nop
   140003237:	90                   	nop

0000000140003238 <malloc>:
   140003238:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a358 <__imp_malloc>
   14000323e:	90                   	nop
   14000323f:	90                   	nop

0000000140003240 <memcpy>:
   140003240:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a360 <__imp_memcpy>
   140003246:	90                   	nop
   140003247:	90                   	nop

0000000140003248 <setvbuf>:
   140003248:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a368 <__imp_setvbuf>
   14000324e:	90                   	nop
   14000324f:	90                   	nop

0000000140003250 <signal>:
   140003250:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a370 <__imp_signal>
   140003256:	90                   	nop
   140003257:	90                   	nop

0000000140003258 <strlen>:
   140003258:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a378 <__imp_strlen>
   14000325e:	90                   	nop
   14000325f:	90                   	nop

0000000140003260 <strncmp>:
   140003260:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a380 <__imp_strncmp>
   140003266:	90                   	nop
   140003267:	90                   	nop

0000000140003268 <vfprintf>:
   140003268:	ff 25 1a 71 00 00    	jmp    QWORD PTR [rip+0x711a]        # 14000a388 <__imp_vfprintf>
   14000326e:	90                   	nop
   14000326f:	90                   	nop

0000000140003270 <VirtualQuery>:
   140003270:	ff 25 42 70 00 00    	jmp    QWORD PTR [rip+0x7042]        # 14000a2b8 <__imp_VirtualQuery>
   140003276:	90                   	nop
   140003277:	90                   	nop

0000000140003278 <VirtualProtect>:
   140003278:	ff 25 32 70 00 00    	jmp    QWORD PTR [rip+0x7032]        # 14000a2b0 <__imp_VirtualProtect>
   14000327e:	90                   	nop
   14000327f:	90                   	nop

0000000140003280 <TlsGetValue>:
   140003280:	ff 25 22 70 00 00    	jmp    QWORD PTR [rip+0x7022]        # 14000a2a8 <__imp_TlsGetValue>
   140003286:	90                   	nop
   140003287:	90                   	nop

0000000140003288 <Sleep>:
   140003288:	ff 25 12 70 00 00    	jmp    QWORD PTR [rip+0x7012]        # 14000a2a0 <__imp_Sleep>
   14000328e:	90                   	nop
   14000328f:	90                   	nop

0000000140003290 <SetUnhandledExceptionFilter>:
   140003290:	ff 25 02 70 00 00    	jmp    QWORD PTR [rip+0x7002]        # 14000a298 <__imp_SetUnhandledExceptionFilter>
   140003296:	90                   	nop
   140003297:	90                   	nop

0000000140003298 <LoadLibraryA>:
   140003298:	ff 25 f2 6f 00 00    	jmp    QWORD PTR [rip+0x6ff2]        # 14000a290 <__imp_LoadLibraryA>
   14000329e:	90                   	nop
   14000329f:	90                   	nop

00000001400032a0 <LeaveCriticalSection>:
   1400032a0:	ff 25 e2 6f 00 00    	jmp    QWORD PTR [rip+0x6fe2]        # 14000a288 <__imp_LeaveCriticalSection>
   1400032a6:	90                   	nop
   1400032a7:	90                   	nop

00000001400032a8 <InitializeCriticalSection>:
   1400032a8:	ff 25 d2 6f 00 00    	jmp    QWORD PTR [rip+0x6fd2]        # 14000a280 <__imp_InitializeCriticalSection>
   1400032ae:	90                   	nop
   1400032af:	90                   	nop

00000001400032b0 <GetProcAddress>:
   1400032b0:	ff 25 c2 6f 00 00    	jmp    QWORD PTR [rip+0x6fc2]        # 14000a278 <__imp_GetProcAddress>
   1400032b6:	90                   	nop
   1400032b7:	90                   	nop

00000001400032b8 <GetModuleHandleA>:
   1400032b8:	ff 25 b2 6f 00 00    	jmp    QWORD PTR [rip+0x6fb2]        # 14000a270 <__imp_GetModuleHandleA>
   1400032be:	90                   	nop
   1400032bf:	90                   	nop

00000001400032c0 <GetLastError>:
   1400032c0:	ff 25 a2 6f 00 00    	jmp    QWORD PTR [rip+0x6fa2]        # 14000a268 <__imp_GetLastError>
   1400032c6:	90                   	nop
   1400032c7:	90                   	nop

00000001400032c8 <FreeLibrary>:
   1400032c8:	ff 25 92 6f 00 00    	jmp    QWORD PTR [rip+0x6f92]        # 14000a260 <__imp_FreeLibrary>
   1400032ce:	90                   	nop
   1400032cf:	90                   	nop

00000001400032d0 <EnterCriticalSection>:
   1400032d0:	ff 25 82 6f 00 00    	jmp    QWORD PTR [rip+0x6f82]        # 14000a258 <__imp_EnterCriticalSection>
   1400032d6:	90                   	nop
   1400032d7:	90                   	nop

00000001400032d8 <DeleteCriticalSection>:
   1400032d8:	ff 25 72 6f 00 00    	jmp    QWORD PTR [rip+0x6f72]        # 14000a250 <__imp_DeleteCriticalSection>
   1400032de:	90                   	nop
   1400032df:	90                   	nop

00000001400032e0 <std::bad_any_cast::what() const>:
   1400032e0:	48 8d 05 69 1d 00 00 	lea    rax,[rip+0x1d69]        # 140005050 <.rdata>
   1400032e7:	c3                   	ret
   1400032e8:	90                   	nop
   1400032e9:	90                   	nop
   1400032ea:	90                   	nop
   1400032eb:	90                   	nop
   1400032ec:	90                   	nop
   1400032ed:	90                   	nop
   1400032ee:	90                   	nop
   1400032ef:	90                   	nop

00000001400032f0 <std::bad_any_cast::~bad_any_cast()>:
   1400032f0:	48 83 ec 38          	sub    rsp,0x38
   1400032f4:	48 8d 05 55 23 00 00 	lea    rax,[rip+0x2355]        # 140005650 <vtable for std::bad_any_cast+0x10>
   1400032fb:	48 89 01             	mov    QWORD PTR [rcx],rax
   1400032fe:	48 89 4c 24 28       	mov    QWORD PTR [rsp+0x28],rcx
   140003303:	e8 70 e4 ff ff       	call   140001778 <std::bad_cast::~bad_cast()>
   140003308:	48 8b 4c 24 28       	mov    rcx,QWORD PTR [rsp+0x28]
   14000330d:	ba 08 00 00 00       	mov    edx,0x8
   140003312:	48 83 c4 38          	add    rsp,0x38
   140003316:	e9 55 e4 ff ff       	jmp    140001770 <operator delete(void*, unsigned long long)>
   14000331b:	90                   	nop
   14000331c:	90                   	nop
   14000331d:	90                   	nop
   14000331e:	90                   	nop
   14000331f:	90                   	nop

0000000140003320 <std::bad_any_cast::~bad_any_cast()>:
   140003320:	48 8d 05 29 23 00 00 	lea    rax,[rip+0x2329]        # 140005650 <vtable for std::bad_any_cast+0x10>
   140003327:	48 89 01             	mov    QWORD PTR [rcx],rax
   14000332a:	e9 49 e4 ff ff       	jmp    140001778 <std::bad_cast::~bad_cast()>
   14000332f:	90                   	nop

0000000140003330 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)>:
   140003330:	56                   	push   rsi
   140003331:	53                   	push   rbx
   140003332:	48 83 ec 58          	sub    rsp,0x58
   140003336:	4d 89 c2             	mov    r10,r8
   140003339:	49 89 d1             	mov    r9,rdx
   14000333c:	4c 8b 42 08          	mov    r8,QWORD PTR [rdx+0x8]
   140003340:	83 f9 04             	cmp    ecx,0x4
   140003343:	77 1e                	ja     140003363 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x33>
   140003345:	48 8d 15 28 1d 00 00 	lea    rdx,[rip+0x1d28]        # 140005074 <.rdata+0x24>
   14000334c:	89 c9                	mov    ecx,ecx
   14000334e:	48 63 04 8a          	movsxd rax,DWORD PTR [rdx+rcx*4]
   140003352:	48 01 d0             	add    rax,rdx
   140003355:	ff e0                	jmp    rax
   140003357:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000335e:	00 00 
   140003360:	4d 89 02             	mov    QWORD PTR [r10],r8
   140003363:	48 83 c4 58          	add    rsp,0x58
   140003367:	5b                   	pop    rbx
   140003368:	5e                   	pop    rsi
   140003369:	c3                   	ret
   14000336a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
   140003370:	4d 85 c0             	test   r8,r8
   140003373:	74 ee                	je     140003363 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x33>
   140003375:	49 8b 08             	mov    rcx,QWORD PTR [r8]
   140003378:	49 8d 40 10          	lea    rax,[r8+0x10]
   14000337c:	48 39 c1             	cmp    rcx,rax
   14000337f:	74 17                	je     140003398 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x68>
   140003381:	49 8b 40 10          	mov    rax,QWORD PTR [r8+0x10]
   140003385:	4c 89 44 24 28       	mov    QWORD PTR [rsp+0x28],r8
   14000338a:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000338e:	e8 dd e3 ff ff       	call   140001770 <operator delete(void*, unsigned long long)>
   140003393:	4c 8b 44 24 28       	mov    r8,QWORD PTR [rsp+0x28]
   140003398:	ba 20 00 00 00       	mov    edx,0x20
   14000339d:	4c 89 c1             	mov    rcx,r8
   1400033a0:	48 83 c4 58          	add    rsp,0x58
   1400033a4:	5b                   	pop    rbx
   1400033a5:	5e                   	pop    rsi
   1400033a6:	e9 c5 e3 ff ff       	jmp    140001770 <operator delete(void*, unsigned long long)>
   1400033ab:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
   1400033b0:	49 8b 02             	mov    rax,QWORD PTR [r10]
   1400033b3:	4c 89 40 08          	mov    QWORD PTR [rax+0x8],r8
   1400033b7:	49 8b 02             	mov    rax,QWORD PTR [r10]
   1400033ba:	49 8b 11             	mov    rdx,QWORD PTR [r9]
   1400033bd:	48 89 10             	mov    QWORD PTR [rax],rdx
   1400033c0:	49 c7 01 00 00 00 00 	mov    QWORD PTR [r9],0x0
   1400033c7:	48 83 c4 58          	add    rsp,0x58
   1400033cb:	5b                   	pop    rbx
   1400033cc:	5e                   	pop    rsi
   1400033cd:	c3                   	ret
   1400033ce:	66 90                	xchg   ax,ax
   1400033d0:	48 8d 05 79 21 00 00 	lea    rax,[rip+0x2179]        # 140005550 <typeinfo for std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >>
   1400033d7:	49 89 02             	mov    QWORD PTR [r10],rax
   1400033da:	48 83 c4 58          	add    rsp,0x58
   1400033de:	5b                   	pop    rbx
   1400033df:	5e                   	pop    rsi
   1400033e0:	c3                   	ret
   1400033e1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   1400033e8:	b9 20 00 00 00       	mov    ecx,0x20
   1400033ed:	4c 89 54 24 38       	mov    QWORD PTR [rsp+0x38],r10
   1400033f2:	4c 89 4c 24 30       	mov    QWORD PTR [rsp+0x30],r9
   1400033f7:	4c 89 44 24 28       	mov    QWORD PTR [rsp+0x28],r8
   1400033fc:	e8 67 e3 ff ff       	call   140001768 <operator new(unsigned long long)>
   140003401:	4c 8b 44 24 28       	mov    r8,QWORD PTR [rsp+0x28]
   140003406:	4c 8b 4c 24 30       	mov    r9,QWORD PTR [rsp+0x30]
   14000340b:	48 8d 48 10          	lea    rcx,[rax+0x10]
   14000340f:	4c 8b 54 24 38       	mov    r10,QWORD PTR [rsp+0x38]
   140003414:	48 89 c3             	mov    rbx,rax
   140003417:	4d 8b 58 08          	mov    r11,QWORD PTR [r8+0x8]
   14000341b:	48 89 08             	mov    QWORD PTR [rax],rcx
   14000341e:	49 8b 10             	mov    rdx,QWORD PTR [r8]
   140003421:	49 83 fb 0f          	cmp    r11,0xf
   140003425:	4d 8d 43 01          	lea    r8,[r11+0x1]
   140003429:	77 2d                	ja     140003458 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x128>
   14000342b:	4d 85 db             	test   r11,r11
   14000342e:	75 6c                	jne    14000349c <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x16c>
   140003430:	0f b6 02             	movzx  eax,BYTE PTR [rdx]
   140003433:	88 43 10             	mov    BYTE PTR [rbx+0x10],al
   140003436:	49 8b 02             	mov    rax,QWORD PTR [r10]
   140003439:	4c 89 5b 08          	mov    QWORD PTR [rbx+0x8],r11
   14000343d:	48 89 58 08          	mov    QWORD PTR [rax+0x8],rbx
   140003441:	49 8b 02             	mov    rax,QWORD PTR [r10]
   140003444:	49 8b 11             	mov    rdx,QWORD PTR [r9]
   140003447:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000344a:	48 83 c4 58          	add    rsp,0x58
   14000344e:	5b                   	pop    rbx
   14000344f:	5e                   	pop    rsi
   140003450:	c3                   	ret
   140003451:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
   140003458:	4c 89 c1             	mov    rcx,r8
   14000345b:	4c 89 54 24 48       	mov    QWORD PTR [rsp+0x48],r10
   140003460:	4c 89 4c 24 40       	mov    QWORD PTR [rsp+0x40],r9
   140003465:	48 89 54 24 38       	mov    QWORD PTR [rsp+0x38],rdx
   14000346a:	4c 89 5c 24 30       	mov    QWORD PTR [rsp+0x30],r11
   14000346f:	4c 89 44 24 28       	mov    QWORD PTR [rsp+0x28],r8
   140003474:	e8 ef e2 ff ff       	call   140001768 <operator new(unsigned long long)>
   140003479:	4c 8b 5c 24 30       	mov    r11,QWORD PTR [rsp+0x30]
   14000347e:	4c 8b 44 24 28       	mov    r8,QWORD PTR [rsp+0x28]
   140003483:	48 89 03             	mov    QWORD PTR [rbx],rax
   140003486:	48 89 c1             	mov    rcx,rax
   140003489:	48 8b 54 24 38       	mov    rdx,QWORD PTR [rsp+0x38]
   14000348e:	4c 8b 4c 24 40       	mov    r9,QWORD PTR [rsp+0x40]
   140003493:	4c 89 5b 10          	mov    QWORD PTR [rbx+0x10],r11
   140003497:	4c 8b 54 24 48       	mov    r10,QWORD PTR [rsp+0x48]
   14000349c:	4c 89 54 24 38       	mov    QWORD PTR [rsp+0x38],r10
   1400034a1:	4c 89 4c 24 30       	mov    QWORD PTR [rsp+0x30],r9
   1400034a6:	4c 89 5c 24 28       	mov    QWORD PTR [rsp+0x28],r11
   1400034ab:	e8 90 fd ff ff       	call   140003240 <memcpy>
   1400034b0:	4c 8b 54 24 38       	mov    r10,QWORD PTR [rsp+0x38]
   1400034b5:	4c 8b 4c 24 30       	mov    r9,QWORD PTR [rsp+0x30]
   1400034ba:	4c 8b 5c 24 28       	mov    r11,QWORD PTR [rsp+0x28]
   1400034bf:	e9 72 ff ff ff       	jmp    140003436 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x106>
   1400034c4:	48 89 c6             	mov    rsi,rax
   1400034c7:	48 89 d9             	mov    rcx,rbx
   1400034ca:	ba 20 00 00 00       	mov    edx,0x20
   1400034cf:	e8 9c e2 ff ff       	call   140001770 <operator delete(void*, unsigned long long)>
   1400034d4:	48 89 f1             	mov    rcx,rsi
   1400034d7:	e8 74 fb ff ff       	call   140003050 <_Unwind_Resume>
   1400034dc:	90                   	nop
   1400034dd:	90                   	nop
   1400034de:	90                   	nop
   1400034df:	90                   	nop

00000001400034e0 <std::any::_Manager_internal<int>::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)>:
   1400034e0:	83 f9 04             	cmp    ecx,0x4
   1400034e3:	77 31                	ja     140003516 <std::any::_Manager_internal<int>::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)+0x36>
   1400034e5:	4c 8d 0d 74 1b 00 00 	lea    r9,[rip+0x1b74]        # 140005060 <.rdata+0x10>
   1400034ec:	89 c9                	mov    ecx,ecx
   1400034ee:	49 63 04 89          	movsxd rax,DWORD PTR [r9+rcx*4]
   1400034f2:	4c 01 c8             	add    rax,r9
   1400034f5:	ff e0                	jmp    rax
   1400034f7:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   1400034fe:	00 00 
   140003500:	49 8b 00             	mov    rax,QWORD PTR [r8]
   140003503:	8b 4a 08             	mov    ecx,DWORD PTR [rdx+0x8]
   140003506:	89 48 08             	mov    DWORD PTR [rax+0x8],ecx
   140003509:	48 8b 0a             	mov    rcx,QWORD PTR [rdx]
   14000350c:	48 89 08             	mov    QWORD PTR [rax],rcx
   14000350f:	48 c7 02 00 00 00 00 	mov    QWORD PTR [rdx],0x0
   140003516:	c3                   	ret
   140003517:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000351e:	00 00 
   140003520:	8b 4a 08             	mov    ecx,DWORD PTR [rdx+0x8]
   140003523:	49 8b 00             	mov    rax,QWORD PTR [r8]
   140003526:	48 8b 12             	mov    rdx,QWORD PTR [rdx]
   140003529:	89 48 08             	mov    DWORD PTR [rax+0x8],ecx
   14000352c:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000352f:	c3                   	ret
   140003530:	48 83 c2 08          	add    rdx,0x8
   140003534:	49 89 10             	mov    QWORD PTR [r8],rdx
   140003537:	c3                   	ret
   140003538:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000353f:	00 
   140003540:	48 8b 05 59 1e 00 00 	mov    rax,QWORD PTR [rip+0x1e59]        # 1400053a0 <__fu4__ZTIi>
   140003547:	49 89 00             	mov    QWORD PTR [r8],rax
   14000354a:	c3                   	ret
   14000354b:	90                   	nop
   14000354c:	90                   	nop
   14000354d:	90                   	nop
   14000354e:	90                   	nop
   14000354f:	90                   	nop

0000000140003550 <std::any::reset()>:
   140003550:	53                   	push   rbx
   140003551:	48 83 ec 20          	sub    rsp,0x20
   140003555:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   140003558:	48 89 cb             	mov    rbx,rcx
   14000355b:	48 85 c0             	test   rax,rax
   14000355e:	74 14                	je     140003574 <std::any::reset()+0x24>
   140003560:	48 89 ca             	mov    rdx,rcx
   140003563:	45 31 c0             	xor    r8d,r8d
   140003566:	b9 03 00 00 00       	mov    ecx,0x3
   14000356b:	ff d0                	call   rax
   14000356d:	48 c7 03 00 00 00 00 	mov    QWORD PTR [rbx],0x0
   140003574:	48 83 c4 20          	add    rsp,0x20
   140003578:	5b                   	pop    rbx
   140003579:	c3                   	ret
   14000357a:	90                   	nop
   14000357b:	90                   	nop
   14000357c:	90                   	nop
   14000357d:	90                   	nop
   14000357e:	90                   	nop
   14000357f:	90                   	nop

0000000140003580 <main.cold>:
   140003580:	48 89 d9             	mov    rcx,rbx
   140003583:	ba 28 00 00 00       	mov    edx,0x28
   140003588:	48 89 44 24 28       	mov    QWORD PTR [rsp+0x28],rax
   14000358d:	e8 de e1 ff ff       	call   140001770 <operator delete(void*, unsigned long long)>
   140003592:	48 8b 5c 24 28       	mov    rbx,QWORD PTR [rsp+0x28]
   140003597:	48 8d 4c 24 40       	lea    rcx,[rsp+0x40]
   14000359c:	e8 af ff ff ff       	call   140003550 <std::any::reset()>
   1400035a1:	48 89 d9             	mov    rcx,rbx
   1400035a4:	e8 a7 fa ff ff       	call   140003050 <_Unwind_Resume>
   1400035a9:	90                   	nop
   1400035aa:	90                   	nop
   1400035ab:	90                   	nop
   1400035ac:	90                   	nop
   1400035ad:	90                   	nop
   1400035ae:	90                   	nop
   1400035af:	90                   	nop

00000001400035b0 <main>:
   1400035b0:	53                   	push   rbx
   1400035b1:	48 83 ec 60          	sub    rsp,0x60
   1400035b5:	e8 7d e2 ff ff       	call   140001837 <__main>
   1400035ba:	48 8d 05 1f ff ff ff 	lea    rax,[rip+0xffffffffffffff1f]        # 1400034e0 <std::any::_Manager_internal<int>::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)>
   1400035c1:	b9 28 00 00 00       	mov    ecx,0x28
   1400035c6:	c7 44 24 3c 2a 00 00 	mov    DWORD PTR [rsp+0x3c],0x2a
   1400035cd:	00 
   1400035ce:	48 89 44 24 40       	mov    QWORD PTR [rsp+0x40],rax
   1400035d3:	8b 44 24 3c          	mov    eax,DWORD PTR [rsp+0x3c]
   1400035d7:	48 c7 44 24 48 2a 00 	mov    QWORD PTR [rsp+0x48],0x2a
   1400035de:	00 00 
   1400035e0:	e8 83 e1 ff ff       	call   140001768 <operator new(unsigned long long)>
   1400035e5:	48 89 c3             	mov    rbx,rax
   1400035e8:	b9 20 00 00 00       	mov    ecx,0x20
   1400035ed:	48 b8 74 68 69 73 20 	movabs rax,0x7274732073696874
   1400035f4:	73 74 72 
   1400035f7:	48 ba 69 6e 67 20 69 	movabs rdx,0x6c20736920676e69
   1400035fe:	73 20 6c 
   140003601:	48 89 03             	mov    QWORD PTR [rbx],rax
   140003604:	48 b8 6f 6e 67 65 72 	movabs rax,0x6874207265676e6f
   14000360b:	20 74 68 
   14000360e:	48 89 53 08          	mov    QWORD PTR [rbx+0x8],rdx
   140003612:	48 ba 61 6e 20 31 36 	movabs rdx,0x7962203631206e61
   140003619:	20 62 79 
   14000361c:	48 89 43 10          	mov    QWORD PTR [rbx+0x10],rax
   140003620:	48 b8 79 74 65 73 20 	movabs rax,0x4f42532073657479
   140003627:	53 42 4f 
   14000362a:	48 89 53 18          	mov    QWORD PTR [rbx+0x18],rdx
   14000362e:	c6 43 27 00          	mov    BYTE PTR [rbx+0x27],0x0
   140003632:	48 89 43 1f          	mov    QWORD PTR [rbx+0x1f],rax
   140003636:	48 8d 05 f3 fc ff ff 	lea    rax,[rip+0xfffffffffffffcf3]        # 140003330 <std::any::_Manager_external<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)>
   14000363d:	48 89 44 24 50       	mov    QWORD PTR [rsp+0x50],rax
   140003642:	48 c7 44 24 58 00 00 	mov    QWORD PTR [rsp+0x58],0x0
   140003649:	00 00 
   14000364b:	e8 18 e1 ff ff       	call   140001768 <operator new(unsigned long long)>
   140003650:	ba 27 00 00 00       	mov    edx,0x27
   140003655:	48 89 18             	mov    QWORD PTR [rax],rbx
   140003658:	48 8d 4c 24 50       	lea    rcx,[rsp+0x50]
   14000365d:	66 48 0f 6e c2       	movq   xmm0,rdx
   140003662:	48 89 44 24 58       	mov    QWORD PTR [rsp+0x58],rax
   140003667:	66 0f 6c c0          	punpcklqdq xmm0,xmm0
   14000366b:	c6 44 24 3b 01       	mov    BYTE PTR [rsp+0x3b],0x1
   140003670:	0f 11 40 08          	movups XMMWORD PTR [rax+0x8],xmm0
   140003674:	0f b6 44 24 3b       	movzx  eax,BYTE PTR [rsp+0x3b]
   140003679:	e8 d2 fe ff ff       	call   140003550 <std::any::reset()>
   14000367e:	48 8d 4c 24 40       	lea    rcx,[rsp+0x40]
   140003683:	e8 c8 fe ff ff       	call   140003550 <std::any::reset()>
   140003688:	31 c0                	xor    eax,eax
   14000368a:	48 83 c4 60          	add    rsp,0x60
   14000368e:	5b                   	pop    rbx
   14000368f:	c3                   	ret
   140003690:	48 89 c3             	mov    rbx,rax
   140003693:	e9 ff fe ff ff       	jmp    140003597 <main.cold+0x17>
   140003698:	e9 e3 fe ff ff       	jmp    140003580 <main.cold>
   14000369d:	90                   	nop
   14000369e:	90                   	nop
   14000369f:	90                   	nop

00000001400036a0 <register_frame_ctor>:
   1400036a0:	e9 cb df ff ff       	jmp    140001670 <__gcc_register_frame>
   1400036a5:	90                   	nop
   1400036a6:	90                   	nop
   1400036a7:	90                   	nop
   1400036a8:	90                   	nop
   1400036a9:	90                   	nop
   1400036aa:	90                   	nop
   1400036ab:	90                   	nop
   1400036ac:	90                   	nop
   1400036ad:	90                   	nop
   1400036ae:	90                   	nop
   1400036af:	90                   	nop
