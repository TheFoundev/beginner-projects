// Demo JavaScript for the fictional Foundev Robotics training site.
// These values are intentionally fake and exist only for the exercise.

const API_KEY = "demo_key_do_not_use_123456789";
const INTERNAL_DASHBOARD = "/staging/";

function showWelcome() {
  const banner = document.createElement("p");
  banner.textContent = "Training site loaded. Nothing here is real.";
  banner.style.fontSize = "13px";
  banner.style.color = "#0f766e";
  document.querySelector("footer").prepend(banner);
}

document.addEventListener("DOMContentLoaded", showWelcome);
