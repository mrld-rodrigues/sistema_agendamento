/**
 * admin.js – Lógica base para todas as páginas administrativas.
 * 
 * Funções:
 * - checkAdmin(): verifica se o usuário é admin e redireciona se não for.
 * - loadNavbar(): carrega a barra de navegação comum a todas as páginas admin.
 * - logout(): já herdado de api.js, mas mantido para consistência.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Primeiro, verifica se há um token (autenticação básica)
    checkAuth();

    // Em seguida, verifica se o usuário é administrador
    checkAdmin();
});

/**
 * Verifica se o usuário logado é do tipo 'admin'.
 * Se não for, redireciona para o dashboard apropriado (cliente ou profissional).
 * Se for admin, continua o carregamento da página.
 */
async function checkAdmin() {
    try {
        const user = await apiFetch('/auth/me');
        if (user.tipo !== 'admin') {
            // Redireciona para o dashboard correto baseado no tipo
            redirectByType(); // função definida em api.js
        }
        // Se for admin, não faz nada (pode carregar a página)
    } catch (err) {
        console.error('Erro ao verificar tipo de usuário:', err);
        // Em caso de erro (ex: token inválido), faz logout
        logout();
    }
}