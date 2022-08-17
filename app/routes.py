from app import app
from flask import render_template
from app.forms import RegisterForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated!')
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        new_user = User(name=name, phone_number=phone_number, address=address)
        print(f"{new_user.name} has been created.")
    return render_template('register.html', form=form)