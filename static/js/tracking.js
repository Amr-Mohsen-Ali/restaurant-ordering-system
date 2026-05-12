// Frontend behavior for the order tracking page.
const form = document.querySelector("#trackingForm");
const orderInput = document.querySelector("#orderId");
const resultBox = document.querySelector("#result");
const trackButton = document.querySelector("#trackButton");
const advanceButton = document.querySelector("#advanceButton");
const orderDetails = document.querySelector("#orderDetails");
const statusSteps = document.querySelectorAll("[data-status-step]");

let currentOrderId = "";


function showMessage(message, type) {
  // Reset result styles before showing the next message.
  resultBox.className = "";

  if (type) {
    resultBox.classList.add(type);
  }

  resultBox.textContent = message;
}


function updateProgress(status) {
  const statusOrder = ["Preparing", "Out for Delivery", "Delivered"];
  const activeIndex = statusOrder.indexOf(status);

  statusSteps.forEach((step, index) => {
    step.classList.toggle("active", index <= activeIndex);
  });
}


function showOrderDetails(order) {
  const itemList = order.items.length > 0 ? order.items.join(", ") : "No items listed";

  orderDetails.hidden = false;
  orderDetails.innerHTML = `
    <h2>Order Details</h2>
    <p><strong>Items:</strong> ${itemList}</p>
    <p><strong>Total:</strong> ${Number(order.total).toFixed(2)}</p>
  `;
}


function resetOrderDisplay() {
  currentOrderId = "";
  advanceButton.hidden = true;
  orderDetails.hidden = true;
  orderDetails.innerHTML = "";
  updateProgress("");
}


function showSuccessfulOrder(orderId, data) {
  currentOrderId = orderId;
  showMessage(`Order ${orderId}: ${data.status}`, "success");
  showOrderDetails(data.order);
  updateProgress(data.status);
  advanceButton.hidden = data.status === "Delivered";
}


form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const orderId = orderInput.value.trim();

  if (orderId === "") {
    resetOrderDisplay();
    showMessage("Please enter an order ID", "error");
    orderInput.focus();
    return;
  }

  trackButton.disabled = true;
  advanceButton.disabled = true;
  showMessage("Loading order status...", "");

  try {
    const response = await fetch(`/track/${encodeURIComponent(orderId)}`);
    const data = await response.json();

    if (!response.ok || data.success === false) {
      resetOrderDisplay();
      showMessage(data.error || "Something went wrong. Please try again.", "error");
      return;
    }

    showSuccessfulOrder(orderId, data);
  } catch (error) {
    resetOrderDisplay();
    showMessage("Unable to connect to the server. Please try again.", "error");
  } finally {
    trackButton.disabled = false;
    advanceButton.disabled = false;
  }
});


advanceButton.addEventListener("click", async () => {
  if (currentOrderId === "") {
    return;
  }

  advanceButton.disabled = true;
  showMessage("Updating order status...", "");

  try {
    const response = await fetch(`/track/${encodeURIComponent(currentOrderId)}/advance`, {
      method: "POST",
    });
    const data = await response.json();

    if (!response.ok || data.success === false) {
      showMessage(data.error || "Unable to update order status.", "error");
      return;
    }

    showSuccessfulOrder(currentOrderId, data);
  } catch (error) {
    showMessage("Unable to connect to the server. Please try again.", "error");
  } finally {
    advanceButton.disabled = false;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const orderIdParam = urlParams.get('order_id');
  if (orderIdParam) {
    orderInput.value = orderIdParam;
    form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
  }
});