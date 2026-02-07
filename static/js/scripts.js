window.toggleTarefaConcluida =  function (tarefaId) {
    fetch(`/tarefa/concluir/${tarefaId}`, { method: 'GET' })
        .then(response => {
            if (response.ok) {
                const container = document.getElementById(`tarefa-container-${tarefaId}`);
                container.classList.toggle('text-decoration-line-through');
                container.classList.toggle('text-muted');
            }
        })
}

window.deletarTarefa = function (id) {
    if (!confirm("Deseja realmente excluir esta tarefa?")) return;

    fetch(`/tarefa/del/${id}`, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        });
}

window.prepararEditTarefa = function (id, nome, prio) {
    document.getElementById('editForm').action = `/tarefa/edi/${id}`;
    document.getElementById('editNome').value = nome;
    document.getElementById('editPrio').value = prio;
}