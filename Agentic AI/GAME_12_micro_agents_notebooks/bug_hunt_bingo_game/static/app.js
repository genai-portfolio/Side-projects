(() => {
  let state=window.__INITIAL_GAME__||null;
  const gridEl=document.getElementById("bingo-grid"),msgEl=document.getElementById("bingo-msg"),newBtn=document.getElementById("new-btn"),statsEl=document.getElementById("stats");

  function render(){
    if(!state?.state)return;const s=state.state;
    gridEl.innerHTML="";
    const bingoIdxs=new Set();
    (s.bingo_lines||[]).forEach(line=>line.forEach(i=>bingoIdxs.add(i)));
    s.cells.forEach(c=>{
      const d=document.createElement("div");
      d.className="bingo-cell"+(c.marked?" marked":"")+(bingoIdxs.has(c.index-1)&&c.marked?" bingo-line":"");
      d.textContent=(c.marked?"✗ ":"")+c.name;
      d.addEventListener("click",()=>toggle(c.index));
      gridEl.appendChild(d);
    });
    if(s.bingo)msgEl.textContent="🎉 BINGO! You got a line!";
    else msgEl.textContent=s.marked_count>0?`${s.marked_count}/9 marked`:"Click a bug when you find it!";
    statsEl.innerHTML="";
    [["Marked",s.marked_count],["Bingos Won",s.total_games]].forEach(([l,v])=>{const d=document.createElement("div");d.className="stat";d.innerHTML=`<div class="stat-label">${l}</div><div class="stat-value">${v}</div>`;statsEl.appendChild(d);});
  }

  async function toggle(idx){
    const r=await(await fetch("/api/toggle",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({index:idx})})).json();
    if(r.state){state={goals:state.goals,state:r.state};render();}
  }

  newBtn.addEventListener("click",async()=>{
    const r=await(await fetch("/api/new_card",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"})).json();
    if(r.state){state={goals:state.goals,state:r.state};render();}
    msgEl.textContent=r.message||"";
  });

  document.addEventListener("DOMContentLoaded",render);
})();
