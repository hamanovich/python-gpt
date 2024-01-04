const form = document.getElementById("form");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  getColors();
});

function getColors() {
  fetch("/palette", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      query: form.elements.query.value,
    }),
  })
    .then((response) => response.json())
    .then(({ colors }) => {
      const container = document.querySelector(".container");
      createColorBoxes(colors, container);
    });
}

function createColorBoxes(colors, container) {
  container.innerHTML = "";

  for (const color of colors) {
    const div = document.createElement("div");
    div.classList.add("color");
    div.style.backgroundColor = color;
    div.style.width = `calc(100%/${colors.length})`;

    div.addEventListener("click", () => navigator.clipboard.writeText(color));

    const span = document.createElement("span");
    span.classList.add("color-hex");
    span.innerText = color;
    div.appendChild(span);
    container.appendChild(div);
  }
}
