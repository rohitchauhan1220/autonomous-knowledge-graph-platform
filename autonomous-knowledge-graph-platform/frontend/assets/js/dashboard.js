function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function toDisplayDate(value) {
  if (!value) return "Unknown";
  return new Date(value).toLocaleString();
}

function openActivityDetail(title, bodyHtml, showGraphButton = true) {
  const modal = document.getElementById("activityDetailModal");
  const modalTitle = document.getElementById("activityDetailTitle");
  const modalBody = document.getElementById("activityDetailBody");
  const graphButton = document.getElementById("openGraphFromActivity");
  if (!modal || !modalTitle || !modalBody) return;
  modalTitle.textContent = title;
  modalBody.innerHTML = bodyHtml;
  if (graphButton) {
    graphButton.style.display = showGraphButton ? "" : "none";
  }
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

function buildInsightDetail(item) {
  const normalized = String(item || "").toLowerCase();
  let explanation = "This executive insight highlights a current operational signal in the graph.";
  let nextSteps = [
    "Open the Graph view to inspect connected entities.",
    "Review recent documents and queries tied to this topic.",
    "Use the activity feed to jump into the relevant source record."
  ];

  if (normalized.includes("supplier")) {
    explanation = "This insight points to supplier dependency risk and the strongest upstream impact paths.";
    nextSteps = [
      "Open the Graph view to trace supplier nodes and dependency edges.",
      "Review delayed delivery documents and related query history.",
      "Prioritize the supplier cluster with the highest connectivity."
    ];
  } else if (normalized.includes("incident")) {
    explanation = "This insight points to open incident pressure and the entities most likely to absorb impact.";
    nextSteps = [
      "Open the Graph view to inspect incident-linked entities.",
      "Check the latest activity items for matching incident evidence.",
      "Track whether the incident connects to any renewal or SLA commitments."
    ];
  } else if (normalized.includes("refresh") || normalized.includes("report")) {
    explanation = "This insight points to operational cadence and executive reporting discipline.";
    nextSteps = [
      "Open the Graph view to verify the latest graph version.",
      "Review recent ingestion activity before exporting reports.",
      "Schedule a weekly refresh if the data source changes frequently."
    ];
  }

  return `
    <div class="detail-grid">
      <div>
        <h3>Insight</h3>
        <p>${escapeHtml(item)}</p>
      </div>
      <div>
        <h3>Why it matters</h3>
        <p>${escapeHtml(explanation)}</p>
      </div>
      <div>
        <h3>Next steps</h3>
        <ul>${nextSteps.map(step => `<li>${escapeHtml(step)}</li>`).join("")}</ul>
      </div>
      <div>
        <h3>Graph action</h3>
        <p>Use the Open Graph button above to move directly into the node and edge view.</p>
      </div>
    </div>
  `;
}

function openMetricDetail(title, bodyHtml) {
  const modal = document.getElementById("metricDetailModal");
  const modalTitle = document.getElementById("metricDetailTitle");
  const modalBody = document.getElementById("metricDetailBody");
  if (!modal || !modalTitle || !modalBody) return;
  modalTitle.textContent = title;
  modalBody.innerHTML = bodyHtml;
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

function closeMetricDetail() {
  const modal = document.getElementById("metricDetailModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function closeActivityDetail() {
  const modal = document.getElementById("activityDetailModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function openGraphFromActivity() {
  window.location.href = "graph.html";
}

function parseActivityPayload(card) {
  return JSON.parse(card.getAttribute("data-activity") || "{}");
}

function getActivityCard(card) {
  const activityType = card.getAttribute("data-activity-type");
  const payload = parseActivityPayload(card);
  return { activityType, payload };
}

async function deleteActivityRecord(activityType, payload) {
  try {
    if (!payload || !payload.id) {
      throw new Error(`Invalid ${activityType}: missing ID`);
    }
    const endpoint = activityType === "document"
      ? `/api/dashboard/activity/documents/${payload.id}`
      : `/api/dashboard/activity/queries/${payload.id}`;
    console.log(`[Delete] Calling ${endpoint}`);
    await API.delete(endpoint);
    console.log(`[Delete] Success: ${endpoint}`);
    await loadMetrics();
    await loadActivity();
  } catch (error) {
    console.error(`[Delete] Error:`, error);
    throw error;
  }
}

async function editActivityRecord(activityType, payload) {
}

// Global state to track the current edit item
let currentEditItem = { type: null, payload: null };

function openEditModal(title, type, payload, field1Label, field1Value, field2Label, field2Value) {
  currentEditItem = { type, payload };
  const modal = document.getElementById("editActivityModal");
  const titleElem = document.getElementById("editActivityTitle");
  const form = document.getElementById("editActivityForm");
  const label1 = form.querySelector("label[for='editFieldOne']");
  const label2 = form.querySelector("label[for='editFieldTwo']");
  const field1 = document.getElementById("editFieldOne");
  const field2 = document.getElementById("editFieldTwo");
  
  if (!modal || !titleElem) return;
  
  titleElem.textContent = title;
  label1.textContent = field1Label;
  field1.placeholder = field1Label;
  field1.value = field1Value || "";
  label2.textContent = field2Label;
  field2.placeholder = field2Label;
  field2.value = field2Value || "";
  
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
  field1.focus();
}

function closeEditModal() {
  const modal = document.getElementById("editActivityModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
  currentEditItem = { type: null, payload: null };
}

async function submitEditForm() {
  if (!currentEditItem.type || !currentEditItem.payload) {
    console.warn("[Edit Form] No current edit item");
    return;
  }
  
  const field1 = document.getElementById("editFieldOne").value || "";
  const field2 = document.getElementById("editFieldTwo").value || "";
  
  try {
    if (currentEditItem.type === "document") {
      const endpoint = `/api/dashboard/activity/documents/${currentEditItem.payload.id}`;
      console.log(`[Edit Form] Submitting document edit: ${endpoint}`);
      await API.patch(endpoint, { filename: field1, summary: field2 });
      console.log(`[Edit Form] Success`);
    } else if (currentEditItem.type === "query") {
      const endpoint = `/api/dashboard/activity/queries/${currentEditItem.payload.id}`;
      console.log(`[Edit Form] Submitting query edit: ${endpoint}`);
      await API.patch(endpoint, { question: field1, answer: field2 });
      console.log(`[Edit Form] Success`);
    }
    closeEditModal();
    await loadActivity();
    window.alert(`${currentEditItem.type} updated successfully.`);
  } catch (error) {
    console.error(`[Edit Form] Error:`, error);
    window.alert(`Failed to update ${currentEditItem.type}: ${error.message}`);
  }
}

function summarizeDocument(document) {
  const metadata = document.metadata || {};
  const keywords = Array.isArray(document.keywords) ? document.keywords.slice(0, 4) : [];
  const rawSummary = document.summary ? document.summary.replace(/\s+/g, " ").trim() : "";
  const looksStructured = rawSummary.startsWith("{") || rawSummary.startsWith("[");
  const summary = looksStructured
    ? "Structured dataset ingested. Open the source file for row-level details."
    : rawSummary || "Processed document";
  const preview = summary.length > 220 ? `${summary.slice(0, 217)}...` : summary;
  const metadataBits = [metadata.source_type, metadata.filename, metadata.size_bytes ? `${metadata.size_bytes} bytes` : null]
    .filter(Boolean)
    .join(" • ");
  return `
    <article class="activity-card" data-activity-type="document" data-activity='${escapeHtml(JSON.stringify(document))}'>
      <button type="button" class="activity-item activity-button activity-main" data-activity-action="open">
        <strong>${escapeHtml(document.filename)}</strong>
        <p>${escapeHtml(metadataBits)}</p>
        <p>${escapeHtml(preview)}</p>
        ${keywords.length ? `<div class="tag-row">${keywords.map(item => `<span class="tag">${escapeHtml(item)}</span>`).join("")}</div>` : ""}
      </button>
      <div class="row-actions">
        <button type="button" class="secondary small" data-activity-action="edit">Edit</button>
        <button type="button" class="danger small" data-activity-action="delete">Delete</button>
      </div>
    </article>
  `;
}

function summarizeQuery(query) {
  const answer = query.answer ? query.answer.replace(/\s+/g, " ").trim() : "";
  const preview = answer.length > 220 ? `${answer.slice(0, 217)}...` : answer || "Answered query";
  return `
    <article class="activity-card" data-activity-type="query" data-activity='${escapeHtml(JSON.stringify(query))}'>
      <button type="button" class="activity-item activity-button activity-main" data-activity-action="open">
        <strong>${escapeHtml(query.question)}</strong>
        <p>${escapeHtml(preview)}</p>
        <p>${escapeHtml(toDisplayDate(query.created_at))}</p>
      </button>
      <div class="row-actions">
        <button type="button" class="secondary small" data-activity-action="edit">Edit</button>
        <button type="button" class="danger small" data-activity-action="delete">Delete</button>
      </div>
    </article>
  `;
}

function renderSourceList(sources) {
  if (!Array.isArray(sources) || !sources.length) return "<p class='muted'>No sources captured.</p>";
  return `<div class="source-stack">${sources.map(source => `
    <div class="source-item">
      <strong>${escapeHtml(source.document || source.name || "Source")}</strong>
      <p>${escapeHtml(source.snippet || source.excerpt || source.evidence || source.text || "Matched evidence from the graph.")}</p>
      <div class="source-meta">
        ${source.id ? `<span>ID ${escapeHtml(source.id)}</span>` : ""}
        ${source.confidence !== undefined ? `<span>Confidence ${escapeHtml(source.confidence)}</span>` : ""}
      </div>
    </div>
  `).join("")}</div>`;
}

async function loadMetrics() {
  const metrics = await API.get("/api/dashboard/metrics");
  const labels = {
    documents: "Documents",
    entities: "Entities",
    relations: "Relations",
    queries: "Queries",
    risk_score: "Risk Score",
    automation_rate: "Automation Rate"
  };
  document.getElementById("metricGrid").innerHTML = Object.entries(labels).map(([key, label]) => `
    <button type="button" class="metric-card metric-button" data-metric="${key}">
      <strong>${metrics[key]}</strong><span>${label}</span>
    </button>
  `).join("");
}

async function loadMetricDetails(metricKey) {
  const [activity, graph, queryHistory] = await Promise.all([
    API.get("/api/dashboard/activity"),
    API.get("/api/graph/snapshot"),
    API.get("/api/query/history")
  ]);

  if (metricKey === "documents") {
    const documents = activity.documents.slice(0, 5);
    return `
      <div class="detail-grid">
        <div><h3>What this shows</h3><p>Recently ingested documents available in the platform.</p></div>
        <div><h3>Recent documents</h3>${documents.length ? `<div class="source-stack">${documents.map(doc => `<div class="source-item"><strong>${escapeHtml(doc.filename)}</strong><p>${escapeHtml(doc.summary || "No summary available.")}</p></div>`).join("")}</div>` : "<p class='muted'>No documents yet.</p>"}</div>
      </div>
    `;
  }

  if (metricKey === "entities") {
    const entities = graph.nodes.slice(0, 8);
    return `
      <div class="detail-grid">
        <div><h3>What this shows</h3><p>Entities currently present in the graph snapshot.</p></div>
        <div><h3>Sample entities</h3>${entities.length ? `<div class="tag-row">${entities.map(entity => `<span class="tag">${escapeHtml(entity.data.label)}</span>`).join("")}</div>` : "<p class='muted'>No entities yet.</p>"}</div>
      </div>
    `;
  }

  if (metricKey === "relations") {
    const relations = graph.edges.slice(0, 8);
    return `
      <div class="detail-grid">
        <div><h3>What this shows</h3><p>Relationships connecting entities in the current snapshot.</p></div>
        <div><h3>Sample relations</h3>${relations.length ? `<div class="source-stack">${relations.map(edge => `<div class="source-item"><strong>${escapeHtml(edge.data.label || "Relation")}</strong><p>${escapeHtml(edge.data.source)} → ${escapeHtml(edge.data.target)}</p></div>`).join("")}</div>` : "<p class='muted'>No relations yet.</p>"}</div>
      </div>
    `;
  }

  if (metricKey === "queries") {
    const queries = queryHistory.history.slice(0, 5);
    return `
      <div class="detail-grid">
        <div><h3>What this shows</h3><p>Recent user questions and graph-backed answers.</p></div>
        <div><h3>Recent queries</h3>${queries.length ? `<div class="source-stack">${queries.map(query => `<div class="source-item"><strong>${escapeHtml(query.question)}</strong><p>${escapeHtml(query.answer || "")}</p></div>`).join("")}</div>` : "<p class='muted'>No queries yet.</p>"}</div>
      </div>
    `;
  }

  if (metricKey === "risk_score") {
    return `
      <div class="detail-grid">
        <div><h3>Interpretation</h3><p>This is an internal demo score summarizing dependency and incident pressure across the graph.</p></div>
        <div><h3>Action</h3><p>Open the Graph and Query pages to inspect the risk-bearing entities and connected evidence.</p></div>
      </div>
    `;
  }

  return `
    <div class="detail-grid">
      <div><h3>Interpretation</h3><p>Automation rate represents how much of the current pipeline is handled by deterministic or AI-assisted processing.</p></div>
      <div><h3>Action</h3><p>Use ingestion, query, and graph exploration to validate and improve the automated flow.</p></div>
    </div>
  `;
}

async function loadActivity() {
  try {
    const data = await API.get("/api/dashboard/activity");
    console.log("[Activity] Loaded", { docs: data.documents?.length, queries: data.queries?.length });
    
    const documents = Array.isArray(data.documents) ? data.documents : [];
    const queries = Array.isArray(data.queries) ? data.queries : [];
    
    const items = [
      ...documents.map(item => ({ type: "document", ...item })),
      ...queries.map(item => ({ type: "query", ...item }))
    ];
    
    const list = document.getElementById("activityList");
    if (!list) {
      console.warn("[Activity] activityList element not found");
      return;
    }
    
    list.innerHTML = items.map(item => item.type === "document" ? summarizeDocument(item) : summarizeQuery(item)).join("") || "<p class='muted'>No activity yet.</p>";
    console.log(`[Activity] Rendered ${items.length} items`);
  } catch (error) {
    console.error("[Activity] Load error:", error);
    const list = document.getElementById("activityList");
    if (list) {
      list.innerHTML = `<p class='muted'>Error loading activity: ${escapeHtml(error.message)}</p>`;
    }
  }
}

function buildHeatmapDetail(item) {
  return `
    <div class="detail-grid">
      <div><h3>Area</h3><p>${escapeHtml(item.area)}</p></div>
      <div><h3>Risk Score</h3><p>${escapeHtml(item.risk)}%</p></div>
      <div><h3>What to do</h3><p>Review the linked documents, suppliers, or incidents in the graph for this hotspot.</p></div>
      <div><h3>Action</h3><p>Open the Graph page to inspect connected nodes and the exact dependency path.</p></div>
    </div>
  `;
}

function buildHealthDetail(key, value) {
  const label = key.replaceAll("_", " ");
  return `
    <div class="detail-grid">
      <div><h3>Signal</h3><p>${escapeHtml(label)}</p></div>
      <div><h3>Value</h3><p>${escapeHtml(value)}</p></div>
      <div><h3>Meaning</h3><p>This is a live system health indicator used by the executive dashboard.</p></div>
      <div><h3>Action</h3><p>Open the Graph or Recent Activity sections to trace the data behind this signal.</p></div>
    </div>
  `;
}

async function loadExecutivePanels() {
  const [summary, heatmap, health] = await Promise.all([
    API.get("/api/dashboard/executive-summary"),
    API.get("/api/dashboard/heatmap"),
    API.get("/api/dashboard/health")
  ]);
  document.getElementById("executiveHeadline").textContent = summary.headline;
  document.getElementById("recommendations").innerHTML = summary.recommendations.map(item => `
    <button type="button" class="activity-item activity-button insight-button" data-insight="${escapeHtml(item)}">${escapeHtml(item)}</button>
  `).join("");
  document.getElementById("riskHeatmap").innerHTML = heatmap.heatmap.map(item => `
    <button type="button" class="heat-cell clickable-panel" data-heat-item='${escapeHtml(JSON.stringify(item))}'>
      <span>${escapeHtml(item.area)}</span>
      <div class="heat-bar" style="width:${item.risk}%"></div>
    </button>
  `).join("");
  document.getElementById("healthPanel").innerHTML = Object.entries(health).slice(0, 6).map(([key, value]) => `
    <button type="button" class="activity-item activity-button clickable-panel health-button" data-health-key="${escapeHtml(key)}" data-health-value="${escapeHtml(String(value))}">
      <strong>${escapeHtml(key.replaceAll("_", " "))}</strong><p>${escapeHtml(value)}</p>
    </button>
  `).join("");
}

document.getElementById("uploadForm")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const status = document.getElementById("uploadStatus");
  status.textContent = "Processing document and updating graph...";
  try {
    const result = await API.upload(new FormData(event.target));
    status.innerHTML = `<strong>Upload complete</strong> ${escapeHtml(result.document.filename)} created ${result.entities_created} entities.`;
    await loadMetrics();
    await loadActivity();
  } catch (error) {
    if (error.status === 409 && error.data?.document) {
      status.innerHTML = `
        <strong>Duplicate document detected</strong>
        <div class="activity-item">
          <p><strong>${escapeHtml(error.data.document.filename)}</strong></p>
          <p>Already exists in the graph. Use a renamed file or updated source.</p>
        </div>
      `;
      return;
    }
    status.textContent = error.message;
  }
});

document.getElementById("activityList")?.addEventListener("click", async event => {
  const actionButton = event.target.closest("button[data-activity-action]");
  const activityCard = event.target.closest("article[data-activity-type]");
  
  if (!activityCard) {
    console.warn("[Activity Click] No activity card found");
    return;
  }
  
  const { activityType, payload } = getActivityCard(activityCard);
  const action = actionButton?.getAttribute("data-activity-action") || "open";
  
  console.log(`[Activity Click] Action=${action}, Type=${activityType}, ID=${payload?.id}`);

  if (action === "delete") {
    console.log(`[Delete] Requesting confirmation for ${activityType}`);
    if (!window.confirm(`Delete this ${activityType} item? This cannot be undone.`)) {
      console.log(`[Delete] User cancelled`);
      return;
    }
    try {
      await deleteActivityRecord(activityType, payload);
      window.alert(`${activityType} deleted successfully.`);
    } catch (error) {
      console.error(`[Delete] Caught error:`, error);
      window.alert(`Failed to delete ${activityType}: ${error.message}`);
    }
    return;
  }

  if (action === "edit") {
    console.log(`[Edit] Starting edit for ${activityType}`);
    console.log(`[Edit] Starting modal edit for ${activityType}`);
    if (activityType === "document") {
      openEditModal(
        `Edit Document: ${payload.filename || "Document"}`,
        activityType,
        payload,
        "Filename",
        payload.filename || "",
        "Summary",
        payload.summary || ""
      );
    } else if (activityType === "query") {
      openEditModal(
        `Edit Query: ${payload.question?.slice(0, 50) || "Query"}`,
        activityType,
        payload,
        "Question",
        payload.question || "",
        "Answer",
        payload.answer || ""
      );
    }
    return;
  }

  if (activityType === "document") {
    const metadata = payload.metadata || {};
    const keywords = Array.isArray(payload.keywords) ? payload.keywords : [];
    const summaryText = payload.summary || "";
    const isStructuredDataset = payload.source_type === "csv" || summaryText.startsWith("[") || summaryText.startsWith("{");
    const metadataRows = Object.entries(metadata).map(([key, value]) => `<li><strong>${escapeHtml(key)}</strong>: ${escapeHtml(Array.isArray(value) ? value.join(", ") : value)}</li>`).join("");
    openActivityDetail(payload.filename || "Document detail", `
      <div class="detail-grid">
        <div>
          <h3>Summary</h3>
          <p>${escapeHtml(isStructuredDataset ? "Structured dataset ingested. Open the source file for row-level analysis and graphing." : (summaryText || "No summary available."))}</p>
        </div>
        <div>
          <h3>Classification</h3>
          <p>${escapeHtml(payload.classification || "Unclassified")}</p>
        </div>
        <div>
          <h3>Metadata</h3>
          <ul>${metadataRows || "<li>No metadata available.</li>"}</ul>
        </div>
        <div>
          <h3>Keywords</h3>
          <div class="tag-row">${keywords.length ? keywords.map(item => `<span class="tag">${escapeHtml(item)}</span>`).join("") : "<span class='muted'>No keywords</span>"}</div>
        </div>
      </div>
    `);
  }

  if (activityType === "query") {
    openActivityDetail(payload.question || "Query detail", `
      <div class="detail-grid">
        <div>
          <h3>Question</h3>
          <p>${escapeHtml(payload.question || "")}</p>
        </div>
        <div>
          <h3>Answer</h3>
          <p>${escapeHtml(payload.answer || "")}</p>
        </div>
        <div>
          <h3>Created At</h3>
          <p>${escapeHtml(toDisplayDate(payload.created_at))}</p>
        </div>
        <div>
          <h3>Sources</h3>
          ${renderSourceList(payload.sources)}
        </div>
      </div>
    `);
  }
});

document.getElementById("recommendations")?.addEventListener("click", event => {
  const button = event.target.closest("button[data-insight]");
  if (!button) return;
  const insight = button.getAttribute("data-insight") || "Executive insight";
  openActivityDetail("Executive AI Insight", buildInsightDetail(insight));
});

document.getElementById("riskHeatmap")?.addEventListener("click", event => {
  const button = event.target.closest("button[data-heat-item]");
  if (!button) return;
  const item = JSON.parse(button.getAttribute("data-heat-item") || "{}");
  openActivityDetail(`Risk Heatmap: ${item.area || "Item"}`, buildHeatmapDetail(item), false);
});

document.getElementById("healthPanel")?.addEventListener("click", event => {
  const button = event.target.closest("button[data-health-key]");
  if (!button) return;
  const key = button.getAttribute("data-health-key") || "signal";
  const value = button.getAttribute("data-health-value") || "";
  openActivityDetail(`System Health: ${key.replaceAll("_", " ")}`, buildHealthDetail(key, value), false);
});

document.getElementById("metricGrid")?.addEventListener("click", async event => {
  const button = event.target.closest("button[data-metric]");
  if (!button) return;
  const metricKey = button.getAttribute("data-metric");
  const metricLabel = button.querySelector("span")?.textContent || metricKey;
  openMetricDetail(metricLabel, "<p class='muted'>Loading metric details...</p>");
  try {
    const bodyHtml = await loadMetricDetails(metricKey);
    openMetricDetail(metricLabel, bodyHtml);
  } catch (error) {
    openMetricDetail(metricLabel, `<p class='muted'>${escapeHtml(error.message)}</p>`);
  }
});

document.getElementById("closeActivityDetail")?.addEventListener("click", closeActivityDetail);
document.getElementById("openGraphFromActivity")?.addEventListener("click", openGraphFromActivity);
document.getElementById("closeEditModal")?.addEventListener("click", closeEditModal);
document.getElementById("cancelEditModal")?.addEventListener("click", closeEditModal);
document.getElementById("editActivityForm")?.addEventListener("submit", async event => {
  event.preventDefault();
  await submitEditForm();
});
document.getElementById("editActivityModal")?.addEventListener("click", event => {
  if (event.target.id === "editActivityModal") closeEditModal();
});
document.getElementById("activityDetailModal")?.addEventListener("click", event => {
  if (event.target.id === "activityDetailModal") closeActivityDetail();
});
document.getElementById("closeMetricDetail")?.addEventListener("click", closeMetricDetail);
document.getElementById("metricDetailModal")?.addEventListener("click", event => {
  if (event.target.id === "metricDetailModal") closeMetricDetail();
});

console.log("[Dashboard] Initializing...");
Promise.all([
  loadMetrics().catch(e => { console.error("[Metrics] Error:", e); }),
  loadActivity().catch(e => { console.error("[Activity] Error:", e); }),
  loadExecutivePanels().catch(e => { console.error("[Panels] Error:", e); })
]).then(() => console.log("[Dashboard] All loaded"));

console.log("[Dashboard] Event listeners attached", {
  activityList: !!document.getElementById("activityList"),
  activityDetailModal: !!document.getElementById("activityDetailModal")
});
