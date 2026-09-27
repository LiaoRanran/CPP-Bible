/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/gl-bench@1.0.42/dist/gl-bench.module.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
var y=`<div class="gl-box">
  <svg viewBox="0 0 55 60">
    <text x="27" y="56" class="gl-fps">00 FPS</text>
    <text x="28" y="8" class="gl-mem"></text>
    <rect x="0" y="14" rx="4" ry="4" width="55" height="32"></rect>
    <polyline class="gl-chart"></polyline>
  </svg>
  <svg viewBox="0 0 14 60" class="gl-cpu-svg">
    <line x1="7" y1="38" x2="7" y2="11" class="opacity"/>
    <line x1="7" y1="38" x2="7" y2="11" class="gl-cpu" stroke-dasharray="0 27"/>
    <path d="M5.35 43c-.464 0-.812.377-.812.812v1.16c-.783.1972-1.421.812-1.595 1.624h-1.16c-.435 0-.812.348-.812.812s.348.812.812.812h1.102v1.653H1.812c-.464 0-.812.377-.812.812 0 .464.377.812.812.812h1.131c.1943.783.812 1.392 1.595 1.595v1.131c0 .464.377.812.812.812.464 0 .812-.377.812-.812V53.15h1.653v1.073c0 .464.377.812.812.812.464 0 .812-.377.812-.812v-1.131c.783-.1943 1.392-.812 1.595-1.595h1.131c.464 0 .812-.377.812-.812 0-.464-.377-.812-.812-.812h-1.073V48.22h1.102c.435 0 .812-.348.812-.812s-.348-.812-.812-.812h-1.16c-.1885-.783-.812-1.421-1.595-1.624v-1.131c0-.464-.377-.812-.812-.812-.464 0-.812.377-.812.812v1.073H6.162v-1.073c0-.464-.377-.812-.812-.812zm.58 3.48h2.088c.754 0 1.363.609 1.363 1.363v2.088c0 .754-.609 1.363-1.363 1.363H5.93c-.754 0-1.363-.609-1.363-1.363v-2.088c0-.754.609-1.363 1.363-1.363z"/>
  </svg>
  <svg viewBox="0 0 14 60" class="gl-gpu-svg">
    <line x1="7" y1="38" x2="7" y2="11" class="opacity"/>
    <line x1="7" y1="38" x2="7" y2="11" class="gl-gpu" stroke-dasharray="0 27"/>
    <path d="M1.94775 43.3772a.736.736 0 10-.00416 1.472c.58535.00231.56465.1288.6348.3197.07015.18975.04933.43585.04933.43585l-.00653.05405v8.671a.736.736 0 101.472 0v-1.4145c.253.09522.52785.1495.81765.1495h5.267c1.2535 0 2.254-.9752 2.254-2.185v-3.105c0-1.2075-1.00625-2.185-2.254-2.185h-5.267c-.28865 0-.5635.05405-.8165.1495.01806-.16445.04209-.598-.1357-1.0787-.22425-.6072-.9499-1.2765-2.0125-1.2765zm2.9095 3.6455c.42435 0 .7659.36225.7659.8119v2.9785c0 .44965-.34155.8119-.7659.8119s-.7659-.36225-.7659-.8119v-2.9785c0-.44965.34155-.8119.7659-.8119zm4.117 0a2.3 2.3 0 012.3 2.3 2.3 2.3 0 01-2.3 2.3 2.3 2.3 0 01-2.3-2.3 2.3 2.3 0 012.3-2.3z"/>
  </svg>
</div>`,A=`#gl-bench {
  position:absolute;
  left:0;
  top:0;
  z-index:1000;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

#gl-bench div {
  position: relative;
  display: block;
  margin: 4px;
  padding: 0 7px 0 10px;
  background: #6c6;
  border-radius: 15px;
  cursor: pointer;
  opacity: 0.9;
}

#gl-bench svg {
  height: 60px;
  margin: 0 -1px;
}

#gl-bench text {
  font-size: 12px;
  font-family: Helvetica,Arial,sans-serif;
  font-weight: 700;
  dominant-baseline: middle;
  text-anchor: middle;
}

#gl-bench .gl-mem {
  font-size: 9px;
}

#gl-bench line {
  stroke-width: 5;
  stroke: #112211;
  stroke-linecap: round;
}

#gl-bench polyline {
  fill: none;
  stroke: #112211;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 3.5;
}

#gl-bench rect {
  fill: #448844;
}

#gl-bench .opacity {
  stroke: #448844;
}
`;class b{constructor(t,c={}){this.css=A,this.svg=y,this.paramLogger=()=>{},this.chartLogger=()=>{},this.chartLen=20,this.chartHz=20,this.names=[],this.cpuAccums=[],this.gpuAccums=[],this.activeAccums=[],this.chart=new Array(this.chartLen),this.now=()=>performance&&performance.now?performance.now():Date.now(),this.updateUI=()=>{[].forEach.call(this.nodes["gl-gpu-svg"],s=>{s.style.display=this.trackGPU?"inline":"none"})},Object.assign(this,c),this.detected=0,this.finished=[],this.isFramebuffer=0,this.frameId=0;let h,m=0,l,o=s=>{++m<20?h=requestAnimationFrame(o):(this.detected=Math.ceil(1e3*m/(s-l)/70),cancelAnimationFrame(h)),l||(l=s)};if(requestAnimationFrame(o),t){const s=async(n,r)=>Promise.resolve(setTimeout(()=>{t.getError();const i=this.now()-n;r.forEach((e,a)=>{e&&(this.gpuAccums[a]+=i)})},0)),d=(n,r,i)=>function(){const e=r.now();n.apply(i,arguments),r.trackGPU&&r.finished.push(s(e,r.activeAccums.slice(0)))};["drawArrays","drawElements","drawArraysInstanced","drawBuffers","drawElementsInstanced","drawRangeElements"].forEach(n=>{t[n]&&(t[n]=d(t[n],this,t))}),t.getExtension=((n,r)=>function(){let i=n.apply(t,arguments);return i&&["drawElementsInstancedANGLE","drawBuffersWEBGL"].forEach(e=>{i[e]&&(i[e]=d(i[e],r,i))}),i})(t.getExtension,this)}if(!this.withoutUI){this.dom||(this.dom=document.body);let s=document.createElement("div");s.id="gl-bench",this.dom.appendChild(s),this.dom.insertAdjacentHTML("afterbegin",'<style id="gl-bench-style">'+this.css+"</style>"),this.dom=s,this.dom.addEventListener("click",()=>{this.trackGPU=!this.trackGPU,this.updateUI()}),this.paramLogger=((d,n,r)=>{const i=["gl-cpu","gl-gpu","gl-mem","gl-fps","gl-gpu-svg","gl-chart"],e=Object.assign({},i);return i.forEach(a=>e[a]=n.getElementsByClassName(a)),this.nodes=e,(a,p,u,g,f,v,x)=>{e["gl-cpu"][a].style.strokeDasharray=(p*.27).toFixed(0)+" 100",e["gl-gpu"][a].style.strokeDasharray=(u*.27).toFixed(0)+" 100",e["gl-mem"][a].innerHTML=r[a]?r[a]:g?"mem: "+g.toFixed(0)+"mb":"",e["gl-fps"][a].innerHTML=f.toFixed(0)+" FPS",d(r[a],p,u,g,f,v,x)}})(this.paramLogger,this.dom,this.names),this.chartLogger=((d,n)=>{let r={"gl-chart":n.getElementsByClassName("gl-chart")};return(i,e,a)=>{let p="",u=e.length;for(let g=0;g<u;g++){let f=(a+g+1)%u;e[f]!=null&&(p=p+" "+(55*g/(u-1)).toFixed(1)+","+(45-e[f]*22/60/this.detected).toFixed(1))}r["gl-chart"][i].setAttribute("points",p),d(this.names[i],e,a)}})(this.chartLogger,this.dom)}}addUI(t){this.names.indexOf(t)==-1&&(this.names.push(t),this.dom&&(this.dom.insertAdjacentHTML("beforeend",this.svg),this.updateUI()),this.cpuAccums.push(0),this.gpuAccums.push(0),this.activeAccums.push(!1))}nextFrame(t){this.frameId++;const c=t||this.now();if(this.frameId<=1)this.paramFrame=this.frameId,this.paramTime=c;else{let h=c-this.paramTime;if(h>=1e3){const m=this.frameId-this.paramFrame,l=m/h*1e3;for(let o=0;o<this.names.length;o++){const s=this.cpuAccums[o]/h*100,d=this.gpuAccums[o]/h*100,n=performance&&performance.memory?performance.memory.usedJSHeapSize/(1<<20):0;this.paramLogger(o,s,d,n,l,h,m),this.cpuAccums[o]=0,Promise.all(this.finished).then(()=>{this.gpuAccums[o]=0,this.finished=[]})}this.paramFrame=this.frameId,this.paramTime=c}}if(!this.detected||!this.chartFrame)this.chartFrame=this.frameId,this.chartTime=c,this.circularId=0;else{let h=c-this.chartTime,m=this.chartHz*h/1e3;for(;--m>0&&this.detected;){const o=(this.frameId-this.chartFrame)/h*1e3;this.chart[this.circularId%this.chartLen]=o;for(let s=0;s<this.names.length;s++)this.chartLogger(s,this.chart,this.circularId);this.circularId++,this.chartFrame=this.frameId,this.chartTime=c}}}begin(t){this.updateAccums(t)}end(t){this.updateAccums(t)}updateAccums(t){let c=this.names.indexOf(t);c==-1&&(c=this.names.length,this.addUI(t));const h=this.now(),m=h-this.t0;for(let l=0;l<c+1;l++)this.activeAccums[l]&&(this.cpuAccums[l]+=m);this.activeAccums[c]=!this.activeAccums[c],this.t0=h}}export{b as default};
//# sourceMappingURL=/sm/23fa93cc62c8e1af9fdbc4dabd93d5bad9de6cedb2d0bd9315bf32f2b76da1a4.map