/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/@luma.gl/shadertools@9.3.6/dist/index.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
import{clamp as ct,Matrix4 as ge}from"./math.gl-core4.1.0.js";import{log as ft}from"./luma.gl-core9.3.6.js";function x(e,t){if(!e){const o=new Error(t||"shadertools: assertion failed.");throw Error.captureStackTrace?.(o,x),o}}const K={number:{type:"number",validate(e,t){return Number.isFinite(e)&&typeof t=="object"&&(t.max===void 0||e<=t.max)&&(t.min===void 0||e>=t.min)}},array:{type:"array",validate(e,t){return Array.isArray(e)||ArrayBuffer.isView(e)}}};function pt(e){const t={};for(const[o,i]of Object.entries(e))t[o]=gt(i);return t}function ut(e,t,o){const i={};for(const[n,r]of Object.entries(t))e&&n in e&&!r.private?(r.validate&&x(r.validate(e[n],r),`${o}: invalid ${n}`),i[n]=e[n]):i[n]=r.value;return i}function gt(e){let t=me(e);if(t!=="object")return{value:e,...K[t],type:t};if(typeof e=="object")return e?e.type!==void 0?{...e,...K[e.type],type:e.type}:e.value===void 0?{type:"object",value:e}:(t=me(e.value),{...e,...K[t],type:t}):{type:"object",value:null};throw new Error("props")}function me(e){return Array.isArray(e)||ArrayBuffer.isView(e)?"array":typeof e}const mt=`#ifdef MODULE_LOGDEPTH
  logdepth_adjustPosition(gl_Position);
#endif
`,dt=`#ifdef MODULE_MATERIAL
  fragColor = material_filterColor(fragColor);
#endif

#ifdef MODULE_LIGHTING
  fragColor = lighting_filterColor(fragColor);
#endif

#ifdef MODULE_FOG
  fragColor = fog_filterColor(fragColor);
#endif

#ifdef MODULE_PICKING
  fragColor = picking_filterHighlightColor(fragColor);
  fragColor = picking_filterPickingColor(fragColor);
#endif

#ifdef MODULE_LOGDEPTH
  logdepth_setFragDepth();
#endif
`,ht={vertex:mt,fragment:dt},de=/void\s+main\s*\([^)]*\)\s*\{\n?/,he=/}\n?[^{}]*$/,X=[],D="__LUMA_INJECT_DECLARATIONS__";function _t(e){const t={vertex:{},fragment:{}};for(const o in e){let i=e[o];const n=bt(o);typeof i=="string"&&(i={order:0,injection:i}),t[n][o]=i}return t}function bt(e){const t=e.slice(0,2);switch(t){case"vs":return"vertex";case"fs":return"fragment";default:throw new Error(t)}}function H(e,t,o,i=!1){const n=t==="vertex";for(const r in o){const a=o[r];a.sort((s,c)=>s.order-c.order),X.length=a.length;for(let s=0,c=a.length;s<c;++s)X[s]=a[s].injection;const l=`${X.join(`
`)}
`;switch(r){case"vs:#decl":n&&(e=e.replace(D,l));break;case"vs:#main-start":n&&(e=e.replace(de,s=>s+l));break;case"vs:#main-end":n&&(e=e.replace(he,s=>l+s));break;case"fs:#decl":n||(e=e.replace(D,l));break;case"fs:#main-start":n||(e=e.replace(de,s=>s+l));break;case"fs:#main-end":n||(e=e.replace(he,s=>l+s));break;default:e=e.replace(r,s=>s+l)}}return e=e.replace(D,""),i&&(e=e.replace(/\}\s*$/,r=>r+ht[t])),e}function vt(e){const t={};return x(Array.isArray(e)&&e.length>1),e.forEach(o=>{for(const i in o)t[i]=t[i]?`${t[i]}
${o[i]}`:o[i]}),t}function y(e){e.map(t=>Z(t))}function Z(e){if(e.instance)return;y(e.dependencies||[]);const{propTypes:t={},deprecations:o=[],inject:i={}}=e,n={normalizedInjections:_t(i),parsedDeprecations:Lt(o)};t&&(n.propValidators=pt(t)),e.instance=n;let r={};t&&(r=Object.entries(t).reduce((a,[l,s])=>{const c=s?.value;return c&&(a[l]=c),a},{})),e.defaultUniforms={...e.defaultUniforms,...r}}function St(e,t,o){Z(e);const i=o||{...e.defaultUniforms};return t&&e.getUniforms?e.getUniforms(t,i):ut(t,e.instance?.propValidators,e.name)}function Y(e,t,o){e.deprecations?.forEach(i=>{i.regex?.test(t)&&(i.deprecated?o.deprecated(i.old,i.new)():o.removed(i.old,i.new)())})}function Lt(e){return e.forEach(t=>{t.type==="function"?t.regex=new RegExp(`\\b${t.old}\\(`):t.regex=new RegExp(`${t.type} ${t.old};`)}),e}function J(e){y(e);const t={},o={};G({modules:e,level:0,moduleMap:t,moduleDepth:o});const i=Object.keys(o).sort((n,r)=>o[r]-o[n]).map(n=>t[n]);return y(i),i}function G(e){const{modules:t,level:o,moduleMap:i,moduleDepth:n}=e;if(o>=5)throw new Error("Possible loop in shader dependency graph");for(const r of t)i[r.name]=r,(n[r.name]===void 0||n[r.name]<o)&&(n[r.name]=o);for(const r of t)r.dependencies&&G({modules:r.dependencies,level:o+1,moduleMap:i,moduleDepth:n})}function It(e){y(e);const t={},o={};return G({modules:e,level:0,moduleMap:t,moduleDepth:o}),e=Object.keys(o).sort((i,n)=>o[n]-o[i]).map(i=>t[i]),y(e),e}function Ct(e){return It(e)}const Rt=/^(?:uniform\s+)?(?:(?:lowp|mediump|highp)\s+)?[A-Za-z0-9_]+(?:<[^>]+>)?\s+([A-Za-z0-9_]+)(?:\s*\[[^\]]+\])?\s*;/,At=/((?:layout\s*\([^)]*\)\s*)*)uniform\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{([\s\S]*?)\}\s*([A-Za-z_][A-Za-z0-9_]*)?\s*;/g;function Q(e){return`${e.name}Uniforms`}function _e(e,t){const o=t==="wgsl"?e.source:t==="vertex"?e.vs:e.fs;if(!o)return null;const i=Q(e);return Et(o,t==="wgsl"?"wgsl":"glsl",i)}function be(e,t){const o=Object.keys(e.uniformTypes||{});if(!o.length)return null;const i=_e(e,t);return i?{moduleName:e.name,uniformBlockName:Q(e),stage:t,expectedUniformNames:o,actualUniformNames:i,matches:yt(o,i)}:null}function ve(e,t,o={}){const i=be(e,t);if(!i||i.matches)return i;const n=Nt(i);return o.log?.error?.(n,i)(),o.throwOnError!==!1&&x(!1,n),i}function ee(e){const t=[],o=Pt(e);for(const i of o.matchAll(At)){const n=i[1]?.trim()||null;t.push({blockName:i[2],body:i[3],instanceName:i[4]||null,layoutQualifier:n,hasLayoutQualifier:!!n,isStd140:!!(n&&/\blayout\s*\([^)]*\bstd140\b[^)]*\)/.exec(n))})}return t}function Se(e,t,o,i){const n=ee(e).filter(a=>!a.isStd140),r=new Set;for(const a of n){if(r.has(a.blockName))continue;r.add(a.blockName);const l=i?.label?`${i.label} `:"",s=a.hasLayoutQualifier?`declares ${Ut(a.layoutQualifier)} instead of layout(std140)`:"does not declare layout(std140)",c=`${l}${t} shader uniform block ${a.blockName} ${s}. luma.gl host-side shader block packing assumes explicit layout(std140) for GLSL uniform blocks. Add \`layout(std140)\` to the block declaration.`;o?.warn?.(c,a)()}return n}function Et(e,t,o){const i=t==="wgsl"?Mt(e,o):xt(e,o);if(!i)return null;const n=[];for(const r of i.split(`
`)){const a=r.replace(/\/\/.*$/,"").trim();if(!a||a.startsWith("#"))continue;const l=t==="wgsl"?a.match(/^([A-Za-z0-9_]+)\s*:/):a.match(Rt);l&&n.push(l[1])}return n}function Mt(e,t){const o=new RegExp(`\\bstruct\\s+${t}\\b`,"m").exec(e);if(!o)return null;const i=e.indexOf("{",o.index);if(i<0)return null;let n=0;for(let r=i;r<e.length;r++){const a=e[r];if(a==="{"){n++;continue}if(a==="}"&&(n--,n===0))return e.slice(i+1,r)}return null}function xt(e,t){return ee(e).find(i=>i.blockName===t)?.body||null}function yt(e,t){if(e.length!==t.length)return!1;for(let o=0;o<e.length;o++)if(e[o]!==t[o])return!1;return!0}function Nt(e){const{expectedUniformNames:t,actualUniformNames:o}=e,i=t.filter(l=>!o.includes(l)),n=o.filter(l=>!t.includes(l)),r=[`Expected ${t.length} fields, found ${o.length}.`],a=Tt(t,o);return a&&r.push(a),i.length&&r.push(`Missing from shader block (${i.length}): ${Le(i)}.`),n.length&&r.push(`Unexpected in shader block (${n.length}): ${Le(n)}.`),t.length<=12&&o.length<=12&&(i.length||n.length)&&(r.push(`Expected: ${t.join(", ")}.`),r.push(`Actual: ${o.join(", ")}.`)),`${e.moduleName}: ${e.stage} shader uniform block ${e.uniformBlockName} does not match module.uniformTypes. ${r.join(" ")}`}function Pt(e){return e.replace(/\/\*[\s\S]*?\*\//g,"").replace(/\/\/.*$/gm,"")}function Ut(e){return e.replace(/\s+/g," ").trim()}function Tt(e,t){const o=Math.min(e.length,t.length);for(let i=0;i<o;i++)if(e[i]!==t[i])return`First mismatch at field ${i+1}: expected ${e[i]}, found ${t[i]}.`;return e.length>t.length?`Shader block ends after field ${t.length}; expected next field ${e[t.length]}.`:t.length>e.length?`Shader block has extra field ${t.length}: ${t[e.length]}.`:null}function Le(e,t=8){if(e.length<=t)return e.join(", ");const o=e.length-t;return`${e.slice(0,t).join(", ")}, ... (${o} more)`}function Ot(e){switch(e?.gpu.toLowerCase()){case"apple":return`#define APPLE_GPU
// Apple optimizes away the calculation necessary for emulated fp64
#define LUMA_FP64_CODE_ELIMINATION_WORKAROUND 1
#define LUMA_FP32_TAN_PRECISION_WORKAROUND 1
// Intel GPU doesn't have full 32 bits precision in same cases, causes overflow
#define LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND 1
`;case"nvidia":return`#define NVIDIA_GPU
// Nvidia optimizes away the calculation necessary for emulated fp64
#define LUMA_FP64_CODE_ELIMINATION_WORKAROUND 1
`;case"intel":return`#define INTEL_GPU
// Intel optimizes away the calculation necessary for emulated fp64
#define LUMA_FP64_CODE_ELIMINATION_WORKAROUND 1
// Intel's built-in 'tan' function doesn't have acceptable precision
#define LUMA_FP32_TAN_PRECISION_WORKAROUND 1
// Intel GPU doesn't have full 32 bits precision in same cases, causes overflow
#define LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND 1
`;case"amd":return`#define AMD_GPU
`;default:return`#define DEFAULT_GPU
// Prevent driver from optimizing away the calculation necessary for emulated fp64
#define LUMA_FP64_CODE_ELIMINATION_WORKAROUND 1
// Headless Chrome's software shader 'tan' function doesn't have acceptable precision
#define LUMA_FP32_TAN_PRECISION_WORKAROUND 1
// If the GPU doesn't have full 32 bits precision, will causes overflow
#define LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND 1
`}}function Ft(e,t){if(Number(e.match(/^#version[ \t]+(\d+)/m)?.[1]||100)!==300)throw new Error("luma.gl v9 only supports GLSL 3.00 shader sources");switch(t){case"vertex":return e=Ce(e,Vt),e;case"fragment":return e=Ce(e,Bt),e;default:throw new Error(t)}}const Ie=[[/^(#version[ \t]+(100|300[ \t]+es))?[ \t]*\n/,`#version 300 es
`],[/\btexture(2D|2DProj|Cube)Lod(EXT)?\(/g,"textureLod("],[/\btexture(2D|2DProj|Cube)(EXT)?\(/g,"texture("]],Vt=[...Ie,[te("attribute"),"in $1"],[te("varying"),"out $1"]],Bt=[...Ie,[te("varying"),"in $1"]];function Ce(e,t){for(const[o,i]of t)e=e.replace(o,i);return e}function te(e){return new RegExp(`\\b${e}[ \\t]+(\\w+[ \\t]+\\w+(\\[\\w+\\])?;)`,"g")}function Re(e,t){let o="";for(const i in e){const n=e[i];if(o+=`void ${n.signature} {
`,n.header&&(o+=`  ${n.header}`),t[i]){const r=t[i];r.sort((a,l)=>a.order-l.order);for(const a of r)o+=`  ${a.injection}
`}n.footer&&(o+=`  ${n.footer}`),o+=`}
`}return o}function Ae(e){const t={vertex:{},fragment:{}};for(const o of e){let i,n;typeof o!="string"?(i=o,n=i.hook):(i={},n=o),n=n.trim();const[r,a]=n.split(":"),l=n.replace(/\(.+/,""),s=Object.assign(i,{signature:a});switch(r){case"vs":t.vertex[l]=s;break;case"fs":t.fragment[l]=s;break;default:throw new Error(r)}}return t}function Ee(e,t){return{name:wt(e,t),language:"glsl",version:kt(e)}}function wt(e,t="unnamed"){const i=/#define[^\S\r\n]*SHADER_NAME[^\S\r\n]*([A-Za-z0-9_-]+)\s*/.exec(e);return i?i[1]:t}function kt(e){let t=100;const o=e.match(/[^\s]+/g);if(o&&o.length>=2&&o[0]==="#version"){const i=parseInt(o[1],10);Number.isFinite(i)&&(t=i)}if(t!==100&&t!==300)throw new Error(`Invalid GLSL version ${t}`);return t}const S="(?:var<\\s*(uniform|storage(?:\\s*,\\s*[A-Za-z_][A-Za-z0-9_]*)?)\\s*>|var)\\s+([A-Za-z_][A-Za-z0-9_]*)",L="\\s*",V=[new RegExp(`@binding\\(\\s*(auto|\\d+)\\s*\\)${L}@group\\(\\s*(\\d+)\\s*\\)${L}${S}`,"g"),new RegExp(`@group\\(\\s*(\\d+)\\s*\\)${L}@binding\\(\\s*(auto|\\d+)\\s*\\)${L}${S}`,"g")],oe=[new RegExp(`@binding\\(\\s*(auto|\\d+)\\s*\\)${L}@group\\(\\s*(\\d+)\\s*\\)${L}${S}`,"g"),new RegExp(`@group\\(\\s*(\\d+)\\s*\\)${L}@binding\\(\\s*(auto|\\d+)\\s*\\)${L}${S}`,"g")],Dt=[new RegExp(`@binding\\(\\s*(\\d+)\\s*\\)${L}@group\\(\\s*(\\d+)\\s*\\)${L}${S}`,"g"),new RegExp(`@group\\(\\s*(\\d+)\\s*\\)${L}@binding\\(\\s*(\\d+)\\s*\\)${L}${S}`,"g")],Ht=[new RegExp(`@binding\\(\\s*(auto)\\s*\\)\\s*@group\\(\\s*(\\d+)\\s*\\)\\s*${S}`,"g"),new RegExp(`@group\\(\\s*(\\d+)\\s*\\)\\s*@binding\\(\\s*(auto)\\s*\\)\\s*${S}`,"g"),new RegExp(`@binding\\(\\s*(auto)\\s*\\)\\s*@group\\(\\s*(\\d+)\\s*\\)(?:[\\s\\n\\r]*@[A-Za-z_][^\\n\\r]*)*[\\s\\n\\r]*${S}`,"g"),new RegExp(`@group\\(\\s*(\\d+)\\s*\\)\\s*@binding\\(\\s*(auto)\\s*\\)(?:[\\s\\n\\r]*@[A-Za-z_][^\\n\\r]*)*[\\s\\n\\r]*${S}`,"g")];function ie(e){const t=e.split("");let o=0,i=0,n=!1,r=!1,a=!1;for(;o<e.length;){const l=e[o],s=e[o+1];if(r){a?a=!1:l==="\\"?a=!0:l==='"'&&(r=!1),o++;continue}if(n){l===`
`||l==="\r"?n=!1:t[o]=" ",o++;continue}if(i>0){if(l==="/"&&s==="*"){t[o]=" ",t[o+1]=" ",i++,o+=2;continue}if(l==="*"&&s==="/"){t[o]=" ",t[o+1]=" ",i--,o+=2;continue}l!==`
`&&l!=="\r"&&(t[o]=" "),o++;continue}if(l==='"'){r=!0,o++;continue}if(l==="/"&&s==="/"){t[o]=" ",t[o+1]=" ",n=!0,o+=2;continue}if(l==="/"&&s==="*"){t[o]=" ",t[o+1]=" ",i=1,o+=2;continue}o++}return t.join("")}function U(e,t){const o=ie(e),i=[];for(const n of t){n.lastIndex=0;let r;for(r=n.exec(o);r;){const a=n===t[0],l=r.index,s=r[0].length;i.push({match:e.slice(l,l+s),index:l,length:s,bindingToken:r[a?1:2],groupToken:r[a?2:1],accessDeclaration:r[3]?.trim(),name:r[4]}),r=n.exec(o)}}return i.sort((n,r)=>n.index-r.index)}function Me(e,t,o){const i=U(e,t);if(!i.length)return e;let n="",r=0;for(const a of i)n+=e.slice(r,a.index),n+=o(a),r=a.index+a.length;return n+=e.slice(r),n}function xe(e){return/@binding\(\s*auto\s*\)/.test(ie(e))}function Gt(e,t){return U(e,t===V||t===oe?Ht:t).find(i=>i.bindingToken==="auto")}const ye=[new RegExp(`@binding\\(\\s*(\\d+)\\s*\\)\\s*@group\\(\\s*(\\d+)\\s*\\)\\s*${S}\\s*:\\s*([^;]+);`,"g"),new RegExp(`@group\\(\\s*(\\d+)\\s*\\)\\s*@binding\\(\\s*(\\d+)\\s*\\)\\s*${S}\\s*:\\s*([^;]+);`,"g")];function Ne(e,t=[]){const o=ie(e),i=new Map;for(const r of t)i.set(Pe(r.name,r.group,r.location),r.moduleName);const n=[];for(const r of ye){r.lastIndex=0;let a;for(a=r.exec(o);a;){const l=r===ye[0],s=Number(a[l?1:2]),c=Number(a[l?2:1]),f=a[3]?.trim(),p=a[4],u=a[5].trim(),m=i.get(Pe(p,c,s));n.push(zt({name:p,group:c,binding:s,owner:m?"module":"application",moduleName:m,accessDeclaration:f,resourceType:u})),a=r.exec(o)}}return n.sort((r,a)=>r.group!==a.group?r.group-a.group:r.binding!==a.binding?r.binding-a.binding:r.name.localeCompare(a.name))}function zt(e){const t={name:e.name,group:e.group,binding:e.binding,owner:e.owner,kind:"unknown",moduleName:e.moduleName,resourceType:e.resourceType};if(e.accessDeclaration){const o=e.accessDeclaration.split(",").map(i=>i.trim());if(o[0]==="uniform")return{...t,kind:"uniform",access:"uniform"};if(o[0]==="storage"){const i=o[1]||"read_write";return{...t,kind:i==="read"?"read-only-storage":"storage",access:i}}}return e.resourceType==="sampler"||e.resourceType==="sampler_comparison"?{...t,kind:"sampler",samplerKind:e.resourceType==="sampler_comparison"?"comparison":"filtering"}:e.resourceType.startsWith("texture_storage_")?{...t,kind:"storage-texture",access:jt(e.resourceType),viewDimension:Ue(e.resourceType)}:e.resourceType.startsWith("texture_")?{...t,kind:"texture",viewDimension:Ue(e.resourceType),sampleType:$t(e.resourceType),multisampled:e.resourceType.startsWith("texture_multisampled_")}:t}function Pe(e,t,o){return`${t}:${o}:${e}`}function Ue(e){if(e.includes("cube_array"))return"cube-array";if(e.includes("2d_array"))return"2d-array";if(e.includes("cube"))return"cube";if(e.includes("3d"))return"3d";if(e.includes("2d"))return"2d";if(e.includes("1d"))return"1d"}function $t(e){if(e.startsWith("texture_depth_"))return"depth";if(e.includes("<i32>"))return"sint";if(e.includes("<u32>"))return"uint";if(e.includes("<f32>"))return"float"}function jt(e){return/,\s*([A-Za-z_][A-Za-z0-9_]*)\s*>$/.exec(e)?.[1]}const re=`

${D}
`,B=100,Wt=`precision highp float;
`;function qt(e){const t=J(e.modules||[]),{source:o,bindingAssignments:i}=Kt(e.platformInfo,{...e,source:e.source,stage:"vertex",modules:t});return{source:o,getUniforms:Fe(t),bindingAssignments:i,bindingTable:Ne(o,i)}}function Te(e){const{vs:t,fs:o}=e,i=J(e.modules||[]);return{vs:Oe(e.platformInfo,{...e,source:t,stage:"vertex",modules:i}),fs:Oe(e.platformInfo,{...e,source:o,stage:"fragment",modules:i}),getUniforms:Fe(i)}}function Kt(e,t){const{source:o,stage:i,modules:n,hookFunctions:r=[],inject:a={},log:l}=t;x(typeof o=="string","shader source must be a string");const s=o;let c="";const f=Ae(r),p={},u={},m={};for(const h in a){const I=typeof a[h]=="string"?{injection:a[h],order:0}:a[h],C=/^(v|f)s:(#)?([\w-]+)$/.exec(h);if(C){const d=C[2],b=C[3];d?b==="decl"?u[h]=[I]:m[h]=[I]:p[h]=[I]}else m[h]=[I]}const _=n,M=Yt(s),A=Zt(M.source),g=to(_,t._bindingRegistry,A),F=[];for(const h of _){l&&Y(h,s,l);const I=Jt(ne(h,"wgsl",l),h,{usedBindingsByGroup:A,bindingRegistry:t._bindingRegistry,reservedBindingKeysByGroup:g});F.push(...I.bindingAssignments);const C=I.source;c+=C;const d=h.injections?.[i]||{};for(const b in d){const R=/^(v|f)s:#([\w-]+)$/.exec(b);if(R){const E=R[2]==="decl"?u:m;E[b]=E[b]||[],E[b].push(d[b])}else p[b]=p[b]||[],p[b].push(d[b])}}return c+=re,c=H(c,i,u),c+=Re(f[i],p),c+=ao(F),c+=M.source,c=H(c,i,m),no(c),{source:c,bindingAssignments:F}}function Oe(e,t){const{source:o,stage:i,language:n="glsl",modules:r,defines:a={},hookFunctions:l=[],inject:s={},prologue:c=!0,log:f}=t;x(typeof o=="string","shader source must be a string");const p=n==="glsl"?Ee(o).version:-1,u=e.shaderLanguageVersion,m=p===100?"#version 100":"#version 300 es",M=o.split(`
`).slice(1).join(`
`),A={};r.forEach(d=>{Object.assign(A,d.defines)}),Object.assign(A,a);let g="";switch(n){case"wgsl":break;case"glsl":g=c?`${m}

// ----- PROLOGUE -------------------------
${`#define SHADER_TYPE_${i.toUpperCase()}`}

${Ot(e)}
${i==="fragment"?Wt:""}

// ----- APPLICATION DEFINES -------------------------

${Xt(A)}

`:`${m}
`;break}const F=Ae(l),h={},I={},C={};for(const d in s){const b=typeof s[d]=="string"?{injection:s[d],order:0}:s[d],R=/^(v|f)s:(#)?([\w-]+)$/.exec(d);if(R){const v=R[2],E=R[3];v?E==="decl"?I[d]=[b]:C[d]=[b]:h[d]=[b]}else C[d]=[b]}for(const d of r){f&&Y(d,M,f);const b=ne(d,i,f);g+=b;const R=d.instance?.normalizedInjections[i]||{};for(const v in R){const E=/^(v|f)s:#([\w-]+)$/.exec(v);if(E){const q=E[2]==="decl"?I:C;q[v]=q[v]||[],q[v].push(R[v])}else h[v]=h[v]||[],h[v].push(R[v])}}return g+="// ----- MAIN SHADER SOURCE -------------------------",g+=re,g=H(g,i,I),g+=Re(F[i],h),g+=M,g=H(g,i,C),n==="glsl"&&p!==u&&(g=Ft(g,i)),n==="glsl"&&Se(g,i,f),g.trim()}function Fe(e){return function(o){const i={};for(const n of e){const r=n.getUniforms?.(o,i);Object.assign(i,r)}return i}}function Xt(e={}){let t="";for(const o in e){const i=e[o];(i||Number.isFinite(i))&&(t+=`#define ${o.toUpperCase()} ${e[o]}
`)}return t}function ne(e,t,o){let i;switch(t){case"vertex":i=e.vs||"";break;case"fragment":i=e.fs||"";break;case"wgsl":i=e.source||"";break;default:x(!1)}if(!e.name)throw new Error("Shader module must have a name");ve(e,t,{log:o});const n=e.name.toUpperCase().replace(/[^0-9a-z]/gi,"_");let r=`// ----- MODULE ${e.name} ---------------

`;return t!=="wgsl"&&(r+=`#define MODULE_${n}
`),r+=`${i}
`,r}function Zt(e){const t=new Map;for(const o of U(e,Dt)){const i=Number(o.bindingToken),n=Number(o.groupToken);ae(n,i,o.name),T(t,n,i,`application binding "${o.name}"`)}return t}function Yt(e){const t=U(e,oe),o=new Map;for(const r of t){if(r.bindingToken==="auto")continue;const a=Number(r.bindingToken),l=Number(r.groupToken);ae(l,a,r.name),T(o,l,a,`application binding "${r.name}"`)}const i={sawSupportedBindingDeclaration:t.length>0},n=Me(e,oe,r=>eo(r,o,i));if(xe(e)&&!i.sawSupportedBindingDeclaration)throw new Error('Unsupported @binding(auto) declaration form in application WGSL. Use adjacent "@group(N)" and "@binding(auto)" decorators followed by a bindable "var" declaration.');return{source:n}}function Jt(e,t,o){const i=[],r={sawSupportedBindingDeclaration:U(e,V).length>0,nextHintedBindingLocation:typeof t.firstBindingSlot=="number"?t.firstBindingSlot:null},a=Me(e,V,l=>Qt(l,{module:t,context:o,bindingAssignments:i,relocationState:r}));if(xe(e)&&!r.sawSupportedBindingDeclaration)throw new Error(`Unsupported @binding(auto) declaration form in module "${t.name}". Use adjacent "@group(N)" and "@binding(auto)" decorators followed by a bindable "var" declaration.`);return{source:a,bindingAssignments:i}}function Qt(e,t){const{module:o,context:i,bindingAssignments:n,relocationState:r}=t,{match:a,bindingToken:l,groupToken:s,name:c}=e,f=Number(s);if(l==="auto"){const u=we(f,o.name,c),m=i.bindingRegistry?.get(u),_=m!==void 0?m:r.nextHintedBindingLocation===null?Be(f,i.usedBindingsByGroup):Be(f,i.usedBindingsByGroup,r.nextHintedBindingLocation);return Ve(o.name,f,_,c),m!==void 0&&oo(i.reservedBindingKeysByGroup,f,_,u)?(n.push({moduleName:o.name,name:c,group:f,location:_}),a.replace(/@binding\(\s*auto\s*\)/,`@binding(${_})`)):(T(i.usedBindingsByGroup,f,_,`module "${o.name}" binding "${c}"`),i.bindingRegistry?.set(u,_),n.push({moduleName:o.name,name:c,group:f,location:_}),r.nextHintedBindingLocation!==null&&m===void 0&&(r.nextHintedBindingLocation=_+1),a.replace(/@binding\(\s*auto\s*\)/,`@binding(${_})`))}const p=Number(l);return Ve(o.name,f,p,c),T(i.usedBindingsByGroup,f,p,`module "${o.name}" binding "${c}"`),n.push({moduleName:o.name,name:c,group:f,location:p}),a}function eo(e,t,o){const{match:i,bindingToken:n,groupToken:r,name:a}=e,l=Number(r);if(n==="auto"){const s=ro(l,t);return ae(l,s,a),T(t,l,s,`application binding "${a}"`),i.replace(/@binding\(\s*auto\s*\)/,`@binding(${s})`)}return o.sawSupportedBindingDeclaration=!0,i}function to(e,t,o){const i=new Map;if(!t)return i;for(const n of e)for(const r of io(n)){const a=we(r.group,n.name,r.name),l=t.get(a);if(l!==void 0){const s=i.get(r.group)||new Map,c=s.get(l);if(c&&c!==a)throw new Error(`Duplicate WGSL binding reservation for modules "${c}" and "${a}": group ${r.group}, binding ${l}.`);T(o,r.group,l,`registered module binding "${a}"`),s.set(l,a),i.set(r.group,s)}}return i}function oo(e,t,o,i){const n=e.get(t);if(!n)return!1;const r=n.get(o);if(!r)return!1;if(r!==i)throw new Error(`Registered module binding "${i}" collided with "${r}": group ${t}, binding ${o}.`);return!0}function io(e){const t=[],o=e.source||"";for(const i of U(o,V))t.push({name:i.name,group:Number(i.groupToken)});return t}function ae(e,t,o){if(e===0&&t>=B)throw new Error(`Application binding "${o}" in group 0 uses reserved binding ${t}. Application-owned explicit group-0 bindings must stay below ${B}.`)}function Ve(e,t,o,i){if(t===0&&o<B)throw new Error(`Module "${e}" binding "${i}" in group 0 uses reserved application binding ${o}. Module-owned explicit group-0 bindings must be ${B} or higher.`)}function T(e,t,o,i){const n=e.get(t)||new Set;if(n.has(o))throw new Error(`Duplicate WGSL binding assignment for ${i}: group ${t}, binding ${o}.`);n.add(o),e.set(t,n)}function Be(e,t,o){const i=t.get(e)||new Set;let n=o??(e===0?B:i.size>0?Math.max(...i)+1:0);for(;i.has(n);)n++;return n}function ro(e,t){const o=t.get(e)||new Set;let i=0;for(;o.has(i);)i++;return i}function no(e){const t=Gt(e,V);if(!t)return;const o=lo(e,t.index);throw o?new Error(`Unresolved @binding(auto) for module "${o}" binding "${t.name}" remained in assembled WGSL source.`):so(e,t.index)?new Error(`Unresolved @binding(auto) for application binding "${t.name}" remained in assembled WGSL source.`):new Error(`Unresolved @binding(auto) remained in assembled WGSL source near "${co(t.match)}".`)}function ao(e){if(e.length===0)return"";let t=`// ----- MODULE WGSL BINDING ASSIGNMENTS ---------------
`;for(const o of e)t+=`// ${o.moduleName}.${o.name} -> @group(${o.group}) @binding(${o.location})
`;return t+=`
`,t}function we(e,t,o){return`${e}:${t}:${o}`}function lo(e,t){const o=/^\/\/ ----- MODULE ([^\n]+) ---------------$/gm;let i,n;for(n=o.exec(e);n&&n.index<=t;)i=n[1],n=o.exec(e);return i}function so(e,t){const o=e.indexOf(re);return o>=0?t>o:!0}function co(e){return e.replace(/\s+/g," ").trim()}const le="([a-zA-Z_][a-zA-Z0-9_]*)",fo=new RegExp(`^\\s*\\#\\s*ifdef\\s*${le}\\s*$`),po=new RegExp(`^\\s*\\#\\s*ifndef\\s*${le}\\s*(?:\\/\\/.*)?$`),uo=/^\s*\#\s*else\s*(?:\/\/.*)?$/,go=/^\s*\#\s*endif\s*$/,mo=new RegExp(`^\\s*\\#\\s*ifdef\\s*${le}\\s*(?:\\/\\/.*)?$`),ho=/^\s*\#\s*endif\s*(?:\/\/.*)?$/;function ke(e,t){const o=e.split(`
`),i=[],n=[];let r=!0;for(const a of o){const l=a.match(mo)||a.match(fo),s=a.match(po),c=a.match(uo),f=a.match(ho)||a.match(go);if(l||s){const p=(l||s)?.[1],u=!!t?.defines?.[p],m=l?u:!u,_=r&&m;n.push({parentActive:r,branchTaken:m,active:_}),r=_}else if(c){const p=n[n.length-1];if(!p)throw new Error("Encountered #else without matching #ifdef or #ifndef");p.active=p.parentActive&&!p.branchTaken,p.branchTaken=!0,r=p.active}else f?(n.pop(),r=n.length?n[n.length-1].active:!0):r&&i.push(a)}if(n.length>0)throw new Error("Unterminated conditional block in shader source");return i.join(`
`)}class O{static defaultShaderAssembler;_hookFunctions=[];_defaultModules=[];_wgslBindingRegistry=new Map;static getDefaultShaderAssembler(){return O.defaultShaderAssembler=O.defaultShaderAssembler||new O,O.defaultShaderAssembler}addDefaultModule(t){this._defaultModules.find(o=>o.name===(typeof t=="string"?t:t.name))||this._defaultModules.push(t)}removeDefaultModule(t){const o=typeof t=="string"?t:t.name;this._defaultModules=this._defaultModules.filter(i=>i.name!==o)}addShaderHook(t,o){o&&(t=Object.assign(o,{hook:t})),this._hookFunctions.push(t)}assembleWGSLShader(t){const o=this._getModuleList(t.modules),i=this._hookFunctions,{source:n,getUniforms:r,bindingAssignments:a}=qt({...t,source:t.source,_bindingRegistry:this._wgslBindingRegistry,modules:o,hookFunctions:i}),l={...o.reduce((c,f)=>(Object.assign(c,f.defines),c),{}),...t.defines},s=t.platformInfo.shaderLanguage==="wgsl"?ke(n,{defines:l}):n;return{source:s,getUniforms:r,modules:o,bindingAssignments:a,bindingTable:Ne(s,a)}}assembleGLSLShaderPair(t){const o=this._getModuleList(t.modules),i=this._hookFunctions;return{...Te({...t,vs:t.vs,fs:t.fs,modules:o,hookFunctions:i}),modules:o}}_getModuleList(t=[]){const o=new Array(this._defaultModules.length+t.length),i={};let n=0;for(let r=0,a=this._defaultModules.length;r<a;++r){const l=this._defaultModules[r],s=l.name;o[n++]=l,i[s]=!0}for(let r=0,a=t.length;r<a;++r){const l=t[r],s=l.name;i[s]||(o[n++]=l,i[s]=!0)}return o.length=n,y(o),o}}const _o=`out vec4 transform_output;
void main() {
  transform_output = vec4(0);
}`,bo=`#version 300 es
${_o}`;function vo(e,t){t=Array.isArray(t)?t:[t];const o=e.replace(/^\s+/,"").split(/\s+/),[i,n,r]=o;if(!t.includes(i)||!n||!r)return null;const a=r.split(";")[0];return{qualifier:i,type:n,name:a}}function So(e){const{input:t,inputChannels:o,output:i}=e||{};if(!t)return bo;if(!o)throw new Error("inputChannels");const n=Co(o),r=De(t,o);return`#version 300 es
in ${n} ${t};
out vec4 ${i};
void main() {
  ${i} = ${r};
}`}function Lo(e){switch(e){case"float":return"x";case"vec2":return"xy";case"vec3":return"xyz";case"vec4":return"xyzw";default:throw new Error(e)}}function Io(e){switch(e){case"float":return 1;case"vec2":return 2;case"vec3":return 3;case"vec4":return 4;default:throw new Error(e)}}function Co(e){switch(e){case 1:return"float";case 2:return"vec2";case 3:return"vec3";case 4:return"vec4";default:throw new Error(`invalid channels: ${e}`)}}function De(e,t){switch(t){case 1:return`vec4(${e}, 0.0, 0.0, 1.0)`;case 2:return`vec4(${e}, 0.0, 1.0)`;case 3:return`vec4(${e}, 1.0)`;case 4:return e;default:throw new Error(`invalid channels: ${t}`)}}function z(e){return typeof e=="string"?e.charAt(0).toUpperCase()+e.slice(1):e}function Ro(e,t){return Ao(e,t)}function Ao(e,t){const o=[];switch(t.uniforms){case"scoped-interface-blocks":case"unscoped-interface-blocks":o.push(`layout(std140) uniform ${z(e.name)} {`);break}for(const[i,n]of Object.entries(e.uniformTypes||{})){if(typeof n!="string")throw new Error(`Composite uniform types are not supported by GLSL shader generation: ${e.name}.${i}`);const r=Eo(n);switch(t.uniforms){case"scoped-interface-blocks":o.push(`  ${r} ${i};`);break;case"unscoped-interface-blocks":o.push(`  ${r} ${e.name}_${i};`);break;case"uniforms":o.push(`uniform ${r} ${e.name}_${i};`)}}switch(t.uniforms){case"scoped-interface-blocks":o.push(`} ${e.name};`);break;case"unscoped-interface-blocks":o.push("};");break}return o.push(""),o.join(`
`)}function Eo(e){return{f32:"float",i32:"int",u32:"uint","vec2<f32>":"vec2","vec3<f32>":"vec3","vec4<f32>":"vec4","vec2<i32>":"ivec2","vec3<i32>":"ivec3","vec4<i32>":"ivec4","vec2<u32>":"uvec2","vec3<u32>":"uvec3","vec4<u32>":"uvec4","mat2x2<f32>":"mat2","mat2x3<f32>":"mat2x3","mat2x4<f32>":"mat2x4","mat3x2<f32>":"mat3x2","mat3x3<f32>":"mat3","mat3x4<f32>":"mat3x4","mat4x2<f32>":"mat4x2","mat4x3<f32>":"mat4x3","mat4x4<f32>":"mat4"}[e]}function Mo(e,t){return xo(e)}function xo(e,t){const o=[];o.push(`struct ${z(e.name)} {`);for(const[i,n]of Object.entries(e?.uniformTypes||{})){if(typeof n!="string")throw new Error(`Composite uniform types are not supported by WGSL shader generation: ${e.name}.${i}`);const r=n;o.push(`  ${i} : ${r};`)}return o.push("};"),o.push(`var<uniform> ${e.name} : ${z(e.name)};`),o.join(`
`)}function yo(e,t){switch(t.shaderLanguage){case"glsl":return Ro(e,t);case"wgsl":return Mo(e)}}let N=null;const He=new ArrayBuffer(4),Ge=new Float32Array(He),ze=new Uint32Array(He);function No(e){N||=$e(),e=ct(e,-65504,65504),Ge[0]=e;const t=ze[0],o=t>>23&511;return N.baseTable[o]+((t&8388607)>>N.shiftTable[o])}function Po(e){N||=$e();const t=e>>10;return ze[0]=N.mantissaTable[N.offsetTable[t]+(e&1023)]+N.exponentTable[t],Ge[0]}function $e(){const e=new Uint32Array(512),t=new Uint32Array(512);for(let r=0;r<256;++r){const a=r-127;a<-27?(e[r]=0,e[r|256]=32768,t[r]=24,t[r|256]=24):a<-14?(e[r]=1024>>-a-14,e[r|256]=1024>>-a-14|32768,t[r]=-a-1,t[r|256]=-a-1):a<=15?(e[r]=a+15<<10,e[r|256]=a+15<<10|32768,t[r]=13,t[r|256]=13):a<128?(e[r]=31744,e[r|256]=64512,t[r]=24,t[r|256]=24):(e[r]=31744,e[r|256]=64512,t[r]=13,t[r|256]=13)}const o=new Uint32Array(2048),i=new Uint32Array(64),n=new Uint32Array(64);for(let r=1;r<1024;++r){let a=r<<13,l=0;for(;(a&8388608)===0;)a<<=1,l-=8388608;a&=-8388609,l+=947912704,o[r]=a|l}for(let r=1024;r<2048;++r)o[r]=939524096+(r-1024<<13);for(let r=1;r<31;++r)i[r]=r<<23;i[31]=1199570944,i[32]=2147483648;for(let r=33;r<63;++r)i[r]=2147483648+(r-32<<23);i[63]=3347054592;for(let r=1;r<64;++r)r!==32&&(n[r]=1024);return{baseTable:e,shiftTable:t,mantissaTable:o,exponentTable:i,offsetTable:n}}function $(e,t=[],o=0){const i=Math.fround(e),n=e-i;return t[o]=i,t[o+1]=n,t}function se(e){return e-Math.fround(e)}function ce(e){const t=new Float32Array(32);for(let o=0;o<4;++o)for(let i=0;i<4;++i){const n=o*4+i;$(e[i*4+o],t,n*2)}return t}function fe(e,t=!0){return e??t}function pe(e=[0,0,0],t=!0){return t?e.map(o=>o/255):[...e]}function je(e,t=!0){const o=pe(e.slice(0,3),t),i=Number.isFinite(e[3]),n=i?e[3]:1;return[o[0],o[1],o[2],t&&i?n/255:n]}const Uo=`fn random(scale: vec3f, seed: f32) -> f32 {
  return fract(sin(dot(scale + vec3f(seed), vec3f(12.9898, 78.233, 151.7182))) * 43758.5453 + seed);
}
`,To=`float random(vec3 scale, float seed) {
  /* use the fragment position for a different seed per-pixel */
  return fract(sin(dot(gl_FragCoord.xyz + seed, scale)) * 43758.5453 + seed);
}
`,Oo={name:"random",source:Uo,fs:To},Fo=`#ifdef LUMA_FP32_TAN_PRECISION_WORKAROUND

// All these functions are for substituting tan() function from Intel GPU only
const float TWO_PI = 6.2831854820251465;
const float PI_2 = 1.5707963705062866;
const float PI_16 = 0.1963495463132858;

const float SIN_TABLE_0 = 0.19509032368659973;
const float SIN_TABLE_1 = 0.3826834261417389;
const float SIN_TABLE_2 = 0.5555702447891235;
const float SIN_TABLE_3 = 0.7071067690849304;

const float COS_TABLE_0 = 0.9807852506637573;
const float COS_TABLE_1 = 0.9238795042037964;
const float COS_TABLE_2 = 0.8314695954322815;
const float COS_TABLE_3 = 0.7071067690849304;

const float INVERSE_FACTORIAL_3 = 1.666666716337204e-01; // 1/3!
const float INVERSE_FACTORIAL_5 = 8.333333767950535e-03; // 1/5!
const float INVERSE_FACTORIAL_7 = 1.9841270113829523e-04; // 1/7!
const float INVERSE_FACTORIAL_9 = 2.75573188446287533e-06; // 1/9!

float sin_taylor_fp32(float a) {
  float r, s, t, x;

  if (a == 0.0) {
    return 0.0;
  }

  x = -a * a;
  s = a;
  r = a;

  r = r * x;
  t = r * INVERSE_FACTORIAL_3;
  s = s + t;

  r = r * x;
  t = r * INVERSE_FACTORIAL_5;
  s = s + t;

  r = r * x;
  t = r * INVERSE_FACTORIAL_7;
  s = s + t;

  r = r * x;
  t = r * INVERSE_FACTORIAL_9;
  s = s + t;

  return s;
}

void sincos_taylor_fp32(float a, out float sin_t, out float cos_t) {
  if (a == 0.0) {
    sin_t = 0.0;
    cos_t = 1.0;
  }
  sin_t = sin_taylor_fp32(a);
  cos_t = sqrt(1.0 - sin_t * sin_t);
}

float tan_taylor_fp32(float a) {
    float sin_a;
    float cos_a;

    if (a == 0.0) {
        return 0.0;
    }

    // 2pi range reduction
    float z = floor(a / TWO_PI);
    float r = a - TWO_PI * z;

    float t;
    float q = floor(r / PI_2 + 0.5);
    int j = int(q);

    if (j < -2 || j > 2) {
        return 1.0 / 0.0;
    }

    t = r - PI_2 * q;

    q = floor(t / PI_16 + 0.5);
    int k = int(q);
    int abs_k = int(abs(float(k)));

    if (abs_k > 4) {
        return 1.0 / 0.0;
    } else {
        t = t - PI_16 * q;
    }

    float u = 0.0;
    float v = 0.0;

    float sin_t, cos_t;
    float s, c;
    sincos_taylor_fp32(t, sin_t, cos_t);

    if (k == 0) {
        s = sin_t;
        c = cos_t;
    } else {
        if (abs(float(abs_k) - 1.0) < 0.5) {
            u = COS_TABLE_0;
            v = SIN_TABLE_0;
        } else if (abs(float(abs_k) - 2.0) < 0.5) {
            u = COS_TABLE_1;
            v = SIN_TABLE_1;
        } else if (abs(float(abs_k) - 3.0) < 0.5) {
            u = COS_TABLE_2;
            v = SIN_TABLE_2;
        } else if (abs(float(abs_k) - 4.0) < 0.5) {
            u = COS_TABLE_3;
            v = SIN_TABLE_3;
        }
        if (k > 0) {
            s = u * sin_t + v * cos_t;
            c = u * cos_t - v * sin_t;
        } else {
            s = u * sin_t - v * cos_t;
            c = u * cos_t + v * sin_t;
        }
    }

    if (j == 0) {
        sin_a = s;
        cos_a = c;
    } else if (j == 1) {
        sin_a = c;
        cos_a = -s;
    } else if (j == -1) {
        sin_a = -c;
        cos_a = s;
    } else {
        sin_a = -s;
        cos_a = -c;
    }
    return sin_a / cos_a;
}
#endif

float tan_fp32(float a) {
#ifdef LUMA_FP32_TAN_PRECISION_WORKAROUND
  return tan_taylor_fp32(a);
#else
  return tan(a);
#endif
}
`,Vo={name:"fp32",vs:Fo},We=`
layout(std140) uniform fp64arithmeticUniforms {
  uniform float ONE;
  uniform float SPLIT;
} fp64;

/*
About LUMA_FP64_CODE_ELIMINATION_WORKAROUND

The purpose of this workaround is to prevent shader compilers from
optimizing away necessary arithmetic operations by swapping their sequences
or transform the equation to some 'equivalent' form.

These helpers implement Dekker/Veltkamp-style error tracking. If the compiler
folds constants or reassociates the arithmetic, the high/low split can stop
tracking the rounding error correctly. That failure mode tends to look fine in
simple coordinate setup, but then breaks down inside iterative arithmetic such
as fp64 Mandelbrot loops.

The method is to multiply an artifical variable, ONE, which will be known to
the compiler to be 1 only at runtime. The whole expression is then represented
as a polynomial with respective to ONE. In the coefficients of all terms, only one a
and one b should appear

err = (a + b) * ONE^6 - a * ONE^5 - (a + b) * ONE^4 + a * ONE^3 - b - (a + b) * ONE^2 + a * ONE
*/

float prevent_fp64_optimization(float value) {
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  return value + fp64.ONE * 0.0;
#else
  return value;
#endif
}

// Divide float number to high and low floats to extend fraction bits
vec2 split(float a) {
  // Keep SPLIT as a runtime uniform so the compiler cannot fold the Dekker
  // split into a constant expression and reassociate the recovery steps.
  float split = prevent_fp64_optimization(fp64.SPLIT);
  float t = prevent_fp64_optimization(a * split);
  float temp = t - a;
  float a_hi = t - temp;
  float a_lo = a - a_hi;
  return vec2(a_hi, a_lo);
}

// Divide float number again when high float uses too many fraction bits
vec2 split2(vec2 a) {
  vec2 b = split(a.x);
  b.y += a.y;
  return b;
}

// Special sum operation when a > b
vec2 quickTwoSum(float a, float b) {
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  float sum = (a + b) * fp64.ONE;
  float err = b - (sum - a) * fp64.ONE;
#else
  float sum = a + b;
  float err = b - (sum - a);
#endif
  return vec2(sum, err);
}

// General sum operation
vec2 twoSum(float a, float b) {
  float s = (a + b);
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  float v = (s * fp64.ONE - a) * fp64.ONE;
  float err = (a - (s - v) * fp64.ONE) * fp64.ONE * fp64.ONE * fp64.ONE + (b - v);
#else
  float v = s - a;
  float err = (a - (s - v)) + (b - v);
#endif
  return vec2(s, err);
}

vec2 twoSub(float a, float b) {
  float s = (a - b);
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  float v = (s * fp64.ONE - a) * fp64.ONE;
  float err = (a - (s - v) * fp64.ONE) * fp64.ONE * fp64.ONE * fp64.ONE - (b + v);
#else
  float v = s - a;
  float err = (a - (s - v)) - (b + v);
#endif
  return vec2(s, err);
}

vec2 twoSqr(float a) {
  float prod = a * a;
  vec2 a_fp64 = split(a);
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  float err = ((a_fp64.x * a_fp64.x - prod) * fp64.ONE + 2.0 * a_fp64.x *
    a_fp64.y * fp64.ONE * fp64.ONE) + a_fp64.y * a_fp64.y * fp64.ONE * fp64.ONE * fp64.ONE;
#else
  float err = ((a_fp64.x * a_fp64.x - prod) + 2.0 * a_fp64.x * a_fp64.y) + a_fp64.y * a_fp64.y;
#endif
  return vec2(prod, err);
}

vec2 twoProd(float a, float b) {
  float prod = a * b;
  vec2 a_fp64 = split(a);
  vec2 b_fp64 = split(b);
  // twoProd is especially sensitive because mul_fp64 and div_fp64 both depend
  // on the split terms and cross terms staying in the original evaluation
  // order. If the compiler folds or reassociates them, the low part tends to
  // collapse to zero or NaN on some drivers.
  float highProduct = prevent_fp64_optimization(a_fp64.x * b_fp64.x);
  float crossProduct1 = prevent_fp64_optimization(a_fp64.x * b_fp64.y);
  float crossProduct2 = prevent_fp64_optimization(a_fp64.y * b_fp64.x);
  float lowProduct = prevent_fp64_optimization(a_fp64.y * b_fp64.y);
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  float err1 = (highProduct - prod) * fp64.ONE;
  float err2 = crossProduct1 * fp64.ONE * fp64.ONE;
  float err3 = crossProduct2 * fp64.ONE * fp64.ONE * fp64.ONE;
  float err4 = lowProduct * fp64.ONE * fp64.ONE * fp64.ONE * fp64.ONE;
#else
  float err1 = highProduct - prod;
  float err2 = crossProduct1;
  float err3 = crossProduct2;
  float err4 = lowProduct;
#endif
  float err = ((err1 + err2) + err3) + err4;
  return vec2(prod, err);
}

vec2 sum_fp64(vec2 a, vec2 b) {
  vec2 s, t;
  s = twoSum(a.x, b.x);
  t = twoSum(a.y, b.y);
  s.y += t.x;
  s = quickTwoSum(s.x, s.y);
  s.y += t.y;
  s = quickTwoSum(s.x, s.y);
  return s;
}

vec2 sub_fp64(vec2 a, vec2 b) {
  vec2 s, t;
  s = twoSub(a.x, b.x);
  t = twoSub(a.y, b.y);
  s.y += t.x;
  s = quickTwoSum(s.x, s.y);
  s.y += t.y;
  s = quickTwoSum(s.x, s.y);
  return s;
}

vec2 mul_fp64(vec2 a, vec2 b) {
  vec2 prod = twoProd(a.x, b.x);
  // y component is for the error
  prod.y += a.x * b.y;
#if defined(LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND)
  prod = split2(prod);
#endif
  prod = quickTwoSum(prod.x, prod.y);
  prod.y += a.y * b.x;
#if defined(LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND)
  prod = split2(prod);
#endif
  prod = quickTwoSum(prod.x, prod.y);
  return prod;
}

vec2 div_fp64(vec2 a, vec2 b) {
  float xn = 1.0 / b.x;
#if defined(LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND)
  vec2 yn = mul_fp64(a, vec2(xn, 0));
#else
  vec2 yn = a * xn;
#endif
  float diff = (sub_fp64(a, mul_fp64(b, yn))).x;
  vec2 prod = twoProd(xn, diff);
  return sum_fp64(yn, prod);
}

vec2 sqrt_fp64(vec2 a) {
  if (a.x == 0.0 && a.y == 0.0) return vec2(0.0, 0.0);
  if (a.x < 0.0) return vec2(0.0 / 0.0, 0.0 / 0.0);

  float x = 1.0 / sqrt(a.x);
  float yn = a.x * x;
#if defined(LUMA_FP64_CODE_ELIMINATION_WORKAROUND)
  vec2 yn_sqr = twoSqr(yn) * fp64.ONE;
#else
  vec2 yn_sqr = twoSqr(yn);
#endif
  float diff = sub_fp64(a, yn_sqr).x;
  vec2 prod = twoProd(x * 0.5, diff);
#if defined(LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND)
  return sum_fp64(split(yn), prod);
#else
  return sum_fp64(vec2(yn, 0.0), prod);
#endif
}
`,Bo=`struct Fp64ArithmeticUniforms {
  ONE: f32,
  SPLIT: f32,
};

@group(0) @binding(auto) var<uniform> fp64arithmetic : Fp64ArithmeticUniforms;

fn fp64_nan(seed: f32) -> f32 {
  let nanBits = 0x7fc00000u | select(0u, 1u, seed < 0.0);
  return bitcast<f32>(nanBits);
}

fn fp64_runtime_zero() -> f32 {
  return fp64arithmetic.ONE * 0.0;
}

fn prevent_fp64_optimization(value: f32) -> f32 {
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  return value + fp64_runtime_zero();
#else
  return value;
#endif
}

fn split(a: f32) -> vec2f {
  let splitValue = prevent_fp64_optimization(fp64arithmetic.SPLIT + fp64_runtime_zero());
  let t = prevent_fp64_optimization(a * splitValue);
  let temp = prevent_fp64_optimization(t - a);
  let aHi = prevent_fp64_optimization(t - temp);
  let aLo = prevent_fp64_optimization(a - aHi);
  return vec2f(aHi, aLo);
}

fn split2(a: vec2f) -> vec2f {
  var b = split(a.x);
  b.y = b.y + a.y;
  return b;
}

fn quickTwoSum(a: f32, b: f32) -> vec2f {
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  let sum = prevent_fp64_optimization((a + b) * fp64arithmetic.ONE);
  let err = prevent_fp64_optimization(b - (sum - a) * fp64arithmetic.ONE);
#else
  let sum = prevent_fp64_optimization(a + b);
  let err = prevent_fp64_optimization(b - (sum - a));
#endif
  return vec2f(sum, err);
}

fn twoSum(a: f32, b: f32) -> vec2f {
  let s = prevent_fp64_optimization(a + b);
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  let v = prevent_fp64_optimization((s * fp64arithmetic.ONE - a) * fp64arithmetic.ONE);
  let err =
    prevent_fp64_optimization((a - (s - v) * fp64arithmetic.ONE) *
      fp64arithmetic.ONE *
      fp64arithmetic.ONE *
      fp64arithmetic.ONE) +
    prevent_fp64_optimization(b - v);
#else
  let v = prevent_fp64_optimization(s - a);
  let err = prevent_fp64_optimization(a - (s - v)) + prevent_fp64_optimization(b - v);
#endif
  return vec2f(s, err);
}

fn twoSub(a: f32, b: f32) -> vec2f {
  let s = prevent_fp64_optimization(a - b);
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  let v = prevent_fp64_optimization((s * fp64arithmetic.ONE - a) * fp64arithmetic.ONE);
  let err =
    prevent_fp64_optimization((a - (s - v) * fp64arithmetic.ONE) *
      fp64arithmetic.ONE *
      fp64arithmetic.ONE *
      fp64arithmetic.ONE) -
    prevent_fp64_optimization(b + v);
#else
  let v = prevent_fp64_optimization(s - a);
  let err = prevent_fp64_optimization(a - (s - v)) - prevent_fp64_optimization(b + v);
#endif
  return vec2f(s, err);
}

fn twoSqr(a: f32) -> vec2f {
  let prod = prevent_fp64_optimization(a * a);
  let aFp64 = split(a);
  let highProduct = prevent_fp64_optimization(aFp64.x * aFp64.x);
  let crossProduct = prevent_fp64_optimization(2.0 * aFp64.x * aFp64.y);
  let lowProduct = prevent_fp64_optimization(aFp64.y * aFp64.y);
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  let err =
    (prevent_fp64_optimization(highProduct - prod) * fp64arithmetic.ONE +
      crossProduct * fp64arithmetic.ONE * fp64arithmetic.ONE) +
    lowProduct * fp64arithmetic.ONE * fp64arithmetic.ONE * fp64arithmetic.ONE;
#else
  let err = ((prevent_fp64_optimization(highProduct - prod) + crossProduct) + lowProduct);
#endif
  return vec2f(prod, err);
}

fn twoProd(a: f32, b: f32) -> vec2f {
  let prod = prevent_fp64_optimization(a * b);
  let aFp64 = split(a);
  let bFp64 = split(b);
  let highProduct = prevent_fp64_optimization(aFp64.x * bFp64.x);
  let crossProduct1 = prevent_fp64_optimization(aFp64.x * bFp64.y);
  let crossProduct2 = prevent_fp64_optimization(aFp64.y * bFp64.x);
  let lowProduct = prevent_fp64_optimization(aFp64.y * bFp64.y);
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  let err1 = (highProduct - prod) * fp64arithmetic.ONE;
  let err2 = crossProduct1 * fp64arithmetic.ONE * fp64arithmetic.ONE;
  let err3 = crossProduct2 * fp64arithmetic.ONE * fp64arithmetic.ONE * fp64arithmetic.ONE;
  let err4 =
    lowProduct *
    fp64arithmetic.ONE *
    fp64arithmetic.ONE *
    fp64arithmetic.ONE *
    fp64arithmetic.ONE;
#else
  let err1 = highProduct - prod;
  let err2 = crossProduct1;
  let err3 = crossProduct2;
  let err4 = lowProduct;
#endif
  let err12InputA = prevent_fp64_optimization(err1);
  let err12InputB = prevent_fp64_optimization(err2);
  let err12 = prevent_fp64_optimization(err12InputA + err12InputB);
  let err123InputA = prevent_fp64_optimization(err12);
  let err123InputB = prevent_fp64_optimization(err3);
  let err123 = prevent_fp64_optimization(err123InputA + err123InputB);
  let err1234InputA = prevent_fp64_optimization(err123);
  let err1234InputB = prevent_fp64_optimization(err4);
  let err = prevent_fp64_optimization(err1234InputA + err1234InputB);
  return vec2f(prod, err);
}

fn sum_fp64(a: vec2f, b: vec2f) -> vec2f {
  var s = twoSum(a.x, b.x);
  let t = twoSum(a.y, b.y);
  s.y = prevent_fp64_optimization(s.y + t.x);
  s = quickTwoSum(s.x, s.y);
  s.y = prevent_fp64_optimization(s.y + t.y);
  s = quickTwoSum(s.x, s.y);
  return s;
}

fn sub_fp64(a: vec2f, b: vec2f) -> vec2f {
  var s = twoSub(a.x, b.x);
  let t = twoSub(a.y, b.y);
  s.y = prevent_fp64_optimization(s.y + t.x);
  s = quickTwoSum(s.x, s.y);
  s.y = prevent_fp64_optimization(s.y + t.y);
  s = quickTwoSum(s.x, s.y);
  return s;
}

fn mul_fp64(a: vec2f, b: vec2f) -> vec2f {
  var prod = twoProd(a.x, b.x);
  let crossProduct1 = prevent_fp64_optimization(a.x * b.y);
  prod.y = prevent_fp64_optimization(prod.y + crossProduct1);
#ifdef LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND
  prod = split2(prod);
#endif
  prod = quickTwoSum(prod.x, prod.y);
  let crossProduct2 = prevent_fp64_optimization(a.y * b.x);
  prod.y = prevent_fp64_optimization(prod.y + crossProduct2);
#ifdef LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND
  prod = split2(prod);
#endif
  prod = quickTwoSum(prod.x, prod.y);
  return prod;
}

fn div_fp64(a: vec2f, b: vec2f) -> vec2f {
  let xn = prevent_fp64_optimization(1.0 / b.x);
  let yn = mul_fp64(a, vec2f(xn, fp64_runtime_zero()));
  let diff = prevent_fp64_optimization(sub_fp64(a, mul_fp64(b, yn)).x);
  let prod = twoProd(xn, diff);
  return sum_fp64(yn, prod);
}

fn sqrt_fp64(a: vec2f) -> vec2f {
  if (a.x == 0.0 && a.y == 0.0) {
    return vec2f(0.0, 0.0);
  }
  if (a.x < 0.0) {
    let nanValue = fp64_nan(a.x);
    return vec2f(nanValue, nanValue);
  }

  let x = prevent_fp64_optimization(1.0 / sqrt(a.x));
  let yn = prevent_fp64_optimization(a.x * x);
#ifdef LUMA_FP64_CODE_ELIMINATION_WORKAROUND
  let ynSqr = twoSqr(yn) * fp64arithmetic.ONE;
#else
  let ynSqr = twoSqr(yn);
#endif
  let diff = prevent_fp64_optimization(sub_fp64(a, ynSqr).x);
  let prod = twoProd(prevent_fp64_optimization(x * 0.5), diff);
#ifdef LUMA_FP64_HIGH_BITS_OVERFLOW_WORKAROUND
  return sum_fp64(split(yn), prod);
#else
  return sum_fp64(vec2f(yn, 0.0), prod);
#endif
}
`,wo=`const vec2 E_FP64 = vec2(2.7182817459106445e+00, 8.254840366817007e-08);
const vec2 LOG2_FP64 = vec2(0.6931471824645996e+00, -1.9046542121259336e-09);
const vec2 PI_FP64 = vec2(3.1415927410125732, -8.742278012618954e-8);
const vec2 TWO_PI_FP64 = vec2(6.2831854820251465, -1.7484556025237907e-7);
const vec2 PI_2_FP64 = vec2(1.5707963705062866, -4.371139006309477e-8);
const vec2 PI_4_FP64 = vec2(0.7853981852531433, -2.1855695031547384e-8);
const vec2 PI_16_FP64 = vec2(0.19634954631328583, -5.463923757886846e-9);
const vec2 PI_16_2_FP64 = vec2(0.39269909262657166, -1.0927847515773692e-8);
const vec2 PI_16_3_FP64 = vec2(0.5890486240386963, -1.4906100798128818e-9);
const vec2 PI_180_FP64 = vec2(0.01745329238474369, 1.3519960498364902e-10);

const vec2 SIN_TABLE_0_FP64 = vec2(0.19509032368659973, -1.6704714833615242e-9);
const vec2 SIN_TABLE_1_FP64 = vec2(0.3826834261417389, 6.22335089017767e-9);
const vec2 SIN_TABLE_2_FP64 = vec2(0.5555702447891235, -1.1769521357507529e-8);
const vec2 SIN_TABLE_3_FP64 = vec2(0.7071067690849304, 1.2101617041793133e-8);

const vec2 COS_TABLE_0_FP64 = vec2(0.9807852506637573, 2.9739473106360492e-8);
const vec2 COS_TABLE_1_FP64 = vec2(0.9238795042037964, 2.8307490351764386e-8);
const vec2 COS_TABLE_2_FP64 = vec2(0.8314695954322815, 1.6870263741530778e-8);
const vec2 COS_TABLE_3_FP64 = vec2(0.7071067690849304, 1.2101617152815436e-8);

const vec2 INVERSE_FACTORIAL_3_FP64 = vec2(1.666666716337204e-01, -4.967053879312289e-09); // 1/3!
const vec2 INVERSE_FACTORIAL_4_FP64 = vec2(4.16666679084301e-02, -1.2417634698280722e-09); // 1/4!
const vec2 INVERSE_FACTORIAL_5_FP64 = vec2(8.333333767950535e-03, -4.34617203337595e-10); // 1/5!
const vec2 INVERSE_FACTORIAL_6_FP64 = vec2(1.3888889225199819e-03, -3.3631094437103215e-11); // 1/6!
const vec2 INVERSE_FACTORIAL_7_FP64 = vec2(1.9841270113829523e-04,  -2.725596874933456e-12); // 1/7!
const vec2 INVERSE_FACTORIAL_8_FP64 = vec2(2.4801587642286904e-05, -3.406996025904184e-13); // 1/8!
const vec2 INVERSE_FACTORIAL_9_FP64 = vec2(2.75573188446287533e-06, 3.7935713937038186e-14); // 1/9!
const vec2 INVERSE_FACTORIAL_10_FP64 = vec2(2.755731998149713e-07, -7.575112367869873e-15); // 1/10!

float nint(float d) {
    if (d == floor(d)) return d;
    return floor(d + 0.5);
}

vec2 nint_fp64(vec2 a) {
    float hi = nint(a.x);
    float lo;
    vec2 tmp;
    if (hi == a.x) {
        lo = nint(a.y);
        tmp = quickTwoSum(hi, lo);
    } else {
        lo = 0.0;
        if (abs(hi - a.x) == 0.5 && a.y < 0.0) {
            hi -= 1.0;
        }
        tmp = vec2(hi, lo);
    }
    return tmp;
}

/* k_power controls how much range reduction we would like to have
Range reduction uses the following method:
assume a = k_power * r + m * log(2), k and m being integers.
Set k_power = 4 (we can choose other k to trade accuracy with performance.
we only need to calculate exp(r) and using exp(a) = 2^m * exp(r)^k_power;
*/

vec2 exp_fp64(vec2 a) {
  // We need to make sure these two numbers match
  // as bit-wise shift is not available in GLSL 1.0
  const int k_power = 4;
  const float k = 16.0;

  const float inv_k = 1.0 / k;

  if (a.x <= -88.0) return vec2(0.0, 0.0);
  if (a.x >= 88.0) return vec2(1.0 / 0.0, 1.0 / 0.0);
  if (a.x == 0.0 && a.y == 0.0) return vec2(1.0, 0.0);
  if (a.x == 1.0 && a.y == 0.0) return E_FP64;

  float m = floor(a.x / LOG2_FP64.x + 0.5);
  vec2 r = sub_fp64(a, mul_fp64(LOG2_FP64, vec2(m, 0.0))) * inv_k;
  vec2 s, t, p;

  p = mul_fp64(r, r);
  s = sum_fp64(r, p * 0.5);
  p = mul_fp64(p, r);
  t = mul_fp64(p, INVERSE_FACTORIAL_3_FP64);

  s = sum_fp64(s, t);
  p = mul_fp64(p, r);
  t = mul_fp64(p, INVERSE_FACTORIAL_4_FP64);

  s = sum_fp64(s, t);
  p = mul_fp64(p, r);
  t = mul_fp64(p, INVERSE_FACTORIAL_5_FP64);

  // s = sum_fp64(s, t);
  // p = mul_fp64(p, r);
  // t = mul_fp64(p, INVERSE_FACTORIAL_6_FP64);

  // s = sum_fp64(s, t);
  // p = mul_fp64(p, r);
  // t = mul_fp64(p, INVERSE_FACTORIAL_7_FP64);

  s = sum_fp64(s, t);


  // At this point, s = exp(r) - 1; but after following 4 recursions, we will get exp(r) ^ 512 - 1.
  for (int i = 0; i < k_power; i++) {
    s = sum_fp64(s * 2.0, mul_fp64(s, s));
  }

#if defined(NVIDIA_FP64_WORKAROUND) || defined(INTEL_FP64_WORKAROUND)
  s = sum_fp64(s, vec2(fp64.ONE, 0.0));
#else
  s = sum_fp64(s, vec2(1.0, 0.0));
#endif

  return s * pow(2.0, m);
//   return r;
}

vec2 log_fp64(vec2 a)
{
  if (a.x == 1.0 && a.y == 0.0) return vec2(0.0, 0.0);
  if (a.x <= 0.0) return vec2(0.0 / 0.0, 0.0 / 0.0);
  vec2 x = vec2(log(a.x), 0.0);
  vec2 s;
#if defined(NVIDIA_FP64_WORKAROUND) || defined(INTEL_FP64_WORKAROUND)
  s = vec2(fp64.ONE, 0.0);
#else
  s = vec2(1.0, 0.0);
#endif

  x = sub_fp64(sum_fp64(x, mul_fp64(a, exp_fp64(-x))), s);
  return x;
}

vec2 sin_taylor_fp64(vec2 a) {
  vec2 r, s, t, x;

  if (a.x == 0.0 && a.y == 0.0) {
    return vec2(0.0, 0.0);
  }

  x = -mul_fp64(a, a);
  s = a;
  r = a;

  r = mul_fp64(r, x);
  t = mul_fp64(r, INVERSE_FACTORIAL_3_FP64);
  s = sum_fp64(s, t);

  r = mul_fp64(r, x);
  t = mul_fp64(r, INVERSE_FACTORIAL_5_FP64);
  s = sum_fp64(s, t);

  /* keep the following commented code in case we need them
  for extra accuracy from the Taylor expansion*/

  // r = mul_fp64(r, x);
  // t = mul_fp64(r, INVERSE_FACTORIAL_7_FP64);
  // s = sum_fp64(s, t);

  // r = mul_fp64(r, x);
  // t = mul_fp64(r, INVERSE_FACTORIAL_9_FP64);
  // s = sum_fp64(s, t);

  return s;
}

vec2 cos_taylor_fp64(vec2 a) {
  vec2 r, s, t, x;

  if (a.x == 0.0 && a.y == 0.0) {
    return vec2(1.0, 0.0);
  }

  x = -mul_fp64(a, a);
  r = x;
  s = sum_fp64(vec2(1.0, 0.0), r * 0.5);

  r = mul_fp64(r, x);
  t = mul_fp64(r, INVERSE_FACTORIAL_4_FP64);
  s = sum_fp64(s, t);

  r = mul_fp64(r, x);
  t = mul_fp64(r, INVERSE_FACTORIAL_6_FP64);
  s = sum_fp64(s, t);

  /* keep the following commented code in case we need them
  for extra accuracy from the Taylor expansion*/

  // r = mul_fp64(r, x);
  // t = mul_fp64(r, INVERSE_FACTORIAL_8_FP64);
  // s = sum_fp64(s, t);

  // r = mul_fp64(r, x);
  // t = mul_fp64(r, INVERSE_FACTORIAL_10_FP64);
  // s = sum_fp64(s, t);

  return s;
}

void sincos_taylor_fp64(vec2 a, out vec2 sin_t, out vec2 cos_t) {
  if (a.x == 0.0 && a.y == 0.0) {
    sin_t = vec2(0.0, 0.0);
    cos_t = vec2(1.0, 0.0);
  }

  sin_t = sin_taylor_fp64(a);
  cos_t = sqrt_fp64(sub_fp64(vec2(1.0, 0.0), mul_fp64(sin_t, sin_t)));
}

vec2 sin_fp64(vec2 a) {
    if (a.x == 0.0 && a.y == 0.0) {
        return vec2(0.0, 0.0);
    }

    // 2pi range reduction
    vec2 z = nint_fp64(div_fp64(a, TWO_PI_FP64));
    vec2 r = sub_fp64(a, mul_fp64(TWO_PI_FP64, z));

    vec2 t;
    float q = floor(r.x / PI_2_FP64.x + 0.5);
    int j = int(q);

    if (j < -2 || j > 2) {
        return vec2(0.0 / 0.0, 0.0 / 0.0);
    }

    t = sub_fp64(r, mul_fp64(PI_2_FP64, vec2(q, 0.0)));

    q = floor(t.x / PI_16_FP64.x + 0.5);
    int k = int(q);

    if (k == 0) {
        if (j == 0) {
            return sin_taylor_fp64(t);
        } else if (j == 1) {
            return cos_taylor_fp64(t);
        } else if (j == -1) {
            return -cos_taylor_fp64(t);
        } else {
            return -sin_taylor_fp64(t);
        }
    }

    int abs_k = int(abs(float(k)));

    if (abs_k > 4) {
        return vec2(0.0 / 0.0, 0.0 / 0.0);
    } else {
        t = sub_fp64(t, mul_fp64(PI_16_FP64, vec2(q, 0.0)));
    }

    vec2 u = vec2(0.0, 0.0);
    vec2 v = vec2(0.0, 0.0);

#if defined(NVIDIA_FP64_WORKAROUND) || defined(INTEL_FP64_WORKAROUND)
    if (abs(float(abs_k) - 1.0) < 0.5) {
        u = COS_TABLE_0_FP64;
        v = SIN_TABLE_0_FP64;
    } else if (abs(float(abs_k) - 2.0) < 0.5) {
        u = COS_TABLE_1_FP64;
        v = SIN_TABLE_1_FP64;
    } else if (abs(float(abs_k) - 3.0) < 0.5) {
        u = COS_TABLE_2_FP64;
        v = SIN_TABLE_2_FP64;
    } else if (abs(float(abs_k) - 4.0) < 0.5) {
        u = COS_TABLE_3_FP64;
        v = SIN_TABLE_3_FP64;
    }
#else
    if (abs_k == 1) {
        u = COS_TABLE_0_FP64;
        v = SIN_TABLE_0_FP64;
    } else if (abs_k == 2) {
        u = COS_TABLE_1_FP64;
        v = SIN_TABLE_1_FP64;
    } else if (abs_k == 3) {
        u = COS_TABLE_2_FP64;
        v = SIN_TABLE_2_FP64;
    } else if (abs_k == 4) {
        u = COS_TABLE_3_FP64;
        v = SIN_TABLE_3_FP64;
    }
#endif

    vec2 sin_t, cos_t;
    sincos_taylor_fp64(t, sin_t, cos_t);



    vec2 result = vec2(0.0, 0.0);
    if (j == 0) {
        if (k > 0) {
            result = sum_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
        } else {
            result = sub_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
        }
    } else if (j == 1) {
        if (k > 0) {
            result = sub_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        } else {
            result = sum_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        }
    } else if (j == -1) {
        if (k > 0) {
            result = sub_fp64(mul_fp64(v, sin_t), mul_fp64(u, cos_t));
        } else {
            result = -sum_fp64(mul_fp64(v, sin_t), mul_fp64(u, cos_t));
        }
    } else {
        if (k > 0) {
            result = -sum_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
        } else {
            result = sub_fp64(mul_fp64(v, cos_t), mul_fp64(u, sin_t));
        }
    }

    return result;
}

vec2 cos_fp64(vec2 a) {
    if (a.x == 0.0 && a.y == 0.0) {
        return vec2(1.0, 0.0);
    }

    // 2pi range reduction
    vec2 z = nint_fp64(div_fp64(a, TWO_PI_FP64));
    vec2 r = sub_fp64(a, mul_fp64(TWO_PI_FP64, z));

    vec2 t;
    float q = floor(r.x / PI_2_FP64.x + 0.5);
    int j = int(q);

    if (j < -2 || j > 2) {
        return vec2(0.0 / 0.0, 0.0 / 0.0);
    }

    t = sub_fp64(r, mul_fp64(PI_2_FP64, vec2(q, 0.0)));

    q = floor(t.x / PI_16_FP64.x + 0.5);
    int k = int(q);

    if (k == 0) {
        if (j == 0) {
            return cos_taylor_fp64(t);
        } else if (j == 1) {
            return -sin_taylor_fp64(t);
        } else if (j == -1) {
            return sin_taylor_fp64(t);
        } else {
            return -cos_taylor_fp64(t);
        }
    }

    int abs_k = int(abs(float(k)));

    if (abs_k > 4) {
        return vec2(0.0 / 0.0, 0.0 / 0.0);
    } else {
        t = sub_fp64(t, mul_fp64(PI_16_FP64, vec2(q, 0.0)));
    }

    vec2 u = vec2(0.0, 0.0);
    vec2 v = vec2(0.0, 0.0);

#if defined(NVIDIA_FP64_WORKAROUND) || defined(INTEL_FP64_WORKAROUND)
    if (abs(float(abs_k) - 1.0) < 0.5) {
        u = COS_TABLE_0_FP64;
        v = SIN_TABLE_0_FP64;
    } else if (abs(float(abs_k) - 2.0) < 0.5) {
        u = COS_TABLE_1_FP64;
        v = SIN_TABLE_1_FP64;
    } else if (abs(float(abs_k) - 3.0) < 0.5) {
        u = COS_TABLE_2_FP64;
        v = SIN_TABLE_2_FP64;
    } else if (abs(float(abs_k) - 4.0) < 0.5) {
        u = COS_TABLE_3_FP64;
        v = SIN_TABLE_3_FP64;
    }
#else
    if (abs_k == 1) {
        u = COS_TABLE_0_FP64;
        v = SIN_TABLE_0_FP64;
    } else if (abs_k == 2) {
        u = COS_TABLE_1_FP64;
        v = SIN_TABLE_1_FP64;
    } else if (abs_k == 3) {
        u = COS_TABLE_2_FP64;
        v = SIN_TABLE_2_FP64;
    } else if (abs_k == 4) {
        u = COS_TABLE_3_FP64;
        v = SIN_TABLE_3_FP64;
    }
#endif

    vec2 sin_t, cos_t;
    sincos_taylor_fp64(t, sin_t, cos_t);

    vec2 result = vec2(0.0, 0.0);
    if (j == 0) {
        if (k > 0) {
            result = sub_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        } else {
            result = sum_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        }
    } else if (j == 1) {
        if (k > 0) {
            result = -sum_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
        } else {
            result = sub_fp64(mul_fp64(v, cos_t), mul_fp64(u, sin_t));
        }
    } else if (j == -1) {
        if (k > 0) {
            result = sum_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
        } else {
            result = sub_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
        }
    } else {
        if (k > 0) {
            result = sub_fp64(mul_fp64(v, sin_t), mul_fp64(u, cos_t));
        } else {
            result = -sum_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        }
    }

    return result;
}

vec2 tan_fp64(vec2 a) {
    vec2 sin_a;
    vec2 cos_a;

    if (a.x == 0.0 && a.y == 0.0) {
        return vec2(0.0, 0.0);
    }

    // 2pi range reduction
    vec2 z = nint_fp64(div_fp64(a, TWO_PI_FP64));
    vec2 r = sub_fp64(a, mul_fp64(TWO_PI_FP64, z));

    vec2 t;
    float q = floor(r.x / PI_2_FP64.x + 0.5);
    int j = int(q);


    if (j < -2 || j > 2) {
        return vec2(0.0 / 0.0, 0.0 / 0.0);
    }

    t = sub_fp64(r, mul_fp64(PI_2_FP64, vec2(q, 0.0)));

    q = floor(t.x / PI_16_FP64.x + 0.5);
    int k = int(q);
    int abs_k = int(abs(float(k)));

    // We just can't get PI/16 * 3.0 very accurately.
    // so let's just store it
    if (abs_k > 4) {
        return vec2(0.0 / 0.0, 0.0 / 0.0);
    } else {
        t = sub_fp64(t, mul_fp64(PI_16_FP64, vec2(q, 0.0)));
    }


    vec2 u = vec2(0.0, 0.0);
    vec2 v = vec2(0.0, 0.0);

    vec2 sin_t, cos_t;
    vec2 s, c;
    sincos_taylor_fp64(t, sin_t, cos_t);

    if (k == 0) {
        s = sin_t;
        c = cos_t;
    } else {
#if defined(NVIDIA_FP64_WORKAROUND) || defined(INTEL_FP64_WORKAROUND)
        if (abs(float(abs_k) - 1.0) < 0.5) {
            u = COS_TABLE_0_FP64;
            v = SIN_TABLE_0_FP64;
        } else if (abs(float(abs_k) - 2.0) < 0.5) {
            u = COS_TABLE_1_FP64;
            v = SIN_TABLE_1_FP64;
        } else if (abs(float(abs_k) - 3.0) < 0.5) {
            u = COS_TABLE_2_FP64;
            v = SIN_TABLE_2_FP64;
        } else if (abs(float(abs_k) - 4.0) < 0.5) {
            u = COS_TABLE_3_FP64;
            v = SIN_TABLE_3_FP64;
        }
#else
        if (abs_k == 1) {
            u = COS_TABLE_0_FP64;
            v = SIN_TABLE_0_FP64;
        } else if (abs_k == 2) {
            u = COS_TABLE_1_FP64;
            v = SIN_TABLE_1_FP64;
        } else if (abs_k == 3) {
            u = COS_TABLE_2_FP64;
            v = SIN_TABLE_2_FP64;
        } else if (abs_k == 4) {
            u = COS_TABLE_3_FP64;
            v = SIN_TABLE_3_FP64;
        }
#endif
        if (k > 0) {
            s = sum_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
            c = sub_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        } else {
            s = sub_fp64(mul_fp64(u, sin_t), mul_fp64(v, cos_t));
            c = sum_fp64(mul_fp64(u, cos_t), mul_fp64(v, sin_t));
        }
    }

    if (j == 0) {
        sin_a = s;
        cos_a = c;
    } else if (j == 1) {
        sin_a = c;
        cos_a = -s;
    } else if (j == -1) {
        sin_a = -c;
        cos_a = s;
    } else {
        sin_a = -s;
        cos_a = -c;
    }
    return div_fp64(sin_a, cos_a);
}

vec2 radians_fp64(vec2 degree) {
  return mul_fp64(degree, PI_180_FP64);
}

vec2 mix_fp64(vec2 a, vec2 b, float x) {
  vec2 range = sub_fp64(b, a);
  return sum_fp64(a, mul_fp64(range, vec2(x, 0.0)));
}

// Vector functions
// vec2 functions
void vec2_sum_fp64(vec2 a[2], vec2 b[2], out vec2 out_val[2]) {
    out_val[0] = sum_fp64(a[0], b[0]);
    out_val[1] = sum_fp64(a[1], b[1]);
}

void vec2_sub_fp64(vec2 a[2], vec2 b[2], out vec2 out_val[2]) {
    out_val[0] = sub_fp64(a[0], b[0]);
    out_val[1] = sub_fp64(a[1], b[1]);
}

void vec2_mul_fp64(vec2 a[2], vec2 b[2], out vec2 out_val[2]) {
    out_val[0] = mul_fp64(a[0], b[0]);
    out_val[1] = mul_fp64(a[1], b[1]);
}

void vec2_div_fp64(vec2 a[2], vec2 b[2], out vec2 out_val[2]) {
    out_val[0] = div_fp64(a[0], b[0]);
    out_val[1] = div_fp64(a[1], b[1]);
}

void vec2_mix_fp64(vec2 x[2], vec2 y[2], float a, out vec2 out_val[2]) {
  vec2 range[2];
  vec2_sub_fp64(y, x, range);
  vec2 portion[2];
  portion[0] = range[0] * a;
  portion[1] = range[1] * a;
  vec2_sum_fp64(x, portion, out_val);
}

vec2 vec2_length_fp64(vec2 x[2]) {
  return sqrt_fp64(sum_fp64(mul_fp64(x[0], x[0]), mul_fp64(x[1], x[1])));
}

void vec2_normalize_fp64(vec2 x[2], out vec2 out_val[2]) {
  vec2 length = vec2_length_fp64(x);
  vec2 length_vec2[2];
  length_vec2[0] = length;
  length_vec2[1] = length;

  vec2_div_fp64(x, length_vec2, out_val);
}

vec2 vec2_distance_fp64(vec2 x[2], vec2 y[2]) {
  vec2 diff[2];
  vec2_sub_fp64(x, y, diff);
  return vec2_length_fp64(diff);
}

vec2 vec2_dot_fp64(vec2 a[2], vec2 b[2]) {
  vec2 v[2];

  v[0] = mul_fp64(a[0], b[0]);
  v[1] = mul_fp64(a[1], b[1]);

  return sum_fp64(v[0], v[1]);
}

// vec3 functions
void vec3_sub_fp64(vec2 a[3], vec2 b[3], out vec2 out_val[3]) {
  for (int i = 0; i < 3; i++) {
    out_val[i] = sum_fp64(a[i], b[i]);
  }
}

void vec3_sum_fp64(vec2 a[3], vec2 b[3], out vec2 out_val[3]) {
  for (int i = 0; i < 3; i++) {
    out_val[i] = sum_fp64(a[i], b[i]);
  }
}

vec2 vec3_length_fp64(vec2 x[3]) {
  return sqrt_fp64(sum_fp64(sum_fp64(mul_fp64(x[0], x[0]), mul_fp64(x[1], x[1])),
    mul_fp64(x[2], x[2])));
}

vec2 vec3_distance_fp64(vec2 x[3], vec2 y[3]) {
  vec2 diff[3];
  vec3_sub_fp64(x, y, diff);
  return vec3_length_fp64(diff);
}

// vec4 functions
void vec4_fp64(vec4 a, out vec2 out_val[4]) {
  out_val[0].x = a[0];
  out_val[0].y = 0.0;

  out_val[1].x = a[1];
  out_val[1].y = 0.0;

  out_val[2].x = a[2];
  out_val[2].y = 0.0;

  out_val[3].x = a[3];
  out_val[3].y = 0.0;
}

void vec4_scalar_mul_fp64(vec2 a[4], vec2 b, out vec2 out_val[4]) {
  out_val[0] = mul_fp64(a[0], b);
  out_val[1] = mul_fp64(a[1], b);
  out_val[2] = mul_fp64(a[2], b);
  out_val[3] = mul_fp64(a[3], b);
}

void vec4_sum_fp64(vec2 a[4], vec2 b[4], out vec2 out_val[4]) {
  for (int i = 0; i < 4; i++) {
    out_val[i] = sum_fp64(a[i], b[i]);
  }
}

void vec4_dot_fp64(vec2 a[4], vec2 b[4], out vec2 out_val) {
  vec2 v[4];

  v[0] = mul_fp64(a[0], b[0]);
  v[1] = mul_fp64(a[1], b[1]);
  v[2] = mul_fp64(a[2], b[2]);
  v[3] = mul_fp64(a[3], b[3]);

  out_val = sum_fp64(sum_fp64(v[0], v[1]), sum_fp64(v[2], v[3]));
}

void mat4_vec4_mul_fp64(vec2 b[16], vec2 a[4], out vec2 out_val[4]) {
  vec2 tmp[4];

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      tmp[j] = b[j + i * 4];
    }
    vec4_dot_fp64(a, tmp, out_val[i]);
  }
}
`,ko={ONE:1,SPLIT:4097},qe={name:"fp64arithmetic",source:Bo,fs:We,vs:We,defaultUniforms:ko,uniformTypes:{ONE:"f32",SPLIT:"f32"},fp64ify:$,fp64LowPart:se,fp64ifyMatrix4:ce},Do={name:"fp64",vs:wo,dependencies:[qe],fp64ify:$,fp64LowPart:se,fp64ifyMatrix4:ce},Ke=`layout(std140) uniform floatColorsUniforms {
  float useByteColors;
} floatColors;

vec3 floatColors_normalize(vec3 inputColor) {
  return floatColors.useByteColors > 0.5 ? inputColor / 255.0 : inputColor;
}

vec4 floatColors_normalize(vec4 inputColor) {
  return floatColors.useByteColors > 0.5 ? inputColor / 255.0 : inputColor;
}

vec4 floatColors_premultiplyAlpha(vec4 inputColor) {
  return vec4(inputColor.rgb * inputColor.a, inputColor.a);
}

vec4 floatColors_unpremultiplyAlpha(vec4 inputColor) {
  return inputColor.a > 0.0 ? vec4(inputColor.rgb / inputColor.a, inputColor.a) : vec4(0.0);
}

vec4 floatColors_premultiply_alpha(vec4 inputColor) {
  return floatColors_premultiplyAlpha(inputColor);
}

vec4 floatColors_unpremultiply_alpha(vec4 inputColor) {
  return floatColors_unpremultiplyAlpha(inputColor);
}
`,Ho=`struct floatColorsUniforms {
  useByteColors: f32
};

@group(0) @binding(auto) var<uniform> floatColors : floatColorsUniforms;

fn floatColors_normalize(inputColor: vec3<f32>) -> vec3<f32> {
  return select(inputColor, inputColor / 255.0, floatColors.useByteColors > 0.5);
}

fn floatColors_normalize4(inputColor: vec4<f32>) -> vec4<f32> {
  return select(inputColor, inputColor / 255.0, floatColors.useByteColors > 0.5);
}

fn floatColors_premultiplyAlpha(inputColor: vec4<f32>) -> vec4<f32> {
  return vec4<f32>(inputColor.rgb * inputColor.a, inputColor.a);
}

fn floatColors_unpremultiplyAlpha(inputColor: vec4<f32>) -> vec4<f32> {
  return select(
    vec4<f32>(0.0),
    vec4<f32>(inputColor.rgb / inputColor.a, inputColor.a),
    inputColor.a > 0.0
  );
}

fn floatColors_premultiply_alpha(inputColor: vec4<f32>) -> vec4<f32> {
  return floatColors_premultiplyAlpha(inputColor);
}

fn floatColors_unpremultiply_alpha(inputColor: vec4<f32>) -> vec4<f32> {
  return floatColors_unpremultiplyAlpha(inputColor);
}
`,ue={name:"floatColors",props:{},uniforms:{},vs:Ke,fs:Ke,source:Ho,uniformTypes:{useByteColors:"f32"},defaultUniforms:{useByteColors:!0}},Go=[0,1,1,1],zo=`layout(std140) uniform pickingUniforms {
  float isActive;
  float isAttribute;
  float isHighlightActive;
  float useByteColors;
  vec3 highlightedObjectColor;
  vec4 highlightColor;
} picking;

out vec4 picking_vRGBcolor_Avalid;

// Normalize unsigned byte color to 0-1 range
vec3 picking_normalizeColor(vec3 color) {
  return picking.useByteColors > 0.5 ? color / 255.0 : color;
}

// Normalize unsigned byte color to 0-1 range
vec4 picking_normalizeColor(vec4 color) {
  return picking.useByteColors > 0.5 ? color / 255.0 : color;
}

bool picking_isColorZero(vec3 color) {
  return dot(color, vec3(1.0)) < 0.00001;
}

bool picking_isColorValid(vec3 color) {
  return dot(color, vec3(1.0)) > 0.00001;
}

// Check if this vertex is highlighted 
bool isVertexHighlighted(vec3 vertexColor) {
  vec3 highlightedObjectColor = picking_normalizeColor(picking.highlightedObjectColor);
  return
    bool(picking.isHighlightActive) && picking_isColorZero(abs(vertexColor - highlightedObjectColor));
}

// Set the current picking color
void picking_setPickingColor(vec3 pickingColor) {
  pickingColor = picking_normalizeColor(pickingColor);

  if (bool(picking.isActive)) {
    // Use alpha as the validity flag. If pickingColor is [0, 0, 0] fragment is non-pickable
    picking_vRGBcolor_Avalid.a = float(picking_isColorValid(pickingColor));

    if (!bool(picking.isAttribute)) {
      // Stores the picking color so that the fragment shader can render it during picking
      picking_vRGBcolor_Avalid.rgb = pickingColor;
    }
  } else {
    // Do the comparison with selected item color in vertex shader as it should mean fewer compares
    picking_vRGBcolor_Avalid.a = float(isVertexHighlighted(pickingColor));
  }
}

void picking_setPickingAttribute(float value) {
  if (bool(picking.isAttribute)) {
    picking_vRGBcolor_Avalid.r = value;
  }
}

void picking_setPickingAttribute(vec2 value) {
  if (bool(picking.isAttribute)) {
    picking_vRGBcolor_Avalid.rg = value;
  }
}

void picking_setPickingAttribute(vec3 value) {
  if (bool(picking.isAttribute)) {
    picking_vRGBcolor_Avalid.rgb = value;
  }
}
`,$o=`layout(std140) uniform pickingUniforms {
  float isActive;
  float isAttribute;
  float isHighlightActive;
  float useByteColors;
  vec3 highlightedObjectColor;
  vec4 highlightColor;
} picking;

in vec4 picking_vRGBcolor_Avalid;

/*
 * Returns highlight color if this item is selected.
 */
vec4 picking_filterHighlightColor(vec4 color) {
  // If we are still picking, we don't highlight
  if (picking.isActive > 0.5) {
    return color;
  }

  bool selected = bool(picking_vRGBcolor_Avalid.a);

  if (selected) {
    // Blend in highlight color based on its alpha value
    float highLightAlpha = picking.highlightColor.a;
    float blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);
    float highLightRatio = highLightAlpha / blendedAlpha;

    vec3 blendedRGB = mix(color.rgb, picking.highlightColor.rgb, highLightRatio);
    return vec4(blendedRGB, blendedAlpha);
  } else {
    return color;
  }
}

