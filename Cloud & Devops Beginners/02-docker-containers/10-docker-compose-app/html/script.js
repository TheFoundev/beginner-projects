/**
 * To-Do Counter Application - Frontend JS
 * Fetches data from Flask API (served via Nginx) backed by Redis.
 */

const API_BASE = '/api';

// ─── Fetch Statistics ───────────────────────────────
async function fetchStats() {
  try {
    const res = await fetch(`${API_BASE}/stats`);
    const data = await res.json();

    document.getElementById('visitorCount').textContent = data.visits || 0;
    document.getElementById('redisStatus').textContent = data.online ? 'Online' : 'Offline';
    document.getElementById('todoCount').textContent = data.todos || 0;
  } catch (err) {
    console.error('Failed to fetch stats:', err);
    document.getElementById('redisStatus').textContent = 'Error';
  }
}

// ─── Fetch Todos ────────────────────────────────────
async function fetchTodos() {
  try {
    const res = await fetch(`${API_BASE}/todos`);
    const todos = await res.json();
    const list = document.getElementById('todoList');

    if (todos.length === 0) {
      list.innerHTML = '<p class="empty-msg">No tasks yet. Add one above!</p>';
    } else {
      list.innerHTML = todos.map(todo => `
        <div class="todo-item">
          <span>${todo.task}</span>
          <small>${todo.created_at}</small>
        </div>
      `).join('');
    }
    document.getElementById('todoCount').textContent = todos.length;
  } catch (err) {
    console.error('Failed to fetch todos:', err);
  }
}

// ─── Add Todo ───────────────────────────────────────
const todoForm = document.getElementById('todoForm');
if (todoForm) {
  todoForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const input = document.getElementById('taskInput');
    const task = input.value.trim();

    if (!task) return;

    try {
      await fetch(`${API_BASE}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
      });
      input.value = '';
      fetchTodos();
      fetchStats();
    } catch (err) {
      console.error('Failed to add todo:', err);
    }
  });
}

// ─── Initialize ─────────────────────────────────────
fetchStats();
fetchTodos();

// Refresh stats every 5 seconds
setInterval(fetchStats, 5000);

console.log('To-Do Counter running. Backend: Flask + Redis via Nginx proxy.');
