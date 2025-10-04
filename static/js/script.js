const drawBtn = document.getElementById("drawBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const cardsContainer = document.getElementById("cards");
const reading = document.getElementById("reading");
const againBtn = document.getElementById("againBtn");

drawBtn.addEventListener("click", async () => {
  drawBtn.classList.add("d-none");
  loading.classList.remove("d-none");

  try {
    const response = await fetch("/api/draw");
    const data = await response.json();

    // Show results
    loading.classList.add("d-none");
    result.classList.remove("d-none");
    renderCards(data.cards);
    reading.textContent = data.reading;
  } catch (err) {
    loading.classList.add("d-none");
    alert("Error: Could not connect to the mystical realm (Ollama).");
    console.error(err);
  }
});

againBtn.addEventListener("click", () => {
  result.classList.add("d-none");
  drawBtn.classList.remove("d-none");
  cardsContainer.innerHTML = "";
  reading.textContent = "";
});

function renderCards(cards) {
  cardsContainer.innerHTML = "";
  cards.forEach((card) => {
    const imgPath = `/static/images/cards/${card.image}`;
    const reversedClass = card.reversed ? "reversed" : "";
    const meaning = card.reversed ? card.reversed : card.upright;

    cardsContainer.innerHTML += `
      <div class="card bg-dark border-light" style="width: 12rem;">
        <img src="${imgPath}" class="card-img-top ${reversedClass}" alt="${card.name}">
        <div class="card-body">
          <h5 class="card-title">${card.name}</h5>
          <p class="card-text">${meaning}</p>
        </div>
      </div>`;
  });
}
