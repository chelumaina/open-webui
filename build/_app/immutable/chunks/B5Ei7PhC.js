import{R as a}from"./DzLIgThl.js";const c=async r=>{let n=null;const e=await fetch(`${a}/config`,{method:"GET",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(n=t.detail,null));if(n)throw n;return e},h=async(r,n)=>{let e=null;const t=await fetch(`${a}/config/update`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`},body:JSON.stringify({...n})}).then(async o=>{if(!o.ok)throw await o.json();return o.json()}).catch(o=>(e=o.detail,null));if(e)throw e;return t},u=async r=>{let n=null;const e=await fetch(`${a}/query/settings`,{method:"GET",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(n=t.detail,null));if(n)throw n;return e},l=async(r,n)=>{let e=null;const t=await fetch(`${a}/query/settings/update`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`},body:JSON.stringify({...n})}).then(async o=>{if(!o.ok)throw await o.json();return o.json()}).catch(o=>(e=o.detail,null));if(e)throw e;return t},d=async r=>{let n=null;const e=await fetch(`${a}/embedding`,{method:"GET",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(n=t.detail,null));if(n)throw n;return e},p=async(r,n)=>{let e=null;const t=await fetch(`${a}/embedding/update`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`},body:JSON.stringify({...n})}).then(async o=>{if(!o.ok)throw await o.json();return o.json()}).catch(o=>(e=o.detail,null));if(e)throw e;return t},f=async r=>{let n=null;const e=await fetch(`${a}/reranking`,{method:"GET",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(n=t.detail,null));if(n)throw n;return e},y=async(r,n)=>{let e=null;const t=await fetch(`${a}/reranking/update`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${r}`},body:JSON.stringify({...n})}).then(async o=>{if(!o.ok)throw await o.json();return o.json()}).catch(o=>(e=o.detail,null));if(e)throw e;return t},w=async(r,n)=>{let e=null;const t=await fetch(`${a}/process/youtube`,{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${r}`},body:JSON.stringify({url:n})}).then(async o=>{if(!o.ok)throw await o.json();return o.json()}).catch(o=>(e=o.detail,null));if(e)throw e;return t},j=async(r,n,e)=>{let t=null;const o=await fetch(`${a}/process/web`,{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json",authorization:`Bearer ${r}`},body:JSON.stringify({url:e,collection_name:n})}).then(async i=>{if(!i.ok)throw await i.json();return i.json()}).catch(i=>(t=i.detail,null));if(t)throw t;return o},g=async r=>{let n=null;const e=await fetch(`${a}/reset/db`,{method:"POST",headers:{Accept:"application/json",authorization:`Bearer ${r}`}}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(n=t.detail,null));if(n)throw n;return e};export{c as a,h as b,l as c,d,f as e,p as f,u as g,w as h,j as p,g as r,y as u};
//# sourceMappingURL=B5Ei7PhC.js.map
