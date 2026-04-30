document.getElementById("askForm")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const answerBox = document.getElementById("answerBox");
  const sourceList = document.getElementById("sourceList");
  answerBox.textContent = "Reasoning across graph evidence...";
  sourceList.innerHTML = "";
  try {
    const data = await API.post("/api/query/ask", { question: form.get("question") });
    answerBox.textContent = data.answer;
    sourceList.innerHTML = data.sources.map(source => `
      <div class="source-item"><strong>${source.document}</strong><span> Source ID ${source.id}</span></div>
    `).join("");
    await loadHistory();
  } catch (error) {
    answerBox.textContent = error.message;
  }
});

async function loadSuggestions() {
  const data = await API.get("/api/query/suggestions");
  document.getElementById("suggestions").innerHTML = data.suggestions.map(text => `
    <button type="button" data-question="${text}">${text}</button>
  `).join("");
  document.querySelectorAll("[data-question]").forEach(button => {
    button.addEventListener("click", () => {
      document.querySelector("#askForm input[name='question']").value = button.dataset.question;
    });
  });
}

async function loadHistory() {
  const data = await API.get("/api/query/history");
  document.getElementById("queryHistory").innerHTML = data.history.map(item => `
    <div class="activity-item"><strong>${item.question}</strong><p>${item.answer}</p></div>
  `).join("") || "<p class='muted'>No query history yet.</p>";
}

loadSuggestions().catch(console.error);
loadHistory().catch(console.error);
