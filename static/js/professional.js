/**
 * professional.js – Lógica do dashboard do profissional.
 * Exibe agenda diária, lista de bloqueios e agenda semanal com agendamentos e bloqueios.
 */

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();

    let currentDate = new Date();
    let professionalId = null;
    let currentWeekStart = getMonday(new Date()); // início da semana atual (segunda-feira)

    // Formata data para exibição no formato DD/MM/YYYY
    function formatDate(date) {
        return date.toLocaleDateString('pt-BR');
    }

    // Formata data para a API (YYYY-MM-DD)
    function formatDateForAPI(date) {
        return date.toISOString().split('T')[0];
    }

    // Formata data abreviada (DD/MM)
    function formatDateShort(date) {
        return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
    }

    // Retorna a segunda-feira da semana de uma determinada data
    function getMonday(date) {
        const d = new Date(date);
        const day = d.getDay(); // 0 = domingo, 1 = segunda, ..., 6 = sábado
        const diff = (day === 0 ? 6 : day - 1); // ajuste para considerar segunda como primeiro dia
        d.setDate(d.getDate() - diff);
        return d;
    }

    // Atualiza o cabeçalho da semana
    function updateWeekRange() {
        const start = currentWeekStart;
        const end = new Date(start);
        end.setDate(start.getDate() + 6);
        document.getElementById('weekRange').textContent = `${formatDateShort(start)} - ${formatDateShort(end)}`;
    }

    /**
     * Carrega os dados do profissional logado via /auth/me.
     */
    async function loadProfessionalData() {
        try {
            const user = await apiFetch('/auth/me');
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
            // Inicializa a agenda semanal
            updateWeekRange();
            await loadWeeklyAppointments();
        } catch (err) {
            console.error('Erro ao carregar dados do profissional:', err);
            logout();
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
     * Carrega todos os bloqueios (dias, horários e recorrentes) e os exibe na seção blocksList.
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

    /**
     * Função global para excluir bloqueios de dia ou horário.
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
            // Recarrega a lista de bloqueios
            loadBlocks();
        } catch (err) {
            alert('Erro ao excluir bloqueio: ' + err.message);
        }
    };

    /**
     * Função global para excluir bloqueio recorrente.
     */
    window.deleteRecurrentBlock = async function(id) {
        if (!confirm('Tem certeza que deseja excluir este bloqueio recorrente?')) return;
        try {
            await apiFetch(`/bloqueios/recorrente/${id}`, { method: 'DELETE' });
            loadBlocks(); // recarrega a lista
        } catch (err) {
            alert('Erro ao excluir bloqueio recorrente: ' + err.message);
        }
    };

    // ==========================================================
    // AGENDA SEMANAL COM AGENDAMENTOS E BLOQUEIOS
    // ==========================================================
    async function loadWeeklyAppointments() {
        if (!professionalId) return;

        const start = currentWeekStart;
        const weekDays = [];
        for (let i = 0; i < 7; i++) {
            const day = new Date(start);
            day.setDate(start.getDate() + i);
            weekDays.push(day);
        }

        // Para filtrar recorrentes ativos, precisamos da lista completa de recorrentes
        let recorrentes = [];
        try {
            const blocksData = await apiFetch(`/profissionais/${professionalId}/bloqueios`);
            recorrentes = blocksData.recorrentes || [];
        } catch (err) {
            console.error('Erro ao carregar bloqueios recorrentes:', err);
        }

        const container = document.getElementById('weeklyAppointments');
        if (!container) {
            console.error('Elemento #weeklyAppointments não encontrado!');
            return;
        }
        container.innerHTML = '';

        for (let day of weekDays) {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'bg-white p-2 rounded shadow';

            // Cabeçalho do dia
            const dayHeader = document.createElement('h3');
            dayHeader.className = 'font-bold text-center mb-2';
            dayHeader.textContent = day.toLocaleDateString('pt-BR', { weekday: 'short', day: 'numeric' });
            dayDiv.appendChild(dayHeader);

            // Container para agendamentos e bloqueios do dia
            const eventsList = document.createElement('div');
            eventsList.className = 'space-y-1';

            // Formata a data manualmente para evitar problemas de fuso horário
            const year = day.getFullYear();
            const month = String(day.getMonth() + 1).padStart(2, '0');
            const dayOfMonth = String(day.getDate()).padStart(2, '0');
            const dateStr = `${year}-${month}-${dayOfMonth}`;

            // 1. Buscar agendamentos do dia
            let appointments = [];
            try {
                appointments = await apiFetch(`/agendamentos?profissional_id=${professionalId}&data=${dateStr}`);
            } catch (err) {
                console.error(`Erro ao buscar agendamentos para ${dateStr}:`, err);
            }

            // 2. Buscar bloqueios pontuais (dias e horários) da data
            let dayBlocks = [];
            try {
                dayBlocks = await apiFetch(`/bloqueios/todos?profissional_id=${professionalId}&data=${dateStr}`);
            } catch (err) {
                console.error(`Erro ao buscar bloqueios para ${dateStr}:`, err);
            }

            // 3. Converter o dia da semana do JavaScript (0=domingo,1=segunda,...,6=sábado)
            //    para o padrão do backend (0=segunda,1=terça,...,6=domingo)
            const jsDay = day.getDay(); // 0=dom, 1=seg, 2=ter, 3=qua, 4=qui, 5=sex, 6=sáb
            const backendDay = jsDay === 0 ? 6 : jsDay - 1; // 0=seg, 1=ter, ..., 5=sáb, 6=dom

            // Filtrar bloqueios recorrentes ativos na data
            const activeRecurrent = recorrentes.filter(r => {
                // Verifica dia da semana (agora usando backendDay)
                if (r.dia_semana !== backendDay) return false;

                // Verifica período de validade (já usando strings YYYY-MM-DD)
                if (r.data_inicio && r.data_inicio > dateStr) return false;
                if (r.data_fim && r.data_fim < dateStr) return false;

                return true;
            });

            // 4. Construir lista de itens para o dia
            const items = [];

            // Verifica se há bloqueio de dia inteiro
            const fullDayBlocks = dayBlocks.filter(b => b.tipo === 'dia');
            if (fullDayBlocks.length > 0) {
                // Pega o primeiro bloqueio (se houver mais de um, mas normalmente só um por dia)
                const block = fullDayBlocks[0];
                const motivo = block.motivo || 'Dia inteiro bloqueado';
                // Define cor baseada no motivo (ex: férias = laranja)
                const cor = block.motivo && block.motivo.toLowerCase().includes('férias') ? 'bg-orange-300' : 'bg-gray-300';
                items.push({
                    type: 'fullday',
                    time: '00:00', // horário fictício para ordenação
                    html: `<div class="text-sm p-1 ${cor} rounded font-bold">🚫 ${motivo}</div>`
                });
            } else {
                // Sem bloqueio de dia inteiro: exibe agendamentos e outros bloqueios
                // Agendamentos
                appointments.forEach(app => {
                    const time = new Date(app.data_hora).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
                    items.push({
                        type: 'appointment',
                        time: time,
                        html: `<div class="text-sm p-1 bg-blue-50 rounded"><span class="font-semibold">${time}</span> - ${app.cliente} - ${app.servico}</div>`
                    });
                });

                // Bloqueios de horário
                dayBlocks.filter(b => b.tipo === 'horario').forEach(b => {
                    items.push({
                        type: 'block',
                        time: b.hora_inicio,
                        html: `<div class="text-sm p-1 bg-red-100 rounded"><span class="font-semibold">${b.hora_inicio} às ${b.hora_fim}</span> – 🔒 ${b.motivo || 'Bloqueio'}</div>`
                    });
                });

                // Bloqueios recorrentes ativos
                activeRecurrent.forEach(r => {
                    items.push({
                        type: 'recurrent',
                        time: r.hora_inicio,
                        html: `<div class="text-sm p-1 bg-yellow-100 rounded"><span class="font-semibold">${r.hora_inicio} às ${r.hora_fim}</span> – 🔁 ${r.motivo || 'Recorrente'}</div>`
                    });
                });
            }

            // Ordenar itens por horário
            items.sort((a, b) => (a.time > b.time ? 1 : -1));

            // Adicionar itens ao eventsList
            if (items.length === 0) {
                eventsList.innerHTML = '<p class="text-gray-400 text-sm">Nenhum</p>';
            } else {
                eventsList.innerHTML = items.map(item => item.html).join('');
            }

            dayDiv.appendChild(eventsList);
            container.appendChild(dayDiv);
        }
    }

    // Eventos dos botões de navegação diária
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

    // Eventos dos botões de navegação semanal
    document.getElementById('prevWeek').addEventListener('click', () => {
        currentWeekStart.setDate(currentWeekStart.getDate() - 7);
        updateWeekRange();
        loadWeeklyAppointments();
    });

    document.getElementById('nextWeek').addEventListener('click', () => {
        currentWeekStart.setDate(currentWeekStart.getDate() + 7);
        updateWeekRange();
        loadWeeklyAppointments();
    });

    // Inicia o processo
    loadProfessionalData();
});