# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 13:29:47 2018

@author: admin
"""
from flask import Flask , jsonify, abort, make_response
app = Flask(__name__)
articles = [
    {
        'id': 1,
        'title': 'the way to python',
        'content': 'tuple, list, dict'
    },
    {
        'id': 2,
        'title': 'the way to REST',
        'content': 'GET, POST, PUT'
    }
]
@app.route('/blog/api/articles', methods=['GET'])
def get_articles():
    """ 获取所有文章列表 """
    return jsonify({'articles': articles})
@app.route('/blog/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """ 获取某篇文章 """
    article = filter(lambda a: a['id'] == article_id, articles)
    if len(article) == 0:
        abort(404)
    return jsonify({'article': article[0]})
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5632, debug=True)