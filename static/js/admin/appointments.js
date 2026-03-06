/**
 * appointments.js – Lógica da página de listagem de agendamentos (admin).
 */

document.addEventListener('DOMContentLoaded', function() {
    carregarProfissionais();
    carregarAgendamentos();

    document.getElementById('btnFiltrar').addEventListener('click', () => {
        carregarAgendamentos();
    });

    document.getElementById('btnLimpar').addEventListener('click', () => {
        document.getElementById('filtroProfissional').value = '';
        document.getElementById('filtroData').value = '';
        carregarAgendamentos();
    });

    // Modal de remarcação
    const modal = document.getElementById('rescheduleModal');
    document.getElementById('btnCancelarModal').addEventListener('click', () => {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    });

    document.getElementById('btnConfirmarRemarcacao').addEventListener('click', async () => {
        const id = document.getElementById('rescheduleId').value;
        const novaData = document.getElementById('rescheduleDateTime').value;
        if (!novaData) {
            alert('Selecione uma data/hora');
            return;
        }
        try {
            await apiFetch(`/admin/agendamentos/${id}/remarcar`, {
                method: 'PUT',
                body: JSON.stringify({ data_hora: novaData.replace('T', ' ') + ':00' })
            });
            alert('Agendamento remarcado com sucesso!');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            carregarAgendamentos();
        } catch (err) {
            alert('Erro: ' + err.message);
        }
    });
});

async function carregarProfissionais() {
    try {
        const profissionais = await apiFetch('/profissionais');
        const select = document.getElementById('filtroProfissional');
        profissionais.forEach(p => {
            select.innerHTML += `<option value="${p.id}">${p.nome} (${p.especialidade})</option>`;
        });
    } catch (err) {
        console.error('Erro ao carregar profissionais:', err);
    }
}

async function carregarAgendamentos() {
    try {
        const profissionalId = document.getElementById('filtroProfissional').value;
        const data = document.getElementById('filtroData').value;

        let url = '/admin/agendamentos';
        const params = new URLSearchParams();
        if (profissionalId) params.append('profissional_id', profissionalId);
        if (data) params.append('data', data);
        if (params.toString()) url += '?' + params.toString();

        const agendamentos = await apiFetch(url);
        const tbody = document.getElementById('appointmentsTableBody');
        if (!tbody) return;

        if (agendamentos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="px-6 py-4 text-center text-gray-500">Nenhum agendamento encontrado.</td></tr>';
            return;
        }

        let html = '';
        agendamentos.forEach(a => {
            const dataHora = new Date(a.data_hora).toLocaleString('pt-BR');
            html += `
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap">${a.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${a.cliente}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${a.profissional}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${a.servico}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${dataHora}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${a.duracao_minutos} min</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button onclick="abrirModalRemarcacao(${a.id})" class="text-blue-600 hover:text-blue-900 mr-2">Remarcar</button>
                        <button onclick="cancelarAgendamento(${a.id})" class="text-red-600 hover:text-red-900">Cancelar</button>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error('Erro ao carregar agendamentos:', err);
        const tbody = document.getElementById('appointmentsTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="7" class="px-6 py-4 text-center text-red-500">Erro ao carregar agendamentos.</td></tr>';
        }
    }
}

// Funções globais
window.abrirModalRemarcacao = function(id) {
    document.getElementById('rescheduleId').value = id;
    document.getElementById('rescheduleDateTime').value = '';
    const modal = document.getElementById('rescheduleModal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
};

window.cancelarAgendamento = async function(id) {
    if (!confirm('Tem certeza que deseja cancelar este agendamento?')) return;
    try {
        await apiFetch(`/admin/agendamentos/${id}`, { method: 'DELETE' });
        alert('Agendamento cancelado com sucesso!');
        carregarAgendamentos();
    } catch (err) {
        alert('Erro: ' + err.message);
    }
};