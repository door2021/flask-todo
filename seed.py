from app import create_app, db
from app.models import User, Todo
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # Optional: Clear old data
    # db.drop_all()
    # db.create_all()

# Create users
    user1 = User(
        username="admin",
        email="admin@gmail.com",
        password=generate_password_hash("123456")
    )

    user2 = User(
        username="john",
        email="john@gmail.com",
        password=generate_password_hash("asd12345")
    )

# Add users first (so they get IDs)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

# Create todos with required user_id
    todo1 = Todo(
        title="Learn Flask",
        description="Study Flask with SQLAlchemy",
        completed=False,
        favorite=False,
        priority="high",
        user_id=user1.id
    )

    todo2 = Todo(
        title="Build Project",
        description="Create a full CRUD app",
        completed=False,
        favorite=True,
        priority="medium",
        user_id=user2.id
    )

    db.session.add(todo1)
    db.session.add(todo2)
    db.session.commit()

    print("Database seeded successfully!")