import{d as r}from"./DzLIgThl.js";const s=async(o="")=>{let n=null;const e=await fetch(`${r}/evaluations/config`,{method:"GET",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).then(t=>t).catch(t=>(n=t.detail,null));if(n)throw n;return e},l=async(o,n)=>{let e=null;const t=await fetch(`${r}/evaluations/config`,{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`},body:JSON.stringify({...n})}).then(async a=>{if(!a.ok)throw await a.json();return a.json()}).catch(a=>(e=a.detail,null));if(e)throw e;return t},h=async(o="")=>{let n=null;const e=await fetch(`${r}/evaluations/feedbacks/all`,{method:"GET",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).then(t=>t).catch(t=>(n=t.detail,null));if(n)throw n;return e},u=async(o="")=>{let n=null;const e=await fetch(`${r}/evaluations/feedbacks/all/export`,{method:"GET",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).then(t=>t).catch(t=>(n=t.detail,null));if(n)throw n;return e},p=async(o,n)=>{let e=null;const t=await fetch(`${r}/evaluations/feedback`,{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`},body:JSON.stringify({...n})}).then(async a=>{if(!a.ok)throw await a.json();return a.json()}).catch(a=>(e=a.detail,null));if(e)throw e;return t},d=async(o,n,e)=>{let t=null;const a=await fetch(`${r}/evaluations/feedback/${n}`,{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`},body:JSON.stringify({...e})}).then(async i=>{if(!i.ok)throw await i.json();return i.json()}).catch(i=>(t=i.detail,null));if(t)throw t;return a},f=async(o,n)=>{let e=null;const t=await fetch(`${r}/evaluations/feedback/${n}`,{method:"DELETE",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${o}`}}).then(async a=>{if(!a.ok)throw await a.json();return a.json()}).catch(a=>(e=a.detail,null));if(e)throw e;return t};export{s as a,l as b,p as c,f as d,u as e,h as g,d as u};
//# sourceMappingURL=DWqM7rJl.js.map
