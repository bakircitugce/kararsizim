document.querySelectorAll(".message-close").forEach((button) => {
  button.addEventListener("click", () => button.closest(".message").remove());
});

window.setTimeout(() => {
  document.querySelectorAll(".message").forEach((message) => message.remove());
}, 4000);
