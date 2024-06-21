import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs- done
    """
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow - done
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories. - done
    """
    @app.route('/categories', methods=['GET'])
    def get_catagories():
        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        categories_dict = {category.id : category.type for category in categories}

        return jsonify(
            {
                'success': True,
                'categories': categories_dict
            }
        ), 200

    


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=["GET"])
    def get_questions():
        try:
            questions = Question.query.all()
            total_questions = len(questions)
            paginated_questions = paginate_questions(request, selection=questions)

            if(len(paginated_questions)) == 0:
                abort(404)

            categories = Category.query.all()
            categories_dict = {category.id : category.type for category in categories}

            return jsonify(
                {
                    'success': True,
                    'questions': paginated_questions,
                    'totalQuestions': total_questions,
                    'categories': categories_dict
                }
            )
        except Exception as e:
            print(e)
            abort(400)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:id>', methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify(
                {
                    'success': True,
                    'questionDeleted': id
                }
            )
        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=["POST"])
    def add_question():
        body = request.get_json()
        try:
            question=body.get('question')
            answer=body.get('answer')
            difficulty=body.get('difficulty')
            category=body.get('category')
            if(question is None or answer is None or difficulty is None or category is None):
                abort(400)
            #resolving erorr of category
            add_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            add_question.insert()
            
            return jsonify(
                {
                    'success': True
                }, 200
            )
        except:
            abort(400)



    @app.route('/search', methods=["POST"])
    def search_question():
        
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')
            print(search_term)
            if search_term:
                questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()

                if len(questions) ==0:
                    abort(404)
            
                currentQuestions = [question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'questions': currentQuestions,
                    'totalQuestions': len(questions)
                })
            else:
                abort(404)
        except:
            abort(404)
        
            
       


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions', methods=["GET"])
    def get_questions_by_category(id):
        try:
            questions = Question.query.filter(Question.category == id).all()
            if questions == []:
                abort(404)

            return jsonify({
                'success': True,
                'questions': paginate_questions(request, selection=questions),
                'total_questions': len(questions),
                'current_category': id
            })
        except:
            abort(404)
            
    

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=["POST"])
    def get_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', [])
            category = body.get('quiz_category')
            category_id = category['id']
            print(category)

            if category_id:
                questions = Question.query.filter(Question.category == category_id,Question.id.notin_(previous_questions)).all()
                print(questions)
            else:
                questions = Question.query.filter(Question.id.not_in(previous_questions)).all()

            if len(questions) == 0:
                abort(404)

            question = random.choice(questions).format()['question']
            print({
                'success': True,
                'question': question
            })
            return jsonify({
                'success': True,
                'question': question
            })
        except Exception as e:
            print(e)
            abort(404)
        


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    
    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500, "message": "internal server error"}), 500

    return app

