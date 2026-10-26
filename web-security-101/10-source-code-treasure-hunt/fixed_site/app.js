function showWelcome() {
  const banner = document.createElement("p");
  banner.textContent = "Training site loaded. Nothing here is real.";
  banner.style.fontSize = "13px";
  banner.style.color = "#0f766e";
  document.querySelector("footer").prepend(banner);
}

document.addEventListener("DOMContentLoaded", showWelcome);
