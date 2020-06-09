from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from passlib.hash import pbkdf2_sha256 as hash_password

from db import setup_db
from models import User

USERS_PER_PAGE = 10


# Paginates users (Shows only 10 users per page)
def paginate_users(request, users):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * USERS_PER_PAGE
    end = start + USERS_PER_PAGE

    formatted_users = [user.format() for user in users]
    paged_users = formatted_users[start:end]

    return paged_users


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Created a user
    @app.route('/users/create', methods=['POST'])
    def create_user():

        if request.method is not 'POST':
            abort(405)

        body = request.get_json()

        name = body.get('name')
        username = body.get('username')
        password = body.get('password')

        hashed_password = hash_password.hash(password)

        users = User.query.all()

        for u in users:
            if u.username == username:
                abort(409)

        try:

            user = User(name, username, hashed_password)
            user.insert()

            registered_user = User.query.filter(User.username == username).first()

            token = registered_user.generate_token()

            return jsonify({
                'success': True,
                'id': registered_user.id,
                'token': token
            })

        except:
            abort(422)

    # Logs in a user
    @app.route('/users/login', methods=['POST'])
    def login_user():

        if request.method is not 'POST':
            abort(405)

        body = request.get_json()

        username = body.get('username')
        password = body.get('password')

        hashed_password = hash_password.hash(password)

        users = User.query.all()

        try:

            for u in users:
                if u.username == username and u.password == hashed_password:

                    token = u.generate_token()

                    return jsonify({
                        'success': True,
                        'id': u.id,
                        'token': token
                    })
                else:
                    abort(401)

        except:
            abort(422)

    # Deletes a user by passing 'id' as a parameter
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):

        if request.method is not 'DELETE':
            abort(405)

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        try:
            user.delete()

            return jsonify({
                'success': True,
                'id': user.id
            })

        except:
            abort(422)

    # Updates a user info by passing 'id' as a parameter
    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def update_user(user_id):

        if request.method is not 'PATCH':
            abort(405)

        body = request.get_json()

        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        name = body.get('name')
        username = body.get('username')
        password = body.get('password')

        hashed_password = password

        try:

            user.name = name
            user.username = username
            user.password = hashed_password

            return jsonify({
                'success': True,
                'id': user.id,
            })

        except:
            abort(422)

    # Fetches a list of paged users based on the provided search term using a form
    @app.route('/users/search', methods=['POST'])
    def search_question():

        if request.method is not 'POST':
            abort(405)

        search_term = request.form['search_term']
        users = User.query.filter(User.username.ilike(f'%{search_term}%')).all()

        if not len(users):
            abort(404)

        paged_users = paginate_users(request, users)

        return jsonify({
            'success': True,
            'users': paged_users,
            'total_users': len(users),
        })

    # Error handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method_not_allowed"
        }), 405

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "conflict"
        }), 409

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
