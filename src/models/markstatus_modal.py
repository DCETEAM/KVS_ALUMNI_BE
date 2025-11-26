from src import db
from datetime import datetime

class MarkStatus(db.Model):
    __tablename__ = "mark_status"

    id = db.Column(db.Integer, primary_key=True)
    enrollNumber = db.Column(db.String(10), nullable=False)
    markType = db.Column(db.String(20), nullable=False)   # Entry / Food / KitBag
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "enrollNumber": self.enrollNumber,
            "markType": self.markType,
            "timestamp": self.timestamp.isoformat()
        }
