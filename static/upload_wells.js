// Function to handle return to index
function handleReturnIndex() {
  window.location.href = "/";
}

// Function to handle well addition
function handleAddWell() {
  let input = document.createElement("input");
  input.type = "file";
  input.onchange = (e) => {
    let file = e.target.files[0];
    let formData = new FormData();
    formData.append("file", file);
    fetch("/upload", { method: "POST", body: formData }).then(() =>
      location.reload()
    );
  };
  input.click();
}

// Function to handle page refresh
function handleRefreshPage() {
  location.reload();
}

// Function to handle well selection
function handleWellSelection(event) {
  // Remove the selected class from all wells
  document.querySelectorAll(".well-item").forEach((well) => {
    well.classList.remove("well-item-selected");
  });

  // Add the selected class to the clicked well
  event.target.classList.add("well-item-selected");

  selectedWell = event.target.getAttribute("data-well-name");
  document.getElementById("remove-well").style.display = "block";
  document.getElementById("rename-well").style.display = "block";
}

// Function to handle well removal
function handleRemoveWell() {
  if (selectedWell) {
    fetch("/remove", {
      method: "POST",
      body: JSON.stringify({ filename: selectedWell }),
      headers: { "Content-Type": "application/json" },
    }).then(() => location.reload());
  }
}

// Function to handle well renaming
function handleRenameWell() {
  if (selectedWell) {
    let newName = prompt("Enter the new name for the well:");
    if (newName) {
      fetch("/rename", {
        method: "POST",
        body: JSON.stringify({ oldName: selectedWell, newName }),
        headers: { "Content-Type": "application/json" },
      }).then(() => location.reload());
    }
  }
}

// Add event listeners
document
  .getElementById("return-index")
  .addEventListener("click", handleReturnIndex);
document.getElementById("add-well").addEventListener("click", handleAddWell);
document
  .getElementById("refresh-page")
  .addEventListener("click", handleRefreshPage);
document
  .getElementById("remove-well")
  .addEventListener("click", handleRemoveWell);
document
  .getElementById("rename-well")
  .addEventListener("click", handleRenameWell);
document.querySelectorAll(".well-item").forEach((item) => {
  item.addEventListener("click", handleWellSelection);
});

// Variable to store the selected well
let selectedWell;
