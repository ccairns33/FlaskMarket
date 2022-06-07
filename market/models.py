from market import db, bcrypt, login_manager
from flask_login import UserMixin
# MUST INSTALL PIP INSTALL WHEEL AS WELL OR WILL RECIEVE A CIRCULAR IMPORT OR BCRYPT NAME ERROR


# will display an exception without this decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
        # see the owner of specific items, with lazy=true sqlalchemy will not grab all the items in one load

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"${str(self.budget)[:-3]},{str(self.budget)[-3:]}"
        else:
            return f"${self.budget}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        # return true or false if the password is correct


    def __repr__(self):
        return f"Item {self.username}"


# table inside our database
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
        # this is related to the user id field
    def __repr__(self):
        return f"Item {self.name}"
