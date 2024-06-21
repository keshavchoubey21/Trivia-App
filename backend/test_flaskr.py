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
        database_user = os.getenv('DB_USER', 'postgres')
        database_password = os.getenv('DB_PASSWORD', 'hazard')
        database_host = os.getenv('DB_HOST', '127.0.0.1:5432')
        database_name = os.getenv('DB_NAME', 'trivia_test')
        database_path = 'postgresql://{}:{}@{}/{}'.format(database_user,database_password,database_host, database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": database_path
        })

        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # def test_get_categories(self):
    #     res = self.client().get("/categories")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data['categories'])

    # def test_method_not_allowed_get_categories(self):
    #     res = self.client().post("/categories")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertTrue(data["message"], "Method not allowed")

    # def test_get_questions(self):
    #     res = self.client().get("/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["totalQuestions"])
    #     self.assertTrue(len(data["categories"]))
    
    # def test_404_error_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/questions?page=1000")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "bad request")

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/4")
    #     data = json.loads(res.data)

    #     book = Question.query.filter(Question.id == 4).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)

    # def test_404_error_if_question_not_found(self):
    #     res = self.client().delete("/questions/1000")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_search_question(self):
    #     search = {'searchTerm': 'What is', }
    #     res = self.client().post('/search', json=search)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertEqual(data['totalQuestions'], 2)


    # def test_404_error_search_question(self):
    #     search = {'searchTerm': 'no match found', }
    #     res = self.client().post('/search', json=search)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_add_question(self):
    #     new_question = {"question": "new question", "answer": "answer1", "category": 1, "difficulty": 1}
    #     res = self.client().post('/questions', json=new_question)
    #     self.assertEqual(res.status_code, 200)

    # def test_400_error_add_question(self):
    #     new_question = {"question": "2+2=?", "answer": 4, "category": "ABC", "difficulty": 1}
    #     res = self.client().post('/questions', json=new_question)
    #     self.assertEqual(res.status_code, 400)

    # def test_get_questions_by_category(self):
    #     res = self.client().get('/categories/2/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['current_category'])

    # def test_404_error_get_questions_by_category(self):
    #     res = self.client().get('/categories/100/questions')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions':[],'quiz_category': {'type': 'abc', 'id': 1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_error_get_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions':[],'quiz_category': {'type': 'abc', 'id': 100}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()