/*! @license DOMPurify 3.2.4 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.2.4/LICENSE */const{entries:dt,setPrototypeOf:at,isFrozen:Wt,getPrototypeOf:Bt,getOwnPropertyDescriptor:Yt}=Object;let{freeze:S,seal:O,create:Tt}=Object,{apply:Ce,construct:we}=typeof Reflect<"u"&&Reflect;S||(S=function(o){return o});O||(O=function(o){return o});Ce||(Ce=function(o,l,s){return o.apply(l,s)});we||(we=function(o,l){return new o(...l)});const se=R(Array.prototype.forEach),Xt=R(Array.prototype.lastIndexOf),rt=R(Array.prototype.pop),V=R(Array.prototype.push),jt=R(Array.prototype.splice),ce=R(String.prototype.toLowerCase),Ne=R(String.prototype.toString),st=R(String.prototype.match),$=R(String.prototype.replace),Vt=R(String.prototype.indexOf),$t=R(String.prototype.trim),L=R(Object.prototype.hasOwnProperty),A=R(RegExp.prototype.test),q=qt(TypeError);function R(r){return function(o){for(var l=arguments.length,s=new Array(l>1?l-1:0),T=1;T<l;T++)s[T-1]=arguments[T];return Ce(r,o,s)}}function qt(r){return function(){for(var o=arguments.length,l=new Array(o),s=0;s<o;s++)l[s]=arguments[s];return we(r,l)}}function a(r,o){let l=arguments.length>2&&arguments[2]!==void 0?arguments[2]:ce;at&&at(r,null);let s=o.length;for(;s--;){let T=o[s];if(typeof T=="string"){const b=l(T);b!==T&&(Wt(o)||(o[s]=b),T=b)}r[T]=!0}return r}function Kt(r){for(let o=0;o<r.length;o++)L(r,o)||(r[o]=null);return r}function w(r){const o=Tt(null);for(const[l,s]of dt(r))L(r,l)&&(Array.isArray(s)?o[l]=Kt(s):s&&typeof s=="object"&&s.constructor===Object?o[l]=w(s):o[l]=s);return o}function K(r,o){for(;r!==null;){const s=Yt(r,o);if(s){if(s.get)return R(s.get);if(typeof s.value=="function")return R(s.value)}r=Bt(r)}function l(){return null}return l}const lt=S(["a","abbr","acronym","address","area","article","aside","audio","b","bdi","bdo","big","blink","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","content","data","datalist","dd","decorator","del","details","dfn","dialog","dir","div","dl","dt","element","em","fieldset","figcaption","figure","font","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","img","input","ins","kbd","label","legend","li","main","map","mark","marquee","menu","menuitem","meter","nav","nobr","ol","optgroup","option","output","p","picture","pre","progress","q","rp","rt","ruby","s","samp","section","select","shadow","small","source","spacer","span","strike","strong","style","sub","summary","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","tr","track","tt","u","ul","var","video","wbr"]),De=S(["svg","a","altglyph","altglyphdef","altglyphitem","animatecolor","animatemotion","animatetransform","circle","clippath","defs","desc","ellipse","filter","font","g","glyph","glyphref","hkern","image","line","lineargradient","marker","mask","metadata","mpath","path","pattern","polygon","polyline","radialgradient","rect","stop","style","switch","symbol","text","textpath","title","tref","tspan","view","vkern"]),be=S(["feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feDropShadow","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence"]),Zt=S(["animate","color-profile","cursor","discard","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignobject","hatch","hatchpath","mesh","meshgradient","meshpatch","meshrow","missing-glyph","script","set","solidcolor","unknown","use"]),Ie=S(["math","menclose","merror","mfenced","mfrac","mglyph","mi","mlabeledtr","mmultiscripts","mn","mo","mover","mpadded","mphantom","mroot","mrow","ms","mspace","msqrt","mstyle","msub","msup","msubsup","mtable","mtd","mtext","mtr","munder","munderover","mprescripts"]),Jt=S(["maction","maligngroup","malignmark","mlongdiv","mscarries","mscarry","msgroup","mstack","msline","msrow","semantics","annotation","annotation-xml","mprescripts","none"]),ct=S(["#text"]),ft=S(["accept","action","align","alt","autocapitalize","autocomplete","autopictureinpicture","autoplay","background","bgcolor","border","capture","cellpadding","cellspacing","checked","cite","class","clear","color","cols","colspan","controls","controlslist","coords","crossorigin","datetime","decoding","default","dir","disabled","disablepictureinpicture","disableremoteplayback","download","draggable","enctype","enterkeyhint","face","for","headers","height","hidden","high","href","hreflang","id","inputmode","integrity","ismap","kind","label","lang","list","loading","loop","low","max","maxlength","media","method","min","minlength","multiple","muted","name","nonce","noshade","novalidate","nowrap","open","optimum","pattern","placeholder","playsinline","popover","popovertarget","popovertargetaction","poster","preload","pubdate","radiogroup","readonly","rel","required","rev","reversed","role","rows","rowspan","spellcheck","scope","selected","shape","size","sizes","span","srclang","start","src","srcset","step","style","summary","tabindex","title","translate","type","usemap","valign","value","width","wrap","xmlns","slot"]),Me=S(["accent-height","accumulate","additive","alignment-baseline","amplitude","ascent","attributename","attributetype","azimuth","basefrequency","baseline-shift","begin","bias","by","class","clip","clippathunits","clip-path","clip-rule","color","color-interpolation","color-interpolation-filters","color-profile","color-rendering","cx","cy","d","dx","dy","diffuseconstant","direction","display","divisor","dur","edgemode","elevation","end","exponent","fill","fill-opacity","fill-rule","filter","filterunits","flood-color","flood-opacity","font-family","font-size","font-size-adjust","font-stretch","font-style","font-variant","font-weight","fx","fy","g1","g2","glyph-name","glyphref","gradientunits","gradienttransform","height","href","id","image-rendering","in","in2","intercept","k","k1","k2","k3","k4","kerning","keypoints","keysplines","keytimes","lang","lengthadjust","letter-spacing","kernelmatrix","kernelunitlength","lighting-color","local","marker-end","marker-mid","marker-start","markerheight","markerunits","markerwidth","maskcontentunits","maskunits","max","mask","media","method","mode","min","name","numoctaves","offset","operator","opacity","order","orient","orientation","origin","overflow","paint-order","path","pathlength","patterncontentunits","patterntransform","patternunits","points","preservealpha","preserveaspectratio","primitiveunits","r","rx","ry","radius","refx","refy","repeatcount","repeatdur","restart","result","rotate","scale","seed","shape-rendering","slope","specularconstant","specularexponent","spreadmethod","startoffset","stddeviation","stitchtiles","stop-color","stop-opacity","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke","stroke-width","style","surfacescale","systemlanguage","tabindex","tablevalues","targetx","targety","transform","transform-origin","text-anchor","text-decoration","text-rendering","textlength","type","u1","u2","unicode","values","viewbox","visibility","version","vert-adv-y","vert-origin-x","vert-origin-y","width","word-spacing","wrap","writing-mode","xchannelselector","ychannelselector","x","x1","x2","xmlns","y","y1","y2","z","zoomandpan"]),ut=S(["accent","accentunder","align","bevelled","close","columnsalign","columnlines","columnspan","denomalign","depth","dir","display","displaystyle","encoding","fence","frame","height","href","id","largeop","length","linethickness","lspace","lquote","mathbackground","mathcolor","mathsize","mathvariant","maxsize","minsize","movablelimits","notation","numalign","open","rowalign","rowlines","rowspacing","rowspan","rspace","rquote","scriptlevel","scriptminsize","scriptsizemultiplier","selection","separator","separators","stretchy","subscriptshift","supscriptshift","symmetric","voffset","width","xmlns"]),le=S(["xlink:href","xml:id","xlink:title","xml:space","xmlns:xlink"]),Qt=O(/\{\{[\w\W]*|[\w\W]*\}\}/gm),en=O(/<%[\w\W]*|[\w\W]*%>/gm),tn=O(/\$\{[\w\W]*/gm),nn=O(/^data-[\-\w.\u00B7-\uFFFF]+$/),on=O(/^aria-[\-\w]+$/),_t=O(/^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i),an=O(/^(?:\w+script|data):/i),rn=O(/[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g),Et=O(/^html$/i),sn=O(/^[a-z][.\w]*(-[.\w]+)+$/i);var mt=Object.freeze({__proto__:null,ARIA_ATTR:on,ATTR_WHITESPACE:rn,CUSTOM_ELEMENT:sn,DATA_ATTR:nn,DOCTYPE_NAME:Et,ERB_EXPR:en,IS_ALLOWED_URI:_t,IS_SCRIPT_OR_DATA:an,MUSTACHE_EXPR:Qt,TMPLIT_EXPR:tn});const Z={element:1,attribute:2,text:3,cdataSection:4,entityReference:5,entityNode:6,progressingInstruction:7,comment:8,document:9,documentType:10,documentFragment:11,notation:12},ln=function(){return typeof window>"u"?null:window},cn=function(o,l){if(typeof o!="object"||typeof o.createPolicy!="function")return null;let s=null;const T="data-tt-policy-suffix";l&&l.hasAttribute(T)&&(s=l.getAttribute(T));const b="dompurify"+(s?"#"+s:"");try{return o.createPolicy(b,{createHTML(x){return x},createScriptURL(x){return x}})}catch{return console.warn("TrustedTypes policy "+b+" could not be created."),null}},pt=function(){return{afterSanitizeAttributes:[],afterSanitizeElements:[],afterSanitizeShadowDOM:[],beforeSanitizeAttributes:[],beforeSanitizeElements:[],beforeSanitizeShadowDOM:[],uponSanitizeAttribute:[],uponSanitizeElement:[],uponSanitizeShadowNode:[]}};function gt(){let r=arguments.length>0&&arguments[0]!==void 0?arguments[0]:ln();const o=i=>gt(i);if(o.version="3.2.4",o.removed=[],!r||!r.document||r.document.nodeType!==Z.document||!r.Element)return o.isSupported=!1,o;let{document:l}=r;const s=l,T=s.currentScript,{DocumentFragment:b,HTMLTemplateElement:x,Node:fe,Element:xe,NodeFilter:z,NamedNodeMap:ht=r.NamedNodeMap||r.MozNamedAttrMap,HTMLFormElement:At,DOMParser:St,trustedTypes:J}=r,G=xe.prototype,Rt=K(G,"cloneNode"),yt=K(G,"remove"),Ot=K(G,"nextSibling"),Lt=K(G,"childNodes"),Q=K(G,"parentNode");if(typeof x=="function"){const i=l.createElement("template");i.content&&i.content.ownerDocument&&(l=i.content.ownerDocument)}let E,W="";const{implementation:ue,createNodeIterator:Nt,createDocumentFragment:Dt,getElementsByTagName:bt}=l,{importNode:It}=s;let g=pt();o.isSupported=typeof dt=="function"&&typeof Q=="function"&&ue&&ue.createHTMLDocument!==void 0;const{MUSTACHE_EXPR:me,ERB_EXPR:pe,TMPLIT_EXPR:de,DATA_ATTR:Mt,ARIA_ATTR:Ct,IS_SCRIPT_OR_DATA:wt,ATTR_WHITESPACE:Pe,CUSTOM_ELEMENT:xt}=mt;let{IS_ALLOWED_URI:ve}=mt,u=null;const ke=a({},[...lt,...De,...be,...Ie,...ct]);let p=null;const Ue=a({},[...ft,...Me,...ut,...le]);let f=Object.seal(Tt(null,{tagNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},allowCustomizedBuiltInElements:{writable:!0,configurable:!1,enumerable:!0,value:!1}})),B=null,Te=null,Fe=!0,_e=!0,He=!1,ze=!0,P=!1,Ee=!0,C=!1,ge=!1,he=!1,v=!1,ee=!1,te=!1,Ge=!0,We=!1;const Pt="user-content-";let Ae=!0,Y=!1,k={},U=null;const Be=a({},["annotation-xml","audio","colgroup","desc","foreignobject","head","iframe","math","mi","mn","mo","ms","mtext","noembed","noframes","noscript","plaintext","script","style","svg","template","thead","title","video","xmp"]);let Ye=null;const Xe=a({},["audio","video","img","source","image","track"]);let Se=null;const je=a({},["alt","class","for","id","label","name","pattern","placeholder","role","summary","title","value","style","xmlns"]),ne="http://www.w3.org/1998/Math/MathML",oe="http://www.w3.org/2000/svg",I="http://www.w3.org/1999/xhtml";let F=I,Re=!1,ye=null;const vt=a({},[ne,oe,I],Ne);let ie=a({},["mi","mo","mn","ms","mtext"]),ae=a({},["annotation-xml"]);const kt=a({},["title","style","font","a","script"]);let X=null;const Ut=["application/xhtml+xml","text/html"],Ft="text/html";let m=null,H=null;const Ht=l.createElement("form"),Ve=function(e){return e instanceof RegExp||e instanceof Function},Oe=function(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};if(!(H&&H===e)){if((!e||typeof e!="object")&&(e={}),e=w(e),X=Ut.indexOf(e.PARSER_MEDIA_TYPE)===-1?Ft:e.PARSER_MEDIA_TYPE,m=X==="application/xhtml+xml"?Ne:ce,u=L(e,"ALLOWED_TAGS")?a({},e.ALLOWED_TAGS,m):ke,p=L(e,"ALLOWED_ATTR")?a({},e.ALLOWED_ATTR,m):Ue,ye=L(e,"ALLOWED_NAMESPACES")?a({},e.ALLOWED_NAMESPACES,Ne):vt,Se=L(e,"ADD_URI_SAFE_ATTR")?a(w(je),e.ADD_URI_SAFE_ATTR,m):je,Ye=L(e,"ADD_DATA_URI_TAGS")?a(w(Xe),e.ADD_DATA_URI_TAGS,m):Xe,U=L(e,"FORBID_CONTENTS")?a({},e.FORBID_CONTENTS,m):Be,B=L(e,"FORBID_TAGS")?a({},e.FORBID_TAGS,m):{},Te=L(e,"FORBID_ATTR")?a({},e.FORBID_ATTR,m):{},k=L(e,"USE_PROFILES")?e.USE_PROFILES:!1,Fe=e.ALLOW_ARIA_ATTR!==!1,_e=e.ALLOW_DATA_ATTR!==!1,He=e.ALLOW_UNKNOWN_PROTOCOLS||!1,ze=e.ALLOW_SELF_CLOSE_IN_ATTR!==!1,P=e.SAFE_FOR_TEMPLATES||!1,Ee=e.SAFE_FOR_XML!==!1,C=e.WHOLE_DOCUMENT||!1,v=e.RETURN_DOM||!1,ee=e.RETURN_DOM_FRAGMENT||!1,te=e.RETURN_TRUSTED_TYPE||!1,he=e.FORCE_BODY||!1,Ge=e.SANITIZE_DOM!==!1,We=e.SANITIZE_NAMED_PROPS||!1,Ae=e.KEEP_CONTENT!==!1,Y=e.IN_PLACE||!1,ve=e.ALLOWED_URI_REGEXP||_t,F=e.NAMESPACE||I,ie=e.MATHML_TEXT_INTEGRATION_POINTS||ie,ae=e.HTML_INTEGRATION_POINTS||ae,f=e.CUSTOM_ELEMENT_HANDLING||{},e.CUSTOM_ELEMENT_HANDLING&&Ve(e.CUSTOM_ELEMENT_HANDLING.tagNameCheck)&&(f.tagNameCheck=e.CUSTOM_ELEMENT_HANDLING.tagNameCheck),e.CUSTOM_ELEMENT_HANDLING&&Ve(e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)&&(f.attributeNameCheck=e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck),e.CUSTOM_ELEMENT_HANDLING&&typeof e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements=="boolean"&&(f.allowCustomizedBuiltInElements=e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements),P&&(_e=!1),ee&&(v=!0),k&&(u=a({},ct),p=[],k.html===!0&&(a(u,lt),a(p,ft)),k.svg===!0&&(a(u,De),a(p,Me),a(p,le)),k.svgFilters===!0&&(a(u,be),a(p,Me),a(p,le)),k.mathMl===!0&&(a(u,Ie),a(p,ut),a(p,le))),e.ADD_TAGS&&(u===ke&&(u=w(u)),a(u,e.ADD_TAGS,m)),e.ADD_ATTR&&(p===Ue&&(p=w(p)),a(p,e.ADD_ATTR,m)),e.ADD_URI_SAFE_ATTR&&a(Se,e.ADD_URI_SAFE_ATTR,m),e.FORBID_CONTENTS&&(U===Be&&(U=w(U)),a(U,e.FORBID_CONTENTS,m)),Ae&&(u["#text"]=!0),C&&a(u,["html","head","body"]),u.table&&(a(u,["tbody"]),delete B.tbody),e.TRUSTED_TYPES_POLICY){if(typeof e.TRUSTED_TYPES_POLICY.createHTML!="function")throw q('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');if(typeof e.TRUSTED_TYPES_POLICY.createScriptURL!="function")throw q('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');E=e.TRUSTED_TYPES_POLICY,W=E.createHTML("")}else E===void 0&&(E=cn(J,T)),E!==null&&typeof W=="string"&&(W=E.createHTML(""));S&&S(e),H=e}},$e=a({},[...De,...be,...Zt]),qe=a({},[...Ie,...Jt]),zt=function(e){let t=Q(e);(!t||!t.tagName)&&(t={namespaceURI:F,tagName:"template"});const n=ce(e.tagName),c=ce(t.tagName);return ye[e.namespaceURI]?e.namespaceURI===oe?t.namespaceURI===I?n==="svg":t.namespaceURI===ne?n==="svg"&&(c==="annotation-xml"||ie[c]):!!$e[n]:e.namespaceURI===ne?t.namespaceURI===I?n==="math":t.namespaceURI===oe?n==="math"&&ae[c]:!!qe[n]:e.namespaceURI===I?t.namespaceURI===oe&&!ae[c]||t.namespaceURI===ne&&!ie[c]?!1:!qe[n]&&(kt[n]||!$e[n]):!!(X==="application/xhtml+xml"&&ye[e.namespaceURI]):!1},N=function(e){V(o.removed,{element:e});try{Q(e).removeChild(e)}catch{yt(e)}},re=function(e,t){try{V(o.removed,{attribute:t.getAttributeNode(e),from:t})}catch{V(o.removed,{attribute:null,from:t})}if(t.removeAttribute(e),e==="is")if(v||ee)try{N(t)}catch{}else try{t.setAttribute(e,"")}catch{}},Ke=function(e){let t=null,n=null;if(he)e="<remove></remove>"+e;else{const d=st(e,/^[\r\n\t ]+/);n=d&&d[0]}X==="application/xhtml+xml"&&F===I&&(e='<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>'+e+"</body></html>");const c=E?E.createHTML(e):e;if(F===I)try{t=new St().parseFromString(c,X)}catch{}if(!t||!t.documentElement){t=ue.createDocument(F,"template",null);try{t.documentElement.innerHTML=Re?W:c}catch{}}const _=t.body||t.documentElement;return e&&n&&_.insertBefore(l.createTextNode(n),_.childNodes[0]||null),F===I?bt.call(t,C?"html":"body")[0]:C?t.documentElement:_},Ze=function(e){return Nt.call(e.ownerDocument||e,e,z.SHOW_ELEMENT|z.SHOW_COMMENT|z.SHOW_TEXT|z.SHOW_PROCESSING_INSTRUCTION|z.SHOW_CDATA_SECTION,null)},Le=function(e){return e instanceof At&&(typeof e.nodeName!="string"||typeof e.textContent!="string"||typeof e.removeChild!="function"||!(e.attributes instanceof ht)||typeof e.removeAttribute!="function"||typeof e.setAttribute!="function"||typeof e.namespaceURI!="string"||typeof e.insertBefore!="function"||typeof e.hasChildNodes!="function")},Je=function(e){return typeof fe=="function"&&e instanceof fe};function M(i,e,t){se(i,n=>{n.call(o,e,t,H)})}const Qe=function(e){let t=null;if(M(g.beforeSanitizeElements,e,null),Le(e))return N(e),!0;const n=m(e.nodeName);if(M(g.uponSanitizeElement,e,{tagName:n,allowedTags:u}),e.hasChildNodes()&&!Je(e.firstElementChild)&&A(/<[/\w]/g,e.innerHTML)&&A(/<[/\w]/g,e.textContent)||e.nodeType===Z.progressingInstruction||Ee&&e.nodeType===Z.comment&&A(/<[/\w]/g,e.data))return N(e),!0;if(!u[n]||B[n]){if(!B[n]&&tt(n)&&(f.tagNameCheck instanceof RegExp&&A(f.tagNameCheck,n)||f.tagNameCheck instanceof Function&&f.tagNameCheck(n)))return!1;if(Ae&&!U[n]){const c=Q(e)||e.parentNode,_=Lt(e)||e.childNodes;if(_&&c){const d=_.length;for(let y=d-1;y>=0;--y){const D=Rt(_[y],!0);D.__removalCount=(e.__removalCount||0)+1,c.insertBefore(D,Ot(e))}}}return N(e),!0}return e instanceof xe&&!zt(e)||(n==="noscript"||n==="noembed"||n==="noframes")&&A(/<\/no(script|embed|frames)/i,e.innerHTML)?(N(e),!0):(P&&e.nodeType===Z.text&&(t=e.textContent,se([me,pe,de],c=>{t=$(t,c," ")}),e.textContent!==t&&(V(o.removed,{element:e.cloneNode()}),e.textContent=t)),M(g.afterSanitizeElements,e,null),!1)},et=function(e,t,n){if(Ge&&(t==="id"||t==="name")&&(n in l||n in Ht))return!1;if(!(_e&&!Te[t]&&A(Mt,t))){if(!(Fe&&A(Ct,t))){if(!p[t]||Te[t]){if(!(tt(e)&&(f.tagNameCheck instanceof RegExp&&A(f.tagNameCheck,e)||f.tagNameCheck instanceof Function&&f.tagNameCheck(e))&&(f.attributeNameCheck instanceof RegExp&&A(f.attributeNameCheck,t)||f.attributeNameCheck instanceof Function&&f.attributeNameCheck(t))||t==="is"&&f.allowCustomizedBuiltInElements&&(f.tagNameCheck instanceof RegExp&&A(f.tagNameCheck,n)||f.tagNameCheck instanceof Function&&f.tagNameCheck(n))))return!1}else if(!Se[t]){if(!A(ve,$(n,Pe,""))){if(!((t==="src"||t==="xlink:href"||t==="href")&&e!=="script"&&Vt(n,"data:")===0&&Ye[e])){if(!(He&&!A(wt,$(n,Pe,"")))){if(n)return!1}}}}}}return!0},tt=function(e){return e!=="annotation-xml"&&st(e,xt)},nt=function(e){M(g.beforeSanitizeAttributes,e,null);const{attributes:t}=e;if(!t||Le(e))return;const n={attrName:"",attrValue:"",keepAttr:!0,allowedAttributes:p,forceKeepAttr:void 0};let c=t.length;for(;c--;){const _=t[c],{name:d,namespaceURI:y,value:D}=_,j=m(d);let h=d==="value"?D:$t(D);if(n.attrName=j,n.attrValue=h,n.keepAttr=!0,n.forceKeepAttr=void 0,M(g.uponSanitizeAttribute,e,n),h=n.attrValue,We&&(j==="id"||j==="name")&&(re(d,e),h=Pt+h),Ee&&A(/((--!?|])>)|<\/(style|title)/i,h)){re(d,e);continue}if(n.forceKeepAttr||(re(d,e),!n.keepAttr))continue;if(!ze&&A(/\/>/i,h)){re(d,e);continue}P&&se([me,pe,de],it=>{h=$(h,it," ")});const ot=m(e.nodeName);if(et(ot,j,h)){if(E&&typeof J=="object"&&typeof J.getAttributeType=="function"&&!y)switch(J.getAttributeType(ot,j)){case"TrustedHTML":{h=E.createHTML(h);break}case"TrustedScriptURL":{h=E.createScriptURL(h);break}}try{y?e.setAttributeNS(y,d,h):e.setAttribute(d,h),Le(e)?N(e):rt(o.removed)}catch{}}}M(g.afterSanitizeAttributes,e,null)},Gt=function i(e){let t=null;const n=Ze(e);for(M(g.beforeSanitizeShadowDOM,e,null);t=n.nextNode();)M(g.uponSanitizeShadowNode,t,null),Qe(t),nt(t),t.content instanceof b&&i(t.content);M(g.afterSanitizeShadowDOM,e,null)};return o.sanitize=function(i){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},t=null,n=null,c=null,_=null;if(Re=!i,Re&&(i="<!-->"),typeof i!="string"&&!Je(i))if(typeof i.toString=="function"){if(i=i.toString(),typeof i!="string")throw q("dirty is not a string, aborting")}else throw q("toString is not a function");if(!o.isSupported)return i;if(ge||Oe(e),o.removed=[],typeof i=="string"&&(Y=!1),Y){if(i.nodeName){const D=m(i.nodeName);if(!u[D]||B[D])throw q("root node is forbidden and cannot be sanitized in-place")}}else if(i instanceof fe)t=Ke("<!---->"),n=t.ownerDocument.importNode(i,!0),n.nodeType===Z.element&&n.nodeName==="BODY"||n.nodeName==="HTML"?t=n:t.appendChild(n);else{if(!v&&!P&&!C&&i.indexOf("<")===-1)return E&&te?E.createHTML(i):i;if(t=Ke(i),!t)return v?null:te?W:""}t&&he&&N(t.firstChild);const d=Ze(Y?i:t);for(;c=d.nextNode();)Qe(c),nt(c),c.content instanceof b&&Gt(c.content);if(Y)return i;if(v){if(ee)for(_=Dt.call(t.ownerDocument);t.firstChild;)_.appendChild(t.firstChild);else _=t;return(p.shadowroot||p.shadowrootmode)&&(_=It.call(s,_,!0)),_}let y=C?t.outerHTML:t.innerHTML;return C&&u["!doctype"]&&t.ownerDocument&&t.ownerDocument.doctype&&t.ownerDocument.doctype.name&&A(Et,t.ownerDocument.doctype.name)&&(y="<!DOCTYPE "+t.ownerDocument.doctype.name+`>
`+y),P&&se([me,pe,de],D=>{y=$(y,D," ")}),E&&te?E.createHTML(y):y},o.setConfig=function(){let i=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};Oe(i),ge=!0},o.clearConfig=function(){H=null,ge=!1},o.isValidAttribute=function(i,e,t){H||Oe({});const n=m(i),c=m(e);return et(n,c,t)},o.addHook=function(i,e){typeof e=="function"&&V(g[i],e)},o.removeHook=function(i,e){if(e!==void 0){const t=Xt(g[i],e);return t===-1?void 0:jt(g[i],t,1)[0]}return rt(g[i])},o.removeHooks=function(i){g[i]=[]},o.removeAllHooks=function(){g=pt()},o}var fn=gt();export{fn as default};
//# sourceMappingURL=D-QPbZEk.js.map
