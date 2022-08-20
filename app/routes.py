from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, SignUpForm, LoginForm
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"Welcome back {user.username}!", "success")
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/view')
@login_required
def view():
    addresses = Address.query.filter_by(user_id=current_user.id)
    return render_template('view.html', addresses=addresses)

@app.route('/register',  methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated!')
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        new_address = Address(name=name, phone_number=phone_number, address=address, user_id=current_user.id)
        print(f"{new_address.name} has been created.")
        return redirect(url_for('view'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    address_to_edit = Address.query.get_or_404(id)
    if address_to_edit.book_user != current_user:
        flash('You do not have permission to edit this contact.', 'danger')
        return redirect(url_for('index', id=id))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        address_to_edit.update(name=name, phone_number=phone_number, address=address)
        flash(f"{address_to_edit.name} has been updated.", 'success')
        return redirect(url_for('view', id=id))
    return render_template('edit.html', address=address_to_edit, form=form)

@app.route('/<id>/delete')
@login_required
def delete(id):
    address_to_delete = Address.query.get_or_404(id)
    if address_to_delete.book_user != current_user:
        flash('You do not have permission to delete this contact.', 'danger')
        return redirect(url_for('index'))
    address_to_delete.delete()
    flash(f"{address_to_delete.name} has been deleted from your contacts.", "success")
    return redirect(url_for('view'))