const statusBox = document.getElementById("settingsStatus");

function showStatus(message) {
  if (statusBox) statusBox.textContent = message;
}

function renderActions(actions) {
  return `<div class="row-actions">${actions.join("")}</div>`;
}

function promptUserCreate() {
  const name = prompt("Full name");
  if (name === null) return null;
  const email = prompt("Email address");
  if (email === null) return null;
  const password = prompt("Temporary password");
  if (password === null) return null;
  const role = prompt("Role", "analyst");
  if (role === null) return null;
  const organization = prompt("Organization", "Demo Enterprise");
  if (organization === null) return null;
  const department = prompt("Department", "Enterprise Intelligence");
  if (department === null) return null;
  return { name, email, password, role, organization, department };
}

function promptUserEdit(user) {
  const name = prompt("Update name", user.name);
  if (name === null) return null;
  const role = prompt("Update role", user.role);
  if (role === null) return null;
  const organization = prompt("Update organization", user.organization);
  if (organization === null) return null;
  const department = prompt("Update department", user.department);
  if (department === null) return null;
  const tenantId = prompt("Update tenant id", user.tenant_id || "demo-tenant");
  if (tenantId === null) return null;
  return { name, role, organization, department, tenant_id: tenantId };
}

function promptIntegrationEdit(item) {
  const provider = prompt("Update provider", item.provider);
  if (provider === null) return null;
  const status = prompt("Update status", item.status);
  if (status === null) return null;
  const configText = prompt("Update config as JSON", JSON.stringify(item.config || {}, null, 2));
  if (configText === null) return null;
  return { provider, status, config: JSON.parse(configText) };
}

function promptScheduleEdit(job) {
  const name = prompt("Update job name", job.name);
  if (name === null) return null;
  const sourceType = prompt("Update source type", job.source_type);
  if (sourceType === null) return null;
  const cadence = prompt("Update cadence", job.cadence);
  if (cadence === null) return null;
  const active = prompt("Active? true or false", job.is_active ? "true" : "false");
  if (active === null) return null;
  return { name, source_type: sourceType, cadence, is_active: active.toLowerCase() === "true" };
}

function promptIntegrationCreate() {
  const provider = prompt("Provider name", "custom-api");
  if (provider === null) return null;
  const configText = prompt("Config as JSON", "{}");
  if (configText === null) return null;
  return { provider, config: JSON.parse(configText) };
}

function promptScheduleCreate() {
  const name = prompt("Job name", "Daily enterprise sync");
  if (name === null) return null;
  const sourceType = prompt("Source type", "api");
  if (sourceType === null) return null;
  const cadence = prompt("Cadence", "daily");
  if (cadence === null) return null;
  return { name, source_type: sourceType, cadence };
}

async function loadAdmin() {
  showStatus("Loading settings and governance data...");
  const users = await API.get("/api/admin/users");
  document.getElementById("usersList").innerHTML = users.users.map(user => `
    <div class="data-row">
      <div>
        <strong>${user.name}</strong>
        <p>${user.email} | ${user.role} | ${user.organization}</p>
      </div>
      ${renderActions([
        `<button class="secondary" data-action="edit-user" data-id="${user.id}">Edit</button>`,
        `<button class="danger" data-action="delete-user" data-id="${user.id}">Delete</button>`
      ])}
    </div>
  `).join("") || "<p class='muted'>No users found.</p>";

  const logs = await API.get("/api/admin/audit-logs");
  document.getElementById("auditList").innerHTML = logs.audit_logs.map(log => `
    <div class="audit-row"><strong>${log.action}</strong><p>${log.actor} - ${new Date(log.created_at).toLocaleString()}</p></div>
  `).join("") || "<p class='muted'>No audit events yet.</p>";

  const integrations = await API.get("/api/admin/integrations");
  document.getElementById("integrationList").innerHTML = integrations.integrations.map(item => `
    <div class="data-row">
      <div>
        <strong>${item.provider}</strong>
        <p>${item.status}</p>
      </div>
      ${renderActions([
        `<button class="secondary" data-action="edit-integration" data-id="${item.id}">Edit</button>`,
        `<button class="danger" data-action="delete-integration" data-id="${item.id}">Delete</button>`
      ])}
    </div>
  `).join("") || "<p class='muted'>No integrations configured.</p>";

  const schedules = await API.get("/api/admin/scheduled-ingestion");
  document.getElementById("scheduleList").innerHTML = schedules.jobs.map(item => `
    <div class="data-row">
      <div>
        <strong>${item.name}</strong>
        <p>${item.source_type} - ${item.cadence} - ${item.is_active ? "Active" : "Paused"}</p>
      </div>
      ${renderActions([
        `<button class="secondary" data-action="edit-schedule" data-id="${item.id}">Edit</button>`,
        `<button class="danger" data-action="delete-schedule" data-id="${item.id}">Delete</button>`
      ])}
    </div>
  `).join("") || "<p class='muted'>No scheduled jobs yet.</p>";

  showStatus("Settings loaded. Use Edit or Delete to manage demo records.");
}

document.addEventListener("click", async event => {
  const target = event.target.closest("button[data-action]");
  if (!target) return;
  const id = target.getAttribute("data-id");
  const action = target.getAttribute("data-action");

  try {
    if (action === "add-user") {
      const payload = promptUserCreate();
      if (!payload) return;
      await API.post("/api/auth/signup", payload);
      showStatus("User created.");
    }
    if (action === "add-integration") {
      const payload = promptIntegrationCreate();
      if (!payload) return;
      await API.post("/api/admin/integrations", payload);
      showStatus("Integration created.");
    }
    if (action === "add-schedule") {
      const payload = promptScheduleCreate();
      if (!payload) return;
      await API.post("/api/admin/scheduled-ingestion", payload);
      showStatus("Schedule created.");
    }
    if (action === "edit-user") {
      const user = (await API.get("/api/admin/users")).users.find(item => String(item.id) === id);
      const payload = promptUserEdit(user);
      if (!payload) return;
      await API.patch(`/api/admin/users/${id}`, payload);
      showStatus("User updated successfully.");
    }
    if (action === "delete-user") {
      if (!confirm("Delete this user?")) return;
      await API.delete(`/api/admin/users/${id}`);
      showStatus("User deleted.");
    }
    if (action === "edit-integration") {
      const item = (await API.get("/api/admin/integrations")).integrations.find(record => String(record.id) === id);
      const payload = promptIntegrationEdit(item);
      if (!payload) return;
      await API.patch(`/api/admin/integrations/${id}`, payload);
      showStatus("Integration updated.");
    }
    if (action === "delete-integration") {
      if (!confirm("Delete this integration?")) return;
      await API.delete(`/api/admin/integrations/${id}`);
      showStatus("Integration deleted.");
    }
    if (action === "edit-schedule") {
      const job = (await API.get("/api/admin/scheduled-ingestion")).jobs.find(record => String(record.id) === id);
      const payload = promptScheduleEdit(job);
      if (!payload) return;
      await API.patch(`/api/admin/scheduled-ingestion/${id}`, payload);
      showStatus("Schedule updated.");
    }
    if (action === "delete-schedule") {
      if (!confirm("Delete this scheduled job?")) return;
      await API.delete(`/api/admin/scheduled-ingestion/${id}`);
      showStatus("Scheduled job deleted.");
    }
    await loadAdmin();
  } catch (error) {
    showStatus(error.data?.error || error.message);
  }
});

loadAdmin().catch(error => {
  if (document.getElementById("auditList")) document.getElementById("auditList").textContent = error.message;
  showStatus(error.message);
});
