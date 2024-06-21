# API Development and Documentation Final Project

## Trivia App

This trivia app enables you to play and learn via an interactive quiz game where the user can enter questions for different quiz categories and randomly generate a quiz based on the entered data and the user earns points based on successful answers. It is built using the following technologies - 

1. Python
2. Flask
3. SQLAlchemy
4. CORS
5. TDD (Test Driven Design)
6. Pagination
7. Project and API documentation

# API Endpoints

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/api/v1.0/questions'`

- returns a list of questions,number of total questions, current category, categories
- Request Arguments: None
- Returns: An object with keys - , `success`, `questions` which contains list of paginated questions, `totalQuestions`, `categories`

```json
{     
    "current_category": "Geography",

    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },

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
    "total_questions": 20
    "success": true,
}
```

`DELETE '/api/v1.0/questions/{int: questions_id}'`

- Deletes the question corrosponding to the provided question id in the database
- Request Arguments: question_id
- Returns: An object with a single key, `questionDeleted`, that contains an object of `id: category_string` key: value pairs.

```json
{
    "success": true,
    "questionDeleted": 1
}
```

`POST '/api/v1.0/questions'`

- creates a new question entry in the database with the provided details in the request
- Request Arguments: question, answer, difficulty, category
- Returns: An object with a single key, `success`, that contains a boolean value.

```json
{
    "success": true
}
```

`POST '/api/v1.0/search'`

- returns a question or a list of questions which match the given input string. 
- Request Arguments: searchTerm
- Returns: An object with a two keys, `question`, that contains a list of questions that match the given value, `totalQuestions` returns the total number of questions that fit the match.

```json
{
  "questions": [
    {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
    }
  ], 
  "total_questions": 1,
  "success": true
}
```


`GET '/api/v1.0/categories/{int:category_id}/questions'`

- returns a question or a list of questions based on the provided category id in the request.
- Request Arguments: category_id
- Returns: An object with a three keys, `question`, that contains a list of questions that match the given value, `totalQuestions` returns the total number of questions that fit the match and `current_category`.

```json
{
  "questions": [
    {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
    }
  ], 
  "total_questions": 1,
  "success": true,
  "current_category": 4 
}
```

`POST '/api/v1.0/quizzes'`

- returns a question to the user to play. If the user provides a category in the request, the question is provdided from the same category.
- Request Arguments: previous_questions, quiz_category
- Returns: An object with a single key, `question` which is a randomly selected question from the given category and not in the given list of questions which have already been played.
```json
{
  "success": true,
  "question": "Who invented Peanut Butter?"
}
```