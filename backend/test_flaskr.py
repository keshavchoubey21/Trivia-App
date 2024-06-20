import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
    #     """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'hazard', 'localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:hazard@localhost:5432/trivia_test"
        })

        self.client = self.app.test_client
    # def setUp(self):
    #     """Define test variables and initialize app."""
    #     self.app = create_app()
    #     self.client = self.app.test_client
    #     self.database_name = "trivia_test"
    #     self.database_path = "postgresql://postgres:hazard@localhost:5432/trivia_test"
        # setup_db(self.app, self.database_path)

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"]))
    
    def test_404_error_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # todo
    def test_delete_question(self):
        res = self.client().delete("/questions/4")
        data = json.loads(res.data)

        book = Question.query.filter(Question.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_error_if_question_not_found(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_search_question(self):
        search = {'searchTerm': 'What is', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 6)

    # todo
    def test_404_error_search_question(self):
        search = {'searchTerm': 'no match found', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_add_question(self):
        new_question = {"question": "new question", "answer": "answer1", "category": 1, "difficulty": 1}
        res = self.client().post('/questions', json=new_question)
        self.assertEqual(res.status_code, 200)

    def test_400_error_add_question(self):
        new_question = {"question": "2+2=?", "answer": 4, "category": "ABC", "difficulty": 1}
        res = self.client().post('/questions', json=new_question)
        self.assertEqual(res.status_code, 400)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_error_get_questions_by_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={"quiz_category": 1, "previous_questions": 5})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()