const taskInput = document.getElementById('taskInput');
const addButton = document.getElementById('addBt');
const incompleteList = document.getElementById('incompleteTasks');
const completedList = document.getElementById('completedTasks');

function createTaskElement(task) {
    const li = document.createElement('li');
    li.className = 'task-item';
    if (task.completed) {
        li.classList.add('completed');
    }

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'task-checkbox';
    checkbox.checked = task.completed;
    
    checkbox.addEventListener('change', async function() {
        try {
            const response = await fetch(`/api/tasks/${task.id}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ completed: checkbox.checked })
            });
            if (response.ok) {
                if (checkbox.checked) {
                    completedList.appendChild(li);
                    li.classList.add('completed');
                } else {
                    incompleteList.appendChild(li); 
                    li.classList.remove('completed');
                }
            } else {
                checkbox.checked = !checkbox.checked;
                alert("Failed to update task status.");
            }
        } catch (err) {
            checkbox.checked = !checkbox.checked;
            alert("Error connecting to server.");
        }
    });

    const detailsDiv = document.createElement('div');
    detailsDiv.className = 'task-details';

    const textSpan = document.createElement('span');
    textSpan.innerText = task.text;
    textSpan.className = 'task-text';

    const timeSpan = document.createElement('span');
    timeSpan.innerText = task.created_at ? `Added: ${task.created_at}` : '';
    timeSpan.className = 'task-time';

    detailsDiv.appendChild(textSpan);
    detailsDiv.appendChild(timeSpan);

    const deleteBtn = document.createElement('button');
    deleteBtn.innerHTML = '🗑️'; 
    deleteBtn.className = 'delete-btn';
    
    deleteBtn.addEventListener('click', async function() {
        try {
            const response = await fetch(`/api/tasks/${task.id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                li.remove();
            } else {
                alert("Failed to delete task.");
            }
        } catch (err) {
            alert("Error connecting to server.");
        }
    });

    li.appendChild(checkbox);
    li.appendChild(detailsDiv);
    li.appendChild(deleteBtn);

    return li;
}

async function fetchTasks() {
    try {
        const response = await fetch('/api/tasks');
        if (response.ok) {
            const tasks = await response.json();
            incompleteList.innerHTML = '';
            completedList.innerHTML = '';
            tasks.forEach(task => {
                const element = createTaskElement(task);
                if (task.completed) {
                    completedList.appendChild(element);
                } else {
                    incompleteList.appendChild(element);
                }
            });
        }
    } catch (err) {
        console.error("Failed to load tasks:", err);
    }
}

async function addTask() {
    const taskText = taskInput.value.trim();
    
    if (taskText === "") {
        alert("Please enter a task!");
        return;
    }

    addButton.disabled = true;

    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: taskText })
        });

        if (response.ok) {
            const newTask = await response.json();
            const element = createTaskElement(newTask);
            incompleteList.appendChild(element);
            taskInput.value = "";
        } else {
            const data = await response.json();
            alert(data.error || "Failed to create task.");
        }
    } catch (err) {
        alert("Error connecting to server.");
    } finally {
        addButton.disabled = false;
    }
}

addButton.addEventListener('click', addTask);

taskInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTask();
    }
});

// Load tasks on startup
document.addEventListener('DOMContentLoaded', fetchTasks);