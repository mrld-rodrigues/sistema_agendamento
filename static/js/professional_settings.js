/**
 * professional-settings.js – Edição do perfil do profissional.
 * Carrega os dados atuais e permite atualização via PUT.
 */

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();

    let professionalId = null;

    /**
     * Carrega os dados do profissional logado e preenche o formulário.
     */
    async function loadProfessionalData() {
        try {
            const user = await apiFetch('/auth/me');
            if (user.tipo !== 'profissional') {
                window.location.href = '/auth/login';
                return;
            }
            professionalId = user.profissional_id;
            // Busca os dados completos do profissional
            const prof = await apiFetch(`/profissionais/${professionalId}`);
            document.getElementById('name').value = prof.nome;
            document.getElementById('email').value = prof.email || '';
            document.getElementById('phone').value = prof.telefone || '';
            document.getElementById('buffer').value = prof.intervalo_minutos;
        } catch (err) {
            console.error('Erro ao carregar dados do profissional:', err);
            logout();
        }
    }

    /**
     * Envia as alterações do perfil via PUT /profissionais/{id}.
     */
    document.getElementById('profileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            nome: document.getElementById('name').value,
            email: document.getElementById('email').value,
            telefone: document.getElementById('phone').value,
            intervalo_minutos: parseInt(document.getElementById('buffer').value)
        };
        try {
            await apiFetch(`/profissionais/${professionalId}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            alert('Perfil atualizado com sucesso!');
        } catch (err) {
            alert('Erro: ' + err.message);
        }
    });

    loadProfessionalData();
});