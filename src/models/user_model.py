from src import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    refresh_token = db.Column(db.Text)
    refresh_token_created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<User {self.username}>"
