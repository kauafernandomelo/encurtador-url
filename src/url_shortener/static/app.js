const form = document.querySelector("#shorten-form");
const urlInput = document.querySelector("#url-input");
const submitButton = document.querySelector("#submit-button");
const formMessage = document.querySelector("#form-message");
const resultCard = document.querySelector("#result-card");
const shortUrl = document.querySelector("#short-url");
const statsLink = document.querySelector("#stats-link");
const copyButton = document.querySelector("#copy-button");

function showMessage(message, type = "") {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type}`.trim();
}

async function copyToClipboard(text) {
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  submitButton.disabled = true;
  showMessage("Gerando link curto...");

  try {
    const response = await fetch("/api/urls", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput.value }),
    });

    if (!response.ok) {
      throw new Error("Informe uma URL válida começando com http:// ou https://.");
    }

    const data = await response.json();
    shortUrl.textContent = data.short_url;
    shortUrl.href = data.short_url;
    statsLink.href = `/api/urls/${data.code}`;
    resultCard.hidden = false;
    showMessage("URL encurtada com sucesso.", "success");
  } catch (error) {
    resultCard.hidden = true;
    showMessage(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
});

copyButton.addEventListener("click", async () => {
  await copyToClipboard(shortUrl.href);
  showMessage("Link copiado para a área de transferência.", "success");
});