/*
 * Returns picking color if picking enabled else unmodified argument.
 */
vec4 picking_filterPickingColor(vec4 color) {
  if (bool(picking.isActive)) {
    if (picking_vRGBcolor_Avalid.a == 0.0) {
      discard;
    }
    return picking_vRGBcolor_Avalid;
  }
  return color;
}

/*
 * Returns picking color if picking is enabled if not
 * highlight color if this item is selected, otherwise unmodified argument.
 */
vec4 picking_filterColor(vec4 color) {
  vec4 highlightColor = picking_filterHighlightColor(color);
  return picking_filterPickingColor(highlightColor);
}
`,jo={props:{},uniforms:{},name:"picking",uniformTypes:{isActive:"f32",isAttribute:"f32",isHighlightActive:"f32",useByteColors:"f32",highlightedObjectColor:"vec3<f32>",highlightColor:"vec4<f32>"},defaultUniforms:{isActive:!1,isAttribute:!1,isHighlightActive:!1,useByteColors:!0,highlightedObjectColor:[0,0,0],highlightColor:Go},vs:zo,fs:$o,getUniforms:Wo};function Wo(e={},t){const o={},i=fe(e.useByteColors,!0);if(e.highlightedObjectColor!==void 0)if(e.highlightedObjectColor===null)o.isHighlightActive=!1;else{o.isHighlightActive=!0;const n=e.highlightedObjectColor.slice(0,3);o.highlightedObjectColor=n}return e.highlightColor&&(o.highlightColor=je(e.highlightColor,i)),e.isActive!==void 0&&(o.isActive=!!e.isActive,o.isAttribute=!!e.isAttribute),e.useByteColors!==void 0&&(o.useByteColors=!!e.useByteColors),o}const w=20,qo=`
struct skinUniforms {
  jointMatrix: array<mat4x4<f32>, ${w}>,
};

