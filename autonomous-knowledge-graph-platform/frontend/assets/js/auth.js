document.getElementById("loginForm")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  try {
    const data = await API.login(form.get("email"), form.get("password"));
    localStorage.setItem("akg_token", data.access_token);
    localStorage.setItem("akg_user", JSON.stringify(data.user));
    window.location.href = "dashboard.html";
  } catch (error) {
    alert(error.message);
  }
});
