import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format(
        #     "localhost:5432", self.database_name
        # )
        self.database_path = "postgres://postgres:postgres@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # variables to check database contents
        self.categories = len(Category.query.all())
        self.questions = len(Question.query.all())

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test to check "/categories" route
    # this test also assures that the function "query_all_categories" is working
    def test_get_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data["categories"], dict)
        self.assertEqual(len(data["categories"]), self.categories)

    # test to check "/questions" route
    # this test also assures that the function "paginate_questions" is working
    def test_get_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(data["questions"]), 10)
        self.assertEqual(data["total_questions"], self.questions)
        self.assertEqual(len(data["categories"]), self.categories)
        self.assertEqual(data["current_category"], None)

    # test to check "/questions" [POST] route success case
    def test_create_question_success(self):
        test_question = {
            "question": "test question",
            "answer": "test answer",
            "difficulty": 3,
            "category": 3,
        }
        response = self.client().post(
            "/questions",
            data=json.dumps(test_question),
            content_type="application/json",
        )
        data = json.loads(response.data)
        questions = len(Category.query.all())

        self.assertEqual(response.status_code, 200)

    # test to check "/questions" [POST] route fail case
    def test_create_question_fail(self):
        test_question = {
            "question": "test question",
            "answer": None,
            "difficulty": 3,
            "category": 3,
        }
        response = self.client().post(
            "/questions",
            data=json.dumps(test_question),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    # test to check "/questions/<int:id>" [DELETE] route success case
    def test_delete_question_success(self):
        # existing question id
        question = Question.query.filter_by(question="test question").first()
        question_id = question.id
        response = self.client().delete(f"/questions/{question_id}")
        self.assertEqual(response.status_code, 200)

    # test to check "/questions/<int:id>" [DELETE] route fail case
    def test_delete_question_fail(self):
        # non existing question id
        question_id = 9001
        response = self.client().delete(f"/questions/{question_id}")
        self.assertEqual(response.status_code, 404)

    # test to check "/questions/search" [POST] route
    def test_search_questions(self):
        search_term = {"searchTerm": "Hematology"}
        response = self.client().post(
            "/questions/search",
            data=json.dumps(search_term),
            content_type="application/json",
        )
        data = json.loads(response.data)
        self.assertIsInstance(data["questions"], list)
        self.assertEqual(data["total_questions"], 1)

    # test to check "/categories/<int:id>/questions" route succes case
    def test_get_category_questions_success(self):
        category_id = 1
        response = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data["questions"], list)
        self.assertEqual(data["total_questions"], 3)
        self.assertEqual(data["current_category"], category_id)
        for question in data["questions"]:
            self.assertEqual(question["category"], category_id)

    # test to check "/categories/<int:id>/questions" route fail case
    def test_get_category_questions_fail(self):
        category_id = 9001
        response = self.client().get(f"/categories/{category_id}/questions")
        self.assertEqual(response.status_code, 404)

    # test to check "/quizzes" [POST] route
    def test_get_quiz_questions(self):
        test_data = {
            "previous_questions": [1, 2, 3, 4],
            "quiz_category": {"id": 1, "type": "Science"},
        }
        response = self.client().post(
            "/quizzes", data=json.dumps(test_data), content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(data["question"]["id"], test_data["previous_questions"])
        self.assertEqual(data["question"]["category"], test_data["quiz_category"]["id"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
