from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


relationships=db.Table("users_events",
            db.Column('user_id',db.Integer,db.ForeignKey("Users.user_id")),
            db.Column('event_id',db.Integer,db.ForeignKey("Events.event_id"))
)

relationship2=db.Table("events_possibletimes",
            db.Column('event_id',db.Integer,db.ForeignKey("Events.event_id")),
            db.Column('time_id',db.Integer,db.ForeignKey("Times.time_id"))
)
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    schedule=db.relationship("Event", backref="user", lazy=True,uselist=False)
    rel=db.relationship("Event",secondary=relationships,backref=db.backref("users",lazy='dynamic'))
    def get_id(self):
             return (self.user_id)
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    __tablename__ = "Events"
    event_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(256))
    start = db.Column(db.String(256))
    end = db.Column(db.String(256))
    schedule_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    rel=db.relationship("Times",secondary=relationship2,backref=db.backref("events",lazy='dynamic'))
    def __repr__(self):
        return '<Event {}>'.format(self.id)

class Times(db.Model):
    __tablename__ = "Times"
    time_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)
    
    
