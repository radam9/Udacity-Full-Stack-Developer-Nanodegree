import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# function to paginate questions
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# function to query categories
def query_all_categories():
    # query all categories
    category = Category.query.all()
    # format the response
    categories = dict()
    for c in category:
        categories[c.id] = c.type
    return categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers / after response configuration and access control
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # route to handle categories GET requests
    @app.route("/categories")
    def get_categories():
        categories = query_all_categories()
        return jsonify({"categories": categories}), 200

    # route to handle questions GET requests
    @app.route("/questions")
    def get_questions():
        # query all questions
        selection = Question.query.all()
        # paginate questions
        questions = paginate_questions(request, selection)
        # query all categories
        categories = query_all_categories()
        response = {
            "questions": questions,
            "total_questions": len(selection),
            "categories": categories,
            "current_category": None,
        }
        return jsonify(response), 200

    # route to handle question creation POST requests
    @app.route("/questions", methods=["POST"])
    def create_question():
        # get new question details from json body
        json_body = request.get_json()
        question = json_body.get("question", None)
        answer = json_body.get("answer", None)
        category = json_body.get("category", None)
        difficulty = json_body.get("difficulty", None)

        if not (question and answer and category and difficulty):
            abort(400)

        try:
            new_question = Question(question, answer, category, difficulty)
            new_question.insert()
            return jsonify({"message": "new question added successfully"}), 200
        except:
            abort(422)

    # route to handle question deletion GET requests
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        # get question with provided id
        question = Question.query.get(id)
        if question == None:
            abort(404)
        try:
            # delete question and return reponse
            question.delete()
            return (
                jsonify({"message": f"Successfully deleted question with id: {id}"}),
                200,
            )
        except:
            # return error if deletion was unsuccessful
            abort(422)

    # route to handle question searches POST requests
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:
            search = request.json.get("searchTerm", None)
            selection = (
                Question.query.order_by(Question.id)
                .filter(Question.question.ilike("%{}%".format(search)))
                .all()
            )
            questions = paginate_questions(request, selection)
            response = {
                "questions": questions,
                "total_questions": len(selection),
                "current_category": None,
            }
            return jsonify(response), 200
        except:
            abort(422)

    # route to handle questions filtering by category GET requests
    @app.route("/categories/<int:id>/questions")
    def get_category_questions(id):
        categories = [c[0] for c in Category.query.with_entities(Category.id).all()]
        if id not in categories:
            abort(404)
        try:
            # get questions by category id
            selection = Question.query.filter_by(category=id).all()
            questions = paginate_questions(request, selection)
            response = {
                "questions": questions,
                "total_questions": len(selection),
                "current_category": id,
            }
            return jsonify(response), 200
        except:
            abort(422)

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        # get the body of the request
        json_body = request.get_json()
        # list of id for the previously provided questions
        previous_questions = json_body.get("previous_questions")
        category = int(json_body.get("quiz_category")["id"])

        try:
            # get questions with category id & exclude previous question ids
            # if category id = 0 get all categories
            if category == 0:
                question = (
                    Question.query.filter(Question.id.notin_(previous_questions))
                    .order_by(func.random())
                    .first()
                )
                print(question)
            else:
                question = (
                    Question.query.filter_by(category=category)
                    .filter(Question.id.notin_(previous_questions))
                    .order_by(func.random())
                    .first()
                )
                print(question)

            # return empty response if no more questions exist
            if not question:
                return jsonify({})
            return jsonify({"question": question.format()}), 200
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Not Processable"}),
            422,
        )

    return app
