from market import app
from market.models import Item, User
from flask import flash, redirect, render_template, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchasItemForm
from flask_login import login_user, logout_user, login_required, current_user

# no . property bc it is in init file
from market import db
@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

# user must be logged in to access /market @login_required will redirect to login if user attempts
# login_required is configured in init
# login_manager.login_view = "login_page"
    # makes @login_required functional

@app.route('/market', methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchasItemForm()
    if request.method == "POST":
        purchased_item = request.form.get("purchase_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            # current logged in user
            p_item_object.owner = current_user.id
            # updating budget
            current_user.budget = current_user.budget - p_item_object.price
            # saving db
            db.session.commit()


    items = Item.query.all()
    return render_template("market.html", items=items, purchase_form=purchase_form)

@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    # if user has clicked on submit btn
    # from Flask_wtf package, which froms inherti from FlaskForm
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                             email=form.email_address.data,
                             password=form.password1.data)
                            #  line of code goes to User's password.setter
        db.session.add(user_to_create)
        db.session.commit()

        # flash success message and login the new user
        # login user from flask_login
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are errors from validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category="danger")

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # validates if all info is valid and if user clicked on submit
        attempted_user = User.query.filter_by(username=form.username.data).first()
        print(attempted_user)
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # user exists, check if the password matches from the database unhashed using method from User class
            # use login_user function and print success
            login_user(attempted_user)
            flash(f"Success! You have logged in as {attempted_user.username}", category="success")
            # flask_login has built in functions like current_user
            return redirect(url_for('market_page'))
        else:
            flash(f"The username or password is not correct.", category="danger")
    if form.errors != {}: #if there are errors from validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category="danger")

    return render_template("login.html", form=form)

@app.route('/logout')
def logout_page():
    # built in flask_login function
    logout_user()
    # after logout, display alert
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
