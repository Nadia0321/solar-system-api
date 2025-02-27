from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.planet import Planet

# Post a record
planet_bp = Blueprint("planet_blue_print", __name__, url_prefix="/planets")
@planet_bp.route("", methods=["POST"])
def create_planets():
    try:
        request_body = request.get_json()
        new_planet = Planet.from_dict(request_body)
        db.session.add(new_planet)
        db.session.commit()
        return make_response(jsonify(f"Planet {new_planet.name} successfully created"), 201)
    except(KeyError):
        return make_response(jsonify("Something is wrong!"), 400)

# Get all the records
@planet_bp.route("", methods=["GET"])
def get_all_planets():
    query_params = request.args.get("name")
    if query_params:
        planets = Planet.query.filter_by(title=query_params)
    else:
        planets = Planet.query.all()
    return jsonify([planet.to_dict() for planet in planets])

# Get one record
@planet_bp.route("/<id>", methods=["GET"])
def get_one_planet(id):
    planet = validate_id(Planet, id)
    return planet.to_dict(), 200

# Replace one record
@planet_bp.route("/<planet_id>", methods=["PUT"])
def replace_planet(planet_id):  
    planet = validate_id(Planet, planet_id)
    try:
        request_body = request.get_json()
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.number_of_moons = request_body["number_of_moons"]
        db.session.commit()
        return make_response(jsonify(f"planet #{planet.id} successfully replaced"))
    except(KeyError):
        return make_response(jsonify("incomplete information"), 400)

# Update one record
@planet_bp.route("/<planet_id>", methods=["PATCH"])
def update_planet(planet_id):  
    planet = validate_id(Planet, planet_id)
    request_body = request.get_json()
    flag = False
    if request_body.get("name"):
        flag = True
        planet.name = request_body["name"]
    if request_body.get("description"):
        flag = True
        planet.description = request_body["description"]
    if request_body.get("number_of_moons"):
        flag = True
        planet.number_of_moons = request_body["number_of_moons"]
    db.session.commit()
    if flag:
        return make_response(jsonify(f"planet #{planet.id} successfully updated"))
    else:
        return make_response(jsonify(f"nothing was updated"))

# Delete one record  
@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_id(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()
    return make_response(f"Planet #{planet.id} successfully deleted")

# Helper function
def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message" :f"this is not a valid id: {id}"}, 400))
    
    planet = cls.query.get(id)
    if not planet:
        abort(make_response(f"{cls.__name__} {id} not found!", 404))
    return planet

#============================= ########################################################### Should I delete?
#Part 1 and 2, I didn't know if we should delete this part or not

# class Planet:
#     def __init__(self, id, name, description):
#         self.id = id
#         self.name = name
#         self.description = description

#     def to_dict(self):
#         return {"id": self.id,
#             "name" : self.name,
#             "description": self.description}

# planets = [
#     Planet(1, "Earth", "Solid"),
#     Planet(2, "Mars", "Solid"),
#     Planet(3, "Saturn", "Gas")
# ]

# planet_bp = Blueprint("planet_blue_print", __name__, url_prefix="/planets")
# @planet_bp.route("", methods=["GET"])
# def get_planet():
#     all_planets = []
#     for planet in planets:
#         planet_dic = planet.to_dict()
#         all_planets.append(planet_dic)
#     return jsonify(all_planets)


# @planet_bp.route("/<planet_id>", methods=["GET"])
# def get_one_planet(planet_id):
#     planet = validate_id(planet_id)
#     return planet.to_dict()

# def validate_id(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message":f"id {planet_id} is not valid"}, 400))
#     for planet in planets:
#         if planet.id == id:
#             return planet
#     abort(make_response({"message":f"id {planet_id} not found"}, 404))