@group(0) @binding(auto) var<uniform> skin: skinUniforms;

fn getSkinMatrix(weights: vec4f, joints: vec4u) -> mat4x4<f32> {
  return (weights.x * skin.jointMatrix[joints.x])
       + (weights.y * skin.jointMatrix[joints.y])
       + (weights.z * skin.jointMatrix[joints.z])
       + (weights.w * skin.jointMatrix[joints.w]);
}
`,Ko=`
layout(std140) uniform skinUniforms {
  mat4 jointMatrix[SKIN_MAX_JOINTS];
} skin;

mat4 getSkinMatrix(vec4 weights, uvec4 joints) {
  return (weights.x * skin.jointMatrix[joints.x])
       + (weights.y * skin.jointMatrix[joints.y])
       + (weights.z * skin.jointMatrix[joints.z])
       + (weights.w * skin.jointMatrix[joints.w]);
}

`,Xo="",Zo={props:{},uniforms:{},name:"skin",bindingLayout:[{name:"skin",group:0}],dependencies:[],source:qo,vs:Ko,fs:Xo,defines:{SKIN_MAX_JOINTS:w},getUniforms:(e={},t)=>{const{scenegraphsFromGLTF:o}=e;if(!o?.gltf?.skins?.[0])return{jointMatrix:[]};const{inverseBindMatrices:i,joints:n,skeleton:r}=o.gltf.skins[0],a=[],l=i.value.length/16;for(let p=0;p<l;p++){const u=i.value.subarray(p*16,p*16+16);a.push(new ge(Array.from(u)))}const s=o.gltfNodeIndexToNodeMap.get(r),c={};s.preorderTraversal((p,{worldMatrix:u})=>{c[p.id]=u});const f=new Float32Array(w*16);for(let p=0;p<w;++p){const u=n[p];if(u===void 0)break;const m=c[o.gltfNodeIndexToNodeMap.get(u).id],_=a[p],M=new ge().copy(m).multiplyRight(_),A=p*16;for(let g=0;g<16;g++)f[A+g]=M[g]}return{jointMatrix:f}},uniformTypes:{jointMatrix:["mat4x4<f32>",w]}},Xe=`precision highp int;

