from datetime import datetime
from src import db

class AlumniLogoSelection(db.Model):
    __tablename__ = "alumni_logo_selection"

    id = db.Column(db.Integer, primary_key=True)
    enroll_number = db.Column(db.String(50), nullable=False, unique=True)
    selected_logo = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "enrollNumber": self.enroll_number,
            "selectedLogo": self.selected_logo
        }
