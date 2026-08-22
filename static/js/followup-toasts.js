const FOLLOWUP_INTERVAL_MS = 15 * 60 * 1000;
const FOLLOWUP_FIRST_DELAY_MS = 3500;
const FOLLOWUP_VISIBLE_MS = 12000;

function getFollowupTasks() {
    const dataElement = document.getElementById('followup-toast-data');
    if (!dataElement) {
        return [];
    }

    try {
        return JSON.parse(dataElement.textContent) || [];
    } catch {
        return [];
    }
}

function pickRandomTask(tasks, lastTaskId) {
    if (tasks.length <= 1) {
        return tasks[0];
    }

    const availableTasks = tasks.filter((task) => task.id !== lastTaskId);
    return availableTasks[Math.floor(Math.random() * availableTasks.length)];
}

function removeFloatingToast(toast) {
    if (!toast) {
        return;
    }

    toast.classList.add('is-leaving');
    window.setTimeout(() => toast.remove(), 220);
}

function showFloatingToast(task) {
    document.querySelectorAll('.floating-followup-toast').forEach(removeFloatingToast);

    const toast = document.createElement('aside');
    toast.className = 'floating-followup-toast';
    if (task.vencida) {
        toast.classList.add('floating-followup-toast-alert');
    } else if (task.venceHoje) {
        toast.classList.add('floating-followup-toast-warning');
    }
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    const closeButton = document.createElement('button');
    closeButton.className = 'floating-followup-close';
    closeButton.type = 'button';
    closeButton.setAttribute('aria-label', 'Fechar lembrete');
    closeButton.textContent = 'x';

    const priority = document.createElement('span');
    priority.textContent = task.prioridade;

    const title = document.createElement('h2');
    title.textContent = task.titulo;

    const meta = document.createElement('p');
    meta.textContent = task.prazo ? `${task.responsavel} - Prazo ${task.prazo}` : task.responsavel;

    const actions = document.createElement('div');
    actions.className = 'floating-followup-actions';

    const link = document.createElement('a');
    link.href = task.url;
    link.textContent = 'Ver tarefa';

    actions.appendChild(link);
    toast.append(closeButton, priority, title, meta, actions);

    document.body.appendChild(toast);
    window.setTimeout(() => toast.classList.add('is-visible'), 20);

    closeButton.addEventListener('click', () => {
        removeFloatingToast(toast);
    });

    window.setTimeout(() => {
        removeFloatingToast(toast);
    }, FOLLOWUP_VISIBLE_MS);
}

document.addEventListener('DOMContentLoaded', () => {
    const tasks = getFollowupTasks();
    if (!tasks.length) {
        return;
    }

    let lastTaskId = null;
    const cycleToast = () => {
        const task = pickRandomTask(tasks, lastTaskId);
        lastTaskId = task.id;
        showFloatingToast(task);
    };

    window.setTimeout(cycleToast, FOLLOWUP_FIRST_DELAY_MS);
    window.setInterval(cycleToast, FOLLOWUP_INTERVAL_MS);
});
