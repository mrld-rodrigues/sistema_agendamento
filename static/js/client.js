/**
 * client.js - Client dashboard logic
 */

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();

    async function loadAppointments() {
        const div = document.getElementById('appointments');
        if (!div) {
            console.error('Element #appointments not found');
            return;
        }

        try {
            const appointments = await apiFetch('/clientes/me/appointments');
            if (appointments.length === 0) {
                div.innerHTML = '<p class="text-gray-500">You have no appointments yet.</p>';
            } else {
                let html = '';
                appointments.forEach(app => {
                    const date = new Date(app.data_hora).toLocaleString('pt-BR');
                    html += `
                        <div class="bg-white p-4 rounded shadow">
                            <p><strong>Date:</strong> ${date}</p>
                            <p><strong>Professional:</strong> ${app.profissional}</p>
                            <p><strong>Service:</strong> ${app.servico} (${app.duracao_minutos} min)</p>
                        </div>
                    `;
                });
                div.innerHTML = html;
            }
        } catch (err) {
            console.error('Error loading appointments:', err);
            div.innerHTML = '<p class="text-red-500">Error loading appointments.</p>';
        }
    }

    const newBtn = document.getElementById('newAppointmentBtn');
    if (newBtn) {
        newBtn.addEventListener('click', () => {
            window.location.href = '/client/new-appointment';
        });
    } else {
        console.error('Button #newAppointmentBtn not found');
    }

    loadAppointments();
});