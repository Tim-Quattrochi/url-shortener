const form = document.getElementById("create-form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const apiKey = document.getElementById("api_key").value;
  const code = document.getElementById("code").value;
  const url = document.getElementById("url").value;

  fetch("/url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "API-KEY": apiKey,
    },
    body: JSON.stringify({ code, url }),
  })
    .then(async (res) => {
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Something went wrong");
      }
      return res.json();
    })
    .then((data) => {
      console.log(data);
      form.reset();

      displaySuccess(
        `Shortened URL: <a href="${data.url}" target="_blank">${data.url}</a>`
      );
    })
    .catch((error) => {
      displayError(error.message);
    });
});

function displayError(message) {
  const errorContainer = document.getElementById("error-message");
  errorContainer.textContent = message;
  errorContainer.style.display = "block";
}

function displaySuccess(message) {
  const successContainer = document.getElementById("success-message");
  successContainer.textContent = message;
  successContainer.style.display = "block";
}
