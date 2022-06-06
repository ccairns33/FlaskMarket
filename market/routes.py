from market import app
from market.models import Item, User
from flask import flash, redirect, render_template, url_for, flash
from market.forms import RegisterForm

# no . property bc it is in init file
from market import db
@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)

@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    # if user has clicked on submit btn
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                             email=form.email_address.data,
                             password=form.password1.data)
                            #  line of code goes to User's password.setter
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are errors from validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category="danger")

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    return render_template("login.html")     