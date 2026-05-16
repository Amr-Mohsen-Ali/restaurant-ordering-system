document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("reservation_date");
  const slotInput = document.getElementById("reservation_slot");
  const partyInput = document.getElementById("party_size");
  const tableInput = document.getElementById("table_number");
  const floorPlan = document.getElementById("floorPlan");
  const availabilityMessage = document.getElementById("availabilityMessage");

  function setMessage(message) {
    availabilityMessage.textContent = message;
  }

  function selectTable(button) {
    if (button.disabled) {
      return;
    }
    floorPlan.querySelectorAll(".table-card").forEach((table) => {
      table.classList.remove("selected");
    });
    button.classList.add("selected");
    tableInput.value = button.dataset.tableNumber;
  }

  async function refreshAvailability() {
    const date = dateInput.value;
    const slot = slotInput.value;
    const partySize = partyInput.value;

    if (!date || !slot || !partySize) {
      setMessage("Choose a date, slot, and party size to see availability.");
      return;
    }

    setMessage("Checking table availability...");
    try {
      const params = new URLSearchParams({ date, slot, party_size: partySize });
      const response = await fetch(`/api/reservations/availability?${params}`);
      const data = await response.json();

      if (!response.ok || !data.success) {
        setMessage(data.error || "Could not check availability.");
        return;
      }

      const byNumber = new Map(data.tables.map((table) => [String(table.number), table]));
      floorPlan.querySelectorAll(".table-card").forEach((button) => {
        const table = byNumber.get(button.dataset.tableNumber);
        const available = table && table.available;
        button.disabled = !available;
        button.classList.toggle("booked", table && table.booked);
        button.classList.toggle("too-small", table && !table.fits_party);
        if (!available && button.classList.contains("selected")) {
          button.classList.remove("selected");
          tableInput.value = "";
        }
      });

      const availableCount = data.tables.filter((table) => table.available).length;
      setMessage(`${availableCount} tables available for this slot.`);
    } catch (error) {
      setMessage("Could not check availability.");
    }
  }

  floorPlan.addEventListener("click", (event) => {
    const button = event.target.closest(".table-card");
    if (button) {
      selectTable(button);
    }
  });

  [dateInput, slotInput, partyInput].forEach((input) => {
    input.addEventListener("change", refreshAvailability);
  });

  const today = new Date().toISOString().split("T")[0];
  dateInput.min = today;
  refreshAvailability();
});
