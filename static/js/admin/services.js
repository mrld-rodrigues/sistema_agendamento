/**
 * services.js – Lógica da página de listagem de serviços (admin).
 */

document.addEventListener('DOMContentLoaded', function() {
    carregarServicos();
});

async function carregarServicos() {
    try {
        // Usa incluir_inativos=true para mostrar todos
        const servicos = await apiFetch('/admin/api/servicos?incluir_inativos=true');
        const tbody = document.getElementById('servicesTableBody');
        if (!tbody) return;

        if (servicos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="px-6 py-4 text-center text-gray-500">Nenhum serviço cadastrado.</td></tr>';
            return;
        }

        let html = '';
        servicos.forEach(s => {
            html += `
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap">${s.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${s.nome}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${s.descricao || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${s.duracao_minutos}</td>
                    <td class="px-6 py-4 whitespace-nowrap">€ ${parseFloat(s.preco).toFixed(2)}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${s.ativo ? 'Sim' : 'Não'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button onclick="editarServico(${s.id})" class="text-blue-600 hover:text-blue-900 mr-2">Editar</button>
                        <button onclick="desativarServico(${s.id})" class="text-red-600 hover:text-red-900">${s.ativo ? 'Desativar' : 'Ativar'}</button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error('Erro ao carregar serviços:', err);
        const tbody = document.getElementById('servicesTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" class="px-6 py-4 text-center text-red-500">Erro ao carregar serviços.</td></tr>';
        }
    }
}

// Funções globais para os botões
window.editarServico = function(id) {
    window.location.href = `/admin/services/${id}/edit`;
};

window.desativarServico = async function(id) {
    if (!confirm('Tem certeza que deseja alterar o status deste serviço?')) return;

    try {
        // Obtém o serviço atual para saber o status
        const servico = await apiFetch(`/servicos/${id}`);
        const novoAtivo = !servico.ativo;

        await apiFetch(`/servicos/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ ativo: novoAtivo })
        });

        alert(novoAtivo ? 'Serviço ativado com sucesso!' : 'Serviço desativado com sucesso!');
        carregarServicos(); // recarrega a lista
    } catch (err) {
        alert('Erro: ' + err.message);
    }
};