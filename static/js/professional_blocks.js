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
            document.getElementById('professionalIdPeriod').value = professionalId;
            // Carrega a lista de bloqueios existentes
            loadBlocks();
        } catch (err) {
            console.error('Erro ao carregar profissional:', err);
            logout();
        }
    }

    /**
     * Carrega todos os bloqueios (dias, horários e recorrentes) e os exibe na lista.
     */
    async function loadBlocks() {
        if (!professionalId) return;
        try {
            const blocksData = await apiFetch(`/profissionais/${professionalId}/bloqueios`);
            const listDiv = document.getElementById('blocksList');
            if (!listDiv) return;

            let html = '<ul class="space-y-2">';

            // Dias
            if (blocksData.dias && blocksData.dias.length > 0) {
                blocksData.dias.forEach(d => {
                    html += `
                        <li class="bg-gray-50 p-2 rounded flex justify-between items-center">
                            <span>Dia inteiro: ${d.data} – ${d.motivo || 'sem motivo'}</span>
                            <button onclick="deleteBlock(${d.id}, 'dia')" class="text-red-500 hover:text-red-700">Excluir</button>
                        </li>
                    `;
                });
            }

            // Horários
            if (blocksData.horarios && blocksData.horarios.length > 0) {
                blocksData.horarios.forEach(h => {
                    html += `
                        <li class="bg-gray-50 p-2 rounded flex justify-between items-center">
                            <span>Horário: ${h.data} ${h.hora_inicio} às ${h.hora_fim} – ${h.motivo || 'sem motivo'}</span>
                            <button onclick="deleteBlock(${h.id}, 'horario')" class="text-red-500 hover:text-red-700">Excluir</button>
                        </li>
                    `;
                });
            }

            // Recorrentes
            if (blocksData.recorrentes && blocksData.recorrentes.length > 0) {
                const diasSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
                blocksData.recorrentes.forEach(r => {
                    const dia = diasSemana[r.dia_semana] || r.dia_semana;
                    let periodo = '';
                    if (r.data_inicio && r.data_fim) {
                        periodo = ` (válido de ${r.data_inicio} até ${r.data_fim})`;
                    } else if (r.data_inicio) {
                        periodo = ` (válido a partir de ${r.data_inicio})`;
                    } else if (r.data_fim) {
                        periodo = ` (válido até ${r.data_fim})`;
                    }
                    html += `
                        <li class="bg-gray-50 p-2 rounded flex justify-between items-center">
                            <span>Recorrente: ${dia}, ${r.hora_inicio} às ${r.hora_fim} – ${r.motivo || 'sem motivo'}${periodo}</span>
                            <button onclick="deleteRecurrentBlock(${r.id})" class="text-red-500 hover:text-red-700">Excluir</button>
                        </li>
                    `;
                });
            }

            if (blocksData.dias?.length === 0 && blocksData.horarios?.length === 0 && blocksData.recorrentes?.length === 0) {
                html += '<p class="text-gray-500">Nenhum bloqueio cadastrado.</p>';
            }

            html += '</ul>';
            listDiv.innerHTML = html;
        } catch (err) {
            console.error('Erro ao carregar bloqueios:', err);
            document.getElementById('blocksList').innerHTML = '<p class="text-red-500">Erro ao carregar bloqueios.</p>';
        }
    }

    // Adicionar as funções de exclusão (se ainda não existirem)
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
            loadBlocks();
        } catch (err) {
            alert('Erro ao excluir bloqueio: ' + err.message);
        }
    };

    window.deleteRecurrentBlock = async function(id) {
        if (!confirm('Tem certeza que deseja excluir este bloqueio recorrente?')) return;
        try {
            await apiFetch(`/bloqueios/recorrente/${id}`, { method: 'DELETE' });
            loadBlocks();
        } catch (err) {
            alert('Erro ao excluir bloqueio recorrente: ' + err.message);
        }
    };

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


    // Formulário: Bloquear período (férias)
    document.getElementById('periodBlockForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            profissional_id: professionalId,
            data_inicio: document.getElementById('periodStart').value,
            data_fim: document.getElementById('periodEnd').value,
            motivo: document.getElementById('periodReason').value
        };
        try {
            await apiFetch('/bloqueios/bloquear-periodo', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            alert('Período bloqueado com sucesso!');
            document.getElementById('periodStart').value = '';
            document.getElementById('periodEnd').value = '';
            document.getElementById('periodReason').value = '';
            // Recarrega a lista de bloqueios (dias) para mostrar os novos dias
            loadBlocks(); // função já existente que recarrega a lista de bloqueios (dias e horários)
        } catch (err) {
            alert('Erro: ' + err.message);
        }
    });

    // Inicializa
    loadProfessionalId();
});