from pymongo import MongoClient
import os

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from bson.objectid import ObjectId


client = MongoClient()
db = client.ContractorProject
purchases = db.purchases


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
    return render_template('purchase_show.html', purchase=purchase,)


@app.route('/cart/<purchase_id>', methods=['POST'])
def purchase_update(purchase_id):
    """Edit and submit the edited purchase."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }

    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/cart', methods=['POST', 'GET'])
def cart_submit():
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
        print("marco reus")
        print(purchase)
        purchase_id = purchases.insert_one(purchase).inserted_id
        return redirect(url_for('purchase_show', purchase_id=purchase_id))
    if request.method == 'GET':
        purchase_list = purchases.find({})
        return render_template('cart.html', purchase_list=purchase_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
