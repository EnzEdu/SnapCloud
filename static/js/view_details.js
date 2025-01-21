// Redirecionar para a Dashboard com um Filtro
document.querySelectorAll('.category-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const category = e.target.getAttribute('data-category');

        // Redirecionar para a dashboard com um filtro na URL
        if (category) {
            window.location.href = `/templates/dashboard.html?category=${category}`;
        }
    });
});

// Adicione funcionalidade para abrir e fechar o modal:
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("upload-modal");
    const openModal = document.getElementById("open-upload-modal");
    const closeModal = document.querySelector(".close-btn");

    openModal.addEventListener("click", (e) => {
        e.preventDefault();
        modal.style.display = "block";
    });

    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});

// Upload
document.getElementById('file-upload').addEventListener('change', function(event) {
    const files = event.target.files;
    const fileDetailsDiv = document.getElementById('file-details');
    
    fileDetailsDiv.innerHTML = '';
    
    Array.from(files).forEach((file, index) => {
        const fileContainer = document.createElement('div');
        fileContainer.classList.add('file-container');
        fileContainer.innerHTML = `
            <h4>Arquivo: ${file.name}</h4>
            <label for="description-${index}">Descrição:</label>
            <textarea id="description-${index}" name="description-${index}" placeholder="Adicione uma descrição..." required></textarea>
            
            <label for="tags-${index}">Tags (separadas por vírgulas):</label>
            <input type="text" id="tags-${index}" name="tags-${index}" placeholder="Ex.: Natureza, Música">
            
            <label for="genre-${index}">Gênero:</label>
            <select id="genre-${index}" name="genre-${index}" required>
                <option value="">Selecione um gênero</option>
                <option value="nao_aplicavel">Não Aplicável</option>
                <option value="natureza">Natureza</option>
                <option value="tecnologia">Tecnologia</option>
                <option value="música">Música</option>
                <option value="arte">Arte</option>
                <option value="filme">Filme</option>
                <option value="educacional">Educacional</option>
            </select>
        `;
        fileDetailsDiv.appendChild(fileContainer);
    });
});

// Editar
document.addEventListener('DOMContentLoaded', function() {
    const editBtns = document.querySelectorAll('.edit-btn');
    editBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const input = this.closest('.input-group').querySelector('input, textarea');
            input.classList.add('editavel');
            input.removeAttribute('readonly');
            input.focus();
        });
    });
});