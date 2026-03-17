(() => {
  const api = {
    async getState() {
      const res = await fetch("/api/state");
      if (!res.ok) throw new Error("Failed to fetch state");
      return res.json();
    },
    async spin() {
      const res = await fetch("/api/spin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      if (!res.ok) throw new Error("Failed to spin");
      return res.json();
    },
    async taskOperation(operation, task, command) {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ operation, task, command }),
      });
      if (!res.ok) throw new Error("Task operation failed");
      return res.json();
    },
    async complete(task, response) {
      const res = await fetch("/api/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task, response }),
      });
      if (!res.ok) throw new Error("Completion failed");
      return res.json();
    },
  };

  const wheelEl = document.getElementById("wheel");
  const spinBtn = document.getElementById("spin-btn");
  const spinStatusEl = document.getElementById("spin-status");
  const currentTaskEl = document.getElementById("current-task");
  const completionFeedbackEl = document.getElementById("completion-feedback");
  const btnDone = document.getElementById("btn-done");
  const btnSkip = document.getElementById("btn-skip");
  const tasksListEl = document.getElementById("tasks-list");
  const tasksCountEl = document.getElementById("tasks-count");
  const statsSummaryEl = document.getElementById("stats-summary");
  const addTaskForm = document.getElementById("add-task-form");
  const newTaskInput = document.getElementById("new-task-input");

  let state = window.__INITIAL_GAME__ || null;
  let currentRotation = 0;
  let currentTaskName = null;
  let isSpinning = false;

  function getTasksArray() {
    return (state && state.state && state.state.tasks) || [];
  }

  function computeGradient(tasks) {
    if (!tasks.length) {
      return "conic-gradient(from 0deg, #0ea5e9, #22c55e, #f97316, #e11d48, #6366f1, #0ea5e9)";
    }
    const step = 360 / tasks.length;
    const palette = [
      "#38bdf8",
      "#a855f7",
      "#f97316",
      "#22c55e",
      "#e11d48",
      "#6366f1",
      "#facc15",
      "#14b8a6",
    ];
    const parts = tasks.map((t, i) => {
      const start = i * step;
      const end = (i + 1) * step;
      const color = palette[i % palette.length];
      return `${color} ${start}deg ${end}deg`;
    });
    return `conic-gradient(from -90deg, ${parts.join(",")})`;
  }

  function renderWheel() {
    const tasks = getTasksArray();
    wheelEl.style.backgroundImage = computeGradient(tasks);
  }

  function renderTasks() {
    const tasks = getTasksArray();
    tasksListEl.innerHTML = "";

    tasksCountEl.textContent = `${tasks.length} task${tasks.length === 1 ? "" : "s"}`;

    if (!tasks.length) {
      tasksListEl.innerHTML =
        '<div class="task-row"><div class="task-main"><div class="task-title">No tasks yet. Add one below!</div></div></div>';
      return;
    }

    tasks.forEach((t) => {
      const row = document.createElement("div");
      row.className = "task-row";

      const main = document.createElement("div");
      main.className = "task-main";
      const title = document.createElement("div");
      title.className = "task-title";
      title.textContent = t.name;
      main.appendChild(title);

      const meta = document.createElement("div");
      meta.className = "task-meta";

      if (t.picked_count) {
        const span = document.createElement("span");
        span.textContent = `🎯 picked ${t.picked_count}x`;
        meta.appendChild(span);
      }
      if (t.completed_count) {
        const span = document.createElement("span");
        span.textContent = `✅ done ${t.completed_count}x`;
        meta.appendChild(span);
      }
      if (t.skipped_count) {
        const span = document.createElement("span");
        span.textContent = `⏭ skipped ${t.skipped_count}x`;
        meta.appendChild(span);
      }

      if (t.favorite) {
        const chip = document.createElement("span");
        chip.className = "chip favorite";
        chip.textContent = "⭐ favorite";
        meta.appendChild(chip);
      }

      if (t.hated) {
        const chip = document.createElement("span");
        chip.className = "chip hated";
        chip.textContent = "💀 hated";
        meta.appendChild(chip);
      }

      if (meta.children.length) {
        main.appendChild(meta);
      }

      const actions = document.createElement("div");
      actions.className = "task-actions";

      const favBtn = document.createElement("button");
      favBtn.textContent = t.favorite ? "Unfavorite" : "Favorite";
      favBtn.addEventListener("click", async () => {
        const op = t.favorite ? "hate" : "favorite"; // toggling via bias for fun
        await runTaskOperation(op, t.name);
      });

      const hateBtn = document.createElement("button");
      hateBtn.textContent = t.hated ? "Unhate" : "Hate";
      hateBtn.addEventListener("click", async () => {
        const op = t.hated ? "favorite" : "hate";
        await runTaskOperation(op, t.name);
      });

      const rmBtn = document.createElement("button");
      rmBtn.textContent = "Remove";
      rmBtn.classList.add("danger");
      rmBtn.addEventListener("click", async () => {
        if (!confirm("Remove this task from the wheel?")) return;
        await runTaskOperation("remove", t.name);
      });

      actions.appendChild(favBtn);
      actions.appendChild(hateBtn);
      actions.appendChild(rmBtn);

      row.appendChild(main);
      row.appendChild(actions);
      tasksListEl.appendChild(row);
    });
  }

  function renderStats() {
    if (!state || !state.state) return;
    const totals = state.state.totals || { completed: 0, skipped: 0 };

    statsSummaryEl.innerHTML = "";

    const completed = document.createElement("div");
    completed.className = "stat";
    completed.innerHTML =
      '<div class="stat-label">Completed</div><div class="stat-value">' +
      totals.completed +
      "</div>";

    const skipped = document.createElement("div");
    skipped.className = "stat";
    skipped.innerHTML =
      '<div class="stat-label">Skipped</div><div class="stat-value">' +
      totals.skipped +
      "</div>";

    statsSummaryEl.appendChild(completed);
    statsSummaryEl.appendChild(skipped);
  }

  function refreshFromState(newState) {
    state = newState;
    renderWheel();
    renderTasks();
    renderStats();

    const last = state.state.last_spin || {};
    if (last.task) {
      currentTaskName = last.task;
      currentTaskEl.textContent = `→ ${last.task}\n\nPicked ${last.count} time${
        last.count === 1 ? "" : "s"
      } so far.`;
      btnDone.disabled = false;
      btnSkip.disabled = false;
    }
  }

  async function runTaskOperation(operation, task, command) {
    spinStatusEl.textContent = "Updating tasks…";
    try {
      const result = await api.taskOperation(operation, task, command);
      if (result.message) {
        spinStatusEl.textContent = result.message;
      } else {
        spinStatusEl.textContent = "";
      }
      if (result.state) {
        refreshFromState({
          goals: state.goals,
          state: result.state,
        });
      }
    } catch (err) {
      console.error(err);
      spinStatusEl.textContent = "Something went wrong updating tasks.";
    }
  }

  function animateWheelToTask(taskName) {
    const tasks = getTasksArray();
    if (!tasks.length) return;

    const index = tasks.findIndex((t) => t.name === taskName);
    if (index === -1) {
      // Fallback: random rotation
      const extraTurns = 5 + Math.random() * 2;
      const delta = 360 * extraTurns;
      currentRotation += delta;
      wheelEl.style.transform = `rotate(${currentRotation}deg)`;
      return;
    }

    const step = 360 / tasks.length;
    const targetAngle = index * step + step / 2;
    const extraTurns = 6; // full dramatic spins
    const finalRotation = 360 * extraTurns + (360 - targetAngle);
    currentRotation += finalRotation;
    wheelEl.style.transform = `rotate(${currentRotation}deg)`;
  }

  async function handleSpin() {
    if (isSpinning) return;
    isSpinning = true;
    spinBtn.disabled = true;
    btnDone.disabled = true;
    btnSkip.disabled = true;
    completionFeedbackEl.textContent = "";
    spinStatusEl.textContent = "Spinning...";

    try {
      const result = await api.spin();
      if (result && result.state) {
        refreshFromState({
          goals: state.goals,
          state: result.state,
        });
      }
      currentTaskName = result.task;
      currentTaskEl.textContent = result.message;

      animateWheelToTask(result.task);

      setTimeout(() => {
        btnDone.disabled = false;
        btnSkip.disabled = false;
        spinStatusEl.textContent = "";
        isSpinning = false;
        spinBtn.disabled = false;
      }, 3300);
    } catch (err) {
      console.error(err);
      spinStatusEl.textContent = "Spin failed. Try again.";
      isSpinning = false;
      spinBtn.disabled = false;
    }
  }

  async function handleCompletion(response) {
    if (!currentTaskName) return;
    completionFeedbackEl.textContent = "Saving...";
    try {
      const result = await api.complete(currentTaskName, response);
      if (result && result.state) {
        refreshFromState({
          goals: state.goals,
          state: result.state,
        });
      }
      completionFeedbackEl.textContent = result.feedback || "";
    } catch (err) {
      console.error(err);
      completionFeedbackEl.textContent = "Could not save completion.";
    }
  }

  function init() {
    if (state) {
      refreshFromState(state);
    } else {
      api
        .getState()
        .then((s) => refreshFromState(s))
        .catch((err) => console.error(err));
    }

    renderWheel();

    spinBtn.addEventListener("click", handleSpin);

    btnDone.addEventListener("click", () => handleCompletion("yes"));
    btnSkip.addEventListener("click", () => handleCompletion("skip"));

    addTaskForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const value = newTaskInput.value.trim();
      if (!value) return;
      await runTaskOperation("add", value);
      newTaskInput.value = "";
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();

