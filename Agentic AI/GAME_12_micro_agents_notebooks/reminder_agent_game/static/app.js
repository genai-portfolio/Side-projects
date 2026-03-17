(() => {
  let state=window.__INITIAL_GAME__||null;
  const form=document.getElementById("set-form"),minInput=document.getElementById("minutes-input"),taskInput=document.getElementById("task-input"),feedback=document.getElementById("set-feedback"),activeEl=document.getElementById("active-list"),statsEl=document.getElementById("stats"),historyEl=document.getElementById("history");
  function fmt(sec){const m=Math.floor(sec/60),s=sec%60;return `${m}:${String(s).padStart(2,"0")}`;}
  function render(){if(!state?.state)return;const s=state.state;
    activeEl.innerHTML="";(s.active||[]).forEach(r=>{const d=document.createElement("div");d.className="active-item";d.innerHTML=`<span class="active-task">${r.task}</span><span class="active-time">${fmt(r.remaining_sec)}</span>`;activeEl.appendChild(d);});
    statsEl.innerHTML="";[["Total Set",s.total_set],["Completed",s.total_done]].forEach(([l,v])=>{const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">${l}</div><div class="stat-value">${v}</div>`;statsEl.appendChild(d);});
    historyEl.innerHTML="";(s.history||[]).forEach(r=>{const d=document.createElement("div");d.className="log-entry";d.textContent=`✅ ${r.task} (${r.minutes}min)`;historyEl.appendChild(d);});}
  form.addEventListener("submit",async e=>{e.preventDefault();const m=parseInt(minInput.value),t=taskInput.value.trim();if(!m||!t)return;feedback.textContent="Setting…";
    const r=await(await fetch("/api/set",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({minutes:m,task:t})})).json();
    feedback.textContent=r.message||"";if(r.state){state={goals:state.goals,state:r.state};render();}minInput.value="";taskInput.value="";});
  // Poll every 5 seconds to update countdowns and check for fired reminders
  setInterval(async()=>{try{const r=await(await fetch("/api/poll",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"})).json();
    if(r.fired&&r.fired.length>0)r.fired.forEach(t=>alert(`⏰ REMINDER: ${t}`));
    if(r.state){state={goals:state.goals,state:r.state};render();}}catch(e){}},5000);
  document.addEventListener("DOMContentLoaded",render);
})();
