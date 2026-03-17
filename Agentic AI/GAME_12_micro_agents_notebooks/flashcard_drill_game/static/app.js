(() => {
  const api = {
    async draw() { return (await fetch("/api/draw",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"})).json(); },
    async rate(question,rating) { return (await fetch("/api/rate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,rating})})).json(); },
    async addCard(q,a) { return (await fetch("/api/add_card",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({q,a})})).json(); },
  };

  const flashcard=document.getElementById("flashcard"),cardQ=document.getElementById("card-q"),cardA=document.getElementById("card-a");
  const drawBtn=document.getElementById("draw-btn"),flipBtn=document.getElementById("flip-btn");
  const ratingBar=document.getElementById("rating-bar"),feedback=document.getElementById("card-feedback");
  const statsEl=document.getElementById("stats"),cardsListEl=document.getElementById("cards-list");
  const addForm=document.getElementById("add-form"),newQ=document.getElementById("new-q"),newA=document.getElementById("new-a");

  let state=window.__INITIAL_GAME__||null, currentQ="", isFlipped=false;

  function renderStats(){
    if(!state?.state)return; const s=state.state; statsEl.innerHTML="";
    [["Total Cards",s.total_cards],["Total Reviews",s.total_reviews]].forEach(([l,v])=>{const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">${l}</div><div class="stat-value">${v}</div>`;statsEl.appendChild(d);});
  }
  function renderCards(){
    if(!state?.state)return; cardsListEl.innerHTML="";
    state.state.cards.forEach(c=>{const d=document.createElement("div");d.className="cl-row";
      d.innerHTML=`<div>${c.q}</div><div class="cl-ratings">E:${c.ratings.easy||0} M:${c.ratings.medium||0} H:${c.ratings.hard||0} (${c.total_reviews} reviews)</div>`;
      cardsListEl.appendChild(d);});
  }
  function refresh(ns){state=ns;renderStats();renderCards();}
  function resetFlip(){flashcard.classList.remove("flipped");isFlipped=false;}

  drawBtn.addEventListener("click",async()=>{
    resetFlip();ratingBar.classList.add("hidden");feedback.textContent="";
    const r=await api.draw();if(r.state)refresh({goals:state.goals,state:r.state});
    currentQ=r.q;cardQ.textContent=r.q;cardA.textContent=r.a;flipBtn.disabled=false;
  });

  flipBtn.addEventListener("click",()=>{
    if(!currentQ)return;
    isFlipped=!isFlipped;
    if(isFlipped){flashcard.classList.add("flipped");ratingBar.classList.remove("hidden");}
    else{flashcard.classList.remove("flipped");ratingBar.classList.add("hidden");}
  });

  flashcard.addEventListener("click",()=>{if(currentQ)flipBtn.click();});

  ratingBar.querySelectorAll("button").forEach(b=>b.addEventListener("click",async()=>{
    const rating=b.dataset.r;feedback.textContent="Saving…";
    const r=await api.rate(currentQ,rating);if(r.state)refresh({goals:state.goals,state:r.state});
    feedback.textContent=r.message||"Rated!";ratingBar.classList.add("hidden");
  }));

  addForm.addEventListener("submit",async e=>{
    e.preventDefault();const q=newQ.value.trim(),a=newA.value.trim();if(!q||!a)return;
    const r=await api.addCard(q,a);if(r.state)refresh({goals:state.goals,state:r.state});
    feedback.textContent=r.message||"";newQ.value="";newA.value="";
  });

  document.addEventListener("DOMContentLoaded",()=>{if(state){renderStats();renderCards();}});
})();