// #if (defined(SHADER_TYPE_FRAGMENT) && defined(LIGHTING_FRAGMENT)) || (defined(SHADER_TYPE_VERTEX) && defined(LIGHTING_VERTEX))
struct AmbientLight {
  vec3 color;
};

struct PointLight {
  vec3 color;
  vec3 position;
  vec3 attenuation; // 2nd order x:Constant-y:Linear-z:Exponential
};

struct SpotLight {
  vec3 color;
  vec3 position;
  vec3 direction;
  vec3 attenuation;
  vec2 coneCos;
};

struct DirectionalLight {
  vec3 color;
  vec3 direction;
};

struct UniformLight {
  vec3 color;
  vec3 position;
  vec3 direction;
  vec3 attenuation;
  vec2 coneCos;
};

layout(std140) uniform lightingUniforms {
  int enabled;
  int directionalLightCount;
  int pointLightCount;
  int spotLightCount;
  vec3 ambientColor;
  UniformLight lights[5];
} lighting;

PointLight lighting_getPointLight(int index) {
  UniformLight light = lighting.lights[index];
  return PointLight(light.color, light.position, light.attenuation);
}

SpotLight lighting_getSpotLight(int index) {
  UniformLight light = lighting.lights[lighting.pointLightCount + index];
  return SpotLight(light.color, light.position, light.direction, light.attenuation, light.coneCos);
}

DirectionalLight lighting_getDirectionalLight(int index) {
  UniformLight light =
    lighting.lights[lighting.pointLightCount + lighting.spotLightCount + index];
  return DirectionalLight(light.color, light.direction);
}

float getPointLightAttenuation(PointLight pointLight, float distance) {
  return pointLight.attenuation.x
       + pointLight.attenuation.y * distance
       + pointLight.attenuation.z * distance * distance;
}

float getSpotLightAttenuation(SpotLight spotLight, vec3 positionWorldspace) {
  vec3 light_direction = normalize(positionWorldspace - spotLight.position);
  float coneFactor = smoothstep(
    spotLight.coneCos.y,
    spotLight.coneCos.x,
    dot(normalize(spotLight.direction), light_direction)
  );
  float distanceAttenuation = getPointLightAttenuation(
    PointLight(spotLight.color, spotLight.position, spotLight.attenuation),
    distance(spotLight.position, positionWorldspace)
  );
  return distanceAttenuation / max(coneFactor, 0.0001);
}

// #endif
`,Yo=`// #if (defined(SHADER_TYPE_FRAGMENT) && defined(LIGHTING_FRAGMENT)) || (defined(SHADER_TYPE_VERTEX) && defined(LIGHTING_VERTEX))
const MAX_LIGHTS: i32 = 5;

struct AmbientLight {
  color: vec3<f32>,
};

struct PointLight {
  color: vec3<f32>,
  position: vec3<f32>,
  attenuation: vec3<f32>, // 2nd order x:Constant-y:Linear-z:Exponential
};

struct SpotLight {
  color: vec3<f32>,
  position: vec3<f32>,
  direction: vec3<f32>,
  attenuation: vec3<f32>,
  coneCos: vec2<f32>,
};

struct DirectionalLight {
  color: vec3<f32>,
  direction: vec3<f32>,
};

struct UniformLight {
  color: vec3<f32>,
  position: vec3<f32>,
  direction: vec3<f32>,
  attenuation: vec3<f32>,
  coneCos: vec2<f32>,
};

struct lightingUniforms {
  enabled: i32,
  directionalLightCount: i32,
  pointLightCount: i32,
  spotLightCount: i32,
  ambientColor: vec3<f32>,
  lights: array<UniformLight, 5>,
};

@group(2) @binding(auto) var<uniform> lighting : lightingUniforms;

fn lighting_getPointLight(index: i32) -> PointLight {
  let light = lighting.lights[index];
  return PointLight(light.color, light.position, light.attenuation);
}

fn lighting_getSpotLight(index: i32) -> SpotLight {
  let light = lighting.lights[lighting.pointLightCount + index];
  return SpotLight(light.color, light.position, light.direction, light.attenuation, light.coneCos);
}

fn lighting_getDirectionalLight(index: i32) -> DirectionalLight {
  let light = lighting.lights[lighting.pointLightCount + lighting.spotLightCount + index];
  return DirectionalLight(light.color, light.direction);
}

fn getPointLightAttenuation(pointLight: PointLight, distance: f32) -> f32 {
  return pointLight.attenuation.x
       + pointLight.attenuation.y * distance
       + pointLight.attenuation.z * distance * distance;
}

fn getSpotLightAttenuation(spotLight: SpotLight, positionWorldspace: vec3<f32>) -> f32 {
  let lightDirection = normalize(positionWorldspace - spotLight.position);
  let coneFactor = smoothstep(
    spotLight.coneCos.y,
    spotLight.coneCos.x,
    dot(normalize(spotLight.direction), lightDirection)
  );
  let distanceAttenuation = getPointLightAttenuation(
    PointLight(spotLight.color, spotLight.position, spotLight.attenuation),
    distance(spotLight.position, positionWorldspace)
  );
  return distanceAttenuation / max(coneFactor, 0.0001);
}
`,P=5,Jo={color:"vec3<f32>",position:"vec3<f32>",direction:"vec3<f32>",attenuation:"vec3<f32>",coneCos:"vec2<f32>"},k={props:{},uniforms:{},name:"lighting",defines:{},uniformTypes:{enabled:"i32",directionalLightCount:"i32",pointLightCount:"i32",spotLightCount:"i32",ambientColor:"vec3<f32>",lights:[Jo,P]},defaultUniforms:W(),bindingLayout:[{name:"lighting",group:2}],firstBindingSlot:0,source:Yo,vs:Xe,fs:Xe,getUniforms:Qo};function Qo(e,t={}){if(e=e&&{...e},!e)return W();e.lights&&(e={...e,...ti(e.lights),lights:void 0});const{useByteColors:o,ambientLight:i,pointLights:n,spotLights:r,directionalLights:a}=e||{};if(!(i||n&&n.length>0||r&&r.length>0||a&&a.length>0))return{...W(),enabled:0};const s={...W(),...ei({useByteColors:o,ambientLight:i,pointLights:n,spotLights:r,directionalLights:a})};return e.enabled!==void 0&&(s.enabled=e.enabled?1:0),s}function ei({useByteColors:e,ambientLight:t,pointLights:o=[],spotLights:i=[],directionalLights:n=[]}){const r=Ze();let a=0,l=0,s=0,c=0;for(const f of o){if(a>=P)break;r[a]={...r[a],color:j(f,e),position:f.position,attenuation:f.attenuation||[1,0,0]},a++,l++}for(const f of i){if(a>=P)break;r[a]={...r[a],color:j(f,e),position:f.position,direction:f.direction,attenuation:f.attenuation||[1,0,0],coneCos:ii(f)},a++,s++}for(const f of n){if(a>=P)break;r[a]={...r[a],color:j(f,e),direction:f.direction},a++,c++}return o.length+i.length+n.length>P&&ft.warn(`MAX_LIGHTS exceeded, truncating to ${P}`)(),{ambientColor:j(t,e),directionalLightCount:c,pointLightCount:l,spotLightCount:s,lights:r}}function ti(e){const t={pointLights:[],spotLights:[],directionalLights:[]};for(const o of e||[])switch(o.type){case"ambient":t.ambientLight=o;break;case"directional":t.directionalLights?.push(o);break;case"point":t.pointLights?.push(o);break;case"spot":t.spotLights?.push(o);break}return t}function j(e={},t){const{color:o=[0,0,0],intensity:i=1}=e;return pe(o,fe(t,!0)).map(r=>r*i)}function W(){return{enabled:1,directionalLightCount:0,pointLightCount:0,spotLightCount:0,ambientColor:[.1,.1,.1],lights:Ze()}}function Ze(){return Array.from({length:P},()=>oi())}function oi(){return{color:[1,1,1],position:[1,1,2],direction:[1,1,1],attenuation:[1,0,0],coneCos:[1,0]}}function ii(e){const t=e.innerConeAngle??0,o=e.outerConeAngle??Math.PI/4;return[Math.cos(t),Math.cos(o)]}const ri=`#ifdef USE_IBL
@group(2) @binding(auto) var pbr_diffuseEnvSampler: texture_cube<f32>;
@group(2) @binding(auto) var pbr_diffuseEnvSamplerSampler: sampler;
@group(2) @binding(auto) var pbr_specularEnvSampler: texture_cube<f32>;
@group(2) @binding(auto) var pbr_specularEnvSamplerSampler: sampler;
@group(2) @binding(auto) var pbr_brdfLUT: texture_2d<f32>;
@group(2) @binding(auto) var pbr_brdfLUTSampler: sampler;
#endif
`,Ye=`#ifdef USE_IBL
uniform samplerCube pbr_diffuseEnvSampler;
uniform samplerCube pbr_specularEnvSampler;
uniform sampler2D pbr_brdfLUT;
#endif
`,Je={name:"ibl",firstBindingSlot:32,bindingLayout:[{name:"pbr_diffuseEnvSampler",group:2},{name:"pbr_specularEnvSampler",group:2},{name:"pbr_brdfLUT",group:2}],source:ri,vs:Ye,fs:Ye},ni=`struct dirlightUniforms {
  lightDirection: vec3<f32>,
};

alias DirlightNormal = vec3<f32>;

struct DirlightInputs {
  normal: DirlightNormal,
};

@group(2) @binding(auto) var<uniform> dirlight : dirlightUniforms;

// For vertex
fn dirlight_setNormal(normal: vec3<f32>) -> DirlightNormal {
  return normalize(normal);
}

// Returns color attenuated by angle from light source
fn dirlight_filterColor(color: vec4<f32>, inputs: DirlightInputs) -> vec4<f32> {
  // TODO - fix default light direction
  // let lightDirection = dirlight.lightDirection;
  let lightDirection = vec3<f32>(1, 1, 1);
  let d: f32 = abs(dot(inputs.normal, normalize(lightDirection)));
  return vec4<f32>(color.rgb * d, color.a);
}
`,ai=`out vec3 dirlight_vNormal;

void dirlight_setNormal(vec3 normal) {
  dirlight_vNormal = normalize(normal);
}
`,li=`layout(std140) uniform dirlightUniforms {
  vec3 lightDirection;
} dirlight;

in vec3 dirlight_vNormal;

// Returns color attenuated by angle from light source
vec4 dirlight_filterColor(vec4 color) {
  float d = abs(dot(dirlight_vNormal, normalize(dirlight.lightDirection)));
  return vec4(color.rgb * d, color.a);
}
`,Qe={props:{},uniforms:{},name:"dirlight",bindingLayout:[{name:"dirlight",group:2}],firstBindingSlot:16,dependencies:[],source:ni,vs:ai,fs:li,uniformTypes:{lightDirection:"vec3<f32>"},defaultUniforms:{lightDirection:[1,1,2]},getUniforms:si};function si(e=Qe.defaultUniforms){const t={};return e.lightDirection&&(t.lightDirection=e.lightDirection),t}const ci=`struct lambertMaterialUniforms {
  unlit: u32,
  ambient: f32,
  diffuse: f32,
};

@group(3) @binding(auto) var<uniform> lambertMaterial : lambertMaterialUniforms;

fn lighting_getLightColor(surfaceColor: vec3<f32>, light_direction: vec3<f32>, normal_worldspace: vec3<f32>, color: vec3<f32>) -> vec3<f32> {
  let lambertian: f32 = max(dot(light_direction, normal_worldspace), 0.0);
  return lambertian * lambertMaterial.diffuse * surfaceColor * color;
}

fn lighting_getLightColor2(surfaceColor: vec3<f32>, cameraPosition: vec3<f32>, position_worldspace: vec3<f32>, normal_worldspace: vec3<f32>) -> vec3<f32> {
  var lightColor: vec3<f32> = surfaceColor;

  if (lambertMaterial.unlit != 0u) {
    return surfaceColor;
  }

  if (lighting.enabled == 0) {
    return lightColor;
  }

  lightColor = lambertMaterial.ambient * surfaceColor * lighting.ambientColor;

  for (var i: i32 = 0; i < lighting.pointLightCount; i++) {
    let pointLight: PointLight = lighting_getPointLight(i);
    let light_position_worldspace: vec3<f32> = pointLight.position;
    let light_direction: vec3<f32> = normalize(light_position_worldspace - position_worldspace);
    let light_attenuation = getPointLightAttenuation(
      pointLight,
      distance(light_position_worldspace, position_worldspace)
    );
    lightColor += lighting_getLightColor(
      surfaceColor,
      light_direction,
      normal_worldspace,
      pointLight.color / light_attenuation
    );
  }

  for (var i: i32 = 0; i < lighting.spotLightCount; i++) {
    let spotLight: SpotLight = lighting_getSpotLight(i);
    let light_position_worldspace: vec3<f32> = spotLight.position;
    let light_direction: vec3<f32> = normalize(light_position_worldspace - position_worldspace);
    let light_attenuation = getSpotLightAttenuation(spotLight, position_worldspace);
    lightColor += lighting_getLightColor(
      surfaceColor,
      light_direction,
      normal_worldspace,
      spotLight.color / light_attenuation
    );
  }

  for (var i: i32 = 0; i < lighting.directionalLightCount; i++) {
    let directionalLight: DirectionalLight = lighting_getDirectionalLight(i);
    lightColor += lighting_getLightColor(
      surfaceColor,
      -directionalLight.direction,
      normal_worldspace,
      directionalLight.color
    );
  }

  return lightColor;
}
`,fi=`layout(std140) uniform lambertMaterialUniforms {
  uniform bool unlit;
  uniform float ambient;
  uniform float diffuse;
} material;
`,pi=`layout(std140) uniform lambertMaterialUniforms {
  uniform bool unlit;
  uniform float ambient;
  uniform float diffuse;
} material;

vec3 lighting_getLightColor(vec3 surfaceColor, vec3 light_direction, vec3 normal_worldspace, vec3 color) {
  float lambertian = max(dot(light_direction, normal_worldspace), 0.0);
  return lambertian * material.diffuse * surfaceColor * color;
}

vec3 lighting_getLightColor(vec3 surfaceColor, vec3 cameraPosition, vec3 position_worldspace, vec3 normal_worldspace) {
  vec3 lightColor = surfaceColor;

  if (material.unlit) {
    return surfaceColor;
  }

  if (lighting.enabled == 0) {
    return lightColor;
  }

  lightColor = material.ambient * surfaceColor * lighting.ambientColor;

  for (int i = 0; i < lighting.pointLightCount; i++) {
    PointLight pointLight = lighting_getPointLight(i);
    vec3 light_position_worldspace = pointLight.position;
    vec3 light_direction = normalize(light_position_worldspace - position_worldspace);
    float light_attenuation = getPointLightAttenuation(pointLight, distance(light_position_worldspace, position_worldspace));
    lightColor += lighting_getLightColor(surfaceColor, light_direction, normal_worldspace, pointLight.color / light_attenuation);
  }

  for (int i = 0; i < lighting.spotLightCount; i++) {
    SpotLight spotLight = lighting_getSpotLight(i);
    vec3 light_position_worldspace = spotLight.position;
    vec3 light_direction = normalize(light_position_worldspace - position_worldspace);
    float light_attenuation = getSpotLightAttenuation(spotLight, position_worldspace);
    lightColor += lighting_getLightColor(surfaceColor, light_direction, normal_worldspace, spotLight.color / light_attenuation);
  }

  for (int i = 0; i < lighting.directionalLightCount; i++) {
    DirectionalLight directionalLight = lighting_getDirectionalLight(i);
    lightColor += lighting_getLightColor(surfaceColor, -directionalLight.direction, normal_worldspace, directionalLight.color);
  }

  return lightColor;
}
`,et={name:"lambertMaterial",firstBindingSlot:0,bindingLayout:[{name:"lambertMaterial",group:3}],dependencies:[k],source:ci,vs:fi,fs:pi,defines:{LIGHTING_FRAGMENT:!0},uniformTypes:{unlit:"i32",ambient:"f32",diffuse:"f32"},defaultUniforms:{unlit:!1,ambient:.35,diffuse:.6},getUniforms(e){return{...et.defaultUniforms,...e}}},tt=`layout(std140) uniform phongMaterialUniforms {
  uniform bool unlit;
  uniform float ambient;
  uniform float diffuse;
  uniform float shininess;
  uniform vec3  specularColor;
} material;
`,ot=`layout(std140) uniform phongMaterialUniforms {
  uniform bool unlit;
  uniform float ambient;
  uniform float diffuse;
  uniform float shininess;
  uniform vec3  specularColor;
} material;

vec3 lighting_getLightColor(vec3 surfaceColor, vec3 light_direction, vec3 view_direction, vec3 normal_worldspace, vec3 color) {
  vec3 halfway_direction = normalize(light_direction + view_direction);
  float lambertian = dot(light_direction, normal_worldspace);
  float specular = 0.0;
  if (lambertian > 0.0) {
    float specular_angle = max(dot(normal_worldspace, halfway_direction), 0.0);
    specular = pow(specular_angle, material.shininess);
  }
  lambertian = max(lambertian, 0.0);
  return (lambertian * material.diffuse * surfaceColor + specular * floatColors_normalize(material.specularColor)) * color;
}

