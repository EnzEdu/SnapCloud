// Adicionando o comportamento para o botão "Sair"
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function(event) {
            event.preventDefault();
            // Redireciona para a pág de login e substitui a pág atual no histórico
            window.location.replace("login.html");
        });
    }
});