/**
 * admin.js – Lógica comum para todas as páginas administrativas.
 * Verifica se o usuário está autenticado e se é administrador.
 * Redireciona para o dashboard apropriado caso contrário.
 */

document.addEventListener('DOMContentLoaded', async function() {
    // Primeiro, verifica se há token (autenticação básica)
    checkAuth();

    try {
        // Obtém dados do usuário logado
        const user = await apiFetch('/auth/me');
        
        // Se não for admin, redireciona para o dashboard correspondente
        if (user.tipo !== 'admin') {
            redirectByType(); // redireciona para cliente ou profissional
            return; // não executa o resto
        }
        
        // Se for admin, a página pode carregar normalmente
        console.log('Acesso admin autorizado para:', user.email);
        
    } catch (err) {
        console.error('Erro ao verificar permissões de admin:', err);
        // Se houver erro (ex: token expirado), o apiFetch já redireciona para login
        // Mas podemos garantir:
        logout();
    }
});