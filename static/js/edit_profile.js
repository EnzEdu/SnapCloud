// Adicionando o comportamento para o botão "Sair"
// document.addEventListener('DOMContentLoaded', function() {
//     const logoutBtn = document.getElementById("logout-btn");
//     if (logoutBtn) {
//         logoutBtn.addEventListener("click", function(event) {
//             event.preventDefault();
//             // Redireciona para a pág de login e substitui a pág atual no histórico
//             window.location.replace("login.html");
//         });
//     }
// });

// Editar dados
function habilitarEdicao(id) {
    const campo = document.getElementById(id);
    if (campo) {
        campo.removeAttribute('readonly');
        campo.classList.add('editavel');
        campo.focus();
    }
}

// Cancelar edição
// function cancelarEdicao() {
//     if (confirm('Deseja cancelar as alterações?')) {
//         window.location.href = "dashboard.html";
//     }
// }

// Salvar os dados do usuário
// function salvarDados(event) {
//     event.preventDefault();
//     alert('Dados salvos com sucesso!');
//     // Aqui você pode adicionar lógica para salvar os dados no servidor, se necessário
// }