from flask import Blueprint, jsonify, request
from . import db
from .models import Response

main = Blueprint('main', __name__)

@main.route('/add_response', methods=['POST'])

def add_response():
    response_data = request.get_json()
    
    new_response = Response(question=response_data['question'], response=response_data['response'], score=response_data['score'])

    
    db.session.add(new_response)
    db.session.commit()
    return 'Done', 201

@main.route('/responses')

def responses():
    response_list = Response.query.all()
    responses = []

    for response in response_list:
        responses.append({'question': response.question, 'response': response.response, 'score': response.score})

    return jsonify({'responses' : responses})