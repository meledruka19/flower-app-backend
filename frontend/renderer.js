document.addEventListener("DOMContentLoaded", () => {
  const flowerImg = document.getElementById("flower");
  const button = document.getElementById("waterBtn");
  const status = document.getElementById("status");
  const API_URL = "http://127.0.0.1:5000"; // Replace with online backend URL later

  const flowerStages = [
    "./assets/sprout.png",       // days 1-2
    "./assets/small_flower.png", // days 3-4
    "./assets/almost_flower.png",// days 5-6
    "./assets/full_flower.png"   // day 7
  ];

  let flowerState = {
    day: 1,
    growth: 100,
    last_watered: null
  };

  function getFlowerImage(day) {
    if (day <= 2) return flowerStages[0];
    if (day <= 4) return flowerStages[1];
    if (day <= 6) return flowerStages[2];
    return flowerStages[3];
  }

  async function fetchFlowerState() {
    try {
      const response = await fetch(`${API_URL}/flower`);
      const data = await response.json();
      flowerState = data;
      updateFlowerUI();
    } catch (error) {
      console.error("Failed to fetch flower state:", error);
      status.textContent = "Cannot reach server";
    }
  }

  function updateFlowerUI() {
    flowerImg.src = getFlowerImage(flowerState.day);
    flowerImg.style.width = flowerState.growth + "px";

    if (!flowerState.last_watered) {
      status.textContent = "💀 Flower died! Starting over.";
    } else {
      const lastDate = new Date(flowerState.last_watered);
      const today = new Date();
      const diffHours = (today - lastDate) / (1000 * 60 * 60);
      if (diffHours >= 24) {
        status.textContent = "💀 Flower died! Starting over.";
      } else if (lastDate.toDateString() === today.toDateString()) {
        status.textContent = "🌸 Already watered today!";
      } else {
        status.textContent = `💜 Day ${flowerState.day}/7`;
      }
    }
  }

  async function waterFlower() {
    try {
      const response = await fetch(`${API_URL}/water`, { method: "POST" });
      const data = await response.json();
      flowerState = data;
      updateFlowerUI();
    } catch (error) {
      console.error("Failed to water flower:", error);
      status.textContent = "Cannot reach server";
    }
  }

  button.addEventListener("click", waterFlower);

  // Auto-refresh every 5 seconds to sync with partner
  setInterval(fetchFlowerState, 5000);

  // Initial load
  fetchFlowerState();
});
