from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    # This tells SQLAlchemy the database table name.
    __tablename__ = "users"

    # Every user gets a unique ID. primary_key=True makes this the main identifier.
    id = db.Column(db.Integer, primary_key=True)

    # nullable=False means this field is required.
    # unique=True means two users cannot share the same email.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # We store the user's display name separately from their email.
    name = db.Column(db.String(80), nullable=False)

    # Never store raw passwords. This will hold the hashed password instead.
    password_hash = db.Column(db.String(255), nullable=False)

    # Useful later for showing when an account was created.
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def set_password(self, password):
        # Converts a plain password into a secure hash before saving it.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Compares a login password against the stored hash.
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        # This controls what user data we send back in API responses.
        # Notice we do not return password_hash.
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
        }
