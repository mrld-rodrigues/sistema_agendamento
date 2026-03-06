/**
 * clients.js – Lógica da página de listagem de clientes (admin).
 */

document.addEventListener('DOMContentLoaded', function() {
    // A verificação de admin já é feita no admin.js, então apenas carregamos os clientes.
    carregarClientes();
});

async function carregarClientes() {
    try {
        // A função apiFetch já lida com token e redirecionamento 401
        const clientes = await apiFetch('/admin/api/clientes');  // URL corrigida
        const tbody = document.getElementById('clientesTableBody');
        if (!tbody) {
            console.error('Elemento #clientesTableBody não encontrado');
            return;
        }

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
        // Se o erro for de sessão expirada, apiFetch já redireciona.
        // Caso contrário, mostramos uma mensagem amigável.
        if (!err.message.includes('Sessão expirada')) {
            alert('Erro ao carregar clientes: ' + err.message);
        }
    }
}

async function editarCliente(id) {
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
