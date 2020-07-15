import os
from flask import Flask
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'contact_manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_contacts')
def hello():
    return render_template("contacts.html", contacts=mongo.db.contacts.find())

@app.route('/add_contact')
def add_task():
    contacts = mongo.db.contacts
    contacts.insert_one(request.form.to_dict())
    return redirect(url_for('get_contacts'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)