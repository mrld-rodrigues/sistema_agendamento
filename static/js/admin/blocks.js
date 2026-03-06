/**
 * blocks.js – Lógica da página de gerenciamento de bloqueios (admin).
 */

document.addEventListener('DOMContentLoaded', function() {
    carregarProfissionais();
    document.getElementById('profissionalSelect').addEventListener('change', carregarBloqueios);
});

async function carregarProfissionais() {
    try {
        const profissionais = await apiFetch('/profissionais');
        const select = document.getElementById('profissionalSelect');
        select.innerHTML = '<option value="">Selecione um profissional...</option>';
        profissionais.forEach(p => {
            select.innerHTML += `<option value="${p.id}">${p.nome} (${p.especialidade})</option>`;
        });
    } catch (err) {
        showToast('Erro ao carregar profissionais: ' + err.message, 'error');
    }
}

async function carregarBloqueios() {
    const profissionalId = document.getElementById('profissionalSelect').value;
    if (!profissionalId) return;

    try {
        const dados = await apiFetch(`/profissionais/${profissionalId}/bloqueios`);
        const container = document.getElementById('blocksContainer');
        let html = '<h3 class="text-lg font-bold mb-2">Bloqueios</h3>';

        // Dias
        if (dados.dias && dados.dias.length > 0) {
            html += '<h4 class="font-semibold mt-2">Dias inteiros:</h4><ul class="list-disc pl-5">';
            dados.dias.forEach(d => {
                html += `<li>${d.data} – ${d.motivo || 'sem motivo'} 
                    <button onclick="excluirBloqueio('dia', ${d.id})" class="text-red-500 hover:text-red-700 ml-2">Excluir</button>
                </li>`;
            });
            html += '</ul>';
        }

        // Horários
        if (dados.horarios && dados.horarios.length > 0) {
            html += '<h4 class="font-semibold mt-2">Horários:</h4><ul class="list-disc pl-5">';
            dados.horarios.forEach(h => {
                html += `<li>${h.data} ${h.hora_inicio} às ${h.hora_fim} – ${h.motivo || 'sem motivo'}
                    <button onclick="excluirBloqueio('horario', ${h.id})" class="text-red-500 hover:text-red-700 ml-2">Excluir</button>
                </li>`;
            });
            html += '</ul>';
        }

        // Recorrentes
        if (dados.recorrentes && dados.recorrentes.length > 0) {
            html += '<h4 class="font-semibold mt-2">Recorrentes:</h4><ul class="list-disc pl-5">';
            const diasSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
            dados.recorrentes.forEach(r => {
                const dia = diasSemana[r.dia_semana] || r.dia_semana;
                let periodo = '';
                if (r.data_inicio && r.data_fim) periodo = ` (${r.data_inicio} a ${r.data_fim})`;
                else if (r.data_inicio) periodo = ` (a partir de ${r.data_inicio})`;
                else if (r.data_fim) periodo = ` (até ${r.data_fim})`;
                html += `<li>${dia}, ${r.hora_inicio} às ${r.hora_fim} – ${r.motivo || 'sem motivo'}${periodo}
                    <button onclick="excluirBloqueio('recorrente', ${r.id})" class="text-red-500 hover:text-red-700 ml-2">Excluir</button>
                </li>`;
            });
            html += '</ul>';
        }

        if (!dados.dias?.length && !dados.horarios?.length && !dados.recorrentes?.length) {
            html = '<p class="text-gray-500">Nenhum bloqueio cadastrado para este profissional.</p>';
        }

        container.innerHTML = html;
    } catch (err) {
        showToast('Erro ao carregar bloqueios: ' + err.message, 'error');
    }
}

window.excluirBloqueio = async function(tipo, id) {
    if (!confirm('Tem certeza que deseja excluir este bloqueio?')) return;

    let endpoint = '';
    if (tipo === 'dia') endpoint = `/bloqueios/apagar-dia/${id}`;
    else if (tipo === 'horario') endpoint = `/bloqueios/apagar-horario/${id}`;
    else if (tipo === 'recorrente') endpoint = `/bloqueios/recorrente/${id}`;
    else return;

    try {
        await apiFetch(endpoint, { method: 'DELETE' });
        showToast('Bloqueio excluído com sucesso!', 'success');
        carregarBloqueios(); // recarrega a lista
    } catch (err) {
        showToast('Erro ao excluir bloqueio: ' + err.message, 'error');
    }
};