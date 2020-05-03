# Full Stack Trivia API Project

Trivia is a game base project that lets the user test their knowledge by answering trivia questions in different categories.
The project is composed of a backend and a frontend. The backend is an API based web server built using [Flask and Flask CORS], while the frontend is built using [React and Javascript].
The main tasks and goals of the project are as follows:
1.  Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2.  Delete questions.
3.  Add questions and require that they include question and answer text.
4.  Search for questions based on a text query string.
5.  Play the quiz game, randomizing either all questions or within a specific category.

## Getting started

### Dependencies
To run this project you need the following dependencies installed:

 - Python 3.7
 - pip
 - node.js
 - npm

### Frontend dependencies
For details regarding the fronend dependencies check the frontend README.md in the fronend directory.

### Backend dependencies
#### Python 3.7

Follow instructions to install the latest version of python for your platform in the  [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the  [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the  `/backend`  directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the  `requirements.txt`  file.

##### Key Dependencies

-   [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

-   [SQLAlchemy](https://www.sqlalchemy.org/)  is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

-   [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)  is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided.
**Note:** you have to create the ``trivia`` database or it should exist prior to executing the command below.

From the backend folder, containing the ``trivia.psql`` file, in terminal run:
```
psql trivia < trivia.psql
```


## Running the server

### Backend server
From within the  `backend`  directory first ensure you are working using your created virtual environment (if you have created one).

To run the server, execute:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the  `FLASK_ENV`  variable to  `development`  will run the server in DEBUG mode.

### Frontend server
From within the `frontend` directory, run the following command:
```
npm start
```
Open [http://localhost:3000](http://localhost:3000/) to view it in the browser. The page will reload if you make edits.

## API Reference

### Getting Started

-   Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default,  `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
-   Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

`{
    "success": False,
    "error": 400,
    "message": "bad request"
}`

The API will return three error types when requests fail:

-   400: Bad Request
-   404: Resource Not Found
-   422: Not Processable

### Endpoints

#### GET /categories

 - General:
	 - Returns a a full list of question categories.
- Request parameters: `None`
- Sample response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
---
#### GET /questions?page=<page_number>

 - General:
	 - Returns a paginated list of all question disregarding categories. (10 questions per page)
- Request parameters: `None`
- Sample response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "total_questions": 19
}
```
---
#### POST /questions

 - General:
	 - Creates a new question using the provided (Question, Answer, Difficulty, Category).
- Request parameters: `Question`, `Answer`, `Difficulty`, `Category`
- Sample response:
```
{"message": "new question added successfully"}
```
---
#### Delete /questions/<question_id>

 - General:
	 - Deletes a question using the provided question id if it exists.
- Request parameters: `id`
- Sample response:
```
{"message": "successfully deleted question with id: 7"}
```
---
#### POST /questions/search

 - General:
	 - Searches all questions where a substring matches the search term, the search is case insensitive.
- Request parameters: `searchTerm`
- Sample response:
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "total_questions": 1
}
```
---
#### GET /categories/<int:id>/questions

 - General:
	 - Returns a list of all questions belonging to a specific category.
- Request parameters: `id`
- Sample response:
```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },  
  ],
  "success": true,
  "total_questions": 3
}
```
---
#### POST /quizzes

 - General:
	 - Returns a random question belonging to the provided category and not included in the previous questions list.
- Request parameters: `previous_questions`,`quiz_category`
- Sample response:
```    
{
	"question":
	{
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
}
```
---

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
