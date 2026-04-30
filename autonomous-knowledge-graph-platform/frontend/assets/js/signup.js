const passwordInput = document.getElementById("passwordInput");
const strengthBar = document.getElementById("strengthBar");
const strengthText = document.getElementById("strengthText");

function passwordChecks(password) {
  return [
    password.length >= 12,
    /[a-z]/.test(password),
    /[A-Z]/.test(password),
    /\d/.test(password),
    /[^A-Za-z0-9]/.test(password)
  ];
}

function updatePasswordStrength() {
  if (!passwordInput || !strengthBar || !strengthText) return;
  const password = passwordInput.value;
  const score = passwordChecks(password).filter(Boolean).length;
  strengthBar.style.width = `${score * 20}%`;
  strengthBar.dataset.score = String(score);
  const labels = ["Very weak", "Very weak", "Weak", "Good", "Strong", "Very strong"];
  strengthText.textContent = password
    ? `${labels[score]} password`
    : "Use 12+ characters with upper, lower, number, and symbol.";
}

function randomFrom(chars) {
  const values = new Uint32Array(1);
  crypto.getRandomValues(values);
  return chars[values[0] % chars.length];
}

function shuffle(text) {
  const chars = text.split("");
  for (let index = chars.length - 1; index > 0; index -= 1) {
    const values = new Uint32Array(1);
    crypto.getRandomValues(values);
    const swapIndex = values[0] % (index + 1);
    [chars[index], chars[swapIndex]] = [chars[swapIndex], chars[index]];
  }
  return chars.join("");
}

function generateStrongPassword() {
  const lower = "abcdefghijkmnopqrstuvwxyz";
  const upper = "ABCDEFGHJKLMNPQRSTUVWXYZ";
  const numbers = "23456789";
  const symbols = "!@#$%^&*?";
  const all = lower + upper + numbers + symbols;
  let password = [
    randomFrom(lower),
    randomFrom(upper),
    randomFrom(numbers),
    randomFrom(symbols)
  ].join("");
  while (password.length < 16) {
    password += randomFrom(all);
  }
  return shuffle(password);
}

passwordInput?.addEventListener("input", updatePasswordStrength);

document.getElementById("generatePassword")?.addEventListener("click", () => {
  passwordInput.value = generateStrongPassword();
  passwordInput.type = "text";
  document.getElementById("togglePassword").textContent = "Hide";
  document.getElementById("togglePassword").setAttribute("aria-label", "Hide password");
  updatePasswordStrength();
  passwordInput.focus();
});

document.getElementById("togglePassword")?.addEventListener("click", (event) => {
  const isHidden = passwordInput.type === "password";
  passwordInput.type = isHidden ? "text" : "password";
  event.currentTarget.textContent = isHidden ? "Hide" : "Show";
  event.currentTarget.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
});

document.getElementById("signupForm")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  if (passwordChecks(form.get("password") || "").filter(Boolean).length < 5) {
    alert("Please use a strong password with 12+ characters, uppercase, lowercase, number, and symbol.");
    return;
  }
  try {
    await API.post("/api/auth/signup", {
      name: form.get("name"),
      email: form.get("email"),
      password: form.get("password"),
      organization: form.get("organization"),
      department: form.get("department"),
      role: form.get("role")
    });
    window.location.href = "login.html";
  } catch (error) {
    alert(error.message);
  }
});
