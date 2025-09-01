function sendMessage() {
  let userInput = document.getElementById("user-input").value;
  if (!userInput.trim()) return;

  appendMessage("You", userInput, "user-message");

  fetch(`/get?msg=${encodeURIComponent(userInput)}`)
    .then(response => response.text())
    .then(data => {
      appendMessage("Bot", data, "bot-message");
      document.getElementById("user-input").value = "";
    });
}

function appendMessage(sender, text, className) {
  const chatBox = document.getElementById("chat-box");
  const message = document.createElement("div");
  message.classList.add("chat-message", className);
  message.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}
