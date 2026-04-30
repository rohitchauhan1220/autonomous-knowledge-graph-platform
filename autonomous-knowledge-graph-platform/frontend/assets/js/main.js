if (!localStorage.getItem("akg_token")) {
  window.location.href = "index.html";
}

if (localStorage.getItem("akg_theme") === "dark") {
  document.body.classList.add("dark");
}

document.getElementById("themeToggle")?.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  localStorage.setItem("akg_theme", document.body.classList.contains("dark") ? "dark" : "light");
});

document.getElementById("logoutBtn")?.addEventListener("click", () => {
  localStorage.removeItem("akg_token");
  localStorage.removeItem("akg_user");
  window.location.href = "index.html";
});
