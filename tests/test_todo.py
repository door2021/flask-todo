from app.models import Todo
from app.extensions import db

def test_add_todo(client, app):
    response = client.post("/todo/add", data={
        "title": "Test Todo Title",
        "description": "Test Todo Description"
    })

    assert response.status_code == 302

    with app.app_context():
        todo = Todo.query.first_or_404()
        assert todo is not None
        assert todo.title == "Test Todo Title"
        assert todo.description == "Test Todo Description"

def test_edit_todo(client, app):
    with app.app_context():
        todo = Todo(title="Old Title")
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.post(f"/todo/edit/{todo_id}", data={
        "title": "Updated Title"
    })

    assert response.status_code == 302

    with app.app_context():
        updated = Todo.query.get_or_404(todo_id)
        assert updated.title == "Updated Title"        

def test_delete_todo(client, app):
    with app.app_context():
        todo = Todo(title="Delete Me")
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.post(f"/todo/delete/{todo_id}")
    assert response.status_code == 302

    with app.app_context():
        deleted = Todo.query.get(todo_id)
        assert deleted is None        