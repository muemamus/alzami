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
def get_contacts():
    return render_template("contacts.html", contacts=mongo.db.contacts.find())

@app.route('/add_contact')
def add_contact():
    return render_template('addcontact.html')

@app.route('/add_contact',methods=['POST'])
def insert_contact():
    contacts = mongo.db.contacts
    contacts.insert_one(request.form.to_dict())
    return redirect(url_for('get_contacts'))

@app.route('/edit_contact/<contact_id>')
def edit_contact(contact_id):
    contact_toedit =  mongo.db.contacts.find_one({"_id": ObjectId(contact_id)})
    return render_template('editcontact.html', contact=contact_toedit)

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

@app.route('/delete_contact/<contact_id>')
def delete_contact(contact_id):
    mongo.db.contacts.remove({'_id': ObjectId(contact_id)})
    return redirect(url_for('get_contacts'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)