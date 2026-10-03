(() => {
    const form = document.querySelector("#prediction-form");
    const button = document.querySelector("#predict-button");

    if (!form || !button) {
        return;
    }

    form.addEventListener("submit", (event) => {
        if (!form.reportValidity()) {
            event.preventDefault();
            return;
        }

        if (button.disabled) {
            event.preventDefault();
            return;
        }

        button.disabled = true;
        button.classList.add("is-loading");
        button.setAttribute("aria-busy", "true");
        button.querySelector(".button-label").textContent = "Generating prediction…";
    });
})();
