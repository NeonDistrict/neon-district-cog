from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from cakechat.api.response import get_response
from cakechat.api.utils import get_api_error_response, parse_dataset_param
from cakechat.config import EMOTIONS_TYPES, DEFAULT_CONDITION
from cakechat.utils.logger import get_logger
from cakechat.utils.profile import timer

import sys
sys.path.append('../')
from cog import cog

_logger = get_logger(__name__)

app = Flask(__name__, static_folder='build')

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["6 per second"],
)

## REACT
@app.route("/")
@app.route("/index.html")
def home():
    return app.send_static_file('index.html')

@app.route("/manifest.json")
def manifest():
    return app.send_static_file('manifest.json')

@app.route("/asset-manifest.json")
def assetmanifest():
    return app.send_static_file('asset-manifest.json')

@app.route("/service-worker.js")
def serviceworker():
    return app.send_static_file('service-worker.js')

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('build/vendor', path)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('build/static', path)
## REACT


@app.route('/cakechat_api/v1/actions/get_response', methods=['POST'])
@timer
def get_model_response():
    params = request.get_json()
    _logger.info('request params: %s' % params)

    try:
        dialog_context = parse_dataset_param(params, param_name='context')
    except KeyError as e:
        return get_api_error_response('Malformed request, no "%s" param was found' % str(e), 400, _logger)
    except ValueError as e:
        return get_api_error_response('Malformed request: %s' % str(e), 400, _logger)

    emotion = params.get('emotion', DEFAULT_CONDITION)
    if emotion not in EMOTIONS_TYPES:
        return get_api_error_response('Malformed request, emotion param "%s" is not in emotion list %s' %
                                      (emotion, list(EMOTIONS_TYPES)), 400, _logger)

    # ND Find Match
    fm_response, fm_emotion, fm_activity = cog.find_match(dialog_context[0])
    if fm_response is not None:
        return jsonify({'response': fm_response, 'emotion': fm_emotion, 'activity': fm_activity}), 200

    response = get_response(dialog_context, emotion)

    if not response:
        _logger.error('No response for context: %s; emotion "%s"' % (dialog_context, emotion))
        return jsonify({}), 200

    _logger.info('Given response: "%s" for context: %s; emotion "%s"' % (response, dialog_context, emotion))

    return jsonify({'response': response, 'emotion': emotion, 'activity': 'none'}), 200
