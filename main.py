from flask import Flask, jsonify, request
from werkzeug.urls import url_encode
import pymongo

from scrapy_theguardian.scrapy_theguardian.settings import MONGO_DATABASE, MONGO_URI

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value
    
    return '{}?{}'.format(request.base_url, url_encode(args))

@app.route('/article', methods=['GET'])
def get_articles():
    articles = db.articles
    output = []
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    keywords = request.args.get('keywords', '').split(',')
    query = {} if not keywords else {'keywords': {'$in': keywords }}
    for article in articles.find(query).skip(skip).limit(limit):
        del article['_id']
        output.append(article)
    result = {
        'count': len(output),
        'next_page': modify_query(skip=skip+limit, limit=limit) if len(output) == limit else '',
        'result' : output
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
