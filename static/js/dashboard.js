// Função que esconde todas as seções
function hideAllSections() {
    const sections = document.querySelectorAll('.dashboard-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
}

// Função que mostra a seção com o id especificado
function showSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    }
}

// Configurar a página com base no parâmetro de categoria da URL
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category'); // Obter o parâmetro `category` da URL

    // Esconde todas as seções inicialmente
    hideAllSections();

    // Determinar a categoria e exibir a seção correspondente
    if (category === 'imagens') {
        showSection('imagens-section');
    } else if (category === 'videos') {
        showSection('videos-section');
    } else if (category === 'audios') {
        showSection('audios-section');
    } else {
        // Se nenhuma categoria for especificada, mostra todas as seções
        showSection('imagens-section');
        showSection('videos-section');
        showSection('audios-section');
    }

    // Marcar o link ativo na navbar
    document.querySelectorAll('.category-link').forEach(link => {
        if (link.getAttribute('data-category') === category) {
            link.classList.add('active');
        }
    });

    // Evento para quando o usuário clicar nas categorias da navbar
    document.querySelectorAll('.category-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Remover a classe 'active' de todos os links
            document.querySelectorAll('.category-link').forEach(link => {
                link.classList.remove('active');
            });

            // Adicionar a classe 'active' ao link clicado
            e.target.classList.add('active');

            const category = e.target.getAttribute('data-category');

            // Esconde todas as seções
            hideAllSections();

            // Exibe apenas a seção correspondente
            if (category === 'imagens') {
                showSection('imagens-section');
            } else if (category === 'videos') {
                showSection('videos-section');
            } else if (category === 'audios') {
                showSection('audios-section');
            } else {
                // Se for 'Todos', mostra todas as seções
                showSection('imagens-section');
                showSection('videos-section');
                showSection('audios-section');
            }
        });
    });
});

// Adicione funcionalidade para abrir e fechar o modal do Upload
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
                <option value="musica">Música</option>
                <option value="arte">Arte</option>
                <option value="filme">Filme</option>
                <option value="educacional">Educacional</option>
            </select>
        `;
        fileDetailsDiv.appendChild(fileContainer);
    });
});