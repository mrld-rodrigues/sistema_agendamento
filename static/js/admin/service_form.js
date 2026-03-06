/**
 * service_form.js – Lógica do formulário de criação/edição de serviços.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Extrai o ID da URL no formato /admin/services/5/edit
    const pathParts = window.location.pathname.split('/');
    const servicoId = pathParts.length >= 4 && pathParts[3] !== 'new' ? pathParts[3] : null;

    if (servicoId) {
        document.getElementById('serviceId').value = servicoId;
        carregarDadosServico(servicoId);
    }
});

async function carregarDadosServico(id) {
    try {
        const servico = await apiFetch(`/servicos/${id}`);
        document.getElementById('nome').value = servico.nome || '';
        document.getElementById('descricao').value = servico.descricao || '';
        document.getElementById('duracao').value = servico.duracao_minutos || '';
        document.getElementById('preco').value = servico.preco || '';
        document.getElementById('ativo').value = servico.ativo ? '1' : '0';
    } catch (err) {
        console.error('Erro ao carregar dados do serviço:', err);
        alert('Erro ao carregar dados do serviço.');
    }
}

document.getElementById('serviceForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const servicoId = document.getElementById('serviceId').value;
    const payload = {
        nome: document.getElementById('nome').value,
        descricao: document.getElementById('descricao').value || '',
        duracao_minutos: parseInt(document.getElementById('duracao').value),
        preco: parseFloat(document.getElementById('preco').value),
        ativo: parseInt(document.getElementById('ativo').value) === 1
    };

    try {
        if (servicoId) {
            await apiFetch(`/servicos/${servicoId}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            alert('Serviço atualizado com sucesso!');
        } else {
            await apiFetch('/servicos', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            alert('Serviço criado com sucesso!');
        }
        window.location.href = '/admin/services';
    } catch (err) {
        alert('Erro ao salvar serviço: ' + err.message);
    }
});