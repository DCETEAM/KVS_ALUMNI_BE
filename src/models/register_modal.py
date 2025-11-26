from src import db

class Alumni(db.Model):
    __tablename__ = "alumni"

    id = db.Column(db.Integer, primary_key=True)
    enrollNumber = db.Column(db.String(6), unique=True)

    # ---------- PERSONAL DETAILS ----------
    personal_basic = db.Column(db.JSON)            # name, mobile, email, dob, address...
    personal_occupation = db.Column(db.JSON)       # entrepreneur/employed/doctor/student details

    # ---------- EVENT PARTICIPATION ----------
    event_participation = db.Column(db.JSON)

    # ---------- SPORTS ACTIVITY ----------
    sports_activity = db.Column(db.JSON)

    # ---------- BUSINESS (COLLABORATION) ----------
    business = db.Column(db.JSON)

    # ---------- SPONSORSHIP ----------
    sponsorship = db.Column(db.JSON)

    # ---------- FILES ----------
    profileAssetPath = db.Column(db.String(400))  

    def serialize(self):
        """Return clean API-friendly JSON"""
        return {
            "id": self.id,
            "enrollNumber": self.enrollNumber,

            "personalDetails": {
                "basic": self.personal_basic,
                "occupationDetails": self.personal_occupation
            },

            "eventParticipation": self.event_participation,
            "sportsActivity": self.sports_activity,
            "business": self.business,
            "sponsorship": self.sponsorship,

            "profileAssetPath": self.profileAssetPath
        }
