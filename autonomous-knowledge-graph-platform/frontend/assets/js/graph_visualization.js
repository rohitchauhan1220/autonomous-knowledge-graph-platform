let cy;
let currentLayout = "tree";

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function normalizeClassName(value) {
  return String(value || "entity").toLowerCase().replace(/[^a-z0-9]+/g, "-");
}

function getRoots(nodes, edges) {
  const incoming = new Set(edges.map(edge => edge.data.target));
  const roots = nodes.filter(node => !incoming.has(node.data.id)).map(node => `#${node.data.id}`);
  return roots.length ? roots : nodes.slice(0, 1).map(node => `#${node.data.id}`);
}

function truncateLabel(value, maxLength = 16) {
  const text = String(value || "");
  return text.length > maxLength ? `${text.slice(0, maxLength - 1)}…` : text;
}

function renderTreeSummary(nodes, edges) {
  const nodeMap = new Map(nodes.map(node => [node.data.id, node]));
  const childrenMap = new Map();
  edges.forEach(edge => {
    if (!childrenMap.has(edge.data.source)) childrenMap.set(edge.data.source, []);
    childrenMap.get(edge.data.source).push(edge.data.target);
  });

  const roots = getRoots(nodes, edges).map(rootSelector => rootSelector.slice(1));
  const visited = new Set();

  function renderNode(nodeId, depth = 0) {
    const node = nodeMap.get(nodeId);
    if (!node) return "";
    const summaryLabel = node.data.order ? `${node.data.order}. ${node.data.label || node.data.id}` : (node.data.label || node.data.id);
    const label = escapeHtml(summaryLabel);
    const type = escapeHtml(node.data.type || "entity");
    const children = childrenMap.get(nodeId) || [];
    const alreadyVisited = visited.has(nodeId);
    if (alreadyVisited) {
      return `<li class="tree-entry tree-entry-cycle"><span>${label}</span><small>cycle</small></li>`;
    }
    visited.add(nodeId);
    return `
      <li class="tree-entry" data-depth="${depth}">
        <div class="tree-entry-head">
          <strong>${label}</strong>
          <span>${type}</span>
        </div>
        ${children.length ? `<ul>${children.map(childId => renderNode(childId, depth + 1)).join("")}</ul>` : ""}
      </li>
    `;
  }

  const markup = roots.map(rootId => renderNode(rootId)).join("");
  document.getElementById("treeSummary").innerHTML = markup ? `<ul class="tree-list">${markup}</ul>` : "<p class='muted'>No tree data available.</p>";
}

async function renderGraph(layoutName = currentLayout) {
  currentLayout = layoutName;
  const data = await API.get("/api/graph/snapshot");
  document.getElementById("graphStats").textContent = `${data.nodes.length} nodes, ${data.edges.length} relationships, version ${data.version}`;
  const numberedNodes = data.nodes.map((node, index) => ({
    ...node,
    data: {
      ...node.data,
      order: index + 1,
      displayLabel: `${index + 1}. ${truncateLabel(node.data.label)}`
    }
  }));
  cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [
      ...numberedNodes.map(node => ({ ...node, classes: normalizeClassName(node.data.type) })),
      ...data.edges
    ],
    style: [
      { selector: "node", style: {
        "background-color": "#116466",
        "label": "data(displayLabel)",
        "color": "#ffffff",
        "font-size": 16,
        "font-weight": "800",
        "text-wrap": "none",
        "width": 56,
        "height": 56,
        "shape": "ellipse",
        "text-valign": "center",
        "text-halign": "center",
        "border-width": 2,
        "border-color": "#ffffff",
        "text-background-color": "#116466",
        "text-background-opacity": 1,
        "text-background-padding": 2,
        "min-zoomed-font-size": 16,
        "text-outline-width": 1,
        "text-outline-color": "#0b4f50"
      }},
      { selector: ".entity", style: { "background-color": "#116466" } },
      { selector: ".supplier", style: { "background-color": "#0b4f50" } },
      { selector: ".document", style: { "background-color": "#c84b31" } },
      { selector: ".incident", style: { "background-color": "#d19a2a" } },
      { selector: ".risk", style: { "background-color": "#258a58" } },
      { selector: "edge", style: {
        "width": 2,
        "line-color": "#9aa7b6",
        "target-arrow-color": "#9aa7b6",
        "target-arrow-shape": "triangle",
        "curve-style": "bezier",
        "label": "",
        "font-size": 8,
        "text-background-opacity": 0,
        "text-background-padding": 0
      }},
      { selector: ".faded", style: { "opacity": 0.14 } }
    ],
    layout: layoutName === "tree"
      ? { name: "breadthfirst", directed: true, orientation: "vertical", fit: true, padding: 180, spacingFactor: 2.8, avoidOverlap: true, roots: getRoots(data.nodes, data.edges), nodeDimensionsIncludeLabels: true }
      : { name: "cose", animate: true, fit: true, padding: 60, avoidOverlap: true }
  });

  cy.on("tap", "node", event => {
    cy.edges().removeClass("highlighted-edge");
    event.target.connectedEdges().addClass("highlighted-edge");
  });

  cy.fit();

  renderTreeSummary(numberedNodes, data.edges);
}

async function loadVersions() {
  const data = await API.get("/api/graph/versions");
  document.getElementById("versionTimeline").innerHTML = data.versions.map((item, index) => `
    <div class="version-node">
      <div class="version-marker">${data.versions.length - index}</div>
      <div class="version-card">
        <div class="version-headline">
          <strong>Version ${item.version}</strong>
          <span>${new Date(item.created_at).toLocaleString()}</span>
        </div>
        <p>${escapeHtml(item.summary || "No summary available.")}</p>
        <div class="version-meta">
          <span>${escapeHtml(item.change_type || "update")}</span>
          ${item.document_id ? `<span>Doc ${escapeHtml(item.document_id)}</span>` : ""}
        </div>
      </div>
    </div>
  `).join("") || "<p class='muted'>No graph versions yet.</p>";
}

document.getElementById("refreshGraph")?.addEventListener("click", renderGraph);
document.getElementById("treeLayoutBtn")?.addEventListener("click", () => renderGraph("tree"));
document.getElementById("forceLayoutBtn")?.addEventListener("click", () => renderGraph("force"));
document.getElementById("graphFilter")?.addEventListener("input", (event) => {
  const value = event.target.value.toLowerCase();
  if (!cy) return;
  cy.elements().removeClass("faded");
  if (!value) return;
  cy.nodes().forEach(node => {
    if (!node.data("label").toLowerCase().includes(value)) node.addClass("faded");
  });
});

renderGraph("tree").catch(console.error);
loadVersions().catch(console.error);