vec3 lighting_getLightColor(vec3 surfaceColor, vec3 cameraPosition, vec3 position_worldspace, vec3 normal_worldspace) {
  vec3 lightColor = surfaceColor;

  if (material.unlit) {
    return surfaceColor;
  }

  if (lighting.enabled == 0) {
    return lightColor;
  }

  vec3 view_direction = normalize(cameraPosition - position_worldspace);
  lightColor = material.ambient * surfaceColor * lighting.ambientColor;

  for (int i = 0; i < lighting.pointLightCount; i++) {
    PointLight pointLight = lighting_getPointLight(i);
    vec3 light_position_worldspace = pointLight.position;
    vec3 light_direction = normalize(light_position_worldspace - position_worldspace);
    float light_attenuation = getPointLightAttenuation(pointLight, distance(light_position_worldspace, position_worldspace));
    lightColor += lighting_getLightColor(surfaceColor, light_direction, view_direction, normal_worldspace, pointLight.color / light_attenuation);
  }

  for (int i = 0; i < lighting.spotLightCount; i++) {
    SpotLight spotLight = lighting_getSpotLight(i);
    vec3 light_position_worldspace = spotLight.position;
    vec3 light_direction = normalize(light_position_worldspace - position_worldspace);
    float light_attenuation = getSpotLightAttenuation(spotLight, position_worldspace);
    lightColor += lighting_getLightColor(surfaceColor, light_direction, view_direction, normal_worldspace, spotLight.color / light_attenuation);
  }

  for (int i = 0; i < lighting.directionalLightCount; i++) {
    DirectionalLight directionalLight = lighting_getDirectionalLight(i);
    lightColor += lighting_getLightColor(surfaceColor, -directionalLight.direction, view_direction, normal_worldspace, directionalLight.color);
  }
  
  return lightColor;
}
`,it=`struct phongMaterialUniforms {
  unlit: u32,
  ambient: f32,
  diffuse: f32,
  shininess: f32,
  specularColor: vec3<f32>,
};

@group(3) @binding(auto) var<uniform> phongMaterial : phongMaterialUniforms;

fn lighting_getLightColor(surfaceColor: vec3<f32>, light_direction: vec3<f32>, view_direction: vec3<f32>, normal_worldspace: vec3<f32>, color: vec3<f32>) -> vec3<f32> {
  let halfway_direction: vec3<f32> = normalize(light_direction + view_direction);
  var lambertian: f32 = dot(light_direction, normal_worldspace);
  var specular: f32 = 0.0;
  if (lambertian > 0.0) {
    let specular_angle = max(dot(normal_worldspace, halfway_direction), 0.0);
    specular = pow(specular_angle, phongMaterial.shininess);
  }
  lambertian = max(lambertian, 0.0);
  return (
    lambertian * phongMaterial.diffuse * surfaceColor +
    specular * floatColors_normalize(phongMaterial.specularColor)
  ) * color;
}

fn lighting_getLightColor2(surfaceColor: vec3<f32>, cameraPosition: vec3<f32>, position_worldspace: vec3<f32>, normal_worldspace: vec3<f32>) -> vec3<f32> {
  var lightColor: vec3<f32> = surfaceColor;

  if (phongMaterial.unlit != 0u) {
    return surfaceColor;
  }

  if (lighting.enabled == 0) {
    return lightColor;
  }

  let view_direction: vec3<f32> = normalize(cameraPosition - position_worldspace);
  lightColor = phongMaterial.ambient * surfaceColor * lighting.ambientColor;

  for (var i: i32 = 0; i < lighting.pointLightCount; i++) {
    let pointLight: PointLight = lighting_getPointLight(i);
    let light_position_worldspace: vec3<f32> = pointLight.position;
    let light_direction: vec3<f32> = normalize(light_position_worldspace - position_worldspace);
    let light_attenuation = getPointLightAttenuation(
      pointLight,
      distance(light_position_worldspace, position_worldspace)
    );
    lightColor += lighting_getLightColor(
      surfaceColor,
      light_direction,
      view_direction,
      normal_worldspace,
      pointLight.color / light_attenuation
    );
  }

  for (var i: i32 = 0; i < lighting.spotLightCount; i++) {
    let spotLight: SpotLight = lighting_getSpotLight(i);
    let light_position_worldspace: vec3<f32> = spotLight.position;
    let light_direction: vec3<f32> = normalize(light_position_worldspace - position_worldspace);
    let light_attenuation = getSpotLightAttenuation(spotLight, position_worldspace);
    lightColor += lighting_getLightColor(
      surfaceColor,
      light_direction,
      view_direction,
      normal_worldspace,
      spotLight.color / light_attenuation
    );
  }

  for (var i: i32 = 0; i < lighting.directionalLightCount; i++) {
    let directionalLight: DirectionalLight = lighting_getDirectionalLight(i);
    lightColor += lighting_getLightColor(surfaceColor, -directionalLight.direction, view_direction, normal_worldspace, directionalLight.color);
  }  
  
  return lightColor;
}

fn lighting_getSpecularLightColor(cameraPosition: vec3<f32>, position_worldspace: vec3<f32>, normal_worldspace: vec3<f32>) -> vec3<f32>{
  var lightColor = vec3<f32>(0, 0, 0);
  let surfaceColor = vec3<f32>(0, 0, 0);

  if (lighting.enabled != 0) {
    let view_direction = normalize(cameraPosition - position_worldspace);

    for (var i: i32 = 0; i < lighting.pointLightCount; i++) {
      let pointLight: PointLight = lighting_getPointLight(i);
      let light_position_worldspace: vec3<f32> = pointLight.position;
      let light_direction: vec3<f32> = normalize(light_position_worldspace - position_worldspace);
      let light_attenuation = getPointLightAttenuation(
        pointLight,
        distance(light_position_worldspace, position_worldspace)
      );
      lightColor += lighting_getLightColor(
        surfaceColor,
        light_direction,
        view_direction,
        normal_worldspace,
        pointLight.color / light_attenuation
      );
    }

    for (var i: i32 = 0; i < lighting.spotLightCount; i++) {
      let spotLight: SpotLight = lighting_getSpotLight(i);
      let light_position_worldspace: vec3<f32> = spotLight.position;
      let light_direction: vec3<f32> = normalize(light_position_worldspace - position_worldspace);
      let light_attenuation = getSpotLightAttenuation(spotLight, position_worldspace);
      lightColor += lighting_getLightColor(
        surfaceColor,
        light_direction,
        view_direction,
        normal_worldspace,
        spotLight.color / light_attenuation
      );
    }

    for (var i: i32 = 0; i < lighting.directionalLightCount; i++) {
        let directionalLight: DirectionalLight = lighting_getDirectionalLight(i);
        lightColor += lighting_getLightColor(surfaceColor, -directionalLight.direction, view_direction, normal_worldspace, directionalLight.color);
    }
  }
  return lightColor;
}
`,ui=[38.25,38.25,38.25],rt={props:{},name:"gouraudMaterial",bindingLayout:[{name:"gouraudMaterial",group:3}],vs:ot.replace("phongMaterial","gouraudMaterial"),fs:tt.replace("phongMaterial","gouraudMaterial"),source:it.replaceAll("phongMaterial","gouraudMaterial"),defines:{LIGHTING_VERTEX:!0},dependencies:[k,ue],uniformTypes:{unlit:"i32",ambient:"f32",diffuse:"f32",shininess:"f32",specularColor:"vec3<f32>"},defaultUniforms:{unlit:!1,ambient:.35,diffuse:.6,shininess:32,specularColor:ui},getUniforms(e){return{...rt.defaultUniforms,...e}}},gi=[38.25,38.25,38.25],nt={name:"phongMaterial",firstBindingSlot:0,bindingLayout:[{name:"phongMaterial",group:3}],dependencies:[k,ue],source:it,vs:tt,fs:ot,defines:{LIGHTING_FRAGMENT:!0},uniformTypes:{unlit:"i32",ambient:"f32",diffuse:"f32",shininess:"f32",specularColor:"vec3<f32>"},defaultUniforms:{unlit:!1,ambient:.35,diffuse:.6,shininess:32,specularColor:gi},getUniforms(e){return{...nt.defaultUniforms,...e}}},mi=`out vec3 pbr_vPosition;
out vec2 pbr_vUV0;
out vec2 pbr_vUV1;

#ifdef HAS_NORMALS
# ifdef HAS_TANGENTS
out mat3 pbr_vTBN;
# else
out vec3 pbr_vNormal;
# endif
#endif

void pbr_setPositionNormalTangentUV(
  vec4 position,
  vec4 normal,
  vec4 tangent,
  vec2 uv0,
  vec2 uv1
)
{
  vec4 pos = pbrProjection.modelMatrix * position;
  pbr_vPosition = vec3(pos.xyz) / pos.w;

#ifdef HAS_NORMALS
#ifdef HAS_TANGENTS
  vec3 normalW = normalize(vec3(pbrProjection.normalMatrix * vec4(normal.xyz, 0.0)));
  vec3 tangentW = normalize(vec3(pbrProjection.modelMatrix * vec4(tangent.xyz, 0.0)));
  vec3 bitangentW = cross(normalW, tangentW) * tangent.w;
  pbr_vTBN = mat3(tangentW, bitangentW, normalW);
#else // HAS_TANGENTS != 1
  pbr_vNormal = normalize(vec3(pbrProjection.modelMatrix * vec4(normal.xyz, 0.0)));
#endif
#endif

#ifdef HAS_UV
  pbr_vUV0 = uv0;
#else
  pbr_vUV0 = vec2(0.,0.);
#endif

  pbr_vUV1 = uv1;
}
`,di=`precision highp float;

layout(std140) uniform pbrMaterialUniforms {
  // Material is unlit
  bool unlit;

  // Base color map
  bool baseColorMapEnabled;
  vec4 baseColorFactor;

  bool normalMapEnabled;  
  float normalScale; // #ifdef HAS_NORMALMAP

  bool emissiveMapEnabled;
  vec3 emissiveFactor; // #ifdef HAS_EMISSIVEMAP

  vec2 metallicRoughnessValues;
  bool metallicRoughnessMapEnabled;

  bool occlusionMapEnabled;
  float occlusionStrength; // #ifdef HAS_OCCLUSIONMAP
  
  bool alphaCutoffEnabled;
  float alphaCutoff; // #ifdef ALPHA_CUTOFF

  vec3 specularColorFactor;
  float specularIntensityFactor;
  bool specularColorMapEnabled;
  bool specularIntensityMapEnabled;

  float ior;

  float transmissionFactor;
  bool transmissionMapEnabled;

  float thicknessFactor;
  float attenuationDistance;
  vec3 attenuationColor;

  float clearcoatFactor;
  float clearcoatRoughnessFactor;
  bool clearcoatMapEnabled;
  bool clearcoatRoughnessMapEnabled;

  vec3 sheenColorFactor;
  float sheenRoughnessFactor;
  bool sheenColorMapEnabled;
  bool sheenRoughnessMapEnabled;

  float iridescenceFactor;
  float iridescenceIor;
  vec2 iridescenceThicknessRange;
  bool iridescenceMapEnabled;

  float anisotropyStrength;
  float anisotropyRotation;
  vec2 anisotropyDirection;
  bool anisotropyMapEnabled;

  float emissiveStrength;
  
  // IBL
  bool IBLenabled;
  vec2 scaleIBLAmbient; // #ifdef USE_IBL
  
  // debugging flags used for shader output of intermediate PBR variables
  // #ifdef PBR_DEBUG
  vec4 scaleDiffBaseMR;
  vec4 scaleFGDSpec;
  // #endif

  int baseColorUVSet;
  mat3 baseColorUVTransform;
  int metallicRoughnessUVSet;
  mat3 metallicRoughnessUVTransform;
  int normalUVSet;
  mat3 normalUVTransform;
  int occlusionUVSet;
  mat3 occlusionUVTransform;
  int emissiveUVSet;
  mat3 emissiveUVTransform;
  int specularColorUVSet;
  mat3 specularColorUVTransform;
  int specularIntensityUVSet;
  mat3 specularIntensityUVTransform;
  int transmissionUVSet;
  mat3 transmissionUVTransform;
  int thicknessUVSet;
  mat3 thicknessUVTransform;
  int clearcoatUVSet;
  mat3 clearcoatUVTransform;
  int clearcoatRoughnessUVSet;
  mat3 clearcoatRoughnessUVTransform;
  int clearcoatNormalUVSet;
  mat3 clearcoatNormalUVTransform;
  int sheenColorUVSet;
  mat3 sheenColorUVTransform;
  int sheenRoughnessUVSet;
  mat3 sheenRoughnessUVTransform;
  int iridescenceUVSet;
  mat3 iridescenceUVTransform;
  int iridescenceThicknessUVSet;
  mat3 iridescenceThicknessUVTransform;
  int anisotropyUVSet;
  mat3 anisotropyUVTransform;
} pbrMaterial;

// Samplers
#ifdef HAS_BASECOLORMAP
uniform sampler2D pbr_baseColorSampler;
#endif
#ifdef HAS_NORMALMAP
uniform sampler2D pbr_normalSampler;
#endif
#ifdef HAS_EMISSIVEMAP
uniform sampler2D pbr_emissiveSampler;
#endif
#ifdef HAS_METALROUGHNESSMAP
uniform sampler2D pbr_metallicRoughnessSampler;
#endif
#ifdef HAS_OCCLUSIONMAP
uniform sampler2D pbr_occlusionSampler;
#endif
#ifdef HAS_SPECULARCOLORMAP
uniform sampler2D pbr_specularColorSampler;
#endif
#ifdef HAS_SPECULARINTENSITYMAP
uniform sampler2D pbr_specularIntensitySampler;
#endif
#ifdef HAS_TRANSMISSIONMAP
uniform sampler2D pbr_transmissionSampler;
#endif
#ifdef HAS_THICKNESSMAP
uniform sampler2D pbr_thicknessSampler;
#endif
#ifdef HAS_CLEARCOATMAP
uniform sampler2D pbr_clearcoatSampler;
#endif
#ifdef HAS_CLEARCOATROUGHNESSMAP
uniform sampler2D pbr_clearcoatRoughnessSampler;
#endif
#ifdef HAS_CLEARCOATNORMALMAP
uniform sampler2D pbr_clearcoatNormalSampler;
#endif
#ifdef HAS_SHEENCOLORMAP
uniform sampler2D pbr_sheenColorSampler;
#endif
#ifdef HAS_SHEENROUGHNESSMAP
uniform sampler2D pbr_sheenRoughnessSampler;
#endif
#ifdef HAS_IRIDESCENCEMAP
uniform sampler2D pbr_iridescenceSampler;
#endif
#ifdef HAS_IRIDESCENCETHICKNESSMAP
uniform sampler2D pbr_iridescenceThicknessSampler;
#endif
#ifdef HAS_ANISOTROPYMAP
uniform sampler2D pbr_anisotropySampler;
#endif
// Inputs from vertex shader

in vec3 pbr_vPosition;
in vec2 pbr_vUV0;
in vec2 pbr_vUV1;

#ifdef HAS_NORMALS
#ifdef HAS_TANGENTS
in mat3 pbr_vTBN;
#else
in vec3 pbr_vNormal;
#endif
#endif

// Encapsulate the various inputs used by the various functions in the shading equation
// We store values in this struct to simplify the integration of alternative implementations
// of the shading terms, outlined in the Readme.MD Appendix.
struct PBRInfo {
  float NdotL;                  // cos angle between normal and light direction
  float NdotV;                  // cos angle between normal and view direction
  float NdotH;                  // cos angle between normal and half vector
  float LdotH;                  // cos angle between light direction and half vector
  float VdotH;                  // cos angle between view direction and half vector
  float perceptualRoughness;    // roughness value, as authored by the model creator (input to shader)
  float metalness;              // metallic value at the surface
  vec3 reflectance0;            // full reflectance color (normal incidence angle)
  vec3 reflectance90;           // reflectance color at grazing angle
  float alphaRoughness;         // roughness mapped to a more linear change in the roughness (proposed by [2])
  vec3 diffuseColor;            // color contribution from diffuse lighting
  vec3 specularColor;           // color contribution from specular lighting
  vec3 n;                       // normal at surface point
  vec3 v;                       // vector from surface point to camera
};

const float M_PI = 3.141592653589793;
const float c_MinRoughness = 0.04;

vec3 calculateFinalColor(PBRInfo pbrInfo, vec3 lightColor);

vec4 SRGBtoLINEAR(vec4 srgbIn)
{
#ifdef MANUAL_SRGB
#ifdef SRGB_FAST_APPROXIMATION
  vec3 linOut = pow(srgbIn.xyz,vec3(2.2));
#else // SRGB_FAST_APPROXIMATION
  vec3 bLess = step(vec3(0.04045),srgbIn.xyz);
  vec3 linOut = mix( srgbIn.xyz/vec3(12.92), pow((srgbIn.xyz+vec3(0.055))/vec3(1.055),vec3(2.4)), bLess );
#endif //SRGB_FAST_APPROXIMATION
  return vec4(linOut,srgbIn.w);;
#else //MANUAL_SRGB
  return srgbIn;
#endif //MANUAL_SRGB
}

vec2 getMaterialUV(int uvSet, mat3 uvTransform)
{
  vec2 baseUV = uvSet == 1 ? pbr_vUV1 : pbr_vUV0;
  return (uvTransform * vec3(baseUV, 1.0)).xy;
}

// Build the tangent basis from interpolated attributes or screen-space derivatives.
mat3 getTBN(vec2 uv)
{
#ifndef HAS_TANGENTS
  vec3 pos_dx = dFdx(pbr_vPosition);
  vec3 pos_dy = dFdy(pbr_vPosition);
  vec3 tex_dx = dFdx(vec3(uv, 0.0));
  vec3 tex_dy = dFdy(vec3(uv, 0.0));
  vec3 t = (tex_dy.t * pos_dx - tex_dx.t * pos_dy) / (tex_dx.s * tex_dy.t - tex_dy.s * tex_dx.t);

#ifdef HAS_NORMALS
  vec3 ng = normalize(pbr_vNormal);
#else
  vec3 ng = cross(pos_dx, pos_dy);
#endif

  t = normalize(t - ng * dot(ng, t));
  vec3 b = normalize(cross(ng, t));
  mat3 tbn = mat3(t, b, ng);
#else // HAS_TANGENTS
  mat3 tbn = pbr_vTBN;
#endif

  return tbn;
}

// Find the normal for this fragment, pulling either from a predefined normal map
// or from the interpolated mesh normal and tangent attributes.
vec3 getMappedNormal(sampler2D normalSampler, mat3 tbn, float normalScale, vec2 uv)
{
  vec3 n = texture(normalSampler, uv).rgb;
  return normalize(tbn * ((2.0 * n - 1.0) * vec3(normalScale, normalScale, 1.0)));
}

vec3 getNormal(mat3 tbn, vec2 uv)
{
#ifdef HAS_NORMALMAP
  vec3 n = getMappedNormal(pbr_normalSampler, tbn, pbrMaterial.normalScale, uv);
#else
  // The tbn matrix is linearly interpolated, so we need to re-normalize
  vec3 n = normalize(tbn[2].xyz);
#endif

  return n;
}

vec3 getClearcoatNormal(mat3 tbn, vec3 baseNormal, vec2 uv)
{
#ifdef HAS_CLEARCOATNORMALMAP
  return getMappedNormal(pbr_clearcoatNormalSampler, tbn, 1.0, uv);
#else
  return baseNormal;
#endif
}

// Calculation of the lighting contribution from an optional Image Based Light source.
// Precomputed Environment Maps are required uniform inputs and are computed as outlined in [1].
// See our README.md on Environment Maps [3] for additional discussion.
#ifdef USE_IBL
vec3 getIBLContribution(PBRInfo pbrInfo, vec3 n, vec3 reflection)
{
  float mipCount = 9.0; // resolution of 512x512
  float lod = (pbrInfo.perceptualRoughness * mipCount);
  // retrieve a scale and bias to F0. See [1], Figure 3
  vec3 brdf = SRGBtoLINEAR(texture(pbr_brdfLUT,
    vec2(pbrInfo.NdotV, 1.0 - pbrInfo.perceptualRoughness))).rgb;
  vec3 diffuseLight = SRGBtoLINEAR(texture(pbr_diffuseEnvSampler, n)).rgb;

#ifdef USE_TEX_LOD
  vec3 specularLight = SRGBtoLINEAR(texture(pbr_specularEnvSampler, reflection, lod)).rgb;
#else
  vec3 specularLight = SRGBtoLINEAR(texture(pbr_specularEnvSampler, reflection)).rgb;
#endif

  vec3 diffuse = diffuseLight * pbrInfo.diffuseColor;
  vec3 specular = specularLight * (pbrInfo.specularColor * brdf.x + brdf.y);

  // For presentation, this allows us to disable IBL terms
  diffuse *= pbrMaterial.scaleIBLAmbient.x;
  specular *= pbrMaterial.scaleIBLAmbient.y;

  return diffuse + specular;
}
#endif

// Basic Lambertian diffuse
// Implementation from Lambert's Photometria https://archive.org/details/lambertsphotome00lambgoog
// See also [1], Equation 1
vec3 diffuse(PBRInfo pbrInfo)
{
  return pbrInfo.diffuseColor / M_PI;
}

// The following equation models the Fresnel reflectance term of the spec equation (aka F())
// Implementation of fresnel from [4], Equation 15
vec3 specularReflection(PBRInfo pbrInfo)
{
  return pbrInfo.reflectance0 +
    (pbrInfo.reflectance90 - pbrInfo.reflectance0) *
    pow(clamp(1.0 - pbrInfo.VdotH, 0.0, 1.0), 5.0);
}

// This calculates the specular geometric attenuation (aka G()),
// where rougher material will reflect less light back to the viewer.
// This implementation is based on [1] Equation 4, and we adopt their modifications to
// alphaRoughness as input as originally proposed in [2].
float geometricOcclusion(PBRInfo pbrInfo)
{
  float NdotL = pbrInfo.NdotL;
  float NdotV = pbrInfo.NdotV;
  float r = pbrInfo.alphaRoughness;

  float attenuationL = 2.0 * NdotL / (NdotL + sqrt(r * r + (1.0 - r * r) * (NdotL * NdotL)));
  float attenuationV = 2.0 * NdotV / (NdotV + sqrt(r * r + (1.0 - r * r) * (NdotV * NdotV)));
  return attenuationL * attenuationV;
}

// The following equation(s) model the distribution of microfacet normals across
// the area being drawn (aka D())
// Implementation from "Average Irregularity Representation of a Roughened Surface
// for Ray Reflection" by T. S. Trowbridge, and K. P. Reitz
// Follows the distribution function recommended in the SIGGRAPH 2013 course notes
// from EPIC Games [1], Equation 3.
float microfacetDistribution(PBRInfo pbrInfo)
{
  float roughnessSq = pbrInfo.alphaRoughness * pbrInfo.alphaRoughness;
  float f = (pbrInfo.NdotH * roughnessSq - pbrInfo.NdotH) * pbrInfo.NdotH + 1.0;
  return roughnessSq / (M_PI * f * f);
}

float maxComponent(vec3 value)
{
  return max(max(value.r, value.g), value.b);
}

float getDielectricF0(float ior)
{
  float clampedIor = max(ior, 1.0);
  float ratio = (clampedIor - 1.0) / (clampedIor + 1.0);
  return ratio * ratio;
}

vec2 normalizeDirection(vec2 direction)
{
  float directionLength = length(direction);
  return directionLength > 0.0001 ? direction / directionLength : vec2(1.0, 0.0);
}

vec2 rotateDirection(vec2 direction, float rotation)
{
  float s = sin(rotation);
  float c = cos(rotation);
  return vec2(direction.x * c - direction.y * s, direction.x * s + direction.y * c);
}

vec3 getIridescenceTint(float iridescence, float thickness, float NdotV)
{
  if (iridescence <= 0.0) {
    return vec3(1.0);
  }

  float phase = 0.015 * thickness * pbrMaterial.iridescenceIor + (1.0 - NdotV) * 6.0;
  vec3 thinFilmTint =
    0.5 + 0.5 * cos(vec3(phase, phase + 2.0943951, phase + 4.1887902));
  return mix(vec3(1.0), thinFilmTint, iridescence);
}

vec3 getVolumeAttenuation(float thickness)
{
  if (thickness <= 0.0) {
    return vec3(1.0);
  }

  vec3 attenuationCoefficient =
    -log(max(pbrMaterial.attenuationColor, vec3(0.0001))) /
    max(pbrMaterial.attenuationDistance, 0.0001);
  return exp(-attenuationCoefficient * thickness);
}

PBRInfo createClearcoatPBRInfo(PBRInfo basePBRInfo, vec3 clearcoatNormal, float clearcoatRoughness)
{
  float perceptualRoughness = clamp(clearcoatRoughness, c_MinRoughness, 1.0);
  float alphaRoughness = perceptualRoughness * perceptualRoughness;
  float NdotV = clamp(abs(dot(clearcoatNormal, basePBRInfo.v)), 0.001, 1.0);

  return PBRInfo(
    basePBRInfo.NdotL,
    NdotV,
    basePBRInfo.NdotH,
    basePBRInfo.LdotH,
    basePBRInfo.VdotH,
    perceptualRoughness,
    0.0,
    vec3(0.04),
    vec3(1.0),
    alphaRoughness,
    vec3(0.0),
    vec3(0.04),
    clearcoatNormal,
    basePBRInfo.v
  );
}

vec3 calculateClearcoatContribution(
  PBRInfo pbrInfo,
  vec3 lightColor,
  vec3 clearcoatNormal,
  float clearcoatFactor,
  float clearcoatRoughness
) {
  if (clearcoatFactor <= 0.0) {
    return vec3(0.0);
  }

  PBRInfo clearcoatPBRInfo = createClearcoatPBRInfo(pbrInfo, clearcoatNormal, clearcoatRoughness);
  return calculateFinalColor(clearcoatPBRInfo, lightColor) * clearcoatFactor;
}

#ifdef USE_IBL
vec3 calculateClearcoatIBLContribution(
  PBRInfo pbrInfo,
  vec3 clearcoatNormal,
  vec3 reflection,
  float clearcoatFactor,
  float clearcoatRoughness
) {
  if (clearcoatFactor <= 0.0) {
    return vec3(0.0);
  }

  PBRInfo clearcoatPBRInfo = createClearcoatPBRInfo(pbrInfo, clearcoatNormal, clearcoatRoughness);
  return getIBLContribution(clearcoatPBRInfo, clearcoatNormal, reflection) * clearcoatFactor;
}
#endif

vec3 calculateSheenContribution(
  PBRInfo pbrInfo,
  vec3 lightColor,
  vec3 sheenColor,
  float sheenRoughness
) {
  if (maxComponent(sheenColor) <= 0.0) {
    return vec3(0.0);
  }

  float sheenFresnel = pow(clamp(1.0 - pbrInfo.VdotH, 0.0, 1.0), 5.0);
  float sheenVisibility = mix(1.0, pbrInfo.NdotL * pbrInfo.NdotV, sheenRoughness);
  return pbrInfo.NdotL *
    lightColor *
    sheenColor *
    (0.25 + 0.75 * sheenFresnel) *
    sheenVisibility *
    (1.0 - pbrInfo.metalness);
}

float calculateAnisotropyBoost(
  PBRInfo pbrInfo,
  vec3 anisotropyTangent,
  float anisotropyStrength
) {
  if (anisotropyStrength <= 0.0) {
    return 1.0;
  }

  vec3 anisotropyBitangent = normalize(cross(pbrInfo.n, anisotropyTangent));
  float bitangentViewAlignment = abs(dot(pbrInfo.v, anisotropyBitangent));
  return mix(1.0, 0.65 + 0.7 * bitangentViewAlignment, anisotropyStrength);
}

vec3 calculateMaterialLightColor(
  PBRInfo pbrInfo,
  vec3 lightColor,
  vec3 clearcoatNormal,
  float clearcoatFactor,
  float clearcoatRoughness,
  vec3 sheenColor,
  float sheenRoughness,
  vec3 anisotropyTangent,
  float anisotropyStrength
) {
  float anisotropyBoost = calculateAnisotropyBoost(pbrInfo, anisotropyTangent, anisotropyStrength);
  vec3 color = calculateFinalColor(pbrInfo, lightColor) * anisotropyBoost;
  color += calculateClearcoatContribution(
    pbrInfo,
    lightColor,
    clearcoatNormal,
    clearcoatFactor,
    clearcoatRoughness
  );
  color += calculateSheenContribution(pbrInfo, lightColor, sheenColor, sheenRoughness);
  return color;
}

