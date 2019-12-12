from flask import Flask, request, Response, jsonify
import json , time
from datetime import datetime as dt
from flask_cors import CORS, cross_origin
import top_users,pagerank_users

print("we are going to start the server in 2-3 min")
# allowing different host to make call
app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

cache_result = {}
top_persons_count = 500

cache_popular_person = {}
popular_persons_count = 500

#import top users class
tp = top_users.TopUser()

#import page ranked users class
pr = pagerank_users.PageRank()

# error handling https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.after_request
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def after_request(response):
    """ Logging after every request. """
    log = "{} [{}] {} {} {} {} {} ".format(
        request.remote_addr,
        dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
        request.method,
        request.path,
        request.scheme,
        response.status,
        response.content_length,)
    myTime = int(time.time())
    response_log = {
        myTime : log
    }
    print(response_log)
    return response

@app.route('/get_popular_users',methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_popular_users():
    result = {}
    global popular_persons_count,cache_popular_person
    popular_persons_count -= 1
    # check for refreshing top users for every 500 calls  
    if popular_persons_count <= 0 :
        cache_popular_person = {}
        popular_persons_count = 500
    if len(cache_popular_person) == 0:
        mentions,users = pr.parse_tweets()
        graph_structure = pr.generate_graph_structure(mentions,users)
        result = pr.calculate_pagerank(graph_structure)
        cache_popular_person = result
    response = {
        "result":cache_popular_person
    }
    print(cache_result)
    return jsonify(response)


@app.route('/get_top_users',methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_top_users():
    result = {}
    global top_persons_count,cache_result
    top_persons_count -= 1
    # check for refreshing top users for every 500 calls  
    if top_persons_count <= 0 :
        cache_result = {}
        top_persons_count = 500
    if len(cache_result) == 0:
        result = tp.get_top_user_list()
        cache_result = result
    response = {
        "result":cache_result
    }
    print(cache_result)
    return jsonify(response)


# start flask app
print("we are going to start the server in 2-3 min")
app.run(host="0.0.0.0", port=5000)