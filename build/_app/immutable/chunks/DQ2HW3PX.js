import{d as r}from"./DzLIgThl.js";const c=async(o,n)=>await fetch(`${r}/utils/gravatar?email=${n}`,{method:"GET",headers:{"Content-Type":"application/json",Authorization:`Bearer ${o}`}}).then(async a=>{if(!a.ok)throw await a.json();return a.json()}).catch(a=>null),l=async(o,n)=>{let e=null;const a=await fetch(`${r}/utils/code/execute`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${o}`},body:JSON.stringify({code:n})}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(e=t,t.detail&&(e=t.detail),null));if(e)throw e;return a},s=async(o,n)=>{let e=null;const a=await fetch(`${r}/utils/code/format`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${o}`},body:JSON.stringify({code:n})}).then(async t=>{if(!t.ok)throw await t.json();return t.json()}).catch(t=>(e=t,t.detail&&(e=t.detail),null));if(e)throw e;return a},d=async o=>{let n=null;if(await fetch(`${r}/utils/db/download`,{method:"GET",headers:{"Content-Type":"application/json",Authorization:`Bearer ${o}`}}).then(async e=>{if(!e.ok)throw await e.json();return e.blob()}).then(e=>{const a=window.URL.createObjectURL(e),t=document.createElement("a");t.href=a,t.download="webui.db",document.body.appendChild(t),t.click(),window.URL.revokeObjectURL(a)}).catch(e=>(n=e.detail,null)),n)throw n};export{d,l as e,s as f,c as g};
//# sourceMappingURL=DQ2HW3PX.js.map
