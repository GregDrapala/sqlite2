import os
from flask import Flask, jsonify, abort, make_response, request

from models import books, tasks, load_books_JSON_backup
from __main__ import app

@app.route("/api/books/book/", methods=["GET"])
def get_books_list():
    return jsonify(books.select_all())


@app.route("/api/books/task/", methods=["GET"])
def get_tasks_list():
    return jsonify(tasks.select_all())


@app.route("/api/books/book/<int:book_id>", methods=["GET"])
def get_single_book(book_id):
    book = books.select_where(id=book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/api/books/task/<int:id>", methods=["GET"])
def get_single_task(id):
    task = tasks.select_where(id=id)
    if not task:
        abort(404)
    return jsonify({"task": task})


@app.route("/api/books/task/<status>", methods=["GET"])
def get_task_by_status(status):
    task = tasks.select_task_by_status(status)
    if not task:
        abort(404)
    return jsonify({"task": task})


@app.route("/api/books/book/", methods=["POST"])
def create_episode():
    if not request.json or not 'title' in request.json:
        abort(400)

    data = request.json
    title = data.get('title')
    description = data.get('description')

    book = (title, description)
    books.add_book(book)
    return jsonify({'book': book}), 201


@app.route("/api/book/task/", methods=["POST"])
def create_task():
    if not request.json or not 'book_id' in request.json:
        abort(400)

    data = request.json
    book_id = data.get('book_id')
    task = data.get('task')
    task_description = data.get('task_description')
    status = data.get('status')
    read_date = data.get('read_date')
    

    taski = (book_id, task, task_description, status, read_date,)

    tasks.add_task(taski)
    return jsonify({'task': taski}), 201

@app.route("/api/books/book/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.select_where(id=book_id)
    book = book[0]
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'id' in data and not isinstance(data.get('id'), int),
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'author' in data and not isinstance(data.get('author'),str)
    ]):
        abort(400)

    title = data.get('title', book[1])
    description = data.get('description', book[2])
    author = data.get('author', book[3])
    
    books.update(id=book_id, title=title, description=description, author=author)
    return jsonify({'book': book})


@app.route("/api/books/task/<int:id>", methods=["PUT"])
def update_task(id):
    taski = tasks.select_where(id=id)
    taski = taski[0]
    if not taski:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'id' in data and not isinstance(data.get('id'), int),
        'book_id' in data and not isinstance(data.get('book_id'), int),
        'task' in data and not isinstance(data.get('task'), str),
        'task_description' in data and not isinstance(data.get('task_description'), str),
        'status' in data and not isinstance(data.get('status'), str),
        'read_date' in data and not isinstance(data.get('read_date'), str),
        ]):
        abort(400)

    book_id = data.get('book_id', taski[1])
    task = data.get('task', taski[2])
    task_description = data.get('task_description',taski[3])
    status = data.get('status', taski[4])
    read_date = data.get('read_date', taski[5])
    
    
    tasks.update(id=id, book_id=book_id, task=task, task_description=task_description, status=status, read_date=read_date,)
    return jsonify({'task': taski})


@app.route("/api/books/book/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result_1 = tasks.delete_where(book_id=book_id)
    result_2 = books.delete_where(id=book_id)
    if not result_1 and not result_2:
        abort(404)
    return jsonify({'result': [result_1, result_2]})


@app.route("/api/books/task/<int:id>", methods=['DELETE'])
def delete_task(id):
    result = tasks.delete_where(id=id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/books/delete/", methods=['DELETE'])
def delete_all():
    tasks.delete_all()
    books.delete_all()
    return jsonify({'result': "Tables books and tasks cleared"})


@app.route("/api/books/restore/", methods=["GET"])
def restore_all_from_JSON():
    result = load_books_JSON_backup()
    return jsonify({'result': result})