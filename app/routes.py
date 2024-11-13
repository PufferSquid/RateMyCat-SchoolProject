from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from app.models import User
from app import db


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            session['user_id'] = user.id
            return redirect(url_for('main.cat_rating'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
    
    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        new_user = User(username=username, password=password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception:
            flash('Username already exists! Please choose a different one.', 'danger')
            db.session.rollback()
    
    return render_template('register.html')


@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))


@main.route('/cat_rating', methods=["GET"])
def cat_rating():
    if 'user_id' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('main.login'))
    
    data = get_cat_image_data()
    #vote_data = get_cat_vote_data(image_data[0]["id"])
    #data = get_cat_data()
    return render_template('catRanking.html', data=data)


@main.route('/cat_image_data', methods=['GET'])
def get_cat_image_data():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    return data


API_KEY : str = "live_M03wyBxpvJs4NwwVqhUWBGgqijLWLXtdX8QpqWtYfVQ0U4cp30HyRwn5tMyZdtmF"


@main.route('/cat_data', methods=['GET'])
def get_cat_data():

    image_data = get_cat_image_data()

    print(image_data[0]['id'])

    headers = {
        'Content-Type' : 'application/json',
        'x-api-key' : API_KEY
    }
    print(headers['x-api-key'])

    _id = image_data[0]['id']
    url = f"https://api.thecatapi.com/v1/votes/{_id}"

    try:
        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return {'error': 'Failed to fetch data'}, response.status_code
        
        data = response.json()
        print(data)
        print(response)
        return data
    except Exception:
        print(Exception)

    return data