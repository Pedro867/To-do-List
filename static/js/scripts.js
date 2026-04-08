window.toggleTarefaConcluida =  function (tarefaId) {
    fetch(`/tarefa/concluir_tarefa/${tarefaId}`, { method: 'PUT' })
        .then(response => {
            if (response.ok) {
                const container = document.getElementById(`tarefa-container-${tarefaId}`);
                container.classList.toggle('text-decoration-line-through');
                container.classList.toggle('text-muted');
            }
        })
}

window.deletarTarefa = async function (id) {
    if (!confirm("Deseja realmente excluir esta tarefa?")) return;

    const response = await fetch(`/tarefa/${id}`, { method: 'DELETE' });

    if (response.ok) {
        const result = await response.json();
        window.location.href = result.url;
    } else {
        alert("Erro ao editar");
    }
}

window.prepararEditTarefa = function (id, nome, prio) {
    document.getElementById('editNome').value           = nome;
    document.getElementById('editPrio').value           = prio;
    document.getElementById('editForm').dataset.idAtual = id;
}

document.getElementById('editForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const id = form.dataset.idAtual;
    const formData = new FormData(form);
    const response = await fetch(`/tarefa/${id}`, {
        method: 'PUT',
        body: formData
    });

    if (response.ok) {
        const result = await response.json();
        window.location.href = result.url;
    } else {
        alert("Erro ao editar");
    }
});