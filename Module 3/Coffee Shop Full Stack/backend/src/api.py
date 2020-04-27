import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# Route to get the drinks
@app.route("/drinks")
def get_drinks():
    # Query all drinks from database
    drinks = Drink.query.all()
    # Raise 404 if no drinks where found
    if not drinks:
        abort(404)
    # Format the drinks using .short() method
    final_drinks = [d.short() for d in drinks]
    # Return the drinks reponse
    return jsonify({"success": True, "drinks": final_drinks})


# Route to return the drinks details
# Requires the user to be authorized to "get:drinks-details"
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drink_detail(jwt):
    # Query all drinks from database
    drinks = Drink.query.all()
    # Raise 404 if no drinks where found
    if not drinks:
        abort(404)
    # Format the drinks using .long() method
    final_drinks = [d.long() for d in drinks]
    # Return the drinks reponse
    return jsonify({"success": True, "drinks": final_drinks})


# Route to create drinks
# Requires the user to be authorized to "post:drinks"
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(jwt):
    # Extract title and recipe from request body
    body = request.get_json()
    title = body["title"]
    recipe = json.dumps(body["recipe"])
    # Attempt to create a new drink object
    try:
        drink = Drink(title=title, recipe=recipe)
        # add drink to the database
        drink.insert()
        # Return the drink reponse using the long() method format
        return jsonify({"success": True, "drinks": drink.long()})
    # Raise 422 if drink creation fails
    except Exception:
        abort(422)


# Route to modify a drink
# Requires the user to be authorized to "patch:drinks"
@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def modify_drink(jwt, id):
    # Query the requested drink using ID
    drink = Drink.query.get(id)
    # Raise 404 error if the drink doesn't exist
    if not drink:
        abort(404)
    # Extract title and recipe from the request body
    body = request.get_json()
    title = body.get("title")
    recipe = body.get("recipe", None)
    # Attempt to modify the drink
    try:
        # Modify title if it exists in body
        if title and recipe:
            drink.title = title
        # Modify recipe if it exists in body
        if recipe:
            drink.recipe = json.dumps(recipe)
        # Modify the drink in the database
        drink.update()
        # Return the long() formatted drink as a reponse
        return jsonify({"success": True, "drinks": [drink.long()]})
    # Raise 422 error otherwise
    except Exception:
        abort(422)


# Route to delete a drink
# Requires the user to be authorized to "delete:drinks"
@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(jwt, id):
    # Query the requested drink using ID
    drink = Drink.query.get(id)
    # Raise 404 error if the drink doesn't exist
    if not drink:
        abort(404)
    # Attempt to delete the requested drink
    try:
        # Delete the drink from the database
        drink.delete()
        # Return the ID of the delete drink
        return jsonify({"success": True, "delete": id})
    # Raise 422 error otherwise
    except Exception:
        abort(422)


# 404 Error handler
@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
        404,
    )


# 422 Error handler
@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "Not Processable"}),
        422,
    )


# AuthError handler
@app.errorhandler(AuthError)
def handle_auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
