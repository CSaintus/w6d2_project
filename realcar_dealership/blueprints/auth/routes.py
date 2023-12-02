from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


from realcar_dealership.models import User, db



auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signin', methods=['GET', 'POST'])
def signin():

    register_form = RegisterForm()

    if request.method == 'POST': and register_form.validate_on_submit():
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        print(username, email, password)

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'Please try again', 'danger')
            return redirect('/signin')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect('/signin')
        else:
            new_user = User(first_name, last_name, email, password, username)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/dealer')

        user = User(username, email, password, first_name, last_name)


        db.session.add(user)
        db.session.commit()


        flash('Account created', 'info')
        return redirect('/signin')

    return render_template('sign_up.html', register_form=register_form)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():

    login_form = LoginForm()


    if request.method == 'POST': and loginform.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        print("login info", email, password)

        user = User.query.filter(User.email=email).first()


        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dealer')
        else:
            flash('Invalid Credentials', 'danger')
            return redirect('/signin')

    return render_template('login.html', loginform=login_form)


@auth.route('/signout')
def signout():
    logout_user()
    return redirect('/')