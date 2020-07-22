""" 
    The softwares used to develop this software found in requirements.txt

    Procfile file contains command to be run to start the server when
    
    this application is deployed to heroku.

    For further  information about this application refer to README.md
"""

# Core imports 

import os
from flask import Flask
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

"""
 We start the server which is listening on a given Internet Protocol
 Address and bound to a given Port.The server uses MongoDB to store data.
 The IP address ,port and MongoDB connection are exposed as environment
 variables.The data from database is sent to the client as HTML.
 
"""

# Initialise flask application
app = Flask(__name__)

# Getting MONGODB connection 
app.config["MONGO_DBNAME"] = 'contact_manager'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

# Connect our flask application to the database
mongo = PyMongo(app)

""" The server exposes 4 core endpoints that clients e.g browser can use 
    to get, add , update and delete clients contacts
"""

# Endpoint 1
# Getting all the contacts in the database.
@app.route('/')
@app.route('/get_contacts')
def get_contacts():
    return render_template("contacts.html", contacts=mongo.db.contacts.find())


# Endpoint 2
# Add a new contact in the database and redirect to homepage
@app.route('/add_contact',methods=['POST'])
def insert_contact():
    contacts = mongo.db.contacts
    contacts.insert_one(request.form.to_dict())
    return redirect(url_for('get_contacts'))

# Endpoint 3
# Edit an existing contact and redirect to homepage
@app.route('/update_contact/<contact_id>',methods=['POST'])
def update_contact(contact_id):
    contacts = mongo.db.contacts
    contacts.update( {'_id': ObjectId(contact_id)},
    {
        'phonenumber':request.form.get('phonenumber'),
        'firstname':request.form.get('firstname'),
        'lastname': request.form.get('lastname'),
        'email': request.form.get('email')
        
    })
    return redirect(url_for('get_contacts'))

# Endpoint 4
# This endpoint is used to a given contact in the database and redirect to homepage
@app.route('/delete_contact/<contact_id>')
def delete_contact(contact_id):
    mongo.db.contacts.remove({'_id': ObjectId(contact_id)})
    return redirect(url_for('get_contacts'))


""" The following 2 endpoints return both delete and add HTML webapges.
"""

# Webpage used for adding contacts and send request to the server
@app.route('/add_contact')
def add_contact():
    return render_template('addcontact.html')

# Webpage used for editing contacts and send request to the server
@app.route('/edit_contact/<contact_id>')
def edit_contact(contact_id):
    contact_toedit =  mongo.db.contacts.find_one({"_id": ObjectId(contact_id)})
    return render_template('editcontact.html', contact=contact_toedit)

# Server is listening on a given IP address and port
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)