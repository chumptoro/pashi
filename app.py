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
    return render_template('order.html')


@app.route('/cart', methods=['POST'])
def cart():
    """creating new purchase."""
    purchase = {
        'saag_paneer_number': request.form.get('saag_paneer_number'),
        'saag_tofu_number': request.form.get('saag_tofu_number'),
        'saag_seitan_number': request.form.get('saag_seitan_number'),
        'name': request.form.get('name'),
        'number': request.form.get('number'),
        'phone': request.form.get('phone'),
        'delivery_address': request.form.get('delivery_address'), }
    print("marco reus")
    print(purchase)
    purchase_id = purchases.insert_one(purchase).inserted_id
    return redirect(url_for('purchase_show.html', purchase_id=purchase_id))


@app.route('/cart/<purchase_id>')
def purchase_show(purchase_id):
    """Show a single purchase."""
    purchase = purchase.find_one(
        {'_id': ObjectId(purchase_id)})  # PyMongo add an '_id' field to each oject
    return render_template('purchase_show.html', purchase=purchase)


'''
@app.route('/cart', methods=['GET'])
def cart():
    purchase_list = purchases.find()
    return render_template('cart.html', purchase_list=purchase_list)
    '''


'''
@app.route('/cart')
def saag_cart():
    """Shows the front page."""
    return render_template('cart.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')


@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one(
        {'_id': ObjectId(playlist_id)})  # PyMongo add an '_id' field to each oject
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)


@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'created_at': datetime.now()
    }
    print(playlist)
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')


@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }

    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))


@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
