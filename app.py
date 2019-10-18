from pymongo import MongoClient
import os

from datetime import datetime


from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

app.secret_key = 'babyiloveyoubutthatsnotenough'


from bson.objectid import ObjectId


client = MongoClient()
db = client.ContractorProject
purchases = db.purchases
users = db.users

'''
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
'''

'''
@app.route('/account')
def account_details():
    '''show details of user'''
    if users.find_one({"username": session['username'], "password": session['password']}) == None:
        message = 'Please sign in or sign up first'
        return redirect(url_for('signin', message=message))
    else:
        return redirect(url_for('account_details'))
'''


@app.route('/account/<user_id>')
def account_show(user_id):
    """Show a single purchase."""
    account = users.find_one(
        {'_id': ObjectId(user_id)})  # PyMongo add an '_id' field to each oject
    return render_template('purchase_show.html', account=account, user_id=user_id)

'''
@app.route('/signin')
def signin():
    username_attempt = request.form.get('username')
    password_attempt = request.form.get('password')
    if users.find_one({'username': username_attempt, 'password': password_attempt}) == None:
        message = 'incorrect login info.  please try again'
        return render_template('signin.html', message=message)
    else:
        return redirect(url_for('account_details'))
'''


@app.route('/signup')
def signup():
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    new_user = {
        'user_name': request.form.get('username'),
        'password': request.form.get('password'),
        'purchases': []
    }
    '''improve by sking for unique username'''
    user_id = users.insert_one(new_user).inserted_id
    return redirect(url_for('account_show', user_id=user_id))


@app.route('/')
def saag_index():
    """Shows the front page."""
    return render_template('index.html')


@app.route('/why_saag')
def why_saag():
    """Shows the front page."""
    return render_template('why_saag.html')


@app.route('/order')
def order():
    """Shows the order page."""
    return render_template('order.html', purchases={})


@app.route('/cart/<purchase_id>')
def purchase_show(purchase_id):
    """Show a single purchase."""
    purchase = purchases.find_one(
        {'_id': ObjectId(purchase_id)})  # PyMongo add an '_id' field to each oject
    return render_template('purchase_show.html', purchase=purchase, purchase_id=purchase_id)


@app.route('/cart/<purchase_id>', methods=['POST'])
def purchase_update(purchase_id):
    """Edit and submit the edited purchase."""
    updated_purchase = {
        'saag_paneer_number': request.form.get('saag_paneer_number'),
        'saag_tofu_number': request.form.get('saag_tofu_number'),
        'saag_seitan_number': request.form.get('saag_seitan_number'),
        'name': request.form.get('name'),
        'number': request.form.get('number'),
        'phone': request.form.get('phone'),
        'delivery_address': request.form.get('delivery_address'),
        'email': request.form.get('email'),
    }

    purchases.update_one(
        {'_id': ObjectId(purchase_id)},
        {'$set': updated_purchase})
    return redirect(url_for('cart', purchase_list=purchases.find(), purchase_id=purchase_id))


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    """creating new purchase."""
    if request.method == 'POST':
        purchase = {
            'saag_paneer_number': request.form.get('saag_paneer_number'),
            'saag_tofu_number': request.form.get('saag_tofu_number'),
            'saag_seitan_number': request.form.get('saag_seitan_number'),
            'name': request.form.get('name'),
            'number': request.form.get('number'),
            'phone': request.form.get('phone'),
            'delivery_address': request.form.get('delivery_address'),
            'email': request.form.get('email'),
        }
        # print("marco reus")
        print(purchase)
        purchase_id = purchases.insert_one(purchase).inserted_id
        return redirect(url_for('purchase_show', purchase_id=purchase_id))
    if request.method == 'GET':
        purchase_list = purchases.find({})
        return render_template('cart.html', purchase_list=purchase_list)


@app.route('/cart/<purchase_id>/cancel', methods=['POST'])
def purchase_delete(purchase_id):
    """Delete one purchase."""
    purchases.delete_one({'_id': ObjectId(purchase_id)})
    return render_template('cart.html', purchase_list=purchases.find({}), purchase_id=purchase_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
