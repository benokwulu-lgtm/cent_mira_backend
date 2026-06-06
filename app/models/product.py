from datetime import datetime, timezone

from app.extensions import db


class Product(db.Model):
    # This will create a "products" table in the database.
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Product name is required because every product needs a display title.
    name = db.Column(db.String(120), nullable=False)

    # Description can be longer, so db.Text is better than db.String.
    description = db.Column(db.Text, nullable=True)

    # For now, we use Float for learning simplicity.
    # Later, we may switch to an integer amount in kobo/cents for better money handling.
    price = db.Column(db.Float, nullable=False)

    # Stock tells us how many units are available.
    stock = db.Column(db.Integer, default=0, nullable=False)

    # Optional image URL for the frontend to display product images.
    image_url = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        # This controls how a product is returned as JSON.
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
        }