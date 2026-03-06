/**
 * admin/clientes.js – Lógica da página de listagem de clientes (admin).
 * Carrega a lista de clientes via API e exibe em tabela.
 */

document.addEventListener('DOMContentLoaded', function() {
    // As funções checkAuth e checkAdmin já são chamadas no admin.js
    // Agora carregamos a lista de clientes
    carregarClientes();
});

async function carregarClientes() {
    try {
        const clientes = await apiFetch('/admin/clients');
        const tbody = document.getElementById('clientesTableBody');
        if (clientes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="px-6 py-4 text-center text-gray-500">Nenhum cliente cadastrado.</td></tr>';
            return;
        }
        let html = '';
        clientes.forEach(cliente => {
            html += `
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap">${cliente.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${cliente.nome}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${cliente.email || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${cliente.telefone || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button onclick="editarCliente(${cliente.id})" class="text-blue-600 hover:text-blue-900 mr-2">Editar</button>
                        <button onclick="excluirCliente(${cliente.id})" class="text-red-600 hover:text-red-900">Excluir</button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error('Erro ao carregar clientes:', err);
        alert('Erro ao carregar clientes.');
    }
}

function editarCliente(id) {
    // Redireciona para a página de edição (criaremos depois)
    window.location.href = `/admin/clients/${id}/edit`;
}

async function excluirCliente(id) {
    if (!confirm('Tem certeza que deseja excluir este cliente?')) return;
    try {
        await apiFetch(`/clientes/${id}`, { method: 'DELETE' });
        alert('Cliente excluído com sucesso!');
        carregarClientes(); // recarrega a lista
    } catch (err) {
        alert('Erro ao excluir cliente: ' + err.message);
    }
}

document.getElementById('novoClienteBtn').addEventListener('click', () => {
    window.location.href = '/admin/clients/new';
});