(() => {
  const api = {
    async getState() { return (await fetch("/api/state")).json(); },
    async question(topic) { return (await fetch("/api/question", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ topic }) })).json(); },
    async answer(topic, question, answer, confidence) { return (await fetch("/api/answer", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ topic, question, answer, confidence }) })).json(); },
  };

  const tabsEl = document.getElementById("topic-tabs");
  const qCard = document.getElementById("question-card");
  const qText = document.getElementById("q-text");
  const ansForm = document.getElementById("answer-form");
  const ansInput = document.getElementById("answer-input");
  const ansFeedback = document.getElementById("answer-feedback");
  const confBtns = document.getElementById("conf-btns");
  const statsEl = document.getElementById("stats-summary");
  const recentEl = document.getElementById("recent-logs");

  let state = window.__INITIAL_GAME__ || null;
  let currentTopic = "";
  let currentQuestion = "";
  let selectedConf = 3;

  function renderTabs() {
    if (!state?.state) return;
    tabsEl.innerHTML = "";
    state.state.topics.forEach(t => {
      const btn = document.createElement("button");
      btn.className = "topic-tab" + (t === currentTopic ? " active" : "");
      btn.textContent = t.toUpperCase() + ` (${state.state.per_topic_count[t] || 0})`;
      btn.addEventListener("click", () => pickTopic(t));
      tabsEl.appendChild(btn);
    });
  }

  function renderConf() {
    confBtns.innerHTML = "";
    for (let i = 1; i <= 5; i++) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "conf-btn" + (i === selectedConf ? " selected" : "");
      b.textContent = i;
      b.addEventListener("click", () => { selectedConf = i; renderConf(); });
      confBtns.appendChild(b);
    }
  }

  function renderStats() {
    if (!state?.state) return;
    statsEl.innerHTML = "";
    const s = state.state;
    [["Total Attempts", s.attempt_count]].concat(s.topics.map(t => [t.toUpperCase(), s.per_topic_count[t] || 0]))
      .forEach(([l, v]) => { const d = document.createElement("div"); d.className = "stat"; d.innerHTML = `<div class="stat-label">${l}</div><div class="stat-value">${v}</div>`; statsEl.appendChild(d); });
  }

  function renderRecent() {
    if (!state?.state) return;
    recentEl.innerHTML = "";
    (state.state.recent || []).forEach(a => {
      const d = document.createElement("div"); d.className = "log-entry";
      d.innerHTML = `<span class="log-topic">${a.topic}</span><span class="log-q">${a.question}</span><div class="log-a">${a.answer}</div><span class="log-conf">Confidence: ${a.confidence}/5</span>`;
      recentEl.appendChild(d);
    });
  }

  function refresh(ns) { state = ns; renderTabs(); renderStats(); renderRecent(); }

  async function pickTopic(topic) {
    currentTopic = topic;
    renderTabs();
    ansFeedback.textContent = "";
    try {
      const r = await api.question(topic);
      if (r.error) { ansFeedback.textContent = r.error; return; }
      currentQuestion = r.question;
      qText.textContent = r.question;
      qCard.classList.remove("hidden");
      qCard.style.animation = "none"; void qCard.offsetHeight; qCard.style.animation = "";
      ansInput.value = ""; ansInput.focus();
    } catch (e) { ansFeedback.textContent = "Failed to load question."; }
  }

  ansForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const ans = ansInput.value.trim();
    if (!ans) return;
    ansFeedback.textContent = "Saving…";
    try {
      const r = await api.answer(currentTopic, currentQuestion, ans, selectedConf);
      if (r.state) refresh({ goals: state.goals, state: r.state });
      ansFeedback.textContent = r.message || "Logged!";
      ansInput.value = "";
      // Auto-load next question
      setTimeout(() => pickTopic(currentTopic), 800);
    } catch (e) { ansFeedback.textContent = "Could not save."; }
  });

  document.addEventListener("DOMContentLoaded", () => {
    renderConf();
    if (state) { renderTabs(); renderStats(); renderRecent(); }
    else api.getState().then(refresh).catch(console.error);
  });
})();
