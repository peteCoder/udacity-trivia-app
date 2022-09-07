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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'petertalk', 'localhost:5434', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_get_request_for_all_categories(self):
        response = self.client().get('/categories')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])

    def test_retieve_all_questions(self):
        response = self.client().get('/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['currentCategory'])


    def test_retireved_questions_beyond_a_certain_page(self):
        response = self.client().get('/questions?page=100000')
        data = response.get_json()
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "resource not found")       
        self.assertEqual(data['error'], 404)     

    # def test_delete_questions(self):
    #     response = self.client().delete('/questions/25')
    #     self.assertEqual(response.status_code, 200)

    def test_delete_question_that_does_not_exist(self):
        response = self.client().delete('/questions/100000000000000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertFalse(data['success'])


    def test_add_a_question_to_the_list_with_invalid_input(self):
        # Test if the datatype entered is valid
        response = self.client().post('/questions', json={
            "question": "What's my favourite color ?", 
            "answer": "Blue", 
            "difficulty": 1, 
            "category": "4"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])


    def test_add_a_question_to_the_list_with_invalid_input(self):
        # Test if the datatype entered is invalid
        response = self.client().post('/questions', json={
            "difficulty": "bad word", 
            "category": "bad word"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    def test_get_question_search_with_result(self):
        # Testing if searched questions are found 
        response = self.client().post('/questions', json={'searchTerm': "What boxer's original name is Cassius Clay?"})
        data = json.loads(response.data)
        self.assertEqual(data["search_term"], "What boxer's original name is Cassius Clay?")
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(response.status_code, 200)

    def test_search_not_found(self):
        # Testing if searched questions are not found 
        response = self.client().post('/questions', json={'searchTerm': 'jlskdhsuydiuks'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['questions']) # questions becomes an empty list === []
        self.assertTrue(data['total_questions'])
        self.assertFalse(data['questions'])


    def test_get_questions_by_category(self):
        # Testing if category does exist...
        response = self.client().get('/categories/1/questions')
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(response.status_code, 200)

    def test_get_questions_from_category_that_does_not_exist(self):
        # Testing if category does not exist... 
        response = self.client().get('/categories/100100/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertFalse(data["questions"])
        self.assertTrue(data["success"])


    def test_solve_quiz_questions_belonging_to_a_category(self):
        response = self.client().post(
            '/quizzes', 
            json={
                "previous_questions": [], 
                "quiz_category": {"type": "Geography", "id": "3"}
            }
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)

        self.assertTrue(data["success"])
        self.assertTrue(data["question"])
        self.assertTrue(data["total_quiz_in_category"])
        self.assertTrue(data["category"])
        self.assertEqual(data["category"], "Geography")



    def test_solve_quiz_questions_not_belonging_to_a_category(self):
        response = self.client().post(
            '/quizzes', 
            json={
                "previous_questions": [], 
                "quiz_category": {"type": "click", "id": "0"} # This happens when 'All' is selected
            }
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)

        self.assertTrue(data["success"])
        self.assertFalse(data["question"]) # returns an empty dictionary {} since there is no question in category
        self.assertFalse(data["total_quiz_in_category"]) # returns 0 -- No question in category
        self.assertEqual(data["category"], "click")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()