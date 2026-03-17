(() => {
  let state=window.__INITIAL_GAME__||null;
  const form=document.getElementById("decide-form"),resultCard=document.getElementById("result-card"),winnerEl=document.getElementById("winner"),scoresBar=document.getElementById("scores-bar"),statsEl=document.getElementById("stats"),historyEl=document.getElementById("history");
  function render(){if(!state?.state)return;const s=state.state;
    statsEl.innerHTML="";const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">Total Decisions</div><div class="stat-value">${s.total_decisions}</div>`;statsEl.appendChild(d);
    historyEl.innerHTML="";(s.recent||[]).forEach(r=>{const d=document.createElement("div");d.className="log-entry";d.innerHTML=`<span class="log-winner">🏆 ${r.winner}</span> — ${r.option_a} (${r.score_a}) vs ${r.option_b} (${r.score_b})`;historyEl.appendChild(d);});}
  form.addEventListener("submit",async e=>{e.preventDefault();
    const oa=document.getElementById("opt-a").value.trim(),ob=document.getElementById("opt-b").value.trim();if(!oa||!ob)return;
    const sa={time:+document.getElementById("sa-time").value,difficulty:+document.getElementById("sa-diff").value,impact:+document.getElementById("sa-impact").value};
    const sb={time:+document.getElementById("sb-time").value,difficulty:+document.getElementById("sb-diff").value,impact:+document.getElementById("sb-impact").value};
    try{const r=await(await fetch("/api/decide",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({option_a:oa,option_b:ob,scores_a:sa,scores_b:sb})})).json();
      if(r.error)return;
      winnerEl.textContent=`🏆 Winner: ${r.winner}`;
      scoresBar.innerHTML=`<div class="score-bar"><div class="score-label">${r.option_a}</div><div class="score-value${r.winner===r.option_a?" winner":""}">${r.score_a}</div></div><div class="score-bar"><div class="score-label">${r.option_b}</div><div class="score-value${r.winner===r.option_b?" winner":""}">${r.score_b}</div></div>`;
      resultCard.classList.remove("hidden");resultCard.style.animation="none";void resultCard.offsetHeight;resultCard.style.animation="";
      if(r.state){state={goals:state.goals,state:r.state};render();}}catch(e){console.error(e);}});
  document.addEventListener("DOMContentLoaded",render);
})();
