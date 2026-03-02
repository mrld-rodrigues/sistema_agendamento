/**
 * professional_blocks.js – Gerenciamento de bloqueios do profissional.
 * Permite criar e excluir bloqueios de dia, horário e recorrentes.
 */

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();

    let professionalId = null;

    /**
     * Obtém o ID do profissional logado via /auth/me.
     */
    async function loadProfessionalId() {
        try {
            const user = await apiFetch('/auth/me');
            if (user.tipo !== 'profissional') {
                window.location.href = '/auth/login';
                return;
            }
            professionalId = user.profissional_id;
            // Preenche os campos ocultos (opcional, mas mantido para compatibilidade)
            document.getElementById('professionalId').value = professionalId;
            document.getElementById('professionalIdTime').value = professionalId;
            document.getElementById('professionalIdRec').value = professionalId;
            // Carrega a lista de bloqueios existentes
            loadBlocks();
        } catch (err) {
            console.error('Erro ao carregar profissional:', err);
            logout();
        }
    }

    /**
     * Carrega todos os bloqueios (dias e horários) do profissional e os exibe.
     */
    async function loadBlocks() {
        if (!professionalId) return;
        try {
            const blocks = await apiFetch(`/bloqueios/todos?profissional_id=${professionalId}`);
            const listDiv = document.getElementById('blocksList');
            if (blocks.length === 0) {
                listDiv.innerHTML = '<p class="text-gray-500">Nenhum bloqueio cadastrado.</p>';
                return;
            }
            let html = '<ul class="space-y-2">';
            blocks.forEach(block => {
                let description = '';
                if (block.tipo === 'dia') {
                    description = `Dia inteiro: ${block.data} – ${block.motivo || 'sem motivo'}`;
                } else if (block.tipo === 'horario') {
                    description = `Horário: ${block.data} ${block.hora_inicio} às ${block.hora_fim} – ${block.motivo || 'sem motivo'}`;
                }
                html += `
                    <li class="bg-gray-50 p-2 rounded flex justify-between items-center">
                        <span>${description}</span>
                        <button onclick="deleteBlock(${block.id}, '${block.tipo}')" class="text-red-500 hover:text-red-700">Excluir</button>
                    </li>
                `;
            });
            html += '</ul>';
            listDiv.innerHTML = html;
        } catch (err) {
            console.error('Erro ao carregar bloqueios:', err);
        }
    }

    /**
     * Função global para excluir um bloqueio.
     */
    window.deleteBlock = async function(id, tipo) {
        if (!confirm('Tem certeza que deseja excluir este bloqueio?')) return;
        try {
            let endpoint = '';
            if (tipo === 'dia') {
                endpoint = `/bloqueios/apagar-dia/${id}`;
            } else if (tipo === 'horario') {
                endpoint = `/bloqueios/apagar-horario/${id}`;
            } else {
                return;
            }
            await apiFetch(endpoint, { method: 'DELETE' });
            loadBlocks(); // recarrega a lista
        } catch (err) {
            alert('Erro ao excluir bloqueio: ' + err.message);
        }
    };

    // Formulário: Bloquear dia inteiro
    document.getElementById('blockDayForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            profissional_id: professionalId,
            data: document.getElementById('blockDate').value,
            motivo: document.getElementById('blockReason').value
        };
        try {
            await apiFetch('/bloqueios/bloquear-dia', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            alert('Dia bloqueado com sucesso!');
            document.getElementById('blockDate').value = '';
            document.getElementById('blockReason').value = '';
            loadBlocks();
        } catch (err) {
            alert('Erro: ' + err.message);
        }
    });

    // Formulário: Bloquear horário
    document.getElementById('blockTimeForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            profissional_id: professionalId,
            data: document.getElementById('blockTimeDate').value,
            hora_inicio: document.getElementById('blockStart').value,
            hora_fim: document.getElementById('blockEnd').value,
            motivo: document.getElementById('blockTimeReason').value
        };
        try {
            await apiFetch('/bloqueios/bloquear-horario', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            alert('Horário bloqueado com sucesso!');
            document.getElementById('blockTimeDate').value = '';
            document.getElementById('blockStart').value = '';
            document.getElementById('blockEnd').value = '';
            document.getElementById('blockTimeReason').value = '';
            loadBlocks();
        } catch (err) {
            alert('Erro: ' + err.message);
        }
    });

    // Formulário: Bloqueio recorrente
    document.getElementById('recurringBlockForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            profissional_id: professionalId,
            dia_semana: parseInt(document.getElementById('recurringDay').value),
            hora_inicio: document.getElementById('recurringStart').value,
            hora_fim: document.getElementById('recurringEnd').value,
            data_inicio: document.getElementById('recurringStartDate').value || null,
            data_fim: document.getElementById('recurringEndDate').value || null,
            motivo: document.getElementById('recurringReason').value
        };
        try {
            await apiFetch('/bloqueios/recorrente', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            alert('Bloqueio recorrente criado com sucesso!');
            // Limpa os campos
            document.getElementById('recurringDay').value = '0';
            document.getElementById('recurringStart').value = '';
            document.getElementById('recurringEnd').value = '';
            document.getElementById('recurringStartDate').value = '';
            document.getElementById('recurringEndDate').value = '';
            document.getElementById('recurringReason').value = '';
            // Não recarrega a lista porque recorrentes não aparecem em /todos
        } catch (err) {
            alert('Erro: ' + err.message);
        }
    });

    // Inicializa
    loadProfessionalId();
});