(() => {
  let state=window.__INITIAL_GAME__||null, lastCleaned="";
  const rawInput=document.getElementById("raw-input"),cleanOutput=document.getElementById("clean-output"),cleanBtn=document.getElementById("clean-btn"),downloadBtn=document.getElementById("download-btn"),feedback=document.getElementById("feedback"),statsEl=document.getElementById("stats");
  function renderStats(){if(!state?.state)return;statsEl.innerHTML="";const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">Total Cleans</div><div class="stat-value">${state.state.total_cleans}</div>`;statsEl.appendChild(d);}
  cleanBtn.addEventListener("click",async()=>{const raw=rawInput.value.trim();if(!raw)return;feedback.textContent="Cleaning…";try{const r=await(await fetch("/api/clean",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({raw})})).json();if(r.error){feedback.textContent=r.error;return;}cleanOutput.textContent=r.cleaned;lastCleaned=r.cleaned;feedback.textContent=r.message||"";downloadBtn.disabled=false;if(r.state)state={goals:state.goals,state:r.state};renderStats();}catch(e){feedback.textContent="Failed.";}});
  downloadBtn.addEventListener("click",()=>{if(!lastCleaned)return;const blob=new Blob([lastCleaned],{type:"text/markdown"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="clean_notes.md";a.click();});
  document.addEventListener("DOMContentLoaded",()=>renderStats());
})();
