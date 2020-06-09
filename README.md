# Registry API

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension to handle cross origin requests

## Database Setup
The databse should already be created

To populate it, excute:
    
```bash
createdb users
flask db migrate 
```

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py`  will find the application

## Endpoints
```

POST '/users/create'

- Creates a user by getting (name, username, password) from a frontend
- Returns the newly created user's id and a token
{ 
    'success': True,
    'id': 1,
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsIm5hbWUiOiJOYW1lIn0.fQiFAVMvXNxpqa44zWjv_U2Ay_RgGMCnoXMo1ft7gZ8'
}

POST '/users/login'

- Logs in a user by getting (username, password) from a frontend
- Returns the newly logged in user's id and a token
{ 
    'success': True,
    'id': 1,
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsIm5hbWUiOiJOYW1lIn0.fQiFAVMvXNxpqa44zWjv_U2Ay_RgGMCnoXMo1ft7gZ8'
}


DELETE '/users/1'

- Deletes a user by getting passing user's id as a parameter
- Returns the deleted user's id
{ 
    'success': True,
    'id': 1
}

    
PATCH '/users/1'

- Update a user by getting (name, username, password) from a frontend
- Returns the updated user's id
{ 
    'success': True,
    'id': 1
}

POST '/users/search'
- Searches for users by passing a username in a frontend form
- Returns: a list of users filtered by the provided search term which is paged (10 users per page) and the total users 


{
    'success' : True,
    'users': [
                    { 
                        'id' : 1,
                        'name' : "John Doe",
                        'username' : "john_doe"
                    } 
                    { 
                        'id' : 2,
                        'question' : "Mark",
                        'username' : "mark20"
                    } 
                ]
    'total_users': 2,
}

```

### Errors

##### Supported Http Status Codes:
- 200 : Request has been fulfilled
- 201 : Entity has been created
- 401 : Not authorized
- 404 : Resource not found
- 422 : Wrong info provided
- 405 : Method not allowed
- 409 : Conflict found

## Testing
To run the tests, run
```
createdb users_test
python tests.py
```
