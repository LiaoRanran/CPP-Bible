/**
 * Bundled by jsDelivr using Rollup v4.62.2 and esbuild v0.28.1.
 * Original file: /npm/@cosmograph/cosmos@3.4.1/dist/index.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
import{select as N}from"./d3-selection3.0.0.js";import"./d3-transition3.0.1.js";import{easeQuadIn as be,easeQuadOut as Te,easeQuadInOut as J,easeCircleInOut as ut,easeCircleOut as ct,easeCircleIn as ft,easeExpInOut as pt,easeExpOut as mt,easeExpIn as gt,easeSinInOut as vt,easeSinOut as xt,easeSinIn as St,easeCubicInOut as Pt,easeCubicOut as yt,easeCubicIn as Ct,easeLinear as ke}from"./d3-ease3.0.1.js";import{luma as bt,Buffer as x,UniformStore as T,Texture as g,textureFormatDecoder as Tt}from"./luma.gl-core9.3.6.js";import{webgl2Adapter as kt}from"./luma.gl-webgl9.3.6.js";import{color as zt}from"./d3-color3.1.0.js";import wt from"./dompurify3.4.12.js";import{scaleLinear as ze,scalePow as Dt}from"./d3-scale4.0.2.js";import{mat3 as W,vec3 as P,mat4 as O}from"./gl-matrix3.4.4.js";import{Random as Ft}from"./random4.1.0.js";import{Model as b}from"./luma.gl-engine9.3.6.js";import It from"./gl-bench1.0.42.js";import{range as Lt}from"./d3-array3.2.4.js";import{zoomIdentity as X,zoom as we}from"./d3-zoom3.0.0.js";import{drag as Ut}from"./d3-drag3.0.0.js";const ne=.001,ee=64,Bt=4,te=2;class At{constructor(){this.pointsTextureSize=0,this.linksTextureSize=0,this.alpha=1,this.transform=W.create(),this.screenSize=[0,0],this.mousePosition=[0,0],this.mousePosition3D=[0,0,0],this.dragPlanePoint3D=void 0,this.screenMousePosition=[0,0],this.searchArea=[[0,0],[0,0]],this.isSimulationRunning=!1,this.simulationProgress=0,this.maxPointSize=ee,this.hoveredPoint=void 0,this.focusedPoint=void 0,this.draggingPointIndex=void 0,this.hoveredLinkIndex=void 0,this.adjustedSpaceSize=M.spaceSize,this.spaceDimensions=2,this.viewProjection3D=void 0,this.depthFadeRange=[0,1],this.isSpaceKeyPressed=!1,this.webglMaxTextureSize=16384,this.hoveredPointRingColor=[1,1,1,Be],this.focusedPointRingColor=[1,1,1,Ae],this.outlinedPointRingColor=[1,1,1,1],this.highlightedPointSet=void 0,this.outlinedPointSet=void 0,this.hoveredLinkColor=[-1,-1,-1,-1],this.greyoutPointColor=[-1,-1,-1,-1],this.isDarkenGreyout=!1,this.isLinkHoveringEnabled=!1,this.alphaTarget=0,this.scalePointX=ze(),this.scalePointY=ze(),this.random=new Ft,this._backgroundColor=[0,0,0,0],this.alphaDecay=e=>1-Math.pow(ne,1/e)}get backgroundColor(){return this._backgroundColor}get is3D(){return this.spaceDimensions===3}get transformationMatrix4x4(){if(this.is3D&&this.viewProjection3D)return this.viewProjection3D;const e=this.transform;if(e.length!==9)throw new Error(`Transform must be a 9-element array (3x3 matrix), got ${e.length} elements`);return[e[0],e[1],e[2],0,e[3],e[4],e[5],0,e[6],e[7],e[8],0,0,0,0,1]}set backgroundColor(e){this._backgroundColor=e;const t=Le(e[0],e[1],e[2]);document.documentElement.style.setProperty("--cosmosgl-attribution-color",t>.65?"black":"white"),document.documentElement.style.setProperty("--cosmosgl-error-message-color",t>.65?"black":"white"),this.div&&(this.div.style.backgroundColor=`rgba(${e[0]*255}, ${e[1]*255}, ${e[2]*255}, ${e[3]})`),this.isDarkenGreyout=t<.65}addRandomSeed(e){this.random=this.random.clone(e)}getRandomFloat(e,t){return this.random.float(e,t)}adjustSpaceSize(e,t){(e<=0||!isFinite(e))&&(console.error(`Invalid spaceSize value: ${e}. Using default value of ${M.spaceSize}`),e=M.spaceSize);const i=2;if(e<i&&(console.warn(`spaceSize (${e}) is too small. Using minimum value of ${i}`),e=i),!Number.isFinite(t)||t<=0||t<i){console.warn(`Invalid webglMaxTextureSize: ${t}. Using configSpaceSize without WebGL limit adjustment.`),this.adjustedSpaceSize=e;return}e>=t?(this.adjustedSpaceSize=Math.max(t/2,i),console.warn(`The \`spaceSize\` has been reduced to ${this.adjustedSpaceSize} due to WebGL limits`)):this.adjustedSpaceSize=e}setWebGLMaxTextureSize(e){this.webglMaxTextureSize=e}updateScreenSize(e,t){const{adjustedSpaceSize:i}=this;this.screenSize=[e,t],this.scalePointX.domain([0,i]).range([(e-i)/2,(e+i)/2]),this.scalePointY.domain([i,0]).range([(t-i)/2,(t+i)/2])}scaleX(e){return this.scalePointX(e)}scaleY(e){return this.scalePointY(e)}setHoveredPointRingColor(e){const t=E(e);this.hoveredPointRingColor[0]=t[0],this.hoveredPointRingColor[1]=t[1],this.hoveredPointRingColor[2]=t[2]}setFocusedPointRingColor(e){const t=E(e);this.focusedPointRingColor[0]=t[0],this.focusedPointRingColor[1]=t[1],this.focusedPointRingColor[2]=t[2]}setOutlinedPointRingColor(e){const t=E(e);this.outlinedPointRingColor[0]=t[0],this.outlinedPointRingColor[1]=t[1],this.outlinedPointRingColor[2]=t[2],this.outlinedPointRingColor[3]=t[3]}setHighlightedPointSet(e){this.highlightedPointSet=e?new Set(e):void 0}setOutlinedPointSet(e){this.outlinedPointSet=e?new Set(e):void 0}setGreyoutPointColor(e){if(e===void 0){this.greyoutPointColor=[-1,-1,-1,-1];return}const t=E(e);this.greyoutPointColor[0]=t[0],this.greyoutPointColor[1]=t[1],this.greyoutPointColor[2]=t[2],this.greyoutPointColor[3]=t[3]}updateLinkHoveringEnabled(e){this.isLinkHoveringEnabled=!!(e.onLinkClick||e.onLinkContextMenu||e.onLinkMouseOver||e.onLinkMouseOut),this.isLinkHoveringEnabled||(this.hoveredLinkIndex=void 0)}setHoveredLinkColor(e){if(e===void 0){this.hoveredLinkColor=[-1,-1,-1,-1];return}const t=E(e);this.hoveredLinkColor[0]=t[0],this.hoveredLinkColor[1]=t[1],this.hoveredLinkColor[2]=t[2],this.hoveredLinkColor[3]=t[3]}setFocusedPoint(e){e!==void 0?this.focusedPoint={index:e}:this.focusedPoint=void 0}addAlpha(e){return(this.alphaTarget-this.alpha)*this.alphaDecay(e)}}const De=h=>typeof h=="function",ae=h=>Array.isArray(h),Fe=h=>h instanceof Object,Ie=h=>h instanceof Object?h.constructor.name!=="Function"&&h.constructor.name!=="Object":!1,Rt=h=>Fe(h)&&!ae(h)&&!De(h)&&!Ie(h);function E(h){let e;if(ae(h))e=h;else{const t=zt(h),i=t?.rgb();e=[(i?.r??0)/255,(i?.g??0)/255,(i?.b??0)/255,t?.opacity??1]}return e}function Le(h,e,t){return .2126*h+.7152*e+.0722*t}function B(h,e,t=0,i=0,o,s){return h.readPixelsToArrayWebGL(e,{sourceX:t,sourceY:i,sourceWidth:o,sourceHeight:s})}function le(h){const e=[];for(let t=0;t<h.length;t+=4)h[t]!==0&&e.push(t/4);return e}function de(h,e){switch(h.info.type){case"webgl":{const t=h.gl,i=t.getParameter(t.ALIASED_POINT_SIZE_RANGE);return(i?.[1]??ee)/e}case"webgpu":return ee/e;default:return ee/e}}function H(h,e,t){return Math.min(Math.max(h,e),t)}function _(h){return h!=null&&!Number.isNaN(h)}function q(h,e,t=2){const i=e*t;return Number.isNaN(h[i])||Number.isNaN(h[i+1])?!0:t===3&&Number.isNaN(h[i+2])}function Ue(h,e){return wt.sanitize(h,{ALLOWED_TAGS:["a","b","i","em","strong","span","div","p","br"],ALLOWED_ATTR:["href","target","class","id","style"],ALLOW_DATA_ATTR:!1,...e})}var he=(h=>(h[h.Circle=0]="Circle",h[h.Square=1]="Square",h[h.Triangle=2]="Triangle",h[h.Diamond=3]="Diamond",h[h.Pentagon=4]="Pentagon",h[h.Hexagon=5]="Hexagon",h[h.Star=6]="Star",h[h.Cross=7]="Cross",h[h.None=8]="None",h))(he||{}),ue=(h=>(h[h.Solid=0]="Solid",h[h.Dashed=1]="Dashed",h[h.Dotted=2]="Dotted",h))(ue||{});class Mt{constructor(e){this.inputPointDimensions=2,this.inputClusterPositionsDimensions=2,this.pointDimensions=2,this.sourcePointsNumber=0,this.targetPointsNumber=0,this.clusterPositionsDimensions=2,this._config=e}get pointsNumber(){return this.pointPositions&&Math.trunc(this.pointPositions.length/this.pointDimensions)}get defaultRgba(){return this._defaultRgba??(this._defaultRgba=E(this._config.pointDefaultColor)),this._defaultRgba}get linksNumber(){return this.links&&Math.trunc(this.links.length/2)}hasPointAbsenceChanged(){const e=this.pointPositions,t=this.inputPointPositions;if(!e||!t||e===t)return!1;const i=this.pointDimensions,o=this.inputPointDimensions,s=Math.min(e.length/i,t.length/o);for(let r=0;r<s;r++)if(q(e,r,i)!==q(t,r,o))return!0;return!1}isPointAbsent(e){return this.pointPositions?q(this.pointPositions,e,this.pointDimensions):!1}updatePoints(){this.pointPositions!==this.inputPointPositions&&(this.sourcePointsNumber=this.pointPositions?Math.trunc(this.pointPositions.length/this.pointDimensions):0,this.pointPositions=this.inputPointPositions,this.pointDimensions=this.inputPointDimensions,this.targetPointsNumber=this.pointPositions?Math.trunc(this.pointPositions.length/this.pointDimensions):0)}updatePointColor(){if(this.pointsNumber===void 0){this.pointColors=void 0;return}this._defaultRgba=void 0,this.inputPointColors===void 0||this.inputPointColors.length/4!==this.pointsNumber?this.pointColors=new Float32Array(this.pointsNumber*4).fill(NaN):this.pointColors=this.inputPointColors}getResolvedPointColorChannel(e,t){var i;const o=(i=this.pointColors)==null?void 0:i[e*4+t];return _(o)?o:this.isPointAbsent(e)?Y:this.defaultRgba[t]}updatePointSize(){if(this.pointsNumber===void 0){this.pointSizes=void 0;return}this.inputPointSizes===void 0||this.inputPointSizes.length!==this.pointsNumber?this.pointSizes=new Float32Array(this.pointsNumber).fill(NaN):this.pointSizes=this.inputPointSizes}getResolvedPointSize(e){var t;const i=(t=this.pointSizes)==null?void 0:t[e];return _(i)?i:this.isPointAbsent(e)?ie:this._config.pointDefaultSize}updatePointShape(){if(this.pointsNumber===void 0){this.pointShapes=void 0;return}const{pointDefaultShape:e}=this._config,t=typeof e=="string"?Number(e):e,i=Number.isInteger(t)&&t>=0&&t<=8?t:M.pointDefaultShape;if(this.inputPointShapes===void 0||this.inputPointShapes.length!==this.pointsNumber)this.pointShapes=new Float32Array(this.pointsNumber).fill(i);else{this.pointShapes=new Float32Array(this.inputPointShapes);const o=this.pointShapes;for(let s=0;s<o.length;s++){const r=o[s]??-1;(!Number.isInteger(r)||r<0||r>8)&&(o[s]=i)}}}updatePointImageIndices(){if(this.pointsNumber===void 0){this.pointImageIndices=void 0;return}if(this.inputPointImageIndices===void 0||this.inputPointImageIndices.length!==this.pointsNumber)this.pointImageIndices=new Float32Array(this.pointsNumber).fill(-1);else{const e=new Float32Array(this.inputPointImageIndices);for(let t=0;t<e.length;t++){const i=e[t],o=i===void 0?NaN:i;!Number.isFinite(o)||o<0?e[t]=-1:e[t]=Math.trunc(o)}this.pointImageIndices=e}}updatePointImageSizes(){if(this.pointsNumber===void 0){this.pointImageSizes=void 0;return}if(this.inputPointImageSizes===void 0||this.inputPointImageSizes.length!==this.pointsNumber){this.pointImageSizes=new Float32Array(this.pointsNumber);for(let e=0;e<this.pointsNumber;e++)this.pointImageSizes[e]=this.getResolvedPointSize(e)}else{this.pointImageSizes=new Float32Array(this.inputPointImageSizes);for(let e=0;e<this.pointImageSizes.length;e++)_(this.pointImageSizes[e])||(this.pointImageSizes[e]=this.getResolvedPointSize(e))}}updateLinks(){this.links=this.inputLinks}updateLinkColor(){if(this.linksNumber===void 0){this.linkColors=void 0;return}const e=E(this._config.linkDefaultColor);if(this.inputLinkColors===void 0||this.inputLinkColors.length/4!==this.linksNumber){this.linkColors=new Float32Array(this.linksNumber*4);for(let t=0;t<this.linkColors.length/4;t++)this.linkColors[t*4]=e[0],this.linkColors[t*4+1]=e[1],this.linkColors[t*4+2]=e[2],this.linkColors[t*4+3]=e[3]}else{this.linkColors=this.inputLinkColors;for(let t=0;t<this.linkColors.length/4;t++)_(this.linkColors[t*4])||(this.linkColors[t*4]=e[0]),_(this.linkColors[t*4+1])||(this.linkColors[t*4+1]=e[1]),_(this.linkColors[t*4+2])||(this.linkColors[t*4+2]=e[2]),_(this.linkColors[t*4+3])||(this.linkColors[t*4+3]=e[3])}}updateLinkWidth(){if(this.linksNumber===void 0){this.linkWidths=void 0;return}const e=this._config.linkDefaultWidth;if(this.inputLinkWidths===void 0||this.inputLinkWidths.length!==this.linksNumber)this.linkWidths=new Float32Array(this.linksNumber).fill(e);else{this.linkWidths=this.inputLinkWidths;for(let t=0;t<this.linkWidths.length;t++)_(this.linkWidths[t])||(this.linkWidths[t]=e)}}updateLinkStyles(){if(this.linksNumber===void 0){this.linkStyles=void 0;return}const{linkDefaultStyle:e}=this._config,t=typeof e=="string"?Number(e):e,i=Number.isInteger(t)&&t>=0&&t<=2?t:M.linkDefaultStyle;if(this.inputLinkStyles===void 0||this.inputLinkStyles.length!==this.linksNumber)this.linkStyles=new Float32Array(this.linksNumber).fill(i);else{this.linkStyles=new Float32Array(this.inputLinkStyles);const o=this.linkStyles;for(let s=0;s<o.length;s++){const r=o[s]??-1;(!Number.isInteger(r)||r<0||r>2)&&(o[s]=i)}}}updateArrows(){if(this.linksNumber===void 0){this.linkArrows=void 0;return}const e=this._config.linkDefaultArrows;this.linkArrowsBoolean===void 0||this.linkArrowsBoolean.length!==this.linksNumber?this.linkArrows=new Array(this.linksNumber).fill(+e):this.linkArrows=this.linkArrowsBoolean.map(t=>+t)}updateLinkStrength(){this.linksNumber===void 0&&(this.linkStrength=void 0),this.inputLinkStrength===void 0||this.inputLinkStrength.length!==this.linksNumber?this.linkStrength=void 0:this.linkStrength=this.inputLinkStrength}updateClusters(){if(this.pointsNumber===void 0){this.pointClusters=void 0,this.clusterPositions=void 0;return}this.inputPointClusters===void 0||this.inputPointClusters.length!==this.pointsNumber?this.pointClusters=void 0:this.pointClusters=this.inputPointClusters,this.inputClusterPositions===void 0?this.clusterPositions=void 0:(this.clusterPositions=this.inputClusterPositions,this.clusterPositionsDimensions=this.inputClusterPositionsDimensions),this.inputClusterStrength===void 0||this.inputClusterStrength.length!==this.pointsNumber?this.clusterStrength=void 0:this.clusterStrength=this.inputClusterStrength}update(){this.updatePoints(),this.updatePointColor(),this.updatePointSize(),this.updatePointShape(),this.updatePointImageIndices(),this.updatePointImageSizes(),this.updateLinks(),this.updateLinkColor(),this.updateLinkWidth(),this.updateArrows(),this.updateLinkStyles(),this.updateLinkStrength(),this.updateClusters(),this._createAdjacencyLists(),this._calculateDegrees()}getNeighboringPointIndices(e){var t,i;const o=Array.isArray(e)?e:[e],s=this.pointsNumber??0,r=new Set;for(const n of o)if(!(n<0||n>=s)){for(const[a]of((t=this.sourceIndexToTargetIndices)==null?void 0:t[n])??[])r.add(a);for(const[a]of((i=this.targetIndexToSourceIndices)==null?void 0:i[n])??[])r.add(a)}return[...r]}getConnectedLinkIndices(e){var t;const i=Array.isArray(e)?e:[e],o=this.pointsNumber??0,s=new Set(i),r=new Set;for(const n of s)if(!(n<0||n>=o))for(const[a,l]of((t=this.sourceIndexToTargetIndices)==null?void 0:t[n])??[])s.has(a)&&r.add(l);return[...r]}getConnectedPointIndices(e){const t=Array.isArray(e)?e:[e],i=new Set;if(this.links===void 0)return[];const o=this.linksNumber??0;for(const s of t){if(s<0||s>=o)continue;const r=this.links[s*2],n=this.links[s*2+1];r!==void 0&&i.add(r),n!==void 0&&i.add(n)}return[...i]}_createAdjacencyLists(){var e,t;if(this.linksNumber===void 0||this.links===void 0){this.sourceIndexToTargetIndices=void 0,this.targetIndexToSourceIndices=void 0;return}this.sourceIndexToTargetIndices=new Array(this.pointsNumber).fill(void 0),this.targetIndexToSourceIndices=new Array(this.pointsNumber).fill(void 0);for(let i=0;i<this.linksNumber;i++){const o=this.links[i*2],s=this.links[i*2+1];o!==void 0&&s!==void 0&&(this.sourceIndexToTargetIndices[o]===void 0&&(this.sourceIndexToTargetIndices[o]=[]),(e=this.sourceIndexToTargetIndices[o])==null||e.push([s,i]),this.targetIndexToSourceIndices[s]===void 0&&(this.targetIndexToSourceIndices[s]=[]),(t=this.targetIndexToSourceIndices[s])==null||t.push([o,i]))}}_calculateDegrees(){var e,t,i,o;if(this.pointsNumber===void 0){this.degree=void 0,this.inDegree=void 0,this.outDegree=void 0;return}this.degree=new Array(this.pointsNumber).fill(0),this.inDegree=new Array(this.pointsNumber).fill(0),this.outDegree=new Array(this.pointsNumber).fill(0);for(let s=0;s<this.pointsNumber;s++)this.inDegree[s]=((t=(e=this.targetIndexToSourceIndices)==null?void 0:e[s])==null?void 0:t.length)??0,this.outDegree[s]=((o=(i=this.sourceIndexToTargetIndices)==null?void 0:i[s])==null?void 0:o.length)??0,this.degree[s]=(this.inDegree[s]??0)+(this.outDegree[s]??0)}}var F=(h=>(h.Positions="positions",h.PointColors="pointColors",h.PointSizes="pointSizes",h.LinkColors="linkColors",h.LinkWidths="linkWidths",h))(F||{}),ce=(h=>(h.Linear="linear",h.QuadIn="quad-in",h.QuadOut="quad-out",h.QuadInOut="quad-in-out",h.CubicIn="cubic-in",h.CubicOut="cubic-out",h.CubicInOut="cubic-in-out",h.SinIn="sin-in",h.SinOut="sin-out",h.SinInOut="sin-in-out",h.ExpIn="exp-in",h.ExpOut="exp-out",h.ExpInOut="exp-in-out",h.CircleIn="circle-in",h.CircleOut="circle-out",h.CircleInOut="circle-in-out",h))(ce||{});const Nt={linear:ke,"quad-in":be,"quad-out":Te,"quad-in-out":J,"cubic-in":Ct,"cubic-out":yt,"cubic-in-out":Pt,"sin-in":St,"sin-out":xt,"sin-in-out":vt,"exp-in":gt,"exp-out":mt,"exp-in-out":pt,"circle-in":ft,"circle-out":ct,"circle-in-out":ut};class Et{constructor(e){this.progress=1,this.startTime=0,this.pendingProperties=new Set,this.activeProperties=new Set,this.activeDuration=0,this.config=e}get duration(){return this.overrideDuration??this.config.transitionDuration}get isPending(){return this.pendingProperties.size>0}get isActive(){return this.activeProperties.size>0}setDurationOverride(e){this.overrideDuration=e!==void 0&&Number.isFinite(e)?e:void 0}isPendingFor(e){return this.pendingProperties.has(e)}isActiveFor(e){return this.activeProperties.has(e)}queue(e){this.pendingProperties.add(e)}dequeue(e){this.pendingProperties.delete(e)}start(){var e,t,i,o;const s=this.duration;if(this.overrideDuration=void 0,!!this.isPending){if(s<=0){const r=this.isActive;this.pendingProperties.clear(),this.clearActiveCycle(),r&&((t=(e=this.config).onTransitionEnd)==null||t.call(e,!0));return}this.isActive&&this.end(!0),this.activeDuration=s,this.startTime=performance.now(),this.progress=0,this.activeProperties=new Set(this.pendingProperties),this.pendingProperties.clear(),(o=(i=this.config).onTransitionStart)==null||o.call(i)}}step(){var e,t;if(!this.isActive)return;const i=this.activeDuration;if(i<=0){this.end(!0);return}const o=Math.min((performance.now()-this.startTime)/i,1),s=this.applyEasing(o);this.progress=s,(t=(e=this.config).onTransition)==null||t.call(e,s),o>=1&&this.end(!1)}end(e){var t,i;this.isActive&&(this.clearActiveCycle(),(i=(t=this.config).onTransitionEnd)==null||i.call(t,e))}abort(){this.pendingProperties.clear(),this.overrideDuration=void 0,this.clearActiveCycle()}applyEasing(e){return(Nt[this.config.transitionEasing]??ke)(e)}clearActiveCycle(){this.startTime=0,this.progress=1,this.activeProperties.clear()}}const M={enableSimulation:!0,transitionDuration:800,transitionEasing:ce.CubicInOut,backgroundColor:"#222222",spaceSize:4096,spaceDimensions:2,pointDefaultColor:"#b3b3b3",pointDefaultSize:4,pointDefaultShape:he.Circle,pointOpacity:1,pointGreyoutOpacity:void 0,pointGreyoutColor:void 0,pointSizeScale:1,pointOcclusionCulling:!0,pointDepthFade:.4,pointSphereShading:!1,scalePointsOnZoom:!1,hoveredPointCursor:"auto",renderHoveredPointRing:!1,hoveredPointRingColor:"white",focusedPointRingColor:"white",focusedPointIndex:void 0,highlightedPointIndices:void 0,outlinedPointIndices:void 0,outlinedPointRingColor:"white",renderLinks:!0,linkDefaultColor:"#666666",linkDefaultWidth:1,linkDefaultStyle:ue.Solid,linkDashLength:8,linkDashGap:4,linkColorInterpolateFromEndpoints:!1,linkOpacity:1,linkGreyoutOpacity:.1,linkWidthScale:1,scaleLinksOnZoom:!1,linkBlending:!0,curvedLinks:!1,curvedLinkSegments:19,curvedLinkWeight:.8,curvedLinkControlPointDistance:.5,linkDefaultArrows:!1,linkArrowsSizeScale:1,linkVisibilityDistanceRange:[50,150],linkVisibilityMinTransparency:.25,hoveredLinkCursor:"auto",hoveredLinkColor:void 0,hoveredLinkWidthIncrease:5,highlightedLinkIndices:void 0,focusedLinkIndex:void 0,focusedLinkWidthIncrease:5,simulationDecay:5e3,simulationGravity:.25,simulationCenter:0,simulationRepulsion:1,simulationRepulsionTheta:1.15,simulationLinkSpring:1,simulationLinkDistance:10,simulationLinkDistRandomVariationRange:[1,1.2],simulationFriction:.85,simulationCluster:.1,simulationCollision:0,simulationCollisionRadius:void 0,simulationCollisionPadding:0,simulationCollisionIterations:1,simulationAlphaOnDrag:.3,onSimulationStart:void 0,onSimulationTick:void 0,onSimulationEnd:void 0,onSimulationPause:void 0,onSimulationUnpause:void 0,onTransitionStart:void 0,onTransition:void 0,onTransitionEnd:void 0,onClick:void 0,onPointClick:void 0,onLinkClick:void 0,onBackgroundClick:void 0,onContextMenu:void 0,onPointContextMenu:void 0,onLinkContextMenu:void 0,onBackgroundContextMenu:void 0,onMouseMove:void 0,onPointMouseOver:void 0,onPointMouseOut:void 0,onLinkMouseOver:void 0,onLinkMouseOut:void 0,onZoomStart:void 0,onZoom:void 0,onZoomEnd:void 0,onDragStart:void 0,onDrag:void 0,onDragEnd:void 0,showFPSMonitor:!1,pixelRatio:typeof window<"u"&&window.devicePixelRatio||2,enableZoom:!0,enableSimulationDuringZoom:!1,initialZoomLevel:void 0,enableDrag:!1,fitViewOnInit:!0,fitViewDelay:250,fitViewPadding:.1,fitViewDuration:250,fitViewByPointsInRect:void 0,fitViewByPointIndices:void 0,pointSamplingDistance:100,linkSamplingDistance:100,randomSeed:void 0,rescalePositions:void 0,attribution:"",cameraFov:45,cameraNear:void 0,cameraFar:void 0,cameraInitialPosition:void 0},Be=.7,Ae=.95,ie=0,Y=0;function Re(){const h={};for(const[e,t]of Object.entries(M))h[e]=Array.isArray(t)?[...t]:t;return h}function _t(h){Object.assign(h,Re())}function fe(h,e,t=!1){const i={};for(const[o,s]of Object.entries(e))if(s!==void 0)i[o]=s;else if(t){const r=M[o];i[o]=Array.isArray(r)?[...r]:r}Object.assign(h,i)}class V{constructor(e,t,i,o,s){this._debugRandomNumber=Math.floor(Math.random()*1e3),this.device=e,this.config=t,this.store=i,this.data=o,s&&(this.points=s)}}const Ot=`#version 300 es
precision highp float;

in vec4 rgba;
out vec4 fragColor;

void main() {
  fragColor = rgba;
}`,Vt=`#version 300 es
precision highp float;

uniform sampler2D positionsTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform calculateCentermassUniforms {
  float pointsTextureSize;
} calculateCentermass;

#define pointsTextureSize calculateCentermass.pointsTextureSize
#else
uniform float pointsTextureSize;
#endif

in vec2 pointIndices;

out vec4 rgba;

void main() {
  rgba = vec4(0.0);

  // Absent points must not contribute to the centroid \u2014 a NaN position would
  // poison the sum and break the force for every point. (exit.G = current absence)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  // Additive blend accumulates: [sum(x), sum(y), count, sum(z)].
  // z lives in the position alpha channel and is 0 in 2D mode.
  rgba = vec4(pointPosition.xy, 1.0, pointPosition.a);

  gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
  gl_PointSize = 1.0;
}
`,Gt=`#version 300 es
precision highp float;

uniform sampler2D positionsTexture;
uniform sampler2D centermassTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceCenterUniforms {
  float centerForce;
  float alpha;
} forceCenter;

#define centerForce forceCenter.centerForce
#define alpha forceCenter.alpha
#else
uniform float centerForce;
uniform float alpha;
#endif

in vec2 textureCoords;
out vec4 fragColor;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec4 velocity = vec4(0.0);
  vec4 centermassValues = texture(centermassTexture, vec2(0.0));

  #ifdef SPACE_3D
  // Centermass accumulates [sum(x), sum(y), count, sum(z)]; z velocity goes to blue.
  vec3 centermassPosition = vec3(centermassValues.xy, centermassValues.a) / centermassValues.b;
  vec3 position = vec3(pointPosition.xy, pointPosition.a);
  vec3 distVector = centermassPosition - position;
  float dist = length(distVector);
  if (dist > 0.0) {
    float addV = alpha * centerForce * dist * 0.01;
    velocity.rgb += addV * (distVector / dist);
  }
  #else
  vec2 centermassPosition = centermassValues.xy / centermassValues.b;
  vec2 distVector = centermassPosition - pointPosition.xy;
  float dist = sqrt(dot(distVector, distVector));
  if (dist > 0.0) {
    float angle = atan(distVector.y, distVector.x);
    float addV = alpha * centerForce * dist * 0.01;
    velocity.rg += addV * vec2(cos(angle), sin(angle));
  }
  #endif

  fragColor = velocity;
}`;function K(h){const e=new Float32Array(h*h*2);for(let t=0;t<h;t++)for(let i=0;i<h;i++){const o=t*h*2+i*2;e[o+0]=i,e[o+1]=t}return e}function Me(h,e,t){return!e||e.byteLength!==t.byteLength?(e&&!e.destroyed&&e.destroy(),h.createBuffer({data:t,usage:x.VERTEX|x.COPY_DST})):(e.write(t),e)}function oe(h,e,t,i,o,s){const r=o?o.length/s:0,n=e.length/s;if(r===n&&t&&!t.destroyed&&i&&!i.destroyed){const u=i,d=t;return d.write(e),{source:u,target:d,previous:new Float32Array(e)}}const a=new Float32Array(e.length),l=Math.min(r,n);for(let u=0;u<l*s;u+=1)a[u]=o?.[u]??e[u]??0;for(let u=l*s;u<e.length;u+=1)a[u]=e[u]??0;return t&&!t.destroyed&&t.destroy(),i&&!i.destroyed&&i.destroy(),{source:h.createBuffer({data:a,usage:x.VERTEX|x.COPY_DST}),target:h.createBuffer({data:e,usage:x.VERTEX|x.COPY_DST}),previous:new Float32Array(e)}}function y(h,e){const t=Tt.getInfo(h);return e*(t.bytesPerPixel??0)}const U=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec2 vertexCoord; // Vertex coordinates in normalized device coordinates
out vec2 textureCoords; // Texture coordinates to pass to the fragment shader

void main() {
    // Convert vertex coordinates from [-1, 1] range to [0, 1] range for texture sampling
    textureCoords = (vertexCoord + 1.0) / 2.0;
    gl_Position = vec4(vertexCoord, 0, 1);
}
`;class Ne extends V{constructor(){super(...arguments),this.programsSpaceDimensions=2}create(){var e;const{device:t,store:i}=this,{pointsTextureSize:o}=i;if(o){if(this.centermassTexture||(this.centermassTexture=t.createTexture({width:1,height:1,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST})),this.centermassTexture.copyImageData({data:new Float32Array(4).fill(0),bytesPerRow:y("rgba32float",1),mipLevel:0,x:0,y:0}),this.centermassFbo||(this.centermassFbo=t.createFramebuffer({width:1,height:1,colorAttachments:[this.centermassTexture]})),!this.pointIndices||this.previousPointsTextureSize!==i.pointsTextureSize){this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy();const s=K(i.pointsTextureSize);this.pointIndices=t.createBuffer({data:s,usage:x.VERTEX|x.COPY_DST}),(e=this.calculateCentermassCommand)==null||e.setAttributes({pointIndices:this.pointIndices})}this.previousPointsTextureSize=o}}initPrograms(){const{device:e,store:t,points:i}=this;!i||!t.pointsTextureSize||!this.centermassFbo||this.centermassFbo.destroyed||!this.centermassTexture||this.centermassTexture.destroyed||(this.programsSpaceDimensions!==t.spaceDimensions&&(this.programsSpaceDimensions=t.spaceDimensions,this.runCommand&&(this.runCommand.destroy(),this.runCommand=void 0)),this.forceVertexCoordBuffer||(this.forceVertexCoordBuffer=e.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.calculateUniformStore||(this.calculateUniformStore=new T(e,{calculateCentermassUniforms:{uniformTypes:{pointsTextureSize:"f32"}}})),this.forceUniformStore||(this.forceUniformStore=new T(e,{forceCenterUniforms:{uniformTypes:{centerForce:"f32",alpha:"f32"}}})),this.calculateCentermassCommand||(this.calculateCentermassCommand=new b(e,{fs:Ot,vs:Vt,topology:"point-list",attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{calculateCentermassUniforms:this.calculateUniformStore.getManagedUniformBuffer("calculateCentermassUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.calculateCentermassCommand.setVertexCount(this.data.pointsNumber??0),this.runCommand||(this.runCommand=new b(e,{fs:Gt,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...t.is3D?{SPACE_3D:!0}:{}},bindings:{forceCenterUniforms:this.forceUniformStore.getManagedUniformBuffer("forceCenterUniforms")},parameters:{depthWriteEnabled:!1,depthCompare:"always"}})))}run(){const{device:e,store:t,points:i}=this;if(!i||!this.calculateCentermassCommand||!this.calculateUniformStore||!this.runCommand||!this.forceUniformStore||!this.centermassFbo||!this.centermassTexture||!i.previousPositionTexture||i.previousPositionTexture.destroyed||!i.exitTexture||i.exitTexture.destroyed||!i.velocityFbo||i.velocityFbo.destroyed||t.pointsTextureSize!==this.previousPointsTextureSize||!this.pointIndices)return;const o=e.beginRenderPass({framebuffer:this.centermassFbo,clearColor:[0,0,0,0]});this.calculateUniformStore.setUniforms({calculateCentermassUniforms:{pointsTextureSize:t.pointsTextureSize??0}}),this.calculateCentermassCommand.setBindings({positionsTexture:i.previousPositionTexture,exitTexture:i.exitTexture}),this.calculateCentermassCommand.draw(o),o.end(),this.forceUniformStore.setUniforms({forceCenterUniforms:{centerForce:this.config.simulationCenter,alpha:t.alpha}}),this.runCommand.setBindings({positionsTexture:i.previousPositionTexture,centermassTexture:this.centermassTexture});const s=e.beginRenderPass({framebuffer:i.velocityFbo,clearColor:[0,0,0,0]});this.runCommand.draw(s),s.end()}destroy(){var e,t,i,o;(e=this.calculateCentermassCommand)==null||e.destroy(),this.calculateCentermassCommand=void 0,(t=this.runCommand)==null||t.destroy(),this.runCommand=void 0,this.centermassFbo&&!this.centermassFbo.destroyed&&this.centermassFbo.destroy(),this.centermassFbo=void 0,this.centermassTexture&&!this.centermassTexture.destroyed&&this.centermassTexture.destroy(),this.centermassTexture=void 0,(i=this.calculateUniformStore)==null||i.destroy(),this.calculateUniformStore=void 0,(o=this.forceUniformStore)==null||o.destroy(),this.forceUniformStore=void 0,this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy(),this.pointIndices=void 0,this.forceVertexCoordBuffer&&!this.forceVertexCoordBuffer.destroyed&&this.forceVertexCoordBuffer.destroy(),this.forceVertexCoordBuffer=void 0,this.previousPointsTextureSize=void 0}}const Wt=`#version 300 es
precision highp float;

uniform sampler2D positionsTexture;
uniform sampler2D sizeTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform buildGridUniforms {
  float pointsTextureSize;
  float gridTextureSize;   // Cells per axis
  float cellSize;
  float tilesPerRow;        // 3D only: z-slices per texture row (tiled layout)
  float gridTextureWidth;   // 3D only: tiled texture dimensions in pixels
  float gridTextureHeight;
  vec3 gridOffset;          // Offset for multi-pass (0-1 range, multiplied by cellSize)
} buildGrid;

#define pointsTextureSize buildGrid.pointsTextureSize
#define gridTextureSize buildGrid.gridTextureSize
#define cellSize buildGrid.cellSize
#define tilesPerRow buildGrid.tilesPerRow
#define gridTextureWidth buildGrid.gridTextureWidth
#define gridTextureHeight buildGrid.gridTextureHeight
#define gridOffset buildGrid.gridOffset
#else
uniform float pointsTextureSize;
uniform float gridTextureSize;
uniform float cellSize;
uniform float tilesPerRow;
uniform float gridTextureWidth;
uniform float gridTextureHeight;
uniform vec3 gridOffset;
#endif

in vec2 pointIndices;

// 2D: xy = position sum, z = size sum, w = count
// 3D: xyz = position sum, w = count (the force pass approximates neighbor radii
// with the reading point's own radius \u2014 no channel is left for a size sum)
out vec4 cellData;

void main() {
  // Absent points must not enter the grid \u2014 a NaN position bins to a NaN cell and
  // poisons the accumulated position/size sum for every point in that cell. (exit.g = absent)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    cellData = vec4(0.0);
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);

#ifdef SPACE_3D
  // The position texture stores z in the alpha channel
  vec3 position = vec3(pointPosition.xy, pointPosition.a);
  cellData = vec4(position, 1.0);

  // Apply grid offset for multi-pass collision detection
  vec3 offsetPosition = position + gridOffset * cellSize;

  int gridSize = int(gridTextureSize);
  ivec3 cell = clamp(ivec3(floor(offsetPosition / cellSize)), ivec3(0), ivec3(gridSize - 1));

  // z-slices are tiled into a 2D texture (same layout as the octree levels)
  int rowTiles = int(tilesPerRow);
  ivec2 pixel = ivec2(
    (cell.z % rowTiles) * gridSize + cell.x,
    (cell.z / rowTiles) * gridSize + cell.y
  );
  vec2 gridPosition = 2.0 * (vec2(pixel) + 0.5) / vec2(gridTextureWidth, gridTextureHeight) - 1.0;
#else
  // Output: position sum, size sum, count
  vec4 pointSize = texture(sizeTexture, (pointIndices + 0.5) / pointsTextureSize);
  cellData = vec4(pointPosition.xy, pointSize.r, 1.0);

  // Apply grid offset for multi-pass collision detection
  vec2 offsetPosition = pointPosition.xy + gridOffset.xy * cellSize;

  // Calculate which grid cell this point belongs to
  float cellX = floor(offsetPosition.x / cellSize);
  float cellY = floor(offsetPosition.y / cellSize);

  // Clamp to grid bounds
  cellX = clamp(cellX, 0.0, gridTextureSize - 1.0);
  cellY = clamp(cellY, 0.0, gridTextureSize - 1.0);

  // Convert to clip space coordinates
  vec2 gridPosition = 2.0 * (vec2(cellX, cellY) + 0.5) / gridTextureSize - 1.0;
#endif

  gl_Position = vec4(gridPosition, 0.0, 1.0);
  gl_PointSize = 1.0;
}
`,Ht=`#version 300 es
precision highp float;

in vec4 cellData;
out vec4 fragColor;

void main() {
  // Output accumulated cell data (blended additively)
  // xy = sum of positions, z = sum of sizes, w = count
  fragColor = cellData;
}
`,jt=`#version 300 es
precision highp float;

uniform sampler2D positionsTexture;
uniform sampler2D sizeTexture;
uniform sampler2D gridTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceCollisionUniforms {
  float pointsTextureSize;
  float gridTextureSize;   // Cells per axis
  float cellSize;
  float alpha;
  float collisionStrength;
  float collisionRadius;
  float collisionPadding;
  float pointsNumber;
  float tilesPerRow;        // 3D only: z-slices per texture row (tiled layout)
  float passesCount;        // Number of offset passes the force is split across
  vec3 gridOffset;          // Must match the offset used when building the grid
} forceCollision;

#define pointsTextureSize forceCollision.pointsTextureSize
#define gridTextureSize forceCollision.gridTextureSize
#define cellSize forceCollision.cellSize
#define alpha forceCollision.alpha
#define collisionStrength forceCollision.collisionStrength
#define collisionRadius forceCollision.collisionRadius
#define collisionPadding forceCollision.collisionPadding
#define pointsNumber forceCollision.pointsNumber
#define tilesPerRow forceCollision.tilesPerRow
#define passesCount forceCollision.passesCount
#define gridOffset forceCollision.gridOffset
#else
uniform float pointsTextureSize;
uniform float gridTextureSize;
uniform float cellSize;
uniform float alpha;
uniform float collisionStrength;
uniform float collisionRadius;
uniform float collisionPadding;
uniform float pointsNumber;
uniform float tilesPerRow;
uniform float passesCount;
uniform vec3 gridOffset;
#endif

in vec2 textureCoords;
out vec4 fragColor;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec4 velocity = vec4(0.0);

  // Get current point's index
  float currentIndex = pointPosition.b;

  // Skip if this is an empty texel
  if (currentIndex < 0.0 || currentIndex >= pointsNumber) {
    fragColor = velocity;
    return;
  }

  // Get current point's size for collision radius
  vec4 currentSizeData = texture(sizeTexture, textureCoords);
  float currentSize = currentSizeData.r;
  float currentCollisionRadius = (collisionRadius > 0.0 ? collisionRadius : currentSize * 0.5) + collisionPadding;

  // Track total neighbor count for damping
  float totalNeighbors = 0.0;

#ifdef SPACE_3D
  // The position texture stores z in the alpha channel
  vec3 currentPos = vec3(pointPosition.rg, pointPosition.a);

  // Apply the same offset used when building the grid
  vec3 offsetPos = currentPos + gridOffset * cellSize;

  // Calculate which grid cell this point is in (with offset), clamped to match build-grid.vert
  int gridSize = int(gridTextureSize);
  int rowTiles = int(tilesPerRow);
  ivec3 myCell = clamp(ivec3(floor(offsetPos / cellSize)), ivec3(0), ivec3(gridSize - 1));

  // Check 3x3x3 neighborhood of cells
  for (int dx = -1; dx <= 1; dx++) {
    for (int dy = -1; dy <= 1; dy++) {
      for (int dz = -1; dz <= 1; dz++) {
        ivec3 cell = myCell + ivec3(dx, dy, dz);

        // Skip cells outside grid bounds
        if (any(lessThan(cell, ivec3(0))) || any(greaterThanEqual(cell, ivec3(gridSize)))) continue;

        // Sample the grid cell (z-slices tiled into the 2D texture)
        ivec2 pixel = ivec2(
          (cell.z % rowTiles) * gridSize + cell.x,
          (cell.z / rowTiles) * gridSize + cell.y
        );
        vec4 cellData = texelFetch(gridTexture, pixel, 0);

        float cellCount = cellData.w;
        if (cellCount < 0.5) continue; // Empty cell

        // Scale force by number of points in cell
        // Subtract 1 if this is our own cell to avoid self-collision
        float effectiveCount = cellCount;
        if (dx == 0 && dy == 0 && dz == 0) {
          effectiveCount = max(0.0, cellCount - 1.0);
        }

        totalNeighbors += effectiveCount;

        // Get average position in this cell. The 3D grid payload has no room for
        // a size sum, so neighbor radii are approximated by this point's own
        // radius (exact when \`collisionRadius\` is set or sizes are uniform).
        vec3 avgPos = cellData.xyz / cellCount;
        float otherCollisionRadius = currentCollisionRadius;

        // Calculate combined collision radius
        float combinedRadius = currentCollisionRadius + otherCollisionRadius;

        // Calculate distance vector to average position (using original positions)
        vec3 distVector = currentPos - avgPos;
        float dist = length(distVector);

        // Check for collision
        if (dist < combinedRadius && dist > 0.001) {
          // Calculate overlap ratio (0 = just touching, 1 = fully overlapping)
          float overlapRatio = (combinedRadius - dist) / combinedRadius;

          // Soft collision curve: use square root for gentler force near edges
          float softOverlap = sqrt(overlapRatio) * combinedRadius * 0.5;

          // Direction to push apart (normalized)
          vec3 direction = distVector / dist;

          // Apply repulsion force with soft curve, split across the offset passes
          float force = alpha * collisionStrength * softOverlap * (1.0 / passesCount) * effectiveCount;

          // Clamp maximum force to prevent instability
          force = min(force, combinedRadius * 0.5);

          velocity.rgb += force * direction;
        } else if (dist <= 0.001 && effectiveCount > 0.0) {
          // Points at same position - push in a direction from the index
          // (golden-spiral point on the unit sphere, so coincident points scatter evenly)
          float angle = currentIndex * 0.618033988749895 * 6.283185307179586;
          float zDir = 2.0 * fract(currentIndex * 0.754877666246693) - 1.0;
          float ring = sqrt(max(0.0, 1.0 - zDir * zDir));
          vec3 direction = vec3(ring * cos(angle), ring * sin(angle), zDir);
          float force = min(alpha * collisionStrength * combinedRadius * 0.1, combinedRadius * 0.3);
          velocity.rgb += force * effectiveCount * direction;
        }
      }
    }
  }

  // Apply density-based damping: reduce force when surrounded by many neighbors.
  // 3D cells hold far more points than 2D ones (volume vs area), so the damping
  // is floored \u2014 otherwise a dense pile is suppressed so hard it can never
  // push itself apart (the per-pass correction cap below prevents oscillation).
  if (totalNeighbors > 2.0) {
    float damping = max(2.0 / totalNeighbors, 0.05);
    velocity.rgb *= damping;
  }

  // Cap the per-pass correction so overlaps resolve by relaxation instead of
  // overshooting in one frame.
  float maxCorrection = currentCollisionRadius * 0.25;
  float correction = length(velocity.rgb);
  if (correction > maxCorrection) {
    velocity.rgb *= maxCorrection / correction;
  }

  // z velocity lives in the blue channel (update-position.frag SPACE_3D contract)
#else
  vec2 currentPos = pointPosition.rg;

  // Apply the same offset used when building the grid
  vec2 offsetPos = currentPos + gridOffset.xy * cellSize;

  // Calculate which grid cell this point is in (with offset).
  // Clamp to the grid bounds to match build-grid.vert, so a point that drifts
  // outside the space still reads the edge cell it was binned into.
  float myCellX = clamp(floor(offsetPos.x / cellSize), 0.0, gridTextureSize - 1.0);
  float myCellY = clamp(floor(offsetPos.y / cellSize), 0.0, gridTextureSize - 1.0);

  // Check 3x3 neighborhood of cells
  for (int dx = -1; dx <= 1; dx++) {
    for (int dy = -1; dy <= 1; dy++) {
      float neighborCellX = myCellX + float(dx);
      float neighborCellY = myCellY + float(dy);

      // Skip cells outside grid bounds
      if (neighborCellX < 0.0 || neighborCellX >= gridTextureSize ||
          neighborCellY < 0.0 || neighborCellY >= gridTextureSize) {
        continue;
      }

      // Sample the grid cell
      vec2 gridCoord = (vec2(neighborCellX, neighborCellY) + 0.5) / gridTextureSize;
      vec4 cellData = texture(gridTexture, gridCoord);

      float cellCount = cellData.w;
      if (cellCount < 0.5) continue; // Empty cell

      // Scale force by number of points in cell
      // Subtract 1 if this is our own cell to avoid self-collision
      float effectiveCount = cellCount;
      if (dx == 0 && dy == 0) {
        effectiveCount = max(0.0, cellCount - 1.0);
      }

      totalNeighbors += effectiveCount;

      // Get average position and size in this cell
      vec2 avgPos = cellData.xy / cellCount;
      float avgSize = cellData.z / cellCount;
      float otherCollisionRadius = (collisionRadius > 0.0 ? collisionRadius : avgSize * 0.5) + collisionPadding;

      // Calculate combined collision radius
      float combinedRadius = currentCollisionRadius + otherCollisionRadius;

      // Calculate distance vector to average position (using original positions)
      vec2 distVector = currentPos - avgPos;
      float dist = length(distVector);

      // Check for collision
      if (dist < combinedRadius && dist > 0.001) {
        // Calculate overlap ratio (0 = just touching, 1 = fully overlapping)
        float overlapRatio = (combinedRadius - dist) / combinedRadius;

        // Soft collision curve: use square root for gentler force near edges
        // This prevents the "ping-pong" effect at boundaries
        float softOverlap = sqrt(overlapRatio) * combinedRadius * 0.5;

        // Direction to push apart (normalized)
        vec2 direction = distVector / dist;

        // Apply repulsion force with soft curve, split across the offset passes
        float force = alpha * collisionStrength * softOverlap * (1.0 / passesCount) * effectiveCount;

        // Clamp maximum force to prevent instability
        force = min(force, combinedRadius * 0.5);

        velocity.rg += force * direction;
      } else if (dist <= 0.001 && effectiveCount > 0.0) {
        // Points at same position - push based on index
        float angle = currentIndex * 0.618033988749895;
        float force = min(alpha * collisionStrength * combinedRadius * 0.1, combinedRadius * 0.3);
        velocity.rg += force * effectiveCount * vec2(cos(angle), sin(angle));
      }
    }
  }

  // Apply density-based damping: reduce force when surrounded by many neighbors.
  // This prevents chaotic oscillations in dense clusters. Floored (like the 3D
  // branch) so a dense pile is never suppressed so hard it can't push itself
  // apart \u2014 the per-pass correction cap below prevents oscillation.
  if (totalNeighbors > 2.0) {
    float damping = max(2.0 / totalNeighbors, 0.05);
    velocity.rg *= damping;
  }

  // Cap the per-pass correction so overlaps resolve by relaxation instead of
  // overshooting in one frame. Across the offset passes the total displacement
  // stays within ~one collision radius per tick, so a full overlap resolves in
  // a frame or two while the soft force curve keeps light contacts gentle.
  float maxCorrection = currentCollisionRadius * 0.25;
  float correction = length(velocity.rg);
  if (correction > maxCorrection) {
    velocity.rg *= maxCorrection / correction;
  }
#endif

  fragColor = velocity;
}
`,Ee=[[0,0,0],[.5,0,0],[0,.5,0],[.5,.5,0]],_e=[[0,0,0],[.5,0,0],[0,.5,0],[.5,.5,0],[0,0,.5],[.5,0,.5],[0,.5,.5],[.5,.5,.5]],qt=64,Zt=.25;class Oe extends V{constructor(){super(...arguments),this.gridTargets=[],this.programsSpaceDimensions=2,this.gridTextureSize=0,this.gridTextureWidth=0,this.gridTextureHeight=0,this.tilesPerRow=1,this.cellSize=0}create(){var e;const{device:t,store:i,data:o,config:s}=this;if(!i.pointsTextureSize||o.pointsNumber===void 0)return;let r=s.pointDefaultSize??M.pointDefaultSize;if(o.pointSizes)for(let c=0;c<(o.pointsNumber??0);c++)r=Math.max(r,o.getResolvedPointSize(c));const n=s.simulationCollisionRadius??0,a=s.simulationCollisionPadding??0,l=(n>0?n:r*.5)+a;this.cellSize=Math.max(l,8),i.is3D?(this.gridTextureSize=Math.min(qt,Math.max(8,Math.ceil(i.adjustedSpaceSize/this.cellSize))),this.cellSize=i.adjustedSpaceSize/this.gridTextureSize,this.tilesPerRow=Math.ceil(Math.sqrt(this.gridTextureSize)),this.gridTextureWidth=this.gridTextureSize*this.tilesPerRow,this.gridTextureHeight=this.gridTextureSize*Math.ceil(this.gridTextureSize/this.tilesPerRow)):(this.gridTextureSize=Math.min(512,Math.max(32,Math.ceil(i.adjustedSpaceSize/this.cellSize))),this.cellSize=i.adjustedSpaceSize/this.gridTextureSize,this.tilesPerRow=1,this.gridTextureWidth=this.gridTextureSize,this.gridTextureHeight=this.gridTextureSize);const u=i.is3D?_e:Ee;this.gridTargets.length===u.length&&this.gridTargets.every(c=>!c.texture.destroyed&&!c.fbo.destroyed&&c.texture.width===this.gridTextureWidth&&c.texture.height===this.gridTextureHeight)||(this.destroyGridTargets(),this.gridTargets=u.map(()=>{const c=t.createTexture({width:this.gridTextureWidth,height:this.gridTextureHeight,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST}),f=t.createFramebuffer({width:this.gridTextureWidth,height:this.gridTextureHeight,colorAttachments:[c]});return{texture:c,fbo:f}}));const d=new Float32Array(i.pointsTextureSize*i.pointsTextureSize*4);for(let c=0;c<o.pointsNumber;c++)d[c*4]=o.getResolvedPointSize(c);(!this.sizeTexture||this.sizeTexture.destroyed||this.sizeTexture.width!==i.pointsTextureSize||this.sizeTexture.height!==i.pointsTextureSize)&&(this.sizeTexture&&!this.sizeTexture.destroyed&&this.sizeTexture.destroy(),this.sizeTexture=t.createTexture({width:i.pointsTextureSize,height:i.pointsTextureSize,format:"rgba32float",usage:g.SAMPLE|g.COPY_DST})),this.sizeTexture.copyImageData({data:d,bytesPerRow:y("rgba32float",i.pointsTextureSize),mipLevel:0,x:0,y:0}),(!this.pointIndices||this.previousPointsTextureSize!==i.pointsTextureSize)&&(this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy(),this.pointIndices=t.createBuffer({data:K(i.pointsTextureSize),usage:x.VERTEX|x.COPY_DST}),(e=this.buildGridCommand)==null||e.setAttributes({pointIndices:this.pointIndices})),this.previousPointsTextureSize=i.pointsTextureSize,this.previousSpaceSize=i.adjustedSpaceSize}initPrograms(){var e,t;const{device:i,store:o,data:s}=this;!s.pointsNumber||!o.pointsTextureSize||(this.programsSpaceDimensions!==o.spaceDimensions&&(this.programsSpaceDimensions=o.spaceDimensions,(e=this.buildGridCommand)==null||e.destroy(),this.buildGridCommand=void 0,(t=this.forceCommand)==null||t.destroy(),this.forceCommand=void 0),this.buildGridUniformStore||(this.buildGridUniformStore=new T(i,{buildGridUniforms:{uniformTypes:{pointsTextureSize:"f32",gridTextureSize:"f32",cellSize:"f32",tilesPerRow:"f32",gridTextureWidth:"f32",gridTextureHeight:"f32",gridOffset:"vec3<f32>"}}})),this.buildGridCommand||(this.buildGridCommand=new b(i,{fs:Ht,vs:Wt,topology:"point-list",vertexCount:s.pointsNumber,attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...o.is3D?{SPACE_3D:!0}:{}},bindings:{buildGridUniforms:this.buildGridUniformStore.getManagedUniformBuffer("buildGridUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.forceUniformStore||(this.forceUniformStore=new T(i,{forceCollisionUniforms:{uniformTypes:{pointsTextureSize:"f32",gridTextureSize:"f32",cellSize:"f32",alpha:"f32",collisionStrength:"f32",collisionRadius:"f32",collisionPadding:"f32",pointsNumber:"f32",tilesPerRow:"f32",passesCount:"f32",gridOffset:"vec3<f32>"}}})),this.forceVertexCoordBuffer||(this.forceVertexCoordBuffer=i.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.forceCommand||(this.forceCommand=new b(i,{fs:jt,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...o.is3D?{SPACE_3D:!0}:{}},bindings:{forceCollisionUniforms:this.forceUniformStore.getManagedUniformBuffer("forceCollisionUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})))}run(){const{device:e,store:t,data:i,points:o,config:s}=this;if(!o||!this.buildGridCommand||!this.buildGridUniformStore||!this.forceCommand||!this.forceUniformStore||!this.pointIndices||i.pointsNumber===void 0||!o.previousPositionTexture||o.previousPositionTexture.destroyed||!o.exitTexture||o.exitTexture.destroyed||!o.velocityFbo||o.velocityFbo.destroyed||!this.sizeTexture||this.sizeTexture.destroyed)return;const r=t.is3D?_e:Ee;if(this.gridTargets.length!==r.length||t.pointsTextureSize!==this.previousPointsTextureSize||t.adjustedSpaceSize!==this.previousSpaceSize||this.programsSpaceDimensions!==t.spaceDimensions)return;const n=s.simulationCollisionRadius??0,a=s.simulationCollisionPadding??0;this.buildGridCommand.setVertexCount(i.pointsNumber),this.buildGridCommand.setBindings({positionsTexture:o.previousPositionTexture,exitTexture:o.exitTexture,...t.is3D?{}:{sizeTexture:this.sizeTexture}});for(const[u,d]of r.entries()){const c=this.gridTargets[u];if(!c||c.fbo.destroyed||c.texture.destroyed)continue;this.buildGridUniformStore.setUniforms({buildGridUniforms:{pointsTextureSize:t.pointsTextureSize??0,gridTextureSize:this.gridTextureSize,cellSize:this.cellSize,tilesPerRow:this.tilesPerRow,gridTextureWidth:this.gridTextureWidth,gridTextureHeight:this.gridTextureHeight,gridOffset:d}});const f=e.beginRenderPass({framebuffer:c.fbo,clearColor:[0,0,0,0]});this.buildGridCommand.draw(f),f.end()}this.forceCommand.setBindings({positionsTexture:o.previousPositionTexture,sizeTexture:this.sizeTexture});const l=e.beginRenderPass({framebuffer:o.velocityFbo,clearColor:[0,0,0,0]});for(const[u,d]of r.entries()){const c=this.gridTargets[u];!c||c.texture.destroyed||(this.forceUniformStore.setUniforms({forceCollisionUniforms:{pointsTextureSize:t.pointsTextureSize??0,gridTextureSize:this.gridTextureSize,cellSize:this.cellSize,alpha:Math.max(t.alpha,Zt),collisionStrength:s.simulationCollision??0,collisionRadius:n,collisionPadding:a,pointsNumber:i.pointsNumber,tilesPerRow:this.tilesPerRow,passesCount:r.length,gridOffset:d}}),this.forceCommand.setBindings({gridTexture:c.texture}),this.forceCommand.draw(l))}l.end()}destroy(){var e,t,i,o;(e=this.buildGridCommand)==null||e.destroy(),this.buildGridCommand=void 0,(t=this.forceCommand)==null||t.destroy(),this.forceCommand=void 0,this.destroyGridTargets(),this.sizeTexture&&!this.sizeTexture.destroyed&&this.sizeTexture.destroy(),this.sizeTexture=void 0,(i=this.buildGridUniformStore)==null||i.destroy(),this.buildGridUniformStore=void 0,(o=this.forceUniformStore)==null||o.destroy(),this.forceUniformStore=void 0,this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy(),this.pointIndices=void 0,this.forceVertexCoordBuffer&&!this.forceVertexCoordBuffer.destroyed&&this.forceVertexCoordBuffer.destroy(),this.forceVertexCoordBuffer=void 0}destroyGridTargets(){for(const e of this.gridTargets)e.fbo&&!e.fbo.destroyed&&e.fbo.destroy();for(const e of this.gridTargets)e.texture&&!e.texture.destroyed&&e.texture.destroy();this.gridTargets=[]}}const Xt=`#version 300 es
precision highp float;

uniform sampler2D positionsTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceGravityUniforms {
  float gravity;
  float spaceSize;
  float alpha;
} forceGravity;

#define gravity forceGravity.gravity
#define spaceSize forceGravity.spaceSize
#define alpha forceGravity.alpha
#else
uniform float gravity;
uniform float spaceSize;
uniform float alpha;
#endif

in vec2 textureCoords;
out vec4 fragColor;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);

  vec4 velocity = vec4(0.0);

  #ifdef SPACE_3D
  // 3D: z lives in the position alpha channel; z velocity goes to the blue channel.
  vec3 centerPosition = vec3(spaceSize * 0.5);
  vec3 position = vec3(pointPosition.rg, pointPosition.a);
  vec3 distVector = centerPosition - position;
  float dist = length(distVector);
  if (dist > 0.0) {
    float additionalVelocity = alpha * gravity * dist * 0.1;
    velocity.rgb += additionalVelocity * (distVector / dist);
  }
  #else
  vec2 centerPosition = vec2(spaceSize * 0.5);
  vec2 distVector = centerPosition - pointPosition.rg;
  float dist = sqrt(dot(distVector, distVector));
  if (dist > 0.0) {
    float angle = atan(distVector.y, distVector.x);
    float additionalVelocity = alpha * gravity * dist * 0.1;
    velocity.rg += additionalVelocity * vec2(cos(angle), sin(angle));
  }
  #endif

  fragColor = velocity;
}`;class Ve extends V{constructor(){super(...arguments),this.programsSpaceDimensions=2}initPrograms(){const{device:e,points:t,store:i}=this;!t||!i.pointsTextureSize||(this.programsSpaceDimensions!==i.spaceDimensions&&(this.programsSpaceDimensions=i.spaceDimensions,this.runCommand&&(this.runCommand.destroy(),this.runCommand=void 0)),this.vertexCoordBuffer||(this.vertexCoordBuffer=e.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.uniformStore||(this.uniformStore=new T(e,{forceGravityUniforms:{uniformTypes:{gravity:"f32",spaceSize:"f32",alpha:"f32"}}})),this.runCommand||(this.runCommand=new b(e,{fs:Xt,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.vertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...i.is3D?{SPACE_3D:!0}:{}},bindings:{forceGravityUniforms:this.uniformStore.getManagedUniformBuffer("forceGravityUniforms")},parameters:{depthWriteEnabled:!1,depthCompare:"always"}})))}run(){const{device:e,points:t,store:i}=this;if(!t||!this.runCommand||!this.uniformStore||!t.previousPositionTexture||t.previousPositionTexture.destroyed||!t.velocityFbo||t.velocityFbo.destroyed)return;this.uniformStore.setUniforms({forceGravityUniforms:{gravity:this.config.simulationGravity,spaceSize:i.adjustedSpaceSize,alpha:i.alpha}}),this.runCommand.setBindings({positionsTexture:t.previousPositionTexture});const o=e.beginRenderPass({framebuffer:t.velocityFbo,clearColor:[0,0,0,0]});this.runCommand.draw(o),o.end()}destroy(){var e,t;(e=this.runCommand)==null||e.destroy(),this.runCommand=void 0,(t=this.uniformStore)==null||t.destroy(),this.uniformStore=void 0,this.vertexCoordBuffer&&!this.vertexCoordBuffer.destroyed&&this.vertexCoordBuffer.destroy(),this.vertexCoordBuffer=void 0}}function Yt(h){return`#version 300 es
precision highp float;

uniform sampler2D positionsTexture;
uniform sampler2D exitTexture;
uniform sampler2D linkInfoTexture; // Texture storing first link indices and amount
uniform sampler2D linkIndicesTexture;
uniform sampler2D linkPropertiesTexture; // Texture storing link bias and strength
uniform sampler2D linkRandomDistanceTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceLinkUniforms {
  float linkSpring;
  float linkDistance;
  vec2 linkDistRandomVariationRange;
  float pointsTextureSize;
  float linksTextureSize;
  float alpha;
} forceLink;

#define linkSpring forceLink.linkSpring
#define linkDistance forceLink.linkDistance
#define linkDistRandomVariationRange forceLink.linkDistRandomVariationRange
#define pointsTextureSize forceLink.pointsTextureSize
#define linksTextureSize forceLink.linksTextureSize
#define alpha forceLink.alpha
#else
uniform float linkSpring;
uniform float linkDistance;
uniform vec2 linkDistRandomVariationRange;
uniform float pointsTextureSize;
uniform float linksTextureSize;
uniform float alpha;
#endif

in vec2 textureCoords;
out vec4 fragColor;

const float MAX_LINKS = ${h}.0;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec4 velocity = vec4(0.0);

  vec4 linkInfo = texture(linkInfoTexture, textureCoords);
  float iCount = linkInfo.r;
  float jCount = linkInfo.g;
  float linkAmount = linkInfo.b;
  if (linkAmount > 0.0) {
    for (float i = 0.0; i < MAX_LINKS; i += 1.0) {
      if (i < linkAmount) {
        if (iCount >= linksTextureSize) {
          iCount = 0.0;
          jCount += 1.0;
        }
        vec2 linkTextureIndex = (vec2(iCount, jCount) + 0.5) / linksTextureSize;
        vec4 connectedPointIndex = texture(linkIndicesTexture, linkTextureIndex);
        vec4 biasAndStrength = texture(linkPropertiesTexture, linkTextureIndex);
        vec4 randomMinDistance = texture(linkRandomDistanceTexture, linkTextureIndex);
        float bias = biasAndStrength.r;
        float strength = biasAndStrength.g;
        float randomMinLinkDist = randomMinDistance.r * (linkDistRandomVariationRange.g - linkDistRandomVariationRange.r) + linkDistRandomVariationRange.r;
        randomMinLinkDist *= linkDistance;

        iCount += 1.0;

        // Skip a link to an absent point \u2014 its position would poison the spring
        // force. (exit.G = current absence)
        vec4 connectedExit = texture(exitTexture, (connectedPointIndex.rg + 0.5) / pointsTextureSize);
        if (connectedExit.g > 0.5) {
          continue;
        }

        vec4 connectedPointPosition = texture(positionsTexture, (connectedPointIndex.rg + 0.5) / pointsTextureSize);
        float x = connectedPointPosition.x - (pointPosition.x + velocity.x);
        float y = connectedPointPosition.y - (pointPosition.y + velocity.y);
        #ifdef SPACE_3D
        // z lives in the position alpha channel; z velocity accumulates in the blue channel.
        float z = connectedPointPosition.a - (pointPosition.a + velocity.b);
        float l = sqrt(x * x + y * y + z * z);
        #else
        float l = sqrt(x * x + y * y);
        #endif

        // Apply the link force
        l = max(l, randomMinLinkDist * 0.99);
        l = (l - randomMinLinkDist) / l;
        l *= linkSpring * alpha;
        l *= strength;
        l *= bias;
        x *= l;
        y *= l;
        velocity.x += x;
        velocity.y += y;
        #ifdef SPACE_3D
        z *= l;
        velocity.b += z;
        #endif
      }
    }
  }

  fragColor = vec4(velocity.rg, velocity.b, 0.0);
}
  `}function k(h,e){return!h||h.length!==2?e:[h[0],h[1]]}function w(h,e){return!h||h.length!==4?e:[h[0],h[1],h[2],h[3]]}const $=h=>Number.isInteger(h)?h.toFixed(1):String(h);var pe=(h=>(h.OUTGOING="outgoing",h.INCOMING="incoming",h))(pe||{});class se extends V{constructor(){super(...arguments),this.linkFirstIndicesAndAmount=new Float32Array,this.indices=new Float32Array,this.maxPointDegree=0,this.programsSpaceDimensions=2}create(e){var t;const{device:i,store:{pointsTextureSize:o,linksTextureSize:s},data:r}=this;if(!o||!s)return;this.linkFirstIndicesAndAmount=new Float32Array(o*o*4),this.indices=new Float32Array(s*s*4);const n=new Float32Array(s*s*4),a=new Float32Array(s*s*4),l=e==="incoming"?r.sourceIndexToTargetIndices:r.targetIndexToSourceIndices;this.maxPointDegree=0;let u=0;l?.forEach((f,p)=>{f&&(this.linkFirstIndicesAndAmount[p*4+0]=u%s,this.linkFirstIndicesAndAmount[p*4+1]=Math.floor(u/s),this.linkFirstIndicesAndAmount[p*4+2]=f.length??0,f.forEach(([m,S])=>{var v,C,D;this.indices[u*4+0]=m%o,this.indices[u*4+1]=Math.floor(m/o);const I=((v=r.degree)==null?void 0:v[m])??0,L=((C=r.degree)==null?void 0:C[p])??0,z=I+L,R=z!==0?I/z:.5,G=Math.min(I,L);let j=((D=r.linkStrength)==null?void 0:D[S])??1/Math.max(G,1);j=Math.sqrt(j),n[u*4+0]=R,n[u*4+1]=j,a[u*4]=this.store.getRandomFloat(0,1),u+=1}),this.maxPointDegree=Math.max(this.maxPointDegree,f.length??0))});const d=!this.linkFirstIndicesAndAmountTexture||this.linkFirstIndicesAndAmountTexture.width!==o||this.linkFirstIndicesAndAmountTexture.height!==o,c=!this.indicesTexture||this.indicesTexture.width!==s||this.indicesTexture.height!==s;d&&(this.linkFirstIndicesAndAmountTexture&&!this.linkFirstIndicesAndAmountTexture.destroyed&&this.linkFirstIndicesAndAmountTexture.destroy(),this.linkFirstIndicesAndAmountTexture=i.createTexture({width:o,height:o,format:"rgba32float",usage:g.SAMPLE|g.COPY_DST})),this.linkFirstIndicesAndAmountTexture.copyImageData({data:this.linkFirstIndicesAndAmount,bytesPerRow:y("rgba32float",o),mipLevel:0,x:0,y:0}),c&&(this.indicesTexture&&!this.indicesTexture.destroyed&&this.indicesTexture.destroy(),this.biasAndStrengthTexture&&!this.biasAndStrengthTexture.destroyed&&this.biasAndStrengthTexture.destroy(),this.randomDistanceTexture&&!this.randomDistanceTexture.destroyed&&this.randomDistanceTexture.destroy(),this.indicesTexture=i.createTexture({width:s,height:s,format:"rgba32float",usage:g.SAMPLE|g.COPY_DST}),this.biasAndStrengthTexture=i.createTexture({width:s,height:s,format:"rgba32float",usage:g.SAMPLE|g.COPY_DST}),this.randomDistanceTexture=i.createTexture({width:s,height:s,format:"rgba32float",usage:g.SAMPLE|g.COPY_DST})),this.indicesTexture.copyImageData({data:this.indices,bytesPerRow:y("rgba32float",s),mipLevel:0,x:0,y:0}),this.biasAndStrengthTexture.copyImageData({data:n,bytesPerRow:y("rgba32float",s),mipLevel:0,x:0,y:0}),this.randomDistanceTexture.copyImageData({data:a,bytesPerRow:y("rgba32float",s),mipLevel:0,x:0,y:0}),this.previousMaxPointDegree!==void 0&&this.previousMaxPointDegree!==this.maxPointDegree&&((t=this.runCommand)==null||t.destroy(),this.runCommand=void 0),this.previousMaxPointDegree=this.maxPointDegree,this.previousPointsTextureSize=o,this.previousLinksTextureSize=s}initPrograms(){const{device:e,store:t,points:i}=this;!i||!t.pointsTextureSize||!t.linksTextureSize||!this.linkFirstIndicesAndAmountTexture||!this.indicesTexture||!this.biasAndStrengthTexture||!this.randomDistanceTexture||(this.programsSpaceDimensions!==t.spaceDimensions&&(this.programsSpaceDimensions=t.spaceDimensions,this.runCommand&&(this.runCommand.destroy(),this.runCommand=void 0)),this.vertexCoordBuffer||(this.vertexCoordBuffer=e.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.uniformStore||(this.uniformStore=new T(e,{forceLinkUniforms:{uniformTypes:{linkSpring:"f32",linkDistance:"f32",linkDistRandomVariationRange:"vec2<f32>",pointsTextureSize:"f32",linksTextureSize:"f32",alpha:"f32"}}})),this.runCommand||(this.runCommand=new b(e,{fs:Yt(this.maxPointDegree),vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.vertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...t.is3D?{SPACE_3D:!0}:{}},bindings:{forceLinkUniforms:this.uniformStore.getManagedUniformBuffer("forceLinkUniforms")},parameters:{depthWriteEnabled:!1,depthCompare:"always"}})))}run(){const{device:e,store:t,points:i}=this;if(!i||!this.runCommand||!this.uniformStore||!i.previousPositionTexture||i.previousPositionTexture.destroyed||!i.exitTexture||i.exitTexture.destroyed||!this.linkFirstIndicesAndAmountTexture||!this.indicesTexture||!this.biasAndStrengthTexture||!this.randomDistanceTexture||!i.velocityFbo||i.velocityFbo.destroyed||t.pointsTextureSize!==this.previousPointsTextureSize||t.linksTextureSize!==this.previousLinksTextureSize)return;this.uniformStore.setUniforms({forceLinkUniforms:{linkSpring:this.config.simulationLinkSpring,linkDistance:this.config.simulationLinkDistance,linkDistRandomVariationRange:k(this.config.simulationLinkDistRandomVariationRange,[0,0]),pointsTextureSize:t.pointsTextureSize,linksTextureSize:t.linksTextureSize,alpha:t.alpha}}),this.runCommand.setBindings({positionsTexture:i.previousPositionTexture,exitTexture:i.exitTexture,linkInfoTexture:this.linkFirstIndicesAndAmountTexture,linkIndicesTexture:this.indicesTexture,linkPropertiesTexture:this.biasAndStrengthTexture,linkRandomDistanceTexture:this.randomDistanceTexture});const o=e.beginRenderPass({framebuffer:i.velocityFbo,clearColor:[0,0,0,0]});this.runCommand.draw(o),o.end()}destroy(){var e,t;(e=this.runCommand)==null||e.destroy(),this.runCommand=void 0,this.linkFirstIndicesAndAmountTexture&&!this.linkFirstIndicesAndAmountTexture.destroyed&&this.linkFirstIndicesAndAmountTexture.destroy(),this.linkFirstIndicesAndAmountTexture=void 0,this.indicesTexture&&!this.indicesTexture.destroyed&&this.indicesTexture.destroy(),this.indicesTexture=void 0,this.biasAndStrengthTexture&&!this.biasAndStrengthTexture.destroyed&&this.biasAndStrengthTexture.destroy(),this.biasAndStrengthTexture=void 0,this.randomDistanceTexture&&!this.randomDistanceTexture.destroyed&&this.randomDistanceTexture.destroy(),this.randomDistanceTexture=void 0,(t=this.uniformStore)==null||t.destroy(),this.uniformStore=void 0,this.vertexCoordBuffer&&!this.vertexCoordBuffer.destroyed&&this.vertexCoordBuffer.destroy(),this.vertexCoordBuffer=void 0}}const Ge=`#version 300 es
precision highp float;

in vec4 vColor;
out vec4 fragColor;

void main() {
  fragColor = vColor;
}`,Kt=`#version 300 es
precision highp float;

// Aggregates each point into its grid cell. A level is a plain 2D grid of
// \`levelGridSize\` cells per axis rendered one texel per cell; additive blending
// accumulates [sum(x), sum(y), count, 0] per cell via calculate-level.frag.

uniform sampler2D positionsTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform calculateLevelsPreciseUniforms {
  float pointsTextureSize;
  float levelGridSize;
  float cellSize;
} calculateLevelsPrecise;

#define pointsTextureSize calculateLevelsPrecise.pointsTextureSize
#define levelGridSize calculateLevelsPrecise.levelGridSize
#define cellSize calculateLevelsPrecise.cellSize
#else
uniform float pointsTextureSize;
uniform float levelGridSize;
uniform float cellSize;
#endif

in vec2 pointIndices;

out vec4 vColor;

void main() {
  vColor = vec4(0.0);

  // Absent points must not enter the grid \u2014 a NaN position bins to a NaN cell and
  // poisons the centermass that drives repulsion for every point. (exit.G = absent)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  vColor = vec4(pointPosition.rg, 1.0, 0.0);

  // The clamp must match the force shaders exactly, or boundary points fall out
  // of the level decomposition's exactly-once coverage.
  int gridSize = int(levelGridSize);
  ivec2 cell = clamp(ivec2(floor(pointPosition.rg / cellSize)), ivec2(0), ivec2(gridSize - 1));

  vec2 levelPosition = 2.0 * (vec2(cell) + 0.5) / levelGridSize - 1.0;
  gl_Position = vec4(levelPosition, 0.0, 1.0);
  gl_PointSize = 1.0;
}
`,$t=`#version 300 es
precision highp float;

// 3D analog of calculate-level.vert: aggregates each point into its octree cell.
// A level is a 3D grid of \`levelGridSize\` cells per axis, flattened into a 2D
// texture by tiling the z-slices in a grid of \`tilesPerRow\` tiles per row.
// Additive blending accumulates [sum(x), sum(y), count, sum(z)] per cell \u2014
// the same payload layout as the ForceCenter centermass aggregation.

uniform sampler2D positionsTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform calculateLevels3DUniforms {
  float pointsTextureSize;
  float levelGridSize;
  float cellSize;
  float tilesPerRow;
  float levelTextureWidth;
  float levelTextureHeight;
} calculateLevels3D;

#define pointsTextureSize calculateLevels3D.pointsTextureSize
#define levelGridSize calculateLevels3D.levelGridSize
#define cellSize calculateLevels3D.cellSize
#define tilesPerRow calculateLevels3D.tilesPerRow
#define levelTextureWidth calculateLevels3D.levelTextureWidth
#define levelTextureHeight calculateLevels3D.levelTextureHeight
#else
uniform float pointsTextureSize;
uniform float levelGridSize;
uniform float cellSize;
uniform float tilesPerRow;
uniform float levelTextureWidth;
uniform float levelTextureHeight;
#endif

in vec2 pointIndices;

out vec4 vColor;

void main() {
  vColor = vec4(0.0);

  // Absent points must not enter the octree \u2014 a NaN position bins to a NaN cell and
  // poisons the centermass that drives repulsion for every point. (exit.G = absent)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  // z lives in the position alpha channel
  vec3 position = vec3(pointPosition.rg, pointPosition.a);
  vColor = vec4(position.xy, 1.0, position.z);

  // The clamp must match the force shaders exactly, or edge points fall out of
  // the level decomposition's exactly-once coverage.
  int gridSize = int(levelGridSize);
  ivec3 cell = clamp(ivec3(floor(position / cellSize)), ivec3(0), ivec3(gridSize - 1));

  int rowTiles = int(tilesPerRow);
  ivec2 pixel = ivec2(
    (cell.z % rowTiles) * gridSize + cell.x,
    (cell.z / rowTiles) * gridSize + cell.y
  );

  vec2 levelPosition = 2.0 * (vec2(pixel) + 0.5) / vec2(levelTextureWidth, levelTextureHeight) - 1.0;
  gl_Position = vec4(levelPosition, 0.0, 1.0);
  gl_PointSize = 1.0;
}
`,Qt=`#version 300 es
precision highp float;

// One grid level of precise many-body repulsion (Barnes-Hut-style approximation).
//
// Levels are 2D grids of increasing resolution (4\xB2, 8\xB2, \u2026) holding
// [sum(x), sum(y), count, 0] per cell. The decomposition tiles space exactly
// once across the level passes: after level L the only un-accumulated region is
// the 3\xD73 Chebyshev-1 neighborhood of the point's cell, which the next level
// refines (its aligned 6\xD76 child block), and which force-nearfield.frag finally
// covers at the finest level. The exclusion shell is fixed at Chebyshev
// distance 1.

uniform sampler2D positionsTexture;
uniform sampler2D levelTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceLevelPreciseUniforms {
  float levelGridSize;
  float cellSize;
  float isFirstLevel;
  float alpha;
  float repulsion;
} forceLevelPrecise;

#define levelGridSize forceLevelPrecise.levelGridSize
#define cellSize forceLevelPrecise.cellSize
#define isFirstLevel forceLevelPrecise.isFirstLevel
#define alpha forceLevelPrecise.alpha
#define repulsion forceLevelPrecise.repulsion
#else
uniform float levelGridSize;
uniform float cellSize;
uniform float isFirstLevel;
uniform float alpha;
uniform float repulsion;
#endif

in vec2 textureCoords;
out vec4 fragColor;

// Repulsion from one cell's center of mass \u2014 a d3-style clamped
// inverse-distance falloff.
vec2 cellVelocity(ivec2 cell, vec2 position) {
  vec4 centermass = texelFetch(levelTexture, cell, 0);
  // Count-only guard: zero coordinate sums are legitimate, but dividing by a zero
  // count would produce NaN that additive blending propagates into the velocity FBO.
  if (centermass.b <= 0.0) return vec2(0.0);
  vec2 centermassPosition = centermass.rg / centermass.b;
  vec2 distVector = position - centermassPosition;
  float l = dot(distVector, distVector);
  if (l <= 0.0) return vec2(0.0);
  float distanceMin2 = 1.0;
  if (l < distanceMin2) l = sqrt(distanceMin2 * l);
  float addV = alpha * repulsion * centermass.b / sqrt(l);
  return addV * normalize(distVector);
}

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec2 position = pointPosition.rg;

  int gridSize = int(levelGridSize);
  // Must match the aggregation shader's cell formula exactly.
  ivec2 pointCell = clamp(ivec2(floor(position / cellSize)), ivec2(0), ivec2(gridSize - 1));

  vec2 velocity = vec2(0.0);

  if (isFirstLevel > 0.5) {
    // Coarsest level: every cell except the 3\xD73 neighborhood, which finer levels refine.
    for (int j = 0; j < gridSize; j += 1) {
      for (int i = 0; i < gridSize; i += 1) {
        ivec2 cell = ivec2(i, j);
        ivec2 cellDist = abs(cell - pointCell);
        if (max(cellDist.x, cellDist.y) <= 1) continue;
        velocity += cellVelocity(cell, position);
      }
    }
  } else {
    // The coarser level left its 3\xD73 neighborhood unhandled; those cells refine to
    // the aligned 6\xD76 child block at this level. Sample it minus this level's own
    // 3\xD73 neighborhood (always strictly inside the block).
    ivec2 base = (pointCell / 2) * 2 - 2;
    for (int j = 0; j < 6; j += 1) {
      for (int i = 0; i < 6; i += 1) {
        ivec2 cell = base + ivec2(i, j);
        // Bounds check must precede texelFetch (out-of-range fetches are undefined).
        if (any(lessThan(cell, ivec2(0))) || any(greaterThanEqual(cell, ivec2(gridSize)))) continue;
        ivec2 cellDist = abs(cell - pointCell);
        if (max(cellDist.x, cellDist.y) <= 1) continue;
        velocity += cellVelocity(cell, position);
      }
    }
  }

  fragColor = vec4(velocity, 0.0, 0.0);
}
`,Jt=`#version 300 es
precision highp float;

// One octree level of 3D many-body repulsion (Barnes-Hut-style approximation).
//
// Levels are 3D grids of increasing resolution (4\xB3, 8\xB3, \u2026), each flattened into a
// 2D texture of tiled z-slices holding [sum(x), sum(y), count, sum(z)] per cell.
// The decomposition tiles space exactly once across the level passes:
// after level L the only un-accumulated region is the 3\xB3 Chebyshev-1 neighborhood
// of the point's cell, which the next level refines (its aligned 6\xB3 child block),
// and which force-nearfield-3d.frag finally covers at the finest level.
// The exclusion shell is fixed at Chebyshev distance 1 \u2014 the 2D theta parameter
// does not apply in 3D.

uniform sampler2D positionsTexture;
uniform sampler2D levelTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceLevel3DUniforms {
  float levelGridSize;
  float cellSize;
  float tilesPerRow;
  float isFirstLevel;
  float alpha;
  float repulsion;
} forceLevel3D;

#define levelGridSize forceLevel3D.levelGridSize
#define cellSize forceLevel3D.cellSize
#define tilesPerRow forceLevel3D.tilesPerRow
#define isFirstLevel forceLevel3D.isFirstLevel
#define alpha forceLevel3D.alpha
#define repulsion forceLevel3D.repulsion
#else
uniform float levelGridSize;
uniform float cellSize;
uniform float tilesPerRow;
uniform float isFirstLevel;
uniform float alpha;
uniform float repulsion;
#endif

in vec2 textureCoords;
out vec4 fragColor;

// Repulsion from one cell's center of mass \u2014 the 3D transcription of the 2D
// calculateAdditionalVelocity (same d3-style clamped inverse-distance falloff).
vec3 cellVelocity(ivec3 cell, int gridSize, int rowTiles, vec3 position) {
  ivec2 pixel = ivec2(
    (cell.z % rowTiles) * gridSize + cell.x,
    (cell.z / rowTiles) * gridSize + cell.y
  );
  vec4 centermass = texelFetch(levelTexture, pixel, 0);
  // Count-only guard: zero coordinate sums are legitimate, but dividing by a zero
  // count would produce NaN that additive blending propagates into the velocity FBO.
  if (centermass.b <= 0.0) return vec3(0.0);
  vec3 centermassPosition = vec3(centermass.r, centermass.g, centermass.a) / centermass.b;
  vec3 distVector = position - centermassPosition;
  float l = dot(distVector, distVector);
  if (l <= 0.0) return vec3(0.0);
  float distanceMin2 = 1.0;
  if (l < distanceMin2) l = sqrt(distanceMin2 * l);
  float addV = alpha * repulsion * centermass.b / sqrt(l);
  return addV * normalize(distVector);
}

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec3 position = vec3(pointPosition.rg, pointPosition.a);

  int gridSize = int(levelGridSize);
  int rowTiles = int(tilesPerRow);
  // Must match the aggregation shader's cell formula exactly.
  ivec3 pointCell = clamp(ivec3(floor(position / cellSize)), ivec3(0), ivec3(gridSize - 1));

  vec3 velocity = vec3(0.0);

  if (isFirstLevel > 0.5) {
    // Coarsest level: every cell except the 3\xB3 neighborhood, which finer levels refine.
    for (int k = 0; k < gridSize; k += 1) {
      for (int j = 0; j < gridSize; j += 1) {
        for (int i = 0; i < gridSize; i += 1) {
          ivec3 cell = ivec3(i, j, k);
          ivec3 cellDist = abs(cell - pointCell);
          if (max(max(cellDist.x, cellDist.y), cellDist.z) <= 1) continue;
          velocity += cellVelocity(cell, gridSize, rowTiles, position);
        }
      }
    }
  } else {
    // The coarser level left its 3\xB3 neighborhood unhandled; those cells refine to
    // the aligned 6\xB3 child block at this level. Sample it minus this level's own
    // 3\xB3 neighborhood (always strictly inside the block).
    ivec3 base = (pointCell / 2) * 2 - 2;
    for (int k = 0; k < 6; k += 1) {
      for (int j = 0; j < 6; j += 1) {
        for (int i = 0; i < 6; i += 1) {
          ivec3 cell = base + ivec3(i, j, k);
          // Bounds check must precede texelFetch (out-of-range fetches are undefined).
          if (any(lessThan(cell, ivec3(0))) || any(greaterThanEqual(cell, ivec3(gridSize)))) continue;
          ivec3 cellDist = abs(cell - pointCell);
          if (max(max(cellDist.x, cellDist.y), cellDist.z) <= 1) continue;
          velocity += cellVelocity(cell, gridSize, rowTiles, position);
        }
      }
    }
  }

  // z velocity lives in the blue channel (update-position.frag SPACE_3D contract) \u2014
  // unlike the 2D force shaders, which write a constant 1.0 there.
  fragColor = vec4(velocity, 0.0);
}
`,ei=`#version 300 es
precision highp float;

// Near-field pass of the precise grid repulsion (P3M-style). After the finest
// level pass, the only un-accumulated region is the 3\xD73 neighborhood of the
// point's cell.
//
// Cell centroids exert a purely radial force there, which flattens dense hubs
// into disks and petals \u2014 even as a residual for unsampled mass, the centroid
// bias dominates (tangential repulsion scaled by ~K/n never spreads a dense
// clump before alpha decays). So the near field is a pure Monte-Carlo estimator
// instead: the K depth-peeled points of a cell are a uniform random subset
// (re-drawn every tick by build-nearfield-slots.vert), and weighting each
// sampled pairwise force by count/sampled makes the expected force equal the
// exact all-pairs sum \u2014 unbiased, no centroid term. Cells holding \u2264 K points
// are sampled exhaustively, so their forces are exact. The per-tick sampling
// noise acts as annealed jitter: it shrinks with alpha and is precisely what
// breaks clumps apart. The point itself is excluded from both the sample and
// the count.

uniform sampler2D positionsTexture;
uniform sampler2D levelTexture;
uniform sampler2D randomValues;
// One sampler per near-field slot. We list them out instead of using an array
// because WebGL2's GLSL won't let you index a sampler array in a loop. Keep this
// list the same length as NEAR_FIELD_SLOTS in index.ts.
uniform sampler2D slotTexture0;
uniform sampler2D slotTexture1;
uniform sampler2D slotTexture2;
uniform sampler2D slotTexture3;
uniform sampler2D slotTexture4;
uniform sampler2D slotTexture5;
uniform sampler2D slotTexture6;
uniform sampler2D slotTexture7;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceNearFieldUniforms {
  float pointsTextureSize;
  float levelGridSize;
  float cellSize;
  float alpha;
  float repulsion;
} forceNearField;

#define pointsTextureSize forceNearField.pointsTextureSize
#define levelGridSize forceNearField.levelGridSize
#define cellSize forceNearField.cellSize
#define alpha forceNearField.alpha
#define repulsion forceNearField.repulsion
#else
uniform float pointsTextureSize;
uniform float levelGridSize;
uniform float cellSize;
uniform float alpha;
uniform float repulsion;
#endif

in vec2 textureCoords;
out vec4 fragColor;

// Same clamped inverse-distance falloff as the level passes (must stay identical).
vec2 pairwiseVelocity(vec2 position, vec2 otherPosition, vec2 randomDir) {
  vec2 distVector = position - otherPosition;
  float l = dot(distVector, distVector);
  if (l <= 0.0) {
    // Exactly coincident points have no separation direction, so an inverse-distance
    // force is undefined and they would stay stacked forever \u2014 a stack's cell count
    // then repels everything around it, carving a void ring. Kick along this point's
    // random vector instead (each point has a different one, so a pile disperses).
    distVector = randomDir;
    l = dot(distVector, distVector);
    if (l <= 0.0) return vec2(0.0);
  }
  float distanceMin2 = 1.0;
  if (l < distanceMin2) l = sqrt(distanceMin2 * l);
  float addV = alpha * repulsion / sqrt(l);
  return addV * normalize(distVector);
}

// One peeled slot of a cell: the unweighted pairwise force from the sampled
// point, counting it toward the sample size. Empty slots and the point itself
// contribute nothing.
vec2 slotVelocity(vec2 slot, vec2 position, float selfIndex, vec2 randomDir, inout float sampled) {
  float index = slot.x;
  // Skip empty slots (index -1) and the point itself. This exact \`==\` \u2014 and the
  // texel math just below \u2014 count on a point index fitting exactly in a float,
  // which only holds for whole numbers up to ~16.7M (2^24). That's every
  // realistic graph; you'd need a points texture bigger than 4096\xB2 to get there.
  // Past that, indices start rounding, so a point could sample the wrong texel or
  // fail to skip itself \u2014 but you'd hit memory limits long before it matters.
  if (index < 0.0 || index == selfIndex) return vec2(0.0);
  int size = int(pointsTextureSize);
  int i = int(index);
  vec4 other = texelFetch(positionsTexture, ivec2(i % size, i / size), 0);
  sampled += 1.0;
  return pairwiseVelocity(position, other.rg, randomDir);
}

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec2 position = pointPosition.rg;
  // One fragment per point: the fragment's pixel is the point's texel.
  float selfIndex = floor(gl_FragCoord.y) * pointsTextureSize + floor(gl_FragCoord.x);
  vec4 random = texture(randomValues, textureCoords);

  int gridSize = int(levelGridSize);
  ivec2 pointCell = clamp(ivec2(floor(position / cellSize)), ivec2(0), ivec2(gridSize - 1));

  vec2 velocity = vec2(0.0);

  for (int j = -1; j <= 1; j += 1) {
    for (int i = -1; i <= 1; i += 1) {
      ivec2 cell = pointCell + ivec2(i, j);
      if (any(lessThan(cell, ivec2(0))) || any(greaterThanEqual(cell, ivec2(gridSize)))) continue;

      // [sum(x), sum(y), count, 0] \u2014 only the count is used here.
      vec4 aggregate = texelFetch(levelTexture, cell, 0);
      // The count never includes the point itself in the estimate.
      bool ownCell = (i == 0 && j == 0);
      float others = aggregate.b - (ownCell ? 1.0 : 0.0);
      if (others <= 0.0) continue;

      vec2 pairSum = vec2(0.0);
      float sampled = 0.0;
      // Same story as the sampler list above: no looping over samplers in
      // WebGL2, so we read each slot on its own line. This has to match
      // NEAR_FIELD_SLOTS too (and the samplers above, and the bindings in
      // index.ts).
      pairSum += slotVelocity(texelFetch(slotTexture0, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture1, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture2, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture3, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture4, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture5, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture6, cell, 0).rg, position, selfIndex, random.rg, sampled);
      pairSum += slotVelocity(texelFetch(slotTexture7, cell, 0).rg, position, selfIndex, random.rg, sampled);

      // Horvitz\u2013Thompson weighting: the sample is uniform among the cell's
      // other points (conditioned on whether the point itself was peeled),
      // so scaling by others/sampled gives E[force] = exact all-pairs sum.
      // Exhaustively peeled cells (others == sampled) are exact.
      if (sampled > 0.0) velocity += (others / sampled) * pairSum;
    }
  }

  // Random jitter proportional to the velocity, to keep points from sticking.
  velocity += velocity * random.rg;

  // Bound the per-tick kick to the neighborhood scale. The estimator is unbiased
  // but high-variance: in a cell holding far more points than sampled slots, the
  // count/sampled weight can turn a few close samples into a huge one-tick kick.
  // Unbounded, that flings points across the screen at startup and \u2014 because the
  // weight is largest where density is highest \u2014 ejects points from dense cluster
  // centers, leaving voids. Clamping the magnitude keeps the spreading direction
  // while capping the fling; genuine spreading kicks are far below this bound and
  // pass through untouched. The far-field grid levels still drive bulk expansion.
  float maxStep = 2.0 * cellSize;
  float speed = length(velocity);
  if (speed > maxStep) velocity *= maxStep / speed;

  fragColor = vec4(velocity, 0.0, 0.0);
}
`,ti=`#version 300 es
precision highp float;

// Near-field pass of the 3D octree repulsion (P3M-style). After the finest level
// pass, the only un-accumulated region is the 3\xB3 neighborhood of the point's cell.
//
// Cell centroids exert a purely radial force there, which flattens dense hubs
// into disks and petals \u2014 even as a residual for unsampled mass, the centroid
// bias dominates (tangential repulsion scaled by ~K/n never spreads a dense
// clump before alpha decays). So the near field is a pure Monte-Carlo estimator
// instead: the K depth-peeled points of a cell are a uniform random subset
// (re-drawn every tick by build-nearfield-slots.vert), and weighting each
// sampled pairwise force by count/sampled makes the expected force equal the
// exact all-pairs sum \u2014 unbiased, no centroid term. Cells holding \u2264 K points
// are sampled exhaustively, so their forces are exact. The per-tick sampling
// noise acts as annealed jitter: it shrinks with alpha and is precisely what
// breaks clumps apart. The point itself is excluded from both the sample and
// the count.

uniform sampler2D positionsTexture;
uniform sampler2D levelTexture;
uniform sampler2D randomValues;
uniform sampler2D slotTexture0;
uniform sampler2D slotTexture1;
uniform sampler2D slotTexture2;
uniform sampler2D slotTexture3;
uniform sampler2D slotTexture4;
uniform sampler2D slotTexture5;
uniform sampler2D slotTexture6;
uniform sampler2D slotTexture7;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceNearField3DUniforms {
  float pointsTextureSize;
  float levelGridSize;
  float cellSize;
  float tilesPerRow;
  float alpha;
  float repulsion;
} forceNearField3D;

#define pointsTextureSize forceNearField3D.pointsTextureSize
#define levelGridSize forceNearField3D.levelGridSize
#define cellSize forceNearField3D.cellSize
#define tilesPerRow forceNearField3D.tilesPerRow
#define alpha forceNearField3D.alpha
#define repulsion forceNearField3D.repulsion
#else
uniform float pointsTextureSize;
uniform float levelGridSize;
uniform float cellSize;
uniform float tilesPerRow;
uniform float alpha;
uniform float repulsion;
#endif

in vec2 textureCoords;
out vec4 fragColor;

// Same clamped inverse-distance falloff as the level passes (must stay identical).
vec3 pairwiseVelocity(vec3 position, vec3 otherPosition, float mass) {
  vec3 distVector = position - otherPosition;
  float l = dot(distVector, distVector);
  if (l <= 0.0) return vec3(0.0);
  float distanceMin2 = 1.0;
  if (l < distanceMin2) l = sqrt(distanceMin2 * l);
  float addV = alpha * repulsion * mass / sqrt(l);
  return addV * normalize(distVector);
}

// One peeled slot of a cell: the unweighted pairwise force from the sampled
// point, counting it toward the sample size. Empty slots and the point itself
// contribute nothing.
vec3 slotVelocity(vec2 slot, vec3 position, float selfIndex, inout float sampled) {
  float index = slot.x;
  if (index < 0.0 || index == selfIndex) return vec3(0.0);
  int size = int(pointsTextureSize);
  int i = int(index);
  vec4 other = texelFetch(positionsTexture, ivec2(i % size, i / size), 0);
  sampled += 1.0;
  return pairwiseVelocity(position, vec3(other.rg, other.a), 1.0);
}

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec3 position = vec3(pointPosition.rg, pointPosition.a);
  float selfIndex = pointPosition.b;
  vec4 random = texture(randomValues, textureCoords);

  int gridSize = int(levelGridSize);
  int rowTiles = int(tilesPerRow);
  ivec3 pointCell = clamp(ivec3(floor(position / cellSize)), ivec3(0), ivec3(gridSize - 1));

  vec3 velocity = vec3(0.0);

  for (int k = -1; k <= 1; k += 1) {
    for (int j = -1; j <= 1; j += 1) {
      for (int i = -1; i <= 1; i += 1) {
        ivec3 cell = pointCell + ivec3(i, j, k);
        if (any(lessThan(cell, ivec3(0))) || any(greaterThanEqual(cell, ivec3(gridSize)))) continue;
        ivec2 pixel = ivec2(
          (cell.z % rowTiles) * gridSize + cell.x,
          (cell.z / rowTiles) * gridSize + cell.y
        );

        // [sum(x), sum(y), count, sum(z)] \u2014 only the count is used here.
        vec4 aggregate = texelFetch(levelTexture, pixel, 0);
        // The count never includes the point itself in the estimate.
        bool ownCell = (i == 0 && j == 0 && k == 0);
        float others = aggregate.b - (ownCell ? 1.0 : 0.0);
        if (others <= 0.0) continue;

        vec3 pairSum = vec3(0.0);
        float sampled = 0.0;
        // Sampler arrays cannot be indexed dynamically in GLSL ES 3.0 \u2014 unrolled.
        pairSum += slotVelocity(texelFetch(slotTexture0, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture1, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture2, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture3, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture4, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture5, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture6, pixel, 0).rg, position, selfIndex, sampled);
        pairSum += slotVelocity(texelFetch(slotTexture7, pixel, 0).rg, position, selfIndex, sampled);

        // Horvitz\u2013Thompson weighting: the sample is uniform among the cell's
        // other points (conditioned on whether the point itself was peeled),
        // so scaling by others/sampled gives E[force] = exact all-pairs sum.
        // Exhaustively peeled cells (others == sampled) are exact.
        if (sampled > 0.0) velocity += (others / sampled) * pairSum;
      }
    }
  }

  // Random jitter proportional to the velocity, like the 2D centermass fallback.
  velocity += velocity * random.rgb;

  // z velocity lives in the blue channel (update-position.frag SPACE_3D contract).
  fragColor = vec4(velocity, 0.0);
}
`,ii=`#version 300 es
precision highp float;

// One depth-peeling pass of the near-field point-slot build (2D).
//
// The precise grid's near field needs actual point-to-point forces (cell
// centroids alone exert a purely radial force that flattens dense hubs into
// disks and spikes). Each peeling pass selects, per finest-level cell, the
// not-yet-peeled point with the smallest per-tick random hash: the depth test
// keeps the smallest \`hashValue\` among eligible points, and eligibility excludes
// points already captured by the previous slot (hash <= previous slot's hash).
// Running K passes yields a uniform random K-subset per cell, re-randomized
// every tick via \`randomSeed\`; force-nearfield.frag turns it into an unbiased
// estimate of the cell's exact all-pairs repulsion (Monte-Carlo P3M).
//
// The 3D counterpart is build-nearfield-slots-3d.vert, which bins into a tiled
// octree layout instead of this flat grid.

uniform sampler2D positionsTexture;
uniform sampler2D previousSlot;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform buildNearFieldSlotsUniforms {
  float pointsTextureSize;
  float levelGridSize;
  float cellSize;
  float hasPreviousSlot;
  float randomSeed;
} buildNearFieldSlots;

#define pointsTextureSize buildNearFieldSlots.pointsTextureSize
#define levelGridSize buildNearFieldSlots.levelGridSize
#define cellSize buildNearFieldSlots.cellSize
#define hasPreviousSlot buildNearFieldSlots.hasPreviousSlot
#define randomSeed buildNearFieldSlots.randomSeed
#else
uniform float pointsTextureSize;
uniform float levelGridSize;
uniform float cellSize;
uniform float hasPreviousSlot;
uniform float randomSeed;
#endif

in vec2 pointIndices;

out vec2 slotData; // [point index, hash]

void main() {
  // Absent points must not be captured as neighbors \u2014 a NaN position bins to an
  // undefined cell and its distance poisons the force of every point sampling
  // that slot. Same guard as calculate-level.vert. (exit.G = absent)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    slotData = vec2(-1.0, 1.0);
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 1.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  float index = pointIndices.y * pointsTextureSize + pointIndices.x;

  // Per-tick random ordering via an integer hash (lowbias32). A fract(sin(...))
  // hash breaks down here: at large point indices GPU sin() loses precision
  // (differently per vendor), producing correlated or colliding hashes \u2014 and a
  // hash collision makes the peeling test below silently drop a point from the
  // sample. Integer ops are exact everywhere, and both inputs are exact (the
  // index is an integer-valued float; floatBitsToUint reinterprets seed bits).
  uint h = uint(index) ^ floatBitsToUint(randomSeed);
  h ^= h >> 16u;
  h *= 0x7feb352du;
  h ^= h >> 15u;
  h *= 0x846ca68bu;
  h ^= h >> 16u;
  // Top 24 bits only, so the value is exactly representable in a float32 and
  // round-trips bit-exactly through the slot texture into the next pass's
  // comparison. Kept strictly inside (0, 1) so the depth range is safe.
  float hashValue = (float(h >> 8u) + 0.5) / 16777216.0;
  hashValue = 0.001 + hashValue * 0.998;

  // Must match the cell formula of the aggregation and force shaders exactly.
  int gridSize = int(levelGridSize);
  ivec2 cell = clamp(ivec2(floor(pointPosition.rg / cellSize)), ivec2(0), ivec2(gridSize - 1));

  if (hasPreviousSlot > 0.5) {
    vec2 previous = texelFetch(previousSlot, cell, 0).rg;
    // Eligible only if the previous slot captured a point with a smaller hash.
    // An empty previous slot (index -1) means the cell is exhausted \u2014 otherwise
    // this pass would re-capture already-peeled points and double-count them.
    if (previous.x < 0.0 || hashValue <= previous.y) {
      slotData = vec2(-1.0, 1.0);
      gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
      gl_PointSize = 1.0;
      return;
    }
  }

  slotData = vec2(index, hashValue);
  vec2 ndc = 2.0 * (vec2(cell) + 0.5) / levelGridSize - 1.0;
  // The depth test (less) keeps the eligible point with the smallest hash.
  gl_Position = vec4(ndc, hashValue * 2.0 - 1.0, 1.0);
  gl_PointSize = 1.0;
}
`,oi=`#version 300 es
precision highp float;

// One depth-peeling pass of the near-field point-slot build.
//
// The octree's near field needs actual point-to-point forces (cell centroids
// alone exert a purely radial force that flattens dense hubs into disks and
// spikes). Each peeling pass selects, per finest-level cell, the not-yet-peeled
// point with the smallest per-tick random hash: the depth test keeps the
// smallest \`hashValue\` among eligible points, and eligibility excludes points
// already captured by the previous slot (hash <= previous slot's hash). Running
// K passes yields a uniform random K-subset per cell, re-randomized every tick
// via \`randomSeed\`; force-nearfield-3d.frag turns it into an unbiased estimate
// of the cell's exact all-pairs repulsion (Monte-Carlo P3M).

uniform sampler2D positionsTexture;
uniform sampler2D previousSlot;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform buildNearFieldSlots3DUniforms {
  float pointsTextureSize;
  float levelGridSize;
  float cellSize;
  float tilesPerRow;
  float levelTextureWidth;
  float levelTextureHeight;
  float hasPreviousSlot;
  float randomSeed;
} buildNearFieldSlots3D;

#define pointsTextureSize buildNearFieldSlots3D.pointsTextureSize
#define levelGridSize buildNearFieldSlots3D.levelGridSize
#define cellSize buildNearFieldSlots3D.cellSize
#define tilesPerRow buildNearFieldSlots3D.tilesPerRow
#define levelTextureWidth buildNearFieldSlots3D.levelTextureWidth
#define levelTextureHeight buildNearFieldSlots3D.levelTextureHeight
#define hasPreviousSlot buildNearFieldSlots3D.hasPreviousSlot
#define randomSeed buildNearFieldSlots3D.randomSeed
#else
uniform float pointsTextureSize;
uniform float levelGridSize;
uniform float cellSize;
uniform float tilesPerRow;
uniform float levelTextureWidth;
uniform float levelTextureHeight;
uniform float hasPreviousSlot;
uniform float randomSeed;
#endif

in vec2 pointIndices;

out vec2 slotData; // [point index, hash]

void main() {
  // Absent points must not be captured as neighbors \u2014 a NaN position bins to an
  // undefined cell and its distance poisons the force of every point sampling
  // that slot. Same guard as calculate-level-3d.vert. (exit.G = absent)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    slotData = vec2(-1.0, 1.0);
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 1.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  vec3 position = vec3(pointPosition.rg, pointPosition.a);
  float index = pointIndices.y * pointsTextureSize + pointIndices.x;

  // Per-tick random ordering via an integer hash (lowbias32). A fract(sin(...))
  // hash breaks down here: at large point indices GPU sin() loses precision
  // (differently per vendor), producing correlated or colliding hashes \u2014 and a
  // hash collision makes the peeling test below silently drop a point from the
  // sample. Integer ops are exact everywhere, and both inputs are exact (the
  // index is an integer-valued float; floatBitsToUint reinterprets seed bits).
  uint h = uint(index) ^ floatBitsToUint(randomSeed);
  h ^= h >> 16u;
  h *= 0x7feb352du;
  h ^= h >> 15u;
  h *= 0x846ca68bu;
  h ^= h >> 16u;
  // Top 24 bits only, so the value is exactly representable in a float32 and
  // round-trips bit-exactly through the slot texture into the next pass's
  // comparison. Kept strictly inside (0, 1) so the depth range is safe.
  float hashValue = (float(h >> 8u) + 0.5) / 16777216.0;
  hashValue = 0.001 + hashValue * 0.998;

  // Must match the cell formula of the aggregation and force shaders exactly.
  int gridSize = int(levelGridSize);
  ivec3 cell = clamp(ivec3(floor(position / cellSize)), ivec3(0), ivec3(gridSize - 1));
  int rowTiles = int(tilesPerRow);
  ivec2 pixel = ivec2(
    (cell.z % rowTiles) * gridSize + cell.x,
    (cell.z / rowTiles) * gridSize + cell.y
  );

  if (hasPreviousSlot > 0.5) {
    vec2 previous = texelFetch(previousSlot, pixel, 0).rg;
    // Eligible only if the previous slot captured a point with a smaller hash.
    // An empty previous slot (index -1) means the cell is exhausted \u2014 otherwise
    // this pass would re-capture already-peeled points and double-count them.
    if (previous.x < 0.0 || hashValue <= previous.y) {
      slotData = vec2(-1.0, 1.0);
      gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
      gl_PointSize = 1.0;
      return;
    }
  }

  slotData = vec2(index, hashValue);
  vec2 ndc = 2.0 * (vec2(pixel) + 0.5) / vec2(levelTextureWidth, levelTextureHeight) - 1.0;
  // The depth test (less) keeps the eligible point with the smallest hash.
  gl_Position = vec4(ndc, hashValue * 2.0 - 1.0, 1.0);
  gl_PointSize = 1.0;
}
`,We=`#version 300 es
precision highp float;

in vec2 slotData;
out vec4 fragColor;

void main() {
  fragColor = vec4(slotData, 0.0, 0.0);
}
`,si=`#version 300 es
precision highp float;

// Exact O(n\xB2) 3D repulsion, used for graphs up to BRUTE_FORCE_3D_MAX_POINTS points
// (larger 3D graphs use the octree passes in calculate-level-3d / force-level-3d /
// force-centermass-3d). It matches the 2D force semantics (d3-style clamped
// inverse-distance falloff) with per-point mass 1.

uniform sampler2D positionsTexture;
uniform sampler2D randomValues;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform forceBruteForceUniforms {
  float pointsTextureSize;
  float pointsNumber;
  float alpha;
  float repulsion;
} forceBruteForce;

#define pointsTextureSize forceBruteForce.pointsTextureSize
#define pointsNumber forceBruteForce.pointsNumber
#define alpha forceBruteForce.alpha
#define repulsion forceBruteForce.repulsion
#else
uniform float pointsTextureSize;
uniform float pointsNumber;
uniform float alpha;
uniform float repulsion;
#endif

in vec2 textureCoords;
out vec4 fragColor;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  // z lives in the position alpha channel
  vec3 position = vec3(pointPosition.rg, pointPosition.a);
  vec4 random = texture(randomValues, textureCoords);

  vec3 velocity = vec3(0.0);
  int size = int(pointsTextureSize);
  int count = int(pointsNumber);
  ivec2 selfPixel = ivec2(gl_FragCoord.xy);
  int pointIndex = 0;

  for (int j = 0; j < size; j += 1) {
    if (pointIndex >= count) break;
    for (int i = 0; i < size; i += 1) {
      if (pointIndex >= count) break;
      pointIndex += 1;
      if (i == selfPixel.x && j == selfPixel.y) continue;

      vec4 otherPosition = texelFetch(positionsTexture, ivec2(i, j), 0);
      vec3 distVector = position - vec3(otherPosition.rg, otherPosition.a);
      float l = dot(distVector, distVector);
      if (l == 0.0) {
        // Coincident points: kick in this point's own random direction so pairs
        // can separate (each point has a different random value).
        distVector = random.rgb;
        l = dot(distVector, distVector);
        if (l == 0.0) continue;
      }

      // Mirrors the 2D level force: c / dist with a minimum-distance clamp.
      float distanceMin2 = 1.0;
      if (l < distanceMin2) l = sqrt(distanceMin2 * l);
      float addV = alpha * repulsion / sqrt(l);
      velocity += addV * normalize(distVector);
    }
  }

  // Random jitter proportional to the velocity, like the 2D centermass force.
  velocity += velocity * random.rgb;

  fragColor = vec4(velocity, 0.0);
}
`,He=4096,ri=512,ni=64,me=8,re=8;class je extends V{constructor(){super(...arguments),this.levels=0,this.levelTargets=new Map,this.levels3D=0,this.levelTargets3D=new Map,this.nearFieldSlotTargets=[],this.nearFieldSlotTargets3D=[]}create(){var e,t,i,o;const{device:s,store:r}=this;if(!r.pointsTextureSize)return;r.is3D?(this.destroyLevelTargets(),this.levels=0,this.createLevels3D()):(this.destroyLevelTargets3D(),this.levels3D=0,this.createLevels());const n=r.pointsTextureSize*r.pointsTextureSize,a=new Float32Array(n*4);for(let l=0;l<n;++l)a[l*4]=r.getRandomFloat(-1,1)*1e-5,a[l*4+1]=r.getRandomFloat(-1,1)*1e-5,a[l*4+2]=r.getRandomFloat(-1,1)*1e-5;if((!this.randomValuesTexture||this.randomValuesTexture.destroyed||this.randomValuesTexture.width!==r.pointsTextureSize||this.randomValuesTexture.height!==r.pointsTextureSize)&&(this.randomValuesTexture&&!this.randomValuesTexture.destroyed&&this.randomValuesTexture.destroy(),this.randomValuesTexture=s.createTexture({width:r.pointsTextureSize,height:r.pointsTextureSize,format:"rgba32float",usage:g.SAMPLE|g.COPY_DST})),this.randomValuesTexture.copyImageData({data:a,bytesPerRow:y("rgba32float",r.pointsTextureSize),mipLevel:0,x:0,y:0}),!this.pointIndices||this.previousPointsTextureSize!==r.pointsTextureSize){this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy();const l=K(r.pointsTextureSize);this.pointIndices=s.createBuffer({data:l,usage:x.VERTEX|x.COPY_DST}),(e=this.calculateLevelsCommand)==null||e.setAttributes({pointIndices:this.pointIndices}),(t=this.calculateLevels3DCommand)==null||t.setAttributes({pointIndices:this.pointIndices}),(i=this.buildNearFieldSlotsCommand)==null||i.setAttributes({pointIndices:this.pointIndices}),(o=this.buildNearFieldSlots3DCommand)==null||o.setAttributes({pointIndices:this.pointIndices})}this.previousPointsTextureSize=r.pointsTextureSize,this.previousPointsNumber=this.data.pointsNumber}initPrograms(){const{device:e,store:t,data:i,points:o}=this;!i.pointsNumber||!o||!t.pointsTextureSize||(this.forceVertexCoordBuffer||(this.forceVertexCoordBuffer=e.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.calculateLevelsUniformStore||(this.calculateLevelsUniformStore=new T(e,{calculateLevelsPreciseUniforms:{uniformTypes:{pointsTextureSize:"f32",levelGridSize:"f32",cellSize:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,levelGridSize:0,cellSize:0}}})),this.calculateLevelsCommand||(this.calculateLevelsCommand=new b(e,{fs:Ge,vs:Kt,topology:"point-list",vertexCount:i.pointsNumber,attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{calculateLevelsPreciseUniforms:this.calculateLevelsUniformStore.getManagedUniformBuffer("calculateLevelsPreciseUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.forceLevelUniformStore||(this.forceLevelUniformStore=new T(e,{forceLevelPreciseUniforms:{uniformTypes:{levelGridSize:"f32",cellSize:"f32",isFirstLevel:"f32",alpha:"f32",repulsion:"f32"},defaultUniforms:{levelGridSize:0,cellSize:0,isFirstLevel:0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}})),this.forceLevelCommand||(this.forceLevelCommand=new b(e,{fs:Qt,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{forceLevelPreciseUniforms:this.forceLevelUniformStore.getManagedUniformBuffer("forceLevelPreciseUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.buildNearFieldSlotsUniformStore||(this.buildNearFieldSlotsUniformStore=new T(e,{buildNearFieldSlotsUniforms:{uniformTypes:{pointsTextureSize:"f32",levelGridSize:"f32",cellSize:"f32",hasPreviousSlot:"f32",randomSeed:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,levelGridSize:0,cellSize:0,hasPreviousSlot:0,randomSeed:0}}})),this.buildNearFieldSlotsCommand||(this.buildNearFieldSlotsCommand=new b(e,{fs:We,vs:ii,topology:"point-list",vertexCount:i.pointsNumber,attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{buildNearFieldSlotsUniforms:this.buildNearFieldSlotsUniformStore.getManagedUniformBuffer("buildNearFieldSlotsUniforms")},parameters:{blend:!1,depthWriteEnabled:!0,depthCompare:"less"}})),this.forceNearFieldUniformStore||(this.forceNearFieldUniformStore=new T(e,{forceNearFieldUniforms:{uniformTypes:{pointsTextureSize:"f32",levelGridSize:"f32",cellSize:"f32",alpha:"f32",repulsion:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,levelGridSize:0,cellSize:0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}})),this.forceNearFieldCommand||(this.forceNearFieldCommand=new b(e,{fs:ei,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{forceNearFieldUniforms:this.forceNearFieldUniformStore.getManagedUniformBuffer("forceNearFieldUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),t.is3D&&(this.bruteForce3DUniformStore||(this.bruteForce3DUniformStore=new T(e,{forceBruteForceUniforms:{uniformTypes:{pointsTextureSize:"f32",pointsNumber:"f32",alpha:"f32",repulsion:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,pointsNumber:i.pointsNumber,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}})),this.bruteForce3DCommand||(this.bruteForce3DCommand=new b(e,{fs:si,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{forceBruteForceUniforms:this.bruteForce3DUniformStore.getManagedUniformBuffer("forceBruteForceUniforms")},parameters:{depthWriteEnabled:!1,depthCompare:"always"}})),this.calculateLevels3DUniformStore||(this.calculateLevels3DUniformStore=new T(e,{calculateLevels3DUniforms:{uniformTypes:{pointsTextureSize:"f32",levelGridSize:"f32",cellSize:"f32",tilesPerRow:"f32",levelTextureWidth:"f32",levelTextureHeight:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,levelGridSize:0,cellSize:0,tilesPerRow:0,levelTextureWidth:0,levelTextureHeight:0}}})),this.calculateLevels3DCommand||(this.calculateLevels3DCommand=new b(e,{fs:Ge,vs:$t,topology:"point-list",vertexCount:i.pointsNumber,attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{calculateLevels3DUniforms:this.calculateLevels3DUniformStore.getManagedUniformBuffer("calculateLevels3DUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.forceLevel3DUniformStore||(this.forceLevel3DUniformStore=new T(e,{forceLevel3DUniforms:{uniformTypes:{levelGridSize:"f32",cellSize:"f32",tilesPerRow:"f32",isFirstLevel:"f32",alpha:"f32",repulsion:"f32"},defaultUniforms:{levelGridSize:0,cellSize:0,tilesPerRow:0,isFirstLevel:0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}})),this.forceLevel3DCommand||(this.forceLevel3DCommand=new b(e,{fs:Jt,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{forceLevel3DUniforms:this.forceLevel3DUniformStore.getManagedUniformBuffer("forceLevel3DUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.buildNearFieldSlots3DUniformStore||(this.buildNearFieldSlots3DUniformStore=new T(e,{buildNearFieldSlots3DUniforms:{uniformTypes:{pointsTextureSize:"f32",levelGridSize:"f32",cellSize:"f32",tilesPerRow:"f32",levelTextureWidth:"f32",levelTextureHeight:"f32",hasPreviousSlot:"f32",randomSeed:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,levelGridSize:0,cellSize:0,tilesPerRow:0,levelTextureWidth:0,levelTextureHeight:0,hasPreviousSlot:0,randomSeed:0}}})),this.buildNearFieldSlots3DCommand||(this.buildNearFieldSlots3DCommand=new b(e,{fs:We,vs:oi,topology:"point-list",vertexCount:i.pointsNumber,attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{buildNearFieldSlots3DUniforms:this.buildNearFieldSlots3DUniformStore.getManagedUniformBuffer("buildNearFieldSlots3DUniforms")},parameters:{blend:!1,depthWriteEnabled:!0,depthCompare:"less"}})),this.forceNearField3DUniformStore||(this.forceNearField3DUniformStore=new T(e,{forceNearField3DUniforms:{uniformTypes:{pointsTextureSize:"f32",levelGridSize:"f32",cellSize:"f32",tilesPerRow:"f32",alpha:"f32",repulsion:"f32"},defaultUniforms:{pointsTextureSize:t.pointsTextureSize,levelGridSize:0,cellSize:0,tilesPerRow:0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}})),this.forceNearField3DCommand||(this.forceNearField3DCommand=new b(e,{fs:ti,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.forceVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{forceNearField3DUniforms:this.forceNearField3DUniformStore.getManagedUniformBuffer("forceNearField3DUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}}))))}run(){this.store.pointsTextureSize!==this.previousPointsTextureSize||this.data.pointsNumber!==this.previousPointsNumber||(this.store.is3D?(this.data.pointsNumber??0)>He&&this.levelTargets3D.size>0&&this.nearFieldSlotTargets3D.length===re?(this.drawLevels3D(),this.drawNearFieldSlots3D(),this.drawForcesOctree3D()):this.drawForcesBruteForce3D():(this.drawLevels(),this.drawNearFieldSlots(),this.drawForces()))}destroy(){var e,t,i,o,s,r,n,a,l,u,d,c,f,p,m,S,v,C;(e=this.calculateLevelsCommand)==null||e.destroy(),this.calculateLevelsCommand=void 0,(t=this.forceLevelCommand)==null||t.destroy(),this.forceLevelCommand=void 0,(i=this.buildNearFieldSlotsCommand)==null||i.destroy(),this.buildNearFieldSlotsCommand=void 0,(o=this.forceNearFieldCommand)==null||o.destroy(),this.forceNearFieldCommand=void 0,(s=this.bruteForce3DCommand)==null||s.destroy(),this.bruteForce3DCommand=void 0,(r=this.calculateLevels3DCommand)==null||r.destroy(),this.calculateLevels3DCommand=void 0,(n=this.forceLevel3DCommand)==null||n.destroy(),this.forceLevel3DCommand=void 0,(a=this.buildNearFieldSlots3DCommand)==null||a.destroy(),this.buildNearFieldSlots3DCommand=void 0,(l=this.forceNearField3DCommand)==null||l.destroy(),this.forceNearField3DCommand=void 0,this.destroyLevelTargets(),this.randomValuesTexture&&!this.randomValuesTexture.destroyed&&this.randomValuesTexture.destroy(),this.randomValuesTexture=void 0,this.destroyLevelTargets3D(),(u=this.calculateLevelsUniformStore)==null||u.destroy(),this.calculateLevelsUniformStore=void 0,(d=this.forceLevelUniformStore)==null||d.destroy(),this.forceLevelUniformStore=void 0,(c=this.buildNearFieldSlotsUniformStore)==null||c.destroy(),this.buildNearFieldSlotsUniformStore=void 0,(f=this.forceNearFieldUniformStore)==null||f.destroy(),this.forceNearFieldUniformStore=void 0,(p=this.bruteForce3DUniformStore)==null||p.destroy(),this.bruteForce3DUniformStore=void 0,(m=this.calculateLevels3DUniformStore)==null||m.destroy(),this.calculateLevels3DUniformStore=void 0,(S=this.forceLevel3DUniformStore)==null||S.destroy(),this.forceLevel3DUniformStore=void 0,(v=this.buildNearFieldSlots3DUniformStore)==null||v.destroy(),this.buildNearFieldSlots3DUniformStore=void 0,(C=this.forceNearField3DUniformStore)==null||C.destroy(),this.forceNearField3DUniformStore=void 0,this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy(),this.pointIndices=void 0,this.forceVertexCoordBuffer&&!this.forceVertexCoordBuffer.destroyed&&this.forceVertexCoordBuffer.destroy(),this.forceVertexCoordBuffer=void 0}drawForcesBruteForce3D(){const{device:e,store:t,data:i,points:o}=this;if(!o||!this.bruteForce3DCommand||!this.bruteForce3DUniformStore||!o.previousPositionTexture||o.previousPositionTexture.destroyed||!this.randomValuesTexture||this.randomValuesTexture.destroyed||!o.velocityFbo||o.velocityFbo.destroyed)return;this.bruteForce3DUniformStore.setUniforms({forceBruteForceUniforms:{pointsTextureSize:t.pointsTextureSize??0,pointsNumber:i.pointsNumber??0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}),this.bruteForce3DCommand.setBindings({positionsTexture:o.previousPositionTexture,randomValues:this.randomValuesTexture});const s=e.beginRenderPass({framebuffer:o.velocityFbo,clearColor:[0,0,0,0]});this.bruteForce3DCommand.draw(s),s.end()}drawLevels3D(){const{device:e,store:t,data:i,points:o}=this;if(o&&!(!this.calculateLevels3DCommand||!this.calculateLevels3DUniformStore)&&!(!o.previousPositionTexture||o.previousPositionTexture.destroyed)&&!(!o.exitTexture||o.exitTexture.destroyed)&&i.pointsNumber&&this.pointIndices)for(let s=0;s<this.levels3D;s+=1){const r=this.levelTargets3D.get(s);if(!r||r.fbo.destroyed||r.texture.destroyed)continue;this.calculateLevels3DUniformStore.setUniforms({calculateLevels3DUniforms:{pointsTextureSize:t.pointsTextureSize??0,levelGridSize:r.gridSize,cellSize:t.adjustedSpaceSize/r.gridSize,tilesPerRow:r.tilesPerRow,levelTextureWidth:r.width,levelTextureHeight:r.height}}),this.calculateLevels3DCommand.setVertexCount(i.pointsNumber),this.calculateLevels3DCommand.setBindings({positionsTexture:o.previousPositionTexture,exitTexture:o.exitTexture});const n=e.beginRenderPass({framebuffer:r.fbo,clearColor:[0,0,0,0]});this.calculateLevels3DCommand.draw(n),n.end()}}drawForcesOctree3D(){const{device:e,store:t,points:i}=this;if(!i||!this.forceLevel3DCommand||!this.forceLevel3DUniformStore||!this.forceNearField3DCommand||!this.forceNearField3DUniformStore||this.nearFieldSlotTargets3D.length!==re||!i.previousPositionTexture||i.previousPositionTexture.destroyed||!this.randomValuesTexture||this.randomValuesTexture.destroyed||!i.velocityFbo||i.velocityFbo.destroyed)return;const o=e.beginRenderPass({framebuffer:i.velocityFbo,clearColor:[0,0,0,0]});for(let s=0;s<this.levels3D;s+=1){const r=this.levelTargets3D.get(s);if(!r||r.texture.destroyed)continue;const n=t.adjustedSpaceSize/r.gridSize;this.forceLevel3DUniformStore.setUniforms({forceLevel3DUniforms:{levelGridSize:r.gridSize,cellSize:n,tilesPerRow:r.tilesPerRow,isFirstLevel:s===0?1:0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}),this.forceLevel3DCommand.setBindings({positionsTexture:i.previousPositionTexture,levelTexture:r.texture}),this.forceLevel3DCommand.draw(o),s===this.levels3D-1&&(this.forceNearField3DUniformStore.setUniforms({forceNearField3DUniforms:{pointsTextureSize:t.pointsTextureSize??0,levelGridSize:r.gridSize,cellSize:n,tilesPerRow:r.tilesPerRow,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}),this.forceNearField3DCommand.setBindings({positionsTexture:i.previousPositionTexture,levelTexture:r.texture,randomValues:this.randomValuesTexture,slotTexture0:this.nearFieldSlotTargets3D[0].texture,slotTexture1:this.nearFieldSlotTargets3D[1].texture,slotTexture2:this.nearFieldSlotTargets3D[2].texture,slotTexture3:this.nearFieldSlotTargets3D[3].texture,slotTexture4:this.nearFieldSlotTargets3D[4].texture,slotTexture5:this.nearFieldSlotTargets3D[5].texture,slotTexture6:this.nearFieldSlotTargets3D[6].texture,slotTexture7:this.nearFieldSlotTargets3D[7].texture}),this.forceNearField3DCommand.draw(o))}o.end()}drawNearFieldSlots3D(){const{device:e,store:t,data:i,points:o}=this;if(!o||!this.buildNearFieldSlots3DCommand||!this.buildNearFieldSlots3DUniformStore||!o.previousPositionTexture||o.previousPositionTexture.destroyed||!o.exitTexture||o.exitTexture.destroyed||!i.pointsNumber||!this.pointIndices)return;const s=this.levelTargets3D.get(this.levels3D-1);if(!s||s.texture.destroyed)return;const r=t.getRandomFloat(0,1);for(let n=0;n<this.nearFieldSlotTargets3D.length;n+=1){const a=this.nearFieldSlotTargets3D[n];if(!a||a.fbo.destroyed)continue;this.buildNearFieldSlots3DUniformStore.setUniforms({buildNearFieldSlots3DUniforms:{pointsTextureSize:t.pointsTextureSize??0,levelGridSize:s.gridSize,cellSize:t.adjustedSpaceSize/s.gridSize,tilesPerRow:s.tilesPerRow,levelTextureWidth:s.width,levelTextureHeight:s.height,hasPreviousSlot:n===0?0:1,randomSeed:r}}),this.buildNearFieldSlots3DCommand.setVertexCount(i.pointsNumber),this.buildNearFieldSlots3DCommand.setBindings({positionsTexture:o.previousPositionTexture,exitTexture:o.exitTexture,previousSlot:n===0?o.previousPositionTexture:this.nearFieldSlotTargets3D[n-1].texture});const l=e.beginRenderPass({framebuffer:a.fbo,clearColor:[-1,1,0,0],clearDepth:1});this.buildNearFieldSlots3DCommand.draw(l),l.end()}}drawNearFieldSlots(){const{device:e,store:t,data:i,points:o}=this;if(!o||!this.buildNearFieldSlotsCommand||!this.buildNearFieldSlotsUniformStore||!o.previousPositionTexture||o.previousPositionTexture.destroyed||!o.exitTexture||o.exitTexture.destroyed||!i.pointsNumber||!this.pointIndices)return;const s=this.levelTargets.get(this.levels-1);if(!s||s.texture.destroyed)return;const r=t.getRandomFloat(0,1);for(let n=0;n<this.nearFieldSlotTargets.length;n+=1){const a=this.nearFieldSlotTargets[n];if(!a||a.fbo.destroyed)continue;this.buildNearFieldSlotsUniformStore.setUniforms({buildNearFieldSlotsUniforms:{pointsTextureSize:t.pointsTextureSize??0,levelGridSize:s.gridSize,cellSize:t.adjustedSpaceSize/s.gridSize,hasPreviousSlot:n===0?0:1,randomSeed:r}}),this.buildNearFieldSlotsCommand.setVertexCount(i.pointsNumber),this.buildNearFieldSlotsCommand.setBindings({positionsTexture:o.previousPositionTexture,exitTexture:o.exitTexture,previousSlot:n===0?o.previousPositionTexture:this.nearFieldSlotTargets[n-1].texture});const l=e.beginRenderPass({framebuffer:a.fbo,clearColor:[-1,1,0,0],clearDepth:1});this.buildNearFieldSlotsCommand.draw(l),l.end()}}createLevels3D(){const{device:e}=this,t=this.data.pointsNumber??0;if(t<=He){this.destroyLevelTargets3D(),this.levels3D=0;return}const i=2*Math.cbrt(t),o=Math.min(ni,Math.max(8,Math.pow(2,Math.ceil(Math.log2(i)))));this.levels3D=Math.log2(o)-1;for(let r=0;r<this.levels3D;r+=1){const n=Math.pow(2,r+2),a=Math.ceil(Math.sqrt(n)),l=n*a,u=n*Math.ceil(n/a),d=this.levelTargets3D.get(r);if(d&&d.width===l&&d.height===u)continue;d&&(d.fbo.destroyed||d.fbo.destroy(),d.texture.destroyed||d.texture.destroy());const c=e.createTexture({width:l,height:u,format:"rgba32float",usage:g.SAMPLE|g.RENDER}),f=e.createFramebuffer({width:l,height:u,colorAttachments:[c]});this.levelTargets3D.set(r,{texture:c,fbo:f,gridSize:n,tilesPerRow:a,width:l,height:u})}for(const[r,n]of Array.from(this.levelTargets3D.entries()))r>=this.levels3D&&(n.fbo.destroyed||n.fbo.destroy(),n.texture.destroyed||n.texture.destroy(),this.levelTargets3D.delete(r));const s=this.levelTargets3D.get(this.levels3D-1);s&&this.createNearFieldSlotTargets3D(s)}createNearFieldSlotTargets3D(e){const t=this.nearFieldSlotTargets3D[0];t&&!t.texture.destroyed&&t.texture.width===e.width&&t.texture.height===e.height&&this.nearFieldSlotTargets3D.length===re||(this.destroyNearFieldSlotTargets3D(),this.nearFieldSlotTargets3D=this.createSlotTargets(e.width,e.height,re))}createLevels(){const{device:e}=this,t=this.data.pointsNumber??0,i=2*Math.sqrt(t),o=Math.min(ri,Math.max(8,Math.pow(2,Math.ceil(Math.log2(i)))));this.levels=Math.log2(o)-1;for(let r=0;r<this.levels;r+=1){if(this.levelTargets.has(r))continue;const n=Math.pow(2,r+2),a=e.createTexture({width:n,height:n,format:"rgba32float",usage:g.SAMPLE|g.RENDER}),l=e.createFramebuffer({width:n,height:n,colorAttachments:[a]});this.levelTargets.set(r,{texture:a,fbo:l,gridSize:n})}for(const[r,n]of Array.from(this.levelTargets.entries()))r>=this.levels&&(n.fbo.destroyed||n.fbo.destroy(),n.texture.destroyed||n.texture.destroy(),this.levelTargets.delete(r));const s=this.levelTargets.get(this.levels-1);s&&this.createNearFieldSlotTargets(s)}createNearFieldSlotTargets(e){const t=this.nearFieldSlotTargets[0];t&&!t.texture.destroyed&&t.texture.width===e.gridSize&&t.texture.height===e.gridSize&&this.nearFieldSlotTargets.length===me||(this.destroyNearFieldSlotTargets(),this.nearFieldSlotTargets=this.createSlotTargets(e.gridSize,e.gridSize,me))}createSlotTargets(e,t,i){const{device:o}=this,s=[];for(let r=0;r<i;r+=1){const n=o.createTexture({width:e,height:t,format:"rg32float",usage:g.SAMPLE|g.RENDER}),a=o.createFramebuffer({width:e,height:t,colorAttachments:[n],depthStencilAttachment:"depth24plus"});s.push({texture:n,fbo:a})}return s}destroyNearFieldSlotTargets(){for(const e of this.nearFieldSlotTargets)e.fbo.destroyed||e.fbo.destroy(),e.texture.destroyed||e.texture.destroy();this.nearFieldSlotTargets=[]}destroyNearFieldSlotTargets3D(){for(const e of this.nearFieldSlotTargets3D)e.fbo.destroyed||e.fbo.destroy(),e.texture.destroyed||e.texture.destroy();this.nearFieldSlotTargets3D=[]}destroyLevelTargets(){for(const e of this.levelTargets.values())e.fbo.destroyed||e.fbo.destroy(),e.texture.destroyed||e.texture.destroy();this.levelTargets.clear(),this.destroyNearFieldSlotTargets()}destroyLevelTargets3D(){for(const e of this.levelTargets3D.values())e.fbo.destroyed||e.fbo.destroy(),e.texture.destroyed||e.texture.destroy();this.levelTargets3D.clear(),this.destroyNearFieldSlotTargets3D()}drawLevels(){const{device:e,store:t,data:i,points:o}=this;if(o&&!(!this.calculateLevelsCommand||!this.calculateLevelsUniformStore)&&!(!o.previousPositionTexture||o.previousPositionTexture.destroyed)&&!(!o.exitTexture||o.exitTexture.destroyed)&&i.pointsNumber&&this.pointIndices)for(let s=0;s<this.levels;s+=1){const r=this.levelTargets.get(s);if(!r||r.fbo.destroyed||r.texture.destroyed)continue;this.calculateLevelsUniformStore.setUniforms({calculateLevelsPreciseUniforms:{pointsTextureSize:t.pointsTextureSize??0,levelGridSize:r.gridSize,cellSize:t.adjustedSpaceSize/r.gridSize}}),this.calculateLevelsCommand.setVertexCount(i.pointsNumber),this.calculateLevelsCommand.setBindings({positionsTexture:o.previousPositionTexture,exitTexture:o.exitTexture});const n=e.beginRenderPass({framebuffer:r.fbo,clearColor:[0,0,0,0]});this.calculateLevelsCommand.draw(n),n.end()}}drawForces(){const{device:e,store:t,points:i}=this;if(!i||!this.forceLevelCommand||!this.forceLevelUniformStore||!this.forceNearFieldCommand||!this.forceNearFieldUniformStore||this.nearFieldSlotTargets.length!==me||!i.previousPositionTexture||i.previousPositionTexture.destroyed||!this.randomValuesTexture||this.randomValuesTexture.destroyed||!i.velocityFbo||i.velocityFbo.destroyed)return;const o=e.beginRenderPass({framebuffer:i.velocityFbo,clearColor:[0,0,0,0]});for(let s=0;s<this.levels;s+=1){const r=this.levelTargets.get(s);if(!r||r.texture.destroyed)continue;const n=t.adjustedSpaceSize/r.gridSize;this.forceLevelUniformStore.setUniforms({forceLevelPreciseUniforms:{levelGridSize:r.gridSize,cellSize:n,isFirstLevel:s===0?1:0,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}),this.forceLevelCommand.setBindings({positionsTexture:i.previousPositionTexture,levelTexture:r.texture}),this.forceLevelCommand.draw(o),s===this.levels-1&&(this.forceNearFieldUniformStore.setUniforms({forceNearFieldUniforms:{pointsTextureSize:t.pointsTextureSize??0,levelGridSize:r.gridSize,cellSize:n,alpha:t.alpha,repulsion:this.config.simulationRepulsion}}),this.forceNearFieldCommand.setBindings({positionsTexture:i.previousPositionTexture,levelTexture:r.texture,randomValues:this.randomValuesTexture,slotTexture0:this.nearFieldSlotTargets[0].texture,slotTexture1:this.nearFieldSlotTargets[1].texture,slotTexture2:this.nearFieldSlotTargets[2].texture,slotTexture3:this.nearFieldSlotTargets[3].texture,slotTexture4:this.nearFieldSlotTargets[4].texture,slotTexture5:this.nearFieldSlotTargets[5].texture,slotTexture6:this.nearFieldSlotTargets[6].texture,slotTexture7:this.nearFieldSlotTargets[7].texture}),this.forceNearFieldCommand.draw(o))}o.end()}}const ai=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec4 rgba;

out vec4 fragColor;

void main() {
  fragColor = rgba;
}`,li=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;
uniform sampler2D clusterTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform calculateCentermassUniforms {
  float pointsTextureSize;
  float clustersTextureSize;
} calculateCentermass;

#define pointsTextureSize calculateCentermass.pointsTextureSize
#define clustersTextureSize calculateCentermass.clustersTextureSize
#else
uniform float pointsTextureSize;
uniform float clustersTextureSize;
#endif

in vec2 pointIndices;

out vec4 rgba;

void main() {
  rgba = vec4(0.0);

  // Absent points must not contribute to their cluster's centroid. (exit.G = absent)
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  if (exitStatus.g > 0.5) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  // Payload accumulated per cluster pixel: [sum(x), sum(y), count, sum(z)].
  // The position texture stores z in the alpha channel in 3D mode.
#ifdef SPACE_3D
  rgba = vec4(pointPosition.xy, 1.0, pointPosition.a);
#else
  rgba = vec4(pointPosition.xy, 1.0, 0.0);
#endif

  vec4 pointClusterIndices = texture(clusterTexture, (pointIndices + 0.5) / pointsTextureSize);
  // Unclustered points ([-1, -1]) must not contribute mass to any cluster \u2014
  // vec2(0.0) is the NDC center (a real cluster's texel), so cull them off-screen.
  if (pointClusterIndices.x < 0.0 || pointClusterIndices.y < 0.0) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 1.0;
    return;
  }
  vec2 xy = 2.0 * (pointClusterIndices.xy + 0.5) / clustersTextureSize - 1.0;

  gl_Position = vec4(xy, 0.0, 1.0);
  gl_PointSize = 1.0;
}
`,di=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;
uniform sampler2D centermassTexture;
uniform sampler2D clusterTexture;
uniform sampler2D clusterPositionsTexture;
uniform sampler2D clusterForceCoefficient;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform applyForcesUniforms {
  float alpha;
  float clustersTextureSize;
  float clusterCoefficient;
} applyForces;

#define alpha applyForces.alpha
#define clustersTextureSize applyForces.clustersTextureSize
#define clusterCoefficient applyForces.clusterCoefficient
#else
uniform float alpha;
uniform float clustersTextureSize;
uniform float clusterCoefficient;
#endif

in vec2 textureCoords;

out vec4 fragColor;


void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec4 velocity = vec4(0.0);
  vec4 pointClusterIndices = texture(clusterTexture, textureCoords);
  // no cluster, so no forces
  if (pointClusterIndices.x >= 0.0 && pointClusterIndices.y >= 0.0) {
#ifdef SPACE_3D
    // positioning points to custom cluster position or either to the center of mass;
    // the centermass texture holds [sum(x), sum(y), count, sum(z)] and the position
    // texture stores z in the alpha channel
    vec4 custom = texture(clusterPositionsTexture, pointClusterIndices.xy / clustersTextureSize);
    vec4 centermassValues = texture(centermassTexture, pointClusterIndices.xy / clustersTextureSize);
    vec3 centermass = vec3(centermassValues.rg, centermassValues.a) / centermassValues.b;
    vec3 clusterPositions;
    if (custom.x < 0.0 || custom.y < 0.0) {
      clusterPositions = centermass;
    } else {
      // A custom position set via the 2D setter has no z (stored as -1) \u2014
      // pin x/y and let z follow the cluster's centroid
      clusterPositions = vec3(custom.xy, custom.b >= 0.0 ? custom.b : centermass.z);
    }
    vec4 clusterCustomCoeff = texture(clusterForceCoefficient, textureCoords);
    vec3 distVector = clusterPositions - vec3(pointPosition.xy, pointPosition.a);
    float dist = length(distVector);
    if (dist > 0.0) {
      float addV = alpha * dist * clusterCoefficient * clusterCustomCoeff.r;
      // z velocity lives in the blue channel (update-position.frag SPACE_3D contract)
      velocity.rgb += addV * normalize(distVector);
    }
#else
    // positioning points to custom cluster position or either to the center of mass
    vec2 clusterPositions = texture(clusterPositionsTexture, pointClusterIndices.xy / clustersTextureSize).xy;
    if (clusterPositions.x < 0.0 || clusterPositions.y < 0.0) {
      vec4 centermassValues = texture(centermassTexture, pointClusterIndices.xy / clustersTextureSize);
      clusterPositions = centermassValues.xy / centermassValues.b;
    }
    vec4 clusterCustomCoeff = texture(clusterForceCoefficient, textureCoords);
    vec2 distVector = clusterPositions.xy - pointPosition.xy;
    float dist = length(distVector);
    if (dist > 0.0) {
      float addV = alpha * dist * clusterCoefficient * clusterCustomCoeff.r;
      velocity.rg += addV * normalize(distVector);
    }
#endif
  }

  fragColor = velocity;
}`;class hi extends V{constructor(){super(...arguments),this.programsSpaceDimensions=2,this.cachedCentroidPositions=null}create(){var e,t;this.cachedCentroidPositions=null;const{device:i,store:o,data:s}=this,{pointsTextureSize:r}=o;if(s.pointsNumber===void 0||!s.pointClusters&&!s.clusterPositions)return;this.clusterCount=(s.pointClusters??[]).reduce((f,p)=>p===void 0||p<0?f:Math.max(f,p),0)+1,this.clustersTextureSize=Math.ceil(Math.sqrt(this.clusterCount));const n=this.previousPointsTextureSize!==r||this.previousClustersTextureSize!==this.clustersTextureSize||this.previousClusterCount!==this.clusterCount,a=r*r*4,l=this.clustersTextureSize*this.clustersTextureSize*4,u=new Float32Array(a),d=new Float32Array(l).fill(-1),c=new Float32Array(a).fill(1);if(s.clusterPositions){const f=s.clusterPositionsDimensions;for(let p=0;p<this.clusterCount;++p)d[p*4+0]=s.clusterPositions[p*f+0]??-1,d[p*4+1]=s.clusterPositions[p*f+1]??-1,f===3&&(d[p*4+2]=s.clusterPositions[p*f+2]??-1)}for(let f=0;f<s.pointsNumber;++f){const p=(e=s.pointClusters)==null?void 0:e[f];p===void 0?(u[f*4+0]=-1,u[f*4+1]=-1):(u[f*4+0]=p%this.clustersTextureSize,u[f*4+1]=Math.floor(p/this.clustersTextureSize)),s.clusterStrength&&(c[f*4+0]=s.clusterStrength[f]??1)}if(!this.clusterTexture||n?(this.clusterTexture&&!this.clusterTexture.destroyed&&this.clusterTexture.destroy(),this.clusterTexture=i.createTexture({width:r,height:r,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST}),this.clusterTexture.copyImageData({data:u,bytesPerRow:y("rgba32float",r),mipLevel:0,x:0,y:0})):this.clusterTexture.copyImageData({data:u,bytesPerRow:y("rgba32float",r),mipLevel:0,x:0,y:0}),!this.clusterPositionsTexture||n?(this.clusterPositionsTexture&&!this.clusterPositionsTexture.destroyed&&this.clusterPositionsTexture.destroy(),this.clusterPositionsTexture=i.createTexture({width:this.clustersTextureSize,height:this.clustersTextureSize,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST}),this.clusterPositionsTexture.copyImageData({data:d,bytesPerRow:y("rgba32float",this.clustersTextureSize),mipLevel:0,x:0,y:0})):this.clusterPositionsTexture.copyImageData({data:d,bytesPerRow:y("rgba32float",this.clustersTextureSize),mipLevel:0,x:0,y:0}),!this.clusterForceCoefficientTexture||n?(this.clusterForceCoefficientTexture&&!this.clusterForceCoefficientTexture.destroyed&&this.clusterForceCoefficientTexture.destroy(),this.clusterForceCoefficientTexture=i.createTexture({width:r,height:r,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST}),this.clusterForceCoefficientTexture.copyImageData({data:c,bytesPerRow:y("rgba32float",r),mipLevel:0,x:0,y:0})):this.clusterForceCoefficientTexture.copyImageData({data:c,bytesPerRow:y("rgba32float",r),mipLevel:0,x:0,y:0}),!this.centermassTexture||this.previousClustersTextureSize!==this.clustersTextureSize?(this.centermassFbo&&!this.centermassFbo.destroyed&&this.centermassFbo.destroy(),this.centermassTexture&&!this.centermassTexture.destroyed&&this.centermassTexture.destroy(),this.centermassTexture=i.createTexture({width:this.clustersTextureSize,height:this.clustersTextureSize,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST}),this.centermassTexture.copyImageData({data:new Float32Array(l).fill(0),bytesPerRow:y("rgba32float",this.clustersTextureSize),mipLevel:0,x:0,y:0}),this.centermassFbo=i.createFramebuffer({width:this.clustersTextureSize,height:this.clustersTextureSize,colorAttachments:[this.centermassTexture]})):this.centermassTexture.copyImageData({data:new Float32Array(l).fill(0),bytesPerRow:y("rgba32float",this.clustersTextureSize),mipLevel:0,x:0,y:0}),!this.pointIndices||this.previousPointsTextureSize!==r){this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy();const f=K(o.pointsTextureSize);this.pointIndices=i.createBuffer({data:f,usage:x.VERTEX|x.COPY_DST}),(t=this.calculateCentermassCommand)==null||t.setAttributes({pointIndices:this.pointIndices})}this.previousPointsTextureSize=r,this.previousClustersTextureSize=this.clustersTextureSize,this.previousClusterCount=this.clusterCount}initPrograms(){var e,t;const{device:i,store:o,data:s}=this;s.pointsNumber===void 0||!s.pointClusters&&!s.clusterPositions||(this.programsSpaceDimensions!==o.spaceDimensions&&(this.programsSpaceDimensions=o.spaceDimensions,(e=this.calculateCentermassCommand)==null||e.destroy(),this.calculateCentermassCommand=void 0,(t=this.applyForcesCommand)==null||t.destroy(),this.applyForcesCommand=void 0),this.calculateCentermassUniformStore||(this.calculateCentermassUniformStore=new T(i,{calculateCentermassUniforms:{uniformTypes:{pointsTextureSize:"f32",clustersTextureSize:"f32"},defaultUniforms:{pointsTextureSize:o.pointsTextureSize,clustersTextureSize:this.clustersTextureSize??0}}})),this.calculateCentermassCommand||(this.calculateCentermassCommand=new b(i,{fs:ai,vs:li,topology:"point-list",vertexCount:s.pointsNumber??0,attributes:{...this.pointIndices&&{pointIndices:this.pointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...o.is3D?{SPACE_3D:!0}:{}},bindings:{calculateCentermassUniforms:this.calculateCentermassUniformStore.getManagedUniformBuffer("calculateCentermassUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"one",blendColorDstFactor:"one",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one",depthWriteEnabled:!1,depthCompare:"always"}})),this.applyForcesUniformStore||(this.applyForcesUniformStore=new T(i,{applyForcesUniforms:{uniformTypes:{alpha:"f32",clustersTextureSize:"f32",clusterCoefficient:"f32"},defaultUniforms:{alpha:o.alpha,clustersTextureSize:this.clustersTextureSize??0,clusterCoefficient:this.config.simulationCluster}}})),this.applyForcesVertexCoordBuffer||(this.applyForcesVertexCoordBuffer=i.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.applyForcesCommand||(this.applyForcesCommand=new b(i,{fs:di,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.applyForcesVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...o.is3D?{SPACE_3D:!0}:{}},bindings:{applyForcesUniforms:this.applyForcesUniformStore.getManagedUniformBuffer("applyForcesUniforms")}})))}calculateCentermass(){const{device:e,points:t}=this;if(!t||!this.calculateCentermassCommand||!this.calculateCentermassUniformStore||!this.pointIndices||!this.centermassFbo||this.centermassFbo.destroyed||!this.clusterTexture||this.clusterTexture.destroyed||!t.previousPositionTexture||t.previousPositionTexture.destroyed||!t.exitTexture||t.exitTexture.destroyed)return;this.calculateCentermassCommand.setVertexCount(this.data.pointsNumber??0),this.calculateCentermassUniformStore.setUniforms({calculateCentermassUniforms:{pointsTextureSize:this.store.pointsTextureSize,clustersTextureSize:this.clustersTextureSize??0}}),this.calculateCentermassCommand.setBindings({clusterTexture:this.clusterTexture,positionsTexture:t.previousPositionTexture,exitTexture:t.exitTexture});const i=e.beginRenderPass({framebuffer:this.centermassFbo,clearColor:[0,0,0,0]});this.calculateCentermassCommand.draw(i),i.end()}getCentroidPositions(e=2){return this.computeCentroidPositions(e)}run(){var e;if(!this.data.pointClusters&&!this.data.clusterPositions||(this.calculateCentermass(),!this.applyForcesCommand||!this.applyForcesUniformStore)||!this.clusterTexture||this.clusterTexture.destroyed||!this.centermassTexture||this.centermassTexture.destroyed||!this.clusterPositionsTexture||this.clusterPositionsTexture.destroyed||!this.clusterForceCoefficientTexture||this.clusterForceCoefficientTexture.destroyed||!((e=this.points)!=null&&e.previousPositionTexture)||this.points.previousPositionTexture.destroyed||!this.points.velocityFbo||this.points.velocityFbo.destroyed)return;this.applyForcesUniformStore.setUniforms({applyForcesUniforms:{alpha:this.store.alpha,clustersTextureSize:this.clustersTextureSize??0,clusterCoefficient:this.config.simulationCluster}}),this.applyForcesCommand.setBindings({clusterTexture:this.clusterTexture,centermassTexture:this.centermassTexture,clusterPositionsTexture:this.clusterPositionsTexture,clusterForceCoefficient:this.clusterForceCoefficientTexture,positionsTexture:this.points.previousPositionTexture});const t=this.device.beginRenderPass({framebuffer:this.points.velocityFbo,clearColor:[0,0,0,0]});this.applyForcesCommand.draw(t),t.end()}destroy(){var e,t,i,o;this.cachedCentroidPositions=null,(e=this.calculateCentermassCommand)==null||e.destroy(),this.calculateCentermassCommand=void 0,(t=this.applyForcesCommand)==null||t.destroy(),this.applyForcesCommand=void 0,this.centermassFbo&&!this.centermassFbo.destroyed&&this.centermassFbo.destroy(),this.centermassFbo=void 0,this.clusterTexture&&!this.clusterTexture.destroyed&&this.clusterTexture.destroy(),this.clusterTexture=void 0,this.clusterPositionsTexture&&!this.clusterPositionsTexture.destroyed&&this.clusterPositionsTexture.destroy(),this.clusterPositionsTexture=void 0,this.clusterForceCoefficientTexture&&!this.clusterForceCoefficientTexture.destroyed&&this.clusterForceCoefficientTexture.destroy(),this.clusterForceCoefficientTexture=void 0,this.centermassTexture&&!this.centermassTexture.destroyed&&this.centermassTexture.destroy(),this.centermassTexture=void 0,(i=this.calculateCentermassUniformStore)==null||i.destroy(),this.calculateCentermassUniformStore=void 0,(o=this.applyForcesUniformStore)==null||o.destroy(),this.applyForcesUniformStore=void 0,this.pointIndices&&!this.pointIndices.destroyed&&this.pointIndices.destroy(),this.pointIndices=void 0,this.applyForcesVertexCoordBuffer&&!this.applyForcesVertexCoordBuffer.destroyed&&this.applyForcesVertexCoordBuffer.destroy(),this.applyForcesVertexCoordBuffer=void 0}computeCentroidPositions(e){var t,i;const{config:{enableSimulation:o},store:{isSimulationRunning:s}}=this,r=!o||!s;if(r&&(t=this.points)!=null&&t.areClusterCentroidsUpToDate&&((i=this.cachedCentroidPositions)==null?void 0:i.dimensions)===e)return this.cachedCentroidPositions.positions;if(this.calculateCentermass(),!this.centermassFbo||this.centermassFbo.destroyed||this.clusterCount===void 0)return[];const n=B(this.device,this.centermassFbo),a=[];a.length=this.clusterCount*e;for(let l=0;l<this.clusterCount;l+=1){const u=n[l*4+0],d=n[l*4+1],c=n[l*4+2],f=n[l*4+3];u!==void 0&&d!==void 0&&c!==void 0&&(a[l*e]=u/c,a[l*e+1]=d/c,e===3&&(a[l*e+2]=(f??0)/c))}return r&&this.points&&(this.cachedCentroidPositions={dimensions:e,positions:a},this.points.areClusterCentroidsUpToDate=!0),a}}const ui=`
  #gl-bench {
    position:absolute;
    right:0;
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
    background: #5f69de;
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
    fill: #8288e4;
  }
  #gl-bench .opacity {
    stroke: #8288e4;
  }
`;class qe{constructor(e){this.destroy();const t=e.getContext("webgl")||e.getContext("experimental-webgl");this.bench=new It(t,{css:ui})}begin(){var e;(e=this.bench)==null||e.begin("frame")}end(e){var t,i;(t=this.bench)==null||t.end("frame"),(i=this.bench)==null||i.nextFrame(e)}destroy(){this.bench=void 0,N("#gl-bench").remove()}}const ci=`
vec2 conicParametricCurve(vec2 A, vec2 B, vec2 ControlPoint, float t, float w) {
  vec2 divident = (1.0 - t) * (1.0 - t) * A + 2.0 * (1.0 - t) * t * w * ControlPoint + t * t * B;
  float divisor = (1.0 - t) * (1.0 - t) + 2.0 * (1.0 - t) * t * w + t * t;
  return divident / divisor;
}

// 3D overload: the same rational quadratic Bezier evaluated component-wise for
// world-space curves (3D links bend within the plane facing the camera).
vec3 conicParametricCurve(vec3 A, vec3 B, vec3 ControlPoint, float t, float w) {
  vec3 divident = (1.0 - t) * (1.0 - t) * A + 2.0 * (1.0 - t) * t * w * ControlPoint + t * t * B;
  float divisor = (1.0 - t) * (1.0 - t) + 2.0 * (1.0 - t) * t * w + t * t;
  return divident / divisor;
}
`,Ze={name:"conicParametricCurve",vs:ci},fi=`
float focalNdc(mat4 m) {
  return length(vec3(m[0][1], m[1][1], m[2][1]));
}

float pxPerSpaceUnit(mat4 viewProjection, vec2 screen, float w) {
  return 0.5 * screen.y * focalNdc(viewProjection) / w;
}

vec3 cameraForward(mat4 viewProjection) {
  return vec3(viewProjection[0][3], viewProjection[1][3], viewProjection[2][3]);
}
`,Q={name:"space3d",vs:fi},pi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec4 rgbaColor;
in vec2 pos;
in float arrowLength;
in float useArrow;
in float smoothing;
in float arrowWidthFactor;
in float linkIndex;
flat in float vLinkStyle;
flat in float vLinkDashSpan;
flat in float vLinkDashWidth;
flat in vec4 vEndpointColorA;
flat in vec4 vEndpointColorB;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform drawLineFragmentUniforms {
  float renderMode;
  float linkDashLength;
  float linkDashGap;
  float linkColorInterpolateFromEndpoints;
  float hoveredLinkIndex;
  vec4 hoveredLinkColor;
} drawLineFrag;

#define renderMode drawLineFrag.renderMode
#define linkDashLength drawLineFrag.linkDashLength
#define linkDashGap drawLineFrag.linkDashGap
#define linkColorInterpolateFromEndpoints drawLineFrag.linkColorInterpolateFromEndpoints
#define hoveredLinkIndex drawLineFrag.hoveredLinkIndex
#define hoveredLinkColor drawLineFrag.hoveredLinkColor
#else
// renderMode: 0.0 = normal rendering, 1.0 = index buffer rendering for picking
uniform float renderMode;
uniform float linkDashLength;
uniform float linkDashGap;
uniform float linkColorInterpolateFromEndpoints;
uniform float hoveredLinkIndex;
uniform vec4 hoveredLinkColor;
#endif

out vec4 fragColor;

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

// LinkStyle enum values (must match \`LinkStyle\` in modules/GraphData). Compared with
// exact equality, like the point shapes: the CPU sanitizer guarantees exact integers
// and vLinkStyle is flat, so an unknown future style matches nothing and renders solid.
const float LINK_STYLE_DASHED = 1.0;
const float LINK_STYLE_DOTTED = 2.0;

// Anti-aliased on/off mask for one dash period. \`phase\` is distance-along-line in px,
// \`on\` is the lit dash length, \`period\` is on + gap, \`aa\` is the smoothing half-width in px.
float strokeMask(float phase, float on, float period, float aa) {
  float m = mod(phase, period);
  return smoothstep(-aa, aa, m) * (1.0 - smoothstep(on - aa, on + aa, m));
}

void main() {
  float opacity = 1.0;
  vec3 color = rgbaColor.rgb;

  // Arrowhead extent along the link (pos.x space) \u2014 used by the arrow rendering
  // and by the dash mask, which leaves the arrowhead solid.
  float end_arrow = 0.5 + arrowLength / 2.0;
  float start_arrow = end_arrow - arrowLength;

  // Gradient links: interpolate RGB from the source point color to the target point color
  // along the link. Opacity (visibility / greyout) still comes from rgbaColor.a.
  if (linkColorInterpolateFromEndpoints > 0.5) {
    color = mix(vEndpointColorA.rgb, vEndpointColorB.rgb, clamp(pos.x, 0.0, 1.0));
  }

  if (useArrow > 0.5) {
    float arrowWidthDelta = arrowWidthFactor / 2.0;
    float linkOpacity = rgbaColor.a * smoothstep(0.5 - arrowWidthDelta, 0.5 - arrowWidthDelta - smoothing / 2.0, abs(pos.y));
    float arrowOpacity = 1.0;
    if (pos.x > start_arrow && pos.x < start_arrow + arrowLength) {
      float xmapped = map(pos.x, start_arrow, end_arrow, 0.0, 1.0);
      arrowOpacity = rgbaColor.a * smoothstep(xmapped - smoothing, xmapped, map(abs(pos.y), 0.5, 0.0, 0.0, 1.0));
      if (linkOpacity != arrowOpacity) {
        linkOpacity = max(linkOpacity, arrowOpacity);
      }
    }
    opacity = linkOpacity;
  } else opacity = rgbaColor.a * smoothstep(0.5, 0.5 - smoothing, abs(pos.y));

  // Dashed / dotted stroke patterns. Applied to the visible pass only (renderMode == 0.0)
  // so that gaps stay fully pickable in the index pass. The arrowhead region is left solid.
  if (renderMode < 0.5 && (vLinkStyle == LINK_STYLE_DASHED || vLinkStyle == LINK_STYLE_DOTTED)) {
    bool inArrowHead = (useArrow > 0.5) && (pos.x > start_arrow) && (pos.x < end_arrow);
    if (!inArrowHead) {
      // Distance along the link in the dash pattern's space (screen px or world units; see the vertex shader).
      // fwidth() gives the screen-space rate of change, so anti-aliasing stays ~1px wide in either space.
      float phase = clamp(pos.x, 0.0, 1.0) * vLinkDashSpan;
      if (vLinkStyle == LINK_STYLE_DASHED) {
        float period = max(linkDashLength + linkDashGap, 0.001);
        float aa = max(fwidth(phase), 1e-4);
        opacity *= strokeMask(phase, linkDashLength, period, aa);
      } else {
        // Dotted: round dots sized to the stroke width, spaced by diameter + gap.
        // On arrowed links the quad is widened to fit the arrowhead and the stroke
        // occupies only (1 - arrowWidthFactor) of it \u2014 size dots to the stroke,
        // not the widened quad.
        float diameter = useArrow > 0.5 ? vLinkDashWidth * (1.0 - arrowWidthFactor) : vLinkDashWidth;
        float period = max(diameter + linkDashGap, 0.001);
        float localX = mod(phase, period) - period * 0.5;
        float localY = pos.y * vLinkDashWidth;
        float r = length(vec2(localX, localY));
        float aa = max(fwidth(r), 1e-4);
        opacity *= 1.0 - smoothstep(diameter * 0.5 - aa, diameter * 0.5 + aa, r);
      }
    }
  }

  // Apply hover color if this is the hovered link and hover color is defined.
  // Done last \u2014 after the gradient and the dash mask \u2014 so hover wins over every
  // color source (per-link color from the vertex stage and the endpoint gradient
  // alike), while the dash pattern and AA stay intact in the hover color.
  if (hoveredLinkIndex == linkIndex && hoveredLinkColor.a > -0.5) {
    color = hoveredLinkColor.rgb;
    opacity *= hoveredLinkColor.a;
  }

  if (renderMode > 0.0) {
    if (opacity <= 0.0) discard;
    fragColor = vec4(linkIndex, 0.0, 0.0, 1.0);
  } else fragColor = vec4(color, opacity);

}
`,mi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec2 position, pointA, pointB;
in vec4 sourceColor;
in vec4 targetColor;
in float sourceWidth;
in float targetWidth;
in float arrow;
in float linkIndices;
in float linkStyle;

uniform sampler2D positionsTexture;
uniform sampler2D linkStatus;
uniform sampler2D exitTexture;
uniform sampler2D pointColorsTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform drawLineUniforms {
  mat4 transformationMatrix;
  float pointsTextureSize;
  float widthScale;
  float linkArrowsSizeScale;
  float spaceSize;
  vec2 screenSize;
  vec2 linkVisibilityDistanceRange;
  float linkVisibilityMinTransparency;
  float linkOpacity;
  float greyoutOpacity;
  float curvedWeight;
  float curvedLinkControlPointDistance;
  float curvedLinkSegments;
  float scaleLinksOnZoom;
  float maxPointSize;
  float renderMode;
  float hoveredLinkIndex;
  float hoveredLinkWidthIncrease;
  float isLinkHighlightingActive;
  float linkStatusTextureSize;
  float focusedLinkIndex;
  float focusedLinkWidthIncrease;
  float transitionProgress;
  float animateColors;
  float animateWidths;
  float animatePositions;
  vec4 pointDefaultColor;
  float linkColorInterpolateFromEndpoints;
} drawLine;

#define transformationMatrix drawLine.transformationMatrix
#define pointsTextureSize drawLine.pointsTextureSize
#define widthScale drawLine.widthScale
#define linkArrowsSizeScale drawLine.linkArrowsSizeScale
#define spaceSize drawLine.spaceSize
#define screenSize drawLine.screenSize
#define linkVisibilityDistanceRange drawLine.linkVisibilityDistanceRange
#define linkVisibilityMinTransparency drawLine.linkVisibilityMinTransparency
#define linkOpacity drawLine.linkOpacity
#define greyoutOpacity drawLine.greyoutOpacity
#define curvedWeight drawLine.curvedWeight
#define curvedLinkControlPointDistance drawLine.curvedLinkControlPointDistance
#define curvedLinkSegments drawLine.curvedLinkSegments
#define scaleLinksOnZoom drawLine.scaleLinksOnZoom
#define maxPointSize drawLine.maxPointSize
#define renderMode drawLine.renderMode
#define hoveredLinkIndex drawLine.hoveredLinkIndex
#define hoveredLinkWidthIncrease drawLine.hoveredLinkWidthIncrease
#define isLinkHighlightingActive drawLine.isLinkHighlightingActive
#define linkStatusTextureSize drawLine.linkStatusTextureSize
#define focusedLinkIndex drawLine.focusedLinkIndex
#define focusedLinkWidthIncrease drawLine.focusedLinkWidthIncrease
#define transitionProgress drawLine.transitionProgress
#define animateColors drawLine.animateColors
#define animateWidths drawLine.animateWidths
#define animatePositions drawLine.animatePositions
#define pointDefaultColor drawLine.pointDefaultColor
#define linkColorInterpolateFromEndpoints drawLine.linkColorInterpolateFromEndpoints
#else
uniform mat3 transformationMatrix;
uniform float pointsTextureSize;
uniform float widthScale;
uniform float linkArrowsSizeScale;
uniform float spaceSize;
uniform vec2 screenSize;
uniform vec2 linkVisibilityDistanceRange;
uniform float linkVisibilityMinTransparency;
uniform float linkOpacity;
uniform float greyoutOpacity;
uniform float curvedWeight;
uniform float curvedLinkControlPointDistance;
uniform float curvedLinkSegments;
uniform bool scaleLinksOnZoom;
uniform float maxPointSize;
// renderMode: 0.0 = normal rendering, 1.0 = index buffer rendering for picking
uniform float renderMode;
uniform float hoveredLinkIndex;
uniform float hoveredLinkWidthIncrease;
uniform float isLinkHighlightingActive;
uniform float linkStatusTextureSize;
uniform float focusedLinkIndex;
uniform float focusedLinkWidthIncrease;
uniform float transitionProgress;
uniform float animateColors;
uniform float animateWidths;
uniform float animatePositions;
uniform vec4 pointDefaultColor;
uniform float linkColorInterpolateFromEndpoints;
#endif

out vec4 rgbaColor;
out vec2 pos;
out float arrowLength;
out float useArrow;
out float smoothing;
out float arrowWidthFactor;
out float linkIndex;
// Per-instance constants (no per-vertex variation), so \`flat\` skips interpolation.
flat out float vLinkStyle;
flat out float vLinkDashSpan;
flat out float vLinkDashWidth;
flat out vec4 vEndpointColorA;
flat out vec4 vEndpointColorB;

float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

// Resolves NaN color channels the way the point draw shader does: NaN means "use the
// default" \u2014 the config default, blended toward the exit default as the endpoint fades
// out. Mirrors resolveColor in draw-points.vert.
vec4 resolveColor(vec4 color, float exitRamp) {
  vec4 defaultColor = mix(pointDefaultColor, vec4(EXIT_DEFAULT_COLOR_CHANNEL), exitRamp);
  return mix(color, defaultColor, isnan(color));
}

float calculateLinkWidth(float width) {
  float linkWidth;
  if (scaleLinksOnZoom > 0.0) {
    // Use original width if links should scale with zoom
    linkWidth = width;
  } else {
    // Adjust width based on zoom level to maintain visual size
    linkWidth = width / transformationMatrix[0][0];
    // Apply a non-linear scaling to avoid extreme widths
    linkWidth *= min(5.0, max(1.0, transformationMatrix[0][0] * 0.01));
  }
  // Limit link width based on whether it has an arrow
  if (useArrow > 0.5) {
    return min(linkWidth, (maxPointSize * 2.0) / transformationMatrix[0][0]);
  } else {
    return min(linkWidth, maxPointSize / transformationMatrix[0][0]);
  }
}

float calculateArrowWidth(float arrowWidth) {
  if (scaleLinksOnZoom > 0.0) {
    return arrowWidth;
  } else {
    // Apply the same scaling logic as calculateLinkWidth to maintain proportionality
    arrowWidth = arrowWidth / transformationMatrix[0][0];
    // Apply the same non-linear scaling to avoid extreme widths
    arrowWidth *= min(5.0, max(1.0, transformationMatrix[0][0] * 0.01));
    return arrowWidth;
  }
}

#ifdef SPACE_3D
// 3D variants work in pixels throughout (the quad is extruded in screen space after
// projection), unlike the 2D functions above which return space units. \`pxPerUnit\`
// is the perspective-attenuated zoom factor at the vertex's depth.
float calculateLinkWidth3D(float width, float pxPerUnit) {
  float linkWidth;
  if (scaleLinksOnZoom > 0.0) {
    linkWidth = width * pxPerUnit;
  } else {
    linkWidth = width * min(5.0, max(1.0, pxPerUnit * 0.01));
  }
  // Limit link width based on whether it has an arrow
  if (useArrow > 0.5) {
    return min(linkWidth, maxPointSize * 2.0);
  } else {
    return min(linkWidth, maxPointSize);
  }
}

float calculateArrowWidth3D(float arrowWidth, float pxPerUnit) {
  if (scaleLinksOnZoom > 0.0) {
    return arrowWidth * pxPerUnit;
  } else {
    return arrowWidth * min(5.0, max(1.0, pxPerUnit * 0.01));
  }
}
#endif

void main() {
  pos = position;
  linkIndex = linkIndices;
  vLinkStyle = linkStyle;

  vec2 pointTexturePosA = (pointA + 0.5) / pointsTextureSize;
  vec2 pointTexturePosB = (pointB + 0.5) / pointsTextureSize;

  vec4 pointPositionA = texture(positionsTexture, pointTexturePosA);
  vec4 pointPositionB = texture(positionsTexture, pointTexturePosB);

  // Skip links touching an absent (NaN position) point \u2014 interpolating from a NaN
  // endpoint would produce garbage geometry. Collapse the link off-screen. This only
  // catches snap removals: an animated removal freezes the endpoint at its last real
  // position, so absence must be read from the exit texture below. Checked before the
  // 2D/3D split (alpha carries z in 3D) so both projections are guarded.
  if (isnan(pointPositionA.x) || isnan(pointPositionA.y) || isnan(pointPositionA.a) ||
      isnan(pointPositionB.x) || isnan(pointPositionB.y) || isnan(pointPositionB.a)) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    return;
  }

  // Exit status of both endpoints (R = previous absence, G = current absence). A link
  // is only as present as its endpoints.
  vec4 exitStatusA = texture(exitTexture, pointTexturePosA);
  vec4 exitStatusB = texture(exitTexture, pointTexturePosB);

  // Picking must not report a link to a removed point even mid-fade \u2014 same rule as
  // point picking, which excludes on current absence.
  if (renderMode > 0.0 && (exitStatusA.g > 0.5 || exitStatusB.g > 0.5)) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    return;
  }

  // Visible pass: fade the link with the same animated exit ramp the point fade uses
  // (blend R\u2192G during a position transition, settled G otherwise), so a removed
  // point's links fade out in sync with it instead of dangling at full opacity.
  float exitA = animatePositions > 0.0 ? mix(exitStatusA.r, exitStatusA.g, transitionProgress) : exitStatusA.g;
  float exitB = animatePositions > 0.0 ? mix(exitStatusB.r, exitStatusB.g, transitionProgress) : exitStatusB.g;
  float exitPresence = (1.0 - exitA) * (1.0 - exitB);
  if (exitPresence <= 0.0) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    return;
  }

  // Sample the source/target point colors so the fragment shader can build a gradient
  // along the link. Skipped entirely when the gradient is off \u2014 the fragment shader
  // only reads these varyings inside its own gradient branch, keyed on the same flag.
  // The texture mirrors GraphData.pointColors, so channels may be NaN ("use the
  // default") \u2014 resolve them with the endpoint's exit ramp, like the point draw.
  // Assigned before the 2D/3D split so both paths write the varyings.
  if (linkColorInterpolateFromEndpoints > 0.5) {
    vEndpointColorA = resolveColor(texture(pointColorsTexture, pointTexturePosA), exitA);
    vEndpointColorB = resolveColor(texture(pointColorsTexture, pointTexturePosB), exitB);
  }

  // Dash/dot pattern geometry, filled per-branch below. \`dashSpan\` is the link length in
  // the pattern's space (screen px when scaleLinksOnZoom is off, else world units);
  // \`dashWidthScale\` converts that branch's native linkWidthPx into the same space.
  float dashSpan = 0.0;
  float dashWidthScale = 1.0;

  #ifdef SPACE_3D
  // 3D mode: project both endpoints (z lives in the position texture's alpha channel)
  // and extrude the quad in screen space after projection. Curved links are rational
  // Bezier curves evaluated in world space, bent within the plane facing the camera so
  // they read as curved from any orbit angle; with curvature off (a single segment) or
  // a zero control-point distance the link stays a straight clip-space segment.
  vec3 a3 = vec3(pointPositionA.rg, pointPositionA.a);
  vec3 b3 = vec3(pointPositionB.rg, pointPositionB.a);
  vec4 clipA = transformationMatrix * vec4(a3, 1.0);
  vec4 clipB = transformationMatrix * vec4(b3, 1.0);
  bool isCurved = curvedLinkSegments > 1.0 && curvedLinkControlPointDistance != 0.0;

  vec3 controlPoint3 = (a3 + b3) * 0.5;
  // Clip w is affine in world position and the curve stays inside the convex hull of
  // {a, b, control point} (given a non-negative curve weight), so the minimum over
  // those three bounds w along the whole curve. Straight links only need the endpoints.
  float minW = min(clipA.w, clipB.w);
  if (isCurved) {
    vec3 dirLink = b3 - a3;
    // Bend within the camera-facing plane; fall back to world-up (then world-x) when
    // the link is (nearly) parallel to the view direction.
    vec3 bend = cross(cameraForward(transformationMatrix), dirLink);
    if (dot(bend, bend) < 1e-6) bend = cross(dirLink, vec3(0.0, 1.0, 0.0));
    if (dot(bend, bend) < 1e-6) bend = vec3(1.0, 0.0, 0.0);
    controlPoint3 += normalize(bend) * length(dirLink) * curvedLinkControlPointDistance;
    minW = min(minW, (transformationMatrix * vec4(controlPoint3, 1.0)).w);
  }
  if (minW <= 0.0) {
    // Some part of the link can reach behind the camera \u2014 cull the whole link.
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    rgbaColor = vec4(0.0);
    arrowLength = 0.0;
    useArrow = 0.0;
    smoothing = 0.0;
    arrowWidthFactor = 0.0;
    return;
  }
  vec2 screenA = (clipA.xy / clipA.w) * 0.5 * screenSize;
  vec2 screenB = (clipB.xy / clipB.w) * 0.5 * screenSize;
  vec2 segPx = screenB - screenA;
  // Projected chord length in pixels \u2014 drives the visibility fade and the arrow
  // proportions for curved links too, matching 2D (which also uses the chord).
  float linkDistPx = length(segPx);

  // Centerline point for this vertex and the screen-space tangent to extrude along.
  vec4 clipCurr;
  vec2 tangentPx;
  if (isCurved) {
    float tCurr = position.x;
    float tPrev = max(0.0, tCurr - 1.0 / curvedLinkSegments);
    float tNext = min(1.0, tCurr + 1.0 / curvedLinkSegments);
    clipCurr = transformationMatrix * vec4(conicParametricCurve(a3, b3, controlPoint3, tCurr, curvedWeight), 1.0);
    vec4 clipPrev = transformationMatrix * vec4(conicParametricCurve(a3, b3, controlPoint3, tPrev, curvedWeight), 1.0);
    vec4 clipNext = transformationMatrix * vec4(conicParametricCurve(a3, b3, controlPoint3, tNext, curvedWeight), 1.0);
    // Every curve sample has w > 0 (guarded above), so the divides are safe.
    tangentPx = (clipNext.xy / clipNext.w - clipPrev.xy / clipPrev.w) * 0.5 * screenSize;
  } else {
    // Straight segment: interpolate in clip space (projectively correct for straight lines).
    clipCurr = mix(clipA, clipB, position.x);
    tangentPx = segPx;
  }
  // Pixels per space unit at this vertex's depth \u2014 gives a natural perspective
  // taper along the link when widths scale with zoom.
  float pxPerUnit = pxPerSpaceUnit(transformationMatrix, screenSize, clipCurr.w);

  // Dash pattern space in 3D. Screen mode uses the projected chord length in px;
  // world mode uses the straight-line world length. linkWidthPx (below) is in px,
  // so world mode divides it back into world units to match dashSpan.
  float worldLen3D = length(b3 - a3);
  dashSpan = scaleLinksOnZoom > 0.0 ? worldLen3D : linkDistPx;
  dashWidthScale = scaleLinksOnZoom > 0.0 ? (pxPerUnit > 0.0 ? 1.0 / pxPerUnit : 0.0) : 1.0;
  #else
  vec2 a = pointPositionA.xy;
  vec2 b = pointPositionB.xy;

  // Calculate direction vector and its perpendicular
  vec2 xBasis = b - a;
  vec2 yBasis = normalize(vec2(-xBasis.y, xBasis.x));

  // Calculate link distance and control point for curved link
  float linkDist = length(xBasis);
  float h = curvedLinkControlPointDistance;
  vec2 controlPoint = (a + b) / 2.0 + yBasis * linkDist * h;

  // Convert link distance to screen pixels
  float linkDistPx = linkDist * transformationMatrix[0][0];

  // Dash pattern space in 2D. Screen mode measures in screen px (linkDist * zoom == linkDistPx);
  // world mode measures in world units. linkWidthPx (below) is in world units here, so the same
  // scale converts it into the pattern's space.
  dashWidthScale = scaleLinksOnZoom > 0.0 ? 1.0 : transformationMatrix[0][0];
  dashSpan = linkDist * dashWidthScale;
  #endif

  float lineWidthBase = animateWidths > 0.0
    ? mix(sourceWidth, targetWidth, transitionProgress)
    : targetWidth;
  vec4 lineColor = animateColors > 0.0
    ? mix(sourceColor, targetColor, transitionProgress)
    : targetColor;
  
  // Calculate line width using the width scale
  float linkWidth = lineWidthBase * widthScale;
  float k = 2.0;
  // Arrow width is proportionally larger than the line width
  float arrowWidth = linkWidth * k;
  arrowWidth *= linkArrowsSizeScale;

  // Ensure arrow width difference is non-negative to prevent unwanted changes to link width
  float arrowWidthDifference = max(0.0, arrowWidth - linkWidth);

  // Calculate arrow width in pixels
  // Calculate arrow length proportional to its width
  // 0.866 is approximately sqrt(3)/2 - related to equilateral triangle geometry
  // Cap the length to avoid overly long arrows on short links
  #ifdef SPACE_3D
  float arrowWidthPx = calculateArrowWidth3D(arrowWidth, pxPerUnit);
  arrowLength = min(0.3, (0.866 * arrowWidthPx * 2.0) / max(linkDistPx, 1e-6));
  #else
  float arrowWidthPx = calculateArrowWidth(arrowWidth);
  arrowLength = min(0.3, (0.866 * arrowWidthPx * 2.0) / linkDist);
  #endif

  useArrow = arrow;
  if (useArrow > 0.5) {
    linkWidth += arrowWidthDifference;
  }

  arrowWidthFactor = arrowWidthDifference / linkWidth;

  // Calculate final link width with smoothing.
  // In 3D everything below is in pixels; in 2D it is in space units (px / zoom factor).
  #ifdef SPACE_3D
  float linkWidthPx = calculateLinkWidth3D(linkWidth, pxPerUnit);

  if (renderMode > 0.0) {
    // Add 5 pixels padding for better hover detection
    linkWidthPx += 5.0;
  }
  // Match the visible-pass width increases so the pickable area covers the full rendered link
  if (hoveredLinkIndex == linkIndex) {
    linkWidthPx += hoveredLinkWidthIncrease;
  }
  if (focusedLinkIndex == linkIndex) {
    linkWidthPx += focusedLinkWidthIncrease;
  }
  float smoothingPx = 0.5;
  smoothing = smoothingPx / linkWidthPx;
  linkWidthPx += smoothingPx;
  #else
  float linkWidthPx = calculateLinkWidth(linkWidth);

  if (renderMode > 0.0) {
    // Add 5 pixels padding for better hover detection
    linkWidthPx += 5.0 / transformationMatrix[0][0];
    // Match the visible-pass width increases so the pickable area covers the full rendered link
    if (hoveredLinkIndex == linkIndex) {
      linkWidthPx += hoveredLinkWidthIncrease / transformationMatrix[0][0];
    }
    if (focusedLinkIndex == linkIndex) {
      linkWidthPx += focusedLinkWidthIncrease / transformationMatrix[0][0];
    }
  } else {
    // Add pixel increase if this is the hovered link
    if (hoveredLinkIndex == linkIndex) {
      linkWidthPx += hoveredLinkWidthIncrease / transformationMatrix[0][0];
    }
    // Add pixel increase if this is the focused link
    if (focusedLinkIndex == linkIndex) {
      linkWidthPx += focusedLinkWidthIncrease / transformationMatrix[0][0];
    }
  }
  float smoothingPx = 0.5 / transformationMatrix[0][0];
  smoothing = smoothingPx / linkWidthPx;
  linkWidthPx += smoothingPx;
  #endif

  // Publish the dash pattern span and the link thickness in the pattern's space so the
  // fragment shader can draw dashes/dots (dotted dots are sized to the stroke width).
  // Both are in the same units (screen px or world), keeping dots round in either mode.
  vLinkDashSpan = dashSpan;
  vLinkDashWidth = linkWidthPx * dashWidthScale;

  // Calculate final color with opacity based on link distance
  vec3 rgbColor = lineColor.rgb;
  // Fade long links toward the minimum transparency, saturating at 1 so links
  // shorter than the range minimum never exceed the configured opacity. A
  // degenerate (or inverted) range acts as a hard threshold instead of
  // dividing by zero in map().
  float visibilityFade = linkVisibilityDistanceRange.g > linkVisibilityDistanceRange.r
    ? map(linkDistPx, linkVisibilityDistanceRange.g, linkVisibilityDistanceRange.r, 0.0, 1.0)
    : (linkDistPx <= linkVisibilityDistanceRange.g ? 1.0 : 0.0);
  float opacity = lineColor.a * linkOpacity * clamp(visibilityFade, linkVisibilityMinTransparency, 1.0);
  // Fade with the exit ramp of the endpoints (1 = both fully present).
  opacity *= exitPresence;

  // Apply greyed-out opacity from link status texture
  if (isLinkHighlightingActive > 0.0 && linkStatusTextureSize > 0.0) {
    float texX = mod(linkIndices, linkStatusTextureSize);
    float texY = floor(linkIndices / linkStatusTextureSize);
    vec2 linkStatusCoord = (vec2(texX, texY) + 0.5) / linkStatusTextureSize;
    vec4 linkStatusValue = texture(linkStatus, linkStatusCoord);
    if (linkStatusValue.r > 0.0) {
      opacity *= greyoutOpacity;
    }
  }

  // Pass final color to fragment shader. Hover color is applied in the fragment
  // shader, after the endpoint gradient, so it wins for gradient links too.
  rgbaColor = vec4(rgbColor, opacity);

  #ifdef SPACE_3D
  // Offset the centerline point along the screen-space perpendicular of its tangent.
  // The offset is pre-multiplied by w so it survives the perspective divide.
  vec2 normalPx = dot(tangentPx, tangentPx) > 0.0 ? normalize(vec2(-tangentPx.y, tangentPx.x)) : vec2(0.0, 1.0);
  clipCurr.xy += normalPx * (linkWidthPx * position.y) * (2.0 / screenSize) * clipCurr.w;
  gl_Position = clipCurr;
  #else
  // Calculate position on the curved path
  float t = position.x;
  float w = curvedWeight;

  float tPrev = t - 1.0 / curvedLinkSegments;
  float tNext = t + 1.0 / curvedLinkSegments;

  vec2 pointCurr = conicParametricCurve(a, b, controlPoint, t, w);

  vec2 pointPrev = conicParametricCurve(a, b, controlPoint, max(0.0, tPrev), w);
  vec2 pointNext = conicParametricCurve(a, b, controlPoint, min(tNext, 1.0), w);

  vec2 xBasisCurved = pointNext - pointPrev;
  vec2 yBasisCurved = normalize(vec2(-xBasisCurved.y, xBasisCurved.x));

  pointCurr += yBasisCurved * linkWidthPx * position.y;

  // Transform to clip space coordinates
  vec2 p = 2.0 * pointCurr / spaceSize - 1.0;
  p *= spaceSize / screenSize;

  #ifdef USE_UNIFORM_BUFFERS
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 final = transformMat3 * vec3(p, 1);
  #else
  vec3 final = transformationMatrix * vec3(p, 1);
  #endif

  gl_Position = vec4(final.rg, 0, 1);
  #endif
}`,gi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec4 rgba;

out vec4 fragColor;

void main() {
  fragColor = rgba;
}
`,vi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec2 pointA;
in vec2 pointB;
in float linkIndices;

uniform sampler2D positionsTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform fillSampledLinksUniforms {
  float pointsTextureSize;
  mat4 transformationMatrix;
  float spaceSize;
  vec2 screenSize;
  float curvedWeight;
  float curvedLinkControlPointDistance;
  float curvedLinkSegments;
} fillSampledLinks;

#define pointsTextureSize fillSampledLinks.pointsTextureSize
#define transformationMatrix fillSampledLinks.transformationMatrix
#define spaceSize fillSampledLinks.spaceSize
#define screenSize fillSampledLinks.screenSize
#define curvedWeight fillSampledLinks.curvedWeight
#define curvedLinkControlPointDistance fillSampledLinks.curvedLinkControlPointDistance
#define curvedLinkSegments fillSampledLinks.curvedLinkSegments
#else
uniform float pointsTextureSize;
uniform float spaceSize;
uniform vec2 screenSize;
uniform float curvedWeight;
uniform float curvedLinkControlPointDistance;
uniform float curvedLinkSegments;
uniform mat3 transformationMatrix;
#endif

out vec4 rgba;

void main() {
  // Skip a link touching an absent (faded-out) point. exit.G = current absence.
  if (texture(exitTexture, (pointA + 0.5) / pointsTextureSize).g > 0.5 ||
      texture(exitTexture, (pointB + 0.5) / pointsTextureSize).g > 0.5) {
    rgba = vec4(0.0);
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 posA = texture(positionsTexture, (pointA + 0.5) / pointsTextureSize);
  vec4 posB = texture(positionsTexture, (pointB + 0.5) / pointsTextureSize);

  #ifdef SPACE_3D
  // 3D mode: project both endpoints (z in the texture's alpha channel), compute the
  // label angle from the projected screen tangent, and place the sample at the
  // projected chord midpoint (even when links render curved \u2014 the curve's midpoint
  // tangent is chord-parallel anyway). Midpoint z is recovered on the CPU.
  vec4 clipA = transformationMatrix * vec4(posA.rg, posA.a, 1.0);
  vec4 clipB = transformationMatrix * vec4(posB.rg, posB.a, 1.0);
  vec3 mid3 = (vec3(posA.rg, posA.a) + vec3(posB.rg, posB.a)) * 0.5;
  vec4 clipMid = transformationMatrix * vec4(mid3, 1.0);
  if (clipA.w <= 0.0 || clipB.w <= 0.0 || clipMid.w <= 0.0) {
    // Either endpoint behind the camera \u2014 keep the vertex off the sampling grid.
    rgba = vec4(-1.0);
    gl_Position = vec4(2.0, 2.0, 0.0, 1.0);
    gl_PointSize = 1.0;
    return;
  }
  vec2 screenA = (clipA.xy / clipA.w + 1.0) * screenSize / 2.0;
  vec2 screenB = (clipB.xy / clipB.w + 1.0) * screenSize / 2.0;
  vec2 tangent = screenB - screenA;
  float angle = -atan(tangent.y, tangent.x);
  vec2 mid = mid3.xy;
  vec2 pointScreenPosition = (clipMid.xy / clipMid.w + 1.0) * screenSize / 2.0;
  #else
  vec2 a = posA.rg;
  vec2 b = posB.rg;

  vec2 tangent = b - a;
  float angle = -atan(tangent.y, tangent.x);

  vec2 mid;
  if (curvedLinkSegments <= 1.0) {
    mid = (a + b) * 0.5;
  } else if (curvedLinkControlPointDistance != 0.0 && curvedWeight != 0.0) {
    vec2 xBasis = b - a;
    vec2 yBasis = normalize(vec2(-xBasis.y, xBasis.x));
    float linkDist = length(xBasis);
    float h = curvedLinkControlPointDistance;
    vec2 controlPoint = (a + b) / 2.0 + yBasis * linkDist * h;
    mid = conicParametricCurve(a, b, controlPoint, 0.5, curvedWeight);
  } else {
    mid = (a + b) * 0.5;
  }

  vec2 p = 2.0 * mid / spaceSize - 1.0;
  p *= spaceSize / screenSize;
  #ifdef USE_UNIFORM_BUFFERS
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 final = transformMat3 * vec3(p, 1);
  #else
  vec3 final = transformationMatrix * vec3(p, 1);
  #endif

  vec2 pointScreenPosition = (final.xy + 1.0) * screenSize / 2.0;
  #endif

  rgba = vec4(linkIndices, mid.x, mid.y, angle);
  float i = (pointScreenPosition.x + 0.5) / screenSize.x;
  float j = (pointScreenPosition.y + 0.5) / screenSize.y;
  gl_Position = vec4(2.0 * vec2(i, j) - 1.0, 0.0, 1.0);

  gl_PointSize = 1.0;
}
`;function Xe(h){const e=h[0];return h[3]>0&&e>=0?e:void 0}class Ye{constructor(e,t){this.buffer=null,this.sync=null,this.isInFlight=!1,this.gl=e,this.data=new Float32Array(t)}get inFlight(){return this.isInFlight}issue(e,t,i,o,s){if(this.isInFlight)return!1;const{gl:r}=this;if(o*s*4>this.data.length||(this.buffer||(this.buffer=r.createBuffer()),!this.buffer))return!1;const n=r.getParameter(r.READ_FRAMEBUFFER_BINDING);return r.bindFramebuffer(r.READ_FRAMEBUFFER,e),r.bindBuffer(r.PIXEL_PACK_BUFFER,this.buffer),r.bufferData(r.PIXEL_PACK_BUFFER,this.data.byteLength,r.STREAM_READ),r.readPixels(t,i,o,s,r.RGBA,r.FLOAT,0),r.bindBuffer(r.PIXEL_PACK_BUFFER,null),r.bindFramebuffer(r.READ_FRAMEBUFFER,n),this.sync=r.fenceSync(r.SYNC_GPU_COMMANDS_COMPLETE,0),r.flush(),this.isInFlight=this.sync!==null,this.isInFlight}poll(){if(!this.isInFlight||!this.sync||!this.buffer)return null;const{gl:e}=this,t=e.clientWaitSync(this.sync,0,0);return t===e.TIMEOUT_EXPIRED||(e.deleteSync(this.sync),this.sync=null,this.isInFlight=!1,t!==e.ALREADY_SIGNALED&&t!==e.CONDITION_SATISFIED)?null:(e.bindBuffer(e.PIXEL_PACK_BUFFER,this.buffer),e.getBufferSubData(e.PIXEL_PACK_BUFFER,0,this.data),e.bindBuffer(e.PIXEL_PACK_BUFFER,null),this.data)}cancel(){this.sync&&(this.gl.deleteSync(this.sync),this.sync=null),this.isInFlight=!1}destroy(){this.cancel(),this.buffer&&(this.gl.deleteBuffer(this.buffer),this.buffer=null)}}const xi=h=>{const e=Dt().exponent(2).range([0,1]).domain([-1,1]),t=Lt(0,h).map(o=>-.5+o/h);t.push(.5);const i=new Array(t.length*2);return t.forEach((o,s)=>{i[s*2]=[e(o*2),.5],i[s*2+1]=[e(o*2),-.5]}),i};class Si extends V{constructor(){super(...arguments),this.isLinkIndexBufferStale=!0,this.linkStatusTextureSize=0,this.programsSpaceDimensions=2,this.transitionProgress=1,this.shouldAnimateLinkColors=!1,this.shouldAnimateLinkWidths=!1,this.shouldAnimatePositions=!1}get isPickInFlight(){var e;return((e=this.pickingReadback)==null?void 0:e.inFlight)??!1}initPrograms(){const{device:e,config:t,store:i,data:o}=this;this.programsSpaceDimensions!==i.spaceDimensions&&(this.programsSpaceDimensions=i.spaceDimensions,this.drawCurveCommand&&(this.drawCurveCommand.destroy(),this.drawCurveCommand=void 0),this.drawCurvePickingCommand&&(this.drawCurvePickingCommand.destroy(),this.drawCurvePickingCommand=void 0),this.fillSampledLinksFboCommand&&(this.fillSampledLinksFboCommand.destroy(),this.fillSampledLinksFboCommand=void 0)),this.updateLinkIndexFbo(),this.isLinkIndexBufferStale=!0,this.curveLineGeometry||this.updateCurveLineGeometry();const s=this.data.linksNumber??0;this.pointABuffer||(this.pointABuffer=e.createBuffer({data:new Float32Array(s*2),usage:x.VERTEX|x.COPY_DST})),this.pointBBuffer||(this.pointBBuffer=e.createBuffer({data:new Float32Array(s*2),usage:x.VERTEX|x.COPY_DST})),this.arrowBuffer||(this.arrowBuffer=e.createBuffer({data:new Float32Array(s),usage:x.VERTEX|x.COPY_DST})),this.linkStyleBuffer||(this.linkStyleBuffer=e.createBuffer({data:new Float32Array(s),usage:x.VERTEX|x.COPY_DST})),this.linkIndexBuffer||(this.linkIndexBuffer=e.createBuffer({data:new Float32Array(s),usage:x.VERTEX|x.COPY_DST})),this.drawLineUniformStore||(this.drawLineUniformStore=new T(e,{drawLineUniforms:{uniformTypes:{transformationMatrix:"mat4x4<f32>",pointsTextureSize:"f32",widthScale:"f32",linkArrowsSizeScale:"f32",spaceSize:"f32",screenSize:"vec2<f32>",linkVisibilityDistanceRange:"vec2<f32>",linkVisibilityMinTransparency:"f32",linkOpacity:"f32",greyoutOpacity:"f32",curvedWeight:"f32",curvedLinkControlPointDistance:"f32",curvedLinkSegments:"f32",scaleLinksOnZoom:"f32",maxPointSize:"f32",renderMode:"f32",hoveredLinkIndex:"f32",hoveredLinkWidthIncrease:"f32",isLinkHighlightingActive:"f32",linkStatusTextureSize:"f32",focusedLinkIndex:"f32",focusedLinkWidthIncrease:"f32",transitionProgress:"f32",animateColors:"f32",animateWidths:"f32",animatePositions:"f32",pointDefaultColor:"vec4<f32>",linkColorInterpolateFromEndpoints:"f32"},defaultUniforms:{transformationMatrix:i.transformationMatrix4x4,pointsTextureSize:i.pointsTextureSize,widthScale:t.linkWidthScale,linkArrowsSizeScale:t.linkArrowsSizeScale,spaceSize:i.adjustedSpaceSize,screenSize:k(i.screenSize,[0,0]),linkVisibilityDistanceRange:k(t.linkVisibilityDistanceRange,[0,0]),linkVisibilityMinTransparency:t.linkVisibilityMinTransparency,linkOpacity:t.linkOpacity,greyoutOpacity:t.linkGreyoutOpacity,curvedWeight:t.curvedLinkWeight,curvedLinkControlPointDistance:t.curvedLinkControlPointDistance,curvedLinkSegments:t.curvedLinks?t.curvedLinkSegments:1,scaleLinksOnZoom:t.scaleLinksOnZoom?1:0,maxPointSize:i.maxPointSize,renderMode:0,hoveredLinkIndex:i.hoveredLinkIndex??-1,hoveredLinkWidthIncrease:t.hoveredLinkWidthIncrease,isLinkHighlightingActive:0,linkStatusTextureSize:0,focusedLinkIndex:t.focusedLinkIndex??-1,focusedLinkWidthIncrease:t.focusedLinkWidthIncrease,transitionProgress:1,animateColors:0,animateWidths:0,animatePositions:0,pointDefaultColor:w(this.data.defaultRgba,[0,0,0,1]),linkColorInterpolateFromEndpoints:t.linkColorInterpolateFromEndpoints?1:0}},drawLineFragmentUniforms:{uniformTypes:{renderMode:"f32",linkDashLength:"f32",linkDashGap:"f32",linkColorInterpolateFromEndpoints:"f32",hoveredLinkIndex:"f32",hoveredLinkColor:"vec4<f32>"},defaultUniforms:{renderMode:0,linkDashLength:t.linkDashLength,linkDashGap:t.linkDashGap,linkColorInterpolateFromEndpoints:t.linkColorInterpolateFromEndpoints?1:0,hoveredLinkIndex:i.hoveredLinkIndex??-1,hoveredLinkColor:w(i.hoveredLinkColor,[-1,-1,-1,-1])}}})),this.drawCurveCommand||(this.drawCurveCommand=this.createDrawCurveCommand(this.getLinkBlendParameters(this.config.linkBlending))),this.isLinkBlendingActive=this.config.linkBlending,this.fillSampledLinksUniformStore||(this.fillSampledLinksUniformStore=new T(e,{fillSampledLinksUniforms:{uniformTypes:{pointsTextureSize:"f32",transformationMatrix:"mat4x4<f32>",spaceSize:"f32",screenSize:"vec2<f32>",curvedWeight:"f32",curvedLinkControlPointDistance:"f32",curvedLinkSegments:"f32"},defaultUniforms:{pointsTextureSize:i.pointsTextureSize??0,transformationMatrix:i.transformationMatrix4x4,spaceSize:i.adjustedSpaceSize,screenSize:k(i.screenSize,[0,0]),curvedWeight:t.curvedLinkWeight,curvedLinkControlPointDistance:t.curvedLinkControlPointDistance,curvedLinkSegments:t.curvedLinks?t.curvedLinkSegments:1}}})),this.fillSampledLinksFboCommand||(this.fillSampledLinksFboCommand=new b(e,{fs:gi,vs:vi,modules:[Ze],topology:"point-list",vertexCount:o.linksNumber??0,attributes:{...this.pointABuffer&&{pointA:this.pointABuffer},...this.pointBBuffer&&{pointB:this.pointBBuffer},...this.linkIndexBuffer&&{linkIndices:this.linkIndexBuffer}},bufferLayout:[{name:"pointA",format:"float32x2"},{name:"pointB",format:"float32x2"},{name:"linkIndices",format:"float32"}],defines:{USE_UNIFORM_BUFFERS:!0,...i.is3D?{SPACE_3D:!0}:{}},bindings:{fillSampledLinksUniforms:this.fillSampledLinksUniformStore.getManagedUniformBuffer("fillSampledLinksUniforms")},parameters:{depthWriteEnabled:!1,depthCompare:"always",blend:!1}})),this.updateSampledLinksGrid(),this.updateLinkStatus()}draw(e){const{config:t,points:i,store:o}=this;if(!i||!i.currentPositionTexture||i.currentPositionTexture.destroyed||(i.exitTexture||i.updateExit(),!i.exitTexture||i.exitTexture.destroyed)||((!this.pointABuffer||!this.pointBBuffer)&&this.updatePointsBuffer(),this.targetColorBuffer||this.updateColor(),this.targetWidthBuffer||this.updateWidth(),this.arrowBuffer||this.updateArrow(),this.linkStyleBuffer||this.updateStyle(),this.curveLineGeometry||this.updateCurveLineGeometry(),!this.drawCurveCommand||!this.drawLineUniformStore||!this.linkStatusTexture))return;this.updateLinkBlending();const s=t.highlightedLinkIndices!==void 0;this.drawLineUniformStore.setUniforms({drawLineUniforms:{transformationMatrix:o.transformationMatrix4x4,pointsTextureSize:o.pointsTextureSize,widthScale:t.linkWidthScale,linkArrowsSizeScale:t.linkArrowsSizeScale,spaceSize:o.adjustedSpaceSize,screenSize:k(o.screenSize,[0,0]),linkVisibilityDistanceRange:k(t.linkVisibilityDistanceRange,[0,0]),linkVisibilityMinTransparency:t.linkVisibilityMinTransparency,linkOpacity:t.linkOpacity,greyoutOpacity:t.linkGreyoutOpacity,curvedWeight:t.curvedLinkWeight,curvedLinkControlPointDistance:t.curvedLinkControlPointDistance,curvedLinkSegments:t.curvedLinks?t.curvedLinkSegments:1,scaleLinksOnZoom:t.scaleLinksOnZoom?1:0,maxPointSize:o.maxPointSize,renderMode:0,hoveredLinkIndex:o.hoveredLinkIndex??-1,hoveredLinkWidthIncrease:t.hoveredLinkWidthIncrease,isLinkHighlightingActive:s?1:0,linkStatusTextureSize:this.linkStatusTextureSize,focusedLinkIndex:t.focusedLinkIndex??-1,focusedLinkWidthIncrease:t.focusedLinkWidthIncrease,transitionProgress:this.transitionProgress,animateColors:this.shouldAnimateLinkColors?1:0,animateWidths:this.shouldAnimateLinkWidths?1:0,animatePositions:this.shouldAnimatePositions?1:0,pointDefaultColor:w(this.data.defaultRgba,[0,0,0,1]),linkColorInterpolateFromEndpoints:t.linkColorInterpolateFromEndpoints?1:0},drawLineFragmentUniforms:{renderMode:0,linkDashLength:t.linkDashLength,linkDashGap:t.linkDashGap,linkColorInterpolateFromEndpoints:t.linkColorInterpolateFromEndpoints?1:0,hoveredLinkIndex:o.hoveredLinkIndex??-1,hoveredLinkColor:w(o.hoveredLinkColor,[-1,-1,-1,-1])}}),this.drawCurveCommand.setBindings({positionsTexture:i.currentPositionTexture,exitTexture:i.exitTexture,linkStatus:this.linkStatusTexture,pointColorsTexture:i.pointColorsTexture??i.currentPositionTexture}),this.drawCurveCommand.setInstanceCount(this.data.linksNumber??0),this.drawCurveCommand.draw(e)}updateLinkIndexFbo(){var e,t,i;const{device:o,store:s}=this;if(!this.store.isLinkHoveringEnabled)return;const r=s.screenSize??[0,0],n=r[0],a=r[1];if(!n||!a)return;const l=((e=this.previousScreenSize)==null?void 0:e[0])!==n||((t=this.previousScreenSize)==null?void 0:t[1])!==a;(!this.linkIndexTexture||l)&&((i=this.pickingReadback)==null||i.cancel(),this.linkIndexFbo&&!this.linkIndexFbo.destroyed&&this.linkIndexFbo.destroy(),this.linkIndexTexture&&!this.linkIndexTexture.destroyed&&this.linkIndexTexture.destroy(),this.linkIndexTexture=o.createTexture({width:n,height:a,format:"rgba32float",usage:g.SAMPLE|g.RENDER}),this.linkIndexFbo=o.createFramebuffer({width:n,height:a,colorAttachments:[this.linkIndexTexture]}),this.previousScreenSize=[n,a],this.isLinkIndexBufferStale=!0)}updateSampledLinksGrid(){const{store:{screenSize:e},config:{linkSamplingDistance:t},device:i}=this;let o=t??Math.min(...e)/2;o===0&&(o=M.linkSamplingDistance);const s=Math.ceil(e[0]/o),r=Math.ceil(e[1]/o);s===0||r===0||(!this.sampledLinksFbo||this.sampledLinksFbo.width!==s||this.sampledLinksFbo.height!==r)&&(this.sampledLinksFbo&&!this.sampledLinksFbo.destroyed&&this.sampledLinksFbo.destroy(),this.sampledLinksFbo=i.createFramebuffer({width:s,height:r,colorAttachments:["rgba32float"]}))}updatePointsBuffer(){var e;const{device:t,data:i,store:o}=this;if(i.linksNumber===void 0||i.links===void 0||!o.pointsTextureSize)return;this.isLinkIndexBufferStale=!0,this.discardPendingPick();const s=new Float32Array(i.linksNumber*2),r=new Float32Array(i.linksNumber*2);for(let l=0;l<i.linksNumber;l++){const u=i.links[l*2],d=i.links[l*2+1],c=u%o.pointsTextureSize,f=Math.floor(u/o.pointsTextureSize),p=d%o.pointsTextureSize,m=Math.floor(d/o.pointsTextureSize);s[l*2]=c,s[l*2+1]=f,r[l*2]=p,r[l*2+1]=m}const n=(((e=this.pointABuffer)==null?void 0:e.byteLength)??0)/(Float32Array.BYTES_PER_ELEMENT*2);!this.pointABuffer||n!==i.linksNumber?(this.pointABuffer&&!this.pointABuffer.destroyed&&this.pointABuffer.destroy(),this.pointABuffer=t.createBuffer({data:s,usage:x.VERTEX|x.COPY_DST})):this.pointABuffer.write(s),!this.pointBBuffer||n!==i.linksNumber?(this.pointBBuffer&&!this.pointBBuffer.destroyed&&this.pointBBuffer.destroy(),this.pointBBuffer=t.createBuffer({data:r,usage:x.VERTEX|x.COPY_DST})):this.pointBBuffer.write(r);const a=new Float32Array(i.linksNumber);for(let l=0;l<i.linksNumber;l++)a[l]=l;!this.linkIndexBuffer||n!==i.linksNumber?(this.linkIndexBuffer&&!this.linkIndexBuffer.destroyed&&this.linkIndexBuffer.destroy(),this.linkIndexBuffer=t.createBuffer({data:a,usage:x.VERTEX|x.COPY_DST})):this.linkIndexBuffer.write(a),this.setDrawCurveCommandAttributes({pointA:this.pointABuffer,pointB:this.pointBBuffer,linkIndices:this.linkIndexBuffer}),this.fillSampledLinksFboCommand&&this.fillSampledLinksFboCommand.setAttributes({pointA:this.pointABuffer,pointB:this.pointBBuffer,linkIndices:this.linkIndexBuffer}),this.updateSampledLinksGrid(),this.config.highlightedLinkIndices!==void 0&&this.updateLinkStatus()}updateColor(){const{data:e}=this,t=e.linksNumber??0;this.isLinkIndexBufferStale=!0;const i=e.linkColors??new Float32Array(t*4).fill(0),{source:o,target:s,previous:r}=oe(this.device,i,this.sourceColorBuffer,this.targetColorBuffer,this.previousColorData,4);this.sourceColorBuffer=o,this.targetColorBuffer=s,this.previousColorData=r,this.setDrawCurveCommandAttributes({...this.sourceColorBuffer&&{sourceColor:this.sourceColorBuffer},...this.targetColorBuffer&&{targetColor:this.targetColorBuffer}})}updateWidth(){const{data:e}=this,t=e.linksNumber??0;this.isLinkIndexBufferStale=!0;const i=e.linkWidths??new Float32Array(t).fill(0),{source:o,target:s,previous:r}=oe(this.device,i,this.sourceWidthBuffer,this.targetWidthBuffer,this.previousWidthData,1);this.sourceWidthBuffer=o,this.targetWidthBuffer=s,this.previousWidthData=r,this.setDrawCurveCommandAttributes({...this.sourceWidthBuffer&&{sourceWidth:this.sourceWidthBuffer},...this.targetWidthBuffer&&{targetWidth:this.targetWidthBuffer}})}updateArrow(){const{device:e,data:t}=this;this.isLinkIndexBufferStale=!0;const i=t.linksNumber??0,o=t.linkArrows?new Float32Array(t.linkArrows):new Float32Array(i);this.arrowBuffer=Me(e,this.arrowBuffer,o),this.setDrawCurveCommandAttributes({arrow:this.arrowBuffer})}updateStyle(){const{device:e,data:t}=this;t.linksNumber===void 0||t.linkStyles===void 0||(this.linkStyleBuffer=Me(e,this.linkStyleBuffer,t.linkStyles),this.setDrawCurveCommandAttributes({linkStyle:this.linkStyleBuffer}))}updateLinkStatus(){const{device:e,config:t,data:i}=this,o=i.linksNumber??0;if(this.isLinkIndexBufferStale=!0,!o){this.linkStatusTexture||this.ensureLinkStatusPlaceholder();return}const{highlightedLinkIndices:s}=t;if(s===void 0){this.linkStatusTexture||this.ensureLinkStatusPlaceholder(),this.linkStatusTextureSize=0;return}const r=Math.ceil(Math.sqrt(o));this.linkStatusTextureSize=r;const n=new Float32Array(r*r*4);for(let l=0;l<o;l++)n[l*4]=1;for(const l of s)l>=0&&l<o&&(n[l*4]=0);const a={data:n,bytesPerRow:y("rgba32float",r),mipLevel:0,x:0,y:0};!this.linkStatusTexture||this.linkStatusTexture.width!==r||this.linkStatusTexture.height!==r?(this.linkStatusTexture&&!this.linkStatusTexture.destroyed&&this.linkStatusTexture.destroy(),this.linkStatusTexture=e.createTexture({width:r,height:r,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST}),this.linkStatusTexture.copyImageData(a)):this.linkStatusTexture.copyImageData(a)}updateCurveLineGeometry(){var e,t;const{device:i,config:{curvedLinks:o,curvedLinkSegments:s}}=this;this.isLinkIndexBufferStale=!0,this.curveLineGeometry=xi(o?s:1);const r=new Float32Array(this.curveLineGeometry.length*2);for(let n=0;n<this.curveLineGeometry.length;n++)r[n*2]=this.curveLineGeometry[n][0],r[n*2+1]=this.curveLineGeometry[n][1];!this.curveLineBuffer||this.curveLineBuffer.byteLength!==r.byteLength?(this.curveLineBuffer&&!this.curveLineBuffer.destroyed&&this.curveLineBuffer.destroy(),this.curveLineBuffer=i.createBuffer({data:r,usage:x.VERTEX|x.COPY_DST})):this.curveLineBuffer.write(r),this.setDrawCurveCommandAttributes({position:this.curveLineBuffer}),(e=this.drawCurveCommand)==null||e.setVertexCount(this.curveLineGeometry.length),(t=this.drawCurvePickingCommand)==null||t.setVertexCount(this.curveLineGeometry.length)}updateLinkBlending(){var e;const t=this.config.linkBlending;t!==this.isLinkBlendingActive&&((e=this.drawCurveCommand)==null||e.setParameters(this.getLinkBlendParameters(t)),this.isLinkBlendingActive=t)}getSampledLinkPositionsMap(e=2){if(e===3){const o=new Map,s=this.fillAndReadSampledLinksFbo();if(!s)return o;const r=this.getSampledLinkMidZ(s);for(let n=0;n<s.length/4;n++){const a=s[n*4],l=s[n*4+1],u=s[n*4+2],d=s[n*4+3];if(a!==void 0&&a>=0&&l!==void 0&&u!==void 0&&d!==void 0){const c=Math.round(a);o.set(c,[l,u,r?.get(c)??0,d])}}return o}const t=new Map,i=this.fillAndReadSampledLinksFbo();if(!i)return t;for(let o=0;o<i.length/4;o++){const s=i[o*4],r=i[o*4+1],n=i[o*4+2],a=i[o*4+3];s!==void 0&&s>=0&&r!==void 0&&n!==void 0&&a!==void 0&&t.set(Math.round(s),[r,n,a])}return t}getSampledLinks(e=2){const t=[],i=[],o=[],s=this.fillAndReadSampledLinksFbo();if(!s)return{indices:t,positions:i,angles:o};const r=e===3?this.getSampledLinkMidZ(s):void 0;for(let n=0;n<s.length/4;n++){const a=s[n*4],l=s[n*4+1],u=s[n*4+2],d=s[n*4+3];if(a!==void 0&&a>=0&&l!==void 0&&u!==void 0&&d!==void 0){const c=Math.round(a);t.push(c),i.push(l,u),e===3&&i.push(r?.get(c)??0),o.push(d)}}return{indices:t,positions:i,angles:o}}updateLinkIndexBuffer(){if(!this.isLinkIndexBufferStale)return;this.updateLinkIndexFbo();const{config:e,points:t,store:i}=this;if(!t||!t.currentPositionTexture||t.currentPositionTexture.destroyed||(t.exitTexture||t.updateExit(),!t.exitTexture||t.exitTexture.destroyed)||!this.data.linksNumber||!this.store.isLinkHoveringEnabled||!this.linkIndexFbo||!this.drawLineUniformStore||!this.linkStatusTexture||!this.linkIndexTexture||this.linkIndexTexture.destroyed)return;this.drawCurvePickingCommand||(this.drawCurvePickingCommand=this.createDrawCurveCommand(this.getLinkBlendParameters(!1)));const o=e.highlightedLinkIndices!==void 0;this.drawLineUniformStore.setUniforms({drawLineUniforms:{transformationMatrix:i.transformationMatrix4x4,pointsTextureSize:i.pointsTextureSize,widthScale:e.linkWidthScale,linkArrowsSizeScale:e.linkArrowsSizeScale,spaceSize:i.adjustedSpaceSize,screenSize:k(i.screenSize,[0,0]),linkVisibilityDistanceRange:k(e.linkVisibilityDistanceRange,[0,0]),linkVisibilityMinTransparency:e.linkVisibilityMinTransparency,linkOpacity:e.linkOpacity,greyoutOpacity:e.linkGreyoutOpacity,curvedWeight:e.curvedLinkWeight,curvedLinkControlPointDistance:e.curvedLinkControlPointDistance,curvedLinkSegments:e.curvedLinks?e.curvedLinkSegments:1,scaleLinksOnZoom:e.scaleLinksOnZoom?1:0,maxPointSize:i.maxPointSize,renderMode:1,hoveredLinkIndex:i.hoveredLinkIndex??-1,hoveredLinkWidthIncrease:e.hoveredLinkWidthIncrease,isLinkHighlightingActive:o?1:0,linkStatusTextureSize:this.linkStatusTextureSize,focusedLinkIndex:e.focusedLinkIndex??-1,focusedLinkWidthIncrease:e.focusedLinkWidthIncrease,transitionProgress:this.transitionProgress,animateColors:this.shouldAnimateLinkColors?1:0,animateWidths:this.shouldAnimateLinkWidths?1:0,animatePositions:this.shouldAnimatePositions?1:0,pointDefaultColor:w(this.data.defaultRgba,[0,0,0,1]),linkColorInterpolateFromEndpoints:e.linkColorInterpolateFromEndpoints?1:0},drawLineFragmentUniforms:{renderMode:1,linkDashLength:e.linkDashLength,linkDashGap:e.linkDashGap,linkColorInterpolateFromEndpoints:e.linkColorInterpolateFromEndpoints?1:0,hoveredLinkIndex:i.hoveredLinkIndex??-1,hoveredLinkColor:w(i.hoveredLinkColor,[-1,-1,-1,-1])}}),this.drawCurvePickingCommand.setBindings({positionsTexture:t.currentPositionTexture,exitTexture:t.exitTexture,linkStatus:this.linkStatusTexture,pointColorsTexture:t.pointColorsTexture??t.currentPositionTexture}),this.drawCurvePickingCommand.setInstanceCount(this.data.linksNumber??0);const s=this.device.beginRenderPass({framebuffer:this.linkIndexFbo,clearColor:[0,0,0,0]});this.drawCurvePickingCommand.draw(s),s.end(),this.isLinkIndexBufferStale=!1}pickLinkSync(){this.updateLinkIndexBuffer();const e=this.getCursorPickingPixel();if(!e||!this.linkIndexFbo||this.linkIndexFbo.destroyed)return;const t=B(this.device,this.linkIndexFbo,e.x,e.y,1,1);return Xe(t)}requestPickLink(){var e;if((e=this.pickingReadback)!=null&&e.inFlight)return!1;if(this.updateLinkIndexBuffer(),!this.linkIndexFbo||this.linkIndexFbo.destroyed)return!0;const t=this.device.gl,i=this.linkIndexFbo.handle;if(!t||!i)return!0;this.pickingReadback||(this.pickingReadback=new Ye(t,4));const o=this.getCursorPickingPixel();return o?this.pickingReadback.issue(i,o.x,o.y,1,1):!0}discardPendingPick(){var e;(e=this.pickingReadback)==null||e.cancel()}takePickLinkResult(){if(!this.pickingReadback)return;const e=this.pickingReadback.poll();if(e)return Xe(e)??null}setTransitionProgress(e,t=!1,i=!1,o=!1){e!==this.transitionProgress&&(t||i)&&(this.isLinkIndexBufferStale=!0),this.transitionProgress=e,this.shouldAnimateLinkColors=t,this.shouldAnimateLinkWidths=i,this.shouldAnimatePositions=o}destroy(){var e,t,i,o,s,r;(e=this.drawCurveCommand)==null||e.destroy(),this.drawCurveCommand=void 0,(t=this.drawCurvePickingCommand)==null||t.destroy(),this.drawCurvePickingCommand=void 0,this.isLinkBlendingActive=void 0,(i=this.fillSampledLinksFboCommand)==null||i.destroy(),this.fillSampledLinksFboCommand=void 0,(o=this.pickingReadback)==null||o.destroy(),this.pickingReadback=void 0,this.linkIndexFbo&&!this.linkIndexFbo.destroyed&&this.linkIndexFbo.destroy(),this.linkIndexFbo=void 0,this.sampledLinksFbo&&!this.sampledLinksFbo.destroyed&&this.sampledLinksFbo.destroy(),this.sampledLinksFbo=void 0,this.linkIndexTexture&&!this.linkIndexTexture.destroyed&&this.linkIndexTexture.destroy(),this.linkIndexTexture=void 0,this.linkStatusTexture&&!this.linkStatusTexture.destroyed&&this.linkStatusTexture.destroy(),this.linkStatusTexture=void 0,(s=this.drawLineUniformStore)==null||s.destroy(),this.drawLineUniformStore=void 0,(r=this.fillSampledLinksUniformStore)==null||r.destroy(),this.fillSampledLinksUniformStore=void 0,this.pointABuffer&&!this.pointABuffer.destroyed&&this.pointABuffer.destroy(),this.pointABuffer=void 0,this.pointBBuffer&&!this.pointBBuffer.destroyed&&this.pointBBuffer.destroy(),this.pointBBuffer=void 0,this.sourceColorBuffer&&!this.sourceColorBuffer.destroyed&&this.sourceColorBuffer.destroy(),this.sourceColorBuffer=void 0,this.targetColorBuffer&&!this.targetColorBuffer.destroyed&&this.targetColorBuffer.destroy(),this.targetColorBuffer=void 0,this.previousColorData=void 0,this.sourceWidthBuffer&&!this.sourceWidthBuffer.destroyed&&this.sourceWidthBuffer.destroy(),this.sourceWidthBuffer=void 0,this.targetWidthBuffer&&!this.targetWidthBuffer.destroyed&&this.targetWidthBuffer.destroy(),this.targetWidthBuffer=void 0,this.previousWidthData=void 0,this.arrowBuffer&&!this.arrowBuffer.destroyed&&this.arrowBuffer.destroy(),this.arrowBuffer=void 0,this.linkStyleBuffer&&!this.linkStyleBuffer.destroyed&&this.linkStyleBuffer.destroy(),this.linkStyleBuffer=void 0,this.curveLineBuffer&&!this.curveLineBuffer.destroyed&&this.curveLineBuffer.destroy(),this.curveLineBuffer=void 0,this.linkIndexBuffer&&!this.linkIndexBuffer.destroyed&&this.linkIndexBuffer.destroy(),this.linkIndexBuffer=void 0}getCursorPickingPixel(){if(!this.linkIndexFbo||this.linkIndexFbo.destroyed)return;const[e,t]=this.store.screenSize;if(!e||!t)return;const i=Math.floor(this.store.screenMousePosition[0]*(this.linkIndexFbo.width/e)),o=Math.floor(this.store.screenMousePosition[1]*(this.linkIndexFbo.height/t));return{x:Math.min(Math.max(i,0),this.linkIndexFbo.width-1),y:Math.min(Math.max(o,0),this.linkIndexFbo.height-1)}}fillAndReadSampledLinksFbo(){if(!this.sampledLinksFbo||this.sampledLinksFbo.destroyed)return;const e=this.points;if(!(!(e!=null&&e.currentPositionTexture)||e.currentPositionTexture.destroyed)&&(e.exitTexture||e.updateExit(),!(!e.exitTexture||e.exitTexture.destroyed))){if(this.fillSampledLinksFboCommand&&this.fillSampledLinksUniformStore){this.fillSampledLinksFboCommand.setVertexCount(this.data.linksNumber??0),this.fillSampledLinksUniformStore.setUniforms({fillSampledLinksUniforms:{pointsTextureSize:this.store.pointsTextureSize??0,transformationMatrix:this.store.transformationMatrix4x4,spaceSize:this.store.adjustedSpaceSize,screenSize:k(this.store.screenSize,[0,0]),curvedWeight:this.config.curvedLinkWeight,curvedLinkControlPointDistance:this.config.curvedLinkControlPointDistance,curvedLinkSegments:this.config.curvedLinks?this.config.curvedLinkSegments:1}}),this.fillSampledLinksFboCommand.setBindings({positionsTexture:e.currentPositionTexture,exitTexture:e.exitTexture});const t=this.device.beginRenderPass({framebuffer:this.sampledLinksFbo,clearColor:[-1,-1,-1,-1]});this.fillSampledLinksFboCommand.draw(t),t.end()}return B(this.device,this.sampledLinksFbo)}}getSampledLinkMidZ(e){var t;if(!this.store.is3D)return;const i=this.data.links,o=(t=this.points)==null?void 0:t.currentPositionFbo;if(!i||!o||o.destroyed)return;const s=B(this.device,o),r=new Map;for(let n=0;n<e.length/4;n++){const a=e[n*4];if(a===void 0||a<0)continue;const l=Math.round(a),u=i[l*2],d=i[l*2+1];if(u===void 0||d===void 0)continue;const c=s[u*4+3]??0,f=s[d*4+3]??0;r.set(l,(c+f)/2)}return r}createDrawCurveCommand(e){var t;if(!this.drawLineUniformStore)throw new Error("Draw line uniforms must be initialized before creating link draw commands");return new b(this.device,{vs:mi,fs:pi,modules:[Ze,Q],topology:"triangle-strip",vertexCount:((t=this.curveLineGeometry)==null?void 0:t.length)??0,attributes:this.getDrawCurveCommandAttributes(),bufferLayout:[{name:"position",format:"float32x2"},{name:"pointA",format:"float32x2",stepMode:"instance"},{name:"pointB",format:"float32x2",stepMode:"instance"},{name:"sourceColor",format:"float32x4",stepMode:"instance"},{name:"targetColor",format:"float32x4",stepMode:"instance"},{name:"sourceWidth",format:"float32",stepMode:"instance"},{name:"targetWidth",format:"float32",stepMode:"instance"},{name:"arrow",format:"float32",stepMode:"instance"},{name:"linkIndices",format:"float32",stepMode:"instance"},{name:"linkStyle",format:"float32",stepMode:"instance"}],defines:{USE_UNIFORM_BUFFERS:!0,...this.store.is3D?{SPACE_3D:!0}:{},EXIT_DEFAULT_COLOR_CHANNEL:$(Y)},bindings:{drawLineUniforms:this.drawLineUniformStore.getManagedUniformBuffer("drawLineUniforms"),drawLineFragmentUniforms:this.drawLineUniformStore.getManagedUniformBuffer("drawLineFragmentUniforms")},parameters:e})}getDrawCurveCommandAttributes(){const e={};return this.curveLineBuffer&&(e.position=this.curveLineBuffer),this.pointABuffer&&(e.pointA=this.pointABuffer),this.pointBBuffer&&(e.pointB=this.pointBBuffer),this.sourceColorBuffer&&(e.sourceColor=this.sourceColorBuffer),this.targetColorBuffer&&(e.targetColor=this.targetColorBuffer),this.sourceWidthBuffer&&(e.sourceWidth=this.sourceWidthBuffer),this.targetWidthBuffer&&(e.targetWidth=this.targetWidthBuffer),this.arrowBuffer&&(e.arrow=this.arrowBuffer),this.linkIndexBuffer&&(e.linkIndices=this.linkIndexBuffer),this.linkStyleBuffer&&(e.linkStyle=this.linkStyleBuffer),e}setDrawCurveCommandAttributes(e){var t,i;(t=this.drawCurveCommand)==null||t.setAttributes(e),(i=this.drawCurvePickingCommand)==null||i.setAttributes(e)}getLinkBlendParameters(e){const t=this.store.is3D,i={cullMode:t?"none":"back",depthWriteEnabled:t&&!e,depthCompare:t?"less-equal":"always"};return e?{...i,blend:!0,blendColorOperation:"add",blendColorSrcFactor:"src-alpha",blendColorDstFactor:"one-minus-src-alpha",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one-minus-src-alpha"}:{...i,blend:!1}}ensureLinkStatusPlaceholder(){this.linkStatusTexture&&!this.linkStatusTexture.destroyed||(this.linkStatusTexture=this.device.createTexture({width:1,height:1,format:"rgba32float",usage:g.SAMPLE|g.RENDER|g.COPY_DST,data:new Float32Array(4).fill(0)}),this.linkStatusTextureSize=0)}}const Ke=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D imageAtlasTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform drawFragmentUniforms {
  float greyoutOpacity;
  float pointOpacity;
  float isDarkenGreyout;
  vec4 backgroundColor;
  vec4 outlineColor;
  float outlineWidth;
  float renderMode;
  float sphereShading;
} drawFragment;

#define greyoutOpacity drawFragment.greyoutOpacity
#define pointOpacity drawFragment.pointOpacity
#define isDarkenGreyout drawFragment.isDarkenGreyout
#define backgroundColor drawFragment.backgroundColor
#define outlineColor drawFragment.outlineColor
#define outlineWidth drawFragment.outlineWidth
#define renderMode drawFragment.renderMode
#define sphereShading drawFragment.sphereShading
#else
uniform float greyoutOpacity;
uniform float pointOpacity;
uniform float isDarkenGreyout;
uniform vec4 backgroundColor;
uniform vec4 outlineColor;
uniform float outlineWidth;
uniform float renderMode;
uniform float sphereShading;
#endif


in float pointShape;
in float isGreyedOut;
in float isOutlined;
in vec4 shapeColor;
in vec4 imageAtlasUV;
in float shapeSize;
in float imageSizeVarying;
in float overallSize;
in float depthFadeVarying;

out vec4 fragColor;

// Smoothing controls the smoothness of the point's edge
const float smoothing = 0.9;

// Occlusion culling splits fragments between the opaque core pass (renderMode 1)
// and the blended fringe pass (renderMode 2) at this final-alpha threshold
const float OPAQUE_ALPHA_THRESHOLD = 0.999;

// Shape constants
const float CIRCLE = 0.0;
const float SQUARE = 1.0;
const float TRIANGLE = 2.0;
const float DIAMOND = 3.0;
const float PENTAGON = 4.0;
const float HEXAGON = 5.0;
const float STAR = 6.0;
const float CROSS = 7.0;
const float NONE = 8.0;

// Distance functions for different shapes
float circleDistance(vec2 p) {
    return dot(p, p);
}

// Function to apply greyout logic to image colors
vec4 applyGreyoutToImage(vec4 imageColor, float isGreyedOutValue) {
    vec3 finalColor = imageColor.rgb;
    float finalAlpha = imageColor.a;
    
    if (isGreyedOutValue > 0.0) {
        float blendFactor = 0.65; // Controls how much to modify (0.0 = original, 1.0 = target color)
        
        if (isDarkenGreyout > 0.0) {
            finalColor = mix(finalColor, vec3(0.2), blendFactor);
        } else {
            finalColor = mix(finalColor, max(backgroundColor.rgb, vec3(0.8)), blendFactor);
        }
    }
    
    return vec4(finalColor, finalAlpha);
}

float squareDistance(vec2 p) {
    vec2 d = abs(p) - vec2(0.8);
    return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

float triangleDistance(vec2 p) {
    const float k = sqrt(3.0);   // \u22481.732; slope of 60\xB0 lines for an equilateral triangle
    p.x = abs(p.x) - 0.9;        // fold the X axis and shift: brings left and right halves together
    p.y = p.y + 0.55;             // move the whole shape up slightly so it is centred vertically

    // reflect points that fall outside the main triangle back inside, to reuse the same maths
    if (p.x + k * p.y > 0.0)
        p = vec2(p.x - k * p.y,  -k * p.x - p.y) / 2.0;

    p.x -= clamp(p.x, -1.0, 0.0); // clip any remainder on the left side

    // Return signed distance: negative = inside; positive = outside
    return -length(p) * sign(p.y);
}

float diamondDistance(vec2 p) {
    // aspect > 1  \u2192  taller diamond
    const float aspect = 1.2;
    return abs(p.x) + abs(p.y) / aspect - 0.8;
}

float pentagonDistance(vec2 p) {
    // Regular pentagon signed-distance (Inigo Quilez)
    const vec3 k = vec3(0.809016994, 0.587785252, 0.726542528);
    p.x = abs(p.x);

    // Reflect across the two tilted edges \u2500 only if point is outside
    p -= 2.0 * min(dot(vec2(-k.x, k.y), p), 0.0) * vec2(-k.x, k.y);
    p -= 2.0 * min(dot(vec2( k.x, k.y), p), 0.0) * vec2( k.x, k.y);

    // Clip against the top horizontal edge (keeps top point sharp)
    p -= vec2(clamp(p.x, -k.z * k.x, k.z * k.x), k.z);

    // Return signed distance (negative \u2192 inside, positive \u2192 outside)
    return length(p) * sign(p.y);
}

float hexagonDistance(vec2 p) {
    const vec3 k = vec3(-0.866025404, 0.5, 0.577350269);
    p = abs(p);
    p -= 2.0 * min(dot(k.xy, p), 0.0) * k.xy;
    p -= vec2(clamp(p.x, -k.z * 0.8, k.z * 0.8), 0.8);
    return length(p) * sign(p.y);
}

float starDistance(vec2 p) {
    // 5-point star signed-distance function (adapted from Inigo Quilez)
    // r  \u2013 outer radius, rf \u2013 inner/outer radius ratio
    const float r  = 0.9;
    const float rf = 0.45;

    // Pre-computed rotation vectors for the star arms (36\xB0 increments)
    const vec2 k1 = vec2(0.809016994, -0.587785252);
    const vec2 k2 = vec2(-k1.x, k1.y);

    // Fold the plane into a single arm sector
    p.x = abs(p.x);
    p -= 2.0 * max(dot(k1, p), 0.0) * k1;
    p -= 2.0 * max(dot(k2, p), 0.0) * k2;
    p.x = abs(p.x);

    // Translate so the top tip of the star lies on the X-axis
    p.y -= r;

    // Vector describing the edge between an outer tip and its adjacent inner point
    vec2 ba = rf * vec2(-k1.y, k1.x) - vec2(0.0, 1.0);
    // Project the point onto that edge and clamp the projection to the segment
    float h = clamp(dot(p, ba) / dot(ba, ba), 0.0, r);

    // Return signed distance (negative => inside, positive => outside)
    return length(p - ba * h) * sign(p.y * ba.x - p.x * ba.y);
}

float crossDistance(vec2 p) {
    // Signed distance function for a cross (union of two rectangles)
    // Adapted from Inigo Quilez (https://iquilezles.org/)
    // Each arm has half-sizes 0.3 (thickness) and 0.8 (length)
    p = abs(p);
    if (p.y > p.x) p = p.yx;       // exploit symmetry

    vec2 q = p - vec2(0.8, 0.3);   // subtract half-sizes (length, thickness)

    // Standard rectangle SDF, then take union of the two arms
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0);
}

float getShapeDistance(vec2 p, float shape) {
    if (shape == SQUARE) return squareDistance(p);
    else if (shape == TRIANGLE) return triangleDistance(p);
    else if (shape == DIAMOND) return diamondDistance(p);
    else if (shape == PENTAGON) return pentagonDistance(p);
    else if (shape == HEXAGON) return hexagonDistance(p);
    else if (shape == STAR) return starDistance(p);
    else if (shape == CROSS) return crossDistance(p);
    else return circleDistance(p); // Default to circle
}

void main() {
    // Discard the fragment if the point is fully transparent and has no image
    if (shapeColor.a == 0.0 && imageAtlasUV.x == -1.0) {
        discard;
    }

    // Discard the fragment if the point has no shape and no image
    if (pointShape == NONE && imageAtlasUV.x == -1.0) {
        discard;
    }

    // Calculate coordinates within the point
    vec2 pointCoord = 2.0 * gl_PointCoord - 1.0;

    vec4 finalShapeColor = vec4(0.0);
    vec4 finalImageColor = vec4(0.0);
    // Geometric sprite coverage (shape SDF / image / outline ring alpha, before any
    // color-alpha or opacity multiplies) \u2014 drives the 3D depth-write discard below.
    float coverage = 0.0;
    
    // Handle shape rendering with centering logic
    if (pointShape != NONE) {
        // Calculate shape coordinates with centering
        vec2 shapeCoord = pointCoord;
        if (overallSize > shapeSize && shapeSize > 0.0) {
            // Shape is smaller than overall size, center it
            float scale = shapeSize / overallSize;
            shapeCoord = pointCoord / scale;
        }
        
        float opacity;
        if (pointShape == CIRCLE) {
            // For circles, use the original distance calculation
            float pointCenterDistance = dot(shapeCoord, shapeCoord);
            opacity = 1.0 - smoothstep(smoothing, 1.0, pointCenterDistance);
        } else {
            // For other shapes, use the shape distance function
            float shapeDistance = getShapeDistance(shapeCoord, pointShape);
            opacity = 1.0 - smoothstep(-0.01, 0.01, shapeDistance);
        }
        coverage = opacity;
        opacity *= shapeColor.a;

        finalShapeColor = vec4(shapeColor.rgb, opacity);
    }

    // Handle image rendering with centering logic
    if (imageAtlasUV.x != -1.0) {
        // Calculate image coordinates with centering
        vec2 imageCoord = pointCoord;
        if (overallSize > imageSizeVarying && imageSizeVarying > 0.0) {
            // Image is smaller than overall size, center it
            float scale = imageSizeVarying / overallSize;
            imageCoord = pointCoord / scale;
            
            // Check if we're outside the valid image area
            if (abs(imageCoord.x) > 1.0 || abs(imageCoord.y) > 1.0) {
                // We're outside the image bounds, don't render the image
                finalImageColor = vec4(0.0);
            } else {
                // Sample from texture atlas
                vec2 atlasUV = mix(imageAtlasUV.xy, imageAtlasUV.zw, (imageCoord + 1.0) * 0.5);
                vec4 imageColor = texture(imageAtlasTexture, atlasUV);
                finalImageColor = applyGreyoutToImage(imageColor, isGreyedOut);
            }
        } else {
            // Image is same size or larger than overall size, no scaling needed
            // Sample from texture atlas
            vec2 atlasUV = mix(imageAtlasUV.xy, imageAtlasUV.zw, (imageCoord + 1.0) * 0.5);
            vec4 imageColor = texture(imageAtlasTexture, atlasUV);
            finalImageColor = applyGreyoutToImage(imageColor, isGreyedOut);
        }
    }

    coverage = max(coverage, finalImageColor.a);

    float finalPointAlpha = max(finalShapeColor.a, finalImageColor.a);
    if (isGreyedOut > 0.0 && greyoutOpacity != -1.0) {
        finalPointAlpha *= greyoutOpacity;
    } else {
        finalPointAlpha *= pointOpacity;
    }

    // Blend image color above point color
    fragColor = vec4(
        mix(finalShapeColor.rgb, finalImageColor.rgb, finalImageColor.a),
        finalPointAlpha
    );

    // Render outline ring around the point
    if (isOutlined > 0.0) {
        float r = length(pointCoord);
        const float ringSmoothing = 1.025;
        float rSafe = max(r, 1e-6);
        float wSafe = max(outlineWidth, 1e-6);
        float outerEdge = smoothstep(rSafe, rSafe * ringSmoothing, 1.0);
        float innerEdge = smoothstep(wSafe, wSafe * ringSmoothing, r);
        float ringAlpha = outerEdge * innerEdge;
        coverage = max(coverage, ringAlpha);

        // Grey out the ring color when the point is greyed
        vec3 ringColor = outlineColor.rgb;
        if (isGreyedOut > 0.0) {
            float blendFactor = 0.65;
            if (isDarkenGreyout > 0.0) {
                ringColor = mix(ringColor, vec3(0.2), blendFactor);
            } else {
                ringColor = mix(ringColor, max(backgroundColor.rgb, vec3(0.8)), blendFactor);
            }
        }

        float ringOpacity = ringAlpha * outlineColor.a;
        // Composite ring on top of existing fragment
        fragColor = vec4(
            mix(fragColor.rgb, ringColor, ringOpacity),
            max(fragColor.a, ringOpacity)
        );
    }

    #ifdef SPACE_3D
    // Impostor sphere shading: light circle sprites as spheres (soft headlight
    // from the upper left) so overlapping points read as separate volumes.
    // gl_PointCoord's y is screen-down, so it's negated for the normal's up.
    if (sphereShading > 0.5 && pointShape < 0.5) {
        float r2 = dot(pointCoord, pointCoord);
        vec3 sphereNormal = normalize(vec3(pointCoord.x, -pointCoord.y, sqrt(max(1.0 - r2, 0.0))));
        const vec3 lightDirection = vec3(-0.324443, 0.486664, 0.811107); // normalize(vec3(-0.4, 0.6, 1.0))
        float diffuse = 0.72 + 0.28 * max(dot(sphereNormal, lightDirection), 0.0);
        fragColor.rgb *= diffuse;
    }

    // Depth cueing: recede distant points toward the background (strength and
    // range computed per point in the vertex shader).
    fragColor.rgb = mix(fragColor.rgb, backgroundColor.rgb, depthFadeVarying);

    // Depth writes are enabled in 3D: the transparent corners of the point sprite
    // must not write depth, or they would punch invisible holes into points behind.
    // Test geometric coverage, not final alpha \u2014 pointOpacity/greyoutOpacity and the
    // point color's alpha apply uniformly across the sprite and must not make
    // low-opacity points disappear entirely.
    if (coverage < 0.33) {
        discard;
    }
    #endif

    // Occlusion culling (2D only; renderMode stays 0 in 3D): split every fragment
    // between the opaque core pass (depth-writing, unblended) and the blended
    // fringe pass. The same final-alpha rule runs in both passes so each fragment
    // renders exactly once.
    if (renderMode > 1.5) {
        if (fragColor.a >= OPAQUE_ALPHA_THRESHOLD) discard; // already drawn by core pass
    } else if (renderMode > 0.5) {
        if (fragColor.a < OPAQUE_ALPHA_THRESHOLD) discard;  // left for fringe pass
    }
}
`,$e=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec2 pointIndices;
in float sourceSize;
in float targetSize;
in vec4 sourceColor;
in vec4 targetColor;
in float shape;
in float imageIndex;
in float imageSize;

uniform sampler2D positionsTexture;
uniform sampler2D pointStatus;
uniform sampler2D exitTexture;
uniform sampler2D imageAtlasCoords;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform drawVertexUniforms {
  float ratio;
  mat4 transformationMatrix;
  float pointsTextureSize;
  float sizeScale;
  float spaceSize;
  vec2 screenSize;
  vec4 greyoutColor;
  vec4 backgroundColor;
  float scalePointsOnZoom;
  float maxPointSize;
  float isDarkenGreyout;
  float skipHighlighted;
  float skipGreyed;
  float hasImages;
  float imageCount;
  float imageAtlasCoordsTextureSize;
  float transitionProgress;
  float animateColors;
  float animateSizes;
  float pointsNumber;
  float pointDepthFade;
  float depthFadeNear;
  float depthFadeFar;
  float animatePositions;
  vec4 pointDefaultColor;
  float pointDefaultSize;
} drawVertex;

#define ratio drawVertex.ratio
#define transformationMatrix drawVertex.transformationMatrix
#define pointsTextureSize drawVertex.pointsTextureSize
#define sizeScale drawVertex.sizeScale
#define spaceSize drawVertex.spaceSize
#define screenSize drawVertex.screenSize
#define greyoutColor drawVertex.greyoutColor
#define backgroundColor drawVertex.backgroundColor
#define scalePointsOnZoom drawVertex.scalePointsOnZoom
#define maxPointSize drawVertex.maxPointSize
#define isDarkenGreyout drawVertex.isDarkenGreyout
#define skipHighlighted drawVertex.skipHighlighted
#define skipGreyed drawVertex.skipGreyed
#define hasImages drawVertex.hasImages
#define imageCount drawVertex.imageCount
#define imageAtlasCoordsTextureSize drawVertex.imageAtlasCoordsTextureSize
#define transitionProgress drawVertex.transitionProgress
#define animateColors drawVertex.animateColors
#define animateSizes drawVertex.animateSizes
#define pointsNumber drawVertex.pointsNumber
#define pointDepthFade drawVertex.pointDepthFade
#define depthFadeNear drawVertex.depthFadeNear
#define depthFadeFar drawVertex.depthFadeFar
#define animatePositions drawVertex.animatePositions
#define pointDefaultColor drawVertex.pointDefaultColor
#define pointDefaultSize drawVertex.pointDefaultSize
#else
uniform float ratio;
uniform mat3 transformationMatrix;
uniform float pointsTextureSize;
uniform float sizeScale;
uniform float spaceSize;
uniform vec2 screenSize;
uniform vec4 greyoutColor;
uniform vec4 backgroundColor;
uniform float scalePointsOnZoom;
uniform float maxPointSize;
uniform float isDarkenGreyout;
uniform float skipHighlighted;
uniform float skipGreyed;
uniform float hasImages;
uniform float imageCount;
uniform float imageAtlasCoordsTextureSize;
uniform float transitionProgress;
uniform float animateColors;
uniform float animateSizes;
uniform float pointsNumber;
uniform float pointDepthFade;
uniform float depthFadeNear;
uniform float depthFadeFar;
uniform float animatePositions;
uniform vec4 pointDefaultColor;
uniform float pointDefaultSize;
#endif

out float pointShape;
out float isGreyedOut;
out float isOutlined;
out vec4 shapeColor;
out vec4 imageAtlasUV;
out float shapeSize;
out float imageSizeVarying;
out float overallSize;
out float depthFadeVarying;

// \`pxPerUnit\` is the zoom factor: \`transformationMatrix[0][0]\` in 2D,
// perspective-attenuated \`pxPerSpaceUnit(...)\` in 3D. This function is duplicated in
// find-hovered-point.vert and must stay identical there, or hover misses points.
float calculatePointSize(float size, float pxPerUnit) {
  float pSize;

  if (scalePointsOnZoom > 0.0) {
    pSize = size * ratio * pxPerUnit;
  } else {
    pSize = size * ratio * min(5.0, max(1.0, pxPerUnit * 0.01));
  }

  return min(pSize, maxPointSize * ratio);
}

const float outlineRingScale = 1.3;

// Read-time resolution of NaN channels \u2014 input arrays are used verbatim and never
// edited, so "use the default" stays encoded as NaN all the way to the GPU. A NaN
// resolves to the config default blended toward the exit default along the animated
// exit ramp (0 = present, 1 = gone), so the enter/exit fade of default-valued
// channels drives itself \u2014 no size/color transition needed for a removal. Explicit
// (real) values pass through. EXIT_DEFAULT_* are #defines injected from variables.ts,
// shared with the CPU resolvers (GraphData.getResolvedPoint*).
float resolveSize(float size, float exitRamp) {
  if (!isnan(size)) return size;
  return mix(pointDefaultSize, EXIT_DEFAULT_SIZE, exitRamp);
}

vec4 resolveColor(vec4 color, float exitRamp) {
  vec4 defaultColor = mix(pointDefaultColor, vec4(EXIT_DEFAULT_COLOR_CHANNEL), exitRamp);
  return mix(color, defaultColor, isnan(color));
}

void main() {
  // Read point status texture: R = greyout, G = outlined
  vec4 status = texture(pointStatus, (pointIndices + 0.5) / pointsTextureSize);
  isGreyedOut = status.r;
  isOutlined = status.g;
  float isHighlighted = (status.r == 0.0) ? 1.0 : 0.0;

  // Discard point based on rendering mode
  if (skipHighlighted > 0.0 && isHighlighted > 0.0) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }
  if (skipGreyed > 0.0 && isHighlighted <= 0.0) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  // Exit texture: R = previous absence, G = current absence (1 = absent). During a
  // position transition, blend R\u2192G to animate the enter/exit; otherwise use G (the
  // settled current absence) so an unrelated color/size transition can't replay the
  // ramp. The caller drives the visual fade via setPointSizes/setPointColors; here
  // we only remove the point once it is fully gone.
  vec4 exitStatus = texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize);
  float exit = animatePositions > 0.0
    ? mix(exitStatus.r, exitStatus.g, transitionProgress)
    : exitStatus.g;
  if (exit >= 1.0) {
    // Fully gone \u2014 skip. Also avoids using a NaN position on the snapped path.
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  // Position
  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);

  #ifdef SPACE_3D
  // 3D mode: transformationMatrix carries the camera's view-projection matrix.
  // World position (z stored in the texture's alpha channel) maps straight to
  // clip space; the GPU performs the perspective divide.
  vec4 clip = transformationMatrix * vec4(pointPosition.rg, pointPosition.a, 1.0);
  if (clip.w <= 0.0) {
    // Behind the camera \u2014 cull, or the perspective divide would mirror the position.
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }
  gl_Position = clip;
  // Depth cueing: 0 at the near edge of the scene sphere, up to \`pointDepthFade\`
  // at the far edge. clip.w is the eye-space distance under a perspective
  // projection; the range is the camera distance \xB1 the fitted scene radius.
  depthFadeVarying = pointDepthFade * smoothstep(depthFadeNear, depthFadeFar, clip.w);
  float pxPerUnit = pxPerSpaceUnit(transformationMatrix, screenSize, clip.w);
  #else
  vec2 point = pointPosition.rg;

  // Transform point position to normalized device coordinates
  // Convert from space coordinates [0, spaceSize] to normalized [-1, 1]
  vec2 normalizedPosition = 2.0 * point / spaceSize - 1.0;

  // Apply aspect ratio correction - this is needed to map the square space to the rectangular screen
  // The transformation matrix handles zoom/pan, but we need this to handle aspect ratio
  normalizedPosition *= spaceSize / screenSize;

  #ifdef USE_UNIFORM_BUFFERS
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 finalPosition = transformMat3 * vec3(normalizedPosition, 1);
  #else
  vec3 finalPosition = transformationMatrix * vec3(normalizedPosition, 1);
  #endif
  // Depth encodes stacking order (2D only \u2014 the 3D branch above outputs real
  // perspective depth): higher point index = drawn on top = nearer (smaller z).
  // Harmless when depth testing is off (depthCompare 'always'); used by the
  // occlusion-culling core/fringe passes.
  float linearIndex = pointIndices.y * pointsTextureSize + pointIndices.x;
  float depthZ = 1.0 - 2.0 * (linearIndex + 0.5) / max(pointsNumber, 1.0);
  gl_Position = vec4(finalPosition.rg, depthZ, 1.0);
  depthFadeVarying = 0.0;
  float pxPerUnit = transformationMatrix[0][0];
  #endif

  // Resolve NaN channels against the animated exit ramp before mixing \u2014 default
  // sizes/colors of an entering or leaving point fade with the ramp regardless of
  // whether a size/color transition is active.
  float pointSize = animateSizes > 0.0
    ? mix(resolveSize(sourceSize, exit), resolveSize(targetSize, exit), transitionProgress)
    : resolveSize(targetSize, exit);
  vec4 pointColor = animateColors > 0.0
    ? mix(resolveColor(sourceColor, exit), resolveColor(targetColor, exit), transitionProgress)
    : resolveColor(targetColor, exit);

  // Calculate sizes for shape and image
  float shapeSizeValue = calculatePointSize(pointSize * sizeScale, pxPerUnit);
  float imageSizeValue = calculatePointSize(imageSize * sizeScale, pxPerUnit);

  // Use the larger of the two sizes for the overall point size
  float overallSizeValue = max(shapeSizeValue, imageSizeValue);

  // Scale up point sprite to fit outline ring; clamp to hardware gl_PointSize limit so the
  // sprite never gets silently clipped \u2014 the point body is unaffected, only the ring narrows.
  if (isOutlined > 0.0) {
    overallSizeValue *= outlineRingScale;
    overallSizeValue = min(overallSizeValue, maxPointSize * ratio);
  }

  gl_PointSize = overallSizeValue;

  // Pass size information to fragment shader
  shapeSize = shapeSizeValue;
  imageSizeVarying = imageSizeValue;
  overallSize = overallSizeValue;

  shapeColor = pointColor;
  pointShape = shape;

  // Adjust color of greyed-out points
  if (isGreyedOut > 0.0) {
    if (greyoutColor[0] != -1.0) {
      shapeColor = greyoutColor;
    } else {
      // If greyoutColor is not set, make color lighter or darker based on isDarkenGreyout
      float blendFactor = 0.65;

      #ifdef USE_UNIFORM_BUFFERS
      if (isDarkenGreyout > 0.0) {
        shapeColor.rgb = mix(shapeColor.rgb, vec3(0.2), blendFactor);
      } else {
        shapeColor.rgb = mix(shapeColor.rgb, max(backgroundColor.rgb, vec3(0.8)), blendFactor);
      }
      #else
      if (isDarkenGreyout > 0.0) {
        shapeColor.rgb = mix(shapeColor.rgb, vec3(0.2), blendFactor);
      } else {
        shapeColor.rgb = mix(shapeColor.rgb, max(backgroundColor.rgb, vec3(0.8)), blendFactor);
      }
      #endif
    }
  }

  #ifdef USE_UNIFORM_BUFFERS
  if (hasImages <= 0.0 || imageIndex < 0.0 || imageIndex >= imageCount) {
    imageAtlasUV = vec4(-1.0);
  } else {
    float atlasCoordIndex = imageIndex;
    float texX = mod(atlasCoordIndex, imageAtlasCoordsTextureSize);
    float texY = floor(atlasCoordIndex / imageAtlasCoordsTextureSize);
    vec2 atlasCoordTexCoord = (vec2(texX, texY) + 0.5) / imageAtlasCoordsTextureSize;
    vec4 atlasCoords = texture(imageAtlasCoords, atlasCoordTexCoord);
    imageAtlasUV = atlasCoords;
  }
  #else
  if (hasImages <= 0.0 || imageIndex < 0.0 || imageIndex >= imageCount) {
    imageAtlasUV = vec4(-1.0);
  } else {
    float atlasCoordIndex = imageIndex;
    float texX = mod(atlasCoordIndex, imageAtlasCoordsTextureSize);
    float texY = floor(atlasCoordIndex / imageAtlasCoordsTextureSize);
    vec2 atlasCoordTexCoord = (vec2(texX, texY) + 0.5) / imageAtlasCoordsTextureSize;
    vec4 atlasCoords = texture(imageAtlasCoords, atlasCoordTexCoord);
    imageAtlasUV = atlasCoords;
  }
  #endif
}
`,Pi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;
uniform sampler2D pointSize;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform findPointsInRectUniforms {
  float sizeScale;
  float spaceSize;
  vec2 screenSize;
  float ratio;
  mat4 transformationMatrix;
  vec2 rect0;
  vec2 rect1;
  float scalePointsOnZoom;
  float maxPointSize;
} findPointsInRect;

#define sizeScale findPointsInRect.sizeScale
#define spaceSize findPointsInRect.spaceSize
#define screenSize findPointsInRect.screenSize
#define ratio findPointsInRect.ratio
#define transformationMatrix findPointsInRect.transformationMatrix
#define rect0 findPointsInRect.rect0
#define rect1 findPointsInRect.rect1
#define scalePointsOnZoom findPointsInRect.scalePointsOnZoom
#define maxPointSize findPointsInRect.maxPointSize
#else
uniform float sizeScale;
uniform float spaceSize;
uniform vec2 screenSize;
uniform float ratio;
uniform mat3 transformationMatrix;
uniform vec2 rect0;
uniform vec2 rect1;
uniform float scalePointsOnZoom;
uniform float maxPointSize;
#endif

in vec2 textureCoords;

out vec4 fragColor;

float pointSizeF(float size) {
  float pSize;
  // Extract top-left element from mat4 (or use mat3 conversion)
  #ifdef USE_UNIFORM_BUFFERS
  float scale = transformationMatrix[0][0]; // mat4 first element
  #else
  float scale = transformationMatrix[0][0]; // mat3 first element
  #endif
  if (scalePointsOnZoom > 0.0) { 
    pSize = size * ratio * scale;
  } else {
    pSize = size * ratio * min(5.0, max(1.0, scale * 0.01));
  }
  return min(pSize, maxPointSize * ratio);
}

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  // Texels beyond the point count carry index -1 \u2014 they are not points.
  if (pointPosition.b < 0.0) {
    fragColor = vec4(0.0);
    return;
  }
  // Skip absent (faded-out) points \u2014 never select a removed point. exit.G = absent.
  if (texture(exitTexture, textureCoords).g > 0.5) {
    fragColor = vec4(0.0);
    return;
  }
  vec2 p = 2.0 * pointPosition.rg / spaceSize - 1.0;
  p *= spaceSize / screenSize;
  #ifdef USE_UNIFORM_BUFFERS
  // Convert mat4 to mat3 for vec3 multiplication
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 final = transformMat3 * vec3(p, 1);
  #else
  vec3 final = transformationMatrix * vec3(p, 1);
  #endif

  vec4 pSize = texture(pointSize, textureCoords);
  float size = pSize.r * sizeScale;

  float left = 2.0 * (rect0.x - 0.5 * pointSizeF(size)) / screenSize.x - 1.0;
  float right = 2.0 * (rect1.x + 0.5 * pointSizeF(size)) / screenSize.x - 1.0;
  float top =  2.0 * (rect0.y - 0.5 * pointSizeF(size)) / screenSize.y - 1.0;
  float bottom =  2.0 * (rect1.y + 0.5 * pointSizeF(size)) / screenSize.y - 1.0;

  fragColor = vec4(0.0, 0.0, pointPosition.r, pointPosition.g);
  if (final.x >= left && final.x <= right && final.y >= top && final.y <= bottom) {
    fragColor.r = 1.0;
  }
}

`,yi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;
uniform sampler2D polygonPathTexture; // Texture containing polygon path points
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform findPointsInPolygonUniforms {
  float spaceSize;
  vec2 screenSize;
  mat4 transformationMatrix;
  float polygonPathLength;
} findPointsInPolygon;

#define spaceSize findPointsInPolygon.spaceSize
#define screenSize findPointsInPolygon.screenSize
#define transformationMatrix findPointsInPolygon.transformationMatrix
#define polygonPathLength int(findPointsInPolygon.polygonPathLength)
#else
uniform int polygonPathLength;
uniform float spaceSize;
uniform vec2 screenSize;
uniform mat3 transformationMatrix;
#endif

in vec2 textureCoords;

out vec4 fragColor;

// Get a point from the polygon path texture at a specific index
vec2 getPolygonPoint(sampler2D pathTexture, int index, int pathLength) {
  if (index >= pathLength) return vec2(0.0);
  
  // Calculate texture coordinates for the index
  int textureSize = int(ceil(sqrt(float(pathLength))));
  int x = index - (index / textureSize) * textureSize;
  int y = index / textureSize;
  
  vec2 texCoord = (vec2(float(x), float(y)) + 0.5) / float(textureSize);
  vec4 pathData = texture(pathTexture, texCoord);
  
  return pathData.xy;
}

// Point-in-polygon algorithm using ray casting
bool pointInPolygon(vec2 point, sampler2D pathTexture, int pathLength) {
  bool inside = false;
  
  for (int i = 0; i < 2048; i++) {
    if (i >= pathLength) break;
    
    int j = int(mod(float(i + 1), float(pathLength)));
    
    vec2 pi = getPolygonPoint(pathTexture, i, pathLength);
    vec2 pj = getPolygonPoint(pathTexture, j, pathLength);
    
    if (((pi.y > point.y) != (pj.y > point.y)) &&
        (point.x < (pj.x - pi.x) * (point.y - pi.y) / (pj.y - pi.y) + pi.x)) {
      inside = !inside;
    }
  }
  
  return inside;
}

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  // Texels beyond the point count carry index -1 \u2014 they are not points.
  if (pointPosition.b < 0.0) {
    fragColor = vec4(0.0);
    return;
  }
  // Skip absent (faded-out) points \u2014 never select a removed point. exit.G = absent.
  if (texture(exitTexture, textureCoords).g > 0.5) {
    fragColor = vec4(0.0);
    return;
  }
  vec2 p = 2.0 * pointPosition.rg / spaceSize - 1.0;
  p *= spaceSize / screenSize;
  #ifdef USE_UNIFORM_BUFFERS
  // Convert mat4 to mat3 for vec3 multiplication
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 final = transformMat3 * vec3(p, 1);
  #else
  vec3 final = transformationMatrix * vec3(p, 1);
  #endif

  // Convert to screen coordinates for polygon check
  vec2 screenPos = (final.xy + 1.0) * screenSize / 2.0;
  
  fragColor = vec4(0.0, 0.0, pointPosition.r, pointPosition.g);
  
  // Check if point center is inside the polygon
  if (pointInPolygon(screenPos, polygonPathTexture, polygonPathLength)) {
    fragColor.r = 1.0;
  }
} `,Ci=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform drawHighlightedUniforms {
  float size;
  mat4 transformationMatrix;
  float pointsTextureSize;
  float sizeScale;
  float spaceSize;
  vec2 screenSize;
  float scalePointsOnZoom;
  float pointIndex;
  float maxPointSize;
  vec4 color;
  float universalPointOpacity;
  float greyoutOpacity;
  float isDarkenGreyout;
  vec4 backgroundColor;
  vec4 greyoutColor;
  float width;
} drawHighlighted;

#define width drawHighlighted.width
#else
uniform float width;
#endif

in vec2 vertexPosition;
in float pointOpacity;
in vec3 rgbColor;

out vec4 fragColor;

const float smoothing = 1.05;

void main () {
  float r = dot(vertexPosition, vertexPosition);
  float opacity = smoothstep(r, r * smoothing, 1.0);
  float stroke = smoothstep(width, width * smoothing, r);
  fragColor = vec4(rgbColor, opacity * stroke * pointOpacity);
}`,bi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec2 vertexCoord;

uniform sampler2D positionsTexture;
uniform sampler2D pointStatus;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform drawHighlightedUniforms {
  float size;
  mat4 transformationMatrix;
  float pointsTextureSize;
  float sizeScale;
  float spaceSize;
  vec2 screenSize;
  float scalePointsOnZoom;
  float pointIndex;
  float maxPointSize;
  vec4 color;
  float universalPointOpacity;
  float greyoutOpacity;
  float isDarkenGreyout;
  vec4 backgroundColor;
  vec4 greyoutColor;
  float width;
} drawHighlighted;

#define size drawHighlighted.size
#define transformationMatrix drawHighlighted.transformationMatrix
#define pointsTextureSize drawHighlighted.pointsTextureSize
#define sizeScale drawHighlighted.sizeScale
#define spaceSize drawHighlighted.spaceSize
#define screenSize drawHighlighted.screenSize
#define scalePointsOnZoom drawHighlighted.scalePointsOnZoom
#define pointIndex drawHighlighted.pointIndex
#define maxPointSize drawHighlighted.maxPointSize
#define color drawHighlighted.color
#define universalPointOpacity drawHighlighted.universalPointOpacity
#define greyoutOpacity drawHighlighted.greyoutOpacity
#define isDarkenGreyout drawHighlighted.isDarkenGreyout
#define backgroundColor drawHighlighted.backgroundColor
#define greyoutColor drawHighlighted.greyoutColor
#else
uniform float size;
uniform mat3 transformationMatrix;
uniform float pointsTextureSize;
uniform float sizeScale;
uniform float spaceSize;
uniform vec2 screenSize;
uniform float scalePointsOnZoom;
uniform float pointIndex;
uniform float maxPointSize;
uniform vec4 color;
uniform float universalPointOpacity;
uniform float greyoutOpacity;
uniform float isDarkenGreyout;
uniform vec4 backgroundColor;
uniform vec4 greyoutColor;
uniform float width;
#endif
out vec2 vertexPosition;
out float pointOpacity;
out vec3 rgbColor;

// \`pxPerUnit\` is the zoom factor: \`transformationMatrix[0][0]\` in 2D,
// perspective-attenuated \`pxPerSpaceUnit(...)\` in 3D. Mirrors draw-points.vert
// (without the \`ratio\` factor \u2014 this shader works in CSS pixels).
float calculatePointSize(float pointSize, float pxPerUnit) {
  float pSize;

  if (scalePointsOnZoom > 0.0) {
    pSize = pointSize * pxPerUnit;
  } else {
    pSize = pointSize * min(5.0, max(1.0, pxPerUnit * 0.01));
  }

  return min(pSize, maxPointSize);
}

const float relativeRingRadius = 1.3;

void main () {
  vertexPosition = vertexCoord;

  vec2 textureCoordinates = vec2(mod(pointIndex, pointsTextureSize), floor(pointIndex / pointsTextureSize)) + 0.5;

  // Don't draw a highlight/outline for an absent (faded-out) point. exit.G = absent.
  if (texture(exitTexture, textureCoordinates / pointsTextureSize).g > 0.5) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    return;
  }

  vec4 pointPosition = texture(positionsTexture, textureCoordinates / pointsTextureSize);

  rgbColor = color.rgb;
  pointOpacity = color.a * universalPointOpacity;
  vec4 greyoutStatus = texture(pointStatus, textureCoordinates / pointsTextureSize);
  if (greyoutStatus.r > 0.0) {
    if (greyoutColor[0] != -1.0) {
      rgbColor = greyoutColor.rgb;
      pointOpacity = greyoutColor.a;
    } else {
      // If greyoutColor is not set, make color lighter or darker based on isDarkenGreyout
      float blendFactor = 0.65; // Controls how much to modify (0.0 = original, 1.0 = target color)
      
      #ifdef USE_UNIFORM_BUFFERS
      if (isDarkenGreyout > 0.0) {
        // Darken the color
        rgbColor = mix(rgbColor, vec3(0.2), blendFactor);
      } else {
        // Lighten the color
        rgbColor = mix(rgbColor, max(backgroundColor.rgb, vec3(0.8)), blendFactor);
      }
      #else
      if (isDarkenGreyout > 0.0) {
        // Darken the color
        rgbColor = mix(rgbColor, vec3(0.2), blendFactor);
      } else {
        // Lighten the color
        rgbColor = mix(rgbColor, max(backgroundColor.rgb, vec3(0.8)), blendFactor);
      }
      #endif
    }

    if (greyoutOpacity != -1.0) {
      pointOpacity *= greyoutOpacity;
    }
  }

  #ifdef SPACE_3D
  // 3D mode: project the point center with the view-projection matrix and
  // billboard the ring quad in screen space (pre-multiplied by w so the offset
  // survives the perspective divide).
  vec4 clip = transformationMatrix * vec4(pointPosition.rg, pointPosition.a, 1.0);
  if (clip.w <= 0.0) {
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    return;
  }
  float pxPerUnit = pxPerSpaceUnit(transformationMatrix, screenSize, clip.w);
  float radiusPx = calculatePointSize(size * sizeScale, pxPerUnit) * relativeRingRadius * 0.5;
  clip.xy += vertexCoord * radiusPx * (2.0 / screenSize) * clip.w;
  gl_Position = clip;
  #else
  // Calculate point radius
  float pointSize = (calculatePointSize(size * sizeScale, transformationMatrix[0][0]) * relativeRingRadius) / transformationMatrix[0][0];
  float radius = pointSize * 0.5;

  // Calculate point position in screen space
  vec2 a = pointPosition.xy;
  vec2 b = pointPosition.xy + vec2(0.0, radius);
  vec2 xBasis = b - a;
  vec2 yBasis = normalize(vec2(-xBasis.y, xBasis.x));
  vec2 pointPositionInScreenSpace = a + xBasis * vertexCoord.x + yBasis * radius * vertexCoord.y;

  // Transform point position to normalized device coordinates
  vec2 p = 2.0 * pointPositionInScreenSpace / spaceSize - 1.0;
  p *= spaceSize / screenSize;
  #ifdef USE_UNIFORM_BUFFERS
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 final = transformMat3 * vec3(p, 1);
  #else
  vec3 final = transformationMatrix * vec3(p, 1);
  #endif

  gl_Position = vec4(final.rg, 0, 1);
  #endif
}`,Ti=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec4 rgba;

out vec4 fragColor;

void main() {
  // Circular sprite: hover is radius-based, like the rendered point shape.
  vec2 fromCenter = 2.0 * gl_PointCoord - 1.0;
  if (dot(fromCenter, fromCenter) > 1.0) discard;
  fragColor = rgba;
}
`,ki=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

// Fills the screen-space picking buffer: every point rasterizes its sprite at
// its projected screen position, carrying [index, x, y, z] to the fragment
// shader. Hover detection then only reads a small window of this buffer under
// the cursor \u2014 it never has to touch the point set again until the scene
// changes (see Points.updatePickingBuffer / Graph.findHoveredItem).
//
// In 3D candidates depth-test against each other so the nearest point wins;
// the two-pass highlight priority mirrors find-hovered semantics: the
// highlighted pass gets the nearer half of the depth range, so it beats the
// greyed pass, matching the two-pass draw order in 2D (greyed first).

in vec2 pointIndices;
in float size;
in float imageSize;

uniform sampler2D positionsTexture;
uniform sampler2D pointStatus;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform fillPickingBufferUniforms {
  float pointsTextureSize;
  float sizeScale;
  float spaceSize;
  vec2 screenSize;
  float ratio;
  float pickingPixelRatio;
  mat4 transformationMatrix;
  float scalePointsOnZoom;
  float maxPointSize;
  float skipHighlighted;
  float skipGreyed;
  float pointDefaultSize;
} fillPickingBuffer;

#define pointsTextureSize fillPickingBuffer.pointsTextureSize
#define sizeScale fillPickingBuffer.sizeScale
#define spaceSize fillPickingBuffer.spaceSize
#define screenSize fillPickingBuffer.screenSize
#define ratio fillPickingBuffer.ratio
#define pickingPixelRatio fillPickingBuffer.pickingPixelRatio
#define transformationMatrix fillPickingBuffer.transformationMatrix
#define scalePointsOnZoom fillPickingBuffer.scalePointsOnZoom
#define maxPointSize fillPickingBuffer.maxPointSize
#define skipHighlighted fillPickingBuffer.skipHighlighted
#define skipGreyed fillPickingBuffer.skipGreyed
#define pointDefaultSize fillPickingBuffer.pointDefaultSize
#else
uniform float pointsTextureSize;
uniform float sizeScale;
uniform float spaceSize;
uniform vec2 screenSize;
uniform float ratio;
uniform float pickingPixelRatio;
uniform mat3 transformationMatrix;
uniform float scalePointsOnZoom;
uniform float maxPointSize;
uniform float skipHighlighted;
uniform float skipGreyed;
uniform float pointDefaultSize;
#endif

out vec4 rgba;

// Keep tiny points pickable: below this sprite footprint (in picking-buffer
// pixels) a point could fall between the buffer's texels.
const float minPickingSize = 2.0;

// Must stay identical to calculatePointSize in draw-points.vert (same \`pxPerUnit\`
// semantics), or the picking radius drifts from the rendered point size.
float calculatePointSize(float size, float pxPerUnit) {
  float pSize;

  if (scalePointsOnZoom > 0.0) {
    pSize = size * ratio * pxPerUnit;
  } else {
    pSize = size * ratio * min(5.0, max(1.0, pxPerUnit * 0.01));
  }

  return min(pSize, maxPointSize * ratio);
}

void main() {
  // Fully clipped: a skipped point must not rasterize anywhere in the buffer.
  rgba = vec4(-1.0);
  gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
  gl_PointSize = 1.0;

  // Skip absent (faded-out) points so picking never lands on a removed one. Their
  // size/position may still look hittable mid-fade (only alpha faded), so the exit
  // status is the reliable signal. exit.G = current absence.
  if (texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize).g > 0.5) return;

  vec4 greyoutStatus = texture(pointStatus, (pointIndices + 0.5) / pointsTextureSize);
  float isHighlighted = (greyoutStatus.r == 0.0) ? 1.0 : 0.0;

  if (skipHighlighted > 0.0 && isHighlighted > 0.0) return;
  if (skipGreyed > 0.0 && isHighlighted <= 0.0) return;

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);

  #ifdef SPACE_3D
  // 3D mode: same projection as draw-points.vert (z in the texture's alpha channel).
  vec4 clip = transformationMatrix * vec4(pointPosition.rg, pointPosition.a, 1.0);
  if (clip.w <= 0.0) return; // behind the camera \u2014 never a pick candidate
  float pxPerUnit = pxPerSpaceUnit(transformationMatrix, screenSize, clip.w);
  vec2 ndc = clip.xy / clip.w;
  #else
  vec2 point = pointPosition.rg;

  vec2 normalizedPosition = 2.0 * point / spaceSize - 1.0;
  normalizedPosition *= spaceSize / screenSize;

  #ifdef USE_UNIFORM_BUFFERS
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 finalPosition = transformMat3 * vec3(normalizedPosition, 1);
  #else
  vec3 finalPosition = transformationMatrix * vec3(normalizedPosition, 1);
  #endif
  float pxPerUnit = transformationMatrix[0][0];
  vec2 ndc = finalPosition.xy;
  #endif

  // Resolve a NaN size at read time. The absent-point guard above already returned,
  // so a NaN here means "use the config default".
  float resolvedSize = isnan(size) ? pointDefaultSize : size;

  float shapeSizeValue = calculatePointSize(resolvedSize * sizeScale, pxPerUnit);
  float imageSizeValue = calculatePointSize(imageSize * sizeScale, pxPerUnit);
  // Device px \u2192 CSS px \u2192 picking-buffer px (the buffer is smaller than the screen)
  float spriteSize = max(shapeSizeValue, imageSizeValue) / ratio * pickingPixelRatio;

  float index = pointIndices.g * pointsTextureSize + pointIndices.r;
  rgba = vec4(index, pointPosition.rg, pointPosition.a);
  gl_PointSize = max(spriteSize, minPickingSize);

  #ifdef SPACE_3D
  // Nearest-wins: candidates depth-test against each other. The highlighted
  // pass (skipGreyed == 1) gets the nearer half of the depth range so it keeps
  // priority over the greyed pass, matching the 2D two-pass order.
  float depth01 = clamp(clip.z / clip.w * 0.5 + 0.5, 0.0, 1.0);
  float priority = (skipHighlighted > 0.0) ? 0.5 : 0.0;
  gl_Position = vec4(ndc, (priority + 0.5 * depth01) * 2.0 - 1.0, 1.0);
  #else
  // 2D: later points overwrite earlier ones (depth test off), matching draw order.
  gl_Position = vec4(ndc, 0.0, 1.0);
  #endif
}
`,zi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec4 rgba;

out vec4 fragColor;

void main() {
  fragColor = rgba;
}`,wi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

in vec2 pointIndices;

uniform sampler2D positionsTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform fillSampledPointsUniforms {
  float pointsTextureSize;
  mat4 transformationMatrix;
  float spaceSize;
  vec2 screenSize;
} fillSampledPoints;

#define pointsTextureSize fillSampledPoints.pointsTextureSize
#define transformationMatrix fillSampledPoints.transformationMatrix
#define spaceSize fillSampledPoints.spaceSize
#define screenSize fillSampledPoints.screenSize
#else
uniform float pointsTextureSize;
uniform float spaceSize;
uniform vec2 screenSize;
uniform mat3 transformationMatrix;
#endif

out vec4 rgba;

void main() {
  // Keep absent (faded-out) points out of the sample. exit.G = current absence.
  if (texture(exitTexture, (pointIndices + 0.5) / pointsTextureSize).g > 0.5) {
    rgba = vec4(0.0);
    gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
    gl_PointSize = 0.0;
    return;
  }

  vec4 pointPosition = texture(positionsTexture, (pointIndices + 0.5) / pointsTextureSize);
  float index = pointIndices.g * pointsTextureSize + pointIndices.r;

  #ifdef SPACE_3D
  // 3D mode: project with the camera's view-projection matrix (z in the texture's
  // alpha channel). The second channel carries z instead of the constant validity
  // flag \u2014 validity is index >= 0 (the pass clears the FBO to -1).
  vec4 clip = transformationMatrix * vec4(pointPosition.rg, pointPosition.a, 1.0);
  if (clip.w <= 0.0) {
    // Behind the camera \u2014 keep the vertex off the sampling grid.
    rgba = vec4(-1.0);
    gl_Position = vec4(2.0, 2.0, 0.0, 1.0);
    gl_PointSize = 1.0;
    return;
  }
  vec2 pointScreenPosition = (clip.xy / clip.w + 1.0) * screenSize / 2.0;
  rgba = vec4(index, pointPosition.a, pointPosition.xy);
  #else
  vec2 p = 2.0 * pointPosition.rg / spaceSize - 1.0;
  p *= spaceSize / screenSize;
  #ifdef USE_UNIFORM_BUFFERS
  // Convert mat4 to mat3 for vec3 multiplication
  mat3 transformMat3 = mat3(transformationMatrix);
  vec3 final = transformMat3 * vec3(p, 1);
  #else
  vec3 final = transformationMatrix * vec3(p, 1);
  #endif

  vec2 pointScreenPosition = (final.xy + 1.0) * screenSize / 2.0;
  rgba = vec4(index, 1.0, pointPosition.xy);
  #endif

  float i = (pointScreenPosition.x + 0.5) / screenSize.x;
  float j = (pointScreenPosition.y + 0.5) / screenSize.y;
  gl_Position = vec4(2.0 * vec2(i, j) - 1.0, 0.0, 1.0);

  gl_PointSize = 1.0;
}`,Di=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;
uniform sampler2D velocity;
uniform sampler2D pinnedStatusTexture;
uniform sampler2D exitTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform updatePositionUniforms {
  float friction;
  float spaceSize;
} updatePosition;

#define friction updatePosition.friction
#define spaceSize updatePosition.spaceSize
#else
uniform float friction;
uniform float spaceSize;
#endif

in vec2 textureCoords;

out vec4 fragColor;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);
  vec4 pointVelocity = texture(velocity, textureCoords);

  // Check if point is pinned
  // pinnedStatusTexture has the same size and layout as positionsTexture
  // Each pixel corresponds to a point: red channel > 0.5 means the point is pinned
  vec4 pinnedStatus = texture(pinnedStatusTexture, textureCoords);
  
  // If pinned, don't update position
  if (pinnedStatus.r > 0.5) {
    fragColor = pointPosition;
    return;
  }

  // If absent (current absence = exit.G), leave it untouched \u2014 don't integrate or
  // clamp it (clamping NaN is undefined and could resurrect the point at (0,0)).
  vec4 exitStatus = texture(exitTexture, textureCoords);
  if (exitStatus.g > 0.5) {
    fragColor = pointPosition;
    return;
  }

  // Friction
  pointVelocity.rg *= friction;

  pointPosition.rg += pointVelocity.rg;

  pointPosition.r = clamp(pointPosition.r, 0.0, spaceSize);
  pointPosition.g = clamp(pointPosition.g, 0.0, spaceSize);

  #ifdef SPACE_3D
  // The z coordinate lives in the position alpha channel and its velocity in
  // the velocity blue channel; integrate and clamp it like x and y.
  pointVelocity.b *= friction;
  pointPosition.a += pointVelocity.b;
  pointPosition.a = clamp(pointPosition.a, 0.0, spaceSize);
  #endif

  fragColor = pointPosition;
}`,Fi=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D sourceTexture;
uniform sampler2D targetTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform interpolatePositionUniforms {
  float progress;
} interpolatePosition;

#define progress interpolatePosition.progress
#else
uniform float progress;
#endif

in vec2 textureCoords;

out vec4 fragColor;

void main() {
  vec4 source = texture(sourceTexture, textureCoords);
  vec4 target = texture(targetTexture, textureCoords);
  // NaN means absent (ingest normalizes partially-NaN to full-NaN, so checking one
  // channel suffices). Hold the real side so the point stays put while it fades,
  // never interpolating to/from NaN:
  //   \xB7 exiting  (target NaN): freeze at source.
  //   \xB7 entering (source NaN): appear at target (no slide in from NaN).
  // Alpha holds the z coordinate (0 in 2D mode) and must be held with x/y.
  vec3 src = isnan(source.r) ? vec3(target.rg, target.a) : vec3(source.rg, source.a);
  vec3 tgt = isnan(target.r) ? src : vec3(target.rg, target.a);
  vec3 position = mix(src, tgt, progress);
  fragColor = vec4(position.xy, source.b, position.z);
}
`,Ii=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;
uniform sampler2D trackedIndices;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform trackPointsUniforms {
  float pointsTextureSize;
} trackPoints;

#define pointsTextureSize trackPoints.pointsTextureSize
#else
uniform float pointsTextureSize;
#endif

in vec2 textureCoords;

out vec4 fragColor;

void main() {
  vec4 trackedPointIndices = texture(trackedIndices, textureCoords);
  if (trackedPointIndices.r < 0.0) discard;
  vec4 pointPosition = texture(positionsTexture, (trackedPointIndices.rg + 0.5) / pointsTextureSize);

  // Blue carries the z coordinate (stored in the position texture's alpha; 0 in 2D mode).
  fragColor = vec4(pointPosition.rg, pointPosition.a, 1.0);
}

`,Li=`#version 300 es
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D positionsTexture;

#ifdef USE_UNIFORM_BUFFERS
layout(std140) uniform dragPointUniforms {
  vec4 mousePos; // [x, y, z, unused] \u2014 z is only consumed in 3D mode
  float index;
} dragPoint;

#define mousePos dragPoint.mousePos
#define index dragPoint.index
#else
uniform vec4 mousePos;
uniform float index;
#endif

in vec2 textureCoords;

out vec4 fragColor;

void main() {
  vec4 pointPosition = texture(positionsTexture, textureCoords);

  // Check if a point is being dragged
  if (index >= 0.0 && index == pointPosition.b) {
    pointPosition.rg = mousePos.rg;
    #ifdef SPACE_3D
    // The z coordinate lives in the position alpha channel.
    pointPosition.a = mousePos.b;
    #endif
  }

  fragColor = pointPosition;
}`;function Ui(h,e=16384){if(!(h!=null&&h.length))return null;let t=0;for(const l of h){const u=Math.max(l.width,l.height);u>t&&(t=u)}if(t===0)return console.warn("Invalid image dimensions: all images have zero width or height"),null;const i=t,o=Math.ceil(Math.sqrt(h.length));let s=o*t,r=1;s>e&&(r=e/s,t=Math.max(1,Math.floor(t*r)),s=Math.max(1,Math.floor(s*r)),console.warn(`\u{1F5BC}\uFE0F  Atlas scaling required: Original size ${(i*o).toLocaleString()}px exceeds WebGL limit ${e.toLocaleString()}px. Scaling down to ${s.toLocaleString()}px (${Math.round(r*100)}% of original quality)`));const n=new Uint8Array(s*s*4).fill(0),a=new Float32Array(o*o*4).fill(-1);for(const[l,u]of h.entries()){const d=u.width,c=u.height;if(d===0||c===0)continue;const f=Math.min(1,t/Math.max(d,c)),p=Math.floor(d*f),m=Math.floor(c*f),S=Math.floor(l/o),v=l%o*t,C=S*t;a[l*4]=v/s,a[l*4+1]=C/s,a[l*4+2]=(v+p)/s,a[l*4+3]=(C+m)/s;for(let D=0;D<m;D++)for(let I=0;I<p;I++){const L=Math.floor(I*(d/p)),z=(Math.floor(D*(c/m))*d+L)*4,R=((C+D)*s+(v+I))*4;n[R]=u.data[z]??0,n[R+1]=u.data[z+1]??0,n[R+2]=u.data[z+2]??0,n[R+3]=u.data[z+3]??255}}return{atlasData:n,atlasSize:s,atlasCoords:a,atlasCoordsSize:o}}function Bi(h,e,t,i=2){const o=e*e,s=new Float32Array(o*4),r=h?t:0;for(let n=r;n<o;++n)s[n*4+2]=-1;if(!h)return s;for(let n=0;n<t;++n){const a=q(h,n,i);s[n*4+0]=a?NaN:h[n*i+0],s[n*4+1]=a?NaN:h[n*i+1],s[n*4+2]=n,a?s[n*4+3]=NaN:s[n*4+3]=i===3?h[n*3+2]:0}return s}function Ai(h,e,t,i,o){const s=o*o,r=new Float32Array(s*4);for(let n=i;n<s;n+=1)r[n*4+2]=-1;for(let n=0;n<t;n+=1)r[n*4+0]=h[n*4+0],r[n*4+1]=h[n*4+1],r[n*4+2]=n,r[n*4+3]=h[n*4+3];for(let n=t;n<i;n+=1)r[n*4+0]=e[n*4+0],r[n*4+1]=e[n*4+1],r[n*4+2]=n,r[n*4+3]=e[n*4+3];return r}const ge=.5,Ri=1536,A=9,ve={blend:!0,blendColorOperation:"add",blendColorSrcFactor:"src-alpha",blendColorDstFactor:"one-minus-src-alpha",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one-minus-src-alpha"},Qe={...ve,depthWriteEnabled:!1,depthCompare:"always"},Mi={...ve,depthWriteEnabled:!0,depthCompare:"less-equal"},Ni={blend:!1,depthWriteEnabled:!0,depthCompare:"less"},Ei={...ve,depthWriteEnabled:!1,depthCompare:"less"};class _i extends V{constructor(){super(...arguments),this.isPickingBufferStale=!0,this.imageCount=0,this.areClusterCentroidsUpToDate=!1,this.isPositionsUpToDate=!1,this.programsSpaceDimensions=2,this.hasAnyAbsentPoint=!1,this.polygonPathLength=0,this.isOcclusionCullingActive=!1,this.transitionProgress=1,this.shouldAnimatePointColors=!1,this.shouldAnimatePointSizes=!1,this.shouldAnimatePointPositions=!1}get isPickInFlight(){var e;return((e=this.pickingReadback)==null?void 0:e.inFlight)??!1}updatePositions(){var e,t;const{device:i,store:o,data:s,config:{rescalePositions:r,enableSimulation:n}}=this,{pointsTextureSize:a}=o;if(!a||!s.pointPositions||s.pointsNumber===void 0)return!1;let l=r;r===void 0&&!n&&(l=!0),this.shouldSkipRescale&&(l=!1),l?this.rescaleInitialNodePositions():this.shouldSkipRescale||(this.scaleX=void 0,this.scaleY=void 0),this.shouldSkipRescale=void 0;const u=s.sourcePointsNumber,d=s.targetPointsNumber,c=u===d,f=((e=this.transition)==null?void 0:e.isPendingFor(F.Positions))===!0&&(((t=this.transition)==null?void 0:t.duration)??this.config.transitionDuration)>0&&!!this.currentPositionTexture,p=Bi(s.pointPositions,a,d,s.pointDimensions);let m;if(f&&(this.createTransitionResources(),this.sourcePositionTexture&&this.targetPositionTexture)){if(c){const C=this.currentPositionTexture;if(C&&!C.destroyed){const D=this.device.createCommandEncoder();D.copyTextureToTexture({sourceTexture:C,destinationTexture:this.sourcePositionTexture,width:a,height:a}),this.device.submit(D.finish())}}else if(this.currentPositionFbo){const C=B(i,this.currentPositionFbo);m=Ai(C,p,Math.min(u,d),d,a),this.writePositionTexture(this.sourcePositionTexture,m,a)}else this.writePositionTexture(this.sourcePositionTexture,p,a);this.writePositionTexture(this.targetPositionTexture,p,a)}this.ensurePositionTextures(a),f?m&&(this.writePositionTexture(this.currentPositionTexture,m,a),this.writePositionTexture(this.previousPositionTexture,m,a)):(this.writePositionTexture(this.currentPositionTexture,p,a),this.writePositionTexture(this.previousPositionTexture,p,a)),this.areClusterCentroidsUpToDate=!1,this.isPositionsUpToDate=!1,this.config.enableSimulation&&this.ensureSimulationResources(),!this.searchTexture||this.searchTexture.width!==a||this.searchTexture.height!==a?(this.searchTexture&&!this.searchTexture.destroyed&&this.searchTexture.destroy(),this.searchFbo&&!this.searchFbo.destroyed&&this.searchFbo.destroy(),this.searchTexture=i.createTexture({width:a,height:a,format:"rgba32float"}),this.searchTexture.copyImageData({data:p,bytesPerRow:y("rgba32float",a),mipLevel:0,x:0,y:0}),this.searchFbo=i.createFramebuffer({width:a,height:a,colorAttachments:[this.searchTexture]})):this.searchTexture.copyImageData({data:p,bytesPerRow:y("rgba32float",a),mipLevel:0,x:0,y:0}),this.isPickingBufferStale=!0,this.discardPendingPick();const S=K(o.pointsTextureSize),v=S.byteLength;return!this.drawPointIndices||this.drawPointIndices.byteLength!==v?(this.drawPointIndices&&!this.drawPointIndices.destroyed&&this.drawPointIndices.destroy(),this.drawPointIndices=i.createBuffer({data:S,usage:x.VERTEX|x.COPY_DST})):this.drawPointIndices.write(S),this.drawCommand&&this.drawCommand.setAttributes({pointIndices:this.drawPointIndices}),this.drawCoreCommand&&this.drawCoreCommand.setAttributes({pointIndices:this.drawPointIndices}),this.updateReversedPointIndexBuffer(),!this.hoveredPointIndices||this.hoveredPointIndices.byteLength!==v?(this.hoveredPointIndices&&!this.hoveredPointIndices.destroyed&&this.hoveredPointIndices.destroy(),this.hoveredPointIndices=i.createBuffer({data:S,usage:x.VERTEX|x.COPY_DST})):this.hoveredPointIndices.write(S),!this.sampledPointIndices||this.sampledPointIndices.byteLength!==v?(this.sampledPointIndices&&!this.sampledPointIndices.destroyed&&this.sampledPointIndices.destroy(),this.sampledPointIndices=i.createBuffer({data:S,usage:x.VERTEX|x.COPY_DST})):this.sampledPointIndices.write(S),this.fillSampledPointsFboCommand&&this.fillSampledPointsFboCommand.setAttributes({pointIndices:this.sampledPointIndices}),this.updatePointStatus(),this.updatePinnedStatus(),this.updateExit(),this.updateSampledPointsGrid(),f||this.trackPoints(),f}initPrograms(){var e,t,i;const{device:o,config:s,store:r,data:n}=this;this.programsSpaceDimensions!==r.spaceDimensions&&(this.programsSpaceDimensions=r.spaceDimensions,this.drawCommand&&(this.drawCommand.destroy(),this.drawCommand=void 0),this.drawCoreCommand&&(this.drawCoreCommand.destroy(),this.drawCoreCommand=void 0),this.isOcclusionCullingActive=!1,this.fillPickingBufferCommand&&(this.fillPickingBufferCommand.destroy(),this.fillPickingBufferCommand=void 0),this.isPickingBufferStale=!0,this.drawHighlightedCommand&&(this.drawHighlightedCommand.destroy(),this.drawHighlightedCommand=void 0),this.fillSampledPointsFboCommand&&(this.fillSampledPointsFboCommand.destroy(),this.fillSampledPointsFboCommand=void 0),this.updatePositionCommand&&(this.updatePositionCommand.destroy(),this.updatePositionCommand=void 0),this.dragPointCommand&&(this.dragPointCommand.destroy(),this.dragPointCommand=void 0)),(!this.imageAtlasCoordsTexture||!this.imageAtlasTexture)&&this.createAtlas(),this.targetColorBuffer||this.updateColor(),this.targetSizeBuffer||this.updateSize(),this.exitTexture||this.updateExit(),this.shapeBuffer||this.updateShape(),this.imageIndicesBuffer||this.updateImageIndices(),this.imageSizesBuffer||this.updateImageSizes(),this.pointStatusTexture||this.updatePointStatus(),s.enableSimulation&&this.ensureUpdatePositionProgram(),this.dragPointVertexCoordBuffer||(this.dragPointVertexCoordBuffer=o.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.dragPointUniformStore||(this.dragPointUniformStore=new T(o,{dragPointUniforms:{uniformTypes:{mousePos:"vec4<f32>",index:"f32"},defaultUniforms:{mousePos:[0,0,0,0],index:((e=r.hoveredPoint)==null?void 0:e.index)??-1}}})),this.dragPointCommand||(this.dragPointCommand=new b(o,{fs:Li,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.dragPointVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...r.is3D?{SPACE_3D:!0}:{}},bindings:{dragPointUniforms:this.dragPointUniformStore.getManagedUniformBuffer("dragPointUniforms")}})),this.drawUniformStore||(this.drawUniformStore=new T(o,{drawVertexUniforms:{uniformTypes:{ratio:"f32",transformationMatrix:"mat4x4<f32>",pointsTextureSize:"f32",sizeScale:"f32",spaceSize:"f32",screenSize:"vec2<f32>",greyoutColor:"vec4<f32>",backgroundColor:"vec4<f32>",scalePointsOnZoom:"f32",maxPointSize:"f32",isDarkenGreyout:"f32",skipHighlighted:"f32",skipGreyed:"f32",hasImages:"f32",imageCount:"f32",imageAtlasCoordsTextureSize:"f32",transitionProgress:"f32",animateColors:"f32",animateSizes:"f32",pointsNumber:"f32",pointDepthFade:"f32",depthFadeNear:"f32",depthFadeFar:"f32",animatePositions:"f32",pointDefaultColor:"vec4<f32>",pointDefaultSize:"f32"},defaultUniforms:{ratio:s.pixelRatio,transformationMatrix:(()=>{const a=r.transform??[1,0,0,0,1,0,0,0,1];return[a[0],a[1],a[2],0,a[3],a[4],a[5],0,a[6],a[7],a[8],0,0,0,0,1]})(),pointsTextureSize:r.pointsTextureSize??0,sizeScale:s.pointSizeScale,spaceSize:r.adjustedSpaceSize,screenSize:k(r.screenSize,[0,0]),greyoutColor:w(r.greyoutPointColor,[0,0,0,1]),backgroundColor:w(r.backgroundColor,[0,0,0,1]),scalePointsOnZoom:s.scalePointsOnZoom?1:0,maxPointSize:r.maxPointSize,isDarkenGreyout:r.isDarkenGreyout??!1?1:0,skipHighlighted:0,skipGreyed:0,hasImages:this.imageCount>0?1:0,imageCount:this.imageCount,imageAtlasCoordsTextureSize:this.imageAtlasCoordsTextureSize??0,transitionProgress:1,animateColors:0,animateSizes:0,pointsNumber:n.pointsNumber??0,pointDepthFade:0,depthFadeNear:0,depthFadeFar:1,animatePositions:0,pointDefaultColor:w(n.defaultRgba,[0,0,0,1]),pointDefaultSize:s.pointDefaultSize}},drawFragmentUniforms:{uniformTypes:{greyoutOpacity:"f32",pointOpacity:"f32",isDarkenGreyout:"f32",backgroundColor:"vec4<f32>",outlineColor:"vec4<f32>",outlineWidth:"f32",renderMode:"f32",sphereShading:"f32"},defaultUniforms:{greyoutOpacity:s.pointGreyoutOpacity??-1,pointOpacity:s.pointOpacity,isDarkenGreyout:r.isDarkenGreyout??!1?1:0,backgroundColor:w(r.backgroundColor,[0,0,0,1]),outlineColor:w(r.outlinedPointRingColor,[1,1,1,1]),outlineWidth:.9,renderMode:0,sphereShading:0}}})),this.drawCommand||(this.drawCommand=new b(o,{fs:Ke,vs:$e,modules:[Q],topology:"point-list",vertexCount:n.pointsNumber??0,attributes:{...this.drawPointIndices&&{pointIndices:this.drawPointIndices},...this.sourceSizeBuffer&&{sourceSize:this.sourceSizeBuffer},...this.targetSizeBuffer&&{targetSize:this.targetSizeBuffer},...this.sourceColorBuffer&&{sourceColor:this.sourceColorBuffer},...this.targetColorBuffer&&{targetColor:this.targetColorBuffer},...this.shapeBuffer&&{shape:this.shapeBuffer},...this.imageIndicesBuffer&&{imageIndex:this.imageIndicesBuffer},...this.imageSizesBuffer&&{imageSize:this.imageSizesBuffer}},bufferLayout:[{name:"pointIndices",format:"float32x2"},{name:"sourceSize",format:"float32"},{name:"targetSize",format:"float32"},{name:"sourceColor",format:"float32x4"},{name:"targetColor",format:"float32x4"},{name:"shape",format:"float32"},{name:"imageIndex",format:"float32"},{name:"imageSize",format:"float32"}],defines:{USE_UNIFORM_BUFFERS:!0,...r.is3D?{SPACE_3D:!0}:{},EXIT_DEFAULT_SIZE:$(ie),EXIT_DEFAULT_COLOR_CHANNEL:$(Y)},bindings:{drawVertexUniforms:this.drawUniformStore.getManagedUniformBuffer("drawVertexUniforms"),drawFragmentUniforms:this.drawUniformStore.getManagedUniformBuffer("drawFragmentUniforms")},parameters:r.is3D?Mi:Qe})),r.is3D||(this.updateReversedPointIndexBuffer(),this.drawCoreCommand||(this.drawCoreCommand=new b(o,{fs:Ke,vs:$e,modules:[Q],topology:"point-list",vertexCount:n.pointsNumber??0,indexBuffer:this.reversedPointIndexBuffer??null,attributes:{...this.drawPointIndices&&{pointIndices:this.drawPointIndices},...this.sourceSizeBuffer&&{sourceSize:this.sourceSizeBuffer},...this.targetSizeBuffer&&{targetSize:this.targetSizeBuffer},...this.sourceColorBuffer&&{sourceColor:this.sourceColorBuffer},...this.targetColorBuffer&&{targetColor:this.targetColorBuffer},...this.shapeBuffer&&{shape:this.shapeBuffer},...this.imageIndicesBuffer&&{imageIndex:this.imageIndicesBuffer},...this.imageSizesBuffer&&{imageSize:this.imageSizesBuffer}},bufferLayout:[{name:"pointIndices",format:"float32x2"},{name:"sourceSize",format:"float32"},{name:"targetSize",format:"float32"},{name:"sourceColor",format:"float32x4"},{name:"targetColor",format:"float32x4"},{name:"shape",format:"float32"},{name:"imageIndex",format:"float32"},{name:"imageSize",format:"float32"}],defines:{USE_UNIFORM_BUFFERS:!0,EXIT_DEFAULT_SIZE:$(ie),EXIT_DEFAULT_COLOR_CHANNEL:$(Y)},bindings:{drawVertexUniforms:this.drawUniformStore.getManagedUniformBuffer("drawVertexUniforms"),drawFragmentUniforms:this.drawUniformStore.getManagedUniformBuffer("drawFragmentUniforms")},parameters:Ni}))),this.findPointsInRectVertexCoordBuffer||(this.findPointsInRectVertexCoordBuffer=o.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.findPointsInRectUniformStore||(this.findPointsInRectUniformStore=new T(o,{findPointsInRectUniforms:{uniformTypes:{sizeScale:"f32",spaceSize:"f32",screenSize:"vec2<f32>",ratio:"f32",transformationMatrix:"mat4x4<f32>",rect0:"vec2<f32>",rect1:"vec2<f32>",scalePointsOnZoom:"f32",maxPointSize:"f32"},defaultUniforms:{sizeScale:s.pointSizeScale,spaceSize:r.adjustedSpaceSize,screenSize:k(r.screenSize,[0,0]),ratio:s.pixelRatio,transformationMatrix:r.transformationMatrix4x4,rect0:k((t=r.searchArea)==null?void 0:t[0],[0,0]),rect1:k((i=r.searchArea)==null?void 0:i[1],[0,0]),scalePointsOnZoom:s.scalePointsOnZoom?1:0,maxPointSize:r.maxPointSize}}})),this.findPointsInRectCommand||(this.findPointsInRectCommand=new b(o,{fs:Pi,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.findPointsInRectVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{findPointsInRectUniforms:this.findPointsInRectUniformStore.getManagedUniformBuffer("findPointsInRectUniforms")}})),this.findPointsInPolygonVertexCoordBuffer||(this.findPointsInPolygonVertexCoordBuffer=o.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.findPointsInPolygonUniformStore||(this.findPointsInPolygonUniformStore=new T(o,{findPointsInPolygonUniforms:{uniformTypes:{spaceSize:"f32",screenSize:"vec2<f32>",transformationMatrix:"mat4x4<f32>",polygonPathLength:"f32"},defaultUniforms:{spaceSize:r.adjustedSpaceSize,screenSize:k(r.screenSize,[0,0]),transformationMatrix:r.transformationMatrix4x4,polygonPathLength:this.polygonPathLength}}})),this.findPointsInPolygonCommand||(this.findPointsInPolygonCommand=new b(o,{fs:yi,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.findPointsInPolygonVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{findPointsInPolygonUniforms:this.findPointsInPolygonUniformStore.getManagedUniformBuffer("findPointsInPolygonUniforms")}})),this.fillPickingBufferUniformStore||(this.fillPickingBufferUniformStore=new T(o,{fillPickingBufferUniforms:{uniformTypes:{pointsTextureSize:"f32",sizeScale:"f32",spaceSize:"f32",screenSize:"vec2<f32>",ratio:"f32",pickingPixelRatio:"f32",transformationMatrix:"mat4x4<f32>",scalePointsOnZoom:"f32",maxPointSize:"f32",skipHighlighted:"f32",skipGreyed:"f32",pointDefaultSize:"f32"},defaultUniforms:{pointsTextureSize:r.pointsTextureSize??0,sizeScale:s.pointSizeScale,spaceSize:r.adjustedSpaceSize,screenSize:k(r.screenSize,[0,0]),ratio:s.pixelRatio,pickingPixelRatio:ge,transformationMatrix:r.transformationMatrix4x4,scalePointsOnZoom:s.scalePointsOnZoom?1:0,maxPointSize:r.maxPointSize,skipHighlighted:0,skipGreyed:0,pointDefaultSize:s.pointDefaultSize}}})),this.fillPickingBufferCommand||(this.fillPickingBufferCommand=new b(o,{fs:Ti,vs:ki,modules:[Q],topology:"point-list",vertexCount:n.pointsNumber??0,attributes:{...this.hoveredPointIndices&&{pointIndices:this.hoveredPointIndices},...this.targetSizeBuffer&&{size:this.targetSizeBuffer},...this.imageSizesBuffer&&{imageSize:this.imageSizesBuffer}},bufferLayout:[{name:"pointIndices",format:"float32x2"},{name:"size",format:"float32"},{name:"imageSize",format:"float32"}],defines:{USE_UNIFORM_BUFFERS:!0,...r.is3D?{SPACE_3D:!0}:{}},bindings:{fillPickingBufferUniforms:this.fillPickingBufferUniformStore.getManagedUniformBuffer("fillPickingBufferUniforms")},parameters:{depthWriteEnabled:r.is3D,depthCompare:r.is3D?"less-equal":"always",blend:!1}})),this.fillSampledPointsUniformStore||(this.fillSampledPointsUniformStore=new T(o,{fillSampledPointsUniforms:{uniformTypes:{pointsTextureSize:"f32",transformationMatrix:"mat4x4<f32>",spaceSize:"f32",screenSize:"vec2<f32>"},defaultUniforms:{pointsTextureSize:r.pointsTextureSize??0,transformationMatrix:r.transformationMatrix4x4,spaceSize:r.adjustedSpaceSize,screenSize:k(r.screenSize,[0,0])}}})),this.fillSampledPointsFboCommand||(this.fillSampledPointsFboCommand=new b(o,{fs:zi,vs:wi,topology:"point-list",vertexCount:n.pointsNumber??0,attributes:{...this.sampledPointIndices&&{pointIndices:this.sampledPointIndices}},bufferLayout:[{name:"pointIndices",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...r.is3D?{SPACE_3D:!0}:{}},bindings:{fillSampledPointsUniforms:this.fillSampledPointsUniformStore.getManagedUniformBuffer("fillSampledPointsUniforms")},parameters:{depthWriteEnabled:!1,depthCompare:"always"}})),this.drawHighlightedVertexCoordBuffer||(this.drawHighlightedVertexCoordBuffer=o.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.drawHighlightedUniformStore||(this.drawHighlightedUniformStore=new T(o,{drawHighlightedUniforms:{uniformTypes:{size:"f32",transformationMatrix:"mat4x4<f32>",pointsTextureSize:"f32",sizeScale:"f32",spaceSize:"f32",screenSize:"vec2<f32>",scalePointsOnZoom:"f32",pointIndex:"f32",maxPointSize:"f32",color:"vec4<f32>",universalPointOpacity:"f32",greyoutOpacity:"f32",isDarkenGreyout:"f32",backgroundColor:"vec4<f32>",greyoutColor:"vec4<f32>",width:"f32"},defaultUniforms:{size:1,transformationMatrix:r.transformationMatrix4x4,pointsTextureSize:r.pointsTextureSize??0,sizeScale:s.pointSizeScale,spaceSize:r.adjustedSpaceSize,screenSize:k(r.screenSize,[0,0]),scalePointsOnZoom:s.scalePointsOnZoom?1:0,pointIndex:-1,maxPointSize:r.maxPointSize,color:[0,0,0,1],universalPointOpacity:s.pointOpacity,greyoutOpacity:s.pointGreyoutOpacity??-1,isDarkenGreyout:r.isDarkenGreyout??!1?1:0,backgroundColor:w(r.backgroundColor,[0,0,0,1]),greyoutColor:w(r.greyoutPointColor,[0,0,0,1]),width:.85}}})),this.drawHighlightedCommand||(this.drawHighlightedCommand=new b(o,{fs:Ci,vs:bi,modules:[Q],topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.drawHighlightedVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...r.is3D?{SPACE_3D:!0}:{}},bindings:{drawHighlightedUniforms:this.drawHighlightedUniformStore.getManagedUniformBuffer("drawHighlightedUniforms")},parameters:{blend:!0,blendColorOperation:"add",blendColorSrcFactor:"src-alpha",blendColorDstFactor:"one-minus-src-alpha",blendAlphaOperation:"add",blendAlphaSrcFactor:"one",blendAlphaDstFactor:"one-minus-src-alpha",depthWriteEnabled:!1,depthCompare:r.is3D?"less-equal":"always"}})),this.trackPointsVertexCoordBuffer||(this.trackPointsVertexCoordBuffer=o.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.trackPointsUniformStore||(this.trackPointsUniformStore=new T(o,{trackPointsUniforms:{uniformTypes:{pointsTextureSize:"f32"},defaultUniforms:{pointsTextureSize:r.pointsTextureSize??0}}})),this.trackPointsCommand||(this.trackPointsCommand=new b(o,{fs:Ii,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.trackPointsVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{trackPointsUniforms:this.trackPointsUniformStore.getManagedUniformBuffer("trackPointsUniforms")}}))}updateColor(){const{device:e,store:{pointsTextureSize:t},data:i}=this;if(!t)return;const o=i.pointColors,{source:s,target:r,previous:n}=oe(this.device,o,this.sourceColorBuffer,this.targetColorBuffer,this.previousColorData,4);this.sourceColorBuffer=s,this.targetColorBuffer=r,this.previousColorData=n;const a={...this.sourceColorBuffer&&{sourceColor:this.sourceColorBuffer},...this.targetColorBuffer&&{targetColor:this.targetColorBuffer}};if(this.drawCommand&&this.drawCommand.setAttributes(a),this.drawCoreCommand&&this.drawCoreCommand.setAttributes(a),this.config.linkColorInterpolateFromEndpoints){const l=new Float32Array(t*t*4);l.set(o.subarray(0,Math.min(o.length,l.length))),(!this.pointColorsTexture||this.pointColorsTexture.width!==t||this.pointColorsTexture.height!==t)&&(this.pointColorsTexture&&!this.pointColorsTexture.destroyed&&this.pointColorsTexture.destroy(),this.pointColorsTexture=e.createTexture({width:t,height:t,format:"rgba32float"})),this.pointColorsTexture.copyImageData({data:l,bytesPerRow:y("rgba32float",t),mipLevel:0,x:0,y:0})}else this.pointColorsTexture&&(this.pointColorsTexture.destroyed||this.pointColorsTexture.destroy(),this.pointColorsTexture=void 0)}updateExit(){const{device:e,store:{pointsTextureSize:t},data:i}=this;if(!t)return;const o=i.pointsNumber??0,s=this.previousExitData,r=this.hasAnyAbsentPoint,n=new Float32Array(o);let a=!1;for(let d=0;d<o;d++){const c=i.pointPositions&&q(i.pointPositions,d,i.pointDimensions)?1:0;n[d]=c,c&&(a=!0)}if(this.previousExitData=n,this.hasAnyAbsentPoint=a,!a&&!r){if(this.exitTexture&&!this.exitTexture.destroyed&&this.exitTexture.width===1)return;this.exitTexture&&!this.exitTexture.destroyed&&this.exitTexture.destroy(),this.exitTexture=e.createTexture({width:1,height:1,format:"rgba32float"}),this.exitTexture.copyImageData({data:new Float32Array(4),bytesPerRow:y("rgba32float",1),mipLevel:0,x:0,y:0});return}const l=new Float32Array(t*t*4);for(let d=0;d<o;d++){const c=n[d],f=d<(s?.length??0)?s[d]:c;l[d*4]=f,l[d*4+1]=c}const u=!!this.exitTexture&&this.exitTexture.width===t&&this.exitTexture.height===t;(!this.exitTexture||!u)&&(this.exitTexture&&!this.exitTexture.destroyed&&this.exitTexture.destroy(),this.exitTexture=e.createTexture({width:t,height:t,format:"rgba32float"})),this.exitTexture.copyImageData({data:l,bytesPerRow:y("rgba32float",t),mipLevel:0,x:0,y:0})}updatePointStatus(){const{device:e,config:t,data:i,store:{pointsTextureSize:o}}=this;if(!o||i.pointsNumber===void 0)return;this.isPickingBufferStale=!0;const{highlightedPointIndices:s,outlinedPointIndices:r}=t,n=s!==void 0,a=r!==void 0,l=new Float32Array(o*o*4);if(n){for(let d=0;d<l.length;d+=4)l[d]=1;for(const d of s)d>=0&&d<i.pointsNumber&&(l[d*4]=0)}if(a)for(const d of r)d>=0&&d<i.pointsNumber&&(l[d*4+1]=1);const u={data:l,bytesPerRow:y("rgba32float",o),mipLevel:0,x:0,y:0};!this.pointStatusTexture||this.pointStatusTexture.width!==o||this.pointStatusTexture.height!==o?(this.pointStatusTexture&&!this.pointStatusTexture.destroyed&&this.pointStatusTexture.destroy(),this.pointStatusTexture=e.createTexture({width:o,height:o,format:"rgba32float"}),this.pointStatusTexture.copyImageData(u)):this.pointStatusTexture.copyImageData(u)}updatePinnedStatus(){const{device:e,store:{pointsTextureSize:t},data:i}=this;if(!t)return;const o=new Float32Array(t*t*4).fill(0);if(i.inputPinnedPoints&&i.pointsNumber!==void 0)for(const s of i.inputPinnedPoints)s>=0&&s<i.pointsNumber&&(o[s*4]=1);!this.pinnedStatusTexture||this.pinnedStatusTexture.width!==t||this.pinnedStatusTexture.height!==t?(this.pinnedStatusTexture&&!this.pinnedStatusTexture.destroyed&&this.pinnedStatusTexture.destroy(),this.pinnedStatusTexture=e.createTexture({width:t,height:t,format:"rgba32float"}),this.pinnedStatusTexture.copyImageData({data:o,bytesPerRow:y("rgba32float",t),mipLevel:0,x:0,y:0})):this.pinnedStatusTexture.copyImageData({data:o,bytesPerRow:y("rgba32float",t),mipLevel:0,x:0,y:0})}updateSize(){var e;const{device:t,store:{pointsTextureSize:i},data:o}=this;if(!i||o.pointsNumber===void 0)return;this.isPickingBufferStale=!0;const s=o.pointSizes,{source:r,target:n,previous:a}=oe(this.device,s,this.sourceSizeBuffer,this.targetSizeBuffer,this.previousSizeData,1);this.sourceSizeBuffer=r,this.targetSizeBuffer=n,this.previousSizeData=a;const l={...this.sourceSizeBuffer&&{sourceSize:this.sourceSizeBuffer},...this.targetSizeBuffer&&{targetSize:this.targetSizeBuffer}};this.drawCommand&&this.drawCommand.setAttributes(l),this.drawCoreCommand&&this.drawCoreCommand.setAttributes(l);const u=new Float32Array(i*i*4);for(let d=0;d<o.pointsNumber;d++){const c=o.getResolvedPointSize(d),f=((e=o.pointImageSizes)==null?void 0:e[d])??c;u[d*4]=Math.max(c,f)}if(!this.sizeTexture||this.sizeTexture.width!==i||this.sizeTexture.height!==i){this.sizeTexture&&!this.sizeTexture.destroyed&&this.sizeTexture.destroy();const d=t.createTexture({width:i,height:i,format:"rgba32float"});this.sizeTexture=d,d.copyImageData({data:u,bytesPerRow:y("rgba32float",i),mipLevel:0,x:0,y:0})}else this.sizeTexture.copyImageData({data:u,bytesPerRow:y("rgba32float",i),mipLevel:0,x:0,y:0})}updateShape(){const{device:e,data:t}=this;if(t.pointsNumber===void 0||t.pointShapes===void 0)return;const i=t.pointShapes,o=i.byteLength;!this.shapeBuffer||this.shapeBuffer.byteLength!==o?(this.shapeBuffer&&!this.shapeBuffer.destroyed&&this.shapeBuffer.destroy(),this.shapeBuffer=e.createBuffer({data:i,usage:x.VERTEX|x.COPY_DST})):this.shapeBuffer.write(i),this.drawCommand&&this.drawCommand.setAttributes({shape:this.shapeBuffer}),this.drawCoreCommand&&this.drawCoreCommand.setAttributes({shape:this.shapeBuffer})}updateImageIndices(){const{device:e,data:t}=this;if(t.pointsNumber===void 0||t.pointImageIndices===void 0)return;const i=t.pointImageIndices,o=i.byteLength;!this.imageIndicesBuffer||this.imageIndicesBuffer.byteLength!==o?(this.imageIndicesBuffer&&!this.imageIndicesBuffer.destroyed&&this.imageIndicesBuffer.destroy(),this.imageIndicesBuffer=e.createBuffer({data:i,usage:x.VERTEX|x.COPY_DST})):this.imageIndicesBuffer.write(i),this.drawCommand&&this.drawCommand.setAttributes({imageIndex:this.imageIndicesBuffer}),this.drawCoreCommand&&this.drawCoreCommand.setAttributes({imageIndex:this.imageIndicesBuffer})}updateImageSizes(){const{device:e,data:t}=this;if(t.pointsNumber===void 0||t.pointImageSizes===void 0)return;const i=t.pointImageSizes,o=i.byteLength;!this.imageSizesBuffer||this.imageSizesBuffer.byteLength!==o?(this.imageSizesBuffer&&!this.imageSizesBuffer.destroyed&&this.imageSizesBuffer.destroy(),this.imageSizesBuffer=e.createBuffer({data:i,usage:x.VERTEX|x.COPY_DST})):this.imageSizesBuffer.write(i),this.drawCommand&&this.drawCommand.setAttributes({imageSize:this.imageSizesBuffer}),this.drawCoreCommand&&this.drawCoreCommand.setAttributes({imageSize:this.imageSizesBuffer}),this.fillPickingBufferCommand&&this.fillPickingBufferCommand.setAttributes({imageSize:this.imageSizesBuffer}),this.isPickingBufferStale=!0}createAtlas(){var e;const{device:t,data:i,store:o}=this;if(!((e=i.inputImageData)!=null&&e.length)){this.imageCount=0,this.imageAtlasCoordsTextureSize=0,this.imageAtlasCoordsTexture||(this.imageAtlasCoordsTexture=t.createTexture({data:new Float32Array(4).fill(0),width:1,height:1,format:"rgba32float"})),this.imageAtlasTexture||(this.imageAtlasTexture=t.createTexture({data:new Uint8Array(4).fill(0),width:1,height:1,format:"rgba8unorm"}));return}const s=Ui(i.inputImageData,o.webglMaxTextureSize);if(!s){console.warn("Failed to create atlas from image data");return}this.imageCount=i.inputImageData.length;const{atlasData:r,atlasSize:n,atlasCoords:a,atlasCoordsSize:l}=s;this.imageAtlasCoordsTextureSize=l,this.imageAtlasTexture&&!this.imageAtlasTexture.destroyed&&this.imageAtlasTexture.destroy(),this.imageAtlasTexture=t.createTexture({width:n,height:n,format:"rgba8unorm"}),this.imageAtlasTexture.copyImageData({data:r,bytesPerRow:y("rgba8unorm",n),rowsPerImage:n,mipLevel:0,x:0,y:0}),this.imageAtlasCoordsTexture&&!this.imageAtlasCoordsTexture.destroyed&&this.imageAtlasCoordsTexture.destroy(),this.imageAtlasCoordsTexture=t.createTexture({width:l,height:l,format:"rgba32float"}),this.imageAtlasCoordsTexture.copyImageData({data:a,bytesPerRow:y("rgba32float",l),rowsPerImage:l,mipLevel:0,x:0,y:0})}updateSampledPointsGrid(){const{store:{screenSize:e},config:{pointSamplingDistance:t},device:i}=this;let o=t??Math.min(...e)/2;o===0&&(o=M.pointSamplingDistance);const s=Math.ceil(e[0]/o),r=Math.ceil(e[1]/o);s===0||r===0||(!this.sampledPointsFbo||this.sampledPointsFbo.width!==s||this.sampledPointsFbo.height!==r)&&(this.sampledPointsFbo&&!this.sampledPointsFbo.destroyed&&this.sampledPointsFbo.destroy(),this.sampledPointsFbo=i.createFramebuffer({width:s,height:r,colorAttachments:["rgba32float"]}))}trackPoints(){var e;if(!((e=this.trackedIndices)!=null&&e.length)||!this.trackPointsCommand||!this.trackPointsUniformStore||!this.trackedPositionsFbo||this.trackedPositionsFbo.destroyed||!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.trackedIndicesTexture||this.trackedIndicesTexture.destroyed)return;this.trackPointsUniformStore.setUniforms({trackPointsUniforms:{pointsTextureSize:this.store.pointsTextureSize??0}}),this.trackPointsCommand.setBindings({positionsTexture:this.currentPositionTexture,trackedIndices:this.trackedIndicesTexture});const t=this.device.beginRenderPass({framebuffer:this.trackedPositionsFbo});this.trackPointsCommand.draw(t),t.end()}setTransitionProgress(e,t=!1,i=!1,o=!1){this.transitionProgress=e,this.shouldAnimatePointColors=t,this.shouldAnimatePointSizes=i,this.shouldAnimatePointPositions=o}draw(e){var t,i,o;const{data:s,config:r,store:n}=this;if(this.targetColorBuffer||this.updateColor(),this.targetSizeBuffer||this.updateSize(),this.exitTexture||this.updateExit(),this.shapeBuffer||this.updateShape(),this.imageIndicesBuffer||this.updateImageIndices(),this.imageSizesBuffer||this.updateImageSizes(),!this.drawCommand||!this.drawUniformStore||!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.pointStatusTexture||this.pointStatusTexture.destroyed||!this.exitTexture||this.exitTexture.destroyed||(!this.imageAtlasTexture||!this.imageAtlasCoordsTexture)&&(this.createAtlas(),!this.imageAtlasTexture||!this.imageAtlasCoordsTexture)||this.imageAtlasTexture.destroyed||this.imageAtlasCoordsTexture.destroyed||!s.pointsNumber||s.pointsNumber===0||!n.screenSize||n.screenSize[0]===0||n.screenSize[1]===0)return;this.drawCommand.setVertexCount(s.pointsNumber);const a={ratio:r.pixelRatio,transformationMatrix:n.transformationMatrix4x4,pointsTextureSize:n.pointsTextureSize??0,sizeScale:r.pointSizeScale,spaceSize:n.adjustedSpaceSize,screenSize:k(n.screenSize,[0,0]),greyoutColor:w(n.greyoutPointColor,[-1,-1,-1,-1]),backgroundColor:w(n.backgroundColor,[0,0,0,1]),scalePointsOnZoom:r.scalePointsOnZoom?1:0,maxPointSize:n.maxPointSize,isDarkenGreyout:n.isDarkenGreyout??!1?1:0,hasImages:this.imageCount>0?1:0,imageCount:this.imageCount,imageAtlasCoordsTextureSize:this.imageAtlasCoordsTextureSize??0,transitionProgress:this.transitionProgress,animateColors:this.shouldAnimatePointColors?1:0,animateSizes:this.shouldAnimatePointSizes?1:0,pointsNumber:s.pointsNumber,pointDepthFade:n.is3D?r.pointDepthFade:0,depthFadeNear:n.depthFadeRange[0],depthFadeFar:n.depthFadeRange[1],animatePositions:this.shouldAnimatePointPositions?1:0,pointDefaultColor:w(s.defaultRgba,[0,0,0,1]),pointDefaultSize:r.pointDefaultSize},l={greyoutOpacity:r.pointGreyoutOpacity??-1,pointOpacity:r.pointOpacity,isDarkenGreyout:n.isDarkenGreyout??!1?1:0,backgroundColor:w(n.backgroundColor,[0,0,0,1]),outlineColor:w(n.outlinedPointRingColor,[1,1,1,1]),outlineWidth:.9,renderMode:0,sphereShading:n.is3D&&r.pointSphereShading?1:0},u={positionsTexture:this.currentPositionTexture,pointStatus:this.pointStatusTexture,exitTexture:this.exitTexture,imageAtlasTexture:this.imageAtlasTexture,imageAtlasCoords:this.imageAtlasCoordsTexture},d=r.highlightedPointIndices!==void 0,c=r.pointOcclusionCulling&&r.pointOpacity>=1&&!d&&!n.is3D&&!!this.drawCoreCommand&&((t=this.reversedPointIndexBuffer)==null?void 0:t.byteLength)===s.pointsNumber*4;if(c!==this.isOcclusionCullingActive&&(this.drawCommand.setParameters(c?Ei:Qe),this.isOcclusionCullingActive=c),c&&this.drawCoreCommand?(this.drawUniformStore.setUniforms({drawVertexUniforms:{...a,skipHighlighted:0,skipGreyed:0},drawFragmentUniforms:{...l,renderMode:1}}),this.drawCoreCommand.setVertexCount(s.pointsNumber),this.drawCoreCommand.setBindings(u),this.drawCoreCommand.draw(e),this.drawUniformStore.setUniforms({drawFragmentUniforms:{...l,renderMode:2}}),this.drawCommand.setBindings(u),this.drawCommand.draw(e)):d?(this.drawUniformStore.setUniforms({drawVertexUniforms:{...a,skipHighlighted:1,skipGreyed:0},drawFragmentUniforms:l}),this.drawCommand.setBindings(u),this.drawCommand.draw(e),this.drawUniformStore.setUniforms({drawVertexUniforms:{...a,skipHighlighted:0,skipGreyed:1},drawFragmentUniforms:l}),this.drawCommand.setBindings(u),this.drawCommand.draw(e)):(this.drawUniformStore.setUniforms({drawVertexUniforms:{...a,skipHighlighted:0,skipGreyed:0},drawFragmentUniforms:l}),this.drawCommand.setBindings(u),this.drawCommand.draw(e)),r.renderHoveredPointRing&&n.hoveredPoint&&this.drawHighlightedCommand&&this.drawHighlightedUniformStore){if(!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.pointStatusTexture||this.pointStatusTexture.destroyed||!this.exitTexture||this.exitTexture.destroyed)return;const f=s.getResolvedPointSize(n.hoveredPoint.index),p=((i=s.pointImageSizes)==null?void 0:i[n.hoveredPoint.index])??f;this.drawHighlightedUniformStore.setUniforms({drawHighlightedUniforms:{size:Math.max(f,p),transformationMatrix:n.transformationMatrix4x4,pointsTextureSize:n.pointsTextureSize??0,sizeScale:r.pointSizeScale,spaceSize:n.adjustedSpaceSize,screenSize:k(n.screenSize,[0,0]),scalePointsOnZoom:r.scalePointsOnZoom?1:0,pointIndex:n.hoveredPoint.index,maxPointSize:n.maxPointSize,color:w(n.hoveredPointRingColor,[0,0,0,1]),universalPointOpacity:r.pointOpacity,greyoutOpacity:r.pointGreyoutOpacity??-1,isDarkenGreyout:n.isDarkenGreyout??!1?1:0,backgroundColor:w(n.backgroundColor,[0,0,0,1]),greyoutColor:w(n.greyoutPointColor,[0,0,0,1]),width:.85}}),this.drawHighlightedCommand.setBindings({positionsTexture:this.currentPositionTexture,pointStatus:this.pointStatusTexture,exitTexture:this.exitTexture}),this.drawHighlightedCommand.draw(e)}if(n.focusedPoint&&this.drawHighlightedCommand&&this.drawHighlightedUniformStore){if(!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.pointStatusTexture||this.pointStatusTexture.destroyed||!this.exitTexture||this.exitTexture.destroyed)return;const f=s.getResolvedPointSize(n.focusedPoint.index),p=((o=s.pointImageSizes)==null?void 0:o[n.focusedPoint.index])??f;this.drawHighlightedUniformStore.setUniforms({drawHighlightedUniforms:{size:Math.max(f,p),transformationMatrix:n.transformationMatrix4x4,pointsTextureSize:n.pointsTextureSize??0,sizeScale:r.pointSizeScale,spaceSize:n.adjustedSpaceSize,screenSize:k(n.screenSize,[0,0]),scalePointsOnZoom:r.scalePointsOnZoom?1:0,pointIndex:n.focusedPoint.index,maxPointSize:n.maxPointSize,color:w(n.focusedPointRingColor,[0,0,0,1]),universalPointOpacity:r.pointOpacity,greyoutOpacity:r.pointGreyoutOpacity??-1,isDarkenGreyout:n.isDarkenGreyout??!1?1:0,backgroundColor:w(n.backgroundColor,[0,0,0,1]),greyoutColor:w(n.greyoutPointColor,[0,0,0,1]),width:.85}}),this.drawHighlightedCommand.setBindings({positionsTexture:this.currentPositionTexture,pointStatus:this.pointStatusTexture,exitTexture:this.exitTexture}),this.drawHighlightedCommand.draw(e)}}updatePosition(){if(!this.updatePositionCommand||!this.updatePositionUniformStore||!this.currentPositionFbo||this.currentPositionFbo.destroyed||!this.previousPositionTexture||this.previousPositionTexture.destroyed||!this.velocityTexture||this.velocityTexture.destroyed||!this.pinnedStatusTexture||this.pinnedStatusTexture.destroyed||(this.exitTexture||this.updateExit(),!this.exitTexture||this.exitTexture.destroyed))return;this.updatePositionUniformStore.setUniforms({updatePositionUniforms:{friction:this.config.simulationFriction,spaceSize:this.store.adjustedSpaceSize}}),this.updatePositionCommand.setBindings({positionsTexture:this.previousPositionTexture,velocity:this.velocityTexture,pinnedStatusTexture:this.pinnedStatusTexture,exitTexture:this.exitTexture});const e=this.device.beginRenderPass({framebuffer:this.currentPositionFbo});this.updatePositionCommand.draw(e),e.end(),this.isPositionsUpToDate=!1}drag(){var e;if(!this.dragPointCommand||!this.dragPointUniformStore||!this.currentPositionFbo||this.currentPositionFbo.destroyed||!this.previousPositionTexture||this.previousPositionTexture.destroyed)return;const t=this.store.is3D?[...this.store.mousePosition3D,0]:[this.store.mousePosition[0]??0,this.store.mousePosition[1]??0,0,0];this.dragPointUniformStore.setUniforms({dragPointUniforms:{mousePos:t,index:((e=this.store.hoveredPoint)==null?void 0:e.index)??-1}}),this.dragPointCommand.setBindings({positionsTexture:this.previousPositionTexture});const i=this.device.beginRenderPass({framebuffer:this.currentPositionFbo});this.dragPointCommand.draw(i),i.end(),this.isPositionsUpToDate=!1}findPointsInRect(){var e,t;if(!this.findPointsInRectCommand||!this.findPointsInRectUniformStore||!this.searchFbo||this.searchFbo.destroyed||!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.sizeTexture||this.sizeTexture.destroyed||(this.exitTexture||this.updateExit(),!this.exitTexture||this.exitTexture.destroyed))return!1;this.findPointsInRectUniformStore.setUniforms({findPointsInRectUniforms:{spaceSize:this.store.adjustedSpaceSize,screenSize:k(this.store.screenSize,[0,0]),sizeScale:this.config.pointSizeScale,transformationMatrix:this.store.transformationMatrix4x4,ratio:this.config.pixelRatio,rect0:k((e=this.store.searchArea)==null?void 0:e[0],[0,0]),rect1:k((t=this.store.searchArea)==null?void 0:t[1],[0,0]),scalePointsOnZoom:this.config.scalePointsOnZoom?1:0,maxPointSize:this.store.maxPointSize}}),this.findPointsInRectCommand.setBindings({positionsTexture:this.currentPositionTexture,pointSize:this.sizeTexture,exitTexture:this.exitTexture});const i=this.device.beginRenderPass({framebuffer:this.searchFbo});return this.findPointsInRectCommand.draw(i),i.end(),!0}findPointsInPolygon(){if(!this.findPointsInPolygonCommand||!this.findPointsInPolygonUniformStore||!this.searchFbo||this.searchFbo.destroyed||!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.polygonPathTexture||this.polygonPathTexture.destroyed||(this.exitTexture||this.updateExit(),!this.exitTexture||this.exitTexture.destroyed))return!1;this.findPointsInPolygonUniformStore.setUniforms({findPointsInPolygonUniforms:{spaceSize:this.store.adjustedSpaceSize,screenSize:k(this.store.screenSize,[0,0]),transformationMatrix:this.store.transformationMatrix4x4,polygonPathLength:this.polygonPathLength}}),this.findPointsInPolygonCommand.setBindings({positionsTexture:this.currentPositionTexture,polygonPathTexture:this.polygonPathTexture,exitTexture:this.exitTexture});const e=this.device.beginRenderPass({framebuffer:this.searchFbo});return this.findPointsInPolygonCommand.draw(e),e.end(),!0}updatePolygonPath(e){const{device:t}=this;if(this.polygonPathLength=e.length,e.length===0){this.polygonPathTexture&&!this.polygonPathTexture.destroyed&&this.polygonPathTexture.destroy(),this.polygonPathTexture=void 0;return}const i=Math.ceil(Math.sqrt(e.length)),o=new Float32Array(i*i*4);for(const[s,r]of e.entries()){const[n,a]=r;o[s*4]=n,o[s*4+1]=a,o[s*4+2]=0,o[s*4+3]=0}!this.polygonPathTexture||this.polygonPathTexture.width!==i||this.polygonPathTexture.height!==i?(this.polygonPathTexture&&!this.polygonPathTexture.destroyed&&this.polygonPathTexture.destroy(),this.polygonPathTexture=t.createTexture({width:i,height:i,format:"rgba32float"}),this.polygonPathTexture.copyImageData({data:o,bytesPerRow:y("rgba32float",i),mipLevel:0,x:0,y:0})):this.polygonPathTexture.copyImageData({data:o,bytesPerRow:y("rgba32float",i),mipLevel:0,x:0,y:0})}updatePickingBuffer(){if(!this.isPickingBufferStale||!this.ensurePickingBuffer()||!this.pickingFbo||this.pickingFbo.destroyed||!this.fillPickingBufferCommand||!this.fillPickingBufferUniformStore||!this.currentPositionTexture||this.currentPositionTexture.destroyed||(this.pointStatusTexture||this.updatePointStatus(),!this.pointStatusTexture||this.pointStatusTexture.destroyed)||!this.exitTexture||this.exitTexture.destroyed)return;this.fillPickingBufferCommand.setVertexCount(this.data.pointsNumber??0),this.fillPickingBufferCommand.setAttributes({...this.hoveredPointIndices&&{pointIndices:this.hoveredPointIndices},...this.targetSizeBuffer&&{size:this.targetSizeBuffer},...this.imageSizesBuffer&&{imageSize:this.imageSizesBuffer}});const e=k(this.store.screenSize,[0,0]),t={ratio:this.config.pixelRatio,sizeScale:this.config.pointSizeScale,pointsTextureSize:this.store.pointsTextureSize??0,transformationMatrix:this.store.transformationMatrix4x4,spaceSize:this.store.adjustedSpaceSize,screenSize:e,scalePointsOnZoom:this.config.scalePointsOnZoom?1:0,pickingPixelRatio:e[0]>0?this.pickingFbo.width/e[0]:ge,maxPointSize:this.store.maxPointSize,pointDefaultSize:this.config.pointDefaultSize},i={positionsTexture:this.currentPositionTexture,pointStatus:this.pointStatusTexture,exitTexture:this.exitTexture},o=this.device.beginRenderPass({framebuffer:this.pickingFbo,clearColor:[-1,0,0,0],clearDepth:1});this.config.highlightedPointIndices!==void 0?(this.fillPickingBufferUniformStore.setUniforms({fillPickingBufferUniforms:{...t,skipHighlighted:1,skipGreyed:0}}),this.fillPickingBufferCommand.setBindings(i),this.fillPickingBufferCommand.draw(o),this.fillPickingBufferUniformStore.setUniforms({fillPickingBufferUniforms:{...t,skipHighlighted:0,skipGreyed:1}}),this.fillPickingBufferCommand.setBindings(i),this.fillPickingBufferCommand.draw(o)):(this.fillPickingBufferUniformStore.setUniforms({fillPickingBufferUniforms:{...t,skipHighlighted:0,skipGreyed:0}}),this.fillPickingBufferCommand.setBindings(i),this.fillPickingBufferCommand.draw(o)),o.end(),this.isPickingBufferStale=!1}pickPointSync(){this.updatePickingBuffer();const e=this.getPickingWindow();if(!e||!this.pickingFbo||this.pickingFbo.destroyed)return;const t=B(this.device,this.pickingFbo,e.x,e.y,A,A);return this.resolvePickedPoint(t,e.centerX-e.x,e.centerY-e.y)}requestPickPoint(){var e;if((e=this.pickingReadback)!=null&&e.inFlight)return!1;if(this.updatePickingBuffer(),!this.pickingFbo||this.pickingFbo.destroyed)return!0;const t=this.device.gl,i=this.pickingFbo.handle;if(!t||!i)return!0;this.pickingReadback||(this.pickingReadback=new Ye(t,A*A*4));const o=this.getPickingWindow();return o?this.pickingReadback.issue(i,o.x,o.y,A,A)?(this.issuedPickingWindow=o,!0):!1:!0}discardPendingPick(){var e;(e=this.pickingReadback)==null||e.cancel(),this.issuedPickingWindow=void 0}takePickResult(){if(!this.pickingReadback||!this.issuedPickingWindow)return;const e=this.pickingReadback.poll();if(!e)return;const t=this.issuedPickingWindow;return this.issuedPickingWindow=void 0,this.resolvePickedPoint(e,t.centerX-t.x,t.centerY-t.y)??null}trackPointsByIndices(e){const{store:{pointsTextureSize:t},device:i}=this;if(this.trackedIndices=e,this.trackedPositions2D=void 0,this.trackedPositions3D=void 0,this.isPositionsUpToDate=!1,!(e!=null&&e.length)||!t)return;const o=Math.ceil(Math.sqrt(e.length)),s=new Float32Array(o*o*4).fill(-1);for(const[r,n]of e.entries())n!==void 0&&(s[r*4]=n%t,s[r*4+1]=Math.floor(n/t),s[r*4+2]=0,s[r*4+3]=0);!this.trackedIndicesTexture||this.trackedIndicesTexture.width!==o||this.trackedIndicesTexture.height!==o?(this.trackedIndicesTexture&&!this.trackedIndicesTexture.destroyed&&this.trackedIndicesTexture.destroy(),this.trackedIndicesTexture=i.createTexture({width:o,height:o,format:"rgba32float"}),this.trackedIndicesTexture.copyImageData({data:s,bytesPerRow:y("rgba32float",o),mipLevel:0,x:0,y:0})):this.trackedIndicesTexture.copyImageData({data:s,bytesPerRow:y("rgba32float",o),mipLevel:0,x:0,y:0}),(!this.trackedPositionsFbo||this.trackedPositionsFbo.width!==o||this.trackedPositionsFbo.height!==o)&&(this.trackedPositionsFbo&&!this.trackedPositionsFbo.destroyed&&this.trackedPositionsFbo.destroy(),this.trackedPositionsFbo=i.createFramebuffer({width:o,height:o,colorAttachments:["rgba32float"]})),this.trackPoints()}getTrackedPositionsMap(e=2){if(!this.trackedIndices)return new Map;const{config:{enableSimulation:t},store:{isSimulationRunning:i}}=this,o=e===3?this.trackedPositions3D:this.trackedPositions2D;if((!t||!i)&&this.isPositionsUpToDate&&o)return o;if(!this.trackedPositionsFbo||this.trackedPositionsFbo.destroyed)return new Map;const s=B(this.device,this.trackedPositionsFbo),r=new Map,n=new Map;for(let a=0;a<s.length/4;a+=1){const l=s[a*4],u=s[a*4+1],d=s[a*4+2],c=this.trackedIndices[a];if(l!==void 0&&u!==void 0&&c!==void 0){if(this.data.isPointAbsent(c))continue;r.set(c,[l,u]),n.set(c,[l,u,d??0])}}return(!t||!i)&&(this.trackedPositions2D=r,this.trackedPositions3D=n,this.isPositionsUpToDate=!0),e===3?n:r}getSampledPointPositionsMap(e=2){if(e===3){const o=new Map,s=this.fillAndReadSampledPointsFbo();if(!s)return o;for(let r=0;r<s.length/4;r++){const n=s[r*4],a=this.store.is3D?s[r*4+1]:0,l=s[r*4+2],u=s[r*4+3];n!==void 0&&n>=0&&l!==void 0&&u!==void 0&&o.set(n,[l,u,a??0])}return o}const t=new Map,i=this.fillAndReadSampledPointsFbo();if(!i)return t;for(let o=0;o<i.length/4;o++){const s=i[o*4],r=i[o*4+2],n=i[o*4+3];s!==void 0&&s>=0&&r!==void 0&&n!==void 0&&t.set(s,[r,n])}return t}getSampledPoints(e=2){const t=[],i=[],o=this.fillAndReadSampledPointsFbo();if(!o)return{indices:t,positions:i};for(let s=0;s<o.length/4;s++){const r=o[s*4],n=this.store.is3D?o[s*4+1]:0,a=o[s*4+2],l=o[s*4+3];r!==void 0&&r>=0&&a!==void 0&&l!==void 0&&(t.push(r),i.push(a,l),e===3&&i.push(n??0))}return{indices:t,positions:i}}getTrackedPositionsArray(e=2){const t=[];if(!this.trackedIndices||!this.trackedPositionsFbo||this.trackedPositionsFbo.destroyed)return t;t.length=this.trackedIndices.length*e;const i=B(this.device,this.trackedPositionsFbo);for(let o=0;o<i.length/4;o+=1){const s=i[o*4],r=i[o*4+1],n=i[o*4+2],a=this.trackedIndices[o];if(s!==void 0&&r!==void 0&&a!==void 0){if(this.data.isPointAbsent(a)){t[o*e]=NaN,t[o*e+1]=NaN,e===3&&(t[o*e+2]=NaN);continue}t[o*e]=s,t[o*e+1]=r,e===3&&(t[o*e+2]=n??0)}}return t}destroy(){var e,t,i,o,s,r,n,a,l,u,d,c,f,p,m,S,v,C,D,I,L,z;(e=this.drawCommand)==null||e.destroy(),this.drawCommand=void 0,(t=this.drawCoreCommand)==null||t.destroy(),this.drawCoreCommand=void 0,this.isOcclusionCullingActive=!1,(i=this.drawHighlightedCommand)==null||i.destroy(),this.drawHighlightedCommand=void 0,(o=this.interpolatePositionCommand)==null||o.destroy(),this.interpolatePositionCommand=void 0,(s=this.updatePositionCommand)==null||s.destroy(),this.updatePositionCommand=void 0,(r=this.dragPointCommand)==null||r.destroy(),this.dragPointCommand=void 0,(n=this.findPointsInRectCommand)==null||n.destroy(),this.findPointsInRectCommand=void 0,(a=this.findPointsInPolygonCommand)==null||a.destroy(),this.findPointsInPolygonCommand=void 0,(l=this.fillPickingBufferCommand)==null||l.destroy(),this.fillPickingBufferCommand=void 0,(u=this.fillSampledPointsFboCommand)==null||u.destroy(),this.fillSampledPointsFboCommand=void 0,(d=this.trackPointsCommand)==null||d.destroy(),this.trackPointsCommand=void 0,(c=this.pickingReadback)==null||c.destroy(),this.pickingReadback=void 0,this.issuedPickingWindow=void 0,this.currentPositionFbo&&!this.currentPositionFbo.destroyed&&this.currentPositionFbo.destroy(),this.currentPositionFbo=void 0,this.previousPositionFbo&&!this.previousPositionFbo.destroyed&&this.previousPositionFbo.destroy(),this.previousPositionFbo=void 0,this.sourcePositionFbo&&!this.sourcePositionFbo.destroyed&&this.sourcePositionFbo.destroy(),this.sourcePositionFbo=void 0,this.targetPositionFbo&&!this.targetPositionFbo.destroyed&&this.targetPositionFbo.destroy(),this.targetPositionFbo=void 0,this.velocityFbo&&!this.velocityFbo.destroyed&&this.velocityFbo.destroy(),this.velocityFbo=void 0,this.searchFbo&&!this.searchFbo.destroyed&&this.searchFbo.destroy(),this.searchFbo=void 0,this.pickingFbo&&!this.pickingFbo.destroyed&&this.pickingFbo.destroy(),this.pickingFbo=void 0,this.trackedPositionsFbo&&!this.trackedPositionsFbo.destroyed&&this.trackedPositionsFbo.destroy(),this.trackedPositionsFbo=void 0,this.sampledPointsFbo&&!this.sampledPointsFbo.destroyed&&this.sampledPointsFbo.destroy(),this.sampledPointsFbo=void 0,this.currentPositionTexture&&!this.currentPositionTexture.destroyed&&this.currentPositionTexture.destroy(),this.currentPositionTexture=void 0,this.previousPositionTexture&&!this.previousPositionTexture.destroyed&&this.previousPositionTexture.destroy(),this.previousPositionTexture=void 0,this.sourcePositionTexture&&!this.sourcePositionTexture.destroyed&&this.sourcePositionTexture.destroy(),this.sourcePositionTexture=void 0,this.targetPositionTexture&&!this.targetPositionTexture.destroyed&&this.targetPositionTexture.destroy(),this.targetPositionTexture=void 0,this.velocityTexture&&!this.velocityTexture.destroyed&&this.velocityTexture.destroy(),this.velocityTexture=void 0,this.searchTexture&&!this.searchTexture.destroyed&&this.searchTexture.destroy(),this.searchTexture=void 0,this.pickingTexture&&!this.pickingTexture.destroyed&&this.pickingTexture.destroy(),this.pickingTexture=void 0,this.pointStatusTexture&&!this.pointStatusTexture.destroyed&&this.pointStatusTexture.destroy(),this.pointStatusTexture=void 0,this.pointColorsTexture&&!this.pointColorsTexture.destroyed&&this.pointColorsTexture.destroy(),this.pointColorsTexture=void 0,this.sizeTexture&&!this.sizeTexture.destroyed&&this.sizeTexture.destroy(),this.sizeTexture=void 0,this.trackedIndicesTexture&&!this.trackedIndicesTexture.destroyed&&this.trackedIndicesTexture.destroy(),this.trackedIndicesTexture=void 0,this.polygonPathTexture&&!this.polygonPathTexture.destroyed&&this.polygonPathTexture.destroy(),this.polygonPathTexture=void 0,this.imageAtlasTexture&&!this.imageAtlasTexture.destroyed&&this.imageAtlasTexture.destroy(),this.imageAtlasTexture=void 0,this.imageAtlasCoordsTexture&&!this.imageAtlasCoordsTexture.destroyed&&this.imageAtlasCoordsTexture.destroy(),this.imageAtlasCoordsTexture=void 0,this.pinnedStatusTexture&&!this.pinnedStatusTexture.destroyed&&this.pinnedStatusTexture.destroy(),this.pinnedStatusTexture=void 0,this.exitTexture&&!this.exitTexture.destroyed&&this.exitTexture.destroy(),this.exitTexture=void 0,this.previousExitData=void 0,this.hasAnyAbsentPoint=!1,(f=this.interpolatePositionUniformStore)==null||f.destroy(),this.interpolatePositionUniformStore=void 0,(p=this.updatePositionUniformStore)==null||p.destroy(),this.updatePositionUniformStore=void 0,(m=this.dragPointUniformStore)==null||m.destroy(),this.dragPointUniformStore=void 0,(S=this.drawUniformStore)==null||S.destroy(),this.drawUniformStore=void 0,(v=this.findPointsInRectUniformStore)==null||v.destroy(),this.findPointsInRectUniformStore=void 0,(C=this.findPointsInPolygonUniformStore)==null||C.destroy(),this.findPointsInPolygonUniformStore=void 0,(D=this.fillPickingBufferUniformStore)==null||D.destroy(),this.fillPickingBufferUniformStore=void 0,(I=this.fillSampledPointsUniformStore)==null||I.destroy(),this.fillSampledPointsUniformStore=void 0,(L=this.drawHighlightedUniformStore)==null||L.destroy(),this.drawHighlightedUniformStore=void 0,(z=this.trackPointsUniformStore)==null||z.destroy(),this.trackPointsUniformStore=void 0,this.sourceColorBuffer&&!this.sourceColorBuffer.destroyed&&this.sourceColorBuffer.destroy(),this.sourceColorBuffer=void 0,this.targetColorBuffer&&!this.targetColorBuffer.destroyed&&this.targetColorBuffer.destroy(),this.targetColorBuffer=void 0,this.previousColorData=void 0,this.sourceSizeBuffer&&!this.sourceSizeBuffer.destroyed&&this.sourceSizeBuffer.destroy(),this.sourceSizeBuffer=void 0,this.targetSizeBuffer&&!this.targetSizeBuffer.destroyed&&this.targetSizeBuffer.destroy(),this.targetSizeBuffer=void 0,this.previousSizeData=void 0,this.shapeBuffer&&!this.shapeBuffer.destroyed&&this.shapeBuffer.destroy(),this.shapeBuffer=void 0,this.imageIndicesBuffer&&!this.imageIndicesBuffer.destroyed&&this.imageIndicesBuffer.destroy(),this.imageIndicesBuffer=void 0,this.imageSizesBuffer&&!this.imageSizesBuffer.destroyed&&this.imageSizesBuffer.destroy(),this.imageSizesBuffer=void 0,this.drawPointIndices&&!this.drawPointIndices.destroyed&&this.drawPointIndices.destroy(),this.drawPointIndices=void 0,this.reversedPointIndexBuffer&&!this.reversedPointIndexBuffer.destroyed&&this.reversedPointIndexBuffer.destroy(),this.reversedPointIndexBuffer=void 0,this.hoveredPointIndices&&!this.hoveredPointIndices.destroyed&&this.hoveredPointIndices.destroy(),this.hoveredPointIndices=void 0,this.sampledPointIndices&&!this.sampledPointIndices.destroyed&&this.sampledPointIndices.destroy(),this.sampledPointIndices=void 0,this.updatePositionVertexCoordBuffer&&!this.updatePositionVertexCoordBuffer.destroyed&&this.updatePositionVertexCoordBuffer.destroy(),this.updatePositionVertexCoordBuffer=void 0,this.interpolatePositionVertexCoordBuffer&&!this.interpolatePositionVertexCoordBuffer.destroyed&&this.interpolatePositionVertexCoordBuffer.destroy(),this.interpolatePositionVertexCoordBuffer=void 0,this.dragPointVertexCoordBuffer&&!this.dragPointVertexCoordBuffer.destroyed&&this.dragPointVertexCoordBuffer.destroy(),this.dragPointVertexCoordBuffer=void 0,this.findPointsInRectVertexCoordBuffer&&!this.findPointsInRectVertexCoordBuffer.destroyed&&this.findPointsInRectVertexCoordBuffer.destroy(),this.findPointsInRectVertexCoordBuffer=void 0,this.findPointsInPolygonVertexCoordBuffer&&!this.findPointsInPolygonVertexCoordBuffer.destroyed&&this.findPointsInPolygonVertexCoordBuffer.destroy(),this.findPointsInPolygonVertexCoordBuffer=void 0,this.drawHighlightedVertexCoordBuffer&&!this.drawHighlightedVertexCoordBuffer.destroyed&&this.drawHighlightedVertexCoordBuffer.destroy(),this.drawHighlightedVertexCoordBuffer=void 0,this.trackPointsVertexCoordBuffer&&!this.trackPointsVertexCoordBuffer.destroyed&&this.trackPointsVertexCoordBuffer.destroy(),this.trackPointsVertexCoordBuffer=void 0}ensureSimulationResources(){const{store:{pointsTextureSize:e},device:t}=this;if(!e)return;this.ensureUpdatePositionProgram();const i=new Float32Array(e*e*4).fill(0);!this.velocityTexture||this.velocityTexture.width!==e||this.velocityTexture.height!==e?(this.velocityFbo&&!this.velocityFbo.destroyed&&this.velocityFbo.destroy(),this.velocityTexture&&!this.velocityTexture.destroyed&&this.velocityTexture.destroy(),this.velocityTexture=t.createTexture({width:e,height:e,format:"rgba32float"}),this.velocityTexture.copyImageData({data:i,bytesPerRow:y("rgba32float",e),mipLevel:0,x:0,y:0}),this.velocityFbo=t.createFramebuffer({width:e,height:e,colorAttachments:[this.velocityTexture]})):this.velocityTexture.copyImageData({data:i,bytesPerRow:y("rgba32float",e),mipLevel:0,x:0,y:0})}createTransitionResources(){const{store:{pointsTextureSize:e},device:t}=this;if(!e)return;const i=new Float32Array(e*e*4).fill(0),o=g.SAMPLE|g.RENDER|g.COPY_SRC|g.COPY_DST;(!this.sourcePositionTexture||this.sourcePositionTexture.width!==e||this.sourcePositionTexture.height!==e)&&(this.sourcePositionFbo&&!this.sourcePositionFbo.destroyed&&this.sourcePositionFbo.destroy(),this.sourcePositionTexture&&!this.sourcePositionTexture.destroyed&&this.sourcePositionTexture.destroy(),this.sourcePositionTexture=t.createTexture({width:e,height:e,format:"rgba32float",usage:o}),this.sourcePositionFbo=t.createFramebuffer({width:e,height:e,colorAttachments:[this.sourcePositionTexture]})),this.sourcePositionTexture.copyImageData({data:i,bytesPerRow:y("rgba32float",e),mipLevel:0,x:0,y:0}),(!this.targetPositionTexture||this.targetPositionTexture.width!==e||this.targetPositionTexture.height!==e)&&(this.targetPositionFbo&&!this.targetPositionFbo.destroyed&&this.targetPositionFbo.destroy(),this.targetPositionTexture&&!this.targetPositionTexture.destroyed&&this.targetPositionTexture.destroy(),this.targetPositionTexture=t.createTexture({width:e,height:e,format:"rgba32float",usage:o}),this.targetPositionFbo=t.createFramebuffer({width:e,height:e,colorAttachments:[this.targetPositionTexture]})),this.targetPositionTexture.copyImageData({data:i,bytesPerRow:y("rgba32float",e),mipLevel:0,x:0,y:0}),this.interpolatePositionVertexCoordBuffer||(this.interpolatePositionVertexCoordBuffer=t.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.interpolatePositionUniformStore||(this.interpolatePositionUniformStore=new T(t,{interpolatePositionUniforms:{uniformTypes:{progress:"f32"},defaultUniforms:{progress:0}}})),this.interpolatePositionCommand||(this.interpolatePositionCommand=new b(t,{fs:Fi,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.interpolatePositionVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0},bindings:{interpolatePositionUniforms:this.interpolatePositionUniformStore.getManagedUniformBuffer("interpolatePositionUniforms")}}))}destroyTransitionResources(){var e,t;(e=this.interpolatePositionCommand)==null||e.destroy(),this.interpolatePositionCommand=void 0,(t=this.interpolatePositionUniformStore)==null||t.destroy(),this.interpolatePositionUniformStore=void 0,this.interpolatePositionVertexCoordBuffer&&!this.interpolatePositionVertexCoordBuffer.destroyed&&this.interpolatePositionVertexCoordBuffer.destroy(),this.interpolatePositionVertexCoordBuffer=void 0,this.sourcePositionFbo&&!this.sourcePositionFbo.destroyed&&this.sourcePositionFbo.destroy(),this.sourcePositionFbo=void 0,this.sourcePositionTexture&&!this.sourcePositionTexture.destroyed&&this.sourcePositionTexture.destroy(),this.sourcePositionTexture=void 0,this.targetPositionFbo&&!this.targetPositionFbo.destroyed&&this.targetPositionFbo.destroy(),this.targetPositionFbo=void 0,this.targetPositionTexture&&!this.targetPositionTexture.destroyed&&this.targetPositionTexture.destroy(),this.targetPositionTexture=void 0}interpolatePosition(e){if(!this.interpolatePositionCommand||!this.interpolatePositionUniformStore||!this.sourcePositionTexture||this.sourcePositionTexture.destroyed||!this.targetPositionTexture||this.targetPositionTexture.destroyed||!this.currentPositionFbo||this.currentPositionFbo.destroyed)return;this.interpolatePositionUniformStore.setUniforms({interpolatePositionUniforms:{progress:e}}),this.interpolatePositionCommand.setBindings({sourceTexture:this.sourcePositionTexture,targetTexture:this.targetPositionTexture});const t=this.device.beginRenderPass({framebuffer:this.currentPositionFbo});this.interpolatePositionCommand.draw(t),t.end(),this.isPositionsUpToDate=!1,this.areClusterCentroidsUpToDate=!1}destroySimulationResources(){var e,t;(e=this.updatePositionCommand)==null||e.destroy(),this.updatePositionCommand=void 0,(t=this.updatePositionUniformStore)==null||t.destroy(),this.updatePositionUniformStore=void 0,this.updatePositionVertexCoordBuffer&&!this.updatePositionVertexCoordBuffer.destroyed&&this.updatePositionVertexCoordBuffer.destroy(),this.updatePositionVertexCoordBuffer=void 0,this.velocityFbo&&!this.velocityFbo.destroyed&&this.velocityFbo.destroy(),this.velocityFbo=void 0,this.velocityTexture&&!this.velocityTexture.destroyed&&this.velocityTexture.destroy(),this.velocityTexture=void 0}swapFbo(){if(!this.currentPositionTexture||this.currentPositionTexture.destroyed||!this.previousPositionTexture||this.previousPositionTexture.destroyed||!this.currentPositionFbo||this.currentPositionFbo.destroyed||!this.previousPositionFbo||this.previousPositionFbo.destroyed)return;const e=this.previousPositionTexture,t=this.previousPositionFbo;this.previousPositionTexture=this.currentPositionTexture,this.previousPositionFbo=this.currentPositionFbo,this.currentPositionTexture=e,this.currentPositionFbo=t,this.areClusterCentroidsUpToDate=!1}ensurePositionTextures(e){(!this.currentPositionTexture||this.currentPositionTexture.width!==e||this.currentPositionTexture.height!==e)&&(this.currentPositionTexture&&!this.currentPositionTexture.destroyed&&this.currentPositionTexture.destroy(),this.currentPositionFbo&&!this.currentPositionFbo.destroyed&&this.currentPositionFbo.destroy(),this.currentPositionTexture=this.device.createTexture({width:e,height:e,format:"rgba32float"}),this.currentPositionFbo=this.device.createFramebuffer({width:e,height:e,colorAttachments:[this.currentPositionTexture]})),(!this.previousPositionTexture||this.previousPositionTexture.width!==e||this.previousPositionTexture.height!==e)&&(this.previousPositionTexture&&!this.previousPositionTexture.destroyed&&this.previousPositionTexture.destroy(),this.previousPositionFbo&&!this.previousPositionFbo.destroyed&&this.previousPositionFbo.destroy(),this.previousPositionTexture=this.device.createTexture({width:e,height:e,format:"rgba32float"}),this.previousPositionFbo=this.device.createFramebuffer({width:e,height:e,colorAttachments:[this.previousPositionTexture]}))}writePositionTexture(e,t,i){e.copyImageData({data:t,bytesPerRow:y("rgba32float",i),mipLevel:0,x:0,y:0})}ensurePickingBuffer(){var e;const{device:t,store:i}=this,[o,s]=i.screenSize;if(!o||!s)return!1;const r=Math.min(ge,Ri/Math.max(o,s)),n=Math.max(A,Math.ceil(o*r)),a=Math.max(A,Math.ceil(s*r));return this.pickingTexture&&!this.pickingTexture.destroyed&&this.pickingTexture.width===n&&this.pickingTexture.height===a||((e=this.pickingReadback)==null||e.cancel(),this.issuedPickingWindow=void 0,this.pickingFbo&&!this.pickingFbo.destroyed&&this.pickingFbo.destroy(),this.pickingTexture&&!this.pickingTexture.destroyed&&this.pickingTexture.destroy(),this.pickingTexture=t.createTexture({width:n,height:a,format:"rgba32float",usage:g.SAMPLE|g.RENDER}),this.pickingFbo=t.createFramebuffer({width:n,height:a,colorAttachments:[this.pickingTexture],depthStencilAttachment:"depth16unorm"}),this.isPickingBufferStale=!0),!0}getPickingWindow(){if(!this.pickingFbo||this.pickingFbo.destroyed)return;const[e,t]=this.store.screenSize;if(!e||!t)return;const i=this.store.screenMousePosition[0]*(this.pickingFbo.width/e),o=this.store.screenMousePosition[1]*(this.pickingFbo.height/t),s=Math.floor(A/2),r=Math.min(Math.max(Math.round(i)-s,0),this.pickingFbo.width-A),n=Math.min(Math.max(Math.round(o)-s,0),this.pickingFbo.height-A);return{x:r,y:n,centerX:i,centerY:o}}resolvePickedPoint(e,t,i){let o=-1,s=[0,0,0],r=1/0;for(let n=0;n<A;n+=1)for(let a=0;a<A;a+=1){const l=(n*A+a)*4,u=e[l];if(u<0)continue;const d=a+.5-t,c=n+.5-i,f=d*d+c*c;f<r&&(r=f,o=u,s=[e[l+1],e[l+2],e[l+3]])}if(!(o<0))return{index:o,position:this.store.is3D?s:[s[0],s[1]]}}ensureUpdatePositionProgram(){const{device:e,config:t,store:i}=this;this.updatePositionVertexCoordBuffer||(this.updatePositionVertexCoordBuffer=e.createBuffer({data:new Float32Array([-1,-1,1,-1,-1,1,1,1])})),this.updatePositionUniformStore||(this.updatePositionUniformStore=new T(e,{updatePositionUniforms:{uniformTypes:{friction:"f32",spaceSize:"f32"},defaultUniforms:{friction:t.simulationFriction,spaceSize:i.adjustedSpaceSize}}})),this.updatePositionCommand||(this.updatePositionCommand=new b(e,{fs:Di,vs:U,topology:"triangle-strip",vertexCount:4,attributes:{vertexCoord:this.updatePositionVertexCoordBuffer},bufferLayout:[{name:"vertexCoord",format:"float32x2"}],defines:{USE_UNIFORM_BUFFERS:!0,...i.is3D?{SPACE_3D:!0}:{}},bindings:{updatePositionUniforms:this.updatePositionUniformStore.getManagedUniformBuffer("updatePositionUniforms")}}))}fillAndReadSampledPointsFbo(){if(!(!this.sampledPointsFbo||this.sampledPointsFbo.destroyed)){if(this.fillSampledPointsFboCommand&&this.fillSampledPointsUniformStore){if(!this.currentPositionTexture||this.currentPositionTexture.destroyed||(this.fillSampledPointsFboCommand.setVertexCount(this.data.pointsNumber??0),this.exitTexture||this.updateExit(),!this.exitTexture||this.exitTexture.destroyed))return;this.fillSampledPointsUniformStore.setUniforms({fillSampledPointsUniforms:{pointsTextureSize:this.store.pointsTextureSize??0,transformationMatrix:this.store.transformationMatrix4x4,spaceSize:this.store.adjustedSpaceSize,screenSize:k(this.store.screenSize,[0,0])}}),this.fillSampledPointsFboCommand.setBindings({positionsTexture:this.currentPositionTexture,exitTexture:this.exitTexture});const e=this.device.beginRenderPass({framebuffer:this.sampledPointsFbo,clearColor:[-1,0,0,0]});this.fillSampledPointsFboCommand.draw(e),e.end()}return B(this.device,this.sampledPointsFbo)}}rescaleInitialNodePositions(){if(this.data.pointDimensions===3){this.rescaleInitialNodePositions3D();return}const{config:{spaceSize:e}}=this;if(!this.data.pointPositions||!e)return;const t=this.data.pointPositions,i=t.length/2;let o=1/0,s=-1/0,r=1/0,n=-1/0;for(let v=0;v<t.length;v+=2){const C=t[v],D=t[v+1];o=Math.min(o,C),s=Math.max(s,C),r=Math.min(r,D),n=Math.max(n,D)}const a=s-o,l=n-r,u=Math.max(a,l);if(u>e){this.scaleX=void 0,this.scaleY=void 0;return}const d=e*e*.001,c=i>d?e*Math.max(1.2,Math.sqrt(i)/e):e*.1,f=c/u,p=(e-c)/2,m=(u-a)/2*f+p,S=(u-l)/2*f+p;this.scaleX=v=>(v-o)*f+m,this.scaleY=v=>(v-r)*f+S;for(let v=0;v<i;v++)this.data.pointPositions[v*2]=this.scaleX(t[v*2]),this.data.pointPositions[v*2+1]=this.scaleY(t[v*2+1])}rescaleInitialNodePositions3D(){const{config:{spaceSize:e}}=this,t=this.data.pointPositions;if(!t||!e)return;this.scaleX=void 0,this.scaleY=void 0;const i=t.length/3;let o=1/0,s=-1/0,r=1/0,n=-1/0,a=1/0,l=-1/0;for(let m=0;m<t.length;m+=3){const S=t[m],v=t[m+1],C=t[m+2];o=Math.min(o,S),s=Math.max(s,S),r=Math.min(r,v),n=Math.max(n,v),a=Math.min(a,C),l=Math.max(l,C)}const u=Math.max(s-o,n-r,l-a);if(!(u>0)||u>e)return;const d=e*.8/u,c=(e-(s-o)*d)/2,f=(e-(n-r)*d)/2,p=(e-(l-a)*d)/2;for(let m=0;m<i;m++)t[m*3]=(t[m*3]-o)*d+c,t[m*3+1]=(t[m*3+1]-r)*d+f,t[m*3+2]=(t[m*3+2]-a)*d+p}updateReversedPointIndexBuffer(){var e,t;const{device:i,data:o,store:s}=this;if(s.is3D)return;const r=o.pointsNumber??0;if(r===0)return;const n=r*4;if(((e=this.reversedPointIndexBuffer)==null?void 0:e.byteLength)===n)return;const a=new Uint32Array(r);for(let l=0;l<r;l++)a[l]=r-1-l;this.reversedPointIndexBuffer&&!this.reversedPointIndexBuffer.destroyed&&this.reversedPointIndexBuffer.destroy(),this.reversedPointIndexBuffer=i.createBuffer({data:a,usage:x.INDEX|x.COPY_DST}),(t=this.drawCoreCommand)==null||t.setIndexBuffer(this.reversedPointIndexBuffer)}}class Oi{constructor(e,t){this.eventTransform=X,this.behavior=we().scaleExtent([.001,1/0]).on("start",i=>{var o,s;this.isRunning=!0;const r=!!i.sourceEvent;r&&(this.shouldEnableSimulationDuringZoomOverride=void 0),(s=(o=this.config).onZoomStart)==null||s.call(o,i,r)}).on("zoom",i=>{var o,s;this.eventTransform=i.transform;const{eventTransform:{x:r,y:n,k:a},store:{transform:l,screenSize:u}}=this,d=u[0],c=u[1];if(!d||!c)return;W.projection(l,d,c),W.translate(l,l,[r,n]),W.scale(l,l,[a,a]),W.translate(l,l,[d/2,c/2]),W.scale(l,l,[d/2,c/2]),W.scale(l,l,[1,-1]);const f=!!i.sourceEvent;(s=(o=this.config).onZoom)==null||s.call(o,i,f)}).on("end",i=>{var o,s;this.isRunning=!1;const r=!!i.sourceEvent;(s=(o=this.config).onZoomEnd)==null||s.call(o,i,r)}),this.isRunning=!1,this.shouldEnableSimulationDuringZoomOverride=void 0,this.store=e,this.config=t}getTransform(e,t,i=.1){if(e.length===0)return this.eventTransform;const{store:{screenSize:o}}=this,s=o[0],r=o[1];if(!(s>0)||!(r>0))return this.eventTransform;let n=1/0,a=-1/0,l=1/0,u=-1/0;for(let I=0;I<e.length;I+=2){const L=e[I],z=e[I+1];!Number.isFinite(L)||!Number.isFinite(z)||(L<n&&(n=L),L>a&&(a=L),z<l&&(l=z),z>u&&(u=z))}if(!Number.isFinite(n)||!Number.isFinite(l))return this.eventTransform;const d=[this.store.scaleX(n),this.store.scaleX(a)],c=[this.store.scaleY(l),this.store.scaleY(u)];d[0]===d[1]&&(d[0]-=.5,d[1]+=.5),c[0]===c[1]&&(c[0]+=.5,c[1]-=.5);const f=s*(1-i*2)/(d[1]-d[0]),p=r*(1-i*2)/(c[0]-c[1]),m=H(t??Math.min(f,p),...this.behavior.scaleExtent()),S=(d[1]+d[0])/2,v=(c[1]+c[0])/2,C=s/2-S*m,D=r/2-v*m;return X.translate(C,D).scale(m)}getDistanceToPoint(e){const{x:t,y:i,k:o}=this.eventTransform,s=this.getTransform(e,o),r=t-s.x,n=i-s.y;return Math.sqrt(r*r+n*n)}getMiddlePointTransform(e){if(!Number.isFinite(e[0])||!Number.isFinite(e[1]))return this.eventTransform;const{store:{screenSize:t},eventTransform:{x:i,y:o,k:s}}=this,r=t[0],n=t[1],a=(r/2-i)/s,l=(n/2-o)/s,u=this.store.scaleX(e[0]),d=this.store.scaleY(e[1]),c=(a+u)/2,f=(l+d)/2,p=1,m=r/2-c*p,S=n/2-f*p;return X.translate(m,S).scale(p)}convertScreenToSpacePosition(e){const{eventTransform:{x:t,y:i,k:o},store:{screenSize:s}}=this,r=s[0],n=s[1],a=(e[0]-t)/o,l=(e[1]-i)/o,u=[a,n-l];return u[0]-=(r-this.store.adjustedSpaceSize)/2,u[1]-=(n-this.store.adjustedSpaceSize)/2,u}convertSpaceToScreenPosition(e){const t=this.eventTransform.applyX(this.store.scaleX(e[0])),i=this.eventTransform.applyY(this.store.scaleY(e[1]));return[t,i]}convertSpaceToScreenRadius(e){const{config:{scalePointsOnZoom:t},store:{maxPointSize:i},eventTransform:{k:o}}=this;let s=e*2;return t?s*=o:s*=Math.min(5,Math.max(1,o*.01)),Math.min(s,i)/2}}class Vi{constructor(e,t,i){this.isActive=!1,this.behavior=Ut().subject(o=>{var s;if(this.transition.isActiveFor(F.Positions)||this.transition.isActiveFor(F.PointSizes))return;const r=((s=o.sourceEvent)==null?void 0:s.shiftKey)===!0;return this.store.hoveredPoint&&!this.store.isSpaceKeyPressed&&!r?{x:o.x,y:o.y}:void 0}).on("start",o=>{var s,r;this.store.hoveredPoint&&(this.store.draggingPointIndex=this.store.hoveredPoint.index,this.store.is3D&&this.store.hoveredPoint.position.length===3&&(this.store.dragPlanePoint3D=[...this.store.hoveredPoint.position],this.store.mousePosition3D=[...this.store.hoveredPoint.position]),this.isActive=!0,(r=(s=this.config).onDragStart)==null||r.call(s,o))}).on("drag",o=>{var s,r;(r=(s=this.config).onDrag)==null||r.call(s,o)}).on("end",o=>{var s,r;this.isActive=!1,this.store.draggingPointIndex=void 0,this.store.dragPlanePoint3D=void 0,(r=(s=this.config).onDragEnd)==null||r.call(s,o)}),this.store=e,this.config=t,this.transition=i}}const Z=.01,Je=.05,et=20;function tt(h,e){let t=1/0,i=-1/0,o=1/0,s=-1/0,r=1/0,n=-1/0;for(let f=0;f<h.length;f+=e){const p=h[f],m=h[f+1],S=e===3?h[f+2]:0;p<t&&(t=p),p>i&&(i=p),m<o&&(o=m),m>s&&(s=m),S<r&&(r=S),S>n&&(n=S)}if(t>i)return{center:P.create(),radius:1};const a=P.fromValues((t+i)/2,(o+s)/2,(r+n)/2),l=i-t,u=s-o,d=n-r,c=Math.max(Math.sqrt(l*l+u*u+d*d)/2,1e-6);return{center:a,radius:c}}class Gi{constructor(e,t){this.isRunning=!1,this.target=P.create(),this.distance=1,this.azimuth=0,this.polar=Math.PI/2,this.behavior=we().scaleExtent([.001,1/0]).on("start",i=>{var o,s,r;this.isRunning=!0,i.sourceEvent&&((o=this.canvasSelection)==null||o.interrupt("cosmosCameraFit"),this.baseDistance=this.distance*i.transform.k,this.behavior.scaleExtent([this.baseDistance/(this.sceneRadius*et),this.baseDistance/(this.sceneRadius*Je)])),(r=(s=this.config).onZoomStart)==null||r.call(s,i,!!i.sourceEvent)}).on("zoom",i=>{var o,s,r;const n=i.transform;if(i.sourceEvent){if(n.k!==this.previousTransform.k)this.distance=this.baseDistance/n.k;else{const a=n.x-this.previousTransform.x,l=n.y-this.previousTransform.y,u=((o=i.sourceEvent)==null?void 0:o.shiftKey)===!0;this.store.isSpaceKeyPressed||u?this.pan(a,l):this.rotate(a,l)}this.updateMatrices()}this.previousTransform=n,(r=(s=this.config).onZoom)==null||r.call(s,i,!!i.sourceEvent)}).on("end",i=>{var o,s;this.isRunning=!1,(s=(o=this.config).onZoomEnd)==null||s.call(o,i,!!i.sourceEvent)}),this.view=O.create(),this.projection=O.create(),this.viewProjection=O.create(),this.eye=P.create(),this.baseDistance=1,this.previousTransform=X,this.aspect=1,this.sceneRadius=1,this.store=e,this.config=t}get viewProjectionMatrix(){return Array.from(this.viewProjection)}setViewport(e,t){this.aspect=t===0?1:e/t,this.updateMatrices()}setOrbit(e,t,i,o){this.azimuth=e,this.polar=H(t,Z,Math.PI-Z),this.distance=i,P.copy(this.target,o),this.updateMatrices()}getState(){return{target:[this.target[0],this.target[1],this.target[2]],distance:this.distance,azimuth:this.azimuth,polar:this.polar}}setState(e,t,i=0){t?.interrupt("cosmosCameraFit");const o=this.getState(),s={...o,...e};if(s.distance=Math.max(s.distance,.001),s.polar=H(s.polar,Z,Math.PI-Z),i>0&&t){const r=P.fromValues(o.target[0],o.target[1],o.target[2]),n=P.fromValues(s.target[0],s.target[1],s.target[2]);t.transition("cosmosCameraFit").ease(J).duration(i).tween("cosmos-camera-state",()=>a=>{var l;P.lerp(this.target,r,n,a),this.distance=o.distance+(s.distance-o.distance)*a,this.azimuth=o.azimuth+(s.azimuth-o.azimuth)*a,this.polar=o.polar+(s.polar-o.polar)*a,this.updateMatrices(),(l=this.onUpdate)==null||l.call(this)}).on("end",()=>this.reseedZoomState(t));return}P.set(this.target,s.target[0],s.target[1],s.target[2]),this.distance=s.distance,this.azimuth=s.azimuth,this.polar=s.polar,this.updateMatrices(),t&&this.reseedZoomState(t)}setEyePosition(e,t,i){const{center:o,radius:s}=tt(t,i);this.sceneRadius=s;const r=P.sub(P.create(),P.fromValues(e[0],e[1],e[2]),o),n=Math.max(P.length(r),1e-6);this.setOrbit(Math.atan2(r[0],r[2]),Math.acos(H(r[1]/n,-1,1)),n,o)}getFitOrbit(e,t,i=.1){const{center:o,radius:s}=tt(e,t),r=this.config.cameraFov*Math.PI/180,n=2*Math.atan(Math.tan(r/2)*this.aspect),a=H(1-i*2,.1,1),l=s/Math.sin(Math.min(n,r)/2)/a;return{target:o,distance:l,radius:s}}setSceneRadius(e){this.sceneRadius=e}fitToPositions(e,t,i,o=.1,s=0){if(t.length===0)return;const{target:r,distance:n,radius:a}=this.getFitOrbit(t,i,o);if(this.sceneRadius=a,s===0)e.interrupt("cosmosCameraFit"),P.copy(this.target,r),this.distance=n,this.updateMatrices(),this.reseedZoomState(e);else{const l=P.clone(this.target),u=this.distance;e.transition("cosmosCameraFit").ease(J).duration(s).tween("cosmos-camera-fit",()=>d=>{var c;P.lerp(this.target,l,r,d),this.distance=u+(n-u)*d,this.updateMatrices(),(c=this.onUpdate)==null||c.call(this)}).on("end",()=>this.reseedZoomState(e))}}project(e){const[t,i]=this.store.screenSize,o=[0,0,0,0],s=this.viewProjection;for(let n=0;n<4;n+=1)o[n]=s[n]*e[0]+s[4+n]*e[1]+s[8+n]*e[2]+s[12+n];const r=o[3];return r<=0?[NaN,NaN]:[(o[0]/r+1)/2*t,(1-o[1]/r)/2*i]}unprojectOnPlane(e,t){const[i,o]=this.store.screenSize;if(!i||!o)return t;const s=O.invert(O.create(),this.viewProjection);if(!s)return t;const r=2*e[0]/i-1,n=1-2*e[1]/o,a=P.transformMat4(P.create(),[r,n,-1],s),l=P.transformMat4(P.create(),[r,n,1],s),u=P.normalize(P.create(),P.sub(P.create(),l,a)),d=P.normalize(P.create(),P.sub(P.create(),this.target,this.eye)),c=P.dot(d,u);if(Math.abs(c)<1e-9)return t;const f=P.fromValues(t[0],t[1],t[2]),p=P.dot(d,P.sub(P.create(),f,a))/c,m=P.scaleAndAdd(P.create(),a,u,p);return[m[0],m[1],m[2]]}updateMatrices(){const{cameraFov:e,cameraNear:t,cameraFar:i}=this.config,o=Math.sin(this.polar);P.set(this.eye,this.target[0]+this.distance*o*Math.sin(this.azimuth),this.target[1]+this.distance*Math.cos(this.polar),this.target[2]+this.distance*o*Math.cos(this.azimuth)),O.lookAt(this.view,this.eye,this.target,[0,1,0]);const s=t??Math.max(this.distance-this.sceneRadius*2,this.sceneRadius*.01),r=Math.max(i??this.distance+this.sceneRadius*2,s*1.01);O.perspective(this.projection,e*Math.PI/180,this.aspect,s,r),O.multiply(this.viewProjection,this.projection,this.view),this.store.viewProjection3D=this.viewProjectionMatrix,this.store.depthFadeRange[0]=Math.max(this.distance-this.sceneRadius,0),this.store.depthFadeRange[1]=this.distance+this.sceneRadius}reseedZoomState(e){this.baseDistance=this.distance,this.behavior.scaleExtent([this.baseDistance/(this.sceneRadius*et),this.baseDistance/(this.sceneRadius*Je)]),e.call(this.behavior.transform,X)}rotate(e,t){const i=this.store.screenSize[1]||1;this.azimuth-=2*Math.PI*e/i,this.polar=H(this.polar-2*Math.PI*t/i,Z,Math.PI-Z)}pan(e,t){const i=this.store.screenSize[1]||1,o=this.config.cameraFov*Math.PI/180,s=2*this.distance*Math.tan(o/2)/i,r=this.view;P.scaleAndAdd(this.target,this.target,[r[0],r[4],r[8]],-e*s),P.scaleAndAdd(this.target,this.target,[r[1],r[5],r[9]],t*s)}}const Wi=500,it=10;let Hi=0;const ot=h=>(!h.ctrlKey||h.type==="wheel")&&!h.button,ji=h=>ot(h)&&(h.touches===void 0||h.touches.length<2);class qi{constructor(e,t,i){if(this.config=Re(),this.graph=new Mt(this.config),this.isReady=!1,this.documentEventsNamespace=`cosmos-${Hi++}`,this.requestAnimationFrameId=0,this._longPressStartX=0,this._longPressStartY=0,this._shouldSuppressNextClick=!1,this.store=new At,this.zoomInstance=new Oi(this.store,this.config),this.transition=new Et(this.config),this.dragInstance=new Vi(this.store,this.config,this.transition),this.camera=new Gi(this.store,this.config),this._isCameraInitialized=!1,this._findHoveredItemExecutionCount=0,this._isPointerOnCanvas=!1,this._lastMouseX=0,this._lastMouseY=0,this._lastCheckedMouseX=0,this._lastCheckedMouseY=0,this._shouldForceHoverDetection=!1,this._lastPickingMatrix=[],this._isFirstRenderAfterInit=!0,this.isPointPositionsUpdateNeeded=!1,this.isPointColorUpdateNeeded=!1,this.isPointSizeUpdateNeeded=!1,this.isPointShapeUpdateNeeded=!1,this.isPointImageIndicesUpdateNeeded=!1,this.isLinksUpdateNeeded=!1,this.isLinkColorUpdateNeeded=!1,this.isLinkWidthUpdateNeeded=!1,this.isLinkArrowUpdateNeeded=!1,this.isLinkStyleUpdateNeeded=!1,this.isPointClusterUpdateNeeded=!1,this.isForceManyBodyUpdateNeeded=!1,this.isForceLinkUpdateNeeded=!1,this.isForceCenterUpdateNeeded=!1,this.isPointImageSizesUpdateNeeded=!1,this.isForceCollisionReady=!1,this._isDestroyed=!1,t&&fe(this.config,t),this.store.spaceDimensions=this.config.spaceDimensions,this.hasResizeWakeup=!i&&typeof ResizeObserver<"u",i)this.deviceInitPromise=i,this.shouldDestroyDevice=!1;else{const s=document.createElement("canvas");this.deviceInitPromise=this.createDevice(s),this.shouldDestroyDevice=!0}const o=this.deviceInitPromise.then(async s=>{var r;if(this._isDestroyed)return this.shouldDestroyDevice&&((r=s.canvasContext)==null||r.destroy(),s.destroy()),s;this.device=s;const n=this.validateDevice(s);i&&n.setProps({useDevicePixels:this.config.pixelRatio}),this.store.div=e;const a=n.canvas;if(a.parentNode!==this.store.div&&(a.parentNode&&a.parentNode.removeChild(a),this.store.div.appendChild(a)),this.addAttribution(),a.style.width="100%",a.style.height="100%",this.canvas=a,this.updateCanvasTouchAction(),await Promise.race([n.initialized,new Promise(d=>{setTimeout(d,500)})]),this._isDestroyed)return s;this.camera.onUpdate=()=>{this.requestRender()};const l=this.canvas.clientWidth,u=this.canvas.clientHeight;return this.store.adjustSpaceSize(this.config.spaceSize,this.device.limits.maxTextureDimension2D),this.store.setWebGLMaxTextureSize(this.device.limits.maxTextureDimension2D),this.store.updateScreenSize(l,u),this.store.is3D&&this.camera.setViewport(l,u),this.canvasD3Selection=N(this.canvas).on("pointerenter.cosmos",d=>{d.isPrimary&&(this._isPointerOnCanvas=!0,this._lastMouseX=d.clientX,this._lastMouseY=d.clientY,this.requestRender())}).on("pointermove.cosmos",d=>{var c,f,p,m;if(d.isPrimary){if(this._isPointerOnCanvas=!0,this._lastMouseX=d.clientX,this._lastMouseY=d.clientY,this.currentEvent=d,this.updateMousePosition(d),this._longPressTimerId!==void 0){const S=Math.abs(d.clientX-this._longPressStartX),v=Math.abs(d.clientY-this._longPressStartY);(S>it||v>it)&&this.cancelLongPress()}(m=(p=this.config).onMouseMove)==null||m.call(p,(c=this.store.hoveredPoint)==null?void 0:c.index,(f=this.store.hoveredPoint)==null?void 0:f.position,this.currentEvent),this.requestRender()}}).on("pointerleave.cosmos pointercancel.cosmos",d=>{d.isPrimary&&(this.cancelLongPress(),this._isPointerOnCanvas=!1,d.pointerType==="mouse"&&(this.currentEvent=d,this.store.hoveredPoint!==void 0&&this.config.onPointMouseOut&&this.config.onPointMouseOut(d),this.store.hoveredLinkIndex!==void 0&&this.config.onLinkMouseOut&&this.config.onLinkMouseOut(d),this.store.hoveredPoint=void 0,this.store.hoveredLinkIndex=void 0,this.lines&&(this.lines.isLinkIndexBufferStale=!0),this.updateCanvasCursor(),this.requestRender()))}).on("pointerdown.cosmos",d=>{d.isPrimary&&(this.currentEvent=d,this._shouldSuppressNextClick=!1,this._lastMouseX=d.clientX,this._lastMouseY=d.clientY,this.updateMousePosition(d),this.findHoveredItem(!0),this.requestRender(),d.pointerType!=="mouse"&&(this._longPressStartX=d.clientX,this._longPressStartY=d.clientY,this.cancelLongPress(),this._longPressTimerId=window.setTimeout(()=>{this._longPressTimerId=void 0,!this._isDestroyed&&(this.findHoveredItem(!0),this.requestRender(),this._shouldSuppressNextClick=!0,this.fireContextMenu(d))},Wi)))}).on("pointerup.cosmos",d=>{d.isPrimary&&this.cancelLongPress()}).on("click.cosmos",this.onClick.bind(this)).on("contextmenu.cosmos",this.onContextMenu.bind(this)),this.camera.canvasSelection=this.canvasD3Selection,N(document).on(`keydown.${this.documentEventsNamespace}`,d=>{d.code==="Space"&&(this.store.isSpaceKeyPressed=!0)}).on(`keyup.${this.documentEventsNamespace}`,d=>{d.code==="Space"&&(this.store.isSpaceKeyPressed=!1)}),this.zoomInstance.behavior.on("start.detect",d=>{this.currentEvent=d,this.requestRender()}).on("zoom.detect",d=>{d.sourceEvent&&this.updateMousePosition(d.sourceEvent),this.currentEvent=d,this.requestRender()}).on("end.detect",d=>{this.currentEvent=d,this._shouldForceHoverDetection=!0,this.requestRender()}),this.camera.behavior.on("start.detect",d=>{this.currentEvent=d,this.requestRender()}).on("zoom.detect",d=>{this.currentEvent=d,this.requestRender()}).on("end.detect",d=>{this.currentEvent=d,this._shouldForceHoverDetection=!0,this.requestRender()}),this.dragInstance.behavior.on("start.detect",d=>{this.currentEvent=d,this.dragInstance.isActive&&this.reheatSimulationOnDragStart(),this.updateCanvasCursor(),this.requestRender()}).on("drag.detect",d=>{this.dragInstance.isActive&&this.updateMousePosition(d),this.currentEvent=d,this.requestRender()}).on("end.detect",d=>{this.currentEvent=d,this.updateCanvasCursor(),this.requestRender()}),this.updateZoomDragBehaviors(),this.setZoomLevel(this.config.initialZoomLevel??1),this.store.maxPointSize=de(s,this.config.pixelRatio),this.store.isSimulationRunning=this.config.enableSimulation,this.points=new _i(s,this.config,this.store,this.graph),this.points.transition=this.transition,this.lines=new Si(s,this.config,this.store,this.graph,this.points),this.config.enableSimulation&&(this.forceGravity=new Ve(s,this.config,this.store,this.graph,this.points),this.forceCenter=new Ne(s,this.config,this.store,this.graph,this.points),this.forceManyBody=new je(s,this.config,this.store,this.graph,this.points),this.forceLinkIncoming=new se(s,this.config,this.store,this.graph,this.points),this.forceLinkOutgoing=new se(s,this.config,this.store,this.graph,this.points),this.forceCollision=new Oe(s,this.config,this.store,this.graph,this.points)),this.clusters=new hi(s,this.config,this.store,this.graph,this.points),this.store.backgroundColor=E(this.config.backgroundColor),this.store.setHoveredPointRingColor(this.config.hoveredPointRingColor),this.store.setFocusedPointRingColor(this.config.focusedPointRingColor),this.config.focusedPointIndex!==void 0&&this.store.setFocusedPoint(this.config.focusedPointIndex),this.store.setGreyoutPointColor(this.config.pointGreyoutColor),this.store.setOutlinedPointRingColor(this.config.outlinedPointRingColor),this.store.setHighlightedPointSet(this.config.highlightedPointIndices),this.store.setOutlinedPointSet(this.config.outlinedPointIndices),this.store.setHoveredLinkColor(this.config.hoveredLinkColor),this.store.updateLinkHoveringEnabled(this.config),this.config.showFPSMonitor&&(this.fpsMonitor=new qe(this.canvas)),this.config.randomSeed!==void 0&&this.store.addRandomSeed(this.config.randomSeed),this.isReady=!0,s}).catch(s=>{throw this.device=void 0,this.isReady=!1,console.error("Device initialization failed:",s),s});this.ready=o.then(()=>{})}get progress(){return this._isDestroyed?0:this.store.simulationProgress}get isSimulationRunning(){return this._isDestroyed?!1:this.store.isSimulationRunning}get maxPointSize(){return this._isDestroyed?0:this.store.maxPointSize}get is3D(){return this.store.is3D}setConfig(e){if(this._isDestroyed||this.ensureDevice(()=>this.setConfig(e)))return;const t={...this.config};_t(this.config),fe(this.config,e),e.spaceDimensions===void 0&&(this.config.spaceDimensions=t.spaceDimensions),this.preserveInitOnlyFields(t),this.updateStateFromConfig(t)}setConfigPartial(e){if(this._isDestroyed||this.ensureDevice(()=>this.setConfigPartial(e)))return;const t={...this.config};fe(this.config,e,!0),this.preserveInitOnlyFields(t),this.updateStateFromConfig(t)}setPointPositions(e,t){if(this._isDestroyed||this.ensureDevice(()=>this.setPointPositions(e,t)))return;const{dimensions:i=2,dontRescale:o}=t??{};let s=e;s.length%i!==0&&(console.warn(`cosmos.gl: \`setPointPositions\` expects ${i} coordinates per point; truncating the incomplete trailing point`),s=s.subarray(0,s.length-s.length%i)),this.graph.inputPointPositions=s,this.graph.inputPointDimensions=i,this.points.shouldSkipRescale=o,this.markPointPositionsDirty(),this.maybeInitializeCamera()}setPointColors(e){this._isDestroyed||this.ensureDevice(()=>this.setPointColors(e))||(this.graph.inputPointColors=e,this.isPointColorUpdateNeeded=!0,this.transition.queue(F.PointColors))}getPointColors(){if(this._isDestroyed)return new Float32Array;if(this.graph.pointColors===void 0||this.graph.pointsNumber===void 0)return new Float32Array;const e=new Float32Array(this.graph.pointsNumber*4);for(let t=0;t<this.graph.pointsNumber;t++)for(let i=0;i<4;i++)e[t*4+i]=this.graph.getResolvedPointColorChannel(t,i);return e}setPointSizes(e){this._isDestroyed||this.ensureDevice(()=>this.setPointSizes(e))||(this.graph.inputPointSizes=e,this.isPointSizeUpdateNeeded=!0,this.transition.queue(F.PointSizes))}setPointShapes(e){this._isDestroyed||this.ensureDevice(()=>this.setPointShapes(e))||(this.graph.inputPointShapes=e,this.isPointShapeUpdateNeeded=!0)}setImageData(e){var t;this._isDestroyed||this.ensureDevice(()=>this.setImageData(e))||(this.graph.inputImageData=e,(t=this.points)==null||t.createAtlas(),this.requestRender())}setPointImageIndices(e){this._isDestroyed||this.ensureDevice(()=>this.setPointImageIndices(e))||(this.graph.inputPointImageIndices=e,this.isPointImageIndicesUpdateNeeded=!0)}setPointImageSizes(e){this._isDestroyed||this.ensureDevice(()=>this.setPointImageSizes(e))||(this.graph.inputPointImageSizes=e,this.isPointImageSizesUpdateNeeded=!0)}getPointSizes(){if(this._isDestroyed)return new Float32Array;if(this.graph.pointSizes===void 0||this.graph.pointsNumber===void 0)return new Float32Array;const e=new Float32Array(this.graph.pointsNumber);for(let t=0;t<this.graph.pointsNumber;t++)e[t]=this.graph.getResolvedPointSize(t);return e}setLinks(e){if(this._isDestroyed||this.ensureDevice(()=>this.setLinks(e)))return;let t=e;t.length%2!==0&&(console.warn("cosmos.gl: `setLinks` expects 2 point indices per link; truncating the incomplete trailing link"),t=t.subarray(0,t.length-1)),this.graph.inputLinks=t,this.isLinksUpdateNeeded=!0,this.isLinkColorUpdateNeeded=!0,this.isLinkWidthUpdateNeeded=!0,this.isLinkArrowUpdateNeeded=!0,this.isLinkStyleUpdateNeeded=!0,this.isForceLinkUpdateNeeded=!0}setLinkColors(e){this._isDestroyed||this.ensureDevice(()=>this.setLinkColors(e))||(this.graph.inputLinkColors=e,this.isLinkColorUpdateNeeded=!0,this.transition.queue(F.LinkColors))}getLinkColors(){return this._isDestroyed?new Float32Array:this.graph.linkColors??new Float32Array}setLinkWidths(e){this._isDestroyed||this.ensureDevice(()=>this.setLinkWidths(e))||(this.graph.inputLinkWidths=e,this.isLinkWidthUpdateNeeded=!0,this.transition.queue(F.LinkWidths))}getLinkWidths(){return this._isDestroyed?new Float32Array:this.graph.linkWidths??new Float32Array}setLinkArrows(e){this._isDestroyed||this.ensureDevice(()=>this.setLinkArrows(e))||(this.graph.linkArrowsBoolean=e,this.isLinkArrowUpdateNeeded=!0)}setLinkStyles(e){this._isDestroyed||this.ensureDevice(()=>this.setLinkStyles(e))||(this.graph.inputLinkStyles=e,this.isLinkStyleUpdateNeeded=!0)}getLinkStyles(){return this._isDestroyed?new Float32Array:this.graph.linkStyles??new Float32Array}setLinkStrength(e){this._isDestroyed||this.ensureDevice(()=>this.setLinkStrength(e))||(this.graph.inputLinkStrength=e,this.isForceLinkUpdateNeeded=!0)}setPointClusters(e){this._isDestroyed||this.ensureDevice(()=>this.setPointClusters(e))||(this.graph.inputPointClusters=e,this.isPointClusterUpdateNeeded=!0)}setClusterPositions(e,t){this._isDestroyed||this.ensureDevice(()=>this.setClusterPositions(e,t))||(this.graph.inputClusterPositions=e,this.graph.inputClusterPositionsDimensions=t?.dimensions??2,this.isPointClusterUpdateNeeded=!0)}setPointClusterStrength(e){this._isDestroyed||this.ensureDevice(()=>this.setPointClusterStrength(e))||(this.graph.inputClusterStrength=e,this.isPointClusterUpdateNeeded=!0)}setPinnedPoints(e){var t;this._isDestroyed||this.ensureDevice(()=>this.setPinnedPoints(e))||(this.graph.inputPinnedPoints=e&&e.length>0?e:void 0,(t=this.points)==null||t.updatePinnedStatus(),this.requestRender())}render(e,t){var i,o,s;if(this._isDestroyed||this.ensureDevice(()=>this.render(e,t)))return;this.graph.update();const{fitViewOnInit:r,fitViewDelay:n,fitViewPadding:a,fitViewDuration:l,fitViewByPointsInRect:u,fitViewByPointIndices:d,initialZoomLevel:c}=this.config;if(!this.graph.pointsNumber&&!this.graph.linksNumber){this.stopFrames(),N(this.canvas).style("cursor",null),this.device&&(this.device.beginRenderPass({clearColor:this.store.backgroundColor,clearDepth:1,clearStencil:0}).end(),this.device.submit());return}this._isFirstRenderAfterInit&&r&&c===void 0&&(this._fitViewOnInitTimeoutID=window.setTimeout(()=>{d?this.fitViewByPointIndices(d,l,a):u&&!this.store.is3D?this.setZoomTransformByPointPositions(new Float32Array(this.flatten(u)),l,void 0,a):this.fitView(l,a)},n)),this.transition.setDurationOverride(t),this.update(e),this.transition.isPendingFor(F.Positions)&&this.store.isSimulationRunning&&this.transition.duration>0&&!this._isFirstRenderAfterInit&&(this.store.isSimulationRunning=!1,(o=(i=this.config).onSimulationPause)==null||o.call(i));const f=(s=this.points)==null?void 0:s.currentPositionTexture;this.transition.isPending&&(!f||f.destroyed)&&this.transition.abort(),this.transition.start(),this._shouldForceHoverDetection=!0,this.requestRender(),this._isFirstRenderAfterInit=!1}zoomToPointByIndex(e,t=700,i=3,o=!0,s=!0){if(this._isDestroyed||this.ensureDevice(()=>this.zoomToPointByIndex(e,t,i,o,s))||this.warnIf3D("zoomToPointByIndex")||!this.device||!this.points||!this.canvasD3Selection||this.graph.isPointAbsent(e))return;const{store:{screenSize:r}}=this,n=B(this.device,this.points.currentPositionFbo);if(e===void 0)return;const a=n[e*4+0],l=n[e*4+1];if(a===void 0||l===void 0)return;const u=this.zoomInstance.getDistanceToPoint([a,l]),d=o?i:Math.max(this.getZoomLevel(),i);if(u<Math.min(r[0],r[1]))this.setZoomTransformByPointPositions(new Float32Array([a,l]),t,d,void 0,s);else{this.zoomInstance.shouldEnableSimulationDuringZoomOverride=s;const c=this.zoomInstance.getTransform([a,l],d),f=this.zoomInstance.getMiddlePointTransform([a,l]);this.canvasD3Selection.transition().ease(be).duration(t/2).call(this.zoomInstance.behavior.transform,f).transition().ease(Te).duration(t/2).call(this.zoomInstance.behavior.transform,c)}}zoom(e,t=0,i=!0){this._isDestroyed||this.setZoomLevel(e,t,i)}setZoomLevel(e,t=0,i=!0){this._isDestroyed||this.ensureDevice(()=>this.setZoomLevel(e,t,i))||this.warnIf3D("setZoomLevel")||this.canvasD3Selection&&(this.zoomInstance.shouldEnableSimulationDuringZoomOverride=i,t===0?this.canvasD3Selection.call(this.zoomInstance.behavior.scaleTo,e):this.canvasD3Selection.transition().duration(t).call(this.zoomInstance.behavior.scaleTo,e))}getZoomLevel(){return this._isDestroyed||this.warnIf3D("getZoomLevel")?0:this.zoomInstance.eventTransform.k}getPointPositions(e){if(this._isDestroyed||!this.device||!this.points)return[];if(this.graph.pointsNumber===void 0)return[];const t=e?.dimensions??2,i=[],o=B(this.device,this.points.currentPositionFbo);i.length=this.graph.pointsNumber*t;for(let s=0;s<this.graph.pointsNumber;s+=1){if(this.graph.isPointAbsent(s)){i[s*t]=NaN,i[s*t+1]=NaN,t===3&&(i[s*t+2]=NaN);continue}const r=o[s*4+0],n=o[s*4+1];r!==void 0&&n!==void 0&&(i[s*t]=r,i[s*t+1]=n,t===3&&(i[s*t+2]=o[s*4+3]??0))}return i}getClusterPositions(e){return this._isDestroyed||!this.device||!this.clusters?[]:this.graph.pointClusters===void 0||this.clusters.clusterCount===void 0?[]:this.clusters.getCentroidPositions(e?.dimensions??2)}fitView(e=250,t=.1,i=!0){if(!this._isDestroyed&&!this.ensureDevice(()=>this.fitView(e,t,i))){if(this.store.is3D){this.canvasD3Selection&&(this.camera.fitToPositions(this.canvasD3Selection,this.getFitViewPositions3D(),3,t,e),this.requestRender());return}this.setZoomTransformByPointPositions(this.getFitViewPositions(),e,void 0,t,i)}}fitViewByPointIndices(e,t=250,i=.1,o=!0){if(this._isDestroyed||this.ensureDevice(()=>this.fitViewByPointIndices(e,t,i,o)))return;if(this.store.is3D){const n=this.getFitViewPositions3D(),a=new Float32Array(e.length*3);for(const[l,u]of e.entries())a[l*3]=n[u*3],a[l*3+1]=n[u*3+1],a[l*3+2]=n[u*3+2];this.canvasD3Selection&&(this.camera.fitToPositions(this.canvasD3Selection,a,3,i,t),this.requestRender());return}const s=this.getFitViewPositions(),r=new Float32Array(e.length*2);for(const[n,a]of e.entries())r[n*2]=s[a*2],r[n*2+1]=s[a*2+1];this.setZoomTransformByPointPositions(r,t,void 0,i,o)}fitViewByPointPositions(e,t=250,i=.1,o=!0){if(!this._isDestroyed&&!this.ensureDevice(()=>this.fitViewByPointPositions(e,t,i,o))){if(this.store.is3D){this.canvasD3Selection&&(this.camera.fitToPositions(this.canvasD3Selection,e,3,i,t),this.requestRender());return}this.setZoomTransformByPointPositions(new Float32Array(e),t,void 0,i,o)}}setZoomTransformByPointPositions(e,t=250,i,o=.1,s=!0){var r,n;if(this._isDestroyed||this.ensureDevice(()=>this.setZoomTransformByPointPositions(e,t,i,o,s))||this.warnIf3D("setZoomTransformByPointPositions","use `fitViewByPointPositions` instead"))return;this.zoomInstance.shouldEnableSimulationDuringZoomOverride=s,this.resizeCanvas();const a=this.zoomInstance.getTransform(e,i,o);t<=0?(r=this.canvasD3Selection)==null||r.call(this.zoomInstance.behavior.transform,a):(n=this.canvasD3Selection)==null||n.transition().ease(J).duration(t).call(this.zoomInstance.behavior.transform,a)}findPointsInRect(e){if(this._isDestroyed)return[];if(this.warnIf3D("findPointsInRect"))return[];if(!this.isReady||!this.device||!this.points)return[];const t=this.store.screenSize[1];if(this.store.searchArea=[[e[0][0],t-e[1][1]],[e[1][0],t-e[0][1]]],!this.points.findPointsInRect())return[];const i=this.graph.pointsNumber??0;return le(B(this.device,this.points.searchFbo)).filter(o=>o<i)}findPointsInPolygon(e){if(this._isDestroyed)return[];if(this.warnIf3D("findPointsInPolygon"))return[];if(!this.isReady||!this.device||!this.points)return[];if(e.length<3)return console.warn("Polygon path requires at least 3 points to form a polygon."),[];const t=this.store.screenSize[1],i=e.map(([s,r])=>[s,t-r]);if(this.points.updatePolygonPath(i),!this.points.findPointsInPolygon())return[];const o=this.graph.pointsNumber??0;return le(B(this.device,this.points.searchFbo)).filter(s=>s<o)}getNeighboringPointIndices(e){return this._isDestroyed?[]:this.graph.getNeighboringPointIndices(e)}getConnectedLinkIndices(e){return this._isDestroyed?[]:this.graph.getConnectedLinkIndices(e)}getConnectedPointIndices(e){return this._isDestroyed?[]:this.graph.getConnectedPointIndices(e)}spaceToScreenPosition(e,t){return this._isDestroyed?[0,0]:(t?.dimensions??2)===3?this.store.is3D?this.camera.project(e):(console.warn("cosmos.gl: `spaceToScreenPosition` with `{ dimensions: 3 }` is only available in 3D mode"),[0,0]):this.store.is3D?(console.warn("cosmos.gl: `spaceToScreenPosition` in 3D mode requires `{ dimensions: 3 }`"),[0,0]):this.zoomInstance.convertSpaceToScreenPosition(e)}getCameraState(){if(!(this._isDestroyed||!this.store.is3D))return this.camera.getState()}setCameraState(e,t=0){if(!this._isDestroyed){if(!this.store.is3D){console.warn("cosmos.gl: `setCameraState` is only available in 3D mode");return}this.camera.setState(e,this.canvasD3Selection,t),this.requestRender()}}screenToSpacePosition(e,t){if(this._isDestroyed)return(t?.dimensions??2)===3?[0,0,0]:[0,0];if((t?.dimensions??2)===3){if(!this.store.is3D)return console.warn("cosmos.gl: `screenToSpacePosition` with `{ dimensions: 3 }` is only available in 3D mode"),[0,0,0];const i=this.camera.target;return this.camera.unprojectOnPlane(e,[i[0],i[1],i[2]])}return this.store.is3D?(console.warn("cosmos.gl: `screenToSpacePosition` in 3D mode requires `{ dimensions: 3 }`"),[0,0]):this.zoomInstance.convertScreenToSpacePosition(e)}spaceToScreenRadius(e){return this._isDestroyed||this.warnIf3D("spaceToScreenRadius")?0:this.zoomInstance.convertSpaceToScreenRadius(e)}getPointRadiusByIndex(e){var t;if(this._isDestroyed||this.graph.pointSizes===void 0&&this.graph.pointImageSizes===void 0||e<0||e>=(this.graph.pointsNumber??0))return;const i=this.graph.getResolvedPointSize(e),o=(t=this.graph.pointImageSizes)==null?void 0:t[e];return Math.max(i,o??0)}trackPointPositionsByIndices(e){this._isDestroyed||this.ensureDevice(()=>this.trackPointPositionsByIndices(e))||this.points&&this.points.trackPointsByIndices(e)}getTrackedPointPositionsMap(e){return this._isDestroyed||!this.points?new Map:(e?.dimensions??2)===3?this.points.getTrackedPositionsMap(3):this.points.getTrackedPositionsMap(2)}getTrackedPointPositionsArray(e){return this._isDestroyed||!this.points?[]:this.points.getTrackedPositionsArray(e?.dimensions??2)}getSampledPointPositionsMap(e){return this._isDestroyed||!this.points?new Map:(e?.dimensions??2)===3?this.points.getSampledPointPositionsMap(3):this.points.getSampledPointPositionsMap(2)}getSampledPoints(e){return this._isDestroyed||!this.points?{indices:[],positions:[]}:this.points.getSampledPoints(e?.dimensions??2)}getSampledLinkPositionsMap(e){return this._isDestroyed||!this.lines?new Map:(e?.dimensions??2)===3?this.lines.getSampledLinkPositionsMap(3):this.lines.getSampledLinkPositionsMap(2)}getSampledLinks(e){return this._isDestroyed||!this.lines?{indices:[],positions:[],angles:[]}:this.lines.getSampledLinks(e?.dimensions??2)}getScaleX(){if(!(this._isDestroyed||!this.points))return this.points.scaleX}getScaleY(){if(!(this._isDestroyed||!this.points))return this.points.scaleY}start(e=1){var t,i;if(this._isDestroyed||this.ensureDevice(()=>this.start(e))||!this.config.enableSimulation||!this.graph.pointsNumber)return;this.transition.isActiveFor(F.Positions)&&this.transition.end(!0);const o=this.store.isSimulationRunning;this.store.isSimulationRunning=!0,this.store.simulationProgress=0,this.store.alpha=e,o||(i=(t=this.config).onSimulationStart)==null||i.call(t),this.requestRender()}stop(){var e,t;if(this._isDestroyed)return;const i=this.store.isSimulationRunning||this.store.alpha>0||this.store.simulationProgress>0;this.store.isSimulationRunning=!1,this.store.simulationProgress=0,this.store.alpha=0,i&&((t=(e=this.config).onSimulationEnd)==null||t.call(e))}pause(){var e,t;this._isDestroyed||this.ensureDevice(()=>this.pause())||this.store.isSimulationRunning&&(this.store.isSimulationRunning=!1,(t=(e=this.config).onSimulationPause)==null||t.call(e))}unpause(){var e,t;this._isDestroyed||this.ensureDevice(()=>this.unpause())||this.config.enableSimulation&&(this.store.isSimulationRunning||(this.transition.isActiveFor(F.Positions)&&this.transition.end(!0),this.store.isSimulationRunning=!0,(t=(e=this.config).onSimulationUnpause)==null||t.call(e),this.requestRender()))}step(){this._isDestroyed||this.ensureDevice(()=>this.step())||this.config.enableSimulation&&this.store.pointsTextureSize&&(this.runSimulationStep(!0),this.requestRender())}destroy(){var e,t,i,o,s,r,n,a,l,u,d,c,f,p;this._isDestroyed||(this._isDestroyed=!0,this.isReady=!1,this.transition.abort(),window.clearTimeout(this._fitViewOnInitTimeoutID),this.cancelLongPress(),this.stopFrames(),this.canvasD3Selection&&this.canvasD3Selection.on(".cosmos",null).on(".drag",null).on(".zoom",null),N(document).on(`.${this.documentEventsNamespace}`,null),(e=this.zoomInstance)!=null&&e.behavior&&this.zoomInstance.behavior.on("start.detect",null).on("zoom.detect",null).on("end.detect",null),(t=this.dragInstance)!=null&&t.behavior&&this.dragInstance.behavior.on("start.detect",null).on("drag.detect",null).on("end.detect",null),(i=this.fpsMonitor)==null||i.destroy(),(o=this.points)==null||o.destroy(),(s=this.lines)==null||s.destroy(),(r=this.clusters)==null||r.destroy(),(n=this.forceGravity)==null||n.destroy(),(a=this.forceCenter)==null||a.destroy(),(l=this.forceManyBody)==null||l.destroy(),(u=this.forceLinkIncoming)==null||u.destroy(),(d=this.forceLinkOutgoing)==null||d.destroy(),(c=this.forceCollision)==null||c.destroy(),this.device&&this.shouldDestroyDevice&&(this.device.beginRenderPass({clearColor:this.store.backgroundColor,clearDepth:1,clearStencil:0}).end(),this.device.submit(),(f=this.device.canvasContext)==null||f.destroy(),this.device.destroy()),this.shouldDestroyDevice&&this.canvas&&this.canvas.parentNode&&this.canvas.parentNode.removeChild(this.canvas),this.attributionDivElement&&this.attributionDivElement.parentNode&&this.attributionDivElement.parentNode.removeChild(this.attributionDivElement),(p=document.getElementById("gl-bench-style"))==null||p.remove(),this.canvasD3Selection=void 0,this.camera.canvasSelection=void 0,this.attributionDivElement=void 0)}create(){var e,t,i,o,s;this._isDestroyed||this.ensureDevice(()=>this.create())||this.points&&this.lines&&(this.isPointPositionsUpdateNeeded&&(this.points.updatePositions(),this.lines.isLinkIndexBufferStale=!0),this.isPointColorUpdateNeeded&&this.points.updateColor(),this.isPointSizeUpdateNeeded&&this.points.updateSize(),this.isPointShapeUpdateNeeded&&this.points.updateShape(),this.isPointImageIndicesUpdateNeeded&&this.points.updateImageIndices(),this.isPointImageSizesUpdateNeeded&&this.points.updateImageSizes(),this.isLinksUpdateNeeded&&this.lines.updatePointsBuffer(),this.isLinkColorUpdateNeeded&&this.lines.updateColor(),this.isLinkWidthUpdateNeeded&&this.lines.updateWidth(),this.isLinkArrowUpdateNeeded&&this.lines.updateArrow(),this.isLinkStyleUpdateNeeded&&this.lines.updateStyle(),this.isForceManyBodyUpdateNeeded&&((e=this.forceManyBody)==null||e.create()),(this.isForceManyBodyUpdateNeeded||this.isPointSizeUpdateNeeded)&&(this.isForceCollisionReady=!1),this.isForceLinkUpdateNeeded&&((t=this.forceLinkIncoming)==null||t.create(pe.INCOMING),(i=this.forceLinkOutgoing)==null||i.create(pe.OUTGOING)),this.isForceCenterUpdateNeeded&&((o=this.forceCenter)==null||o.create()),this.isPointClusterUpdateNeeded&&((s=this.clusters)==null||s.create()),this.isPointPositionsUpdateNeeded=!1,this.isPointColorUpdateNeeded=!1,this.isPointSizeUpdateNeeded=!1,this.isPointShapeUpdateNeeded=!1,this.isPointImageIndicesUpdateNeeded=!1,this.isPointImageSizesUpdateNeeded=!1,this.isLinksUpdateNeeded=!1,this.isLinkColorUpdateNeeded=!1,this.isLinkWidthUpdateNeeded=!1,this.isLinkArrowUpdateNeeded=!1,this.isLinkStyleUpdateNeeded=!1,this.isPointClusterUpdateNeeded=!1,this.isForceManyBodyUpdateNeeded=!1,this.isForceLinkUpdateNeeded=!1,this.isForceCenterUpdateNeeded=!1,this.requestRender())}flatten(e){return e.flat()}pair(e){const t=new Array(e.length/2);for(let i=0;i<e.length/2;i++)t[i]=[e[i*2],e[i*2+1]];return t}preserveInitOnlyFields(e){this.config.initialZoomLevel=e.initialZoomLevel,this.config.randomSeed=e.randomSeed,this.config.attribution=e.attribution}getFitViewPositions(){return this.transition.isActive&&this.transition.isActiveFor(F.Positions)&&this.graph.pointPositions&&this.graph.pointPositions?new Float32Array(this.graph.pointPositions):new Float32Array(this.getPointPositions())}getFitViewPositions3D(){return this.transition.isActive&&this.transition.isActiveFor(F.Positions)&&this.graph.pointPositions&&this.graph.pointPositions&&this.graph.pointDimensions===3?this.graph.pointPositions:this.getPointPositions({dimensions:3})}updateStateFromConfig(e){var t,i,o,s,r,n,a,l,u,d,c,f,p,m,S,v,C;this.applyEnableSimulationConfigChange(e),e.pointDefaultColor!==this.config.pointDefaultColor&&(this.graph.updatePointColor(),(t=this.points)==null||t.updateColor()),e.pointDefaultSize!==this.config.pointDefaultSize&&(this.graph.updatePointSize(),(i=this.points)==null||i.updateSize()),e.pointDefaultShape!==this.config.pointDefaultShape&&(this.graph.updatePointShape(),(o=this.points)==null||o.updateShape()),e.linkDefaultColor!==this.config.linkDefaultColor&&(this.graph.updateLinkColor(),(s=this.lines)==null||s.updateColor()),e.linkDefaultWidth!==this.config.linkDefaultWidth&&(this.graph.updateLinkWidth(),(r=this.lines)==null||r.updateWidth()),e.linkDefaultArrows!==this.config.linkDefaultArrows&&(this.graph.updateArrows(),(n=this.lines)==null||n.updateArrow()),e.linkDefaultStyle!==this.config.linkDefaultStyle&&(this.graph.updateLinkStyles(),(a=this.lines)==null||a.updateStyle()),e.linkColorInterpolateFromEndpoints!==this.config.linkColorInterpolateFromEndpoints&&((l=this.points)==null||l.updateColor()),e.linkBlending!==this.config.linkBlending&&((u=this.lines)==null||u.updateLinkBlending()),(e.curvedLinkSegments!==this.config.curvedLinkSegments||e.curvedLinks!==this.config.curvedLinks)&&((d=this.lines)==null||d.updateCurveLineGeometry()),e.backgroundColor!==this.config.backgroundColor&&(this.store.backgroundColor=E(this.config.backgroundColor)),e.hoveredPointRingColor!==this.config.hoveredPointRingColor&&this.store.setHoveredPointRingColor(this.config.hoveredPointRingColor),e.focusedPointRingColor!==this.config.focusedPointRingColor&&this.store.setFocusedPointRingColor(this.config.focusedPointRingColor),e.pointGreyoutColor!==this.config.pointGreyoutColor&&this.store.setGreyoutPointColor(this.config.pointGreyoutColor),e.hoveredLinkColor!==this.config.hoveredLinkColor&&this.store.setHoveredLinkColor(this.config.hoveredLinkColor),e.focusedPointIndex!==this.config.focusedPointIndex&&this.store.setFocusedPoint(this.config.focusedPointIndex),e.outlinedPointRingColor!==this.config.outlinedPointRingColor&&this.store.setOutlinedPointRingColor(this.config.outlinedPointRingColor),e.highlightedPointIndices!==this.config.highlightedPointIndices&&this.store.setHighlightedPointSet(this.config.highlightedPointIndices),e.outlinedPointIndices!==this.config.outlinedPointIndices&&this.store.setOutlinedPointSet(this.config.outlinedPointIndices),(e.highlightedPointIndices!==this.config.highlightedPointIndices||e.outlinedPointIndices!==this.config.outlinedPointIndices)&&((c=this.points)==null||c.updatePointStatus()),e.highlightedLinkIndices!==this.config.highlightedLinkIndices&&((f=this.lines)==null||f.updateLinkStatus()),(e.simulationCollisionRadius!==this.config.simulationCollisionRadius||e.simulationCollisionPadding!==this.config.simulationCollisionPadding||(this.config.simulationCollisionRadius===void 0||this.config.simulationCollisionRadius===0)&&e.pointDefaultSize!==this.config.pointDefaultSize)&&(this.isForceCollisionReady=!1),e.pixelRatio!==this.config.pixelRatio&&(p=this.device)!=null&&p.canvasContext&&(this.device.canvasContext.setProps({useDevicePixels:this.config.pixelRatio}),this.store.maxPointSize=de(this.device,this.config.pixelRatio)),e.spaceSize!==this.config.spaceSize&&(this.store.adjustSpaceSize(this.config.spaceSize,((m=this.device)==null?void 0:m.limits.maxTextureDimension2D)??4096),this.isForceManyBodyUpdateNeeded=!0,this.resizeCanvas(!0),this.update(this.store.isSimulationRunning?this.store.alpha:0)),e.showFPSMonitor!==this.config.showFPSMonitor&&(this.config.showFPSMonitor?this.fpsMonitor=new qe(this.canvas):((S=this.fpsMonitor)==null||S.destroy(),this.fpsMonitor=void 0)),(e.enableZoom!==this.config.enableZoom||e.enableDrag!==this.config.enableDrag)&&this.updateZoomDragBehaviors(),e.pointSamplingDistance!==this.config.pointSamplingDistance&&((v=this.points)==null||v.updateSampledPointsGrid()),e.linkSamplingDistance!==this.config.linkSamplingDistance&&((C=this.lines)==null||C.updateSampledLinksGrid()),e.spaceDimensions!==this.config.spaceDimensions&&this.setSpaceDimensions(this.config.spaceDimensions),(e.cameraFov!==this.config.cameraFov||e.cameraNear!==this.config.cameraNear||e.cameraFar!==this.config.cameraFar)&&this.store.is3D&&this.camera.updateMatrices(),(e.onLinkClick!==this.config.onLinkClick||e.onLinkContextMenu!==this.config.onLinkContextMenu||e.onLinkMouseOver!==this.config.onLinkMouseOver||e.onLinkMouseOut!==this.config.onLinkMouseOut)&&this.store.updateLinkHoveringEnabled(this.config),this.markPickingBuffersStale(),this.requestRender()}applyEnableSimulationConfigChange(e){var t,i,o,s,r;if(e.enableSimulation===this.config.enableSimulation)return;if(this.config.enableSimulation){this.transition.end(!0),this.transition.dequeue(F.Positions),this.ensureSimulationModules(),(t=this.points)==null||t.ensureSimulationResources(),this.isForceManyBodyUpdateNeeded=!0,this.isForceLinkUpdateNeeded=!0,this.isForceCenterUpdateNeeded=!0,this.create(),this.initPrograms(),this.store.simulationProgress=0,this.store.alpha=1,this.store.isSimulationRunning=!0,this._shouldForceHoverDetection=!0,(o=(i=this.config).onSimulationStart)==null||o.call(i);return}const n=this.store.isSimulationRunning||this.store.alpha>0||this.store.simulationProgress>0;this.store.isSimulationRunning=!1,this.store.alpha=0,this.store.simulationProgress=0,this._shouldForceHoverDetection=!0,n&&((r=(s=this.config).onSimulationEnd)==null||r.call(s)),this.destroySimulationModules()}markPointPositionsDirty(){var e;this.isPointPositionsUpdateNeeded=!0;const t=(e=this.points)==null?void 0:e.currentPositionTexture;t&&!t.destroyed&&(this.transition.queue(F.Positions),this.graph.hasPointAbsenceChanged()&&(this.transition.queue(F.PointSizes),this.transition.queue(F.PointColors))),this.isLinksUpdateNeeded=!0,this.isPointColorUpdateNeeded=!0,this.isPointSizeUpdateNeeded=!0,this.isPointShapeUpdateNeeded=!0,this.isPointImageIndicesUpdateNeeded=!0,this.isPointImageSizesUpdateNeeded=!0,this.isPointClusterUpdateNeeded=!0,this.isForceManyBodyUpdateNeeded=!0,this.isForceLinkUpdateNeeded=!0,this.isForceCenterUpdateNeeded=!0}setSpaceDimensions(e){var t;if(this.store.spaceDimensions!==e){if(this.store.spaceDimensions=e,this.isForceCollisionReady=!1,(t=this.forceManyBody)==null||t.create(),this.initPrograms(),e===3){const[i,o]=this.store.screenSize;i&&o&&this.camera.setViewport(i,o),this.handOffFramingTo3D()||this.maybeInitializeCamera()}else this.handOffFramingTo2D();this.updateZoomDragBehaviors()}}handOffFramingTo3D(){const[e,t]=this.store.screenSize;if(!e||!t)return!1;const i=this.zoomInstance.eventTransform.k,o=this.zoomInstance.convertScreenToSpacePosition([e/2,t/2]),s=this.getPointPositions({dimensions:3}),r=s.length?this.camera.getFitOrbit(s,3,0):void 0;r&&this.camera.setSceneRadius(r.radius);const n=this.config.cameraFov*Math.PI/180,a=t/(2*i*Math.tan(n/2)),l=Math.max(a,r?.distance??0);return this.camera.setState({target:[o[0],o[1],r?.target[2]??0],distance:l,azimuth:0,polar:Math.PI/2},this.canvasD3Selection),this._isCameraInitialized=!0,!0}handOffFramingTo2D(){var e;const[t,i]=this.store.screenSize;if(!t||!i||!this._isCameraInitialized)return;const{target:o,distance:s}=this.camera.getState(),r=this.config.cameraFov*Math.PI/180,n=i/(2*s*Math.tan(r/2)),a=this.zoomInstance.getTransform([o[0],o[1]],n);(e=this.canvasD3Selection)==null||e.call(this.zoomInstance.behavior.transform,a)}maybeInitializeCamera(){if(this._isCameraInitialized||!this.store.is3D)return;const e=this.graph.inputPointPositions;if(!e||e.length===0)return;const t=this.graph.inputPointDimensions;this._isCameraInitialized=!0;const{cameraInitialPosition:i,fitViewPadding:o}=this.config;i?(this.camera.setEyePosition(i,e,t),this.canvasD3Selection&&this.camera.reseedZoomState(this.canvasD3Selection)):this.canvasD3Selection?this.camera.fitToPositions(this.canvasD3Selection,e,t,o,0):this._isCameraInitialized=!1}warnIf3D(e,t){return this.store.is3D?(console.warn(`cosmos.gl: \`${e}\` is not supported in 3D mode${t?`; ${t}`:""}`),!0):!1}ensureDevice(e){return this.isReady?!1:(this.ready.then(()=>{this._isDestroyed||e()}).catch(t=>{console.error("Device initialization failed",t)}),!0)}validateDevice(e){const t=e.canvasContext;if(t===null||t.type==="offscreen-canvas")throw new Error("Device must have an HTMLCanvasElement canvas context. OffscreenCanvas and compute-only devices are not supported.");return t}async createDevice(e){return await bt.createDevice({type:"webgl",adapters:[kt],createCanvasContext:{canvas:e,useDevicePixels:this.config.pixelRatio,autoResize:!0,width:void 0,height:void 0},onResize:()=>{this.requestRender()}})}update(e=this.store.alpha){const{graph:t}=this;this.store.pointsTextureSize=Math.ceil(Math.sqrt(t.pointsNumber??0)),this.store.linksTextureSize=Math.ceil(Math.sqrt((t.linksNumber??0)*2)),this.create(),this.initPrograms(),this.store.alpha=e}reheatSimulationOnDragStart(){const e=this.config.simulationAlphaOnDrag??0;!this.config.enableSimulation||e<=0||this.store.isSimulationRunning&&this.store.alpha>=e||this.start(Math.max(this.store.alpha,e))}runSimulationStep(e=!1){var t,i,o,s,r,n,a,l,u,d,c,f,p,m,S,v,C,D,I,L,z,R,G,j,xe,Se,Pe,ye;const{config:{simulationGravity:st,simulationCenter:rt,simulationCollision:nt,enableSimulation:at},store:{isSimulationRunning:lt}}=this;if(!at)return;const dt=this.zoomInstance.shouldEnableSimulationDuringZoomOverride??this.config.enableSimulationDuringZoom;if(e||lt&&!(this.zoomInstance.isRunning&&!dt)){if(st&&((t=this.points)==null||t.swapFbo(),(i=this.forceGravity)==null||i.run(),(o=this.points)==null||o.updatePosition()),rt&&((s=this.points)==null||s.swapFbo(),(r=this.forceCenter)==null||r.run(),(n=this.points)==null||n.updatePosition()),(a=this.points)==null||a.swapFbo(),(l=this.forceManyBody)==null||l.run(),(u=this.points)==null||u.updatePosition(),this.store.linksTextureSize&&((d=this.points)==null||d.swapFbo(),(c=this.forceLinkIncoming)==null||c.run(),(f=this.points)==null||f.updatePosition(),(p=this.points)==null||p.swapFbo(),(m=this.forceLinkOutgoing)==null||m.run(),(S=this.points)==null||S.updatePosition()),(this.graph.pointClusters||this.graph.clusterPositions)&&((v=this.points)==null||v.swapFbo(),(C=this.clusters)==null||C.run(),(D=this.points)==null||D.updatePosition()),nt){this.isForceCollisionReady||((I=this.forceCollision)==null||I.create(),(L=this.forceCollision)==null||L.initPrograms(),this.isForceCollisionReady=!0);const ht=Math.max(1,Math.round(this.config.simulationCollisionIterations??1));for(let Ce=0;Ce<ht;Ce+=1)(z=this.points)==null||z.swapFbo(),(R=this.forceCollision)==null||R.run(),(G=this.points)==null||G.updatePosition()}this.markPickingBuffersStale(),this.store.alpha+=this.store.addAlpha(this.config.simulationDecay),this.store.simulationProgress=Math.sqrt(Math.min(1,ne/this.store.alpha)),(Pe=(Se=this.config).onSimulationTick)==null||Pe.call(Se,this.store.alpha,(j=this.store.hoveredPoint)==null?void 0:j.index,(xe=this.store.hoveredPoint)==null?void 0:xe.position)}(ye=this.points)==null||ye.trackPoints()}initPrograms(){var e,t,i,o,s;this._isDestroyed||!this.points||!this.lines||!this.clusters||(this.points.initPrograms(),this.lines.initPrograms(),(e=this.forceGravity)==null||e.initPrograms(),(t=this.forceManyBody)==null||t.initPrograms(),(i=this.forceCenter)==null||i.initPrograms(),(o=this.forceLinkIncoming)==null||o.initPrograms(),(s=this.forceLinkOutgoing)==null||s.initPrograms(),this.clusters.initPrograms())}ensureSimulationModules(){!this.device||!this.points||(this.forceGravity||(this.forceGravity=new Ve(this.device,this.config,this.store,this.graph,this.points)),this.forceCenter||(this.forceCenter=new Ne(this.device,this.config,this.store,this.graph,this.points)),this.forceManyBody||(this.forceManyBody=new je(this.device,this.config,this.store,this.graph,this.points)),this.forceLinkIncoming||(this.forceLinkIncoming=new se(this.device,this.config,this.store,this.graph,this.points)),this.forceLinkOutgoing||(this.forceLinkOutgoing=new se(this.device,this.config,this.store,this.graph,this.points)),this.forceCollision||(this.forceCollision=new Oe(this.device,this.config,this.store,this.graph,this.points)))}destroySimulationModules(){var e,t,i,o,s,r,n;(e=this.forceGravity)==null||e.destroy(),this.forceGravity=void 0,(t=this.forceCenter)==null||t.destroy(),this.forceCenter=void 0,(i=this.forceManyBody)==null||i.destroy(),this.forceManyBody=void 0,(o=this.forceLinkIncoming)==null||o.destroy(),this.forceLinkIncoming=void 0,(s=this.forceLinkOutgoing)==null||s.destroy(),this.forceLinkOutgoing=void 0,(r=this.forceCollision)==null||r.destroy(),this.forceCollision=void 0,this.isForceCollisionReady=!1,(n=this.points)==null||n.destroySimulationResources()}frame(){this._isDestroyed||this.requestAnimationFrameId||!this.store.pointsTextureSize||!this.graph.pointsNumber&&!this.graph.linksNumber||(this.requestAnimationFrameId=window.requestAnimationFrame(e=>{this.requestAnimationFrameId=0;const{store:{alpha:t,isSimulationRunning:i}}=this;t<ne&&i&&this.end(),this.renderFrame(e),!this._isDestroyed&&this.shouldKeepRendering()&&this.frame()}))}requestRender(){this._isDestroyed||this.frame()}shouldKeepRendering(){var e,t;return!this.hasResizeWakeup||this.fpsMonitor||this.store.isSimulationRunning||this.transition.isActive||this.dragInstance.isActive||this.zoomInstance.isRunning||this.camera.isRunning||(e=this.points)!=null&&e.isPickInFlight||(t=this.lines)!=null&&t.isPickInFlight?!0:this.hasPendingHoverWork()}hasPendingHoverWork(){if(!this._isPointerOnCanvas)return!1;if(this._shouldForceHoverDetection)return!0;const e=Math.abs(this._lastMouseX-this._lastCheckedMouseX),t=Math.abs(this._lastMouseY-this._lastCheckedMouseY);return e>te||t>te}renderFrame(e){var t,i,o,s,r,n,a,l,u,d,c,f,p;if(this._isDestroyed||!this.store.pointsTextureSize)return;const m=e??performance.now();(t=this.fpsMonitor)==null||t.begin(),this.resizeCanvas();const S=this.transition.isActiveFor(F.Positions),v=this.transition.isActiveFor(F.PointColors),C=this.transition.isActiveFor(F.PointSizes),D=this.transition.isActiveFor(F.LinkColors),I=this.transition.isActiveFor(F.LinkWidths);if(this.transition.isActive&&(this.transition.step(),S&&((i=this.points)==null||i.interpolatePosition(this.transition.progress),(o=this.points)==null||o.trackPoints(),this.markPickingBuffersStale())),(s=this.points)==null||s.setTransitionProgress(this.transition.progress,v,C,S),(r=this.lines)==null||r.setTransitionProgress(this.transition.progress,D,I,S),this.dragInstance.isActive||(this.resolvePendingPick(),this.findHoveredItem()),this.runSimulationStep(!1),this.device){const L=this.store.backgroundColor??[0,0,0,1],z=this.device.beginRenderPass({clearColor:L,clearDepth:1,clearStencil:0}),{config:{renderLinks:R}}=this,G=R!==!1&&!!this.store.linksTextureSize&&!!this.graph.linksNumber&&this.graph.linksNumber>0;this.store.is3D?((n=this.points)==null||n.draw(z),G&&((a=this.lines)==null||a.draw(z))):(G&&((l=this.lines)==null||l.draw(z)),(u=this.points)==null||u.draw(z)),this.dragInstance.isActive&&((d=this.points)==null||d.swapFbo(),(c=this.points)==null||c.drag(),(f=this.points)==null||f.trackPoints(),this.markPickingBuffersStale()),z.end(),this.device.submit()}(p=this.fpsMonitor)==null||p.end(m),this.currentEvent=void 0}stopFrames(){this.requestAnimationFrameId&&(window.cancelAnimationFrame(this.requestAnimationFrameId),this.requestAnimationFrameId=0)}end(){var e,t;this.store.isSimulationRunning=!1,this.store.simulationProgress=1,(t=(e=this.config).onSimulationEnd)==null||t.call(e),this._shouldForceHoverDetection=!0}onClick(e){var t,i,o,s,r,n,a,l,u,d;if(this._shouldSuppressNextClick){this._shouldSuppressNextClick=!1;return}(s=(o=this.config).onClick)==null||s.call(o,(t=this.store.hoveredPoint)==null?void 0:t.index,(i=this.store.hoveredPoint)==null?void 0:i.position,e),this.store.hoveredPoint?(n=(r=this.config).onPointClick)==null||n.call(r,this.store.hoveredPoint.index,this.store.hoveredPoint.position,e):this.store.hoveredLinkIndex!==void 0?(l=(a=this.config).onLinkClick)==null||l.call(a,this.store.hoveredLinkIndex,e):(d=(u=this.config).onBackgroundClick)==null||d.call(u,e)}updateMousePosition(e){if(!e)return;const t=e.offsetX??e.x,i=e.offsetY??e.y;t===void 0||i===void 0||(this.store.is3D?this.dragInstance.isActive&&this.store.dragPlanePoint3D&&(this.store.mousePosition3D=this.camera.unprojectOnPlane([t,i],this.store.dragPlanePoint3D)):this.store.mousePosition=this.zoomInstance.convertScreenToSpacePosition([t,i]),this.store.screenMousePosition=[t,this.store.screenSize[1]-i])}onContextMenu(e){e.preventDefault(),this.cancelLongPress(),this._shouldSuppressNextClick=!0,this.fireContextMenu(e)}cancelLongPress(){this._longPressTimerId!==void 0&&(window.clearTimeout(this._longPressTimerId),this._longPressTimerId=void 0)}fireContextMenu(e){var t,i,o,s,r,n,a,l,u,d;(s=(o=this.config).onContextMenu)==null||s.call(o,(t=this.store.hoveredPoint)==null?void 0:t.index,(i=this.store.hoveredPoint)==null?void 0:i.position,e),this.store.hoveredPoint?(n=(r=this.config).onPointContextMenu)==null||n.call(r,this.store.hoveredPoint.index,this.store.hoveredPoint.position,e):this.store.hoveredLinkIndex!==void 0?(l=(a=this.config).onLinkContextMenu)==null||l.call(a,this.store.hoveredLinkIndex,e):(d=(u=this.config).onBackgroundContextMenu)==null||d.call(u,e)}resizeCanvas(e=!1){var t,i,o,s,r,n;if(this._isDestroyed)return;const a=this.canvas.clientWidth,l=this.canvas.clientHeight,[u,d]=this.store.screenSize;if(e||u!==a||d!==l){if(this.store.is3D)this.store.updateScreenSize(a,l),this.camera.setViewport(a,l),(t=this.points)==null||t.updateSampledPointsGrid(),(i=this.lines)==null||i.updateSampledLinksGrid();else{const{k:c}=this.zoomInstance.eventTransform,f=this.zoomInstance.convertScreenToSpacePosition([u/2,d/2]);this.store.updateScreenSize(a,l),(o=this.canvasD3Selection)==null||o.call(this.zoomInstance.behavior.transform,this.zoomInstance.getTransform(f,c)),(s=this.points)==null||s.updateSampledPointsGrid(),(r=this.lines)==null||r.updateSampledLinksGrid()}this.store.isLinkHoveringEnabled&&((n=this.lines)==null||n.updateLinkIndexFbo()),this.markPickingBuffersStale()}}updateZoomDragBehaviors(){var e,t,i,o,s,r,n,a;if((this.store.is3D?this.camera.behavior:this.zoomInstance.behavior).filter(this.config.enableZoom?ot:ji),this.store.is3D){this.config.enableDrag?(e=this.canvasD3Selection)==null||e.call(this.dragInstance.behavior):(t=this.canvasD3Selection)==null||t.call(this.dragInstance.behavior).on(".drag",null),this.config.enableZoom?(i=this.canvasD3Selection)==null||i.call(this.camera.behavior):(o=this.canvasD3Selection)==null||o.call(this.camera.behavior).on("wheel.zoom",null).on("dblclick.zoom",null),this.updateCanvasTouchAction();return}this.config.enableDrag?(s=this.canvasD3Selection)==null||s.call(this.dragInstance.behavior):(r=this.canvasD3Selection)==null||r.call(this.dragInstance.behavior).on(".drag",null),this.config.enableZoom?(n=this.canvasD3Selection)==null||n.call(this.zoomInstance.behavior):(a=this.canvasD3Selection)==null||a.call(this.zoomInstance.behavior).on("wheel.zoom",null).on("dblclick.zoom",null),this.updateCanvasTouchAction()}updateCanvasTouchAction(){this.canvas.style.touchAction=this.config.enableDrag||this.config.enableZoom||this.store.is3D?"none":""}findHoveredItem(e=!1){var t,i,o,s;if(this._isDestroyed||!e&&!this._isPointerOnCanvas||this.transition.isActiveFor(F.PointSizes))return;if(!e&&this._findHoveredItemExecutionCount<Bt){this._findHoveredItemExecutionCount+=1;return}const r=Math.abs(this._lastMouseX-this._lastCheckedMouseX),n=Math.abs(this._lastMouseY-this._lastCheckedMouseY),a=r>te||n>te;if(!e&&!a&&!this._shouldForceHoverDetection)return;this.updatePickingBufferStaleness();const l=!!this.graph.linksNumber&&this.store.isLinkHoveringEnabled;if(e){(t=this.points)==null||t.discardPendingPick(),(i=this.lines)==null||i.discardPendingPick();const u=((o=this.points)==null?void 0:o.pickPointSync())??null;let d;!u&&l&&(d=((s=this.lines)==null?void 0:s.pickLinkSync())??null),this.processHoverResult(u,d)}else{const u=this.points?this.points.requestPickPoint():!0,d=l&&this.lines?this.lines.requestPickLink():!0;if(!u||!d)return}this._findHoveredItemExecutionCount=0,this._lastCheckedMouseX=this._lastMouseX,this._lastCheckedMouseY=this._lastMouseY,this._shouldForceHoverDetection=!1}updatePickingBufferStaleness(){const e=this.store.transformationMatrix4x4;let t=this._lastPickingMatrix.length!==e.length;if(!t){for(const[i,o]of e.entries())if(o!==this._lastPickingMatrix[i]){t=!0;break}}t&&(this._lastPickingMatrix=Array.from(e),this.markPickingBuffersStale())}markPickingBuffersStale(){this.points&&(this.points.isPickingBufferStale=!0),this.lines&&(this.lines.isLinkIndexBufferStale=!0)}resolvePendingPick(){var e,t;const i=(e=this.points)==null?void 0:e.takePickResult(),o=(t=this.lines)==null?void 0:t.takePickLinkResult();i===void 0&&o===void 0||this._isPointerOnCanvas&&this.processHoverResult(i,o)}processHoverResult(e,t){var i,o,s,r,n,a,l,u,d,c;if(this._isDestroyed)return;const f=e===void 0?{mouseover:!1,mouseout:!1}:this.applyPickedPoint(e);let p={mouseover:!1,mouseout:!1};if(this.graph.linksNumber&&this.store.isLinkHoveringEnabled?this.store.hoveredPoint?p=this.applyPickedLink(null):t!==void 0&&(p=this.applyPickedLink(t)):this.store.hoveredLinkIndex!==void 0&&(p=this.applyPickedLink(null)),f.mouseout&&((o=(i=this.config).onPointMouseOut)==null||o.call(i,this.currentEvent)),p.mouseout&&((r=(s=this.config).onLinkMouseOut)==null||r.call(s,this.currentEvent)),f.mouseover&&this.store.hoveredPoint){const m=this.store.hoveredPoint.index;(u=(l=this.config).onPointMouseOver)==null||u.call(l,this.store.hoveredPoint.index,this.store.hoveredPoint.position,this.currentEvent,((n=this.store.highlightedPointSet)==null?void 0:n.has(m))??!1,((a=this.store.outlinedPointSet)==null?void 0:a.has(m))??!1)}p.mouseover&&this.store.hoveredLinkIndex!==void 0&&((c=(d=this.config).onLinkMouseOver)==null||c.call(d,this.store.hoveredLinkIndex)),this.updateCanvasCursor()}applyPickedPoint(e){let t=!1,i=!1;return e&&e.index>=(this.graph.pointsNumber??0)&&(e=null),e?((this.store.hoveredPoint===void 0||this.store.hoveredPoint.index!==e.index)&&(t=!0),this.store.hoveredPoint=e):(this.store.hoveredPoint&&(i=!0),this.store.hoveredPoint=void 0),{mouseover:t,mouseout:i}}applyPickedLink(e){let t=!1,i=!1;return e!==null&&e>=(this.graph.linksNumber??0)&&(e=null),e!==null?(this.store.hoveredLinkIndex!==e&&(t=!0),this.store.hoveredLinkIndex=e):(this.store.hoveredLinkIndex!==void 0&&(i=!0),this.store.hoveredLinkIndex=void 0),(t||i)&&this.lines&&(this.lines.isLinkIndexBufferStale=!0),{mouseover:t,mouseout:i}}updateCanvasCursor(){const{hoveredPointCursor:e,hoveredLinkCursor:t}=this.config;this.dragInstance.isActive?N(this.canvas).style("cursor","grabbing"):this.store.hoveredPoint?!this.config.enableDrag||this.store.isSpaceKeyPressed?N(this.canvas).style("cursor",e):N(this.canvas).style("cursor","grab"):this.store.isLinkHoveringEnabled&&this.store.hoveredLinkIndex!==void 0?N(this.canvas).style("cursor",t):N(this.canvas).style("cursor",null)}addAttribution(){var e;this.config.attribution&&(this.attributionDivElement=document.createElement("div"),this.attributionDivElement.style.cssText=`
      user-select: none;
      position: absolute;
      bottom: 0;
      right: 0;
      color: var(--cosmosgl-attribution-color);
      margin: 0 0.6rem 0.6rem 0;
      font-size: 0.7rem;
      font-family: inherit;
    `,this.attributionDivElement.innerHTML=Ue(this.config.attribution,{ALLOWED_TAGS:["a","b","i","em","strong","span","div","p","br","img"],ALLOWED_ATTR:["href","target","class","id","style","src","alt","title"]}),(e=this.store.div)==null||e.appendChild(this.attributionDivElement))}}export{Y as EXIT_DEFAULT_COLOR_CHANNEL,ie as EXIT_DEFAULT_SIZE,qi as Graph,ue as LinkStyle,he as PointShape,ce as TransitionEasing,H as clamp,M as defaultConfigValues,le as extractIndicesFromPixels,Ae as focusedPointRingOpacity,de as getMaxPointSize,E as getRgbaColor,Be as hoveredPointRingOpacity,Ie as isAClassInstance,ae as isArray,De as isFunction,_ as isNumber,Fe as isObject,Rt as isPlainObject,q as isPointAbsent,B as readPixels,Le as rgbToBrightness,Ue as sanitizeHtml};
//# sourceMappingURL=/sm/f8efcbb3d976142aa6ac8618b30361ff0ba1c99cd76bb975348f979cf6927324.map