void PBRInfo_setAmbientLight(inout PBRInfo pbrInfo) {
  pbrInfo.NdotL = 1.0;
  pbrInfo.NdotH = 0.0;
  pbrInfo.LdotH = 0.0;
  pbrInfo.VdotH = 1.0;
}

void PBRInfo_setDirectionalLight(inout PBRInfo pbrInfo, vec3 lightDirection) {
  vec3 n = pbrInfo.n;
  vec3 v = pbrInfo.v;
  vec3 l = normalize(lightDirection);             // Vector from surface point to light
  vec3 h = normalize(l+v);                        // Half vector between both l and v

  pbrInfo.NdotL = clamp(dot(n, l), 0.001, 1.0);
  pbrInfo.NdotH = clamp(dot(n, h), 0.0, 1.0);
  pbrInfo.LdotH = clamp(dot(l, h), 0.0, 1.0);
  pbrInfo.VdotH = clamp(dot(v, h), 0.0, 1.0);
}

void PBRInfo_setPointLight(inout PBRInfo pbrInfo, PointLight pointLight) {
  vec3 light_direction = normalize(pointLight.position - pbr_vPosition);
  PBRInfo_setDirectionalLight(pbrInfo, light_direction);
}

void PBRInfo_setSpotLight(inout PBRInfo pbrInfo, SpotLight spotLight) {
  vec3 light_direction = normalize(spotLight.position - pbr_vPosition);
  PBRInfo_setDirectionalLight(pbrInfo, light_direction);
}

vec3 calculateFinalColor(PBRInfo pbrInfo, vec3 lightColor) {
  // Calculate the shading terms for the microfacet specular shading model
  vec3 F = specularReflection(pbrInfo);
  float G = geometricOcclusion(pbrInfo);
  float D = microfacetDistribution(pbrInfo);

  // Calculation of analytical lighting contribution
  vec3 diffuseContrib = (1.0 - F) * diffuse(pbrInfo);
  vec3 specContrib = F * G * D / (4.0 * pbrInfo.NdotL * pbrInfo.NdotV);
  // Obtain final intensity as reflectance (BRDF) scaled by the energy of the light (cosine law)
  return pbrInfo.NdotL * lightColor * (diffuseContrib + specContrib);
}

vec4 pbr_filterColor(vec4 colorUnused)
{
  vec2 baseColorUV = getMaterialUV(pbrMaterial.baseColorUVSet, pbrMaterial.baseColorUVTransform);
  vec2 metallicRoughnessUV = getMaterialUV(
    pbrMaterial.metallicRoughnessUVSet,
    pbrMaterial.metallicRoughnessUVTransform
  );
  vec2 normalUV = getMaterialUV(pbrMaterial.normalUVSet, pbrMaterial.normalUVTransform);
  vec2 occlusionUV = getMaterialUV(pbrMaterial.occlusionUVSet, pbrMaterial.occlusionUVTransform);
  vec2 emissiveUV = getMaterialUV(pbrMaterial.emissiveUVSet, pbrMaterial.emissiveUVTransform);
  vec2 specularColorUV = getMaterialUV(
    pbrMaterial.specularColorUVSet,
    pbrMaterial.specularColorUVTransform
  );
  vec2 specularIntensityUV = getMaterialUV(
    pbrMaterial.specularIntensityUVSet,
    pbrMaterial.specularIntensityUVTransform
  );
  vec2 transmissionUV = getMaterialUV(
    pbrMaterial.transmissionUVSet,
    pbrMaterial.transmissionUVTransform
  );
  vec2 thicknessUV = getMaterialUV(pbrMaterial.thicknessUVSet, pbrMaterial.thicknessUVTransform);
  vec2 clearcoatUV = getMaterialUV(pbrMaterial.clearcoatUVSet, pbrMaterial.clearcoatUVTransform);
  vec2 clearcoatRoughnessUV = getMaterialUV(
    pbrMaterial.clearcoatRoughnessUVSet,
    pbrMaterial.clearcoatRoughnessUVTransform
  );
  vec2 clearcoatNormalUV = getMaterialUV(
    pbrMaterial.clearcoatNormalUVSet,
    pbrMaterial.clearcoatNormalUVTransform
  );
  vec2 sheenColorUV = getMaterialUV(
    pbrMaterial.sheenColorUVSet,
    pbrMaterial.sheenColorUVTransform
  );
  vec2 sheenRoughnessUV = getMaterialUV(
    pbrMaterial.sheenRoughnessUVSet,
    pbrMaterial.sheenRoughnessUVTransform
  );
  vec2 iridescenceUV = getMaterialUV(
    pbrMaterial.iridescenceUVSet,
    pbrMaterial.iridescenceUVTransform
  );
  vec2 iridescenceThicknessUV = getMaterialUV(
    pbrMaterial.iridescenceThicknessUVSet,
    pbrMaterial.iridescenceThicknessUVTransform
  );
  vec2 anisotropyUV = getMaterialUV(
    pbrMaterial.anisotropyUVSet,
    pbrMaterial.anisotropyUVTransform
  );

  // The albedo may be defined from a base texture or a flat color
#ifdef HAS_BASECOLORMAP
  vec4 baseColor =
    SRGBtoLINEAR(texture(pbr_baseColorSampler, baseColorUV)) * pbrMaterial.baseColorFactor;
#else
  vec4 baseColor = pbrMaterial.baseColorFactor;
#endif

#ifdef ALPHA_CUTOFF
  if (baseColor.a < pbrMaterial.alphaCutoff) {
    discard;
  }
#endif

  vec3 color = vec3(0, 0, 0);

  float transmission = 0.0;

  if(pbrMaterial.unlit){
    color.rgb = baseColor.rgb;
  }
  else{
    // Metallic and Roughness material properties are packed together
    // In glTF, these factors can be specified by fixed scalar values
    // or from a metallic-roughness map
    float perceptualRoughness = pbrMaterial.metallicRoughnessValues.y;
    float metallic = pbrMaterial.metallicRoughnessValues.x;
#ifdef HAS_METALROUGHNESSMAP
    // Roughness is stored in the 'g' channel, metallic is stored in the 'b' channel.
    // This layout intentionally reserves the 'r' channel for (optional) occlusion map data
    vec4 mrSample = texture(pbr_metallicRoughnessSampler, metallicRoughnessUV);
    perceptualRoughness = mrSample.g * perceptualRoughness;
    metallic = mrSample.b * metallic;
#endif
    perceptualRoughness = clamp(perceptualRoughness, c_MinRoughness, 1.0);
    metallic = clamp(metallic, 0.0, 1.0);
    mat3 tbn = getTBN(normalUV);
    vec3 n = getNormal(tbn, normalUV);                          // normal at surface point
    vec3 v = normalize(pbrProjection.camera - pbr_vPosition);  // Vector from surface point to camera
    float NdotV = clamp(abs(dot(n, v)), 0.001, 1.0);
#ifdef USE_MATERIAL_EXTENSIONS
    bool useExtendedPBR =
      pbrMaterial.specularColorMapEnabled ||
      pbrMaterial.specularIntensityMapEnabled ||
      abs(pbrMaterial.specularIntensityFactor - 1.0) > 0.0001 ||
      maxComponent(abs(pbrMaterial.specularColorFactor - vec3(1.0))) > 0.0001 ||
      abs(pbrMaterial.ior - 1.5) > 0.0001 ||
      pbrMaterial.transmissionMapEnabled ||
      pbrMaterial.transmissionFactor > 0.0001 ||
      pbrMaterial.clearcoatMapEnabled ||
      pbrMaterial.clearcoatRoughnessMapEnabled ||
      pbrMaterial.clearcoatFactor > 0.0001 ||
      pbrMaterial.clearcoatRoughnessFactor > 0.0001 ||
      pbrMaterial.sheenColorMapEnabled ||
      pbrMaterial.sheenRoughnessMapEnabled ||
      maxComponent(pbrMaterial.sheenColorFactor) > 0.0001 ||
      pbrMaterial.sheenRoughnessFactor > 0.0001 ||
      pbrMaterial.iridescenceMapEnabled ||
      pbrMaterial.iridescenceFactor > 0.0001 ||
      abs(pbrMaterial.iridescenceIor - 1.3) > 0.0001 ||
      abs(pbrMaterial.iridescenceThicknessRange.x - 100.0) > 0.0001 ||
      abs(pbrMaterial.iridescenceThicknessRange.y - 400.0) > 0.0001 ||
      pbrMaterial.anisotropyMapEnabled ||
      pbrMaterial.anisotropyStrength > 0.0001 ||
      abs(pbrMaterial.anisotropyRotation) > 0.0001 ||
      length(pbrMaterial.anisotropyDirection - vec2(1.0, 0.0)) > 0.0001;
#else
    bool useExtendedPBR = false;
#endif

    if (!useExtendedPBR) {
      // Keep the baseline metallic-roughness implementation byte-for-byte equivalent in behavior.
      float alphaRoughness = perceptualRoughness * perceptualRoughness;

      vec3 f0 = vec3(0.04);
      vec3 diffuseColor = baseColor.rgb * (vec3(1.0) - f0);
      diffuseColor *= 1.0 - metallic;
      vec3 specularColor = mix(f0, baseColor.rgb, metallic);

      float reflectance = max(max(specularColor.r, specularColor.g), specularColor.b);
      float reflectance90 = clamp(reflectance * 25.0, 0.0, 1.0);
      vec3 specularEnvironmentR0 = specularColor.rgb;
      vec3 specularEnvironmentR90 = vec3(1.0, 1.0, 1.0) * reflectance90;
      vec3 reflection = -normalize(reflect(v, n));

      PBRInfo pbrInfo = PBRInfo(
        0.0, // NdotL
        NdotV,
        0.0, // NdotH
        0.0, // LdotH
        0.0, // VdotH
        perceptualRoughness,
        metallic,
        specularEnvironmentR0,
        specularEnvironmentR90,
        alphaRoughness,
        diffuseColor,
        specularColor,
        n,
        v
      );

#ifdef USE_LIGHTS
      PBRInfo_setAmbientLight(pbrInfo);
      color += calculateFinalColor(pbrInfo, lighting.ambientColor);

      for(int i = 0; i < lighting.directionalLightCount; i++) {
        if (i < lighting.directionalLightCount) {
          PBRInfo_setDirectionalLight(pbrInfo, lighting_getDirectionalLight(i).direction);
          color += calculateFinalColor(pbrInfo, lighting_getDirectionalLight(i).color);
        }
      }

      for(int i = 0; i < lighting.pointLightCount; i++) {
        if (i < lighting.pointLightCount) {
          PBRInfo_setPointLight(pbrInfo, lighting_getPointLight(i));
          float attenuation = getPointLightAttenuation(lighting_getPointLight(i), distance(lighting_getPointLight(i).position, pbr_vPosition));
          color += calculateFinalColor(pbrInfo, lighting_getPointLight(i).color / attenuation);
        }
      }

      for(int i = 0; i < lighting.spotLightCount; i++) {
        if (i < lighting.spotLightCount) {
          PBRInfo_setSpotLight(pbrInfo, lighting_getSpotLight(i));
          float attenuation = getSpotLightAttenuation(lighting_getSpotLight(i), pbr_vPosition);
          color += calculateFinalColor(pbrInfo, lighting_getSpotLight(i).color / attenuation);
        }
      }
#endif

#ifdef USE_IBL
      if (pbrMaterial.IBLenabled) {
        color += getIBLContribution(pbrInfo, n, reflection);
      }
#endif

#ifdef HAS_OCCLUSIONMAP
      if (pbrMaterial.occlusionMapEnabled) {
        float ao = texture(pbr_occlusionSampler, occlusionUV).r;
        color = mix(color, color * ao, pbrMaterial.occlusionStrength);
      }
#endif

      vec3 emissive = pbrMaterial.emissiveFactor;
#ifdef HAS_EMISSIVEMAP
      if (pbrMaterial.emissiveMapEnabled) {
        emissive *= SRGBtoLINEAR(texture(pbr_emissiveSampler, emissiveUV)).rgb;
      }
#endif
      color += emissive * pbrMaterial.emissiveStrength;

#ifdef PBR_DEBUG
      color = mix(color, baseColor.rgb, pbrMaterial.scaleDiffBaseMR.y);
      color = mix(color, vec3(metallic), pbrMaterial.scaleDiffBaseMR.z);
      color = mix(color, vec3(perceptualRoughness), pbrMaterial.scaleDiffBaseMR.w);
#endif

      return vec4(pow(color, vec3(1.0 / 2.2)), baseColor.a);
    }

    float specularIntensity = pbrMaterial.specularIntensityFactor;
#ifdef HAS_SPECULARINTENSITYMAP
    if (pbrMaterial.specularIntensityMapEnabled) {
      specularIntensity *= texture(pbr_specularIntensitySampler, specularIntensityUV).a;
    }
#endif

    vec3 specularFactor = pbrMaterial.specularColorFactor;
#ifdef HAS_SPECULARCOLORMAP
    if (pbrMaterial.specularColorMapEnabled) {
      specularFactor *= SRGBtoLINEAR(texture(pbr_specularColorSampler, specularColorUV)).rgb;
    }
#endif

    transmission = pbrMaterial.transmissionFactor;
#ifdef HAS_TRANSMISSIONMAP
    if (pbrMaterial.transmissionMapEnabled) {
      transmission *= texture(pbr_transmissionSampler, transmissionUV).r;
    }
#endif
    transmission = clamp(transmission * (1.0 - metallic), 0.0, 1.0);
    float thickness = max(pbrMaterial.thicknessFactor, 0.0);
#ifdef HAS_THICKNESSMAP
    thickness *= texture(pbr_thicknessSampler, thicknessUV).g;
#endif

    float clearcoatFactor = pbrMaterial.clearcoatFactor;
    float clearcoatRoughness = pbrMaterial.clearcoatRoughnessFactor;
#ifdef HAS_CLEARCOATMAP
    if (pbrMaterial.clearcoatMapEnabled) {
      clearcoatFactor *= texture(pbr_clearcoatSampler, clearcoatUV).r;
    }
#endif
#ifdef HAS_CLEARCOATROUGHNESSMAP
    if (pbrMaterial.clearcoatRoughnessMapEnabled) {
      clearcoatRoughness *= texture(pbr_clearcoatRoughnessSampler, clearcoatRoughnessUV).g;
    }
#endif
    clearcoatFactor = clamp(clearcoatFactor, 0.0, 1.0);
    clearcoatRoughness = clamp(clearcoatRoughness, c_MinRoughness, 1.0);
    vec3 clearcoatNormal = getClearcoatNormal(getTBN(clearcoatNormalUV), n, clearcoatNormalUV);

    vec3 sheenColor = pbrMaterial.sheenColorFactor;
    float sheenRoughness = pbrMaterial.sheenRoughnessFactor;
#ifdef HAS_SHEENCOLORMAP
    if (pbrMaterial.sheenColorMapEnabled) {
      sheenColor *= SRGBtoLINEAR(texture(pbr_sheenColorSampler, sheenColorUV)).rgb;
    }
#endif
#ifdef HAS_SHEENROUGHNESSMAP
    if (pbrMaterial.sheenRoughnessMapEnabled) {
      sheenRoughness *= texture(pbr_sheenRoughnessSampler, sheenRoughnessUV).a;
    }
#endif
    sheenRoughness = clamp(sheenRoughness, c_MinRoughness, 1.0);

    float iridescence = pbrMaterial.iridescenceFactor;
#ifdef HAS_IRIDESCENCEMAP
    if (pbrMaterial.iridescenceMapEnabled) {
      iridescence *= texture(pbr_iridescenceSampler, iridescenceUV).r;
    }
#endif
    iridescence = clamp(iridescence, 0.0, 1.0);
    float iridescenceThickness = mix(
      pbrMaterial.iridescenceThicknessRange.x,
      pbrMaterial.iridescenceThicknessRange.y,
      0.5
    );
#ifdef HAS_IRIDESCENCETHICKNESSMAP
    iridescenceThickness = mix(
      pbrMaterial.iridescenceThicknessRange.x,
      pbrMaterial.iridescenceThicknessRange.y,
      texture(pbr_iridescenceThicknessSampler, iridescenceThicknessUV).g
    );
#endif

    float anisotropyStrength = clamp(pbrMaterial.anisotropyStrength, 0.0, 1.0);
    vec2 anisotropyDirection = normalizeDirection(pbrMaterial.anisotropyDirection);
#ifdef HAS_ANISOTROPYMAP
    if (pbrMaterial.anisotropyMapEnabled) {
      vec3 anisotropySample = texture(pbr_anisotropySampler, anisotropyUV).rgb;
      anisotropyStrength *= anisotropySample.b;
      vec2 mappedDirection = anisotropySample.rg * 2.0 - 1.0;
      if (length(mappedDirection) > 0.0001) {
        anisotropyDirection = normalize(mappedDirection);
      }
    }
#endif
    anisotropyDirection = rotateDirection(anisotropyDirection, pbrMaterial.anisotropyRotation);
    vec3 anisotropyTangent = normalize(tbn[0] * anisotropyDirection.x + tbn[1] * anisotropyDirection.y);
    if (length(anisotropyTangent) < 0.0001) {
      anisotropyTangent = normalize(tbn[0]);
    }
    float anisotropyViewAlignment = abs(dot(v, anisotropyTangent));
    perceptualRoughness = mix(
      perceptualRoughness,
      clamp(perceptualRoughness * (1.0 - 0.6 * anisotropyViewAlignment), c_MinRoughness, 1.0),
      anisotropyStrength
    );

    // Roughness is authored as perceptual roughness; as is convention,
    // convert to material roughness by squaring the perceptual roughness [2].
    float alphaRoughness = perceptualRoughness * perceptualRoughness;

    float dielectricF0 = getDielectricF0(pbrMaterial.ior);
    vec3 dielectricSpecularF0 = min(
      vec3(dielectricF0) * specularFactor * specularIntensity,
      vec3(1.0)
    );
    vec3 iridescenceTint = getIridescenceTint(iridescence, iridescenceThickness, NdotV);
    dielectricSpecularF0 = mix(
      dielectricSpecularF0,
      dielectricSpecularF0 * iridescenceTint,
      iridescence
    );
    vec3 diffuseColor = baseColor.rgb * (vec3(1.0) - dielectricSpecularF0);
    diffuseColor *= (1.0 - metallic) * (1.0 - transmission);
    vec3 specularColor = mix(dielectricSpecularF0, baseColor.rgb, metallic);

    float baseLayerEnergy = 1.0 - clearcoatFactor * 0.25;
    diffuseColor *= baseLayerEnergy;
    specularColor *= baseLayerEnergy;

    // Compute reflectance.
    float reflectance = max(max(specularColor.r, specularColor.g), specularColor.b);

    // For typical incident reflectance range (between 4% to 100%) set the grazing
    // reflectance to 100% for typical fresnel effect.
    // For very low reflectance range on highly diffuse objects (below 4%),
    // incrementally reduce grazing reflecance to 0%.
    float reflectance90 = clamp(reflectance * 25.0, 0.0, 1.0);
    vec3 specularEnvironmentR0 = specularColor.rgb;
    vec3 specularEnvironmentR90 = vec3(1.0, 1.0, 1.0) * reflectance90;
    vec3 reflection = -normalize(reflect(v, n));

    PBRInfo pbrInfo = PBRInfo(
      0.0, // NdotL
      NdotV,
      0.0, // NdotH
      0.0, // LdotH
      0.0, // VdotH
      perceptualRoughness,
      metallic,
      specularEnvironmentR0,
      specularEnvironmentR90,
      alphaRoughness,
      diffuseColor,
      specularColor,
      n,
      v
    );


#ifdef USE_LIGHTS
    // Apply ambient light
    PBRInfo_setAmbientLight(pbrInfo);
    color += calculateMaterialLightColor(
      pbrInfo,
      lighting.ambientColor,
      clearcoatNormal,
      clearcoatFactor,
      clearcoatRoughness,
      sheenColor,
      sheenRoughness,
      anisotropyTangent,
      anisotropyStrength
    );

    // Apply directional light
    for(int i = 0; i < lighting.directionalLightCount; i++) {
      if (i < lighting.directionalLightCount) {
        PBRInfo_setDirectionalLight(pbrInfo, lighting_getDirectionalLight(i).direction);
        color += calculateMaterialLightColor(
          pbrInfo,
          lighting_getDirectionalLight(i).color,
          clearcoatNormal,
          clearcoatFactor,
          clearcoatRoughness,
          sheenColor,
          sheenRoughness,
          anisotropyTangent,
          anisotropyStrength
        );
      }
    }

    // Apply point light
    for(int i = 0; i < lighting.pointLightCount; i++) {
      if (i < lighting.pointLightCount) {
        PBRInfo_setPointLight(pbrInfo, lighting_getPointLight(i));
        float attenuation = getPointLightAttenuation(lighting_getPointLight(i), distance(lighting_getPointLight(i).position, pbr_vPosition));
        color += calculateMaterialLightColor(
          pbrInfo,
          lighting_getPointLight(i).color / attenuation,
          clearcoatNormal,
          clearcoatFactor,
          clearcoatRoughness,
          sheenColor,
          sheenRoughness,
          anisotropyTangent,
          anisotropyStrength
        );
      }
    }

    for(int i = 0; i < lighting.spotLightCount; i++) {
      if (i < lighting.spotLightCount) {
        PBRInfo_setSpotLight(pbrInfo, lighting_getSpotLight(i));
        float attenuation = getSpotLightAttenuation(lighting_getSpotLight(i), pbr_vPosition);
        color += calculateMaterialLightColor(
          pbrInfo,
          lighting_getSpotLight(i).color / attenuation,
          clearcoatNormal,
          clearcoatFactor,
          clearcoatRoughness,
          sheenColor,
          sheenRoughness,
          anisotropyTangent,
          anisotropyStrength
        );
      }
    }
#endif

    // Calculate lighting contribution from image based lighting source (IBL)
#ifdef USE_IBL
    if (pbrMaterial.IBLenabled) {
      color += getIBLContribution(pbrInfo, n, reflection) *
        calculateAnisotropyBoost(pbrInfo, anisotropyTangent, anisotropyStrength);
      color += calculateClearcoatIBLContribution(
        pbrInfo,
        clearcoatNormal,
        -normalize(reflect(v, clearcoatNormal)),
        clearcoatFactor,
        clearcoatRoughness
      );
      color += sheenColor * pbrMaterial.scaleIBLAmbient.x * (1.0 - sheenRoughness) * 0.25;
    }
#endif

 // Apply optional PBR terms for additional (optional) shading
#ifdef HAS_OCCLUSIONMAP
    if (pbrMaterial.occlusionMapEnabled) {
      float ao = texture(pbr_occlusionSampler, occlusionUV).r;
      color = mix(color, color * ao, pbrMaterial.occlusionStrength);
    }
#endif

    vec3 emissive = pbrMaterial.emissiveFactor;
#ifdef HAS_EMISSIVEMAP
    if (pbrMaterial.emissiveMapEnabled) {
      emissive *= SRGBtoLINEAR(texture(pbr_emissiveSampler, emissiveUV)).rgb;
    }
#endif
    color += emissive * pbrMaterial.emissiveStrength;

    if (transmission > 0.0) {
      color = mix(color, color * getVolumeAttenuation(thickness), transmission);
    }

    // This section uses mix to override final color for reference app visualization
    // of various parameters in the lighting equation.
#ifdef PBR_DEBUG
    // TODO: Figure out how to debug multiple lights

    // color = mix(color, F, pbr_scaleFGDSpec.x);
    // color = mix(color, vec3(G), pbr_scaleFGDSpec.y);
    // color = mix(color, vec3(D), pbr_scaleFGDSpec.z);
    // color = mix(color, specContrib, pbr_scaleFGDSpec.w);

    // color = mix(color, diffuseContrib, pbr_scaleDiffBaseMR.x);
    color = mix(color, baseColor.rgb, pbrMaterial.scaleDiffBaseMR.y);
    color = mix(color, vec3(metallic), pbrMaterial.scaleDiffBaseMR.z);
    color = mix(color, vec3(perceptualRoughness), pbrMaterial.scaleDiffBaseMR.w);
#endif

  }

  float alpha = clamp(baseColor.a * (1.0 - transmission), 0.0, 1.0);
  return vec4(pow(color,vec3(1.0/2.2)), alpha);
}
`,hi=`struct PBRFragmentInputs {
  pbr_vPosition: vec3f,
  pbr_vUV0: vec2f,
  pbr_vUV1: vec2f,
  pbr_vTBN: mat3x3f,
  pbr_vNormal: vec3f
};

var<private> fragmentInputs: PBRFragmentInputs;

fn pbr_setPositionNormalTangentUV(
  position: vec4f,
  normal: vec4f,
  tangent: vec4f,
  uv0: vec2f,
  uv1: vec2f
)
{
  var pos: vec4f = pbrProjection.modelMatrix * position;
  fragmentInputs.pbr_vPosition = pos.xyz / pos.w;
  fragmentInputs.pbr_vNormal = vec3f(0.0, 0.0, 1.0);
  fragmentInputs.pbr_vTBN = mat3x3f(
    vec3f(1.0, 0.0, 0.0),
    vec3f(0.0, 1.0, 0.0),
    vec3f(0.0, 0.0, 1.0)
  );
  fragmentInputs.pbr_vUV0 = vec2f(0.0, 0.0);
  fragmentInputs.pbr_vUV1 = uv1;

#ifdef HAS_NORMALS
  let normalW: vec3f = normalize((pbrProjection.normalMatrix * vec4f(normal.xyz, 0.0)).xyz);
  fragmentInputs.pbr_vNormal = normalW;
#ifdef HAS_TANGENTS
  let tangentW: vec3f = normalize((pbrProjection.modelMatrix * vec4f(tangent.xyz, 0.0)).xyz);
  let bitangentW: vec3f = cross(normalW, tangentW) * tangent.w;
  fragmentInputs.pbr_vTBN = mat3x3f(tangentW, bitangentW, normalW);
#endif
#endif

#ifdef HAS_UV
  fragmentInputs.pbr_vUV0 = uv0;
#endif
}

struct pbrMaterialUniforms {
  // Material is unlit
  unlit: u32,

  // Base color map
  baseColorMapEnabled: u32,
  baseColorFactor: vec4f,

  normalMapEnabled : u32,
  normalScale: f32,  // #ifdef HAS_NORMALMAP

  emissiveMapEnabled: u32,
  emissiveFactor: vec3f, // #ifdef HAS_EMISSIVEMAP

  metallicRoughnessValues: vec2f,
  metallicRoughnessMapEnabled: u32,

  occlusionMapEnabled: i32,
  occlusionStrength: f32, // #ifdef HAS_OCCLUSIONMAP
  
  alphaCutoffEnabled: i32,
  alphaCutoff: f32, // #ifdef ALPHA_CUTOFF

  specularColorFactor: vec3f,
  specularIntensityFactor: f32,
  specularColorMapEnabled: i32,
  specularIntensityMapEnabled: i32,

  ior: f32,

  transmissionFactor: f32,
  transmissionMapEnabled: i32,

  thicknessFactor: f32,
  attenuationDistance: f32,
  attenuationColor: vec3f,

  clearcoatFactor: f32,
  clearcoatRoughnessFactor: f32,
  clearcoatMapEnabled: i32,
  clearcoatRoughnessMapEnabled: i32,

  sheenColorFactor: vec3f,
  sheenRoughnessFactor: f32,
  sheenColorMapEnabled: i32,
  sheenRoughnessMapEnabled: i32,

  iridescenceFactor: f32,
  iridescenceIor: f32,
  iridescenceThicknessRange: vec2f,
  iridescenceMapEnabled: i32,

  anisotropyStrength: f32,
  anisotropyRotation: f32,
  anisotropyDirection: vec2f,
  anisotropyMapEnabled: i32,

  emissiveStrength: f32,
  
  // IBL
  IBLenabled: i32,
  scaleIBLAmbient: vec2f, // #ifdef USE_IBL
  
  // debugging flags used for shader output of intermediate PBR variables
  // #ifdef PBR_DEBUG
  scaleDiffBaseMR: vec4f,
  scaleFGDSpec: vec4f,
  // #endif

