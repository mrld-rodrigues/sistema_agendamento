/**
 * Arquivo: api.js
 * Descrição: Contém funções utilitárias para comunicação com a API backend.
 *            Inclui tratamento de autenticação via token JWT armazenado no localStorage.
 */

// Base da API. Como o frontend está servido pelo mesmo domínio/porta que o backend,
// podemos usar caminhos relativos (ex: '/auth/login'). Deixamos vazio para usar a mesma origem.
const API_BASE = '';

/**
 * Função genérica para fazer requisições à API com autenticação.
 * @param {string} endpoint - Caminho do endpoint (ex: '/auth/login')
 * @param {object} options - Opções do fetch (method, body, headers, etc)
 * @returns {Promise<object>} - Resposta da API já convertida em JSON
 * @throws {Error} - Lança erro com mensagem da API ou mensagem genérica
 */
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };
    const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    const data = await response.json();
    
    if (!response.ok) {
        // Se for erro 401 (não autorizado), faz logout automático
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('tipo');
            window.location.href = '/auth/login';
            throw new Error('Sessão expirada. Faça login novamente.');
        }
        throw new Error(data.erro || 'Erro na requisição');
    }
    return data;
}

/**
 * Realiza login do usuário.
 * @param {string} email - Email do usuário
 * @param {string} senha - Senha do usuário
 * @returns {Promise<object>} - Dados da resposta (token e tipo)
 */
async function login(email, senha) {
    const data = await apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, senha })
    });
    // Armazena token e tipo no localStorage para uso posterior
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('tipo', data.tipo);
    return data;
}

/**
 * Faz logout removendo token e tipo do localStorage e redireciona para login.
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('tipo');
    window.location.href = '/auth/login';
}

/**
 * Verifica se o usuário está autenticado (token presente). Se não, redireciona para login.
 * Deve ser chamado no início de páginas que exigem autenticação.
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/auth/login';
    }
}

/**
 * Redireciona o usuário para o dashboard apropriado baseado no seu tipo.
 * Útil após login.
 */
function redirectByType() {
    const tipo = localStorage.getItem('tipo');
    if (tipo === 'cliente') window.location.href = '/client/dashboard';
    else if (tipo === 'profissional') window.location.href = '/professional/dashboard';
    else if (tipo === 'admin') window.location.href = '/admin/dashboard';
    else window.location.href = '/auth/login'; // fallback
}