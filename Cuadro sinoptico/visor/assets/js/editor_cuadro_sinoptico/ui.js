export function setStatus(statusBox, message, level = "info") {
  statusBox.textContent = message;
  statusBox.className = "status";
  if (level === "error") statusBox.classList.add("error");
  if (level === "ok") statusBox.classList.add("ok");
}

export function openAdvancedModal(advancedModal) {
  advancedModal.classList.remove("hidden");
}

export function closeAdvancedModal(advancedModal) {
  advancedModal.classList.add("hidden");
}
