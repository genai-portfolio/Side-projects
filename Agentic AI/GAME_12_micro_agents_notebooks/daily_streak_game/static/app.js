(() => {
  const api = {
    async getState() { return (await fetch("/api/state")).json(); },
    async log(text) {
      return (await fetch("/api/log", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) })).json();
    },
  };

  const streakEl = document.getElementById("streak-number");
  const flameEl = document.getElementById("flame");
  const calendarEl = document.getElementById("calendar");
  const logForm = document.getElementById("log-form");
  const logInput = document.getElementById("log-input");
  const logFeedback = document.getElementById("log-feedback");
  const milestoneMsg = document.getElementById("milestone-msg");
  const statsEl = document.getElementById("stats-summary");
  const recentEl = document.getElementById("recent-logs");

  let state = window.__INITIAL_GAME__ || null;

  function render() {
    if (!state || !state.state) return;
    const s = state.state;

    streakEl.textContent = s.streak;
    flameEl.style.opacity = s.streak > 0 ? "1" : "0.3";

    // Calendar
    calendarEl.innerHTML = "";
    (s.calendar || []).forEach((d) => {
      const div = document.createElement("div");
      div.className = "cal-day" + (d.active ? " active" : "");
      const tip = document.createElement("span");
      tip.className = "tooltip";
      tip.textContent = d.date;
      div.appendChild(tip);
      calendarEl.appendChild(div);
    });

    // Stats
    statsEl.innerHTML = "";
    [["Current Streak", s.streak], ["Longest Streak", s.longest], ["Total Days", s.total_days]].forEach(([label, val]) => {
      const div = document.createElement("div");
      div.className = "stat";
      div.innerHTML = `<div class="stat-label">${label}</div><div class="stat-value">${val}</div>`;
      statsEl.appendChild(div);
    });

    // Recent logs
    recentEl.innerHTML = "";
    (s.recent_logs || []).forEach((l) => {
      const div = document.createElement("div");
      div.className = "log-entry";
      div.innerHTML = `<span class="log-entry-date">${l.date}</span><span class="log-entry-text">${l.text}</span>`;
      recentEl.appendChild(div);
    });
  }

  function refresh(newState) { state = newState; render(); }

  logForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = logInput.value.trim();
    if (!text) return;
    logFeedback.textContent = "Saving…";
    milestoneMsg.textContent = "";
    try {
      const result = await api.log(text);
      if (result.state) refresh({ goals: state.goals, state: result.state });
      logFeedback.textContent = result.message || "";
      milestoneMsg.textContent = result.milestone || "";
      logInput.value = "";
    } catch (err) {
      logFeedback.textContent = "Could not save.";
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    if (state) render();
    else api.getState().then(refresh).catch(console.error);
  });
})();
