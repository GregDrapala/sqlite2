import os
from flask import Flask, jsonify, abort, make_response, request

from models import books, tasks, load_books_JSON_backup


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"



@app.errorhandler(400)
def validate_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def find_book(error):
    return make_response(jsonify({'error': 'Episode or task not found', 'status_code': 404}), 404)



import views




if __name__ == "__main__":

    books.execute_sql()
    tasks.execute_sql()

    app.run(debug=True)