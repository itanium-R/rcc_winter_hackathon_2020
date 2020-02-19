# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request


api = Flask(__name__)


@api.route('/', methods=['POST'])
def voice_similarity():
    ## -----*---- 音声の類似度を算出 -----*----- ##
    print(request.form)

    result = {}
    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
