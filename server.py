from flask import Flask, request, Response, jsonify
import json , pika, jsonpickle, time
from datetime import datetime as dt
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route('/get_top_users',methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_top_users(userid):
    result = {}
    print(result)
    return jsonify(result[0])