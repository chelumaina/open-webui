import{s as pe,k as R,l as ue,m as ve,d,o as q,i as x,j as U,p as be,y as H,e as p,t as G,c as v,a as b,b as J,f as g,g as n,u as ye,h as K,A as Q,C as X}from"../chunks/vexCXLX9.js";import{S as we,i as Ie,t as z,a as $,c as ke,f as Y,b as Ee,d as Se,m as De,e as Ve,g as Me}from"../chunks/Cdll-xsj.js";import{g as Z}from"../chunks/WDSA219a.js";import{p as Ce}from"../chunks/B9-t4RFp.js";import{d as ee}from"../chunks/aTHIJebK.js";import{i as fe,a as Le,c as Be,W as je,m as Ne}from"../chunks/DzLIgThl.js";import{l as Ue,d as Ae,f as Pe}from"../chunks/hvQ-lebT.js";import{g as Te,c as We}from"../chunks/-eX2sS6k.js";import{M as Oe}from"../chunks/DvsQLqqp.js";import{t as Re}from"../chunks/DMk2eJ1b.js";import"../chunks/Dq9WPRw5.js";import"../chunks/CyFe254w.js";import"../chunks/_0_gBwjO.js";import{g as qe}from"../chunks/CP68AaU9.js";import{g as ze}from"../chunks/Du-v1D_Q.js";import"../chunks/CoGXDCUN.js";import"../chunks/BdiJpjKL.js";import"../chunks/DpyNzh6D.js";function me(e){let f,t,i,c,s,a,u,N,E,S,I=ee(e[4].chat.timestamp).format("LLL")+"",j,w,D,V,_,k,h,A,P,L,B,M,o=e[10].t("Clone Chat")+"",r,C,F,se;function ge(l){e[15](l)}function _e(l){e[16](l)}function he(l){e[17](l)}let T={className:"h-full flex pt-4 pb-8",user:e[5],chatId:e[8],readOnly:!0,selectedModels:e[3],processing:He,bottomPadding:e[12].length>0,sendPrompt:Ge,continueResponse:Je,regenerateResponse:Ke};return e[0]!==void 0&&(T.history=e[0]),e[7]!==void 0&&(T.messages=e[7]),e[2]!==void 0&&(T.autoScroll=e[2]),_=new Oe({props:T}),H.push(()=>Y(_,"history",ge)),H.push(()=>Y(_,"messages",_e)),H.push(()=>Y(_,"autoScroll",he)),{c(){f=p("div"),t=p("div"),i=p("div"),c=p("div"),s=p("div"),a=p("div"),u=G(e[6]),N=R(),E=p("div"),S=p("div"),j=G(I),w=R(),D=p("div"),V=p("div"),Ee(_.$$.fragment),P=R(),L=p("div"),B=p("div"),M=p("button"),r=G(o),this.h()},l(l){f=v(l,"DIV",{class:!0});var m=b(f);t=v(m,"DIV",{class:!0});var y=b(t);i=v(y,"DIV",{class:!0,id:!0});var W=b(i);c=v(W,"DIV",{class:!0});var te=b(c);s=v(te,"DIV",{class:!0});var O=b(s);a=v(O,"DIV",{class:!0});var ae=b(a);u=J(ae,e[6]),ae.forEach(d),N=q(O),E=v(O,"DIV",{class:!0});var oe=b(E);S=v(oe,"DIV",{class:!0});var le=b(S);j=J(le,I),le.forEach(d),oe.forEach(d),O.forEach(d),te.forEach(d),w=q(W),D=v(W,"DIV",{class:!0});var re=b(D);V=v(re,"DIV",{class:!0});var ie=b(V);Se(_.$$.fragment,ie),ie.forEach(d),re.forEach(d),W.forEach(d),P=q(y),L=v(y,"DIV",{class:!0});var ne=b(L);B=v(ne,"DIV",{class:!0});var ce=b(B);M=v(ce,"BUTTON",{class:!0});var de=b(M);r=J(de,o),de.forEach(d),ce.forEach(d),ne.forEach(d),y.forEach(d),m.forEach(d),this.h()},h(){g(a,"class","text-2xl font-semibold line-clamp-1"),g(S,"class","text-gray-400"),g(E,"class","flex text-sm justify-between items-center mt-1"),g(s,"class","px-3"),g(c,"class","pt-5 px-2 w-full max-w-5xl mx-auto"),g(V,"class",""),g(D,"class","h-full w-full flex flex-col py-2"),g(i,"class","flex flex-col w-full flex-auto overflow-auto h-0"),g(i,"id","messages-container"),g(M,"class","px-4 py-2 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"),g(B,"class","pb-5"),g(L,"class","absolute bottom-0 right-0 left-0 flex justify-center w-full bg-linear-to-b from-transparent to-white dark:to-gray-900"),g(t,"class","flex flex-col flex-auto justify-center relative"),g(f,"class","h-screen max-h-[100dvh] w-full flex flex-col text-gray-700 dark:text-gray-100 bg-white dark:bg-gray-900")},m(l,m){x(l,f,m),n(f,t),n(t,i),n(i,c),n(c,s),n(s,a),n(a,u),n(s,N),n(s,E),n(E,S),n(S,j),n(i,w),n(i,D),n(D,V),De(_,V,null),n(t,P),n(t,L),n(L,B),n(B,M),n(M,r),C=!0,F||(se=ye(M,"click",e[13]),F=!0)},p(l,m){(!C||m&64)&&K(u,l[6]),(!C||m&16)&&I!==(I=ee(l[4].chat.timestamp).format("LLL")+"")&&K(j,I);const y={};m&32&&(y.user=l[5]),m&256&&(y.chatId=l[8]),m&8&&(y.selectedModels=l[3]),!k&&m&1&&(k=!0,y.history=l[0],Q(()=>k=!1)),!h&&m&128&&(h=!0,y.messages=l[7],Q(()=>h=!1)),!A&&m&4&&(A=!0,y.autoScroll=l[2],Q(()=>A=!1)),_.$set(y),(!C||m&1024)&&o!==(o=l[10].t("Clone Chat")+"")&&K(r,o)},i(l){C||(z(_.$$.fragment,l),C=!0)},o(l){$(_.$$.fragment,l),C=!1},d(l){l&&d(f),Ve(_),F=!1,se()}}}function Fe(e){let f,t,i,c;document.title=f=`
		`+(e[6]?`${e[6].length>30?`${e[6].slice(0,30)}...`:e[6]} | ${e[9]}`:`${e[9]}`)+`
	`;let s=e[1]&&me(e);return{c(){t=R(),s&&s.c(),i=ue()},l(a){ve("svelte-1123lr8",document.head).forEach(d),t=q(a),s&&s.l(a),i=ue()},m(a,u){x(a,t,u),s&&s.m(a,u),x(a,i,u),c=!0},p(a,[u]){(!c||u&576)&&f!==(f=`
		`+(a[6]?`${a[6].length>30?`${a[6].slice(0,30)}...`:a[6]} | ${a[9]}`:`${a[9]}`)+`
	`)&&(document.title=f),a[1]?s?(s.p(a,u),u&2&&z(s,1)):(s=me(a),s.c(),z(s,1),s.m(i.parentNode,i)):s&&(Me(),$(s,1,1,()=>{s=null}),ke())},i(a){c||(z(s),c=!0)},o(a){$(s),c=!1},d(a){a&&(d(t),d(i)),s&&s.d(a)}}}let He="";const Ge=()=>{},Je=()=>{},Ke=()=>{};function Qe(e,f,t){let i,c,s,a,u,N;U(e,fe,o=>t(8,i=o)),U(e,Ce,o=>t(14,c=o)),U(e,Le,o=>t(18,s=o)),U(e,Be,o=>t(19,a=o)),U(e,je,o=>t(9,u=o));const E=be("i18n");U(e,E,o=>t(10,N=o)),ee.extend(Ue);let S=!1,I=!0,j=[""],w=null,D=null,V="",_=[],k=[],h={messages:{},currentId:null};const A=async()=>{var o;if(await Ne.set(await qe(localStorage.token,((o=a==null?void 0:a.features)==null?void 0:o.enable_direct_connections)&&((s==null?void 0:s.directConnections)??null))),await fe.set(c.params.id),t(4,w=await Te(localStorage.token,i).catch(async r=>(await Z("/"),null))),w){t(5,D=await ze(localStorage.token,w.user_id).catch(C=>(console.error(C),null)));const r=w.chat;return r?(console.log(r),t(3,j=((r==null?void 0:r.models)??void 0)!==void 0?r.models:[r.models??""]),t(0,h=((r==null?void 0:r.history)??void 0)!==void 0?r.history:Pe(r.messages)),t(6,V=r.title),t(2,I=!0),await X(),k.length>0&&t(0,h.messages[k.at(-1).id].done=!0,h),await X(),!0):null}},P=async()=>{if(!w)return;const o=await We(localStorage.token,w.id).catch(r=>(Re.error(`${r}`),null));o&&Z(`/c/${o.id}`)};function L(o){h=o,t(0,h)}function B(o){k=o,t(7,k),t(0,h)}function M(o){I=o,t(2,I)}return e.$$.update=()=>{e.$$.dirty&1&&t(7,k=Ae(h,h.currentId)),e.$$.dirty&16384&&c.params.id&&(async()=>await A()?(await X(),t(1,S=!0)):await Z("/"))()},[h,S,I,j,w,D,V,k,i,u,N,E,_,P,c,L,B,M]}class ms extends we{constructor(f){super(),Ie(this,f,Qe,Fe,pe,{})}}export{ms as component};
//# sourceMappingURL=37.SWMwUupF.js.map
