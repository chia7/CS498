import json
from flask import Flask, request, jsonify

from collections import OrderedDict

from pyhive import hive


conn = hive.Connection(host="localhost", port=10000, database='default')
cursor = conn.cursor()


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(success=True)


@app.route('/results', methods=['POST'])
def results():

    body = json.loads(request.data)

    if body['term'] is None:
        return jsonify(error="parameter `term` not found")

    query = """SELECT clicks FROM webSearch WHERE term = 'searchTerm: ‘{}’'""".format(body['term'])

    # SELECT clicks FROM webSearch WHERE term = 'searchTerm: ‘Portland’';

    cursor.execute(query)
    results = cursor.fetchall()

    if results is None or len(results) == 0:
        return jsonify({'results' : {}})

    results = json.loads(results[0][0])
    results = OrderedDict({k.strip(): v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)})
    resp = {'results' : results}

    return json.dumps(resp)


@app.route('/trends', methods=['POST'])
def trends():

    body = json.loads(request.data)

    if body['term'] is None:
        return jsonify(error="parameter `term` not found")

    query = """SELECT SUM(CNT) FROM webSearch LATERAL VIEW EXPLODE(clicks) clicks_table AS url, CNT WHERE term = 'searchTerm: ‘{}’'""".format(body['term'])

    # SELECT SUM(CNT) FROM webSearch LATERAL VIEW EXPLODE(clicks) clicks_table AS url, CNT WHERE term = 'searchTerm: ‘Portland’';

    cursor.execute(query)
    results = cursor.fetchall()
    
    if results is None or len(results) == 0:
        return jsonify({'clicks' : 0})

    resp = {'clicks' : results[0][0]}

    return jsonify(resp)


@app.route('/popularity', methods=['POST'])
def popularity():

    body = json.loads(request.data)

    if body['url'] is None:
        return jsonify(error="parameter `url` not found")

    query = """SELECT SUM(CNT) FROM webSearch LATERAL VIEW EXPLODE(clicks) clicks_table AS url, CNT WHERE url = '{}'""".format(body['url'])

    # SELECT SUM(CNT) FROM webSearch LATERAL VIEW EXPLODE(clicks) clicks_table AS url, CNT WHERE url = 'en.wikipedia.org';

    cursor.execute(query)
    resp = {'clicks' : cursor.fetchall()[0][0]}

    return jsonify(resp)


@app.route('/getBestTerms', methods=['POST'])
def getBestTermsgetBestTerms():

    body = json.loads(request.data)

    if body['website'] is None:
        return jsonify(error="parameter `website` not found")

    query = """SELECT term, CNT FROM webSearch LATERAL VIEW EXPLODE(clicks) clicks_table AS url, CNT WHERE url = '{}' ORDER BY CNT DESC""".format(body['website'])

    # SELECT term, CNT FROM webSearch LATERAL VIEW EXPLODE(clicks) clicks_table AS url, CNT WHERE url = 'en.wikipedia.org' ORDER BY CNT DESC;

    cursor.execute(query)
    result = cursor.fetchall()

    totalClicks = 0
    resp = {'best_terms' : []}

    for row in result:
        totalClicks += row[1]

    for row in result:
        if row[1] / totalClicks >= 0.05:
            resp['best_terms'].append(row[0][13:-1])

    return jsonify(resp)


app.run(debug=True, host='0.0.0.0', port=80)


# curl -X POST -H "Content-Type: application/json" -d '{"term": "searchTerm: ‘Portland’"}' http://34.132.171.13/results
# curl -X POST -H "Content-Type: application/json" -d '{"term": "Portland Computer"}' http://34.132.171.13/results