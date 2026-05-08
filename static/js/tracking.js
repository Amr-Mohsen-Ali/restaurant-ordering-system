// Frontend behavior for the order tracking page.
const form = document.querySelector("#trackingForm");
const orderInput = document.querySelector("#orderId");
const resultBox = document.querySelector("#result");
const trackButton = document.querySelector("#trackButton");


function showMessage(message, type) {
  // Reset result styles before showing the next message.
  resultBox.className = "";

  if (type) {
    resultBox.classList.add(type);
  }

  resultBox.textContent = message;
}


form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const orderId = orderInput.value.trim();

  if (orderId === "") {
    showMessage("Please enter an order ID", "error");
    orderInput.focus();
    return;
  }

  trackButton.disabled = true;
  showMessage("Loading order status...", "");

  try {
    const response = await fetch(`/track/${encodeURIComponent(orderId)}`);
    const data = await response.json();

    if (!response.ok || data.success === false) {
      showMessage(data.error || "Something went wrong. Please try again.", "error");
      return;
    }

    showMessage(`Order ${orderId}: ${data.status}`, "success");
  } catch (error) {
    showMessage("Unable to connect to the server. Please try again.", "error");
  } finally {
    trackButton.disabled = false;
  }
});