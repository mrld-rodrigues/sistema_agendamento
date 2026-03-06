/**
 * client_form.js – Lógica do formulário de criação/edição de clientes.
 * 
 * Funções:
 * - loadClientData(): se estiver editando, carrega os dados do cliente e preenche o formulário.
 * - saveClient(): envia os dados para a API (POST ou PUT conforme o caso).
 */

document.addEventListener('DOMContentLoaded', function() {
    // Verifica se há um ID na URL (modo edição)
    const pathParts = window.location.pathname.split('/');
    const clientId = pathParts[3] === 'edit' ? pathParts[2] : null; // Ex: /admin/clients/5/edit

    if (clientId) {
        document.getElementById('form-title').textContent = 'Edit Client';
        document.getElementById('clientId').value = clientId;
        loadClientData(clientId);
    }

    document.getElementById('clientForm').addEventListener('submit', saveClient);
});

/**
 * Carrega os dados de um cliente e preenche o formulário.
 * @param {number} id - ID do cliente.
 */
async function loadClientData(id) {
    try {
        const client = await apiFetch(`/clientes/${id}`);
        document.getElementById('nome').value = client.nome || '';
        document.getElementById('email').value = client.email || '';
        document.getElementById('telefone').value = client.telefone || '';
    } catch (err) {
        console.error('Erro ao carregar cliente:', err);
        alert('Error loading client data.');
    }
}

/**
 * Envia os dados do formulário para a API (cria ou atualiza).
 * @param {Event} e - Evento de submit.
 */
async function saveClient(e) {
    e.preventDefault();

    const clientId = document.getElementById('clientId').value;
    const payload = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value || null,
        telefone: document.getElementById('telefone').value || null
    };

    try {
        let response;
        if (clientId) {
            // Edição: PUT /clientes/{id}
            response = await apiFetch(`/clientes/${clientId}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            alert('Client updated successfully!');
        } else {
            // Criação: POST /clientes
            response = await apiFetch('/clientes', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            alert('Client created successfully!');
        }
        // Redireciona para a listagem
        window.location.href = '/admin/clients';
    } catch (err) {
        alert('Error saving client: ' + err.message);
    }
}