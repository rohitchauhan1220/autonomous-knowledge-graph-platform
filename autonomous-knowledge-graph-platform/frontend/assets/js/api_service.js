const API = {
  token() {
    return localStorage.getItem("akg_token");
  },
  headers(json = true) {
    const headers = {};
    if (json) headers["Content-Type"] = "application/json";
    if (this.token()) headers.Authorization = `Bearer ${this.token()}`;
    return headers;
  },
  async request(path, options = {}) {
    const response = await fetch(path, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(data.error || "Request failed");
      error.status = response.status;
      error.data = data;
      throw error;
    }
    return data;
  },
  login(email, password) {
    return this.request("/api/auth/login", {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify({ email, password })
    });
  },
  get(path) {
    return this.request(path, { headers: this.headers(false) });
  },
  post(path, payload) {
    return this.request(path, { method: "POST", headers: this.headers(), body: JSON.stringify(payload) });
  },
  patch(path, payload) {
    return this.request(path, { method: "PATCH", headers: this.headers(), body: JSON.stringify(payload) });
  },
  delete(path) {
    return this.request(path, { method: "DELETE", headers: this.headers(false) });
  },
  upload(formData) {
    return this.request("/api/ingestion/upload", {
      method: "POST",
      headers: this.headers(false),
      body: formData
    });
  }
};
