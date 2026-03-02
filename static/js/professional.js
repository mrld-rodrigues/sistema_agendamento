/**
 * professional.js – Lógica do dashboard do profissional.
 * Exibe a agenda diária com navegação entre dias.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Verifica autenticação (se não houver token, redireciona para login)
    checkAuth();

    let currentDate = new Date();        // data atual (inicia com hoje)
    let professionalId = null;           // será preenchido após carregar usuário

    // Formata data para exibição no formato DD/MM/YYYY
    function formatDate(date) {
        return date.toLocaleDateString('pt-BR');
    }

    // Formata data para a API (YYYY-MM-DD)
    function formatDateForAPI(date) {
        return date.toISOString().split('T')[0];
    }

    /**
     * Carrega os dados do profissional logado via /auth/me.
     * Obtém o professional_id e inicia o carregamento dos agendamentos.
     */
    async function loadProfessionalData() {
        try {
            const user = await apiFetch('/auth/me');
            // Verifica se o tipo é realmente profissional (segurança)
            if (user.tipo !== 'profissional') {
                window.location.href = '/auth/login';
                return;
            }
            professionalId = user.profissional_id;
            // Atualiza a data no cabeçalho
            document.getElementById('currentDate').textContent = formatDate(currentDate);
            // Carrega os agendamentos do dia
            await loadAppointments();
            // Carrega os bloqueios do profissional
            await loadBlocks();
        } catch (err) {
            console.error('Erro ao carregar dados do profissional:', err);
            logout(); // em caso de erro, faz logout
        }
    }

    /**
     * Busca os agendamentos do profissional para a data atual e os exibe.
     */
    async function loadAppointments() {
        if (!professionalId) return;
        const dateStr = formatDateForAPI(currentDate);
        try {
            const appointments = await apiFetch(`/agendamentos?profissional_id=${professionalId}&data=${dateStr}`);
            const listDiv = document.getElementById('appointmentsList');
            if (appointments.length === 0) {
                listDiv.innerHTML = '<p class="text-gray-500">Nenhum agendamento para este dia.</p>';
            } else {
                let html = '';
                appointments.forEach(app => {
                    // Converte a data/hora para exibir apenas o horário
                    const time = new Date(app.data_hora).toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                    html += `
                        <div class="bg-white p-3 rounded shadow flex justify-between items-center">
                            <div>
                                <span class="font-bold">${time}</span> - ${app.cliente} - ${app.servico}
                            </div>
                        </div>
                    `;
                });
                listDiv.innerHTML = html;
            }
        } catch (err) {
            console.error('Erro ao carregar agendamentos:', err);
        }
    }


    /**
 * Carrega todos os bloqueios do profissional e os exibe na seção blocksList.
 */
    async function loadBlocks() {
        if (!professionalId) return;
        try {
            const blocksData = await apiFetch(`/profissionais/${professionalId}/bloqueios`);
            const listDiv = document.getElementById('blocksList');
            if (!listDiv) return;

            let html = '';

            // Dias bloqueados
            if (blocksData.dias && blocksData.dias.length > 0) {
                html += '<h3 class="font-semibold mt-2">Dias inteiros:</h3><ul class="list-disc pl-5">';
                blocksData.dias.forEach(d => {
                    html += `<li>${d.data} – ${d.motivo || 'sem motivo'}</li>`;
                });
                html += '</ul>';
            }

            // Horários bloqueados
            if (blocksData.horarios && blocksData.horarios.length > 0) {
                html += '<h3 class="font-semibold mt-4">Horários específicos:</h3><ul class="list-disc pl-5">';
                blocksData.horarios.forEach(h => {
                    html += `<li>${h.data} ${h.hora_inicio} às ${h.hora_fim} – ${h.motivo || 'sem motivo'}</li>`;
                });
                html += '</ul>';
            }

            // Bloqueios recorrentes
            if (blocksData.recorrentes && blocksData.recorrentes.length > 0) {
                html += '<h3 class="font-semibold mt-4">Recorrentes:</h3><ul class="list-disc pl-5">';
                blocksData.recorrentes.forEach(r => {
                    const diasSemana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
                    const dia = diasSemana[r.dia_semana] || r.dia_semana;
                    let periodo = '';
                    if (r.data_inicio && r.data_fim) {
                        periodo = ` (válido de ${r.data_inicio} até ${r.data_fim})`;
                    } else if (r.data_inicio) {
                        periodo = ` (válido a partir de ${r.data_inicio})`;
                    } else if (r.data_fim) {
                        periodo = ` (válido até ${r.data_fim})`;
                    }
                    html += `<li>${dia}, ${r.hora_inicio} às ${r.hora_fim} – ${r.motivo || 'sem motivo'}${periodo}</li>`;
                });
                html += '</ul>';
            }

            if (html === '') {
                html = '<p class="text-gray-500">Nenhum bloqueio cadastrado.</p>';
            }

            listDiv.innerHTML = html;
        } catch (err) {
            console.error('Erro ao carregar bloqueios:', err);
            document.getElementById('blocksList').innerHTML = '<p class="text-red-500">Erro ao carregar bloqueios.</p>';
        }
    }

    // Eventos dos botões de navegação
    document.getElementById('prevDay').addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() - 1);
        document.getElementById('currentDate').textContent = formatDate(currentDate);
        loadAppointments();
    });

    document.getElementById('nextDay').addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() + 1);
        document.getElementById('currentDate').textContent = formatDate(currentDate);
        loadAppointments();
    });

    // Inicia o processo
    loadProfessionalData();
});