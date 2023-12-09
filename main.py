from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///persons.db"
# Create the extension
db = SQLAlchemy()
# initialise the app with the extension
db.init_app(app)


##CREATE TABLE
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=False)

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    ##READ ALL RECORDS
    # Construct a query to select from the database. Returns the rows in the database
    result = db.session.execute(db.select(Person).order_by(Person.name))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_persons = result.scalars()
    return render_template("index.html", persons=all_persons)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_person = Person(
            name=request.form["name"],
            phone_number=request.form["phone_number"]
        )
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/editNo", methods=["GET", "POST"])
def editNo():
    if request.method == "POST":
        #UPDATE RECORD
        person_id = request.form["id"]
        person_to_update = db.get_or_404(Person, person_id)
        person_to_update.phone_number = request.form["phone_number"]
        db.session.commit()
        return redirect(url_for('home'))
    person_id = request.args.get('id')
    person_selected = db.get_or_404(Person, person_id)
    return render_template("edit_phoneNo.html", person=person_selected)

@app.route("/editName", methods=["GET", "POST"])
def editName():
    if request.method == "POST":
        #UPDATE RECORD
        person_id = request.form["id"]
        person_to_update = db.get_or_404(Person, person_id)
        person_to_update.name = request.form["name"]
        db.session.commit()
        return redirect(url_for('home'))
    person_id = request.args.get('id')
    person_selected = db.get_or_404(Person, person_id)
    return render_template("edit_name.html", person=person_selected)


@app.route("/delete")
def delete():
    person_id = request.args.get('id')
    # DELETE A RECORD BY ID
    person_to_delete = db.get_or_404(Person, person_id)
    # Alternative way to select the person to delete.
    # person_to_delete = db.session.execute(db.select(Person).where(Person.id == person_id)).scalar()
    db.session.delete(person_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

