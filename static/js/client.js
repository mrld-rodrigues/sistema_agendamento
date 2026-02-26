/**
 * Arquivo: cliente.js
 * Descrição: Lógica da dashboard do cliente: listar agendamentos, redirecionar para criação.
 */

// Verifica se o usuário está autenticado; se não, redireciona para login.
checkAuth();

/**
 * Carrega e exibe os agendamentos do cliente.
 * Atualmente é um placeholder, pois o backend ainda não possui um endpoint específico.
 * TODO: implementar após criar endpoint GET /clientes/me/agendamentos
 */
async function carregarAgendamentos() {
    const div = document.getElementById('agendamentos');
    // Mensagem temporária enquanto a funcionalidade não está disponível
    div.innerHTML = '<p class="text-gray-500">Funcionalidade em breve: listar seus agendamentos.</p>';
}

// Adiciona evento ao botão "Novo Agendamento" para redirecionar para a página de criação.
document.getElementById('novoAgendamentoBtn').addEventListener('click', () => {
    window.location.href = '/cliente/novo-agendamento';
});

// Executa a função ao carregar a página
carregarAgendamentos();