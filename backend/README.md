# Backend - Full Stack Trivia API

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


#

# API Reference

Since we are the author of our API, it is only appropriate that well written guide is given to enable the client side development team make better use of it.

The API reference is not exhaustive as more features will be added to it from time to time. This reference document contains the request and response body of our API.


### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.


### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 



### Endpoints 
#### GET /categories
- General:
    - Fetches a json response of categories in which the keys are the ids and the value is the corresponding string of the category, a success flag and the total number of categories.
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.  
- Sample: `curl http://127.0.0.1:5000/categories`



```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}

```


The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 


### Endpoints 
#### GET /questions
- General:
    - Returns a list of question objects, a dictionary of categories, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`



```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    
  ],
  "success": true,
  "total_questions": 12
}
```


#### POST /questions
- General:
    - Creates a new question using the submitted title, author and rating. Returns the id of the created question id, success value, status code, total questions, and question list based on current page number to update the frontend. 

    - Also implements search via  a POST request of a given `serachTerm`.

- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who discovered penicillin?", "answer":"Alexander Fleming", "category":"5", "difficulty":"2"}'`



```json
// Response received from Creating a new question
{
    "success": true,
    "status_code": 200,
    "created": 13,
    "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },

    
  ],
    "total_questions": 13
}

// Response received from search Post request

{
  "success": true,
  "search_term": "Whose autobiography is ...", 
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },

    
  ],
  "total_questions": 13,

}


// questions obj list becomes an empty list if questions do match query 


{
  "success": True,
  "search_term": "Not available search", 
  "questions": [],
  "total_questions": 13,

}


```


#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/questions/11`



```json
{
  "deleted": 9,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
  
  ],
  "success": true,
  "total_questions": 11
}
```


#### POST /quizzes
- General:
    - Guess what, you can actually play a game :[rocket]:
       - This game accepts a request body comprising of a quiz category and a list to track previous or answered questions by id.
        - Firstly, a quiz_category object is selected
       - At each click the previous question list must be updated with previous question id. We do this to keep track.

    - The request and response bodies expressed below:



```json

// Expected Request Body 
{
  "previous_questions": [1, 4, 7], //
  "quiz_category": {"id": "3", "type": "Geography"}
}


// Expected Response Body
{
  "success": true,
  "question": [], 
  "category": "Geography",
  "total_quiz_in_category": 6
}

```






























