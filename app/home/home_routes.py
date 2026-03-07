from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Todo

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def dashboard():
    filter_type = request.args.get('filter', 'all')
    sort_by = request.args.get('sort', 'newest')
    search_query = request.args.get('search', '')
    
    query = Todo.query.filter_by(user_id=current_user.id, deleted=False)
    
    if filter_type == 'favorite':
        query = query.filter_by(favorite=True)
    elif filter_type == 'completed':
        query = query.filter_by(completed=True)
    elif filter_type == 'deleted':
        query = Todo.query.filter_by(user_id=current_user.id, deleted=True)
    
    if search_query:
        query = query.filter(
            db.or_(
                Todo.title.ilike(f'%{search_query}%'),
                Todo.description.ilike(f'%{search_query}%')
            )
        )
    
    if sort_by == 'oldest':
        query = query.order_by(Todo.created_at.asc())
    elif sort_by == 'title':
        query = query.order_by(Todo.title.asc())
    else: 
        query = query.order_by(Todo.created_at.desc())
    
    todos = query.all()
    
    return render_template('home/dashboard.html', todos=todos, active_filter=filter_type)

@home.route('/todos/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium')
    
    if not title or not title.strip():
        flash('Title is required', 'danger')
        return redirect(url_for('home.dashboard'))
    
    todo = Todo(
        title=title.strip(),
        description=description.strip(),
        priority=priority,
        user_id=current_user.id
    )
    
    try:
        db.session.add(todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add todo', 'danger')
    
    return redirect(url_for('home.dashboard'))

@home.route('/todos/update/<int:id>', methods=['POST'])
@login_required
def update_todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        todo.title = request.form.get('title', '').strip()
        todo.description = request.form.get('description', '').strip()
        todo.priority = request.form.get('edit_priority', 'medium')
        todo.completed = request.form.get('completed') == 'on'
        
        db.session.commit()
        flash('Todo updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update todo', 'danger')
    
    return redirect(url_for('home.dashboard'))

@home.route('/todos/delete/<int:id>', methods=['POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        # Soft delete
        todo.deleted = True
        db.session.commit()
        flash('Todo deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete todo', 'danger')
    
    return redirect(url_for('home.dashboard'))

@home.route('/todos/<int:id>/toggle-complete', methods=['POST'])
@login_required
def toggle_complete(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        data = request.get_json()
        if data is None:
            data = {}
        
        todo.completed = data.get('completed', not todo.completed)
        db.session.commit()
        
        return jsonify({'success': True, 'completed': todo.completed})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@home.route('/todos/<int:id>/toggle-favorite', methods=['POST'])
@login_required
def toggle_favorite(id):
    try:
        todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
        
        if not todo:
            return jsonify({
                'success': False, 
                'error': 'Todo not found'
            }), 404
        
        todo.favorite = not todo.favorite
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'favorite': todo.favorite
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error in toggle_favorite: {e}")  # Debug log
        return jsonify({
            'success': False, 
            'error': str(e)
        }), 500