import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import setup_db, Url, Directory
from bookmarkie.auth.auth import requires_auth, AuthError
from werkzeug.exceptions import BadRequest


# Raise error if no query results
def check_query(result):
    if not result:
        abort(404)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # Initialize the database
    setup_db(app)

    # set up CORS, allowing all origins
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """
        Sets access control.
        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    # Welcome home route
    @app.route("/")
    def index():
        return (
            jsonify(
                {
                    "Success": True,
                    "Message": "Welcome to Bookmarkie!, go to [https://github.com/radam9/Bookmarkie] for further instruction on using the API",
                }
            ),
            200,
        )

    # Route to get all bookmarks
    @app.route("/bookmarks")
    @requires_auth("get:bookmarks")
    def get_bookmarks(jwt):
        # Get all bookmarks
        result = Url.query.all()

        # Raise 404 if not bookmarks where found
        check_query(result)

        # Format the bookmarks
        bookmarks = Url.serialize_list(result)

        return jsonify({"bookmarks": bookmarks}), 200

    # Route to get all directories
    @app.route("/directories")
    @requires_auth("get:directories")
    def get_directories(jwt):
        # Get all directories
        result = Directory.query.all()

        # Raise 404 if no directories found
        check_query(result)

        # Format the directories
        directories = Directory.serialize_list(result)

        return jsonify({"directories": directories}), 200

    # Route to get all bookmarks in a given directory id
    @app.route("/directories/<int:id>")
    @requires_auth("get:bookmarks")
    def get_bookmarks_by_directory(jwt, id):
        try:
            # Get all bookmarks in directory with given id
            result = Directory.query.get(id).urls

            # Raise 404 if not bookmarks found
            check_query(result)

            # Format the bookmarks
            bookmarks = Url.serialize_list(result)

            return jsonify({"bookmarks": bookmarks}), 200
        except Exception:
            abort(404)

    # Route to create a bookmark
    @app.route("/bookmarks/create", methods=["POST"])
    @requires_auth("post:bookmarks")
    def create_bookmark(jwt):
        # Attempt to create bookmark
        try:
            # Get request body
            body = request.get_json()
            title = body.get("title", None)
            url = body.get("url", None)
            direcotory_id = body.get("directory_id", None)
            # Create bookmark
            bookmark = Url(title, url, direcotory_id)
            bookmark.insert()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Bookmark ({bookmark.title}) was created successfully!",
                    }
                ),
                200,
            )
        # Raise 400 error if not body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to create a directory
    @app.route("/directories/create", methods=["POST"])
    @requires_auth("post:directories")
    def create_directory(jwt):
        # Attempt to create a directory
        try:
            # Get request body
            body = request.get_json()
            name = body.get("name", None)
            # Create directory
            directory = Directory(name)
            directory.insert()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Directory ({directory.name} was created successfully!)",
                    }
                ),
                200,
            )
        # Raise 400 error if no body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)
        # except Exception as e:
        #     import traceback
        #     traceback.print_exc()
        #     abort(422)

    # Route to modify a bookmark
    @app.route("/bookmarks/<int:id>/modify", methods=["PATCH"])
    @requires_auth("patch:bookmarks")
    def modify_bookmark(jwt, id):
        # Get the bookmark to modify
        bookmark = Url.query.get(id)

        # Raise 404 if bookmark doesn't exit
        check_query(bookmark)

        # Attempt to modify the bookmark
        try:
            # Get request body
            body = request.get_json()
            title = body.get("title", None)
            url = body.get("url", None)
            directory_id = body.get("directory_id", None)

            # Modify bookmark
            if title:
                bookmark.title = title
            if url:
                bookmark.url = url
            if directory_id:
                bookmark.directory_id = directory_id
            bookmark.update()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Bookmark ({bookmark.url}) was modified successfully!",
                    }
                ),
                200,
            )
        # Raise 400 error if no body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to modify a directory
    @app.route("/directories/<int:id>/modify", methods=["PATCH"])
    @requires_auth("patch:directories")
    def modify_directory(jwt, id):
        # Get the directory to modify
        directory = Directory.query.get(id)

        # Raise 404 if directory doesn't exit
        check_query(directory)

        # Attempt to modify the directory
        try:
            # Get request body
            body = request.get_json()
            name = body.get("name", None)
            # Modify directory
            directory.name = name
            directory.update()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The directory ({directory.name}) was modified successfully!",
                    }
                ),
                200,
            )
        # Raise 400 error if no body was provided
        except (AttributeError, BadRequest):
            abort(400)
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to delete a bookmark
    @app.route("/bookmarks/<int:id>/delete", methods=["DELETE"])
    @requires_auth("delete:bookmarks")
    def delete_bookmark(jwt, id):
        # Get the bookmark to delete
        bookmark = Url.query.get(id)
        # Raise 404 if bookmark doesn't exit
        check_query(bookmark)
        # Attempt to delete bookmark
        try:
            bookmark.delete()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Bookmark ({bookmark.url}) was deleted successfully!",
                    }
                ),
                200,
            )
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # Route to delete a directory
    @app.route("/directories/<int:id>/delete", methods=["DELETE"])
    @requires_auth("delete:directories")
    def delete_directory(jwt, id):
        # Get the directory to delete
        directory = Directory.query.get(id)
        # Raise 404 if directory doesn't exit
        check_query(directory)
        # Attempt to delete directory
        try:
            directory.delete()
            return (
                jsonify(
                    {
                        "Success": True,
                        "Message": f"The Directory ({directory.name}) was deleted successfully!",
                    }
                ),
                200,
            )
        # Raise 422 error if not successful
        except Exception:
            abort(422)

    # 400 error handler
    @app.errorhandler(400)
    def resource_not_found(error):
        return (
            jsonify({"Success": False, "Error": 400, "Message": "Bad Request"}),
            400,
        )

    # 401 error handler
    @app.errorhandler(401)
    def resource_not_found(error):
        return (
            jsonify({"Success": False, "Error": 401, "Message": "Unauthorized"}),
            401,
        )

    # 404 error handler
    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({"Success": False, "Error": 404, "Message": "Resource Not Found"}),
            404,
        )

    # 405 error handler
    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"Success": False, "Error": 405, "Message": "Method Not Allowed"}),
            405,
        )

    # 422 error handler
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"Success": False, "Error": 422, "Message": "Unprocessable Entity"}
            ),
            422,
        )

    # AuthError handler
    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
