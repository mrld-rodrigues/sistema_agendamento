/**
 * professionals.js – Lógica da página de listagem de profissionais (admin).
 */

document.addEventListener('DOMContentLoaded', function() {
    carregarProfissionais();
});

async function carregarProfissionais() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/auth/login';
            return;
        }

        const profissionais = await apiFetch('/admin/api/profissionais?incluir_inativos=true');
        const tbody = document.getElementById('profissionaisTableBody');
        if (!tbody) return;

        if (profissionais.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="px-6 py-4 text-center text-gray-500">Nenhum profissional cadastrado.</td></tr>';
            return;
        }

        let html = '';
        profissionais.forEach(prof => {
            html += `
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.nome}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.especialidade}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.email || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.telefone || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.intervalo_minutos}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${prof.ativo ? 'Sim' : 'Não'}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button onclick="editarProfissional(${prof.id})" class="text-blue-600 hover:text-blue-900 mr-2">Editar</button>
                        <button onclick="desativarProfissional(${prof.id})" class="text-red-600 hover:text-red-900">${prof.ativo ? 'Desativar' : 'Ativar'}</button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error('Erro ao carregar profissionais:', err);
        const tbody = document.getElementById('profissionaisTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="8" class="px-6 py-4 text-center text-red-500">Erro ao carregar profissionais.</td></tr>';
        }
    }
}

// ==========================================================
// Funções globais para os botões
// ==========================================================
window.editarProfissional = function(id) {
    window.location.href = `/admin/professionals/${id}/edit`;
};

window.desativarProfissional = async function(id) {
    if (!confirm('Tem certeza que deseja alterar o status deste profissional?')) return;

    try {
        // Para saber se é desativar ou ativar, precisamos consultar o status atual.
        // Poderíamos passar via dataset, mas vamos fazer uma chamada para obter o status.
        // Como já temos a lista, podemos armazenar em um objeto, mas é mais simples: vamos buscar o profissional atual.
        const profissional = await apiFetch(`/profissionais/${id}`);
        const novoAtivo = !profissional.ativo;

        await apiFetch(`/profissionais/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ ativo: novoAtivo })
        });

        alert(novoAtivo ? 'Profissional ativado com sucesso!' : 'Profissional desativado com sucesso!');
        carregarProfissionais(); // recarrega a lista
    } catch (err) {
        alert('Erro: ' + err.message);
    }
};