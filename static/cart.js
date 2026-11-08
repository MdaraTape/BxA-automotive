const addForm = document.querySelector("[data-cart-add]");
if (addForm) {
  addForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = addForm.querySelector("button");
    const status = addForm.querySelector("[data-cart-status]");
    button.disabled = true;
    try {
      const response = await fetch(addForm.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(addForm)
      });
      const result = await response.json();
      status.textContent = result.message;
      if (response.ok) document.querySelector("#cart-count").textContent = result.count;
    } catch {
      status.textContent = "Could not confirm the update. Check your cart before trying again.";
    } finally {
      button.disabled = false;
    }
  });
}
