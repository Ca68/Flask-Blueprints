
from flask import render_template, url_for, jsonify
from .import bp as app



@app.route('/users')
def get_users():
    return jsonify({"message": 'This is the home page'})

@app.route('/profile')
def profile():
    logged_in_user = 'Carine'
    return render_template('profile.html', u=logged_in_user) 



@app.route('/contact')
def contact():
    return ("This is the contact page")