(() => {
  let state=window.__INITIAL_GAME__||null;
  const form=document.getElementById("desc-form"),descInput=document.getElementById("desc-input"),stepCard=document.getElementById("step-card"),stepType=document.getElementById("step-type"),stepText=document.getElementById("step-text"),statsEl=document.getElementById("stats"),historyEl=document.getElementById("history");
  function render(){if(!state?.state)return;const s=state.state;
    statsEl.innerHTML="";const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">Total Plans</div><div class="stat-value">${s.total_plans}</div>`;statsEl.appendChild(d);
    historyEl.innerHTML="";(s.recent||[]).forEach(p=>{const d=document.createElement("div");d.className="log-entry";d.innerHTML=`<span class="log-type">${p.step_type}</span> ${p.description.slice(0,60)}… → ${p.step.slice(0,80)}`;historyEl.appendChild(d);});}
  form.addEventListener("submit",async e=>{e.preventDefault();const desc=descInput.value.trim();if(!desc)return;
    try{const r=await(await fetch("/api/step",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({description:desc})})).json();
      if(r.error)return;stepType.textContent=`🎯 ${r.step_type}`;stepText.textContent=r.step;stepCard.classList.remove("hidden");stepCard.style.animation="none";void stepCard.offsetHeight;stepCard.style.animation="";
      if(r.state){state={goals:state.goals,state:r.state};render();}descInput.value="";}catch(e){console.error(e);}});
  document.addEventListener("DOMContentLoaded",render);
})();
