async function toggleFavorite(todoId) {
  try {
    const response = await fetch(`/todos/${todoId}/toggle-favorite`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    });

    if (response.ok) {
      const data = await response.json();

      const button = document.querySelector(`button[onclick="toggleFavorite(${todoId})"]`);
      if (button) {
        const icon = button.querySelector('i');
        if (data.favorite) {
          button.classList.add('active');
          icon.classList.remove('bi-star');
          icon.classList.add('bi-star-fill');
        } else {
          button.classList.remove('active');
          icon.classList.remove('bi-star-fill');
          icon.classList.add('bi-star');
        }
      }

    } else {
      const errorData = await response.json().catch(() => ({}));
      console.error('Server error:', errorData);
      showToast('Failed to update favorite', 'error');
    }
  } catch (error) {
    console.error('Error toggling favorite:', error);
    showToast('An error occurred while updating favorite', 'error');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('change', function (e) {
    if (e.target.classList.contains('toggle-complete')) {
      const todoId = e.target.dataset.id;
      const completed = e.target.checked;
      const todoCard = e.target.closest('.todo-card');

      fetch(`/todos/${todoId}/toggle-complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ completed: completed })
      })
        .then(response => {
          if (response.ok) {
            if (completed) {
              todoCard.classList.add('completed');
            } else {
              todoCard.classList.remove('completed');
            }
          } else {
            e.target.checked = !completed;
            showToast('Failed to update todo', 'error');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          e.target.checked = !completed;
          showToast('An error occurred', 'error');
        });
    }
  });


  const deleteBtn = document.getElementById('deleteTodoBtn');
  if (deleteBtn) {
    deleteBtn.addEventListener('click', function () {
      const todoId = document.getElementById('editTodoId').value;
      if (confirm('Are you sure you want to delete this todo?')) {
        window.location.href = `/todos/delete/${todoId}`;
      }
    });
  }
});

function openEditModal(id, title, description, completed, priority = 'medium') {

  const decodeHtml = (html) => {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
  };

  document.getElementById('editTodoId').value = id;
  document.getElementById('editTitle').value = decodeHtml(title);
  document.getElementById('editDescription').value = decodeHtml(description);
  document.getElementById('editCompleted').checked = completed;

  const priorityRadios = document.querySelectorAll('input[name="edit_priority"]');
  priorityRadios.forEach(radio => {
    radio.checked = (radio.value === priority);
  });

  document.getElementById('editTodoForm').action = `/todos/update/${id}`;

  const modalElement = document.getElementById('editTodoModal');
  const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
  modal.show();
}

function filterTodos(filter) {
  document.querySelectorAll('.sidebar .list-group-item').forEach(item => {
    item.classList.remove('active');
    if (item.getAttribute('onclick')?.includes(filter)) {
      item.classList.add('active');
    }
  });

  window.location.href = `/?filter=${filter}`;
}

function sortTodos(value) {
  if (value) {
    window.location.href = `/?sort=${value}`;
  }
}

let searchTimeout;
document.addEventListener('input', function (e) {
  if (e.target.id === 'searchTodo') {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      const query = e.target.value;
      window.location.href = `/?search=${encodeURIComponent(query)}`;
    }, 500);
  }
});

function getCSRFToken() {
  const metaTag = document.querySelector('meta[name="csrf-token"]');
  if (metaTag) {
    return metaTag.getAttribute('content');
  }

  const cookie = document.cookie.split('; ').find(row => row.startsWith('csrf_token='));
  return cookie ? cookie.split('=')[1] : '';
}

function showToast(message, type = 'info') {
  let toastContainer = document.querySelector('.toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    toastContainer.style.zIndex = '11';
    document.body.appendChild(toastContainer);
  }

  const toastId = 'toast-' + Date.now();
  const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';

  const toastHTML = `
    <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  `;

  toastContainer.insertAdjacentHTML('beforeend', toastHTML);

  const toastElement = document.getElementById(toastId);
  const toast = new bootstrap.Toast(toastElement, { delay: 2000 });
  toast.show();

  toastElement.addEventListener('hidden.bs.toast', function () {
    toastElement.remove();
  });
}

document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 2000);
  });
});