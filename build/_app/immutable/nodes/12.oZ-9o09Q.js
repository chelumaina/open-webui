import{s as $,l as E,i as y,d,j as _,p as q,q as B,e as I,c as k,a as v,f as S,g as U,n as D}from"../chunks/vexCXLX9.js";import{S as P,i as C,a as g,c as W,t as h,g as j,b as R,d as V,m as N,e as F}from"../chunks/Cdll-xsj.js";import{t as p}from"../chunks/DMk2eJ1b.js";import{g as M}from"../chunks/WDSA219a.js";import{p as Q}from"../chunks/B9-t4RFp.js";import{a as A,c as H,b as w,f as X,m as z}from"../chunks/DzLIgThl.js";import{a as G,u as J,g as K}from"../chunks/Dg2WIrmW.js";import{F as L}from"../chunks/BvHvAbMP.js";import{S as T}from"../chunks/Cmi_MrK3.js";import{g as Y}from"../chunks/CP68AaU9.js";import{e as Z,c as x}from"../chunks/hvQ-lebT.js";function ee(c){let e,n,t,r;return t=new T({}),{c(){e=I("div"),n=I("div"),R(t.$$.fragment),this.h()},l(o){e=k(o,"DIV",{class:!0});var i=v(e);n=k(i,"DIV",{class:!0});var u=v(n);V(t.$$.fragment,u),u.forEach(d),i.forEach(d),this.h()},h(){S(n,"class","pb-16"),S(e,"class","flex items-center justify-center h-full")},m(o,i){y(o,e,i),U(e,n),N(t,n,null),r=!0},p:D,i(o){r||(h(t.$$.fragment,o),r=!0)},o(o){g(t.$$.fragment,o),r=!1},d(o){o&&d(e),F(t)}}}function te(c){let e,n;return e=new L({props:{edit:!0,id:c[0].id,name:c[0].name,meta:c[0].meta,content:c[0].content,onSave:c[3]}}),{c(){R(e.$$.fragment)},l(t){V(e.$$.fragment,t)},m(t,r){N(e,t,r),n=!0},p(t,r){const o={};r&1&&(o.id=t[0].id),r&1&&(o.name=t[0].name),r&1&&(o.meta=t[0].meta),r&1&&(o.content=t[0].content),e.$set(o)},i(t){n||(h(e.$$.fragment,t),n=!0)},o(t){g(e.$$.fragment,t),n=!1},d(t){F(e,t)}}}function ne(c){let e,n,t,r;const o=[te,ee],i=[];function u(s,l){return s[0]?0:1}return e=u(c),n=i[e]=o[e](c),{c(){n.c(),t=E()},l(s){n.l(s),t=E()},m(s,l){i[e].m(s,l),y(s,t,l),r=!0},p(s,[l]){let f=e;e=u(s),e===f?i[e].p(s,l):(j(),g(i[f],1,1,()=>{i[f]=null}),W(),n=i[e],n?n.p(s,l):(n=i[e]=o[e](s),n.c()),h(n,1),n.m(t.parentNode,t))},i(s){r||(h(n),r=!0)},o(s){g(n),r=!1},d(s){s&&d(t),i[e].d(s)}}}function oe(c,e,n){let t,r,o,i;_(c,Q,a=>n(4,t=a)),_(c,A,a=>n(5,r=a)),_(c,H,a=>n(6,o=a));const u=q("i18n");_(c,u,a=>n(7,i=a));let s=null;const l=async a=>{var b;console.log(a);const m=Z(a.content);if(x((m==null?void 0:m.required_open_webui_version)??"0.0.0",w)){console.log("Version is lower than required"),p.error(i.t("BiXAI version (v{{OPEN_WEBUI_VERSION}}) is lower than required version (v{{REQUIRED_VERSION}})",{OPEN_WEBUI_VERSION:w,REQUIRED_VERSION:(m==null?void 0:m.required_open_webui_version)??"0.0.0"}));return}await J(localStorage.token,s.id,{id:a.id,name:a.name,meta:a.meta,content:a.content}).catch(O=>(p.error(`${O}`),null))&&(p.success(i.t("Function updated successfully")),X.set(await K(localStorage.token)),z.set(await Y(localStorage.token,((b=o==null?void 0:o.features)==null?void 0:b.enable_direct_connections)&&((r==null?void 0:r.directConnections)??null))))};return B(async()=>{console.log("mounted");const a=t.url.searchParams.get("id");a&&(n(0,s=await G(localStorage.token,a).catch(m=>(p.error(`${m}`),M("/admin/functions"),null))),console.log(s))}),[s,u,l,a=>{l(a)}]}class ge extends P{constructor(e){super(),C(this,e,oe,ne,$,{})}}export{ge as component};
//# sourceMappingURL=12.oZ-9o09Q.js.map
