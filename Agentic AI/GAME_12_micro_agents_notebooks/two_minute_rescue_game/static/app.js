(() => {
  const api = {
    async getState() {
      const res = await fetch("/api/state");
      if (!res.ok) throw new Error("Failed to fetch state");
      return res.json();
    },
    async pick() {
      const res = await fetch("/api/pick", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      if (!res.ok) throw new Error("Failed to pick");
      return res.json();
    },
    async feedback(scriptName, helped) {
      const res = await fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script_name: scriptName, helped }),
      });
      if (!res.ok) throw new Error("Feedback failed");
      return res.json();
    },
  };

  const pickBtn = document.getElementById("pick-btn");
  const pickStatus = document.getElementById("pick-status");
  const scriptCard = document.getElementById("script-card");
  const scriptNameEl = document.getElementById("script-name");
  const scriptStepsEl = document.getElementById("script-steps");
  const btnYes = document.getElementById("btn-yes");
  const btnNo = document.getElementById("btn-no");
  const feedbackMsg = document.getElementById("feedback-msg");
  const scriptsListEl = document.getElementById("scripts-list");
  const statsSummaryEl = document.getElementById("stats-summary");

  let state = window.__INITIAL_GAME__ || null;
  let currentScriptName = null;

  function renderScripts() {
    if (!state || !state.state) return;
    const scripts = state.state.scripts || [];
    scriptsListEl.innerHTML = "";

    scripts.forEach((s) => {
      const row = document.createElement("div");
      row.className = "script-row";

      const header = document.createElement("div");
      header.className = "script-row-header";
      const name = document.createElement("span");
      name.textContent = s.name;
      const rate = document.createElement("span");
      rate.className = "script-rate";
      rate.textContent = s.total > 0 ? `${s.success_rate}% (${s.helped}/${s.total})` : "No data yet";
      header.appendChild(name);
      header.appendChild(rate);

      const barBg = document.createElement("div");
      barBg.className = "bar-bg";
      const barFill = document.createElement("div");
      barFill.className = "bar-fill";
      barFill.style.width = `${s.success_rate}%`;
      barBg.appendChild(barFill);

      row.appendChild(header);
      row.appendChild(barBg);
      scriptsListEl.appendChild(row);
    });
  }

  function renderStats() {
    if (!state || !state.state) return;
    const totals = state.state.totals || { helped: 0, total: 0 };

    statsSummaryEl.innerHTML = "";

    const helped = document.createElement("div");
    helped.className = "stat";
    helped.innerHTML =
      '<div class="stat-label">Times Helped</div><div class="stat-value">' +
      totals.helped + "</div>";

    const total = document.createElement("div");
    total.className = "stat";
    total.innerHTML =
      '<div class="stat-label">Total Rescues</div><div class="stat-value">' +
      totals.total + "</div>";

    const rate = document.createElement("div");
    rate.className = "stat";
    const pct = totals.total > 0 ? Math.round(totals.helped / totals.total * 100) : 0;
    rate.innerHTML =
      '<div class="stat-label">Success Rate</div><div class="stat-value">' +
      pct + "%</div>";

    statsSummaryEl.appendChild(helped);
    statsSummaryEl.appendChild(total);
    statsSummaryEl.appendChild(rate);
  }

  function refreshFromState(newState) {
    state = newState;
    renderScripts();
    renderStats();
  }

  async function handlePick() {
    pickBtn.disabled = true;
    btnYes.disabled = true;
    btnNo.disabled = true;
    feedbackMsg.textContent = "";
    pickStatus.textContent = "Finding the best script…";

    try {
      const result = await api.pick();
      if (result.state) {
        refreshFromState({ goals: state.goals, state: result.state });
      }

      const script = result.script;
      currentScriptName = script.name;
      scriptNameEl.textContent = `🛠️ ${script.name}`;
      scriptStepsEl.innerHTML = "";
      script.steps.forEach((step) => {
        const li = document.createElement("li");
        li.textContent = step;
        scriptStepsEl.appendChild(li);
      });

      scriptCard.classList.remove("hidden");
      // Re-trigger animation
      scriptCard.style.animation = "none";
      void scriptCard.offsetHeight;
      scriptCard.style.animation = "";

      pickStatus.textContent = "";
      btnYes.disabled = false;
      btnNo.disabled = false;
      pickBtn.disabled = false;
    } catch (err) {
      console.error(err);
      pickStatus.textContent = "Something went wrong. Try again.";
      pickBtn.disabled = false;
    }
  }

  async function handleFeedback(helped) {
    if (!currentScriptName) return;
    btnYes.disabled = true;
    btnNo.disabled = true;
    feedbackMsg.textContent = "Saving…";

    try {
      const result = await api.feedback(currentScriptName, helped);
      if (result.state) {
        refreshFromState({ goals: state.goals, state: result.state });
      }
      feedbackMsg.textContent = result.feedback || "";
    } catch (err) {
      console.error(err);
      feedbackMsg.textContent = "Could not save feedback.";
    }
  }

  function init() {
    if (state) {
      refreshFromState(state);
    } else {
      api.getState()
        .then((s) => refreshFromState(s))
        .catch((err) => console.error(err));
    }

    pickBtn.addEventListener("click", handlePick);
    btnYes.addEventListener("click", () => handleFeedback(true));
    btnNo.addEventListener("click", () => handleFeedback(false));
  }

  document.addEventListener("DOMContentLoaded", init);
})();
