from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

SECRETAPIKEY = "1234"


app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
        "has_sockets": random_cafe.has_sockets,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "id": random_cafe.id,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "map_url": random_cafe.map_url,
        "name": random_cafe.name,
        "seats": random_cafe.seats
    })


@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    dictionary = {
        "cafes": []
    }
    for cafe in all_cafes:
        this_cafe = {
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "id": cafe.id,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "map_url": cafe.map_url,
            "name": cafe.name,
            "seats": cafe.seats
        }
        dictionary["cafes"].append(this_cafe)
    return dictionary


@app.route("/search")
def find_a_cafe():
    loc = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
    all_cafes = result.scalars().all()
    dictionary = {}
    if not all_cafes == []:
        dictionary = {
            "cafes": []
        }
        for cafe in all_cafes:
            this_cafe = {
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price,
                "has_sockets": cafe.has_sockets,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "id": cafe.id,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "map_url": cafe.map_url,
                "name": cafe.name,
                "seats": cafe.seats
            }
            dictionary["cafes"].append(this_cafe)
    else:
        dictionary = {
            "error": {
                "Not Found": "Sorry, we don't have a cafe at that location."
            }
        }
    return dictionary


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    response = {
        "response": {}
    }
    can_take_calls = ""
    has_sockets = ""
    has_toilet = ""
    has_wifi = ""
    if request.form.get("can_take_calls").capitalize() == "True":
        can_take_calls = True
    elif request.form.get("can_take_calls").capitalize() == "False":
        can_take_calls = False
    coffee_price = request.form.get("coffee_price")
    if request.form.get("has_sockets").capitalize() == "True":
        has_sockets = True
    elif request.form.get("has_sockets").capitalize() == "False":
        has_sockets = False
    if request.form.get("has_toilet").capitalize() == "True":
        has_toilet = True
    elif request.form.get("has_toilet").capitalize() == "False":
        has_toilet = False
    if request.form.get("has_wifi").capitalize() == "True":
        has_wifi = True
    elif request.form.get("has_wifi").capitalize() == "False":
        has_wifi = False
    img_url = request.form.get("img_url")
    location = request.form.get("location")
    map_url = request.form.get("map_url")
    name = request.form.get("name")
    seats = request.form.get("seats")

    cafe = Cafe(
        can_take_calls=can_take_calls,
        coffee_price=coffee_price,
        has_sockets=has_sockets,
        has_toilet=has_toilet,
        has_wifi=has_wifi,
        img_url=img_url,
        location=location,
        map_url=map_url,
        name=name,
        seats=seats
    )

    with app.app_context():
        db.session.add(cafe)
        db.session.commit()

    response["response"]["success"] = "Successfully added the new cafe."

    return response


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    updated_price = request.args.get("updated_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    cafe.coffee_price = updated_price
    db.session.commit()
    return jsonify(success='Successfully updated the price.')


@app.errorhandler(404)
def invalid_id(e):
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/cafe-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    if request.args.get("api_key") == SECRETAPIKEY:
        cafe = db.get_or_404(Cafe, cafe_id)
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(success="Successfully deleted the cafe.")
    else:
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."), 403


# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
