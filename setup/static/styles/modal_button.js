const mostrarModalBtn = document.getElementById("mostrarModal");
const modal = document.getElementById("modal");
const fecharModalBtn = document.querySelector(".fechar");

if (mostrarModalBtn) {
    mostrarModalBtn.addEventListener("click", () => {
        modal.style.display = "block";
    });
}

if (fecharModalBtn) {
    fecharModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });
}

window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});