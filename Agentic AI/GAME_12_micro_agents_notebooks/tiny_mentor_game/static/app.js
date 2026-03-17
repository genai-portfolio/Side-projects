(() => {
  let state=window.__INITIAL_GAME__||null;
  const form=document.getElementById("progress-form"),input=document.getElementById("progress-input"),card=document.getElementById("response-card"),praiseEl=document.getElementById("praise"),challengeEl=document.getElementById("challenge"),statsEl=document.getElementById("stats"),logsEl=document.getElementById("logs");
  function render(){if(!state?.state)return;const s=state.state;statsEl.innerHTML="";const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">Total Sessions</div><div class="stat-value">${s.total_sessions}</div>`;statsEl.appendChild(d);
    logsEl.innerHTML="";(s.recent||[]).forEach(l=>{const d=document.createElement("div");d.className="log-entry";d.innerHTML=`<div class="log-progress">${l.progress}</div><div class="log-detail">💬 ${l.praise} | 🎯 ${l.challenge}</div>`;logsEl.appendChild(d);});}
  form.addEventListener("submit",async e=>{e.preventDefault();const t=input.value.trim();if(!t)return;try{const r=await(await fetch("/api/mentor",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({progress:t})})).json();if(r.error)return;praiseEl.textContent=`"${r.praise}"`;challengeEl.textContent=r.challenge;card.classList.remove("hidden");card.style.animation="none";void card.offsetHeight;card.style.animation="";if(r.state){state={goals:state.goals,state:r.state};render();}input.value="";}catch(e){console.error(e);}});
  document.addEventListener("DOMContentLoaded",render);
})();
