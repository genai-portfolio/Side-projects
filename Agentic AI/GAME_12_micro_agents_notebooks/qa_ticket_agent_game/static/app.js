(() => {
  let state=window.__INITIAL_GAME__||null, selectedUrg="medium";
  const form=document.getElementById("ticket-form"),ticketCard=document.getElementById("ticket-card"),ticketText=document.getElementById("ticket-text"),copyBtn=document.getElementById("copy-btn"),statsEl=document.getElementById("stats"),historyEl=document.getElementById("history");

  // Urgency buttons
  document.querySelectorAll(".urg-btn").forEach(b=>{b.addEventListener("click",()=>{document.querySelectorAll(".urg-btn").forEach(x=>x.classList.remove("selected"));b.classList.add("selected");selectedUrg=b.dataset.u;});});

  function render(){if(!state?.state)return;const s=state.state;
    statsEl.innerHTML="";[["Total Tickets",s.total_tickets],["High 🔴",s.urgency_counts.high||0],["Medium 🟡",s.urgency_counts.medium||0],["Low 🟢",s.urgency_counts.low||0]].forEach(([l,v])=>{const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">${l}</div><div class="stat-value">${v}</div>`;statsEl.appendChild(d);});
    historyEl.innerHTML="";(s.recent||[]).forEach(t=>{const d=document.createElement("div");d.className="log-entry";d.innerHTML=`<span class="log-id">#${t.id}</span> <span class="log-urgency ${t.urgency}">${t.urgency}</span> ${t.question.slice(0,60)}`;historyEl.appendChild(d);});}

  form.addEventListener("submit",async e=>{e.preventDefault();
    const q=document.getElementById("f-q").value.trim();if(!q)return;
    const body={question:q,topic:document.getElementById("f-topic").value.trim(),tried:document.getElementById("f-tried").value.trim(),expected:document.getElementById("f-expected").value.trim(),actual:document.getElementById("f-actual").value.trim(),urgency:selectedUrg};
    try{const r=await(await fetch("/api/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)})).json();
      if(r.error)return;ticketText.textContent=r.ticket.formatted;ticketCard.classList.remove("hidden");ticketCard.style.animation="none";void ticketCard.offsetHeight;ticketCard.style.animation="";
      if(r.state){state={goals:state.goals,state:r.state};render();}form.reset();document.querySelectorAll(".urg-btn").forEach(x=>x.classList.remove("selected"));document.querySelector('.urg-btn[data-u="medium"]').classList.add("selected");selectedUrg="medium";}catch(e){console.error(e);}});

  copyBtn.addEventListener("click",()=>{navigator.clipboard.writeText(ticketText.textContent).then(()=>copyBtn.textContent="Copied! ✅").catch(()=>{});setTimeout(()=>copyBtn.textContent="Copy to Clipboard 📋",2000);});

  document.addEventListener("DOMContentLoaded",render);
})();
