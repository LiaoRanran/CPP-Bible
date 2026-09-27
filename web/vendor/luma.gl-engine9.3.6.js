/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/@luma.gl/engine@9.3.6/dist/index.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
import{luma as $e,Buffer as R,vertexFormatDecoder as jt,log as y,isExternalImage as He,getExternalImageSize as Gt,Texture as C,Sampler as le,RenderPipeline as Ut,PipelineFactory as Xe,ShaderFactory as Ve,UniformStore as fe,normalizeBindingsByGroup as zt,TextureView as We,getAttributeInfosFromLayouts as $t,dataTypeDecoder as Ke,ComputePipeline as Ht}from"./luma.gl-core9.3.6.js";import{Stats as Xt}from"./probe.gl-stats4.1.1.js";import{getShaderModuleDependencies as Vt,ShaderAssembler as Ye,getPassthroughFS as qe,initializeShaderModule as Wt,picking as Kt}from"./luma.gl-shadertools9.3.6.js";import{isNumericArray as Je}from"./math.gl-types4.1.0.js";import{Matrix4 as z,Vector3 as X}from"./math.gl-core4.1.0.js";let Yt=1,qt=1;class Jt{time=0;channels=new Map;animations=new Map;playing=!1;lastEngineTime=-1;constructor(){}addChannel(e){const{delay:t=0,duration:i=Number.POSITIVE_INFINITY,rate:s=1,repeat:r=1}=e,a=Yt++,o={time:0,delay:t,duration:i,rate:s,repeat:r};return this._setChannelTime(o,this.time),this.channels.set(a,o),a}removeChannel(e){this.channels.delete(e);for(const[t,i]of this.animations)i.channel===e&&this.detachAnimation(t)}isFinished(e){const t=this.channels.get(e);return t===void 0?!1:this.time>=t.delay+t.duration*t.repeat}getTime(e){if(e===void 0)return this.time;const t=this.channels.get(e);return t===void 0?-1:t.time}setTime(e){this.time=Math.max(0,e);const t=this.channels.values();for(const s of t)this._setChannelTime(s,this.time);const i=this.animations.values();for(const s of i){const{animation:r,channel:a}=s;r.setTime(this.getTime(a))}}play(){this.playing=!0}pause(){this.playing=!1,this.lastEngineTime=-1}reset(){this.setTime(0)}attachAnimation(e,t){const i=qt++;return this.animations.set(i,{animation:e,channel:t}),e.setTime(this.getTime(t)),i}detachAnimation(e){this.animations.delete(e)}update(e){this.playing&&(this.lastEngineTime===-1&&(this.lastEngineTime=e),this.setTime(this.time+(e-this.lastEngineTime)),this.lastEngineTime=e)}_setChannelTime(e,t){const i=t-e.delay,s=e.duration*e.repeat;i>=s?e.time=e.duration*e.rate:(e.time=Math.max(0,i)%e.duration,e.time*=e.rate)}}class Zt{startIndex=-1;endIndex=-1;factor=0;times=[];values=[];_lastTime=-1;constructor(e){this.setKeyFrames(e),this.setTime(0)}setKeyFrames(e){const t=e.length;this.times.length=t,this.values.length=t;for(let i=0;i<t;++i)this.times[i]=e[i][0],this.values[i]=e[i][1];this._calculateKeys(this._lastTime)}setTime(e){e=Math.max(0,e),e!==this._lastTime&&(this._calculateKeys(e),this._lastTime=e)}getStartTime(){return this.times[this.startIndex]}getEndTime(){return this.times[this.endIndex]}getStartData(){return this.values[this.startIndex]}getEndData(){return this.values[this.endIndex]}_calculateKeys(e){let t=0;const i=this.times.length;for(t=0;t<i-2&&!(this.times[t+1]>e);++t);this.startIndex=t,this.endIndex=t+1;const s=this.times[this.startIndex],r=this.times[this.endIndex];this.factor=Math.min(Math.max(0,(e-s)/(r-s)),1)}}class Qt{constructor(e){}async onInitialize(e){return null}}function Ze(n){const e=typeof window<"u"?window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame:null;return e?e.call(window,n):setTimeout(()=>n(typeof performance<"u"?performance.now():Date.now()),1e3/60)}function Qe(n){const e=typeof window<"u"?window.cancelAnimationFrame||window.webkitCancelAnimationFrame||window.mozCancelAnimationFrame:null;if(e){e.call(window,n);return}clearTimeout(n)}let ei=0;const ti="Animation Loop";class ce{static defaultAnimationLoopProps={device:null,onAddHTML:()=>"",onInitialize:async()=>null,onRender:()=>{},onFinalize:()=>{},onError:e=>console.error(e),stats:void 0,autoResizeViewport:!1};device=null;canvas=null;props;animationProps=null;timeline=null;stats;sharedStats;cpuTime;gpuTime;frameRate;display;_needsRedraw="initialized";_initialized=!1;_running=!1;_animationFrameId=null;_nextFramePromise=null;_resolveNextFrame=null;_cpuStartTime=0;_error=null;_lastFrameTime=0;constructor(e){if(this.props={...ce.defaultAnimationLoopProps,...e},e=this.props,!e.device)throw new Error("No device provided");this.stats=e.stats||new Xt({id:`animation-loop-${ei++}`}),this.sharedStats=$e.stats.get(ti),this.frameRate=this.stats.get("Frame Rate"),this.frameRate.setSampleSize(1),this.cpuTime=this.stats.get("CPU Time"),this.gpuTime=this.stats.get("GPU Time"),this.setProps({autoResizeViewport:e.autoResizeViewport}),this.start=this.start.bind(this),this.stop=this.stop.bind(this),this._onMousemove=this._onMousemove.bind(this),this._onMouseleave=this._onMouseleave.bind(this)}destroy(){this.stop(),this._setDisplay(null),this.device?._disableDebugGPUTime()}delete(){this.destroy()}reportError(e){this.props.onError(e),this._error=e}setNeedsRedraw(e){return this._needsRedraw=this._needsRedraw||e,this}needsRedraw(){const e=this._needsRedraw;return this._needsRedraw=!1,e}setProps(e){return"autoResizeViewport"in e&&(this.props.autoResizeViewport=e.autoResizeViewport||!1),this}async start(){if(this._running)return this;this._running=!0;try{let e;if(!this._initialized){if(this._initialized=!0,await this._initDevice(),this._initialize(),!this._running)return null;await this.props.onInitialize(this._getAnimationProps())}return this._running?(e!==!1&&(this._cancelAnimationFrame(),this._requestAnimationFrame()),this):null}catch(e){const t=e instanceof Error?e:new Error("Unknown error");throw this.props.onError(t),t}}stop(){return this._running&&(this.animationProps&&!this._error&&this.props.onFinalize(this.animationProps),this._cancelAnimationFrame(),this._nextFramePromise=null,this._resolveNextFrame=null,this._running=!1,this._lastFrameTime=0),this}redraw(e){return this.device?.isLost||this._error?this:(this._beginFrameTimers(e),this._setupFrame(),this._updateAnimationProps(),this._renderFrame(this._getAnimationProps()),this._clearNeedsRedraw(),this._resolveNextFrame&&(this._resolveNextFrame(this),this._nextFramePromise=null,this._resolveNextFrame=null),this._endFrameTimers(),this)}attachTimeline(e){return this.timeline=e,this.timeline}detachTimeline(){this.timeline=null}waitForRender(){return this.setNeedsRedraw("waitForRender"),this._nextFramePromise||(this._nextFramePromise=new Promise(e=>{this._resolveNextFrame=e})),this._nextFramePromise}async toDataURL(){if(this.setNeedsRedraw("toDataURL"),await this.waitForRender(),this.canvas instanceof HTMLCanvasElement)return this.canvas.toDataURL();throw new Error("OffscreenCanvas")}_initialize(){this._startEventHandling(),this._initializeAnimationProps(),this._updateAnimationProps(),this._resizeViewport(),this.device?._enableDebugGPUTime()}_setDisplay(e){this.display&&(this.display.destroy(),this.display.animationLoop=null),e&&(e.animationLoop=this),this.display=e}_requestAnimationFrame(){this._running&&(this._animationFrameId=Ze(this._animationFrame.bind(this)))}_cancelAnimationFrame(){this._animationFrameId!==null&&(Qe(this._animationFrameId),this._animationFrameId=null)}_animationFrame(e){this._running&&(this.redraw(e),this._requestAnimationFrame())}_renderFrame(e){if(this.display){this.display._renderFrame(e);return}this.props.onRender(this._getAnimationProps()),this.device?.submit()}_clearNeedsRedraw(){this._needsRedraw=!1}_setupFrame(){this._resizeViewport()}_initializeAnimationProps(){const e=this.device?.getDefaultCanvasContext();if(!this.device||!e)throw new Error("loop");const t=e?.canvas,i=e.props.useDevicePixels;this.animationProps={animationLoop:this,device:this.device,canvasContext:e,canvas:t,useDevicePixels:i,timeline:this.timeline,needsRedraw:!1,width:1,height:1,aspect:1,time:0,startTime:Date.now(),engineTime:0,tick:0,tock:0,_mousePosition:null}}_getAnimationProps(){if(!this.animationProps)throw new Error("animationProps");return this.animationProps}_updateAnimationProps(){if(!this.animationProps)return;const{width:e,height:t,aspect:i}=this._getSizeAndAspect();(e!==this.animationProps.width||t!==this.animationProps.height)&&this.setNeedsRedraw("drawing buffer resized"),i!==this.animationProps.aspect&&this.setNeedsRedraw("drawing buffer aspect changed"),this.animationProps.width=e,this.animationProps.height=t,this.animationProps.aspect=i,this.animationProps.needsRedraw=this._needsRedraw,this.animationProps.engineTime=Date.now()-this.animationProps.startTime,this.timeline&&this.timeline.update(this.animationProps.engineTime),this.animationProps.tick=Math.floor(this.animationProps.time/1e3*60),this.animationProps.tock++,this.animationProps.time=this.timeline?this.timeline.getTime():this.animationProps.engineTime}async _initDevice(){if(this.device=await this.props.device,!this.device)throw new Error("No device provided");this.canvas=this.device.getDefaultCanvasContext().canvas||null}_createInfoDiv(){if(this.canvas&&this.props.onAddHTML){const e=document.createElement("div");document.body.appendChild(e),e.style.position="relative";const t=document.createElement("div");t.style.position="absolute",t.style.left="10px",t.style.bottom="10px",t.style.width="300px",t.style.background="white",this.canvas instanceof HTMLCanvasElement&&e.appendChild(this.canvas),e.appendChild(t);const i=this.props.onAddHTML(t);i&&(t.innerHTML=i)}}_getSizeAndAspect(){if(!this.device)return{width:1,height:1,aspect:1};const[e,t]=this.device.getDefaultCanvasContext().getDrawingBufferSize(),i=e>0&&t>0?e/t:1;return{width:e,height:t,aspect:i}}_resizeViewport(){this.props.autoResizeViewport&&this.device.gl&&this.device.gl.viewport(0,0,this.device.gl.drawingBufferWidth,this.device.gl.drawingBufferHeight)}_beginFrameTimers(e){const t=e??(typeof performance<"u"?performance.now():Date.now());if(this._lastFrameTime){const i=t-this._lastFrameTime;i>0&&this.frameRate.addTime(i)}this._lastFrameTime=t,this.device?._isDebugGPUTimeEnabled()&&this._consumeEncodedGpuTime(),this.cpuTime.timeStart()}_endFrameTimers(){this.device?._isDebugGPUTimeEnabled()&&this._consumeEncodedGpuTime(),this.cpuTime.timeEnd(),this._updateSharedStats()}_consumeEncodedGpuTime(){if(!this.device)return;const e=this.device.commandEncoder._gpuTimeMs;e!==void 0&&(this.gpuTime.addTime(e),this.device.commandEncoder._gpuTimeMs=void 0)}_updateSharedStats(){if(this.stats!==this.sharedStats){for(const e of Object.keys(this.sharedStats.stats))this.stats.stats[e]||delete this.sharedStats.stats[e];this.stats.forEach(e=>{const t=this.sharedStats.get(e.name,e.type);t.sampleSize=e.sampleSize,t.time=e.time,t.count=e.count,t.samples=e.samples,t.lastTiming=e.lastTiming,t.lastSampleTime=e.lastSampleTime,t.lastSampleCount=e.lastSampleCount,t._count=e._count,t._time=e._time,t._samples=e._samples,t._startTime=e._startTime,t._timerPending=e._timerPending})}}_startEventHandling(){this.canvas&&(this.canvas.addEventListener("mousemove",this._onMousemove.bind(this)),this.canvas.addEventListener("mouseleave",this._onMouseleave.bind(this)))}_onMousemove(e){e instanceof MouseEvent&&(this._getAnimationProps()._mousePosition=[e.offsetX,e.offsetY])}_onMouseleave(e){this._getAnimationProps()._mousePosition=null}}function ii(n,e){let t=null;const i=e?.device||$e.createDevice({id:"animation-loop",adapters:e?.adapters,createCanvasContext:!0}),s=new ce({...e,device:i,async onInitialize(r){si(r.animationLoop.device);try{return t=new n(r),await t?.onInitialize(r)}catch(a){return console.error(a),ni(r.animationLoop.device,a),null}},onRender:r=>t?.onRender(r),onFinalize:r=>t?.onFinalize(r)});return s.getInfo=()=>this.AnimationLoopTemplateCtor.info,s}function ni(n,e){if(!n)return;const t=n.getDefaultCanvasContext().canvas;if(t instanceof HTMLCanvasElement){t.style.overflow="visible";let i=document.getElementById("animation-loop-error");i?.remove(),i=document.createElement("h1"),i.id="animation-loop-error",i.innerHTML=e.message,i.style.position="absolute",i.style.top="10px",i.style.left="10px",i.style.color="black",i.style.backgroundColor="red",t.parentElement?.appendChild(i)}}function si(n){if(!n)return;const e=document.getElementById("animation-loop-error");e&&e.remove()}const ge={};function O(n="id"){ge[n]=ge[n]||1;const e=ge[n]++;return`${n}-${e}`}class me{id;userData={};topology;bufferLayout=[];vertexCount;indices;attributes;constructor(e){if(this.id=e.id||O("geometry"),this.topology=e.topology,this.indices=e.indices||null,this.attributes=e.attributes,this.vertexCount=e.vertexCount,this.bufferLayout=e.bufferLayout||[],this.indices&&!(this.indices.usage&R.INDEX))throw new Error("Index buffer must have INDEX usage")}destroy(){this.indices?.destroy();for(const e of Object.values(this.attributes))e.destroy()}getVertexCount(){return this.vertexCount}getAttributes(){return this.attributes}getIndexes(){return this.indices||null}_calculateVertexCount(e){return e.byteLength/12}}function ri(n,e){if(e instanceof me)return e;const t=oi(n,e),{attributes:i,bufferLayout:s}=ai(n,e);return new me({topology:e.topology||"triangle-list",bufferLayout:s,vertexCount:e.vertexCount,indices:t,attributes:i})}function oi(n,e){if(!e.indices)return;const t=e.indices.value;return n.createBuffer({usage:R.INDEX,data:t})}function ai(n,e){const t=[],i={};for(const[r,a]of Object.entries(e.attributes)){let o=r;switch(r){case"POSITION":o="positions";break;case"NORMAL":o="normals";break;case"TEXCOORD_0":o="texCoords";break;case"TEXCOORD_1":o="texCoords1";break;case"COLOR_0":o="colors";break}if(a){i[o]=n.createBuffer({data:a.value,id:`${r}-buffer`});const{value:c,size:u,normalized:d}=a;if(u===void 0)throw new Error(`Attribute ${r} is missing a size`);t.push({name:o,format:jt.getVertexFormatFromAttribute(c,u,d)})}}const s=e._calculateVertexCount(e.attributes,e.indices);return{attributes:i,bufferLayout:t,vertexCount:s}}function ci(n,e){const t={},i="Values";if(n.attributes.length===0&&!n.varyings?.length)return{"No attributes or varyings":{[i]:"N/A"}};for(const s of n.attributes)if(s){const r=`${s.location} ${s.name}: ${s.type}`;t[`in ${r}`]={[i]:s.stepMode||"vertex"}}for(const s of n.varyings||[]){const r=`${s.location} ${s.name}`;t[`out ${r}`]={[i]:JSON.stringify(s)}}return t}const et="__debugFramebufferState",pe=8;function ui(n,e,t){if(n.device.type!=="webgl")return;const i=li(n.device);if(!i.flushing){if(gi(n)){di(n,t,i);return}e&&fi(e)&&e.handle!==null&&(i.queuedFramebuffers.includes(e)||i.queuedFramebuffers.push(e))}}function di(n,e,t){if(t.queuedFramebuffers.length===0)return;const i=n.device,{gl:s}=i,r=s.getParameter(36010),a=s.getParameter(36006),[o,c]=n.device.getDefaultCanvasContext().getDrawingBufferSize();let u=tt(e.top,pe);const d=tt(e.left,pe);t.flushing=!0;try{for(const h of t.queuedFramebuffers){const[f,p,m,l,w]=hi({framebuffer:h,targetWidth:o,targetHeight:c,topPx:u,leftPx:d,minimap:e.minimap});s.bindFramebuffer(36008,h.handle),s.bindFramebuffer(36009,null),s.blitFramebuffer(0,0,h.width,h.height,f,p,m,l,16384,9728),u+=w+pe}}finally{s.bindFramebuffer(36008,r),s.bindFramebuffer(36009,a),t.flushing=!1}}function hi(n){const{framebuffer:e,targetWidth:t,targetHeight:i,topPx:s,leftPx:r}=n,a=Math.max(Math.floor(t/4),1),o=Math.max(Math.floor(i/4),1),c=Math.min(a/e.width,o/e.height),u=Math.max(Math.floor(e.width*c),1),d=Math.max(Math.floor(e.height*c),1),h=r,f=Math.max(i-s-d,0),p=h+u,m=f+d;return[h,f,p,m,d]}function li(n){return n.userData[et]||={flushing:!1,queuedFramebuffers:[]},n.userData[et]}function fi(n){return"colorAttachments"in n}function gi(n){const e=n.props.framebuffer;return!e||e.handle===null}function tt(n,e){if(!n)return e;const t=Number.parseInt(n,10);return Number.isFinite(t)?t:e}function be(n,e,t){if(n===e)return!0;if(!t||!n||!e)return!1;if(Array.isArray(n)){if(!Array.isArray(e)||n.length!==e.length)return!1;for(let i=0;i<n.length;i++)if(!be(n[i],e[i],t-1))return!1;return!0}if(Array.isArray(e))return!1;if(typeof n=="object"&&typeof e=="object"){const i=Object.keys(n),s=Object.keys(e);if(i.length!==s.length)return!1;for(const r of i)if(!e.hasOwnProperty(r)||!be(n[r],e[r],t-1))return!1;return!0}return!1}class xe{bufferLayouts;constructor(e){this.bufferLayouts=e}getBufferLayout(e){return this.bufferLayouts.find(t=>t.name===e)||null}getAttributeNamesForBuffer(e){return e.attributes?e.attributes?.map(t=>t.attribute):[e.name]}mergeBufferLayouts(e,t){const i=[...e];for(const s of t){const r=i.findIndex(a=>a.name===s.name);r<0?i.push(s):i[r]=s}return i}getBufferIndex(e){const t=this.bufferLayouts.findIndex(i=>i.name===e);return t===-1&&y.warn(`BufferLayout: Missing buffer for "${e}".`)(),t}}function it(n,e){let t=1/0;for(const i of n){const s=e[i];s!==void 0&&(t=Math.min(t,s))}return t}function mi(n,e){const t=Object.fromEntries(n.attributes.map(s=>[s.name,s.location])),i=e.slice();return i.sort((s,r)=>{const a=s.attributes?s.attributes.map(d=>d.attribute):[s.name],o=r.attributes?r.attributes.map(d=>d.attribute):[r.name],c=it(a,t),u=it(o,t);return c-u}),i}function ne(n,e){if(!n||!e.some(i=>i.bindingLayout?.length))return n;const t={...n,bindings:n.bindings.map(i=>({...i}))};"attributes"in(n||{})&&(t.attributes=n?.attributes||[]);for(const i of e)for(const s of i.bindingLayout||[])for(const r of pi(s.name)){const a=t.bindings.find(o=>o.name===r);a?.group===0&&(a.group=s.group)}return t}function ye(n){return!!(n.uniformTypes&&!bi(n.uniformTypes))}function pi(n){const e=new Set([n,`${n}Uniforms`]);return n.endsWith("Uniforms")||e.add(`${n}Sampler`),[...e]}function bi(n){for(const e in n)return!1;return!0}function xi(n){return Je(n)||typeof n=="number"||typeof n=="boolean"}function yi(n,e={}){const t={bindings:{},uniforms:{}};return Object.keys(n).forEach(i=>{const s=n[i];Object.prototype.hasOwnProperty.call(e,i)||xi(s)?t.uniforms[i]=s:t.bindings[i]=s}),t}class V{options={disableWarnings:!1};modules;moduleUniforms;moduleBindings;constructor(e,t){Object.assign(this.options,t);const i=Vt(Object.values(e).filter(_i));for(const s of i)e[s.name]=s;y.log(1,"Creating ShaderInputs with modules",Object.keys(e))(),this.modules=e,this.moduleUniforms={},this.moduleBindings={};for(const[s,r]of Object.entries(e))r&&(this._addModule(r),r.name&&s!==r.name&&!this.options.disableWarnings&&y.warn(`Module name: ${s} vs ${r.name}`)())}destroy(){}setProps(e){for(const t of Object.keys(e)){const i=t,s=e[i]||{},r=this.modules[i];if(!r)this.options.disableWarnings||y.warn(`Module ${t} not found`)();else{const a=this.moduleUniforms[i],o=this.moduleBindings[i],c=r.getUniforms?.(s,a)||s,{uniforms:u,bindings:d}=yi(c,r.uniformTypes);this.moduleUniforms[i]=nt(a,u,r.uniformTypes),this.moduleBindings[i]={...o,...d}}}}getModules(){return Object.values(this.modules)}getUniformValues(){return this.moduleUniforms}getBindingValues(){const e={};for(const t of Object.values(this.moduleBindings))Object.assign(e,t);return e}getDebugTable(){const e={};for(const[t,i]of Object.entries(this.moduleUniforms))for(const[s,r]of Object.entries(i))e[`${t}.${s}`]={type:this.modules[t].uniformTypes?.[s],value:String(r)};return e}_addModule(e){const t=e.name;this.moduleUniforms[t]=nt({},e.defaultUniforms||{},e.uniformTypes),this.moduleBindings[t]={}}}function nt(n={},e={},t={}){const i={...n};for(const[s,r]of Object.entries(e))r!==void 0&&(i[s]=_e(n[s],r,t[s]));return i}function _e(n,e,t){if(!t||typeof t=="string")return Y(e);if(Array.isArray(t)){if(ve(e)||!Array.isArray(e))return Y(e);const a=Array.isArray(n)&&!ve(n)?[...n]:[],o=a.slice();for(let c=0;c<e.length;c++){const u=e[c];u!==void 0&&(o[c]=_e(a[c],u,t[0]))}return o}if(!Ie(e))return Y(e);const i=t,s=Ie(n)?n:{},r={...s};for(const[a,o]of Object.entries(e))o!==void 0&&(r[a]=_e(s[a],o,i[a]));return r}function Y(n){return ArrayBuffer.isView(n)?Array.prototype.slice.call(n):Array.isArray(n)?ve(n)?n.slice():n.map(t=>t===void 0?void 0:Y(t)):Ie(n)?Object.fromEntries(Object.entries(n).map(([e,t])=>[e,t===void 0?void 0:Y(t)])):n}function ve(n){return ArrayBuffer.isView(n)||Array.isArray(n)&&(n.length===0||typeof n[0]=="number")}function Ie(n){return!!n&&typeof n=="object"&&!Array.isArray(n)&&!ArrayBuffer.isView(n)}function _i(n){return!!n?.dependencies}const st={"+X":0,"-X":1,"+Y":2,"-Y":3,"+Z":4,"-Z":5};function q(n){return n?Array.isArray(n)?n[0]??null:n:null}function vi(n){const{dimension:e,data:t}=n;if(!t)return null;switch(e){case"1d":{const i=q(t);if(!i)return null;const{width:s}=J(i);return{width:s,height:1}}case"2d":{const i=q(t);return i?J(i):null}case"3d":case"2d-array":{if(!Array.isArray(t)||t.length===0)return null;const i=q(t[0]);return i?J(i):null}case"cube":{const i=Object.keys(t)[0]??null;if(!i)return null;const s=t[i],r=q(s);return r?J(r):null}case"cube-array":{if(!Array.isArray(t)||t.length===0)return null;const i=t[0],s=Object.keys(i)[0]??null;if(!s)return null;const r=q(i[s]);return r?J(r):null}default:return null}}function J(n){if(He(n))return Gt(n);if(typeof n=="object"&&"width"in n&&"height"in n)return{width:n.width,height:n.height};throw new Error("Unsupported mip-level data")}function Ii(n){return typeof n=="object"&&n!==null&&"data"in n&&"width"in n&&"height"in n}function wi(n){return ArrayBuffer.isView(n)}function rt(n){const{textureFormat:e,format:t}=n;if(e&&t&&e!==t)throw new Error(`Conflicting texture formats "${e}" and "${t}" provided for the same mip level`);return e??t}function ot(n){const e=st[n];if(e===void 0)throw new Error(`Invalid cube face: ${n}`);return e}function Ci(n,e){return 6*n+ot(e)}function at(n){throw new Error("setTexture1DData not supported in WebGL.")}function Ai(n){return Array.isArray(n)?n:[n]}function K(n,e,t,i){const s=Ai(e),r=n,a=[];for(let o=0;o<s.length;o++){const c=s[o];if(He(c))a.push({type:"external-image",image:c,z:r,mipLevel:o});else if(Ii(c))a.push({type:"texture-data",data:c,textureFormat:rt(c),z:r,mipLevel:o});else if(wi(c)&&t)a.push({type:"texture-data",data:{data:c,width:Math.max(1,t.width>>o),height:Math.max(1,t.height>>o),...i?{format:i}:{}},textureFormat:i,z:r,mipLevel:o});else throw new Error("Unsupported 2D mip-level payload")}return a}function ct(n){const e=[];for(let t=0;t<n.length;t++)e.push(...K(t,n[t]));return e}function ut(n){const e=[];for(let t=0;t<n.length;t++)e.push(...K(t,n[t]));return e}function dt(n){const e=[];for(const[t,i]of Object.entries(n)){const s=ot(t);e.push(...K(s,i))}return e}function ht(n){const e=[];return n.forEach((t,i)=>{for(const[s,r]of Object.entries(t)){const a=Ci(i,s);e.push(...K(a,r))}}),e}class j{device;id;props;_texture=null;_sampler=null;_view=null;ready;isReady=!1;destroyed=!1;resolveReady=()=>{};rejectReady=()=>{};get texture(){if(!this._texture)throw new Error("Texture not initialized yet");return this._texture}get sampler(){if(!this._sampler)throw new Error("Sampler not initialized yet");return this._sampler}get view(){if(!this._view)throw new Error("View not initialized yet");return this._view}get[Symbol.toStringTag](){return"DynamicTexture"}toString(){const e=this._texture?.width??this.props.width??"?",t=this._texture?.height??this.props.height??"?";return`DynamicTexture:"${this.id}":${e}x${t}px:(${this.isReady?"ready":"loading..."})`}constructor(e,t){this.device=e;const i=O("dynamic-texture"),s=t;this.props={...j.defaultProps,id:i,...t,data:null},this.id=this.props.id,this.ready=new Promise((r,a)=>{this.resolveReady=r,this.rejectReady=a}),this.initAsync(s)}async initAsync(e){try{const t=await this._loadAllData(e);this._checkNotDestroyed();const i=t.data?Ti({...t,width:e.width,height:e.height,format:e.format}):[],s="format"in e&&e.format!==void 0,r="usage"in e&&e.usage!==void 0,o=(()=>{if(this.props.width&&this.props.height)return{width:this.props.width,height:this.props.height};const l=vi(t);return l||{width:this.props.width||1,height:this.props.height||1}})();if(!o||o.width<=0||o.height<=0)throw new Error(`${this} size could not be determined or was zero`);const c=Pi(this.device,i,o,{format:s?e.format:void 0}),u=c.format??this.props.format,d={...this.props,...o,format:u,mipLevels:1,data:void 0};this.device.isTextureFormatCompressed(u)&&!r&&(d.usage=C.SAMPLE|C.COPY_DST);const h=this.props.mipmaps&&!c.hasExplicitMipChain&&!this.device.isTextureFormatCompressed(u);if(this.device.type==="webgpu"&&h){const l=this.props.dimension==="3d"?C.SAMPLE|C.STORAGE|C.COPY_DST|C.COPY_SRC:C.SAMPLE|C.RENDER|C.COPY_DST|C.COPY_SRC;d.usage|=l}const f=this.device.getMipLevelCount(d.width,d.height),p=c.hasExplicitMipChain?c.mipLevels:this.props.mipLevels==="auto"?f:Math.max(1,Math.min(f,this.props.mipLevels??1)),m={...d,mipLevels:p};this._texture=this.device.createTexture(m),this._sampler=this.texture.sampler,this._view=this.texture.view,c.subresources.length&&this._setTextureSubresources(c.subresources),this.props.mipmaps&&!c.hasExplicitMipChain&&!h&&y.warn(`${this} skipping auto-generated mipmaps for compressed texture format`)(),h&&this.generateMipmaps(),this.isReady=!0,this.resolveReady(this.texture),y.info(0,`${this} created`)()}catch(t){const i=t instanceof Error?t:new Error(String(t));this.rejectReady(i)}}destroy(){this._texture&&(this._texture.destroy(),this._texture=null,this._sampler=null,this._view=null),this.destroyed=!0}generateMipmaps(){this.device.type==="webgl"?this.texture.generateMipmapsWebGL():this.device.type==="webgpu"?this.device.generateMipmapsWebGPU(this.texture):y.warn(`${this} mipmaps not supported on ${this.device.type}`)}setSampler(e={}){this._checkReady();const t=e instanceof le?e:this.device.createSampler(e);this.texture.setSampler(t),this._sampler=t}async readBuffer(e={}){this.isReady||await this.ready;const t=e.width??this.texture.width,i=e.height??this.texture.height,s=e.depthOrArrayLayers??this.texture.depth,r=this.texture.computeMemoryLayout({width:t,height:i,depthOrArrayLayers:s}),a=this.device.createBuffer({byteLength:r.byteLength,usage:R.COPY_DST|R.MAP_READ});this.texture.readBuffer({...e,width:t,height:i,depthOrArrayLayers:s},a);const o=this.device.createFence();return await o.signaled,o.destroy(),a}async readAsync(e={}){this.isReady||await this.ready;const t=e.width??this.texture.width,i=e.height??this.texture.height,s=e.depthOrArrayLayers??this.texture.depth,r=this.texture.computeMemoryLayout({width:t,height:i,depthOrArrayLayers:s}),a=await this.readBuffer(e),o=await a.readAsync(0,r.byteLength);return a.destroy(),o.buffer}resize(e){if(this._checkReady(),e.width===this.texture.width&&e.height===this.texture.height)return!1;const t=this.texture;return this._texture=t.clone(e),this._sampler=this.texture.sampler,this._view=this.texture.view,t.destroy(),y.info(`${this} resized`),!0}getCubeFaceIndex(e){const t=st[e];if(t===void 0)throw new Error(`Invalid cube face: ${e}`);return t}getCubeArrayFaceIndex(e,t){return 6*e+this.getCubeFaceIndex(t)}setTexture1DData(e){if(this._checkReady(),this.texture.props.dimension!=="1d")throw new Error(`${this} is not 1d`);const t=at();this._setTextureSubresources(t)}setTexture2DData(e,t=0){if(this._checkReady(),this.texture.props.dimension!=="2d")throw new Error(`${this} is not 2d`);const i=K(t,e);this._setTextureSubresources(i)}setTexture3DData(e){if(this.texture.props.dimension!=="3d")throw new Error(`${this} is not 3d`);const t=ct(e);this._setTextureSubresources(t)}setTextureArrayData(e){if(this.texture.props.dimension!=="2d-array")throw new Error(`${this} is not 2d-array`);const t=ut(e);this._setTextureSubresources(t)}setTextureCubeData(e){if(this.texture.props.dimension!=="cube")throw new Error(`${this} is not cube`);const t=dt(e);this._setTextureSubresources(t)}setTextureCubeArrayData(e){if(this.texture.props.dimension!=="cube-array")throw new Error(`${this} is not cube-array`);const t=ht(e);this._setTextureSubresources(t)}_setTextureSubresources(e){for(const t of e){const{z:i,mipLevel:s}=t;switch(t.type){case"external-image":const{image:r,flipY:a}=t;this.texture.copyExternalImage({image:r,z:i,mipLevel:s,flipY:a});break;case"texture-data":const{data:o,textureFormat:c}=t;if(c&&c!==this.texture.format)throw new Error(`${this} mip level ${s} uses format "${c}" but texture format is "${this.texture.format}"`);this.texture.writeData(o.data,{x:0,y:0,z:i,width:o.width,height:o.height,depthOrArrayLayers:1,mipLevel:s});break;default:throw new Error("Unsupported 2D mip-level payload")}}}async _loadAllData(e){const t=await we(e.data);return{dimension:e.dimension??"2d",data:t??null}}_checkNotDestroyed(){this.destroyed&&y.warn(`${this} already destroyed`)}_checkReady(){this.isReady||y.warn(`${this} Cannot perform this operation before ready`)}static defaultProps={...C.defaultProps,dimension:"2d",data:null,mipmaps:!1}}function Ti(n){if(!n.data)return[];const e=n.width&&n.height?{width:n.width,height:n.height}:void 0,t="format"in n?n.format:void 0;switch(n.dimension){case"1d":return at();case"2d":return K(0,n.data,e,t);case"3d":return ct(n.data);case"2d-array":return ut(n.data);case"cube":return dt(n.data);case"cube-array":return ht(n.data);default:throw new Error(`Unhandled dimension ${n.dimension}`)}}function Pi(n,e,t,i){if(e.length===0)return{subresources:e,mipLevels:1,format:i.format,hasExplicitMipChain:!1};const s=new Map;for(const d of e){const h=s.get(d.z)??[];h.push(d),s.set(d.z,h)}const r=e.some(d=>d.mipLevel>0);let a=i.format,o=Number.POSITIVE_INFINITY;const c=[];for(const[d,h]of s){const f=[...h].sort((b,g)=>b.mipLevel-g.mipLevel),p=f[0];if(!p||p.mipLevel!==0)throw new Error(`DynamicTexture: slice ${d} is missing mip level 0`);const m=ft(n,p);if(m.width!==t.width||m.height!==t.height)throw new Error(`DynamicTexture: slice ${d} base level dimensions ${m.width}x${m.height} do not match expected ${t.width}x${t.height}`);const l=lt(p);if(l){if(a&&a!==l)throw new Error(`DynamicTexture: slice ${d} base level format "${l}" does not match texture format "${a}"`);a=l}const w=a&&n.isTextureFormatCompressed(a)?Li(n,m.width,m.height,a):n.getMipLevelCount(m.width,m.height);let _=0;for(let b=0;b<f.length;b++){const g=f[b];if(!g||g.mipLevel!==b||b>=w)break;const x=ft(n,g),v=Math.max(1,m.width>>b),A=Math.max(1,m.height>>b);if(x.width!==v||x.height!==A)break;const P=lt(g);if(P&&(a||(a=P),P!==a))break;_++,c.push(g)}o=Math.min(o,_)}const u=Number.isFinite(o)?Math.max(1,o):1;return{subresources:c.filter(d=>d.mipLevel<u),mipLevels:u,format:a,hasExplicitMipChain:r}}function lt(n){if(n.type==="texture-data")return n.textureFormat??rt(n.data)}function ft(n,e){switch(e.type){case"external-image":return n.getExternalImageSize(e.image);case"texture-data":return{width:e.data.width,height:e.data.height};default:throw new Error("Unsupported texture subresource")}}function Li(n,e,t,i){const{blockWidth:s=1,blockHeight:r=1}=n.getTextureFormatInfo(i);let a=1;for(let o=1;;o++){const c=Math.max(1,e>>o),u=Math.max(1,t>>o);if(c<s||u<r)break;a++}return a}async function we(n){if(n=await n,Array.isArray(n))return await Promise.all(n.map(we));if(n&&typeof n=="object"&&n.constructor===Object){const e=n,t=await Promise.all(Object.values(e).map(we)),i=Object.keys(e),s={};for(let r=0;r<i.length;r++)s[i[r]]=t[r];return s}return n}const $=2,Mi=1e4,gt="render pipeline initialization failed";class H{static defaultProps={...Ut.defaultProps,source:void 0,vs:null,fs:null,id:"unnamed",handle:void 0,userData:{},defines:{},modules:[],geometry:null,indexBuffer:null,attributes:{},constantAttributes:{},bindings:{},uniforms:{},varyings:[],isInstanced:void 0,instanceCount:0,vertexCount:0,shaderInputs:void 0,material:void 0,pipelineFactory:void 0,shaderFactory:void 0,transformFeedback:void 0,shaderAssembler:Ye.getDefaultShaderAssembler(),debugShaders:void 0,disableWarnings:void 0};device;id;source;vs;fs;pipelineFactory;shaderFactory;userData={};parameters;topology;bufferLayout;isInstanced=void 0;instanceCount=0;vertexCount;indexBuffer=null;bufferAttributes={};constantAttributes={};bindings={};vertexArray;transformFeedback=null;pipeline;shaderInputs;material=null;_uniformStore;_attributeInfos={};_gpuGeometry=null;props;_pipelineNeedsUpdate="newly created";_needsRedraw="initializing";_destroyed=!1;_lastDrawTimestamp=-1;_bindingTable=[];get[Symbol.toStringTag](){return"Model"}toString(){return`Model(${this.id})`}constructor(e,t){this.props={...H.defaultProps,...t},t=this.props,this.id=t.id||O("model"),this.device=e,Object.assign(this.userData,t.userData),this.material=t.material||null;const i=Object.fromEntries(this.props.modules?.map(c=>[c.name,c])||[]),s=t.shaderInputs||new V(i,{disableWarnings:this.props.disableWarnings});this.setShaderInputs(s);const r=Si(e),a=(this.props.modules?.length>0?this.props.modules:this.shaderInputs?.getModules())||[];if(this.props.shaderLayout=ne(this.props.shaderLayout,a)||null,this.device.type==="webgpu"&&this.props.source){const{source:c,getUniforms:u,bindingTable:d}=this.props.shaderAssembler.assembleWGSLShader({platformInfo:r,...this.props,modules:a});this.source=c,this._getModuleUniforms=u,this._bindingTable=d;const h=e.getShaderLayout?.(this.source);this.props.shaderLayout=ne(this.props.shaderLayout||h||null,a)||null}else{const{vs:c,fs:u,getUniforms:d}=this.props.shaderAssembler.assembleGLSLShaderPair({platformInfo:r,...this.props,modules:a});this.vs=c,this.fs=u,this._getModuleUniforms=d,this._bindingTable=[]}this.vertexCount=this.props.vertexCount,this.instanceCount=this.props.instanceCount,this.topology=this.props.topology,this.bufferLayout=this.props.bufferLayout,this.parameters=this.props.parameters,t.geometry&&this.setGeometry(t.geometry),this.pipelineFactory=t.pipelineFactory||Xe.getDefaultPipelineFactory(this.device),this.shaderFactory=t.shaderFactory||Ve.getDefaultShaderFactory(this.device),this.pipeline=this._updatePipeline(),this.vertexArray=e.createVertexArray({shaderLayout:this.pipeline.shaderLayout,bufferLayout:this.pipeline.bufferLayout}),this._gpuGeometry&&this._setGeometryAttributes(this._gpuGeometry),"isInstanced"in t&&(this.isInstanced=t.isInstanced),t.instanceCount&&this.setInstanceCount(t.instanceCount),t.vertexCount&&this.setVertexCount(t.vertexCount),t.indexBuffer&&this.setIndexBuffer(t.indexBuffer),t.attributes&&this.setAttributes(t.attributes),t.constantAttributes&&this.setConstantAttributes(t.constantAttributes),t.bindings&&this.setBindings(t.bindings),t.transformFeedback&&(this.transformFeedback=t.transformFeedback)}destroy(){this._destroyed||(this.pipelineFactory.release(this.pipeline),this.shaderFactory.release(this.pipeline.vs),this.pipeline.fs&&this.pipeline.fs!==this.pipeline.vs&&this.shaderFactory.release(this.pipeline.fs),this._uniformStore.destroy(),this._gpuGeometry?.destroy(),this._destroyed=!0)}needsRedraw(){this._getBindingsUpdateTimestamp()>this._lastDrawTimestamp&&this.setNeedsRedraw("contents of bound textures or buffers updated");const e=this._needsRedraw;return this._needsRedraw=!1,e}setNeedsRedraw(e){this._needsRedraw||=e}getBindingDebugTable(){return this._bindingTable}predraw(){this.updateShaderInputs(),this.pipeline=this._updatePipeline()}draw(e){const t=this._areBindingsLoading();if(t)return y.info($,`>>> DRAWING ABORTED ${this.id}: ${t} not loaded`)(),!1;try{e.pushDebugGroup(`${this}.predraw(${e})`),this.predraw()}finally{e.popDebugGroup()}let i,s=this.pipeline.isErrored;try{if(e.pushDebugGroup(`${this}.draw(${e})`),this._logDrawCallStart(),this.pipeline=this._updatePipeline(),s=this.pipeline.isErrored,s)y.info($,`>>> DRAWING ABORTED ${this.id}: ${gt}`)(),i=!1;else{const r=this._getBindings(),a=this._getBindGroups(),{indexBuffer:o}=this.vertexArray,c=o?o.byteLength/(o.indexType==="uint32"?4:2):void 0;i=this.pipeline.draw({renderPass:e,vertexArray:this.vertexArray,isInstanced:this.isInstanced,vertexCount:this.vertexCount,instanceCount:this.instanceCount,indexCount:c,transformFeedback:this.transformFeedback||void 0,bindings:r,bindGroups:a,_bindGroupCacheKeys:this._getBindGroupCacheKeys(),uniforms:this.props.uniforms,parameters:this.parameters,topology:this.topology})}}finally{e.popDebugGroup(),this._logDrawCallEnd()}return this._logFramebuffer(e),i?(this._lastDrawTimestamp=this.device.timestamp,this._needsRedraw=!1):s?this._needsRedraw=gt:this._needsRedraw="waiting for resource initialization",i}setGeometry(e){this._gpuGeometry?.destroy();const t=e&&ri(this.device,e);if(t){this.setTopology(t.topology||"triangle-list");const i=new xe(this.bufferLayout);this.bufferLayout=i.mergeBufferLayouts(t.bufferLayout,this.bufferLayout),this.vertexArray&&this._setGeometryAttributes(t)}this._gpuGeometry=t}setTopology(e){e!==this.topology&&(this.topology=e,this._setPipelineNeedsUpdate("topology"))}setBufferLayout(e){const t=new xe(this.bufferLayout);this.bufferLayout=this._gpuGeometry?t.mergeBufferLayouts(e,this._gpuGeometry.bufferLayout):e,this._setPipelineNeedsUpdate("bufferLayout"),this.pipeline=this._updatePipeline(),this.vertexArray=this.device.createVertexArray({shaderLayout:this.pipeline.shaderLayout,bufferLayout:this.pipeline.bufferLayout}),this._gpuGeometry&&this._setGeometryAttributes(this._gpuGeometry)}setParameters(e){be(e,this.parameters,2)||(this.parameters=e,this._setPipelineNeedsUpdate("parameters"))}setInstanceCount(e){this.instanceCount=e,this.isInstanced===void 0&&e>0&&(this.isInstanced=!0),this.setNeedsRedraw("instanceCount")}setVertexCount(e){this.vertexCount=e,this.setNeedsRedraw("vertexCount")}setShaderInputs(e){this.shaderInputs=e,this._uniformStore=new fe(this.device,this.shaderInputs.modules);for(const[t,i]of Object.entries(this.shaderInputs.modules))if(ye(i)&&!this.material?.ownsModule(t)){const s=this._uniformStore.getManagedUniformBuffer(t);this.bindings[`${t}Uniforms`]=s}this.setNeedsRedraw("shaderInputs")}setMaterial(e){this.material=e,this.setNeedsRedraw("material")}updateShaderInputs(){this._uniformStore.setUniforms(this.shaderInputs.getUniformValues()),this.setBindings(this._getNonMaterialBindings(this.shaderInputs.getBindingValues())),this.setNeedsRedraw("shaderInputs")}setBindings(e){Object.assign(this.bindings,e),this.setNeedsRedraw("bindings")}setTransformFeedback(e){this.transformFeedback=e,this.setNeedsRedraw("transformFeedback")}setIndexBuffer(e){this.vertexArray.setIndexBuffer(e),this.setNeedsRedraw("indexBuffer")}setAttributes(e,t){const i=t?.disableWarnings??this.props.disableWarnings;e.indices&&y.warn(`Model:${this.id} setAttributes() - indexBuffer should be set using setIndexBuffer()`)(),this.bufferLayout=mi(this.pipeline.shaderLayout,this.bufferLayout);const s=new xe(this.bufferLayout);for(const[r,a]of Object.entries(e)){const o=s.getBufferLayout(r);if(!o){i||y.warn(`Model(${this.id}): Missing layout for buffer "${r}".`)();continue}const c=s.getAttributeNamesForBuffer(o);let u=!1;for(const d of c){const h=this._attributeInfos[d];if(h){const f=this.device.type==="webgpu"?s.getBufferIndex(h.bufferName):h.location;this.vertexArray.setBuffer(f,a),u=!0}}!u&&!i&&y.warn(`Model(${this.id}): Ignoring buffer "${a.id}" for unknown attribute "${r}"`)()}this.setNeedsRedraw("attributes")}setConstantAttributes(e,t){for(const[i,s]of Object.entries(e)){const r=this._attributeInfos[i];r?this.vertexArray.setConstantWebGL(r.location,s):(t?.disableWarnings??this.props.disableWarnings)||y.warn(`Model "${this.id}: Ignoring constant supplied for unknown attribute "${i}"`)()}this.setNeedsRedraw("constants")}_areBindingsLoading(){for(const e of Object.values(this.bindings))if(e instanceof j&&!e.isReady)return e.id;for(const e of Object.values(this.material?.bindings||{}))if(e instanceof j&&!e.isReady)return e.id;return!1}_getBindings(){const e={};for(const[t,i]of Object.entries(this.bindings))i instanceof j?i.isReady&&(e[t]=i.texture):e[t]=i;return e}_getBindGroups(){const e=this.pipeline?.shaderLayout||this.props.shaderLayout||{bindings:[]},t=e.bindings.length?zt(e,this._getBindings()):{0:this._getBindings()};if(!this.material)return t;for(const[i,s]of Object.entries(this.material.getBindingsByGroup())){const r=Number(i);t[r]={...t[r]||{},...s}}return t}_getBindGroupCacheKeys(){const e=this.material?.getBindGroupCacheKey(3);return e?{3:e}:{}}_getBindingsUpdateTimestamp(){let e=0;for(const t of Object.values(this.bindings))t instanceof We?e=Math.max(e,t.texture.updateTimestamp):t instanceof R||t instanceof C?e=Math.max(e,t.updateTimestamp):t instanceof j?e=t.texture?Math.max(e,t.texture.updateTimestamp):1/0:t instanceof le||(e=Math.max(e,t.buffer.updateTimestamp));return Math.max(e,this.material?.getBindingsUpdateTimestamp()||0)}_setGeometryAttributes(e){const t={...e.attributes};for(const[i]of Object.entries(t))!this.pipeline.shaderLayout.attributes.find(s=>s.name===i)&&i!=="positions"&&delete t[i];this.vertexCount=e.vertexCount,this.setIndexBuffer(e.indices||null),this.setAttributes(e.attributes,{disableWarnings:!0}),this.setAttributes(t,{disableWarnings:this.props.disableWarnings}),this.setNeedsRedraw("geometry attributes")}_setPipelineNeedsUpdate(e){this._pipelineNeedsUpdate||=e,this.setNeedsRedraw(e)}_updatePipeline(){if(this._pipelineNeedsUpdate){let e=null,t=null;this.pipeline&&(y.log(1,`Model ${this.id}: Recreating pipeline because "${this._pipelineNeedsUpdate}".`)(),e=this.pipeline.vs,t=this.pipeline.fs),this._pipelineNeedsUpdate=!1;const i=this.shaderFactory.createShader({id:`${this.id}-vertex`,stage:"vertex",source:this.source||this.vs,debugShaders:this.props.debugShaders});let s=null;this.source?s=i:this.fs&&(s=this.shaderFactory.createShader({id:`${this.id}-fragment`,stage:"fragment",source:this.source||this.fs,debugShaders:this.props.debugShaders})),this.pipeline=this.pipelineFactory.createRenderPipeline({...this.props,bindings:void 0,bufferLayout:this.bufferLayout,topology:this.topology,parameters:this.parameters,bindGroups:this._getBindGroups(),vs:i,fs:s}),this._attributeInfos=$t(this.pipeline.shaderLayout,this.bufferLayout),e&&this.shaderFactory.release(e),t&&t!==e&&this.shaderFactory.release(t)}return this.pipeline}_lastLogTime=0;_logOpen=!1;_logDrawCallStart(){const e=y.level>3?0:Mi;y.level<2||Date.now()-this._lastLogTime<e||(this._lastLogTime=Date.now(),this._logOpen=!0,y.group($,`>>> DRAWING MODEL ${this.id}`,{collapsed:y.level<=2})())}_logDrawCallEnd(){if(this._logOpen){const e=ci(this.pipeline.shaderLayout,this.id);y.table($,e)();const t=this.shaderInputs.getDebugTable();y.table($,t)();const i=this._getAttributeDebugTable();y.table($,this._attributeInfos)(),y.table($,i)(),y.groupEnd($)(),this._logOpen=!1}}_drawCount=0;_logFramebuffer(e){const t=this.device.props.debugFramebuffers;if(this._drawCount++,!t)return;const i=e.props.framebuffer;ui(e,i,{id:i?.id||`${this.id}-framebuffer`,minimap:!0})}_getAttributeDebugTable(){const e={};for(const[t,i]of Object.entries(this._attributeInfos)){const s=this.vertexArray.attributes[i.location];e[i.location]={name:t,type:i.shaderType,values:s?this._getBufferOrConstantValues(s,i.bufferDataType):"null"}}if(this.vertexArray.indexBuffer){const{indexBuffer:t}=this.vertexArray,i=t.indexType==="uint32"?new Uint32Array(t.debugData):new Uint16Array(t.debugData);e.indices={name:"indices",type:t.indexType,values:i.toString()}}return e}_getBufferOrConstantValues(e,t){const i=Ke.getTypedArrayConstructor(t);return(e instanceof R?new i(e.debugData):e).toString()}_getNonMaterialBindings(e){if(!this.material)return e;const t={};for(const[i,s]of Object.entries(e))this.material.ownsBinding(i)||(t[i]=s);return t}}function Si(n){return{type:n.type,shaderLanguage:n.info.shadingLanguage,shaderLanguageVersion:n.info.shadingLanguageVersion,gpu:n.info.gpu,features:n.features}}const se=3;class mt{device;modules;_materialBindingNames;_materialModuleNames;constructor(e,t={}){this.device=e,this.modules=t.modules||[];const i=new V(Object.fromEntries(this.modules.map(s=>[s.name,s])));this._materialBindingNames=Oi(i),this._materialModuleNames=ki(i)}createMaterial(e={}){return new bt(this.device,{...e,factory:this})}getBindingNames(){return Array.from(this._materialBindingNames)}ownsBinding(e){if(this._materialBindingNames.has(e))return!0;const t=pt(e);return t?this._materialModuleNames.has(t):!1}ownsModule(e){return this._materialModuleNames.has(e)}getBindingsByGroup(e){return Object.keys(e).length>0?{[se]:e}:{}}}function pt(n){return n.endsWith("Uniforms")?n.slice(0,-8):null}function Oi(n){const e=new Set;for(const t of Object.values(n.modules))for(const i of t.bindingLayout||[])i.group===se&&e.add(i.name);return e}function ki(n){const e=new Set;for(const t of Object.values(n.modules))t.name&&t.bindingLayout?.some(i=>i.group===se&&i.name===t.name)&&e.add(t.name);return e}class bt{id;device;factory;shaderInputs;bindings={};_uniformStore;_bindGroupCacheToken={};constructor(e,t={}){this.id=t.id||O("material"),this.device=e,this.factory=t.factory||new mt(e,{modules:t.modules||t.shaderInputs?.getModules()||[]});const i=Object.fromEntries((t.shaderInputs?.getModules()||this.factory.modules).map(s=>[s.name,s]));this.shaderInputs=t.shaderInputs||new V(i),this._uniformStore=new fe(this.device,this.shaderInputs.modules);for(const[s,r]of Object.entries(this.shaderInputs.modules))if(this.ownsModule(s)&&ye(r)){const a=this._uniformStore.getManagedUniformBuffer(s);this.bindings[`${s}Uniforms`]=a}this.updateShaderInputs(),t.bindings&&this._replaceOwnedBindings(t.bindings)}destroy(){this._uniformStore.destroy()}clone(e={}){const t=this.factory.createMaterial({id:e.id,shaderInputs:e.shaderInputs,bindings:{...this.getResourceBindings(),...e.bindings}});return e.shaderInputs||t.setProps(this.shaderInputs.getUniformValues()),e.moduleProps&&t.setProps(e.moduleProps),t}ownsBinding(e){return this.factory.ownsBinding(e)}ownsModule(e){return this.factory.ownsModule(e)}setProps(e){this.shaderInputs.setProps(e),this.updateShaderInputs()}updateShaderInputs(){this._uniformStore.setUniforms(this.shaderInputs.getUniformValues()),this._setOwnedBindings(this.shaderInputs.getBindingValues())&&(this._bindGroupCacheToken={})}getResourceBindings(){const e={};for(const[t,i]of Object.entries(this.bindings))pt(t)||(e[t]=i);return e}getBindings(){const e={},t=e;for(const[i,s]of Object.entries(this.bindings))s instanceof j?s.isReady&&(t[i]=s.texture):t[i]=s;return e}getBindingsByGroup(){return this.factory.getBindingsByGroup(this.getBindings())}getBindGroupCacheKey(e){return e===se?this._bindGroupCacheToken:null}getBindingsUpdateTimestamp(){let e=0;for(const t of Object.values(this.bindings))t instanceof We?e=Math.max(e,t.texture.updateTimestamp):t instanceof R||t instanceof C?e=Math.max(e,t.updateTimestamp):t instanceof j?e=t.texture?Math.max(e,t.texture.updateTimestamp):1/0:t instanceof le||(e=Math.max(e,t.buffer.updateTimestamp));return e}_replaceOwnedBindings(e){this._setOwnedBindings(e)&&(this._bindGroupCacheToken={})}_setOwnedBindings(e){let t=!1;for(const[i,s]of Object.entries(e))s!==void 0&&this.ownsBinding(i)&&this.bindings[i]!==s&&(this.bindings[i]=s,t=!0);return t}}class ue{device;model;transformFeedback;static defaultProps={...H.defaultProps,outputs:void 0,feedbackBuffers:void 0};static isSupported(e){return e?.info?.type==="webgl"}constructor(e,t=ue.defaultProps){if(!ue.isSupported(e))throw new Error("BufferTransform not yet implemented on WebGPU");this.device=e,this.model=new H(this.device,{id:t.id||"buffer-transform-model",fs:t.fs||qe(),topology:t.topology||"point-list",varyings:t.outputs||t.varyings,...t}),this.transformFeedback=this.device.createTransformFeedback({layout:this.model.pipeline.shaderLayout,buffers:t.feedbackBuffers}),this.model.setTransformFeedback(this.transformFeedback),Object.seal(this)}destroy(){this.model&&this.model.destroy()}delete(){this.destroy()}run(e){e?.inputBuffers&&this.model.setAttributes(e.inputBuffers),e?.outputBuffers&&this.transformFeedback.setBuffers(e.outputBuffers);const t=this.device.beginRenderPass(e);this.model.draw(t),t.end()}getBuffer(e){return this.transformFeedback.getBuffer(e)}readAsync(e){const t=this.getBuffer(e);if(!t)throw new Error("BufferTransform#getBuffer");if(t instanceof R)return t.readAsync();const{buffer:i,byteOffset:s=0,byteLength:r=i.byteLength}=t;return i.readAsync(s,r)}}const Di="transform_output";class Ei{device;model;sampler;currentIndex=0;samplerTextureMap=null;bindings=[];resources={};constructor(e,t){this.device=e,this.sampler=e.createSampler({addressModeU:"clamp-to-edge",addressModeV:"clamp-to-edge",minFilter:"nearest",magFilter:"nearest",mipmapFilter:"nearest"}),this.model=new H(this.device,{id:t.id||O("texture-transform-model"),fs:t.fs||qe({input:t.targetTextureVarying,inputChannels:t.targetTextureChannels,output:Di}),vertexCount:t.vertexCount,...t}),this._initialize(t),Object.seal(this)}destroy(){this.model.destroy();for(const e of this.bindings)e.framebuffer?.destroy()}delete(){this.destroy()}run(e){const{framebuffer:t}=this.bindings[this.currentIndex],i=this.device.beginRenderPass({framebuffer:t,...e});this.model.draw(i),i.end(),this.device.submit()}getTargetTexture(){const{targetTexture:e}=this.bindings[this.currentIndex];return e}getFramebuffer(){return this.bindings[this.currentIndex].framebuffer}_initialize(e){this._updateBindings(e)}_updateBindings(e){this.bindings[this.currentIndex]=this._updateBinding(this.bindings[this.currentIndex],e)}_updateBinding(e,{sourceBuffers:t,sourceTextures:i,targetTexture:s}){if(e||(e={sourceBuffers:{},sourceTextures:{},targetTexture:null}),Object.assign(e.sourceTextures,i),Object.assign(e.sourceBuffers,t),s){e.targetTexture=s;const{width:r,height:a}=s;e.framebuffer&&e.framebuffer.destroy(),e.framebuffer=this.device.createFramebuffer({id:"transform-framebuffer",width:r,height:a,colorAttachments:[s]}),e.framebuffer.resize({width:r,height:a})}return e}_setSourceTextureParameters(){const e=this.currentIndex,{sourceTextures:t}=this.bindings[e];for(const i in t)t[i].sampler=this.sampler}}class W{id;topology;vertexCount;indices;attributes;userData={};constructor(e){const{attributes:t={},indices:i=null,vertexCount:s=null}=e;this.id=e.id||O("geometry"),this.topology=e.topology,i&&(this.indices=ArrayBuffer.isView(i)?{value:i,size:1}:i),this.attributes={};for(const[r,a]of Object.entries(t)){const o=ArrayBuffer.isView(a)?{value:a}:a;if(!ArrayBuffer.isView(o.value))throw new Error(`${this._print(r)}: must be typed array or object with value as typed array`);if((r==="POSITION"||r==="positions")&&!o.size&&(o.size=3),r==="indices"){if(this.indices)throw new Error("Multiple indices detected");this.indices=o}else this.attributes[r]=o}this.indices&&this.indices.isIndexed!==void 0&&(this.indices=Object.assign({},this.indices),delete this.indices.isIndexed),this.vertexCount=s||this._calculateVertexCount(this.attributes,this.indices)}getVertexCount(){return this.vertexCount}getAttributes(){return this.indices?{indices:this.indices,...this.attributes}:this.attributes}_print(e){return`Geometry ${this.id} attribute ${e}`}_setAttributes(e,t){return this}_calculateVertexCount(e,t){if(t)return t.value.length;let i=1/0;for(const s of Object.values(e)){const{value:r,size:a,constant:o}=s;!o&&r&&a!==void 0&&a>=1&&(i=Math.min(i,r.length/a))}return i}}const Ri=`struct VertexInputs {
  @location(0) clipSpacePositions: vec2<f32>,
  @location(1) texCoords: vec2<f32>,
  @location(2) coordinates: vec2<f32>
}

struct FragmentInputs {
  @builtin(position) Position : vec4<f32>,
  @location(0) position : vec2<f32>,
  @location(1) coordinate : vec2<f32>,
  @location(2) uv : vec2<f32>
};

@vertex
fn vertexMain(inputs: VertexInputs) -> FragmentInputs {
  var outputs: FragmentInputs;
  outputs.Position = vec4(inputs.clipSpacePositions, 0., 1.);
  outputs.position = inputs.clipSpacePositions;
  outputs.coordinate = inputs.coordinates;
  outputs.uv = inputs.texCoords;
  return outputs;
}
`,Fi=`#version 300 es
in vec2 clipSpacePositions;
in vec2 texCoords;
in vec2 coordinates;

out vec2 position;
out vec2 coordinate;
out vec2 uv;

void main(void) {
  gl_Position = vec4(clipSpacePositions, 0., 1.);
  position = clipSpacePositions;
  coordinate = coordinates;
  uv = texCoords;
}
`,xt=[-1,-1,1,-1,-1,1,1,1];class Ce extends H{constructor(e,t){const i=xt.map(s=>s===-1?0:s);t.source&&(t={...t,source:`${Ri}
${t.source}`}),super(e,{id:t.id||O("clip-space"),...t,vs:Fi,vertexCount:4,geometry:new W({topology:"triangle-strip",vertexCount:4,attributes:{clipSpacePositions:{size:2,value:new Float32Array(xt)},texCoords:{size:2,value:new Float32Array(i)},coordinates:{size:2,value:new Float32Array(i)}}})})}}const Ni={name:"background",uniformTypes:{scale:"vec2<f32>"}},Bi=`@group(0) @binding(auto) var backgroundTexture: texture_2d<f32>;
@group(0) @binding(auto) var backgroundTextureSampler: sampler;
struct backgroundUniforms {
  scale: vec2<f32>,
};
@group(0) @binding(auto) var<uniform> background: backgroundUniforms;

fn billboardTexture_getTextureUV(uv: vec2<f32>) -> vec2<f32> {
        let scale: vec2<f32> = background.scale;
        var position: vec2<f32> = (uv - vec2<f32>(0.5, 0.5)) / scale + vec2<f32>(0.5, 0.5);
        return position;
}

@fragment
fn fragmentMain(inputs: FragmentInputs) -> @location(0) vec4<f32> {
        let position: vec2<f32> = billboardTexture_getTextureUV(inputs.uv);
        return textureSample(backgroundTexture, backgroundTextureSampler, position);
}
`,ji=`#version 300 es
precision highp float;

uniform sampler2D backgroundTexture;

layout(std140) uniform backgroundUniforms {
  vec2 scale;
} background;

in vec2 coordinate;
out vec4 fragColor;

vec2 billboardTexture_getTextureUV(vec2 coord) {
  vec2 position = (coord - 0.5) / background.scale + 0.5;
  return position;
}

void main(void) {
  vec2 position = billboardTexture_getTextureUV(coordinate);
  fragColor = texture(backgroundTexture, position);
}
`;class yt extends Ce{backgroundTexture=null;constructor(e,t){if(super(e,{...t,id:t.id||"background-texture-model",source:Bi,fs:ji,modules:[...t.modules||[],Ni],parameters:{depthWriteEnabled:!1,...t.parameters||{},...t.blend?{blend:!0,blendColorOperation:"add",blendAlphaOperation:"add",blendColorSrcFactor:"one-minus-dst-alpha",blendColorDstFactor:"one",blendAlphaSrcFactor:"one-minus-dst-alpha",blendAlphaDstFactor:"one"}:{}}}),!t.backgroundTexture)throw new Error("BackgroundTextureModel requires a backgroundTexture prop");this.setProps(t)}setProps(e){const{backgroundTexture:t}=e;if(t)if(this.setBindings({backgroundTexture:t}),t.isReady){const i=t instanceof j?t.texture:t;this.backgroundTexture=i,this.updateScale(i)}else t.ready.then(i=>{this.backgroundTexture=i,this.updateScale(i)})}predraw(){super.predraw()}updateScale(e){if(!e){this.shaderInputs.setProps({background:{scale:[1,1]}});return}const[t,i]=this.device.getCanvasContext().getDrawingBufferSize(),s=e.width,r=e.height,a=t/i,o=s/r;let c=1,u=1;a>o?u=a/o:c=o/a,this.shaderInputs.setProps({background:{scale:[c,u]}})}}class _t extends W{constructor(e={}){const{id:t=O("sphere-geometry")}=e,{indices:i,attributes:s}=Gi(e);super({...e,id:t,topology:"triangle-list",indices:i,attributes:{...s,...e.attributes}})}}function Gi(n){const{nlat:e=10,nlong:t=10}=n,r=Math.PI-0,c=2*Math.PI-0,u=(e+1)*(t+1),d=(_,b,g,x,v)=>n.radius||1,h=new Float32Array(u*3),f=new Float32Array(u*3),p=new Float32Array(u*2),m=u>65535?Uint32Array:Uint16Array,l=new m(e*t*6);for(let _=0;_<=e;_++)for(let b=0;b<=t;b++){const g=b/t,x=_/e,v=b+_*(t+1),A=v*2,P=v*3,D=c*g,S=r*x,E=Math.sin(D),I=Math.cos(D),T=Math.sin(S),M=Math.cos(S),N=I*T,G=M,U=E*T,B=d();h[P+0]=B*N,h[P+1]=B*G,h[P+2]=B*U,f[P+0]=N,f[P+1]=G,f[P+2]=U,p[A+0]=g,p[A+1]=1-x}const w=t+1;for(let _=0;_<t;_++)for(let b=0;b<e;b++){const g=(_*e+b)*6;l[g+0]=b*w+_,l[g+1]=b*w+_+1,l[g+2]=(b+1)*w+_,l[g+3]=(b+1)*w+_,l[g+4]=b*w+_+1,l[g+5]=(b+1)*w+_+1}return{indices:{size:1,value:l},attributes:{POSITION:{size:3,value:h},NORMAL:{size:3,value:f},TEXCOORD_0:{size:2,value:p}}}}const Ui=.02,zi=.12,$i=.15,Hi=.2,Ae=[0,1,0],Xi=[255,255,255],Vi=1,Te=.35,Pe=255,Wi=1,Ki=.01,Yi={depthCompare:"less-equal",depthWriteEnabled:!1,cullMode:"none"},qi=[{name:"instancePosition",format:"float32x3",stepMode:"instance"},{name:"instanceDirection",format:"float32x3",stepMode:"instance"},{name:"instanceScale",format:"float32x3",stepMode:"instance"},{name:"instanceColor",format:"float32x4",stepMode:"instance"}],Ji={name:"lightMarker",props:{},uniforms:{},uniformTypes:{viewProjectionMatrix:"mat4x4<f32>"}},Zi="inputs.positions * inputs.instanceScale",Qi="vec3<f32>(inputs.positions.x * inputs.instanceScale.x, (inputs.positions.y - 0.5) * inputs.instanceScale.y, inputs.positions.z * inputs.instanceScale.z)",en="positions * instanceScale",tn="vec3(positions.x * instanceScale.x, (positions.y - 0.5) * instanceScale.y, positions.z * instanceScale.z)";class Le extends H{lightModelProps;_instanceData;_managedBuffers;buildInstanceData;sizePropNames;constructor(e,t,i){const s=i.buildInstanceData(t),r=Ct(e,t.id||i.idPrefix,s),a=new V({lightMarker:Ji});a.setProps({lightMarker:{viewProjectionMatrix:Tt(t)}});const{source:o,vs:c,fs:u}=dn(i.anchorMode),d=t;super(e,{...d,id:t.id||i.idPrefix,source:o,vs:c,fs:u,geometry:i.geometry,shaderInputs:a,bufferLayout:[...qi],attributes:r,instanceCount:s.instanceCount,parameters:Pt(t.parameters)}),this.lightModelProps=t,this._instanceData=s,this._managedBuffers=r,this.buildInstanceData=i.buildInstanceData,this.sizePropNames=i.sizePropNames}destroy(){super.destroy(),At(this._managedBuffers),this._managedBuffers={}}draw(e){return this.instanceCount===0?!0:super.draw(e)}setProps(e){this.lightModelProps={...this.lightModelProps,...e},e.parameters&&this.setParameters(Pt(this.lightModelProps.parameters)),("viewMatrix"in e||"projectionMatrix"in e)&&(this.shaderInputs.setProps({lightMarker:{viewProjectionMatrix:Tt(this.lightModelProps)}}),this.setNeedsRedraw("lightMarker camera")),un(e,this.sizePropNames)&&this.rebuildInstanceData()}rebuildInstanceData(){const e=this.buildInstanceData(this.lightModelProps),t=Ct(this.device,this.id,e);this.setAttributes(t),this.setInstanceCount(e.instanceCount),At(this._managedBuffers),this._managedBuffers=t,this._instanceData=e}}function nn(n){const e=vt(n.lights),t=Me(n),i=n.pointLightRadius??Ui*t.sceneScale*t.markerScale;return Oe(e.length,(s,r)=>({color:Se(s),direction:Ae,position:s.position,scale:[i,i,i]}),e)}function sn(n){const e=It(n.lights),t=Me(n),i=n.spotLightLength??zi*t.sceneScale*t.markerScale;return Oe(e.length,(s,r)=>{const a=Z(s.outerConeAngle??Math.PI/4,0,Math.PI/2-Ki),o=Math.tan(a)*i;return{color:Se(s),direction:wt(s.direction),position:s.position,scale:[o,i,o]}},e)}function rn(n){const e=on(n.lights),t=Me(n),i=n.directionalLightLength??$i*t.sceneScale*t.markerScale,s=i*Hi;return Oe(e.length,(r,a)=>{const o=wt(r.direction),c=[t.sceneCenter[0]-o[0]*t.sceneScale*Te,t.sceneCenter[1]-o[1]*t.sceneScale*Te,t.sceneCenter[2]-o[2]*t.sceneScale*Te];return{color:Se(r),direction:o,position:c,scale:[s,i,s]}},e)}function vt(n){return n.filter(e=>e.type==="point")}function It(n){return n.filter(e=>e.type==="spot")}function on(n){return n.filter(e=>e.type==="directional")}function Me(n){const e=an(n.lights,n.bounds),t=[(e[0][0]+e[1][0])/2,(e[0][1]+e[1][1])/2,(e[0][2]+e[1][2])/2],i=Math.max(Math.hypot(e[1][0]-e[0][0],e[1][1]-e[0][1],e[1][2]-e[0][2]),Wi);return{bounds:e,markerScale:Math.max(n.markerScale??Vi,0),sceneCenter:t,sceneScale:i}}function Se(n){const e=n.color||Xi,t=Math.max(n.intensity??1,0),i=Z(.35+.3*Math.log10(t+1),.35,1);return[Z(e[0]/Pe,0,1)*i,Z(e[1]/Pe,0,1)*i,Z(e[2]/Pe,0,1)*i,1]}function wt(n){const[e,t,i]=n||Ae,s=Math.hypot(e,t,i);return s===0?[...Ae]:[e/s,t/s,i/s]}function Oe(n,e,t=[]){const i=new Float32Array(n*3),s=new Float32Array(n*3),r=new Float32Array(n*3),a=new Float32Array(n*4);for(const[o,c]of t.entries()){const u=e(c,o);i.set(u.position,o*3),s.set(u.direction,o*3),r.set(u.scale,o*3),a.set(u.color,o*4)}return{instanceCount:n,instancePositions:i,instanceDirections:s,instanceScales:r,instanceColors:a}}function an(n,e){if(e)return cn(e);const t=[...vt(n).map(r=>r.position),...It(n).map(r=>r.position)];if(t.length===0)return[[-.5,-.5,-.5],[.5,.5,.5]];const i=[...t[0]],s=[...t[0]];for(const r of t.slice(1))i[0]=Math.min(i[0],r[0]),i[1]=Math.min(i[1],r[1]),i[2]=Math.min(i[2],r[2]),s[0]=Math.max(s[0],r[0]),s[1]=Math.max(s[1],r[1]),s[2]=Math.max(s[2],r[2]);return[i,s]}function cn(n){return[[...n[0]],[...n[1]]]}function Ct(n,e,t){return{instancePosition:n.createBuffer({id:`${e}-instance-position`,data:re(t.instancePositions,3)}),instanceDirection:n.createBuffer({id:`${e}-instance-direction`,data:re(t.instanceDirections,3)}),instanceScale:n.createBuffer({id:`${e}-instance-scale`,data:re(t.instanceScales,3)}),instanceColor:n.createBuffer({id:`${e}-instance-color`,data:re(t.instanceColors,4)})}}function re(n,e){return n.length>0?n:new Float32Array(e)}function At(n){for(const e of Object.values(n))e?.destroy()}function Tt(n){return new z(n.projectionMatrix).multiplyRight(n.viewMatrix)}function un(n,e){return"lights"in n||"bounds"in n||"markerScale"in n?!0:e.some(t=>t in n)}function Pt(n){return{...Yi,...n||{}}}function dn(n){const e=n==="apex"?Qi:Zi,t=n==="apex"?tn:en;return{source:`struct lightMarkerUniforms {
  viewProjectionMatrix: mat4x4<f32>,
};

@group(0) @binding(auto) var<uniform> lightMarker : lightMarkerUniforms;

struct VertexInputs {
  @location(0) positions : vec3<f32>,
  @location(1) instancePosition : vec3<f32>,
  @location(2) instanceDirection : vec3<f32>,
  @location(3) instanceScale : vec3<f32>,
  @location(4) instanceColor : vec4<f32>,
};

struct FragmentInputs {
  @builtin(position) Position : vec4<f32>,
  @location(0) color : vec4<f32>,
};

fn lightMarker_rotate(localPosition: vec3<f32>, direction: vec3<f32>) -> vec3<f32> {
  let forward = normalize(direction);
  var helperAxis = vec3<f32>(0.0, 1.0, 0.0);
  if (abs(forward.y) > 0.999) {
    helperAxis = vec3<f32>(1.0, 0.0, 0.0);
  }

  let tangent = normalize(cross(helperAxis, forward));
  let bitangent = cross(forward, tangent);
  return tangent * localPosition.x + forward * localPosition.y + bitangent * localPosition.z;
}

@vertex
fn vertexMain(inputs: VertexInputs) -> FragmentInputs {
  var outputs : FragmentInputs;
  let localPosition = ${e};
  let worldPosition = inputs.instancePosition + lightMarker_rotate(localPosition, inputs.instanceDirection);
  outputs.Position = lightMarker.viewProjectionMatrix * vec4<f32>(worldPosition, 1.0);
  outputs.color = inputs.instanceColor;
  return outputs;
}

@fragment
fn fragmentMain(inputs: FragmentInputs) -> @location(0) vec4<f32> {
  return inputs.color;
}
`,vs:`#version 300 es

in vec3 positions;
in vec3 instancePosition;
in vec3 instanceDirection;
in vec3 instanceScale;
in vec4 instanceColor;

layout(std140) uniform lightMarkerUniforms {
  mat4 viewProjectionMatrix;
} lightMarker;

out vec4 vColor;

vec3 lightMarker_rotate(vec3 localPosition, vec3 direction) {
  vec3 forward = normalize(direction);
  vec3 helperAxis = abs(forward.y) > 0.999 ? vec3(1.0, 0.0, 0.0) : vec3(0.0, 1.0, 0.0);
  vec3 tangent = normalize(cross(helperAxis, forward));
  vec3 bitangent = cross(forward, tangent);
  return tangent * localPosition.x + forward * localPosition.y + bitangent * localPosition.z;
}

void main(void) {
  vec3 localPosition = ${t};
  vec3 worldPosition = instancePosition + lightMarker_rotate(localPosition, instanceDirection);
  gl_Position = lightMarker.viewProjectionMatrix * vec4(worldPosition, 1.0);
  vColor = instanceColor;
}
`,fs:`#version 300 es
precision highp float;

in vec4 vColor;
out vec4 fragColor;

void main(void) {
  fragColor = vColor;
}
`}}function Z(n,e,t){return Math.min(t,Math.max(e,n))}const hn=new _t({nlat:8,nlong:12,radius:1});class ln extends Le{constructor(e,t){super(e,t,{anchorMode:"centered",buildInstanceData:nn,geometry:hn,idPrefix:"point-light-model",sizePropNames:["pointLightRadius"]})}}const fn={x:[2,0,1],y:[0,1,2],z:[1,2,0]};class ke extends W{constructor(e={}){const{id:t=O("truncated-code-geometry")}=e,{indices:i,attributes:s}=gn(e);super({...e,id:t,topology:"triangle-list",indices:i,attributes:{POSITION:{size:3,value:s.POSITION},NORMAL:{size:3,value:s.NORMAL},TEXCOORD_0:{size:2,value:s.TEXCOORD_0},...e.attributes}})}}function gn(n={}){const{bottomRadius:e=0,topRadius:t=0,height:i=1,nradial:s=10,nvertical:r=10,verticalAxis:a="y",topCap:o=!1,bottomCap:c=!1}=n,u=(o?2:0)+(c?2:0),d=(s+1)*(r+1+u),h=Math.atan2(e-t,i),f=Math.sin,p=Math.cos,m=Math.PI,l=p(h),w=f(h),_=o?-2:0,b=r+(c?2:0),g=s+1,x=new Uint16Array(s*(r+u)*6),v=fn[a],A=new Float32Array(d*3),P=new Float32Array(d*3),D=new Float32Array(d*2);let S=0,E=0;for(let I=_;I<=b;I++){let T=I/r,M=i*T,N;I<0?(M=0,T=1,N=e):I>r?(M=i,T=1,N=t):N=e+(t-e)*(I/r),(I===-2||I===r+2)&&(N=0,T=0),M-=i/2;for(let G=0;G<g;G++){const U=f(G*m*2/s),B=p(G*m*2/s);A[S+v[0]]=U*N,A[S+v[1]]=M,A[S+v[2]]=B*N,P[S+v[0]]=I<0||I>r?0:U*l,P[S+v[1]]=I<0?-1:I>r?1:w,P[S+v[2]]=I<0||I>r?0:B*l,D[E+0]=G/s,D[E+1]=T,E+=2,S+=3}}for(let I=0;I<r+u;I++)for(let T=0;T<s;T++){const M=(I*s+T)*6;x[M+0]=g*(I+0)+0+T,x[M+1]=g*(I+0)+1+T,x[M+2]=g*(I+1)+1+T,x[M+3]=g*(I+0)+0+T,x[M+4]=g*(I+1)+1+T,x[M+5]=g*(I+1)+0+T}return{indices:x,attributes:{POSITION:A,NORMAL:P,TEXCOORD_0:D}}}class De extends ke{constructor(e={}){const{id:t=O("cone-geometry"),radius:i=1,cap:s=!0}=e;super({...e,id:t,topRadius:0,topCap:!!s,bottomCap:!!s,bottomRadius:i})}}const mn=new De({cap:!0,nradial:16,nvertical:1,radius:1});class pn extends Le{constructor(e,t){super(e,t,{anchorMode:"apex",buildInstanceData:sn,geometry:mn,idPrefix:"spot-light-model",sizePropNames:["spotLightLength"]})}}const bn=new De({cap:!0,nradial:12,nvertical:1,radius:1});class xn extends Le{constructor(e,t){super(e,t,{anchorMode:"apex",buildInstanceData:rn,geometry:bn,idPrefix:"directional-light-model",sizePropNames:["directionalLightLength"]})}}function Ee(n,e){if(!n)throw new Error(e)}class oe{id;matrix=new z;display=!0;position=new X;rotation=new X;scale=new X(1,1,1);userData={};props={};constructor(e={}){const{id:t}=e;this.id=t||O(this.constructor.name),this._setScenegraphNodeProps(e)}getBounds(){return null}destroy(){}delete(){this.destroy()}setProps(e){return this._setScenegraphNodeProps(e),this}toString(){return`{type: ScenegraphNode, id: ${this.id})}`}setPosition(e){return Ee(e.length===3,"setPosition requires vector argument"),this.position=e,this}setRotation(e){return Ee(e.length===3||e.length===4,"setRotation requires vector argument"),this.rotation=e,this}setScale(e){return Ee(e.length===3,"setScale requires vector argument"),this.scale=e,this}setMatrix(e,t=!0){t?this.matrix.copy(e):this.matrix=e}setMatrixComponents(e){const{position:t,rotation:i,scale:s,update:r=!0}=e;return t&&this.setPosition(t),i&&this.setRotation(i),s&&this.setScale(s),r&&this.updateMatrix(),this}updateMatrix(){if(this.matrix.identity(),this.matrix.translate(this.position),this.rotation.length===4){const e=new z().fromQuaternion(this.rotation);this.matrix.multiplyRight(e)}else this.matrix.rotateXYZ(this.rotation);return this.matrix.scale(this.scale),this}update({position:e,rotation:t,scale:i}={}){return e&&this.setPosition(e),t&&this.setRotation(t),i&&this.setScale(i),this.updateMatrix(),this}getCoordinateUniforms(e,t){t=t||this.matrix;const i=new z(e).multiplyRight(t),s=i.invert(),r=s.transpose();return{viewMatrix:e,modelMatrix:t,objectMatrix:t,worldMatrix:i,worldInverseMatrix:s,worldInverseTransposeMatrix:r}}_setScenegraphNodeProps(e){e?.position&&this.setPosition(e.position),e?.rotation&&this.setRotation(e.rotation),e?.scale&&this.setScale(e.scale),this.updateMatrix(),e?.matrix&&this.setMatrix(e.matrix),Object.assign(this.props,e)}}class de extends oe{children;constructor(e={}){e=Array.isArray(e)?{children:e}:e;const{children:t=[]}=e;y.assert(t.every(i=>i instanceof oe),"every child must an instance of ScenegraphNode"),super(e),this.children=t}getBounds(){const e=[[1/0,1/0,1/0],[-1/0,-1/0,-1/0]];return this.traverse((t,{worldMatrix:i})=>{const s=t.getBounds();if(!s)return;const[r,a]=s,o=new X(r).add(a).divide([2,2,2]);i.transformAsPoint(o,o);const c=new X(a).subtract(r).divide([2,2,2]);i.transformAsVector(c,c);for(let u=0;u<8;u++){const d=new X(u&1?-1:1,u&2?-1:1,u&4?-1:1).multiply(c).add(o);for(let h=0;h<3;h++)e[0][h]=Math.min(e[0][h],d[h]),e[1][h]=Math.max(e[1][h],d[h])}}),Number.isFinite(e[0][0])?e:null}destroy(){this.children.forEach(e=>e.destroy()),this.removeAll(),super.destroy()}add(...e){for(const t of e)Array.isArray(t)?this.add(...t):this.children.push(t);return this}remove(e){const t=this.children,i=t.indexOf(e);return i>-1&&t.splice(i,1),this}removeAll(){return this.children=[],this}traverse(e,{worldMatrix:t=new z}={}){const i=new z(t).multiplyRight(this.matrix);for(const s of this.children)s instanceof de?s.traverse(e,{worldMatrix:i}):e(s,{worldMatrix:i})}preorderTraversal(e,{worldMatrix:t=new z}={}){const i=new z(t).multiplyRight(this.matrix);e(this,{worldMatrix:i});for(const s of this.children)s instanceof de?s.preorderTraversal(e,{worldMatrix:i}):e(s,{worldMatrix:i})}}class yn extends oe{model;bounds=null;managedResources;constructor(e){super(e),this.model=e.model,this.managedResources=e.managedResources||[],this.bounds=e.bounds||null,this.setProps(e)}destroy(){this.model&&(this.model.destroy(),this.model=null),this.managedResources.forEach(e=>e.destroy()),this.managedResources=[]}getBounds(){return this.bounds}draw(e){return this.model.draw(e)}}class _n extends W{constructor(e={}){const{id:t=O("cube-geometry"),indices:i=!0}=e;super(i?{...e,id:t,topology:"triangle-list",indices:{size:1,value:vn},attributes:{...Ln,...e.attributes}}:{...e,id:t,topology:"triangle-list",indices:void 0,attributes:{...Mn,...e.attributes}})}}const vn=new Uint16Array([0,1,2,0,2,3,4,5,6,4,6,7,8,9,10,8,10,11,12,13,14,12,14,15,16,17,18,16,18,19,20,21,22,20,22,23]),In=new Float32Array([-1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,1,1,1,1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,-1,-1,1,1,-1,-1,1,1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1]),wn=new Float32Array([0,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,1,0,0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,0]),Cn=new Float32Array([0,0,1,0,1,1,0,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1]),An=new Float32Array([1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,1,1,1,-1,1,1,-1,-1,1,-1,-1,1,1,-1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,-1]),Tn=new Float32Array([1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,0,0]),Pn=new Float32Array([1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,0,0,1,0,1,0,1,1,1,0,1,1,0,0,1,0,1,0,1]),Ln={POSITION:{size:3,value:In},NORMAL:{size:3,value:wn},TEXCOORD_0:{size:2,value:Cn}},Mn={POSITION:{size:3,value:An},TEXCOORD_0:{size:2,value:Tn},COLOR_0:{size:3,value:Pn}};class Sn extends ke{constructor(e={}){const{id:t=O("cylinder-geometry"),radius:i=1}=e;super({...e,id:t,bottomRadius:i,topRadius:i})}}const On=[-1,0,0,0,1,0,0,0,-1,0,0,1,0,-1,0,1,0,0],kn=[3,4,5,3,5,1,3,1,0,3,0,4,4,0,2,4,2,5,2,0,1,5,2,1];class Dn extends W{constructor(e={}){const{id:t=O("ico-sphere-geometry")}=e,{indices:i,attributes:s}=En(e);super({...e,id:t,topology:"triangle-list",indices:i,attributes:{...s,...e.attributes}})}}function En(n){const{iterations:e=0}=n,t=Math.PI,i=t*2,s=[...On];let r=[...kn];s.push(),r.push();const a=(()=>{const d={};return(h,f)=>{h*=3,f*=3;const p=h<f?h:f,m=h>f?h:f,l=`${p}|${m}`;if(l in d)return d[l];const w=s[h],_=s[h+1],b=s[h+2],g=s[f],x=s[f+1],v=s[f+2];let A=(w+g)/2,P=(_+x)/2,D=(b+v)/2;const S=Math.sqrt(A*A+P*P+D*D);A/=S,P/=S,D/=S,s.push(A,P,D);const E=s.length/3-1;return d[l]=E,E}})();for(let d=0;d<e;d++){const h=[];for(let f=0;f<r.length;f+=3){const p=a(r[f+0],r[f+1]),m=a(r[f+1],r[f+2]),l=a(r[f+2],r[f+0]);h.push(l,r[f+0],p,p,r[f+1],m,m,r[f+2],l,p,m,l)}r=h}const o=new Array(s.length),c=new Array(s.length/3*2),u=r.length;for(let d=u-3;d>=0;d-=3){const h=r[d+0],f=r[d+1],p=r[d+2],m=h*3,l=f*3,w=p*3,_=h*2,b=f*2,g=p*2,x=s[m+0],v=s[m+1],A=s[m+2],P=Math.acos(A/Math.sqrt(x*x+v*v+A*A)),D=Math.atan2(v,x)+t,S=P/t,E=1-D/i,I=s[l+0],T=s[l+1],M=s[l+2],N=Math.acos(M/Math.sqrt(I*I+T*T+M*M)),G=Math.atan2(T,I)+t,U=N/t,B=1-G/i,Q=s[w+0],ee=s[w+1],te=s[w+2],Rt=Math.acos(te/Math.sqrt(Q*Q+ee*ee+te*te)),Ft=Math.atan2(ee,Q)+t,ze=Rt/t,ie=1-Ft/i,Nt=[Q-I,ee-T,te-M],Bt=[x-I,v-T,A-M],F=new X(Nt).cross(Bt).normalize();let L;(E===0||B===0||ie===0)&&(E===0||E>.5)&&(B===0||B>.5)&&(ie===0||ie>.5)&&(s.push(s[m+0],s[m+1],s[m+2]),L=s.length/3-1,r.push(L),c[L*2+0]=1,c[L*2+1]=S,o[L*3+0]=F.x,o[L*3+1]=F.y,o[L*3+2]=F.z,s.push(s[l+0],s[l+1],s[l+2]),L=s.length/3-1,r.push(L),c[L*2+0]=1,c[L*2+1]=U,o[L*3+0]=F.x,o[L*3+1]=F.y,o[L*3+2]=F.z,s.push(s[w+0],s[w+1],s[w+2]),L=s.length/3-1,r.push(L),c[L*2+0]=1,c[L*2+1]=ze,o[L*3+0]=F.x,o[L*3+1]=F.y,o[L*3+2]=F.z),o[m+0]=o[l+0]=o[w+0]=F.x,o[m+1]=o[l+1]=o[w+1]=F.y,o[m+2]=o[l+2]=o[w+2]=F.z,c[_+0]=E,c[_+1]=S,c[b+0]=B,c[b+1]=U,c[g+0]=ie,c[g+1]=ze}return{indices:{size:1,value:new Uint16Array(r)},attributes:{POSITION:{size:3,value:new Float32Array(s)},NORMAL:{size:3,value:new Float32Array(o)},TEXCOORD_0:{size:2,value:new Float32Array(c)}}}}function Rn(n){const{indices:e,attributes:t}=n;if(!e)return n;const i=e.value.length,s={};for(const r in t){const a=t[r],{constant:o,value:c,size:u}=a;if(o||!u)continue;const d=new c.constructor(i*u);for(let h=0;h<i;++h){const f=e.value[h];for(let p=0;p<u;p++)d[h*u+p]=c[f*u+p]}s[r]={size:u,value:d}}return{attributes:Object.assign({},t,s)}}class Fn extends W{constructor(e={}){const{id:t=O("plane-geometry")}=e,{indices:i,attributes:s}=Nn(e);super({...e,id:t,topology:"triangle-list",indices:i,attributes:{...s,...e.attributes}})}}function Nn(n){const{type:e="x,y",offset:t=0,flipCull:i=!1,unpack:s=!1}=n,r=e.split(",");let a=n[`${r[0]}len`]||1;const o=n[`${r[1]}len`]||1,c=n[`n${r[0]}`]||1,u=n[`n${r[1]}`]||1,d=(c+1)*(u+1),h=new Float32Array(d*3),f=new Float32Array(d*3),p=new Float32Array(d*2);i&&(a=-a);let m=0,l=0;for(let g=0;g<=u;g++)for(let x=0;x<=c;x++){const v=x/c,A=g/u;switch(p[m+0]=i?1-v:v,p[m+1]=A,e){case"x,y":h[l+0]=a*v-a*.5,h[l+1]=o*A-o*.5,h[l+2]=t,f[l+0]=0,f[l+1]=0,f[l+2]=i?1:-1;break;case"x,z":h[l+0]=a*v-a*.5,h[l+1]=t,h[l+2]=o*A-o*.5,f[l+0]=0,f[l+1]=i?1:-1,f[l+2]=0;break;case"y,z":h[l+0]=t,h[l+1]=a*v-a*.5,h[l+2]=o*A-o*.5,f[l+0]=i?1:-1,f[l+1]=0,f[l+2]=0;break;default:throw new Error("PlaneGeometry: unknown type")}m+=2,l+=3}const w=c+1,_=new Uint16Array(c*u*6);for(let g=0;g<u;g++)for(let x=0;x<c;x++){const v=(g*c+x)*6;_[v+0]=(g+0)*w+x,_[v+1]=(g+1)*w+x,_[v+2]=(g+0)*w+x+1,_[v+3]=(g+1)*w+x,_[v+4]=(g+1)*w+x+1,_[v+5]=(g+0)*w+x+1}const b={indices:{size:1,value:_},attributes:{POSITION:{size:3,value:h},NORMAL:{size:3,value:f},TEXCOORD_0:{size:2,value:p}}};return s?Rn(b):b}function Bn(){let n=1,e=1;return()=>(n=Math.sin(e*17.23),e=Math.cos(n*27.92),jn(Math.abs(n*e)*1432.71))}function jn(n){return n-Math.floor(n)}let Re="";function Gn(n){Re=n}async function Un(n,e){const t=new Image;return t.crossOrigin=e?.crossOrigin||"anonymous",t.src=n.startsWith("http")?n:Re+n,await t.decode(),e?await createImageBitmap(t,e):await createImageBitmap(t)}async function zn(n,e){return await new Promise((t,i)=>{try{const s=new Image;s.onload=()=>t(s),s.onerror=()=>i(new Error(`Could not load image ${n}.`)),s.crossOrigin=e?.crossOrigin||"anonymous",s.src=n.startsWith("http")?n:Re+n}catch(s){i(s)}})}class Fe{id;current;next;constructor(e){this.id=e.id||"swap",this.current=e.current,this.next=e.next}destroy(){this.current?.destroy(),this.next?.destroy()}swap(){const e=this.current;this.current=this.next,this.next=e}}class Lt extends Fe{constructor(e,t){t={...t};const{width:i=1,height:s=1}=t;let r=t.colorAttachments?.map(c=>typeof c!="string"?c:e.createTexture({id:`${t.id}-texture-0`,format:c,usage:C.SAMPLE|C.RENDER|C.COPY_SRC|C.COPY_DST,width:i,height:s}));const a=e.createFramebuffer({...t,colorAttachments:r});r=t.colorAttachments?.map(c=>typeof c!="string"?c:e.createTexture({id:`${t.id}-texture-1`,format:c,usage:C.SAMPLE|C.RENDER|C.COPY_SRC|C.COPY_DST,width:i,height:s}));const o=e.createFramebuffer({...t,colorAttachments:r});super({current:a,next:o})}resize(e){if(e.width===this.current.width&&e.height===this.current.height)return!1;const{current:t,next:i}=this;return this.current=t.clone(e),t.destroy(),this.next=i.clone(e),i.destroy(),!0}}class $n extends Fe{constructor(e,t){super({current:e.createBuffer(t),next:e.createBuffer(t)})}resize(e){if(e.byteLength===this.current.byteLength)return!1;const{current:t,next:i}=this;return this.current=t.clone(e),t.destroy(),this.next=i.clone(e),i.destroy(),!0}}function Hn(n){const{shaderPass:e,action:t,shadingLanguage:i}=n;switch(t){case"filter":const s=`${e.name}_filterColor_ext`;return i==="wgsl"?Xn(s):Wn(s);case"sample":const r=`${e.name}_sampleColor`;return i==="wgsl"?Vn(r):Kn(r);default:throw new Error(`${e.name} no fragment shader generated for shader pass`)}}function Xn(n){return`@group(0) @binding(auto) var sourceTexture: texture_2d<f32>;
@group(0) @binding(auto) var sourceTextureSampler: sampler;

@fragment
fn fragmentMain(inputs: FragmentInputs) -> @location(0) vec4f {
  let texCoord = inputs.coordinate;
  let texSize = vec2f(textureDimensions(sourceTexture));

  var fragColor = textureSample(sourceTexture, sourceTextureSampler, texCoord);
  fragColor = ${n}(fragColor, texSize, texCoord);
  return fragColor;
}
`}function Vn(n){return`@group(0) @binding(auto) var sourceTexture: texture_2d<f32>;
@group(0) @binding(auto) var sourceTextureSampler: sampler;

@fragment
fn fragmentMain(inputs: FragmentInputs) -> @location(0) vec4f {
  let texCoord = inputs.coordinate;
  let texSize = vec2f(textureDimensions(sourceTexture));
  return ${n}(sourceTexture, sourceTextureSampler, texSize, texCoord);
}
`}function Wn(n){return`#version 300 es

uniform sampler2D sourceTexture;

in vec2 position;
in vec2 coordinate;
in vec2 uv;

out vec4 fragColor;

void main() {
  vec2 texCoord = coordinate;
  ivec2 iTexSize = textureSize(sourceTexture, 0);
  vec2 texSize = vec2(float(iTexSize.x), float(iTexSize.y));

  fragColor = texture(sourceTexture, texCoord);
  fragColor = ${n}(fragColor, texSize, texCoord);
}
`}function Kn(n){return`#version 300 es

uniform sampler2D sourceTexture;

in vec2 position;
in vec2 coordinate;
in vec2 uv;

out vec4 fragColor;

void main() {
  vec2 texCoord = coordinate;
  ivec2 iTexSize = textureSize(sourceTexture, 0);
  vec2 texSize = vec2(float(iTexSize.x), float(iTexSize.y));

  fragColor = ${n}(sourceTexture, texSize, texCoord);
}
`}class Yn{device;shaderInputs;passRenderers;swapFramebuffers;textureModel;constructor(e,t){this.device=e,t.shaderPasses.map(r=>Wt(r));const i=t.shaderPasses.reduce((r,a)=>({...r,[a.name]:a}),{});this.shaderInputs=t.shaderInputs||new V(i);const s=e.getCanvasContext().getDrawingBufferSize();this.swapFramebuffers=new Lt(e,{colorAttachments:[e.preferredColorFormat],width:s[0],height:s[1]}),this.textureModel=new yt(e,{backgroundTexture:this.swapFramebuffers.current.colorAttachments[0].texture}),this.passRenderers=t.shaderPasses.map(r=>new qn(e,r))}destroy(){for(const e of this.passRenderers)e.destroy();this.swapFramebuffers.destroy(),this.textureModel.destroy()}resize(e){e||=this.device.getCanvasContext().getDrawingBufferSize(),this.swapFramebuffers.resize({width:e[0],height:e[1]})}renderToScreen(e){const t=this.renderToTexture(e);if(!t)return!1;const i=this.device.getDefaultCanvasContext().getCurrentFramebuffer({depthStencilFormat:!1}),s=this.device.beginRenderPass({id:"shader-pass-renderer-to-screen",framebuffer:i,clearDepth:!1});return this.textureModel.setProps({backgroundTexture:t}),this.textureModel.draw(s),s.end(),!0}renderToTexture(e){const{sourceTexture:t}=e;if(!t.isReady)return null;if(this.passRenderers.length===0)return t.texture;this.textureModel.setProps({backgroundTexture:t});const i=this.device.beginRenderPass({id:"shader-pass-renderer-clear-texture",framebuffer:this.swapFramebuffers.current,clearColor:[1,0,0,1]});this.textureModel.draw(i),i.end();let s=!0;for(const a of this.passRenderers)for(const o of a.subPassRenderers){s||this.swapFramebuffers.swap(),s=!1;const u={sourceTexture:this.swapFramebuffers.current.colorAttachments[0].texture},d=this.device.beginRenderPass({id:"shader-pass-renderer-run-pass",framebuffer:this.swapFramebuffers.next,clearColor:[0,0,0,1],clearDepth:1});o.render({renderPass:d,bindings:u}),d.end()}return this.swapFramebuffers.swap(),this.swapFramebuffers.current.colorAttachments[0].texture}}class qn{shaderPass;subPassRenderers;constructor(e,t,i={}){this.shaderPass=t;const s=t.passes||[];this.subPassRenderers=s.map(r=>new Jn(e,t,r))}destroy(){for(const e of this.subPassRenderers)e.destroy()}}class Jn{model;shaderPass;subPass;constructor(e,t,i){this.shaderPass=t,this.subPass=i;const s=i.action||i.filter&&"filter"||i.sampler&&"sample"||"filter",r=Hn({shaderPass:t,action:s,shadingLanguage:e.info.shadingLanguage});this.model=new Ce(e,{id:`${t.name}-subpass`,source:r,fs:r,modules:[t],parameters:{depthWriteEnabled:!1}})}destroy(){this.model.destroy()}render(e){const{renderPass:t,bindings:i}=e;this.model.shaderInputs.setProps({[this.shaderPass.name]:this.shaderPass.uniforms||{}}),this.model.shaderInputs.setProps({[this.shaderPass.name]:this.subPass.uniforms||{}}),this.model.setBindings(i||{}),this.model.draw(t)}}const Ne=2,Zn=1e4;class Ue{static defaultProps={...Ht.defaultProps,id:"unnamed",handle:void 0,userData:{},source:"",modules:[],defines:{},bindings:void 0,shaderInputs:void 0,pipelineFactory:void 0,shaderFactory:void 0,shaderAssembler:Ye.getDefaultShaderAssembler(),debugShaders:void 0};device;id;pipelineFactory;shaderFactory;userData={};bindings={};pipeline;source;shader;shaderInputs;_uniformStore;_pipelineNeedsUpdate="newly created";_getModuleUniforms;props;_destroyed=!1;constructor(e,t){if(e.type!=="webgpu")throw new Error("Computation is only supported in WebGPU");this.props={...Ue.defaultProps,...t},t=this.props,this.id=t.id||O("model"),this.device=e,Object.assign(this.userData,t.userData);const i=Object.fromEntries(this.props.modules?.map(u=>[u.name,u])||[]);this.shaderInputs=t.shaderInputs||new V(i),this.setShaderInputs(this.shaderInputs);const s=Qn(e),r=(this.props.modules?.length>0?this.props.modules:this.shaderInputs?.getModules())||[];this.props.shaderLayout=ne(this.props.shaderLayout,r)||null,this.pipelineFactory=t.pipelineFactory||Xe.getDefaultPipelineFactory(this.device),this.shaderFactory=t.shaderFactory||Ve.getDefaultShaderFactory(this.device);const{source:a,getUniforms:o}=this.props.shaderAssembler.assembleWGSLShader({platformInfo:s,...this.props,modules:r});this.source=a,this._getModuleUniforms=o;const c=e.getShaderLayout?.(this.source);this.props.shaderLayout=ne(this.props.shaderLayout||c||null,r)||null,this.pipeline=this._updatePipeline(),t.bindings&&this.setBindings(t.bindings),Object.seal(this)}destroy(){this._destroyed||(this.pipelineFactory.release(this.pipeline),this.shaderFactory.release(this.shader),this._uniformStore.destroy(),this._destroyed=!0)}predraw(){this.updateShaderInputs()}dispatch(e,t,i,s){try{this._logDrawCallStart(),this.pipeline=this._updatePipeline(),this.pipeline.setBindings(this.bindings),e.setPipeline(this.pipeline),e.setBindings({}),e.dispatch(t,i,s)}finally{this._logDrawCallEnd()}}setVertexCount(e){}setInstanceCount(e){}setShaderInputs(e){this.shaderInputs=e,this._uniformStore=new fe(this.device,this.shaderInputs.modules);for(const[t,i]of Object.entries(this.shaderInputs.modules))if(ye(i)){const s=this._uniformStore.getManagedUniformBuffer(t);this.bindings[`${t}Uniforms`]=s}}setShaderModuleProps(e){const t=this._getModuleUniforms(e),i=Object.keys(t).filter(s=>{const r=t[s];return!Je(r)&&typeof r!="number"&&typeof r!="boolean"});for(const s of i)t[s],delete t[s]}updateShaderInputs(){this._uniformStore.setUniforms(this.shaderInputs.getUniformValues())}setBindings(e){Object.assign(this.bindings,e)}_setPipelineNeedsUpdate(e){this._pipelineNeedsUpdate=this._pipelineNeedsUpdate||e}_updatePipeline(){if(this._pipelineNeedsUpdate){let e=null;this.pipeline&&(y.log(1,`Model ${this.id}: Recreating pipeline because "${this._pipelineNeedsUpdate}".`)(),e=this.shader),this._pipelineNeedsUpdate=!1,this.shader=this.shaderFactory.createShader({id:`${this.id}-fragment`,stage:"compute",source:this.source,debugShaders:this.props.debugShaders}),this.pipeline=this.pipelineFactory.createComputePipeline({...this.props,shader:this.shader}),e&&this.shaderFactory.release(e)}return this.pipeline}_lastLogTime=0;_logOpen=!1;_logDrawCallStart(){const e=y.level>3?0:Zn;y.level<2||Date.now()-this._lastLogTime<e||(this._lastLogTime=Date.now(),this._logOpen=!0,y.group(Ne,`>>> DRAWING MODEL ${this.id}`,{collapsed:y.level<=2})())}_logDrawCallEnd(){if(this._logOpen){const e=this.shaderInputs.getDebugTable();y.table(Ne,e)(),y.groupEnd(Ne)(),this._logOpen=!1}}_drawCount=0;_getBufferOrConstantValues(e,t){const i=Ke.getTypedArrayConstructor(t);return(e instanceof R?new i(e.debugData):e).toString()}}function Qn(n){return{type:n.type,shaderLanguage:n.info.shadingLanguage,shaderLanguageVersion:n.info.shadingLanguageVersion,gpu:n.info.gpu,features:n.features}}const es=[0,1,1,1],k=-1,ts={isActive:"i32",indexMode:"i32",batchIndex:"i32",isHighlightActive:"i32",highlightedBatchIndex:"i32",highlightedObjectIndex:"i32",highlightColor:"vec4<f32>"},ae=`precision highp float;
precision highp int;

layout(std140) uniform pickingUniforms {
  int isActive;
  int indexMode;
  int batchIndex;

  int isHighlightActive;
  int highlightedBatchIndex;
  int highlightedObjectIndex;
  vec4 highlightColor;
} picking;
`,Mt=`struct pickingUniforms {
  isActive: i32,
  indexMode: i32,
  batchIndex: i32,

  isHighlightActive: i32,
  highlightedBatchIndex: i32,
  highlightedObjectIndex: i32,
  highlightColor: vec4<f32>,
};

@group(0) @binding(auto) var<uniform> picking: pickingUniforms;
`;function is(n={},e){const t={...e};switch(n.isActive!==void 0&&(t.isActive=!!n.isActive),n.indexMode){case"instance":t.indexMode=0;break;case"attribute":t.indexMode=1;break}switch(typeof n.batchIndex=="number"&&(t.batchIndex=n.batchIndex),n.highlightedObjectIndex){case void 0:break;case null:t.isHighlightActive=!1,t.highlightedObjectIndex=k;break;default:t.isHighlightActive=!0,t.highlightedObjectIndex=n.highlightedObjectIndex}switch(n.highlightedBatchIndex){case void 0:break;case null:t.isHighlightActive=!1,t.highlightedBatchIndex=k;break;default:t.isHighlightActive=!0,t.highlightedBatchIndex=n.highlightedBatchIndex}return n.highlightColor&&(t.highlightColor=n.highlightColor),t}const Be={props:{},uniforms:{},name:"picking",uniformTypes:ts,defaultUniforms:{isActive:!1,indexMode:0,batchIndex:0,isHighlightActive:!1,highlightedBatchIndex:k,highlightedObjectIndex:k,highlightColor:es},getUniforms:is},St=1,ns=new Int32Array([k,k,0,0]);function je(n,e="color",t=n==="webgpu"){if(e==="auto")return t?"index":"color";if(e==="index"&&!t)throw new Error(`Picking mode "${e}" requires WebGPU or a WebGL device that supports renderable rg32sint textures.`);return e}function Ot(n){return n.type==="webgpu"||n.type==="webgl"&&n.isTextureFormatRenderable("rg32sint")}const ss=je;function kt(n){return{objectIndex:n[0]===k?null:n[0],batchIndex:n[1]===k?null:n[1]}}function Dt(n){const e=n[0]+n[1]*256+n[2]*65536;if(e===0)return{objectIndex:null,batchIndex:null};const t=n[3]>0?n[3]-1:0;return{objectIndex:e-1,batchIndex:t}}class he{device;props;mode;pickInfo={batchIndex:null,objectIndex:null};framebuffer=null;static defaultProps={shaderInputs:void 0,onObjectPicked:()=>{},mode:"color",backend:"color"};constructor(e,t){this.device=e,this.props={...he.defaultProps,...t};const i=t.mode??t.backend??he.defaultProps.mode;this.props.mode=i,this.props.backend=i,this.mode=je(this.device.type,i,Ot(this.device))}destroy(){this.framebuffer?.destroy()}getFramebuffer(){return this.framebuffer||(this.framebuffer=this.mode==="index"?this.createIndexFramebuffer():this.createColorFramebuffer()),this.framebuffer}clearPickState(){this.setPickingProps({highlightedBatchIndex:null,highlightedObjectIndex:null})}beginRenderPass(){const e=this.getFramebuffer();return e.resize(this.device.getDefaultCanvasContext().getDevicePixelSize()),this.setPickingProps({isActive:!0}),this.mode==="index"?this.device.beginRenderPass({framebuffer:e,clearColors:[new Float32Array([0,0,0,0]),ns],clearDepth:1}):this.device.beginRenderPass({framebuffer:e,clearColor:[0,0,0,0],clearDepth:1})}async updatePickInfo(e){const t=this.getFramebuffer(),i=this.getPickPosition(e),s=await this.readPickInfo(t,i);return s?(this.hasPickInfoChanged(s)&&(this.pickInfo=s,this.props.onObjectPicked(s)),this.setPickingProps({isActive:!1,highlightedBatchIndex:s.batchIndex,highlightedObjectIndex:s.objectIndex}),this.pickInfo):null}getPickPosition(e){const t=this.device.type!=="webgpu",i=this.device.getDefaultCanvasContext().cssToDevicePixels(e,t),s=i.x+Math.floor(i.width/2),r=i.y+Math.floor(i.height/2);return[s,r]}createIndexFramebuffer(){const e=this.device.createTexture({format:"rgba8unorm",width:1,height:1,usage:C.RENDER_ATTACHMENT}),t=this.device.createTexture({format:"rg32sint",width:1,height:1,usage:C.RENDER_ATTACHMENT|C.COPY_SRC});return this.device.createFramebuffer({colorAttachments:[e,t],depthStencilAttachment:"depth24plus"})}createColorFramebuffer(){const e=this.device.createTexture({format:"rgba8unorm",width:1,height:1,usage:C.RENDER_ATTACHMENT|C.COPY_SRC});return this.device.createFramebuffer({colorAttachments:[e],depthStencilAttachment:"depth24plus"})}setPickingProps(e){this.props.shaderInputs?.setProps({picking:e})}async readPickInfo(e,t){return this.mode==="index"?this.readIndexPickInfo(e,t):this.readColorPickInfo(e,t)}async readIndexPickInfo(e,[t,i]){if(this.device.type==="webgpu"){const r=e.colorAttachments[St]?.texture;if(!r)return null;const a=r.computeMemoryLayout({width:1,height:1}),o=this.device.createBuffer({byteLength:a.byteLength,usage:R.COPY_DST|R.MAP_READ});try{r.readBuffer({x:t,y:i,width:1,height:1},o);const c=await o.readAsync(0,a.byteLength);return kt(new Int32Array(c.buffer,c.byteOffset,2))}finally{o.destroy()}}const s=this.device.readPixelsToArrayWebGL(e,{sourceX:t,sourceY:i,sourceWidth:1,sourceHeight:1,sourceAttachment:St});return s?kt(new Int32Array(s.buffer,s.byteOffset,2)):null}async readColorPickInfo(e,[t,i]){if(this.device.type==="webgpu"){const r=e.colorAttachments[0]?.texture;if(!r)return null;const a=r.computeMemoryLayout({width:1,height:1}),o=this.device.createBuffer({byteLength:a.byteLength,usage:R.COPY_DST|R.MAP_READ});try{r.readBuffer({x:t,y:i,width:1,height:1},o);const c=await o.readAsync(0,a.byteLength);return Dt(new Uint8Array(c.buffer,c.byteOffset,4))}finally{o.destroy()}}const s=this.device.readPixelsToArrayWebGL(e,{sourceX:t,sourceY:i,sourceWidth:1,sourceHeight:1,sourceAttachment:0});return s?Dt(new Uint8Array(s.buffer,s.byteOffset,4)):null}hasPickInfoChanged(e){return e.objectIndex!==this.pickInfo.objectIndex||e.batchIndex!==this.pickInfo.batchIndex}}const rs=`${Mt}

const COLOR_PICKING_INVALID_INDEX = ${k};
const COLOR_PICKING_MAX_OBJECT_INDEX = 16777214;
const COLOR_PICKING_MAX_BATCH_INDEX = 254;

fn picking_setObjectIndex(objectIndex: i32) -> i32 {
  return objectIndex;
}

fn picking_isObjectHighlighted(objectIndex: i32) -> bool {
  return
    picking.isHighlightActive != 0 &&
    picking.highlightedBatchIndex == picking.batchIndex &&
    picking.highlightedObjectIndex == objectIndex;
}

fn picking_filterHighlightColor(color: vec4<f32>, objectIndex: i32) -> vec4<f32> {
  if (picking.isActive != 0 || !picking_isObjectHighlighted(objectIndex)) {
    return color;
  }

  let highLightAlpha = picking.highlightColor.a;
  let blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);
  if (blendedAlpha == 0.0) {
    return vec4<f32>(color.rgb, 0.0);
  }

  let highLightRatio = highLightAlpha / blendedAlpha;
  let blendedRGB = mix(color.rgb, picking.highlightColor.rgb, highLightRatio);
  return vec4<f32>(blendedRGB, blendedAlpha);
}

fn picking_canEncodePickInfo(objectIndex: i32) -> bool {
  return
    objectIndex != COLOR_PICKING_INVALID_INDEX &&
    objectIndex >= 0 &&
    objectIndex <= COLOR_PICKING_MAX_OBJECT_INDEX &&
    picking.batchIndex >= 0 &&
    picking.batchIndex <= COLOR_PICKING_MAX_BATCH_INDEX;
}

fn picking_getPickingColor(objectIndex: i32) -> vec4<f32> {
  if (!picking_canEncodePickInfo(objectIndex)) {
    return vec4<f32>(0.0, 0.0, 0.0, 0.0);
  }

  let encodedObjectIndex = objectIndex + 1;
  let red = encodedObjectIndex % 256;
  let green = (encodedObjectIndex / 256) % 256;
  let blue = (encodedObjectIndex / 65536) % 256;
  let alpha = picking.batchIndex + 1;

  return vec4<f32>(
    f32(red) / 255.0,
    f32(green) / 255.0,
    f32(blue) / 255.0,
    f32(alpha) / 255.0
  );
}

fn picking_filterPickingColor(color: vec4<f32>, objectIndex: i32) -> vec4<f32> {
  if (picking.isActive != 0) {
    if (!picking_canEncodePickInfo(objectIndex)) {
      discard;
    }
    return picking_getPickingColor(objectIndex);
  }

  return color;
}
`,os=`${ae}

const int INDEX_PICKING_MODE_INSTANCE = 0;
const int INDEX_PICKING_MODE_CUSTOM = 1;

const int COLOR_PICKING_INVALID_INDEX = ${k};

flat out int picking_objectIndex;

void picking_setObjectIndex(int objectIndex) {
  switch (picking.indexMode) {
    case INDEX_PICKING_MODE_INSTANCE:
      picking_objectIndex = gl_InstanceID;
      break;
    case INDEX_PICKING_MODE_CUSTOM:
      picking_objectIndex = objectIndex;
      break;
  }
}
`,as=`${ae}

const int COLOR_PICKING_INVALID_INDEX = ${k};
const int COLOR_PICKING_MAX_OBJECT_INDEX = 16777214;
const int COLOR_PICKING_MAX_BATCH_INDEX = 254;

flat in int picking_objectIndex;

bool picking_isFragmentHighlighted() {
  return
    bool(picking.isHighlightActive) &&
    picking.highlightedBatchIndex == picking.batchIndex &&
    picking.highlightedObjectIndex == picking_objectIndex
    ;
}

vec4 picking_filterHighlightColor(vec4 color) {
  if (bool(picking.isActive)) {
    return color;
  }

  if (!picking_isFragmentHighlighted()) {
    return color;
  }

  float highLightAlpha = picking.highlightColor.a;
  float blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);
  float highLightRatio = highLightAlpha / blendedAlpha;

  vec3 blendedRGB = mix(color.rgb, picking.highlightColor.rgb, highLightRatio);
  return vec4(blendedRGB, blendedAlpha);
}

bool picking_canEncodePickInfo(int objectIndex) {
  return
    objectIndex != COLOR_PICKING_INVALID_INDEX &&
    objectIndex >= 0 &&
    objectIndex <= COLOR_PICKING_MAX_OBJECT_INDEX &&
    picking.batchIndex >= 0 &&
    picking.batchIndex <= COLOR_PICKING_MAX_BATCH_INDEX;
}

vec4 picking_getPickingColor() {
  if (!picking_canEncodePickInfo(picking_objectIndex)) {
    return vec4(0.0);
  }

  int encodedObjectIndex = picking_objectIndex + 1;
  int red = encodedObjectIndex % 256;
  int green = (encodedObjectIndex / 256) % 256;
  int blue = (encodedObjectIndex / 65536) % 256;
  int alpha = picking.batchIndex + 1;

  return vec4(float(red), float(green), float(blue), float(alpha)) / 255.0;
}

vec4 picking_filterPickingColor(vec4 color) {
  if (bool(picking.isActive)) {
    if (!picking_canEncodePickInfo(picking_objectIndex)) {
      discard;
    }
    return picking_getPickingColor();
  }

  return color;
}

vec4 picking_filterColor(vec4 color) {
  vec4 outColor = color;
  outColor = picking_filterHighlightColor(outColor);
  outColor = picking_filterPickingColor(outColor);
  return outColor;
}
`,Ge={...Be,name:"picking",source:rs,vs:os,fs:as},cs=`${Mt}

const INDEX_PICKING_MODE_INSTANCE = 0;
const INDEX_PICKING_MODE_CUSTOM = 1;
const INDEX_PICKING_INVALID_INDEX = ${k}; // 2^32 - 1

/**
 * WGSL shaders need to carry the returned object index through their own stage outputs.
 */
fn picking_setObjectIndex(objectIndex: i32) -> i32 {
  return objectIndex;
}

fn picking_isObjectHighlighted(objectIndex: i32) -> bool {
  return
    picking.isHighlightActive != 0 &&
    picking.highlightedBatchIndex == picking.batchIndex &&
    picking.highlightedObjectIndex == objectIndex;
}

fn picking_filterHighlightColor(color: vec4<f32>, objectIndex: i32) -> vec4<f32> {
  if (picking.isActive != 0 || !picking_isObjectHighlighted(objectIndex)) {
    return color;
  }

  let highLightAlpha = picking.highlightColor.a;
  let blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);
  if (blendedAlpha == 0.0) {
    return vec4<f32>(color.rgb, 0.0);
  }

  let highLightRatio = highLightAlpha / blendedAlpha;
  let blendedRGB = mix(color.rgb, picking.highlightColor.rgb, highLightRatio);
  return vec4<f32>(blendedRGB, blendedAlpha);
}

fn picking_filterPickingColor(color: vec4<f32>, objectIndex: i32) -> vec4<f32> {
  if (picking.isActive != 0 && objectIndex == INDEX_PICKING_INVALID_INDEX) {
    discard;
  }
  return color;
}

fn picking_getPickingColor(objectIndex: i32) -> vec2<i32> {
  return vec2<i32>(objectIndex, picking.batchIndex);
}

`,us=`${ae}

const int INDEX_PICKING_MODE_INSTANCE = 0;
const int INDEX_PICKING_MODE_CUSTOM = 1;

const int INDEX_PICKING_INVALID_INDEX = ${k}; // 2^32 - 1

flat out int picking_objectIndex;

/**
 * Vertex shaders should call this function to set the object index.
 * If using instance or vertex mode, argument will be ignored, 0 can be supplied.
 */
void picking_setObjectIndex(int objectIndex) {
  switch (picking.indexMode) {
    case INDEX_PICKING_MODE_INSTANCE:
      picking_objectIndex = gl_InstanceID;
      break;
    case INDEX_PICKING_MODE_CUSTOM:
      picking_objectIndex = objectIndex;
      break;
  }
}
`,ds=`${ae}

const int INDEX_PICKING_INVALID_INDEX = ${k}; // 2^32 - 1

flat in int picking_objectIndex;

/**
 * Check if this vertex is highlighted (part of the selected batch and object)
 */ 
bool picking_isFragmentHighlighted() {
  return 
    bool(picking.isHighlightActive) &&
    picking.highlightedBatchIndex == picking.batchIndex &&
    picking.highlightedObjectIndex == picking_objectIndex
    ;
}

/**
 * Returns highlight color if this item is selected.
 */
vec4 picking_filterHighlightColor(vec4 color) {
  // If we are still picking, we don't highlight
  if (bool(picking.isActive)) {
    return color;
  }

  // If we are not highlighted, return color as is
  if (!picking_isFragmentHighlighted()) {
    return color;
  }
   
  // Blend in highlight color based on its alpha value
  float highLightAlpha = picking.highlightColor.a;
  float blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);
  float highLightRatio = highLightAlpha / blendedAlpha;

  vec3 blendedRGB = mix(color.rgb, picking.highlightColor.rgb, highLightRatio);
  return vec4(blendedRGB, blendedAlpha);
}

/*
 * Returns picking color if picking enabled else unmodified argument.
 */
ivec4 picking_getPickingColor() {
  // Assumes that colorAttachment0 is rg32int
  // TODO? - we could render indices into a second color attachment and not mess with fragColor
  return ivec4(picking_objectIndex, picking.batchIndex, 0u, 0u);  
}

vec4 picking_filterPickingColor(vec4 color) {
  if (bool(picking.isActive)) {
    if (picking_objectIndex == INDEX_PICKING_INVALID_INDEX) {
      discard;
    }
  }
  return color;
}

/*
 * Returns picking color if picking is enabled if not
 * highlight color if this item is selected, otherwise unmodified argument.
 */
vec4 picking_filterColor(vec4 color) {
  vec4 outColor = color;
  outColor = picking_filterHighlightColor(outColor);
  outColor = picking_filterPickingColor(outColor);
  return outColor;
}
`,Et={...Be,name:"picking",source:cs,vs:us,fs:ds},hs={...Be,name:"picking",source:Et.source,vs:Ge.vs,fs:Ge.fs};class ls{device;framebuffer=null;shaderInputs;constructor(e,t){this.device=e,this.shaderInputs=t}destroy(){this.framebuffer?.destroy()}getFramebuffer(){return this.framebuffer||(this.framebuffer=this.device.createFramebuffer({colorAttachments:["rgba8unorm"],depthStencilAttachment:"depth24plus"})),this.framebuffer}clearPickState(){this.shaderInputs.setProps({picking:{highlightedObjectColor:null}})}beginRenderPass(){const e=this.getFramebuffer();return e.resize(this.device.getCanvasContext().getDevicePixelSize()),this.shaderInputs.setProps({picking:{isActive:!0}}),this.device.beginRenderPass({framebuffer:e,clearColor:[0,0,0,0],clearDepth:1})}updatePickState(e){const t=this.getFramebuffer(),[i,s]=this.getPickPosition(e);let a=[...this.device.readPixelsToArrayWebGL(t,{sourceX:i,sourceY:s,sourceWidth:1,sourceHeight:1})].map(c=>c/255);a[0]+a[1]+a[2]>0||(a=null),this.shaderInputs.setProps({picking:{isActive:!1,highlightedObjectColor:a}})}getPickPosition(e){const t=this.device.getCanvasContext().cssToDevicePixels(e),i=t.x+Math.floor(t.width/2),s=t.y+Math.floor(t.height/2);return[i,s]}}const fs=Kt,gs=j;export{ce as AnimationLoop,Qt as AnimationLoopTemplate,gs as AsyncTexture,yt as BackgroundTextureModel,ue as BufferTransform,Ce as ClipSpace,Ue as Computation,De as ConeGeometry,_n as CubeGeometry,Sn as CylinderGeometry,xn as DirectionalLightModel,j as DynamicTexture,me as GPUGeometry,W as Geometry,de as GroupNode,Dn as IcoSphereGeometry,Zt as KeyFrames,ls as LegacyPickingManager,bt as Material,mt as MaterialFactory,H as Model,yn as ModelNode,he as PickingManager,Fn as PlaneGeometry,ln as PointLightModel,oe as ScenegraphNode,V as ShaderInputs,Yn as ShaderPassRenderer,_t as SphereGeometry,pn as SpotLightModel,Fe as Swap,$n as SwapBuffers,Lt as SwapFramebuffers,Ei as TextureTransform,Jt as Timeline,ke as TruncatedConeGeometry,Qe as cancelAnimationFramePolyfill,Ge as colorPicking,Et as indexPicking,fs as legacyColorPicking,zn as loadImage,Un as loadImageBitmap,ii as makeAnimationLoop,Bn as makeRandomGenerator,hs as picking,Ze as requestAnimationFramePolyfill,ss as resolvePickingBackend,je as resolvePickingMode,Gn as setPathPrefix,Ot as supportsIndexPicking};
//# sourceMappingURL=/sm/e779e700d81e0227bbff56abac178032551d60414bd2853c9d72a9fe61c9af91.map