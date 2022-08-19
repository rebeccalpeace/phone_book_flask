from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import RegisterForm, SignUpForm
from app.models import Address, User


@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form has been validated!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated!')
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        new_user = Address(name=name, phone_number=phone_number, address=address)
        print(f"{new_user.name} has been created.")
        return redirect(url_for('index'))
    return render_template('register.html', form=form)