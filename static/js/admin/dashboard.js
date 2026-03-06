/**
 * admin/dashboard.js – Carrega as estatísticas e preenche os cards do dashboard.
 */

document.addEventListener('DOMContentLoaded', function() {
    // O admin.js já verificou que o usuário é admin, então podemos carregar os dados.
    loadStats();
});

/**
 * Faz as requisições para cada endpoint de estatísticas e atualiza os elementos HTML.
 */
async function loadStats() {
    try {
        // Agendamentos hoje
        const today = await apiFetch('/admin/status/agendamentos-hoje');
        document.getElementById('todayAppointments').textContent = today.total;

        // Agendamentos no mês
        const month = await apiFetch('/admin/status/agendamentos-mes');
        document.getElementById('monthAppointments').textContent = month.total;

        // Total de clientes
        const clients = await apiFetch('/admin/status/clientes');
        document.getElementById('totalClients').textContent = clients.total;

        // Profissionais ativos
        const professionals = await apiFetch('/admin/status/profissionais');
        document.getElementById('activeProfessionals').textContent = professionals.total;

        // Serviços ativos
        const services = await apiFetch('/admin/status/servicos');
        document.getElementById('activeServices').textContent = services.total;
    } catch (err) {
        console.error('Erro ao carregar estatísticas:', err);
        // Exibir mensagem de erro amigável (pode ser um toast)
        alert('Não foi possível carregar as estatísticas. Tente novamente mais tarde.');
    }
}