  baseColorUVSet: i32,
  baseColorUVTransform: mat3x3f,
  metallicRoughnessUVSet: i32,
  metallicRoughnessUVTransform: mat3x3f,
  normalUVSet: i32,
  normalUVTransform: mat3x3f,
  occlusionUVSet: i32,
  occlusionUVTransform: mat3x3f,
  emissiveUVSet: i32,
  emissiveUVTransform: mat3x3f,
  specularColorUVSet: i32,
  specularColorUVTransform: mat3x3f,
  specularIntensityUVSet: i32,
  specularIntensityUVTransform: mat3x3f,
  transmissionUVSet: i32,
  transmissionUVTransform: mat3x3f,
  thicknessUVSet: i32,
  thicknessUVTransform: mat3x3f,
  clearcoatUVSet: i32,
  clearcoatUVTransform: mat3x3f,
  clearcoatRoughnessUVSet: i32,
  clearcoatRoughnessUVTransform: mat3x3f,
  clearcoatNormalUVSet: i32,
  clearcoatNormalUVTransform: mat3x3f,
  sheenColorUVSet: i32,
  sheenColorUVTransform: mat3x3f,
  sheenRoughnessUVSet: i32,
  sheenRoughnessUVTransform: mat3x3f,
  iridescenceUVSet: i32,
  iridescenceUVTransform: mat3x3f,
  iridescenceThicknessUVSet: i32,
  iridescenceThicknessUVTransform: mat3x3f,
  anisotropyUVSet: i32,
  anisotropyUVTransform: mat3x3f,
}

@group(3) @binding(auto) var<uniform> pbrMaterial : pbrMaterialUniforms;

// Samplers
#ifdef HAS_BASECOLORMAP
@group(3) @binding(auto) var pbr_baseColorSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_baseColorSamplerSampler: sampler;
#endif
#ifdef HAS_NORMALMAP
@group(3) @binding(auto) var pbr_normalSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_normalSamplerSampler: sampler;
#endif
#ifdef HAS_EMISSIVEMAP
@group(3) @binding(auto) var pbr_emissiveSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_emissiveSamplerSampler: sampler;
#endif
#ifdef HAS_METALROUGHNESSMAP
@group(3) @binding(auto) var pbr_metallicRoughnessSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_metallicRoughnessSamplerSampler: sampler;
#endif
#ifdef HAS_OCCLUSIONMAP
@group(3) @binding(auto) var pbr_occlusionSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_occlusionSamplerSampler: sampler;
#endif
#ifdef HAS_SPECULARCOLORMAP
@group(3) @binding(auto) var pbr_specularColorSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_specularColorSamplerSampler: sampler;
#endif
#ifdef HAS_SPECULARINTENSITYMAP
@group(3) @binding(auto) var pbr_specularIntensitySampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_specularIntensitySamplerSampler: sampler;
#endif
#ifdef HAS_TRANSMISSIONMAP
@group(3) @binding(auto) var pbr_transmissionSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_transmissionSamplerSampler: sampler;
#endif
#ifdef HAS_THICKNESSMAP
@group(3) @binding(auto) var pbr_thicknessSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_thicknessSamplerSampler: sampler;
#endif
#ifdef HAS_CLEARCOATMAP
@group(3) @binding(auto) var pbr_clearcoatSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_clearcoatSamplerSampler: sampler;
#endif
#ifdef HAS_CLEARCOATROUGHNESSMAP
@group(3) @binding(auto) var pbr_clearcoatRoughnessSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_clearcoatRoughnessSamplerSampler: sampler;
#endif
#ifdef HAS_CLEARCOATNORMALMAP
@group(3) @binding(auto) var pbr_clearcoatNormalSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_clearcoatNormalSamplerSampler: sampler;
#endif
#ifdef HAS_SHEENCOLORMAP
@group(3) @binding(auto) var pbr_sheenColorSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_sheenColorSamplerSampler: sampler;
#endif
#ifdef HAS_SHEENROUGHNESSMAP
@group(3) @binding(auto) var pbr_sheenRoughnessSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_sheenRoughnessSamplerSampler: sampler;
#endif
#ifdef HAS_IRIDESCENCEMAP
@group(3) @binding(auto) var pbr_iridescenceSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_iridescenceSamplerSampler: sampler;
#endif
#ifdef HAS_IRIDESCENCETHICKNESSMAP
@group(3) @binding(auto) var pbr_iridescenceThicknessSampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_iridescenceThicknessSamplerSampler: sampler;
#endif
#ifdef HAS_ANISOTROPYMAP
@group(3) @binding(auto) var pbr_anisotropySampler: texture_2d<f32>;
@group(3) @binding(auto) var pbr_anisotropySamplerSampler: sampler;
#endif
// Encapsulate the various inputs used by the various functions in the shading equation
// We store values in this struct to simplify the integration of alternative implementations
// of the shading terms, outlined in the Readme.MD Appendix.
struct PBRInfo {
  NdotL: f32,                  // cos angle between normal and light direction
  NdotV: f32,                  // cos angle between normal and view direction
  NdotH: f32,                  // cos angle between normal and half vector
  LdotH: f32,                  // cos angle between light direction and half vector
  VdotH: f32,                  // cos angle between view direction and half vector
  perceptualRoughness: f32,    // roughness value, as authored by the model creator (input to shader)
  metalness: f32,              // metallic value at the surface
  reflectance0: vec3f,            // full reflectance color (normal incidence angle)
  reflectance90: vec3f,           // reflectance color at grazing angle
  alphaRoughness: f32,         // roughness mapped to a more linear change in the roughness (proposed by [2])
  diffuseColor: vec3f,            // color contribution from diffuse lighting
  specularColor: vec3f,           // color contribution from specular lighting
  n: vec3f,                       // normal at surface point
  v: vec3f,                       // vector from surface point to camera
};

const M_PI = 3.141592653589793;
const c_MinRoughness = 0.04;

fn SRGBtoLINEAR(srgbIn: vec4f ) -> vec4f
{
  var linOut: vec3f = srgbIn.xyz;
#ifdef MANUAL_SRGB
  let bLess: vec3f = step(vec3f(0.04045), srgbIn.xyz);
  linOut = mix(
    srgbIn.xyz / vec3f(12.92),
    pow((srgbIn.xyz + vec3f(0.055)) / vec3f(1.055), vec3f(2.4)),
    bLess
  );
#ifdef SRGB_FAST_APPROXIMATION
  linOut = pow(srgbIn.xyz, vec3f(2.2));
#endif
#endif
  return vec4f(linOut, srgbIn.w);
}

fn getMaterialUV(uvSet: i32, uvTransform: mat3x3f) -> vec2f
{
  var baseUV = fragmentInputs.pbr_vUV0;
  if (uvSet == 1) {
    baseUV = fragmentInputs.pbr_vUV1;
  }
  return (uvTransform * vec3f(baseUV, 1.0)).xy;
}

// Build the tangent basis from interpolated attributes or screen-space derivatives.
fn getTBN(uv: vec2f) -> mat3x3f
{
  let pos_dx: vec3f = dpdx(fragmentInputs.pbr_vPosition);
  let pos_dy: vec3f = dpdy(fragmentInputs.pbr_vPosition);
  let tex_dx: vec3f = dpdx(vec3f(uv, 0.0));
  let tex_dy: vec3f = dpdy(vec3f(uv, 0.0));
  var t: vec3f = (tex_dy.y * pos_dx - tex_dx.y * pos_dy) / (tex_dx.x * tex_dy.y - tex_dy.x * tex_dx.y);

  var ng: vec3f = cross(pos_dx, pos_dy);
#ifdef HAS_NORMALS
  ng = normalize(fragmentInputs.pbr_vNormal);
#endif
  t = normalize(t - ng * dot(ng, t));
  var b: vec3f = normalize(cross(ng, t));
  var tbn: mat3x3f = mat3x3f(t, b, ng);
#ifdef HAS_TANGENTS
  tbn = fragmentInputs.pbr_vTBN;
#endif

  return tbn;
}

// Find the normal for this fragment, pulling either from a predefined normal map
// or from the interpolated mesh normal and tangent attributes.
fn getMappedNormal(
  normalSampler: texture_2d<f32>,
  normalSamplerBinding: sampler,
  tbn: mat3x3f,
  normalScale: f32,
  uv: vec2f
) -> vec3f
{
  let n = textureSample(normalSampler, normalSamplerBinding, uv).rgb;
  return normalize(tbn * ((2.0 * n - 1.0) * vec3f(normalScale, normalScale, 1.0)));
}

fn getNormal(tbn: mat3x3f, uv: vec2f) -> vec3f
{
  // The tbn matrix is linearly interpolated, so we need to re-normalize
  var n: vec3f = normalize(tbn[2].xyz);
#ifdef HAS_NORMALMAP
  n = getMappedNormal(
    pbr_normalSampler,
    pbr_normalSamplerSampler,
    tbn,
    pbrMaterial.normalScale,
    uv
  );
#endif

  return n;
}

fn getClearcoatNormal(tbn: mat3x3f, baseNormal: vec3f, uv: vec2f) -> vec3f
{
#ifdef HAS_CLEARCOATNORMALMAP
  return getMappedNormal(
    pbr_clearcoatNormalSampler,
    pbr_clearcoatNormalSamplerSampler,
    tbn,
    1.0,
    uv
  );
#else
  return baseNormal;
#endif
}

// Calculation of the lighting contribution from an optional Image Based Light source.
// Precomputed Environment Maps are required uniform inputs and are computed as outlined in [1].
// See our README.md on Environment Maps [3] for additional discussion.
#ifdef USE_IBL
fn getIBLContribution(pbrInfo: PBRInfo, n: vec3f, reflection: vec3f) -> vec3f
{
  let mipCount: f32 = 9.0; // resolution of 512x512
  let lod: f32 = pbrInfo.perceptualRoughness * mipCount;
  // retrieve a scale and bias to F0. See [1], Figure 3
  let brdf = SRGBtoLINEAR(
    textureSampleLevel(
      pbr_brdfLUT,
      pbr_brdfLUTSampler,
      vec2f(pbrInfo.NdotV, 1.0 - pbrInfo.perceptualRoughness),
      0.0
    )
  ).rgb;
  let diffuseLight =
    SRGBtoLINEAR(
      textureSampleLevel(pbr_diffuseEnvSampler, pbr_diffuseEnvSamplerSampler, n, 0.0)
    ).rgb;
  var specularLight = SRGBtoLINEAR(
    textureSampleLevel(
      pbr_specularEnvSampler,
      pbr_specularEnvSamplerSampler,
      reflection,
      0.0
    )
  ).rgb;
#ifdef USE_TEX_LOD
  specularLight = SRGBtoLINEAR(
    textureSampleLevel(
      pbr_specularEnvSampler,
      pbr_specularEnvSamplerSampler,
      reflection,
      lod
    )
  ).rgb;
#endif

  let diffuse = diffuseLight * pbrInfo.diffuseColor * pbrMaterial.scaleIBLAmbient.x;
  let specular =
    specularLight * (pbrInfo.specularColor * brdf.x + brdf.y) * pbrMaterial.scaleIBLAmbient.y;

  return diffuse + specular;
}
#endif

// Basic Lambertian diffuse
// Implementation from Lambert's Photometria https://archive.org/details/lambertsphotome00lambgoog
// See also [1], Equation 1
fn diffuse(pbrInfo: PBRInfo) -> vec3<f32> {
  return pbrInfo.diffuseColor / M_PI;
}

// The following equation models the Fresnel reflectance term of the spec equation (aka F())
// Implementation of fresnel from [4], Equation 15
fn specularReflection(pbrInfo: PBRInfo) -> vec3<f32> {
  return pbrInfo.reflectance0 +
    (pbrInfo.reflectance90 - pbrInfo.reflectance0) *
    pow(clamp(1.0 - pbrInfo.VdotH, 0.0, 1.0), 5.0);
}

// This calculates the specular geometric attenuation (aka G()),
// where rougher material will reflect less light back to the viewer.
// This implementation is based on [1] Equation 4, and we adopt their modifications to
// alphaRoughness as input as originally proposed in [2].
fn geometricOcclusion(pbrInfo: PBRInfo) -> f32 {
  let NdotL: f32 = pbrInfo.NdotL;
  let NdotV: f32 = pbrInfo.NdotV;
  let r: f32 = pbrInfo.alphaRoughness;

  let attenuationL = 2.0 * NdotL / (NdotL + sqrt(r * r + (1.0 - r * r) * (NdotL * NdotL)));
  let attenuationV = 2.0 * NdotV / (NdotV + sqrt(r * r + (1.0 - r * r) * (NdotV * NdotV)));
  return attenuationL * attenuationV;
}

// The following equation(s) model the distribution of microfacet normals across
// the area being drawn (aka D())
// Implementation from "Average Irregularity Representation of a Roughened Surface
// for Ray Reflection" by T. S. Trowbridge, and K. P. Reitz
// Follows the distribution function recommended in the SIGGRAPH 2013 course notes
// from EPIC Games [1], Equation 3.
fn microfacetDistribution(pbrInfo: PBRInfo) -> f32 {
  let roughnessSq = pbrInfo.alphaRoughness * pbrInfo.alphaRoughness;
  let f = (pbrInfo.NdotH * roughnessSq - pbrInfo.NdotH) * pbrInfo.NdotH + 1.0;
  return roughnessSq / (M_PI * f * f);
}

fn maxComponent(value: vec3f) -> f32 {
  return max(max(value.r, value.g), value.b);
}

fn getDielectricF0(ior: f32) -> f32 {
  let clampedIor = max(ior, 1.0);
  let ratio = (clampedIor - 1.0) / (clampedIor + 1.0);
  return ratio * ratio;
}

fn normalizeDirection(direction: vec2f) -> vec2f {
  let directionLength = length(direction);
  if (directionLength > 0.0001) {
    return direction / directionLength;
  }

  return vec2f(1.0, 0.0);
}

fn rotateDirection(direction: vec2f, rotation: f32) -> vec2f {
  let s = sin(rotation);
  let c = cos(rotation);
  return vec2f(direction.x * c - direction.y * s, direction.x * s + direction.y * c);
}

fn getIridescenceTint(iridescence: f32, thickness: f32, NdotV: f32) -> vec3f {
  if (iridescence <= 0.0) {
    return vec3f(1.0);
  }

  let phase = 0.015 * thickness * pbrMaterial.iridescenceIor + (1.0 - NdotV) * 6.0;
  let thinFilmTint =
    0.5 +
    0.5 *
    cos(vec3f(phase, phase + 2.0943951, phase + 4.1887902));
  return mix(vec3f(1.0), thinFilmTint, iridescence);
}

fn getVolumeAttenuation(thickness: f32) -> vec3f {
  if (thickness <= 0.0) {
    return vec3f(1.0);
  }

  let attenuationCoefficient =
    -log(max(pbrMaterial.attenuationColor, vec3f(0.0001))) /
    max(pbrMaterial.attenuationDistance, 0.0001);
  return exp(-attenuationCoefficient * thickness);
}

fn createClearcoatPBRInfo(
  basePBRInfo: PBRInfo,
  clearcoatNormal: vec3f,
  clearcoatRoughness: f32
) -> PBRInfo {
  let perceptualRoughness = clamp(clearcoatRoughness, c_MinRoughness, 1.0);
  let alphaRoughness = perceptualRoughness * perceptualRoughness;
  let NdotV = clamp(abs(dot(clearcoatNormal, basePBRInfo.v)), 0.001, 1.0);

  return PBRInfo(
    basePBRInfo.NdotL,
    NdotV,
    basePBRInfo.NdotH,
    basePBRInfo.LdotH,
    basePBRInfo.VdotH,
    perceptualRoughness,
    0.0,
    vec3f(0.04),
    vec3f(1.0),
    alphaRoughness,
    vec3f(0.0),
    vec3f(0.04),
    clearcoatNormal,
    basePBRInfo.v
  );
}

fn calculateClearcoatContribution(
  pbrInfo: PBRInfo,
  lightColor: vec3f,
  clearcoatNormal: vec3f,
  clearcoatFactor: f32,
  clearcoatRoughness: f32
) -> vec3f {
  if (clearcoatFactor <= 0.0) {
    return vec3f(0.0);
  }

  let clearcoatPBRInfo = createClearcoatPBRInfo(pbrInfo, clearcoatNormal, clearcoatRoughness);
  return calculateFinalColor(clearcoatPBRInfo, lightColor) * clearcoatFactor;
}

#ifdef USE_IBL
fn calculateClearcoatIBLContribution(
  pbrInfo: PBRInfo,
  clearcoatNormal: vec3f,
  reflection: vec3f,
  clearcoatFactor: f32,
  clearcoatRoughness: f32
) -> vec3f {
  if (clearcoatFactor <= 0.0) {
    return vec3f(0.0);
  }

  let clearcoatPBRInfo = createClearcoatPBRInfo(pbrInfo, clearcoatNormal, clearcoatRoughness);
  return getIBLContribution(clearcoatPBRInfo, clearcoatNormal, reflection) * clearcoatFactor;
}
#endif

fn calculateSheenContribution(
  pbrInfo: PBRInfo,
  lightColor: vec3f,
  sheenColor: vec3f,
  sheenRoughness: f32
) -> vec3f {
  if (maxComponent(sheenColor) <= 0.0) {
    return vec3f(0.0);
  }

  let sheenFresnel = pow(clamp(1.0 - pbrInfo.VdotH, 0.0, 1.0), 5.0);
  let sheenVisibility = mix(1.0, pbrInfo.NdotL * pbrInfo.NdotV, sheenRoughness);
  return pbrInfo.NdotL *
    lightColor *
    sheenColor *
    (0.25 + 0.75 * sheenFresnel) *
    sheenVisibility *
    (1.0 - pbrInfo.metalness);
}

fn calculateAnisotropyBoost(
  pbrInfo: PBRInfo,
  anisotropyTangent: vec3f,
  anisotropyStrength: f32
) -> f32 {
  if (anisotropyStrength <= 0.0) {
    return 1.0;
  }

  let anisotropyBitangent = normalize(cross(pbrInfo.n, anisotropyTangent));
  let bitangentViewAlignment = abs(dot(pbrInfo.v, anisotropyBitangent));
  return mix(1.0, 0.65 + 0.7 * bitangentViewAlignment, anisotropyStrength);
}

fn calculateMaterialLightColor(
  pbrInfo: PBRInfo,
  lightColor: vec3f,
  clearcoatNormal: vec3f,
  clearcoatFactor: f32,
  clearcoatRoughness: f32,
  sheenColor: vec3f,
  sheenRoughness: f32,
  anisotropyTangent: vec3f,
  anisotropyStrength: f32
) -> vec3f {
  let anisotropyBoost = calculateAnisotropyBoost(pbrInfo, anisotropyTangent, anisotropyStrength);
  var color = calculateFinalColor(pbrInfo, lightColor) * anisotropyBoost;
  color += calculateClearcoatContribution(
    pbrInfo,
    lightColor,
    clearcoatNormal,
    clearcoatFactor,
    clearcoatRoughness
  );
  color += calculateSheenContribution(pbrInfo, lightColor, sheenColor, sheenRoughness);
  return color;
}

fn PBRInfo_setAmbientLight(pbrInfo: ptr<function, PBRInfo>) {
  (*pbrInfo).NdotL = 1.0;
  (*pbrInfo).NdotH = 0.0;
  (*pbrInfo).LdotH = 0.0;
  (*pbrInfo).VdotH = 1.0;
}

fn PBRInfo_setDirectionalLight(pbrInfo: ptr<function, PBRInfo>, lightDirection: vec3<f32>) {
  let n = (*pbrInfo).n;
  let v = (*pbrInfo).v;
  let l = normalize(lightDirection);             // Vector from surface point to light
  let h = normalize(l + v);                      // Half vector between both l and v

  (*pbrInfo).NdotL = clamp(dot(n, l), 0.001, 1.0);
  (*pbrInfo).NdotH = clamp(dot(n, h), 0.0, 1.0);
  (*pbrInfo).LdotH = clamp(dot(l, h), 0.0, 1.0);
  (*pbrInfo).VdotH = clamp(dot(v, h), 0.0, 1.0);
}

fn PBRInfo_setPointLight(pbrInfo: ptr<function, PBRInfo>, pointLight: PointLight) {
  let light_direction = normalize(pointLight.position - fragmentInputs.pbr_vPosition);
  PBRInfo_setDirectionalLight(pbrInfo, light_direction);
}

fn PBRInfo_setSpotLight(pbrInfo: ptr<function, PBRInfo>, spotLight: SpotLight) {
  let light_direction = normalize(spotLight.position - fragmentInputs.pbr_vPosition);
  PBRInfo_setDirectionalLight(pbrInfo, light_direction);
}

fn calculateFinalColor(pbrInfo: PBRInfo, lightColor: vec3<f32>) -> vec3<f32> {
  // Calculate the shading terms for the microfacet specular shading model
  let F = specularReflection(pbrInfo);
  let G = geometricOcclusion(pbrInfo);
  let D = microfacetDistribution(pbrInfo);

  // Calculation of analytical lighting contribution
  let diffuseContrib = (1.0 - F) * diffuse(pbrInfo);
  let specContrib = F * G * D / (4.0 * pbrInfo.NdotL * pbrInfo.NdotV);
  // Obtain final intensity as reflectance (BRDF) scaled by the energy of the light (cosine law)
  return pbrInfo.NdotL * lightColor * (diffuseContrib + specContrib);
}

