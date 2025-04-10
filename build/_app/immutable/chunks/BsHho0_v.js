import{s as X,e as w,k as D,D as V,c as $,a as b,o as A,E as S,d as _,f as h,i as I,g as m,u as O,n as F,j as L,F as Z,p as ee,B as C,P as te,H as re,t as le,b as ae,h as se,l as W}from"./vexCXLX9.js";import{S as q,i as z,t as y,g as ne,c as oe,a as B,b as P,d as U,m as M,e as j}from"./Cdll-xsj.js";import{e as x}from"./DNXpXRYa.js";import{v as ie}from"./DzLIgThl.js";import{t as ue}from"./DMk2eJ1b.js";import{T as fe}from"./DzHlmjPS.js";import{X as ce}from"./4edIpoVY.js";function G(r,e,a){const t=r.slice();return t[11]=e[a],t}function J(r){let e,a,t,l,f,s,o,i,c,v,k,E,p=x(r[4]),n=[];for(let u=0;u<p.length;u+=1)n[u]=K(G(r,p,u));return{c(){e=w("div"),a=w("input"),l=D(),f=w("datalist");for(let u=0;u<n.length;u+=1)n[u].c();s=D(),o=w("button"),i=V("svg"),c=V("path"),this.h()},l(u){e=$(u,"DIV",{class:!0});var d=b(e);a=$(d,"INPUT",{class:!0,placeholder:!0,list:!0}),l=A(d),f=$(d,"DATALIST",{id:!0});var g=b(f);for(let H=0;H<n.length;H+=1)n[H].l(g);g.forEach(_),s=A(d),o=$(d,"BUTTON",{type:!0,"aria-label":!0});var T=b(o);i=S(T,"svg",{xmlns:!0,viewBox:!0,fill:!0,"stroke-width":!0,class:!0});var N=b(i);c=S(N,"path",{"fill-rule":!0,d:!0,"clip-rule":!0}),b(c).forEach(_),N.forEach(_),T.forEach(_),d.forEach(_),this.h()},h(){h(a,"class","px-2 cursor-pointer self-center text-xs h-fit bg-transparent outline-hidden line-clamp-1 w-[6.5rem]"),h(a,"placeholder",t=r[3].t("Add a tag")),h(a,"list","tagOptions"),h(f,"id","tagOptions"),h(c,"fill-rule","evenodd"),h(c,"d","M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z"),h(c,"clip-rule","evenodd"),h(i,"xmlns","http://www.w3.org/2000/svg"),h(i,"viewBox","0 0 16 16"),h(i,"fill","currentColor"),h(i,"stroke-width","2"),h(i,"class","w-3 h-3"),h(o,"type","button"),h(o,"aria-label",v=r[3].t("Save Tag")),h(e,"class","flex items-center")},m(u,d){I(u,e,d),m(e,a),C(a,r[2]),m(e,l),m(e,f);for(let g=0;g<n.length;g+=1)n[g]&&n[g].m(f,null);m(e,s),m(e,o),m(o,i),m(i,c),k||(E=[O(a,"input",r[7]),O(a,"keydown",r[8]),O(o,"click",r[6])],k=!0)},p(u,d){if(d&8&&t!==(t=u[3].t("Add a tag"))&&h(a,"placeholder",t),d&4&&a.value!==u[2]&&C(a,u[2]),d&16){p=x(u[4]);let g;for(g=0;g<p.length;g+=1){const T=G(u,p,g);n[g]?n[g].p(T,d):(n[g]=K(T),n[g].c(),n[g].m(f,null))}for(;g<n.length;g+=1)n[g].d(1);n.length=p.length}d&8&&v!==(v=u[3].t("Save Tag"))&&h(o,"aria-label",v)},d(u){u&&_(e),te(n,u),k=!1,re(E)}}}function K(r){let e,a;return{c(){e=w("option"),this.h()},l(t){e=$(t,"OPTION",{}),b(e).forEach(_),this.h()},h(){e.__value=a=r[11].name,C(e,e.__value)},m(t,l){I(t,e,l)},p(t,l){l&16&&a!==(a=t[11].name)&&(e.__value=a,C(e,e.__value))},d(t){t&&_(e)}}}function Q(r){let e,a;return{c(){e=w("span"),a=le(r[0]),this.h()},l(t){e=$(t,"SPAN",{class:!0});var l=b(e);a=ae(l,r[0]),l.forEach(_),this.h()},h(){h(e,"class","text-xs pl-2 self-center")},m(t,l){I(t,e,l),m(e,a)},p(t,l){l&1&&se(a,t[0])},d(t){t&&_(e)}}}function he(r){let e,a,t,l,f,s,o,i,c,v,k,E,p=r[1]&&J(r),n=r[0]&&!r[1]&&Q(r);return{c(){e=w("div"),p&&p.c(),a=D(),t=w("button"),l=w("div"),f=V("svg"),s=V("path"),c=D(),n&&n.c(),this.h()},l(u){e=$(u,"DIV",{class:!0});var d=b(e);p&&p.l(d),a=A(d),t=$(d,"BUTTON",{class:!0,type:!0,"aria-label":!0});var g=b(t);l=$(g,"DIV",{class:!0});var T=b(l);f=S(T,"svg",{xmlns:!0,viewBox:!0,fill:!0,class:!0});var N=b(f);s=S(N,"path",{d:!0}),b(s).forEach(_),N.forEach(_),T.forEach(_),g.forEach(_),c=A(d),n&&n.l(d),d.forEach(_),this.h()},h(){h(s,"d","M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"),h(f,"xmlns","http://www.w3.org/2000/svg"),h(f,"viewBox","0 0 16 16"),h(f,"fill","currentColor"),h(f,"class",o="w-3 h-3 "+(r[1]?"rotate-45":"")+" transition-all transform"),h(l,"class","m-auto self-center"),h(t,"class","cursor-pointer self-center p-0.5 flex h-fit items-center dark:hover:bg-gray-700 rounded-full transition border dark:border-gray-600 border-dashed"),h(t,"type","button"),h(t,"aria-label",i=r[3].t("Add Tag")),h(e,"class",v="px-0.5 flex "+(r[1]?"flex-row-reverse":""))},m(u,d){I(u,e,d),p&&p.m(e,null),m(e,a),m(e,t),m(t,l),m(l,f),m(f,s),m(e,c),n&&n.m(e,null),k||(E=O(t,"click",r[9]),k=!0)},p(u,[d]){u[1]?p?p.p(u,d):(p=J(u),p.c(),p.m(e,a)):p&&(p.d(1),p=null),d&2&&o!==(o="w-3 h-3 "+(u[1]?"rotate-45":"")+" transition-all transform")&&h(f,"class",o),d&8&&i!==(i=u[3].t("Add Tag"))&&h(t,"aria-label",i),u[0]&&!u[1]?n?n.p(u,d):(n=Q(u),n.c(),n.m(e,null)):n&&(n.d(1),n=null),d&2&&v!==(v="px-0.5 flex "+(u[1]?"flex-row-reverse":""))&&h(e,"class",v)},i:F,o:F,d(u){u&&_(e),p&&p.d(),n&&n.d(),k=!1,E()}}}function de(r,e,a){let t,l;L(r,ie,n=>a(4,l=n));const f=Z(),s=ee("i18n");L(r,s,n=>a(3,t=n));let{label:o=""}=e,i=!1,c="";const v=async()=>{a(2,c=c.trim()),c!==""?(f("add",c),a(2,c=""),a(1,i=!1)):ue.error(t.t("Invalid Tag"))};function k(){c=this.value,a(2,c)}const E=n=>{n.key==="Enter"&&v()},p=()=>{a(1,i=!i)};return r.$$set=n=>{"label"in n&&a(0,o=n.label)},[o,i,c,t,l,s,v,k,E,p]}class pe extends q{constructor(e){super(),z(this,e,de,he,X,{label:0})}}function R(r,e,a){const t=r.slice();return t[3]=e[a],t}function ge(r){let e,a,t=r[3].name+"",l,f,s,o,i,c,v,k,E;i=new ce({props:{className:"size-3",strokeWidth:"2.5"}});function p(){return r[2](r[3])}return{c(){e=w("div"),a=w("div"),l=le(t),f=D(),s=w("div"),o=w("button"),P(i.$$.fragment),c=D(),this.h()},l(n){e=$(n,"DIV",{class:!0});var u=b(e);a=$(u,"DIV",{class:!0});var d=b(a);l=ae(d,t),d.forEach(_),f=A(u),s=$(u,"DIV",{class:!0});var g=b(s);o=$(g,"BUTTON",{class:!0,type:!0});var T=b(o);U(i.$$.fragment,T),T.forEach(_),g.forEach(_),u.forEach(_),c=A(n),this.h()},h(){h(a,"class","text-[0.7rem] font-medium self-center line-clamp-1 w-fit"),h(o,"class","rounded-full border bg-white dark:bg-gray-700 h-full flex self-center cursor-pointer"),h(o,"type","button"),h(s,"class","absolute invisible right-0.5 group-hover/tags:visible transition"),h(e,"class","relative group/tags px-1.5 py-[0.2px] gap-0.5 flex justify-between h-fit max-h-fit w-fit items-center rounded-full bg-gray-500/20 text-gray-700 dark:text-gray-200 transition cursor-pointer")},m(n,u){I(n,e,u),m(e,a),m(a,l),m(e,f),m(e,s),m(s,o),M(i,o,null),I(n,c,u),v=!0,k||(E=O(o,"click",p),k=!0)},p(n,u){r=n,(!v||u&1)&&t!==(t=r[3].name+"")&&se(l,t)},i(n){v||(y(i.$$.fragment,n),v=!0)},o(n){B(i.$$.fragment,n),v=!1},d(n){n&&(_(e),_(c)),j(i),k=!1,E()}}}function Y(r){let e,a;return e=new fe({props:{content:r[3].name,$$slots:{default:[ge]},$$scope:{ctx:r}}}),{c(){P(e.$$.fragment)},l(t){U(e.$$.fragment,t)},m(t,l){M(e,t,l),a=!0},p(t,l){const f={};l&1&&(f.content=t[3].name),l&65&&(f.$$scope={dirty:l,ctx:t}),e.$set(f)},i(t){a||(y(e.$$.fragment,t),a=!0)},o(t){B(e.$$.fragment,t),a=!1},d(t){j(e,t)}}}function _e(r){let e,a,t=x(r[0]),l=[];for(let s=0;s<t.length;s+=1)l[s]=Y(R(r,t,s));const f=s=>B(l[s],1,1,()=>{l[s]=null});return{c(){for(let s=0;s<l.length;s+=1)l[s].c();e=W()},l(s){for(let o=0;o<l.length;o+=1)l[o].l(s);e=W()},m(s,o){for(let i=0;i<l.length;i+=1)l[i]&&l[i].m(s,o);I(s,e,o),a=!0},p(s,[o]){if(o&3){t=x(s[0]);let i;for(i=0;i<t.length;i+=1){const c=R(s,t,i);l[i]?(l[i].p(c,o),y(l[i],1)):(l[i]=Y(c),l[i].c(),y(l[i],1),l[i].m(e.parentNode,e))}for(ne(),i=t.length;i<l.length;i+=1)f(i);oe()}},i(s){if(!a){for(let o=0;o<t.length;o+=1)y(l[o]);a=!0}},o(s){l=l.filter(Boolean);for(let o=0;o<l.length;o+=1)B(l[o]);a=!1},d(s){s&&_(e),te(l,s)}}}function me(r,e,a){const t=Z();let{tags:l=[]}=e;const f=s=>{t("delete",s.name)};return r.$$set=s=>{"tags"in s&&a(0,l=s.tags)},[l,t,f]}class ve extends q{constructor(e){super(),z(this,e,me,_e,X,{tags:0})}}function be(r){let e,a,t,l,f;return a=new ve({props:{tags:r[0]}}),a.$on("delete",r[4]),l=new pe({props:{label:r[0].length==0?r[1].t("Add Tags"):""}}),l.$on("add",r[5]),{c(){e=w("div"),P(a.$$.fragment),t=D(),P(l.$$.fragment),this.h()},l(s){e=$(s,"DIV",{class:!0});var o=b(e);U(a.$$.fragment,o),t=A(o),U(l.$$.fragment,o),o.forEach(_),this.h()},h(){h(e,"class","flex flex-row flex-wrap gap-1 line-clamp-1")},m(s,o){I(s,e,o),M(a,e,null),m(e,t),M(l,e,null),f=!0},p(s,[o]){const i={};o&1&&(i.tags=s[0]),a.$set(i);const c={};o&3&&(c.label=s[0].length==0?s[1].t("Add Tags"):""),l.$set(c)},i(s){f||(y(a.$$.fragment,s),y(l.$$.fragment,s),f=!0)},o(s){B(a.$$.fragment,s),B(l.$$.fragment,s),f=!1},d(s){s&&_(e),j(a),j(l)}}}function we(r,e,a){let t;const l=Z(),f=ee("i18n");L(r,f,c=>a(1,t=c));let{tags:s=[]}=e;const o=c=>{l("delete",c.detail)},i=c=>{l("add",c.detail)};return r.$$set=c=>{"tags"in c&&a(0,s=c.tags)},[s,t,l,f,o,i]}class Ae extends q{constructor(e){super(),z(this,e,we,be,X,{tags:0})}}export{Ae as T};
//# sourceMappingURL=BsHho0_v.js.map
