
ch50_vi_test.exe:     file format pei-x86-64


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
   140001024:	e8 9f 85 00 00       	call   1400095c8 <fflush>
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
   14000103f:	48 8b 05 da a5 00 00 	mov    rax,QWORD PTR [rip+0xa5da]        # 14000b620 <.refptr.__mingw_app_type>
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
   14000106e:	48 8b 05 ab a5 00 00 	mov    rax,QWORD PTR [rip+0xa5ab]        # 14000b620 <.refptr.__mingw_app_type>
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
   1400010e8:	48 8b 05 99 f1 00 00 	mov    rax,QWORD PTR [rip+0xf199]        # 140010288 <__imp_Sleep>
   1400010ef:	ff d0                	call   rax
   1400010f1:	48 8b 05 78 a5 00 00 	mov    rax,QWORD PTR [rip+0xa578]        # 14000b670 <.refptr.__native_startup_lock>
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
   140001128:	48 8b 05 51 a5 00 00 	mov    rax,QWORD PTR [rip+0xa551]        # 14000b680 <.refptr.__native_startup_state>
   14000112f:	8b 00                	mov    eax,DWORD PTR [rax]
   140001131:	83 f8 01             	cmp    eax,0x1
   140001134:	75 0a                	jne    140001140 <__tmainCRTStartup+0xb2>
   140001136:	b9 1f 00 00 00       	mov    ecx,0x1f
   14000113b:	e8 38 84 00 00       	call   140009578 <_amsg_exit>
   140001140:	48 8b 05 39 a5 00 00 	mov    rax,QWORD PTR [rip+0xa539]        # 14000b680 <.refptr.__native_startup_state>
   140001147:	8b 00                	mov    eax,DWORD PTR [rax]
   140001149:	85 c0                	test   eax,eax
   14000114b:	0f 85 e3 01 00 00    	jne    140001334 <__tmainCRTStartup+0x2a6>
   140001151:	48 8b 05 28 a5 00 00 	mov    rax,QWORD PTR [rip+0xa528]        # 14000b680 <.refptr.__native_startup_state>
   140001158:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000115e:	b9 02 00 00 00       	mov    ecx,0x2
   140001163:	e8 38 7e 00 00       	call   140008fa0 <__acrt_iob_func>
   140001168:	41 b9 00 00 00 00    	mov    r9d,0x0
   14000116e:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001174:	ba 00 00 00 00       	mov    edx,0x0
   140001179:	48 89 c1             	mov    rcx,rax
   14000117c:	e8 7f 84 00 00       	call   140009600 <setvbuf>
   140001181:	48 8d 05 8f fe ff ff 	lea    rax,[rip+0xfffffffffffffe8f]        # 140001017 <safe_flush>
   140001188:	48 89 c1             	mov    rcx,rax
   14000118b:	e8 9f 04 00 00       	call   14000162f <atexit>
   140001190:	85 c0                	test   eax,eax
   140001192:	74 05                	je     140001199 <__tmainCRTStartup+0x10b>
   140001194:	e8 17 84 00 00       	call   1400095b0 <abort>
   140001199:	e8 02 11 00 00       	call   1400022a0 <_pei386_runtime_relocator>
   14000119e:	48 8b 05 6b a5 00 00 	mov    rax,QWORD PTR [rip+0xa56b]        # 14000b710 <.refptr._gnu_exception_handler>
   1400011a5:	48 89 c1             	mov    rcx,rax
   1400011a8:	48 8b 05 d1 f0 00 00 	mov    rax,QWORD PTR [rip+0xf0d1]        # 140010280 <__imp_SetUnhandledExceptionFilter>
   1400011af:	ff d0                	call   rax
   1400011b1:	48 8b 15 a8 a4 00 00 	mov    rdx,QWORD PTR [rip+0xa4a8]        # 14000b660 <.refptr.__mingw_oldexcpt_handler>
   1400011b8:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400011bb:	48 8d 05 3e fe ff ff 	lea    rax,[rip+0xfffffffffffffe3e]        # 140001000 <__mingw_invalidParameterHandler>
   1400011c2:	48 89 c1             	mov    rcx,rax
   1400011c5:	e8 76 7d 00 00       	call   140008f40 <_set_invalid_parameter_handler>
   1400011ca:	e8 e1 19 00 00       	call   140002bb0 <_fpreset>
   1400011cf:	e8 18 02 00 00       	call   1400013ec <check_managed_app>
   1400011d4:	89 05 3e de 00 00    	mov    DWORD PTR [rip+0xde3e],eax        # 14000f018 <managedapp>
   1400011da:	48 8b 05 3f a4 00 00 	mov    rax,QWORD PTR [rip+0xa43f]        # 14000b620 <.refptr.__mingw_app_type>
   1400011e1:	8b 00                	mov    eax,DWORD PTR [rax]
   1400011e3:	85 c0                	test   eax,eax
   1400011e5:	74 0c                	je     1400011f3 <__tmainCRTStartup+0x165>
   1400011e7:	b9 02 00 00 00       	mov    ecx,0x2
   1400011ec:	e8 77 83 00 00       	call   140009568 <__set_app_type>
   1400011f1:	eb 0a                	jmp    1400011fd <__tmainCRTStartup+0x16f>
   1400011f3:	b9 01 00 00 00       	mov    ecx,0x1
   1400011f8:	e8 6b 83 00 00       	call   140009568 <__set_app_type>
   1400011fd:	e8 ee 7b 00 00       	call   140008df0 <__p__fmode>
   140001202:	48 8b 15 f7 a4 00 00 	mov    rdx,QWORD PTR [rip+0xa4f7]        # 14000b700 <.refptr._fmode>
   140001209:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000120b:	89 10                	mov    DWORD PTR [rax],edx
   14000120d:	e8 ee 7b 00 00       	call   140008e00 <__p__commode>
   140001212:	48 8b 15 c7 a4 00 00 	mov    rdx,QWORD PTR [rip+0xa4c7]        # 14000b6e0 <.refptr._commode>
   140001219:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000121b:	89 10                	mov    DWORD PTR [rax],edx
   14000121d:	e8 5e 06 00 00       	call   140001880 <_setargv>
   140001222:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140001225:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140001229:	79 0a                	jns    140001235 <__tmainCRTStartup+0x1a7>
   14000122b:	b9 08 00 00 00       	mov    ecx,0x8
   140001230:	e8 43 83 00 00       	call   140009578 <_amsg_exit>
   140001235:	48 8b 05 34 a3 00 00 	mov    rax,QWORD PTR [rip+0xa334]        # 14000b570 <.refptr._MINGW_INSTALL_DEBUG_MATHERR>
   14000123c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000123e:	83 f8 01             	cmp    eax,0x1
   140001241:	75 0f                	jne    140001252 <__tmainCRTStartup+0x1c4>
   140001243:	48 8b 05 d6 a4 00 00 	mov    rax,QWORD PTR [rip+0xa4d6]        # 14000b720 <.refptr._matherr>
   14000124a:	48 89 c1             	mov    rcx,rax
   14000124d:	e8 68 11 00 00       	call   1400023ba <__mingw_setusermatherr>
   140001252:	48 8b 05 87 a3 00 00 	mov    rax,QWORD PTR [rip+0xa387]        # 14000b5e0 <.refptr.__globallocalestatus>
   140001259:	8b 00                	mov    eax,DWORD PTR [rax]
   14000125b:	83 f8 ff             	cmp    eax,0xffffffff
   14000125e:	75 0a                	jne    14000126a <__tmainCRTStartup+0x1dc>
   140001260:	b9 ff ff ff ff       	mov    ecx,0xffffffff
   140001265:	e8 16 7d 00 00       	call   140008f80 <_configthreadlocale>
   14000126a:	48 8b 15 5f a4 00 00 	mov    rdx,QWORD PTR [rip+0xa45f]        # 14000b6d0 <.refptr.__xi_z>
   140001271:	48 8b 05 48 a4 00 00 	mov    rax,QWORD PTR [rip+0xa448]        # 14000b6c0 <.refptr.__xi_a>
   140001278:	48 89 c1             	mov    rcx,rax
   14000127b:	e8 10 7b 00 00       	call   140008d90 <_initterm_e>
   140001280:	85 c0                	test   eax,eax
   140001282:	74 0a                	je     14000128e <__tmainCRTStartup+0x200>
   140001284:	b9 0a 00 00 00       	mov    ecx,0xa
   140001289:	e8 ea 82 00 00       	call   140009578 <_amsg_exit>
   14000128e:	48 8b 05 9b a4 00 00 	mov    rax,QWORD PTR [rip+0xa49b]        # 14000b730 <.refptr._newmode>
   140001295:	8b 00                	mov    eax,DWORD PTR [rax]
   140001297:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000129a:	48 8b 05 4f a4 00 00 	mov    rax,QWORD PTR [rip+0xa44f]        # 14000b6f0 <.refptr._dowildcard>
   1400012a1:	44 8b 00             	mov    r8d,DWORD PTR [rax]
   1400012a4:	4c 8d 15 65 dd 00 00 	lea    r10,[rip+0xdd65]        # 14000f010 <envp>
   1400012ab:	48 8d 15 56 dd 00 00 	lea    rdx,[rip+0xdd56]        # 14000f008 <argv>
   1400012b2:	48 8d 05 4b dd 00 00 	lea    rax,[rip+0xdd4b]        # 14000f004 <argc>
   1400012b9:	48 8d 4d ac          	lea    rcx,[rbp-0x54]
   1400012bd:	48 89 4c 24 20       	mov    QWORD PTR [rsp+0x20],rcx
   1400012c2:	45 89 c1             	mov    r9d,r8d
   1400012c5:	4d 89 d0             	mov    r8,r10
   1400012c8:	48 89 c1             	mov    rcx,rax
   1400012cb:	e8 88 82 00 00       	call   140009558 <__getmainargs>
   1400012d0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012d3:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012d7:	79 0a                	jns    1400012e3 <__tmainCRTStartup+0x255>
   1400012d9:	b9 08 00 00 00       	mov    ecx,0x8
   1400012de:	e8 95 82 00 00       	call   140009578 <_amsg_exit>
   1400012e3:	8b 05 1b dd 00 00    	mov    eax,DWORD PTR [rip+0xdd1b]        # 14000f004 <argc>
   1400012e9:	48 8d 15 18 dd 00 00 	lea    rdx,[rip+0xdd18]        # 14000f008 <argv>
   1400012f0:	89 c1                	mov    ecx,eax
   1400012f2:	e8 f9 01 00 00       	call   1400014f0 <duplicate_ppstrings>
   1400012f7:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400012fa:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   1400012fe:	74 0a                	je     14000130a <__tmainCRTStartup+0x27c>
   140001300:	b9 08 00 00 00       	mov    ecx,0x8
   140001305:	e8 6e 82 00 00       	call   140009578 <_amsg_exit>
   14000130a:	48 8b 15 9f a3 00 00 	mov    rdx,QWORD PTR [rip+0xa39f]        # 14000b6b0 <.refptr.__xc_z>
   140001311:	48 8b 05 88 a3 00 00 	mov    rax,QWORD PTR [rip+0xa388]        # 14000b6a0 <.refptr.__xc_a>
   140001318:	48 89 c1             	mov    rcx,rax
   14000131b:	e8 70 82 00 00       	call   140009590 <_initterm>
   140001320:	e8 32 05 00 00       	call   140001857 <__main>
   140001325:	48 8b 05 54 a3 00 00 	mov    rax,QWORD PTR [rip+0xa354]        # 14000b680 <.refptr.__native_startup_state>
   14000132c:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   140001332:	eb 0a                	jmp    14000133e <__tmainCRTStartup+0x2b0>
   140001334:	c7 05 de dc 00 00 01 	mov    DWORD PTR [rip+0xdcde],0x1        # 14000f01c <has_cctor>
   14000133b:	00 00 00 
   14000133e:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140001342:	75 1e                	jne    140001362 <__tmainCRTStartup+0x2d4>
   140001344:	48 8b 05 25 a3 00 00 	mov    rax,QWORD PTR [rip+0xa325]        # 14000b670 <.refptr.__native_startup_lock>
   14000134b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000134f:	48 c7 45 b0 00 00 00 	mov    QWORD PTR [rbp-0x50],0x0
   140001356:	00 
   140001357:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000135b:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000135f:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140001362:	48 8b 05 67 a2 00 00 	mov    rax,QWORD PTR [rip+0xa267]        # 14000b5d0 <.refptr.__dyn_tls_init_callback>
   140001369:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000136c:	48 85 c0             	test   rax,rax
   14000136f:	74 1c                	je     14000138d <__tmainCRTStartup+0x2ff>
   140001371:	48 8b 05 58 a2 00 00 	mov    rax,QWORD PTR [rip+0xa258]        # 14000b5d0 <.refptr.__dyn_tls_init_callback>
   140001378:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000137b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140001381:	ba 02 00 00 00       	mov    edx,0x2
   140001386:	b9 00 00 00 00       	mov    ecx,0x0
   14000138b:	ff d0                	call   rax
   14000138d:	e8 7e 7a 00 00       	call   140008e10 <__p___initenv>
   140001392:	48 8b 15 77 dc 00 00 	mov    rdx,QWORD PTR [rip+0xdc77]        # 14000f010 <envp>
   140001399:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000139c:	48 8b 0d 6d dc 00 00 	mov    rcx,QWORD PTR [rip+0xdc6d]        # 14000f010 <envp>
   1400013a3:	48 8b 15 5e dc 00 00 	mov    rdx,QWORD PTR [rip+0xdc5e]        # 14000f008 <argv>
   1400013aa:	8b 05 54 dc 00 00    	mov    eax,DWORD PTR [rip+0xdc54]        # 14000f004 <argc>
   1400013b0:	49 89 c8             	mov    r8,rcx
   1400013b3:	89 c1                	mov    ecx,eax
   1400013b5:	e8 46 83 00 00       	call   140009700 <main>
   1400013ba:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400013bd:	8b 05 55 dc 00 00    	mov    eax,DWORD PTR [rip+0xdc55]        # 14000f018 <managedapp>
   1400013c3:	85 c0                	test   eax,eax
   1400013c5:	75 0a                	jne    1400013d1 <__tmainCRTStartup+0x343>
   1400013c7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013ca:	89 c1                	mov    ecx,eax
   1400013cc:	e8 ef 81 00 00       	call   1400095c0 <exit>
   1400013d1:	8b 05 45 dc 00 00    	mov    eax,DWORD PTR [rip+0xdc45]        # 14000f01c <has_cctor>
   1400013d7:	85 c0                	test   eax,eax
   1400013d9:	75 05                	jne    1400013e0 <__tmainCRTStartup+0x352>
   1400013db:	e8 a0 81 00 00       	call   140009580 <_cexit>
   1400013e0:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   1400013e3:	48 81 c4 90 00 00 00 	add    rsp,0x90
   1400013ea:	5d                   	pop    rbp
   1400013eb:	c3                   	ret

00000001400013ec <check_managed_app>:
   1400013ec:	55                   	push   rbp
   1400013ed:	48 89 e5             	mov    rbp,rsp
   1400013f0:	48 83 ec 20          	sub    rsp,0x20
   1400013f4:	48 8b 05 35 a2 00 00 	mov    rax,QWORD PTR [rip+0xa235]        # 14000b630 <.refptr.__mingw_initltsdrot_force>
   1400013fb:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   140001401:	48 8b 05 38 a2 00 00 	mov    rax,QWORD PTR [rip+0xa238]        # 14000b640 <.refptr.__mingw_initltsdyn_force>
   140001408:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000140e:	48 8b 05 3b a2 00 00 	mov    rax,QWORD PTR [rip+0xa23b]        # 14000b650 <.refptr.__mingw_initltssuo_force>
   140001415:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   14000141b:	48 8b 05 6e a1 00 00 	mov    rax,QWORD PTR [rip+0xa16e]        # 14000b590 <.refptr.__ImageBase>
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
   140001511:	e8 da 80 00 00       	call   1400095f0 <malloc>
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
   14000155c:	e8 b7 80 00 00       	call   140009618 <strlen>
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
   140001585:	e8 66 80 00 00       	call   1400095f0 <malloc>
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
   1400015e8:	e8 0b 80 00 00       	call   1400095f8 <memcpy>
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
   140001642:	e8 61 7f 00 00       	call   1400095a8 <_crt_atexit>
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
   14000167b:	48 8d 0d 7e 99 00 00 	lea    rcx,[rip+0x997e]        # 14000b000 <.rdata>
   140001682:	ff 15 c8 eb 00 00    	call   QWORD PTR [rip+0xebc8]        # 140010250 <__imp_GetModuleHandleA>
   140001688:	48 89 c3             	mov    rbx,rax
   14000168b:	48 85 c0             	test   rax,rax
   14000168e:	74 70                	je     140001700 <__gcc_register_frame+0x90>
   140001690:	48 8d 0d 69 99 00 00 	lea    rcx,[rip+0x9969]        # 14000b000 <.rdata>
   140001697:	ff 15 d3 eb 00 00    	call   QWORD PTR [rip+0xebd3]        # 140010270 <__imp_LoadLibraryA>
   14000169d:	4c 8b 0d b4 eb 00 00 	mov    r9,QWORD PTR [rip+0xebb4]        # 140010258 <__imp_GetProcAddress>
   1400016a4:	48 8d 15 68 99 00 00 	lea    rdx,[rip+0x9968]        # 14000b013 <.rdata+0x13>
   1400016ab:	48 89 d9             	mov    rcx,rbx
   1400016ae:	48 89 05 6b d9 00 00 	mov    QWORD PTR [rip+0xd96b],rax        # 14000f020 <hmod_libgcc>
   1400016b5:	4c 89 4d f0          	mov    QWORD PTR [rbp-0x10],r9
   1400016b9:	41 ff d1             	call   r9
   1400016bc:	48 8d 15 66 99 00 00 	lea    rdx,[rip+0x9966]        # 14000b029 <.rdata+0x29>
   1400016c3:	48 89 d9             	mov    rcx,rbx
   1400016c6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400016ca:	ff 55 f0             	call   QWORD PTR [rbp-0x10]
   1400016cd:	4c 8b 45 f8          	mov    r8,QWORD PTR [rbp-0x8]
   1400016d1:	48 89 05 28 89 00 00 	mov    QWORD PTR [rip+0x8928],rax        # 14000a000 <__data_start__>
   1400016d8:	4d 85 c0             	test   r8,r8
   1400016db:	74 11                	je     1400016ee <__gcc_register_frame+0x7e>
   1400016dd:	48 8d 15 5c d9 00 00 	lea    rdx,[rip+0xd95c]        # 14000f040 <obj>
   1400016e4:	48 8d 0d 15 a9 00 00 	lea    rcx,[rip+0xa915]        # 14000c000 <__EH_FRAME_BEGIN__>
   1400016eb:	41 ff d0             	call   r8
   1400016ee:	48 8d 0d 2b 00 00 00 	lea    rcx,[rip+0x2b]        # 140001720 <__gcc_deregister_frame>
   1400016f5:	48 83 c4 38          	add    rsp,0x38
   1400016f9:	5b                   	pop    rbx
   1400016fa:	5d                   	pop    rbp
   1400016fb:	e9 2f ff ff ff       	jmp    14000162f <atexit>
   140001700:	48 8d 05 59 ff ff ff 	lea    rax,[rip+0xffffffffffffff59]        # 140001660 <.weak.__deregister_frame_info.hmod_libgcc>
   140001707:	4c 8d 05 42 ff ff ff 	lea    r8,[rip+0xffffffffffffff42]        # 140001650 <.weak.__register_frame_info.hmod_libgcc>
   14000170e:	48 89 05 eb 88 00 00 	mov    QWORD PTR [rip+0x88eb],rax        # 14000a000 <__data_start__>
   140001715:	eb c6                	jmp    1400016dd <__gcc_register_frame+0x6d>
   140001717:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
   14000171e:	00 00 

0000000140001720 <__gcc_deregister_frame>:
   140001720:	55                   	push   rbp
   140001721:	48 89 e5             	mov    rbp,rsp
   140001724:	48 83 ec 20          	sub    rsp,0x20
   140001728:	48 8b 05 d1 88 00 00 	mov    rax,QWORD PTR [rip+0x88d1]        # 14000a000 <__data_start__>
   14000172f:	48 85 c0             	test   rax,rax
   140001732:	74 09                	je     14000173d <__gcc_deregister_frame+0x1d>
   140001734:	48 8d 0d c5 a8 00 00 	lea    rcx,[rip+0xa8c5]        # 14000c000 <__EH_FRAME_BEGIN__>
   14000173b:	ff d0                	call   rax
   14000173d:	48 8b 0d dc d8 00 00 	mov    rcx,QWORD PTR [rip+0xd8dc]        # 14000f020 <hmod_libgcc>
   140001744:	48 85 c9             	test   rcx,rcx
   140001747:	74 0f                	je     140001758 <__gcc_deregister_frame+0x38>
   140001749:	48 83 c4 20          	add    rsp,0x20
   14000174d:	5d                   	pop    rbp
   14000174e:	48 ff 25 e3 ea 00 00 	rex.W jmp QWORD PTR [rip+0xeae3]        # 140010238 <__imp_FreeLibrary>
   140001755:	0f 1f 00             	nop    DWORD PTR [rax]
   140001758:	48 83 c4 20          	add    rsp,0x20
   14000175c:	5d                   	pop    rbp
   14000175d:	c3                   	ret
   14000175e:	90                   	nop
   14000175f:	90                   	nop

0000000140001760 <callD(D*)>:
   140001760:	4c 8d 05 69 7f 00 00 	lea    r8,[rip+0x7f69]        # 1400096d0 <D::f()>
   140001767:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   14000176a:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   14000176d:	4c 39 c2             	cmp    rdx,r8
   140001770:	75 0e                	jne    140001780 <callD(D*)+0x20>
   140001772:	48 8b 50 e8          	mov    rdx,QWORD PTR [rax-0x18]
   140001776:	8b 41 08             	mov    eax,DWORD PTR [rcx+0x8]
   140001779:	03 44 11 08          	add    eax,DWORD PTR [rcx+rdx*1+0x8]
   14000177d:	c3                   	ret
   14000177e:	66 90                	xchg   ax,ax
   140001780:	48 ff e2             	rex.W jmp rdx
   140001783:	66 90                	xchg   ax,ax
   140001785:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
   14000178c:	00 00 00 00 

0000000140001790 <callB(B*)>:
   140001790:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   140001793:	48 ff 20             	rex.W jmp QWORD PTR [rax]
   140001796:	90                   	nop
   140001797:	90                   	nop
   140001798:	90                   	nop
   140001799:	90                   	nop
   14000179a:	90                   	nop
   14000179b:	90                   	nop
   14000179c:	90                   	nop
   14000179d:	90                   	nop
   14000179e:	90                   	nop
   14000179f:	90                   	nop

00000001400017a0 <__do_global_dtors>:
   1400017a0:	55                   	push   rbp
   1400017a1:	48 89 e5             	mov    rbp,rsp
   1400017a4:	48 83 ec 20          	sub    rsp,0x20
   1400017a8:	eb 1e                	jmp    1400017c8 <__do_global_dtors+0x28>
   1400017aa:	48 8b 05 5f 88 00 00 	mov    rax,QWORD PTR [rip+0x885f]        # 14000a010 <p.0>
   1400017b1:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017b4:	ff d0                	call   rax
   1400017b6:	48 8b 05 53 88 00 00 	mov    rax,QWORD PTR [rip+0x8853]        # 14000a010 <p.0>
   1400017bd:	48 83 c0 08          	add    rax,0x8
   1400017c1:	48 89 05 48 88 00 00 	mov    QWORD PTR [rip+0x8848],rax        # 14000a010 <p.0>
   1400017c8:	48 8b 05 41 88 00 00 	mov    rax,QWORD PTR [rip+0x8841]        # 14000a010 <p.0>
   1400017cf:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017d2:	48 85 c0             	test   rax,rax
   1400017d5:	75 d3                	jne    1400017aa <__do_global_dtors+0xa>
   1400017d7:	90                   	nop
   1400017d8:	90                   	nop
   1400017d9:	48 83 c4 20          	add    rsp,0x20
   1400017dd:	5d                   	pop    rbp
   1400017de:	c3                   	ret

00000001400017df <__do_global_ctors>:
   1400017df:	55                   	push   rbp
   1400017e0:	48 89 e5             	mov    rbp,rsp
   1400017e3:	48 83 ec 30          	sub    rsp,0x30
   1400017e7:	48 8b 05 92 9d 00 00 	mov    rax,QWORD PTR [rip+0x9d92]        # 14000b580 <.refptr.__CTOR_LIST__>
   1400017ee:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400017f1:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400017f4:	83 7d fc ff          	cmp    DWORD PTR [rbp-0x4],0xffffffff
   1400017f8:	75 25                	jne    14000181f <__do_global_ctors+0x40>
   1400017fa:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001801:	eb 04                	jmp    140001807 <__do_global_ctors+0x28>
   140001803:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001807:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000180a:	8d 50 01             	lea    edx,[rax+0x1]
   14000180d:	48 8b 05 6c 9d 00 00 	mov    rax,QWORD PTR [rip+0x9d6c]        # 14000b580 <.refptr.__CTOR_LIST__>
   140001814:	89 d2                	mov    edx,edx
   140001816:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   14000181a:	48 85 c0             	test   rax,rax
   14000181d:	75 e4                	jne    140001803 <__do_global_ctors+0x24>
   14000181f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001822:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140001825:	eb 14                	jmp    14000183b <__do_global_ctors+0x5c>
   140001827:	48 8b 05 52 9d 00 00 	mov    rax,QWORD PTR [rip+0x9d52]        # 14000b580 <.refptr.__CTOR_LIST__>
   14000182e:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140001831:	48 8b 04 d0          	mov    rax,QWORD PTR [rax+rdx*8]
   140001835:	ff d0                	call   rax
   140001837:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   14000183b:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000183f:	75 e6                	jne    140001827 <__do_global_ctors+0x48>
   140001841:	48 8d 05 58 ff ff ff 	lea    rax,[rip+0xffffffffffffff58]        # 1400017a0 <__do_global_dtors>
   140001848:	48 89 c1             	mov    rcx,rax
   14000184b:	e8 df fd ff ff       	call   14000162f <atexit>
   140001850:	90                   	nop
   140001851:	48 83 c4 30          	add    rsp,0x30
   140001855:	5d                   	pop    rbp
   140001856:	c3                   	ret

0000000140001857 <__main>:
   140001857:	55                   	push   rbp
   140001858:	48 89 e5             	mov    rbp,rsp
   14000185b:	48 83 ec 20          	sub    rsp,0x20
   14000185f:	8b 05 1b d8 00 00    	mov    eax,DWORD PTR [rip+0xd81b]        # 14000f080 <initialized>
   140001865:	85 c0                	test   eax,eax
   140001867:	75 0f                	jne    140001878 <__main+0x21>
   140001869:	c7 05 0d d8 00 00 01 	mov    DWORD PTR [rip+0xd80d],0x1        # 14000f080 <initialized>
   140001870:	00 00 00 
   140001873:	e8 67 ff ff ff       	call   1400017df <__do_global_ctors>
   140001878:	90                   	nop
   140001879:	48 83 c4 20          	add    rsp,0x20
   14000187d:	5d                   	pop    rbp
   14000187e:	c3                   	ret
   14000187f:	90                   	nop

0000000140001880 <_setargv>:
   140001880:	55                   	push   rbp
   140001881:	48 89 e5             	mov    rbp,rsp
   140001884:	b8 00 00 00 00       	mov    eax,0x0
   140001889:	5d                   	pop    rbp
   14000188a:	c3                   	ret
   14000188b:	90                   	nop
   14000188c:	90                   	nop
   14000188d:	90                   	nop
   14000188e:	90                   	nop
   14000188f:	90                   	nop

0000000140001890 <__dyn_tls_init>:
   140001890:	55                   	push   rbp
   140001891:	48 89 e5             	mov    rbp,rsp
   140001894:	48 83 ec 30          	sub    rsp,0x30
   140001898:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000189c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000189f:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400018a3:	48 8b 05 b6 9c 00 00 	mov    rax,QWORD PTR [rip+0x9cb6]        # 14000b560 <.refptr._CRT_MT>
   1400018aa:	8b 00                	mov    eax,DWORD PTR [rax]
   1400018ac:	83 f8 02             	cmp    eax,0x2
   1400018af:	74 0d                	je     1400018be <__dyn_tls_init+0x2e>
   1400018b1:	48 8b 05 a8 9c 00 00 	mov    rax,QWORD PTR [rip+0x9ca8]        # 14000b560 <.refptr._CRT_MT>
   1400018b8:	c7 00 02 00 00 00    	mov    DWORD PTR [rax],0x2
   1400018be:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   1400018c2:	74 1e                	je     1400018e2 <__dyn_tls_init+0x52>
   1400018c4:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   1400018c8:	75 5b                	jne    140001925 <__dyn_tls_init+0x95>
   1400018ca:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   1400018ce:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   1400018d1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400018d5:	49 89 c8             	mov    r8,rcx
   1400018d8:	48 89 c1             	mov    rcx,rax
   1400018db:	e8 d1 11 00 00       	call   140002ab1 <__mingw_TLScallback>
   1400018e0:	eb 43                	jmp    140001925 <__dyn_tls_init+0x95>
   1400018e2:	48 8d 05 d7 a0 00 00 	lea    rax,[rip+0xa0d7]        # 14000b9c0 <___crt_xd_start__>
   1400018e9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400018ed:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   1400018f2:	eb 22                	jmp    140001916 <__dyn_tls_init+0x86>
   1400018f4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400018f8:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400018fc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001900:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140001903:	48 85 c0             	test   rax,rax
   140001906:	74 09                	je     140001911 <__dyn_tls_init+0x81>
   140001908:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000190c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000190f:	ff d0                	call   rax
   140001911:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140001916:	48 8d 05 ab a0 00 00 	lea    rax,[rip+0xa0ab]        # 14000b9c8 <__xd_z>
   14000191d:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140001921:	75 d1                	jne    1400018f4 <__dyn_tls_init+0x64>
   140001923:	eb 01                	jmp    140001926 <__dyn_tls_init+0x96>
   140001925:	90                   	nop
   140001926:	48 83 c4 30          	add    rsp,0x30
   14000192a:	5d                   	pop    rbp
   14000192b:	c3                   	ret

000000014000192c <__tlregdtor>:
   14000192c:	55                   	push   rbp
   14000192d:	48 89 e5             	mov    rbp,rsp
   140001930:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001934:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140001939:	75 07                	jne    140001942 <__tlregdtor+0x16>
   14000193b:	b8 00 00 00 00       	mov    eax,0x0
   140001940:	eb 05                	jmp    140001947 <__tlregdtor+0x1b>
   140001942:	b8 00 00 00 00       	mov    eax,0x0
   140001947:	5d                   	pop    rbp
   140001948:	c3                   	ret

0000000140001949 <__dyn_tls_dtor>:
   140001949:	55                   	push   rbp
   14000194a:	48 89 e5             	mov    rbp,rsp
   14000194d:	48 83 ec 20          	sub    rsp,0x20
   140001951:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001955:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140001958:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000195c:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140001960:	74 06                	je     140001968 <__dyn_tls_dtor+0x1f>
   140001962:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140001966:	75 18                	jne    140001980 <__dyn_tls_dtor+0x37>
   140001968:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   14000196c:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   14000196f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001973:	49 89 c8             	mov    r8,rcx
   140001976:	48 89 c1             	mov    rcx,rax
   140001979:	e8 33 11 00 00       	call   140002ab1 <__mingw_TLScallback>
   14000197e:	eb 01                	jmp    140001981 <__dyn_tls_dtor+0x38>
   140001980:	90                   	nop
   140001981:	48 83 c4 20          	add    rsp,0x20
   140001985:	5d                   	pop    rbp
   140001986:	c3                   	ret
   140001987:	90                   	nop
   140001988:	90                   	nop
   140001989:	90                   	nop
   14000198a:	90                   	nop
   14000198b:	90                   	nop
   14000198c:	90                   	nop
   14000198d:	90                   	nop
   14000198e:	90                   	nop
   14000198f:	90                   	nop

0000000140001990 <_matherr>:
   140001990:	55                   	push   rbp
   140001991:	53                   	push   rbx
   140001992:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140001999:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   14000199e:	0f 29 75 00          	movaps XMMWORD PTR [rbp+0x0],xmm6
   1400019a2:	0f 29 7d 10          	movaps XMMWORD PTR [rbp+0x10],xmm7
   1400019a6:	44 0f 29 45 20       	movaps XMMWORD PTR [rbp+0x20],xmm8
   1400019ab:	48 89 4d 50          	mov    QWORD PTR [rbp+0x50],rcx
   1400019af:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   1400019b3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400019b5:	83 f8 06             	cmp    eax,0x6
   1400019b8:	74 56                	je     140001a10 <_matherr+0x80>
   1400019ba:	83 f8 06             	cmp    eax,0x6
   1400019bd:	7f 78                	jg     140001a37 <_matherr+0xa7>
   1400019bf:	83 f8 05             	cmp    eax,0x5
   1400019c2:	74 59                	je     140001a1d <_matherr+0x8d>
   1400019c4:	83 f8 05             	cmp    eax,0x5
   1400019c7:	7f 6e                	jg     140001a37 <_matherr+0xa7>
   1400019c9:	83 f8 04             	cmp    eax,0x4
   1400019cc:	74 5c                	je     140001a2a <_matherr+0x9a>
   1400019ce:	83 f8 04             	cmp    eax,0x4
   1400019d1:	7f 64                	jg     140001a37 <_matherr+0xa7>
   1400019d3:	83 f8 03             	cmp    eax,0x3
   1400019d6:	74 2b                	je     140001a03 <_matherr+0x73>
   1400019d8:	83 f8 03             	cmp    eax,0x3
   1400019db:	7f 5a                	jg     140001a37 <_matherr+0xa7>
   1400019dd:	83 f8 01             	cmp    eax,0x1
   1400019e0:	74 07                	je     1400019e9 <_matherr+0x59>
   1400019e2:	83 f8 02             	cmp    eax,0x2
   1400019e5:	74 0f                	je     1400019f6 <_matherr+0x66>
   1400019e7:	eb 4e                	jmp    140001a37 <_matherr+0xa7>
   1400019e9:	48 8d 05 b0 96 00 00 	lea    rax,[rip+0x96b0]        # 14000b0a0 <.rdata>
   1400019f0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400019f4:	eb 4d                	jmp    140001a43 <_matherr+0xb3>
   1400019f6:	48 8d 05 c2 96 00 00 	lea    rax,[rip+0x96c2]        # 14000b0bf <.rdata+0x1f>
   1400019fd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a01:	eb 40                	jmp    140001a43 <_matherr+0xb3>
   140001a03:	48 8d 05 d6 96 00 00 	lea    rax,[rip+0x96d6]        # 14000b0e0 <.rdata+0x40>
   140001a0a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a0e:	eb 33                	jmp    140001a43 <_matherr+0xb3>
   140001a10:	48 8d 05 e9 96 00 00 	lea    rax,[rip+0x96e9]        # 14000b100 <.rdata+0x60>
   140001a17:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a1b:	eb 26                	jmp    140001a43 <_matherr+0xb3>
   140001a1d:	48 8d 05 04 97 00 00 	lea    rax,[rip+0x9704]        # 14000b128 <.rdata+0x88>
   140001a24:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a28:	eb 19                	jmp    140001a43 <_matherr+0xb3>
   140001a2a:	48 8d 05 1f 97 00 00 	lea    rax,[rip+0x971f]        # 14000b150 <.rdata+0xb0>
   140001a31:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a35:	eb 0c                	jmp    140001a43 <_matherr+0xb3>
   140001a37:	48 8d 05 48 97 00 00 	lea    rax,[rip+0x9748]        # 14000b186 <.rdata+0xe6>
   140001a3e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001a42:	90                   	nop
   140001a43:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a47:	f2 44 0f 10 40 20    	movsd  xmm8,QWORD PTR [rax+0x20]
   140001a4d:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a51:	f2 0f 10 78 18       	movsd  xmm7,QWORD PTR [rax+0x18]
   140001a56:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a5a:	f2 0f 10 70 10       	movsd  xmm6,QWORD PTR [rax+0x10]
   140001a5f:	48 8b 45 50          	mov    rax,QWORD PTR [rbp+0x50]
   140001a63:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
   140001a67:	b9 02 00 00 00       	mov    ecx,0x2
   140001a6c:	e8 2f 75 00 00       	call   140008fa0 <__acrt_iob_func>
   140001a71:	48 89 c1             	mov    rcx,rax
   140001a74:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140001a78:	48 8d 05 19 97 00 00 	lea    rax,[rip+0x9719]        # 14000b198 <.rdata+0xf8>
   140001a7f:	f2 44 0f 11 44 24 30 	movsd  QWORD PTR [rsp+0x30],xmm8
   140001a86:	f2 0f 11 7c 24 28    	movsd  QWORD PTR [rsp+0x28],xmm7
   140001a8c:	f2 0f 11 74 24 20    	movsd  QWORD PTR [rsp+0x20],xmm6
   140001a92:	49 89 d9             	mov    r9,rbx
   140001a95:	49 89 d0             	mov    r8,rdx
   140001a98:	48 89 c2             	mov    rdx,rax
   140001a9b:	e8 30 7b 00 00       	call   1400095d0 <fprintf>
   140001aa0:	b8 00 00 00 00       	mov    eax,0x0
   140001aa5:	0f 28 75 00          	movaps xmm6,XMMWORD PTR [rbp+0x0]
   140001aa9:	0f 28 7d 10          	movaps xmm7,XMMWORD PTR [rbp+0x10]
   140001aad:	44 0f 28 45 20       	movaps xmm8,XMMWORD PTR [rbp+0x20]
   140001ab2:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140001ab9:	5b                   	pop    rbx
   140001aba:	5d                   	pop    rbp
   140001abb:	c3                   	ret
   140001abc:	90                   	nop
   140001abd:	90                   	nop
   140001abe:	90                   	nop
   140001abf:	90                   	nop

0000000140001ac0 <__report_error>:
   140001ac0:	55                   	push   rbp
   140001ac1:	53                   	push   rbx
   140001ac2:	48 83 ec 38          	sub    rsp,0x38
   140001ac6:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140001acb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140001acf:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140001ad3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140001ad7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140001adb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   140001adf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001ae3:	b9 02 00 00 00       	mov    ecx,0x2
   140001ae8:	e8 b3 74 00 00       	call   140008fa0 <__acrt_iob_func>
   140001aed:	48 89 c1             	mov    rcx,rax
   140001af0:	48 8d 05 d9 96 00 00 	lea    rax,[rip+0x96d9]        # 14000b1d0 <.rdata>
   140001af7:	48 89 c2             	mov    rdx,rax
   140001afa:	e8 d1 7a 00 00       	call   1400095d0 <fprintf>
   140001aff:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   140001b03:	b9 02 00 00 00       	mov    ecx,0x2
   140001b08:	e8 93 74 00 00       	call   140008fa0 <__acrt_iob_func>
   140001b0d:	48 89 c1             	mov    rcx,rax
   140001b10:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001b14:	49 89 d8             	mov    r8,rbx
   140001b17:	48 89 c2             	mov    rdx,rax
   140001b1a:	e8 09 7b 00 00       	call   140009628 <vfprintf>
   140001b1f:	e8 8c 7a 00 00       	call   1400095b0 <abort>
   140001b24:	90                   	nop

0000000140001b25 <mark_section_writable>:
   140001b25:	55                   	push   rbp
   140001b26:	48 89 e5             	mov    rbp,rsp
   140001b29:	48 83 ec 60          	sub    rsp,0x60
   140001b2d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001b31:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001b38:	e9 82 00 00 00       	jmp    140001bbf <mark_section_writable+0x9a>
   140001b3d:	48 8b 0d 9c d5 00 00 	mov    rcx,QWORD PTR [rip+0xd59c]        # 14000f0e0 <the_secs>
   140001b44:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b47:	48 63 d0             	movsxd rdx,eax
   140001b4a:	48 89 d0             	mov    rax,rdx
   140001b4d:	48 c1 e0 02          	shl    rax,0x2
   140001b51:	48 01 d0             	add    rax,rdx
   140001b54:	48 c1 e0 03          	shl    rax,0x3
   140001b58:	48 01 c8             	add    rax,rcx
   140001b5b:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001b5f:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001b63:	72 56                	jb     140001bbb <mark_section_writable+0x96>
   140001b65:	48 8b 0d 74 d5 00 00 	mov    rcx,QWORD PTR [rip+0xd574]        # 14000f0e0 <the_secs>
   140001b6c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b6f:	48 63 d0             	movsxd rdx,eax
   140001b72:	48 89 d0             	mov    rax,rdx
   140001b75:	48 c1 e0 02          	shl    rax,0x2
   140001b79:	48 01 d0             	add    rax,rdx
   140001b7c:	48 c1 e0 03          	shl    rax,0x3
   140001b80:	48 01 c8             	add    rax,rcx
   140001b83:	48 8b 48 18          	mov    rcx,QWORD PTR [rax+0x18]
   140001b87:	4c 8b 05 52 d5 00 00 	mov    r8,QWORD PTR [rip+0xd552]        # 14000f0e0 <the_secs>
   140001b8e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001b91:	48 63 d0             	movsxd rdx,eax
   140001b94:	48 89 d0             	mov    rax,rdx
   140001b97:	48 c1 e0 02          	shl    rax,0x2
   140001b9b:	48 01 d0             	add    rax,rdx
   140001b9e:	48 c1 e0 03          	shl    rax,0x3
   140001ba2:	4c 01 c0             	add    rax,r8
   140001ba5:	48 8b 40 20          	mov    rax,QWORD PTR [rax+0x20]
   140001ba9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001bac:	89 c0                	mov    eax,eax
   140001bae:	48 01 c8             	add    rax,rcx
   140001bb1:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140001bb5:	0f 82 41 02 00 00    	jb     140001dfc <mark_section_writable+0x2d7>
   140001bbb:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001bbf:	8b 05 23 d5 00 00    	mov    eax,DWORD PTR [rip+0xd523]        # 14000f0e8 <maxSections>
   140001bc5:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001bc8:	0f 8c 6f ff ff ff    	jl     140001b3d <mark_section_writable+0x18>
   140001bce:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001bd2:	48 89 c1             	mov    rcx,rax
   140001bd5:	e8 c1 11 00 00       	call   140002d9b <__mingw_GetSectionForAddress>
   140001bda:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140001bde:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140001be3:	75 13                	jne    140001bf8 <mark_section_writable+0xd3>
   140001be5:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001be9:	48 8d 0d 00 96 00 00 	lea    rcx,[rip+0x9600]        # 14000b1f0 <.rdata+0x20>
   140001bf0:	48 89 c2             	mov    rdx,rax
   140001bf3:	e8 c8 fe ff ff       	call   140001ac0 <__report_error>
   140001bf8:	48 8b 0d e1 d4 00 00 	mov    rcx,QWORD PTR [rip+0xd4e1]        # 14000f0e0 <the_secs>
   140001bff:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c02:	48 63 d0             	movsxd rdx,eax
   140001c05:	48 89 d0             	mov    rax,rdx
   140001c08:	48 c1 e0 02          	shl    rax,0x2
   140001c0c:	48 01 d0             	add    rax,rdx
   140001c0f:	48 c1 e0 03          	shl    rax,0x3
   140001c13:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001c17:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c1b:	48 89 42 20          	mov    QWORD PTR [rdx+0x20],rax
   140001c1f:	48 8b 0d ba d4 00 00 	mov    rcx,QWORD PTR [rip+0xd4ba]        # 14000f0e0 <the_secs>
   140001c26:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c29:	48 63 d0             	movsxd rdx,eax
   140001c2c:	48 89 d0             	mov    rax,rdx
   140001c2f:	48 c1 e0 02          	shl    rax,0x2
   140001c33:	48 01 d0             	add    rax,rdx
   140001c36:	48 c1 e0 03          	shl    rax,0x3
   140001c3a:	48 01 c8             	add    rax,rcx
   140001c3d:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140001c43:	e8 9f 12 00 00       	call   140002ee7 <_GetPEImageBase>
   140001c48:	48 89 c1             	mov    rcx,rax
   140001c4b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001c4f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140001c52:	41 89 c1             	mov    r9d,eax
   140001c55:	4c 8b 05 84 d4 00 00 	mov    r8,QWORD PTR [rip+0xd484]        # 14000f0e0 <the_secs>
   140001c5c:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c5f:	48 63 d0             	movsxd rdx,eax
   140001c62:	48 89 d0             	mov    rax,rdx
   140001c65:	48 c1 e0 02          	shl    rax,0x2
   140001c69:	48 01 d0             	add    rax,rdx
   140001c6c:	48 c1 e0 03          	shl    rax,0x3
   140001c70:	4c 01 c0             	add    rax,r8
   140001c73:	4a 8d 14 09          	lea    rdx,[rcx+r9*1]
   140001c77:	48 89 50 18          	mov    QWORD PTR [rax+0x18],rdx
   140001c7b:	48 8b 0d 5e d4 00 00 	mov    rcx,QWORD PTR [rip+0xd45e]        # 14000f0e0 <the_secs>
   140001c82:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001c85:	48 63 d0             	movsxd rdx,eax
   140001c88:	48 89 d0             	mov    rax,rdx
   140001c8b:	48 c1 e0 02          	shl    rax,0x2
   140001c8f:	48 01 d0             	add    rax,rdx
   140001c92:	48 c1 e0 03          	shl    rax,0x3
   140001c96:	48 01 c8             	add    rax,rcx
   140001c99:	48 8b 40 18          	mov    rax,QWORD PTR [rax+0x18]
   140001c9d:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140001ca1:	41 b8 30 00 00 00    	mov    r8d,0x30
   140001ca7:	48 89 c1             	mov    rcx,rax
   140001caa:	48 8b 05 ef e5 00 00 	mov    rax,QWORD PTR [rip+0xe5ef]        # 1400102a0 <__imp_VirtualQuery>
   140001cb1:	ff d0                	call   rax
   140001cb3:	48 85 c0             	test   rax,rax
   140001cb6:	75 3f                	jne    140001cf7 <mark_section_writable+0x1d2>
   140001cb8:	48 8b 0d 21 d4 00 00 	mov    rcx,QWORD PTR [rip+0xd421]        # 14000f0e0 <the_secs>
   140001cbf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001cc2:	48 63 d0             	movsxd rdx,eax
   140001cc5:	48 89 d0             	mov    rax,rdx
   140001cc8:	48 c1 e0 02          	shl    rax,0x2
   140001ccc:	48 01 d0             	add    rax,rdx
   140001ccf:	48 c1 e0 03          	shl    rax,0x3
   140001cd3:	48 01 c8             	add    rax,rcx
   140001cd6:	48 8b 50 18          	mov    rdx,QWORD PTR [rax+0x18]
   140001cda:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140001cde:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001ce1:	89 c1                	mov    ecx,eax
   140001ce3:	48 8d 05 26 95 00 00 	lea    rax,[rip+0x9526]        # 14000b210 <.rdata+0x40>
   140001cea:	49 89 d0             	mov    r8,rdx
   140001ced:	89 ca                	mov    edx,ecx
   140001cef:	48 89 c1             	mov    rcx,rax
   140001cf2:	e8 c9 fd ff ff       	call   140001ac0 <__report_error>
   140001cf7:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001cfa:	83 f8 40             	cmp    eax,0x40
   140001cfd:	0f 84 e8 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d03:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d06:	83 f8 04             	cmp    eax,0x4
   140001d09:	0f 84 dc 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d0f:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d12:	3d 80 00 00 00       	cmp    eax,0x80
   140001d17:	0f 84 ce 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d1d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d20:	83 f8 08             	cmp    eax,0x8
   140001d23:	0f 84 c2 00 00 00    	je     140001deb <mark_section_writable+0x2c6>
   140001d29:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140001d2c:	83 f8 02             	cmp    eax,0x2
   140001d2f:	75 09                	jne    140001d3a <mark_section_writable+0x215>
   140001d31:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140001d38:	eb 07                	jmp    140001d41 <mark_section_writable+0x21c>
   140001d3a:	c7 45 f8 40 00 00 00 	mov    DWORD PTR [rbp-0x8],0x40
   140001d41:	48 8b 0d 98 d3 00 00 	mov    rcx,QWORD PTR [rip+0xd398]        # 14000f0e0 <the_secs>
   140001d48:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d4b:	48 63 d0             	movsxd rdx,eax
   140001d4e:	48 89 d0             	mov    rax,rdx
   140001d51:	48 c1 e0 02          	shl    rax,0x2
   140001d55:	48 01 d0             	add    rax,rdx
   140001d58:	48 c1 e0 03          	shl    rax,0x3
   140001d5c:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d60:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001d64:	48 89 42 08          	mov    QWORD PTR [rdx+0x8],rax
   140001d68:	48 8b 0d 71 d3 00 00 	mov    rcx,QWORD PTR [rip+0xd371]        # 14000f0e0 <the_secs>
   140001d6f:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d72:	48 63 d0             	movsxd rdx,eax
   140001d75:	48 89 d0             	mov    rax,rdx
   140001d78:	48 c1 e0 02          	shl    rax,0x2
   140001d7c:	48 01 d0             	add    rax,rdx
   140001d7f:	48 c1 e0 03          	shl    rax,0x3
   140001d83:	48 8d 14 01          	lea    rdx,[rcx+rax*1]
   140001d87:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140001d8b:	48 89 42 10          	mov    QWORD PTR [rdx+0x10],rax
   140001d8f:	48 8b 0d 4a d3 00 00 	mov    rcx,QWORD PTR [rip+0xd34a]        # 14000f0e0 <the_secs>
   140001d96:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001d99:	48 63 d0             	movsxd rdx,eax
   140001d9c:	48 89 d0             	mov    rax,rdx
   140001d9f:	48 c1 e0 02          	shl    rax,0x2
   140001da3:	48 01 d0             	add    rax,rdx
   140001da6:	48 c1 e0 03          	shl    rax,0x3
   140001daa:	48 01 c8             	add    rax,rcx
   140001dad:	49 89 c0             	mov    r8,rax
   140001db0:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140001db4:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140001db8:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140001dbb:	4d 89 c1             	mov    r9,r8
   140001dbe:	41 89 c8             	mov    r8d,ecx
   140001dc1:	48 89 c1             	mov    rcx,rax
   140001dc4:	48 8b 05 cd e4 00 00 	mov    rax,QWORD PTR [rip+0xe4cd]        # 140010298 <__imp_VirtualProtect>
   140001dcb:	ff d0                	call   rax
   140001dcd:	85 c0                	test   eax,eax
   140001dcf:	75 1a                	jne    140001deb <mark_section_writable+0x2c6>
   140001dd1:	48 8b 05 70 e4 00 00 	mov    rax,QWORD PTR [rip+0xe470]        # 140010248 <__imp_GetLastError>
   140001dd8:	ff d0                	call   rax
   140001dda:	89 c2                	mov    edx,eax
   140001ddc:	48 8d 05 65 94 00 00 	lea    rax,[rip+0x9465]        # 14000b248 <.rdata+0x78>
   140001de3:	48 89 c1             	mov    rcx,rax
   140001de6:	e8 d5 fc ff ff       	call   140001ac0 <__report_error>
   140001deb:	8b 05 f7 d2 00 00    	mov    eax,DWORD PTR [rip+0xd2f7]        # 14000f0e8 <maxSections>
   140001df1:	83 c0 01             	add    eax,0x1
   140001df4:	89 05 ee d2 00 00    	mov    DWORD PTR [rip+0xd2ee],eax        # 14000f0e8 <maxSections>
   140001dfa:	eb 01                	jmp    140001dfd <mark_section_writable+0x2d8>
   140001dfc:	90                   	nop
   140001dfd:	48 83 c4 60          	add    rsp,0x60
   140001e01:	5d                   	pop    rbp
   140001e02:	c3                   	ret

0000000140001e03 <restore_modified_sections>:
   140001e03:	55                   	push   rbp
   140001e04:	48 89 e5             	mov    rbp,rsp
   140001e07:	48 83 ec 30          	sub    rsp,0x30
   140001e0b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140001e12:	e9 ad 00 00 00       	jmp    140001ec4 <restore_modified_sections+0xc1>
   140001e17:	48 8b 0d c2 d2 00 00 	mov    rcx,QWORD PTR [rip+0xd2c2]        # 14000f0e0 <the_secs>
   140001e1e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e21:	48 63 d0             	movsxd rdx,eax
   140001e24:	48 89 d0             	mov    rax,rdx
   140001e27:	48 c1 e0 02          	shl    rax,0x2
   140001e2b:	48 01 d0             	add    rax,rdx
   140001e2e:	48 c1 e0 03          	shl    rax,0x3
   140001e32:	48 01 c8             	add    rax,rcx
   140001e35:	8b 00                	mov    eax,DWORD PTR [rax]
   140001e37:	85 c0                	test   eax,eax
   140001e39:	0f 84 80 00 00 00    	je     140001ebf <restore_modified_sections+0xbc>
   140001e3f:	48 8b 0d 9a d2 00 00 	mov    rcx,QWORD PTR [rip+0xd29a]        # 14000f0e0 <the_secs>
   140001e46:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e49:	48 63 d0             	movsxd rdx,eax
   140001e4c:	48 89 d0             	mov    rax,rdx
   140001e4f:	48 c1 e0 02          	shl    rax,0x2
   140001e53:	48 01 d0             	add    rax,rdx
   140001e56:	48 c1 e0 03          	shl    rax,0x3
   140001e5a:	48 01 c8             	add    rax,rcx
   140001e5d:	44 8b 10             	mov    r10d,DWORD PTR [rax]
   140001e60:	48 8b 0d 79 d2 00 00 	mov    rcx,QWORD PTR [rip+0xd279]        # 14000f0e0 <the_secs>
   140001e67:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e6a:	48 63 d0             	movsxd rdx,eax
   140001e6d:	48 89 d0             	mov    rax,rdx
   140001e70:	48 c1 e0 02          	shl    rax,0x2
   140001e74:	48 01 d0             	add    rax,rdx
   140001e77:	48 c1 e0 03          	shl    rax,0x3
   140001e7b:	48 01 c8             	add    rax,rcx
   140001e7e:	48 8b 48 10          	mov    rcx,QWORD PTR [rax+0x10]
   140001e82:	4c 8b 05 57 d2 00 00 	mov    r8,QWORD PTR [rip+0xd257]        # 14000f0e0 <the_secs>
   140001e89:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140001e8c:	48 63 d0             	movsxd rdx,eax
   140001e8f:	48 89 d0             	mov    rax,rdx
   140001e92:	48 c1 e0 02          	shl    rax,0x2
   140001e96:	48 01 d0             	add    rax,rdx
   140001e99:	48 c1 e0 03          	shl    rax,0x3
   140001e9d:	4c 01 c0             	add    rax,r8
   140001ea0:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
   140001ea4:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   140001ea8:	49 89 d1             	mov    r9,rdx
   140001eab:	45 89 d0             	mov    r8d,r10d
   140001eae:	48 89 ca             	mov    rdx,rcx
   140001eb1:	48 89 c1             	mov    rcx,rax
   140001eb4:	48 8b 05 dd e3 00 00 	mov    rax,QWORD PTR [rip+0xe3dd]        # 140010298 <__imp_VirtualProtect>
   140001ebb:	ff d0                	call   rax
   140001ebd:	eb 01                	jmp    140001ec0 <restore_modified_sections+0xbd>
   140001ebf:	90                   	nop
   140001ec0:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140001ec4:	8b 05 1e d2 00 00    	mov    eax,DWORD PTR [rip+0xd21e]        # 14000f0e8 <maxSections>
   140001eca:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140001ecd:	0f 8c 44 ff ff ff    	jl     140001e17 <restore_modified_sections+0x14>
   140001ed3:	90                   	nop
   140001ed4:	90                   	nop
   140001ed5:	48 83 c4 30          	add    rsp,0x30
   140001ed9:	5d                   	pop    rbp
   140001eda:	c3                   	ret

0000000140001edb <__write_memory>:
   140001edb:	55                   	push   rbp
   140001edc:	48 89 e5             	mov    rbp,rsp
   140001edf:	48 83 ec 20          	sub    rsp,0x20
   140001ee3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001ee7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001eeb:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001eef:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140001ef4:	74 25                	je     140001f1b <__write_memory+0x40>
   140001ef6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001efa:	48 89 c1             	mov    rcx,rax
   140001efd:	e8 23 fc ff ff       	call   140001b25 <mark_section_writable>
   140001f02:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140001f06:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140001f0a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f0e:	49 89 c8             	mov    r8,rcx
   140001f11:	48 89 c1             	mov    rcx,rax
   140001f14:	e8 df 76 00 00       	call   1400095f8 <memcpy>
   140001f19:	eb 01                	jmp    140001f1c <__write_memory+0x41>
   140001f1b:	90                   	nop
   140001f1c:	48 83 c4 20          	add    rsp,0x20
   140001f20:	5d                   	pop    rbp
   140001f21:	c3                   	ret

0000000140001f22 <do_pseudo_reloc>:
   140001f22:	55                   	push   rbp
   140001f23:	48 89 e5             	mov    rbp,rsp
   140001f26:	48 83 c4 80          	add    rsp,0xffffffffffffff80
   140001f2a:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140001f2e:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140001f32:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140001f36:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140001f3a:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140001f3e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001f42:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140001f46:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140001f4a:	48 83 7d e0 07       	cmp    QWORD PTR [rbp-0x20],0x7
   140001f4f:	0f 8e 44 03 00 00    	jle    140002299 <do_pseudo_reloc+0x377>
   140001f55:	48 83 7d e0 0b       	cmp    QWORD PTR [rbp-0x20],0xb
   140001f5a:	7e 25                	jle    140001f81 <do_pseudo_reloc+0x5f>
   140001f5c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f60:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f62:	85 c0                	test   eax,eax
   140001f64:	75 1b                	jne    140001f81 <do_pseudo_reloc+0x5f>
   140001f66:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f6a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f6d:	85 c0                	test   eax,eax
   140001f6f:	75 10                	jne    140001f81 <do_pseudo_reloc+0x5f>
   140001f71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f75:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001f78:	85 c0                	test   eax,eax
   140001f7a:	75 05                	jne    140001f81 <do_pseudo_reloc+0x5f>
   140001f7c:	48 83 45 f8 0c       	add    QWORD PTR [rbp-0x8],0xc
   140001f81:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f85:	8b 00                	mov    eax,DWORD PTR [rax]
   140001f87:	85 c0                	test   eax,eax
   140001f89:	75 0b                	jne    140001f96 <do_pseudo_reloc+0x74>
   140001f8b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f8f:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001f92:	85 c0                	test   eax,eax
   140001f94:	74 59                	je     140001fef <do_pseudo_reloc+0xcd>
   140001f96:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001f9a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140001f9e:	eb 40                	jmp    140001fe0 <do_pseudo_reloc+0xbe>
   140001fa0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fa4:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140001fa7:	89 c2                	mov    edx,eax
   140001fa9:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140001fad:	48 01 d0             	add    rax,rdx
   140001fb0:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140001fb4:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fb8:	8b 10                	mov    edx,DWORD PTR [rax]
   140001fba:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fbe:	8b 00                	mov    eax,DWORD PTR [rax]
   140001fc0:	01 d0                	add    eax,edx
   140001fc2:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
   140001fc5:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140001fc9:	48 8d 55 b4          	lea    rdx,[rbp-0x4c]
   140001fcd:	41 b8 04 00 00 00    	mov    r8d,0x4
   140001fd3:	48 89 c1             	mov    rcx,rax
   140001fd6:	e8 00 ff ff ff       	call   140001edb <__write_memory>
   140001fdb:	48 83 45 e8 08       	add    QWORD PTR [rbp-0x18],0x8
   140001fe0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140001fe4:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140001fe8:	72 b6                	jb     140001fa0 <do_pseudo_reloc+0x7e>
   140001fea:	e9 ab 02 00 00       	jmp    14000229a <do_pseudo_reloc+0x378>
   140001fef:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001ff3:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140001ff6:	83 f8 01             	cmp    eax,0x1
   140001ff9:	74 18                	je     140002013 <do_pseudo_reloc+0xf1>
   140001ffb:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140001fff:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002002:	89 c2                	mov    edx,eax
   140002004:	48 8d 05 65 92 00 00 	lea    rax,[rip+0x9265]        # 14000b270 <.rdata+0xa0>
   14000200b:	48 89 c1             	mov    rcx,rax
   14000200e:	e8 ad fa ff ff       	call   140001ac0 <__report_error>
   140002013:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002017:	48 83 c0 0c          	add    rax,0xc
   14000201b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000201f:	e9 65 02 00 00       	jmp    140002289 <do_pseudo_reloc+0x367>
   140002024:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002028:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000202b:	89 c2                	mov    edx,eax
   14000202d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002031:	48 01 d0             	add    rax,rdx
   140002034:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002038:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000203c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000203e:	89 c2                	mov    edx,eax
   140002040:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002044:	48 01 d0             	add    rax,rdx
   140002047:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000204b:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000204f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002052:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002056:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000205a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000205d:	0f b6 c0             	movzx  eax,al
   140002060:	83 f8 40             	cmp    eax,0x40
   140002063:	0f 84 b6 00 00 00    	je     14000211f <do_pseudo_reloc+0x1fd>
   140002069:	83 f8 40             	cmp    eax,0x40
   14000206c:	0f 87 ba 00 00 00    	ja     14000212c <do_pseudo_reloc+0x20a>
   140002072:	83 f8 20             	cmp    eax,0x20
   140002075:	74 77                	je     1400020ee <do_pseudo_reloc+0x1cc>
   140002077:	83 f8 20             	cmp    eax,0x20
   14000207a:	0f 87 ac 00 00 00    	ja     14000212c <do_pseudo_reloc+0x20a>
   140002080:	83 f8 08             	cmp    eax,0x8
   140002083:	74 0a                	je     14000208f <do_pseudo_reloc+0x16d>
   140002085:	83 f8 10             	cmp    eax,0x10
   140002088:	74 38                	je     1400020c2 <do_pseudo_reloc+0x1a0>
   14000208a:	e9 9d 00 00 00       	jmp    14000212c <do_pseudo_reloc+0x20a>
   14000208f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002093:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140002096:	0f b6 c0             	movzx  eax,al
   140002099:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000209d:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020a1:	25 80 00 00 00       	and    eax,0x80
   1400020a6:	48 85 c0             	test   rax,rax
   1400020a9:	0f 84 9d 00 00 00    	je     14000214c <do_pseudo_reloc+0x22a>
   1400020af:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020b3:	48 0d 00 ff ff ff    	or     rax,0xffffffffffffff00
   1400020b9:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020bd:	e9 8a 00 00 00       	jmp    14000214c <do_pseudo_reloc+0x22a>
   1400020c2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020c6:	0f b7 00             	movzx  eax,WORD PTR [rax]
   1400020c9:	0f b7 c0             	movzx  eax,ax
   1400020cc:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020d0:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020d4:	25 00 80 00 00       	and    eax,0x8000
   1400020d9:	48 85 c0             	test   rax,rax
   1400020dc:	74 71                	je     14000214f <do_pseudo_reloc+0x22d>
   1400020de:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020e2:	48 0d 00 00 ff ff    	or     rax,0xffffffffffff0000
   1400020e8:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020ec:	eb 61                	jmp    14000214f <do_pseudo_reloc+0x22d>
   1400020ee:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400020f2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400020f4:	89 c0                	mov    eax,eax
   1400020f6:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400020fa:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400020fe:	25 00 00 00 80       	and    eax,0x80000000
   140002103:	48 85 c0             	test   rax,rax
   140002106:	74 4a                	je     140002152 <do_pseudo_reloc+0x230>
   140002108:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000210c:	48 ba 00 00 00 00 ff 	movabs rdx,0xffffffff00000000
   140002113:	ff ff ff 
   140002116:	48 09 d0             	or     rax,rdx
   140002119:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000211d:	eb 33                	jmp    140002152 <do_pseudo_reloc+0x230>
   14000211f:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002123:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002126:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000212a:	eb 27                	jmp    140002153 <do_pseudo_reloc+0x231>
   14000212c:	48 c7 45 b8 00 00 00 	mov    QWORD PTR [rbp-0x48],0x0
   140002133:	00 
   140002134:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002138:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000213b:	0f b6 c0             	movzx  eax,al
   14000213e:	48 8d 0d 63 91 00 00 	lea    rcx,[rip+0x9163]        # 14000b2a8 <.rdata+0xd8>
   140002145:	89 c2                	mov    edx,eax
   140002147:	e8 74 f9 ff ff       	call   140001ac0 <__report_error>
   14000214c:	90                   	nop
   14000214d:	eb 04                	jmp    140002153 <do_pseudo_reloc+0x231>
   14000214f:	90                   	nop
   140002150:	eb 01                	jmp    140002153 <do_pseudo_reloc+0x231>
   140002152:	90                   	nop
   140002153:	48 8b 4d b8          	mov    rcx,QWORD PTR [rbp-0x48]
   140002157:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000215b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000215d:	89 c2                	mov    edx,eax
   14000215f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140002163:	48 01 c2             	add    rdx,rax
   140002166:	48 89 c8             	mov    rax,rcx
   140002169:	48 29 d0             	sub    rax,rdx
   14000216c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140002170:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140002174:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140002178:	48 01 d0             	add    rax,rdx
   14000217b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000217f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002183:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002186:	25 ff 00 00 00       	and    eax,0xff
   14000218b:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000218e:	83 7d d4 3f          	cmp    DWORD PTR [rbp-0x2c],0x3f
   140002192:	77 67                	ja     1400021fb <do_pseudo_reloc+0x2d9>
   140002194:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140002197:	ba 01 00 00 00       	mov    edx,0x1
   14000219c:	89 c1                	mov    ecx,eax
   14000219e:	48 d3 e2             	shl    rdx,cl
   1400021a1:	48 89 d0             	mov    rax,rdx
   1400021a4:	48 83 e8 01          	sub    rax,0x1
   1400021a8:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   1400021ac:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021af:	83 e8 01             	sub    eax,0x1
   1400021b2:	48 c7 c2 ff ff ff ff 	mov    rdx,0xffffffffffffffff
   1400021b9:	89 c1                	mov    ecx,eax
   1400021bb:	48 d3 e2             	shl    rdx,cl
   1400021be:	48 89 d0             	mov    rax,rdx
   1400021c1:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400021c5:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021c9:	48 39 45 c8          	cmp    QWORD PTR [rbp-0x38],rax
   1400021cd:	7c 0a                	jl     1400021d9 <do_pseudo_reloc+0x2b7>
   1400021cf:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400021d3:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400021d7:	7e 22                	jle    1400021fb <do_pseudo_reloc+0x2d9>
   1400021d9:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   1400021dd:	4c 8b 4d d8          	mov    r9,QWORD PTR [rbp-0x28]
   1400021e1:	4c 8b 45 e0          	mov    r8,QWORD PTR [rbp-0x20]
   1400021e5:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400021e8:	48 8d 0d e9 90 00 00 	lea    rcx,[rip+0x90e9]        # 14000b2d8 <.rdata+0x108>
   1400021ef:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   1400021f4:	89 c2                	mov    edx,eax
   1400021f6:	e8 c5 f8 ff ff       	call   140001ac0 <__report_error>
   1400021fb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400021ff:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002202:	0f b6 c0             	movzx  eax,al
   140002205:	83 f8 40             	cmp    eax,0x40
   140002208:	74 63                	je     14000226d <do_pseudo_reloc+0x34b>
   14000220a:	83 f8 40             	cmp    eax,0x40
   14000220d:	77 75                	ja     140002284 <do_pseudo_reloc+0x362>
   14000220f:	83 f8 20             	cmp    eax,0x20
   140002212:	74 41                	je     140002255 <do_pseudo_reloc+0x333>
   140002214:	83 f8 20             	cmp    eax,0x20
   140002217:	77 6b                	ja     140002284 <do_pseudo_reloc+0x362>
   140002219:	83 f8 08             	cmp    eax,0x8
   14000221c:	74 07                	je     140002225 <do_pseudo_reloc+0x303>
   14000221e:	83 f8 10             	cmp    eax,0x10
   140002221:	74 1a                	je     14000223d <do_pseudo_reloc+0x31b>
   140002223:	eb 5f                	jmp    140002284 <do_pseudo_reloc+0x362>
   140002225:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002229:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000222d:	41 b8 01 00 00 00    	mov    r8d,0x1
   140002233:	48 89 c1             	mov    rcx,rax
   140002236:	e8 a0 fc ff ff       	call   140001edb <__write_memory>
   14000223b:	eb 47                	jmp    140002284 <do_pseudo_reloc+0x362>
   14000223d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002241:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002245:	41 b8 02 00 00 00    	mov    r8d,0x2
   14000224b:	48 89 c1             	mov    rcx,rax
   14000224e:	e8 88 fc ff ff       	call   140001edb <__write_memory>
   140002253:	eb 2f                	jmp    140002284 <do_pseudo_reloc+0x362>
   140002255:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002259:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   14000225d:	41 b8 04 00 00 00    	mov    r8d,0x4
   140002263:	48 89 c1             	mov    rcx,rax
   140002266:	e8 70 fc ff ff       	call   140001edb <__write_memory>
   14000226b:	eb 17                	jmp    140002284 <do_pseudo_reloc+0x362>
   14000226d:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002271:	48 8d 55 b8          	lea    rdx,[rbp-0x48]
   140002275:	41 b8 08 00 00 00    	mov    r8d,0x8
   14000227b:	48 89 c1             	mov    rcx,rax
   14000227e:	e8 58 fc ff ff       	call   140001edb <__write_memory>
   140002283:	90                   	nop
   140002284:	48 83 45 f0 0c       	add    QWORD PTR [rbp-0x10],0xc
   140002289:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000228d:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140002291:	0f 82 8d fd ff ff    	jb     140002024 <do_pseudo_reloc+0x102>
   140002297:	eb 01                	jmp    14000229a <do_pseudo_reloc+0x378>
   140002299:	90                   	nop
   14000229a:	48 83 ec 80          	sub    rsp,0xffffffffffffff80
   14000229e:	5d                   	pop    rbp
   14000229f:	c3                   	ret

00000001400022a0 <_pei386_runtime_relocator>:
   1400022a0:	55                   	push   rbp
   1400022a1:	48 89 e5             	mov    rbp,rsp
   1400022a4:	48 83 ec 30          	sub    rsp,0x30
   1400022a8:	8b 05 3e ce 00 00    	mov    eax,DWORD PTR [rip+0xce3e]        # 14000f0ec <was_init.0>
   1400022ae:	85 c0                	test   eax,eax
   1400022b0:	0f 85 88 00 00 00    	jne    14000233e <_pei386_runtime_relocator+0x9e>
   1400022b6:	8b 05 30 ce 00 00    	mov    eax,DWORD PTR [rip+0xce30]        # 14000f0ec <was_init.0>
   1400022bc:	83 c0 01             	add    eax,0x1
   1400022bf:	89 05 27 ce 00 00    	mov    DWORD PTR [rip+0xce27],eax        # 14000f0ec <was_init.0>
   1400022c5:	e8 21 0b 00 00       	call   140002deb <__mingw_GetSectionCount>
   1400022ca:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400022cd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400022d0:	48 63 d0             	movsxd rdx,eax
   1400022d3:	48 89 d0             	mov    rax,rdx
   1400022d6:	48 c1 e0 02          	shl    rax,0x2
   1400022da:	48 01 d0             	add    rax,rdx
   1400022dd:	48 c1 e0 03          	shl    rax,0x3
   1400022e1:	48 83 c0 0f          	add    rax,0xf
   1400022e5:	48 c1 e8 04          	shr    rax,0x4
   1400022e9:	48 c1 e0 04          	shl    rax,0x4
   1400022ed:	e8 7e 0d 00 00       	call   140003070 <___chkstk_ms>
   1400022f2:	48 29 c4             	sub    rsp,rax
   1400022f5:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400022fa:	48 83 c0 0f          	add    rax,0xf
   1400022fe:	48 c1 e8 04          	shr    rax,0x4
   140002302:	48 c1 e0 04          	shl    rax,0x4
   140002306:	48 89 05 d3 cd 00 00 	mov    QWORD PTR [rip+0xcdd3],rax        # 14000f0e0 <the_secs>
   14000230d:	c7 05 d1 cd 00 00 00 	mov    DWORD PTR [rip+0xcdd1],0x0        # 14000f0e8 <maxSections>
   140002314:	00 00 00 
   140002317:	48 8b 0d 72 92 00 00 	mov    rcx,QWORD PTR [rip+0x9272]        # 14000b590 <.refptr.__ImageBase>
   14000231e:	48 8b 15 7b 92 00 00 	mov    rdx,QWORD PTR [rip+0x927b]        # 14000b5a0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST_END__>
   140002325:	48 8b 05 84 92 00 00 	mov    rax,QWORD PTR [rip+0x9284]        # 14000b5b0 <.refptr.__RUNTIME_PSEUDO_RELOC_LIST__>
   14000232c:	49 89 c8             	mov    r8,rcx
   14000232f:	48 89 c1             	mov    rcx,rax
   140002332:	e8 eb fb ff ff       	call   140001f22 <do_pseudo_reloc>
   140002337:	e8 c7 fa ff ff       	call   140001e03 <restore_modified_sections>
   14000233c:	eb 01                	jmp    14000233f <_pei386_runtime_relocator+0x9f>
   14000233e:	90                   	nop
   14000233f:	48 89 ec             	mov    rsp,rbp
   140002342:	5d                   	pop    rbp
   140002343:	c3                   	ret
   140002344:	90                   	nop
   140002345:	90                   	nop
   140002346:	90                   	nop
   140002347:	90                   	nop
   140002348:	90                   	nop
   140002349:	90                   	nop
   14000234a:	90                   	nop
   14000234b:	90                   	nop
   14000234c:	90                   	nop
   14000234d:	90                   	nop
   14000234e:	90                   	nop
   14000234f:	90                   	nop

0000000140002350 <__mingw_raise_matherr>:
   140002350:	55                   	push   rbp
   140002351:	48 89 e5             	mov    rbp,rsp
   140002354:	48 83 ec 50          	sub    rsp,0x50
   140002358:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000235b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000235f:	f2 0f 11 55 20       	movsd  QWORD PTR [rbp+0x20],xmm2
   140002364:	f2 0f 11 5d 28       	movsd  QWORD PTR [rbp+0x28],xmm3
   140002369:	48 8b 05 80 cd 00 00 	mov    rax,QWORD PTR [rip+0xcd80]        # 14000f0f0 <stUserMathErr>
   140002370:	48 85 c0             	test   rax,rax
   140002373:	74 3e                	je     1400023b3 <__mingw_raise_matherr+0x63>
   140002375:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140002378:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   14000237b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000237f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002383:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140002388:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   14000238d:	f2 0f 10 45 28       	movsd  xmm0,QWORD PTR [rbp+0x28]
   140002392:	f2 0f 11 45 e8       	movsd  QWORD PTR [rbp-0x18],xmm0
   140002397:	f2 0f 10 45 30       	movsd  xmm0,QWORD PTR [rbp+0x30]
   14000239c:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   1400023a1:	48 8b 15 48 cd 00 00 	mov    rdx,QWORD PTR [rip+0xcd48]        # 14000f0f0 <stUserMathErr>
   1400023a8:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   1400023ac:	48 89 c1             	mov    rcx,rax
   1400023af:	ff d2                	call   rdx
   1400023b1:	eb 01                	jmp    1400023b4 <__mingw_raise_matherr+0x64>
   1400023b3:	90                   	nop
   1400023b4:	48 83 c4 50          	add    rsp,0x50
   1400023b8:	5d                   	pop    rbp
   1400023b9:	c3                   	ret

00000001400023ba <__mingw_setusermatherr>:
   1400023ba:	55                   	push   rbp
   1400023bb:	48 89 e5             	mov    rbp,rsp
   1400023be:	48 83 ec 20          	sub    rsp,0x20
   1400023c2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023c6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023ca:	48 89 05 1f cd 00 00 	mov    QWORD PTR [rip+0xcd1f],rax        # 14000f0f0 <stUserMathErr>
   1400023d1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400023d5:	48 89 c1             	mov    rcx,rax
   1400023d8:	e8 93 71 00 00       	call   140009570 <__setusermatherr>
   1400023dd:	90                   	nop
   1400023de:	48 83 c4 20          	add    rsp,0x20
   1400023e2:	5d                   	pop    rbp
   1400023e3:	c3                   	ret
   1400023e4:	90                   	nop
   1400023e5:	90                   	nop
   1400023e6:	90                   	nop
   1400023e7:	90                   	nop
   1400023e8:	90                   	nop
   1400023e9:	90                   	nop
   1400023ea:	90                   	nop
   1400023eb:	90                   	nop
   1400023ec:	90                   	nop
   1400023ed:	90                   	nop
   1400023ee:	90                   	nop
   1400023ef:	90                   	nop

00000001400023f0 <__mingw_SEH_error_handler>:
   1400023f0:	55                   	push   rbp
   1400023f1:	48 89 e5             	mov    rbp,rsp
   1400023f4:	48 83 ec 30          	sub    rsp,0x30
   1400023f8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400023fc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002400:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002404:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140002408:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   14000240f:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002416:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000241a:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000241d:	83 e0 02             	and    eax,0x2
   140002420:	85 c0                	test   eax,eax
   140002422:	74 0a                	je     14000242e <__mingw_SEH_error_handler+0x3e>
   140002424:	b8 01 00 00 00       	mov    eax,0x1
   140002429:	e9 16 02 00 00       	jmp    140002644 <__mingw_SEH_error_handler+0x254>
   14000242e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002432:	8b 00                	mov    eax,DWORD PTR [rax]
   140002434:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002439:	3d 43 43 47 20       	cmp    eax,0x20474343
   14000243e:	75 18                	jne    140002458 <__mingw_SEH_error_handler+0x68>
   140002440:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002444:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002447:	83 e0 01             	and    eax,0x1
   14000244a:	85 c0                	test   eax,eax
   14000244c:	75 0a                	jne    140002458 <__mingw_SEH_error_handler+0x68>
   14000244e:	b8 00 00 00 00       	mov    eax,0x0
   140002453:	e9 ec 01 00 00       	jmp    140002644 <__mingw_SEH_error_handler+0x254>
   140002458:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000245c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000245e:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   140002463:	0f 84 12 01 00 00    	je     14000257b <__mingw_SEH_error_handler+0x18b>
   140002469:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   14000246e:	0f 87 c3 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   140002474:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   140002479:	0f 87 b8 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   14000247f:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   140002484:	0f 83 4c 01 00 00    	jae    1400025d6 <__mingw_SEH_error_handler+0x1e6>
   14000248a:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000248f:	0f 84 3a 01 00 00    	je     1400025cf <__mingw_SEH_error_handler+0x1df>
   140002495:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   14000249a:	0f 87 97 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024a0:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024a5:	0f 84 83 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   1400024ab:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400024b0:	0f 87 81 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024b6:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400024bb:	0f 87 76 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024c1:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   1400024c6:	0f 83 03 01 00 00    	jae    1400025cf <__mingw_SEH_error_handler+0x1df>
   1400024cc:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024d1:	0f 84 57 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   1400024d7:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   1400024dc:	0f 87 55 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024e2:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024e7:	0f 84 8e 00 00 00    	je     14000257b <__mingw_SEH_error_handler+0x18b>
   1400024ed:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   1400024f2:	0f 87 3f 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   1400024f8:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   1400024fd:	0f 84 2b 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   140002503:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002508:	0f 87 29 01 00 00    	ja     140002637 <__mingw_SEH_error_handler+0x247>
   14000250e:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002513:	0f 84 15 01 00 00    	je     14000262e <__mingw_SEH_error_handler+0x23e>
   140002519:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000251e:	0f 85 13 01 00 00    	jne    140002637 <__mingw_SEH_error_handler+0x247>
   140002524:	ba 00 00 00 00       	mov    edx,0x0
   140002529:	b9 0b 00 00 00       	mov    ecx,0xb
   14000252e:	e8 d5 70 00 00       	call   140009608 <signal>
   140002533:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002537:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000253c:	75 1b                	jne    140002559 <__mingw_SEH_error_handler+0x169>
   14000253e:	ba 01 00 00 00       	mov    edx,0x1
   140002543:	b9 0b 00 00 00       	mov    ecx,0xb
   140002548:	e8 bb 70 00 00       	call   140009608 <signal>
   14000254d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002554:	e9 e1 00 00 00       	jmp    14000263a <__mingw_SEH_error_handler+0x24a>
   140002559:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000255e:	0f 84 d6 00 00 00    	je     14000263a <__mingw_SEH_error_handler+0x24a>
   140002564:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002568:	b9 0b 00 00 00       	mov    ecx,0xb
   14000256d:	ff d0                	call   rax
   14000256f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002576:	e9 bf 00 00 00       	jmp    14000263a <__mingw_SEH_error_handler+0x24a>
   14000257b:	ba 00 00 00 00       	mov    edx,0x0
   140002580:	b9 04 00 00 00       	mov    ecx,0x4
   140002585:	e8 7e 70 00 00       	call   140009608 <signal>
   14000258a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000258e:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   140002593:	75 1b                	jne    1400025b0 <__mingw_SEH_error_handler+0x1c0>
   140002595:	ba 01 00 00 00       	mov    edx,0x1
   14000259a:	b9 04 00 00 00       	mov    ecx,0x4
   14000259f:	e8 64 70 00 00       	call   140009608 <signal>
   1400025a4:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025ab:	e9 8d 00 00 00       	jmp    14000263d <__mingw_SEH_error_handler+0x24d>
   1400025b0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400025b5:	0f 84 82 00 00 00    	je     14000263d <__mingw_SEH_error_handler+0x24d>
   1400025bb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400025bf:	b9 04 00 00 00       	mov    ecx,0x4
   1400025c4:	ff d0                	call   rax
   1400025c6:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400025cd:	eb 6e                	jmp    14000263d <__mingw_SEH_error_handler+0x24d>
   1400025cf:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400025d6:	ba 00 00 00 00       	mov    edx,0x0
   1400025db:	b9 08 00 00 00       	mov    ecx,0x8
   1400025e0:	e8 23 70 00 00       	call   140009608 <signal>
   1400025e5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400025e9:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400025ee:	75 23                	jne    140002613 <__mingw_SEH_error_handler+0x223>
   1400025f0:	ba 01 00 00 00       	mov    edx,0x1
   1400025f5:	b9 08 00 00 00       	mov    ecx,0x8
   1400025fa:	e8 09 70 00 00       	call   140009608 <signal>
   1400025ff:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002603:	74 05                	je     14000260a <__mingw_SEH_error_handler+0x21a>
   140002605:	e8 a6 05 00 00       	call   140002bb0 <_fpreset>
   14000260a:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002611:	eb 2d                	jmp    140002640 <__mingw_SEH_error_handler+0x250>
   140002613:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002618:	74 26                	je     140002640 <__mingw_SEH_error_handler+0x250>
   14000261a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000261e:	b9 08 00 00 00       	mov    ecx,0x8
   140002623:	ff d0                	call   rax
   140002625:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000262c:	eb 12                	jmp    140002640 <__mingw_SEH_error_handler+0x250>
   14000262e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140002635:	eb 0a                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   140002637:	90                   	nop
   140002638:	eb 07                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   14000263a:	90                   	nop
   14000263b:	eb 04                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   14000263d:	90                   	nop
   14000263e:	eb 01                	jmp    140002641 <__mingw_SEH_error_handler+0x251>
   140002640:	90                   	nop
   140002641:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140002644:	48 83 c4 30          	add    rsp,0x30
   140002648:	5d                   	pop    rbp
   140002649:	c3                   	ret

000000014000264a <_gnu_exception_handler>:
   14000264a:	55                   	push   rbp
   14000264b:	48 89 e5             	mov    rbp,rsp
   14000264e:	48 83 ec 30          	sub    rsp,0x30
   140002652:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002656:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000265d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140002664:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002668:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000266b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000266d:	25 ff ff ff 20       	and    eax,0x20ffffff
   140002672:	3d 43 43 47 20       	cmp    eax,0x20474343
   140002677:	75 1b                	jne    140002694 <_gnu_exception_handler+0x4a>
   140002679:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000267d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140002680:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140002683:	83 e0 01             	and    eax,0x1
   140002686:	85 c0                	test   eax,eax
   140002688:	75 0a                	jne    140002694 <_gnu_exception_handler+0x4a>
   14000268a:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000268f:	e9 14 02 00 00       	jmp    1400028a8 <_gnu_exception_handler+0x25e>
   140002694:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002698:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000269b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000269d:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026a2:	0f 84 12 01 00 00    	je     1400027ba <_gnu_exception_handler+0x170>
   1400026a8:	3d 96 00 00 c0       	cmp    eax,0xc0000096
   1400026ad:	0f 87 c3 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026b3:	3d 95 00 00 c0       	cmp    eax,0xc0000095
   1400026b8:	0f 87 b8 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026be:	3d 94 00 00 c0       	cmp    eax,0xc0000094
   1400026c3:	0f 83 4c 01 00 00    	jae    140002815 <_gnu_exception_handler+0x1cb>
   1400026c9:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026ce:	0f 84 3a 01 00 00    	je     14000280e <_gnu_exception_handler+0x1c4>
   1400026d4:	3d 93 00 00 c0       	cmp    eax,0xc0000093
   1400026d9:	0f 87 97 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026df:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026e4:	0f 84 83 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   1400026ea:	3d 92 00 00 c0       	cmp    eax,0xc0000092
   1400026ef:	0f 87 81 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   1400026f5:	3d 91 00 00 c0       	cmp    eax,0xc0000091
   1400026fa:	0f 87 76 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   140002700:	3d 8d 00 00 c0       	cmp    eax,0xc000008d
   140002705:	0f 83 03 01 00 00    	jae    14000280e <_gnu_exception_handler+0x1c4>
   14000270b:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   140002710:	0f 84 57 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   140002716:	3d 8c 00 00 c0       	cmp    eax,0xc000008c
   14000271b:	0f 87 55 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   140002721:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002726:	0f 84 8e 00 00 00    	je     1400027ba <_gnu_exception_handler+0x170>
   14000272c:	3d 1d 00 00 c0       	cmp    eax,0xc000001d
   140002731:	0f 87 3f 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   140002737:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   14000273c:	0f 84 2b 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   140002742:	3d 08 00 00 c0       	cmp    eax,0xc0000008
   140002747:	0f 87 29 01 00 00    	ja     140002876 <_gnu_exception_handler+0x22c>
   14000274d:	3d 02 00 00 80       	cmp    eax,0x80000002
   140002752:	0f 84 15 01 00 00    	je     14000286d <_gnu_exception_handler+0x223>
   140002758:	3d 05 00 00 c0       	cmp    eax,0xc0000005
   14000275d:	0f 85 13 01 00 00    	jne    140002876 <_gnu_exception_handler+0x22c>
   140002763:	ba 00 00 00 00       	mov    edx,0x0
   140002768:	b9 0b 00 00 00       	mov    ecx,0xb
   14000276d:	e8 96 6e 00 00       	call   140009608 <signal>
   140002772:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002776:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000277b:	75 1b                	jne    140002798 <_gnu_exception_handler+0x14e>
   14000277d:	ba 01 00 00 00       	mov    edx,0x1
   140002782:	b9 0b 00 00 00       	mov    ecx,0xb
   140002787:	e8 7c 6e 00 00       	call   140009608 <signal>
   14000278c:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002793:	e9 e1 00 00 00       	jmp    140002879 <_gnu_exception_handler+0x22f>
   140002798:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000279d:	0f 84 d6 00 00 00    	je     140002879 <_gnu_exception_handler+0x22f>
   1400027a3:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027a7:	b9 0b 00 00 00       	mov    ecx,0xb
   1400027ac:	ff d0                	call   rax
   1400027ae:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027b5:	e9 bf 00 00 00       	jmp    140002879 <_gnu_exception_handler+0x22f>
   1400027ba:	ba 00 00 00 00       	mov    edx,0x0
   1400027bf:	b9 04 00 00 00       	mov    ecx,0x4
   1400027c4:	e8 3f 6e 00 00       	call   140009608 <signal>
   1400027c9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400027cd:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   1400027d2:	75 1b                	jne    1400027ef <_gnu_exception_handler+0x1a5>
   1400027d4:	ba 01 00 00 00       	mov    edx,0x1
   1400027d9:	b9 04 00 00 00       	mov    ecx,0x4
   1400027de:	e8 25 6e 00 00       	call   140009608 <signal>
   1400027e3:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   1400027ea:	e9 8d 00 00 00       	jmp    14000287c <_gnu_exception_handler+0x232>
   1400027ef:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400027f4:	0f 84 82 00 00 00    	je     14000287c <_gnu_exception_handler+0x232>
   1400027fa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400027fe:	b9 04 00 00 00       	mov    ecx,0x4
   140002803:	ff d0                	call   rax
   140002805:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000280c:	eb 6e                	jmp    14000287c <_gnu_exception_handler+0x232>
   14000280e:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140002815:	ba 00 00 00 00       	mov    edx,0x0
   14000281a:	b9 08 00 00 00       	mov    ecx,0x8
   14000281f:	e8 e4 6d 00 00       	call   140009608 <signal>
   140002824:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002828:	48 83 7d f0 01       	cmp    QWORD PTR [rbp-0x10],0x1
   14000282d:	75 23                	jne    140002852 <_gnu_exception_handler+0x208>
   14000282f:	ba 01 00 00 00       	mov    edx,0x1
   140002834:	b9 08 00 00 00       	mov    ecx,0x8
   140002839:	e8 ca 6d 00 00       	call   140009608 <signal>
   14000283e:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140002842:	74 05                	je     140002849 <_gnu_exception_handler+0x1ff>
   140002844:	e8 67 03 00 00       	call   140002bb0 <_fpreset>
   140002849:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002850:	eb 2d                	jmp    14000287f <_gnu_exception_handler+0x235>
   140002852:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002857:	74 26                	je     14000287f <_gnu_exception_handler+0x235>
   140002859:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000285d:	b9 08 00 00 00       	mov    ecx,0x8
   140002862:	ff d0                	call   rax
   140002864:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   14000286b:	eb 12                	jmp    14000287f <_gnu_exception_handler+0x235>
   14000286d:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
   140002874:	eb 0a                	jmp    140002880 <_gnu_exception_handler+0x236>
   140002876:	90                   	nop
   140002877:	eb 07                	jmp    140002880 <_gnu_exception_handler+0x236>
   140002879:	90                   	nop
   14000287a:	eb 04                	jmp    140002880 <_gnu_exception_handler+0x236>
   14000287c:	90                   	nop
   14000287d:	eb 01                	jmp    140002880 <_gnu_exception_handler+0x236>
   14000287f:	90                   	nop
   140002880:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140002884:	75 1f                	jne    1400028a5 <_gnu_exception_handler+0x25b>
   140002886:	48 8b 05 83 c8 00 00 	mov    rax,QWORD PTR [rip+0xc883]        # 14000f110 <__mingw_oldexcpt_handler>
   14000288d:	48 85 c0             	test   rax,rax
   140002890:	74 13                	je     1400028a5 <_gnu_exception_handler+0x25b>
   140002892:	48 8b 15 77 c8 00 00 	mov    rdx,QWORD PTR [rip+0xc877]        # 14000f110 <__mingw_oldexcpt_handler>
   140002899:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000289d:	48 89 c1             	mov    rcx,rax
   1400028a0:	ff d2                	call   rdx
   1400028a2:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400028a5:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400028a8:	48 83 c4 30          	add    rsp,0x30
   1400028ac:	5d                   	pop    rbp
   1400028ad:	c3                   	ret
   1400028ae:	90                   	nop
   1400028af:	90                   	nop

00000001400028b0 <___w64_mingwthr_add_key_dtor>:
   1400028b0:	55                   	push   rbp
   1400028b1:	48 89 e5             	mov    rbp,rsp
   1400028b4:	48 83 ec 30          	sub    rsp,0x30
   1400028b8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400028bb:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400028bf:	8b 05 83 c8 00 00    	mov    eax,DWORD PTR [rip+0xc883]        # 14000f148 <__mingwthr_cs_init>
   1400028c5:	85 c0                	test   eax,eax
   1400028c7:	75 07                	jne    1400028d0 <___w64_mingwthr_add_key_dtor+0x20>
   1400028c9:	b8 00 00 00 00       	mov    eax,0x0
   1400028ce:	eb 7b                	jmp    14000294b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028d0:	ba 18 00 00 00       	mov    edx,0x18
   1400028d5:	b9 01 00 00 00       	mov    ecx,0x1
   1400028da:	e8 d9 6c 00 00       	call   1400095b8 <calloc>
   1400028df:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400028e3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400028e8:	75 07                	jne    1400028f1 <___w64_mingwthr_add_key_dtor+0x41>
   1400028ea:	b8 ff ff ff ff       	mov    eax,0xffffffff
   1400028ef:	eb 5a                	jmp    14000294b <___w64_mingwthr_add_key_dtor+0x9b>
   1400028f1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028f5:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   1400028f8:	89 10                	mov    DWORD PTR [rax],edx
   1400028fa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400028fe:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140002902:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
   140002906:	48 8d 05 13 c8 00 00 	lea    rax,[rip+0xc813]        # 14000f120 <__mingwthr_cs>
   14000290d:	48 89 c1             	mov    rcx,rax
   140002910:	48 8b 05 19 d9 00 00 	mov    rax,QWORD PTR [rip+0xd919]        # 140010230 <__imp_EnterCriticalSection>
   140002917:	ff d0                	call   rax
   140002919:	48 8b 15 30 c8 00 00 	mov    rdx,QWORD PTR [rip+0xc830]        # 14000f150 <key_dtor_list>
   140002920:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002924:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   140002928:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000292c:	48 89 05 1d c8 00 00 	mov    QWORD PTR [rip+0xc81d],rax        # 14000f150 <key_dtor_list>
   140002933:	48 8d 05 e6 c7 00 00 	lea    rax,[rip+0xc7e6]        # 14000f120 <__mingwthr_cs>
   14000293a:	48 89 c1             	mov    rcx,rax
   14000293d:	48 8b 05 24 d9 00 00 	mov    rax,QWORD PTR [rip+0xd924]        # 140010268 <__imp_LeaveCriticalSection>
   140002944:	ff d0                	call   rax
   140002946:	b8 00 00 00 00       	mov    eax,0x0
   14000294b:	48 83 c4 30          	add    rsp,0x30
   14000294f:	5d                   	pop    rbp
   140002950:	c3                   	ret

0000000140002951 <___w64_mingwthr_remove_key_dtor>:
   140002951:	55                   	push   rbp
   140002952:	48 89 e5             	mov    rbp,rsp
   140002955:	48 83 ec 30          	sub    rsp,0x30
   140002959:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000295c:	8b 05 e6 c7 00 00    	mov    eax,DWORD PTR [rip+0xc7e6]        # 14000f148 <__mingwthr_cs_init>
   140002962:	85 c0                	test   eax,eax
   140002964:	75 0a                	jne    140002970 <___w64_mingwthr_remove_key_dtor+0x1f>
   140002966:	b8 00 00 00 00       	mov    eax,0x0
   14000296b:	e9 9c 00 00 00       	jmp    140002a0c <___w64_mingwthr_remove_key_dtor+0xbb>
   140002970:	48 8d 05 a9 c7 00 00 	lea    rax,[rip+0xc7a9]        # 14000f120 <__mingwthr_cs>
   140002977:	48 89 c1             	mov    rcx,rax
   14000297a:	48 8b 05 af d8 00 00 	mov    rax,QWORD PTR [rip+0xd8af]        # 140010230 <__imp_EnterCriticalSection>
   140002981:	ff d0                	call   rax
   140002983:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   14000298a:	00 
   14000298b:	48 8b 05 be c7 00 00 	mov    rax,QWORD PTR [rip+0xc7be]        # 14000f150 <key_dtor_list>
   140002992:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002996:	eb 55                	jmp    1400029ed <___w64_mingwthr_remove_key_dtor+0x9c>
   140002998:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000299c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000299e:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   1400029a1:	75 36                	jne    1400029d9 <___w64_mingwthr_remove_key_dtor+0x88>
   1400029a3:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400029a8:	75 11                	jne    1400029bb <___w64_mingwthr_remove_key_dtor+0x6a>
   1400029aa:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029ae:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029b2:	48 89 05 97 c7 00 00 	mov    QWORD PTR [rip+0xc797],rax        # 14000f150 <key_dtor_list>
   1400029b9:	eb 10                	jmp    1400029cb <___w64_mingwthr_remove_key_dtor+0x7a>
   1400029bb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029bf:	48 8b 50 10          	mov    rdx,QWORD PTR [rax+0x10]
   1400029c3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400029c7:	48 89 50 10          	mov    QWORD PTR [rax+0x10],rdx
   1400029cb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029cf:	48 89 c1             	mov    rcx,rax
   1400029d2:	e8 09 6c 00 00       	call   1400095e0 <free>
   1400029d7:	eb 1b                	jmp    1400029f4 <___w64_mingwthr_remove_key_dtor+0xa3>
   1400029d9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029dd:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400029e1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400029e5:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   1400029e9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400029ed:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400029f2:	75 a4                	jne    140002998 <___w64_mingwthr_remove_key_dtor+0x47>
   1400029f4:	48 8d 05 25 c7 00 00 	lea    rax,[rip+0xc725]        # 14000f120 <__mingwthr_cs>
   1400029fb:	48 89 c1             	mov    rcx,rax
   1400029fe:	48 8b 05 63 d8 00 00 	mov    rax,QWORD PTR [rip+0xd863]        # 140010268 <__imp_LeaveCriticalSection>
   140002a05:	ff d0                	call   rax
   140002a07:	b8 00 00 00 00       	mov    eax,0x0
   140002a0c:	48 83 c4 30          	add    rsp,0x30
   140002a10:	5d                   	pop    rbp
   140002a11:	c3                   	ret

0000000140002a12 <__mingwthr_run_key_dtors>:
   140002a12:	55                   	push   rbp
   140002a13:	48 89 e5             	mov    rbp,rsp
   140002a16:	48 83 ec 30          	sub    rsp,0x30
   140002a1a:	8b 05 28 c7 00 00    	mov    eax,DWORD PTR [rip+0xc728]        # 14000f148 <__mingwthr_cs_init>
   140002a20:	85 c0                	test   eax,eax
   140002a22:	0f 84 82 00 00 00    	je     140002aaa <__mingwthr_run_key_dtors+0x98>
   140002a28:	48 8d 05 f1 c6 00 00 	lea    rax,[rip+0xc6f1]        # 14000f120 <__mingwthr_cs>
   140002a2f:	48 89 c1             	mov    rcx,rax
   140002a32:	48 8b 05 f7 d7 00 00 	mov    rax,QWORD PTR [rip+0xd7f7]        # 140010230 <__imp_EnterCriticalSection>
   140002a39:	ff d0                	call   rax
   140002a3b:	48 8b 05 0e c7 00 00 	mov    rax,QWORD PTR [rip+0xc70e]        # 14000f150 <key_dtor_list>
   140002a42:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a46:	eb 46                	jmp    140002a8e <__mingwthr_run_key_dtors+0x7c>
   140002a48:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a4c:	8b 00                	mov    eax,DWORD PTR [rax]
   140002a4e:	89 c1                	mov    ecx,eax
   140002a50:	48 8b 05 39 d8 00 00 	mov    rax,QWORD PTR [rip+0xd839]        # 140010290 <__imp_TlsGetValue>
   140002a57:	ff d0                	call   rax
   140002a59:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002a5d:	48 8b 05 e4 d7 00 00 	mov    rax,QWORD PTR [rip+0xd7e4]        # 140010248 <__imp_GetLastError>
   140002a64:	ff d0                	call   rax
   140002a66:	85 c0                	test   eax,eax
   140002a68:	75 18                	jne    140002a82 <__mingwthr_run_key_dtors+0x70>
   140002a6a:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140002a6f:	74 11                	je     140002a82 <__mingwthr_run_key_dtors+0x70>
   140002a71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a75:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140002a79:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002a7d:	48 89 c1             	mov    rcx,rax
   140002a80:	ff d2                	call   rdx
   140002a82:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002a86:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002a8a:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002a8e:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002a93:	75 b3                	jne    140002a48 <__mingwthr_run_key_dtors+0x36>
   140002a95:	48 8d 05 84 c6 00 00 	lea    rax,[rip+0xc684]        # 14000f120 <__mingwthr_cs>
   140002a9c:	48 89 c1             	mov    rcx,rax
   140002a9f:	48 8b 05 c2 d7 00 00 	mov    rax,QWORD PTR [rip+0xd7c2]        # 140010268 <__imp_LeaveCriticalSection>
   140002aa6:	ff d0                	call   rax
   140002aa8:	eb 01                	jmp    140002aab <__mingwthr_run_key_dtors+0x99>
   140002aaa:	90                   	nop
   140002aab:	48 83 c4 30          	add    rsp,0x30
   140002aaf:	5d                   	pop    rbp
   140002ab0:	c3                   	ret

0000000140002ab1 <__mingw_TLScallback>:
   140002ab1:	55                   	push   rbp
   140002ab2:	48 89 e5             	mov    rbp,rsp
   140002ab5:	48 83 ec 30          	sub    rsp,0x30
   140002ab9:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002abd:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140002ac0:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140002ac4:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ac8:	0f 84 cc 00 00 00    	je     140002b9a <__mingw_TLScallback+0xe9>
   140002ace:	83 7d 18 03          	cmp    DWORD PTR [rbp+0x18],0x3
   140002ad2:	0f 87 ca 00 00 00    	ja     140002ba2 <__mingw_TLScallback+0xf1>
   140002ad8:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002adc:	0f 84 b1 00 00 00    	je     140002b93 <__mingw_TLScallback+0xe2>
   140002ae2:	83 7d 18 02          	cmp    DWORD PTR [rbp+0x18],0x2
   140002ae6:	0f 87 b6 00 00 00    	ja     140002ba2 <__mingw_TLScallback+0xf1>
   140002aec:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140002af0:	74 33                	je     140002b25 <__mingw_TLScallback+0x74>
   140002af2:	83 7d 18 01          	cmp    DWORD PTR [rbp+0x18],0x1
   140002af6:	0f 85 a6 00 00 00    	jne    140002ba2 <__mingw_TLScallback+0xf1>
   140002afc:	8b 05 46 c6 00 00    	mov    eax,DWORD PTR [rip+0xc646]        # 14000f148 <__mingwthr_cs_init>
   140002b02:	85 c0                	test   eax,eax
   140002b04:	75 13                	jne    140002b19 <__mingw_TLScallback+0x68>
   140002b06:	48 8d 05 13 c6 00 00 	lea    rax,[rip+0xc613]        # 14000f120 <__mingwthr_cs>
   140002b0d:	48 89 c1             	mov    rcx,rax
   140002b10:	48 8b 05 49 d7 00 00 	mov    rax,QWORD PTR [rip+0xd749]        # 140010260 <__imp_InitializeCriticalSection>
   140002b17:	ff d0                	call   rax
   140002b19:	c7 05 25 c6 00 00 01 	mov    DWORD PTR [rip+0xc625],0x1        # 14000f148 <__mingwthr_cs_init>
   140002b20:	00 00 00 
   140002b23:	eb 7d                	jmp    140002ba2 <__mingw_TLScallback+0xf1>
   140002b25:	e8 e8 fe ff ff       	call   140002a12 <__mingwthr_run_key_dtors>
   140002b2a:	8b 05 18 c6 00 00    	mov    eax,DWORD PTR [rip+0xc618]        # 14000f148 <__mingwthr_cs_init>
   140002b30:	83 f8 01             	cmp    eax,0x1
   140002b33:	75 6c                	jne    140002ba1 <__mingw_TLScallback+0xf0>
   140002b35:	48 8b 05 14 c6 00 00 	mov    rax,QWORD PTR [rip+0xc614]        # 14000f150 <key_dtor_list>
   140002b3c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b40:	eb 20                	jmp    140002b62 <__mingw_TLScallback+0xb1>
   140002b42:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b46:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
   140002b4a:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002b4e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002b52:	48 89 c1             	mov    rcx,rax
   140002b55:	e8 86 6a 00 00       	call   1400095e0 <free>
   140002b5a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002b5e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002b62:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140002b67:	75 d9                	jne    140002b42 <__mingw_TLScallback+0x91>
   140002b69:	48 c7 05 dc c5 00 00 	mov    QWORD PTR [rip+0xc5dc],0x0        # 14000f150 <key_dtor_list>
   140002b70:	00 00 00 00 
   140002b74:	c7 05 ca c5 00 00 00 	mov    DWORD PTR [rip+0xc5ca],0x0        # 14000f148 <__mingwthr_cs_init>
   140002b7b:	00 00 00 
   140002b7e:	48 8d 05 9b c5 00 00 	lea    rax,[rip+0xc59b]        # 14000f120 <__mingwthr_cs>
   140002b85:	48 89 c1             	mov    rcx,rax
   140002b88:	48 8b 05 99 d6 00 00 	mov    rax,QWORD PTR [rip+0xd699]        # 140010228 <__imp_DeleteCriticalSection>
   140002b8f:	ff d0                	call   rax
   140002b91:	eb 0e                	jmp    140002ba1 <__mingw_TLScallback+0xf0>
   140002b93:	e8 18 00 00 00       	call   140002bb0 <_fpreset>
   140002b98:	eb 08                	jmp    140002ba2 <__mingw_TLScallback+0xf1>
   140002b9a:	e8 73 fe ff ff       	call   140002a12 <__mingwthr_run_key_dtors>
   140002b9f:	eb 01                	jmp    140002ba2 <__mingw_TLScallback+0xf1>
   140002ba1:	90                   	nop
   140002ba2:	b8 01 00 00 00       	mov    eax,0x1
   140002ba7:	48 83 c4 30          	add    rsp,0x30
   140002bab:	5d                   	pop    rbp
   140002bac:	c3                   	ret
   140002bad:	90                   	nop
   140002bae:	90                   	nop
   140002baf:	90                   	nop

0000000140002bb0 <_fpreset>:
   140002bb0:	55                   	push   rbp
   140002bb1:	48 89 e5             	mov    rbp,rsp
   140002bb4:	db e3                	fninit
   140002bb6:	90                   	nop
   140002bb7:	5d                   	pop    rbp
   140002bb8:	c3                   	ret
   140002bb9:	90                   	nop
   140002bba:	90                   	nop
   140002bbb:	90                   	nop
   140002bbc:	90                   	nop
   140002bbd:	90                   	nop
   140002bbe:	90                   	nop
   140002bbf:	90                   	nop

0000000140002bc0 <_ValidateImageBase>:
   140002bc0:	55                   	push   rbp
   140002bc1:	48 89 e5             	mov    rbp,rsp
   140002bc4:	48 83 ec 20          	sub    rsp,0x20
   140002bc8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002bcc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002bd0:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002bd4:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bd8:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002bdb:	66 3d 4d 5a          	cmp    ax,0x5a4d
   140002bdf:	74 07                	je     140002be8 <_ValidateImageBase+0x28>
   140002be1:	b8 00 00 00 00       	mov    eax,0x0
   140002be6:	eb 4e                	jmp    140002c36 <_ValidateImageBase+0x76>
   140002be8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bec:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002bef:	48 63 d0             	movsxd rdx,eax
   140002bf2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002bf6:	48 01 d0             	add    rax,rdx
   140002bf9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002bfd:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c01:	8b 00                	mov    eax,DWORD PTR [rax]
   140002c03:	3d 50 45 00 00       	cmp    eax,0x4550
   140002c08:	74 07                	je     140002c11 <_ValidateImageBase+0x51>
   140002c0a:	b8 00 00 00 00       	mov    eax,0x0
   140002c0f:	eb 25                	jmp    140002c36 <_ValidateImageBase+0x76>
   140002c11:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002c15:	48 83 c0 18          	add    rax,0x18
   140002c19:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c1d:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c21:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140002c24:	66 3d 0b 02          	cmp    ax,0x20b
   140002c28:	74 07                	je     140002c31 <_ValidateImageBase+0x71>
   140002c2a:	b8 00 00 00 00       	mov    eax,0x0
   140002c2f:	eb 05                	jmp    140002c36 <_ValidateImageBase+0x76>
   140002c31:	b8 01 00 00 00       	mov    eax,0x1
   140002c36:	48 83 c4 20          	add    rsp,0x20
   140002c3a:	5d                   	pop    rbp
   140002c3b:	c3                   	ret

0000000140002c3c <_FindPESection>:
   140002c3c:	55                   	push   rbp
   140002c3d:	48 89 e5             	mov    rbp,rsp
   140002c40:	48 83 ec 20          	sub    rsp,0x20
   140002c44:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002c48:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140002c4c:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c50:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002c53:	48 63 d0             	movsxd rdx,eax
   140002c56:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002c5a:	48 01 d0             	add    rax,rdx
   140002c5d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002c61:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002c68:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c6c:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002c70:	0f b7 d0             	movzx  edx,ax
   140002c73:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002c77:	48 01 d0             	add    rax,rdx
   140002c7a:	48 83 c0 18          	add    rax,0x18
   140002c7e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002c82:	eb 36                	jmp    140002cba <_FindPESection+0x7e>
   140002c84:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c88:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140002c8b:	89 c0                	mov    eax,eax
   140002c8d:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002c91:	72 1e                	jb     140002cb1 <_FindPESection+0x75>
   140002c93:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c97:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140002c9a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002c9e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140002ca1:	01 d0                	add    eax,edx
   140002ca3:	89 c0                	mov    eax,eax
   140002ca5:	48 39 45 18          	cmp    QWORD PTR [rbp+0x18],rax
   140002ca9:	73 06                	jae    140002cb1 <_FindPESection+0x75>
   140002cab:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002caf:	eb 1e                	jmp    140002ccf <_FindPESection+0x93>
   140002cb1:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002cb5:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002cba:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002cbe:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002cc2:	0f b7 c0             	movzx  eax,ax
   140002cc5:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002cc8:	72 ba                	jb     140002c84 <_FindPESection+0x48>
   140002cca:	b8 00 00 00 00       	mov    eax,0x0
   140002ccf:	48 83 c4 20          	add    rsp,0x20
   140002cd3:	5d                   	pop    rbp
   140002cd4:	c3                   	ret

0000000140002cd5 <_FindPESectionByName>:
   140002cd5:	55                   	push   rbp
   140002cd6:	48 89 e5             	mov    rbp,rsp
   140002cd9:	48 83 ec 40          	sub    rsp,0x40
   140002cdd:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002ce1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002ce5:	48 89 c1             	mov    rcx,rax
   140002ce8:	e8 2b 69 00 00       	call   140009618 <strlen>
   140002ced:	48 83 f8 08          	cmp    rax,0x8
   140002cf1:	76 0a                	jbe    140002cfd <_FindPESectionByName+0x28>
   140002cf3:	b8 00 00 00 00       	mov    eax,0x0
   140002cf8:	e9 98 00 00 00       	jmp    140002d95 <_FindPESectionByName+0xc0>
   140002cfd:	48 8b 05 8c 88 00 00 	mov    rax,QWORD PTR [rip+0x888c]        # 14000b590 <.refptr.__ImageBase>
   140002d04:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002d08:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d0c:	48 89 c1             	mov    rcx,rax
   140002d0f:	e8 ac fe ff ff       	call   140002bc0 <_ValidateImageBase>
   140002d14:	85 c0                	test   eax,eax
   140002d16:	75 07                	jne    140002d1f <_FindPESectionByName+0x4a>
   140002d18:	b8 00 00 00 00       	mov    eax,0x0
   140002d1d:	eb 76                	jmp    140002d95 <_FindPESectionByName+0xc0>
   140002d1f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d23:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002d26:	48 63 d0             	movsxd rdx,eax
   140002d29:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002d2d:	48 01 d0             	add    rax,rdx
   140002d30:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002d34:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002d3b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d3f:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002d43:	0f b7 d0             	movzx  edx,ax
   140002d46:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d4a:	48 01 d0             	add    rax,rdx
   140002d4d:	48 83 c0 18          	add    rax,0x18
   140002d51:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002d55:	eb 29                	jmp    140002d80 <_FindPESectionByName+0xab>
   140002d57:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d5b:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140002d5f:	41 b8 08 00 00 00    	mov    r8d,0x8
   140002d65:	48 89 c1             	mov    rcx,rax
   140002d68:	e8 b3 68 00 00       	call   140009620 <strncmp>
   140002d6d:	85 c0                	test   eax,eax
   140002d6f:	75 06                	jne    140002d77 <_FindPESectionByName+0xa2>
   140002d71:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002d75:	eb 1e                	jmp    140002d95 <_FindPESectionByName+0xc0>
   140002d77:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002d7b:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002d80:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002d84:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002d88:	0f b7 c0             	movzx  eax,ax
   140002d8b:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002d8e:	72 c7                	jb     140002d57 <_FindPESectionByName+0x82>
   140002d90:	b8 00 00 00 00       	mov    eax,0x0
   140002d95:	48 83 c4 40          	add    rsp,0x40
   140002d99:	5d                   	pop    rbp
   140002d9a:	c3                   	ret

0000000140002d9b <__mingw_GetSectionForAddress>:
   140002d9b:	55                   	push   rbp
   140002d9c:	48 89 e5             	mov    rbp,rsp
   140002d9f:	48 83 ec 30          	sub    rsp,0x30
   140002da3:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002da7:	48 8b 05 e2 87 00 00 	mov    rax,QWORD PTR [rip+0x87e2]        # 14000b590 <.refptr.__ImageBase>
   140002dae:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002db2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002db6:	48 89 c1             	mov    rcx,rax
   140002db9:	e8 02 fe ff ff       	call   140002bc0 <_ValidateImageBase>
   140002dbe:	85 c0                	test   eax,eax
   140002dc0:	75 07                	jne    140002dc9 <__mingw_GetSectionForAddress+0x2e>
   140002dc2:	b8 00 00 00 00       	mov    eax,0x0
   140002dc7:	eb 1c                	jmp    140002de5 <__mingw_GetSectionForAddress+0x4a>
   140002dc9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002dcd:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002dd1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002dd5:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002dd9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ddd:	48 89 c1             	mov    rcx,rax
   140002de0:	e8 57 fe ff ff       	call   140002c3c <_FindPESection>
   140002de5:	48 83 c4 30          	add    rsp,0x30
   140002de9:	5d                   	pop    rbp
   140002dea:	c3                   	ret

0000000140002deb <__mingw_GetSectionCount>:
   140002deb:	55                   	push   rbp
   140002dec:	48 89 e5             	mov    rbp,rsp
   140002def:	48 83 ec 30          	sub    rsp,0x30
   140002df3:	48 8b 05 96 87 00 00 	mov    rax,QWORD PTR [rip+0x8796]        # 14000b590 <.refptr.__ImageBase>
   140002dfa:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002dfe:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e02:	48 89 c1             	mov    rcx,rax
   140002e05:	e8 b6 fd ff ff       	call   140002bc0 <_ValidateImageBase>
   140002e0a:	85 c0                	test   eax,eax
   140002e0c:	75 07                	jne    140002e15 <__mingw_GetSectionCount+0x2a>
   140002e0e:	b8 00 00 00 00       	mov    eax,0x0
   140002e13:	eb 20                	jmp    140002e35 <__mingw_GetSectionCount+0x4a>
   140002e15:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e19:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e1c:	48 63 d0             	movsxd rdx,eax
   140002e1f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002e23:	48 01 d0             	add    rax,rdx
   140002e26:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002e2a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002e2e:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002e32:	0f b7 c0             	movzx  eax,ax
   140002e35:	48 83 c4 30          	add    rsp,0x30
   140002e39:	5d                   	pop    rbp
   140002e3a:	c3                   	ret

0000000140002e3b <_FindPESectionExec>:
   140002e3b:	55                   	push   rbp
   140002e3c:	48 89 e5             	mov    rbp,rsp
   140002e3f:	48 83 ec 40          	sub    rsp,0x40
   140002e43:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002e47:	48 8b 05 42 87 00 00 	mov    rax,QWORD PTR [rip+0x8742]        # 14000b590 <.refptr.__ImageBase>
   140002e4e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002e52:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e56:	48 89 c1             	mov    rcx,rax
   140002e59:	e8 62 fd ff ff       	call   140002bc0 <_ValidateImageBase>
   140002e5e:	85 c0                	test   eax,eax
   140002e60:	75 07                	jne    140002e69 <_FindPESectionExec+0x2e>
   140002e62:	b8 00 00 00 00       	mov    eax,0x0
   140002e67:	eb 78                	jmp    140002ee1 <_FindPESectionExec+0xa6>
   140002e69:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e6d:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002e70:	48 63 d0             	movsxd rdx,eax
   140002e73:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002e77:	48 01 d0             	add    rax,rdx
   140002e7a:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140002e7e:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140002e85:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e89:	0f b7 40 14          	movzx  eax,WORD PTR [rax+0x14]
   140002e8d:	0f b7 d0             	movzx  edx,ax
   140002e90:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002e94:	48 01 d0             	add    rax,rdx
   140002e97:	48 83 c0 18          	add    rax,0x18
   140002e9b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002e9f:	eb 2b                	jmp    140002ecc <_FindPESectionExec+0x91>
   140002ea1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ea5:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002ea8:	25 00 00 00 20       	and    eax,0x20000000
   140002ead:	85 c0                	test   eax,eax
   140002eaf:	74 12                	je     140002ec3 <_FindPESectionExec+0x88>
   140002eb1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140002eb6:	75 06                	jne    140002ebe <_FindPESectionExec+0x83>
   140002eb8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002ebc:	eb 23                	jmp    140002ee1 <_FindPESectionExec+0xa6>
   140002ebe:	48 83 6d 10 01       	sub    QWORD PTR [rbp+0x10],0x1
   140002ec3:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140002ec7:	48 83 45 f8 28       	add    QWORD PTR [rbp-0x8],0x28
   140002ecc:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140002ed0:	0f b7 40 06          	movzx  eax,WORD PTR [rax+0x6]
   140002ed4:	0f b7 c0             	movzx  eax,ax
   140002ed7:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140002eda:	72 c5                	jb     140002ea1 <_FindPESectionExec+0x66>
   140002edc:	b8 00 00 00 00       	mov    eax,0x0
   140002ee1:	48 83 c4 40          	add    rsp,0x40
   140002ee5:	5d                   	pop    rbp
   140002ee6:	c3                   	ret

0000000140002ee7 <_GetPEImageBase>:
   140002ee7:	55                   	push   rbp
   140002ee8:	48 89 e5             	mov    rbp,rsp
   140002eeb:	48 83 ec 30          	sub    rsp,0x30
   140002eef:	48 8b 05 9a 86 00 00 	mov    rax,QWORD PTR [rip+0x869a]        # 14000b590 <.refptr.__ImageBase>
   140002ef6:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002efa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002efe:	48 89 c1             	mov    rcx,rax
   140002f01:	e8 ba fc ff ff       	call   140002bc0 <_ValidateImageBase>
   140002f06:	85 c0                	test   eax,eax
   140002f08:	75 07                	jne    140002f11 <_GetPEImageBase+0x2a>
   140002f0a:	b8 00 00 00 00       	mov    eax,0x0
   140002f0f:	eb 04                	jmp    140002f15 <_GetPEImageBase+0x2e>
   140002f11:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f15:	48 83 c4 30          	add    rsp,0x30
   140002f19:	5d                   	pop    rbp
   140002f1a:	c3                   	ret

0000000140002f1b <_IsNonwritableInCurrentImage>:
   140002f1b:	55                   	push   rbp
   140002f1c:	48 89 e5             	mov    rbp,rsp
   140002f1f:	48 83 ec 40          	sub    rsp,0x40
   140002f23:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140002f27:	48 8b 05 62 86 00 00 	mov    rax,QWORD PTR [rip+0x8662]        # 14000b590 <.refptr.__ImageBase>
   140002f2e:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140002f32:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f36:	48 89 c1             	mov    rcx,rax
   140002f39:	e8 82 fc ff ff       	call   140002bc0 <_ValidateImageBase>
   140002f3e:	85 c0                	test   eax,eax
   140002f40:	75 07                	jne    140002f49 <_IsNonwritableInCurrentImage+0x2e>
   140002f42:	b8 00 00 00 00       	mov    eax,0x0
   140002f47:	eb 3d                	jmp    140002f86 <_IsNonwritableInCurrentImage+0x6b>
   140002f49:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140002f4d:	48 2b 45 f8          	sub    rax,QWORD PTR [rbp-0x8]
   140002f51:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002f55:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140002f59:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140002f5d:	48 89 c1             	mov    rcx,rax
   140002f60:	e8 d7 fc ff ff       	call   140002c3c <_FindPESection>
   140002f65:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002f69:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140002f6e:	75 07                	jne    140002f77 <_IsNonwritableInCurrentImage+0x5c>
   140002f70:	b8 00 00 00 00       	mov    eax,0x0
   140002f75:	eb 0f                	jmp    140002f86 <_IsNonwritableInCurrentImage+0x6b>
   140002f77:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002f7b:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140002f7e:	f7 d0                	not    eax
   140002f80:	c1 e8 1f             	shr    eax,0x1f
   140002f83:	0f b6 c0             	movzx  eax,al
   140002f86:	48 83 c4 40          	add    rsp,0x40
   140002f8a:	5d                   	pop    rbp
   140002f8b:	c3                   	ret

0000000140002f8c <__mingw_enum_import_library_names>:
   140002f8c:	55                   	push   rbp
   140002f8d:	48 89 e5             	mov    rbp,rsp
   140002f90:	48 83 ec 50          	sub    rsp,0x50
   140002f94:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140002f97:	48 8b 05 f2 85 00 00 	mov    rax,QWORD PTR [rip+0x85f2]        # 14000b590 <.refptr.__ImageBase>
   140002f9e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140002fa2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fa6:	48 89 c1             	mov    rcx,rax
   140002fa9:	e8 12 fc ff ff       	call   140002bc0 <_ValidateImageBase>
   140002fae:	85 c0                	test   eax,eax
   140002fb0:	75 0a                	jne    140002fbc <__mingw_enum_import_library_names+0x30>
   140002fb2:	b8 00 00 00 00       	mov    eax,0x0
   140002fb7:	e9 ab 00 00 00       	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140002fbc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fc0:	8b 40 3c             	mov    eax,DWORD PTR [rax+0x3c]
   140002fc3:	48 63 d0             	movsxd rdx,eax
   140002fc6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002fca:	48 01 d0             	add    rax,rdx
   140002fcd:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140002fd1:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140002fd5:	8b 80 90 00 00 00    	mov    eax,DWORD PTR [rax+0x90]
   140002fdb:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140002fde:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140002fe2:	75 07                	jne    140002feb <__mingw_enum_import_library_names+0x5f>
   140002fe4:	b8 00 00 00 00       	mov    eax,0x0
   140002fe9:	eb 7c                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140002feb:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140002fee:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140002ff2:	48 89 c1             	mov    rcx,rax
   140002ff5:	e8 42 fc ff ff       	call   140002c3c <_FindPESection>
   140002ffa:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140002ffe:	48 83 7d d8 00       	cmp    QWORD PTR [rbp-0x28],0x0
   140003003:	75 07                	jne    14000300c <__mingw_enum_import_library_names+0x80>
   140003005:	b8 00 00 00 00       	mov    eax,0x0
   14000300a:	eb 5b                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   14000300c:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   14000300f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003013:	48 01 d0             	add    rax,rdx
   140003016:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000301a:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   14000301f:	75 07                	jne    140003028 <__mingw_enum_import_library_names+0x9c>
   140003021:	b8 00 00 00 00       	mov    eax,0x0
   140003026:	eb 3f                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140003028:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000302c:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000302f:	85 c0                	test   eax,eax
   140003031:	75 0b                	jne    14000303e <__mingw_enum_import_library_names+0xb2>
   140003033:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003037:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000303a:	85 c0                	test   eax,eax
   14000303c:	74 23                	je     140003061 <__mingw_enum_import_library_names+0xd5>
   14000303e:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140003042:	7f 12                	jg     140003056 <__mingw_enum_import_library_names+0xca>
   140003044:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003048:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000304b:	89 c2                	mov    edx,eax
   14000304d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003051:	48 01 d0             	add    rax,rdx
   140003054:	eb 11                	jmp    140003067 <__mingw_enum_import_library_names+0xdb>
   140003056:	83 6d 10 01          	sub    DWORD PTR [rbp+0x10],0x1
   14000305a:	48 83 45 f8 14       	add    QWORD PTR [rbp-0x8],0x14
   14000305f:	eb c7                	jmp    140003028 <__mingw_enum_import_library_names+0x9c>
   140003061:	90                   	nop
   140003062:	b8 00 00 00 00       	mov    eax,0x0
   140003067:	48 83 c4 50          	add    rsp,0x50
   14000306b:	5d                   	pop    rbp
   14000306c:	c3                   	ret
   14000306d:	90                   	nop
   14000306e:	90                   	nop
   14000306f:	90                   	nop

0000000140003070 <___chkstk_ms>:
   140003070:	51                   	push   rcx
   140003071:	50                   	push   rax
   140003072:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003078:	48 8d 4c 24 18       	lea    rcx,[rsp+0x18]
   14000307d:	72 19                	jb     140003098 <___chkstk_ms+0x28>
   14000307f:	48 81 e9 00 10 00 00 	sub    rcx,0x1000
   140003086:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000308a:	48 2d 00 10 00 00    	sub    rax,0x1000
   140003090:	48 3d 00 10 00 00    	cmp    rax,0x1000
   140003096:	77 e7                	ja     14000307f <___chkstk_ms+0xf>
   140003098:	48 29 c1             	sub    rcx,rax
   14000309b:	48 83 09 00          	or     QWORD PTR [rcx],0x0
   14000309f:	58                   	pop    rax
   1400030a0:	59                   	pop    rcx
   1400030a1:	c3                   	ret
   1400030a2:	90                   	nop
   1400030a3:	90                   	nop
   1400030a4:	90                   	nop
   1400030a5:	90                   	nop
   1400030a6:	90                   	nop
   1400030a7:	90                   	nop
   1400030a8:	90                   	nop
   1400030a9:	90                   	nop
   1400030aa:	90                   	nop
   1400030ab:	90                   	nop
   1400030ac:	90                   	nop
   1400030ad:	90                   	nop
   1400030ae:	90                   	nop
   1400030af:	90                   	nop

00000001400030b0 <__mingw_printf>:
   1400030b0:	55                   	push   rbp
   1400030b1:	53                   	push   rbx
   1400030b2:	48 83 ec 48          	sub    rsp,0x48
   1400030b6:	48 8d 6c 24 40       	lea    rbp,[rsp+0x40]
   1400030bb:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   1400030bf:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   1400030c3:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   1400030c7:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   1400030cb:	48 8d 45 28          	lea    rax,[rbp+0x28]
   1400030cf:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400030d3:	b9 01 00 00 00       	mov    ecx,0x1
   1400030d8:	e8 c3 5e 00 00       	call   140008fa0 <__acrt_iob_func>
   1400030dd:	48 89 c1             	mov    rcx,rax
   1400030e0:	e8 3b 5d 00 00       	call   140008e20 <_lock_file>
   1400030e5:	48 8b 5d f8          	mov    rbx,QWORD PTR [rbp-0x8]
   1400030e9:	b9 01 00 00 00       	mov    ecx,0x1
   1400030ee:	e8 ad 5e 00 00       	call   140008fa0 <__acrt_iob_func>
   1400030f3:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400030f7:	48 89 5c 24 20       	mov    QWORD PTR [rsp+0x20],rbx
   1400030fc:	49 89 d1             	mov    r9,rdx
   1400030ff:	41 b8 00 00 00 00    	mov    r8d,0x0
   140003105:	48 89 c2             	mov    rdx,rax
   140003108:	b9 00 60 00 00       	mov    ecx,0x6000
   14000310d:	e8 b1 1f 00 00       	call   1400050c3 <__mingw_pformat>
   140003112:	89 c3                	mov    ebx,eax
   140003114:	b9 01 00 00 00       	mov    ecx,0x1
   140003119:	e8 82 5e 00 00       	call   140008fa0 <__acrt_iob_func>
   14000311e:	48 89 c1             	mov    rcx,rax
   140003121:	e8 84 5d 00 00       	call   140008eaa <_unlock_file>
   140003126:	89 d8                	mov    eax,ebx
   140003128:	48 83 c4 48          	add    rsp,0x48
   14000312c:	5b                   	pop    rbx
   14000312d:	5d                   	pop    rbp
   14000312e:	c3                   	ret
   14000312f:	90                   	nop

0000000140003130 <__pformat_putc>:
   140003130:	55                   	push   rbp
   140003131:	48 89 e5             	mov    rbp,rsp
   140003134:	48 83 ec 20          	sub    rsp,0x20
   140003138:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000313b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000313f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003143:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003146:	25 00 40 00 00       	and    eax,0x4000
   14000314b:	85 c0                	test   eax,eax
   14000314d:	75 12                	jne    140003161 <__pformat_putc+0x31>
   14000314f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003153:	8b 50 28             	mov    edx,DWORD PTR [rax+0x28]
   140003156:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000315a:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   14000315d:	39 c2                	cmp    edx,eax
   14000315f:	7e 3b                	jle    14000319c <__pformat_putc+0x6c>
   140003161:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003165:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003168:	25 00 20 00 00       	and    eax,0x2000
   14000316d:	85 c0                	test   eax,eax
   14000316f:	74 13                	je     140003184 <__pformat_putc+0x54>
   140003171:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003175:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   140003178:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   14000317b:	89 c1                	mov    ecx,eax
   14000317d:	e8 56 64 00 00       	call   1400095d8 <fputc>
   140003182:	eb 18                	jmp    14000319c <__pformat_putc+0x6c>
   140003184:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003188:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   14000318b:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000318f:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   140003192:	48 98                	cdqe
   140003194:	48 01 d0             	add    rax,rdx
   140003197:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   14000319a:	88 10                	mov    BYTE PTR [rax],dl
   14000319c:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400031a0:	8b 40 24             	mov    eax,DWORD PTR [rax+0x24]
   1400031a3:	8d 50 01             	lea    edx,[rax+0x1]
   1400031a6:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400031aa:	89 50 24             	mov    DWORD PTR [rax+0x24],edx
   1400031ad:	90                   	nop
   1400031ae:	48 83 c4 20          	add    rsp,0x20
   1400031b2:	5d                   	pop    rbp
   1400031b3:	c3                   	ret

00000001400031b4 <__pformat_putchars>:
   1400031b4:	55                   	push   rbp
   1400031b5:	48 89 e5             	mov    rbp,rsp
   1400031b8:	48 83 ec 20          	sub    rsp,0x20
   1400031bc:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400031c0:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   1400031c3:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400031c7:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031cb:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400031ce:	85 c0                	test   eax,eax
   1400031d0:	78 16                	js     1400031e8 <__pformat_putchars+0x34>
   1400031d2:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031d6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400031d9:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   1400031dc:	7e 0a                	jle    1400031e8 <__pformat_putchars+0x34>
   1400031de:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031e2:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400031e5:	89 45 18             	mov    DWORD PTR [rbp+0x18],eax
   1400031e8:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031ec:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400031ef:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   1400031f2:	7d 15                	jge    140003209 <__pformat_putchars+0x55>
   1400031f4:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400031f8:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400031fb:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   1400031fe:	89 c2                	mov    edx,eax
   140003200:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003204:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140003207:	eb 0b                	jmp    140003214 <__pformat_putchars+0x60>
   140003209:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000320d:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140003214:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003218:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000321b:	85 c0                	test   eax,eax
   14000321d:	7e 57                	jle    140003276 <__pformat_putchars+0xc2>
   14000321f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003223:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003226:	25 00 04 00 00       	and    eax,0x400
   14000322b:	85 c0                	test   eax,eax
   14000322d:	75 47                	jne    140003276 <__pformat_putchars+0xc2>
   14000322f:	eb 11                	jmp    140003242 <__pformat_putchars+0x8e>
   140003231:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003235:	48 89 c2             	mov    rdx,rax
   140003238:	b9 20 00 00 00       	mov    ecx,0x20
   14000323d:	e8 ee fe ff ff       	call   140003130 <__pformat_putc>
   140003242:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003246:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003249:	8d 48 ff             	lea    ecx,[rax-0x1]
   14000324c:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003250:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003253:	85 c0                	test   eax,eax
   140003255:	75 da                	jne    140003231 <__pformat_putchars+0x7d>
   140003257:	eb 1d                	jmp    140003276 <__pformat_putchars+0xc2>
   140003259:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000325d:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003261:	48 89 55 10          	mov    QWORD PTR [rbp+0x10],rdx
   140003265:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003268:	0f be c0             	movsx  eax,al
   14000326b:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   14000326f:	89 c1                	mov    ecx,eax
   140003271:	e8 ba fe ff ff       	call   140003130 <__pformat_putc>
   140003276:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140003279:	8d 50 ff             	lea    edx,[rax-0x1]
   14000327c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000327f:	85 c0                	test   eax,eax
   140003281:	75 d6                	jne    140003259 <__pformat_putchars+0xa5>
   140003283:	eb 11                	jmp    140003296 <__pformat_putchars+0xe2>
   140003285:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003289:	48 89 c2             	mov    rdx,rax
   14000328c:	b9 20 00 00 00       	mov    ecx,0x20
   140003291:	e8 9a fe ff ff       	call   140003130 <__pformat_putc>
   140003296:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000329a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000329d:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400032a0:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400032a4:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400032a7:	85 c0                	test   eax,eax
   1400032a9:	7f da                	jg     140003285 <__pformat_putchars+0xd1>
   1400032ab:	90                   	nop
   1400032ac:	90                   	nop
   1400032ad:	48 83 c4 20          	add    rsp,0x20
   1400032b1:	5d                   	pop    rbp
   1400032b2:	c3                   	ret

00000001400032b3 <__pformat_puts>:
   1400032b3:	55                   	push   rbp
   1400032b4:	48 89 e5             	mov    rbp,rsp
   1400032b7:	48 83 ec 20          	sub    rsp,0x20
   1400032bb:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400032bf:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400032c3:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400032c8:	75 0b                	jne    1400032d5 <__pformat_puts+0x22>
   1400032ca:	48 8d 05 5f 80 00 00 	lea    rax,[rip+0x805f]        # 14000b330 <.rdata>
   1400032d1:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400032d5:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400032d9:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400032dc:	85 c0                	test   eax,eax
   1400032de:	78 2f                	js     14000330f <__pformat_puts+0x5c>
   1400032e0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400032e4:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400032e7:	48 63 d0             	movsxd rdx,eax
   1400032ea:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400032ee:	48 89 c1             	mov    rcx,rax
   1400032f1:	e8 4a 5a 00 00       	call   140008d40 <strnlen>
   1400032f6:	89 c1                	mov    ecx,eax
   1400032f8:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400032fc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003300:	49 89 d0             	mov    r8,rdx
   140003303:	89 ca                	mov    edx,ecx
   140003305:	48 89 c1             	mov    rcx,rax
   140003308:	e8 a7 fe ff ff       	call   1400031b4 <__pformat_putchars>
   14000330d:	eb 23                	jmp    140003332 <__pformat_puts+0x7f>
   14000330f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003313:	48 89 c1             	mov    rcx,rax
   140003316:	e8 fd 62 00 00       	call   140009618 <strlen>
   14000331b:	89 c1                	mov    ecx,eax
   14000331d:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140003321:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140003325:	49 89 d0             	mov    r8,rdx
   140003328:	89 ca                	mov    edx,ecx
   14000332a:	48 89 c1             	mov    rcx,rax
   14000332d:	e8 82 fe ff ff       	call   1400031b4 <__pformat_putchars>
   140003332:	90                   	nop
   140003333:	48 83 c4 20          	add    rsp,0x20
   140003337:	5d                   	pop    rbp
   140003338:	c3                   	ret

0000000140003339 <__pformat_wputchars>:
   140003339:	55                   	push   rbp
   14000333a:	48 89 e5             	mov    rbp,rsp
   14000333d:	48 83 ec 50          	sub    rsp,0x50
   140003341:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003345:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140003348:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   14000334c:	48 c7 45 d8 00 00 00 	mov    QWORD PTR [rbp-0x28],0x0
   140003353:	00 
   140003354:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003358:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000335b:	85 c0                	test   eax,eax
   14000335d:	78 16                	js     140003375 <__pformat_wputchars+0x3c>
   14000335f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003363:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003366:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   140003369:	7e 0a                	jle    140003375 <__pformat_wputchars+0x3c>
   14000336b:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000336f:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003372:	89 45 18             	mov    DWORD PTR [rbp+0x18],eax
   140003375:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003379:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000337c:	39 45 18             	cmp    DWORD PTR [rbp+0x18],eax
   14000337f:	7d 15                	jge    140003396 <__pformat_wputchars+0x5d>
   140003381:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003385:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003388:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   14000338b:	89 c2                	mov    edx,eax
   14000338d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003391:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140003394:	eb 0b                	jmp    1400033a1 <__pformat_wputchars+0x68>
   140003396:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000339a:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   1400033a1:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033a5:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400033a8:	85 c0                	test   eax,eax
   1400033aa:	7e 6e                	jle    14000341a <__pformat_wputchars+0xe1>
   1400033ac:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033b0:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400033b3:	25 00 04 00 00       	and    eax,0x400
   1400033b8:	85 c0                	test   eax,eax
   1400033ba:	75 5e                	jne    14000341a <__pformat_wputchars+0xe1>
   1400033bc:	eb 11                	jmp    1400033cf <__pformat_wputchars+0x96>
   1400033be:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033c2:	48 89 c2             	mov    rdx,rax
   1400033c5:	b9 20 00 00 00       	mov    ecx,0x20
   1400033ca:	e8 61 fd ff ff       	call   140003130 <__pformat_putc>
   1400033cf:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400033d3:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400033d6:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400033d9:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400033dd:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400033e0:	85 c0                	test   eax,eax
   1400033e2:	75 da                	jne    1400033be <__pformat_wputchars+0x85>
   1400033e4:	eb 34                	jmp    14000341a <__pformat_wputchars+0xe1>
   1400033e6:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   1400033ea:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400033ee:	eb 1d                	jmp    14000340d <__pformat_wputchars+0xd4>
   1400033f0:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400033f4:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400033f8:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400033fc:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400033ff:	0f be c0             	movsx  eax,al
   140003402:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003406:	89 c1                	mov    ecx,eax
   140003408:	e8 23 fd ff ff       	call   140003130 <__pformat_putc>
   14000340d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003410:	8d 50 ff             	lea    edx,[rax-0x1]
   140003413:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003416:	85 c0                	test   eax,eax
   140003418:	7f d6                	jg     1400033f0 <__pformat_wputchars+0xb7>
   14000341a:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000341d:	8d 50 ff             	lea    edx,[rax-0x1]
   140003420:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140003423:	85 c0                	test   eax,eax
   140003425:	7e 41                	jle    140003468 <__pformat_wputchars+0x12f>
   140003427:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000342b:	48 8d 50 02          	lea    rdx,[rax+0x2]
   14000342f:	48 89 55 10          	mov    QWORD PTR [rbp+0x10],rdx
   140003433:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140003436:	0f b7 d0             	movzx  edx,ax
   140003439:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
   14000343d:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003441:	49 89 c8             	mov    r8,rcx
   140003444:	48 89 c1             	mov    rcx,rax
   140003447:	e8 84 5b 00 00       	call   140008fd0 <wcrtomb>
   14000344c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000344f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003453:	7f 91                	jg     1400033e6 <__pformat_wputchars+0xad>
   140003455:	eb 11                	jmp    140003468 <__pformat_wputchars+0x12f>
   140003457:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000345b:	48 89 c2             	mov    rdx,rax
   14000345e:	b9 20 00 00 00       	mov    ecx,0x20
   140003463:	e8 c8 fc ff ff       	call   140003130 <__pformat_putc>
   140003468:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000346c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000346f:	8d 48 ff             	lea    ecx,[rax-0x1]
   140003472:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003476:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003479:	85 c0                	test   eax,eax
   14000347b:	7f da                	jg     140003457 <__pformat_wputchars+0x11e>
   14000347d:	90                   	nop
   14000347e:	90                   	nop
   14000347f:	48 83 c4 50          	add    rsp,0x50
   140003483:	5d                   	pop    rbp
   140003484:	c3                   	ret

0000000140003485 <__pformat_wcputs>:
   140003485:	55                   	push   rbp
   140003486:	48 89 e5             	mov    rbp,rsp
   140003489:	48 83 ec 20          	sub    rsp,0x20
   14000348d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140003491:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140003495:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000349a:	75 0b                	jne    1400034a7 <__pformat_wcputs+0x22>
   14000349c:	48 8d 05 95 7e 00 00 	lea    rax,[rip+0x7e95]        # 14000b338 <.rdata+0x8>
   1400034a3:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400034a7:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400034ab:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400034ae:	85 c0                	test   eax,eax
   1400034b0:	78 2f                	js     1400034e1 <__pformat_wcputs+0x5c>
   1400034b2:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400034b6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400034b9:	48 63 d0             	movsxd rdx,eax
   1400034bc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034c0:	48 89 c1             	mov    rcx,rax
   1400034c3:	e8 28 58 00 00       	call   140008cf0 <wcsnlen>
   1400034c8:	89 c1                	mov    ecx,eax
   1400034ca:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400034ce:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034d2:	49 89 d0             	mov    r8,rdx
   1400034d5:	89 ca                	mov    edx,ecx
   1400034d7:	48 89 c1             	mov    rcx,rax
   1400034da:	e8 5a fe ff ff       	call   140003339 <__pformat_wputchars>
   1400034df:	eb 23                	jmp    140003504 <__pformat_wcputs+0x7f>
   1400034e1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034e5:	48 89 c1             	mov    rcx,rax
   1400034e8:	e8 43 61 00 00       	call   140009630 <wcslen>
   1400034ed:	89 c1                	mov    ecx,eax
   1400034ef:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400034f3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400034f7:	49 89 d0             	mov    r8,rdx
   1400034fa:	89 ca                	mov    edx,ecx
   1400034fc:	48 89 c1             	mov    rcx,rax
   1400034ff:	e8 35 fe ff ff       	call   140003339 <__pformat_wputchars>
   140003504:	90                   	nop
   140003505:	48 83 c4 20          	add    rsp,0x20
   140003509:	5d                   	pop    rbp
   14000350a:	c3                   	ret

000000014000350b <__pformat_int_bufsiz>:
   14000350b:	55                   	push   rbp
   14000350c:	48 89 e5             	mov    rbp,rsp
   14000350f:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003512:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140003515:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140003519:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000351c:	83 e8 01             	sub    eax,0x1
   14000351f:	48 98                	cdqe
   140003521:	48 83 c0 40          	add    rax,0x40
   140003525:	8b 55 18             	mov    edx,DWORD PTR [rbp+0x18]
   140003528:	48 63 ca             	movsxd rcx,edx
   14000352b:	ba 00 00 00 00       	mov    edx,0x0
   140003530:	48 f7 f1             	div    rcx
   140003533:	89 c2                	mov    edx,eax
   140003535:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140003538:	01 d0                	add    eax,edx
   14000353a:	89 45 18             	mov    DWORD PTR [rbp+0x18],eax
   14000353d:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003541:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003544:	ba 00 00 00 00       	mov    edx,0x0
   140003549:	85 c0                	test   eax,eax
   14000354b:	0f 48 c2             	cmovs  eax,edx
   14000354e:	01 45 18             	add    DWORD PTR [rbp+0x18],eax
   140003551:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003555:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003558:	25 00 10 00 00       	and    eax,0x1000
   14000355d:	85 c0                	test   eax,eax
   14000355f:	74 29                	je     14000358a <__pformat_int_bufsiz+0x7f>
   140003561:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003565:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   140003569:	66 85 c0             	test   ax,ax
   14000356c:	74 1c                	je     14000358a <__pformat_int_bufsiz+0x7f>
   14000356e:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140003571:	48 63 d0             	movsxd rdx,eax
   140003574:	48 69 d2 56 55 55 55 	imul   rdx,rdx,0x55555556
   14000357b:	48 89 d1             	mov    rcx,rdx
   14000357e:	48 c1 e9 20          	shr    rcx,0x20
   140003582:	99                   	cdq
   140003583:	89 c8                	mov    eax,ecx
   140003585:	29 d0                	sub    eax,edx
   140003587:	01 45 18             	add    DWORD PTR [rbp+0x18],eax
   14000358a:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000358e:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140003591:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140003594:	39 c2                	cmp    edx,eax
   140003596:	0f 4d c2             	cmovge eax,edx
   140003599:	5d                   	pop    rbp
   14000359a:	c3                   	ret

000000014000359b <__pformat_int>:
   14000359b:	55                   	push   rbp
   14000359c:	53                   	push   rbx
   14000359d:	48 83 ec 58          	sub    rsp,0x58
   1400035a1:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   1400035a6:	48 89 cb             	mov    rbx,rcx
   1400035a9:	48 8b 0b             	mov    rcx,QWORD PTR [rbx]
   1400035ac:	48 8b 5b 08          	mov    rbx,QWORD PTR [rbx+0x8]
   1400035b0:	48 89 4d d0          	mov    QWORD PTR [rbp-0x30],rcx
   1400035b4:	48 89 5d d8          	mov    QWORD PTR [rbp-0x28],rbx
   1400035b8:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   1400035bc:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400035c0:	49 89 c0             	mov    r8,rax
   1400035c3:	ba 03 00 00 00       	mov    edx,0x3
   1400035c8:	b9 01 00 00 00       	mov    ecx,0x1
   1400035cd:	e8 39 ff ff ff       	call   14000350b <__pformat_int_bufsiz>
   1400035d2:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   1400035d5:	48 c7 45 e8 00 00 00 	mov    QWORD PTR [rbp-0x18],0x0
   1400035dc:	00 
   1400035dd:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   1400035e0:	48 98                	cdqe
   1400035e2:	48 83 c0 0f          	add    rax,0xf
   1400035e6:	48 c1 e8 04          	shr    rax,0x4
   1400035ea:	48 c1 e0 04          	shl    rax,0x4
   1400035ee:	e8 7d fa ff ff       	call   140003070 <___chkstk_ms>
   1400035f3:	48 29 c4             	sub    rsp,rax
   1400035f6:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400035fb:	48 83 c0 0f          	add    rax,0xf
   1400035ff:	48 c1 e8 04          	shr    rax,0x4
   140003603:	48 c1 e0 04          	shl    rax,0x4
   140003607:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000360b:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000360f:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140003613:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003617:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000361a:	25 80 00 00 00       	and    eax,0x80
   14000361f:	85 c0                	test   eax,eax
   140003621:	0f 84 ea 00 00 00    	je     140003711 <__pformat_int+0x176>
   140003627:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   14000362b:	48 85 c0             	test   rax,rax
   14000362e:	79 10                	jns    140003640 <__pformat_int+0xa5>
   140003630:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140003634:	48 f7 d8             	neg    rax
   140003637:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   14000363b:	e9 d1 00 00 00       	jmp    140003711 <__pformat_int+0x176>
   140003640:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003644:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003647:	24 7f                	and    al,0x7f
   140003649:	89 c2                	mov    edx,eax
   14000364b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000364f:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140003652:	e9 ba 00 00 00       	jmp    140003711 <__pformat_int+0x176>
   140003657:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000365b:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   14000365f:	74 54                	je     1400036b5 <__pformat_int+0x11a>
   140003661:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003665:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003668:	25 00 10 00 00       	and    eax,0x1000
   14000366d:	85 c0                	test   eax,eax
   14000366f:	74 44                	je     1400036b5 <__pformat_int+0x11a>
   140003671:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003675:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   140003679:	66 85 c0             	test   ax,ax
   14000367c:	74 37                	je     1400036b5 <__pformat_int+0x11a>
   14000367e:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003682:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
   140003686:	48 89 c2             	mov    rdx,rax
   140003689:	48 89 d0             	mov    rax,rdx
   14000368c:	48 c1 f8 3f          	sar    rax,0x3f
   140003690:	48 c1 e8 3e          	shr    rax,0x3e
   140003694:	48 01 c2             	add    rdx,rax
   140003697:	83 e2 03             	and    edx,0x3
   14000369a:	48 29 c2             	sub    rdx,rax
   14000369d:	48 89 d0             	mov    rax,rdx
   1400036a0:	48 83 f8 03          	cmp    rax,0x3
   1400036a4:	75 0f                	jne    1400036b5 <__pformat_int+0x11a>
   1400036a6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400036aa:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400036ae:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400036b2:	c6 00 2c             	mov    BYTE PTR [rax],0x2c
   1400036b5:	48 8b 4d d0          	mov    rcx,QWORD PTR [rbp-0x30]
   1400036b9:	48 ba cd cc cc cc cc 	movabs rdx,0xcccccccccccccccd
   1400036c0:	cc cc cc 
   1400036c3:	48 89 c8             	mov    rax,rcx
   1400036c6:	48 f7 e2             	mul    rdx
   1400036c9:	48 c1 ea 03          	shr    rdx,0x3
   1400036cd:	48 89 d0             	mov    rax,rdx
   1400036d0:	48 c1 e0 02          	shl    rax,0x2
   1400036d4:	48 01 d0             	add    rax,rdx
   1400036d7:	48 01 c0             	add    rax,rax
   1400036da:	48 29 c1             	sub    rcx,rax
   1400036dd:	48 89 ca             	mov    rdx,rcx
   1400036e0:	89 d0                	mov    eax,edx
   1400036e2:	8d 48 30             	lea    ecx,[rax+0x30]
   1400036e5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400036e9:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400036ed:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400036f1:	89 ca                	mov    edx,ecx
   1400036f3:	88 10                	mov    BYTE PTR [rax],dl
   1400036f5:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400036f9:	48 ba cd cc cc cc cc 	movabs rdx,0xcccccccccccccccd
   140003700:	cc cc cc 
   140003703:	48 f7 e2             	mul    rdx
   140003706:	48 89 d0             	mov    rax,rdx
   140003709:	48 c1 e8 03          	shr    rax,0x3
   14000370d:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140003711:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140003715:	48 85 c0             	test   rax,rax
   140003718:	0f 85 39 ff ff ff    	jne    140003657 <__pformat_int+0xbc>
   14000371e:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003722:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003725:	85 c0                	test   eax,eax
   140003727:	7e 3e                	jle    140003767 <__pformat_int+0x1cc>
   140003729:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000372d:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003730:	89 c1                	mov    ecx,eax
   140003732:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003736:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
   14000373a:	89 c2                	mov    edx,eax
   14000373c:	89 c8                	mov    eax,ecx
   14000373e:	29 d0                	sub    eax,edx
   140003740:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140003743:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140003747:	7e 1e                	jle    140003767 <__pformat_int+0x1cc>
   140003749:	eb 0f                	jmp    14000375a <__pformat_int+0x1bf>
   14000374b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000374f:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003753:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003757:	c6 00 30             	mov    BYTE PTR [rax],0x30
   14000375a:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000375d:	8d 50 ff             	lea    edx,[rax-0x1]
   140003760:	89 55 f4             	mov    DWORD PTR [rbp-0xc],edx
   140003763:	85 c0                	test   eax,eax
   140003765:	7f e4                	jg     14000374b <__pformat_int+0x1b0>
   140003767:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000376b:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   14000376f:	75 1a                	jne    14000378b <__pformat_int+0x1f0>
   140003771:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003775:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003778:	85 c0                	test   eax,eax
   14000377a:	74 0f                	je     14000378b <__pformat_int+0x1f0>
   14000377c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140003780:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003784:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003788:	c6 00 30             	mov    BYTE PTR [rax],0x30
   14000378b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000378f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003792:	85 c0                	test   eax,eax
   140003794:	0f 8e ce 00 00 00    	jle    140003868 <__pformat_int+0x2cd>
   14000379a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000379e:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400037a1:	89 c1                	mov    ecx,eax
   1400037a3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400037a7:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
   1400037ab:	89 c2                	mov    edx,eax
   1400037ad:	89 c8                	mov    eax,ecx
   1400037af:	29 d0                	sub    eax,edx
   1400037b1:	89 c2                	mov    edx,eax
   1400037b3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037b7:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400037ba:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037be:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400037c1:	85 c0                	test   eax,eax
   1400037c3:	0f 8e 9f 00 00 00    	jle    140003868 <__pformat_int+0x2cd>
   1400037c9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037cd:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400037d0:	25 c0 01 00 00       	and    eax,0x1c0
   1400037d5:	85 c0                	test   eax,eax
   1400037d7:	74 11                	je     1400037ea <__pformat_int+0x24f>
   1400037d9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037dd:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400037e0:	8d 50 ff             	lea    edx,[rax-0x1]
   1400037e3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037e7:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400037ea:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037ee:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400037f1:	85 c0                	test   eax,eax
   1400037f3:	79 3b                	jns    140003830 <__pformat_int+0x295>
   1400037f5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400037f9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400037fc:	25 00 06 00 00       	and    eax,0x600
   140003801:	3d 00 02 00 00       	cmp    eax,0x200
   140003806:	75 28                	jne    140003830 <__pformat_int+0x295>
   140003808:	eb 0f                	jmp    140003819 <__pformat_int+0x27e>
   14000380a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000380e:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003812:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003816:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003819:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000381d:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003820:	8d 48 ff             	lea    ecx,[rax-0x1]
   140003823:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140003827:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   14000382a:	85 c0                	test   eax,eax
   14000382c:	7f dc                	jg     14000380a <__pformat_int+0x26f>
   14000382e:	eb 38                	jmp    140003868 <__pformat_int+0x2cd>
   140003830:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003834:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003837:	25 00 04 00 00       	and    eax,0x400
   14000383c:	85 c0                	test   eax,eax
   14000383e:	75 28                	jne    140003868 <__pformat_int+0x2cd>
   140003840:	eb 11                	jmp    140003853 <__pformat_int+0x2b8>
   140003842:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003846:	48 89 c2             	mov    rdx,rax
   140003849:	b9 20 00 00 00       	mov    ecx,0x20
   14000384e:	e8 dd f8 ff ff       	call   140003130 <__pformat_putc>
   140003853:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003857:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000385a:	8d 48 ff             	lea    ecx,[rax-0x1]
   14000385d:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140003861:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003864:	85 c0                	test   eax,eax
   140003866:	7f da                	jg     140003842 <__pformat_int+0x2a7>
   140003868:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000386c:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000386f:	25 80 00 00 00       	and    eax,0x80
   140003874:	85 c0                	test   eax,eax
   140003876:	74 11                	je     140003889 <__pformat_int+0x2ee>
   140003878:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000387c:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003880:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140003884:	c6 00 2d             	mov    BYTE PTR [rax],0x2d
   140003887:	eb 5a                	jmp    1400038e3 <__pformat_int+0x348>
   140003889:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000388d:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003890:	25 00 01 00 00       	and    eax,0x100
   140003895:	85 c0                	test   eax,eax
   140003897:	74 11                	je     1400038aa <__pformat_int+0x30f>
   140003899:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000389d:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400038a1:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400038a5:	c6 00 2b             	mov    BYTE PTR [rax],0x2b
   1400038a8:	eb 39                	jmp    1400038e3 <__pformat_int+0x348>
   1400038aa:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400038ae:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400038b1:	83 e0 40             	and    eax,0x40
   1400038b4:	85 c0                	test   eax,eax
   1400038b6:	74 2b                	je     1400038e3 <__pformat_int+0x348>
   1400038b8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400038bc:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400038c0:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400038c4:	c6 00 20             	mov    BYTE PTR [rax],0x20
   1400038c7:	eb 1a                	jmp    1400038e3 <__pformat_int+0x348>
   1400038c9:	48 83 6d f8 01       	sub    QWORD PTR [rbp-0x8],0x1
   1400038ce:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400038d2:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400038d5:	0f be c0             	movsx  eax,al
   1400038d8:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400038dc:	89 c1                	mov    ecx,eax
   1400038de:	e8 4d f8 ff ff       	call   140003130 <__pformat_putc>
   1400038e3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400038e7:	48 39 45 e8          	cmp    QWORD PTR [rbp-0x18],rax
   1400038eb:	72 dc                	jb     1400038c9 <__pformat_int+0x32e>
   1400038ed:	eb 11                	jmp    140003900 <__pformat_int+0x365>
   1400038ef:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400038f3:	48 89 c2             	mov    rdx,rax
   1400038f6:	b9 20 00 00 00       	mov    ecx,0x20
   1400038fb:	e8 30 f8 ff ff       	call   140003130 <__pformat_putc>
   140003900:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140003904:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003907:	8d 48 ff             	lea    ecx,[rax-0x1]
   14000390a:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   14000390e:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140003911:	85 c0                	test   eax,eax
   140003913:	7f da                	jg     1400038ef <__pformat_int+0x354>
   140003915:	90                   	nop
   140003916:	90                   	nop
   140003917:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   14000391b:	5b                   	pop    rbx
   14000391c:	5d                   	pop    rbp
   14000391d:	c3                   	ret

000000014000391e <__pformat_xint>:
   14000391e:	55                   	push   rbp
   14000391f:	53                   	push   rbx
   140003920:	48 83 ec 68          	sub    rsp,0x68
   140003924:	48 8d 6c 24 60       	lea    rbp,[rsp+0x60]
   140003929:	89 4d 20             	mov    DWORD PTR [rbp+0x20],ecx
   14000392c:	48 89 d3             	mov    rbx,rdx
   14000392f:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140003932:	48 8b 53 08          	mov    rdx,QWORD PTR [rbx+0x8]
   140003936:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   14000393a:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
   14000393e:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140003942:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003946:	74 1e                	je     140003966 <__pformat_xint+0x48>
   140003948:	83 7d 20 62          	cmp    DWORD PTR [rbp+0x20],0x62
   14000394c:	74 06                	je     140003954 <__pformat_xint+0x36>
   14000394e:	83 7d 20 42          	cmp    DWORD PTR [rbp+0x20],0x42
   140003952:	75 09                	jne    14000395d <__pformat_xint+0x3f>
   140003954:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   14000395b:	eb 10                	jmp    14000396d <__pformat_xint+0x4f>
   14000395d:	c7 45 f8 04 00 00 00 	mov    DWORD PTR [rbp-0x8],0x4
   140003964:	eb 07                	jmp    14000396d <__pformat_xint+0x4f>
   140003966:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   14000396d:	48 8b 55 30          	mov    rdx,QWORD PTR [rbp+0x30]
   140003971:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003974:	49 89 d0             	mov    r8,rdx
   140003977:	89 c2                	mov    edx,eax
   140003979:	b9 02 00 00 00       	mov    ecx,0x2
   14000397e:	e8 88 fb ff ff       	call   14000350b <__pformat_int_bufsiz>
   140003983:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140003986:	48 c7 45 e0 00 00 00 	mov    QWORD PTR [rbp-0x20],0x0
   14000398d:	00 
   14000398e:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140003991:	48 98                	cdqe
   140003993:	48 83 c0 0f          	add    rax,0xf
   140003997:	48 c1 e8 04          	shr    rax,0x4
   14000399b:	48 c1 e0 04          	shl    rax,0x4
   14000399f:	e8 cc f6 ff ff       	call   140003070 <___chkstk_ms>
   1400039a4:	48 29 c4             	sub    rsp,rax
   1400039a7:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   1400039ac:	48 83 c0 0f          	add    rax,0xf
   1400039b0:	48 c1 e8 04          	shr    rax,0x4
   1400039b4:	48 c1 e0 04          	shl    rax,0x4
   1400039b8:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400039bc:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400039c0:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400039c4:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   1400039c8:	74 1e                	je     1400039e8 <__pformat_xint+0xca>
   1400039ca:	83 7d 20 62          	cmp    DWORD PTR [rbp+0x20],0x62
   1400039ce:	74 06                	je     1400039d6 <__pformat_xint+0xb8>
   1400039d0:	83 7d 20 42          	cmp    DWORD PTR [rbp+0x20],0x42
   1400039d4:	75 09                	jne    1400039df <__pformat_xint+0xc1>
   1400039d6:	c7 45 ec 01 00 00 00 	mov    DWORD PTR [rbp-0x14],0x1
   1400039dd:	eb 10                	jmp    1400039ef <__pformat_xint+0xd1>
   1400039df:	c7 45 ec 0f 00 00 00 	mov    DWORD PTR [rbp-0x14],0xf
   1400039e6:	eb 67                	jmp    140003a4f <__pformat_xint+0x131>
   1400039e8:	c7 45 ec 07 00 00 00 	mov    DWORD PTR [rbp-0x14],0x7
   1400039ef:	eb 5e                	jmp    140003a4f <__pformat_xint+0x131>
   1400039f1:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   1400039f5:	89 c2                	mov    edx,eax
   1400039f7:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   1400039fa:	21 d0                	and    eax,edx
   1400039fc:	8d 48 30             	lea    ecx,[rax+0x30]
   1400039ff:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003a03:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003a07:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003a0b:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140003a0f:	89 ca                	mov    edx,ecx
   140003a11:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a15:	88 10                	mov    BYTE PTR [rax],dl
   140003a17:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a1b:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003a1e:	3c 39                	cmp    al,0x39
   140003a20:	7e 1a                	jle    140003a3c <__pformat_xint+0x11e>
   140003a22:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a26:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003a29:	83 c0 07             	add    eax,0x7
   140003a2c:	89 c2                	mov    edx,eax
   140003a2e:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140003a31:	83 e0 20             	and    eax,0x20
   140003a34:	09 c2                	or     edx,eax
   140003a36:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003a3a:	88 10                	mov    BYTE PTR [rax],dl
   140003a3c:	48 8b 55 c0          	mov    rdx,QWORD PTR [rbp-0x40]
   140003a40:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003a43:	89 c1                	mov    ecx,eax
   140003a45:	48 d3 ea             	shr    rdx,cl
   140003a48:	48 89 d0             	mov    rax,rdx
   140003a4b:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140003a4f:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140003a53:	48 85 c0             	test   rax,rax
   140003a56:	75 99                	jne    1400039f1 <__pformat_xint+0xd3>
   140003a58:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003a5c:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   140003a60:	75 13                	jne    140003a75 <__pformat_xint+0x157>
   140003a62:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003a66:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003a69:	80 e4 f7             	and    ah,0xf7
   140003a6c:	89 c2                	mov    edx,eax
   140003a6e:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003a72:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140003a75:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003a79:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003a7c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003a7f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003a83:	7e 3a                	jle    140003abf <__pformat_xint+0x1a1>
   140003a85:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140003a88:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003a8c:	48 2b 45 e0          	sub    rax,QWORD PTR [rbp-0x20]
   140003a90:	89 c1                	mov    ecx,eax
   140003a92:	89 d0                	mov    eax,edx
   140003a94:	29 c8                	sub    eax,ecx
   140003a96:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003a99:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003a9d:	7e 20                	jle    140003abf <__pformat_xint+0x1a1>
   140003a9f:	eb 0f                	jmp    140003ab0 <__pformat_xint+0x192>
   140003aa1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003aa5:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003aa9:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003aad:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003ab0:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003ab3:	8d 50 ff             	lea    edx,[rax-0x1]
   140003ab6:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003ab9:	85 c0                	test   eax,eax
   140003abb:	7f e4                	jg     140003aa1 <__pformat_xint+0x183>
   140003abd:	eb 25                	jmp    140003ae4 <__pformat_xint+0x1c6>
   140003abf:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003ac3:	75 1f                	jne    140003ae4 <__pformat_xint+0x1c6>
   140003ac5:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003ac9:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003acc:	25 00 08 00 00       	and    eax,0x800
   140003ad1:	85 c0                	test   eax,eax
   140003ad3:	74 0f                	je     140003ae4 <__pformat_xint+0x1c6>
   140003ad5:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003ad9:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003add:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003ae1:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003ae4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003ae8:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   140003aec:	75 1a                	jne    140003b08 <__pformat_xint+0x1ea>
   140003aee:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003af2:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003af5:	85 c0                	test   eax,eax
   140003af7:	74 0f                	je     140003b08 <__pformat_xint+0x1ea>
   140003af9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003afd:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003b01:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003b05:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003b08:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b0c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003b0f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140003b13:	48 2b 55 e0          	sub    rdx,QWORD PTR [rbp-0x20]
   140003b17:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003b1a:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140003b1d:	7d 15                	jge    140003b34 <__pformat_xint+0x216>
   140003b1f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b23:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003b26:	2b 45 fc             	sub    eax,DWORD PTR [rbp-0x4]
   140003b29:	89 c2                	mov    edx,eax
   140003b2b:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b2f:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140003b32:	eb 0b                	jmp    140003b3f <__pformat_xint+0x221>
   140003b34:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b38:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140003b3f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b43:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140003b46:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003b49:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003b4d:	7e 1a                	jle    140003b69 <__pformat_xint+0x24b>
   140003b4f:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003b53:	74 14                	je     140003b69 <__pformat_xint+0x24b>
   140003b55:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b59:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003b5c:	25 00 08 00 00       	and    eax,0x800
   140003b61:	85 c0                	test   eax,eax
   140003b63:	74 04                	je     140003b69 <__pformat_xint+0x24b>
   140003b65:	83 6d fc 02          	sub    DWORD PTR [rbp-0x4],0x2
   140003b69:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003b6d:	7e 3c                	jle    140003bab <__pformat_xint+0x28d>
   140003b6f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b73:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140003b76:	85 c0                	test   eax,eax
   140003b78:	79 31                	jns    140003bab <__pformat_xint+0x28d>
   140003b7a:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003b7e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003b81:	25 00 06 00 00       	and    eax,0x600
   140003b86:	3d 00 02 00 00       	cmp    eax,0x200
   140003b8b:	75 1e                	jne    140003bab <__pformat_xint+0x28d>
   140003b8d:	eb 0f                	jmp    140003b9e <__pformat_xint+0x280>
   140003b8f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003b93:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003b97:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003b9b:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003b9e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003ba1:	8d 50 ff             	lea    edx,[rax-0x1]
   140003ba4:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003ba7:	85 c0                	test   eax,eax
   140003ba9:	7f e4                	jg     140003b8f <__pformat_xint+0x271>
   140003bab:	83 7d 20 6f          	cmp    DWORD PTR [rbp+0x20],0x6f
   140003baf:	74 30                	je     140003be1 <__pformat_xint+0x2c3>
   140003bb1:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003bb5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003bb8:	25 00 08 00 00       	and    eax,0x800
   140003bbd:	85 c0                	test   eax,eax
   140003bbf:	74 20                	je     140003be1 <__pformat_xint+0x2c3>
   140003bc1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003bc5:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003bc9:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003bcd:	8b 55 20             	mov    edx,DWORD PTR [rbp+0x20]
   140003bd0:	88 10                	mov    BYTE PTR [rax],dl
   140003bd2:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003bd6:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003bda:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003bde:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140003be1:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003be5:	7e 4c                	jle    140003c33 <__pformat_xint+0x315>
   140003be7:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003beb:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140003bee:	25 00 04 00 00       	and    eax,0x400
   140003bf3:	85 c0                	test   eax,eax
   140003bf5:	75 3c                	jne    140003c33 <__pformat_xint+0x315>
   140003bf7:	eb 11                	jmp    140003c0a <__pformat_xint+0x2ec>
   140003bf9:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003bfd:	48 89 c2             	mov    rdx,rax
   140003c00:	b9 20 00 00 00       	mov    ecx,0x20
   140003c05:	e8 26 f5 ff ff       	call   140003130 <__pformat_putc>
   140003c0a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003c0d:	8d 50 ff             	lea    edx,[rax-0x1]
   140003c10:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003c13:	85 c0                	test   eax,eax
   140003c15:	7f e2                	jg     140003bf9 <__pformat_xint+0x2db>
   140003c17:	eb 1a                	jmp    140003c33 <__pformat_xint+0x315>
   140003c19:	48 83 6d f0 01       	sub    QWORD PTR [rbp-0x10],0x1
   140003c1e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003c22:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003c25:	0f be c0             	movsx  eax,al
   140003c28:	48 8b 55 30          	mov    rdx,QWORD PTR [rbp+0x30]
   140003c2c:	89 c1                	mov    ecx,eax
   140003c2e:	e8 fd f4 ff ff       	call   140003130 <__pformat_putc>
   140003c33:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003c37:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   140003c3b:	72 dc                	jb     140003c19 <__pformat_xint+0x2fb>
   140003c3d:	eb 11                	jmp    140003c50 <__pformat_xint+0x332>
   140003c3f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140003c43:	48 89 c2             	mov    rdx,rax
   140003c46:	b9 20 00 00 00       	mov    ecx,0x20
   140003c4b:	e8 e0 f4 ff ff       	call   140003130 <__pformat_putc>
   140003c50:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003c53:	8d 50 ff             	lea    edx,[rax-0x1]
   140003c56:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003c59:	85 c0                	test   eax,eax
   140003c5b:	7f e2                	jg     140003c3f <__pformat_xint+0x321>
   140003c5d:	90                   	nop
   140003c5e:	90                   	nop
   140003c5f:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   140003c63:	5b                   	pop    rbx
   140003c64:	5d                   	pop    rbp
   140003c65:	c3                   	ret

0000000140003c66 <init_fpreg_ldouble>:
   140003c66:	55                   	push   rbp
   140003c67:	53                   	push   rbx
   140003c68:	48 83 ec 28          	sub    rsp,0x28
   140003c6c:	48 8d 6c 24 20       	lea    rbp,[rsp+0x20]
   140003c71:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140003c75:	48 89 d3             	mov    rbx,rdx
   140003c78:	db 2b                	fld    TBYTE PTR [rbx]
   140003c7a:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140003c7d:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140003c80:	db 7d f0             	fstp   TBYTE PTR [rbp-0x10]
   140003c83:	48 8b 4d 20          	mov    rcx,QWORD PTR [rbp+0x20]
   140003c87:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003c8b:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140003c8f:	48 89 01             	mov    QWORD PTR [rcx],rax
   140003c92:	48 89 51 08          	mov    QWORD PTR [rcx+0x8],rdx
   140003c96:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003c9a:	48 83 c4 28          	add    rsp,0x28
   140003c9e:	5b                   	pop    rbx
   140003c9f:	5d                   	pop    rbp
   140003ca0:	c3                   	ret

0000000140003ca1 <__pformat_cvt>:
   140003ca1:	55                   	push   rbp
   140003ca2:	53                   	push   rbx
   140003ca3:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140003caa:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   140003cb1:	00 
   140003cb2:	89 4d 20             	mov    DWORD PTR [rbp+0x20],ecx
   140003cb5:	48 89 d3             	mov    rbx,rdx
   140003cb8:	db 2b                	fld    TBYTE PTR [rbx]
   140003cba:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140003cbd:	44 89 45 30          	mov    DWORD PTR [rbp+0x30],r8d
   140003cc1:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140003cc5:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140003ccc:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003cd0:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140003cd3:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140003cd6:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140003cda:	48 89 c1             	mov    rcx,rax
   140003cdd:	e8 84 ff ff ff       	call   140003c66 <init_fpreg_ldouble>
   140003ce2:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140003ce5:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140003ce8:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140003cec:	48 89 c1             	mov    rcx,rax
   140003cef:	e8 9c 4e 00 00       	call   140008b90 <__fpclassifyl>
   140003cf4:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140003cf7:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003cfa:	25 00 01 00 00       	and    eax,0x100
   140003cff:	85 c0                	test   eax,eax
   140003d01:	74 1d                	je     140003d20 <__pformat_cvt+0x7f>
   140003d03:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d06:	25 00 04 00 00       	and    eax,0x400
   140003d0b:	85 c0                	test   eax,eax
   140003d0d:	74 07                	je     140003d16 <__pformat_cvt+0x75>
   140003d0f:	b8 03 00 00 00       	mov    eax,0x3
   140003d14:	eb 05                	jmp    140003d1b <__pformat_cvt+0x7a>
   140003d16:	b8 04 00 00 00       	mov    eax,0x4
   140003d1b:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140003d1e:	eb 4a                	jmp    140003d6a <__pformat_cvt+0xc9>
   140003d20:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d23:	25 00 04 00 00       	and    eax,0x400
   140003d28:	85 c0                	test   eax,eax
   140003d2a:	74 37                	je     140003d63 <__pformat_cvt+0xc2>
   140003d2c:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d2f:	25 00 40 00 00       	and    eax,0x4000
   140003d34:	85 c0                	test   eax,eax
   140003d36:	74 10                	je     140003d48 <__pformat_cvt+0xa7>
   140003d38:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140003d3f:	c7 45 fc c3 bf ff ff 	mov    DWORD PTR [rbp-0x4],0xffffbfc3
   140003d46:	eb 22                	jmp    140003d6a <__pformat_cvt+0xc9>
   140003d48:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140003d4f:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140003d53:	98                   	cwde
   140003d54:	25 ff 7f 00 00       	and    eax,0x7fff
   140003d59:	2d 3e 40 00 00       	sub    eax,0x403e
   140003d5e:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003d61:	eb 07                	jmp    140003d6a <__pformat_cvt+0xc9>
   140003d63:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140003d6a:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140003d6d:	83 f8 04             	cmp    eax,0x4
   140003d70:	74 0e                	je     140003d80 <__pformat_cvt+0xdf>
   140003d72:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140003d76:	98                   	cwde
   140003d77:	25 00 80 00 00       	and    eax,0x8000
   140003d7c:	89 c2                	mov    edx,eax
   140003d7e:	eb 05                	jmp    140003d85 <__pformat_cvt+0xe4>
   140003d80:	ba 00 00 00 00       	mov    edx,0x0
   140003d85:	48 8b 45 40          	mov    rax,QWORD PTR [rbp+0x40]
   140003d89:	89 10                	mov    DWORD PTR [rax],edx
   140003d8b:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003d8e:	4c 8d 4d f8          	lea    r9,[rbp-0x8]
   140003d92:	4c 8d 45 e0          	lea    r8,[rbp-0x20]
   140003d96:	48 8d 0d d3 62 00 00 	lea    rcx,[rip+0x62d3]        # 14000a070 <fpi.0>
   140003d9d:	48 8d 55 f0          	lea    rdx,[rbp-0x10]
   140003da1:	48 89 54 24 38       	mov    QWORD PTR [rsp+0x38],rdx
   140003da6:	48 8b 55 38          	mov    rdx,QWORD PTR [rbp+0x38]
   140003daa:	48 89 54 24 30       	mov    QWORD PTR [rsp+0x30],rdx
   140003daf:	8b 55 30             	mov    edx,DWORD PTR [rbp+0x30]
   140003db2:	89 54 24 28          	mov    DWORD PTR [rsp+0x28],edx
   140003db6:	8b 55 20             	mov    edx,DWORD PTR [rbp+0x20]
   140003db9:	89 54 24 20          	mov    DWORD PTR [rsp+0x20],edx
   140003dbd:	89 c2                	mov    edx,eax
   140003dbf:	e8 96 24 00 00       	call   14000625a <__gdtoa>
   140003dc4:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140003dcb:	5b                   	pop    rbx
   140003dcc:	5d                   	pop    rbp
   140003dcd:	c3                   	ret

0000000140003dce <__pformat_ecvt>:
   140003dce:	55                   	push   rbp
   140003dcf:	53                   	push   rbx
   140003dd0:	48 83 ec 58          	sub    rsp,0x58
   140003dd4:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140003dd9:	48 89 cb             	mov    rbx,rcx
   140003ddc:	db 2b                	fld    TBYTE PTR [rbx]
   140003dde:	db 7d f0             	fstp   TBYTE PTR [rbp-0x10]
   140003de1:	89 55 28             	mov    DWORD PTR [rbp+0x28],edx
   140003de4:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140003de8:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140003dec:	db 6d f0             	fld    TBYTE PTR [rbp-0x10]
   140003def:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140003df2:	4c 8b 45 30          	mov    r8,QWORD PTR [rbp+0x30]
   140003df6:	8b 4d 28             	mov    ecx,DWORD PTR [rbp+0x28]
   140003df9:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003dfd:	48 8b 55 38          	mov    rdx,QWORD PTR [rbp+0x38]
   140003e01:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140003e06:	4d 89 c1             	mov    r9,r8
   140003e09:	41 89 c8             	mov    r8d,ecx
   140003e0c:	48 89 c2             	mov    rdx,rax
   140003e0f:	b9 02 00 00 00       	mov    ecx,0x2
   140003e14:	e8 88 fe ff ff       	call   140003ca1 <__pformat_cvt>
   140003e19:	48 83 c4 58          	add    rsp,0x58
   140003e1d:	5b                   	pop    rbx
   140003e1e:	5d                   	pop    rbp
   140003e1f:	c3                   	ret

0000000140003e20 <__pformat_fcvt>:
   140003e20:	55                   	push   rbp
   140003e21:	53                   	push   rbx
   140003e22:	48 83 ec 58          	sub    rsp,0x58
   140003e26:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140003e2b:	48 89 cb             	mov    rbx,rcx
   140003e2e:	db 2b                	fld    TBYTE PTR [rbx]
   140003e30:	db 7d f0             	fstp   TBYTE PTR [rbp-0x10]
   140003e33:	89 55 28             	mov    DWORD PTR [rbp+0x28],edx
   140003e36:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140003e3a:	4c 89 4d 38          	mov    QWORD PTR [rbp+0x38],r9
   140003e3e:	db 6d f0             	fld    TBYTE PTR [rbp-0x10]
   140003e41:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140003e44:	4c 8b 45 30          	mov    r8,QWORD PTR [rbp+0x30]
   140003e48:	8b 4d 28             	mov    ecx,DWORD PTR [rbp+0x28]
   140003e4b:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140003e4f:	48 8b 55 38          	mov    rdx,QWORD PTR [rbp+0x38]
   140003e53:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   140003e58:	4d 89 c1             	mov    r9,r8
   140003e5b:	41 89 c8             	mov    r8d,ecx
   140003e5e:	48 89 c2             	mov    rdx,rax
   140003e61:	b9 03 00 00 00       	mov    ecx,0x3
   140003e66:	e8 36 fe ff ff       	call   140003ca1 <__pformat_cvt>
   140003e6b:	48 83 c4 58          	add    rsp,0x58
   140003e6f:	5b                   	pop    rbx
   140003e70:	5d                   	pop    rbp
   140003e71:	c3                   	ret

0000000140003e72 <__pformat_emit_radix_point>:
   140003e72:	55                   	push   rbp
   140003e73:	53                   	push   rbx
   140003e74:	48 83 ec 68          	sub    rsp,0x68
   140003e78:	48 8d 6c 24 60       	lea    rbp,[rsp+0x60]
   140003e7d:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   140003e81:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003e85:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140003e88:	83 f8 fd             	cmp    eax,0xfffffffd
   140003e8b:	75 48                	jne    140003ed5 <__pformat_emit_radix_point+0x63>
   140003e8d:	48 c7 45 cc 00 00 00 	mov    QWORD PTR [rbp-0x34],0x0
   140003e94:	00 
   140003e95:	e8 4e 57 00 00       	call   1400095e8 <localeconv>
   140003e9a:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   140003e9d:	48 8d 4d cc          	lea    rcx,[rbp-0x34]
   140003ea1:	48 8d 45 d6          	lea    rax,[rbp-0x2a]
   140003ea5:	49 89 c9             	mov    r9,rcx
   140003ea8:	41 b8 10 00 00 00    	mov    r8d,0x10
   140003eae:	48 89 c1             	mov    rcx,rax
   140003eb1:	e8 6a 51 00 00       	call   140009020 <mbrtowc>
   140003eb6:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   140003eb9:	83 7d ec 00          	cmp    DWORD PTR [rbp-0x14],0x0
   140003ebd:	7e 0c                	jle    140003ecb <__pformat_emit_radix_point+0x59>
   140003ebf:	0f b7 55 d6          	movzx  edx,WORD PTR [rbp-0x2a]
   140003ec3:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ec7:	66 89 50 18          	mov    WORD PTR [rax+0x18],dx
   140003ecb:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ecf:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   140003ed2:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140003ed5:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ed9:	0f b7 40 18          	movzx  eax,WORD PTR [rax+0x18]
   140003edd:	66 85 c0             	test   ax,ax
   140003ee0:	0f 84 b8 00 00 00    	je     140003f9e <__pformat_emit_radix_point+0x12c>
   140003ee6:	48 89 e0             	mov    rax,rsp
   140003ee9:	48 89 c3             	mov    rbx,rax
   140003eec:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003ef0:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140003ef3:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003ef6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003ef9:	48 63 d0             	movsxd rdx,eax
   140003efc:	48 83 ea 01          	sub    rdx,0x1
   140003f00:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   140003f04:	48 98                	cdqe
   140003f06:	48 83 c0 0f          	add    rax,0xf
   140003f0a:	48 c1 e8 04          	shr    rax,0x4
   140003f0e:	48 c1 e0 04          	shl    rax,0x4
   140003f12:	e8 59 f1 ff ff       	call   140003070 <___chkstk_ms>
   140003f17:	48 29 c4             	sub    rsp,rax
   140003f1a:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   140003f1f:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140003f23:	48 c7 45 c4 00 00 00 	mov    QWORD PTR [rbp-0x3c],0x0
   140003f2a:	00 
   140003f2b:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003f2f:	0f b7 40 18          	movzx  eax,WORD PTR [rax+0x18]
   140003f33:	0f b7 d0             	movzx  edx,ax
   140003f36:	48 8d 4d c4          	lea    rcx,[rbp-0x3c]
   140003f3a:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003f3e:	49 89 c8             	mov    r8,rcx
   140003f41:	48 89 c1             	mov    rcx,rax
   140003f44:	e8 87 50 00 00       	call   140008fd0 <wcrtomb>
   140003f49:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140003f4c:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140003f50:	7e 36                	jle    140003f88 <__pformat_emit_radix_point+0x116>
   140003f52:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140003f56:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140003f5a:	eb 1d                	jmp    140003f79 <__pformat_emit_radix_point+0x107>
   140003f5c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140003f60:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140003f64:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140003f68:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140003f6b:	0f be c0             	movsx  eax,al
   140003f6e:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140003f72:	89 c1                	mov    ecx,eax
   140003f74:	e8 b7 f1 ff ff       	call   140003130 <__pformat_putc>
   140003f79:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140003f7c:	8d 50 ff             	lea    edx,[rax-0x1]
   140003f7f:	89 55 fc             	mov    DWORD PTR [rbp-0x4],edx
   140003f82:	85 c0                	test   eax,eax
   140003f84:	7f d6                	jg     140003f5c <__pformat_emit_radix_point+0xea>
   140003f86:	eb 11                	jmp    140003f99 <__pformat_emit_radix_point+0x127>
   140003f88:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003f8c:	48 89 c2             	mov    rdx,rax
   140003f8f:	b9 2e 00 00 00       	mov    ecx,0x2e
   140003f94:	e8 97 f1 ff ff       	call   140003130 <__pformat_putc>
   140003f99:	48 89 dc             	mov    rsp,rbx
   140003f9c:	eb 11                	jmp    140003faf <__pformat_emit_radix_point+0x13d>
   140003f9e:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140003fa2:	48 89 c2             	mov    rdx,rax
   140003fa5:	b9 2e 00 00 00       	mov    ecx,0x2e
   140003faa:	e8 81 f1 ff ff       	call   140003130 <__pformat_putc>
   140003faf:	90                   	nop
   140003fb0:	48 8d 65 08          	lea    rsp,[rbp+0x8]
   140003fb4:	5b                   	pop    rbx
   140003fb5:	5d                   	pop    rbp
   140003fb6:	c3                   	ret

0000000140003fb7 <__pformat_emit_numeric_value>:
   140003fb7:	55                   	push   rbp
   140003fb8:	48 89 e5             	mov    rbp,rsp
   140003fbb:	48 83 ec 30          	sub    rsp,0x30
   140003fbf:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140003fc2:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140003fc6:	83 7d 10 2e          	cmp    DWORD PTR [rbp+0x10],0x2e
   140003fca:	75 0e                	jne    140003fda <__pformat_emit_numeric_value+0x23>
   140003fcc:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003fd0:	48 89 c1             	mov    rcx,rax
   140003fd3:	e8 9a fe ff ff       	call   140003e72 <__pformat_emit_radix_point>
   140003fd8:	eb 43                	jmp    14000401d <__pformat_emit_numeric_value+0x66>
   140003fda:	83 7d 10 2c          	cmp    DWORD PTR [rbp+0x10],0x2c
   140003fde:	75 2f                	jne    14000400f <__pformat_emit_numeric_value+0x58>
   140003fe0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140003fe4:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   140003fe8:	66 89 45 fe          	mov    WORD PTR [rbp-0x2],ax
   140003fec:	0f b7 45 fe          	movzx  eax,WORD PTR [rbp-0x2]
   140003ff0:	66 85 c0             	test   ax,ax
   140003ff3:	74 28                	je     14000401d <__pformat_emit_numeric_value+0x66>
   140003ff5:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140003ff9:	48 8d 45 fe          	lea    rax,[rbp-0x2]
   140003ffd:	49 89 d0             	mov    r8,rdx
   140004000:	ba 01 00 00 00       	mov    edx,0x1
   140004005:	48 89 c1             	mov    rcx,rax
   140004008:	e8 2c f3 ff ff       	call   140003339 <__pformat_wputchars>
   14000400d:	eb 0e                	jmp    14000401d <__pformat_emit_numeric_value+0x66>
   14000400f:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140004013:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140004016:	89 c1                	mov    ecx,eax
   140004018:	e8 13 f1 ff ff       	call   140003130 <__pformat_putc>
   14000401d:	90                   	nop
   14000401e:	48 83 c4 30          	add    rsp,0x30
   140004022:	5d                   	pop    rbp
   140004023:	c3                   	ret

0000000140004024 <__pformat_emit_inf_or_nan>:
   140004024:	55                   	push   rbp
   140004025:	48 89 e5             	mov    rbp,rsp
   140004028:	48 83 ec 40          	sub    rsp,0x40
   14000402c:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000402f:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140004033:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140004037:	48 8d 45 ec          	lea    rax,[rbp-0x14]
   14000403b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000403f:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140004043:	c7 40 10 ff ff ff ff 	mov    DWORD PTR [rax+0x10],0xffffffff
   14000404a:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   14000404e:	74 11                	je     140004061 <__pformat_emit_inf_or_nan+0x3d>
   140004050:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140004054:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004058:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   14000405c:	c6 00 2d             	mov    BYTE PTR [rax],0x2d
   14000405f:	eb 3e                	jmp    14000409f <__pformat_emit_inf_or_nan+0x7b>
   140004061:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140004065:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004068:	25 00 01 00 00       	and    eax,0x100
   14000406d:	85 c0                	test   eax,eax
   14000406f:	74 11                	je     140004082 <__pformat_emit_inf_or_nan+0x5e>
   140004071:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140004075:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004079:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   14000407d:	c6 00 2b             	mov    BYTE PTR [rax],0x2b
   140004080:	eb 1d                	jmp    14000409f <__pformat_emit_inf_or_nan+0x7b>
   140004082:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140004086:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004089:	83 e0 40             	and    eax,0x40
   14000408c:	85 c0                	test   eax,eax
   14000408e:	74 0f                	je     14000409f <__pformat_emit_inf_or_nan+0x7b>
   140004090:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140004094:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004098:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   14000409c:	c6 00 20             	mov    BYTE PTR [rax],0x20
   14000409f:	c7 45 fc 03 00 00 00 	mov    DWORD PTR [rbp-0x4],0x3
   1400040a6:	eb 38                	jmp    1400040e0 <__pformat_emit_inf_or_nan+0xbc>
   1400040a8:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400040ac:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400040b0:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400040b4:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400040b7:	83 e0 df             	and    eax,0xffffffdf
   1400040ba:	41 89 c0             	mov    r8d,eax
   1400040bd:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400040c1:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400040c4:	83 e0 20             	and    eax,0x20
   1400040c7:	89 c1                	mov    ecx,eax
   1400040c9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400040cd:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400040d1:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400040d5:	44 89 c2             	mov    edx,r8d
   1400040d8:	09 ca                	or     edx,ecx
   1400040da:	88 10                	mov    BYTE PTR [rax],dl
   1400040dc:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   1400040e0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400040e4:	7f c2                	jg     1400040a8 <__pformat_emit_inf_or_nan+0x84>
   1400040e6:	48 8d 45 ec          	lea    rax,[rbp-0x14]
   1400040ea:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   1400040ee:	48 29 c2             	sub    rdx,rax
   1400040f1:	89 d1                	mov    ecx,edx
   1400040f3:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400040f7:	48 8d 45 ec          	lea    rax,[rbp-0x14]
   1400040fb:	49 89 d0             	mov    r8,rdx
   1400040fe:	89 ca                	mov    edx,ecx
   140004100:	48 89 c1             	mov    rcx,rax
   140004103:	e8 ac f0 ff ff       	call   1400031b4 <__pformat_putchars>
   140004108:	90                   	nop
   140004109:	48 83 c4 40          	add    rsp,0x40
   14000410d:	5d                   	pop    rbp
   14000410e:	c3                   	ret

000000014000410f <__pformat_emit_float>:
   14000410f:	55                   	push   rbp
   140004110:	48 89 e5             	mov    rbp,rsp
   140004113:	48 83 ec 30          	sub    rsp,0x30
   140004117:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000411a:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000411e:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   140004122:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140004126:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   14000412a:	7e 2e                	jle    14000415a <__pformat_emit_float+0x4b>
   14000412c:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004130:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004133:	39 45 20             	cmp    DWORD PTR [rbp+0x20],eax
   140004136:	7f 15                	jg     14000414d <__pformat_emit_float+0x3e>
   140004138:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000413c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000413f:	2b 45 20             	sub    eax,DWORD PTR [rbp+0x20]
   140004142:	89 c2                	mov    edx,eax
   140004144:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004148:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   14000414b:	eb 29                	jmp    140004176 <__pformat_emit_float+0x67>
   14000414d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004151:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140004158:	eb 1c                	jmp    140004176 <__pformat_emit_float+0x67>
   14000415a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000415e:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004161:	85 c0                	test   eax,eax
   140004163:	7e 11                	jle    140004176 <__pformat_emit_float+0x67>
   140004165:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004169:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000416c:	8d 50 ff             	lea    edx,[rax-0x1]
   14000416f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004173:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004176:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000417a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000417d:	85 c0                	test   eax,eax
   14000417f:	78 2b                	js     1400041ac <__pformat_emit_float+0x9d>
   140004181:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004185:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140004188:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000418c:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000418f:	39 c2                	cmp    edx,eax
   140004191:	7e 19                	jle    1400041ac <__pformat_emit_float+0x9d>
   140004193:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004197:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   14000419a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000419e:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400041a1:	29 c2                	sub    edx,eax
   1400041a3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041a7:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400041aa:	eb 0b                	jmp    1400041b7 <__pformat_emit_float+0xa8>
   1400041ac:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041b0:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   1400041b7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041bb:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400041be:	85 c0                	test   eax,eax
   1400041c0:	7e 2c                	jle    1400041ee <__pformat_emit_float+0xdf>
   1400041c2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041c6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400041c9:	85 c0                	test   eax,eax
   1400041cb:	7f 10                	jg     1400041dd <__pformat_emit_float+0xce>
   1400041cd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041d1:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400041d4:	25 00 08 00 00       	and    eax,0x800
   1400041d9:	85 c0                	test   eax,eax
   1400041db:	74 11                	je     1400041ee <__pformat_emit_float+0xdf>
   1400041dd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041e1:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400041e4:	8d 50 ff             	lea    edx,[rax-0x1]
   1400041e7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041eb:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   1400041ee:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   1400041f2:	7e 64                	jle    140004258 <__pformat_emit_float+0x149>
   1400041f4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400041f8:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400041fb:	25 00 10 00 00       	and    eax,0x1000
   140004200:	85 c0                	test   eax,eax
   140004202:	74 54                	je     140004258 <__pformat_emit_float+0x149>
   140004204:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004208:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   14000420c:	66 85 c0             	test   ax,ax
   14000420f:	74 47                	je     140004258 <__pformat_emit_float+0x149>
   140004211:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004214:	83 c0 02             	add    eax,0x2
   140004217:	48 63 d0             	movsxd rdx,eax
   14000421a:	48 69 d2 56 55 55 55 	imul   rdx,rdx,0x55555556
   140004221:	48 c1 ea 20          	shr    rdx,0x20
   140004225:	c1 f8 1f             	sar    eax,0x1f
   140004228:	29 c2                	sub    edx,eax
   14000422a:	8d 42 ff             	lea    eax,[rdx-0x1]
   14000422d:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004230:	eb 15                	jmp    140004247 <__pformat_emit_float+0x138>
   140004232:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   140004236:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000423a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000423d:	8d 50 ff             	lea    edx,[rax-0x1]
   140004240:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004244:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004247:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   14000424b:	7e 0b                	jle    140004258 <__pformat_emit_float+0x149>
   14000424d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004251:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004254:	85 c0                	test   eax,eax
   140004256:	7f da                	jg     140004232 <__pformat_emit_float+0x123>
   140004258:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000425c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000425f:	85 c0                	test   eax,eax
   140004261:	7e 27                	jle    14000428a <__pformat_emit_float+0x17b>
   140004263:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   140004267:	75 10                	jne    140004279 <__pformat_emit_float+0x16a>
   140004269:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000426d:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004270:	25 c0 01 00 00       	and    eax,0x1c0
   140004275:	85 c0                	test   eax,eax
   140004277:	74 11                	je     14000428a <__pformat_emit_float+0x17b>
   140004279:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000427d:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004280:	8d 50 ff             	lea    edx,[rax-0x1]
   140004283:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004287:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   14000428a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000428e:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004291:	85 c0                	test   eax,eax
   140004293:	7e 38                	jle    1400042cd <__pformat_emit_float+0x1be>
   140004295:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004299:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000429c:	25 00 06 00 00       	and    eax,0x600
   1400042a1:	85 c0                	test   eax,eax
   1400042a3:	75 28                	jne    1400042cd <__pformat_emit_float+0x1be>
   1400042a5:	eb 11                	jmp    1400042b8 <__pformat_emit_float+0x1a9>
   1400042a7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042ab:	48 89 c2             	mov    rdx,rax
   1400042ae:	b9 20 00 00 00       	mov    ecx,0x20
   1400042b3:	e8 78 ee ff ff       	call   140003130 <__pformat_putc>
   1400042b8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042bc:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400042bf:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400042c2:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400042c6:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400042c9:	85 c0                	test   eax,eax
   1400042cb:	7f da                	jg     1400042a7 <__pformat_emit_float+0x198>
   1400042cd:	83 7d 10 00          	cmp    DWORD PTR [rbp+0x10],0x0
   1400042d1:	74 13                	je     1400042e6 <__pformat_emit_float+0x1d7>
   1400042d3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042d7:	48 89 c2             	mov    rdx,rax
   1400042da:	b9 2d 00 00 00       	mov    ecx,0x2d
   1400042df:	e8 4c ee ff ff       	call   140003130 <__pformat_putc>
   1400042e4:	eb 42                	jmp    140004328 <__pformat_emit_float+0x219>
   1400042e6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042ea:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400042ed:	25 00 01 00 00       	and    eax,0x100
   1400042f2:	85 c0                	test   eax,eax
   1400042f4:	74 13                	je     140004309 <__pformat_emit_float+0x1fa>
   1400042f6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400042fa:	48 89 c2             	mov    rdx,rax
   1400042fd:	b9 2b 00 00 00       	mov    ecx,0x2b
   140004302:	e8 29 ee ff ff       	call   140003130 <__pformat_putc>
   140004307:	eb 1f                	jmp    140004328 <__pformat_emit_float+0x219>
   140004309:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000430d:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004310:	83 e0 40             	and    eax,0x40
   140004313:	85 c0                	test   eax,eax
   140004315:	74 11                	je     140004328 <__pformat_emit_float+0x219>
   140004317:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000431b:	48 89 c2             	mov    rdx,rax
   14000431e:	b9 20 00 00 00       	mov    ecx,0x20
   140004323:	e8 08 ee ff ff       	call   140003130 <__pformat_putc>
   140004328:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000432c:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000432f:	85 c0                	test   eax,eax
   140004331:	7e 3b                	jle    14000436e <__pformat_emit_float+0x25f>
   140004333:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004337:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000433a:	25 00 06 00 00       	and    eax,0x600
   14000433f:	3d 00 02 00 00       	cmp    eax,0x200
   140004344:	75 28                	jne    14000436e <__pformat_emit_float+0x25f>
   140004346:	eb 11                	jmp    140004359 <__pformat_emit_float+0x24a>
   140004348:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000434c:	48 89 c2             	mov    rdx,rax
   14000434f:	b9 30 00 00 00       	mov    ecx,0x30
   140004354:	e8 d7 ed ff ff       	call   140003130 <__pformat_putc>
   140004359:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000435d:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004360:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004363:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004367:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   14000436a:	85 c0                	test   eax,eax
   14000436c:	7f da                	jg     140004348 <__pformat_emit_float+0x239>
   14000436e:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004372:	0f 8e a7 00 00 00    	jle    14000441f <__pformat_emit_float+0x310>
   140004378:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000437c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000437f:	84 c0                	test   al,al
   140004381:	74 14                	je     140004397 <__pformat_emit_float+0x288>
   140004383:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004387:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000438b:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   14000438f:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004392:	0f be c0             	movsx  eax,al
   140004395:	eb 05                	jmp    14000439c <__pformat_emit_float+0x28d>
   140004397:	b8 30 00 00 00       	mov    eax,0x30
   14000439c:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400043a0:	89 c1                	mov    ecx,eax
   1400043a2:	e8 89 ed ff ff       	call   140003130 <__pformat_putc>
   1400043a7:	83 6d 20 01          	sub    DWORD PTR [rbp+0x20],0x1
   1400043ab:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   1400043af:	74 62                	je     140004413 <__pformat_emit_float+0x304>
   1400043b1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400043b5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400043b8:	25 00 10 00 00       	and    eax,0x1000
   1400043bd:	85 c0                	test   eax,eax
   1400043bf:	74 52                	je     140004413 <__pformat_emit_float+0x304>
   1400043c1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400043c5:	0f b7 40 20          	movzx  eax,WORD PTR [rax+0x20]
   1400043c9:	66 85 c0             	test   ax,ax
   1400043cc:	74 45                	je     140004413 <__pformat_emit_float+0x304>
   1400043ce:	8b 4d 20             	mov    ecx,DWORD PTR [rbp+0x20]
   1400043d1:	48 63 c1             	movsxd rax,ecx
   1400043d4:	48 69 c0 56 55 55 55 	imul   rax,rax,0x55555556
   1400043db:	48 c1 e8 20          	shr    rax,0x20
   1400043df:	48 89 c2             	mov    rdx,rax
   1400043e2:	89 c8                	mov    eax,ecx
   1400043e4:	c1 f8 1f             	sar    eax,0x1f
   1400043e7:	29 c2                	sub    edx,eax
   1400043e9:	89 d0                	mov    eax,edx
   1400043eb:	01 c0                	add    eax,eax
   1400043ed:	01 d0                	add    eax,edx
   1400043ef:	29 c1                	sub    ecx,eax
   1400043f1:	89 ca                	mov    edx,ecx
   1400043f3:	85 d2                	test   edx,edx
   1400043f5:	75 1c                	jne    140004413 <__pformat_emit_float+0x304>
   1400043f7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400043fb:	48 83 c0 20          	add    rax,0x20
   1400043ff:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004403:	49 89 d0             	mov    r8,rdx
   140004406:	ba 01 00 00 00       	mov    edx,0x1
   14000440b:	48 89 c1             	mov    rcx,rax
   14000440e:	e8 26 ef ff ff       	call   140003339 <__pformat_wputchars>
   140004413:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004417:	0f 8f 5b ff ff ff    	jg     140004378 <__pformat_emit_float+0x269>
   14000441d:	eb 11                	jmp    140004430 <__pformat_emit_float+0x321>
   14000441f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004423:	48 89 c2             	mov    rdx,rax
   140004426:	b9 30 00 00 00       	mov    ecx,0x30
   14000442b:	e8 00 ed ff ff       	call   140003130 <__pformat_putc>
   140004430:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004434:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004437:	85 c0                	test   eax,eax
   140004439:	7f 10                	jg     14000444b <__pformat_emit_float+0x33c>
   14000443b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000443f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004442:	25 00 08 00 00       	and    eax,0x800
   140004447:	85 c0                	test   eax,eax
   140004449:	74 0c                	je     140004457 <__pformat_emit_float+0x348>
   14000444b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000444f:	48 89 c1             	mov    rcx,rax
   140004452:	e8 1b fa ff ff       	call   140003e72 <__pformat_emit_radix_point>
   140004457:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   14000445b:	79 5f                	jns    1400044bc <__pformat_emit_float+0x3ad>
   14000445d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004461:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   140004464:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004467:	01 c2                	add    edx,eax
   140004469:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000446d:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004470:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004474:	48 89 c2             	mov    rdx,rax
   140004477:	b9 30 00 00 00       	mov    ecx,0x30
   14000447c:	e8 af ec ff ff       	call   140003130 <__pformat_putc>
   140004481:	83 45 20 01          	add    DWORD PTR [rbp+0x20],0x1
   140004485:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004489:	78 e5                	js     140004470 <__pformat_emit_float+0x361>
   14000448b:	eb 2f                	jmp    1400044bc <__pformat_emit_float+0x3ad>
   14000448d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004491:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004494:	84 c0                	test   al,al
   140004496:	74 14                	je     1400044ac <__pformat_emit_float+0x39d>
   140004498:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000449c:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400044a0:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400044a4:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400044a7:	0f be c0             	movsx  eax,al
   1400044aa:	eb 05                	jmp    1400044b1 <__pformat_emit_float+0x3a2>
   1400044ac:	b8 30 00 00 00       	mov    eax,0x30
   1400044b1:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400044b5:	89 c1                	mov    ecx,eax
   1400044b7:	e8 74 ec ff ff       	call   140003130 <__pformat_putc>
   1400044bc:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400044c0:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400044c3:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400044c6:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400044ca:	89 4a 10             	mov    DWORD PTR [rdx+0x10],ecx
   1400044cd:	85 c0                	test   eax,eax
   1400044cf:	7f bc                	jg     14000448d <__pformat_emit_float+0x37e>
   1400044d1:	90                   	nop
   1400044d2:	90                   	nop
   1400044d3:	48 83 c4 30          	add    rsp,0x30
   1400044d7:	5d                   	pop    rbp
   1400044d8:	c3                   	ret

00000001400044d9 <__pformat_emit_efloat>:
   1400044d9:	55                   	push   rbp
   1400044da:	48 89 e5             	mov    rbp,rsp
   1400044dd:	48 83 ec 50          	sub    rsp,0x50
   1400044e1:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400044e4:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400044e8:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   1400044ec:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400044f0:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400044f7:	83 6d 20 01          	sub    DWORD PTR [rbp+0x20],0x1
   1400044fb:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   1400044ff:	79 09                	jns    14000450a <__pformat_emit_efloat+0x31>
   140004501:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   140004508:	eb 05                	jmp    14000450f <__pformat_emit_efloat+0x36>
   14000450a:	b8 00 00 00 00       	mov    eax,0x0
   14000450f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140004513:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004516:	48 98                	cdqe
   140004518:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000451c:	eb 04                	jmp    140004522 <__pformat_emit_efloat+0x49>
   14000451e:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140004522:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140004525:	48 63 d0             	movsxd rdx,eax
   140004528:	48 69 d2 67 66 66 66 	imul   rdx,rdx,0x66666667
   14000452f:	48 c1 ea 20          	shr    rdx,0x20
   140004533:	89 d1                	mov    ecx,edx
   140004535:	c1 f9 02             	sar    ecx,0x2
   140004538:	99                   	cdq
   140004539:	89 c8                	mov    eax,ecx
   14000453b:	29 d0                	sub    eax,edx
   14000453d:	89 45 20             	mov    DWORD PTR [rbp+0x20],eax
   140004540:	83 7d 20 00          	cmp    DWORD PTR [rbp+0x20],0x0
   140004544:	75 d8                	jne    14000451e <__pformat_emit_efloat+0x45>
   140004546:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000454a:	8b 40 2c             	mov    eax,DWORD PTR [rax+0x2c]
   14000454d:	83 f8 ff             	cmp    eax,0xffffffff
   140004550:	75 0b                	jne    14000455d <__pformat_emit_efloat+0x84>
   140004552:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004556:	c7 40 2c 02 00 00 00 	mov    DWORD PTR [rax+0x2c],0x2
   14000455d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004561:	8b 40 2c             	mov    eax,DWORD PTR [rax+0x2c]
   140004564:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140004567:	7d 0a                	jge    140004573 <__pformat_emit_efloat+0x9a>
   140004569:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000456d:	8b 40 2c             	mov    eax,DWORD PTR [rax+0x2c]
   140004570:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004573:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004577:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000457a:	83 45 fc 02          	add    DWORD PTR [rbp-0x4],0x2
   14000457e:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140004581:	7d 15                	jge    140004598 <__pformat_emit_efloat+0xbf>
   140004583:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004587:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000458a:	2b 45 fc             	sub    eax,DWORD PTR [rbp-0x4]
   14000458d:	89 c2                	mov    edx,eax
   14000458f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004593:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004596:	eb 0b                	jmp    1400045a3 <__pformat_emit_efloat+0xca>
   140004598:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000459c:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   1400045a3:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   1400045a7:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400045ab:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   1400045ae:	49 89 c9             	mov    r9,rcx
   1400045b1:	41 b8 01 00 00 00    	mov    r8d,0x1
   1400045b7:	89 c1                	mov    ecx,eax
   1400045b9:	e8 51 fb ff ff       	call   14000410f <__pformat_emit_float>
   1400045be:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045c2:	8b 50 2c             	mov    edx,DWORD PTR [rax+0x2c]
   1400045c5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045c9:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   1400045cc:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045d0:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400045d3:	0d c0 01 00 00       	or     eax,0x1c0
   1400045d8:	89 c2                	mov    edx,eax
   1400045da:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045de:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   1400045e1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045e5:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400045e8:	83 e0 20             	and    eax,0x20
   1400045eb:	83 c8 45             	or     eax,0x45
   1400045ee:	89 c1                	mov    ecx,eax
   1400045f0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400045f4:	48 89 c2             	mov    rdx,rax
   1400045f7:	e8 34 eb ff ff       	call   140003130 <__pformat_putc>
   1400045fc:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004600:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004603:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140004606:	83 ea 01             	sub    edx,0x1
   140004609:	01 c2                	add    edx,eax
   14000460b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000460f:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004612:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140004616:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   14000461a:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   14000461e:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
   140004622:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004626:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000462a:	48 89 c1             	mov    rcx,rax
   14000462d:	e8 69 ef ff ff       	call   14000359b <__pformat_int>
   140004632:	90                   	nop
   140004633:	48 83 c4 50          	add    rsp,0x50
   140004637:	5d                   	pop    rbp
   140004638:	c3                   	ret

0000000140004639 <__pformat_float>:
   140004639:	55                   	push   rbp
   14000463a:	53                   	push   rbx
   14000463b:	48 83 ec 58          	sub    rsp,0x58
   14000463f:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140004644:	48 89 cb             	mov    rbx,rcx
   140004647:	db 2b                	fld    TBYTE PTR [rbx]
   140004649:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   14000464c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004650:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004654:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004657:	85 c0                	test   eax,eax
   140004659:	79 0b                	jns    140004666 <__pformat_float+0x2d>
   14000465b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000465f:	c7 40 10 06 00 00 00 	mov    DWORD PTR [rax+0x10],0x6
   140004666:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000466a:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   14000466d:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140004670:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004673:	4c 8d 45 f4          	lea    r8,[rbp-0xc]
   140004677:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   14000467b:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   14000467f:	4d 89 c1             	mov    r9,r8
   140004682:	49 89 c8             	mov    r8,rcx
   140004685:	48 89 c1             	mov    rcx,rax
   140004688:	e8 93 f7 ff ff       	call   140003e20 <__pformat_fcvt>
   14000468d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004691:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004694:	3d 00 80 ff ff       	cmp    eax,0xffff8000
   140004699:	75 17                	jne    1400046b2 <__pformat_float+0x79>
   14000469b:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000469e:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   1400046a2:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400046a6:	49 89 c8             	mov    r8,rcx
   1400046a9:	89 c1                	mov    ecx,eax
   1400046ab:	e8 74 f9 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   1400046b0:	eb 43                	jmp    1400046f5 <__pformat_float+0xbc>
   1400046b2:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   1400046b5:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400046b8:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   1400046bc:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400046c0:	4d 89 c1             	mov    r9,r8
   1400046c3:	41 89 c8             	mov    r8d,ecx
   1400046c6:	89 c1                	mov    ecx,eax
   1400046c8:	e8 42 fa ff ff       	call   14000410f <__pformat_emit_float>
   1400046cd:	eb 11                	jmp    1400046e0 <__pformat_float+0xa7>
   1400046cf:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400046d3:	48 89 c2             	mov    rdx,rax
   1400046d6:	b9 20 00 00 00       	mov    ecx,0x20
   1400046db:	e8 50 ea ff ff       	call   140003130 <__pformat_putc>
   1400046e0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400046e4:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400046e7:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400046ea:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400046ee:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   1400046f1:	85 c0                	test   eax,eax
   1400046f3:	7f da                	jg     1400046cf <__pformat_float+0x96>
   1400046f5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400046f9:	48 89 c1             	mov    rcx,rax
   1400046fc:	e8 4e 17 00 00       	call   140005e4f <__freedtoa>
   140004701:	90                   	nop
   140004702:	48 83 c4 58          	add    rsp,0x58
   140004706:	5b                   	pop    rbx
   140004707:	5d                   	pop    rbp
   140004708:	c3                   	ret

0000000140004709 <__pformat_efloat>:
   140004709:	55                   	push   rbp
   14000470a:	53                   	push   rbx
   14000470b:	48 83 ec 58          	sub    rsp,0x58
   14000470f:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140004714:	48 89 cb             	mov    rbx,rcx
   140004717:	db 2b                	fld    TBYTE PTR [rbx]
   140004719:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   14000471c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004720:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004724:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004727:	85 c0                	test   eax,eax
   140004729:	79 0b                	jns    140004736 <__pformat_efloat+0x2d>
   14000472b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000472f:	c7 40 10 06 00 00 00 	mov    DWORD PTR [rax+0x10],0x6
   140004736:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000473a:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000473d:	8d 50 01             	lea    edx,[rax+0x1]
   140004740:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140004743:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004746:	4c 8d 45 f4          	lea    r8,[rbp-0xc]
   14000474a:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   14000474e:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   140004752:	4d 89 c1             	mov    r9,r8
   140004755:	49 89 c8             	mov    r8,rcx
   140004758:	48 89 c1             	mov    rcx,rax
   14000475b:	e8 6e f6 ff ff       	call   140003dce <__pformat_ecvt>
   140004760:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004764:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004767:	3d 00 80 ff ff       	cmp    eax,0xffff8000
   14000476c:	75 17                	jne    140004785 <__pformat_efloat+0x7c>
   14000476e:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140004771:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004775:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004779:	49 89 c8             	mov    r8,rcx
   14000477c:	89 c1                	mov    ecx,eax
   14000477e:	e8 a1 f8 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   140004783:	eb 1b                	jmp    1400047a0 <__pformat_efloat+0x97>
   140004785:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   140004788:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000478b:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   14000478f:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004793:	4d 89 c1             	mov    r9,r8
   140004796:	41 89 c8             	mov    r8d,ecx
   140004799:	89 c1                	mov    ecx,eax
   14000479b:	e8 39 fd ff ff       	call   1400044d9 <__pformat_emit_efloat>
   1400047a0:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400047a4:	48 89 c1             	mov    rcx,rax
   1400047a7:	e8 a3 16 00 00       	call   140005e4f <__freedtoa>
   1400047ac:	90                   	nop
   1400047ad:	48 83 c4 58          	add    rsp,0x58
   1400047b1:	5b                   	pop    rbx
   1400047b2:	5d                   	pop    rbp
   1400047b3:	c3                   	ret

00000001400047b4 <__pformat_gfloat>:
   1400047b4:	55                   	push   rbp
   1400047b5:	53                   	push   rbx
   1400047b6:	48 83 ec 58          	sub    rsp,0x58
   1400047ba:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   1400047bf:	48 89 cb             	mov    rbx,rcx
   1400047c2:	db 2b                	fld    TBYTE PTR [rbx]
   1400047c4:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   1400047c7:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   1400047cb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047cf:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400047d2:	85 c0                	test   eax,eax
   1400047d4:	79 0d                	jns    1400047e3 <__pformat_gfloat+0x2f>
   1400047d6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047da:	c7 40 10 06 00 00 00 	mov    DWORD PTR [rax+0x10],0x6
   1400047e1:	eb 16                	jmp    1400047f9 <__pformat_gfloat+0x45>
   1400047e3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047e7:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400047ea:	85 c0                	test   eax,eax
   1400047ec:	75 0b                	jne    1400047f9 <__pformat_gfloat+0x45>
   1400047ee:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047f2:	c7 40 10 01 00 00 00 	mov    DWORD PTR [rax+0x10],0x1
   1400047f9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400047fd:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   140004800:	db 6d e0             	fld    TBYTE PTR [rbp-0x20]
   140004803:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004806:	4c 8d 45 f4          	lea    r8,[rbp-0xc]
   14000480a:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   14000480e:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   140004812:	4d 89 c1             	mov    r9,r8
   140004815:	49 89 c8             	mov    r8,rcx
   140004818:	48 89 c1             	mov    rcx,rax
   14000481b:	e8 ae f5 ff ff       	call   140003dce <__pformat_ecvt>
   140004820:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004824:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004827:	3d 00 80 ff ff       	cmp    eax,0xffff8000
   14000482c:	75 1a                	jne    140004848 <__pformat_gfloat+0x94>
   14000482e:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140004831:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004835:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004839:	49 89 c8             	mov    r8,rcx
   14000483c:	89 c1                	mov    ecx,eax
   14000483e:	e8 e1 f7 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   140004843:	e9 14 01 00 00       	jmp    14000495c <__pformat_gfloat+0x1a8>
   140004848:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   14000484b:	83 f8 fd             	cmp    eax,0xfffffffd
   14000484e:	0f 8c b2 00 00 00    	jl     140004906 <__pformat_gfloat+0x152>
   140004854:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004858:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   14000485b:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   14000485e:	39 c2                	cmp    edx,eax
   140004860:	0f 8c a0 00 00 00    	jl     140004906 <__pformat_gfloat+0x152>
   140004866:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000486a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000486d:	25 00 08 00 00       	and    eax,0x800
   140004872:	85 c0                	test   eax,eax
   140004874:	74 15                	je     14000488b <__pformat_gfloat+0xd7>
   140004876:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000487a:	8b 50 10             	mov    edx,DWORD PTR [rax+0x10]
   14000487d:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140004880:	29 c2                	sub    edx,eax
   140004882:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004886:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004889:	eb 20                	jmp    1400048ab <__pformat_gfloat+0xf7>
   14000488b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000488f:	48 89 c1             	mov    rcx,rax
   140004892:	e8 81 4d 00 00       	call   140009618 <strlen>
   140004897:	89 c1                	mov    ecx,eax
   140004899:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   14000489c:	89 c2                	mov    edx,eax
   14000489e:	89 c8                	mov    eax,ecx
   1400048a0:	29 d0                	sub    eax,edx
   1400048a2:	89 c2                	mov    edx,eax
   1400048a4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048a8:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   1400048ab:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048af:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400048b2:	85 c0                	test   eax,eax
   1400048b4:	79 0b                	jns    1400048c1 <__pformat_gfloat+0x10d>
   1400048b6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048ba:	c7 40 10 00 00 00 00 	mov    DWORD PTR [rax+0x10],0x0
   1400048c1:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   1400048c4:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400048c7:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   1400048cb:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400048cf:	4d 89 c1             	mov    r9,r8
   1400048d2:	41 89 c8             	mov    r8d,ecx
   1400048d5:	89 c1                	mov    ecx,eax
   1400048d7:	e8 33 f8 ff ff       	call   14000410f <__pformat_emit_float>
   1400048dc:	eb 11                	jmp    1400048ef <__pformat_gfloat+0x13b>
   1400048de:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048e2:	48 89 c2             	mov    rdx,rax
   1400048e5:	b9 20 00 00 00       	mov    ecx,0x20
   1400048ea:	e8 41 e8 ff ff       	call   140003130 <__pformat_putc>
   1400048ef:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400048f3:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   1400048f6:	8d 48 ff             	lea    ecx,[rax-0x1]
   1400048f9:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   1400048fd:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140004900:	85 c0                	test   eax,eax
   140004902:	7f da                	jg     1400048de <__pformat_gfloat+0x12a>
   140004904:	eb 56                	jmp    14000495c <__pformat_gfloat+0x1a8>
   140004906:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000490a:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000490d:	25 00 08 00 00       	and    eax,0x800
   140004912:	85 c0                	test   eax,eax
   140004914:	74 13                	je     140004929 <__pformat_gfloat+0x175>
   140004916:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000491a:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   14000491d:	8d 50 ff             	lea    edx,[rax-0x1]
   140004920:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004924:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004927:	eb 18                	jmp    140004941 <__pformat_gfloat+0x18d>
   140004929:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000492d:	48 89 c1             	mov    rcx,rax
   140004930:	e8 e3 4c 00 00       	call   140009618 <strlen>
   140004935:	83 e8 01             	sub    eax,0x1
   140004938:	89 c2                	mov    edx,eax
   14000493a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000493e:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004941:	8b 4d f0             	mov    ecx,DWORD PTR [rbp-0x10]
   140004944:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140004947:	4c 8b 45 28          	mov    r8,QWORD PTR [rbp+0x28]
   14000494b:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   14000494f:	4d 89 c1             	mov    r9,r8
   140004952:	41 89 c8             	mov    r8d,ecx
   140004955:	89 c1                	mov    ecx,eax
   140004957:	e8 7d fb ff ff       	call   1400044d9 <__pformat_emit_efloat>
   14000495c:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004960:	48 89 c1             	mov    rcx,rax
   140004963:	e8 e7 14 00 00       	call   140005e4f <__freedtoa>
   140004968:	90                   	nop
   140004969:	48 83 c4 58          	add    rsp,0x58
   14000496d:	5b                   	pop    rbx
   14000496e:	5d                   	pop    rbp
   14000496f:	c3                   	ret

0000000140004970 <__pformat_emit_xfloat>:
   140004970:	55                   	push   rbp
   140004971:	53                   	push   rbx
   140004972:	48 81 ec 88 00 00 00 	sub    rsp,0x88
   140004979:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   140004980:	00 
   140004981:	48 89 cb             	mov    rbx,rcx
   140004984:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004988:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   14000498c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140004990:	66 c7 45 f6 02 00    	mov    WORD PTR [rbp-0xa],0x2
   140004996:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004999:	48 85 c0             	test   rax,rax
   14000499c:	75 09                	jne    1400049a7 <__pformat_emit_xfloat+0x37>
   14000499e:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   1400049a2:	66 85 c0             	test   ax,ax
   1400049a5:	74 0b                	je     1400049b2 <__pformat_emit_xfloat+0x42>
   1400049a7:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   1400049ab:	83 e8 03             	sub    eax,0x3
   1400049ae:	66 89 43 08          	mov    WORD PTR [rbx+0x8],ax
   1400049b2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400049b6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400049b9:	85 c0                	test   eax,eax
   1400049bb:	0f 88 90 00 00 00    	js     140004a51 <__pformat_emit_xfloat+0xe1>
   1400049c1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400049c5:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400049c8:	83 f8 0e             	cmp    eax,0xe
   1400049cb:	0f 8f 80 00 00 00    	jg     140004a51 <__pformat_emit_xfloat+0xe1>
   1400049d1:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   1400049d4:	48 d1 e8             	shr    rax,1
   1400049d7:	48 89 03             	mov    QWORD PTR [rbx],rax
   1400049da:	48 8b 13             	mov    rdx,QWORD PTR [rbx]
   1400049dd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400049e1:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   1400049e4:	b9 0e 00 00 00       	mov    ecx,0xe
   1400049e9:	29 c1                	sub    ecx,eax
   1400049eb:	8d 04 8d 00 00 00 00 	lea    eax,[rcx*4+0x0]
   1400049f2:	41 b8 04 00 00 00    	mov    r8d,0x4
   1400049f8:	89 c1                	mov    ecx,eax
   1400049fa:	49 d3 e0             	shl    r8,cl
   1400049fd:	4c 89 c0             	mov    rax,r8
   140004a00:	48 01 d0             	add    rax,rdx
   140004a03:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a06:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a09:	48 85 c0             	test   rax,rax
   140004a0c:	78 0b                	js     140004a19 <__pformat_emit_xfloat+0xa9>
   140004a0e:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a11:	48 01 c0             	add    rax,rax
   140004a14:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a17:	eb 15                	jmp    140004a2e <__pformat_emit_xfloat+0xbe>
   140004a19:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004a1d:	83 c0 04             	add    eax,0x4
   140004a20:	66 89 43 08          	mov    WORD PTR [rbx+0x8],ax
   140004a24:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a27:	48 c1 e8 03          	shr    rax,0x3
   140004a2b:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a2e:	48 8b 13             	mov    rdx,QWORD PTR [rbx]
   140004a31:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a35:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a38:	b9 0f 00 00 00       	mov    ecx,0xf
   140004a3d:	29 c1                	sub    ecx,eax
   140004a3f:	8d 04 8d 00 00 00 00 	lea    eax,[rcx*4+0x0]
   140004a46:	89 c1                	mov    ecx,eax
   140004a48:	48 d3 ea             	shr    rdx,cl
   140004a4b:	48 89 d0             	mov    rax,rdx
   140004a4e:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004a51:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a54:	48 85 c0             	test   rax,rax
   140004a57:	75 0f                	jne    140004a68 <__pformat_emit_xfloat+0xf8>
   140004a59:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a5d:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a60:	85 c0                	test   eax,eax
   140004a62:	0f 8e f8 00 00 00    	jle    140004b60 <__pformat_emit_xfloat+0x1f0>
   140004a68:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a6c:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a6f:	83 f8 0e             	cmp    eax,0xe
   140004a72:	7f 1a                	jg     140004a8e <__pformat_emit_xfloat+0x11e>
   140004a74:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a78:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a7b:	85 c0                	test   eax,eax
   140004a7d:	78 0f                	js     140004a8e <__pformat_emit_xfloat+0x11e>
   140004a7f:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004a83:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004a86:	83 c0 01             	add    eax,0x1
   140004a89:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   140004a8c:	eb 07                	jmp    140004a95 <__pformat_emit_xfloat+0x125>
   140004a8e:	c7 45 f0 10 00 00 00 	mov    DWORD PTR [rbp-0x10],0x10
   140004a95:	e9 bc 00 00 00       	jmp    140004b56 <__pformat_emit_xfloat+0x1e6>
   140004a9a:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004a9d:	83 e0 0f             	and    eax,0xf
   140004aa0:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140004aa3:	83 7d f0 01          	cmp    DWORD PTR [rbp-0x10],0x1
   140004aa7:	75 36                	jne    140004adf <__pformat_emit_xfloat+0x16f>
   140004aa9:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004aad:	48 3b 45 f8          	cmp    rax,QWORD PTR [rbp-0x8]
   140004ab1:	72 1b                	jb     140004ace <__pformat_emit_xfloat+0x15e>
   140004ab3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ab7:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004aba:	25 00 08 00 00       	and    eax,0x800
   140004abf:	85 c0                	test   eax,eax
   140004ac1:	75 0b                	jne    140004ace <__pformat_emit_xfloat+0x15e>
   140004ac3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ac7:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004aca:	85 c0                	test   eax,eax
   140004acc:	7e 2d                	jle    140004afb <__pformat_emit_xfloat+0x18b>
   140004ace:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004ad2:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004ad6:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004ada:	c6 00 2e             	mov    BYTE PTR [rax],0x2e
   140004add:	eb 1c                	jmp    140004afb <__pformat_emit_xfloat+0x18b>
   140004adf:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ae3:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004ae6:	85 c0                	test   eax,eax
   140004ae8:	7e 11                	jle    140004afb <__pformat_emit_xfloat+0x18b>
   140004aea:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004aee:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004af1:	8d 50 ff             	lea    edx,[rax-0x1]
   140004af4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004af8:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140004afb:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140004aff:	75 15                	jne    140004b16 <__pformat_emit_xfloat+0x1a6>
   140004b01:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004b05:	48 3b 45 f8          	cmp    rax,QWORD PTR [rbp-0x8]
   140004b09:	72 0b                	jb     140004b16 <__pformat_emit_xfloat+0x1a6>
   140004b0b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b0f:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004b12:	85 c0                	test   eax,eax
   140004b14:	78 32                	js     140004b48 <__pformat_emit_xfloat+0x1d8>
   140004b16:	83 7d e4 09          	cmp    DWORD PTR [rbp-0x1c],0x9
   140004b1a:	76 16                	jbe    140004b32 <__pformat_emit_xfloat+0x1c2>
   140004b1c:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140004b1f:	8d 50 37             	lea    edx,[rax+0x37]
   140004b22:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b26:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004b29:	83 e0 20             	and    eax,0x20
   140004b2c:	09 d0                	or     eax,edx
   140004b2e:	89 c1                	mov    ecx,eax
   140004b30:	eb 08                	jmp    140004b3a <__pformat_emit_xfloat+0x1ca>
   140004b32:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140004b35:	83 c0 30             	add    eax,0x30
   140004b38:	89 c1                	mov    ecx,eax
   140004b3a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004b3e:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004b42:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004b46:	88 08                	mov    BYTE PTR [rax],cl
   140004b48:	48 8b 03             	mov    rax,QWORD PTR [rbx]
   140004b4b:	48 c1 e8 04          	shr    rax,0x4
   140004b4f:	48 89 03             	mov    QWORD PTR [rbx],rax
   140004b52:	83 6d f0 01          	sub    DWORD PTR [rbp-0x10],0x1
   140004b56:	83 7d f0 00          	cmp    DWORD PTR [rbp-0x10],0x0
   140004b5a:	0f 8f 3a ff ff ff    	jg     140004a9a <__pformat_emit_xfloat+0x12a>
   140004b60:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004b64:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
   140004b68:	75 39                	jne    140004ba3 <__pformat_emit_xfloat+0x233>
   140004b6a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b6e:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004b71:	85 c0                	test   eax,eax
   140004b73:	7f 10                	jg     140004b85 <__pformat_emit_xfloat+0x215>
   140004b75:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004b79:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004b7c:	25 00 08 00 00       	and    eax,0x800
   140004b81:	85 c0                	test   eax,eax
   140004b83:	74 0f                	je     140004b94 <__pformat_emit_xfloat+0x224>
   140004b85:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004b89:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004b8d:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004b91:	c6 00 2e             	mov    BYTE PTR [rax],0x2e
   140004b94:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004b98:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140004b9c:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   140004ba0:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140004ba3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ba7:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004baa:	85 c0                	test   eax,eax
   140004bac:	0f 8e e3 00 00 00    	jle    140004c95 <__pformat_emit_xfloat+0x325>
   140004bb2:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004bb6:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140004bba:	48 29 c2             	sub    rdx,rax
   140004bbd:	89 55 ec             	mov    DWORD PTR [rbp-0x14],edx
   140004bc0:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004bc4:	98                   	cwde
   140004bc5:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140004bc8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004bcc:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004bcf:	85 c0                	test   eax,eax
   140004bd1:	7e 0a                	jle    140004bdd <__pformat_emit_xfloat+0x26d>
   140004bd3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004bd7:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004bda:	01 45 ec             	add    DWORD PTR [rbp-0x14],eax
   140004bdd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004be1:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004be4:	25 c0 01 00 00       	and    eax,0x1c0
   140004be9:	85 c0                	test   eax,eax
   140004beb:	74 07                	je     140004bf4 <__pformat_emit_xfloat+0x284>
   140004bed:	b8 06 00 00 00       	mov    eax,0x6
   140004bf2:	eb 05                	jmp    140004bf9 <__pformat_emit_xfloat+0x289>
   140004bf4:	b8 05 00 00 00       	mov    eax,0x5
   140004bf9:	01 45 ec             	add    DWORD PTR [rbp-0x14],eax
   140004bfc:	eb 0f                	jmp    140004c0d <__pformat_emit_xfloat+0x29d>
   140004bfe:	83 45 ec 01          	add    DWORD PTR [rbp-0x14],0x1
   140004c02:	0f b7 45 f6          	movzx  eax,WORD PTR [rbp-0xa]
   140004c06:	83 c0 01             	add    eax,0x1
   140004c09:	66 89 45 f6          	mov    WORD PTR [rbp-0xa],ax
   140004c0d:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140004c10:	48 63 d0             	movsxd rdx,eax
   140004c13:	48 69 d2 67 66 66 66 	imul   rdx,rdx,0x66666667
   140004c1a:	48 c1 ea 20          	shr    rdx,0x20
   140004c1e:	89 d1                	mov    ecx,edx
   140004c20:	c1 f9 02             	sar    ecx,0x2
   140004c23:	99                   	cdq
   140004c24:	89 c8                	mov    eax,ecx
   140004c26:	29 d0                	sub    eax,edx
   140004c28:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140004c2b:	83 7d e8 00          	cmp    DWORD PTR [rbp-0x18],0x0
   140004c2f:	75 cd                	jne    140004bfe <__pformat_emit_xfloat+0x28e>
   140004c31:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c35:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004c38:	39 45 ec             	cmp    DWORD PTR [rbp-0x14],eax
   140004c3b:	7d 4d                	jge    140004c8a <__pformat_emit_xfloat+0x31a>
   140004c3d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c41:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004c44:	2b 45 ec             	sub    eax,DWORD PTR [rbp-0x14]
   140004c47:	89 c2                	mov    edx,eax
   140004c49:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c4d:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004c50:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c54:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004c57:	25 00 06 00 00       	and    eax,0x600
   140004c5c:	85 c0                	test   eax,eax
   140004c5e:	75 35                	jne    140004c95 <__pformat_emit_xfloat+0x325>
   140004c60:	eb 11                	jmp    140004c73 <__pformat_emit_xfloat+0x303>
   140004c62:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c66:	48 89 c2             	mov    rdx,rax
   140004c69:	b9 20 00 00 00       	mov    ecx,0x20
   140004c6e:	e8 bd e4 ff ff       	call   140003130 <__pformat_putc>
   140004c73:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c77:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004c7a:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004c7d:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004c81:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140004c84:	85 c0                	test   eax,eax
   140004c86:	7f da                	jg     140004c62 <__pformat_emit_xfloat+0x2f2>
   140004c88:	eb 0b                	jmp    140004c95 <__pformat_emit_xfloat+0x325>
   140004c8a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c8e:	c7 40 0c ff ff ff ff 	mov    DWORD PTR [rax+0xc],0xffffffff
   140004c95:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004c99:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004c9c:	25 80 00 00 00       	and    eax,0x80
   140004ca1:	85 c0                	test   eax,eax
   140004ca3:	74 13                	je     140004cb8 <__pformat_emit_xfloat+0x348>
   140004ca5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ca9:	48 89 c2             	mov    rdx,rax
   140004cac:	b9 2d 00 00 00       	mov    ecx,0x2d
   140004cb1:	e8 7a e4 ff ff       	call   140003130 <__pformat_putc>
   140004cb6:	eb 42                	jmp    140004cfa <__pformat_emit_xfloat+0x38a>
   140004cb8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cbc:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004cbf:	25 00 01 00 00       	and    eax,0x100
   140004cc4:	85 c0                	test   eax,eax
   140004cc6:	74 13                	je     140004cdb <__pformat_emit_xfloat+0x36b>
   140004cc8:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ccc:	48 89 c2             	mov    rdx,rax
   140004ccf:	b9 2b 00 00 00       	mov    ecx,0x2b
   140004cd4:	e8 57 e4 ff ff       	call   140003130 <__pformat_putc>
   140004cd9:	eb 1f                	jmp    140004cfa <__pformat_emit_xfloat+0x38a>
   140004cdb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cdf:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004ce2:	83 e0 40             	and    eax,0x40
   140004ce5:	85 c0                	test   eax,eax
   140004ce7:	74 11                	je     140004cfa <__pformat_emit_xfloat+0x38a>
   140004ce9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ced:	48 89 c2             	mov    rdx,rax
   140004cf0:	b9 20 00 00 00       	mov    ecx,0x20
   140004cf5:	e8 36 e4 ff ff       	call   140003130 <__pformat_putc>
   140004cfa:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004cfe:	48 89 c2             	mov    rdx,rax
   140004d01:	b9 30 00 00 00       	mov    ecx,0x30
   140004d06:	e8 25 e4 ff ff       	call   140003130 <__pformat_putc>
   140004d0b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d0f:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004d12:	83 e0 20             	and    eax,0x20
   140004d15:	83 c8 58             	or     eax,0x58
   140004d18:	89 c1                	mov    ecx,eax
   140004d1a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d1e:	48 89 c2             	mov    rdx,rax
   140004d21:	e8 0a e4 ff ff       	call   140003130 <__pformat_putc>
   140004d26:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d2a:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004d2d:	85 c0                	test   eax,eax
   140004d2f:	7e 54                	jle    140004d85 <__pformat_emit_xfloat+0x415>
   140004d31:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d35:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004d38:	25 00 02 00 00       	and    eax,0x200
   140004d3d:	85 c0                	test   eax,eax
   140004d3f:	74 44                	je     140004d85 <__pformat_emit_xfloat+0x415>
   140004d41:	eb 11                	jmp    140004d54 <__pformat_emit_xfloat+0x3e4>
   140004d43:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d47:	48 89 c2             	mov    rdx,rax
   140004d4a:	b9 30 00 00 00       	mov    ecx,0x30
   140004d4f:	e8 dc e3 ff ff       	call   140003130 <__pformat_putc>
   140004d54:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d58:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140004d5b:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004d5e:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004d62:	89 4a 0c             	mov    DWORD PTR [rdx+0xc],ecx
   140004d65:	85 c0                	test   eax,eax
   140004d67:	7f da                	jg     140004d43 <__pformat_emit_xfloat+0x3d3>
   140004d69:	eb 1a                	jmp    140004d85 <__pformat_emit_xfloat+0x415>
   140004d6b:	48 83 6d f8 01       	sub    QWORD PTR [rbp-0x8],0x1
   140004d70:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140004d74:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140004d77:	0f be c0             	movsx  eax,al
   140004d7a:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004d7e:	89 c1                	mov    ecx,eax
   140004d80:	e8 32 f2 ff ff       	call   140003fb7 <__pformat_emit_numeric_value>
   140004d85:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004d89:	48 3b 45 f8          	cmp    rax,QWORD PTR [rbp-0x8]
   140004d8d:	72 dc                	jb     140004d6b <__pformat_emit_xfloat+0x3fb>
   140004d8f:	eb 11                	jmp    140004da2 <__pformat_emit_xfloat+0x432>
   140004d91:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004d95:	48 89 c2             	mov    rdx,rax
   140004d98:	b9 30 00 00 00       	mov    ecx,0x30
   140004d9d:	e8 8e e3 ff ff       	call   140003130 <__pformat_putc>
   140004da2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004da6:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140004da9:	8d 48 ff             	lea    ecx,[rax-0x1]
   140004dac:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004db0:	89 4a 10             	mov    DWORD PTR [rdx+0x10],ecx
   140004db3:	85 c0                	test   eax,eax
   140004db5:	7f da                	jg     140004d91 <__pformat_emit_xfloat+0x421>
   140004db7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dbb:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004dbe:	83 e0 20             	and    eax,0x20
   140004dc1:	83 c8 50             	or     eax,0x50
   140004dc4:	89 c1                	mov    ecx,eax
   140004dc6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dca:	48 89 c2             	mov    rdx,rax
   140004dcd:	e8 5e e3 ff ff       	call   140003130 <__pformat_putc>
   140004dd2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dd6:	8b 50 0c             	mov    edx,DWORD PTR [rax+0xc]
   140004dd9:	0f bf 45 f6          	movsx  eax,WORD PTR [rbp-0xa]
   140004ddd:	01 c2                	add    edx,eax
   140004ddf:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004de3:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140004de6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004dea:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004ded:	0d c0 01 00 00       	or     eax,0x1c0
   140004df2:	89 c2                	mov    edx,eax
   140004df4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004df8:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140004dfb:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004dff:	66 85 c0             	test   ax,ax
   140004e02:	79 09                	jns    140004e0d <__pformat_emit_xfloat+0x49d>
   140004e04:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   140004e0b:	eb 05                	jmp    140004e12 <__pformat_emit_xfloat+0x4a2>
   140004e0d:	b8 00 00 00 00       	mov    eax,0x0
   140004e12:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140004e16:	0f b7 43 08          	movzx  eax,WORD PTR [rbx+0x8]
   140004e1a:	48 0f bf c0          	movsx  rax,ax
   140004e1e:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140004e22:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140004e26:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
   140004e2a:	48 89 45 a0          	mov    QWORD PTR [rbp-0x60],rax
   140004e2e:	48 89 55 a8          	mov    QWORD PTR [rbp-0x58],rdx
   140004e32:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004e36:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140004e3a:	48 89 c1             	mov    rcx,rax
   140004e3d:	e8 59 e7 ff ff       	call   14000359b <__pformat_int>
   140004e42:	90                   	nop
   140004e43:	48 81 c4 88 00 00 00 	add    rsp,0x88
   140004e4a:	5b                   	pop    rbx
   140004e4b:	5d                   	pop    rbp
   140004e4c:	c3                   	ret

0000000140004e4d <__pformat_xldouble>:
   140004e4d:	55                   	push   rbp
   140004e4e:	53                   	push   rbx
   140004e4f:	48 83 ec 78          	sub    rsp,0x78
   140004e53:	48 8d 6c 24 70       	lea    rbp,[rsp+0x70]
   140004e58:	48 89 cb             	mov    rbx,rcx
   140004e5b:	db 2b                	fld    TBYTE PTR [rbx]
   140004e5d:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004e60:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140004e64:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140004e6b:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140004e6f:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140004e72:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140004e75:	48 8d 55 c0          	lea    rdx,[rbp-0x40]
   140004e79:	48 89 c1             	mov    rcx,rax
   140004e7c:	e8 e5 ed ff ff       	call   140003c66 <init_fpreg_ldouble>
   140004e81:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140004e84:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140004e87:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004e8b:	48 89 c1             	mov    rcx,rax
   140004e8e:	e8 ed 3d 00 00       	call   140008c80 <__isnanl>
   140004e93:	85 c0                	test   eax,eax
   140004e95:	74 1d                	je     140004eb4 <__pformat_xldouble+0x67>
   140004e97:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004e9a:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004e9e:	48 8d 15 a1 64 00 00 	lea    rdx,[rip+0x64a1]        # 14000b346 <.rdata+0x16>
   140004ea5:	49 89 c8             	mov    r8,rcx
   140004ea8:	89 c1                	mov    ecx,eax
   140004eaa:	e8 75 f1 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   140004eaf:	e9 aa 00 00 00       	jmp    140004f5e <__pformat_xldouble+0x111>
   140004eb4:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004eb8:	98                   	cwde
   140004eb9:	25 00 80 00 00       	and    eax,0x8000
   140004ebe:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004ec1:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140004ec5:	74 12                	je     140004ed9 <__pformat_xldouble+0x8c>
   140004ec7:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ecb:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004ece:	0c 80                	or     al,0x80
   140004ed0:	89 c2                	mov    edx,eax
   140004ed2:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140004ed6:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140004ed9:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140004edc:	db 7d c0             	fstp   TBYTE PTR [rbp-0x40]
   140004edf:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   140004ee3:	48 89 c1             	mov    rcx,rax
   140004ee6:	e8 a5 3c 00 00       	call   140008b90 <__fpclassifyl>
   140004eeb:	3d 00 05 00 00       	cmp    eax,0x500
   140004ef0:	75 1a                	jne    140004f0c <__pformat_xldouble+0xbf>
   140004ef2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004ef5:	48 8b 4d 28          	mov    rcx,QWORD PTR [rbp+0x28]
   140004ef9:	48 8d 15 4a 64 00 00 	lea    rdx,[rip+0x644a]        # 14000b34a <.rdata+0x1a>
   140004f00:	49 89 c8             	mov    r8,rcx
   140004f03:	89 c1                	mov    ecx,eax
   140004f05:	e8 1a f1 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   140004f0a:	eb 52                	jmp    140004f5e <__pformat_xldouble+0x111>
   140004f0c:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004f10:	66 25 ff 7f          	and    ax,0x7fff
   140004f14:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140004f18:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004f1c:	66 85 c0             	test   ax,ax
   140004f1f:	75 11                	jne    140004f32 <__pformat_xldouble+0xe5>
   140004f21:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140004f25:	48 85 c0             	test   rax,rax
   140004f28:	74 14                	je     140004f3e <__pformat_xldouble+0xf1>
   140004f2a:	66 c7 45 e8 02 c0    	mov    WORD PTR [rbp-0x18],0xc002
   140004f30:	eb 0c                	jmp    140004f3e <__pformat_xldouble+0xf1>
   140004f32:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004f36:	66 2d ff 3f          	sub    ax,0x3fff
   140004f3a:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140004f3e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140004f42:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140004f46:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140004f4a:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
   140004f4e:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140004f52:	48 8d 45 b0          	lea    rax,[rbp-0x50]
   140004f56:	48 89 c1             	mov    rcx,rax
   140004f59:	e8 12 fa ff ff       	call   140004970 <__pformat_emit_xfloat>
   140004f5e:	90                   	nop
   140004f5f:	48 83 c4 78          	add    rsp,0x78
   140004f63:	5b                   	pop    rbx
   140004f64:	5d                   	pop    rbp
   140004f65:	c3                   	ret

0000000140004f66 <__pformat_xdouble>:
   140004f66:	55                   	push   rbp
   140004f67:	48 89 e5             	mov    rbp,rsp
   140004f6a:	48 83 ec 60          	sub    rsp,0x60
   140004f6e:	f2 0f 11 45 10       	movsd  QWORD PTR [rbp+0x10],xmm0
   140004f73:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140004f77:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140004f7e:	dd 45 10             	fld    QWORD PTR [rbp+0x10]
   140004f81:	48 8d 45 e0          	lea    rax,[rbp-0x20]
   140004f85:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140004f88:	48 8d 55 d0          	lea    rdx,[rbp-0x30]
   140004f8c:	48 89 c1             	mov    rcx,rax
   140004f8f:	e8 d2 ec ff ff       	call   140003c66 <init_fpreg_ldouble>
   140004f94:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140004f98:	66 48 0f 6e c0       	movq   xmm0,rax
   140004f9d:	e8 7e 3c 00 00       	call   140008c20 <__isnan>
   140004fa2:	85 c0                	test   eax,eax
   140004fa4:	74 1d                	je     140004fc3 <__pformat_xdouble+0x5d>
   140004fa6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140004fa9:	48 8b 4d 18          	mov    rcx,QWORD PTR [rbp+0x18]
   140004fad:	48 8d 15 92 63 00 00 	lea    rdx,[rip+0x6392]        # 14000b346 <.rdata+0x16>
   140004fb4:	49 89 c8             	mov    r8,rcx
   140004fb7:	89 c1                	mov    ecx,eax
   140004fb9:	e8 66 f0 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   140004fbe:	e9 f9 00 00 00       	jmp    1400050bc <__pformat_xdouble+0x156>
   140004fc3:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140004fc7:	98                   	cwde
   140004fc8:	25 00 80 00 00       	and    eax,0x8000
   140004fcd:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140004fd0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140004fd4:	74 12                	je     140004fe8 <__pformat_xdouble+0x82>
   140004fd6:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004fda:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140004fdd:	0c 80                	or     al,0x80
   140004fdf:	89 c2                	mov    edx,eax
   140004fe1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140004fe5:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140004fe8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140004fec:	66 48 0f 6e c0       	movq   xmm0,rax
   140004ff1:	e8 1a 3b 00 00       	call   140008b10 <__fpclassify>
   140004ff6:	3d 00 05 00 00       	cmp    eax,0x500
   140004ffb:	75 1d                	jne    14000501a <__pformat_xdouble+0xb4>
   140004ffd:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005000:	48 8b 4d 18          	mov    rcx,QWORD PTR [rbp+0x18]
   140005004:	48 8d 15 3f 63 00 00 	lea    rdx,[rip+0x633f]        # 14000b34a <.rdata+0x1a>
   14000500b:	49 89 c8             	mov    r8,rcx
   14000500e:	89 c1                	mov    ecx,eax
   140005010:	e8 0f f0 ff ff       	call   140004024 <__pformat_emit_inf_or_nan>
   140005015:	e9 a2 00 00 00       	jmp    1400050bc <__pformat_xdouble+0x156>
   14000501a:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000501e:	66 25 ff 7f          	and    ax,0x7fff
   140005022:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140005026:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000502a:	66 85 c0             	test   ax,ax
   14000502d:	74 3b                	je     14000506a <__pformat_xdouble+0x104>
   14000502f:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140005033:	66 3d 00 3c          	cmp    ax,0x3c00
   140005037:	7f 31                	jg     14000506a <__pformat_xdouble+0x104>
   140005039:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000503d:	98                   	cwde
   14000503e:	ba 01 3c 00 00       	mov    edx,0x3c01
   140005043:	29 c2                	sub    edx,eax
   140005045:	89 55 f8             	mov    DWORD PTR [rbp-0x8],edx
   140005048:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
   14000504c:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   14000504f:	89 c1                	mov    ecx,eax
   140005051:	48 d3 ea             	shr    rdx,cl
   140005054:	48 89 d0             	mov    rax,rdx
   140005057:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000505b:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000505f:	89 c2                	mov    edx,eax
   140005061:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140005064:	01 d0                	add    eax,edx
   140005066:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   14000506a:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   14000506e:	66 85 c0             	test   ax,ax
   140005071:	75 11                	jne    140005084 <__pformat_xdouble+0x11e>
   140005073:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005077:	48 85 c0             	test   rax,rax
   14000507a:	74 14                	je     140005090 <__pformat_xdouble+0x12a>
   14000507c:	66 c7 45 e8 05 fc    	mov    WORD PTR [rbp-0x18],0xfc05
   140005082:	eb 0c                	jmp    140005090 <__pformat_xdouble+0x12a>
   140005084:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140005088:	66 2d fc 3f          	sub    ax,0x3ffc
   14000508c:	66 89 45 e8          	mov    WORD PTR [rbp-0x18],ax
   140005090:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005094:	48 c1 e8 03          	shr    rax,0x3
   140005098:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000509c:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400050a0:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   1400050a4:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   1400050a8:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
   1400050ac:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400050b0:	48 8d 45 c0          	lea    rax,[rbp-0x40]
   1400050b4:	48 89 c1             	mov    rcx,rax
   1400050b7:	e8 b4 f8 ff ff       	call   140004970 <__pformat_emit_xfloat>
   1400050bc:	90                   	nop
   1400050bd:	48 83 c4 60          	add    rsp,0x60
   1400050c1:	5d                   	pop    rbp
   1400050c2:	c3                   	ret

00000001400050c3 <__mingw_pformat>:
   1400050c3:	55                   	push   rbp
   1400050c4:	48 89 e5             	mov    rbp,rsp
   1400050c7:	48 81 ec d0 00 00 00 	sub    rsp,0xd0
   1400050ce:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   1400050d1:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400050d5:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   1400050d9:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   1400050dd:	e8 a6 44 00 00       	call   140009588 <_errno>
   1400050e2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400050e4:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   1400050e7:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400050eb:	48 89 45 a0          	mov    QWORD PTR [rbp-0x60],rax
   1400050ef:	81 65 10 00 60 00 00 	and    DWORD PTR [rbp+0x10],0x6000
   1400050f6:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   1400050f9:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400050fc:	c7 45 ac ff ff ff ff 	mov    DWORD PTR [rbp-0x54],0xffffffff
   140005103:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   14000510a:	c7 45 b4 fd ff ff ff 	mov    DWORD PTR [rbp-0x4c],0xfffffffd
   140005111:	66 c7 45 b8 00 00    	mov    WORD PTR [rbp-0x48],0x0
   140005117:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
   14000511e:	66 c7 45 c0 00 00    	mov    WORD PTR [rbp-0x40],0x0
   140005124:	c7 45 c4 00 00 00 00 	mov    DWORD PTR [rbp-0x3c],0x0
   14000512b:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   14000512e:	89 45 c8             	mov    DWORD PTR [rbp-0x38],eax
   140005131:	c7 45 cc ff ff ff ff 	mov    DWORD PTR [rbp-0x34],0xffffffff
   140005138:	e9 27 0c 00 00       	jmp    140005d64 <__mingw_pformat+0xca1>
   14000513d:	83 7d e8 25          	cmp    DWORD PTR [rbp-0x18],0x25
   140005141:	0f 85 0f 0c 00 00    	jne    140005d56 <__mingw_pformat+0xc93>
   140005147:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   14000514e:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140005155:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005159:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000515d:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005161:	48 83 c0 0c          	add    rax,0xc
   140005165:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005169:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   14000516c:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   14000516f:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   140005176:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140005179:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000517c:	e9 c4 0b 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005181:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005185:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140005189:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   14000518d:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005190:	0f be c0             	movsx  eax,al
   140005193:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140005196:	83 7d e8 7a          	cmp    DWORD PTR [rbp-0x18],0x7a
   14000519a:	0f 84 94 09 00 00    	je     140005b34 <__mingw_pformat+0xa71>
   1400051a0:	83 7d e8 7a          	cmp    DWORD PTR [rbp-0x18],0x7a
   1400051a4:	0f 8f 02 0b 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400051aa:	83 7d e8 78          	cmp    DWORD PTR [rbp-0x18],0x78
   1400051ae:	0f 84 eb 03 00 00    	je     14000559f <__mingw_pformat+0x4dc>
   1400051b4:	83 7d e8 78          	cmp    DWORD PTR [rbp-0x18],0x78
   1400051b8:	0f 8f ee 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400051be:	83 7d e8 77          	cmp    DWORD PTR [rbp-0x18],0x77
   1400051c2:	0f 84 31 09 00 00    	je     140005af9 <__mingw_pformat+0xa36>
   1400051c8:	83 7d e8 77          	cmp    DWORD PTR [rbp-0x18],0x77
   1400051cc:	0f 8f da 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400051d2:	83 7d e8 75          	cmp    DWORD PTR [rbp-0x18],0x75
   1400051d6:	0f 84 c3 03 00 00    	je     14000559f <__mingw_pformat+0x4dc>
   1400051dc:	83 7d e8 75          	cmp    DWORD PTR [rbp-0x18],0x75
   1400051e0:	0f 8f c6 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400051e6:	83 7d e8 74          	cmp    DWORD PTR [rbp-0x18],0x74
   1400051ea:	0f 84 31 09 00 00    	je     140005b21 <__mingw_pformat+0xa5e>
   1400051f0:	83 7d e8 74          	cmp    DWORD PTR [rbp-0x18],0x74
   1400051f4:	0f 8f b2 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400051fa:	83 7d e8 73          	cmp    DWORD PTR [rbp-0x18],0x73
   1400051fe:	0f 84 31 03 00 00    	je     140005535 <__mingw_pformat+0x472>
   140005204:	83 7d e8 73          	cmp    DWORD PTR [rbp-0x18],0x73
   140005208:	0f 8f 9e 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000520e:	83 7d e8 70          	cmp    DWORD PTR [rbp-0x18],0x70
   140005212:	0f 84 28 05 00 00    	je     140005740 <__mingw_pformat+0x67d>
   140005218:	83 7d e8 70          	cmp    DWORD PTR [rbp-0x18],0x70
   14000521c:	0f 8f 8a 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005222:	83 7d e8 6f          	cmp    DWORD PTR [rbp-0x18],0x6f
   140005226:	0f 84 73 03 00 00    	je     14000559f <__mingw_pformat+0x4dc>
   14000522c:	83 7d e8 6f          	cmp    DWORD PTR [rbp-0x18],0x6f
   140005230:	0f 8f 76 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005236:	83 7d e8 6e          	cmp    DWORD PTR [rbp-0x18],0x6e
   14000523a:	0f 84 4d 07 00 00    	je     14000598d <__mingw_pformat+0x8ca>
   140005240:	83 7d e8 6e          	cmp    DWORD PTR [rbp-0x18],0x6e
   140005244:	0f 8f 62 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000524a:	83 7d e8 6d          	cmp    DWORD PTR [rbp-0x18],0x6d
   14000524e:	0f 84 2d 03 00 00    	je     140005581 <__mingw_pformat+0x4be>
   140005254:	83 7d e8 6d          	cmp    DWORD PTR [rbp-0x18],0x6d
   140005258:	0f 8f 4e 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000525e:	83 7d e8 6c          	cmp    DWORD PTR [rbp-0x18],0x6c
   140005262:	0f 84 65 08 00 00    	je     140005acd <__mingw_pformat+0xa0a>
   140005268:	83 7d e8 6c          	cmp    DWORD PTR [rbp-0x18],0x6c
   14000526c:	0f 8f 3a 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005272:	83 7d e8 6a          	cmp    DWORD PTR [rbp-0x18],0x6a
   140005276:	0f 84 db 07 00 00    	je     140005a57 <__mingw_pformat+0x994>
   14000527c:	83 7d e8 6a          	cmp    DWORD PTR [rbp-0x18],0x6a
   140005280:	0f 8f 26 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005286:	83 7d e8 69          	cmp    DWORD PTR [rbp-0x18],0x69
   14000528a:	0f 84 ee 03 00 00    	je     14000567e <__mingw_pformat+0x5bb>
   140005290:	83 7d e8 69          	cmp    DWORD PTR [rbp-0x18],0x69
   140005294:	0f 8f 12 0a 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000529a:	83 7d e8 68          	cmp    DWORD PTR [rbp-0x18],0x68
   14000529e:	0f 84 87 07 00 00    	je     140005a2b <__mingw_pformat+0x968>
   1400052a4:	83 7d e8 68          	cmp    DWORD PTR [rbp-0x18],0x68
   1400052a8:	0f 8f fe 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400052ae:	83 7d e8 67          	cmp    DWORD PTR [rbp-0x18],0x67
   1400052b2:	0f 84 f3 05 00 00    	je     1400058ab <__mingw_pformat+0x7e8>
   1400052b8:	83 7d e8 67          	cmp    DWORD PTR [rbp-0x18],0x67
   1400052bc:	0f 8f ea 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400052c2:	83 7d e8 66          	cmp    DWORD PTR [rbp-0x18],0x66
   1400052c6:	0f 84 61 05 00 00    	je     14000582d <__mingw_pformat+0x76a>
   1400052cc:	83 7d e8 66          	cmp    DWORD PTR [rbp-0x18],0x66
   1400052d0:	0f 8f d6 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400052d6:	83 7d e8 65          	cmp    DWORD PTR [rbp-0x18],0x65
   1400052da:	0f 84 cf 04 00 00    	je     1400057af <__mingw_pformat+0x6ec>
   1400052e0:	83 7d e8 65          	cmp    DWORD PTR [rbp-0x18],0x65
   1400052e4:	0f 8f c2 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400052ea:	83 7d e8 64          	cmp    DWORD PTR [rbp-0x18],0x64
   1400052ee:	0f 84 8a 03 00 00    	je     14000567e <__mingw_pformat+0x5bb>
   1400052f4:	83 7d e8 64          	cmp    DWORD PTR [rbp-0x18],0x64
   1400052f8:	0f 8f ae 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400052fe:	83 7d e8 63          	cmp    DWORD PTR [rbp-0x18],0x63
   140005302:	0f 84 b5 01 00 00    	je     1400054bd <__mingw_pformat+0x3fa>
   140005308:	83 7d e8 63          	cmp    DWORD PTR [rbp-0x18],0x63
   14000530c:	0f 8f 9a 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005312:	83 7d e8 62          	cmp    DWORD PTR [rbp-0x18],0x62
   140005316:	0f 84 83 02 00 00    	je     14000559f <__mingw_pformat+0x4dc>
   14000531c:	83 7d e8 62          	cmp    DWORD PTR [rbp-0x18],0x62
   140005320:	0f 8f 86 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005326:	83 7d e8 61          	cmp    DWORD PTR [rbp-0x18],0x61
   14000532a:	0f 84 f9 05 00 00    	je     140005929 <__mingw_pformat+0x866>
   140005330:	83 7d e8 61          	cmp    DWORD PTR [rbp-0x18],0x61
   140005334:	0f 8f 72 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000533a:	83 7d e8 58          	cmp    DWORD PTR [rbp-0x18],0x58
   14000533e:	0f 84 5b 02 00 00    	je     14000559f <__mingw_pformat+0x4dc>
   140005344:	83 7d e8 58          	cmp    DWORD PTR [rbp-0x18],0x58
   140005348:	0f 8f 5e 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000534e:	83 7d e8 53          	cmp    DWORD PTR [rbp-0x18],0x53
   140005352:	0f 84 d6 01 00 00    	je     14000552e <__mingw_pformat+0x46b>
   140005358:	83 7d e8 53          	cmp    DWORD PTR [rbp-0x18],0x53
   14000535c:	0f 8f 4a 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005362:	83 7d e8 4c          	cmp    DWORD PTR [rbp-0x18],0x4c
   140005366:	0f 84 a0 07 00 00    	je     140005b0c <__mingw_pformat+0xa49>
   14000536c:	83 7d e8 4c          	cmp    DWORD PTR [rbp-0x18],0x4c
   140005370:	0f 8f 36 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005376:	83 7d e8 49          	cmp    DWORD PTR [rbp-0x18],0x49
   14000537a:	0f 84 ea 06 00 00    	je     140005a6a <__mingw_pformat+0x9a7>
   140005380:	83 7d e8 49          	cmp    DWORD PTR [rbp-0x18],0x49
   140005384:	0f 8f 22 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000538a:	83 7d e8 47          	cmp    DWORD PTR [rbp-0x18],0x47
   14000538e:	0f 84 20 05 00 00    	je     1400058b4 <__mingw_pformat+0x7f1>
   140005394:	83 7d e8 47          	cmp    DWORD PTR [rbp-0x18],0x47
   140005398:	0f 8f 0e 09 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000539e:	83 7d e8 46          	cmp    DWORD PTR [rbp-0x18],0x46
   1400053a2:	0f 84 8e 04 00 00    	je     140005836 <__mingw_pformat+0x773>
   1400053a8:	83 7d e8 46          	cmp    DWORD PTR [rbp-0x18],0x46
   1400053ac:	0f 8f fa 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400053b2:	83 7d e8 45          	cmp    DWORD PTR [rbp-0x18],0x45
   1400053b6:	0f 84 fc 03 00 00    	je     1400057b8 <__mingw_pformat+0x6f5>
   1400053bc:	83 7d e8 45          	cmp    DWORD PTR [rbp-0x18],0x45
   1400053c0:	0f 8f e6 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400053c6:	83 7d e8 43          	cmp    DWORD PTR [rbp-0x18],0x43
   1400053ca:	0f 84 e6 00 00 00    	je     1400054b6 <__mingw_pformat+0x3f3>
   1400053d0:	83 7d e8 43          	cmp    DWORD PTR [rbp-0x18],0x43
   1400053d4:	0f 8f d2 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400053da:	83 7d e8 42          	cmp    DWORD PTR [rbp-0x18],0x42
   1400053de:	0f 84 bb 01 00 00    	je     14000559f <__mingw_pformat+0x4dc>
   1400053e4:	83 7d e8 42          	cmp    DWORD PTR [rbp-0x18],0x42
   1400053e8:	0f 8f be 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   1400053ee:	83 7d e8 41          	cmp    DWORD PTR [rbp-0x18],0x41
   1400053f2:	0f 84 3a 05 00 00    	je     140005932 <__mingw_pformat+0x86f>
   1400053f8:	83 7d e8 41          	cmp    DWORD PTR [rbp-0x18],0x41
   1400053fc:	0f 8f aa 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005402:	83 7d e8 30          	cmp    DWORD PTR [rbp-0x18],0x30
   140005406:	0f 84 8c 08 00 00    	je     140005c98 <__mingw_pformat+0xbd5>
   14000540c:	83 7d e8 30          	cmp    DWORD PTR [rbp-0x18],0x30
   140005410:	0f 8f 96 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005416:	83 7d e8 2e          	cmp    DWORD PTR [rbp-0x18],0x2e
   14000541a:	0f 84 27 07 00 00    	je     140005b47 <__mingw_pformat+0xa84>
   140005420:	83 7d e8 2e          	cmp    DWORD PTR [rbp-0x18],0x2e
   140005424:	0f 8f 82 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000542a:	83 7d e8 2d          	cmp    DWORD PTR [rbp-0x18],0x2d
   14000542e:	0f 84 db 07 00 00    	je     140005c0f <__mingw_pformat+0xb4c>
   140005434:	83 7d e8 2d          	cmp    DWORD PTR [rbp-0x18],0x2d
   140005438:	0f 8f 6e 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000543e:	83 7d e8 2b          	cmp    DWORD PTR [rbp-0x18],0x2b
   140005442:	0f 84 af 07 00 00    	je     140005bf7 <__mingw_pformat+0xb34>
   140005448:	83 7d e8 2b          	cmp    DWORD PTR [rbp-0x18],0x2b
   14000544c:	0f 8f 5a 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005452:	83 7d e8 2a          	cmp    DWORD PTR [rbp-0x18],0x2a
   140005456:	0f 84 1c 07 00 00    	je     140005b78 <__mingw_pformat+0xab5>
   14000545c:	83 7d e8 2a          	cmp    DWORD PTR [rbp-0x18],0x2a
   140005460:	0f 8f 46 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   140005466:	83 7d e8 27          	cmp    DWORD PTR [rbp-0x18],0x27
   14000546a:	0f 84 b7 07 00 00    	je     140005c27 <__mingw_pformat+0xb64>
   140005470:	83 7d e8 27          	cmp    DWORD PTR [rbp-0x18],0x27
   140005474:	0f 8f 32 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000547a:	83 7d e8 25          	cmp    DWORD PTR [rbp-0x18],0x25
   14000547e:	74 23                	je     1400054a3 <__mingw_pformat+0x3e0>
   140005480:	83 7d e8 25          	cmp    DWORD PTR [rbp-0x18],0x25
   140005484:	0f 8f 22 08 00 00    	jg     140005cac <__mingw_pformat+0xbe9>
   14000548a:	83 7d e8 20          	cmp    DWORD PTR [rbp-0x18],0x20
   14000548e:	0f 84 ec 07 00 00    	je     140005c80 <__mingw_pformat+0xbbd>
   140005494:	83 7d e8 23          	cmp    DWORD PTR [rbp-0x18],0x23
   140005498:	0f 84 41 07 00 00    	je     140005bdf <__mingw_pformat+0xb1c>
   14000549e:	e9 09 08 00 00       	jmp    140005cac <__mingw_pformat+0xbe9>
   1400054a3:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400054a7:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   1400054aa:	89 c1                	mov    ecx,eax
   1400054ac:	e8 7f dc ff ff       	call   140003130 <__pformat_putc>
   1400054b1:	e9 82 fc ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400054b6:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   1400054bd:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   1400054c4:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400054c8:	74 06                	je     1400054d0 <__mingw_pformat+0x40d>
   1400054ca:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   1400054ce:	75 30                	jne    140005500 <__mingw_pformat+0x43d>
   1400054d0:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400054d4:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400054d8:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400054dc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400054de:	66 89 45 8e          	mov    WORD PTR [rbp-0x72],ax
   1400054e2:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400054e6:	48 8d 45 8e          	lea    rax,[rbp-0x72]
   1400054ea:	49 89 d0             	mov    r8,rdx
   1400054ed:	ba 01 00 00 00       	mov    edx,0x1
   1400054f2:	48 89 c1             	mov    rcx,rax
   1400054f5:	e8 3f de ff ff       	call   140003339 <__pformat_wputchars>
   1400054fa:	90                   	nop
   1400054fb:	e9 38 fc ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005500:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005504:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005508:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000550c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000550e:	88 45 90             	mov    BYTE PTR [rbp-0x70],al
   140005511:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005515:	48 8d 45 90          	lea    rax,[rbp-0x70]
   140005519:	49 89 d0             	mov    r8,rdx
   14000551c:	ba 01 00 00 00       	mov    edx,0x1
   140005521:	48 89 c1             	mov    rcx,rax
   140005524:	e8 8b dc ff ff       	call   1400031b4 <__pformat_putchars>
   140005529:	e9 0a fc ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000552e:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005535:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140005539:	74 06                	je     140005541 <__mingw_pformat+0x47e>
   14000553b:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   14000553f:	75 20                	jne    140005561 <__mingw_pformat+0x49e>
   140005541:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005545:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005549:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000554d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005550:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005554:	48 89 c1             	mov    rcx,rax
   140005557:	e8 29 df ff ff       	call   140003485 <__pformat_wcputs>
   14000555c:	e9 d7 fb ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005561:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005565:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005569:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000556d:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005570:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005574:	48 89 c1             	mov    rcx,rax
   140005577:	e8 37 dd ff ff       	call   1400032b3 <__pformat_puts>
   14000557c:	e9 b7 fb ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005581:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   140005584:	89 c1                	mov    ecx,eax
   140005586:	e8 85 40 00 00       	call   140009610 <strerror>
   14000558b:	48 89 c1             	mov    rcx,rax
   14000558e:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005592:	48 89 c2             	mov    rdx,rax
   140005595:	e8 19 dd ff ff       	call   1400032b3 <__pformat_puts>
   14000559a:	e9 99 fb ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000559f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400055a2:	80 e4 fe             	and    ah,0xfe
   1400055a5:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400055a8:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   1400055ac:	75 15                	jne    1400055c3 <__mingw_pformat+0x500>
   1400055ae:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400055b2:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400055b6:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400055ba:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400055bd:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055c1:	eb 54                	jmp    140005617 <__mingw_pformat+0x554>
   1400055c3:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400055c7:	75 16                	jne    1400055df <__mingw_pformat+0x51c>
   1400055c9:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400055cd:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400055d1:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400055d5:	8b 00                	mov    eax,DWORD PTR [rax]
   1400055d7:	89 c0                	mov    eax,eax
   1400055d9:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055dd:	eb 38                	jmp    140005617 <__mingw_pformat+0x554>
   1400055df:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400055e3:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400055e7:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400055eb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400055ed:	89 c0                	mov    eax,eax
   1400055ef:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400055f3:	83 7d f8 01          	cmp    DWORD PTR [rbp-0x8],0x1
   1400055f7:	75 0d                	jne    140005606 <__mingw_pformat+0x543>
   1400055f9:	0f b7 45 90          	movzx  eax,WORD PTR [rbp-0x70]
   1400055fd:	0f b7 c0             	movzx  eax,ax
   140005600:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   140005604:	eb 11                	jmp    140005617 <__mingw_pformat+0x554>
   140005606:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
   14000560a:	75 0b                	jne    140005617 <__mingw_pformat+0x554>
   14000560c:	0f b6 45 90          	movzx  eax,BYTE PTR [rbp-0x70]
   140005610:	0f b6 c0             	movzx  eax,al
   140005613:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   140005617:	83 7d e8 75          	cmp    DWORD PTR [rbp-0x18],0x75
   14000561b:	75 2e                	jne    14000564b <__mingw_pformat+0x588>
   14000561d:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   140005621:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140005625:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   14000562c:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   140005633:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005637:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
   14000563e:	48 89 c1             	mov    rcx,rax
   140005641:	e8 55 df ff ff       	call   14000359b <__pformat_int>
   140005646:	e9 ed fa ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000564b:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   14000564f:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140005653:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   14000565a:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   140005661:	48 8d 4d a0          	lea    rcx,[rbp-0x60]
   140005665:	48 8d 95 70 ff ff ff 	lea    rdx,[rbp-0x90]
   14000566c:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   14000566f:	49 89 c8             	mov    r8,rcx
   140005672:	89 c1                	mov    ecx,eax
   140005674:	e8 a5 e2 ff ff       	call   14000391e <__pformat_xint>
   140005679:	e9 ba fa ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000567e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005681:	0c 80                	or     al,0x80
   140005683:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005686:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   14000568a:	75 15                	jne    1400056a1 <__mingw_pformat+0x5de>
   14000568c:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005690:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005694:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005698:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000569b:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   14000569f:	eb 56                	jmp    1400056f7 <__mingw_pformat+0x634>
   1400056a1:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400056a5:	75 16                	jne    1400056bd <__mingw_pformat+0x5fa>
   1400056a7:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400056ab:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400056af:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400056b3:	8b 00                	mov    eax,DWORD PTR [rax]
   1400056b5:	48 98                	cdqe
   1400056b7:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056bb:	eb 3a                	jmp    1400056f7 <__mingw_pformat+0x634>
   1400056bd:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400056c1:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400056c5:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400056c9:	8b 00                	mov    eax,DWORD PTR [rax]
   1400056cb:	48 98                	cdqe
   1400056cd:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056d1:	83 7d f8 01          	cmp    DWORD PTR [rbp-0x8],0x1
   1400056d5:	75 0e                	jne    1400056e5 <__mingw_pformat+0x622>
   1400056d7:	0f b7 45 90          	movzx  eax,WORD PTR [rbp-0x70]
   1400056db:	48 0f bf c0          	movsx  rax,ax
   1400056df:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056e3:	eb 12                	jmp    1400056f7 <__mingw_pformat+0x634>
   1400056e5:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
   1400056e9:	75 0c                	jne    1400056f7 <__mingw_pformat+0x634>
   1400056eb:	0f b6 45 90          	movzx  eax,BYTE PTR [rbp-0x70]
   1400056ef:	48 0f be c0          	movsx  rax,al
   1400056f3:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   1400056f7:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   1400056fb:	48 85 c0             	test   rax,rax
   1400056fe:	79 09                	jns    140005709 <__mingw_pformat+0x646>
   140005700:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   140005707:	eb 05                	jmp    14000570e <__mingw_pformat+0x64b>
   140005709:	b8 00 00 00 00       	mov    eax,0x0
   14000570e:	48 89 45 98          	mov    QWORD PTR [rbp-0x68],rax
   140005712:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   140005716:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   14000571a:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   140005721:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   140005728:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   14000572c:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
   140005733:	48 89 c1             	mov    rcx,rax
   140005736:	e8 60 de ff ff       	call   14000359b <__pformat_int>
   14000573b:	e9 f8 f9 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005740:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005744:	75 18                	jne    14000575e <__mingw_pformat+0x69b>
   140005746:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005749:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   14000574c:	75 10                	jne    14000575e <__mingw_pformat+0x69b>
   14000574e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005751:	80 cc 02             	or     ah,0x2
   140005754:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005757:	c7 45 b0 10 00 00 00 	mov    DWORD PTR [rbp-0x50],0x10
   14000575e:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005762:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005766:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000576a:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000576d:	48 89 45 90          	mov    QWORD PTR [rbp-0x70],rax
   140005771:	48 c7 45 98 00 00 00 	mov    QWORD PTR [rbp-0x68],0x0
   140005778:	00 
   140005779:	48 8b 45 90          	mov    rax,QWORD PTR [rbp-0x70]
   14000577d:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140005781:	48 89 85 70 ff ff ff 	mov    QWORD PTR [rbp-0x90],rax
   140005788:	48 89 95 78 ff ff ff 	mov    QWORD PTR [rbp-0x88],rdx
   14000578f:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005793:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
   14000579a:	49 89 d0             	mov    r8,rdx
   14000579d:	48 89 c2             	mov    rdx,rax
   1400057a0:	b9 78 00 00 00       	mov    ecx,0x78
   1400057a5:	e8 74 e1 ff ff       	call   14000391e <__pformat_xint>
   1400057aa:	e9 89 f9 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400057af:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400057b2:	83 c8 20             	or     eax,0x20
   1400057b5:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400057b8:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400057bb:	83 e0 04             	and    eax,0x4
   1400057be:	85 c0                	test   eax,eax
   1400057c0:	74 2f                	je     1400057f1 <__mingw_pformat+0x72e>
   1400057c2:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400057c6:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400057ca:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400057ce:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400057d1:	db 28                	fld    TBYTE PTR [rax]
   1400057d3:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   1400057d9:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400057dd:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   1400057e4:	48 89 c1             	mov    rcx,rax
   1400057e7:	e8 1d ef ff ff       	call   140004709 <__pformat_efloat>
   1400057ec:	e9 47 f9 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400057f1:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400057f5:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400057f9:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400057fd:	f2 0f 10 08          	movsd  xmm1,QWORD PTR [rax]
   140005801:	f2 0f 11 8d 58 ff ff 	movsd  QWORD PTR [rbp-0xa8],xmm1
   140005808:	ff 
   140005809:	dd 85 58 ff ff ff    	fld    QWORD PTR [rbp-0xa8]
   14000580f:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005815:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005819:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   140005820:	48 89 c1             	mov    rcx,rax
   140005823:	e8 e1 ee ff ff       	call   140004709 <__pformat_efloat>
   140005828:	e9 0b f9 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000582d:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005830:	83 c8 20             	or     eax,0x20
   140005833:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005836:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005839:	83 e0 04             	and    eax,0x4
   14000583c:	85 c0                	test   eax,eax
   14000583e:	74 2f                	je     14000586f <__mingw_pformat+0x7ac>
   140005840:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005844:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005848:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000584c:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000584f:	db 28                	fld    TBYTE PTR [rax]
   140005851:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005857:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   14000585b:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   140005862:	48 89 c1             	mov    rcx,rax
   140005865:	e8 cf ed ff ff       	call   140004639 <__pformat_float>
   14000586a:	e9 c9 f8 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000586f:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005873:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005877:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   14000587b:	f2 0f 10 10          	movsd  xmm2,QWORD PTR [rax]
   14000587f:	f2 0f 11 95 58 ff ff 	movsd  QWORD PTR [rbp-0xa8],xmm2
   140005886:	ff 
   140005887:	dd 85 58 ff ff ff    	fld    QWORD PTR [rbp-0xa8]
   14000588d:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005893:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005897:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   14000589e:	48 89 c1             	mov    rcx,rax
   1400058a1:	e8 93 ed ff ff       	call   140004639 <__pformat_float>
   1400058a6:	e9 8d f8 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400058ab:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400058ae:	83 c8 20             	or     eax,0x20
   1400058b1:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   1400058b4:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   1400058b7:	83 e0 04             	and    eax,0x4
   1400058ba:	85 c0                	test   eax,eax
   1400058bc:	74 2f                	je     1400058ed <__mingw_pformat+0x82a>
   1400058be:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400058c2:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400058c6:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400058ca:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400058cd:	db 28                	fld    TBYTE PTR [rax]
   1400058cf:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   1400058d5:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   1400058d9:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   1400058e0:	48 89 c1             	mov    rcx,rax
   1400058e3:	e8 cc ee ff ff       	call   1400047b4 <__pformat_gfloat>
   1400058e8:	e9 4b f8 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400058ed:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400058f1:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400058f5:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400058f9:	f2 0f 10 18          	movsd  xmm3,QWORD PTR [rax]
   1400058fd:	f2 0f 11 9d 58 ff ff 	movsd  QWORD PTR [rbp-0xa8],xmm3
   140005904:	ff 
   140005905:	dd 85 58 ff ff ff    	fld    QWORD PTR [rbp-0xa8]
   14000590b:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005911:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005915:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   14000591c:	48 89 c1             	mov    rcx,rax
   14000591f:	e8 90 ee ff ff       	call   1400047b4 <__pformat_gfloat>
   140005924:	e9 0f f8 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005929:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   14000592c:	83 c8 20             	or     eax,0x20
   14000592f:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005932:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005935:	83 e0 04             	and    eax,0x4
   140005938:	85 c0                	test   eax,eax
   14000593a:	74 2f                	je     14000596b <__mingw_pformat+0x8a8>
   14000593c:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005940:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005944:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005948:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000594b:	db 28                	fld    TBYTE PTR [rax]
   14000594d:	db bd 60 ff ff ff    	fstp   TBYTE PTR [rbp-0xa0]
   140005953:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005957:	48 8d 85 60 ff ff ff 	lea    rax,[rbp-0xa0]
   14000595e:	48 89 c1             	mov    rcx,rax
   140005961:	e8 e7 f4 ff ff       	call   140004e4d <__pformat_xldouble>
   140005966:	e9 cd f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000596b:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000596f:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005973:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005977:	48 8b 00             	mov    rax,QWORD PTR [rax]
   14000597a:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   14000597e:	66 48 0f 6e c0       	movq   xmm0,rax
   140005983:	e8 de f5 ff ff       	call   140004f66 <__pformat_xdouble>
   140005988:	e9 ab f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   14000598d:	83 7d f8 05          	cmp    DWORD PTR [rbp-0x8],0x5
   140005991:	75 1b                	jne    1400059ae <__mingw_pformat+0x8eb>
   140005993:	8b 4d c4             	mov    ecx,DWORD PTR [rbp-0x3c]
   140005996:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000599a:	48 8d 50 08          	lea    rdx,[rax+0x8]
   14000599e:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400059a2:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400059a5:	89 ca                	mov    edx,ecx
   1400059a7:	88 10                	mov    BYTE PTR [rax],dl
   1400059a9:	e9 8a f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400059ae:	83 7d f8 01          	cmp    DWORD PTR [rbp-0x8],0x1
   1400059b2:	75 1c                	jne    1400059d0 <__mingw_pformat+0x90d>
   1400059b4:	8b 4d c4             	mov    ecx,DWORD PTR [rbp-0x3c]
   1400059b7:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400059bb:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400059bf:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400059c3:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400059c6:	89 ca                	mov    edx,ecx
   1400059c8:	66 89 10             	mov    WORD PTR [rax],dx
   1400059cb:	e9 68 f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400059d0:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   1400059d4:	75 19                	jne    1400059ef <__mingw_pformat+0x92c>
   1400059d6:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400059da:	48 8d 50 08          	lea    rdx,[rax+0x8]
   1400059de:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   1400059e2:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400059e5:	8b 55 c4             	mov    edx,DWORD PTR [rbp-0x3c]
   1400059e8:	89 10                	mov    DWORD PTR [rax],edx
   1400059ea:	e9 49 f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   1400059ef:	83 7d f8 03          	cmp    DWORD PTR [rbp-0x8],0x3
   1400059f3:	75 1d                	jne    140005a12 <__mingw_pformat+0x94f>
   1400059f5:	8b 4d c4             	mov    ecx,DWORD PTR [rbp-0x3c]
   1400059f8:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400059fc:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005a00:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005a04:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005a07:	48 63 d1             	movsxd rdx,ecx
   140005a0a:	48 89 10             	mov    QWORD PTR [rax],rdx
   140005a0d:	e9 26 f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005a12:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005a16:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005a1a:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005a1e:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140005a21:	8b 55 c4             	mov    edx,DWORD PTR [rbp-0x3c]
   140005a24:	89 10                	mov    DWORD PTR [rax],edx
   140005a26:	e9 0d f7 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005a2b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a2f:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a32:	3c 68                	cmp    al,0x68
   140005a34:	75 0e                	jne    140005a44 <__mingw_pformat+0x981>
   140005a36:	48 83 45 28 01       	add    QWORD PTR [rbp+0x28],0x1
   140005a3b:	c7 45 f8 05 00 00 00 	mov    DWORD PTR [rbp-0x8],0x5
   140005a42:	eb 07                	jmp    140005a4b <__mingw_pformat+0x988>
   140005a44:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   140005a4b:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005a52:	e9 ee 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005a57:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005a5e:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005a65:	e9 db 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005a6a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a6e:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a71:	3c 36                	cmp    al,0x36
   140005a73:	75 1d                	jne    140005a92 <__mingw_pformat+0x9cf>
   140005a75:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a79:	48 83 c0 01          	add    rax,0x1
   140005a7d:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a80:	3c 34                	cmp    al,0x34
   140005a82:	75 0e                	jne    140005a92 <__mingw_pformat+0x9cf>
   140005a84:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005a8b:	48 83 45 28 02       	add    QWORD PTR [rbp+0x28],0x2
   140005a90:	eb 2f                	jmp    140005ac1 <__mingw_pformat+0x9fe>
   140005a92:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005a96:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005a99:	3c 33                	cmp    al,0x33
   140005a9b:	75 1d                	jne    140005aba <__mingw_pformat+0x9f7>
   140005a9d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005aa1:	48 83 c0 01          	add    rax,0x1
   140005aa5:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005aa8:	3c 32                	cmp    al,0x32
   140005aaa:	75 0e                	jne    140005aba <__mingw_pformat+0x9f7>
   140005aac:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005ab3:	48 83 45 28 02       	add    QWORD PTR [rbp+0x28],0x2
   140005ab8:	eb 07                	jmp    140005ac1 <__mingw_pformat+0x9fe>
   140005aba:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005ac1:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005ac8:	e9 78 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005acd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005ad1:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005ad4:	3c 6c                	cmp    al,0x6c
   140005ad6:	75 0e                	jne    140005ae6 <__mingw_pformat+0xa23>
   140005ad8:	48 83 45 28 01       	add    QWORD PTR [rbp+0x28],0x1
   140005add:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005ae4:	eb 07                	jmp    140005aed <__mingw_pformat+0xa2a>
   140005ae6:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005aed:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005af4:	e9 4c 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005af9:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140005b00:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b07:	e9 39 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005b0c:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005b0f:	83 c8 04             	or     eax,0x4
   140005b12:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005b15:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b1c:	e9 24 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005b21:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005b28:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b2f:	e9 11 02 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005b34:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [rbp-0x8],0x3
   140005b3b:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b42:	e9 fe 01 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005b47:	83 7d fc 01          	cmp    DWORD PTR [rbp-0x4],0x1
   140005b4b:	77 1f                	ja     140005b6c <__mingw_pformat+0xaa9>
   140005b4d:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   140005b54:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005b58:	48 83 c0 10          	add    rax,0x10
   140005b5c:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005b60:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
   140005b67:	e9 d9 01 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005b6c:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005b73:	e9 cd 01 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005b78:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140005b7d:	74 4c                	je     140005bcb <__mingw_pformat+0xb08>
   140005b7f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005b83:	74 06                	je     140005b8b <__mingw_pformat+0xac8>
   140005b85:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
   140005b89:	75 40                	jne    140005bcb <__mingw_pformat+0xb08>
   140005b8b:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140005b8f:	48 8d 50 08          	lea    rdx,[rax+0x8]
   140005b93:	48 89 55 30          	mov    QWORD PTR [rbp+0x30],rdx
   140005b97:	8b 10                	mov    edx,DWORD PTR [rax]
   140005b99:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005b9d:	89 10                	mov    DWORD PTR [rax],edx
   140005b9f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005ba3:	8b 00                	mov    eax,DWORD PTR [rax]
   140005ba5:	85 c0                	test   eax,eax
   140005ba7:	79 29                	jns    140005bd2 <__mingw_pformat+0xb0f>
   140005ba9:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005bad:	75 13                	jne    140005bc2 <__mingw_pformat+0xaff>
   140005baf:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005bb2:	80 cc 04             	or     ah,0x4
   140005bb5:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005bb8:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   140005bbb:	f7 d8                	neg    eax
   140005bbd:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   140005bc0:	eb 10                	jmp    140005bd2 <__mingw_pformat+0xb0f>
   140005bc2:	c7 45 b0 ff ff ff ff 	mov    DWORD PTR [rbp-0x50],0xffffffff
   140005bc9:	eb 07                	jmp    140005bd2 <__mingw_pformat+0xb0f>
   140005bcb:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005bd2:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
   140005bd9:	00 
   140005bda:	e9 66 01 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005bdf:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005be3:	0f 85 4f 01 00 00    	jne    140005d38 <__mingw_pformat+0xc75>
   140005be9:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005bec:	80 cc 08             	or     ah,0x8
   140005bef:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005bf2:	e9 41 01 00 00       	jmp    140005d38 <__mingw_pformat+0xc75>
   140005bf7:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005bfb:	0f 85 3a 01 00 00    	jne    140005d3b <__mingw_pformat+0xc78>
   140005c01:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c04:	80 cc 01             	or     ah,0x1
   140005c07:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c0a:	e9 2c 01 00 00       	jmp    140005d3b <__mingw_pformat+0xc78>
   140005c0f:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c13:	0f 85 25 01 00 00    	jne    140005d3e <__mingw_pformat+0xc7b>
   140005c19:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c1c:	80 cc 04             	or     ah,0x4
   140005c1f:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c22:	e9 17 01 00 00       	jmp    140005d3e <__mingw_pformat+0xc7b>
   140005c27:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c2b:	0f 85 10 01 00 00    	jne    140005d41 <__mingw_pformat+0xc7e>
   140005c31:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c34:	80 cc 10             	or     ah,0x10
   140005c37:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c3a:	48 c7 45 84 00 00 00 	mov    QWORD PTR [rbp-0x7c],0x0
   140005c41:	00 
   140005c42:	e8 a1 39 00 00       	call   1400095e8 <localeconv>
   140005c47:	48 8b 50 08          	mov    rdx,QWORD PTR [rax+0x8]
   140005c4b:	48 8d 4d 84          	lea    rcx,[rbp-0x7c]
   140005c4f:	48 8d 45 8c          	lea    rax,[rbp-0x74]
   140005c53:	49 89 c9             	mov    r9,rcx
   140005c56:	41 b8 10 00 00 00    	mov    r8d,0x10
   140005c5c:	48 89 c1             	mov    rcx,rax
   140005c5f:	e8 bc 33 00 00       	call   140009020 <mbrtowc>
   140005c64:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   140005c67:	83 7d dc 00          	cmp    DWORD PTR [rbp-0x24],0x0
   140005c6b:	7e 08                	jle    140005c75 <__mingw_pformat+0xbb2>
   140005c6d:	0f b7 45 8c          	movzx  eax,WORD PTR [rbp-0x74]
   140005c71:	66 89 45 c0          	mov    WORD PTR [rbp-0x40],ax
   140005c75:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140005c78:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
   140005c7b:	e9 c1 00 00 00       	jmp    140005d41 <__mingw_pformat+0xc7e>
   140005c80:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c84:	0f 85 ba 00 00 00    	jne    140005d44 <__mingw_pformat+0xc81>
   140005c8a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005c8d:	83 c8 40             	or     eax,0x40
   140005c90:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005c93:	e9 ac 00 00 00       	jmp    140005d44 <__mingw_pformat+0xc81>
   140005c98:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005c9c:	75 0e                	jne    140005cac <__mingw_pformat+0xbe9>
   140005c9e:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
   140005ca1:	80 cc 02             	or     ah,0x2
   140005ca4:	89 45 a8             	mov    DWORD PTR [rbp-0x58],eax
   140005ca7:	e9 99 00 00 00       	jmp    140005d45 <__mingw_pformat+0xc82>
   140005cac:	83 7d fc 03          	cmp    DWORD PTR [rbp-0x4],0x3
   140005cb0:	77 68                	ja     140005d1a <__mingw_pformat+0xc57>
   140005cb2:	83 7d e8 39          	cmp    DWORD PTR [rbp-0x18],0x39
   140005cb6:	7f 62                	jg     140005d1a <__mingw_pformat+0xc57>
   140005cb8:	83 7d e8 2f          	cmp    DWORD PTR [rbp-0x18],0x2f
   140005cbc:	7e 5c                	jle    140005d1a <__mingw_pformat+0xc57>
   140005cbe:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140005cc2:	75 09                	jne    140005ccd <__mingw_pformat+0xc0a>
   140005cc4:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   140005ccb:	eb 0d                	jmp    140005cda <__mingw_pformat+0xc17>
   140005ccd:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
   140005cd1:	75 07                	jne    140005cda <__mingw_pformat+0xc17>
   140005cd3:	c7 45 fc 03 00 00 00 	mov    DWORD PTR [rbp-0x4],0x3
   140005cda:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140005cdf:	74 64                	je     140005d45 <__mingw_pformat+0xc82>
   140005ce1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005ce5:	8b 00                	mov    eax,DWORD PTR [rax]
   140005ce7:	85 c0                	test   eax,eax
   140005ce9:	79 0e                	jns    140005cf9 <__mingw_pformat+0xc36>
   140005ceb:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140005cee:	8d 50 d0             	lea    edx,[rax-0x30]
   140005cf1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005cf5:	89 10                	mov    DWORD PTR [rax],edx
   140005cf7:	eb 4c                	jmp    140005d45 <__mingw_pformat+0xc82>
   140005cf9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005cfd:	8b 10                	mov    edx,DWORD PTR [rax]
   140005cff:	89 d0                	mov    eax,edx
   140005d01:	c1 e0 02             	shl    eax,0x2
   140005d04:	01 d0                	add    eax,edx
   140005d06:	01 c0                	add    eax,eax
   140005d08:	89 c2                	mov    edx,eax
   140005d0a:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140005d0d:	01 d0                	add    eax,edx
   140005d0f:	8d 50 d0             	lea    edx,[rax-0x30]
   140005d12:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005d16:	89 10                	mov    DWORD PTR [rax],edx
   140005d18:	eb 2b                	jmp    140005d45 <__mingw_pformat+0xc82>
   140005d1a:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140005d1e:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140005d22:	48 8d 45 a0          	lea    rax,[rbp-0x60]
   140005d26:	48 89 c2             	mov    rdx,rax
   140005d29:	b9 25 00 00 00       	mov    ecx,0x25
   140005d2e:	e8 fd d3 ff ff       	call   140003130 <__pformat_putc>
   140005d33:	e9 00 f4 ff ff       	jmp    140005138 <__mingw_pformat+0x75>
   140005d38:	90                   	nop
   140005d39:	eb 0a                	jmp    140005d45 <__mingw_pformat+0xc82>
   140005d3b:	90                   	nop
   140005d3c:	eb 07                	jmp    140005d45 <__mingw_pformat+0xc82>
   140005d3e:	90                   	nop
   140005d3f:	eb 04                	jmp    140005d45 <__mingw_pformat+0xc82>
   140005d41:	90                   	nop
   140005d42:	eb 01                	jmp    140005d45 <__mingw_pformat+0xc82>
   140005d44:	90                   	nop
   140005d45:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005d49:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005d4c:	84 c0                	test   al,al
   140005d4e:	0f 85 2d f4 ff ff    	jne    140005181 <__mingw_pformat+0xbe>
   140005d54:	eb 0e                	jmp    140005d64 <__mingw_pformat+0xca1>
   140005d56:	48 8d 55 a0          	lea    rdx,[rbp-0x60]
   140005d5a:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140005d5d:	89 c1                	mov    ecx,eax
   140005d5f:	e8 cc d3 ff ff       	call   140003130 <__pformat_putc>
   140005d64:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140005d68:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140005d6c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140005d70:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005d73:	0f be c0             	movsx  eax,al
   140005d76:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140005d79:	83 7d e8 00          	cmp    DWORD PTR [rbp-0x18],0x0
   140005d7d:	0f 85 ba f3 ff ff    	jne    14000513d <__mingw_pformat+0x7a>
   140005d83:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
   140005d86:	48 81 c4 d0 00 00 00 	add    rsp,0xd0
   140005d8d:	5d                   	pop    rbp
   140005d8e:	c3                   	ret
   140005d8f:	90                   	nop

0000000140005d90 <__rv_alloc_D2A>:
   140005d90:	55                   	push   rbp
   140005d91:	48 89 e5             	mov    rbp,rsp
   140005d94:	48 83 ec 30          	sub    rsp,0x30
   140005d98:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140005d9b:	c7 45 fc 04 00 00 00 	mov    DWORD PTR [rbp-0x4],0x4
   140005da2:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140005da9:	eb 07                	jmp    140005db2 <__rv_alloc_D2A+0x22>
   140005dab:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
   140005daf:	d1 65 fc             	shl    DWORD PTR [rbp-0x4],1
   140005db2:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005db5:	83 c0 17             	add    eax,0x17
   140005db8:	39 45 10             	cmp    DWORD PTR [rbp+0x10],eax
   140005dbb:	7f ee                	jg     140005dab <__rv_alloc_D2A+0x1b>
   140005dbd:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140005dc0:	89 c1                	mov    ecx,eax
   140005dc2:	e8 56 1e 00 00       	call   140007c1d <__Balloc_D2A>
   140005dc7:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005dcb:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005dcf:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140005dd2:	89 10                	mov    DWORD PTR [rax],edx
   140005dd4:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005dd8:	48 83 c0 04          	add    rax,0x4
   140005ddc:	48 83 c4 30          	add    rsp,0x30
   140005de0:	5d                   	pop    rbp
   140005de1:	c3                   	ret

0000000140005de2 <__nrv_alloc_D2A>:
   140005de2:	55                   	push   rbp
   140005de3:	48 89 e5             	mov    rbp,rsp
   140005de6:	48 83 ec 30          	sub    rsp,0x30
   140005dea:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140005dee:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140005df2:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   140005df6:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140005df9:	89 c1                	mov    ecx,eax
   140005dfb:	e8 90 ff ff ff       	call   140005d90 <__rv_alloc_D2A>
   140005e00:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005e04:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005e08:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140005e0c:	eb 05                	jmp    140005e13 <__nrv_alloc_D2A+0x31>
   140005e0e:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
   140005e13:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005e17:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140005e1b:	48 89 55 10          	mov    QWORD PTR [rbp+0x10],rdx
   140005e1f:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   140005e22:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e26:	88 10                	mov    BYTE PTR [rax],dl
   140005e28:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e2c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140005e2f:	84 c0                	test   al,al
   140005e31:	75 db                	jne    140005e0e <__nrv_alloc_D2A+0x2c>
   140005e33:	48 83 7d 18 00       	cmp    QWORD PTR [rbp+0x18],0x0
   140005e38:	74 0b                	je     140005e45 <__nrv_alloc_D2A+0x63>
   140005e3a:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140005e3e:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140005e42:	48 89 10             	mov    QWORD PTR [rax],rdx
   140005e45:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005e49:	48 83 c4 30          	add    rsp,0x30
   140005e4d:	5d                   	pop    rbp
   140005e4e:	c3                   	ret

0000000140005e4f <__freedtoa>:
   140005e4f:	55                   	push   rbp
   140005e50:	48 89 e5             	mov    rbp,rsp
   140005e53:	48 83 ec 30          	sub    rsp,0x30
   140005e57:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140005e5b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005e5f:	48 83 e8 04          	sub    rax,0x4
   140005e63:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140005e67:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e6b:	8b 10                	mov    edx,DWORD PTR [rax]
   140005e6d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e71:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140005e74:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e78:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140005e7b:	ba 01 00 00 00       	mov    edx,0x1
   140005e80:	89 c1                	mov    ecx,eax
   140005e82:	d3 e2                	shl    edx,cl
   140005e84:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e88:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140005e8b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140005e8f:	48 89 c1             	mov    rcx,rax
   140005e92:	e8 c7 1e 00 00       	call   140007d5e <__Bfree_D2A>
   140005e97:	90                   	nop
   140005e98:	48 83 c4 30          	add    rsp,0x30
   140005e9c:	5d                   	pop    rbp
   140005e9d:	c3                   	ret

0000000140005e9e <__quorem_D2A>:
   140005e9e:	55                   	push   rbp
   140005e9f:	48 89 e5             	mov    rbp,rsp
   140005ea2:	48 83 ec 70          	sub    rsp,0x70
   140005ea6:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140005eaa:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140005eae:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140005eb2:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140005eb5:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140005eb8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005ebc:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140005ebf:	39 45 fc             	cmp    DWORD PTR [rbp-0x4],eax
   140005ec2:	7e 0a                	jle    140005ece <__quorem_D2A+0x30>
   140005ec4:	b8 00 00 00 00       	mov    eax,0x0
   140005ec9:	e9 3f 02 00 00       	jmp    14000610d <__quorem_D2A+0x26f>
   140005ece:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140005ed2:	48 83 c0 18          	add    rax,0x18
   140005ed6:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140005eda:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   140005ede:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005ee1:	48 98                	cdqe
   140005ee3:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140005eea:	00 
   140005eeb:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140005eef:	48 01 d0             	add    rax,rdx
   140005ef2:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140005ef6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005efa:	48 83 c0 18          	add    rax,0x18
   140005efe:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005f02:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140005f05:	48 98                	cdqe
   140005f07:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140005f0e:	00 
   140005f0f:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005f13:	48 01 d0             	add    rax,rdx
   140005f16:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140005f1a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005f1e:	8b 00                	mov    eax,DWORD PTR [rax]
   140005f20:	48 8b 55 c0          	mov    rdx,QWORD PTR [rbp-0x40]
   140005f24:	8b 12                	mov    edx,DWORD PTR [rdx]
   140005f26:	8d 4a 01             	lea    ecx,[rdx+0x1]
   140005f29:	ba 00 00 00 00       	mov    edx,0x0
   140005f2e:	f7 f1                	div    ecx
   140005f30:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140005f33:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140005f37:	0f 84 c4 00 00 00    	je     140006001 <__quorem_D2A+0x163>
   140005f3d:	48 c7 45 d0 00 00 00 	mov    QWORD PTR [rbp-0x30],0x0
   140005f44:	00 
   140005f45:	48 c7 45 c8 00 00 00 	mov    QWORD PTR [rbp-0x38],0x0
   140005f4c:	00 
   140005f4d:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140005f51:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140005f55:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
   140005f59:	8b 00                	mov    eax,DWORD PTR [rax]
   140005f5b:	89 c2                	mov    edx,eax
   140005f5d:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140005f60:	48 0f af d0          	imul   rdx,rax
   140005f64:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140005f68:	48 01 d0             	add    rax,rdx
   140005f6b:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140005f6f:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140005f73:	48 c1 e8 20          	shr    rax,0x20
   140005f77:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140005f7b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005f7f:	8b 00                	mov    eax,DWORD PTR [rax]
   140005f81:	89 c1                	mov    ecx,eax
   140005f83:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140005f87:	89 c2                	mov    edx,eax
   140005f89:	48 89 c8             	mov    rax,rcx
   140005f8c:	48 29 d0             	sub    rax,rdx
   140005f8f:	48 2b 45 d0          	sub    rax,QWORD PTR [rbp-0x30]
   140005f93:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140005f97:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140005f9b:	48 c1 e8 20          	shr    rax,0x20
   140005f9f:	83 e0 01             	and    eax,0x1
   140005fa2:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140005fa6:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140005faa:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140005fae:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140005fb2:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   140005fb6:	89 10                	mov    DWORD PTR [rax],edx
   140005fb8:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140005fbc:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   140005fc0:	73 8b                	jae    140005f4d <__quorem_D2A+0xaf>
   140005fc2:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005fc6:	8b 00                	mov    eax,DWORD PTR [rax]
   140005fc8:	85 c0                	test   eax,eax
   140005fca:	75 35                	jne    140006001 <__quorem_D2A+0x163>
   140005fcc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005fd0:	48 83 c0 18          	add    rax,0x18
   140005fd4:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140005fd8:	eb 04                	jmp    140005fde <__quorem_D2A+0x140>
   140005fda:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   140005fde:	48 83 6d e8 04       	sub    QWORD PTR [rbp-0x18],0x4
   140005fe3:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005fe7:	48 39 45 f0          	cmp    QWORD PTR [rbp-0x10],rax
   140005feb:	73 0a                	jae    140005ff7 <__quorem_D2A+0x159>
   140005fed:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140005ff1:	8b 00                	mov    eax,DWORD PTR [rax]
   140005ff3:	85 c0                	test   eax,eax
   140005ff5:	74 e3                	je     140005fda <__quorem_D2A+0x13c>
   140005ff7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140005ffb:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140005ffe:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140006001:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140006005:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140006009:	48 89 c1             	mov    rcx,rax
   14000600c:	e8 bc 24 00 00       	call   1400084cd <__cmp_D2A>
   140006011:	85 c0                	test   eax,eax
   140006013:	0f 88 f1 00 00 00    	js     14000610a <__quorem_D2A+0x26c>
   140006019:	83 45 e4 01          	add    DWORD PTR [rbp-0x1c],0x1
   14000601d:	48 c7 45 d0 00 00 00 	mov    QWORD PTR [rbp-0x30],0x0
   140006024:	00 
   140006025:	48 c7 45 c8 00 00 00 	mov    QWORD PTR [rbp-0x38],0x0
   14000602c:	00 
   14000602d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140006031:	48 83 c0 18          	add    rax,0x18
   140006035:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140006039:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000603d:	48 83 c0 18          	add    rax,0x18
   140006041:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140006045:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140006049:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000604d:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
   140006051:	8b 00                	mov    eax,DWORD PTR [rax]
   140006053:	89 c2                	mov    edx,eax
   140006055:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140006059:	48 01 d0             	add    rax,rdx
   14000605c:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140006060:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140006064:	48 c1 e8 20          	shr    rax,0x20
   140006068:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000606c:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140006070:	8b 00                	mov    eax,DWORD PTR [rax]
   140006072:	89 c1                	mov    ecx,eax
   140006074:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   140006078:	89 c2                	mov    edx,eax
   14000607a:	48 89 c8             	mov    rax,rcx
   14000607d:	48 29 d0             	sub    rax,rdx
   140006080:	48 2b 45 d0          	sub    rax,QWORD PTR [rbp-0x30]
   140006084:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140006088:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   14000608c:	48 c1 e8 20          	shr    rax,0x20
   140006090:	83 e0 01             	and    eax,0x1
   140006093:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140006097:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000609b:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000609f:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400060a3:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   1400060a7:	89 10                	mov    DWORD PTR [rax],edx
   1400060a9:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400060ad:	48 39 45 c0          	cmp    QWORD PTR [rbp-0x40],rax
   1400060b1:	73 92                	jae    140006045 <__quorem_D2A+0x1a7>
   1400060b3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400060b7:	48 83 c0 18          	add    rax,0x18
   1400060bb:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400060bf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400060c2:	48 98                	cdqe
   1400060c4:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400060cb:	00 
   1400060cc:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400060d0:	48 01 d0             	add    rax,rdx
   1400060d3:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400060d7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400060db:	8b 00                	mov    eax,DWORD PTR [rax]
   1400060dd:	85 c0                	test   eax,eax
   1400060df:	75 29                	jne    14000610a <__quorem_D2A+0x26c>
   1400060e1:	eb 04                	jmp    1400060e7 <__quorem_D2A+0x249>
   1400060e3:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   1400060e7:	48 83 6d e8 04       	sub    QWORD PTR [rbp-0x18],0x4
   1400060ec:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400060f0:	48 39 45 f0          	cmp    QWORD PTR [rbp-0x10],rax
   1400060f4:	73 0a                	jae    140006100 <__quorem_D2A+0x262>
   1400060f6:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400060fa:	8b 00                	mov    eax,DWORD PTR [rax]
   1400060fc:	85 c0                	test   eax,eax
   1400060fe:	74 e3                	je     1400060e3 <__quorem_D2A+0x245>
   140006100:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140006104:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140006107:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   14000610a:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   14000610d:	48 83 c4 70          	add    rsp,0x70
   140006111:	5d                   	pop    rbp
   140006112:	c3                   	ret
   140006113:	90                   	nop
   140006114:	90                   	nop
   140006115:	90                   	nop
   140006116:	90                   	nop
   140006117:	90                   	nop
   140006118:	90                   	nop
   140006119:	90                   	nop
   14000611a:	90                   	nop
   14000611b:	90                   	nop
   14000611c:	90                   	nop
   14000611d:	90                   	nop
   14000611e:	90                   	nop
   14000611f:	90                   	nop

0000000140006120 <__hi0bits_D2A>:
   140006120:	55                   	push   rbp
   140006121:	48 89 e5             	mov    rbp,rsp
   140006124:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140006127:	0f bd 45 10          	bsr    eax,DWORD PTR [rbp+0x10]
   14000612b:	83 f0 1f             	xor    eax,0x1f
   14000612e:	5d                   	pop    rbp
   14000612f:	c3                   	ret

0000000140006130 <bitstob>:
   140006130:	55                   	push   rbp
   140006131:	53                   	push   rbx
   140006132:	48 83 ec 58          	sub    rsp,0x58
   140006136:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   14000613b:	48 89 4d 20          	mov    QWORD PTR [rbp+0x20],rcx
   14000613f:	89 55 28             	mov    DWORD PTR [rbp+0x28],edx
   140006142:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140006146:	c7 45 fc 20 00 00 00 	mov    DWORD PTR [rbp-0x4],0x20
   14000614d:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   140006154:	eb 07                	jmp    14000615d <bitstob+0x2d>
   140006156:	d1 65 fc             	shl    DWORD PTR [rbp-0x4],1
   140006159:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
   14000615d:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140006160:	3b 45 28             	cmp    eax,DWORD PTR [rbp+0x28]
   140006163:	7c f1                	jl     140006156 <bitstob+0x26>
   140006165:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140006168:	89 c1                	mov    ecx,eax
   14000616a:	e8 ae 1a 00 00       	call   140007c1d <__Balloc_D2A>
   14000616f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140006173:	8b 45 28             	mov    eax,DWORD PTR [rbp+0x28]
   140006176:	83 e8 01             	sub    eax,0x1
   140006179:	c1 f8 05             	sar    eax,0x5
   14000617c:	48 98                	cdqe
   14000617e:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140006185:	00 
   140006186:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000618a:	48 01 d0             	add    rax,rdx
   14000618d:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140006191:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006195:	48 83 c0 18          	add    rax,0x18
   140006199:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000619d:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400061a1:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400061a5:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400061a9:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400061ad:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400061b1:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   1400061b5:	8b 12                	mov    edx,DWORD PTR [rdx]
   1400061b7:	89 10                	mov    DWORD PTR [rax],edx
   1400061b9:	48 83 45 20 04       	add    QWORD PTR [rbp+0x20],0x4
   1400061be:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400061c2:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   1400061c6:	73 dd                	jae    1400061a5 <bitstob+0x75>
   1400061c8:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400061cc:	48 2b 45 d8          	sub    rax,QWORD PTR [rbp-0x28]
   1400061d0:	48 c1 f8 02          	sar    rax,0x2
   1400061d4:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400061d7:	eb 1d                	jmp    1400061f6 <bitstob+0xc6>
   1400061d9:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400061dd:	75 17                	jne    1400061f6 <bitstob+0xc6>
   1400061df:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400061e3:	c7 40 14 00 00 00 00 	mov    DWORD PTR [rax+0x14],0x0
   1400061ea:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   1400061ee:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400061f4:	eb 59                	jmp    14000624f <bitstob+0x11f>
   1400061f6:	83 6d fc 01          	sub    DWORD PTR [rbp-0x4],0x1
   1400061fa:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400061fd:	48 98                	cdqe
   1400061ff:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140006206:	00 
   140006207:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000620b:	48 01 d0             	add    rax,rdx
   14000620e:	8b 00                	mov    eax,DWORD PTR [rax]
   140006210:	85 c0                	test   eax,eax
   140006212:	74 c5                	je     1400061d9 <bitstob+0xa9>
   140006214:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140006217:	8d 50 01             	lea    edx,[rax+0x1]
   14000621a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000621e:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140006221:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140006224:	83 c0 01             	add    eax,0x1
   140006227:	c1 e0 05             	shl    eax,0x5
   14000622a:	89 c3                	mov    ebx,eax
   14000622c:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006230:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140006233:	48 63 d2             	movsxd rdx,edx
   140006236:	48 83 c2 04          	add    rdx,0x4
   14000623a:	8b 44 90 08          	mov    eax,DWORD PTR [rax+rdx*4+0x8]
   14000623e:	89 c1                	mov    ecx,eax
   140006240:	e8 db fe ff ff       	call   140006120 <__hi0bits_D2A>
   140006245:	29 c3                	sub    ebx,eax
   140006247:	89 da                	mov    edx,ebx
   140006249:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   14000624d:	89 10                	mov    DWORD PTR [rax],edx
   14000624f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006253:	48 83 c4 58          	add    rsp,0x58
   140006257:	5b                   	pop    rbx
   140006258:	5d                   	pop    rbp
   140006259:	c3                   	ret

000000014000625a <__gdtoa>:
   14000625a:	55                   	push   rbp
   14000625b:	48 81 ec 00 01 00 00 	sub    rsp,0x100
   140006262:	48 8d ac 24 80 00 00 	lea    rbp,[rsp+0x80]
   140006269:	00 
   14000626a:	48 89 8d 90 00 00 00 	mov    QWORD PTR [rbp+0x90],rcx
   140006271:	89 95 98 00 00 00    	mov    DWORD PTR [rbp+0x98],edx
   140006277:	4c 89 85 a0 00 00 00 	mov    QWORD PTR [rbp+0xa0],r8
   14000627e:	4c 89 8d a8 00 00 00 	mov    QWORD PTR [rbp+0xa8],r9
   140006285:	c7 45 64 00 00 00 00 	mov    DWORD PTR [rbp+0x64],0x0
   14000628c:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   140006293:	8b 00                	mov    eax,DWORD PTR [rax]
   140006295:	83 e0 cf             	and    eax,0xffffffcf
   140006298:	89 c2                	mov    edx,eax
   14000629a:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   1400062a1:	89 10                	mov    DWORD PTR [rax],edx
   1400062a3:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   1400062aa:	8b 00                	mov    eax,DWORD PTR [rax]
   1400062ac:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400062af:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400062b2:	83 e0 07             	and    eax,0x7
   1400062b5:	83 f8 04             	cmp    eax,0x4
   1400062b8:	0f 84 b0 00 00 00    	je     14000636e <__gdtoa+0x114>
   1400062be:	83 f8 04             	cmp    eax,0x4
   1400062c1:	0f 8f d5 00 00 00    	jg     14000639c <__gdtoa+0x142>
   1400062c7:	83 f8 03             	cmp    eax,0x3
   1400062ca:	74 74                	je     140006340 <__gdtoa+0xe6>
   1400062cc:	83 f8 03             	cmp    eax,0x3
   1400062cf:	0f 8f c7 00 00 00    	jg     14000639c <__gdtoa+0x142>
   1400062d5:	85 c0                	test   eax,eax
   1400062d7:	0f 84 05 01 00 00    	je     1400063e2 <__gdtoa+0x188>
   1400062dd:	85 c0                	test   eax,eax
   1400062df:	0f 88 b7 00 00 00    	js     14000639c <__gdtoa+0x142>
   1400062e5:	83 e8 01             	sub    eax,0x1
   1400062e8:	83 f8 01             	cmp    eax,0x1
   1400062eb:	0f 87 ab 00 00 00    	ja     14000639c <__gdtoa+0x142>
   1400062f1:	90                   	nop
   1400062f2:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   1400062f9:	8b 00                	mov    eax,DWORD PTR [rax]
   1400062fb:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   1400062fe:	48 8d 4d b4          	lea    rcx,[rbp-0x4c]
   140006302:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140006305:	48 8b 85 a0 00 00 00 	mov    rax,QWORD PTR [rbp+0xa0]
   14000630c:	49 89 c8             	mov    r8,rcx
   14000630f:	48 89 c1             	mov    rcx,rax
   140006312:	e8 19 fe ff ff       	call   140006130 <bitstob>
   140006317:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000631b:	8b 85 98 00 00 00    	mov    eax,DWORD PTR [rbp+0x98]
   140006321:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140006324:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006328:	48 89 c1             	mov    rcx,rax
   14000632b:	e8 31 16 00 00       	call   140007961 <__trailz_D2A>
   140006330:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006333:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006336:	85 c0                	test   eax,eax
   140006338:	0f 84 8b 00 00 00    	je     1400063c9 <__gdtoa+0x16f>
   14000633e:	eb 66                	jmp    1400063a6 <__gdtoa+0x14c>
   140006340:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   140006347:	c7 00 00 80 ff ff    	mov    DWORD PTR [rax],0xffff8000
   14000634d:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   140006354:	48 8d 0d f5 4f 00 00 	lea    rcx,[rip+0x4ff5]        # 14000b350 <.rdata>
   14000635b:	41 b8 08 00 00 00    	mov    r8d,0x8
   140006361:	48 89 c2             	mov    rdx,rax
   140006364:	e8 79 fa ff ff       	call   140005de2 <__nrv_alloc_D2A>
   140006369:	e9 4a 14 00 00       	jmp    1400077b8 <__gdtoa+0x155e>
   14000636e:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   140006375:	c7 00 00 80 ff ff    	mov    DWORD PTR [rax],0xffff8000
   14000637b:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   140006382:	48 8d 0d d0 4f 00 00 	lea    rcx,[rip+0x4fd0]        # 14000b359 <.rdata+0x9>
   140006389:	41 b8 03 00 00 00    	mov    r8d,0x3
   14000638f:	48 89 c2             	mov    rdx,rax
   140006392:	e8 4b fa ff ff       	call   140005de2 <__nrv_alloc_D2A>
   140006397:	e9 1c 14 00 00       	jmp    1400077b8 <__gdtoa+0x155e>
   14000639c:	b8 00 00 00 00       	mov    eax,0x0
   1400063a1:	e9 12 14 00 00       	jmp    1400077b8 <__gdtoa+0x155e>
   1400063a6:	8b 55 b0             	mov    edx,DWORD PTR [rbp-0x50]
   1400063a9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400063ad:	48 89 c1             	mov    rcx,rax
   1400063b0:	e8 50 14 00 00       	call   140007805 <__rshift_D2A>
   1400063b5:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400063b8:	01 85 98 00 00 00    	add    DWORD PTR [rbp+0x98],eax
   1400063be:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
   1400063c1:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400063c4:	29 c2                	sub    edx,eax
   1400063c6:	89 55 b4             	mov    DWORD PTR [rbp-0x4c],edx
   1400063c9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400063cd:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400063d0:	85 c0                	test   eax,eax
   1400063d2:	75 3d                	jne    140006411 <__gdtoa+0x1b7>
   1400063d4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400063d8:	48 89 c1             	mov    rcx,rax
   1400063db:	e8 7e 19 00 00       	call   140007d5e <__Bfree_D2A>
   1400063e0:	eb 01                	jmp    1400063e3 <__gdtoa+0x189>
   1400063e2:	90                   	nop
   1400063e3:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   1400063ea:	c7 00 01 00 00 00    	mov    DWORD PTR [rax],0x1
   1400063f0:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   1400063f7:	48 8d 0d 5f 4f 00 00 	lea    rcx,[rip+0x4f5f]        # 14000b35d <.rdata+0xd>
   1400063fe:	41 b8 01 00 00 00    	mov    r8d,0x1
   140006404:	48 89 c2             	mov    rdx,rax
   140006407:	e8 d6 f9 ff ff       	call   140005de2 <__nrv_alloc_D2A>
   14000640c:	e9 a7 13 00 00       	jmp    1400077b8 <__gdtoa+0x155e>
   140006411:	48 8d 55 b0          	lea    rdx,[rbp-0x50]
   140006415:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006419:	48 89 c1             	mov    rcx,rax
   14000641c:	e8 75 23 00 00       	call   140008796 <__b2d_D2A>
   140006421:	66 48 0f 7e c0       	movq   rax,xmm0
   140006426:	48 89 45 a8          	mov    QWORD PTR [rbp-0x58],rax
   14000642a:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
   14000642d:	8b 85 98 00 00 00    	mov    eax,DWORD PTR [rbp+0x98]
   140006433:	01 d0                	add    eax,edx
   140006435:	83 e8 01             	sub    eax,0x1
   140006438:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000643b:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   14000643e:	25 ff ff 0f 00       	and    eax,0xfffff
   140006443:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   140006446:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   140006449:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   14000644e:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   140006451:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006456:	f2 0f 10 15 02 4f 00 	movsd  xmm2,QWORD PTR [rip+0x4f02]        # 14000b360 <.rdata+0x10>
   14000645d:	00 
   14000645e:	66 0f 28 c8          	movapd xmm1,xmm0
   140006462:	f2 0f 5c ca          	subsd  xmm1,xmm2
   140006466:	f2 0f 10 05 fa 4e 00 	movsd  xmm0,QWORD PTR [rip+0x4efa]        # 14000b368 <.rdata+0x18>
   14000646d:	00 
   14000646e:	f2 0f 59 c8          	mulsd  xmm1,xmm0
   140006472:	f2 0f 10 05 f6 4e 00 	movsd  xmm0,QWORD PTR [rip+0x4ef6]        # 14000b370 <.rdata+0x20>
   140006479:	00 
   14000647a:	f2 0f 58 c8          	addsd  xmm1,xmm0
   14000647e:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006481:	66 0f ef d2          	pxor   xmm2,xmm2
   140006485:	f2 0f 2a d0          	cvtsi2sd xmm2,eax
   140006489:	f2 0f 10 05 e7 4e 00 	movsd  xmm0,QWORD PTR [rip+0x4ee7]        # 14000b378 <.rdata+0x28>
   140006490:	00 
   140006491:	f2 0f 59 c2          	mulsd  xmm0,xmm2
   140006495:	f2 0f 58 c1          	addsd  xmm0,xmm1
   140006499:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   14000649e:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400064a1:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   1400064a4:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   1400064a8:	79 03                	jns    1400064ad <__gdtoa+0x253>
   1400064aa:	f7 5d 60             	neg    DWORD PTR [rbp+0x60]
   1400064ad:	81 6d 60 35 04 00 00 	sub    DWORD PTR [rbp+0x60],0x435
   1400064b4:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   1400064b8:	7e 23                	jle    1400064dd <__gdtoa+0x283>
   1400064ba:	66 0f ef c9          	pxor   xmm1,xmm1
   1400064be:	f2 0f 2a 4d 60       	cvtsi2sd xmm1,DWORD PTR [rbp+0x60]
   1400064c3:	f2 0f 10 05 b5 4e 00 	movsd  xmm0,QWORD PTR [rip+0x4eb5]        # 14000b380 <.rdata+0x30>
   1400064ca:	00 
   1400064cb:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400064cf:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   1400064d4:	f2 0f 58 c1          	addsd  xmm0,xmm1
   1400064d8:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   1400064dd:	f2 0f 10 45 08       	movsd  xmm0,QWORD PTR [rbp+0x8]
   1400064e2:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   1400064e6:	89 45 58             	mov    DWORD PTR [rbp+0x58],eax
   1400064e9:	66 0f ef c0          	pxor   xmm0,xmm0
   1400064ed:	66 0f 2f 45 08       	comisd xmm0,QWORD PTR [rbp+0x8]
   1400064f2:	76 1b                	jbe    14000650f <__gdtoa+0x2b5>
   1400064f4:	66 0f ef c0          	pxor   xmm0,xmm0
   1400064f8:	f2 0f 2a 45 58       	cvtsi2sd xmm0,DWORD PTR [rbp+0x58]
   1400064fd:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   140006502:	7a 07                	jp     14000650b <__gdtoa+0x2b1>
   140006504:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   140006509:	74 04                	je     14000650f <__gdtoa+0x2b5>
   14000650b:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   14000650f:	c7 45 54 01 00 00 00 	mov    DWORD PTR [rbp+0x54],0x1
   140006516:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
   140006519:	8b 4d b4             	mov    ecx,DWORD PTR [rbp-0x4c]
   14000651c:	8b 95 98 00 00 00    	mov    edx,DWORD PTR [rbp+0x98]
   140006522:	01 ca                	add    edx,ecx
   140006524:	83 ea 01             	sub    edx,0x1
   140006527:	c1 e2 14             	shl    edx,0x14
   14000652a:	01 d0                	add    eax,edx
   14000652c:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
   14000652f:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   140006533:	78 2e                	js     140006563 <__gdtoa+0x309>
   140006535:	83 7d 58 16          	cmp    DWORD PTR [rbp+0x58],0x16
   140006539:	7f 28                	jg     140006563 <__gdtoa+0x309>
   14000653b:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006540:	48 8b 05 49 51 00 00 	mov    rax,QWORD PTR [rip+0x5149]        # 14000b690 <.refptr.__tens_D2A>
   140006547:	8b 55 58             	mov    edx,DWORD PTR [rbp+0x58]
   14000654a:	48 63 d2             	movsxd rdx,edx
   14000654d:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006552:	66 0f 2f c1          	comisd xmm0,xmm1
   140006556:	76 04                	jbe    14000655c <__gdtoa+0x302>
   140006558:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   14000655c:	c7 45 54 00 00 00 00 	mov    DWORD PTR [rbp+0x54],0x0
   140006563:	8b 55 b4             	mov    edx,DWORD PTR [rbp-0x4c]
   140006566:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006569:	29 c2                	sub    edx,eax
   14000656b:	8d 42 ff             	lea    eax,[rdx-0x1]
   14000656e:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006571:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006575:	78 0f                	js     140006586 <__gdtoa+0x32c>
   140006577:	c7 45 7c 00 00 00 00 	mov    DWORD PTR [rbp+0x7c],0x0
   14000657e:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006581:	89 45 40             	mov    DWORD PTR [rbp+0x40],eax
   140006584:	eb 0f                	jmp    140006595 <__gdtoa+0x33b>
   140006586:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006589:	f7 d8                	neg    eax
   14000658b:	89 45 7c             	mov    DWORD PTR [rbp+0x7c],eax
   14000658e:	c7 45 40 00 00 00 00 	mov    DWORD PTR [rbp+0x40],0x0
   140006595:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   140006599:	78 15                	js     1400065b0 <__gdtoa+0x356>
   14000659b:	c7 45 78 00 00 00 00 	mov    DWORD PTR [rbp+0x78],0x0
   1400065a2:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400065a5:	89 45 3c             	mov    DWORD PTR [rbp+0x3c],eax
   1400065a8:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400065ab:	01 45 40             	add    DWORD PTR [rbp+0x40],eax
   1400065ae:	eb 15                	jmp    1400065c5 <__gdtoa+0x36b>
   1400065b0:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400065b3:	29 45 7c             	sub    DWORD PTR [rbp+0x7c],eax
   1400065b6:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400065b9:	f7 d8                	neg    eax
   1400065bb:	89 45 78             	mov    DWORD PTR [rbp+0x78],eax
   1400065be:	c7 45 3c 00 00 00 00 	mov    DWORD PTR [rbp+0x3c],0x0
   1400065c5:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   1400065cc:	78 09                	js     1400065d7 <__gdtoa+0x37d>
   1400065ce:	83 bd b0 00 00 00 09 	cmp    DWORD PTR [rbp+0xb0],0x9
   1400065d5:	7e 0a                	jle    1400065e1 <__gdtoa+0x387>
   1400065d7:	c7 85 b0 00 00 00 00 	mov    DWORD PTR [rbp+0xb0],0x0
   1400065de:	00 00 00 
   1400065e1:	c7 45 34 01 00 00 00 	mov    DWORD PTR [rbp+0x34],0x1
   1400065e8:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   1400065ef:	7e 10                	jle    140006601 <__gdtoa+0x3a7>
   1400065f1:	83 ad b0 00 00 00 04 	sub    DWORD PTR [rbp+0xb0],0x4
   1400065f8:	c7 45 34 00 00 00 00 	mov    DWORD PTR [rbp+0x34],0x0
   1400065ff:	eb 1b                	jmp    14000661c <__gdtoa+0x3c2>
   140006601:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006604:	3d f9 03 00 00       	cmp    eax,0x3f9
   140006609:	7f 0a                	jg     140006615 <__gdtoa+0x3bb>
   14000660b:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   14000660e:	3d 02 fc ff ff       	cmp    eax,0xfffffc02
   140006613:	7d 07                	jge    14000661c <__gdtoa+0x3c2>
   140006615:	c7 45 34 00 00 00 00 	mov    DWORD PTR [rbp+0x34],0x0
   14000661c:	c7 45 50 01 00 00 00 	mov    DWORD PTR [rbp+0x50],0x1
   140006623:	c7 45 68 ff ff ff ff 	mov    DWORD PTR [rbp+0x68],0xffffffff
   14000662a:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   14000662d:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006630:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   140006637:	0f 84 c5 00 00 00    	je     140006702 <__gdtoa+0x4a8>
   14000663d:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   140006644:	0f 8f e6 00 00 00    	jg     140006730 <__gdtoa+0x4d6>
   14000664a:	83 bd b0 00 00 00 04 	cmp    DWORD PTR [rbp+0xb0],0x4
   140006651:	74 7e                	je     1400066d1 <__gdtoa+0x477>
   140006653:	83 bd b0 00 00 00 04 	cmp    DWORD PTR [rbp+0xb0],0x4
   14000665a:	0f 8f d0 00 00 00    	jg     140006730 <__gdtoa+0x4d6>
   140006660:	83 bd b0 00 00 00 03 	cmp    DWORD PTR [rbp+0xb0],0x3
   140006667:	0f 84 8e 00 00 00    	je     1400066fb <__gdtoa+0x4a1>
   14000666d:	83 bd b0 00 00 00 03 	cmp    DWORD PTR [rbp+0xb0],0x3
   140006674:	0f 8f b6 00 00 00    	jg     140006730 <__gdtoa+0x4d6>
   14000667a:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006681:	7f 0e                	jg     140006691 <__gdtoa+0x437>
   140006683:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   14000668a:	79 13                	jns    14000669f <__gdtoa+0x445>
   14000668c:	e9 9f 00 00 00       	jmp    140006730 <__gdtoa+0x4d6>
   140006691:	83 bd b0 00 00 00 02 	cmp    DWORD PTR [rbp+0xb0],0x2
   140006698:	74 30                	je     1400066ca <__gdtoa+0x470>
   14000669a:	e9 91 00 00 00       	jmp    140006730 <__gdtoa+0x4d6>
   14000669f:	66 0f ef c9          	pxor   xmm1,xmm1
   1400066a3:	f2 0f 2a 4d f8       	cvtsi2sd xmm1,DWORD PTR [rbp-0x8]
   1400066a8:	f2 0f 10 05 d8 4c 00 	movsd  xmm0,QWORD PTR [rip+0x4cd8]        # 14000b388 <.rdata+0x38>
   1400066af:	00 
   1400066b0:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400066b4:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   1400066b8:	83 c0 03             	add    eax,0x3
   1400066bb:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400066be:	c7 85 b8 00 00 00 00 	mov    DWORD PTR [rbp+0xb8],0x0
   1400066c5:	00 00 00 
   1400066c8:	eb 66                	jmp    140006730 <__gdtoa+0x4d6>
   1400066ca:	c7 45 50 00 00 00 00 	mov    DWORD PTR [rbp+0x50],0x0
   1400066d1:	83 bd b8 00 00 00 00 	cmp    DWORD PTR [rbp+0xb8],0x0
   1400066d8:	7f 0a                	jg     1400066e4 <__gdtoa+0x48a>
   1400066da:	c7 85 b8 00 00 00 01 	mov    DWORD PTR [rbp+0xb8],0x1
   1400066e1:	00 00 00 
   1400066e4:	8b 85 b8 00 00 00    	mov    eax,DWORD PTR [rbp+0xb8]
   1400066ea:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400066ed:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400066f0:	89 45 68             	mov    DWORD PTR [rbp+0x68],eax
   1400066f3:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   1400066f6:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   1400066f9:	eb 35                	jmp    140006730 <__gdtoa+0x4d6>
   1400066fb:	c7 45 50 00 00 00 00 	mov    DWORD PTR [rbp+0x50],0x0
   140006702:	8b 95 b8 00 00 00    	mov    edx,DWORD PTR [rbp+0xb8]
   140006708:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   14000670b:	01 d0                	add    eax,edx
   14000670d:	83 c0 01             	add    eax,0x1
   140006710:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006713:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006716:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006719:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   14000671c:	83 e8 01             	sub    eax,0x1
   14000671f:	89 45 68             	mov    DWORD PTR [rbp+0x68],eax
   140006722:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006725:	85 c0                	test   eax,eax
   140006727:	7f 07                	jg     140006730 <__gdtoa+0x4d6>
   140006729:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   140006730:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006733:	89 c1                	mov    ecx,eax
   140006735:	e8 56 f6 ff ff       	call   140005d90 <__rv_alloc_D2A>
   14000673a:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000673e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006742:	48 89 45 00          	mov    QWORD PTR [rbp+0x0],rax
   140006746:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   14000674d:	7f 09                	jg     140006758 <__gdtoa+0x4fe>
   14000674f:	c7 45 44 00 00 00 00 	mov    DWORD PTR [rbp+0x44],0x0
   140006756:	eb 38                	jmp    140006790 <__gdtoa+0x536>
   140006758:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   14000675f:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140006762:	83 e8 01             	sub    eax,0x1
   140006765:	89 45 44             	mov    DWORD PTR [rbp+0x44],eax
   140006768:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   14000676c:	74 22                	je     140006790 <__gdtoa+0x536>
   14000676e:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   140006772:	79 07                	jns    14000677b <__gdtoa+0x521>
   140006774:	c7 45 44 02 00 00 00 	mov    DWORD PTR [rbp+0x44],0x2
   14000677b:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000677e:	83 e0 08             	and    eax,0x8
   140006781:	85 c0                	test   eax,eax
   140006783:	74 0b                	je     140006790 <__gdtoa+0x536>
   140006785:	b8 03 00 00 00       	mov    eax,0x3
   14000678a:	2b 45 44             	sub    eax,DWORD PTR [rbp+0x44]
   14000678d:	89 45 44             	mov    DWORD PTR [rbp+0x44],eax
   140006790:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006794:	0f 88 b9 04 00 00    	js     140006c53 <__gdtoa+0x9f9>
   14000679a:	83 7d 6c 0e          	cmp    DWORD PTR [rbp+0x6c],0xe
   14000679e:	0f 8f af 04 00 00    	jg     140006c53 <__gdtoa+0x9f9>
   1400067a4:	83 7d 34 00          	cmp    DWORD PTR [rbp+0x34],0x0
   1400067a8:	0f 84 a5 04 00 00    	je     140006c53 <__gdtoa+0x9f9>
   1400067ae:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   1400067b2:	0f 85 9b 04 00 00    	jne    140006c53 <__gdtoa+0x9f9>
   1400067b8:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   1400067bc:	0f 85 91 04 00 00    	jne    140006c53 <__gdtoa+0x9f9>
   1400067c2:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   1400067c9:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   1400067ce:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
   1400067d3:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400067d6:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   1400067d9:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   1400067dc:	89 45 d8             	mov    DWORD PTR [rbp-0x28],eax
   1400067df:	c7 45 70 02 00 00 00 	mov    DWORD PTR [rbp+0x70],0x2
   1400067e6:	83 7d 58 00          	cmp    DWORD PTR [rbp+0x58],0x0
   1400067ea:	0f 8e 98 00 00 00    	jle    140006888 <__gdtoa+0x62e>
   1400067f0:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   1400067f3:	83 e0 0f             	and    eax,0xf
   1400067f6:	89 c2                	mov    edx,eax
   1400067f8:	48 8b 05 91 4e 00 00 	mov    rax,QWORD PTR [rip+0x4e91]        # 14000b690 <.refptr.__tens_D2A>
   1400067ff:	48 63 d2             	movsxd rdx,edx
   140006802:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006807:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   14000680c:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   14000680f:	c1 f8 04             	sar    eax,0x4
   140006812:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006815:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006818:	83 e0 10             	and    eax,0x10
   14000681b:	85 c0                	test   eax,eax
   14000681d:	74 5e                	je     14000687d <__gdtoa+0x623>
   14000681f:	83 65 60 0f          	and    DWORD PTR [rbp+0x60],0xf
   140006823:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006828:	48 8b 05 91 4d 00 00 	mov    rax,QWORD PTR [rip+0x4d91]        # 14000b5c0 <.refptr.__bigtens_D2A>
   14000682f:	f2 0f 10 48 20       	movsd  xmm1,QWORD PTR [rax+0x20]
   140006834:	f2 0f 5e c1          	divsd  xmm0,xmm1
   140006838:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   14000683d:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   140006841:	eb 3a                	jmp    14000687d <__gdtoa+0x623>
   140006843:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006846:	83 e0 01             	and    eax,0x1
   140006849:	85 c0                	test   eax,eax
   14000684b:	74 24                	je     140006871 <__gdtoa+0x617>
   14000684d:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   140006851:	8b 55 b0             	mov    edx,DWORD PTR [rbp-0x50]
   140006854:	48 8b 05 65 4d 00 00 	mov    rax,QWORD PTR [rip+0x4d65]        # 14000b5c0 <.refptr.__bigtens_D2A>
   14000685b:	48 63 d2             	movsxd rdx,edx
   14000685e:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006863:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   140006868:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   14000686c:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006871:	d1 7d 60             	sar    DWORD PTR [rbp+0x60],1
   140006874:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006877:	83 c0 01             	add    eax,0x1
   14000687a:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000687d:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006881:	75 c0                	jne    140006843 <__gdtoa+0x5e9>
   140006883:	e9 8b 00 00 00       	jmp    140006913 <__gdtoa+0x6b9>
   140006888:	f2 0f 10 05 00 4b 00 	movsd  xmm0,QWORD PTR [rip+0x4b00]        # 14000b390 <.rdata+0x40>
   14000688f:	00 
   140006890:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006895:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   140006898:	f7 d8                	neg    eax
   14000689a:	89 45 5c             	mov    DWORD PTR [rbp+0x5c],eax
   14000689d:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   1400068a1:	74 70                	je     140006913 <__gdtoa+0x6b9>
   1400068a3:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   1400068a8:	8b 45 5c             	mov    eax,DWORD PTR [rbp+0x5c]
   1400068ab:	83 e0 0f             	and    eax,0xf
   1400068ae:	89 c2                	mov    edx,eax
   1400068b0:	48 8b 05 d9 4d 00 00 	mov    rax,QWORD PTR [rip+0x4dd9]        # 14000b690 <.refptr.__tens_D2A>
   1400068b7:	48 63 d2             	movsxd rdx,edx
   1400068ba:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   1400068bf:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400068c3:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   1400068c8:	8b 45 5c             	mov    eax,DWORD PTR [rbp+0x5c]
   1400068cb:	c1 f8 04             	sar    eax,0x4
   1400068ce:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   1400068d1:	eb 3a                	jmp    14000690d <__gdtoa+0x6b3>
   1400068d3:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   1400068d6:	83 e0 01             	and    eax,0x1
   1400068d9:	85 c0                	test   eax,eax
   1400068db:	74 24                	je     140006901 <__gdtoa+0x6a7>
   1400068dd:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   1400068e1:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   1400068e6:	8b 55 b0             	mov    edx,DWORD PTR [rbp-0x50]
   1400068e9:	48 8b 05 d0 4c 00 00 	mov    rax,QWORD PTR [rip+0x4cd0]        # 14000b5c0 <.refptr.__bigtens_D2A>
   1400068f0:	48 63 d2             	movsxd rdx,edx
   1400068f3:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   1400068f8:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   1400068fc:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006901:	d1 7d 60             	sar    DWORD PTR [rbp+0x60],1
   140006904:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006907:	83 c0 01             	add    eax,0x1
   14000690a:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000690d:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006911:	75 c0                	jne    1400068d3 <__gdtoa+0x679>
   140006913:	83 7d 54 00          	cmp    DWORD PTR [rbp+0x54],0x0
   140006917:	74 47                	je     140006960 <__gdtoa+0x706>
   140006919:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   14000691e:	f2 0f 10 05 6a 4a 00 	movsd  xmm0,QWORD PTR [rip+0x4a6a]        # 14000b390 <.rdata+0x40>
   140006925:	00 
   140006926:	66 0f 2f c1          	comisd xmm0,xmm1
   14000692a:	76 34                	jbe    140006960 <__gdtoa+0x706>
   14000692c:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006930:	7e 2e                	jle    140006960 <__gdtoa+0x706>
   140006932:	83 7d 68 00          	cmp    DWORD PTR [rbp+0x68],0x0
   140006936:	0f 8e f5 02 00 00    	jle    140006c31 <__gdtoa+0x9d7>
   14000693c:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   14000693f:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006942:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   140006946:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   14000694b:	f2 0f 10 05 45 4a 00 	movsd  xmm0,QWORD PTR [rip+0x4a45]        # 14000b398 <.rdata+0x48>
   140006952:	00 
   140006953:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006957:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   14000695c:	83 45 70 01          	add    DWORD PTR [rbp+0x70],0x1
   140006960:	66 0f ef c9          	pxor   xmm1,xmm1
   140006964:	f2 0f 2a 4d 70       	cvtsi2sd xmm1,DWORD PTR [rbp+0x70]
   140006969:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   14000696e:	f2 0f 59 c8          	mulsd  xmm1,xmm0
   140006972:	f2 0f 10 05 26 4a 00 	movsd  xmm0,QWORD PTR [rip+0x4a26]        # 14000b3a0 <.rdata+0x50>
   140006979:	00 
   14000697a:	f2 0f 58 c1          	addsd  xmm0,xmm1
   14000697e:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006983:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
   140006986:	2d 00 00 40 03       	sub    eax,0x3400000
   14000698b:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
   14000698e:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006992:	75 5f                	jne    1400069f3 <__gdtoa+0x799>
   140006994:	48 c7 45 18 00 00 00 	mov    QWORD PTR [rbp+0x18],0x0
   14000699b:	00 
   14000699c:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400069a0:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400069a4:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   1400069a9:	f2 0f 10 0d f7 49 00 	movsd  xmm1,QWORD PTR [rip+0x49f7]        # 14000b3a8 <.rdata+0x58>
   1400069b0:	00 
   1400069b1:	f2 0f 5c c1          	subsd  xmm0,xmm1
   1400069b5:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   1400069ba:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   1400069bf:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   1400069c4:	66 0f 2f c1          	comisd xmm0,xmm1
   1400069c8:	0f 87 ac 07 00 00    	ja     14000717a <__gdtoa+0xf20>
   1400069ce:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   1400069d3:	f2 0f 10 45 a0       	movsd  xmm0,QWORD PTR [rbp-0x60]
   1400069d8:	f3 0f 7e 15 d0 49 00 	movq   xmm2,QWORD PTR [rip+0x49d0]        # 14000b3b0 <.rdata+0x60>
   1400069df:	00 
   1400069e0:	66 0f 57 c2          	xorpd  xmm0,xmm2
   1400069e4:	66 0f 2f c1          	comisd xmm0,xmm1
   1400069e8:	0f 87 6e 07 00 00    	ja     14000715c <__gdtoa+0xf02>
   1400069ee:	e9 42 02 00 00       	jmp    140006c35 <__gdtoa+0x9db>
   1400069f3:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   1400069f7:	0f 84 22 01 00 00    	je     140006b1f <__gdtoa+0x8c5>
   1400069fd:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   140006a02:	f2 0f 10 05 b6 49 00 	movsd  xmm0,QWORD PTR [rip+0x49b6]        # 14000b3c0 <.rdata+0x70>
   140006a09:	00 
   140006a0a:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006a0e:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006a11:	8d 50 ff             	lea    edx,[rax-0x1]
   140006a14:	48 8b 05 75 4c 00 00 	mov    rax,QWORD PTR [rip+0x4c75]        # 14000b690 <.refptr.__tens_D2A>
   140006a1b:	48 63 d2             	movsxd rdx,edx
   140006a1e:	f2 0f 10 0c d0       	movsd  xmm1,QWORD PTR [rax+rdx*8]
   140006a23:	f2 0f 5e c1          	divsd  xmm0,xmm1
   140006a27:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006a2c:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006a30:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006a35:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   140006a3c:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006a41:	f2 0f 5e 45 08       	divsd  xmm0,QWORD PTR [rbp+0x8]
   140006a46:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   140006a4a:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140006a4d:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006a52:	66 0f ef c9          	pxor   xmm1,xmm1
   140006a56:	f2 0f 2a 4d d4       	cvtsi2sd xmm1,DWORD PTR [rbp-0x2c]
   140006a5b:	f2 0f 59 4d 08       	mulsd  xmm1,QWORD PTR [rbp+0x8]
   140006a60:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006a64:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006a69:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006a6c:	8d 48 30             	lea    ecx,[rax+0x30]
   140006a6f:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006a73:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006a77:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006a7b:	89 ca                	mov    edx,ecx
   140006a7d:	88 10                	mov    BYTE PTR [rax],dl
   140006a7f:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006a84:	f2 0f 10 45 a0       	movsd  xmm0,QWORD PTR [rbp-0x60]
   140006a89:	66 0f 2f c1          	comisd xmm0,xmm1
   140006a8d:	76 29                	jbe    140006ab8 <__gdtoa+0x85e>
   140006a8f:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006a94:	66 0f ef c9          	pxor   xmm1,xmm1
   140006a98:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006a9c:	7a 0e                	jp     140006aac <__gdtoa+0x852>
   140006a9e:	66 0f ef c9          	pxor   xmm1,xmm1
   140006aa2:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006aa6:	0f 84 90 0c 00 00    	je     14000773c <__gdtoa+0x14e2>
   140006aac:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006ab3:	e9 84 0c 00 00       	jmp    14000773c <__gdtoa+0x14e2>
   140006ab8:	f2 0f 10 55 a8       	movsd  xmm2,QWORD PTR [rbp-0x58]
   140006abd:	f2 0f 10 45 08       	movsd  xmm0,QWORD PTR [rbp+0x8]
   140006ac2:	66 0f 28 c8          	movapd xmm1,xmm0
   140006ac6:	f2 0f 5c ca          	subsd  xmm1,xmm2
   140006aca:	f2 0f 10 45 a0       	movsd  xmm0,QWORD PTR [rbp-0x60]
   140006acf:	66 0f 2f c1          	comisd xmm0,xmm1
   140006ad3:	0f 87 c3 02 00 00    	ja     140006d9c <__gdtoa+0xb42>
   140006ad9:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006adc:	83 c0 01             	add    eax,0x1
   140006adf:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006ae2:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006ae5:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006ae8:	0f 8e 46 01 00 00    	jle    140006c34 <__gdtoa+0x9da>
   140006aee:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006af3:	f2 0f 10 05 9d 48 00 	movsd  xmm0,QWORD PTR [rip+0x489d]        # 14000b398 <.rdata+0x48>
   140006afa:	00 
   140006afb:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006aff:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006b04:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006b09:	f2 0f 10 05 87 48 00 	movsd  xmm0,QWORD PTR [rip+0x4887]        # 14000b398 <.rdata+0x48>
   140006b10:	00 
   140006b11:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006b15:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006b1a:	e9 1d ff ff ff       	jmp    140006a3c <__gdtoa+0x7e2>
   140006b1f:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006b24:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006b27:	8d 50 ff             	lea    edx,[rax-0x1]
   140006b2a:	48 8b 05 5f 4b 00 00 	mov    rax,QWORD PTR [rip+0x4b5f]        # 14000b690 <.refptr.__tens_D2A>
   140006b31:	48 63 d2             	movsxd rdx,edx
   140006b34:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006b39:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006b3d:	f2 0f 11 45 a0       	movsd  QWORD PTR [rbp-0x60],xmm0
   140006b42:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   140006b49:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006b4e:	f2 0f 5e 45 08       	divsd  xmm0,QWORD PTR [rbp+0x8]
   140006b53:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   140006b57:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140006b5a:	83 7d d4 00          	cmp    DWORD PTR [rbp-0x2c],0x0
   140006b5e:	74 1c                	je     140006b7c <__gdtoa+0x922>
   140006b60:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006b65:	66 0f ef c9          	pxor   xmm1,xmm1
   140006b69:	f2 0f 2a 4d d4       	cvtsi2sd xmm1,DWORD PTR [rbp-0x2c]
   140006b6e:	f2 0f 59 4d 08       	mulsd  xmm1,QWORD PTR [rbp+0x8]
   140006b73:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006b77:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006b7c:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006b7f:	8d 48 30             	lea    ecx,[rax+0x30]
   140006b82:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006b86:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006b8a:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006b8e:	89 ca                	mov    edx,ecx
   140006b90:	88 10                	mov    BYTE PTR [rax],dl
   140006b92:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006b95:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006b98:	75 73                	jne    140006c0d <__gdtoa+0x9b3>
   140006b9a:	f2 0f 10 4d 08       	movsd  xmm1,QWORD PTR [rbp+0x8]
   140006b9f:	f2 0f 10 05 19 48 00 	movsd  xmm0,QWORD PTR [rip+0x4819]        # 14000b3c0 <.rdata+0x70>
   140006ba6:	00 
   140006ba7:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006bab:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006bb0:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006bb5:	f2 0f 10 4d a0       	movsd  xmm1,QWORD PTR [rbp-0x60]
   140006bba:	f2 0f 58 4d 08       	addsd  xmm1,QWORD PTR [rbp+0x8]
   140006bbf:	66 0f 2f c1          	comisd xmm0,xmm1
   140006bc3:	0f 87 d6 01 00 00    	ja     140006d9f <__gdtoa+0xb45>
   140006bc9:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006bce:	f2 0f 10 55 a0       	movsd  xmm2,QWORD PTR [rbp-0x60]
   140006bd3:	f2 0f 10 45 08       	movsd  xmm0,QWORD PTR [rbp+0x8]
   140006bd8:	f2 0f 5c c2          	subsd  xmm0,xmm2
   140006bdc:	66 0f 2f c1          	comisd xmm0,xmm1
   140006be0:	77 02                	ja     140006be4 <__gdtoa+0x98a>
   140006be2:	eb 51                	jmp    140006c35 <__gdtoa+0x9db>
   140006be4:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006be9:	66 0f ef c9          	pxor   xmm1,xmm1
   140006bed:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006bf1:	7a 0e                	jp     140006c01 <__gdtoa+0x9a7>
   140006bf3:	66 0f ef c9          	pxor   xmm1,xmm1
   140006bf7:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006bfb:	0f 84 3e 0b 00 00    	je     14000773f <__gdtoa+0x14e5>
   140006c01:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006c08:	e9 32 0b 00 00       	jmp    14000773f <__gdtoa+0x14e5>
   140006c0d:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006c10:	83 c0 01             	add    eax,0x1
   140006c13:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006c16:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006c1b:	f2 0f 10 05 75 47 00 	movsd  xmm0,QWORD PTR [rip+0x4775]        # 14000b398 <.rdata+0x48>
   140006c22:	00 
   140006c23:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006c27:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006c2c:	e9 18 ff ff ff       	jmp    140006b49 <__gdtoa+0x8ef>
   140006c31:	90                   	nop
   140006c32:	eb 01                	jmp    140006c35 <__gdtoa+0x9db>
   140006c34:	90                   	nop
   140006c35:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140006c39:	48 89 45 00          	mov    QWORD PTR [rbp+0x0],rax
   140006c3d:	f2 0f 10 45 e0       	movsd  xmm0,QWORD PTR [rbp-0x20]
   140006c42:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006c47:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140006c4a:	89 45 58             	mov    DWORD PTR [rbp+0x58],eax
   140006c4d:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
   140006c50:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140006c53:	83 bd 98 00 00 00 00 	cmp    DWORD PTR [rbp+0x98],0x0
   140006c5a:	0f 88 bf 01 00 00    	js     140006e1f <__gdtoa+0xbc5>
   140006c60:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   140006c67:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140006c6a:	39 45 58             	cmp    DWORD PTR [rbp+0x58],eax
   140006c6d:	0f 8f ac 01 00 00    	jg     140006e1f <__gdtoa+0xbc5>
   140006c73:	48 8b 05 16 4a 00 00 	mov    rax,QWORD PTR [rip+0x4a16]        # 14000b690 <.refptr.__tens_D2A>
   140006c7a:	8b 55 58             	mov    edx,DWORD PTR [rbp+0x58]
   140006c7d:	48 63 d2             	movsxd rdx,edx
   140006c80:	f2 0f 10 04 d0       	movsd  xmm0,QWORD PTR [rax+rdx*8]
   140006c85:	f2 0f 11 45 08       	movsd  QWORD PTR [rbp+0x8],xmm0
   140006c8a:	83 bd b8 00 00 00 00 	cmp    DWORD PTR [rbp+0xb8],0x0
   140006c91:	79 45                	jns    140006cd8 <__gdtoa+0xa7e>
   140006c93:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006c97:	7f 3f                	jg     140006cd8 <__gdtoa+0xa7e>
   140006c99:	48 c7 45 18 00 00 00 	mov    QWORD PTR [rbp+0x18],0x0
   140006ca0:	00 
   140006ca1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006ca5:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006ca9:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006cad:	0f 88 ac 04 00 00    	js     14000715f <__gdtoa+0xf05>
   140006cb3:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006cb8:	f2 0f 10 55 08       	movsd  xmm2,QWORD PTR [rbp+0x8]
   140006cbd:	f2 0f 10 05 e3 46 00 	movsd  xmm0,QWORD PTR [rip+0x46e3]        # 14000b3a8 <.rdata+0x58>
   140006cc4:	00 
   140006cc5:	f2 0f 59 c2          	mulsd  xmm0,xmm2
   140006cc9:	66 0f 2f c1          	comisd xmm0,xmm1
   140006ccd:	0f 83 8c 04 00 00    	jae    14000715f <__gdtoa+0xf05>
   140006cd3:	e9 a6 04 00 00       	jmp    14000717e <__gdtoa+0xf24>
   140006cd8:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   140006cdf:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006ce4:	f2 0f 5e 45 08       	divsd  xmm0,QWORD PTR [rbp+0x8]
   140006ce9:	f2 0f 2c c0          	cvttsd2si eax,xmm0
   140006ced:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140006cf0:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006cf5:	66 0f ef c9          	pxor   xmm1,xmm1
   140006cf9:	f2 0f 2a 4d d4       	cvtsi2sd xmm1,DWORD PTR [rbp-0x2c]
   140006cfe:	f2 0f 59 4d 08       	mulsd  xmm1,QWORD PTR [rbp+0x8]
   140006d03:	f2 0f 5c c1          	subsd  xmm0,xmm1
   140006d07:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006d0c:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006d0f:	8d 48 30             	lea    ecx,[rax+0x30]
   140006d12:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006d16:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006d1a:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006d1e:	89 ca                	mov    edx,ecx
   140006d20:	88 10                	mov    BYTE PTR [rax],dl
   140006d22:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d27:	66 0f ef c9          	pxor   xmm1,xmm1
   140006d2b:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006d2f:	7a 0e                	jp     140006d3f <__gdtoa+0xae5>
   140006d31:	66 0f ef c9          	pxor   xmm1,xmm1
   140006d35:	66 0f 2e c1          	ucomisd xmm0,xmm1
   140006d39:	0f 84 da 00 00 00    	je     140006e19 <__gdtoa+0xbbf>
   140006d3f:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006d42:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006d45:	0f 85 aa 00 00 00    	jne    140006df5 <__gdtoa+0xb9b>
   140006d4b:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   140006d4f:	74 12                	je     140006d63 <__gdtoa+0xb09>
   140006d51:	83 7d 44 01          	cmp    DWORD PTR [rbp+0x44],0x1
   140006d55:	74 4b                	je     140006da2 <__gdtoa+0xb48>
   140006d57:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006d5e:	e9 e0 09 00 00       	jmp    140007743 <__gdtoa+0x14e9>
   140006d63:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d68:	f2 0f 58 c0          	addsd  xmm0,xmm0
   140006d6c:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006d71:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d76:	66 0f 2f 45 08       	comisd xmm0,QWORD PTR [rbp+0x8]
   140006d7b:	77 28                	ja     140006da5 <__gdtoa+0xb4b>
   140006d7d:	f2 0f 10 45 a8       	movsd  xmm0,QWORD PTR [rbp-0x58]
   140006d82:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   140006d87:	7a 63                	jp     140006dec <__gdtoa+0xb92>
   140006d89:	66 0f 2e 45 08       	ucomisd xmm0,QWORD PTR [rbp+0x8]
   140006d8e:	75 5c                	jne    140006dec <__gdtoa+0xb92>
   140006d90:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   140006d93:	83 e0 01             	and    eax,0x1
   140006d96:	85 c0                	test   eax,eax
   140006d98:	74 52                	je     140006dec <__gdtoa+0xb92>
   140006d9a:	eb 09                	jmp    140006da5 <__gdtoa+0xb4b>
   140006d9c:	90                   	nop
   140006d9d:	eb 07                	jmp    140006da6 <__gdtoa+0xb4c>
   140006d9f:	90                   	nop
   140006da0:	eb 04                	jmp    140006da6 <__gdtoa+0xb4c>
   140006da2:	90                   	nop
   140006da3:	eb 01                	jmp    140006da6 <__gdtoa+0xb4c>
   140006da5:	90                   	nop
   140006da6:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140006dad:	eb 17                	jmp    140006dc6 <__gdtoa+0xb6c>
   140006daf:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006db3:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   140006db7:	75 0d                	jne    140006dc6 <__gdtoa+0xb6c>
   140006db9:	83 45 58 01          	add    DWORD PTR [rbp+0x58],0x1
   140006dbd:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006dc1:	c6 00 30             	mov    BYTE PTR [rax],0x30
   140006dc4:	eb 10                	jmp    140006dd6 <__gdtoa+0xb7c>
   140006dc6:	48 83 6d 00 01       	sub    QWORD PTR [rbp+0x0],0x1
   140006dcb:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006dcf:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140006dd2:	3c 39                	cmp    al,0x39
   140006dd4:	74 d9                	je     140006daf <__gdtoa+0xb55>
   140006dd6:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140006dda:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140006dde:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140006de2:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   140006de5:	83 c2 01             	add    edx,0x1
   140006de8:	88 10                	mov    BYTE PTR [rax],dl
   140006dea:	eb 2e                	jmp    140006e1a <__gdtoa+0xbc0>
   140006dec:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140006df3:	eb 25                	jmp    140006e1a <__gdtoa+0xbc0>
   140006df5:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006df8:	83 c0 01             	add    eax,0x1
   140006dfb:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006dfe:	f2 0f 10 4d a8       	movsd  xmm1,QWORD PTR [rbp-0x58]
   140006e03:	f2 0f 10 05 8d 45 00 	movsd  xmm0,QWORD PTR [rip+0x458d]        # 14000b398 <.rdata+0x48>
   140006e0a:	00 
   140006e0b:	f2 0f 59 c1          	mulsd  xmm0,xmm1
   140006e0f:	f2 0f 11 45 a8       	movsd  QWORD PTR [rbp-0x58],xmm0
   140006e14:	e9 c6 fe ff ff       	jmp    140006cdf <__gdtoa+0xa85>
   140006e19:	90                   	nop
   140006e1a:	e9 24 09 00 00       	jmp    140007743 <__gdtoa+0x14e9>
   140006e1f:	8b 45 7c             	mov    eax,DWORD PTR [rbp+0x7c]
   140006e22:	89 45 4c             	mov    DWORD PTR [rbp+0x4c],eax
   140006e25:	8b 45 78             	mov    eax,DWORD PTR [rbp+0x78]
   140006e28:	89 45 48             	mov    DWORD PTR [rbp+0x48],eax
   140006e2b:	48 c7 45 20 00 00 00 	mov    QWORD PTR [rbp+0x20],0x0
   140006e32:	00 
   140006e33:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140006e37:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140006e3b:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   140006e3f:	0f 84 e0 00 00 00    	je     140006f25 <__gdtoa+0xccb>
   140006e45:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
   140006e48:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140006e4b:	29 c2                	sub    edx,eax
   140006e4d:	89 55 b0             	mov    DWORD PTR [rbp-0x50],edx
   140006e50:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006e53:	8d 50 01             	lea    edx,[rax+0x1]
   140006e56:	89 55 b0             	mov    DWORD PTR [rbp-0x50],edx
   140006e59:	8b 95 98 00 00 00    	mov    edx,DWORD PTR [rbp+0x98]
   140006e5f:	29 c2                	sub    edx,eax
   140006e61:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   140006e68:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140006e6b:	39 c2                	cmp    edx,eax
   140006e6d:	7d 43                	jge    140006eb2 <__gdtoa+0xc58>
   140006e6f:	83 bd b0 00 00 00 03 	cmp    DWORD PTR [rbp+0xb0],0x3
   140006e76:	74 3a                	je     140006eb2 <__gdtoa+0xc58>
   140006e78:	83 bd b0 00 00 00 05 	cmp    DWORD PTR [rbp+0xb0],0x5
   140006e7f:	74 31                	je     140006eb2 <__gdtoa+0xc58>
   140006e81:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   140006e88:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   140006e8b:	8b 95 98 00 00 00    	mov    edx,DWORD PTR [rbp+0x98]
   140006e91:	29 c2                	sub    edx,eax
   140006e93:	8d 42 01             	lea    eax,[rdx+0x1]
   140006e96:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006e99:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006ea0:	7e 68                	jle    140006f0a <__gdtoa+0xcb0>
   140006ea2:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140006ea6:	7e 62                	jle    140006f0a <__gdtoa+0xcb0>
   140006ea8:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006eab:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140006eae:	7d 5a                	jge    140006f0a <__gdtoa+0xcb0>
   140006eb0:	eb 0a                	jmp    140006ebc <__gdtoa+0xc62>
   140006eb2:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   140006eb9:	7e 50                	jle    140006f0b <__gdtoa+0xcb1>
   140006ebb:	90                   	nop
   140006ebc:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006ebf:	83 e8 01             	sub    eax,0x1
   140006ec2:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006ec5:	8b 45 48             	mov    eax,DWORD PTR [rbp+0x48]
   140006ec8:	3b 45 60             	cmp    eax,DWORD PTR [rbp+0x60]
   140006ecb:	7c 08                	jl     140006ed5 <__gdtoa+0xc7b>
   140006ecd:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006ed0:	29 45 48             	sub    DWORD PTR [rbp+0x48],eax
   140006ed3:	eb 19                	jmp    140006eee <__gdtoa+0xc94>
   140006ed5:	8b 45 48             	mov    eax,DWORD PTR [rbp+0x48]
   140006ed8:	29 45 60             	sub    DWORD PTR [rbp+0x60],eax
   140006edb:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006ede:	01 45 3c             	add    DWORD PTR [rbp+0x3c],eax
   140006ee1:	8b 45 60             	mov    eax,DWORD PTR [rbp+0x60]
   140006ee4:	01 45 78             	add    DWORD PTR [rbp+0x78],eax
   140006ee7:	c7 45 48 00 00 00 00 	mov    DWORD PTR [rbp+0x48],0x0
   140006eee:	8b 45 6c             	mov    eax,DWORD PTR [rbp+0x6c]
   140006ef1:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006ef4:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006ef7:	85 c0                	test   eax,eax
   140006ef9:	79 10                	jns    140006f0b <__gdtoa+0xcb1>
   140006efb:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006efe:	29 45 4c             	sub    DWORD PTR [rbp+0x4c],eax
   140006f01:	c7 45 b0 00 00 00 00 	mov    DWORD PTR [rbp-0x50],0x0
   140006f08:	eb 01                	jmp    140006f0b <__gdtoa+0xcb1>
   140006f0a:	90                   	nop
   140006f0b:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f0e:	01 45 7c             	add    DWORD PTR [rbp+0x7c],eax
   140006f11:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f14:	01 45 40             	add    DWORD PTR [rbp+0x40],eax
   140006f17:	b9 01 00 00 00       	mov    ecx,0x1
   140006f1c:	e8 f6 0f 00 00       	call   140007f17 <__i2b_D2A>
   140006f21:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140006f25:	83 7d 4c 00          	cmp    DWORD PTR [rbp+0x4c],0x0
   140006f29:	7e 26                	jle    140006f51 <__gdtoa+0xcf7>
   140006f2b:	83 7d 40 00          	cmp    DWORD PTR [rbp+0x40],0x0
   140006f2f:	7e 20                	jle    140006f51 <__gdtoa+0xcf7>
   140006f31:	8b 55 40             	mov    edx,DWORD PTR [rbp+0x40]
   140006f34:	8b 45 4c             	mov    eax,DWORD PTR [rbp+0x4c]
   140006f37:	39 c2                	cmp    edx,eax
   140006f39:	0f 4e c2             	cmovle eax,edx
   140006f3c:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140006f3f:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f42:	29 45 7c             	sub    DWORD PTR [rbp+0x7c],eax
   140006f45:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f48:	29 45 4c             	sub    DWORD PTR [rbp+0x4c],eax
   140006f4b:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140006f4e:	29 45 40             	sub    DWORD PTR [rbp+0x40],eax
   140006f51:	83 7d 78 00          	cmp    DWORD PTR [rbp+0x78],0x0
   140006f55:	7e 7e                	jle    140006fd5 <__gdtoa+0xd7b>
   140006f57:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   140006f5b:	74 65                	je     140006fc2 <__gdtoa+0xd68>
   140006f5d:	83 7d 48 00          	cmp    DWORD PTR [rbp+0x48],0x0
   140006f61:	7e 3b                	jle    140006f9e <__gdtoa+0xd44>
   140006f63:	8b 55 48             	mov    edx,DWORD PTR [rbp+0x48]
   140006f66:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006f6a:	48 89 c1             	mov    rcx,rax
   140006f6d:	e8 11 12 00 00       	call   140008183 <__pow5mult_D2A>
   140006f72:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140006f76:	48 8b 55 28          	mov    rdx,QWORD PTR [rbp+0x28]
   140006f7a:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140006f7e:	48 89 c1             	mov    rcx,rax
   140006f81:	e8 d7 0f 00 00       	call   140007f5d <__mult_D2A>
   140006f86:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140006f8a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006f8e:	48 89 c1             	mov    rcx,rax
   140006f91:	e8 c8 0d 00 00       	call   140007d5e <__Bfree_D2A>
   140006f96:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140006f9a:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140006f9e:	8b 45 78             	mov    eax,DWORD PTR [rbp+0x78]
   140006fa1:	2b 45 48             	sub    eax,DWORD PTR [rbp+0x48]
   140006fa4:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140006fa7:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140006fab:	74 28                	je     140006fd5 <__gdtoa+0xd7b>
   140006fad:	8b 55 60             	mov    edx,DWORD PTR [rbp+0x60]
   140006fb0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006fb4:	48 89 c1             	mov    rcx,rax
   140006fb7:	e8 c7 11 00 00       	call   140008183 <__pow5mult_D2A>
   140006fbc:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140006fc0:	eb 13                	jmp    140006fd5 <__gdtoa+0xd7b>
   140006fc2:	8b 55 78             	mov    edx,DWORD PTR [rbp+0x78]
   140006fc5:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140006fc9:	48 89 c1             	mov    rcx,rax
   140006fcc:	e8 b2 11 00 00       	call   140008183 <__pow5mult_D2A>
   140006fd1:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140006fd5:	b9 01 00 00 00       	mov    ecx,0x1
   140006fda:	e8 38 0f 00 00       	call   140007f17 <__i2b_D2A>
   140006fdf:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006fe3:	83 7d 3c 00          	cmp    DWORD PTR [rbp+0x3c],0x0
   140006fe7:	7e 13                	jle    140006ffc <__gdtoa+0xda2>
   140006fe9:	8b 55 3c             	mov    edx,DWORD PTR [rbp+0x3c]
   140006fec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140006ff0:	48 89 c1             	mov    rcx,rax
   140006ff3:	e8 8b 11 00 00       	call   140008183 <__pow5mult_D2A>
   140006ff8:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140006ffc:	c7 45 38 00 00 00 00 	mov    DWORD PTR [rbp+0x38],0x0
   140007003:	83 bd b0 00 00 00 01 	cmp    DWORD PTR [rbp+0xb0],0x1
   14000700a:	7f 29                	jg     140007035 <__gdtoa+0xddb>
   14000700c:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
   14000700f:	83 f8 01             	cmp    eax,0x1
   140007012:	75 21                	jne    140007035 <__gdtoa+0xddb>
   140007014:	48 8b 85 90 00 00 00 	mov    rax,QWORD PTR [rbp+0x90]
   14000701b:	8b 40 04             	mov    eax,DWORD PTR [rax+0x4]
   14000701e:	83 c0 01             	add    eax,0x1
   140007021:	39 45 f4             	cmp    DWORD PTR [rbp-0xc],eax
   140007024:	7e 0f                	jle    140007035 <__gdtoa+0xddb>
   140007026:	83 45 7c 01          	add    DWORD PTR [rbp+0x7c],0x1
   14000702a:	83 45 40 01          	add    DWORD PTR [rbp+0x40],0x1
   14000702e:	c7 45 38 01 00 00 00 	mov    DWORD PTR [rbp+0x38],0x1
   140007035:	83 7d 3c 00          	cmp    DWORD PTR [rbp+0x3c],0x0
   140007039:	74 22                	je     14000705d <__gdtoa+0xe03>
   14000703b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000703f:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007042:	8d 50 ff             	lea    edx,[rax-0x1]
   140007045:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007049:	48 63 d2             	movsxd rdx,edx
   14000704c:	48 83 c2 04          	add    rdx,0x4
   140007050:	8b 44 90 08          	mov    eax,DWORD PTR [rax+rdx*4+0x8]
   140007054:	89 c1                	mov    ecx,eax
   140007056:	e8 c5 f0 ff ff       	call   140006120 <__hi0bits_D2A>
   14000705b:	eb 05                	jmp    140007062 <__gdtoa+0xe08>
   14000705d:	b8 1f 00 00 00       	mov    eax,0x1f
   140007062:	2b 45 40             	sub    eax,DWORD PTR [rbp+0x40]
   140007065:	83 e8 04             	sub    eax,0x4
   140007068:	83 e0 1f             	and    eax,0x1f
   14000706b:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   14000706e:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007071:	01 45 4c             	add    DWORD PTR [rbp+0x4c],eax
   140007074:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007077:	01 45 7c             	add    DWORD PTR [rbp+0x7c],eax
   14000707a:	83 7d 7c 00          	cmp    DWORD PTR [rbp+0x7c],0x0
   14000707e:	7e 13                	jle    140007093 <__gdtoa+0xe39>
   140007080:	8b 55 7c             	mov    edx,DWORD PTR [rbp+0x7c]
   140007083:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007087:	48 89 c1             	mov    rcx,rax
   14000708a:	e8 b1 12 00 00       	call   140008340 <__lshift_D2A>
   14000708f:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140007093:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007096:	01 45 40             	add    DWORD PTR [rbp+0x40],eax
   140007099:	83 7d 40 00          	cmp    DWORD PTR [rbp+0x40],0x0
   14000709d:	7e 13                	jle    1400070b2 <__gdtoa+0xe58>
   14000709f:	8b 55 40             	mov    edx,DWORD PTR [rbp+0x40]
   1400070a2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400070a6:	48 89 c1             	mov    rcx,rax
   1400070a9:	e8 92 12 00 00       	call   140008340 <__lshift_D2A>
   1400070ae:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400070b2:	83 7d 54 00          	cmp    DWORD PTR [rbp+0x54],0x0
   1400070b6:	74 5a                	je     140007112 <__gdtoa+0xeb8>
   1400070b8:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   1400070bc:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400070c0:	48 89 c1             	mov    rcx,rax
   1400070c3:	e8 05 14 00 00       	call   1400084cd <__cmp_D2A>
   1400070c8:	85 c0                	test   eax,eax
   1400070ca:	79 46                	jns    140007112 <__gdtoa+0xeb8>
   1400070cc:	83 6d 58 01          	sub    DWORD PTR [rbp+0x58],0x1
   1400070d0:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400070d4:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400070da:	ba 0a 00 00 00       	mov    edx,0xa
   1400070df:	48 89 c1             	mov    rcx,rax
   1400070e2:	e8 02 0d 00 00       	call   140007de9 <__multadd_D2A>
   1400070e7:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   1400070eb:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   1400070ef:	74 1b                	je     14000710c <__gdtoa+0xeb2>
   1400070f1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400070f5:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400070fb:	ba 0a 00 00 00       	mov    edx,0xa
   140007100:	48 89 c1             	mov    rcx,rax
   140007103:	e8 e1 0c 00 00       	call   140007de9 <__multadd_D2A>
   140007108:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   14000710c:	8b 45 68             	mov    eax,DWORD PTR [rbp+0x68]
   14000710f:	89 45 6c             	mov    DWORD PTR [rbp+0x6c],eax
   140007112:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140007116:	0f 8f 81 00 00 00    	jg     14000719d <__gdtoa+0xf43>
   14000711c:	83 bd b0 00 00 00 02 	cmp    DWORD PTR [rbp+0xb0],0x2
   140007123:	7e 78                	jle    14000719d <__gdtoa+0xf43>
   140007125:	83 7d 6c 00          	cmp    DWORD PTR [rbp+0x6c],0x0
   140007129:	78 37                	js     140007162 <__gdtoa+0xf08>
   14000712b:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000712f:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007135:	ba 05 00 00 00       	mov    edx,0x5
   14000713a:	48 89 c1             	mov    rcx,rax
   14000713d:	e8 a7 0c 00 00       	call   140007de9 <__multadd_D2A>
   140007142:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140007146:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   14000714a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000714e:	48 89 c1             	mov    rcx,rax
   140007151:	e8 77 13 00 00       	call   1400084cd <__cmp_D2A>
   140007156:	85 c0                	test   eax,eax
   140007158:	7f 23                	jg     14000717d <__gdtoa+0xf23>
   14000715a:	eb 06                	jmp    140007162 <__gdtoa+0xf08>
   14000715c:	90                   	nop
   14000715d:	eb 04                	jmp    140007163 <__gdtoa+0xf09>
   14000715f:	90                   	nop
   140007160:	eb 01                	jmp    140007163 <__gdtoa+0xf09>
   140007162:	90                   	nop
   140007163:	8b 85 b8 00 00 00    	mov    eax,DWORD PTR [rbp+0xb8]
   140007169:	f7 d0                	not    eax
   14000716b:	89 45 58             	mov    DWORD PTR [rbp+0x58],eax
   14000716e:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140007175:	e9 84 05 00 00       	jmp    1400076fe <__gdtoa+0x14a4>
   14000717a:	90                   	nop
   14000717b:	eb 01                	jmp    14000717e <__gdtoa+0xf24>
   14000717d:	90                   	nop
   14000717e:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007185:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007189:	48 8d 50 01          	lea    rdx,[rax+0x1]
   14000718d:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140007191:	c6 00 31             	mov    BYTE PTR [rax],0x31
   140007194:	83 45 58 01          	add    DWORD PTR [rbp+0x58],0x1
   140007198:	e9 61 05 00 00       	jmp    1400076fe <__gdtoa+0x14a4>
   14000719d:	83 7d 50 00          	cmp    DWORD PTR [rbp+0x50],0x0
   1400071a1:	0f 84 14 04 00 00    	je     1400075bb <__gdtoa+0x1361>
   1400071a7:	83 7d 4c 00          	cmp    DWORD PTR [rbp+0x4c],0x0
   1400071ab:	7e 13                	jle    1400071c0 <__gdtoa+0xf66>
   1400071ad:	8b 55 4c             	mov    edx,DWORD PTR [rbp+0x4c]
   1400071b0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071b4:	48 89 c1             	mov    rcx,rax
   1400071b7:	e8 84 11 00 00       	call   140008340 <__lshift_D2A>
   1400071bc:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400071c0:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071c4:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   1400071c8:	83 7d 38 00          	cmp    DWORD PTR [rbp+0x38],0x0
   1400071cc:	74 57                	je     140007225 <__gdtoa+0xfcb>
   1400071ce:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400071d2:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   1400071d5:	89 c1                	mov    ecx,eax
   1400071d7:	e8 41 0a 00 00       	call   140007c1d <__Balloc_D2A>
   1400071dc:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400071e0:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400071e4:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400071e7:	48 98                	cdqe
   1400071e9:	48 83 c0 02          	add    rax,0x2
   1400071ed:	48 8d 0c 85 00 00 00 	lea    rcx,[rax*4+0x0]
   1400071f4:	00 
   1400071f5:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400071f9:	48 8d 50 10          	lea    rdx,[rax+0x10]
   1400071fd:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007201:	48 83 c0 10          	add    rax,0x10
   140007205:	49 89 c8             	mov    r8,rcx
   140007208:	48 89 c1             	mov    rcx,rax
   14000720b:	e8 e8 23 00 00       	call   1400095f8 <memcpy>
   140007210:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007214:	ba 01 00 00 00       	mov    edx,0x1
   140007219:	48 89 c1             	mov    rcx,rax
   14000721c:	e8 1f 11 00 00       	call   140008340 <__lshift_D2A>
   140007221:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140007225:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   14000722c:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007230:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007234:	48 89 c1             	mov    rcx,rax
   140007237:	e8 62 ec ff ff       	call   140005e9e <__quorem_D2A>
   14000723c:	83 c0 30             	add    eax,0x30
   14000723f:	89 45 74             	mov    DWORD PTR [rbp+0x74],eax
   140007242:	48 8b 55 20          	mov    rdx,QWORD PTR [rbp+0x20]
   140007246:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000724a:	48 89 c1             	mov    rcx,rax
   14000724d:	e8 7b 12 00 00       	call   1400084cd <__cmp_D2A>
   140007252:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   140007255:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140007259:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000725d:	48 89 c1             	mov    rcx,rax
   140007260:	e8 38 13 00 00       	call   14000859d <__diff_D2A>
   140007265:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
   140007269:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   14000726d:	8b 40 10             	mov    eax,DWORD PTR [rax+0x10]
   140007270:	85 c0                	test   eax,eax
   140007272:	75 15                	jne    140007289 <__gdtoa+0x102f>
   140007274:	48 8b 55 c0          	mov    rdx,QWORD PTR [rbp-0x40]
   140007278:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000727c:	48 89 c1             	mov    rcx,rax
   14000727f:	e8 49 12 00 00       	call   1400084cd <__cmp_D2A>
   140007284:	89 45 5c             	mov    DWORD PTR [rbp+0x5c],eax
   140007287:	eb 07                	jmp    140007290 <__gdtoa+0x1036>
   140007289:	c7 45 5c 01 00 00 00 	mov    DWORD PTR [rbp+0x5c],0x1
   140007290:	48 8b 45 c0          	mov    rax,QWORD PTR [rbp-0x40]
   140007294:	48 89 c1             	mov    rcx,rax
   140007297:	e8 c2 0a 00 00       	call   140007d5e <__Bfree_D2A>
   14000729c:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   1400072a0:	75 70                	jne    140007312 <__gdtoa+0x10b8>
   1400072a2:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   1400072a9:	75 67                	jne    140007312 <__gdtoa+0x10b8>
   1400072ab:	48 8b 85 a0 00 00 00 	mov    rax,QWORD PTR [rbp+0xa0]
   1400072b2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400072b4:	83 e0 01             	and    eax,0x1
   1400072b7:	85 c0                	test   eax,eax
   1400072b9:	75 57                	jne    140007312 <__gdtoa+0x10b8>
   1400072bb:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   1400072bf:	75 51                	jne    140007312 <__gdtoa+0x10b8>
   1400072c1:	83 7d 74 39          	cmp    DWORD PTR [rbp+0x74],0x39
   1400072c5:	0f 84 01 02 00 00    	je     1400074cc <__gdtoa+0x1272>
   1400072cb:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   1400072cf:	7f 20                	jg     1400072f1 <__gdtoa+0x1097>
   1400072d1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400072d5:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400072d8:	83 f8 01             	cmp    eax,0x1
   1400072db:	7f 0b                	jg     1400072e8 <__gdtoa+0x108e>
   1400072dd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400072e1:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   1400072e4:	85 c0                	test   eax,eax
   1400072e6:	74 14                	je     1400072fc <__gdtoa+0x10a2>
   1400072e8:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   1400072ef:	eb 0b                	jmp    1400072fc <__gdtoa+0x10a2>
   1400072f1:	83 45 74 01          	add    DWORD PTR [rbp+0x74],0x1
   1400072f5:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   1400072fc:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007300:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140007304:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140007308:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   14000730b:	88 10                	mov    BYTE PTR [rax],dl
   14000730d:	e9 ec 03 00 00       	jmp    1400076fe <__gdtoa+0x14a4>
   140007312:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140007316:	78 2b                	js     140007343 <__gdtoa+0x10e9>
   140007318:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   14000731c:	0f 85 96 01 00 00    	jne    1400074b8 <__gdtoa+0x125e>
   140007322:	83 bd b0 00 00 00 00 	cmp    DWORD PTR [rbp+0xb0],0x0
   140007329:	0f 85 89 01 00 00    	jne    1400074b8 <__gdtoa+0x125e>
   14000732f:	48 8b 85 a0 00 00 00 	mov    rax,QWORD PTR [rbp+0xa0]
   140007336:	8b 00                	mov    eax,DWORD PTR [rax]
   140007338:	83 e0 01             	and    eax,0x1
   14000733b:	85 c0                	test   eax,eax
   14000733d:	0f 85 75 01 00 00    	jne    1400074b8 <__gdtoa+0x125e>
   140007343:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   140007347:	0f 84 db 00 00 00    	je     140007428 <__gdtoa+0x11ce>
   14000734d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007351:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007354:	83 f8 01             	cmp    eax,0x1
   140007357:	7f 0f                	jg     140007368 <__gdtoa+0x110e>
   140007359:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000735d:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140007360:	85 c0                	test   eax,eax
   140007362:	0f 84 c0 00 00 00    	je     140007428 <__gdtoa+0x11ce>
   140007368:	83 7d 44 02          	cmp    DWORD PTR [rbp+0x44],0x2
   14000736c:	0f 85 83 00 00 00    	jne    1400073f5 <__gdtoa+0x119b>
   140007372:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   140007379:	e9 24 01 00 00       	jmp    1400074a2 <__gdtoa+0x1248>
   14000737e:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007382:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140007386:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   14000738a:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   14000738d:	88 10                	mov    BYTE PTR [rax],dl
   14000738f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007393:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007399:	ba 0a 00 00 00       	mov    edx,0xa
   14000739e:	48 89 c1             	mov    rcx,rax
   1400073a1:	e8 43 0a 00 00       	call   140007de9 <__multadd_D2A>
   1400073a6:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400073aa:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400073ae:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   1400073b2:	75 08                	jne    1400073bc <__gdtoa+0x1162>
   1400073b4:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400073b8:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   1400073bc:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400073c0:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400073c4:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400073c8:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400073ce:	ba 0a 00 00 00       	mov    edx,0xa
   1400073d3:	48 89 c1             	mov    rcx,rax
   1400073d6:	e8 0e 0a 00 00       	call   140007de9 <__multadd_D2A>
   1400073db:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   1400073df:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   1400073e3:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400073e7:	48 89 c1             	mov    rcx,rax
   1400073ea:	e8 af ea ff ff       	call   140005e9e <__quorem_D2A>
   1400073ef:	83 c0 30             	add    eax,0x30
   1400073f2:	89 45 74             	mov    DWORD PTR [rbp+0x74],eax
   1400073f5:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400073f9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400073fd:	48 89 c1             	mov    rcx,rax
   140007400:	e8 c8 10 00 00       	call   1400084cd <__cmp_D2A>
   140007405:	85 c0                	test   eax,eax
   140007407:	0f 8f 71 ff ff ff    	jg     14000737e <__gdtoa+0x1124>
   14000740d:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   140007410:	8d 50 01             	lea    edx,[rax+0x1]
   140007413:	89 55 74             	mov    DWORD PTR [rbp+0x74],edx
   140007416:	83 f8 39             	cmp    eax,0x39
   140007419:	0f 84 b0 00 00 00    	je     1400074cf <__gdtoa+0x1275>
   14000741f:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007426:	eb 7a                	jmp    1400074a2 <__gdtoa+0x1248>
   140007428:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   14000742c:	7e 53                	jle    140007481 <__gdtoa+0x1227>
   14000742e:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007432:	ba 01 00 00 00       	mov    edx,0x1
   140007437:	48 89 c1             	mov    rcx,rax
   14000743a:	e8 01 0f 00 00       	call   140008340 <__lshift_D2A>
   14000743f:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140007443:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007447:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000744b:	48 89 c1             	mov    rcx,rax
   14000744e:	e8 7a 10 00 00       	call   1400084cd <__cmp_D2A>
   140007453:	89 45 5c             	mov    DWORD PTR [rbp+0x5c],eax
   140007456:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   14000745a:	7f 10                	jg     14000746c <__gdtoa+0x1212>
   14000745c:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   140007460:	75 18                	jne    14000747a <__gdtoa+0x1220>
   140007462:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   140007465:	83 e0 01             	and    eax,0x1
   140007468:	85 c0                	test   eax,eax
   14000746a:	74 0e                	je     14000747a <__gdtoa+0x1220>
   14000746c:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   14000746f:	8d 50 01             	lea    edx,[rax+0x1]
   140007472:	89 55 74             	mov    DWORD PTR [rbp+0x74],edx
   140007475:	83 f8 39             	cmp    eax,0x39
   140007478:	74 58                	je     1400074d2 <__gdtoa+0x1278>
   14000747a:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007481:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007485:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007488:	83 f8 01             	cmp    eax,0x1
   14000748b:	7f 0b                	jg     140007498 <__gdtoa+0x123e>
   14000748d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007491:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140007494:	85 c0                	test   eax,eax
   140007496:	74 09                	je     1400074a1 <__gdtoa+0x1247>
   140007498:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   14000749f:	eb 01                	jmp    1400074a2 <__gdtoa+0x1248>
   1400074a1:	90                   	nop
   1400074a2:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400074a6:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400074aa:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400074ae:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   1400074b1:	88 10                	mov    BYTE PTR [rax],dl
   1400074b3:	e9 46 02 00 00       	jmp    1400076fe <__gdtoa+0x14a4>
   1400074b8:	83 7d 5c 00          	cmp    DWORD PTR [rbp+0x5c],0x0
   1400074bc:	7e 52                	jle    140007510 <__gdtoa+0x12b6>
   1400074be:	83 7d 44 02          	cmp    DWORD PTR [rbp+0x44],0x2
   1400074c2:	74 4c                	je     140007510 <__gdtoa+0x12b6>
   1400074c4:	83 7d 74 39          	cmp    DWORD PTR [rbp+0x74],0x39
   1400074c8:	75 24                	jne    1400074ee <__gdtoa+0x1294>
   1400074ca:	eb 07                	jmp    1400074d3 <__gdtoa+0x1279>
   1400074cc:	90                   	nop
   1400074cd:	eb 04                	jmp    1400074d3 <__gdtoa+0x1279>
   1400074cf:	90                   	nop
   1400074d0:	eb 01                	jmp    1400074d3 <__gdtoa+0x1279>
   1400074d2:	90                   	nop
   1400074d3:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400074d7:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400074db:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400074df:	c6 00 39             	mov    BYTE PTR [rax],0x39
   1400074e2:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   1400074e9:	e9 9d 01 00 00       	jmp    14000768b <__gdtoa+0x1431>
   1400074ee:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   1400074f5:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   1400074f8:	8d 48 01             	lea    ecx,[rax+0x1]
   1400074fb:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400074ff:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140007503:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   140007507:	89 ca                	mov    edx,ecx
   140007509:	88 10                	mov    BYTE PTR [rax],dl
   14000750b:	e9 ee 01 00 00       	jmp    1400076fe <__gdtoa+0x14a4>
   140007510:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007514:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140007518:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   14000751c:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   14000751f:	88 10                	mov    BYTE PTR [rax],dl
   140007521:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   140007524:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   140007527:	0f 84 ea 00 00 00    	je     140007617 <__gdtoa+0x13bd>
   14000752d:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007531:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007537:	ba 0a 00 00 00       	mov    edx,0xa
   14000753c:	48 89 c1             	mov    rcx,rax
   14000753f:	e8 a5 08 00 00       	call   140007de9 <__multadd_D2A>
   140007544:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   140007548:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000754c:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140007550:	75 25                	jne    140007577 <__gdtoa+0x131d>
   140007552:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007556:	41 b8 00 00 00 00    	mov    r8d,0x0
   14000755c:	ba 0a 00 00 00       	mov    edx,0xa
   140007561:	48 89 c1             	mov    rcx,rax
   140007564:	e8 80 08 00 00       	call   140007de9 <__multadd_D2A>
   140007569:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   14000756d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007571:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   140007575:	eb 36                	jmp    1400075ad <__gdtoa+0x1353>
   140007577:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000757b:	41 b8 00 00 00 00    	mov    r8d,0x0
   140007581:	ba 0a 00 00 00       	mov    edx,0xa
   140007586:	48 89 c1             	mov    rcx,rax
   140007589:	e8 5b 08 00 00       	call   140007de9 <__multadd_D2A>
   14000758e:	48 89 45 20          	mov    QWORD PTR [rbp+0x20],rax
   140007592:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007596:	41 b8 00 00 00 00    	mov    r8d,0x0
   14000759c:	ba 0a 00 00 00       	mov    edx,0xa
   1400075a1:	48 89 c1             	mov    rcx,rax
   1400075a4:	e8 40 08 00 00       	call   140007de9 <__multadd_D2A>
   1400075a9:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   1400075ad:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400075b0:	83 c0 01             	add    eax,0x1
   1400075b3:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   1400075b6:	e9 71 fc ff ff       	jmp    14000722c <__gdtoa+0xfd2>
   1400075bb:	c7 45 b0 01 00 00 00 	mov    DWORD PTR [rbp-0x50],0x1
   1400075c2:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   1400075c6:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400075ca:	48 89 c1             	mov    rcx,rax
   1400075cd:	e8 cc e8 ff ff       	call   140005e9e <__quorem_D2A>
   1400075d2:	83 c0 30             	add    eax,0x30
   1400075d5:	89 45 74             	mov    DWORD PTR [rbp+0x74],eax
   1400075d8:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400075dc:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400075e0:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400075e4:	8b 55 74             	mov    edx,DWORD PTR [rbp+0x74]
   1400075e7:	88 10                	mov    BYTE PTR [rax],dl
   1400075e9:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   1400075ec:	39 45 6c             	cmp    DWORD PTR [rbp+0x6c],eax
   1400075ef:	7e 29                	jle    14000761a <__gdtoa+0x13c0>
   1400075f1:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400075f5:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400075fb:	ba 0a 00 00 00       	mov    edx,0xa
   140007600:	48 89 c1             	mov    rcx,rax
   140007603:	e8 e1 07 00 00       	call   140007de9 <__multadd_D2A>
   140007608:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000760c:	8b 45 b0             	mov    eax,DWORD PTR [rbp-0x50]
   14000760f:	83 c0 01             	add    eax,0x1
   140007612:	89 45 b0             	mov    DWORD PTR [rbp-0x50],eax
   140007615:	eb ab                	jmp    1400075c2 <__gdtoa+0x1368>
   140007617:	90                   	nop
   140007618:	eb 01                	jmp    14000761b <__gdtoa+0x13c1>
   14000761a:	90                   	nop
   14000761b:	83 7d 44 00          	cmp    DWORD PTR [rbp+0x44],0x0
   14000761f:	74 26                	je     140007647 <__gdtoa+0x13ed>
   140007621:	83 7d 44 02          	cmp    DWORD PTR [rbp+0x44],0x2
   140007625:	0f 84 ae 00 00 00    	je     1400076d9 <__gdtoa+0x147f>
   14000762b:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000762f:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007632:	83 f8 01             	cmp    eax,0x1
   140007635:	7f 50                	jg     140007687 <__gdtoa+0x142d>
   140007637:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000763b:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   14000763e:	85 c0                	test   eax,eax
   140007640:	75 45                	jne    140007687 <__gdtoa+0x142d>
   140007642:	e9 92 00 00 00       	jmp    1400076d9 <__gdtoa+0x147f>
   140007647:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000764b:	ba 01 00 00 00       	mov    edx,0x1
   140007650:	48 89 c1             	mov    rcx,rax
   140007653:	e8 e8 0c 00 00       	call   140008340 <__lshift_D2A>
   140007658:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000765c:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007660:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007664:	48 89 c1             	mov    rcx,rax
   140007667:	e8 61 0e 00 00       	call   1400084cd <__cmp_D2A>
   14000766c:	89 45 60             	mov    DWORD PTR [rbp+0x60],eax
   14000766f:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140007673:	7f 15                	jg     14000768a <__gdtoa+0x1430>
   140007675:	83 7d 60 00          	cmp    DWORD PTR [rbp+0x60],0x0
   140007679:	75 61                	jne    1400076dc <__gdtoa+0x1482>
   14000767b:	8b 45 74             	mov    eax,DWORD PTR [rbp+0x74]
   14000767e:	83 e0 01             	and    eax,0x1
   140007681:	85 c0                	test   eax,eax
   140007683:	74 57                	je     1400076dc <__gdtoa+0x1482>
   140007685:	eb 03                	jmp    14000768a <__gdtoa+0x1430>
   140007687:	90                   	nop
   140007688:	eb 01                	jmp    14000768b <__gdtoa+0x1431>
   14000768a:	90                   	nop
   14000768b:	c7 45 64 20 00 00 00 	mov    DWORD PTR [rbp+0x64],0x20
   140007692:	eb 1f                	jmp    1400076b3 <__gdtoa+0x1459>
   140007694:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007698:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   14000769c:	75 15                	jne    1400076b3 <__gdtoa+0x1459>
   14000769e:	83 45 58 01          	add    DWORD PTR [rbp+0x58],0x1
   1400076a2:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400076a6:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400076aa:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400076ae:	c6 00 31             	mov    BYTE PTR [rax],0x31
   1400076b1:	eb 4b                	jmp    1400076fe <__gdtoa+0x14a4>
   1400076b3:	48 83 6d 00 01       	sub    QWORD PTR [rbp+0x0],0x1
   1400076b8:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400076bc:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400076bf:	3c 39                	cmp    al,0x39
   1400076c1:	74 d1                	je     140007694 <__gdtoa+0x143a>
   1400076c3:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   1400076c7:	48 8d 50 01          	lea    rdx,[rax+0x1]
   1400076cb:	48 89 55 00          	mov    QWORD PTR [rbp+0x0],rdx
   1400076cf:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   1400076d2:	83 c2 01             	add    edx,0x1
   1400076d5:	88 10                	mov    BYTE PTR [rax],dl
   1400076d7:	eb 25                	jmp    1400076fe <__gdtoa+0x14a4>
   1400076d9:	90                   	nop
   1400076da:	eb 01                	jmp    1400076dd <__gdtoa+0x1483>
   1400076dc:	90                   	nop
   1400076dd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400076e1:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400076e4:	83 f8 01             	cmp    eax,0x1
   1400076e7:	7f 0b                	jg     1400076f4 <__gdtoa+0x149a>
   1400076e9:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400076ed:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   1400076f0:	85 c0                	test   eax,eax
   1400076f2:	74 09                	je     1400076fd <__gdtoa+0x14a3>
   1400076f4:	c7 45 64 10 00 00 00 	mov    DWORD PTR [rbp+0x64],0x10
   1400076fb:	eb 01                	jmp    1400076fe <__gdtoa+0x14a4>
   1400076fd:	90                   	nop
   1400076fe:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007702:	48 89 c1             	mov    rcx,rax
   140007705:	e8 54 06 00 00       	call   140007d5e <__Bfree_D2A>
   14000770a:	48 83 7d 18 00       	cmp    QWORD PTR [rbp+0x18],0x0
   14000770f:	74 31                	je     140007742 <__gdtoa+0x14e8>
   140007711:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140007716:	74 16                	je     14000772e <__gdtoa+0x14d4>
   140007718:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   14000771c:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140007720:	74 0c                	je     14000772e <__gdtoa+0x14d4>
   140007722:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   140007726:	48 89 c1             	mov    rcx,rax
   140007729:	e8 30 06 00 00       	call   140007d5e <__Bfree_D2A>
   14000772e:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007732:	48 89 c1             	mov    rcx,rax
   140007735:	e8 24 06 00 00       	call   140007d5e <__Bfree_D2A>
   14000773a:	eb 0e                	jmp    14000774a <__gdtoa+0x14f0>
   14000773c:	90                   	nop
   14000773d:	eb 0b                	jmp    14000774a <__gdtoa+0x14f0>
   14000773f:	90                   	nop
   140007740:	eb 08                	jmp    14000774a <__gdtoa+0x14f0>
   140007742:	90                   	nop
   140007743:	eb 05                	jmp    14000774a <__gdtoa+0x14f0>
   140007745:	48 83 6d 00 01       	sub    QWORD PTR [rbp+0x0],0x1
   14000774a:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   14000774e:	48 39 45 e8          	cmp    QWORD PTR [rbp-0x18],rax
   140007752:	73 0f                	jae    140007763 <__gdtoa+0x1509>
   140007754:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007758:	48 83 e8 01          	sub    rax,0x1
   14000775c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000775f:	3c 30                	cmp    al,0x30
   140007761:	74 e2                	je     140007745 <__gdtoa+0x14eb>
   140007763:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140007767:	48 89 c1             	mov    rcx,rax
   14000776a:	e8 ef 05 00 00       	call   140007d5e <__Bfree_D2A>
   14000776f:	48 8b 45 00          	mov    rax,QWORD PTR [rbp+0x0]
   140007773:	c6 00 00             	mov    BYTE PTR [rax],0x0
   140007776:	8b 45 58             	mov    eax,DWORD PTR [rbp+0x58]
   140007779:	8d 50 01             	lea    edx,[rax+0x1]
   14000777c:	48 8b 85 c0 00 00 00 	mov    rax,QWORD PTR [rbp+0xc0]
   140007783:	89 10                	mov    DWORD PTR [rax],edx
   140007785:	48 83 bd c8 00 00 00 	cmp    QWORD PTR [rbp+0xc8],0x0
   14000778c:	00 
   14000778d:	74 0e                	je     14000779d <__gdtoa+0x1543>
   14000778f:	48 8b 85 c8 00 00 00 	mov    rax,QWORD PTR [rbp+0xc8]
   140007796:	48 8b 55 00          	mov    rdx,QWORD PTR [rbp+0x0]
   14000779a:	48 89 10             	mov    QWORD PTR [rax],rdx
   14000779d:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   1400077a4:	8b 00                	mov    eax,DWORD PTR [rax]
   1400077a6:	0b 45 64             	or     eax,DWORD PTR [rbp+0x64]
   1400077a9:	89 c2                	mov    edx,eax
   1400077ab:	48 8b 85 a8 00 00 00 	mov    rax,QWORD PTR [rbp+0xa8]
   1400077b2:	89 10                	mov    DWORD PTR [rax],edx
   1400077b4:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400077b8:	48 81 c4 00 01 00 00 	add    rsp,0x100
   1400077bf:	5d                   	pop    rbp
   1400077c0:	c3                   	ret
   1400077c1:	90                   	nop
   1400077c2:	90                   	nop
   1400077c3:	90                   	nop
   1400077c4:	90                   	nop
   1400077c5:	90                   	nop
   1400077c6:	90                   	nop
   1400077c7:	90                   	nop
   1400077c8:	90                   	nop
   1400077c9:	90                   	nop
   1400077ca:	90                   	nop
   1400077cb:	90                   	nop
   1400077cc:	90                   	nop
   1400077cd:	90                   	nop
   1400077ce:	90                   	nop
   1400077cf:	90                   	nop

00000001400077d0 <__lo0bits_D2A>:
   1400077d0:	55                   	push   rbp
   1400077d1:	48 89 e5             	mov    rbp,rsp
   1400077d4:	48 83 ec 10          	sub    rsp,0x10
   1400077d8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400077dc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400077e0:	8b 00                	mov    eax,DWORD PTR [rax]
   1400077e2:	f3 0f bc c0          	tzcnt  eax,eax
   1400077e6:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400077e9:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400077ed:	8b 10                	mov    edx,DWORD PTR [rax]
   1400077ef:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400077f2:	89 c1                	mov    ecx,eax
   1400077f4:	d3 ea                	shr    edx,cl
   1400077f6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400077fa:	89 10                	mov    DWORD PTR [rax],edx
   1400077fc:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400077ff:	48 83 c4 10          	add    rsp,0x10
   140007803:	5d                   	pop    rbp
   140007804:	c3                   	ret

0000000140007805 <__rshift_D2A>:
   140007805:	55                   	push   rbp
   140007806:	48 89 e5             	mov    rbp,rsp
   140007809:	48 83 ec 20          	sub    rsp,0x20
   14000780d:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007811:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140007814:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007818:	48 83 c0 18          	add    rax,0x18
   14000781c:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007820:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007824:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007828:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000782b:	c1 f8 05             	sar    eax,0x5
   14000782e:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140007831:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007835:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007838:	39 45 e8             	cmp    DWORD PTR [rbp-0x18],eax
   14000783b:	0f 8d e4 00 00 00    	jge    140007925 <__rshift_D2A+0x120>
   140007841:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007845:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007848:	48 98                	cdqe
   14000784a:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140007851:	00 
   140007852:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007856:	48 01 d0             	add    rax,rdx
   140007859:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   14000785d:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140007860:	48 98                	cdqe
   140007862:	48 c1 e0 02          	shl    rax,0x2
   140007866:	48 01 45 f8          	add    QWORD PTR [rbp-0x8],rax
   14000786a:	83 65 18 1f          	and    DWORD PTR [rbp+0x18],0x1f
   14000786e:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140007872:	0f 84 a3 00 00 00    	je     14000791b <__rshift_D2A+0x116>
   140007878:	b8 20 00 00 00       	mov    eax,0x20
   14000787d:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   140007880:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   140007883:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007887:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000788b:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   14000788f:	8b 10                	mov    edx,DWORD PTR [rax]
   140007891:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140007894:	89 c1                	mov    ecx,eax
   140007896:	d3 ea                	shr    edx,cl
   140007898:	89 d0                	mov    eax,edx
   14000789a:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   14000789d:	eb 3c                	jmp    1400078db <__rshift_D2A+0xd6>
   14000789f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400078a3:	8b 10                	mov    edx,DWORD PTR [rax]
   1400078a5:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   1400078a8:	89 c1                	mov    ecx,eax
   1400078aa:	d3 e2                	shl    edx,cl
   1400078ac:	89 d1                	mov    ecx,edx
   1400078ae:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078b2:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400078b6:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400078ba:	0b 4d ec             	or     ecx,DWORD PTR [rbp-0x14]
   1400078bd:	89 ca                	mov    edx,ecx
   1400078bf:	89 10                	mov    DWORD PTR [rax],edx
   1400078c1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400078c5:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400078c9:	48 89 55 f8          	mov    QWORD PTR [rbp-0x8],rdx
   1400078cd:	8b 10                	mov    edx,DWORD PTR [rax]
   1400078cf:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   1400078d2:	89 c1                	mov    ecx,eax
   1400078d4:	d3 ea                	shr    edx,cl
   1400078d6:	89 d0                	mov    eax,edx
   1400078d8:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   1400078db:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400078df:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   1400078e3:	72 ba                	jb     14000789f <__rshift_D2A+0x9a>
   1400078e5:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078e9:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   1400078ec:	89 10                	mov    DWORD PTR [rax],edx
   1400078ee:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400078f2:	8b 00                	mov    eax,DWORD PTR [rax]
   1400078f4:	85 c0                	test   eax,eax
   1400078f6:	74 2d                	je     140007925 <__rshift_D2A+0x120>
   1400078f8:	48 83 45 f0 04       	add    QWORD PTR [rbp-0x10],0x4
   1400078fd:	eb 26                	jmp    140007925 <__rshift_D2A+0x120>
   1400078ff:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140007903:	48 8d 42 04          	lea    rax,[rdx+0x4]
   140007907:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000790b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000790f:	48 8d 48 04          	lea    rcx,[rax+0x4]
   140007913:	48 89 4d f0          	mov    QWORD PTR [rbp-0x10],rcx
   140007917:	8b 12                	mov    edx,DWORD PTR [rdx]
   140007919:	89 10                	mov    DWORD PTR [rax],edx
   14000791b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000791f:	48 3b 45 e0          	cmp    rax,QWORD PTR [rbp-0x20]
   140007923:	72 da                	jb     1400078ff <__rshift_D2A+0xfa>
   140007925:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007929:	48 83 c0 18          	add    rax,0x18
   14000792d:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140007931:	48 29 c2             	sub    rdx,rax
   140007934:	48 89 d0             	mov    rax,rdx
   140007937:	48 c1 f8 02          	sar    rax,0x2
   14000793b:	89 c2                	mov    edx,eax
   14000793d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007941:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140007944:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007948:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   14000794b:	85 c0                	test   eax,eax
   14000794d:	75 0b                	jne    14000795a <__rshift_D2A+0x155>
   14000794f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007953:	c7 40 18 00 00 00 00 	mov    DWORD PTR [rax+0x18],0x0
   14000795a:	90                   	nop
   14000795b:	48 83 c4 20          	add    rsp,0x20
   14000795f:	5d                   	pop    rbp
   140007960:	c3                   	ret

0000000140007961 <__trailz_D2A>:
   140007961:	55                   	push   rbp
   140007962:	48 89 e5             	mov    rbp,rsp
   140007965:	48 83 ec 40          	sub    rsp,0x40
   140007969:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000796d:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140007974:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007978:	48 83 c0 18          	add    rax,0x18
   14000797c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007980:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007984:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007987:	48 98                	cdqe
   140007989:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140007990:	00 
   140007991:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007995:	48 01 d0             	add    rax,rdx
   140007998:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000799c:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   1400079a3:	eb 09                	jmp    1400079ae <__trailz_D2A+0x4d>
   1400079a5:	83 45 f4 20          	add    DWORD PTR [rbp-0xc],0x20
   1400079a9:	48 83 45 f8 04       	add    QWORD PTR [rbp-0x8],0x4
   1400079ae:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079b2:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   1400079b6:	73 0a                	jae    1400079c2 <__trailz_D2A+0x61>
   1400079b8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079bc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400079be:	85 c0                	test   eax,eax
   1400079c0:	74 e3                	je     1400079a5 <__trailz_D2A+0x44>
   1400079c2:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079c6:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
   1400079ca:	73 18                	jae    1400079e4 <__trailz_D2A+0x83>
   1400079cc:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400079d0:	8b 00                	mov    eax,DWORD PTR [rax]
   1400079d2:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   1400079d5:	48 8d 45 e4          	lea    rax,[rbp-0x1c]
   1400079d9:	48 89 c1             	mov    rcx,rax
   1400079dc:	e8 ef fd ff ff       	call   1400077d0 <__lo0bits_D2A>
   1400079e1:	01 45 f4             	add    DWORD PTR [rbp-0xc],eax
   1400079e4:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400079e7:	48 83 c4 40          	add    rsp,0x40
   1400079eb:	5d                   	pop    rbp
   1400079ec:	c3                   	ret
   1400079ed:	90                   	nop
   1400079ee:	90                   	nop
   1400079ef:	90                   	nop

00000001400079f0 <dtoa_lock_cleanup>:
   1400079f0:	55                   	push   rbp
   1400079f1:	48 89 e5             	mov    rbp,rsp
   1400079f4:	48 83 ec 40          	sub    rsp,0x40
   1400079f8:	48 8d 05 f1 77 00 00 	lea    rax,[rip+0x77f1]        # 14000f1f0 <dtoa_CS_init>
   1400079ff:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007a03:	c7 45 ec 03 00 00 00 	mov    DWORD PTR [rbp-0x14],0x3
   140007a0a:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   140007a0d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007a11:	87 10                	xchg   DWORD PTR [rax],edx
   140007a13:	89 d0                	mov    eax,edx
   140007a15:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140007a18:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140007a1c:	75 3d                	jne    140007a5b <dtoa_lock_cleanup+0x6b>
   140007a1e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140007a25:	eb 2e                	jmp    140007a55 <dtoa_lock_cleanup+0x65>
   140007a27:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007a2a:	48 63 d0             	movsxd rdx,eax
   140007a2d:	48 89 d0             	mov    rax,rdx
   140007a30:	48 c1 e0 02          	shl    rax,0x2
   140007a34:	48 01 d0             	add    rax,rdx
   140007a37:	48 c1 e0 03          	shl    rax,0x3
   140007a3b:	48 8d 15 5e 77 00 00 	lea    rdx,[rip+0x775e]        # 14000f1a0 <dtoa_CritSec>
   140007a42:	48 01 d0             	add    rax,rdx
   140007a45:	48 89 c1             	mov    rcx,rax
   140007a48:	48 8b 05 d9 87 00 00 	mov    rax,QWORD PTR [rip+0x87d9]        # 140010228 <__imp_DeleteCriticalSection>
   140007a4f:	ff d0                	call   rax
   140007a51:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007a55:	83 7d fc 01          	cmp    DWORD PTR [rbp-0x4],0x1
   140007a59:	7e cc                	jle    140007a27 <dtoa_lock_cleanup+0x37>
   140007a5b:	90                   	nop
   140007a5c:	48 83 c4 40          	add    rsp,0x40
   140007a60:	5d                   	pop    rbp
   140007a61:	c3                   	ret

0000000140007a62 <dtoa_lock>:
   140007a62:	55                   	push   rbp
   140007a63:	48 89 e5             	mov    rbp,rsp
   140007a66:	48 83 ec 40          	sub    rsp,0x40
   140007a6a:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007a6d:	8b 05 7d 77 00 00    	mov    eax,DWORD PTR [rip+0x777d]        # 14000f1f0 <dtoa_CS_init>
   140007a73:	83 f8 02             	cmp    eax,0x2
   140007a76:	75 2c                	jne    140007aa4 <dtoa_lock+0x42>
   140007a78:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007a7b:	48 89 d0             	mov    rax,rdx
   140007a7e:	48 c1 e0 02          	shl    rax,0x2
   140007a82:	48 01 d0             	add    rax,rdx
   140007a85:	48 c1 e0 03          	shl    rax,0x3
   140007a89:	48 8d 15 10 77 00 00 	lea    rdx,[rip+0x7710]        # 14000f1a0 <dtoa_CritSec>
   140007a90:	48 01 d0             	add    rax,rdx
   140007a93:	48 89 c1             	mov    rcx,rax
   140007a96:	48 8b 05 93 87 00 00 	mov    rax,QWORD PTR [rip+0x8793]        # 140010230 <__imp_EnterCriticalSection>
   140007a9d:	ff d0                	call   rax
   140007a9f:	e9 ea 00 00 00       	jmp    140007b8e <dtoa_lock+0x12c>
   140007aa4:	8b 05 46 77 00 00    	mov    eax,DWORD PTR [rip+0x7746]        # 14000f1f0 <dtoa_CS_init>
   140007aaa:	85 c0                	test   eax,eax
   140007aac:	0f 85 9e 00 00 00    	jne    140007b50 <dtoa_lock+0xee>
   140007ab2:	48 8d 05 37 77 00 00 	lea    rax,[rip+0x7737]        # 14000f1f0 <dtoa_CS_init>
   140007ab9:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007abd:	c7 45 ec 01 00 00 00 	mov    DWORD PTR [rbp-0x14],0x1
   140007ac4:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   140007ac7:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007acb:	87 10                	xchg   DWORD PTR [rax],edx
   140007acd:	89 d0                	mov    eax,edx
   140007acf:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140007ad2:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140007ad6:	75 58                	jne    140007b30 <dtoa_lock+0xce>
   140007ad8:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140007adf:	eb 2e                	jmp    140007b0f <dtoa_lock+0xad>
   140007ae1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007ae4:	48 63 d0             	movsxd rdx,eax
   140007ae7:	48 89 d0             	mov    rax,rdx
   140007aea:	48 c1 e0 02          	shl    rax,0x2
   140007aee:	48 01 d0             	add    rax,rdx
   140007af1:	48 c1 e0 03          	shl    rax,0x3
   140007af5:	48 8d 15 a4 76 00 00 	lea    rdx,[rip+0x76a4]        # 14000f1a0 <dtoa_CritSec>
   140007afc:	48 01 d0             	add    rax,rdx
   140007aff:	48 89 c1             	mov    rcx,rax
   140007b02:	48 8b 05 57 87 00 00 	mov    rax,QWORD PTR [rip+0x8757]        # 140010260 <__imp_InitializeCriticalSection>
   140007b09:	ff d0                	call   rax
   140007b0b:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007b0f:	83 7d fc 01          	cmp    DWORD PTR [rbp-0x4],0x1
   140007b13:	7e cc                	jle    140007ae1 <dtoa_lock+0x7f>
   140007b15:	48 8d 05 d4 fe ff ff 	lea    rax,[rip+0xfffffffffffffed4]        # 1400079f0 <dtoa_lock_cleanup>
   140007b1c:	48 89 c1             	mov    rcx,rax
   140007b1f:	e8 0b 9b ff ff       	call   14000162f <atexit>
   140007b24:	c7 05 c2 76 00 00 02 	mov    DWORD PTR [rip+0x76c2],0x2        # 14000f1f0 <dtoa_CS_init>
   140007b2b:	00 00 00 
   140007b2e:	eb 20                	jmp    140007b50 <dtoa_lock+0xee>
   140007b30:	83 7d f8 02          	cmp    DWORD PTR [rbp-0x8],0x2
   140007b34:	75 1a                	jne    140007b50 <dtoa_lock+0xee>
   140007b36:	c7 05 b0 76 00 00 02 	mov    DWORD PTR [rip+0x76b0],0x2        # 14000f1f0 <dtoa_CS_init>
   140007b3d:	00 00 00 
   140007b40:	eb 0e                	jmp    140007b50 <dtoa_lock+0xee>
   140007b42:	b9 01 00 00 00       	mov    ecx,0x1
   140007b47:	48 8b 05 3a 87 00 00 	mov    rax,QWORD PTR [rip+0x873a]        # 140010288 <__imp_Sleep>
   140007b4e:	ff d0                	call   rax
   140007b50:	8b 05 9a 76 00 00    	mov    eax,DWORD PTR [rip+0x769a]        # 14000f1f0 <dtoa_CS_init>
   140007b56:	83 f8 01             	cmp    eax,0x1
   140007b59:	74 e7                	je     140007b42 <dtoa_lock+0xe0>
   140007b5b:	8b 05 8f 76 00 00    	mov    eax,DWORD PTR [rip+0x768f]        # 14000f1f0 <dtoa_CS_init>
   140007b61:	83 f8 02             	cmp    eax,0x2
   140007b64:	75 28                	jne    140007b8e <dtoa_lock+0x12c>
   140007b66:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007b69:	48 89 d0             	mov    rax,rdx
   140007b6c:	48 c1 e0 02          	shl    rax,0x2
   140007b70:	48 01 d0             	add    rax,rdx
   140007b73:	48 c1 e0 03          	shl    rax,0x3
   140007b77:	48 8d 15 22 76 00 00 	lea    rdx,[rip+0x7622]        # 14000f1a0 <dtoa_CritSec>
   140007b7e:	48 01 d0             	add    rax,rdx
   140007b81:	48 89 c1             	mov    rcx,rax
   140007b84:	48 8b 05 a5 86 00 00 	mov    rax,QWORD PTR [rip+0x86a5]        # 140010230 <__imp_EnterCriticalSection>
   140007b8b:	ff d0                	call   rax
   140007b8d:	90                   	nop
   140007b8e:	48 83 c4 40          	add    rsp,0x40
   140007b92:	5d                   	pop    rbp
   140007b93:	c3                   	ret

0000000140007b94 <dtoa_unlock>:
   140007b94:	55                   	push   rbp
   140007b95:	48 89 e5             	mov    rbp,rsp
   140007b98:	48 83 ec 20          	sub    rsp,0x20
   140007b9c:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007b9f:	8b 05 4b 76 00 00    	mov    eax,DWORD PTR [rip+0x764b]        # 14000f1f0 <dtoa_CS_init>
   140007ba5:	83 f8 02             	cmp    eax,0x2
   140007ba8:	75 27                	jne    140007bd1 <dtoa_unlock+0x3d>
   140007baa:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007bad:	48 89 d0             	mov    rax,rdx
   140007bb0:	48 c1 e0 02          	shl    rax,0x2
   140007bb4:	48 01 d0             	add    rax,rdx
   140007bb7:	48 c1 e0 03          	shl    rax,0x3
   140007bbb:	48 8d 15 de 75 00 00 	lea    rdx,[rip+0x75de]        # 14000f1a0 <dtoa_CritSec>
   140007bc2:	48 01 d0             	add    rax,rdx
   140007bc5:	48 89 c1             	mov    rcx,rax
   140007bc8:	48 8b 05 99 86 00 00 	mov    rax,QWORD PTR [rip+0x8699]        # 140010268 <__imp_LeaveCriticalSection>
   140007bcf:	ff d0                	call   rax
   140007bd1:	90                   	nop
   140007bd2:	48 83 c4 20          	add    rsp,0x20
   140007bd6:	5d                   	pop    rbp
   140007bd7:	c3                   	ret

0000000140007bd8 <__lo0bits_D2A>:
   140007bd8:	55                   	push   rbp
   140007bd9:	48 89 e5             	mov    rbp,rsp
   140007bdc:	48 83 ec 10          	sub    rsp,0x10
   140007be0:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007be4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007be8:	8b 00                	mov    eax,DWORD PTR [rax]
   140007bea:	f3 0f bc c0          	tzcnt  eax,eax
   140007bee:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140007bf1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007bf5:	8b 10                	mov    edx,DWORD PTR [rax]
   140007bf7:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007bfa:	89 c1                	mov    ecx,eax
   140007bfc:	d3 ea                	shr    edx,cl
   140007bfe:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007c02:	89 10                	mov    DWORD PTR [rax],edx
   140007c04:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007c07:	48 83 c4 10          	add    rsp,0x10
   140007c0b:	5d                   	pop    rbp
   140007c0c:	c3                   	ret

0000000140007c0d <__hi0bits_D2A>:
   140007c0d:	55                   	push   rbp
   140007c0e:	48 89 e5             	mov    rbp,rsp
   140007c11:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007c14:	0f bd 45 10          	bsr    eax,DWORD PTR [rbp+0x10]
   140007c18:	83 f0 1f             	xor    eax,0x1f
   140007c1b:	5d                   	pop    rbp
   140007c1c:	c3                   	ret

0000000140007c1d <__Balloc_D2A>:
   140007c1d:	55                   	push   rbp
   140007c1e:	48 89 e5             	mov    rbp,rsp
   140007c21:	48 83 ec 30          	sub    rsp,0x30
   140007c25:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007c28:	b9 00 00 00 00       	mov    ecx,0x0
   140007c2d:	e8 30 fe ff ff       	call   140007a62 <dtoa_lock>
   140007c32:	83 7d 10 09          	cmp    DWORD PTR [rbp+0x10],0x9
   140007c36:	7f 48                	jg     140007c80 <__Balloc_D2A+0x63>
   140007c38:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140007c3b:	48 98                	cdqe
   140007c3d:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140007c44:	00 
   140007c45:	48 8d 05 b4 75 00 00 	lea    rax,[rip+0x75b4]        # 14000f200 <freelist>
   140007c4c:	48 8b 04 02          	mov    rax,QWORD PTR [rdx+rax*1]
   140007c50:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007c54:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140007c59:	74 25                	je     140007c80 <__Balloc_D2A+0x63>
   140007c5b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007c5f:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140007c62:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007c65:	48 63 d2             	movsxd rdx,edx
   140007c68:	48 8d 0c d5 00 00 00 	lea    rcx,[rdx*8+0x0]
   140007c6f:	00 
   140007c70:	48 8d 15 89 75 00 00 	lea    rdx,[rip+0x7589]        # 14000f200 <freelist>
   140007c77:	48 89 04 11          	mov    QWORD PTR [rcx+rdx*1],rax
   140007c7b:	e9 b1 00 00 00       	jmp    140007d31 <__Balloc_D2A+0x114>
   140007c80:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140007c83:	ba 01 00 00 00       	mov    edx,0x1
   140007c88:	89 c1                	mov    ecx,eax
   140007c8a:	d3 e2                	shl    edx,cl
   140007c8c:	89 d0                	mov    eax,edx
   140007c8e:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140007c91:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140007c94:	83 e8 01             	sub    eax,0x1
   140007c97:	48 98                	cdqe
   140007c99:	48 c1 e0 02          	shl    rax,0x2
   140007c9d:	48 83 c0 27          	add    rax,0x27
   140007ca1:	48 c1 e8 03          	shr    rax,0x3
   140007ca5:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   140007ca8:	83 7d 10 09          	cmp    DWORD PTR [rbp+0x10],0x9
   140007cac:	7f 4e                	jg     140007cfc <__Balloc_D2A+0xdf>
   140007cae:	48 8b 15 db 23 00 00 	mov    rdx,QWORD PTR [rip+0x23db]        # 14000a090 <pmem_next>
   140007cb5:	48 8d 05 a4 75 00 00 	lea    rax,[rip+0x75a4]        # 14000f260 <private_mem>
   140007cbc:	48 29 c2             	sub    rdx,rax
   140007cbf:	48 89 d0             	mov    rax,rdx
   140007cc2:	48 c1 f8 03          	sar    rax,0x3
   140007cc6:	48 89 c2             	mov    rdx,rax
   140007cc9:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140007ccc:	48 01 d0             	add    rax,rdx
   140007ccf:	48 3d 20 01 00 00    	cmp    rax,0x120
   140007cd5:	77 25                	ja     140007cfc <__Balloc_D2A+0xdf>
   140007cd7:	48 8b 05 b2 23 00 00 	mov    rax,QWORD PTR [rip+0x23b2]        # 14000a090 <pmem_next>
   140007cde:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007ce2:	48 8b 05 a7 23 00 00 	mov    rax,QWORD PTR [rip+0x23a7]        # 14000a090 <pmem_next>
   140007ce9:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   140007cec:	48 c1 e2 03          	shl    rdx,0x3
   140007cf0:	48 01 d0             	add    rax,rdx
   140007cf3:	48 89 05 96 23 00 00 	mov    QWORD PTR [rip+0x2396],rax        # 14000a090 <pmem_next>
   140007cfa:	eb 21                	jmp    140007d1d <__Balloc_D2A+0x100>
   140007cfc:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140007cff:	48 c1 e0 03          	shl    rax,0x3
   140007d03:	48 89 c1             	mov    rcx,rax
   140007d06:	e8 e5 18 00 00       	call   1400095f0 <malloc>
   140007d0b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007d0f:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140007d14:	75 07                	jne    140007d1d <__Balloc_D2A+0x100>
   140007d16:	b8 00 00 00 00       	mov    eax,0x0
   140007d1b:	eb 3b                	jmp    140007d58 <__Balloc_D2A+0x13b>
   140007d1d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d21:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007d24:	89 50 08             	mov    DWORD PTR [rax+0x8],edx
   140007d27:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d2b:	8b 55 f4             	mov    edx,DWORD PTR [rbp-0xc]
   140007d2e:	89 50 0c             	mov    DWORD PTR [rax+0xc],edx
   140007d31:	b9 00 00 00 00       	mov    ecx,0x0
   140007d36:	e8 59 fe ff ff       	call   140007b94 <dtoa_unlock>
   140007d3b:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d3f:	c7 40 14 00 00 00 00 	mov    DWORD PTR [rax+0x14],0x0
   140007d46:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d4a:	8b 50 14             	mov    edx,DWORD PTR [rax+0x14]
   140007d4d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d51:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   140007d54:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007d58:	48 83 c4 30          	add    rsp,0x30
   140007d5c:	5d                   	pop    rbp
   140007d5d:	c3                   	ret

0000000140007d5e <__Bfree_D2A>:
   140007d5e:	55                   	push   rbp
   140007d5f:	48 89 e5             	mov    rbp,rsp
   140007d62:	48 83 ec 20          	sub    rsp,0x20
   140007d66:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007d6a:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140007d6f:	74 71                	je     140007de2 <__Bfree_D2A+0x84>
   140007d71:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007d75:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007d78:	83 f8 09             	cmp    eax,0x9
   140007d7b:	7e 0e                	jle    140007d8b <__Bfree_D2A+0x2d>
   140007d7d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007d81:	48 89 c1             	mov    rcx,rax
   140007d84:	e8 57 18 00 00       	call   1400095e0 <free>
   140007d89:	eb 57                	jmp    140007de2 <__Bfree_D2A+0x84>
   140007d8b:	b9 00 00 00 00       	mov    ecx,0x0
   140007d90:	e8 cd fc ff ff       	call   140007a62 <dtoa_lock>
   140007d95:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007d99:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007d9c:	48 98                	cdqe
   140007d9e:	48 8d 14 c5 00 00 00 	lea    rdx,[rax*8+0x0]
   140007da5:	00 
   140007da6:	48 8d 05 53 74 00 00 	lea    rax,[rip+0x7453]        # 14000f200 <freelist>
   140007dad:	48 8b 14 02          	mov    rdx,QWORD PTR [rdx+rax*1]
   140007db1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007db5:	48 89 10             	mov    QWORD PTR [rax],rdx
   140007db8:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007dbc:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007dbf:	48 98                	cdqe
   140007dc1:	48 8d 0c c5 00 00 00 	lea    rcx,[rax*8+0x0]
   140007dc8:	00 
   140007dc9:	48 8d 15 30 74 00 00 	lea    rdx,[rip+0x7430]        # 14000f200 <freelist>
   140007dd0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007dd4:	48 89 04 11          	mov    QWORD PTR [rcx+rdx*1],rax
   140007dd8:	b9 00 00 00 00       	mov    ecx,0x0
   140007ddd:	e8 b2 fd ff ff       	call   140007b94 <dtoa_unlock>
   140007de2:	90                   	nop
   140007de3:	48 83 c4 20          	add    rsp,0x20
   140007de7:	5d                   	pop    rbp
   140007de8:	c3                   	ret

0000000140007de9 <__multadd_D2A>:
   140007de9:	55                   	push   rbp
   140007dea:	48 89 e5             	mov    rbp,rsp
   140007ded:	48 83 ec 50          	sub    rsp,0x50
   140007df1:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007df5:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140007df8:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d
   140007dfc:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e00:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007e03:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140007e06:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e0a:	48 83 c0 18          	add    rax,0x18
   140007e0e:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007e12:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140007e19:	8b 45 20             	mov    eax,DWORD PTR [rbp+0x20]
   140007e1c:	48 98                	cdqe
   140007e1e:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140007e22:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007e26:	8b 00                	mov    eax,DWORD PTR [rax]
   140007e28:	89 c2                	mov    edx,eax
   140007e2a:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140007e2d:	48 98                	cdqe
   140007e2f:	48 0f af d0          	imul   rdx,rax
   140007e33:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140007e37:	48 01 d0             	add    rax,rdx
   140007e3a:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140007e3e:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140007e42:	48 c1 e8 20          	shr    rax,0x20
   140007e46:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140007e4a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140007e4e:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140007e52:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140007e56:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
   140007e5a:	89 10                	mov    DWORD PTR [rax],edx
   140007e5c:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007e60:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007e63:	3b 45 e4             	cmp    eax,DWORD PTR [rbp-0x1c]
   140007e66:	7c ba                	jl     140007e22 <__multadd_D2A+0x39>
   140007e68:	48 83 7d e8 00       	cmp    QWORD PTR [rbp-0x18],0x0
   140007e6d:	0f 84 9a 00 00 00    	je     140007f0d <__multadd_D2A+0x124>
   140007e73:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e77:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140007e7a:	39 45 e4             	cmp    DWORD PTR [rbp-0x1c],eax
   140007e7d:	7c 67                	jl     140007ee6 <__multadd_D2A+0xfd>
   140007e7f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007e83:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007e86:	83 c0 01             	add    eax,0x1
   140007e89:	89 c1                	mov    ecx,eax
   140007e8b:	e8 8d fd ff ff       	call   140007c1d <__Balloc_D2A>
   140007e90:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140007e94:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   140007e99:	75 07                	jne    140007ea2 <__multadd_D2A+0xb9>
   140007e9b:	b8 00 00 00 00       	mov    eax,0x0
   140007ea0:	eb 6f                	jmp    140007f11 <__multadd_D2A+0x128>
   140007ea2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007ea6:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007ea9:	48 98                	cdqe
   140007eab:	48 83 c0 02          	add    rax,0x2
   140007eaf:	48 8d 0c 85 00 00 00 	lea    rcx,[rax*4+0x0]
   140007eb6:	00 
   140007eb7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007ebb:	48 8d 50 10          	lea    rdx,[rax+0x10]
   140007ebf:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140007ec3:	48 83 c0 10          	add    rax,0x10
   140007ec7:	49 89 c8             	mov    r8,rcx
   140007eca:	48 89 c1             	mov    rcx,rax
   140007ecd:	e8 26 17 00 00       	call   1400095f8 <memcpy>
   140007ed2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007ed6:	48 89 c1             	mov    rcx,rax
   140007ed9:	e8 80 fe ff ff       	call   140007d5e <__Bfree_D2A>
   140007ede:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140007ee2:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140007ee6:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140007ee9:	8d 50 01             	lea    edx,[rax+0x1]
   140007eec:	89 55 e4             	mov    DWORD PTR [rbp-0x1c],edx
   140007eef:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140007ef3:	89 d1                	mov    ecx,edx
   140007ef5:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140007ef9:	48 98                	cdqe
   140007efb:	48 83 c0 04          	add    rax,0x4
   140007eff:	89 4c 82 08          	mov    DWORD PTR [rdx+rax*4+0x8],ecx
   140007f03:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f07:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140007f0a:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140007f0d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f11:	48 83 c4 50          	add    rsp,0x50
   140007f15:	5d                   	pop    rbp
   140007f16:	c3                   	ret

0000000140007f17 <__i2b_D2A>:
   140007f17:	55                   	push   rbp
   140007f18:	48 89 e5             	mov    rbp,rsp
   140007f1b:	48 83 ec 30          	sub    rsp,0x30
   140007f1f:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140007f22:	b9 01 00 00 00       	mov    ecx,0x1
   140007f27:	e8 f1 fc ff ff       	call   140007c1d <__Balloc_D2A>
   140007f2c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140007f30:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140007f35:	75 07                	jne    140007f3e <__i2b_D2A+0x27>
   140007f37:	b8 00 00 00 00       	mov    eax,0x0
   140007f3c:	eb 19                	jmp    140007f57 <__i2b_D2A+0x40>
   140007f3e:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140007f41:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007f45:	89 50 18             	mov    DWORD PTR [rax+0x18],edx
   140007f48:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007f4c:	c7 40 14 01 00 00 00 	mov    DWORD PTR [rax+0x14],0x1
   140007f53:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140007f57:	48 83 c4 30          	add    rsp,0x30
   140007f5b:	5d                   	pop    rbp
   140007f5c:	c3                   	ret

0000000140007f5d <__mult_D2A>:
   140007f5d:	55                   	push   rbp
   140007f5e:	48 89 e5             	mov    rbp,rsp
   140007f61:	48 81 ec 90 00 00 00 	sub    rsp,0x90
   140007f68:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140007f6c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140007f70:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f74:	8b 50 14             	mov    edx,DWORD PTR [rax+0x14]
   140007f77:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007f7b:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007f7e:	39 c2                	cmp    edx,eax
   140007f80:	7d 18                	jge    140007f9a <__mult_D2A+0x3d>
   140007f82:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f86:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140007f8a:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007f8e:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   140007f92:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140007f96:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140007f9a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007f9e:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140007fa1:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140007fa4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007fa8:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007fab:	89 45 c4             	mov    DWORD PTR [rbp-0x3c],eax
   140007fae:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140007fb2:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140007fb5:	89 45 c0             	mov    DWORD PTR [rbp-0x40],eax
   140007fb8:	8b 55 c4             	mov    edx,DWORD PTR [rbp-0x3c]
   140007fbb:	8b 45 c0             	mov    eax,DWORD PTR [rbp-0x40]
   140007fbe:	01 d0                	add    eax,edx
   140007fc0:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140007fc3:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140007fc7:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   140007fca:	39 45 f8             	cmp    DWORD PTR [rbp-0x8],eax
   140007fcd:	7e 04                	jle    140007fd3 <__mult_D2A+0x76>
   140007fcf:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   140007fd3:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140007fd6:	89 c1                	mov    ecx,eax
   140007fd8:	e8 40 fc ff ff       	call   140007c1d <__Balloc_D2A>
   140007fdd:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140007fe1:	48 83 7d c8 00       	cmp    QWORD PTR [rbp-0x38],0x0
   140007fe6:	75 0a                	jne    140007ff2 <__mult_D2A+0x95>
   140007fe8:	b8 00 00 00 00       	mov    eax,0x0
   140007fed:	e9 88 01 00 00       	jmp    14000817a <__mult_D2A+0x21d>
   140007ff2:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140007ff6:	48 83 c0 18          	add    rax,0x18
   140007ffa:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140007ffe:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008001:	48 98                	cdqe
   140008003:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   14000800a:	00 
   14000800b:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000800f:	48 01 d0             	add    rax,rdx
   140008012:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   140008016:	eb 0f                	jmp    140008027 <__mult_D2A+0xca>
   140008018:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000801c:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140008022:	48 83 45 f0 04       	add    QWORD PTR [rbp-0x10],0x4
   140008027:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000802b:	48 3b 45 b8          	cmp    rax,QWORD PTR [rbp-0x48]
   14000802f:	72 e7                	jb     140008018 <__mult_D2A+0xbb>
   140008031:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008035:	48 83 c0 18          	add    rax,0x18
   140008039:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   14000803d:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
   140008040:	48 98                	cdqe
   140008042:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008049:	00 
   14000804a:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   14000804e:	48 01 d0             	add    rax,rdx
   140008051:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140008055:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008059:	48 83 c0 18          	add    rax,0x18
   14000805d:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008061:	8b 45 c0             	mov    eax,DWORD PTR [rbp-0x40]
   140008064:	48 98                	cdqe
   140008066:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   14000806d:	00 
   14000806e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008072:	48 01 d0             	add    rax,rdx
   140008075:	48 89 45 a8          	mov    QWORD PTR [rbp-0x58],rax
   140008079:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   14000807d:	48 83 c0 18          	add    rax,0x18
   140008081:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008085:	e9 95 00 00 00       	jmp    14000811f <__mult_D2A+0x1c2>
   14000808a:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000808e:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008092:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
   140008096:	8b 00                	mov    eax,DWORD PTR [rax]
   140008098:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
   14000809b:	83 7d a4 00          	cmp    DWORD PTR [rbp-0x5c],0x0
   14000809f:	74 79                	je     14000811a <__mult_D2A+0x1bd>
   1400080a1:	48 8b 45 b8          	mov    rax,QWORD PTR [rbp-0x48]
   1400080a5:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400080a9:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   1400080ad:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400080b1:	48 c7 45 d0 00 00 00 	mov    QWORD PTR [rbp-0x30],0x0
   1400080b8:	00 
   1400080b9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400080bd:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400080c1:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400080c5:	8b 00                	mov    eax,DWORD PTR [rax]
   1400080c7:	89 c2                	mov    edx,eax
   1400080c9:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
   1400080cc:	48 0f af d0          	imul   rdx,rax
   1400080d0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400080d4:	8b 00                	mov    eax,DWORD PTR [rax]
   1400080d6:	89 c0                	mov    eax,eax
   1400080d8:	48 01 c2             	add    rdx,rax
   1400080db:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400080df:	48 01 d0             	add    rax,rdx
   1400080e2:	48 89 45 98          	mov    QWORD PTR [rbp-0x68],rax
   1400080e6:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
   1400080ea:	48 c1 e8 20          	shr    rax,0x20
   1400080ee:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   1400080f2:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400080f6:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400080fa:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   1400080fe:	48 8b 55 98          	mov    rdx,QWORD PTR [rbp-0x68]
   140008102:	89 10                	mov    DWORD PTR [rax],edx
   140008104:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008108:	48 3b 45 b0          	cmp    rax,QWORD PTR [rbp-0x50]
   14000810c:	72 ab                	jb     1400080b9 <__mult_D2A+0x15c>
   14000810e:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008112:	89 c2                	mov    edx,eax
   140008114:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008118:	89 10                	mov    DWORD PTR [rax],edx
   14000811a:	48 83 45 d8 04       	add    QWORD PTR [rbp-0x28],0x4
   14000811f:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008123:	48 3b 45 a8          	cmp    rax,QWORD PTR [rbp-0x58]
   140008127:	0f 82 5d ff ff ff    	jb     14000808a <__mult_D2A+0x12d>
   14000812d:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140008131:	48 83 c0 18          	add    rax,0x18
   140008135:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008139:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   14000813c:	48 98                	cdqe
   14000813e:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008145:	00 
   140008146:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   14000814a:	48 01 d0             	add    rax,rdx
   14000814d:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140008151:	eb 04                	jmp    140008157 <__mult_D2A+0x1fa>
   140008153:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   140008157:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   14000815b:	7e 0f                	jle    14000816c <__mult_D2A+0x20f>
   14000815d:	48 83 6d e0 04       	sub    QWORD PTR [rbp-0x20],0x4
   140008162:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008166:	8b 00                	mov    eax,DWORD PTR [rax]
   140008168:	85 c0                	test   eax,eax
   14000816a:	74 e7                	je     140008153 <__mult_D2A+0x1f6>
   14000816c:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   140008170:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140008173:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140008176:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
   14000817a:	48 81 c4 90 00 00 00 	add    rsp,0x90
   140008181:	5d                   	pop    rbp
   140008182:	c3                   	ret

0000000140008183 <__pow5mult_D2A>:
   140008183:	55                   	push   rbp
   140008184:	48 89 e5             	mov    rbp,rsp
   140008187:	48 83 ec 40          	sub    rsp,0x40
   14000818b:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000818f:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   140008192:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140008195:	83 e0 03             	and    eax,0x3
   140008198:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   14000819b:	83 7d ec 00          	cmp    DWORD PTR [rbp-0x14],0x0
   14000819f:	74 41                	je     1400081e2 <__pow5mult_D2A+0x5f>
   1400081a1:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   1400081a4:	83 e8 01             	sub    eax,0x1
   1400081a7:	48 98                	cdqe
   1400081a9:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400081b0:	00 
   1400081b1:	48 8d 05 e0 1e 00 00 	lea    rax,[rip+0x1ee0]        # 14000a098 <p05.0>
   1400081b8:	8b 14 02             	mov    edx,DWORD PTR [rdx+rax*1]
   1400081bb:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400081bf:	41 b8 00 00 00 00    	mov    r8d,0x0
   1400081c5:	48 89 c1             	mov    rcx,rax
   1400081c8:	e8 1c fc ff ff       	call   140007de9 <__multadd_D2A>
   1400081cd:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400081d1:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400081d6:	75 0a                	jne    1400081e2 <__pow5mult_D2A+0x5f>
   1400081d8:	b8 00 00 00 00       	mov    eax,0x0
   1400081dd:	e9 58 01 00 00       	jmp    14000833a <__pow5mult_D2A+0x1b7>
   1400081e2:	c1 7d 18 02          	sar    DWORD PTR [rbp+0x18],0x2
   1400081e6:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   1400081ea:	75 09                	jne    1400081f5 <__pow5mult_D2A+0x72>
   1400081ec:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400081f0:	e9 45 01 00 00       	jmp    14000833a <__pow5mult_D2A+0x1b7>
   1400081f5:	48 8b 05 64 79 00 00 	mov    rax,QWORD PTR [rip+0x7964]        # 14000fb60 <p5s>
   1400081fc:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008200:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140008205:	75 5e                	jne    140008265 <__pow5mult_D2A+0xe2>
   140008207:	b9 01 00 00 00       	mov    ecx,0x1
   14000820c:	e8 51 f8 ff ff       	call   140007a62 <dtoa_lock>
   140008211:	48 8b 05 48 79 00 00 	mov    rax,QWORD PTR [rip+0x7948]        # 14000fb60 <p5s>
   140008218:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000821c:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140008221:	75 38                	jne    14000825b <__pow5mult_D2A+0xd8>
   140008223:	b9 71 02 00 00       	mov    ecx,0x271
   140008228:	e8 ea fc ff ff       	call   140007f17 <__i2b_D2A>
   14000822d:	48 89 05 2c 79 00 00 	mov    QWORD PTR [rip+0x792c],rax        # 14000fb60 <p5s>
   140008234:	48 8b 05 25 79 00 00 	mov    rax,QWORD PTR [rip+0x7925]        # 14000fb60 <p5s>
   14000823b:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   14000823f:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   140008244:	75 0a                	jne    140008250 <__pow5mult_D2A+0xcd>
   140008246:	b8 00 00 00 00       	mov    eax,0x0
   14000824b:	e9 ea 00 00 00       	jmp    14000833a <__pow5mult_D2A+0x1b7>
   140008250:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008254:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   14000825b:	b9 01 00 00 00       	mov    ecx,0x1
   140008260:	e8 2f f9 ff ff       	call   140007b94 <dtoa_unlock>
   140008265:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140008268:	83 e0 01             	and    eax,0x1
   14000826b:	85 c0                	test   eax,eax
   14000826d:	74 39                	je     1400082a8 <__pow5mult_D2A+0x125>
   14000826f:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   140008273:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008277:	48 89 c1             	mov    rcx,rax
   14000827a:	e8 de fc ff ff       	call   140007f5d <__mult_D2A>
   14000827f:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140008283:	48 83 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
   140008288:	75 0a                	jne    140008294 <__pow5mult_D2A+0x111>
   14000828a:	b8 00 00 00 00       	mov    eax,0x0
   14000828f:	e9 a6 00 00 00       	jmp    14000833a <__pow5mult_D2A+0x1b7>
   140008294:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008298:	48 89 c1             	mov    rcx,rax
   14000829b:	e8 be fa ff ff       	call   140007d5e <__Bfree_D2A>
   1400082a0:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400082a4:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   1400082a8:	d1 7d 18             	sar    DWORD PTR [rbp+0x18],1
   1400082ab:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   1400082af:	0f 84 80 00 00 00    	je     140008335 <__pow5mult_D2A+0x1b2>
   1400082b5:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082b9:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400082bc:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400082c0:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400082c5:	75 61                	jne    140008328 <__pow5mult_D2A+0x1a5>
   1400082c7:	b9 01 00 00 00       	mov    ecx,0x1
   1400082cc:	e8 91 f7 ff ff       	call   140007a62 <dtoa_lock>
   1400082d1:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082d5:	48 8b 00             	mov    rax,QWORD PTR [rax]
   1400082d8:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400082dc:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400082e1:	75 3b                	jne    14000831e <__pow5mult_D2A+0x19b>
   1400082e3:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400082e7:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082eb:	48 89 c1             	mov    rcx,rax
   1400082ee:	e8 6a fc ff ff       	call   140007f5d <__mult_D2A>
   1400082f3:	48 8b 55 f8          	mov    rdx,QWORD PTR [rbp-0x8]
   1400082f7:	48 89 02             	mov    QWORD PTR [rdx],rax
   1400082fa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400082fe:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008301:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140008305:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   14000830a:	75 07                	jne    140008313 <__pow5mult_D2A+0x190>
   14000830c:	b8 00 00 00 00       	mov    eax,0x0
   140008311:	eb 27                	jmp    14000833a <__pow5mult_D2A+0x1b7>
   140008313:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008317:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
   14000831e:	b9 01 00 00 00       	mov    ecx,0x1
   140008323:	e8 6c f8 ff ff       	call   140007b94 <dtoa_unlock>
   140008328:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000832c:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008330:	e9 30 ff ff ff       	jmp    140008265 <__pow5mult_D2A+0xe2>
   140008335:	90                   	nop
   140008336:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000833a:	48 83 c4 40          	add    rsp,0x40
   14000833e:	5d                   	pop    rbp
   14000833f:	c3                   	ret

0000000140008340 <__lshift_D2A>:
   140008340:	55                   	push   rbp
   140008341:	48 89 e5             	mov    rbp,rsp
   140008344:	48 83 ec 60          	sub    rsp,0x60
   140008348:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000834c:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   14000834f:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   140008352:	c1 f8 05             	sar    eax,0x5
   140008355:	89 45 d8             	mov    DWORD PTR [rbp-0x28],eax
   140008358:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000835c:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   14000835f:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008362:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008366:	8b 50 14             	mov    edx,DWORD PTR [rax+0x14]
   140008369:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
   14000836c:	01 d0                	add    eax,edx
   14000836e:	83 c0 01             	add    eax,0x1
   140008371:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140008374:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008378:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
   14000837b:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   14000837e:	eb 07                	jmp    140008387 <__lshift_D2A+0x47>
   140008380:	83 45 f8 01          	add    DWORD PTR [rbp-0x8],0x1
   140008384:	d1 65 fc             	shl    DWORD PTR [rbp-0x4],1
   140008387:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   14000838a:	3b 45 fc             	cmp    eax,DWORD PTR [rbp-0x4]
   14000838d:	7f f1                	jg     140008380 <__lshift_D2A+0x40>
   14000838f:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008392:	89 c1                	mov    ecx,eax
   140008394:	e8 84 f8 ff ff       	call   140007c1d <__Balloc_D2A>
   140008399:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   14000839d:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   1400083a2:	75 0a                	jne    1400083ae <__lshift_D2A+0x6e>
   1400083a4:	b8 00 00 00 00       	mov    eax,0x0
   1400083a9:	e9 19 01 00 00       	jmp    1400084c7 <__lshift_D2A+0x187>
   1400083ae:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400083b2:	48 83 c0 18          	add    rax,0x18
   1400083b6:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400083ba:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   1400083c1:	eb 16                	jmp    1400083d9 <__lshift_D2A+0x99>
   1400083c3:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400083c7:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400083cb:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   1400083cf:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400083d5:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
   1400083d9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400083dc:	3b 45 d8             	cmp    eax,DWORD PTR [rbp-0x28]
   1400083df:	7c e2                	jl     1400083c3 <__lshift_D2A+0x83>
   1400083e1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400083e5:	48 83 c0 18          	add    rax,0x18
   1400083e9:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400083ed:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400083f1:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400083f4:	48 98                	cdqe
   1400083f6:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400083fd:	00 
   1400083fe:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008402:	48 01 d0             	add    rax,rdx
   140008405:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   140008409:	83 65 18 1f          	and    DWORD PTR [rbp+0x18],0x1f
   14000840d:	83 7d 18 00          	cmp    DWORD PTR [rbp+0x18],0x0
   140008411:	74 71                	je     140008484 <__lshift_D2A+0x144>
   140008413:	b8 20 00 00 00       	mov    eax,0x20
   140008418:	2b 45 18             	sub    eax,DWORD PTR [rbp+0x18]
   14000841b:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   14000841e:	c7 45 dc 00 00 00 00 	mov    DWORD PTR [rbp-0x24],0x0
   140008425:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008429:	8b 10                	mov    edx,DWORD PTR [rax]
   14000842b:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000842e:	89 c1                	mov    ecx,eax
   140008430:	d3 e2                	shl    edx,cl
   140008432:	89 d1                	mov    ecx,edx
   140008434:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008438:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000843c:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   140008440:	0b 4d dc             	or     ecx,DWORD PTR [rbp-0x24]
   140008443:	89 ca                	mov    edx,ecx
   140008445:	89 10                	mov    DWORD PTR [rax],edx
   140008447:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000844b:	48 8d 50 04          	lea    rdx,[rax+0x4]
   14000844f:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
   140008453:	8b 10                	mov    edx,DWORD PTR [rax]
   140008455:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008458:	89 c1                	mov    ecx,eax
   14000845a:	d3 ea                	shr    edx,cl
   14000845c:	89 d0                	mov    eax,edx
   14000845e:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   140008461:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008465:	48 3b 45 c8          	cmp    rax,QWORD PTR [rbp-0x38]
   140008469:	72 ba                	jb     140008425 <__lshift_D2A+0xe5>
   14000846b:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   14000846f:	8b 55 dc             	mov    edx,DWORD PTR [rbp-0x24]
   140008472:	89 10                	mov    DWORD PTR [rax],edx
   140008474:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008478:	8b 00                	mov    eax,DWORD PTR [rax]
   14000847a:	85 c0                	test   eax,eax
   14000847c:	74 2c                	je     1400084aa <__lshift_D2A+0x16a>
   14000847e:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
   140008482:	eb 26                	jmp    1400084aa <__lshift_D2A+0x16a>
   140008484:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
   140008488:	48 8d 42 04          	lea    rax,[rdx+0x4]
   14000848c:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008490:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008494:	48 8d 48 04          	lea    rcx,[rax+0x4]
   140008498:	48 89 4d e0          	mov    QWORD PTR [rbp-0x20],rcx
   14000849c:	8b 12                	mov    edx,DWORD PTR [rdx]
   14000849e:	89 10                	mov    DWORD PTR [rax],edx
   1400084a0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400084a4:	48 3b 45 c8          	cmp    rax,QWORD PTR [rbp-0x38]
   1400084a8:	72 da                	jb     140008484 <__lshift_D2A+0x144>
   1400084aa:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   1400084ad:	8d 50 ff             	lea    edx,[rax-0x1]
   1400084b0:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400084b4:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   1400084b7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400084bb:	48 89 c1             	mov    rcx,rax
   1400084be:	e8 9b f8 ff ff       	call   140007d5e <__Bfree_D2A>
   1400084c3:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400084c7:	48 83 c4 60          	add    rsp,0x60
   1400084cb:	5d                   	pop    rbp
   1400084cc:	c3                   	ret

00000001400084cd <__cmp_D2A>:
   1400084cd:	55                   	push   rbp
   1400084ce:	48 89 e5             	mov    rbp,rsp
   1400084d1:	48 83 ec 30          	sub    rsp,0x30
   1400084d5:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400084d9:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400084dd:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400084e1:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400084e4:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   1400084e7:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400084eb:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400084ee:	89 45 e8             	mov    DWORD PTR [rbp-0x18],eax
   1400084f1:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   1400084f4:	29 45 ec             	sub    DWORD PTR [rbp-0x14],eax
   1400084f7:	83 7d ec 00          	cmp    DWORD PTR [rbp-0x14],0x0
   1400084fb:	74 08                	je     140008505 <__cmp_D2A+0x38>
   1400084fd:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   140008500:	e9 92 00 00 00       	jmp    140008597 <__cmp_D2A+0xca>
   140008505:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008509:	48 83 c0 18          	add    rax,0x18
   14000850d:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140008511:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140008514:	48 98                	cdqe
   140008516:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   14000851d:	00 
   14000851e:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008522:	48 01 d0             	add    rax,rdx
   140008525:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008529:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000852d:	48 83 c0 18          	add    rax,0x18
   140008531:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008535:	8b 45 e8             	mov    eax,DWORD PTR [rbp-0x18]
   140008538:	48 98                	cdqe
   14000853a:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008541:	00 
   140008542:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
   140008546:	48 01 d0             	add    rax,rdx
   140008549:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000854d:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   140008552:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008556:	8b 10                	mov    edx,DWORD PTR [rax]
   140008558:	48 83 6d f0 04       	sub    QWORD PTR [rbp-0x10],0x4
   14000855d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008561:	8b 00                	mov    eax,DWORD PTR [rax]
   140008563:	39 c2                	cmp    edx,eax
   140008565:	74 1e                	je     140008585 <__cmp_D2A+0xb8>
   140008567:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000856b:	8b 10                	mov    edx,DWORD PTR [rax]
   14000856d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008571:	8b 00                	mov    eax,DWORD PTR [rax]
   140008573:	39 c2                	cmp    edx,eax
   140008575:	73 07                	jae    14000857e <__cmp_D2A+0xb1>
   140008577:	b8 ff ff ff ff       	mov    eax,0xffffffff
   14000857c:	eb 19                	jmp    140008597 <__cmp_D2A+0xca>
   14000857e:	b8 01 00 00 00       	mov    eax,0x1
   140008583:	eb 12                	jmp    140008597 <__cmp_D2A+0xca>
   140008585:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008589:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   14000858d:	73 02                	jae    140008591 <__cmp_D2A+0xc4>
   14000858f:	eb bc                	jmp    14000854d <__cmp_D2A+0x80>
   140008591:	90                   	nop
   140008592:	b8 00 00 00 00       	mov    eax,0x0
   140008597:	48 83 c4 30          	add    rsp,0x30
   14000859b:	5d                   	pop    rbp
   14000859c:	c3                   	ret

000000014000859d <__diff_D2A>:
   14000859d:	55                   	push   rbp
   14000859e:	48 89 e5             	mov    rbp,rsp
   1400085a1:	48 83 ec 70          	sub    rsp,0x70
   1400085a5:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400085a9:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400085ad:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   1400085b1:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400085b5:	48 89 c1             	mov    rcx,rax
   1400085b8:	e8 10 ff ff ff       	call   1400084cd <__cmp_D2A>
   1400085bd:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   1400085c0:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   1400085c4:	75 3e                	jne    140008604 <__diff_D2A+0x67>
   1400085c6:	b9 00 00 00 00       	mov    ecx,0x0
   1400085cb:	e8 4d f6 ff ff       	call   140007c1d <__Balloc_D2A>
   1400085d0:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   1400085d4:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   1400085d9:	75 0a                	jne    1400085e5 <__diff_D2A+0x48>
   1400085db:	b8 00 00 00 00       	mov    eax,0x0
   1400085e0:	e9 ab 01 00 00       	jmp    140008790 <__diff_D2A+0x1f3>
   1400085e5:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400085e9:	c7 40 14 01 00 00 00 	mov    DWORD PTR [rax+0x14],0x1
   1400085f0:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400085f4:	c7 40 18 00 00 00 00 	mov    DWORD PTR [rax+0x18],0x0
   1400085fb:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400085ff:	e9 8c 01 00 00       	jmp    140008790 <__diff_D2A+0x1f3>
   140008604:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140008608:	79 21                	jns    14000862b <__diff_D2A+0x8e>
   14000860a:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000860e:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140008612:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008616:	48 89 45 10          	mov    QWORD PTR [rbp+0x10],rax
   14000861a:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   14000861e:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140008622:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   140008629:	eb 07                	jmp    140008632 <__diff_D2A+0x95>
   14000862b:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140008632:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008636:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
   140008639:	89 c1                	mov    ecx,eax
   14000863b:	e8 dd f5 ff ff       	call   140007c1d <__Balloc_D2A>
   140008640:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
   140008644:	48 83 7d d0 00       	cmp    QWORD PTR [rbp-0x30],0x0
   140008649:	75 0a                	jne    140008655 <__diff_D2A+0xb8>
   14000864b:	b8 00 00 00 00       	mov    eax,0x0
   140008650:	e9 3b 01 00 00       	jmp    140008790 <__diff_D2A+0x1f3>
   140008655:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008659:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   14000865c:	89 50 10             	mov    DWORD PTR [rax+0x10],edx
   14000865f:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008663:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008666:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008669:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000866d:	48 83 c0 18          	add    rax,0x18
   140008671:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140008675:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008678:	48 98                	cdqe
   14000867a:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   140008681:	00 
   140008682:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008686:	48 01 d0             	add    rax,rdx
   140008689:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
   14000868d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008691:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008694:	89 45 c4             	mov    DWORD PTR [rbp-0x3c],eax
   140008697:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000869b:	48 83 c0 18          	add    rax,0x18
   14000869f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   1400086a3:	8b 45 c4             	mov    eax,DWORD PTR [rbp-0x3c]
   1400086a6:	48 98                	cdqe
   1400086a8:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400086af:	00 
   1400086b0:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400086b4:	48 01 d0             	add    rax,rdx
   1400086b7:	48 89 45 b8          	mov    QWORD PTR [rbp-0x48],rax
   1400086bb:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   1400086bf:	48 83 c0 18          	add    rax,0x18
   1400086c3:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400086c7:	48 c7 45 d8 00 00 00 	mov    QWORD PTR [rbp-0x28],0x0
   1400086ce:	00 
   1400086cf:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400086d3:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400086d7:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   1400086db:	8b 00                	mov    eax,DWORD PTR [rax]
   1400086dd:	89 c1                	mov    ecx,eax
   1400086df:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400086e3:	48 8d 50 04          	lea    rdx,[rax+0x4]
   1400086e7:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
   1400086eb:	8b 00                	mov    eax,DWORD PTR [rax]
   1400086ed:	89 c2                	mov    edx,eax
   1400086ef:	48 89 c8             	mov    rax,rcx
   1400086f2:	48 29 d0             	sub    rax,rdx
   1400086f5:	48 2b 45 d8          	sub    rax,QWORD PTR [rbp-0x28]
   1400086f9:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   1400086fd:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140008701:	48 c1 e8 20          	shr    rax,0x20
   140008705:	83 e0 01             	and    eax,0x1
   140008708:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   14000870c:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008710:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008714:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   140008718:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   14000871c:	89 10                	mov    DWORD PTR [rax],edx
   14000871e:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008722:	48 3b 45 b8          	cmp    rax,QWORD PTR [rbp-0x48]
   140008726:	72 a7                	jb     1400086cf <__diff_D2A+0x132>
   140008728:	eb 39                	jmp    140008763 <__diff_D2A+0x1c6>
   14000872a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   14000872e:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008732:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx
   140008736:	8b 00                	mov    eax,DWORD PTR [rax]
   140008738:	89 c0                	mov    eax,eax
   14000873a:	48 2b 45 d8          	sub    rax,QWORD PTR [rbp-0x28]
   14000873e:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
   140008742:	48 8b 45 b0          	mov    rax,QWORD PTR [rbp-0x50]
   140008746:	48 c1 e8 20          	shr    rax,0x20
   14000874a:	83 e0 01             	and    eax,0x1
   14000874d:	48 89 45 d8          	mov    QWORD PTR [rbp-0x28],rax
   140008751:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   140008755:	48 8d 50 04          	lea    rdx,[rax+0x4]
   140008759:	48 89 55 e0          	mov    QWORD PTR [rbp-0x20],rdx
   14000875d:	48 8b 55 b0          	mov    rdx,QWORD PTR [rbp-0x50]
   140008761:	89 10                	mov    DWORD PTR [rax],edx
   140008763:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008767:	48 3b 45 c8          	cmp    rax,QWORD PTR [rbp-0x38]
   14000876b:	72 bd                	jb     14000872a <__diff_D2A+0x18d>
   14000876d:	eb 04                	jmp    140008773 <__diff_D2A+0x1d6>
   14000876f:	83 6d f8 01          	sub    DWORD PTR [rbp-0x8],0x1
   140008773:	48 83 6d e0 04       	sub    QWORD PTR [rbp-0x20],0x4
   140008778:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   14000877c:	8b 00                	mov    eax,DWORD PTR [rax]
   14000877e:	85 c0                	test   eax,eax
   140008780:	74 ed                	je     14000876f <__diff_D2A+0x1d2>
   140008782:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008786:	8b 55 f8             	mov    edx,DWORD PTR [rbp-0x8]
   140008789:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   14000878c:	48 8b 45 d0          	mov    rax,QWORD PTR [rbp-0x30]
   140008790:	48 83 c4 70          	add    rsp,0x70
   140008794:	5d                   	pop    rbp
   140008795:	c3                   	ret

0000000140008796 <__b2d_D2A>:
   140008796:	55                   	push   rbp
   140008797:	48 89 e5             	mov    rbp,rsp
   14000879a:	48 83 ec 50          	sub    rsp,0x50
   14000879e:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400087a2:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   1400087a6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400087aa:	48 83 c0 18          	add    rax,0x18
   1400087ae:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   1400087b2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400087b6:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   1400087b9:	48 98                	cdqe
   1400087bb:	48 8d 14 85 00 00 00 	lea    rdx,[rax*4+0x0]
   1400087c2:	00 
   1400087c3:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
   1400087c7:	48 01 d0             	add    rax,rdx
   1400087ca:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400087ce:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   1400087d3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400087d7:	8b 00                	mov    eax,DWORD PTR [rax]
   1400087d9:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   1400087dc:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   1400087df:	89 c1                	mov    ecx,eax
   1400087e1:	e8 27 f4 ff ff       	call   140007c0d <__hi0bits_D2A>
   1400087e6:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   1400087e9:	b8 20 00 00 00       	mov    eax,0x20
   1400087ee:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   1400087f1:	89 c2                	mov    edx,eax
   1400087f3:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400087f7:	89 10                	mov    DWORD PTR [rax],edx
   1400087f9:	83 7d dc 0a          	cmp    DWORD PTR [rbp-0x24],0xa
   1400087fd:	7f 66                	jg     140008865 <__b2d_D2A+0xcf>
   1400087ff:	b8 0b 00 00 00       	mov    eax,0xb
   140008804:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   140008807:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   14000880a:	89 c1                	mov    ecx,eax
   14000880c:	d3 ea                	shr    edx,cl
   14000880e:	89 d0                	mov    eax,edx
   140008810:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   140008815:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   140008818:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000881c:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   140008820:	73 10                	jae    140008832 <__b2d_D2A+0x9c>
   140008822:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   140008827:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000882b:	8b 00                	mov    eax,DWORD PTR [rax]
   14000882d:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140008830:	eb 07                	jmp    140008839 <__b2d_D2A+0xa3>
   140008832:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [rbp-0xc],0x0
   140008839:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   14000883c:	83 c0 15             	add    eax,0x15
   14000883f:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   140008842:	89 c1                	mov    ecx,eax
   140008844:	d3 e2                	shl    edx,cl
   140008846:	41 89 d0             	mov    r8d,edx
   140008849:	b8 0b 00 00 00       	mov    eax,0xb
   14000884e:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   140008851:	8b 55 f4             	mov    edx,DWORD PTR [rbp-0xc]
   140008854:	89 c1                	mov    ecx,eax
   140008856:	d3 ea                	shr    edx,cl
   140008858:	89 d0                	mov    eax,edx
   14000885a:	44 09 c0             	or     eax,r8d
   14000885d:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008860:	e9 ac 00 00 00       	jmp    140008911 <__b2d_D2A+0x17b>
   140008865:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008869:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   14000886d:	73 10                	jae    14000887f <__b2d_D2A+0xe9>
   14000886f:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   140008874:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008878:	8b 00                	mov    eax,DWORD PTR [rax]
   14000887a:	89 45 ec             	mov    DWORD PTR [rbp-0x14],eax
   14000887d:	eb 07                	jmp    140008886 <__b2d_D2A+0xf0>
   14000887f:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [rbp-0x14],0x0
   140008886:	83 6d dc 0b          	sub    DWORD PTR [rbp-0x24],0xb
   14000888a:	83 7d dc 00          	cmp    DWORD PTR [rbp-0x24],0x0
   14000888e:	74 70                	je     140008900 <__b2d_D2A+0x16a>
   140008890:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140008893:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   140008896:	89 c1                	mov    ecx,eax
   140008898:	d3 e2                	shl    edx,cl
   14000889a:	41 89 d0             	mov    r8d,edx
   14000889d:	b8 20 00 00 00       	mov    eax,0x20
   1400088a2:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   1400088a5:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   1400088a8:	89 c1                	mov    ecx,eax
   1400088aa:	d3 ea                	shr    edx,cl
   1400088ac:	89 d0                	mov    eax,edx
   1400088ae:	44 09 c0             	or     eax,r8d
   1400088b1:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   1400088b6:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   1400088b9:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400088bd:	48 39 45 e0          	cmp    QWORD PTR [rbp-0x20],rax
   1400088c1:	73 10                	jae    1400088d3 <__b2d_D2A+0x13d>
   1400088c3:	48 83 6d f8 04       	sub    QWORD PTR [rbp-0x8],0x4
   1400088c8:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   1400088cc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400088ce:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   1400088d1:	eb 07                	jmp    1400088da <__b2d_D2A+0x144>
   1400088d3:	c7 45 f0 00 00 00 00 	mov    DWORD PTR [rbp-0x10],0x0
   1400088da:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   1400088dd:	8b 55 ec             	mov    edx,DWORD PTR [rbp-0x14]
   1400088e0:	89 c1                	mov    ecx,eax
   1400088e2:	d3 e2                	shl    edx,cl
   1400088e4:	41 89 d0             	mov    r8d,edx
   1400088e7:	b8 20 00 00 00       	mov    eax,0x20
   1400088ec:	2b 45 dc             	sub    eax,DWORD PTR [rbp-0x24]
   1400088ef:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   1400088f2:	89 c1                	mov    ecx,eax
   1400088f4:	d3 ea                	shr    edx,cl
   1400088f6:	89 d0                	mov    eax,edx
   1400088f8:	44 09 c0             	or     eax,r8d
   1400088fb:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   1400088fe:	eb 11                	jmp    140008911 <__b2d_D2A+0x17b>
   140008900:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140008903:	0d 00 00 f0 3f       	or     eax,0x3ff00000
   140008908:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000890b:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
   14000890e:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008911:	f2 0f 10 45 d0       	movsd  xmm0,QWORD PTR [rbp-0x30]
   140008916:	48 83 c4 50          	add    rsp,0x50
   14000891a:	5d                   	pop    rbp
   14000891b:	c3                   	ret

000000014000891c <__d2b_D2A>:
   14000891c:	55                   	push   rbp
   14000891d:	53                   	push   rbx
   14000891e:	48 83 ec 58          	sub    rsp,0x58
   140008922:	48 8d 6c 24 50       	lea    rbp,[rsp+0x50]
   140008927:	f2 0f 11 45 20       	movsd  QWORD PTR [rbp+0x20],xmm0
   14000892c:	48 89 55 28          	mov    QWORD PTR [rbp+0x28],rdx
   140008930:	4c 89 45 30          	mov    QWORD PTR [rbp+0x30],r8
   140008934:	f2 0f 10 45 20       	movsd  xmm0,QWORD PTR [rbp+0x20]
   140008939:	f2 0f 11 45 d8       	movsd  QWORD PTR [rbp-0x28],xmm0
   14000893e:	b9 01 00 00 00       	mov    ecx,0x1
   140008943:	e8 d5 f2 ff ff       	call   140007c1d <__Balloc_D2A>
   140008948:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   14000894c:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   140008951:	75 0a                	jne    14000895d <__d2b_D2A+0x41>
   140008953:	b8 00 00 00 00       	mov    eax,0x0
   140008958:	e9 68 01 00 00       	jmp    140008ac5 <__d2b_D2A+0x1a9>
   14000895d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008961:	48 83 c0 18          	add    rax,0x18
   140008965:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   140008969:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   14000896c:	25 ff ff 0f 00       	and    eax,0xfffff
   140008971:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008974:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140008977:	25 ff ff ff 7f       	and    eax,0x7fffffff
   14000897c:	89 45 dc             	mov    DWORD PTR [rbp-0x24],eax
   14000897f:	8b 45 dc             	mov    eax,DWORD PTR [rbp-0x24]
   140008982:	c1 e8 14             	shr    eax,0x14
   140008985:	89 45 e4             	mov    DWORD PTR [rbp-0x1c],eax
   140008988:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   14000898c:	74 0b                	je     140008999 <__d2b_D2A+0x7d>
   14000898e:	8b 45 d0             	mov    eax,DWORD PTR [rbp-0x30]
   140008991:	0d 00 00 10 00       	or     eax,0x100000
   140008996:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   140008999:	8b 45 d8             	mov    eax,DWORD PTR [rbp-0x28]
   14000899c:	89 45 d4             	mov    DWORD PTR [rbp-0x2c],eax
   14000899f:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400089a2:	85 c0                	test   eax,eax
   1400089a4:	74 7b                	je     140008a21 <__d2b_D2A+0x105>
   1400089a6:	48 8d 45 d4          	lea    rax,[rbp-0x2c]
   1400089aa:	48 89 c1             	mov    rcx,rax
   1400089ad:	e8 26 f2 ff ff       	call   140007bd8 <__lo0bits_D2A>
   1400089b2:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   1400089b5:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   1400089b9:	74 2b                	je     1400089e6 <__d2b_D2A+0xca>
   1400089bb:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   1400089be:	b8 20 00 00 00       	mov    eax,0x20
   1400089c3:	2b 45 f8             	sub    eax,DWORD PTR [rbp-0x8]
   1400089c6:	89 c1                	mov    ecx,eax
   1400089c8:	d3 e2                	shl    edx,cl
   1400089ca:	8b 45 d4             	mov    eax,DWORD PTR [rbp-0x2c]
   1400089cd:	09 c2                	or     edx,eax
   1400089cf:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400089d3:	89 10                	mov    DWORD PTR [rax],edx
   1400089d5:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   1400089d8:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   1400089db:	89 c1                	mov    ecx,eax
   1400089dd:	d3 ea                	shr    edx,cl
   1400089df:	89 d0                	mov    eax,edx
   1400089e1:	89 45 d0             	mov    DWORD PTR [rbp-0x30],eax
   1400089e4:	eb 09                	jmp    1400089ef <__d2b_D2A+0xd3>
   1400089e6:	8b 55 d4             	mov    edx,DWORD PTR [rbp-0x2c]
   1400089e9:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400089ed:	89 10                	mov    DWORD PTR [rax],edx
   1400089ef:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   1400089f3:	48 83 c0 04          	add    rax,0x4
   1400089f7:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   1400089fa:	89 10                	mov    DWORD PTR [rax],edx
   1400089fc:	8b 00                	mov    eax,DWORD PTR [rax]
   1400089fe:	85 c0                	test   eax,eax
   140008a00:	74 07                	je     140008a09 <__d2b_D2A+0xed>
   140008a02:	ba 02 00 00 00       	mov    edx,0x2
   140008a07:	eb 05                	jmp    140008a0e <__d2b_D2A+0xf2>
   140008a09:	ba 01 00 00 00       	mov    edx,0x1
   140008a0e:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a12:	89 50 14             	mov    DWORD PTR [rax+0x14],edx
   140008a15:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a19:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008a1c:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008a1f:	eb 31                	jmp    140008a52 <__d2b_D2A+0x136>
   140008a21:	48 8d 45 d0          	lea    rax,[rbp-0x30]
   140008a25:	48 89 c1             	mov    rcx,rax
   140008a28:	e8 ab f1 ff ff       	call   140007bd8 <__lo0bits_D2A>
   140008a2d:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008a30:	8b 55 d0             	mov    edx,DWORD PTR [rbp-0x30]
   140008a33:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008a37:	89 10                	mov    DWORD PTR [rax],edx
   140008a39:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a3d:	c7 40 14 01 00 00 00 	mov    DWORD PTR [rax+0x14],0x1
   140008a44:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008a48:	8b 40 14             	mov    eax,DWORD PTR [rax+0x14]
   140008a4b:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008a4e:	83 45 f8 20          	add    DWORD PTR [rbp-0x8],0x20
   140008a52:	83 7d e4 00          	cmp    DWORD PTR [rbp-0x1c],0x0
   140008a56:	74 26                	je     140008a7e <__d2b_D2A+0x162>
   140008a58:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008a5b:	8d 90 cd fb ff ff    	lea    edx,[rax-0x433]
   140008a61:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008a64:	01 c2                	add    edx,eax
   140008a66:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140008a6a:	89 10                	mov    DWORD PTR [rax],edx
   140008a6c:	b8 35 00 00 00       	mov    eax,0x35
   140008a71:	2b 45 f8             	sub    eax,DWORD PTR [rbp-0x8]
   140008a74:	89 c2                	mov    edx,eax
   140008a76:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140008a7a:	89 10                	mov    DWORD PTR [rax],edx
   140008a7c:	eb 43                	jmp    140008ac1 <__d2b_D2A+0x1a5>
   140008a7e:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008a81:	8d 90 ce fb ff ff    	lea    edx,[rax-0x432]
   140008a87:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008a8a:	01 c2                	add    edx,eax
   140008a8c:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140008a90:	89 10                	mov    DWORD PTR [rax],edx
   140008a92:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008a95:	c1 e0 05             	shl    eax,0x5
   140008a98:	89 c3                	mov    ebx,eax
   140008a9a:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008a9d:	48 98                	cdqe
   140008a9f:	48 c1 e0 02          	shl    rax,0x2
   140008aa3:	48 8d 50 fc          	lea    rdx,[rax-0x4]
   140008aa7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   140008aab:	48 01 d0             	add    rax,rdx
   140008aae:	8b 00                	mov    eax,DWORD PTR [rax]
   140008ab0:	89 c1                	mov    ecx,eax
   140008ab2:	e8 56 f1 ff ff       	call   140007c0d <__hi0bits_D2A>
   140008ab7:	29 c3                	sub    ebx,eax
   140008ab9:	89 da                	mov    edx,ebx
   140008abb:	48 8b 45 30          	mov    rax,QWORD PTR [rbp+0x30]
   140008abf:	89 10                	mov    DWORD PTR [rax],edx
   140008ac1:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   140008ac5:	48 83 c4 58          	add    rsp,0x58
   140008ac9:	5b                   	pop    rbx
   140008aca:	5d                   	pop    rbp
   140008acb:	c3                   	ret

0000000140008acc <__strcp_D2A>:
   140008acc:	55                   	push   rbp
   140008acd:	48 89 e5             	mov    rbp,rsp
   140008ad0:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008ad4:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008ad8:	eb 05                	jmp    140008adf <__strcp_D2A+0x13>
   140008ada:	48 83 45 10 01       	add    QWORD PTR [rbp+0x10],0x1
   140008adf:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140008ae3:	48 8d 50 01          	lea    rdx,[rax+0x1]
   140008ae7:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008aeb:	0f b6 10             	movzx  edx,BYTE PTR [rax]
   140008aee:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008af2:	88 10                	mov    BYTE PTR [rax],dl
   140008af4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008af8:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140008afb:	84 c0                	test   al,al
   140008afd:	75 db                	jne    140008ada <__strcp_D2A+0xe>
   140008aff:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008b03:	5d                   	pop    rbp
   140008b04:	c3                   	ret
   140008b05:	90                   	nop
   140008b06:	90                   	nop
   140008b07:	90                   	nop
   140008b08:	90                   	nop
   140008b09:	90                   	nop
   140008b0a:	90                   	nop
   140008b0b:	90                   	nop
   140008b0c:	90                   	nop
   140008b0d:	90                   	nop
   140008b0e:	90                   	nop
   140008b0f:	90                   	nop

0000000140008b10 <__fpclassify>:
   140008b10:	55                   	push   rbp
   140008b11:	48 89 e5             	mov    rbp,rsp
   140008b14:	48 83 ec 10          	sub    rsp,0x10
   140008b18:	f2 0f 11 45 10       	movsd  QWORD PTR [rbp+0x10],xmm0
   140008b1d:	f2 0f 10 45 10       	movsd  xmm0,QWORD PTR [rbp+0x10]
   140008b22:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140008b27:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140008b2a:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008b2d:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140008b30:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
   140008b33:	81 e2 ff ff 0f 00    	and    edx,0xfffff
   140008b39:	09 d0                	or     eax,edx
   140008b3b:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008b3e:	81 65 fc 00 00 f0 7f 	and    DWORD PTR [rbp-0x4],0x7ff00000
   140008b45:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008b48:	0b 45 f8             	or     eax,DWORD PTR [rbp-0x8]
   140008b4b:	85 c0                	test   eax,eax
   140008b4d:	75 07                	jne    140008b56 <__fpclassify+0x46>
   140008b4f:	b8 00 40 00 00       	mov    eax,0x4000
   140008b54:	eb 2f                	jmp    140008b85 <__fpclassify+0x75>
   140008b56:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140008b5a:	75 07                	jne    140008b63 <__fpclassify+0x53>
   140008b5c:	b8 00 44 00 00       	mov    eax,0x4400
   140008b61:	eb 22                	jmp    140008b85 <__fpclassify+0x75>
   140008b63:	81 7d fc 00 00 f0 7f 	cmp    DWORD PTR [rbp-0x4],0x7ff00000
   140008b6a:	75 14                	jne    140008b80 <__fpclassify+0x70>
   140008b6c:	83 7d f8 00          	cmp    DWORD PTR [rbp-0x8],0x0
   140008b70:	74 07                	je     140008b79 <__fpclassify+0x69>
   140008b72:	b8 00 01 00 00       	mov    eax,0x100
   140008b77:	eb 0c                	jmp    140008b85 <__fpclassify+0x75>
   140008b79:	b8 00 05 00 00       	mov    eax,0x500
   140008b7e:	eb 05                	jmp    140008b85 <__fpclassify+0x75>
   140008b80:	b8 00 04 00 00       	mov    eax,0x400
   140008b85:	48 83 c4 10          	add    rsp,0x10
   140008b89:	5d                   	pop    rbp
   140008b8a:	c3                   	ret
   140008b8b:	90                   	nop
   140008b8c:	90                   	nop
   140008b8d:	90                   	nop
   140008b8e:	90                   	nop
   140008b8f:	90                   	nop

0000000140008b90 <__fpclassifyl>:
   140008b90:	55                   	push   rbp
   140008b91:	53                   	push   rbx
   140008b92:	48 83 ec 38          	sub    rsp,0x38
   140008b96:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140008b9b:	48 89 cb             	mov    rbx,rcx
   140008b9e:	db 2b                	fld    TBYTE PTR [rbx]
   140008ba0:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140008ba3:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140008ba6:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140008ba9:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140008bad:	98                   	cwde
   140008bae:	25 ff 7f 00 00       	and    eax,0x7fff
   140008bb3:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008bb6:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   140008bba:	75 25                	jne    140008be1 <__fpclassifyl+0x51>
   140008bbc:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008bbf:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008bc2:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140008bc5:	0b 45 f8             	or     eax,DWORD PTR [rbp-0x8]
   140008bc8:	85 c0                	test   eax,eax
   140008bca:	75 07                	jne    140008bd3 <__fpclassifyl+0x43>
   140008bcc:	b8 00 40 00 00       	mov    eax,0x4000
   140008bd1:	eb 3d                	jmp    140008c10 <__fpclassifyl+0x80>
   140008bd3:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008bd6:	85 c0                	test   eax,eax
   140008bd8:	78 31                	js     140008c0b <__fpclassifyl+0x7b>
   140008bda:	b8 00 44 00 00       	mov    eax,0x4400
   140008bdf:	eb 2f                	jmp    140008c10 <__fpclassifyl+0x80>
   140008be1:	81 7d fc ff 7f 00 00 	cmp    DWORD PTR [rbp-0x4],0x7fff
   140008be8:	75 21                	jne    140008c0b <__fpclassifyl+0x7b>
   140008bea:	8b 45 e4             	mov    eax,DWORD PTR [rbp-0x1c]
   140008bed:	25 ff ff ff 7f       	and    eax,0x7fffffff
   140008bf2:	89 c2                	mov    edx,eax
   140008bf4:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140008bf7:	09 d0                	or     eax,edx
   140008bf9:	85 c0                	test   eax,eax
   140008bfb:	75 07                	jne    140008c04 <__fpclassifyl+0x74>
   140008bfd:	b8 00 05 00 00       	mov    eax,0x500
   140008c02:	eb 0c                	jmp    140008c10 <__fpclassifyl+0x80>
   140008c04:	b8 00 01 00 00       	mov    eax,0x100
   140008c09:	eb 05                	jmp    140008c10 <__fpclassifyl+0x80>
   140008c0b:	b8 00 04 00 00       	mov    eax,0x400
   140008c10:	48 83 c4 38          	add    rsp,0x38
   140008c14:	5b                   	pop    rbx
   140008c15:	5d                   	pop    rbp
   140008c16:	c3                   	ret
   140008c17:	90                   	nop
   140008c18:	90                   	nop
   140008c19:	90                   	nop
   140008c1a:	90                   	nop
   140008c1b:	90                   	nop
   140008c1c:	90                   	nop
   140008c1d:	90                   	nop
   140008c1e:	90                   	nop
   140008c1f:	90                   	nop

0000000140008c20 <__isnan>:
   140008c20:	55                   	push   rbp
   140008c21:	48 89 e5             	mov    rbp,rsp
   140008c24:	48 83 ec 10          	sub    rsp,0x10
   140008c28:	f2 0f 11 45 10       	movsd  QWORD PTR [rbp+0x10],xmm0
   140008c2d:	f2 0f 10 45 10       	movsd  xmm0,QWORD PTR [rbp+0x10]
   140008c32:	f2 0f 11 45 f0       	movsd  QWORD PTR [rbp-0x10],xmm0
   140008c37:	8b 45 f0             	mov    eax,DWORD PTR [rbp-0x10]
   140008c3a:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008c3d:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140008c40:	25 ff ff ff 7f       	and    eax,0x7fffffff
   140008c45:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008c48:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008c4b:	f7 d8                	neg    eax
   140008c4d:	0b 45 fc             	or     eax,DWORD PTR [rbp-0x4]
   140008c50:	c1 e8 1f             	shr    eax,0x1f
   140008c53:	89 c2                	mov    edx,eax
   140008c55:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008c58:	09 d0                	or     eax,edx
   140008c5a:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008c5d:	b8 00 00 f0 7f       	mov    eax,0x7ff00000
   140008c62:	2b 45 f8             	sub    eax,DWORD PTR [rbp-0x8]
   140008c65:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008c68:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008c6b:	c1 f8 1f             	sar    eax,0x1f
   140008c6e:	48 83 c4 10          	add    rsp,0x10
   140008c72:	5d                   	pop    rbp
   140008c73:	c3                   	ret
   140008c74:	90                   	nop
   140008c75:	90                   	nop
   140008c76:	90                   	nop
   140008c77:	90                   	nop
   140008c78:	90                   	nop
   140008c79:	90                   	nop
   140008c7a:	90                   	nop
   140008c7b:	90                   	nop
   140008c7c:	90                   	nop
   140008c7d:	90                   	nop
   140008c7e:	90                   	nop
   140008c7f:	90                   	nop

0000000140008c80 <__isnanl>:
   140008c80:	55                   	push   rbp
   140008c81:	53                   	push   rbx
   140008c82:	48 83 ec 38          	sub    rsp,0x38
   140008c86:	48 8d 6c 24 30       	lea    rbp,[rsp+0x30]
   140008c8b:	48 89 cb             	mov    rbx,rcx
   140008c8e:	db 2b                	fld    TBYTE PTR [rbx]
   140008c90:	db 7d d0             	fstp   TBYTE PTR [rbp-0x30]
   140008c93:	db 6d d0             	fld    TBYTE PTR [rbp-0x30]
   140008c96:	db 7d e0             	fstp   TBYTE PTR [rbp-0x20]
   140008c99:	0f b7 45 e8          	movzx  eax,WORD PTR [rbp-0x18]
   140008c9d:	98                   	cwde
   140008c9e:	01 c0                	add    eax,eax
   140008ca0:	25 ff ff 00 00       	and    eax,0xffff
   140008ca5:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008ca8:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140008cab:	8b 55 e4             	mov    edx,DWORD PTR [rbp-0x1c]
   140008cae:	81 e2 ff ff ff 7f    	and    edx,0x7fffffff
   140008cb4:	09 d0                	or     eax,edx
   140008cb6:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008cb9:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   140008cbc:	f7 d8                	neg    eax
   140008cbe:	0b 45 f8             	or     eax,DWORD PTR [rbp-0x8]
   140008cc1:	c1 e8 1f             	shr    eax,0x1f
   140008cc4:	89 c2                	mov    edx,eax
   140008cc6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008cc9:	09 d0                	or     eax,edx
   140008ccb:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008cce:	b8 fe ff 00 00       	mov    eax,0xfffe
   140008cd3:	2b 45 fc             	sub    eax,DWORD PTR [rbp-0x4]
   140008cd6:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008cd9:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140008cdc:	c1 f8 10             	sar    eax,0x10
   140008cdf:	48 83 c4 38          	add    rsp,0x38
   140008ce3:	5b                   	pop    rbx
   140008ce4:	5d                   	pop    rbp
   140008ce5:	c3                   	ret
   140008ce6:	90                   	nop
   140008ce7:	90                   	nop
   140008ce8:	90                   	nop
   140008ce9:	90                   	nop
   140008cea:	90                   	nop
   140008ceb:	90                   	nop
   140008cec:	90                   	nop
   140008ced:	90                   	nop
   140008cee:	90                   	nop
   140008cef:	90                   	nop

0000000140008cf0 <wcsnlen>:
   140008cf0:	55                   	push   rbp
   140008cf1:	48 89 e5             	mov    rbp,rsp
   140008cf4:	48 83 ec 10          	sub    rsp,0x10
   140008cf8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008cfc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008d00:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   140008d07:	00 
   140008d08:	eb 0a                	jmp    140008d14 <wcsnlen+0x24>
   140008d0a:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
   140008d0f:	48 83 45 10 02       	add    QWORD PTR [rbp+0x10],0x2
   140008d14:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d18:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140008d1c:	73 0c                	jae    140008d2a <wcsnlen+0x3a>
   140008d1e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008d22:	0f b7 00             	movzx  eax,WORD PTR [rax]
   140008d25:	66 85 c0             	test   ax,ax
   140008d28:	75 e0                	jne    140008d0a <wcsnlen+0x1a>
   140008d2a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d2e:	48 83 c4 10          	add    rsp,0x10
   140008d32:	5d                   	pop    rbp
   140008d33:	c3                   	ret
   140008d34:	90                   	nop
   140008d35:	90                   	nop
   140008d36:	90                   	nop
   140008d37:	90                   	nop
   140008d38:	90                   	nop
   140008d39:	90                   	nop
   140008d3a:	90                   	nop
   140008d3b:	90                   	nop
   140008d3c:	90                   	nop
   140008d3d:	90                   	nop
   140008d3e:	90                   	nop
   140008d3f:	90                   	nop

0000000140008d40 <strnlen>:
   140008d40:	55                   	push   rbp
   140008d41:	48 89 e5             	mov    rbp,rsp
   140008d44:	48 83 ec 10          	sub    rsp,0x10
   140008d48:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008d4c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008d50:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008d54:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008d58:	eb 05                	jmp    140008d5f <strnlen+0x1f>
   140008d5a:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
   140008d5f:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d63:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140008d67:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140008d6b:	73 0b                	jae    140008d78 <strnlen+0x38>
   140008d6d:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d71:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140008d74:	84 c0                	test   al,al
   140008d76:	75 e2                	jne    140008d5a <strnlen+0x1a>
   140008d78:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008d7c:	48 2b 45 10          	sub    rax,QWORD PTR [rbp+0x10]
   140008d80:	48 83 c4 10          	add    rsp,0x10
   140008d84:	5d                   	pop    rbp
   140008d85:	c3                   	ret
   140008d86:	90                   	nop
   140008d87:	90                   	nop
   140008d88:	90                   	nop
   140008d89:	90                   	nop
   140008d8a:	90                   	nop
   140008d8b:	90                   	nop
   140008d8c:	90                   	nop
   140008d8d:	90                   	nop
   140008d8e:	90                   	nop
   140008d8f:	90                   	nop

0000000140008d90 <_initterm_e>:
   140008d90:	55                   	push   rbp
   140008d91:	48 89 e5             	mov    rbp,rsp
   140008d94:	48 83 ec 30          	sub    rsp,0x30
   140008d98:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008d9c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140008da0:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008da4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008da8:	eb 29                	jmp    140008dd3 <_initterm_e+0x43>
   140008daa:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008dae:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008db1:	48 85 c0             	test   rax,rax
   140008db4:	74 17                	je     140008dcd <_initterm_e+0x3d>
   140008db6:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008dba:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008dbd:	ff d0                	call   rax
   140008dbf:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   140008dc2:	83 7d f4 00          	cmp    DWORD PTR [rbp-0xc],0x0
   140008dc6:	74 06                	je     140008dce <_initterm_e+0x3e>
   140008dc8:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
   140008dcb:	eb 15                	jmp    140008de2 <_initterm_e+0x52>
   140008dcd:	90                   	nop
   140008dce:	48 83 45 f8 08       	add    QWORD PTR [rbp-0x8],0x8
   140008dd3:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008dd7:	48 3b 45 18          	cmp    rax,QWORD PTR [rbp+0x18]
   140008ddb:	72 cd                	jb     140008daa <_initterm_e+0x1a>
   140008ddd:	b8 00 00 00 00       	mov    eax,0x0
   140008de2:	48 83 c4 30          	add    rsp,0x30
   140008de6:	5d                   	pop    rbp
   140008de7:	c3                   	ret
   140008de8:	90                   	nop
   140008de9:	90                   	nop
   140008dea:	90                   	nop
   140008deb:	90                   	nop
   140008dec:	90                   	nop
   140008ded:	90                   	nop
   140008dee:	90                   	nop
   140008def:	90                   	nop

0000000140008df0 <__p__fmode>:
   140008df0:	55                   	push   rbp
   140008df1:	48 89 e5             	mov    rbp,rsp
   140008df4:	48 8b 05 15 28 00 00 	mov    rax,QWORD PTR [rip+0x2815]        # 14000b610 <.refptr.__imp__fmode>
   140008dfb:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008dfe:	5d                   	pop    rbp
   140008dff:	c3                   	ret

0000000140008e00 <__p__commode>:
   140008e00:	55                   	push   rbp
   140008e01:	48 89 e5             	mov    rbp,rsp
   140008e04:	48 8b 05 f5 27 00 00 	mov    rax,QWORD PTR [rip+0x27f5]        # 14000b600 <.refptr.__imp__commode>
   140008e0b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008e0e:	5d                   	pop    rbp
   140008e0f:	c3                   	ret

0000000140008e10 <__p___initenv>:
   140008e10:	55                   	push   rbp
   140008e11:	48 89 e5             	mov    rbp,rsp
   140008e14:	48 8b 05 d5 27 00 00 	mov    rax,QWORD PTR [rip+0x27d5]        # 14000b5f0 <.refptr.__imp___initenv>
   140008e1b:	48 8b 00             	mov    rax,QWORD PTR [rax]
   140008e1e:	5d                   	pop    rbp
   140008e1f:	c3                   	ret

0000000140008e20 <_lock_file>:
   140008e20:	55                   	push   rbp
   140008e21:	48 89 e5             	mov    rbp,rsp
   140008e24:	48 83 ec 20          	sub    rsp,0x20
   140008e28:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008e2c:	b9 00 00 00 00       	mov    ecx,0x0
   140008e31:	e8 6a 01 00 00       	call   140008fa0 <__acrt_iob_func>
   140008e36:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140008e3a:	72 52                	jb     140008e8e <_lock_file+0x6e>
   140008e3c:	b9 13 00 00 00       	mov    ecx,0x13
   140008e41:	e8 5a 01 00 00       	call   140008fa0 <__acrt_iob_func>
   140008e46:	48 3b 45 10          	cmp    rax,QWORD PTR [rbp+0x10]
   140008e4a:	72 42                	jb     140008e8e <_lock_file+0x6e>
   140008e4c:	b9 00 00 00 00       	mov    ecx,0x0
   140008e51:	e8 4a 01 00 00       	call   140008fa0 <__acrt_iob_func>
   140008e56:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140008e5a:	48 29 c2             	sub    rdx,rax
   140008e5d:	48 c1 fa 04          	sar    rdx,0x4
   140008e61:	48 b8 ab aa aa aa aa 	movabs rax,0xaaaaaaaaaaaaaaab
   140008e68:	aa aa aa 
   140008e6b:	48 0f af c2          	imul   rax,rdx
   140008e6f:	83 c0 10             	add    eax,0x10
   140008e72:	89 c1                	mov    ecx,eax
   140008e74:	e8 1f 07 00 00       	call   140009598 <_lock>
   140008e79:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008e7d:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140008e80:	80 cc 80             	or     ah,0x80
   140008e83:	89 c2                	mov    edx,eax
   140008e85:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008e89:	89 50 18             	mov    DWORD PTR [rax+0x18],edx
   140008e8c:	eb 15                	jmp    140008ea3 <_lock_file+0x83>
   140008e8e:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008e92:	48 83 c0 30          	add    rax,0x30
   140008e96:	48 89 c1             	mov    rcx,rax
   140008e99:	48 8b 05 90 73 00 00 	mov    rax,QWORD PTR [rip+0x7390]        # 140010230 <__imp_EnterCriticalSection>
   140008ea0:	ff d0                	call   rax
   140008ea2:	90                   	nop
   140008ea3:	90                   	nop
   140008ea4:	48 83 c4 20          	add    rsp,0x20
   140008ea8:	5d                   	pop    rbp
   140008ea9:	c3                   	ret

0000000140008eaa <_unlock_file>:
   140008eaa:	55                   	push   rbp
   140008eab:	48 89 e5             	mov    rbp,rsp
   140008eae:	48 83 ec 20          	sub    rsp,0x20
   140008eb2:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008eb6:	b9 00 00 00 00       	mov    ecx,0x0
   140008ebb:	e8 e0 00 00 00       	call   140008fa0 <__acrt_iob_func>
   140008ec0:	48 39 45 10          	cmp    QWORD PTR [rbp+0x10],rax
   140008ec4:	72 52                	jb     140008f18 <_unlock_file+0x6e>
   140008ec6:	b9 13 00 00 00       	mov    ecx,0x13
   140008ecb:	e8 d0 00 00 00       	call   140008fa0 <__acrt_iob_func>
   140008ed0:	48 3b 45 10          	cmp    rax,QWORD PTR [rbp+0x10]
   140008ed4:	72 42                	jb     140008f18 <_unlock_file+0x6e>
   140008ed6:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008eda:	8b 40 18             	mov    eax,DWORD PTR [rax+0x18]
   140008edd:	80 e4 7f             	and    ah,0x7f
   140008ee0:	89 c2                	mov    edx,eax
   140008ee2:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008ee6:	89 50 18             	mov    DWORD PTR [rax+0x18],edx
   140008ee9:	b9 00 00 00 00       	mov    ecx,0x0
   140008eee:	e8 ad 00 00 00       	call   140008fa0 <__acrt_iob_func>
   140008ef3:	48 8b 55 10          	mov    rdx,QWORD PTR [rbp+0x10]
   140008ef7:	48 29 c2             	sub    rdx,rax
   140008efa:	48 c1 fa 04          	sar    rdx,0x4
   140008efe:	48 b8 ab aa aa aa aa 	movabs rax,0xaaaaaaaaaaaaaaab
   140008f05:	aa aa aa 
   140008f08:	48 0f af c2          	imul   rax,rdx
   140008f0c:	83 c0 10             	add    eax,0x10
   140008f0f:	89 c1                	mov    ecx,eax
   140008f11:	e8 8a 06 00 00       	call   1400095a0 <_unlock>
   140008f16:	eb 15                	jmp    140008f2d <_unlock_file+0x83>
   140008f18:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008f1c:	48 83 c0 30          	add    rax,0x30
   140008f20:	48 89 c1             	mov    rcx,rax
   140008f23:	48 8b 05 3e 73 00 00 	mov    rax,QWORD PTR [rip+0x733e]        # 140010268 <__imp_LeaveCriticalSection>
   140008f2a:	ff d0                	call   rax
   140008f2c:	90                   	nop
   140008f2d:	90                   	nop
   140008f2e:	48 83 c4 20          	add    rsp,0x20
   140008f32:	5d                   	pop    rbp
   140008f33:	c3                   	ret
   140008f34:	90                   	nop
   140008f35:	90                   	nop
   140008f36:	90                   	nop
   140008f37:	90                   	nop
   140008f38:	90                   	nop
   140008f39:	90                   	nop
   140008f3a:	90                   	nop
   140008f3b:	90                   	nop
   140008f3c:	90                   	nop
   140008f3d:	90                   	nop
   140008f3e:	90                   	nop
   140008f3f:	90                   	nop

0000000140008f40 <_set_invalid_parameter_handler>:
   140008f40:	55                   	push   rbp
   140008f41:	48 89 e5             	mov    rbp,rsp
   140008f44:	48 83 ec 10          	sub    rsp,0x10
   140008f48:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008f4c:	48 8d 05 2d 6c 00 00 	lea    rax,[rip+0x6c2d]        # 14000fb80 <handler>
   140008f53:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   140008f57:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140008f5b:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   140008f5f:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
   140008f63:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   140008f67:	48 87 10             	xchg   QWORD PTR [rax],rdx
   140008f6a:	48 89 d0             	mov    rax,rdx
   140008f6d:	48 83 c4 10          	add    rsp,0x10
   140008f71:	5d                   	pop    rbp
   140008f72:	c3                   	ret

0000000140008f73 <_get_invalid_parameter_handler>:
   140008f73:	55                   	push   rbp
   140008f74:	48 89 e5             	mov    rbp,rsp
   140008f77:	48 8b 05 02 6c 00 00 	mov    rax,QWORD PTR [rip+0x6c02]        # 14000fb80 <handler>
   140008f7e:	5d                   	pop    rbp
   140008f7f:	c3                   	ret

0000000140008f80 <_configthreadlocale>:
   140008f80:	55                   	push   rbp
   140008f81:	48 89 e5             	mov    rbp,rsp
   140008f84:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140008f87:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
   140008f8b:	75 07                	jne    140008f94 <_configthreadlocale+0x14>
   140008f8d:	b8 ff ff ff ff       	mov    eax,0xffffffff
   140008f92:	eb 05                	jmp    140008f99 <_configthreadlocale+0x19>
   140008f94:	b8 02 00 00 00       	mov    eax,0x2
   140008f99:	5d                   	pop    rbp
   140008f9a:	c3                   	ret
   140008f9b:	90                   	nop
   140008f9c:	90                   	nop
   140008f9d:	90                   	nop
   140008f9e:	90                   	nop
   140008f9f:	90                   	nop

0000000140008fa0 <__acrt_iob_func>:
   140008fa0:	55                   	push   rbp
   140008fa1:	48 89 e5             	mov    rbp,rsp
   140008fa4:	48 83 ec 20          	sub    rsp,0x20
   140008fa8:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   140008fab:	e8 b0 05 00 00       	call   140009560 <__iob_func>
   140008fb0:	48 89 c1             	mov    rcx,rax
   140008fb3:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   140008fb6:	48 89 d0             	mov    rax,rdx
   140008fb9:	48 01 c0             	add    rax,rax
   140008fbc:	48 01 d0             	add    rax,rdx
   140008fbf:	48 c1 e0 04          	shl    rax,0x4
   140008fc3:	48 01 c8             	add    rax,rcx
   140008fc6:	48 83 c4 20          	add    rsp,0x20
   140008fca:	5d                   	pop    rbp
   140008fcb:	c3                   	ret
   140008fcc:	90                   	nop
   140008fcd:	90                   	nop
   140008fce:	90                   	nop
   140008fcf:	90                   	nop

0000000140008fd0 <wcrtomb>:
   140008fd0:	55                   	push   rbp
   140008fd1:	48 89 e5             	mov    rbp,rsp
   140008fd4:	48 83 ec 40          	sub    rsp,0x40
   140008fd8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   140008fdc:	89 d0                	mov    eax,edx
   140008fde:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140008fe2:	66 89 45 18          	mov    WORD PTR [rbp+0x18],ax
   140008fe6:	e8 5d 05 00 00       	call   140009548 <___lc_codepage_func>
   140008feb:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140008fee:	e8 5d 05 00 00       	call   140009550 <___mb_cur_max_func>
   140008ff3:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   140008ff6:	0f b7 55 18          	movzx  edx,WORD PTR [rbp+0x18]
   140008ffa:	44 8b 4d fc          	mov    r9d,DWORD PTR [rbp-0x4]
   140008ffe:	4c 8b 45 20          	mov    r8,QWORD PTR [rbp+0x20]
   140009002:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140009006:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   140009009:	89 4c 24 20          	mov    DWORD PTR [rsp+0x20],ecx
   14000900d:	48 89 c1             	mov    rcx,rax
   140009010:	e8 7b 00 00 00       	call   140009090 <__mingw_wcrtomb_cp>
   140009015:	48 83 c4 40          	add    rsp,0x40
   140009019:	5d                   	pop    rbp
   14000901a:	c3                   	ret
   14000901b:	90                   	nop
   14000901c:	90                   	nop
   14000901d:	90                   	nop
   14000901e:	90                   	nop
   14000901f:	90                   	nop

0000000140009020 <mbrtowc>:
   140009020:	55                   	push   rbp
   140009021:	48 89 e5             	mov    rbp,rsp
   140009024:	48 83 ec 40          	sub    rsp,0x40
   140009028:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000902c:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140009030:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140009034:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140009038:	48 83 7d 28 00       	cmp    QWORD PTR [rbp+0x28],0x0
   14000903d:	75 0b                	jne    14000904a <mbrtowc+0x2a>
   14000903f:	48 8d 05 4a 6b 00 00 	lea    rax,[rip+0x6b4a]        # 14000fb90 <state_mbrtowc.0>
   140009046:	48 89 45 28          	mov    QWORD PTR [rbp+0x28],rax
   14000904a:	e8 f9 04 00 00       	call   140009548 <___lc_codepage_func>
   14000904f:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140009052:	e8 f9 04 00 00       	call   140009550 <___mb_cur_max_func>
   140009057:	89 45 f8             	mov    DWORD PTR [rbp-0x8],eax
   14000905a:	4c 8b 4d 28          	mov    r9,QWORD PTR [rbp+0x28]
   14000905e:	4c 8b 45 20          	mov    r8,QWORD PTR [rbp+0x20]
   140009062:	48 8b 55 18          	mov    rdx,QWORD PTR [rbp+0x18]
   140009066:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000906a:	8b 4d f8             	mov    ecx,DWORD PTR [rbp-0x8]
   14000906d:	89 4c 24 28          	mov    DWORD PTR [rsp+0x28],ecx
   140009071:	8b 4d fc             	mov    ecx,DWORD PTR [rbp-0x4]
   140009074:	89 4c 24 20          	mov    DWORD PTR [rsp+0x20],ecx
   140009078:	48 89 c1             	mov    rcx,rax
   14000907b:	e8 70 01 00 00       	call   1400091f0 <__mingw_mbrtowc_cp>
   140009080:	48 83 c4 40          	add    rsp,0x40
   140009084:	5d                   	pop    rbp
   140009085:	c3                   	ret
   140009086:	90                   	nop
   140009087:	90                   	nop
   140009088:	90                   	nop
   140009089:	90                   	nop
   14000908a:	90                   	nop
   14000908b:	90                   	nop
   14000908c:	90                   	nop
   14000908d:	90                   	nop
   14000908e:	90                   	nop
   14000908f:	90                   	nop

0000000140009090 <__mingw_wcrtomb_cp>:
   140009090:	55                   	push   rbp
   140009091:	48 89 e5             	mov    rbp,rsp
   140009094:	48 83 ec 50          	sub    rsp,0x50
   140009098:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   14000909c:	89 d0                	mov    eax,edx
   14000909e:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   1400090a2:	44 89 4d 28          	mov    DWORD PTR [rbp+0x28],r9d
   1400090a6:	66 89 45 18          	mov    WORD PTR [rbp+0x18],ax
   1400090aa:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400090af:	75 1b                	jne    1400090cc <__mingw_wcrtomb_cp+0x3c>
   1400090b1:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   1400090b6:	74 0a                	je     1400090c2 <__mingw_wcrtomb_cp+0x32>
   1400090b8:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400090bc:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400090c2:	b8 01 00 00 00       	mov    eax,0x1
   1400090c7:	e9 17 01 00 00       	jmp    1400091e3 <__mingw_wcrtomb_cp+0x153>
   1400090cc:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   1400090d1:	74 21                	je     1400090f4 <__mingw_wcrtomb_cp+0x64>
   1400090d3:	48 8b 45 20          	mov    rax,QWORD PTR [rbp+0x20]
   1400090d7:	8b 00                	mov    eax,DWORD PTR [rax]
   1400090d9:	85 c0                	test   eax,eax
   1400090db:	74 17                	je     1400090f4 <__mingw_wcrtomb_cp+0x64>
   1400090dd:	e8 a6 04 00 00       	call   140009588 <_errno>
   1400090e2:	c7 00 16 00 00 00    	mov    DWORD PTR [rax],0x16
   1400090e8:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400090ef:	e9 ef 00 00 00       	jmp    1400091e3 <__mingw_wcrtomb_cp+0x153>
   1400090f4:	0f b7 45 18          	movzx  eax,WORD PTR [rbp+0x18]
   1400090f8:	66 85 c0             	test   ax,ax
   1400090fb:	75 18                	jne    140009115 <__mingw_wcrtomb_cp+0x85>
   1400090fd:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140009102:	74 07                	je     14000910b <__mingw_wcrtomb_cp+0x7b>
   140009104:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140009108:	c6 00 00             	mov    BYTE PTR [rax],0x0
   14000910b:	b8 01 00 00 00       	mov    eax,0x1
   140009110:	e9 ce 00 00 00       	jmp    1400091e3 <__mingw_wcrtomb_cp+0x153>
   140009115:	83 7d 28 00          	cmp    DWORD PTR [rbp+0x28],0x0
   140009119:	75 2b                	jne    140009146 <__mingw_wcrtomb_cp+0xb6>
   14000911b:	0f b7 45 18          	movzx  eax,WORD PTR [rbp+0x18]
   14000911f:	66 3d ff 00          	cmp    ax,0xff
   140009123:	0f 87 a4 00 00 00    	ja     1400091cd <__mingw_wcrtomb_cp+0x13d>
   140009129:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000912e:	74 0c                	je     14000913c <__mingw_wcrtomb_cp+0xac>
   140009130:	0f b7 45 18          	movzx  eax,WORD PTR [rbp+0x18]
   140009134:	89 c2                	mov    edx,eax
   140009136:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   14000913a:	88 10                	mov    BYTE PTR [rax],dl
   14000913c:	b8 01 00 00 00       	mov    eax,0x1
   140009141:	e9 9d 00 00 00       	jmp    1400091e3 <__mingw_wcrtomb_cp+0x153>
   140009146:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   14000914d:	66 c7 45 f6 00 00    	mov    WORD PTR [rbp-0xa],0x0
   140009153:	48 8d 4d 18          	lea    rcx,[rbp+0x18]
   140009157:	8b 45 28             	mov    eax,DWORD PTR [rbp+0x28]
   14000915a:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
   14000915e:	48 89 54 24 38       	mov    QWORD PTR [rsp+0x38],rdx
   140009163:	48 c7 44 24 30 00 00 	mov    QWORD PTR [rsp+0x30],0x0
   14000916a:	00 00 
   14000916c:	8b 55 30             	mov    edx,DWORD PTR [rbp+0x30]
   14000916f:	89 54 24 28          	mov    DWORD PTR [rsp+0x28],edx
   140009173:	48 8d 55 f6          	lea    rdx,[rbp-0xa]
   140009177:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   14000917c:	41 b9 01 00 00 00    	mov    r9d,0x1
   140009182:	49 89 c8             	mov    r8,rcx
   140009185:	ba 00 00 00 00       	mov    edx,0x0
   14000918a:	89 c1                	mov    ecx,eax
   14000918c:	48 8b 05 15 71 00 00 	mov    rax,QWORD PTR [rip+0x7115]        # 1400102a8 <__imp_WideCharToMultiByte>
   140009193:	ff d0                	call   rax
   140009195:	89 45 fc             	mov    DWORD PTR [rbp-0x4],eax
   140009198:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
   14000919c:	74 32                	je     1400091d0 <__mingw_wcrtomb_cp+0x140>
   14000919e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400091a1:	3b 45 30             	cmp    eax,DWORD PTR [rbp+0x30]
   1400091a4:	7f 2a                	jg     1400091d0 <__mingw_wcrtomb_cp+0x140>
   1400091a6:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   1400091a9:	85 c0                	test   eax,eax
   1400091ab:	75 23                	jne    1400091d0 <__mingw_wcrtomb_cp+0x140>
   1400091ad:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400091b0:	48 63 c8             	movsxd rcx,eax
   1400091b3:	48 8d 55 f6          	lea    rdx,[rbp-0xa]
   1400091b7:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400091bb:	49 89 c8             	mov    r8,rcx
   1400091be:	48 89 c1             	mov    rcx,rax
   1400091c1:	e8 32 04 00 00       	call   1400095f8 <memcpy>
   1400091c6:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   1400091c9:	48 98                	cdqe
   1400091cb:	eb 16                	jmp    1400091e3 <__mingw_wcrtomb_cp+0x153>
   1400091cd:	90                   	nop
   1400091ce:	eb 01                	jmp    1400091d1 <__mingw_wcrtomb_cp+0x141>
   1400091d0:	90                   	nop
   1400091d1:	e8 b2 03 00 00       	call   140009588 <_errno>
   1400091d6:	c7 00 2a 00 00 00    	mov    DWORD PTR [rax],0x2a
   1400091dc:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400091e3:	48 83 c4 50          	add    rsp,0x50
   1400091e7:	5d                   	pop    rbp
   1400091e8:	c3                   	ret
   1400091e9:	90                   	nop
   1400091ea:	90                   	nop
   1400091eb:	90                   	nop
   1400091ec:	90                   	nop
   1400091ed:	90                   	nop
   1400091ee:	90                   	nop
   1400091ef:	90                   	nop

00000001400091f0 <__mingw_mbrtowc_cp>:
   1400091f0:	55                   	push   rbp
   1400091f1:	48 89 e5             	mov    rbp,rsp
   1400091f4:	48 83 ec 50          	sub    rsp,0x50
   1400091f8:	48 89 4d 10          	mov    QWORD PTR [rbp+0x10],rcx
   1400091fc:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx
   140009200:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8
   140009204:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9
   140009208:	48 83 7d 18 00       	cmp    QWORD PTR [rbp+0x18],0x0
   14000920d:	75 1b                	jne    14000922a <__mingw_mbrtowc_cp+0x3a>
   14000920f:	48 c7 45 10 00 00 00 	mov    QWORD PTR [rbp+0x10],0x0
   140009216:	00 
   140009217:	48 8d 05 02 23 00 00 	lea    rax,[rip+0x2302]        # 14000b520 <.rdata>
   14000921e:	48 89 45 18          	mov    QWORD PTR [rbp+0x18],rax
   140009222:	48 c7 45 20 01 00 00 	mov    QWORD PTR [rbp+0x20],0x1
   140009229:	00 
   14000922a:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000922e:	8b 00                	mov    eax,DWORD PTR [rax]
   140009230:	3d ff 00 00 00       	cmp    eax,0xff
   140009235:	0f 87 b9 01 00 00    	ja     1400093f4 <__mingw_mbrtowc_cp+0x204>
   14000923b:	48 83 7d 20 00       	cmp    QWORD PTR [rbp+0x20],0x0
   140009240:	75 0c                	jne    14000924e <__mingw_mbrtowc_cp+0x5e>
   140009242:	48 c7 c0 fe ff ff ff 	mov    rax,0xfffffffffffffffe
   140009249:	e9 bc 01 00 00       	jmp    14000940a <__mingw_mbrtowc_cp+0x21a>
   14000924e:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140009252:	8b 00                	mov    eax,DWORD PTR [rax]
   140009254:	89 45 f0             	mov    DWORD PTR [rbp-0x10],eax
   140009257:	83 7d 38 01          	cmp    DWORD PTR [rbp+0x38],0x1
   14000925b:	75 0c                	jne    140009269 <__mingw_mbrtowc_cp+0x79>
   14000925d:	0f b6 45 f0          	movzx  eax,BYTE PTR [rbp-0x10]
   140009261:	84 c0                	test   al,al
   140009263:	0f 85 8e 01 00 00    	jne    1400093f7 <__mingw_mbrtowc_cp+0x207>
   140009269:	83 7d 30 00          	cmp    DWORD PTR [rbp+0x30],0x0
   14000926d:	75 2c                	jne    14000929b <__mingw_mbrtowc_cp+0xab>
   14000926f:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   140009274:	74 11                	je     140009287 <__mingw_mbrtowc_cp+0x97>
   140009276:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000927a:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000927d:	0f b6 d0             	movzx  edx,al
   140009280:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140009284:	66 89 10             	mov    WORD PTR [rax],dx
   140009287:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   14000928b:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000928e:	84 c0                	test   al,al
   140009290:	0f 95 c0             	setne  al
   140009293:	0f b6 c0             	movzx  eax,al
   140009296:	e9 6f 01 00 00       	jmp    14000940a <__mingw_mbrtowc_cp+0x21a>
   14000929b:	c7 45 fc 01 00 00 00 	mov    DWORD PTR [rbp-0x4],0x1
   1400092a2:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
   1400092a9:	0f b6 45 f0          	movzx  eax,BYTE PTR [rbp-0x10]
   1400092ad:	84 c0                	test   al,al
   1400092af:	74 1a                	je     1400092cb <__mingw_mbrtowc_cp+0xdb>
   1400092b1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400092b5:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400092b8:	88 45 f1             	mov    BYTE PTR [rbp-0xf],al
   1400092bb:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   1400092c2:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
   1400092c9:	eb 73                	jmp    14000933e <__mingw_mbrtowc_cp+0x14e>
   1400092cb:	83 7d 38 02          	cmp    DWORD PTR [rbp+0x38],0x2
   1400092cf:	75 5c                	jne    14000932d <__mingw_mbrtowc_cp+0x13d>
   1400092d1:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400092d5:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400092d8:	0f b6 c0             	movzx  eax,al
   1400092db:	8b 55 30             	mov    edx,DWORD PTR [rbp+0x30]
   1400092de:	89 c1                	mov    ecx,eax
   1400092e0:	e8 ad 01 00 00       	call   140009492 <__mingw_isleadbyte_cp>
   1400092e5:	85 c0                	test   eax,eax
   1400092e7:	74 44                	je     14000932d <__mingw_mbrtowc_cp+0x13d>
   1400092e9:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   1400092ed:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   1400092f0:	88 45 f0             	mov    BYTE PTR [rbp-0x10],al
   1400092f3:	48 83 7d 20 01       	cmp    QWORD PTR [rbp+0x20],0x1
   1400092f8:	77 15                	ja     14000930f <__mingw_mbrtowc_cp+0x11f>
   1400092fa:	8b 55 f0             	mov    edx,DWORD PTR [rbp-0x10]
   1400092fd:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   140009301:	89 10                	mov    DWORD PTR [rax],edx
   140009303:	48 c7 c0 fe ff ff ff 	mov    rax,0xfffffffffffffffe
   14000930a:	e9 fb 00 00 00       	jmp    14000940a <__mingw_mbrtowc_cp+0x21a>
   14000930f:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140009313:	48 83 c0 01          	add    rax,0x1
   140009317:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   14000931a:	88 45 f1             	mov    BYTE PTR [rbp-0xf],al
   14000931d:	c7 45 f8 02 00 00 00 	mov    DWORD PTR [rbp-0x8],0x2
   140009324:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [rbp-0x4],0x2
   14000932b:	eb 11                	jmp    14000933e <__mingw_mbrtowc_cp+0x14e>
   14000932d:	48 8b 45 18          	mov    rax,QWORD PTR [rbp+0x18]
   140009331:	0f b6 00             	movzx  eax,BYTE PTR [rax]
   140009334:	88 45 f0             	mov    BYTE PTR [rbp-0x10],al
   140009337:	c7 45 f8 01 00 00 00 	mov    DWORD PTR [rbp-0x8],0x1
   14000933e:	0f b6 45 f0          	movzx  eax,BYTE PTR [rbp-0x10]
   140009342:	84 c0                	test   al,al
   140009344:	75 24                	jne    14000936a <__mingw_mbrtowc_cp+0x17a>
   140009346:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   14000934b:	74 09                	je     140009356 <__mingw_mbrtowc_cp+0x166>
   14000934d:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   140009351:	66 c7 00 00 00       	mov    WORD PTR [rax],0x0
   140009356:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   14000935a:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   140009360:	b8 00 00 00 00       	mov    eax,0x0
   140009365:	e9 a0 00 00 00       	jmp    14000940a <__mingw_mbrtowc_cp+0x21a>
   14000936a:	83 7d fc 02          	cmp    DWORD PTR [rbp-0x4],0x2
   14000936e:	75 08                	jne    140009378 <__mingw_mbrtowc_cp+0x188>
   140009370:	0f b6 45 f1          	movzx  eax,BYTE PTR [rbp-0xf]
   140009374:	84 c0                	test   al,al
   140009376:	74 64                	je     1400093dc <__mingw_mbrtowc_cp+0x1ec>
   140009378:	66 c7 45 ee ff ff    	mov    WORD PTR [rbp-0x12],0xffff
   14000937e:	44 8b 45 fc          	mov    r8d,DWORD PTR [rbp-0x4]
   140009382:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
   140009386:	8b 45 30             	mov    eax,DWORD PTR [rbp+0x30]
   140009389:	c7 44 24 28 01 00 00 	mov    DWORD PTR [rsp+0x28],0x1
   140009390:	00 
   140009391:	48 8d 55 ee          	lea    rdx,[rbp-0x12]
   140009395:	48 89 54 24 20       	mov    QWORD PTR [rsp+0x20],rdx
   14000939a:	45 89 c1             	mov    r9d,r8d
   14000939d:	49 89 c8             	mov    r8,rcx
   1400093a0:	ba 08 00 00 00       	mov    edx,0x8
   1400093a5:	89 c1                	mov    ecx,eax
   1400093a7:	48 8b 05 ca 6e 00 00 	mov    rax,QWORD PTR [rip+0x6eca]        # 140010278 <__imp_MultiByteToWideChar>
   1400093ae:	ff d0                	call   rax
   1400093b0:	89 45 f4             	mov    DWORD PTR [rbp-0xc],eax
   1400093b3:	83 7d f4 01          	cmp    DWORD PTR [rbp-0xc],0x1
   1400093b7:	75 26                	jne    1400093df <__mingw_mbrtowc_cp+0x1ef>
   1400093b9:	48 83 7d 10 00       	cmp    QWORD PTR [rbp+0x10],0x0
   1400093be:	74 0b                	je     1400093cb <__mingw_mbrtowc_cp+0x1db>
   1400093c0:	0f b7 55 ee          	movzx  edx,WORD PTR [rbp-0x12]
   1400093c4:	48 8b 45 10          	mov    rax,QWORD PTR [rbp+0x10]
   1400093c8:	66 89 10             	mov    WORD PTR [rax],dx
   1400093cb:	48 8b 45 28          	mov    rax,QWORD PTR [rbp+0x28]
   1400093cf:	c7 00 00 00 00 00    	mov    DWORD PTR [rax],0x0
   1400093d5:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
   1400093d8:	48 98                	cdqe
   1400093da:	eb 2e                	jmp    14000940a <__mingw_mbrtowc_cp+0x21a>
   1400093dc:	90                   	nop
   1400093dd:	eb 01                	jmp    1400093e0 <__mingw_mbrtowc_cp+0x1f0>
   1400093df:	90                   	nop
   1400093e0:	e8 a3 01 00 00       	call   140009588 <_errno>
   1400093e5:	c7 00 2a 00 00 00    	mov    DWORD PTR [rax],0x2a
   1400093eb:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   1400093f2:	eb 16                	jmp    14000940a <__mingw_mbrtowc_cp+0x21a>
   1400093f4:	90                   	nop
   1400093f5:	eb 01                	jmp    1400093f8 <__mingw_mbrtowc_cp+0x208>
   1400093f7:	90                   	nop
   1400093f8:	e8 8b 01 00 00       	call   140009588 <_errno>
   1400093fd:	c7 00 16 00 00 00    	mov    DWORD PTR [rax],0x16
   140009403:	48 c7 c0 ff ff ff ff 	mov    rax,0xffffffffffffffff
   14000940a:	48 83 c4 50          	add    rsp,0x50
   14000940e:	5d                   	pop    rbp
   14000940f:	c3                   	ret

0000000140009410 <fallback_IsDBCSLeadByteEx>:
   140009410:	55                   	push   rbp
   140009411:	48 89 e5             	mov    rbp,rsp
   140009414:	48 83 ec 40          	sub    rsp,0x40
   140009418:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000941b:	89 d0                	mov    eax,edx
   14000941d:	88 45 18             	mov    BYTE PTR [rbp+0x18],al
   140009420:	48 8d 55 e0          	lea    rdx,[rbp-0x20]
   140009424:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140009427:	89 c1                	mov    ecx,eax
   140009429:	48 8b 05 10 6e 00 00 	mov    rax,QWORD PTR [rip+0x6e10]        # 140010240 <__imp_GetCPInfo>
   140009430:	ff d0                	call   rax
   140009432:	85 c0                	test   eax,eax
   140009434:	74 51                	je     140009487 <fallback_IsDBCSLeadByteEx+0x77>
   140009436:	8b 45 e0             	mov    eax,DWORD PTR [rbp-0x20]
   140009439:	83 f8 02             	cmp    eax,0x2
   14000943c:	75 49                	jne    140009487 <fallback_IsDBCSLeadByteEx+0x77>
   14000943e:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
   140009445:	eb 2c                	jmp    140009473 <fallback_IsDBCSLeadByteEx+0x63>
   140009447:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000944a:	48 98                	cdqe
   14000944c:	0f b6 44 05 e6       	movzx  eax,BYTE PTR [rbp+rax*1-0x1a]
   140009451:	38 45 18             	cmp    BYTE PTR [rbp+0x18],al
   140009454:	72 19                	jb     14000946f <fallback_IsDBCSLeadByteEx+0x5f>
   140009456:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   140009459:	83 c0 01             	add    eax,0x1
   14000945c:	48 98                	cdqe
   14000945e:	0f b6 44 05 e6       	movzx  eax,BYTE PTR [rbp+rax*1-0x1a]
   140009463:	3a 45 18             	cmp    al,BYTE PTR [rbp+0x18]
   140009466:	72 07                	jb     14000946f <fallback_IsDBCSLeadByteEx+0x5f>
   140009468:	b8 01 00 00 00       	mov    eax,0x1
   14000946d:	eb 1d                	jmp    14000948c <fallback_IsDBCSLeadByteEx+0x7c>
   14000946f:	83 45 fc 02          	add    DWORD PTR [rbp-0x4],0x2
   140009473:	83 7d fc 0b          	cmp    DWORD PTR [rbp-0x4],0xb
   140009477:	7f 0e                	jg     140009487 <fallback_IsDBCSLeadByteEx+0x77>
   140009479:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
   14000947c:	48 98                	cdqe
   14000947e:	0f b6 44 05 e6       	movzx  eax,BYTE PTR [rbp+rax*1-0x1a]
   140009483:	84 c0                	test   al,al
   140009485:	75 c0                	jne    140009447 <fallback_IsDBCSLeadByteEx+0x37>
   140009487:	b8 00 00 00 00       	mov    eax,0x0
   14000948c:	48 83 c4 40          	add    rsp,0x40
   140009490:	5d                   	pop    rbp
   140009491:	c3                   	ret

0000000140009492 <__mingw_isleadbyte_cp>:
   140009492:	55                   	push   rbp
   140009493:	48 89 e5             	mov    rbp,rsp
   140009496:	48 83 ec 40          	sub    rsp,0x40
   14000949a:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   14000949d:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   1400094a0:	48 8b 05 f9 66 00 00 	mov    rax,QWORD PTR [rip+0x66f9]        # 14000fba0 <call_IsDBCSLeadByteEx.0>
   1400094a7:	48 85 c0             	test   rax,rax
   1400094aa:	75 71                	jne    14000951d <__mingw_isleadbyte_cp+0x8b>
   1400094ac:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
   1400094b3:	00 
   1400094b4:	48 8d 05 75 20 00 00 	lea    rax,[rip+0x2075]        # 14000b530 <.rdata>
   1400094bb:	48 89 c1             	mov    rcx,rax
   1400094be:	48 8b 05 8b 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d8b]        # 140010250 <__imp_GetModuleHandleA>
   1400094c5:	ff d0                	call   rax
   1400094c7:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
   1400094cb:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
   1400094d0:	74 1b                	je     1400094ed <__mingw_isleadbyte_cp+0x5b>
   1400094d2:	48 8d 15 64 20 00 00 	lea    rdx,[rip+0x2064]        # 14000b53d <.rdata+0xd>
   1400094d9:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
   1400094dd:	48 89 c1             	mov    rcx,rax
   1400094e0:	48 8b 05 71 6d 00 00 	mov    rax,QWORD PTR [rip+0x6d71]        # 140010258 <__imp_GetProcAddress>
   1400094e7:	ff d0                	call   rax
   1400094e9:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400094ed:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
   1400094f2:	75 0b                	jne    1400094ff <__mingw_isleadbyte_cp+0x6d>
   1400094f4:	48 8d 05 15 ff ff ff 	lea    rax,[rip+0xffffffffffffff15]        # 140009410 <fallback_IsDBCSLeadByteEx>
   1400094fb:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
   1400094ff:	48 8d 05 9a 66 00 00 	lea    rax,[rip+0x669a]        # 14000fba0 <call_IsDBCSLeadByteEx.0>
   140009506:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
   14000950a:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
   14000950e:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
   140009512:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
   140009516:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
   14000951a:	48 87 10             	xchg   QWORD PTR [rax],rdx
   14000951d:	4c 8b 05 7c 66 00 00 	mov    r8,QWORD PTR [rip+0x667c]        # 14000fba0 <call_IsDBCSLeadByteEx.0>
   140009524:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
   140009527:	0f b6 d0             	movzx  edx,al
   14000952a:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
   14000952d:	89 c1                	mov    ecx,eax
   14000952f:	41 ff d0             	call   r8
   140009532:	48 83 c4 40          	add    rsp,0x40
   140009536:	5d                   	pop    rbp
   140009537:	c3                   	ret
   140009538:	90                   	nop
   140009539:	90                   	nop
   14000953a:	90                   	nop
   14000953b:	90                   	nop
   14000953c:	90                   	nop
   14000953d:	90                   	nop
   14000953e:	90                   	nop
   14000953f:	90                   	nop

0000000140009540 <__C_specific_handler>:
   140009540:	ff 25 72 6d 00 00    	jmp    QWORD PTR [rip+0x6d72]        # 1400102b8 <__imp___C_specific_handler>
   140009546:	90                   	nop
   140009547:	90                   	nop

0000000140009548 <___lc_codepage_func>:
   140009548:	ff 25 72 6d 00 00    	jmp    QWORD PTR [rip+0x6d72]        # 1400102c0 <__imp____lc_codepage_func>
   14000954e:	90                   	nop
   14000954f:	90                   	nop

0000000140009550 <___mb_cur_max_func>:
   140009550:	ff 25 72 6d 00 00    	jmp    QWORD PTR [rip+0x6d72]        # 1400102c8 <__imp____mb_cur_max_func>
   140009556:	90                   	nop
   140009557:	90                   	nop

0000000140009558 <__getmainargs>:
   140009558:	ff 25 72 6d 00 00    	jmp    QWORD PTR [rip+0x6d72]        # 1400102d0 <__imp___getmainargs>
   14000955e:	90                   	nop
   14000955f:	90                   	nop

0000000140009560 <__iob_func>:
   140009560:	ff 25 7a 6d 00 00    	jmp    QWORD PTR [rip+0x6d7a]        # 1400102e0 <__imp___iob_func>
   140009566:	90                   	nop
   140009567:	90                   	nop

0000000140009568 <__set_app_type>:
   140009568:	ff 25 7a 6d 00 00    	jmp    QWORD PTR [rip+0x6d7a]        # 1400102e8 <__imp___set_app_type>
   14000956e:	90                   	nop
   14000956f:	90                   	nop

0000000140009570 <__setusermatherr>:
   140009570:	ff 25 7a 6d 00 00    	jmp    QWORD PTR [rip+0x6d7a]        # 1400102f0 <__imp___setusermatherr>
   140009576:	90                   	nop
   140009577:	90                   	nop

0000000140009578 <_amsg_exit>:
   140009578:	ff 25 7a 6d 00 00    	jmp    QWORD PTR [rip+0x6d7a]        # 1400102f8 <__imp__amsg_exit>
   14000957e:	90                   	nop
   14000957f:	90                   	nop

0000000140009580 <_cexit>:
   140009580:	ff 25 7a 6d 00 00    	jmp    QWORD PTR [rip+0x6d7a]        # 140010300 <__imp__cexit>
   140009586:	90                   	nop
   140009587:	90                   	nop

0000000140009588 <_errno>:
   140009588:	ff 25 82 6d 00 00    	jmp    QWORD PTR [rip+0x6d82]        # 140010310 <__imp__errno>
   14000958e:	90                   	nop
   14000958f:	90                   	nop

0000000140009590 <_initterm>:
   140009590:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010320 <__imp__initterm>
   140009596:	90                   	nop
   140009597:	90                   	nop

0000000140009598 <_lock>:
   140009598:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010328 <__imp__lock>
   14000959e:	90                   	nop
   14000959f:	90                   	nop

00000001400095a0 <_unlock>:
   1400095a0:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010330 <__imp__unlock>
   1400095a6:	90                   	nop
   1400095a7:	90                   	nop

00000001400095a8 <_crt_atexit>:
   1400095a8:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010338 <__imp__crt_atexit>
   1400095ae:	90                   	nop
   1400095af:	90                   	nop

00000001400095b0 <abort>:
   1400095b0:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010340 <__imp_abort>
   1400095b6:	90                   	nop
   1400095b7:	90                   	nop

00000001400095b8 <calloc>:
   1400095b8:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010348 <__imp_calloc>
   1400095be:	90                   	nop
   1400095bf:	90                   	nop

00000001400095c0 <exit>:
   1400095c0:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010350 <__imp_exit>
   1400095c6:	90                   	nop
   1400095c7:	90                   	nop

00000001400095c8 <fflush>:
   1400095c8:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010358 <__imp_fflush>
   1400095ce:	90                   	nop
   1400095cf:	90                   	nop

00000001400095d0 <fprintf>:
   1400095d0:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010360 <__imp_fprintf>
   1400095d6:	90                   	nop
   1400095d7:	90                   	nop

00000001400095d8 <fputc>:
   1400095d8:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010368 <__imp_fputc>
   1400095de:	90                   	nop
   1400095df:	90                   	nop

00000001400095e0 <free>:
   1400095e0:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010370 <__imp_free>
   1400095e6:	90                   	nop
   1400095e7:	90                   	nop

00000001400095e8 <localeconv>:
   1400095e8:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010378 <__imp_localeconv>
   1400095ee:	90                   	nop
   1400095ef:	90                   	nop

00000001400095f0 <malloc>:
   1400095f0:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010380 <__imp_malloc>
   1400095f6:	90                   	nop
   1400095f7:	90                   	nop

00000001400095f8 <memcpy>:
   1400095f8:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010388 <__imp_memcpy>
   1400095fe:	90                   	nop
   1400095ff:	90                   	nop

0000000140009600 <setvbuf>:
   140009600:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010390 <__imp_setvbuf>
   140009606:	90                   	nop
   140009607:	90                   	nop

0000000140009608 <signal>:
   140009608:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 140010398 <__imp_signal>
   14000960e:	90                   	nop
   14000960f:	90                   	nop

0000000140009610 <strerror>:
   140009610:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 1400103a0 <__imp_strerror>
   140009616:	90                   	nop
   140009617:	90                   	nop

0000000140009618 <strlen>:
   140009618:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 1400103a8 <__imp_strlen>
   14000961e:	90                   	nop
   14000961f:	90                   	nop

0000000140009620 <strncmp>:
   140009620:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 1400103b0 <__imp_strncmp>
   140009626:	90                   	nop
   140009627:	90                   	nop

0000000140009628 <vfprintf>:
   140009628:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 1400103b8 <__imp_vfprintf>
   14000962e:	90                   	nop
   14000962f:	90                   	nop

0000000140009630 <wcslen>:
   140009630:	ff 25 8a 6d 00 00    	jmp    QWORD PTR [rip+0x6d8a]        # 1400103c0 <__imp_wcslen>
   140009636:	90                   	nop
   140009637:	90                   	nop
   140009638:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   14000963f:	00 

0000000140009640 <WideCharToMultiByte>:
   140009640:	ff 25 62 6c 00 00    	jmp    QWORD PTR [rip+0x6c62]        # 1400102a8 <__imp_WideCharToMultiByte>
   140009646:	90                   	nop
   140009647:	90                   	nop

0000000140009648 <VirtualQuery>:
   140009648:	ff 25 52 6c 00 00    	jmp    QWORD PTR [rip+0x6c52]        # 1400102a0 <__imp_VirtualQuery>
   14000964e:	90                   	nop
   14000964f:	90                   	nop

0000000140009650 <VirtualProtect>:
   140009650:	ff 25 42 6c 00 00    	jmp    QWORD PTR [rip+0x6c42]        # 140010298 <__imp_VirtualProtect>
   140009656:	90                   	nop
   140009657:	90                   	nop

0000000140009658 <TlsGetValue>:
   140009658:	ff 25 32 6c 00 00    	jmp    QWORD PTR [rip+0x6c32]        # 140010290 <__imp_TlsGetValue>
   14000965e:	90                   	nop
   14000965f:	90                   	nop

0000000140009660 <Sleep>:
   140009660:	ff 25 22 6c 00 00    	jmp    QWORD PTR [rip+0x6c22]        # 140010288 <__imp_Sleep>
   140009666:	90                   	nop
   140009667:	90                   	nop

0000000140009668 <SetUnhandledExceptionFilter>:
   140009668:	ff 25 12 6c 00 00    	jmp    QWORD PTR [rip+0x6c12]        # 140010280 <__imp_SetUnhandledExceptionFilter>
   14000966e:	90                   	nop
   14000966f:	90                   	nop

0000000140009670 <MultiByteToWideChar>:
   140009670:	ff 25 02 6c 00 00    	jmp    QWORD PTR [rip+0x6c02]        # 140010278 <__imp_MultiByteToWideChar>
   140009676:	90                   	nop
   140009677:	90                   	nop

0000000140009678 <LoadLibraryA>:
   140009678:	ff 25 f2 6b 00 00    	jmp    QWORD PTR [rip+0x6bf2]        # 140010270 <__imp_LoadLibraryA>
   14000967e:	90                   	nop
   14000967f:	90                   	nop

0000000140009680 <LeaveCriticalSection>:
   140009680:	ff 25 e2 6b 00 00    	jmp    QWORD PTR [rip+0x6be2]        # 140010268 <__imp_LeaveCriticalSection>
   140009686:	90                   	nop
   140009687:	90                   	nop

0000000140009688 <InitializeCriticalSection>:
   140009688:	ff 25 d2 6b 00 00    	jmp    QWORD PTR [rip+0x6bd2]        # 140010260 <__imp_InitializeCriticalSection>
   14000968e:	90                   	nop
   14000968f:	90                   	nop

0000000140009690 <GetProcAddress>:
   140009690:	ff 25 c2 6b 00 00    	jmp    QWORD PTR [rip+0x6bc2]        # 140010258 <__imp_GetProcAddress>
   140009696:	90                   	nop
   140009697:	90                   	nop

0000000140009698 <GetModuleHandleA>:
   140009698:	ff 25 b2 6b 00 00    	jmp    QWORD PTR [rip+0x6bb2]        # 140010250 <__imp_GetModuleHandleA>
   14000969e:	90                   	nop
   14000969f:	90                   	nop

00000001400096a0 <GetLastError>:
   1400096a0:	ff 25 a2 6b 00 00    	jmp    QWORD PTR [rip+0x6ba2]        # 140010248 <__imp_GetLastError>
   1400096a6:	90                   	nop
   1400096a7:	90                   	nop

00000001400096a8 <GetCPInfo>:
   1400096a8:	ff 25 92 6b 00 00    	jmp    QWORD PTR [rip+0x6b92]        # 140010240 <__imp_GetCPInfo>
   1400096ae:	90                   	nop
   1400096af:	90                   	nop

00000001400096b0 <FreeLibrary>:
   1400096b0:	ff 25 82 6b 00 00    	jmp    QWORD PTR [rip+0x6b82]        # 140010238 <__imp_FreeLibrary>
   1400096b6:	90                   	nop
   1400096b7:	90                   	nop

00000001400096b8 <EnterCriticalSection>:
   1400096b8:	ff 25 72 6b 00 00    	jmp    QWORD PTR [rip+0x6b72]        # 140010230 <__imp_EnterCriticalSection>
   1400096be:	90                   	nop
   1400096bf:	90                   	nop

00000001400096c0 <DeleteCriticalSection>:
   1400096c0:	ff 25 62 6b 00 00    	jmp    QWORD PTR [rip+0x6b62]        # 140010228 <__imp_DeleteCriticalSection>
   1400096c6:	90                   	nop
   1400096c7:	90                   	nop
   1400096c8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
   1400096cf:	00 

00000001400096d0 <D::f()>:
   1400096d0:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   1400096d3:	48 8b 50 e8          	mov    rdx,QWORD PTR [rax-0x18]
   1400096d7:	8b 41 08             	mov    eax,DWORD PTR [rcx+0x8]
   1400096da:	03 44 11 08          	add    eax,DWORD PTR [rcx+rdx*1+0x8]
   1400096de:	c3                   	ret
   1400096df:	90                   	nop

00000001400096e0 <virtual thunk to D::f()>:
   1400096e0:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   1400096e3:	48 03 48 e8          	add    rcx,QWORD PTR [rax-0x18]
   1400096e7:	48 8b 01             	mov    rax,QWORD PTR [rcx]
   1400096ea:	48 8b 50 e8          	mov    rdx,QWORD PTR [rax-0x18]
   1400096ee:	8b 41 08             	mov    eax,DWORD PTR [rcx+0x8]
   1400096f1:	03 44 11 08          	add    eax,DWORD PTR [rcx+rdx*1+0x8]
   1400096f5:	c3                   	ret
   1400096f6:	90                   	nop
   1400096f7:	90                   	nop
   1400096f8:	90                   	nop
   1400096f9:	90                   	nop
   1400096fa:	90                   	nop
   1400096fb:	90                   	nop
   1400096fc:	90                   	nop
   1400096fd:	90                   	nop
   1400096fe:	90                   	nop
   1400096ff:	90                   	nop

0000000140009700 <main>:
   140009700:	53                   	push   rbx
   140009701:	48 83 ec 40          	sub    rsp,0x40
   140009705:	e8 4d 81 ff ff       	call   140001857 <__main>
   14000970a:	48 8d 05 b7 20 00 00 	lea    rax,[rip+0x20b7]        # 14000b7c8 <vtable for D+0x18>
   140009711:	48 8d 4c 24 20       	lea    rcx,[rsp+0x20]
   140009716:	c7 44 24 38 64 00 00 	mov    DWORD PTR [rsp+0x38],0x64
   14000971d:	00 
   14000971e:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
   140009723:	48 83 c0 20          	add    rax,0x20
   140009727:	48 89 44 24 30       	mov    QWORD PTR [rsp+0x30],rax
   14000972c:	c7 44 24 28 07 00 00 	mov    DWORD PTR [rsp+0x28],0x7
   140009733:	00 
   140009734:	e8 27 80 ff ff       	call   140001760 <callD(D*)>
   140009739:	48 8d 4c 24 30       	lea    rcx,[rsp+0x30]
   14000973e:	89 c3                	mov    ebx,eax
   140009740:	e8 4b 80 ff ff       	call   140001790 <callB(B*)>
   140009745:	48 8d 0d 04 19 00 00 	lea    rcx,[rip+0x1904]        # 14000b050 <.rdata>
   14000974c:	8d 14 03             	lea    edx,[rbx+rax*1]
   14000974f:	e8 5c 99 ff ff       	call   1400030b0 <__mingw_printf>
   140009754:	31 c0                	xor    eax,eax
   140009756:	48 83 c4 40          	add    rsp,0x40
   14000975a:	5b                   	pop    rbx
   14000975b:	c3                   	ret
   14000975c:	90                   	nop
   14000975d:	90                   	nop
   14000975e:	90                   	nop
   14000975f:	90                   	nop

0000000140009760 <register_frame_ctor>:
   140009760:	e9 0b 7f ff ff       	jmp    140001670 <__gcc_register_frame>
   140009765:	90                   	nop
   140009766:	90                   	nop
   140009767:	90                   	nop
   140009768:	90                   	nop
   140009769:	90                   	nop
   14000976a:	90                   	nop
   14000976b:	90                   	nop
   14000976c:	90                   	nop
   14000976d:	90                   	nop
   14000976e:	90                   	nop
   14000976f:	90                   	nop
