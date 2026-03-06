/**
 * client_form.js – Lógica do formulário de criação/edição de clientes.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Obtém o caminho da URL
    const pathParts = window.location.pathname.split('/');
    const last = pathParts[pathParts.length - 1];
    const secondLast = pathParts[pathParts.length - 2];

    // Verifica se é modo edição (URL termina com '/edit' e o penúltimo é um número)
    if (last === 'edit' && !isNaN(secondLast)) {
        const clientId = secondLast;
        document.getElementById('form-title').textContent = 'Edit Client';
        document.getElementById('clientId').value = clientId;
        loadClientData(clientId);
    } else {
        document.getElementById('form-title').textContent = 'New Client';
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
        if (clientId) {
            // Edição: PUT /clientes/{id}
            await apiFetch(`/clientes/${clientId}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            alert('Client updated successfully!');
        } else {
            // Criação: POST /clientes
            await apiFetch('/clientes', {
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