/**
 * professional_form.js – Lógica do formulário de criação/edição de profissionais
 */

document.addEventListener('DOMContentLoaded', function() {
    // Extrai o ID da URL no formato /admin/professionals/5/edit
    const pathParts = window.location.pathname.split('/');
    // pathParts = ["", "admin", "professionals", "5", "edit"]
    const profissionalId = pathParts.length >= 4 && pathParts[3] !== 'new' ? pathParts[3] : null;

    if (profissionalId) {
        document.getElementById('profissional-id').value = profissionalId;
        carregarDadosProfissional(profissionalId);
    }

    document.getElementById('profissional-form').addEventListener('submit', salvarProfissional);
});

async function carregarDadosProfissional(id) {
    try {
        const profissional = await apiFetch(`/profissionais/${id}`);
        document.getElementById('nome').value = profissional.nome || '';
        document.getElementById('especialidade').value = profissional.especialidade || '';
        document.getElementById('email').value = profissional.email || '';
        document.getElementById('telefone').value = profissional.telefone || '';
        document.getElementById('intervalo').value = profissional.intervalo_minutos || 15;
        document.getElementById('ativo').value = profissional.ativo ? '1' : '0';
    } catch (err) {
        console.error('Erro ao carregar dados do profissional:', err);
        alert('Erro ao carregar dados do profissional.');
    }
}

async function salvarProfissional(e) {
    e.preventDefault();

    const profissionalId = document.getElementById('profissional-id').value;
    const payload = {
        nome: document.getElementById('nome').value,
        especialidade: document.getElementById('especialidade').value,
        email: document.getElementById('email').value || null,
        telefone: document.getElementById('telefone').value || null,
        intervalo_minutos: parseInt(document.getElementById('intervalo').value),
        ativo: parseInt(document.getElementById('ativo').value) === 1
    };

    try {
        if (profissionalId) {
            // Edição: usa PUT /profissionais/{id}
            await apiFetch(`/profissionais/${profissionalId}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            showToast('Profissional atualizado com sucesso!', 'success');
        } else {
            // Criação: inclui senha e usa POST /auth/registro/profissional
            payload.senha = document.getElementById('senha').value;
            await apiFetch('/auth/registro/profissional', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            showToast('Profissional criado com sucesso!', 'success');
        }
        window.location.href = '/admin/professionals';
    } catch (err) {
        showToast('Erro ao salvar profissional: ' + err.message, 'error');
    }
}