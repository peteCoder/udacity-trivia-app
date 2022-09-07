from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category
import random


QUESTIONS_PER_PAGE = 10



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, response="*")


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization,X-Requested-With,true"
    )
    response.headers.add(
      "Access-Control-Allow-Credentials", 'true'
    )

    response.headers.add(
      "Access-Control-Allow-Methods", "GET,POST,OPTIONS,PUT,DELETE"
    )

    return response



  # This function is meant to paginate questions.
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    list_of_questions = questions[start:end]

    return list_of_questions


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''


  @app.route('/categories')
  def retrieve_categories():
    categories = { category.format()['id'] : category.format()['type'] for category in Category.query.all() }

    return jsonify({
      "categories": categories,
      "success": True,
      "total_categories": len(Category.query.all())
    })



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route("/questions")
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()

    paginated_questions = paginate_questions(request, questions)

    categories = { category.id : category.type for category in Category.query.all() }

    if len(paginated_questions) == 0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(questions),
        'categories': categories, 
        'currentCategory': "Science"
      })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)

      question.delete()

      all_questions = Question.query.order_by(Question.id).all()

      current_questions = paginate_questions(request, all_questions) 

      return jsonify({
        "success": True,
        "deleted": question_id,
        "questions": current_questions,
        "total_questions": len(all_questions)
      })
    except:
      abort(422)

    

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''



  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)


    search_term = body.get('searchTerm', None)

    all_questions = Question.query.order_by(Question.id).all()


    try:

      if search_term:
        # Filter questions by search_term
        questions = Question.query.order_by(Question.id).filter(
          Question.question.ilike(f"%{search_term}%")
        )
  
        current_questions = paginate_questions(request, questions)
        total_questions = len([question.format() for question in all_questions])

        return jsonify({
          "success": True,
          "search_term": search_term, 
          "questions": current_questions,
          "total_questions": total_questions,
          
        })
      else:

        question = Question(
          question=new_question, 
          answer=new_answer, 
          category=new_category, 
          difficulty=new_difficulty
        )

        question.insert()
        
        current_questions = paginate_questions(request, all_questions)

        return jsonify({
          "success": True,
          "status_code": 200,
          "created": question.id,
          "questions": current_questions,
          "total_questions": len(current_questions)
        })
    except:
        abort(400)

  


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_by_category(category_id):
    
    all_questions = [question for question in Question.query.all()]
    questions = Question.query.filter(Question.category == str(category_id)).all()

    current_questions = paginate_questions(request, questions)

    return jsonify({
      "success": True,
      "questions": current_questions,
      "total_questions": len(all_questions),
    })
    


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def solve_quiz_questions():
    body = request.get_json()

    # Expected request body for quiz_category with attributes of type and id of the 
    # requested category  
    # e.g. {'type': 'click', 'id': '1'}
    quiz_category = body.get("quiz_category", None)

    # The first initialization for previous_questions is an empty list []
    # The client is expected to append or push already answered quiz question ids into previous_questions
    previous_questions = body.get("previous_questions", None) 

    

    
    filtered_questions_by_category = Question.query.filter(Question.category == str(quiz_category['id'])).all()

    

    num_of_question_in_category = 0

    new_question_set = []

    if (quiz_category['id']) == 0:
      new_question_set = Question.query.filter(Question.id.not_in(previous_questions)).all()
      num_of_question_in_category =  len([question.format() for question in Question.query.all()]) 

    else:
      new_question_set = Question.query.filter(
        Question.id.not_in(previous_questions), Question.category == str(quiz_category['id'])
      ).all()
      num_of_question_in_category = len([question.format() for question in filtered_questions_by_category]) 


    randomized_question_set = {}
    if new_question_set:
      new_questions_list = [question.format() for question in new_question_set]
      randomized_question_set = random.choice(new_questions_list)

    print({
      "success": True,
      "question": randomized_question_set, 
      "category": quiz_category['type'],
      "total_quiz_in_category": num_of_question_in_category
    })


    return jsonify({
      "success": True,
      "question": randomized_question_set, 
      "category": quiz_category['type'],
      "total_quiz_in_category": num_of_question_in_category
    })




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

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

  @app.errorhandler(400)
  def bad_request(error):
      return (
        jsonify({"success": False, "error": 400, "message": "bad request"}), 
        400,
      )



  return app

    