fn pbr_filterColor(colorUnused: vec4<f32>) -> vec4<f32> {
  let baseColorUV = getMaterialUV(pbrMaterial.baseColorUVSet, pbrMaterial.baseColorUVTransform);
  let metallicRoughnessUV = getMaterialUV(
    pbrMaterial.metallicRoughnessUVSet,
    pbrMaterial.metallicRoughnessUVTransform
  );
  let normalUV = getMaterialUV(pbrMaterial.normalUVSet, pbrMaterial.normalUVTransform);
  let occlusionUV = getMaterialUV(pbrMaterial.occlusionUVSet, pbrMaterial.occlusionUVTransform);
  let emissiveUV = getMaterialUV(pbrMaterial.emissiveUVSet, pbrMaterial.emissiveUVTransform);
  let specularColorUV = getMaterialUV(
    pbrMaterial.specularColorUVSet,
    pbrMaterial.specularColorUVTransform
  );
  let specularIntensityUV = getMaterialUV(
    pbrMaterial.specularIntensityUVSet,
    pbrMaterial.specularIntensityUVTransform
  );
  let transmissionUV = getMaterialUV(
    pbrMaterial.transmissionUVSet,
    pbrMaterial.transmissionUVTransform
  );
  let thicknessUV = getMaterialUV(pbrMaterial.thicknessUVSet, pbrMaterial.thicknessUVTransform);
  let clearcoatUV = getMaterialUV(pbrMaterial.clearcoatUVSet, pbrMaterial.clearcoatUVTransform);
  let clearcoatRoughnessUV = getMaterialUV(
    pbrMaterial.clearcoatRoughnessUVSet,
    pbrMaterial.clearcoatRoughnessUVTransform
  );
  let clearcoatNormalUV = getMaterialUV(
    pbrMaterial.clearcoatNormalUVSet,
    pbrMaterial.clearcoatNormalUVTransform
  );
  let sheenColorUV = getMaterialUV(
    pbrMaterial.sheenColorUVSet,
    pbrMaterial.sheenColorUVTransform
  );
  let sheenRoughnessUV = getMaterialUV(
    pbrMaterial.sheenRoughnessUVSet,
    pbrMaterial.sheenRoughnessUVTransform
  );
  let iridescenceUV = getMaterialUV(
    pbrMaterial.iridescenceUVSet,
    pbrMaterial.iridescenceUVTransform
  );
  let iridescenceThicknessUV = getMaterialUV(
    pbrMaterial.iridescenceThicknessUVSet,
    pbrMaterial.iridescenceThicknessUVTransform
  );
  let anisotropyUV = getMaterialUV(
    pbrMaterial.anisotropyUVSet,
    pbrMaterial.anisotropyUVTransform
  );

  // The albedo may be defined from a base texture or a flat color
  var baseColor: vec4<f32> = pbrMaterial.baseColorFactor;
  #ifdef HAS_BASECOLORMAP
  baseColor = SRGBtoLINEAR(
    textureSample(pbr_baseColorSampler, pbr_baseColorSamplerSampler, baseColorUV)
  ) * pbrMaterial.baseColorFactor;
  #endif

  #ifdef ALPHA_CUTOFF
  if (baseColor.a < pbrMaterial.alphaCutoff) {
    discard;
  }
  #endif

  var color = vec3<f32>(0.0, 0.0, 0.0);
  var transmission = 0.0;

  if (pbrMaterial.unlit != 0u) {
    color = baseColor.rgb;
  } else {
    // Metallic and Roughness material properties are packed together
    // In glTF, these factors can be specified by fixed scalar values
    // or from a metallic-roughness map
    var perceptualRoughness = pbrMaterial.metallicRoughnessValues.y;
    var metallic = pbrMaterial.metallicRoughnessValues.x;
    #ifdef HAS_METALROUGHNESSMAP
    // Roughness is stored in the 'g' channel, metallic is stored in the 'b' channel.
    // This layout intentionally reserves the 'r' channel for (optional) occlusion map data
    let mrSample = textureSample(
      pbr_metallicRoughnessSampler,
      pbr_metallicRoughnessSamplerSampler,
      metallicRoughnessUV
    );
    perceptualRoughness = mrSample.g * perceptualRoughness;
    metallic = mrSample.b * metallic;
    #endif
    perceptualRoughness = clamp(perceptualRoughness, c_MinRoughness, 1.0);
    metallic = clamp(metallic, 0.0, 1.0);
    let tbn = getTBN(normalUV);
    let n = getNormal(tbn, normalUV);                          // normal at surface point
    let v = normalize(pbrProjection.camera - fragmentInputs.pbr_vPosition);  // Vector from surface point to camera
    let NdotV = clamp(abs(dot(n, v)), 0.001, 1.0);
    var useExtendedPBR = false;
    #ifdef USE_MATERIAL_EXTENSIONS
    useExtendedPBR =
      pbrMaterial.specularColorMapEnabled != 0 ||
      pbrMaterial.specularIntensityMapEnabled != 0 ||
      abs(pbrMaterial.specularIntensityFactor - 1.0) > 0.0001 ||
      maxComponent(abs(pbrMaterial.specularColorFactor - vec3f(1.0))) > 0.0001 ||
      abs(pbrMaterial.ior - 1.5) > 0.0001 ||
      pbrMaterial.transmissionMapEnabled != 0 ||
      pbrMaterial.transmissionFactor > 0.0001 ||
      pbrMaterial.clearcoatMapEnabled != 0 ||
      pbrMaterial.clearcoatRoughnessMapEnabled != 0 ||
      pbrMaterial.clearcoatFactor > 0.0001 ||
      pbrMaterial.clearcoatRoughnessFactor > 0.0001 ||
      pbrMaterial.sheenColorMapEnabled != 0 ||
      pbrMaterial.sheenRoughnessMapEnabled != 0 ||
      maxComponent(pbrMaterial.sheenColorFactor) > 0.0001 ||
      pbrMaterial.sheenRoughnessFactor > 0.0001 ||
      pbrMaterial.iridescenceMapEnabled != 0 ||
      pbrMaterial.iridescenceFactor > 0.0001 ||
      abs(pbrMaterial.iridescenceIor - 1.3) > 0.0001 ||
      abs(pbrMaterial.iridescenceThicknessRange.x - 100.0) > 0.0001 ||
      abs(pbrMaterial.iridescenceThicknessRange.y - 400.0) > 0.0001 ||
      pbrMaterial.anisotropyMapEnabled != 0 ||
      pbrMaterial.anisotropyStrength > 0.0001 ||
      abs(pbrMaterial.anisotropyRotation) > 0.0001 ||
      length(pbrMaterial.anisotropyDirection - vec2f(1.0, 0.0)) > 0.0001;
    #endif

    if (!useExtendedPBR) {
      let alphaRoughness = perceptualRoughness * perceptualRoughness;

      let f0 = vec3<f32>(0.04);
      var diffuseColor = baseColor.rgb * (vec3<f32>(1.0) - f0);
      diffuseColor *= 1.0 - metallic;
      let specularColor = mix(f0, baseColor.rgb, metallic);

      let reflectance = max(max(specularColor.r, specularColor.g), specularColor.b);
      let reflectance90 = clamp(reflectance * 25.0, 0.0, 1.0);
      let specularEnvironmentR0 = specularColor;
      let specularEnvironmentR90 = vec3<f32>(1.0, 1.0, 1.0) * reflectance90;
      let reflection = -normalize(reflect(v, n));

      var pbrInfo = PBRInfo(
        0.0, // NdotL
        NdotV,
        0.0, // NdotH
        0.0, // LdotH
        0.0, // VdotH
        perceptualRoughness,
        metallic,
        specularEnvironmentR0,
        specularEnvironmentR90,
        alphaRoughness,
        diffuseColor,
        specularColor,
        n,
        v
      );

      #ifdef USE_LIGHTS
      PBRInfo_setAmbientLight(&pbrInfo);
      color += calculateFinalColor(pbrInfo, lighting.ambientColor);

      for (var i = 0; i < lighting.directionalLightCount; i++) {
        if (i < lighting.directionalLightCount) {
          PBRInfo_setDirectionalLight(&pbrInfo, lighting_getDirectionalLight(i).direction);
          color += calculateFinalColor(pbrInfo, lighting_getDirectionalLight(i).color);
        }
      }

      for (var i = 0; i < lighting.pointLightCount; i++) {
        if (i < lighting.pointLightCount) {
          PBRInfo_setPointLight(&pbrInfo, lighting_getPointLight(i));
          let attenuation = getPointLightAttenuation(
            lighting_getPointLight(i),
            distance(lighting_getPointLight(i).position, fragmentInputs.pbr_vPosition)
          );
          color += calculateFinalColor(pbrInfo, lighting_getPointLight(i).color / attenuation);
        }
      }

      for (var i = 0; i < lighting.spotLightCount; i++) {
        if (i < lighting.spotLightCount) {
          PBRInfo_setSpotLight(&pbrInfo, lighting_getSpotLight(i));
          let attenuation = getSpotLightAttenuation(
            lighting_getSpotLight(i),
            fragmentInputs.pbr_vPosition
          );
          color += calculateFinalColor(pbrInfo, lighting_getSpotLight(i).color / attenuation);
        }
      }
      #endif

      #ifdef USE_IBL
      if (pbrMaterial.IBLenabled != 0) {
        color += getIBLContribution(pbrInfo, n, reflection);
      }
      #endif

      #ifdef HAS_OCCLUSIONMAP
      if (pbrMaterial.occlusionMapEnabled != 0) {
        let ao = textureSample(pbr_occlusionSampler, pbr_occlusionSamplerSampler, occlusionUV).r;
        color = mix(color, color * ao, pbrMaterial.occlusionStrength);
      }
      #endif

      var emissive = pbrMaterial.emissiveFactor;
      #ifdef HAS_EMISSIVEMAP
      if (pbrMaterial.emissiveMapEnabled != 0u) {
        emissive *= SRGBtoLINEAR(
          textureSample(pbr_emissiveSampler, pbr_emissiveSamplerSampler, emissiveUV)
        ).rgb;
      }
      #endif
      color += emissive * pbrMaterial.emissiveStrength;

      #ifdef PBR_DEBUG
      color = mix(color, baseColor.rgb, pbrMaterial.scaleDiffBaseMR.y);
      color = mix(color, vec3<f32>(metallic), pbrMaterial.scaleDiffBaseMR.z);
      color = mix(color, vec3<f32>(perceptualRoughness), pbrMaterial.scaleDiffBaseMR.w);
      #endif

      return vec4<f32>(pow(color, vec3<f32>(1.0 / 2.2)), baseColor.a);
    }

    var specularIntensity = pbrMaterial.specularIntensityFactor;
    #ifdef HAS_SPECULARINTENSITYMAP
    if (pbrMaterial.specularIntensityMapEnabled != 0) {
      specularIntensity *= textureSample(
        pbr_specularIntensitySampler,
        pbr_specularIntensitySamplerSampler,
        specularIntensityUV
      ).a;
    }
    #endif

    var specularFactor = pbrMaterial.specularColorFactor;
    #ifdef HAS_SPECULARCOLORMAP
    if (pbrMaterial.specularColorMapEnabled != 0) {
      specularFactor *= SRGBtoLINEAR(
        textureSample(
          pbr_specularColorSampler,
          pbr_specularColorSamplerSampler,
          specularColorUV
        )
      ).rgb;
    }
    #endif

    transmission = pbrMaterial.transmissionFactor;
    #ifdef HAS_TRANSMISSIONMAP
    if (pbrMaterial.transmissionMapEnabled != 0) {
      transmission *= textureSample(
        pbr_transmissionSampler,
        pbr_transmissionSamplerSampler,
        transmissionUV
      ).r;
    }
    #endif
    transmission = clamp(transmission * (1.0 - metallic), 0.0, 1.0);
    var thickness = max(pbrMaterial.thicknessFactor, 0.0);
    #ifdef HAS_THICKNESSMAP
    thickness *= textureSample(
      pbr_thicknessSampler,
      pbr_thicknessSamplerSampler,
      thicknessUV
    ).g;
    #endif

    var clearcoatFactor = pbrMaterial.clearcoatFactor;
    var clearcoatRoughness = pbrMaterial.clearcoatRoughnessFactor;
    #ifdef HAS_CLEARCOATMAP
    if (pbrMaterial.clearcoatMapEnabled != 0) {
      clearcoatFactor *= textureSample(
        pbr_clearcoatSampler,
        pbr_clearcoatSamplerSampler,
        clearcoatUV
      ).r;
    }
    #endif
    #ifdef HAS_CLEARCOATROUGHNESSMAP
    if (pbrMaterial.clearcoatRoughnessMapEnabled != 0) {
      clearcoatRoughness *= textureSample(
        pbr_clearcoatRoughnessSampler,
        pbr_clearcoatRoughnessSamplerSampler,
        clearcoatRoughnessUV
      ).g;
    }
    #endif
    clearcoatFactor = clamp(clearcoatFactor, 0.0, 1.0);
    clearcoatRoughness = clamp(clearcoatRoughness, c_MinRoughness, 1.0);
    let clearcoatNormal = getClearcoatNormal(getTBN(clearcoatNormalUV), n, clearcoatNormalUV);

    var sheenColor = pbrMaterial.sheenColorFactor;
    var sheenRoughness = pbrMaterial.sheenRoughnessFactor;
    #ifdef HAS_SHEENCOLORMAP
    if (pbrMaterial.sheenColorMapEnabled != 0) {
      sheenColor *= SRGBtoLINEAR(
        textureSample(
          pbr_sheenColorSampler,
          pbr_sheenColorSamplerSampler,
          sheenColorUV
        )
      ).rgb;
    }
    #endif
    #ifdef HAS_SHEENROUGHNESSMAP
    if (pbrMaterial.sheenRoughnessMapEnabled != 0) {
      sheenRoughness *= textureSample(
        pbr_sheenRoughnessSampler,
        pbr_sheenRoughnessSamplerSampler,
        sheenRoughnessUV
      ).a;
    }
    #endif
    sheenRoughness = clamp(sheenRoughness, c_MinRoughness, 1.0);

    var iridescence = pbrMaterial.iridescenceFactor;
    #ifdef HAS_IRIDESCENCEMAP
    if (pbrMaterial.iridescenceMapEnabled != 0) {
      iridescence *= textureSample(
        pbr_iridescenceSampler,
        pbr_iridescenceSamplerSampler,
        iridescenceUV
      ).r;
    }
    #endif
    iridescence = clamp(iridescence, 0.0, 1.0);
    var iridescenceThickness = mix(
      pbrMaterial.iridescenceThicknessRange.x,
      pbrMaterial.iridescenceThicknessRange.y,
      0.5
    );
    #ifdef HAS_IRIDESCENCETHICKNESSMAP
    iridescenceThickness = mix(
      pbrMaterial.iridescenceThicknessRange.x,
      pbrMaterial.iridescenceThicknessRange.y,
      textureSample(
        pbr_iridescenceThicknessSampler,
        pbr_iridescenceThicknessSamplerSampler,
        iridescenceThicknessUV
      ).g
    );
    #endif

    var anisotropyStrength = clamp(pbrMaterial.anisotropyStrength, 0.0, 1.0);
    var anisotropyDirection = normalizeDirection(pbrMaterial.anisotropyDirection);
    #ifdef HAS_ANISOTROPYMAP
    if (pbrMaterial.anisotropyMapEnabled != 0) {
      let anisotropySample = textureSample(
        pbr_anisotropySampler,
        pbr_anisotropySamplerSampler,
        anisotropyUV
      ).rgb;
      anisotropyStrength *= anisotropySample.b;
      let mappedDirection = anisotropySample.rg * 2.0 - 1.0;
      if (length(mappedDirection) > 0.0001) {
        anisotropyDirection = normalize(mappedDirection);
      }
    }
    #endif
    anisotropyDirection = rotateDirection(anisotropyDirection, pbrMaterial.anisotropyRotation);
    var anisotropyTangent =
      normalize(tbn[0] * anisotropyDirection.x + tbn[1] * anisotropyDirection.y);
    if (length(anisotropyTangent) < 0.0001) {
      anisotropyTangent = normalize(tbn[0]);
    }
    let anisotropyViewAlignment = abs(dot(v, anisotropyTangent));
    perceptualRoughness = mix(
      perceptualRoughness,
      clamp(perceptualRoughness * (1.0 - 0.6 * anisotropyViewAlignment), c_MinRoughness, 1.0),
      anisotropyStrength
    );

    // Roughness is authored as perceptual roughness; as is convention,
    // convert to material roughness by squaring the perceptual roughness [2].
    let alphaRoughness = perceptualRoughness * perceptualRoughness;

    let dielectricF0 = getDielectricF0(pbrMaterial.ior);
    var dielectricSpecularF0 = min(
      vec3f(dielectricF0) * specularFactor * specularIntensity,
      vec3f(1.0)
    );
    let iridescenceTint = getIridescenceTint(iridescence, iridescenceThickness, NdotV);
    dielectricSpecularF0 = mix(
      dielectricSpecularF0,
      dielectricSpecularF0 * iridescenceTint,
      iridescence
    );
    var diffuseColor = baseColor.rgb * (vec3f(1.0) - dielectricSpecularF0);
    diffuseColor *= (1.0 - metallic) * (1.0 - transmission);
    var specularColor = mix(dielectricSpecularF0, baseColor.rgb, metallic);

    let baseLayerEnergy = 1.0 - clearcoatFactor * 0.25;
    diffuseColor *= baseLayerEnergy;
    specularColor *= baseLayerEnergy;

    // Compute reflectance.
    let reflectance = max(max(specularColor.r, specularColor.g), specularColor.b);

    // For typical incident reflectance range (between 4% to 100%) set the grazing
    // reflectance to 100% for typical fresnel effect.
    // For very low reflectance range on highly diffuse objects (below 4%),
    // incrementally reduce grazing reflectance to 0%.
    let reflectance90 = clamp(reflectance * 25.0, 0.0, 1.0);
    let specularEnvironmentR0 = specularColor;
    let specularEnvironmentR90 = vec3<f32>(1.0, 1.0, 1.0) * reflectance90;
    let reflection = -normalize(reflect(v, n));

    var pbrInfo = PBRInfo(
      0.0, // NdotL
      NdotV,
      0.0, // NdotH
      0.0, // LdotH
      0.0, // VdotH
      perceptualRoughness,
      metallic,
      specularEnvironmentR0,
      specularEnvironmentR90,
      alphaRoughness,
      diffuseColor,
      specularColor,
      n,
      v
    );

    #ifdef USE_LIGHTS
    // Apply ambient light
    PBRInfo_setAmbientLight(&pbrInfo);
    color += calculateMaterialLightColor(
      pbrInfo,
      lighting.ambientColor,
      clearcoatNormal,
      clearcoatFactor,
      clearcoatRoughness,
      sheenColor,
      sheenRoughness,
      anisotropyTangent,
      anisotropyStrength
    );

    // Apply directional light
    for (var i = 0; i < lighting.directionalLightCount; i++) {
      if (i < lighting.directionalLightCount) {
        PBRInfo_setDirectionalLight(&pbrInfo, lighting_getDirectionalLight(i).direction);
        color += calculateMaterialLightColor(
          pbrInfo,
          lighting_getDirectionalLight(i).color,
          clearcoatNormal,
          clearcoatFactor,
          clearcoatRoughness,
          sheenColor,
          sheenRoughness,
          anisotropyTangent,
          anisotropyStrength
        );
      }
    }

    // Apply point light
    for (var i = 0; i < lighting.pointLightCount; i++) {
      if (i < lighting.pointLightCount) {
        PBRInfo_setPointLight(&pbrInfo, lighting_getPointLight(i));
        let attenuation = getPointLightAttenuation(
          lighting_getPointLight(i),
          distance(lighting_getPointLight(i).position, fragmentInputs.pbr_vPosition)
        );
        color += calculateMaterialLightColor(
          pbrInfo,
          lighting_getPointLight(i).color / attenuation,
          clearcoatNormal,
          clearcoatFactor,
          clearcoatRoughness,
          sheenColor,
          sheenRoughness,
          anisotropyTangent,
          anisotropyStrength
        );
      }
    }

    for (var i = 0; i < lighting.spotLightCount; i++) {
      if (i < lighting.spotLightCount) {
        PBRInfo_setSpotLight(&pbrInfo, lighting_getSpotLight(i));
        let attenuation = getSpotLightAttenuation(lighting_getSpotLight(i), fragmentInputs.pbr_vPosition);
        color += calculateMaterialLightColor(
          pbrInfo,
          lighting_getSpotLight(i).color / attenuation,
          clearcoatNormal,
          clearcoatFactor,
          clearcoatRoughness,
          sheenColor,
          sheenRoughness,
          anisotropyTangent,
          anisotropyStrength
        );
      }
    }
    #endif

    // Calculate lighting contribution from image based lighting source (IBL)
    #ifdef USE_IBL
    if (pbrMaterial.IBLenabled != 0) {
      color += getIBLContribution(pbrInfo, n, reflection) *
        calculateAnisotropyBoost(pbrInfo, anisotropyTangent, anisotropyStrength);
      color += calculateClearcoatIBLContribution(
        pbrInfo,
        clearcoatNormal,
        -normalize(reflect(v, clearcoatNormal)),
        clearcoatFactor,
        clearcoatRoughness
      );
      color += sheenColor * pbrMaterial.scaleIBLAmbient.x * (1.0 - sheenRoughness) * 0.25;
    }
    #endif

    // Apply optional PBR terms for additional (optional) shading
    #ifdef HAS_OCCLUSIONMAP
    if (pbrMaterial.occlusionMapEnabled != 0) {
      let ao = textureSample(pbr_occlusionSampler, pbr_occlusionSamplerSampler, occlusionUV).r;
      color = mix(color, color * ao, pbrMaterial.occlusionStrength);
    }
    #endif

    var emissive = pbrMaterial.emissiveFactor;
    #ifdef HAS_EMISSIVEMAP
    if (pbrMaterial.emissiveMapEnabled != 0u) {
      emissive *= SRGBtoLINEAR(
        textureSample(pbr_emissiveSampler, pbr_emissiveSamplerSampler, emissiveUV)
      ).rgb;
    }
    #endif
    color += emissive * pbrMaterial.emissiveStrength;

    if (transmission > 0.0) {
      color = mix(color, color * getVolumeAttenuation(thickness), transmission);
    }

    // This section uses mix to override final color for reference app visualization
    // of various parameters in the lighting equation.
    #ifdef PBR_DEBUG
    // TODO: Figure out how to debug multiple lights

    // color = mix(color, F, pbr_scaleFGDSpec.x);
    // color = mix(color, vec3(G), pbr_scaleFGDSpec.y);
    // color = mix(color, vec3(D), pbr_scaleFGDSpec.z);
    // color = mix(color, specContrib, pbr_scaleFGDSpec.w);

    // color = mix(color, diffuseContrib, pbr_scaleDiffBaseMR.x);
    color = mix(color, baseColor.rgb, pbrMaterial.scaleDiffBaseMR.y);
    color = mix(color, vec3<f32>(metallic), pbrMaterial.scaleDiffBaseMR.z);
    color = mix(color, vec3<f32>(perceptualRoughness), pbrMaterial.scaleDiffBaseMR.w);
    #endif
  }

  let alpha = clamp(baseColor.a * (1.0 - transmission), 0.0, 1.0);
  return vec4<f32>(pow(color, vec3<f32>(1.0 / 2.2)), alpha);
}
`,at=`layout(std140) uniform pbrProjectionUniforms {
  mat4 modelViewProjectionMatrix;
  mat4 modelMatrix;
  mat4 normalMatrix;
  vec3 camera;
} pbrProjection;
`,_i=`struct pbrProjectionUniforms {
  modelViewProjectionMatrix: mat4x4<f32>,
  modelMatrix: mat4x4<f32>,
  normalMatrix: mat4x4<f32>,
  camera: vec3<f32>
};

@group(0) @binding(auto) var<uniform> pbrProjection: pbrProjectionUniforms;
`,bi={name:"pbrProjection",bindingLayout:[{name:"pbrProjection",group:0}],source:_i,vs:at,fs:at,getUniforms:e=>e,uniformTypes:{modelViewProjectionMatrix:"mat4x4<f32>",modelMatrix:"mat4x4<f32>",normalMatrix:"mat4x4<f32>",camera:"vec3<f32>"}},vi={props:{},uniforms:{},defaultUniforms:{unlit:!1,baseColorMapEnabled:!1,baseColorFactor:[1,1,1,1],normalMapEnabled:!1,normalScale:1,emissiveMapEnabled:!1,emissiveFactor:[0,0,0],metallicRoughnessValues:[1,1],metallicRoughnessMapEnabled:!1,occlusionMapEnabled:!1,occlusionStrength:1,alphaCutoffEnabled:!1,alphaCutoff:.5,IBLenabled:!1,scaleIBLAmbient:[1,1],scaleDiffBaseMR:[0,0,0,0],scaleFGDSpec:[0,0,0,0],specularColorFactor:[1,1,1],specularIntensityFactor:1,specularColorMapEnabled:!1,specularIntensityMapEnabled:!1,ior:1.5,transmissionFactor:0,transmissionMapEnabled:!1,thicknessFactor:0,attenuationDistance:1e9,attenuationColor:[1,1,1],clearcoatFactor:0,clearcoatRoughnessFactor:0,clearcoatMapEnabled:!1,clearcoatRoughnessMapEnabled:!1,sheenColorFactor:[0,0,0],sheenRoughnessFactor:0,sheenColorMapEnabled:!1,sheenRoughnessMapEnabled:!1,iridescenceFactor:0,iridescenceIor:1.3,iridescenceThicknessRange:[100,400],iridescenceMapEnabled:!1,anisotropyStrength:0,anisotropyRotation:0,anisotropyDirection:[1,0],anisotropyMapEnabled:!1,emissiveStrength:1,baseColorUVSet:0,baseColorUVTransform:[1,0,0,0,1,0,0,0,1],metallicRoughnessUVSet:0,metallicRoughnessUVTransform:[1,0,0,0,1,0,0,0,1],normalUVSet:0,normalUVTransform:[1,0,0,0,1,0,0,0,1],occlusionUVSet:0,occlusionUVTransform:[1,0,0,0,1,0,0,0,1],emissiveUVSet:0,emissiveUVTransform:[1,0,0,0,1,0,0,0,1],specularColorUVSet:0,specularColorUVTransform:[1,0,0,0,1,0,0,0,1],specularIntensityUVSet:0,specularIntensityUVTransform:[1,0,0,0,1,0,0,0,1],transmissionUVSet:0,transmissionUVTransform:[1,0,0,0,1,0,0,0,1],thicknessUVSet:0,thicknessUVTransform:[1,0,0,0,1,0,0,0,1],clearcoatUVSet:0,clearcoatUVTransform:[1,0,0,0,1,0,0,0,1],clearcoatRoughnessUVSet:0,clearcoatRoughnessUVTransform:[1,0,0,0,1,0,0,0,1],clearcoatNormalUVSet:0,clearcoatNormalUVTransform:[1,0,0,0,1,0,0,0,1],sheenColorUVSet:0,sheenColorUVTransform:[1,0,0,0,1,0,0,0,1],sheenRoughnessUVSet:0,sheenRoughnessUVTransform:[1,0,0,0,1,0,0,0,1],iridescenceUVSet:0,iridescenceUVTransform:[1,0,0,0,1,0,0,0,1],iridescenceThicknessUVSet:0,iridescenceThicknessUVTransform:[1,0,0,0,1,0,0,0,1],anisotropyUVSet:0,anisotropyUVTransform:[1,0,0,0,1,0,0,0,1]},name:"pbrMaterial",firstBindingSlot:0,bindingLayout:[{name:"pbrMaterial",group:3},{name:"pbr_baseColorSampler",group:3},{name:"pbr_normalSampler",group:3},{name:"pbr_emissiveSampler",group:3},{name:"pbr_metallicRoughnessSampler",group:3},{name:"pbr_occlusionSampler",group:3},{name:"pbr_specularColorSampler",group:3},{name:"pbr_specularIntensitySampler",group:3},{name:"pbr_transmissionSampler",group:3},{name:"pbr_thicknessSampler",group:3},{name:"pbr_clearcoatSampler",group:3},{name:"pbr_clearcoatRoughnessSampler",group:3},{name:"pbr_clearcoatNormalSampler",group:3},{name:"pbr_sheenColorSampler",group:3},{name:"pbr_sheenRoughnessSampler",group:3},{name:"pbr_iridescenceSampler",group:3},{name:"pbr_iridescenceThicknessSampler",group:3},{name:"pbr_anisotropySampler",group:3}],dependencies:[k,Je,bi],source:hi,vs:mi,fs:di,defines:{LIGHTING_FRAGMENT:!0,HAS_NORMALMAP:!1,HAS_EMISSIVEMAP:!1,HAS_OCCLUSIONMAP:!1,HAS_BASECOLORMAP:!1,HAS_METALROUGHNESSMAP:!1,HAS_SPECULARCOLORMAP:!1,HAS_SPECULARINTENSITYMAP:!1,HAS_TRANSMISSIONMAP:!1,HAS_THICKNESSMAP:!1,HAS_CLEARCOATMAP:!1,HAS_CLEARCOATROUGHNESSMAP:!1,HAS_CLEARCOATNORMALMAP:!1,HAS_SHEENCOLORMAP:!1,HAS_SHEENROUGHNESSMAP:!1,HAS_IRIDESCENCEMAP:!1,HAS_IRIDESCENCETHICKNESSMAP:!1,HAS_ANISOTROPYMAP:!1,USE_MATERIAL_EXTENSIONS:!1,ALPHA_CUTOFF:!1,USE_IBL:!1,PBR_DEBUG:!1},getUniforms:e=>e,uniformTypes:{unlit:"i32",baseColorMapEnabled:"i32",baseColorFactor:"vec4<f32>",normalMapEnabled:"i32",normalScale:"f32",emissiveMapEnabled:"i32",emissiveFactor:"vec3<f32>",metallicRoughnessValues:"vec2<f32>",metallicRoughnessMapEnabled:"i32",occlusionMapEnabled:"i32",occlusionStrength:"f32",alphaCutoffEnabled:"i32",alphaCutoff:"f32",specularColorFactor:"vec3<f32>",specularIntensityFactor:"f32",specularColorMapEnabled:"i32",specularIntensityMapEnabled:"i32",ior:"f32",transmissionFactor:"f32",transmissionMapEnabled:"i32",thicknessFactor:"f32",attenuationDistance:"f32",attenuationColor:"vec3<f32>",clearcoatFactor:"f32",clearcoatRoughnessFactor:"f32",clearcoatMapEnabled:"i32",clearcoatRoughnessMapEnabled:"i32",sheenColorFactor:"vec3<f32>",sheenRoughnessFactor:"f32",sheenColorMapEnabled:"i32",sheenRoughnessMapEnabled:"i32",iridescenceFactor:"f32",iridescenceIor:"f32",iridescenceThicknessRange:"vec2<f32>",iridescenceMapEnabled:"i32",anisotropyStrength:"f32",anisotropyRotation:"f32",anisotropyDirection:"vec2<f32>",anisotropyMapEnabled:"i32",emissiveStrength:"f32",IBLenabled:"i32",scaleIBLAmbient:"vec2<f32>",scaleDiffBaseMR:"vec4<f32>",scaleFGDSpec:"vec4<f32>",baseColorUVSet:"i32",baseColorUVTransform:"mat3x3<f32>",metallicRoughnessUVSet:"i32",metallicRoughnessUVTransform:"mat3x3<f32>",normalUVSet:"i32",normalUVTransform:"mat3x3<f32>",occlusionUVSet:"i32",occlusionUVTransform:"mat3x3<f32>",emissiveUVSet:"i32",emissiveUVTransform:"mat3x3<f32>",specularColorUVSet:"i32",specularColorUVTransform:"mat3x3<f32>",specularIntensityUVSet:"i32",specularIntensityUVTransform:"mat3x3<f32>",transmissionUVSet:"i32",transmissionUVTransform:"mat3x3<f32>",thicknessUVSet:"i32",thicknessUVTransform:"mat3x3<f32>",clearcoatUVSet:"i32",clearcoatUVTransform:"mat3x3<f32>",clearcoatRoughnessUVSet:"i32",clearcoatRoughnessUVTransform:"mat3x3<f32>",clearcoatNormalUVSet:"i32",clearcoatNormalUVTransform:"mat3x3<f32>",sheenColorUVSet:"i32",sheenColorUVTransform:"mat3x3<f32>",sheenRoughnessUVSet:"i32",sheenRoughnessUVTransform:"mat3x3<f32>",iridescenceUVSet:"i32",iridescenceUVTransform:"mat3x3<f32>",iridescenceThicknessUVSet:"i32",iridescenceThicknessUVTransform:"mat3x3<f32>",anisotropyUVSet:"i32",anisotropyUVTransform:"mat3x3<f32>"}},lt=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],st=`layout(std140) uniform pbrSceneUniforms {
  float exposure;
  int toneMapMode;
  float environmentIntensity;
  float environmentRotation;
  vec2 framebufferSize;
  mat4 viewMatrix;
  mat4 projectionMatrix;
} pbrScene;

#ifdef USE_TRANSMISSION_FRAMEBUFFER
uniform sampler2D pbr_transmissionFramebufferSampler;
#endif
`,Si=`struct pbrSceneUniforms {
  exposure: f32,
  toneMapMode: i32,
  environmentIntensity: f32,
  environmentRotation: f32,
  framebufferSize: vec2<f32>,
  viewMatrix: mat4x4<f32>,
  projectionMatrix: mat4x4<f32>
};

@group(1) @binding(auto) var<uniform> pbrScene: pbrSceneUniforms;

#ifdef USE_TRANSMISSION_FRAMEBUFFER
@group(1) @binding(auto) var pbr_transmissionFramebufferSampler: texture_2d<f32>;
@group(1) @binding(auto) var pbr_transmissionFramebufferSamplerSampler: sampler;
#endif
`,Li={name:"pbrScene",bindingLayout:[{name:"pbrScene",group:1},{name:"pbr_transmissionFramebufferSampler",group:1}],source:Si,vs:st,fs:st,getUniforms:e=>e,uniformTypes:{exposure:"f32",toneMapMode:"i32",environmentIntensity:"f32",environmentRotation:"f32",framebufferSize:"vec2<f32>",viewMatrix:"mat4x4<f32>",projectionMatrix:"mat4x4<f32>"},defaultUniforms:{exposure:1,toneMapMode:2,environmentIntensity:1,environmentRotation:Math.PI*.5,framebufferSize:[1,1],viewMatrix:lt,projectionMatrix:lt}};export{O as ShaderAssembler,G as _getDependencyGraph,Ct as _resolveModules,Te as assembleGLSLShaderPair,z as capitalize,Y as checkShaderModuleDeprecations,vt as combineInjects,De as convertToVec4,Qe as dirlight,ue as floatColors,Vo as fp32,Do as fp64,se as fp64LowPart,qe as fp64arithmetic,$ as fp64ify,ce as fp64ifyMatrix4,Po as fromHalfFloat,yo as generateShaderForModule,ee as getGLSLUniformBlocks,So as getPassthroughFS,vo as getQualifierDetails,Ee as getShaderInfo,J as getShaderModuleDependencies,ne as getShaderModuleSource,_e as getShaderModuleUniformBlockFields,Q as getShaderModuleUniformBlockName,be as getShaderModuleUniformLayoutValidationResult,St as getShaderModuleUniforms,rt as gouraudMaterial,Je as ibl,Z as initializeShaderModule,y as initializeShaderModules,et as lambertMaterial,k as lighting,pe as normalizeByteColor3,je as normalizeByteColor4,vi as pbrMaterial,Li as pbrScene,nt as phongMaterial,jo as picking,ke as preprocess,Oo as random,fe as resolveUseByteColors,Zo as skin,No as toHalfFloat,Io as typeToChannelCount,Lo as typeToChannelSuffix,ve as validateShaderModuleUniformLayout,Se as warnIfGLSLUniformBlocksAreNotStd140};
//# sourceMappingURL=/sm/2d2d8b5f691e31a4c90b7db509eaf9d9f5cec53dfcad4ed464c3ed7f714f45eb.map